#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Aide du circuit SEO/GEO : consignes des agents, état, résumé de PR.

    python3 _tools/seo_pipeline/pipeline.py next [--n 3]         slugs à traiter
    python3 _tools/seo_pipeline/pipeline.py field <slug> <champ>  un champ de pages.json
    python3 _tools/seo_pipeline/pipeline.py a-affiner [--n 50]      pages publiées à contrôler (affinage)
    python3 _tools/seo_pipeline/pipeline.py controle <slug> <vert|a_affiner>
    python3 _tools/seo_pipeline/pipeline.py sync                 état des PR relu sur GitHub (gh)
    python3 _tools/seo_pipeline/pipeline.py prompt writer|fix|affine|review <slug>
    python3 _tools/seo_pipeline/pipeline.py extract-review <slug> <sortie_claude.json>
    python3 _tools/seo_pipeline/pipeline.py verdict <slug>        approuver|reviser|rejeter|absent
    python3 _tools/seo_pipeline/pipeline.py summary <slug>        corps de la PR (markdown)
    python3 _tools/seo_pipeline/pipeline.py state <slug> <statut> [note]
    python3 _tools/seo_pipeline/pipeline.py status               tableau de l'état local
"""
import json, os, re, subprocess, sys, datetime

P = os.path.dirname(os.path.abspath(__file__))
RUNS = os.path.join(P, 'runs')
STATE = os.path.join(RUNS, 'state.json')


def cfg():
    return json.load(open(os.path.join(P, 'pages.json'), encoding='utf-8'))


def entree(slug):
    for p in cfg()['pages']:
        if p['slug'] == slug:
            return p
    sys.exit(f'slug inconnu : {slug}')


def state():
    try:
        return json.load(open(STATE, encoding='utf-8'))
    except Exception:
        return {}


def lire_json(slug, nom):
    try:
        return json.load(open(os.path.join(RUNS, slug, nom), encoding='utf-8'))
    except Exception:
        return None


def cmd_next(n):
    st = state()
    todo = [p for p in cfg()['pages']
            if p['statut'] == 'a_faire' and p['mode'] != 'manuel' and not p.get('requete_a_confirmer')
            and st.get(p['slug'], {}).get('statut') not in ('publie', 'pr_ouverte', 'a_revoir', 'bloque', 'en_cours')]
    todo.sort(key=lambda p: (p['priorite'], p['slug']))
    print('\n'.join(p['slug'] for p in todo[:n]))


BLOQUANTS = ('en_cours', 'pr_ouverte', 'a_revoir')


def cmd_a_affiner(n):
    """Pages publiées (pages.json « fait » ou fusionnées par le circuit), hors pages en
    cours ou en attente, les moins récemment contrôlées d'abord."""
    st = state()
    ctl = st.get('_controles', {})
    liste = []
    for p in cfg()['pages']:
        s_ = st.get(p['slug'], {}).get('statut')
        if p['mode'] == 'manuel' or s_ in BLOQUANTS:
            continue
        if p['statut'] == 'fait' or s_ == 'publie':
            liste.append((ctl.get(p['slug'], {}).get('date', ''), p['priorite'], p['slug']))
    liste.sort()
    print('\n'.join(x[2] for x in liste[:n]))


