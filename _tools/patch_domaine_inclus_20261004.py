# -*- coding: utf-8 -*-
"""Article « elegir dominio » : le domaine n'est pas inclus « sin coste adicional ».

VERITE.md §2 : domaine .es au nom du client, inclus la première année, ensuite environ 12 €/an
(décision d'Angelino du 24/09/2026, déjà appliquée ailleurs par patch_domaine_renouvellement.py).
Le 04/10/2026, la réécriture SERPmantics de blog/es/como-elegir-dominio-web-negocio.html a corrigé
la version espagnole statique ; la même phrase restait dans les données du blog de index.html
(ES, VAL, EN) et dans les articles statiques VAL, EN et FR. Idempotent.
"""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

R = [
    # (fichiers, ancien, nouveau)
    (['index.html'],
     'En WebAutonomos incluimos el dominio .es en todos los planes sin coste adicional.',
     'En WebAutonomos registramos el dominio .es a tu nombre: está incluido el primer año y después cuesta unos 12 € al año.'),
    (['index.html', 'blog/val/triar-el-domini-del-teu-negoci.html'],
     'A WebAutonomos incloem el domini .es en tots els plans sense cost addicional.',
     'A WebAutonomos registrem el domini .es al teu nom: està inclòs el primer any i després costa uns 12 € a l\'any.'),
    (['index.html', 'blog/en/how-to-choose-your-domain-name.html'],
     'At WebAutonomos we include the .es domain in all plans at no extra cost.',
     'At WebAutonomos we register the .es domain in your name: it is included for the first year, then costs about €12 a year.'),
    (['blog/fr/choisir-le-nom-de-domaine-de-son-site.html'],
     'Chez WebAutonomos, le nom de domaine est compris dans tous les forfaits, sans supplément.',
     'Chez WebAutonomos, le nom de domaine est enregistré à votre nom et compris la première année, puis coûte environ 12 €/an.'),
    (['blog/fr/choisir-le-nom-de-domaine-de-son-site.html'],
     'chez WebAutonomos le domaine est compris et enregistré à votre nom.',
     'chez WebAutonomos le domaine est enregistré à votre nom et compris la première année.'),
]

for fichiers, ancien, nouveau in R:
    for f in fichiers:
        p = os.path.join(ROOT, f)
        s = open(p, encoding='utf-8').read()
        n = s.count(ancien)
        if n:
            s = s.replace(ancien, nouveau)
            open(p, 'w', encoding='utf-8').write(s)
            print('%s : %d remplacement(s)' % (f, n))
        elif nouveau in s:
            print('%s : déjà corrigé' % f)
        else:
            raise SystemExit('%s : texte introuvable : %s' % (f, ancien[:60]))
