#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Relevé SERPmantics de toutes les pages suivies (gratuit : aucun guide créé).

Pour chaque guide du compte SERPmantics (requête × langue × moteur), retrouve la page
de pages.json qui vise cette requête, mesure son contenu actuel (balise <main>, comme
`serp.py score`) et enregistre la mesure dans le guide : la liste des guides de
SERPmantics affiche ensuite les mêmes notes.

    python3 _tools/seo_pipeline/releve.py [--sortie DOSSIER] [--sans-enregistrer] [--reprendre]

Écrit DOSSIER/releve.json (tout) et DOSSIER/releve.csv (une ligne par page et par
moteur). --reprendre garde les mesures déjà faites dans releve.json.
Clé : SERPMANTICS_API_KEY (variable d'environnement ou ~/.seo_pipeline.env).
Premier relevé : 04/10/2026, après la pose d'une photo et d'une maquette sur chaque page.
"""
import csv
import datetime
import json
import os
import re
import sys
import time

P = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, P)
import serp  # noqa: E402

NOMS = {'GOOGLE': 'Google', 'GOOGLE_AI_OVERVIEW_CITATIONS': 'AI Overview', 'CHATGPT_CITATIONS': 'ChatGPT',
        'GEMINI_CITATIONS': 'Gemini', 'PERPLEXITY_CITATIONS': 'Perplexity', 'CLAUDE_CITATIONS': 'Claude'}
ORDRE = ['Google', 'AI Overview', 'ChatGPT', 'Gemini', 'Perplexity', 'Claude']
STRUCT = ['length', 'images', 'headings', 'paragraphs', 'links', 'lists', 'tables', 'videos']


def charger_cle():
    if os.environ.get('SERPMANTICS_API_KEY'):
        return
    f = os.path.expanduser('~/.seo_pipeline.env')
    if os.path.exists(f):
        for ligne in open(f, encoding='utf-8'):
            m = re.match(r'\s*(?:export\s+)?([A-Z_]+)\s*=\s*(.*)$', ligne)
            if m and m.group(1) == 'SERPMANTICS_API_KEY':
                os.environ['SERPMANTICS_API_KEY'] = m.group(2).strip().strip('"\'')


def nom_moteur(source):
    s = (source or 'GOOGLE').upper()
    if s in NOMS:
        return NOMS[s]
    nom = s.replace('_CITATIONS', '').replace('_', ' ').title().replace('Chatgpt', 'ChatGPT')
    return nom if s.endswith('_CITATIONS') else nom + ' (réponse)'  # guide bâti sur le texte de la réponse IA


def lister_guides():
    tous = []
    for page in range(1, 51):
        code, j = serp.api('GET', '/guides', {'page': page, 'pageSize': 100})
        if code != 200:
            sys.exit(f'liste des guides : HTTP {code} {str(j)[:300]}')
        lot = j.get('guides') or []
        tous += lot
        if len(lot) < 100:
            break
    return tous


def score_affiche(g):
    """Note que la liste SERPmantics affichait avant ce relevé : dernière mesure enregistrée."""
    ca = g.get('contentAnalysis') or {}
    if isinstance(ca.get('score'), (int, float)):
        return ca['score']
    for k in ('score', 'contentScore', 'lastScore', 'editorScore'):
        if isinstance(g.get(k), (int, float)):
            return g[k]
    for k, v in g.items():
        if 'score' in k.lower() and isinstance(v, (int, float)):
            return v
    return None


def contenu(e):
    """<main> de la page ; pour l'accueil SPA, le repli sans JavaScript (seul HTML statique)."""
    if e['fichier'] == 'index.html':
        s = open(os.path.join(serp.REPO, 'index.html'), encoding='utf-8').read()
        m = re.search(r'(?is)<noscript[^>]*id="fallback"[^>]*>(.*?)</noscript>', s)
        if m:
            c = re.sub(r'(?s)<!--.*?-->', ' ', m.group(1))
            return re.sub(r'\s+', ' ', c).strip()
    return serp.contenu_page(e)


def associer(guides, pages):
    """{slug: {moteur: guide le plus récent non expiré}}, guides sans page, guides expirés."""
    par_page, orphelins = {}, []
    for g in guides:
        q, lang = serp.norm(g.get('query')), (g.get('lang') or '').lower()
        cible = None
        for e in pages:
            if serp.norm(e['requete']) != q:
                continue
            codes = serp.lang_codes(e)
            if lang in codes or lang[:2] == e['lang'][:2]:
                cible = e
                if lang in codes:
                    break
        if not cible:
            sec = [e['slug'] for e in pages if q in {serp.norm(x) for x in e.get('requetes_secondaires') or []}]
            orphelins.append({'requete': g.get('query'), 'lang': lang, 'moteur': nom_moteur(g.get('source')),
                              'id': g.get('id'), 'note_affichee': score_affiche(g),
                              'expire': bool(g.get('expired')), 'requete_secondaire_de': sec})
            continue
        m = nom_moteur(g.get('source'))
        actuel = par_page.setdefault(cible['slug'], {}).get(m)
        rang = (not g.get('expired'), g.get('createdAt') or '')
        if actuel is None or rang > (not actuel.get('expired'), actuel.get('createdAt') or ''):
            par_page[cible['slug']][m] = g
    return par_page, orphelins


def mesurer(e, g, txt, enregistrer):
    ca0 = g.get('contentAnalysis') or {}
    res = {'source': g.get('source'), 'guide_id': g.get('id'), 'guide_cree': (g.get('createdAt') or '')[:10],
           'avant': score_affiche(g), 'avant_le': (ca0.get('updatedAt') or '')[:16].replace('T', ' '),
           'avant_images': (ca0.get('structure') or {}).get('images')}
    if g.get('expired'):
        res['erreur'] = 'guide expiré'
        return res
    code, jg = serp.api('GET', '/guide', {'id': g['id']})
    if code != 200 or not jg.get('guide'):
        res['erreur'] = f'guide illisible (HTTP {code})'
        return res
    time.sleep(0.5)
    code, js = serp.api('POST', '/score', corps={'guideId': g['id'], 'content': txt, 'saveToGuide': enregistrer,
                                                 'scoreProgressive': False, 'includeEmbedding': False})
    if code != 200 or not js.get('success', True):
        res['erreur'] = f'mesure refusée (HTTP {code}) {str(js)[:200]}'
        return res
    ca = js.get('contentAnalysis') or {}
    st_g = (jg['guide'].get('guide') or {}).get('structure') or {}
    st_p = ca.get('structure') or {}
    res['maintenant'] = ca.get('score')
    res['structure'] = {k: {'page': st_p.get(k), 'de': (st_g.get(k) or {}).get('from'), 'a': (st_g.get(k) or {}).get('to')}
                        for k in STRUCT if k in st_p or k in st_g}
    a = serp.analyser(jg, js, txt)
    res['sous_fourchette'] = a['sous_fourchette'][:15]
    res['n_sous_fourchette'] = len(a['sous_fourchette'])
    res['au_dessus'] = a['au_dessus_fourchette'][:10]
    res['a_eviter'] = a['a_eviter_presentes']
    return res


def couleur(n):
    if not isinstance(n, (int, float)):
        return ''
    return 'gris' if n > 100 else 'vert' if n >= serp.seuil_vert() else 'orange' if n >= serp.seuil_rouge() else 'rouge'


def main(a):
    charger_cle()
    sortie = os.path.abspath(a[a.index('--sortie') + 1]) if '--sortie' in a else os.path.join(serp.RUNS, '_releve')
    os.makedirs(sortie, exist_ok=True)
    enregistrer = '--sans-enregistrer' not in a
    fjson = os.path.join(sortie, 'releve.json')
    deja = {}
    if '--reprendre' in a and os.path.exists(fjson):
        for p in json.load(open(fjson, encoding='utf-8')).get('pages', []):
            for m, r in (p.get('mesures') or {}).items():
                if 'maintenant' in r:
                    deja[r['guide_id']] = r
    pages = serp.cfg()['pages']
    guides = lister_guides()
    serp.log(f'{len(guides)} guides dans le compte SERPmantics')
    par_page, orphelins = associer(guides, pages)
    rapport = {'date': datetime.datetime.now().strftime('%Y-%m-%d %H:%M'), 'enregistre_dans_les_guides': enregistrer,
               'seuils': {'vert': serp.seuil_vert(), 'rouge': serp.seuil_rouge()}, 'pages': [],
               'guides_sans_page': orphelins}
    for e in pages:
        fichier = os.path.join(serp.REPO, e['fichier'])
        ligne = {k: e.get(k) for k in ('slug', 'url', 'lang', 'requete', 'fichier', 'statut', 'mode', 'objectif_geo')}
        ligne['geo_hors_cible'] = e.get('geo_hors_cible') or []
        ligne['mesures'] = {}
        if not os.path.exists(fichier):
            ligne['erreur'] = 'fichier absent'
            rapport['pages'].append(ligne)
            continue
        txt = contenu(e)
        ligne['images_html'] = len(re.findall(r'(?i)<img\b', txt))
        for m, g in sorted((par_page.get(e['slug']) or {}).items(), key=lambda x: (ORDRE + [x[0]]).index(x[0])):
            if g.get('id') in deja:
                ligne['mesures'][m] = deja[g['id']]
                continue
            serp.log(f"{e['slug']} — {m}")
            ligne['mesures'][m] = mesurer(e, g, txt, enregistrer)
            time.sleep(0.5)
        rapport['pages'].append(ligne)
        json.dump(rapport, open(fjson, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    with open(os.path.join(sortie, 'releve.csv'), 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f, delimiter=';')
        w.writerow(['page', 'url', 'langue', 'requête', 'moteur', 'note avant', 'mesurée le', 'note maintenant', 'couleur',
                    'images page', 'images attendues', 'mots page', 'mots attendus', 'expressions sous la fourchette',
                    'guide créé le', 'guide', 'erreur'])
        for p in rapport['pages']:
            for m, r in p['mesures'].items():
                st = r.get('structure') or {}
                img, mots = st.get('images') or {}, st.get('length') or {}
                w.writerow([p['slug'], p['url'], p['lang'], p['requete'], m, r.get('avant'), r.get('avant_le'), r.get('maintenant'),
                            couleur(r.get('maintenant')), img.get('page'),
                            f"{img.get('de')}–{img.get('a')}" if img else '', mots.get('page'),
                            f"{mots.get('de')}–{mots.get('a')}" if mots else '', r.get('n_sous_fourchette'),
                            r.get('guide_cree'), r.get('guide_id'), r.get('erreur', '')])
    json.dump(rapport, open(fjson, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    n = sum(len(p['mesures']) for p in rapport['pages'])
    sans = [p['slug'] for p in rapport['pages'] if not p['mesures']]
    print(f"{n} mesures sur {len(rapport['pages'])} pages ; pages sans guide : {', '.join(sans) or 'aucune'} ; "
          f"guides sans page : {len(orphelins)} ; écrit dans {sortie}")


if __name__ == '__main__':
    main(sys.argv[1:])
