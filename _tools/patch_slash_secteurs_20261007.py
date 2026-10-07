# -*- coding: utf-8 -*-
"""Liens vers les 7 pages métier : adresse canonique avec slash final (07/10/2026).

Sans slash, Cloudflare répondait 307 (html_handling auto-trailing-slash) et Google
gardait les deux adresses. _redirects porte désormais une 301 pour chacune ; ce
script fait pointer les liens internes directement vers /<métier>/ :

- index.html : bouton de la section « Para quién » (href:"/"+p.key) et repli
  statique « Webs profesionales para » ;
- pages déployées (*.html, llms.txt) : href="/<métier>" et
  href="https://webautonomos.es/<métier>", liens Markdown de llms.txt.

L'article ES « cuanto-cuesta » est laissé tel quel (gelé jusqu'au contrôle du
22/10) : la 301 couvre ses liens. Idempotent ; --dry-run pour compter sans écrire.
_tools/generate_spa_articles.py écrit déjà le slash pour les nouveaux articles.
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
METIERS = ['psicologos', 'reformas', 'electricistas', 'carpinteros', 'fontaneros',
           'fisioterapeutas', 'dentistas']
GELES = {os.path.join('blog', 'es', 'cuanto-cuesta-pagina-web-autonomos-espana.html')}
EXCLUS = {'.git', 'node_modules', '_tools', '.wrangler', '.claude', 'scripts', '.github'}
# /<métier> suivi d'un guillemet ou d'une parenthèse fermante : jamais /<métier>/,
# ni psicologos.webautonomos.es, ni /demo-dentistas/, ni web-para-psicologos-…
LIEN = re.compile(r'''(?<![\w.-])((?:https://(?:www\.)?webautonomos\.es)?/(?:%s))(?=["')])'''
                  % '|'.join(METIERS))
BOUTON_AVANT = 'React.createElement("a",{href:"/"+p.key,'
BOUTON_APRES = 'React.createElement("a",{href:"/"+p.key+"/",'


def corriger(chemin, ecrire):
    s = open(chemin, encoding='utf-8').read()
    n_bouton = 0
    if os.path.basename(chemin) == 'index.html' and os.path.dirname(chemin) == ROOT:
        n_bouton = s.count(BOUTON_AVANT)
        s = s.replace(BOUTON_AVANT, BOUTON_APRES)
    t, n = LIEN.subn(r'\1/', s)
    if (n or n_bouton) and ecrire:
        open(chemin, 'w', encoding='utf-8').write(t)
    return n + n_bouton


def main():
    ecrire = '--dry-run' not in sys.argv
    total, fichiers = 0, 0
    for racine, dossiers, noms in os.walk(ROOT):
        dossiers[:] = [d for d in dossiers if d not in EXCLUS]
        for nom in noms:
            if not (nom.endswith('.html') or nom == 'llms.txt'):
                continue
            chemin = os.path.join(racine, nom)
            if os.path.relpath(chemin, ROOT) in GELES:
                continue
            n = corriger(chemin, ecrire)
            if n:
                total += n
                fichiers += 1
    print('%s : %d liens dans %d fichiers' % ('corrigés' if ecrire else 'à corriger', total, fichiers))
    # Contrôle : plus aucun lien sans slash hors fichiers gelés.
    reste = []
    for racine, dossiers, noms in os.walk(ROOT):
        dossiers[:] = [d for d in dossiers if d not in EXCLUS]
        for nom in noms:
            if nom.endswith('.html') or nom == 'llms.txt':
                chemin = os.path.join(racine, nom)
                rel = os.path.relpath(chemin, ROOT)
                if rel not in GELES and LIEN.search(open(chemin, encoding='utf-8').read()):
                    reste.append(rel)
    if ecrire and reste:
        sys.exit('liens restants : %s' % ', '.join(reste[:10]))


if __name__ == '__main__':
    main()
