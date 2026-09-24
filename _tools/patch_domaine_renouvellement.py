# -*- coding: utf-8 -*-
"""Renouvellement du domaine (~12 €/an après la 1re année) : ne plus écrire
« dominio incluido … ningún coste oculto » sans le dire (décision d'Angelino
du 24/09/2026, option b). Idempotent.

- 6 pages métier ES (fontaneros exclue : sa réécriture est en cours dans une PR
  du circuit, qui corrige déjà ce point) : carte « Precio fijo, sin sorpresas »
- article « 5 razones » ES/EN (FAQ visible + JSON-LD) et FR (paragraphe),
  et les mêmes textes dans les données du blog de index.html
"""
import os

R = [
    # (fichiers, ancien, nouveau)
    (['carpinteros/index.html', 'dentistas/index.html', 'electricistas/index.html',
      'fisioterapeutas/index.html', 'psicologos/index.html', 'reformas/index.html'],
     '15€/mes lo cubre todo: diseño, hosting, dominio, SSL, mantenimiento y actualizaciones. Ningún coste oculto, nunca.',
     '15€/mes lo cubre todo: diseño, hosting, SSL, mantenimiento, actualizaciones y el dominio .es el primer año (después, unos 12 €/año). Sin costes ocultos.'),
    (['blog/es/5-razones-pagina-web-negocio-2026.html', 'index.html'],
     'Sí, el hosting, dominio .es, certificado SSL, mantenimiento y soporte técnico están incluidos en los 15€/mes. No hay costes ocultos. Es una solución todo incluido.',
     'Sí, el hosting, el certificado SSL, el mantenimiento, el soporte técnico y el dominio .es el primer año están incluidos en los 15€/mes. Después, el dominio se renueva por unos 12 €/año; no hay ningún otro coste.'),
    (['blog/es/5-razones-pagina-web-negocio-2026.html', 'index.html'],
     'Incluimos hosting, dominio y mantenimiento, sin costes ocultos.',
     'Incluimos hosting, mantenimiento y el dominio el primer año (después, unos 12 €/año).'),
    (['blog/en/5-reasons-your-business-needs-a-website-in-2026.html', 'index.html'],
     'Yes, hosting, .es domain, SSL certificate, maintenance, and technical support are all included in the €15/month. There are no hidden costs. Its an all-inclusive solution.',
     'Yes, hosting, the SSL certificate, maintenance, technical support and the .es domain for the first year are all included in the €15/month. After that, the domain renews for about €12/year; there are no other costs.'),
    (['blog/en/5-reasons-your-business-needs-a-website-in-2026.html', 'index.html'],
     'We include hosting, domain, and maintenance, with no hidden costs.',
     'We include hosting, maintenance and the domain for the first year (about €12/year after that).'),
    (['blog/fr/5-raisons-davoir-un-site-web-en-2026.html'],
     "L'hébergement, le nom de domaine et la maintenance sont compris, sans frais cachés.",
     "L'hébergement, la maintenance et le nom de domaine la première année (environ 12 €/an ensuite) sont compris."),
]

total = 0
for fichiers, ancien, nouveau in R:
    for f in fichiers:
        s = open(f, encoding='utf-8').read()
        n = s.count(ancien)
        if n == 0:
            etat = 'déjà fait' if nouveau in s else 'INTROUVABLE'
            print(f'{etat:12} {f} : {ancien[:60]}…')
            continue
        s = s.replace(ancien, nouveau)
        open(f, 'w', encoding='utf-8').write(s)
        total += n
        print(f'{n} remplacé(s)  {f} : {ancien[:60]}…')
print('total :', total)
