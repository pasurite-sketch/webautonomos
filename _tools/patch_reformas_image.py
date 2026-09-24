# -*- coding: utf-8 -*-
"""Ajoute l'illustration « diseño web para empresas de reformas » dans /reformas/.

Position : section #diseno-web-reformas (la section qui porte la requête
principale), après le 2e paragraphe, avant « En WebAutonomos hacemos… ».
Image : /assets/diseno-web-empresa-reformas.webp (+ .jpg de secours),
1108×618, chargement différé. Idempotent.

Usage : python3 _tools/patch_reformas_image.py [chemin/vers/reformas/index.html]
"""
import sys

F = sys.argv[1] if len(sys.argv) > 1 else 'reformas/index.html'
s = open(F, encoding='utf-8').read()

if 'diseno-web-empresa-reformas.webp' in s:
    print('déjà en place : rien à faire')
    sys.exit(0)

CSS_ANCRE = '.gd-band{background:var(--off)}'
CSS = ('.gd-band{background:var(--off)}'
       '.gd figure{margin:28px 0 24px}'
       '.gd figure img{display:block;width:100%;height:auto;border-radius:14px;'
       'box-shadow:0 18px 48px rgba(15,32,96,.14);border:1px solid var(--border)}'
       '.gd figcaption{font-size:.92rem;color:#64748b;text-align:center;margin-top:10px;line-height:1.5}')
assert s.count(CSS_ANCRE) == 1, 'ancre CSS introuvable'
s = s.replace(CSS_ANCRE, CSS)

ANCRE = 'el cliente llega después de ver tus proyectos y ya sabe lo que ofreces.</p>'
FIGURE = ANCRE + '''
  <figure>
    <picture>
      <source srcset="/assets/diseno-web-empresa-reformas.webp" type="image/webp">
      <img src="/assets/diseno-web-empresa-reformas.jpg" alt="Diseño web para empresas de reformas: ejemplo de portada con servicios de reformas integrales, cocinas, baños, pintura y carpintería" width="1108" height="618" loading="lazy" decoding="async">
    </picture>
    <figcaption>Ejemplo de portada para un negocio de reformas: los servicios a la vista y el contacto a un clic.</figcaption>
  </figure>'''
assert s.count(ANCRE) == 1, 'ancre du 2e paragraphe introuvable'
s = s.replace(ANCRE, FIGURE)

open(F, 'w', encoding='utf-8').write(s)
print('illustration ajoutée dans', F)
