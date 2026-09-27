# -*- coding: utf-8 -*-
"""Nettoyage du blog du 27/09/2026 (suite de nettoyage_blog.py du 24/09).

Retire des articles du blog, dans les 4 langues :
  - les statistiques sans source vérifiable (« 520 % d'appels en plus », « le Map Pack
    capte 60 à 75 % des clics », taux d'ouverture ou de rebond « normaux »…) ;
  - les faux cas clients nommés (« Lucía, esteticista en Alicante… ») ;
  - des promesses contraires à VERITE.md (intégration d'un système de réservation,
    site prêt en 5 à 10 jours, « des dizaines d'indépendants »).
Les chiffres gardés (offre WebAutonomos, méthode de chiffrage des automatisations,
expressions « 100 % », chiffres sourcés : INE 2025, Google 2016, Qonto/IO 2026…) sont
listés dans le champ « gardes » des tables.

Tables : _tools/nettoyage_blog_20260927.json (une par langue + « sup »), appliquées à
TOUTES les copies : pages du blog, données SPA de index.html, blog-spa-data.json,
_tools/queue, _tools/translations. Correspondance tolérante aux accents, apostrophes,
guillemets et espaces (les copies SPA sont sans accents).

    python3 _tools/nettoyage_blog_20260927.py            # essai : comptes
    python3 _tools/nettoyage_blog_20260927.py --apply    # écrit (rien si un JSON devient invalide)
Idempotent : un second passage ne trouve plus rien.
"""
import glob, json, os, re, sys

APPLY = '--apply' in sys.argv
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
CLS = {'a': 'aáàâ', 'e': 'eéèêë', 'i': 'iíïî', 'o': 'oóòô', 'u': 'uúüù', 'n': 'nñ', 'c': 'cç'}


def fz(lit):
    out = []
    for ch in lit:
        lo = ch.lower()
        if ch in "'’":
            out.append(r"(?:'|’|&#x27;|&#39;|\\')")
        elif ch == '"':
            out.append(r'(?:&quot;|\\"|"|“|”)')
        elif ch in '   ':
            out.append(r'(?:\s|&nbsp;| | )+')
        elif lo in CLS:
            k = CLS[lo]; out.append('[' + k + k.upper() + ']')
        elif lo in 'áàâéèêëíïîóòôúüùñç':
            base = next(b for b, v in CLS.items() if lo in v); k = CLS[base]
            out.append('[' + k + k.upper() + ']')
        else:
            out.append(re.escape(ch))
    return ''.join(out)


D = json.load(open('_tools/nettoyage_blog_20260927.json', encoding='utf-8'))
PAIRES = [p for l in D['ordre'] for p in D[l]['remplacements']]
for a, b in PAIRES:
    assert '"' not in b and '\\' not in b, b

FICHIERS = (sorted(glob.glob('blog/*/*.html')) + sorted(glob.glob('blog/*.html')) + ['index.html', 'blog-spa-data.json']
            + sorted(glob.glob('_tools/queue/published/*.json')) + sorted(glob.glob('_tools/queue/*.json'))
            + sorted(glob.glob('_tools/translations/*.json')))
contenus = {f: open(f, encoding='utf-8').read() for f in FICHIERS if os.path.exists(f)}
origine = dict(contenus)
total = 0
for a, b in PAIRES:
    rx = re.compile(fz(a))
    for f in contenus:
        contenus[f], n = rx.subn(lambda m: b, contenus[f])
        total += n
modifies = [f for f in contenus if contenus[f] != origine[f]]
erreurs = []
for f in modifies:
    s = contenus[f]
    if f.endswith('.json'):
        try:
            json.loads(s)
        except ValueError as e:
            erreurs.append(f'{f} : JSON invalide ({e})')
    for bloc in re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
        try:
            json.loads(bloc)
        except ValueError as e:
            erreurs.append(f'{f} : JSON-LD invalide ({e})')
print(f'{len(PAIRES)} paires, {total} remplacements, {len(modifies)} fichiers')
if erreurs:
    print('ABANDON, rien n\'est écrit :'); print('\n'.join(erreurs)); sys.exit(1)
if APPLY:
    for f in modifies:
        open(f, 'w', encoding='utf-8').write(contenus[f])
    print('écrit.')
