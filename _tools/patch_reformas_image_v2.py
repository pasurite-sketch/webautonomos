# -*- coding: utf-8 -*-
"""/reformas/ : remplace l'illustration par la version haute qualité (24/09/2026).

- /assets/diseno-web-empresa-reformas.webp      1560×855 (écrans larges, retina)
- /assets/diseno-web-empresa-reformas-800.webp  800×439  (mobiles)
- /assets/diseno-web-empresa-reformas.jpg       1560×855 (navigateurs sans WebP)
?v=2 force les navigateurs et le cache à prendre les nouveaux fichiers.
Idempotent.

Usage : python3 _tools/patch_reformas_image_v2.py [chemin/vers/reformas/index.html]
"""
import re
import sys

F = sys.argv[1] if len(sys.argv) > 1 else 'reformas/index.html'
s = open(F, encoding='utf-8').read()

if 'diseno-web-empresa-reformas-800.webp' in s:
    print('déjà en place : rien à faire')
    sys.exit(0)

NOUVEAU = '''<picture>
      <source type="image/webp" srcset="/assets/diseno-web-empresa-reformas-800.webp?v=2 800w, /assets/diseno-web-empresa-reformas.webp?v=2 1560w" sizes="(max-width: 820px) calc(100vw - 40px), 780px">
      <img src="/assets/diseno-web-empresa-reformas.jpg?v=2" alt="Diseño web para empresas de reformas: ejemplo de portada con servicios de reformas integrales, cocinas, baños, pintura y carpintería" width="1560" height="855" loading="lazy" decoding="async">
    </picture>'''

motif = re.compile(r'<picture>\s*<source srcset="/assets/diseno-web-empresa-reformas\.webp".*?</picture>', re.S)
assert len(motif.findall(s)) == 1, "bloc <picture> de l'illustration introuvable"
s = motif.sub(NOUVEAU, s)

open(F, 'w', encoding='utf-8').write(s)
print('illustration remplacée (version haute qualité) dans', F)
