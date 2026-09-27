# -*- coding: utf-8 -*-
"""Corrections du 27/09/2026 hors blog, et renommage d'un article (décisions d'Angelino).

1. FAQ de l'accueil (4 langues, page + données SPA + JSON-LD) : retrait de
   « 46 % des recherches sur Google ont une intention locale » (chiffre sans source,
   VERITE.md §10).
2. Pages de démo (électriciens, plombiers ; 4 langues) : « Ejemplo real de web… »
   devient « Ejemplo de web… » (ce sont des démos, VERITE.md §6). Idem pour
   « ejemplos reales / real examples » dans trois descriptions d'articles.
3. Article FR « La paperasse vous vole huit heures par semaine » : le chiffre n'a pas
   de source. Nouveau titre « Ce que la paperasse coûte vraiment à une TPE », texte
   sans les 8 h / 380 h / 8 %, nouvelle adresse
   /blog/fr/ce-que-la-paperasse-coute-vraiment (301 depuis l'ancienne), hreflang des
   versions ES, VAL et EN, données SPA, index du blog et sitemap mis à jour.
Idempotent. À lancer depuis la racine du dépôt :
    python3 _tools/patch_site_20260927.py            # essai
    python3 _tools/patch_site_20260927.py --apply
"""
import glob, json, os, re, shutil, sys

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


T = [
    # 1. FAQ de l'accueil
    ("Es fundamental para negocios locales: el 46% de las búsquedas en Google tienen intención local.",
     "Es fundamental para un negocio local: es lo que aparece en Google Maps y en las búsquedas de tu zona."),
    ("És fonamental per a negocis locals: el 46% de les cerques en Google tenen intenció local.",
     "És fonamental per a un negoci local: és el que apareix en Google Maps i en les cerques de la teua zona."),
    ("It's essential for local businesses: 46% of Google searches have local intent.",
     "It’s essential for a local business: it’s what shows up in Google Maps and in searches in your area."),
    ("C'est essentiel pour une activité locale : 46 % des recherches sur Google ont une intention locale.",
     "C’est essentiel pour une activité locale : c’est ce qui apparaît dans Google Maps et dans les recherches de votre secteur."),
    # 2. démos et descriptions
    ("Ejemplo real de web para electricistas:", "Ejemplo de web para electricistas:"),
    ("Ejemplo real de web para fontaneros:", "Ejemplo de web para fontaneros:"),
    ("Exemple real de web per a electricistes:", "Exemple de web per a electricistes:"),
    ("Exemple real de web per a fontaners:", "Exemple de web per a fontaners:"),
    ("A real example of a website for electricians:", "An example website for electricians:"),
    ("A real example of a website for plumbers:", "An example website for plumbers:"),
    ("Exemple réel de site pour électriciens :", "Exemple de site pour électriciens :"),
    ("Exemple réel de site pour plombiers :", "Exemple de site pour plombiers :"),
    ("Ejemplos reales y soluciones asequibles.", "Ejemplos concretos y soluciones asequibles."),
    ("Exemples reals i solucions assequibles.", "Exemples concrets i solucions assequibles."),
    ("Real examples and affordable solutions.", "Practical examples and affordable solutions."),
    ("Exemples réels et solutions abordables.", "Exemples concrets et solutions abordables."),
    ("Con herramientas gratuitas y ejemplos reales.", "Con herramientas gratuitas y ejemplos concretos."),
    ("Amb ferramentes gratuïtes i exemples reals.", "Amb ferramentes gratuïtes i exemples concrets."),
    ("con ejemplos reales y los errores que debes evitar", "con ejemplos concretos y los errores que debes evitar"),
    ("amb exemples reals i els errors que has d'evitar", "amb exemples concrets i els errors que has d’evitar"),
    # 3. article FR sur la paperasse
    ("La paperasse vous vole huit heures par semaine", "Ce que la paperasse coûte vraiment à une TPE"),
    ("Un dirigeant de TPE consacre environ huit heures par semaine à l'administratif. D'où vient ce chiffre, ce qu'il coûte vraiment, et comment calculer le vôtre.",
     "La paperasse prend chaque semaine des heures qu’un dirigeant de TPE ne facture pas. Ce qu’elle coûte vraiment, et comment calculer votre propre chiffre en deux minutes."),
    ("Huit heures par semaine, près de 380 heures par an. Et seuls 8 % des dirigeants estiment que ça s'est allégé en cinq ans. Voici ce que ça vous coûte.",
     "Des heures chaque semaine, sans rien facturer. Voici ce que la paperasse vous coûte vraiment, et comment calculer votre propre chiffre."),
    ("Et les études convergent sur un chiffre : environ huit heures par semaine pour un dirigeant de TPE. Presque une journée entière, chaque semaine, à ne rien facturer.",
     "Et pour beaucoup de dirigeants de TPE, ce sont des heures entières, chaque semaine, passées à ne rien facturer."),
    ("Huit heures qui ne se voient nulle part", "Des heures qui ne se voient nulle part"),
    ("Sur une année de travail, cela représente environ 380 heures — l'équivalent de dix semaines pleines.",
     "Additionnées sur une année, ces petites tâches finissent par peser lourd."),
    ("Si votre heure se facture 40 euros, 380 heures représentent plus de 15 000 euros par an de chiffre d'affaires que vous n'avez pas produit.",
     "Si votre heure se facture 40 euros, chaque heure passée sur la paperasse représente 40 euros de chiffre d’affaires que vous n’avez pas produits : multipliez par votre propre nombre d’heures."),
    ("Les huit heures sont une moyenne. La vôtre sera différente, et elle vaut la peine d'être connue tâche par tâche.",
     "Votre chiffre vous est propre, et il vaut la peine d’être connu tâche par tâche."),
    ("D'où vient le chiffre de huit heures par semaine ?", "Combien de temps la paperasse prend-elle à une TPE ?"),
    ("C'est l'ordre de grandeur sur lequel convergent les études françaises consacrées à la gestion administrative des TPE. Votre propre chiffre peut être très différent : le plus fiable est de le calculer tâche par tâche, comme expliqué dans cet article.",
     "Cela varie beaucoup d’une activité à l’autre, et aucune moyenne ne remplace votre propre mesure : le plus fiable est de calculer votre chiffre tâche par tâche, comme expliqué dans cet article."),
]
for a, b in T:
    assert '"' not in b and '\\' not in b, b

