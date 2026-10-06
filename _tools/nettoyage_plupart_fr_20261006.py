# -*- coding: utf-8 -*-
"""Nettoyage du blog FR du 06/10/2026 : généralisations « la plupart des … » (VERITE.md §8).

« la plupart des (clients|patients|gens|internautes|indépendants|artisans|entreprises) » est
interdit par VERITE.md §8 ; REGLES_REDACTEUR.md §2 bis demande « beaucoup de », « souvent »,
« aide à ». Le texte visible des pages blog/fr en gardait 14 (relevé du 06/10/2026), plus
4 copies dans le JSON-LD FAQPage ; les données SPA d'index.html et _tools/queue n'en ont
aucune. Reformulations au vouvoiement, reprises des versions ES/EN réécrites quand elles
existent. Détail et décisions dans le champ « _lisez_moi » de la table.

Table : _tools/nettoyage_plupart_fr_20261006.json, appliquée à TOUTES les copies : pages du
blog, données SPA de index.html, blog-spa-data.json, _tools/queue, _tools/translations.
Correspondance tolérante aux accents, apostrophes, guillemets et espaces.

    python3 _tools/nettoyage_plupart_fr_20261006.py            # essai : comptes
    python3 _tools/nettoyage_plupart_fr_20261006.py -v         # essai, détail par fichier
    python3 _tools/nettoyage_plupart_fr_20261006.py --apply    # écrit (rien si un contrôle échoue)
Idempotent : un second passage ne trouve plus rien.
"""
import glob, json, os, re, sys

APPLY = '--apply' in sys.argv
VERBEUX = '-v' in sys.argv
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
sys.path.insert(0, os.path.join(ROOT, '_tools', 'seo_pipeline'))
sys.path.insert(0, os.path.join(ROOT, '_tools'))
from checks import nombres_du_texte, texte_visible, verite  # noqa: E402
from translate_article import tutoiement_hits  # noqa: E402

CLS = {'a': 'aáàâ', 'e': 'eéèêë', 'i': 'iíïî', 'o': 'oóòô', 'u': 'uúüù', 'n': 'nñ', 'c': 'cç'}


def fz(lit):
    out = []
    for ch in lit:
        lo = ch.lower()
        if ch in "'’":
            out.append(r"(?:'|’|&#x27;|&#39;|\\')")
        elif ch == '"':
            out.append(r'(?:&quot;|\\"|"|“|”)')
        elif ch in ' \u00a0\u202f':
            # \s couvre déjà U+00A0 et U+202F : les remettre en alternative fait exploser
            # le retour arrière sur blog-spa-data.json.
            out.append(r'(?:\s|&nbsp;)+')
        elif lo in CLS:
            k = CLS[lo]; out.append('[' + k + k.upper() + ']')
        elif lo in 'áàâéèêëíïîóòôúüùñç':
            base = next(b for b, v in CLS.items() if lo in v); k = CLS[base]
            out.append('[' + k + k.upper() + ']')
        else:
            out.append(re.escape(ch))
    return ''.join(out)


MOTIF = 'la plupart des (clients|patients|gens|internautes|ind[ée]pendants|artisans|entreprises)'
autorises, interdits = verite()
assert MOTIF in interdits, 'motif absent de VERITE.md §8 : mettre MOTIF à jour'
RX_MOTIF = re.compile(MOTIF, re.I)

D = json.load(open('_tools/nettoyage_plupart_fr_20261006.json', encoding='utf-8'))
PAIRES = [p for l in D['ordre'] for p in D[l]['remplacements']]
for a, b in PAIRES:
    assert '"' not in b and '\\' not in b, b
    assert not RX_MOTIF.search(b), f'motif §8 dans le remplacement : {b}'
    assert not tutoiement_hits(f'<body><p>{b}</p></body>'), f'tutoiement : {b}'
    nouveaux = [k for k in nombres_du_texte(b) if k not in nombres_du_texte(a) and k not in autorises]
    assert not nouveaux, f'nombre ajouté hors VERITE.md §7 ({nouveaux}) : {b}'
    assert '%' not in b and not re.search(r'\+\s?(IVA|TVA|VAT)', b), b

