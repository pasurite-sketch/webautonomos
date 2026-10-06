# -*- coding: utf-8 -*-
"""Blog servi par ses pages statiques (06/10/2026).

L'application React d'index.html garde une copie de chaque article (données SPA). Quand un visiteur
passait par le menu « Blog » ou par une carte d'article, elle affichait cette copie à l'adresse
/blog/<langue>/<slug> : sans photo (son composant ne rend pas les blocs « image ») et avec un texte
qui a divergé des fichiers blog/<langue>/<slug>.html (retouches du 14/09, nettoyages des 27 et 28/09,
réécritures d'octobre). Un rechargement de la même adresse montrait, lui, la page statique.

Ce script pose dans le <head> un court script qui transforme toute navigation interne vers /blog
(history.pushState) en chargement de page : le visiteur reçoit toujours la page statique, à jour et
avec ses photos, dans toutes les langues. Pour l'index du blog, il ajoute l'ancre de la langue de
l'application (#val, #en, #fr ; l'espagnol est en tête de page), lue dans <html lang> que
l'application met à jour (es, ca, en, fr).

Sans risque de boucle : le serveur sert un fichier pour /blog et pour chacune des 190 adresses
d'articles de l'application (vérifié le 06/10), et la page 404 pour une adresse inconnue
(not_found_handling « 404-page » dans wrangler.jsonc), jamais index.html. replaceState n'est pas
touché : l'état initial de l'application reste tel quel.

    python3 _tools/patch_blog_statique_20261006.py            # essai : dit ce qui serait fait
    python3 _tools/patch_blog_statique_20261006.py --apply    # écrit index.html
Idempotent : un second passage ne change rien ; une version antérieure du bloc est remplacée.
"""
import os
import re
import sys

APPLY = '--apply' in sys.argv
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
F = os.path.join(ROOT, 'index.html')
BLOC = (
    '<script id="blog-statique">/* Blog servi par ses pages statiques : une navigation interne vers /blog '
    'recharge la page (index : ancre de la langue). Posé par _tools/patch_blog_statique_20261006.py, '
    'ne pas modifier à la main. */'
    '(function(){var h=window.history,p=h.pushState,A={ca:"val",en:"en",fr:"fr"};'
    'h.pushState=function(s,t,u){if(u!=null){try{var x=new URL(u,location.href);'
    'if(x.origin===location.origin&&/^\\/blog(\\/|$)/.test(x.pathname)){'
    'if(/^\\/blog\\/?$/.test(x.pathname)&&!x.hash){x.pathname="/blog/";'
    'var l=A[document.documentElement.lang];if(l)x.hash=l;}'
    'location.assign(x.href);return;}}catch(e){}}return p.apply(h,arguments);};})();</script>\n'
)
ANCIEN = re.compile(r'<script id="blog-statique">.*?</script>\n?', re.S)

s = open(F, encoding='utf-8').read()
trouves = ANCIEN.findall(s)
if len(trouves) > 1:
    sys.exit('index.html : %d blocs « blog-statique », un seul attendu' % len(trouves))
if trouves and trouves[0] == BLOC:
    print('déjà à jour : rien à faire')
    sys.exit(0)
if trouves:
    nouveau = ANCIEN.sub(lambda m: BLOC, s, count=1)
    print('bloc existant remplacé par la version à jour (%d caractères)' % len(BLOC))
else:
    if s.count('</head>') != 1:
        sys.exit('index.html : « </head> » attendu une seule fois, trouvé %d fois' % s.count('</head>'))
    nouveau = s.replace('</head>', BLOC + '</head>', 1)
    print('bloc à poser avant </head> (%d caractères)' % len(BLOC))
if APPLY:
    open(F, 'w', encoding='utf-8').write(nouveau)
    print('index.html écrit')
else:
    print('essai seulement : relancer avec --apply')
