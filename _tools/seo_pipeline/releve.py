#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Relevé SERPmantics de toutes les pages du site.

Pages : celles du circuit (pages.json) et toutes les autres (requetes_site.json, avec la
requête que vise chacune). Pour chaque page qui a des guides (requête × langue × moteur),
mesure son contenu actuel (balise <main>, comme `serp.py score`) et enregistre la mesure
dans le guide : la liste des guides de SERPmantics affiche ensuite les mêmes notes.
Mesurer est gratuit. Un guide sert à toutes les pages qui visent sa requête ; la mesure
n'est enregistrée que pour la première (celle de pages.json en priorité).

    python3 _tools/seo_pipeline/releve.py [--sortie DOSSIER] [--sans-enregistrer] [--reprendre]
    python3 _tools/seo_pipeline/releve.py creer [--source google] [--phase 1] [--max N] [--reserve 6] [--lot 5] [--essai]

`creer` crée les guides manquants d'un moteur pour les pages de la phase demandée, dans
la limite du quota API de SERPmantics (200 guides par mois, crédits illimités ou non)
moins une réserve laissée au circuit. --essai : liste seulement.

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
SITE = os.path.join(P, 'requetes_site.json')
# Codes que SERPmantics refuse (« Unsupported language code », 04/10/2026) : on passe au suivant
LANGUES_REFUSEES = {'en-es', 'ca-es'}


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
        if code == 404 and tous:  # total multiple de 100 : la page après la dernière répond 404 (08/10/2026)
            break
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


def toutes_pages():
    """Pages de pages.json (phase 1 sauf mention dans requetes_site.json), puis les autres."""
    try:
        site = json.load(open(SITE, encoding='utf-8'))
    except FileNotFoundError:
        site = {}
    phases = site.get('phase_pages_suivies') or {}
    out, vues = [], set()
    for e in serp.cfg()['pages']:
        out.append(dict(e, phase=phases.get(e['slug'], 1), suivie=True))
        vues.add(e['url'].rstrip('/'))
    for e in site.get('pages') or []:
        if e['url'].rstrip('/') not in vues and e.get('fichier'):
            out.append(dict({'statut': 'releve', 'mode': '-'}, **e, suivie=False))
    return out


def associer(guides, pages):
    """{slug: {moteur: guide}} et guides sans page. Pour chaque moteur : guide non expiré, dans
    la langue préférée de la page, le plus récent. Un guide sert à toutes les pages de sa requête."""
    par_page, utilises = {}, set()
    for e in pages:
        q = serp.norm(e.get('requete'))
        if not q:
            continue
        codes = serp.lang_codes(e)
        choix = {}
        for g in guides:
            if serp.norm(g.get('query')) != q:
                continue
            lang = (g.get('lang') or '').lower()
            if lang in codes:
                pref = codes.index(lang)
            elif lang[:2] == e['lang'][:2]:
                pref = len(codes)
            else:
                continue
            m = nom_moteur(g.get('source'))
            rang = (not g.get('expired'), -pref, g.get('createdAt') or '')
            if m not in choix or rang > choix[m][0]:
                choix[m] = (rang, g)
        if choix:
            par_page[e['slug']] = {m: g for m, (_r, g) in choix.items()}
            utilises.update(g.get('id') for _r, g in choix.values())
    orphelins = [{'requete': g.get('query'), 'lang': (g.get('lang') or '').lower(), 'moteur': nom_moteur(g.get('source')),
                  'id': g.get('id'), 'note_affichee': score_affiche(g), 'expire': bool(g.get('expired'))}
                 for g in guides if g.get('id') not in utilises]
    return par_page, orphelins


def quota():
    """Quota API de création de guides : {limit, used, remaining, period_end…} (lecture gratuite)."""
    code, j = serp.api('GET', '/usage')
    d = j.get('data') if code == 200 and isinstance(j, dict) else None
    if not d:
        try:
            _i, sid = serp.mcp_appel('initialize', {'protocolVersion': '2025-06-18', 'capabilities': {},
                                                    'clientInfo': {'name': 'releve', 'version': '1'}})
            r, _ = serp.mcp_appel('tools/call', {'name': 'get_usage', 'arguments': {}}, sid, ident=2)
            d = json.loads(r['result']['content'][0]['text'])['data']
        except Exception as e:
            serp.log(f'quota illisible : {e}')
    return d or {}


