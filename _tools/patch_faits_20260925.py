# -*- coding: utf-8 -*-
"""Retire deux affirmations déclarées fausses par Angelino le 25/09/2026 :
  - « te respondemos con ejemplos reales » (FAQ des pages métier ES)
  - « fotos de alta calidad » (FAQ de /carpinteros/, visible + JSON-LD)
  - « Mira un ejemplo real » (H2 des pages métier : l'image est une démo)
Idempotent. À lancer depuis la racine du dépôt.

    python3 _tools/patch_faits_20260925.py               pages métier hors santé en réparation
    python3 _tools/patch_faits_20260925.py --avec-sante  + dentistas et fisioterapeutas
      (à lancer après la fusion de leurs PR de réparation : leurs versions
       réécrites sont en cours dans le circuit)
"""
import sys

PAGES = ['carpinteros/index.html', 'electricistas/index.html', 'fontaneros/index.html',
         'psicologos/index.html', 'reformas/index.html']
if '--avec-sante' in sys.argv:
    PAGES += ['dentistas/index.html', 'fisioterapeutas/index.html']

R = [
    ('contáctanos y te respondemos con ejemplos reales.', 'contáctanos y te respondemos.'),
    ('proyectos terminados con fotos de alta calidad.', 'proyectos terminados con tus propias fotos.'),
    # l'image des pages métier est une démo, pas le site d'un client (Angelino, 25/09 après-midi)
    ('<h2>Mira un ejemplo real para ', '<h2>Mira un ejemplo de web para '),
]

total = 0
for f in PAGES:
    s = open(f, encoding='utf-8').read()
    avant = s
    for ancien, nouveau in R:
        n = s.count(ancien)
        if n:
            s = s.replace(ancien, nouveau)
            total += n
            print(f'{n} remplacé(s)  {f} : {ancien}')
    if s != avant:
        open(f, 'w', encoding='utf-8').write(s)
    restes = [m for m in ('respondemos con ejemplos reales', 'fotos de alta calidad', 'ejemplo real para') if m in s]
    if restes:
        print(f'À VÉRIFIER  {f} : encore {", ".join(restes)} (autre formulation)')
print('total :', total)
