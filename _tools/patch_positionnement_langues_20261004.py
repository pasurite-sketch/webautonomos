# -*- coding: utf-8 -*-
"""Suite de patch_positionnement_pymes_20261004.py (demande d'Angelino du 04/10/2026). Idempotent.

1. FAQ « comment trouver des clients sur internet » (ES, VAL, EN, FR ; pages et données du blog de
   index.html) : sans chiffre ni superlatif (« entre 5 y 15 llamadas », « las más rentables » :
   VERITE.md §7 et REGLES_REDACTEUR.md §2 bis), prix écrit « 15 €/mes » (VERITE.md §2).
2. Bloc auteur des articles VAL, EN et FR : « autónomos, pequeñas y medianas empresas » traduit.
3. Description de l'organisation (JSON-LD) : modèle d'article ES, articles FR.
Générateurs à jour : generate_spa_articles.py (blocs auteur) et translate_article.py (bloc auteur
et description traduits). La zone servie (areaServed) ne change pas.
"""
import glob
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
G = lambda motif: sorted(os.path.relpath(p, ROOT) for p in glob.glob(os.path.join(ROOT, motif)))
GEN, TRAD = '_tools/generate_spa_articles.py', '_tools/translate_article.py'

TEXTE = [
    # (fichiers, ancien, nouveau)
    (['blog/es/como-conseguir-clientes-por-internet.html', 'index.html'],
     'Las tres estrategias más rentables son: crear una ficha de Google Business Profile (gratis), tener una página web profesional (desde 15€/mes) y pedir reseñas a tus clientes satisfechos. Con estas tres acciones, muchos autónomos, pequeñas y medianas empresas consiguen entre 5 y 15 llamadas nuevas al mes.',
     'Empieza por tres acciones: crear una ficha de Google Business Profile (gratis), tener una página web profesional (15 €/mes) y pedir reseñas a tus clientes satisfechos. Juntas ayudan a autónomos, pequeñas y medianas empresas a conseguir más llamadas de clientes de su zona.'),
    (['blog/val/aconseguir-clients-per-internet.html', 'index.html'],
     'Les tres estratègies més rendibles són: crear una fitxa de Google Business Profile (gratuïta), tindre una pàgina web professional (des de 15€/mes) i demanar ressenyes als teues clients satisfets. Amb aquestes tres accions, molts autònoms de la Comunitat Valenciana aconsegueixen entre 5 i 15 cridades noves al mes.',
     'Comença per tres accions: crear una fitxa de Google Business Profile (gratuïta), tindre una pàgina web professional (15 €/mes) i demanar ressenyes als teus clients satisfets. Juntes ajuden autònoms, xicotetes i mitjanes empreses a aconseguir més cridades de clients de la seua zona.'),
    (['blog/en/how-to-find-clients-online.html', 'index.html'],
     'The three most cost-effective strategies are: creating a Google Business Profile listing (free), having a professional website (from €15/month) and asking satisfied customers for reviews. With those three actions, many freelancers in the Valencian Community get between five and fifteen new calls a month.',
     'Start with three actions: creating a Google Business Profile listing (free), having a professional website (€15/month) and asking satisfied customers for reviews. Together, they help freelancers and small and medium-sized businesses get more calls from customers in their area.'),
    (['blog/fr/comment-trouver-des-clients-sur-internet.html'],
     'Les trois stratégies les plus rentables sont : créer une fiche Google Business Profile (gratuit), avoir un site professionnel (à partir de 15 €/mois) et demander des avis à vos clients satisfaits. Ces trois actions suffisent souvent à faire sonner le téléphone plus régulièrement.',
     "Commencez par trois actions : créer une fiche Google Business Profile (gratuite), avoir un site professionnel (15 €/mois) et demander des avis à vos clients satisfaits. Ensemble, elles aident les indépendants et les petites et moyennes entreprises à recevoir plus d'appels de clients de leur zone."),
    # blocs auteur
    (G('blog/val/*.html') + [GEN],
     'Agència web especialitzada en autònoms de la Comunitat Valenciana.',
     'Agència web especialitzada en autònoms, xicotetes i mitjanes empreses.'),
    (G('blog/en/*.html') + [GEN, TRAD],
     'Web agency specialising in freelancers across the Valencian Community.',
     'Web agency specialising in freelancers and small and medium-sized businesses.'),
    (G('blog/fr/*.html') + [GEN],
     'Agence web spécialisée dans les indépendants de la Communauté valencienne.',
     'Agence web spécialisée dans les indépendants et les petites et moyennes entreprises.'),
    ([TRAD],  # translate_article.py écrit les accents en \uXXXX
     'Ag\\u00e8ncia web especialitzada en aut\\u00f2noms de la Comunitat Valenciana. ',
     'Ag\\u00e8ncia web especialitzada en aut\\u00f2noms, xicotetes i mitjanes empreses. '),
    # description de l'organisation (JSON-LD)
    (['template-article.html'],
     'SEO local para autónomos en la Comunidad Valenciana',
     'SEO local para autónomos, pequeñas y medianas empresas'),
    (G('blog/fr/*.html'),
     'SEO local pour les indépendants de la Communauté valencienne',
     'SEO local pour les indépendants et les petites et moyennes entreprises'),
]

# translate_article.py : chaînes coupées sur deux lignes (indentation conservée)
REGEX = [
    (r"ind\\u00e9pendants de la Communaut\\u00e9 '\n(\s*)'valencienne\. Sites web",
     r"ind\\u00e9pendants et les petites et '\n\1'moyennes entreprises. Sites web"),
    (r"per a aut\\u00f2noms de la '\n(\s*)'Comunitat Valenciana',",
     r"per a aut\\u00f2noms, xicotetes i '\n\1'mitjanes empreses',"),
    (r"pour les ind\\u00e9pendants de la '\n(\s*)'Communaut\\u00e9 valencienne',",
     r"pour les ind\\u00e9pendants et les '\n\1'petites et moyennes entreprises',"),
    (r"for freelancers in the Valencian '\n(\s*)'Community',",
     r"for freelancers and small and '\n\1'medium-sized businesses',"),
]


def lire(f):
    return open(os.path.join(ROOT, f), encoding='utf-8').read()


def ecrire(f, s):
    open(os.path.join(ROOT, f), 'w', encoding='utf-8').write(s)


for fichiers, ancien, nouveau in TEXTE:
    n_total, deja = 0, 0
    for f in fichiers:
        s = lire(f)
        n = s.count(ancien)
        if n:
            ecrire(f, s.replace(ancien, nouveau))
            n_total += n
        elif nouveau in s:
            deja += 1
    if not n_total and not deja:
        raise SystemExit('introuvable : ' + ancien[:70])
    print('%3d remplacement(s), %3d fichier(s) déjà à jour : %s' % (n_total, deja, ancien[:60]))

s = lire(TRAD)
for motif, rempl in REGEX:
    s, n = re.subn(motif, rempl, s)
    print('%3d remplacement(s) dans translate_article.py : %s' % (n, motif[:50]))
ecrire(TRAD, s)
