# -*- coding: utf-8 -*-
"""Blog FR : date d'en-tête écrite en français, et promesse « configuration sans frais » retirée (08/10/2026).

1. Date de l'en-tête (<time datetime="AAAA-MM-JJ">…</time>) : treize articles l'écrivaient en anglais
   (« 14 May 2026 »), en espagnol (« 03 Agosto 2026 ») ou avec une majuscule au mois (« 10 Septembre 2026 »).
   Elle est réécrite en français (« 14 mai 2026 », « 03 août 2026 », « 1er octobre 2026 »), seulement si le texte
   donne déjà la même date que l'attribut datetime : la valeur ne change jamais. La durée de lecture qui suit
   passe en « min de lecture » si elle était restée en espagnol ou en anglais.
2. « Mesurer les résultats de son site » (FR) et sa version valencienne promettaient que WebAutonomos configure
   Google Analytics « sans frais » : absent de VERITE.md, retiré sur décision d'Angelino du 08/10/2026.

Idempotent.
  python3 _tools/dates_fr_20261008.py [--dry-run]
A lancer depuis ~/webautonomos.
"""
import glob
import re
import sys

dry = '--dry-run' in sys.argv

MOIS_FR = ['janvier', 'février', 'mars', 'avril', 'mai', 'juin', 'juillet', 'août', 'septembre', 'octobre',
           'novembre', 'décembre']
NOMS = {}  # nom de mois (minuscules, toutes langues du site) -> numéro
for i, noms in enumerate([
        'janvier enero gener january', 'février fevrier febrero febrer february', 'mars marzo març march',
        'avril abril april', 'mai mayo maig may', 'juin junio juny june', 'juillet julio juliol july',
        'août aout agosto agost august', 'septembre septiembre setembre september',
        'octobre octubre october', 'novembre noviembre november', 'décembre decembre diciembre desembre december'],
        start=1):
    for n in noms.split():
        NOMS[n] = i

total = 0
for f in sorted(glob.glob('blog/fr/*.html')):
    s = open(f, encoding='utf-8').read()
    avant = s

    def date_fr(m):
        a, mo, j = (int(x) for x in m.group(2).split('-'))
        t = re.fullmatch(r'\s*(\d{1,2})(?:er)? (\S+) (\d{4})\s*', m.group(4))
        if not t or NOMS.get(t.group(2).lower()) != mo or int(t.group(1)) != j or int(t.group(3)) != a:
            if t:
                print('%-60s date non reconnue ou différente de datetime : %r' % (f, m.group(4)))
            return m.group(0)
        # le jour garde son écriture (« 03 » reste « 03 ») : le contrôle des nombres de checks.py verrait « 3 »
        # comme un nombre ajouté ; seul « 1 » devient « 1er »
        bon = '%s %s %d' % ('1er' if j == 1 else t.group(1), MOIS_FR[mo - 1], a)
        return m.group(1) + bon + m.group(5)

    s = re.sub(r'(<time datetime="((\d{4})-\d{2}-\d{2})">)([^<]*)(</time>)', date_fr, s, count=1)
    s = re.sub(r'(</time>\s*(?:·|&middot;)\s*(?:⏱\s*)?\d+ min) (?:de lectura|read)\b', r'\1 de lecture', s, count=1)
    if s != avant:
        total += 1
        print('%-60s %s' % (f, re.search(r'<time datetime="[^"]*">([^<]*)</time>[^\n<]*', s).group(0)[-48:]))
        if not dry:
            open(f, 'w', encoding='utf-8').write(s)

RETRAITS = {
    'blog/fr/mesurer-les-resultats-de-son-site.html':
        ' (si votre site est fait par WebAutonomos, nous le configurons pour vous sans frais)',
    'blog/val/mesurar-els-resultats-de-la-teua-web.html':
        ' (si la teua web està feta amb WebAutonomos, te&#x27;l configurem nosaltres sense cost)',
}
for f, phrase in RETRAITS.items():
    s = open(f, encoding='utf-8').read()
    n = s.count(phrase)
    print('%-60s promesse retirée : %d' % (f, n))
    if n and not dry:
        open(f, 'w', encoding='utf-8').write(s.replace(phrase, ''))
print('dates corrigées :', total, '(dry-run)' if dry else '')