ANCIEN, NOUVEAU = 'paperasse-huit-heures-par-semaine', 'ce-que-la-paperasse-coute-vraiment'
F_ANCIEN, F_NOUVEAU = f'blog/fr/{ANCIEN}.html', f'blog/fr/{NOUVEAU}.html'

FICHIERS = (['index.html', 'blog-spa-data.json', 'blog/index.html', 'sitemap.xml']
            + sorted(glob.glob('demo-*.html')) + sorted(glob.glob('demo-*/index.html'))
            + sorted(glob.glob('blog/*/*.html')))
contenus = {f: open(f, encoding='utf-8').read() for f in FICHIERS if os.path.exists(f)}
origine = dict(contenus)
comptes = []
for a, b in T:
    rx = re.compile(fz(a)); n = 0
    for f in contenus:
        contenus[f], k = rx.subn(lambda m: b, contenus[f]); n += k
    comptes.append((n, a))
# renommage : toutes les mentions de l'ancienne adresse
n_slug = 0
for f in contenus:
    n_slug += contenus[f].count(ANCIEN)
    contenus[f] = contenus[f].replace(ANCIEN, NOUVEAU)
modifies = [f for f in contenus if contenus[f] != origine[f]]
erreurs = []
for f in modifies:
    if f.endswith('.json'):
        try: json.loads(contenus[f])
        except ValueError as e: erreurs.append(f'{f} : {e}')
    for bloc in re.findall(r'<script type="application/ld\+json">(.*?)</script>', contenus[f], re.S):
        try: json.loads(bloc)
        except ValueError as e: erreurs.append(f'{f} JSON-LD : {e}')
for n, a in comptes:
    print(f'{n:3}  {a[:80]}')
print(f'adresse de l\'article : {n_slug} mentions remplacées ; {len(modifies)} fichiers modifiés')
if erreurs:
    print('ABANDON :', *erreurs, sep='\n'); sys.exit(1)

red = open('_redirects', encoding='utf-8').read()
regles = [(f'/blog/fr/{ANCIEN}', f'/blog/fr/{NOUVEAU}'), (f'/blog/fr/{ANCIEN}/', f'/blog/fr/{NOUVEAU}'),
          (f'/blog/fr/{ANCIEN}.html', f'/blog/fr/{NOUVEAU}')]
ajout = [f'{a}  {b}   301' for a, b in regles if f'{a} ' not in red]
if APPLY:
    for f in modifies:
        open(f, 'w', encoding='utf-8').write(contenus[f])
    if os.path.exists(F_ANCIEN) and not os.path.exists(F_NOUVEAU):
        shutil.move(F_ANCIEN, F_NOUVEAU)
    if ajout:
        red = red.rstrip('\n') + '\n\n# Article FR renommé le 27/09/2026 (chiffre sans source retiré du titre)\n' + '\n'.join(ajout) + '\n'
        open('_redirects', 'w', encoding='utf-8').write(red)
    print('écrit ; fichier renommé :', os.path.exists(F_NOUVEAU), '; redirections ajoutées :', len(ajout))
