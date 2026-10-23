#!/usr/bin/env python3
"""Liens internes vers les pages de vente de Metrado (22/10/2026).

Ajoute un passage marqué <!-- lien-devia --> dans les trois pages de services :
- servicios.html : section « App de presupuestos Metrado » avant « Redes sociales » ;
- en/services.html : Metrado dans la liste « Two more services » (qui devient « Three ») ;
- fr/prestations.html : paragraphe avant « Questions fréquentes ».

Idempotent : une page qui a déjà le repère est signalée [DEJA].
Usage : python3 _tools/patch_liens_devia_20261022.py [--dry-run]
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DRY = '--dry-run' in sys.argv
MARK = '<!-- lien-devia -->'

PATCHES = {
    'servicios.html': [(
        '  <h2>Redes sociales, bajo petición</h2>\n',
        f'''  {MARK}
  <h2>App de presupuestos Metrado — 3 gratis</h2>
  <p>Si eres tú quien prepara los presupuestos para tus clientes, Metrado te ayuda a hacerlos desde el móvil: los dictas en la obra, pasas a limpio uno en papel o los escribes, y salen en PDF con tu logo, con el IVA y la retención de IRPF calculados al céntimo. Los 3 primeros presupuestos son gratis; después, 10 presupuestos por 12 € + IVA, sin suscripción, y los créditos no caducan. Todo sobre la <a href="/app-presupuestos/" style="color:var(--blue);font-weight:600">app para hacer presupuestos de obra y reformas</a>.</p>

  <h2>Redes sociales, bajo petición</h2>
''')],
    'en/services.html': [
        ('  <h2>Two more services</h2>\n  <p>Beyond our web design services, we offer two more:</p>\n',
         '  <h2>Three more services</h2>\n  <p>Beyond our web design services, we offer three more:</p>\n'),
        ('    <li><a href="/en/ai-visibility/">AI visibility check</a>',
         f'''    <li>{MARK}<a href="/en/quoting-app/">Metrado quoting app</a>: write quotes for your own clients on your phone, by voice or from a paper quote, with IVA and IRPF worked out to the cent; 3 free quotes, then 10 quotes for €12 + VAT, no subscription.</li>
    <li><a href="/en/ai-visibility/">AI visibility check</a>'''),
    ],
    'fr/prestations.html': [(
        '  <h2>Questions fréquentes</h2>\n',
        f'''  {MARK}
  <h2>Et pour vos propres devis : l'application Metrado</h2>
  <p>Vous êtes artisan et vous préparez vous-même les devis de vos clients ?
  Metrado vous permet de les faire sur votre téléphone : vous les dictez sur le
  chantier, vous remettez au propre un devis papier ou vous les saisissez, et ils
  sortent en PDF à votre logo, avec la TVA calculée au centime. Les 3 premiers
  devis sont gratuits ; ensuite, 10 devis pour 12 € HT, sans abonnement, et les
  crédits n'expirent pas. Découvrez l'<a href="/fr/application-devis-artisan/">application
  de devis pour artisans</a>.</p>

  <h2>Questions fréquentes</h2>
'''
    )],
}

for rel, reps in PATCHES.items():
    p = ROOT / rel
    s = p.read_text(encoding='utf-8')
    if MARK in s:
        print(f'[DEJA] {rel}')
        continue
    for old, new in reps:
        n = s.count(old)
        if n != 1:
            print(f'[ECHEC] {rel} : ancre trouvée {n} fois : {old[:60]!r}')
            break
        s = s.replace(old, new)
    else:
        if not DRY:
            p.write_text(s, encoding='utf-8')
        print(f'[OK] {rel}' + (' (essai à blanc)' if DRY else ''))
