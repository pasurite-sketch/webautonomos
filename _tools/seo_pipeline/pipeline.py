#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Aide du circuit SEO/GEO : consignes des agents, état, résumé de PR.

    python3 _tools/seo_pipeline/pipeline.py next [--n 3]         slugs à traiter
    python3 _tools/seo_pipeline/pipeline.py field <slug> <champ>  un champ de pages.json
    python3 _tools/seo_pipeline/pipeline.py prompt writer|fix|review <slug>
    python3 _tools/seo_pipeline/pipeline.py extract-review <slug> <sortie_claude.json>
    python3 _tools/seo_pipeline/pipeline.py verdict <slug>        approuver|reviser|rejeter|absent
    python3 _tools/seo_pipeline/pipeline.py summary <slug>        corps de la PR (markdown)
    python3 _tools/seo_pipeline/pipeline.py state <slug> <statut> [note]
    python3 _tools/seo_pipeline/pipeline.py status               tableau de l'état local
"""
import json, os, re, sys, datetime

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
            and st.get(p['slug'], {}).get('statut') not in ('publie', 'pr_ouverte', 'bloque', 'en_cours')]
    todo.sort(key=lambda p: (p['priorite'], p['slug']))
    print('\n'.join(p['slug'] for p in todo[:n]))


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
    if not fix:
        txt += """
Tu es l'agent RÉDACTEUR. Lis d'abord, en entier :
1. _tools/seo_pipeline/VERITE.md
2. _tools/seo_pipeline/REGLES_REDACTEUR.md
Puis applique REGLES_REDACTEUR.md à cette page, de l'étape 1 à l'étape 6.
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
    if w.get('guide_geo'):
        L.append(f"- **Score GEO (réponses IA de Google)** : {w.get('score_geo_avant', '?')} → **{w.get('score_geo_apres', '?')}**")
    L.append(f"- **Crédits SERPmantics utilisés** : {w.get('credits_utilises', '?')}")
    L.append(f"- **Mots** : {w.get('mots_avant', '?')} → {w.get('mots_apres', '?')}")
    L.append(f"- **Relecteur** : {r.get('verdict', '?')} (confiance {r.get('confiance', '?')}) — {r.get('resume', '')}")
    L.append(f"- **Contrôles automatiques** : {'OK' if c.get('ok') else 'ÉCHEC'}"
             + (f" — {len(c.get('avertissements', []))} avertissement(s)" if c.get('avertissements') else ''))
    L.append(f"- **Mode** : {e['mode']}" + (' — **attend ton accord (page santé)**' if e['mode'] == 'validation' else ''))
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
        print(prompt_review(a[2]) if a[1] == 'review' else prompt_writer(a[2], fix=(a[1] == 'fix')))
    elif c == 'extract-review':
        cmd_extract_review(a[1], a[2])
    elif c == 'verdict':
        cmd_verdict(a[1])
    elif c == 'summary':
        cmd_summary(a[1])
    elif c == 'state':
        cmd_state(a[1], a[2], ' '.join(a[3:]))
    elif c == 'status':
        cmd_status()
    else:
        sys.exit(__doc__)