def cmd_controle(slug, resultat):
    os.makedirs(RUNS, exist_ok=True)
    st = state()
    st.setdefault('_controles', {})[slug] = {
        'resultat': resultat, 'date': datetime.datetime.now().isoformat(timespec='minutes')}
    json.dump(st, open(STATE, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)


def cmd_sync():
    """Relit sur GitHub l'état des PR ouvertes par le circuit : fusionnée → publie,
    fermée sans fusion → ferme (la page redevient disponible)."""
    st = state()
    change = False
    for slug, v in list(st.items()):
        if slug.startswith('_') or not isinstance(v, dict) or v.get('statut') not in ('pr_ouverte', 'a_revoir'):
            continue
        m = re.search(r'https://github\.com/\S+/pull/\d+', v.get('note', ''))
        if not m:
            continue
        try:
            etat = subprocess.run(['gh', 'pr', 'view', m.group(0), '--json', 'state', '-q', '.state'],
                                  capture_output=True, text=True, timeout=60).stdout.strip()
        except Exception:
            continue
        nouveau = {'MERGED': 'publie', 'CLOSED': 'ferme'}.get(etat)
        if nouveau:
            v['statut'] = nouveau
            print(f'{slug} : {etat} → {nouveau}')
            change = True
    if change:
        json.dump(st, open(STATE, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)


ENTETE = """Tu travailles dans le dépôt du site webautonomos.es (répertoire courant).
Page à traiter (entrée de _tools/seo_pipeline/pages.json) :

```json
{entree}
```

Langue du guide SERPmantics : {langue_guide}.
Dossier de travail : _tools/seo_pipeline/runs/{slug}/
"""


def prompt_writer(slug, fix=False):
    e = entree(slug)
    txt = ENTETE.format(entree=json.dumps(e, ensure_ascii=False, indent=2), slug=slug,
                        langue_guide=cfg()['langues_serpmantics'].get(e['lang'], e['lang']))
    if fix == 'affine':
        return txt + """
Tu es l'agent RÉDACTEUR, en AFFINAGE. Cette page est déjà publiée et a été
approuvée : elle n'atteint simplement pas ses seuils SERPmantics. Lis d'abord, en entier :
1. _tools/seo_pipeline/VERITE.md
2. _tools/seo_pipeline/REGLES_REDACTEUR.md (sections 1 à 5, dont « Affinage »)
3. _tools/seo_pipeline/runs/{slug}/score_controle.json (mesure de cette nuit)
4. _tools/seo_pipeline/runs/{slug}/guides.json puis les guide_*.md
Objectif : score Google ≥ {seuil} ; si l'entrée a "objectif_geo": "vert", score GEO
moyen ≥ {seuil} aussi ; sur toutes les pages, chaque guide GEO en rouge (< 25 :
AI Overview, ChatGPT ou Gemini) remonte au vert (≥ {seuil}). Sans faire baisser le
score Google. Pas de plafond de score, mais un texte rédigé naturellement, qui se
lit bien et apporte de la valeur au lecteur : chaque ajout doit apporter une
information réelle, jamais une répétition de mots-clés.
Modifie le MINIMUM nécessaire : ajoute ou complète des passages utiles (réponses
directes, FAQ, précisions), ne réécris pas ce qui fonctionne. Mesure avec
python3 _tools/seo_pipeline/serp.py score {slug} --label apres
(au plus 5 mesures intermédiaires --label essai1 … essai5).
Termine en écrivant _tools/seo_pipeline/runs/{slug}/writer_report.json
(score_avant = mesure de contrôle). Ne fais ni commit, ni push, ni modification hors périmètre.
""".format(slug=slug, seuil=cfg().get('seuil_vert', 50))
    if not fix:
        txt += """
Tu es l'agent RÉDACTEUR. Lis d'abord, en entier :
1. _tools/seo_pipeline/VERITE.md
2. _tools/seo_pipeline/REGLES_REDACTEUR.md
Puis applique REGLES_REDACTEUR.md à cette page, de l'étape 1 à l'étape 7.
Termine en écrivant _tools/seo_pipeline/runs/{slug}/writer_report.json.
Ne fais ni commit, ni push, ni modification hors périmètre.
""".format(slug=slug)
    else:
        txt += """
Tu es l'agent RÉDACTEUR, en correction. Ta modification précédente est dans
l'arbre de travail. Lis :
1. _tools/seo_pipeline/VERITE.md et _tools/seo_pipeline/REGLES_REDACTEUR.md (section 5)
2. _tools/seo_pipeline/runs/{slug}/review.json (verdict du relecteur)
3. _tools/seo_pipeline/runs/{slug}/checks.json (contrôles automatiques)
Corrige UNIQUEMENT les problèmes signalés (bloquants des contrôles, problèmes
du relecteur). Si la page a un générateur, corrige le script et relance-le.
VERITE.md a pu être mis à jour par Angelino APRÈS la relecture : si une
correction demandée contredit VERITE.md, VERITE.md l'emporte. N'applique pas
cette correction et explique-le dans `points_d_attention` du rapport.
Relance la mesure : python3 _tools/seo_pipeline/serp.py score {slug} --label fix (aucun nouveau guide), puis mets à jour writer_report.json.
""".format(slug=slug)
    return txt


def prompt_review(slug):
    e = entree(slug)
    txt = ENTETE.format(entree=json.dumps(e, ensure_ascii=False, indent=2), slug=slug,
                        langue_guide=cfg()['langues_serpmantics'].get(e['lang'], e['lang']))
    txt += """
Tu es l'agent RELECTEUR. Tu n'as pas écrit cette modification.
Lis, en entier :
1. _tools/seo_pipeline/REGLES_RELECTEUR.md (ta grille)
2. _tools/seo_pipeline/VERITE.md
3. _tools/seo_pipeline/runs/{slug}/diff.patch (la modification à relire)
4. _tools/seo_pipeline/runs/{slug}/writer_report.json
5. _tools/seo_pipeline/runs/{slug}/checks.json
Tu peux ouvrir les fichiers du dépôt pour le contexte (page complète, autres
pages pour la cannibalisation). Tu ne modifies rien.

Ta réponse finale doit être UNIQUEMENT l'objet JSON du verdict décrit dans
REGLES_RELECTEUR.md, sans texte avant ni après.
""".format(slug=slug)
    return txt


def extraire_json(texte):
    m = re.search(r'\{.*\}', texte, re.S)
    if not m:
        return None
    brut = m.group(0)
    for fin in range(len(brut), 0, -1):
        if brut[fin - 1] != '}':
            continue
        try:
            return json.loads(brut[:fin])
        except Exception:
            continue
    return None


def cmd_extract_review(slug, chemin):
    try:
        sortie = json.load(open(chemin, encoding='utf-8'))
        texte = sortie.get('result', '') if isinstance(sortie, dict) else str(sortie)
    except Exception:
        texte = open(chemin, encoding='utf-8', errors='replace').read()
    v = extraire_json(texte) or {'verdict': 'rejeter', 'resume': 'Verdict illisible : bloqué par sécurité.',
                                   'problemes': [], 'confiance': 'basse'}
    if v.get('confiance') == 'basse' and v.get('verdict') == 'approuver':
        v['verdict'] = 'reviser'
        v.setdefault('problemes', []).append({'gravite': 'a_corriger', 'regle': 'confiance',
                                              'correction_attendue': 'Confiance basse : approbation refusée.'})
    os.makedirs(os.path.join(RUNS, slug), exist_ok=True)
    json.dump(v, open(os.path.join(RUNS, slug, 'review.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    print(v.get('verdict', 'rejeter'))


def cmd_verdict(slug):
    v = lire_json(slug, 'review.json')
    print(v.get('verdict', 'absent') if v else 'absent')


def cout(slug):
    total = 0.0
    d = os.path.join(RUNS, slug)
    for f in os.listdir(d) if os.path.isdir(d) else []:
        if f.startswith(('writer_', 'review_raw_')) and f.endswith('.json'):
            try:
                total += float(json.load(open(os.path.join(d, f))).get('total_cost_usd') or 0)
            except Exception:
                pass
    return total


def cmd_summary(slug):
    e = entree(slug)
    w = lire_json(slug, 'writer_report.json') or {}
    r = lire_json(slug, 'review.json') or {}
    c = lire_json(slug, 'checks.json') or {}
    L = []
    L.append(f"## {e['url']} — « {e['requete']} »")
    L.append('')
    L.append(f"- **Score SERPmantics** : {w.get('score_avant', '?')} → **{w.get('score_apres', '?')}** "
             f"(cible top 3 : {w.get('cible_top3', '?')})")
    if w.get('guide_geo') or w.get('score_geo_apres') is not None:
        L.append(f"- **Score GEO** (moyenne des guides GEO) : {w.get('score_geo_avant', '?')} → **{w.get('score_geo_apres', '?')}**"
                 f" — objectif : {'vert (≥ %s)' % cfg().get('seuil_vert', 50) if e.get('objectif_geo') == 'vert' else 'au mieux (page de vente)'}")
    sc = None
    for nom_ in ('score_fix.json', 'score_apres.json', 'score_controle.json'):
        sc = lire_json(slug, nom_)
        if sc:
            break
    if sc:
        noms = {'google': 'Google', 'geo': 'AI Overview', 'chatgpt': 'ChatGPT', 'gemini': 'Gemini'}
        parts = [f"{noms.get(k, k)} {v.get('score')}" for k, v in sc.items()
                 if isinstance(v, dict) and v.get('score') is not None]
        if parts:
            L.append('- **Détail des scores (dernière mesure)** : ' + ' · '.join(parts))
    L.append(f"- **Crédits SERPmantics utilisés** : {w.get('credits_utilises', '?')}")
    L.append(f"- **Mots** : {w.get('mots_avant', '?')} → {w.get('mots_apres', '?')}")
    L.append(f"- **Relecteur** : {r.get('verdict', '?')} (confiance {r.get('confiance', '?')}) — {r.get('resume', '')}")
    L.append(f"- **Contrôles automatiques** : {'OK' if c.get('ok') else 'ÉCHEC'}"
             + (f" — {len(c.get('avertissements', []))} avertissement(s)" if c.get('avertissements') else ''))
    L.append(f"- **Mode** : {e['mode']}" + (' — **attend ton accord (page santé)**' if e['mode'] == 'validation' else ''))
    probs = r.get('problemes') or []
    if r.get('verdict') != 'approuver':
        a_traiter = [p for p in probs if p.get('gravite') in ('bloquant', 'a_corriger')]
        titre = '### Remarques du relecteur, à traiter avant toute fusion'
    else:
        a_traiter = [p for p in probs if p.get('gravite') == 'mineur']
        titre = '### Points mineurs signalés par le relecteur'
    if a_traiter:
        L.append('')
        L.append(titre)
        for p in a_traiter:
            ext = (p.get('extrait') or '').replace('\n', ' ')
            ext = ext[:180] + ('…' if len(ext) > 180 else '')
            cor = (p.get('correction_attendue') or '').replace('\n', ' ')
            cor = cor[:500] + ('…' if len(cor) > 500 else '')
            L.append(f"- **{p.get('gravite', '?')}** — « {ext} » → {cor}")
    if c.get('bloquants'):
        L.append('')
        L.append('### Blocages des contrôles automatiques')
        for b in c['bloquants']:
            L.append(f'- {b}')
    af = w.get('affirmations_factuelles') or []
    if af:
        L.append('')
        L.append('### Affirmations factuelles ajoutées')
        for a in af:
            L.append(f"- « {a.get('texte', '')} » — {a.get('source_verite', '?')}")
    if w.get('faits_manquants'):
        L.append('')
        L.append('### Faits manquants à ajouter dans VERITE.md (non utilisés)')
        for f in w['faits_manquants']:
            L.append(f'- {f}')
    if c.get('avertissements'):
        L.append('')
        L.append('### Avertissements')
        for a in c['avertissements']:
            L.append(f'- {a}')
    L.append('')
    L.append(f"_Coût équivalent API : {cout(slug):.2f} $ (non facturé si le circuit tourne sur l'abonnement Claude) — circuit SEO WebAutonomos (Claude Code + SERPmantics)_")
    print('\n'.join(L))


def cmd_state(slug, statut, note=''):
    os.makedirs(RUNS, exist_ok=True)
    st = state()
    st[slug] = {'statut': statut, 'note': note, 'date': datetime.datetime.now().isoformat(timespec='minutes')}
    json.dump(st, open(STATE, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)


def cmd_status():
    st = state()
    for p in cfg()['pages']:
        s = st.get(p['slug'], {})
        print(f"{p['slug']:24} {p['statut']:26} {p['mode']:10} {s.get('statut', '-'):12} {s.get('date', '')} {s.get('note', '')}")


if __name__ == '__main__':
    a = sys.argv[1:]
    if not a:
        sys.exit(__doc__)
    c = a[0]
    if c == 'next':
        cmd_next(int(a[2]) if len(a) > 2 and a[1] == '--n' else 3)
    elif c == 'field':
        v = entree(a[1]).get(a[2])
        print('' if v is None else v)
    elif c == 'prompt':
        mode_ = {'fix': True, 'affine': 'affine'}.get(a[1], False)
        print(prompt_review(a[2]) if a[1] == 'review' else prompt_writer(a[2], fix=mode_))
    elif c == 'extract-review':
        cmd_extract_review(a[1], a[2])
    elif c == 'verdict':
        cmd_verdict(a[1])
    elif c == 'a-affiner':
        cmd_a_affiner(int(a[2]) if len(a) > 2 and a[1] == '--n' else 50)
    elif c == 'etat':
        print(state().get(a[1], {}).get('statut', '-'))
    elif c == 'controle':
        cmd_controle(a[1], a[2])
    elif c == 'sync':
        cmd_sync()
    elif c == 'summary':
        cmd_summary(a[1])
    elif c == 'state':
        cmd_state(a[1], a[2], ' '.join(a[3:]))
    elif c == 'status':
        cmd_status()
    else:
        sys.exit(__doc__)
