# -*- coding: utf-8 -*-
"""Bandeau final des articles d'automatisation : le délai du devis prend sa condition (07/10/2026).

Le bandeau disait « Devis en moins de 48 heures » ; la page du diagnostic précise « sous 48 heures
après la visioconférence » (VERITE.md §5 bis, confirmé par Angelino le 07/10/2026). Le bandeau
reprend désormais la condition, dans les quatre langues, et le générateur
(_tools/generate_spa_articles.py) aussi, pour qu'une régénération ne la retire pas.

Idempotent : la condition n'est ajoutée que si elle n'est pas déjà là.
  python3 _tools/patch_bandeau_devis_20261007.py [--sauf fichier ...] [--dry-run]
A lancer depuis ~/webautonomos.
"""
import glob
import re
import sys

CONDITION = {
    'Precio cerrado · Presupuesto en menos de 48 horas': ' tras la videollamada',
    'Preu tancat · Pressupost en menys de 48 hores': ' després de la videotrucada',
    'Fixed price · Quote within 48 hours': ' of the video call',
    'Prix ferme · Devis en moins de 48 heures': ' après la visioconférence',
}

args = sys.argv[1:]
dry = '--dry-run' in args
sauf = set(args[args.index('--sauf') + 1:]) if '--sauf' in args else set()
fichiers = sorted(glob.glob('blog/*/*.html')) + ['_tools/generate_spa_articles.py']
total = 0
for f in fichiers:
    if f in sauf:
        continue
    s = open(f, encoding='utf-8').read()
    n_f = 0
    for texte, cond in CONDITION.items():
        s, n = re.subn(re.escape(texte) + '(?!' + re.escape(cond) + ')', texte + cond, s)
        n_f += n
    if n_f:
        total += n_f
        print('%-70s %d' % (f, n_f))
        if not dry:
            open(f, 'w', encoding='utf-8').write(s)
print('total', total, '(dry-run)' if dry else '')