def cmd_creer(a, sortie):
    source = a[a.index('--source') + 1] if '--source' in a else 'google'
    phase = int(a[a.index('--phase') + 1]) if '--phase' in a else 1
    maxi = int(a[a.index('--max') + 1]) if '--max' in a else 10 ** 6
    reserve = int(a[a.index('--reserve') + 1]) if '--reserve' in a else 6
    moteur = nom_moteur(source)
    pages = [e for e in toutes_pages() if e.get('phase', 1) <= phase and e.get('requete')]
    par_page, _ = associer(lister_guides(), pages)
    manquants = {}
    for e in pages:
        if moteur in par_page.get(e['slug'], {}):
            continue
        lang = next((c for c in serp.lang_codes(e) if c not in LANGUES_REFUSEES), serp.lang_codes(e)[0])
        x = manquants.setdefault((lang, serp.norm(e['requete'])), {'requete': e['requete'], 'lang': lang, 'pages': []})
        x['pages'].append(e['slug'])
    q = quota()
    reste = q.get('remaining') if isinstance(q.get('remaining'), int) else 0
    liste = list(manquants.values())[:max(0, min(maxi, reste - reserve))]
    print(f"{len(manquants)} guides {moteur} manquants (phase ≤ {phase}) ; quota restant {reste} jusqu'au "
          f"{str(q.get('period_end'))[:10]}, réserve {reserve} : {len(liste)} à créer")
    for x in liste:
        print(f"  {x['lang']}  {x['requete']}  ← {', '.join(x['pages'])}")
    if '--essai' in a or not liste:
        return
    faits = []
    par_lang = {}
    for x in liste:
        par_lang.setdefault(x['lang'], []).append(x)
    taille = int(a[a.index('--lot') + 1]) if '--lot' in a else 5
    for lang, xs in par_lang.items():
        for i in range(0, len(xs), taille):
            lot = xs[i:i + taille]
            for essai in range(8):  # 429 : SERPmantics limite le rythme (04/10 : refus après 20 guides en 4 s)
                code, j = serp.api('POST', '/guides', corps={'queries': [x['requete'] for x in lot], 'lang': lang, 'source': source})
                serp.log(f'création {lang} ({len(lot)} requêtes) : HTTP {code}')
                if code != 429:
                    break
                serp.log(f'trop de demandes : pause de {60 * (essai + 1)} s ({json.dumps(j, ensure_ascii=False)[:200]})')
                time.sleep(60 * (essai + 1))
            crees = {serp.norm(g.get('query')): g.get('id') for g in (j.get('guides') or [])}
            def requetes(cle):
                return {serp.norm(str(v.get('query') if isinstance(v, dict) else v)) for v in (j.get(cle) or [])}
            echecs, inconnus = requetes('guidesFailed'), requetes('guidesUnknown')
            for x in lot:
                n = serp.norm(x['requete'])
                x['id'] = crees.get(n)
                x['etat'] = ('créé' if x['id'] else 'inconnu : ne pas recréer, chercher dans la liste' if n in inconnus
                             else 'refusé' if n in echecs or 400 <= code < 500 else 'absent de la réponse')
                if not x['id']:
                    x['reponse'] = json.dumps(j, ensure_ascii=False)[:400]
                faits.append(x)
            time.sleep(20)
    for x in faits:
        if x.get('id'):
            x['pret'], _j = serp.attendre_guide(x['id'], max_min=30)
            serp.log(f"{x['requete']} ({x['lang']}) : {x['pret']}")
    os.makedirs(sortie, exist_ok=True)
    json.dump(faits, open(os.path.join(sortie, 'creations.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    from collections import Counter
    print('création :', dict(Counter(x['etat'] for x in faits)), '| prêts :', dict(Counter(x.get('pret') for x in faits if x.get('id'))))


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
                    deja[(p['slug'], r['guide_id'])] = r
    pages = toutes_pages()
    guides = lister_guides()
    serp.log(f'{len(guides)} guides dans le compte SERPmantics')
    par_page, orphelins = associer(guides, pages)
    rapport = {'date': datetime.datetime.now().strftime('%Y-%m-%d %H:%M'), 'enregistre_dans_les_guides': enregistrer,
               'seuils': {'vert': serp.seuil_vert(), 'rouge': serp.seuil_rouge()}, 'pages': [],
               'guides_sans_page': orphelins}
    enregistres = set()  # guide partagé par plusieurs pages : on n'enregistre que la première mesure
    for e in pages:
        fichier = os.path.join(serp.REPO, e['fichier'])
        ligne = {k: e.get(k) for k in ('slug', 'url', 'lang', 'requete', 'fichier', 'statut', 'mode', 'objectif_geo',
                                       'phase', 'suivie', 'origine')}
        ligne['geo_hors_cible'] = e.get('geo_hors_cible') or []
        ligne['mesures'] = {}
        if not os.path.exists(fichier):
            ligne['erreur'] = 'fichier absent'
            rapport['pages'].append(ligne)
            continue
        txt = contenu(e)
        ligne['images_html'] = len(re.findall(r'(?i)<img\b', txt))
        for m, g in sorted((par_page.get(e['slug']) or {}).items(), key=lambda x: (ORDRE + [x[0]]).index(x[0])):
            if (e['slug'], g.get('id')) in deja:
                ligne['mesures'][m] = deja[(e['slug'], g['id'])]
                enregistres.add(g.get('id'))
                continue
            serp.log(f"{e['slug']} — {m}")
            ligne['mesures'][m] = mesurer(e, g, txt, enregistrer and g.get('id') not in enregistres)
            enregistres.add(g.get('id'))
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
    print(f"{n} mesures sur {len(rapport['pages']) - len(sans)} pages ; {len(sans)} pages sans guide"
          + (f" ({', '.join(sans)})" if len(sans) <= 15 else '') + f" ; guides sans page : {len(orphelins)} ; écrit dans {sortie}")


if __name__ == '__main__':
    if sys.argv[1:2] == ['creer']:
        charger_cle()
        a = sys.argv[2:]
        cmd_creer(a, os.path.abspath(a[a.index('--sortie') + 1]) if '--sortie' in a else os.path.join(serp.RUNS, '_releve'))
    else:
        main(sys.argv[1:])
