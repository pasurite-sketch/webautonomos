# -*- coding: utf-8 -*-
"""« autónomos de la Comunidad Valenciana » → « autónomos, pequeñas y medianas empresas »
(demande d'Angelino du 04/10/2026). Idempotent.

Pages : bloc auteur des articles ES, index du blog (meta, Open Graph, texte d'accroche), réponse
de FAQ de « como-conseguir-clientes-por-internet » (page statique et données du blog de index.html).
Générateurs, pour que les prochaines pages reprennent le texte : generate_spa_articles.py (bloc
auteur), generate_blog_index.py (index du blog), translate_article.py (clés espagnoles des blocs
auteur à traduire ; les traductions VAL, EN et FR ne changent pas) et le résumé de l'index du blog
dans _tools/photos/sujets.json.
"""
import glob
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ANCIEN, NOUVEAU = 'autónomos de la Comunidad Valenciana', 'autónomos, pequeñas y medianas empresas'
# translate_article.py écrit l'espagnol avec des échappements \uXXXX
ANCIEN_ECH = 'aut\\u00f3nomos de la Comunidad Valenciana'
NOUVEAU_ECH = 'aut\\u00f3nomos, peque\\u00f1as y medianas empresas'

fichiers = sorted(glob.glob(os.path.join(ROOT, 'blog', 'es', '*.html'))) + [os.path.join(ROOT, f) for f in (
    'blog/index.html', 'index.html', '_tools/photos/sujets.json',
    '_tools/generate_spa_articles.py', '_tools/generate_blog_index.py', '_tools/translate_article.py')]
total = 0
for p in fichiers:
    s = open(p, encoding='utf-8').read()
    n = s.count(ANCIEN) + s.count(ANCIEN_ECH)
    if n:
        open(p, 'w', encoding='utf-8').write(s.replace(ANCIEN, NOUVEAU).replace(ANCIEN_ECH, NOUVEAU_ECH))
        total += n
        print('%s : %d' % (os.path.relpath(p, ROOT), n))
print('remplacements :', total)
