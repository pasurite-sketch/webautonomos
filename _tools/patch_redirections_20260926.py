# -*- coding: utf-8 -*-
"""Adresses anciennes qui répondent encore 404 (Search Console, export du 26/09/2026).

Les anciens slugs espagnols des articles EN et VAL sont redirigés depuis le
31/08/2026, mais seulement sans extension. Les anciens sélecteurs de langue
liaient la version en .html (ex. /blog/en/categorias-google-business-como-elegir.html,
47 impressions) : ces adresses répondent 404. On ajoute une règle .html par
ancien slug, vers la cible finale (pas de chaîne de redirections).
Ajoute aussi /blog/how-much-does-website-cost-freelancers-spain (404) et
remplace, dans /dentistas/, trois liens /blog/<slug> qui passaient par une
redirection par l'adresse finale /blog/es/<slug>.
Idempotent. À lancer depuis la racine du dépôt.
"""
import os

R = '_redirects'
s = open(R, encoding='utf-8').read()
regles = []
for l in s.splitlines():
    p = l.split()
    if len(p) >= 3 and p[0].startswith(('/blog/en/', '/blog/val/')) and not p[0].endswith(('/', '.html')):
        regles.append((p[0], p[1]))
for _, cible in regles:
    assert os.path.isfile(cible.lstrip('/') + '.html'), cible
bloc = ['', '# Variantes .html des anciens slugs EN et VAL (26/09/2026, Search Console) :',
        '# les anciens selecteurs de langue liaient /blog/en/<slug-espagnol>.html, qui',
        '# repondait 404. Une regle par ancien slug, vers la cible finale.']
ajout = 0
for ancien, cible in regles:
    src = ancien + '.html'
    if src + ' ' not in s:
        bloc.append('%s  %s   301' % (src, cible))
        ajout += 1
extra = [('/blog/how-much-does-website-cost-freelancers-spain', '/blog/en/how-much-does-a-website-cost-for-freelancers'),
         ('/blog/how-much-does-website-cost-freelancers-spain/', '/blog/en/how-much-does-a-website-cost-for-freelancers')]
for a, c in extra:
    if a + ' ' not in s:
        bloc.append('%s  %s   301' % (a, c))
        ajout += 1
if ajout:
    s = s.rstrip('\n') + '\n' + '\n'.join(bloc) + '\n'
    open(R, 'w', encoding='utf-8').write(s)
print('_redirects : %d règles ajoutées' % ajout)

D = 'dentistas/index.html'
d = open(D, encoding='utf-8').read()
n = 0
for slug in ('como-aparecer-google-maps-autonomos', 'seo-local-que-es-autonomos', 'como-conseguir-resenas-google-negocio'):
    a = 'href="https://webautonomos.es/blog/%s"' % slug
    b = 'href="https://webautonomos.es/blog/es/%s"' % slug
    if a in d:
        assert os.path.isfile('blog/es/%s.html' % slug)
        n += d.count(a)
        d = d.replace(a, b)
if n:
    open(D, 'w', encoding='utf-8').write(d)
print('%s : %d liens corrigés' % (D, n))
