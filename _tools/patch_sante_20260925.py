# -*- coding: utf-8 -*-
"""Pages santé ES + liste des pages (décisions d'Angelino du 25/09/2026, après-midi).

- /fisioterapeutas/ et /psicologos/ : H1 sans promesse de résultat, aligné sur
  /dentistas/ (« …, lista en 24 horas ») ; mot-clé gardé en tête.
- /fisioterapeutas/ : « especialidades » → « tratamientos » (description Google,
  og:description, pastille du hero) — VERITE.md §9.
- pages.json : pages publiées le 25/09 marquées « fait », avec leurs scores.
Idempotent. À lancer depuis la racine du dépôt, après
`python3 _tools/patch_faits_20260925.py --avec-sante`.
"""
import json

R = {
    'fisioterapeutas/index.html': [
        ('<h1>Página web para <span class="ul">fisioterapeutas</span> que llena tu agenda</h1>',
         '<h1>Página web para <span class="ul">fisioterapeutas</span>, lista en 24 horas</h1>'),
        ('Demo personalizada en 24h que muestra tus especialidades.',
         'Demo personalizada en 24h que muestra tus tratamientos.'),
        ('✓ Diseñada para mostrar tus especialidades y servicios',
         '✓ Diseñada para mostrar tus tratamientos y servicios'),
    ],
    'psicologos/index.html': [
        ('<h1>Página web para <span class="ul">psicólogos</span> que llena tu consulta</h1>',
         '<h1>Página web para <span class="ul">psicólogos</span>, lista en 24 horas</h1>'),
    ],
}
for f, reps in R.items():
    s = open(f, encoding='utf-8').read()
    avant = s
    for ancien, nouveau in reps:
        n = s.count(ancien)
        if n:
            s = s.replace(ancien, nouveau)
            print(f'{n} remplacé(s)  {f} : {ancien[:70]}')
        elif nouveau not in s:
            print(f'INTROUVABLE  {f} : {ancien[:70]}')
    if s != avant:
        open(f, 'w', encoding='utf-8').write(s)

PUBLIEES = {  # slug : (PR, score Google avant, après, GEO avant, après)
    'es-electricistas': (3, 50, 70, 16, 28),
    'es-comparatif': (4, 8, 36, 25, 69),
    'es-dentistas': (5, 13, 39, 9, 19),
    'en-carpenters': (7, 41, 53, 10, 20),
    'es-fisioterapeutas': (8, 42, 77, 21, 51),
}
p = '_tools/seo_pipeline/pages.json'
s = open(p, encoding='utf-8').read()
for slug, (pr, g0, g1, e0, e1) in PUBLIEES.items():
    i = s.index(f'"slug": "{slug}"')
    j = s.index('}', i)
    bloc = s[i:j]
    ajout = f'Publiée le 25/09/2026 (PR #{pr}) : score Google {g0} → {g1}, GEO {e0} → {e1}.'
    if ajout in bloc:
        continue
    nb = bloc.replace('"statut": "a_faire"', '"statut": "fait"')
    k = nb.index('"notes": "') + len('"notes": "')
    fin = nb.index('"', k)
    while nb[fin - 1] == '\\':
        fin = nb.index('"', fin + 1)
    nb = nb[:fin] + (' ' if fin > k else '') + ajout + nb[fin:]
    s = s[:i] + nb + s[j:]
    print('pages.json :', slug, '→ fait')
json.loads(s)
open(p, 'w', encoding='utf-8').write(s)