FICHIERS = (sorted(glob.glob('blog/*/*.html')) + sorted(glob.glob('blog/*.html')) + ['index.html', 'blog-spa-data.json']
            + sorted(glob.glob('_tools/queue/published/*.json')) + sorted(glob.glob('_tools/queue/*.json'))
            + sorted(glob.glob('_tools/translations/*.json')))
# newline='' : les fins de ligne restent exactement celles du fichier.
contenus = {f: open(f, encoding='utf-8', newline='').read() for f in FICHIERS if os.path.exists(f)}
origine = dict(contenus)


def famille(f):
    if f.startswith('blog/'):
        return f'pages {f.split("/")[1]} (texte visible)' if f.count('/') == 2 else 'pages blog/ (racine)'
    if f.startswith('_tools/'):
        return '/'.join(f.split('/')[:2])
    return f


def comptes(textes):
    res = {}
    for f, s in textes.items():
        # Pages : texte visible (comme le relecteur) ; ailleurs, données brutes.
        n = len(RX_MOTIF.findall(texte_visible(s) if f.startswith('blog/') else s))
        if n:
            res[famille(f)] = res.get(famille(f), 0) + n
    return res


avant = comptes(origine)
total = 0
for a, b in PAIRES:
    rx = re.compile(fz(a))
    par_paire, detail = 0, []
    for f in contenus:
        contenus[f], n = rx.subn(lambda m: b, contenus[f])
        if n:
            par_paire += n
            detail.append(f'{f} ×{n}' if n > 1 else f)
    print(f'{par_paire:3d}  {a[:96]}')
    if VERBEUX:
        for d in detail:
            print(f'       {d}')
    total += par_paire
modifies = [f for f in contenus if contenus[f] != origine[f]]
apres = comptes(contenus)

# _tools/translations : payloads locaux de translate_article.py, ignorés par git (présents
# seulement dans le dépôt principal) ; comptés à part, hors bilan.
print(f'\nMotif §8 « {MOTIF} » — avant → après :')
for fam in sorted(set(avant) | set(apres)):
    a_, p_ = avant.get(fam, 0), apres.get(fam, 0)
    print(f'  {fam:34s} {a_:3d} → {p_:3d}{"   ⚠ EN HAUSSE" if p_ > a_ else ""}'
          f'{"   (hors bilan)" if fam == "_tools/translations" else ""}')

erreurs = []
for fam in apres:
    if apres[fam] > avant.get(fam, 0):
        erreurs.append(f'{fam} : motif §8 en hausse')
for f in modifies:
    s, s0 = contenus[f], origine[f]
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
    if f.startswith('blog/') and f.endswith('.html'):
        # Bandeau d'appel à l'action, bloc auteur, articles liés et pied de page suivent la
        # dernière question de la FAQ, dans les deux gabarits : cette fin de page ne bouge pas.
        if '</details>' not in s0 or s[s.rfind('</details>'):] != s0[s0.rfind('</details>'):]:
            erreurs.append(f'{f} : fin de page (bandeau, bloc auteur) modifiée ou non vérifiable')
        if len(tutoiement_hits(s)) > len(tutoiement_hits(s0)):
            erreurs.append(f'{f} : tutoiement ajouté')
print(f'\n{len(PAIRES)} paires, {total} remplacements, {len(modifies)} fichiers')
if VERBEUX:
    print('\n'.join('  ' + f for f in modifies))
if erreurs:
    print('ABANDON, rien n\'est écrit :'); print('\n'.join(erreurs)); sys.exit(1)
if APPLY:
    for f in modifies:
        open(f, 'w', encoding='utf-8', newline='').write(contenus[f])
    print('écrit.')
