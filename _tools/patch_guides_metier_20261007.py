# -*- coding: utf-8 -*-
"""Le blog prenait la place des pages métier (07/10/2026).

Constat de l'audit du 06/10 : sur « diseño web para fontaneros », c'est le guide du
blog qui sortait ; la page /fontaneros/ n'avait eu que 2 apparitions en 3 mois, et le
guide des psychologues en faisait 387 contre 61 pour /psicologos/.

Correctif :
1. Chaque guide espagnol renvoie vers sa page métier en haut d'article, juste après le
   chapeau, avec la formulation exacte de la requête commerciale comme ancre.
2. Les titres des 7 pages métier passent en « Páginas web para… » et « Diseño web… »
   (<title>, og:title, twitter:title), largeur vérifiée sous 580 px.

Idempotent (marqueur <!-- lien-page-metier -->) ; --dry-run pour afficher sans écrire.
"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = 'https://webautonomos.es'
MARQUEUR = '<!-- lien-page-metier -->'
STYLE_BLOC = ('background:#f0f7f6; border:1.5px solid #cfe5e0; border-radius:14px; '
              'padding:14px 18px;')
STYLE_LIEN = 'color:#2563eb; font-weight:600;'


def lien(metier, ancre):
    return '<a href="%s/%s/" style="%s">%s</a>' % (BASE, metier, STYLE_LIEN, ancre)


SUITE = ': ves una demo gratis en menos de 24 horas, antes de pagar.'
GUIDES = {
    'blog/es/web-para-fontaneros-guia-completa.html':
        '¿Prefieres que te hagamos la web? Consulta nuestro servicio de %s%s'
        % (lien('fontaneros', 'diseño web para fontaneros'), SUITE),
    'blog/es/web-para-psicologos-terapeutas.html':
        '¿Prefieres que te hagamos la web? Consulta nuestro servicio de %s%s'
        % (lien('psicologos', 'páginas web para psicólogos'), SUITE),
    'blog/es/pagina-web-para-electricistas.html':
        '¿Prefieres que te hagamos la web? Consulta nuestro servicio de %s%s'
        % (lien('electricistas', 'páginas web para electricistas'), SUITE),
    'blog/es/web-para-carpinteros-reformas.html':
        '¿Prefieres que te hagamos la web? Consulta nuestros servicios de %s y de %s%s'
        % (lien('carpinteros', 'páginas web para carpinteros'),
           lien('reformas', 'páginas web para empresas de reformas'), SUITE),
    # Formulation propre à ce guide : avec « servicios », sa note passait de 100 à 103 (gris).
    'blog/es/web-para-clinica-dental-fisioterapeuta.html':
        '¿Prefieres que te la hagamos? Así funcionan nuestras %s y %s: demo gratis en menos de 24 horas.'
        % (lien('dentistas', 'páginas web para dentistas'),
           lien('fisioterapeutas', 'páginas web para fisioterapeutas')),
}
CHAPEAU = '<p class="text-lg text-gray-700 leading-relaxed mb-6">'

TITRES = {  # page : (ancien titre, nouveau titre)
    'fontaneros': ('Diseño web para fontaneros: 15 €/mes, demo gratis en 24h',
                   'Diseño web para fontaneros | Páginas web a 15 €/mes'),
    'psicologos': ('Página web para psicólogos: 15 €/mes, demo gratis en 24h',
                   'Páginas web para psicólogos | Diseño web a 15 €/mes'),
    'dentistas': ('Página web para dentistas: 15 €/mes, demo gratis en 24h',
                  'Páginas web para dentistas | Diseño web a 15 €/mes'),
    'fisioterapeutas': ('Página web para fisioterapeutas: 15 €/mes, demo gratis en 24h',
                        'Páginas web para fisioterapeutas | Diseño web a 15 €/mes'),
    'carpinteros': ('Página web para carpinteros: 15 €/mes, demo gratis en 24h',
                    'Páginas web para carpinteros | Diseño web a 15 €/mes'),
    'electricistas': ('Página web para electricistas: 15 €/mes, demo gratis en 24h',
                      'Páginas web para electricistas | Diseño web a 15 €/mes'),
    'reformas': ('Página web para empresas de reformas: diseño web a 15 €/mes',
                 'Páginas web para empresas de reformas | Diseño web 15 €/mes'),
}


def main():
    ecrire = '--dry-run' not in sys.argv
    for rel, texte in GUIDES.items():
        p = os.path.join(ROOT, rel)
        s = open(p, encoding='utf-8').read()
        if MARQUEUR in s:
            print('déjà fait :', rel)
            continue
        i = s.index('<div class="article-body">')
        j = s.index(CHAPEAU, i)
        k = s.index('</p>', j) + len('</p>')
        bloc = ('\n            %s\n            <p class="text-gray-700 leading-relaxed mb-6" style="%s">%s</p>'
                % (MARQUEUR, STYLE_BLOC, texte))
        s = s[:k] + bloc + s[k:]
        print('lien ajouté :', rel)
        if ecrire:
            open(p, 'w', encoding='utf-8').write(s)
    for metier, (ancien, nouveau) in TITRES.items():
        p = os.path.join(ROOT, metier, 'index.html')
        s = open(p, encoding='utf-8').read()
        n = s.count(ancien)
        if n == 0:
            print('titre déjà changé ou introuvable :', metier, '|', 'nouveau présent' if nouveau in s else 'ABSENT')
            continue
        s = s.replace(ancien, nouveau)
        print('titre %s : %d occurrence(s) → %s' % (metier, n, nouveau))
        if ecrire:
            open(p, 'w', encoding='utf-8').write(s)


if __name__ == '__main__':
    main()
