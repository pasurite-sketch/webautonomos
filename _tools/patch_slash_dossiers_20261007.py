# -*- coding: utf-8 -*-
"""Liens vers les pages servies depuis un dossier : adresse avec slash final (07/10/2026).

Suite de patch_slash_secteurs_20261007.py (les 7 pages métier) pour les autres dossiers
du site : /blog/, /aviso-legal/, /privacidad/, /cookies/, les pages de diagnostic et de
visibilité IA (ES, EN, FR), /en/, /fr/, les démos et les pages de remerciement. Sans
slash, Cloudflare répondait 307 ; _redirects porte désormais une 301 pour chacune.

Ce script fait pointer les liens internes directement vers /<dossier>/ :
- attributs href, og:url, données JSON-LD (fil d'Ariane « Blog », catégories
  /blog/?categoria=…), liens Markdown de llms.txt ;
- dans index.html, seulement les adresses absolues (JSON-LD de l'application) : les
  chaînes relatives du routeur ('/blog' dans getPageFromUrl…) restent telles quelles,
  la navigation interne vers /blog passant déjà par le script blog-statique.

L'article ES « cuanto-cuesta » est laissé tel quel (gelé jusqu'au contrôle du 22/10).
Idempotent ; --dry-run pour compter sans écrire.
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOSSIERS = ['aviso-legal', 'blog', 'cookies', 'demo-carpintero', 'demo-dentistas',
            'diagnostico-automatizacion', 'en', 'en/ai-visibility', 'en/automation-diagnostic',
            'fr', 'fr/diagnostic-automatisation', 'fr/visibilite-ia', 'gracias-gmb', 'gracias-seo',
            'gracias-visibilidad-ia', 'gracias', 'merci', 'privacidad', 'thank-you', 'visibilidad-ia']
GELES = {os.path.join('blog', 'es', 'cuanto-cuesta-pagina-web-autonomos-espana.html')}
EXCLUS = {'.git', 'node_modules', '_tools', '.wrangler', '.claude', 'scripts', '.github'}
_ALT = '|'.join(re.escape(d) for d in sorted(DOSSIERS, key=len, reverse=True))
# /<dossier> suivi d'un guillemet, d'une parenthèse, de « ? » ou de « # » : jamais
# /<dossier>/…, ni /blog/es/…, ni un sous-domaine ou un slug qui le contient.
LIEN = re.compile(r'''(?<![\w.-])((?:https://(?:www\.)?webautonomos\.es)?/(?:%s))(?=["')?#])''' % _ALT)
LIEN_ABSOLU = re.compile(r'''(?<![\w.-])(https://(?:www\.)?webautonomos\.es/(?:%s))(?=["')?#])''' % _ALT)


def motif(chemin):
    return LIEN_ABSOLU if os.path.relpath(chemin, ROOT) == 'index.html' else LIEN


def fichiers():
    for racine, dossiers, noms in os.walk(ROOT):
        dossiers[:] = [d for d in dossiers if d not in EXCLUS]
        for nom in noms:
            if nom.endswith('.html') or nom == 'llms.txt':
                chemin = os.path.join(racine, nom)
                if os.path.relpath(chemin, ROOT) not in GELES:
                    yield chemin


def main():
    ecrire = '--dry-run' not in sys.argv
    total, nb = 0, 0
    for chemin in fichiers():
        s = open(chemin, encoding='utf-8').read()
        t, n = motif(chemin).subn(r'\1/', s)
        if n:
            total += n
            nb += 1
            if ecrire:
                open(chemin, 'w', encoding='utf-8').write(t)
    print('%s : %d liens dans %d fichiers' % ('corrigés' if ecrire else 'à corriger', total, nb))
    if ecrire:
        reste = [os.path.relpath(c, ROOT) for c in fichiers()
                 if motif(c).search(open(c, encoding='utf-8').read())]
        if reste:
            sys.exit('liens restants : %s' % ', '.join(reste[:10]))


if __name__ == '__main__':
    main()
