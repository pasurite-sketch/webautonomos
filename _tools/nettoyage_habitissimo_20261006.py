# -*- coding: utf-8 -*-
"""Nettoyage du blog du 06/10/2026 : « Habitissimo » et inscription aux annuaires.

« Habitissimo » est interdit par VERITE.md §8. Il restait dans deux articles
(citations locales NAP, backlinks locaux) en ES, VAL et EN : pages VAL et EN, données
SPA de index.html, blog-spa-data.json. La conclusion de l'article sur les citations
promettait aussi d'inscrire le client dans les annuaires, service absent de
VERITE.md. Les pages ES, déjà réécrites, servent de modèle. Détail dans le champ
« _lisez_moi » de la table.

Tables : _tools/nettoyage_habitissimo_20261006.json (une par langue), appliquées à
TOUTES les copies : pages du blog, données SPA de index.html, blog-spa-data.json,
_tools/queue, _tools/translations. Correspondance tolérante aux accents, apostrophes,
guillemets et espaces (les copies SPA sont sans accents).

    python3 _tools/nettoyage_habitissimo_20261006.py            # essai : comptes
    python3 _tools/nettoyage_habitissimo_20261006.py --apply    # écrit (rien si un JSON devient invalide)
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


D = json.load(open('_tools/nettoyage_habitissimo_20261006.json', encoding='utf-8'))
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
    par_paire = 0
    for f in contenus:
        contenus[f], n = rx.subn(lambda m: b, contenus[f])
        par_paire += n
    print(f'{par_paire:3d}  {a[:90]}')
    total += par_paire
modifies = [f for f in contenus if contenus[f] != origine[f]]
# _tools/translations : payloads locaux (ignorés par git) extraits d'anciennes versions des
# pages ES. Leur champ « source » ne se modifie pas, et translate_article.py refuse un build
# quand la source a changé de structure : ils ne comptent pas dans ce contrôle.
restes = {f: len(re.findall(r'(?i)habitissimo', s)) for f, s in contenus.items()
          if not f.startswith('_tools/translations/') and re.search(r'(?i)habitissimo', s)}
if restes:
    print('habitissimo reste dans :', ', '.join(f'{f} ({n})' for f, n in restes.items()))
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
