# -*- coding: utf-8 -*-
"""/reformas/ : allège les mots trop répétés signalés par SERPmantics (24/09/2026).

Avant → cible (fourchette SERPmantics du top 10) :
  fotos 21 → 6 (3-6) · cliente 13 → 4 (2-4) · datos 11 → 6 (3-6) · obras 14 → 10 (2-10)
Synonymes choisis pour ne pas faire déborder d'autres expressions :
  trabajos 0 → 3 (2-4) · información 2 → 5 (2-6) · clientes 10 → 11 (8-15).
Les réponses de la FAQ visible et du JSON-LD FAQPage restent identiques
(remplacements attendus 2 fois). Aucun fait ajouté. Idempotent.

Usage : python3 _tools/patch_reformas_repetitions.py [reformas/index.html]
"""
import sys

F = sys.argv[1] if len(sys.argv) > 1 else 'reformas/index.html'
s = open(F, encoding='utf-8').read()

if 'Opiniones e información que dan confianza' in s:
    print('déjà en place : rien à faire')
    sys.exit(0)

R = [
    # (ancien, nouveau, nombre d'occurrences attendu : 2 = FAQ visible + JSON-LD)
    ('con tus fotos y reseñas reales de Google', 'con tus imágenes y reseñas reales de Google', 1),
    ('verás tu web con tus fotos, tus reseñas de Google', 'verás tu web con tus imágenes, tus reseñas de Google', 1),
    ('mira fotos de obras terminadas', 'mira trabajos terminados', 1),
    ('donde el cliente llega comparando tu precio', 'donde los clientes llegan comparando tu precio', 1),
    ('Con tu propia página web, el cliente llega después de ver tus proyectos y ya sabe lo que ofreces.',
     'Con tu propia página web, llegan después de ver tus proyectos y ya saben lo que ofreces.', 1),
    ('se escribe con los datos reales de tu empresa: tus servicios, tu zona, tus fotos y las reseñas',
     'se escribe con la información real de tu empresa: tus servicios, tu zona, tus imágenes y las reseñas', 1),
    ('en la decisión del cliente', 'en la decisión de quien contrata una reforma', 1),
    ('en una galería de obras con fotos del antes y el después', 'en una galería con el antes y el después', 1),
    ('Nada de fotos de stock: el cliente lo nota', 'Nada de imágenes de stock: quien visita tu web lo nota', 1),
    ('y el cliente encuentra la información que necesita', 'y quien llega a tu web encuentra la información que necesita', 1),
    ('cuantos más datos pides', 'cuantos más campos pides', 1),
    ('para que el cliente te envíe fotos del espacio que quiere reformar',
     'para que te envíen imágenes del espacio que quieren reformar', 1),
    ('<h3>Opiniones y datos que dan confianza</h3>', '<h3>Opiniones e información que dan confianza</h3>', 1),
    ('con fotos de tus obras y la información que el cliente busca antes de solicitar presupuesto',
     'con imágenes de tus trabajos y la información que se busca antes de solicitar presupuesto', 1),
    ('<strong>Fotos de stock o de mala calidad.</strong> Restan confianza justo donde el cliente necesita',
     '<strong>Imágenes de stock o de mala calidad.</strong> Restan confianza justo donde quien te visita necesita', 1),
    ('Pedir quince datos antes de dar un presupuesto hace que el cliente llame a otra empresa.',
     'Pedir quince campos antes de dar un presupuesto hace que llamen a otra empresa.', 1),
    ('textos, colores, fotos, secciones añadidas', 'textos, colores, imágenes, secciones añadidas', 2),
    ('cambios de fotos o textos', 'cambios de imágenes o textos', 2),
    ('(textos, fotos, horarios, nuevos servicios)', '(textos, imágenes, horarios, nuevos servicios)', 2),
    ('Nos envías las fotos por WhatsApp o email', 'Nos envías las imágenes por WhatsApp o email', 2),
    ('tipo de obra, zona, plazo o fotos del espacio', 'tipo de obra, zona, plazo o imágenes del espacio', 2),
    ('carga rápida y datos coherentes con tu ficha de Google', 'carga rápida e información coherente con tu ficha de Google', 2),
    ('quiere ver obras terminadas y teme los retrasos', 'quiere ver trabajos terminados y teme los retrasos', 2),
    ('Mismas prestaciones, textos y fotos incluidos.', 'Mismas prestaciones, textos e imágenes incluidos.', 1),
]

for ancien, nouveau, n in R:
    trouve = s.count(ancien)
    assert trouve == n, f'{trouve} occurrence(s) au lieu de {n} : {ancien!r}'
    s = s.replace(ancien, nouveau)

open(F, 'w', encoding='utf-8').write(s)
print(f'{len(R)} passages allégés dans', F)
