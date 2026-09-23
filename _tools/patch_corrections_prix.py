# -*- coding: utf-8 -*-
"""Corrections d'offre et de prix, FR / ES / EN (23/09/2026, plan SEO FR-EN).

1. TVA / IVA / VAT (8 pages) : « la TVA est déductible pour les indépendants »
   était faux pour les activités exonérées (santé) et, en France, pour les
   micro-entrepreneurs en franchise en base.
2. Modifications :
   - FAQ de l'accueil (SPA, es / ca / en) : « modificaciones ilimitadas »
     -> une modification par mois (l'offre : ajustements illimités AVANT la
     mise en ligne, puis 1 modification par mois) ;
   - 7 pages métier, carte 349 € : « 30 días de modificaciones ilimitadas »
     -> « 1 modificación al mes incluida » (décision du 23/09 : mêmes services
     que l'abonnement).
3. /fr/tarifs : le paiement unique « ne couvre pas la maintenance au-delà de la
   première année » -> faux, mêmes services. Description JSON-LD de l'offre
   corrigée (l'hébergement n'est pas limité à la première année).
4. /fr/tarifs : le tableau comparatif passe aux prix FRANÇAIS relevés le 23/09
   (IONOS pack S 199 € + 45 € HT/mois, 12 mois ; Wix Light 14 € HT annuel),
   comme le comparatif français. Totaux et calculateur recalculés.
5. Hostinger Espagne : 2,99 € -> 2,59 €/mois (48 mois), renouvellement 9,99 €,
   coût 24 mois 84 € -> 74 € sur /precios, /en/pricing et
   /mejores-creadores-paginas-web-autonomos.
6. Calculateurs : la colonne 15 €/mois affichait 384 € au chargement, puis
   385 € dès qu'on touchait au taux horaire (372 + 0,5 h x 25 € = 384,5,
   arrondi à 385). Valeur de départ alignée sur le calcul.

Sauvegarde : ~/webautonomos-work/backups/corrections_prix_<date>/
Abandon total, rien d'écrit, si une vérification échoue.

À lancer depuis ~/webautonomos, APRÈS git pull (index.html est modifié) :
    python3 _tools/patch_corrections_prix.py
"""
import datetime
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NNBSP = '\u202f'  # espace fine insécable, comme dans le tableau


def abandon(msg):
    sys.exit('ABANDON : %s\nRien n\'a été modifié.' % msg)


# ─── 1. TVA ──────────────────────────────────────────────────────────────────
TVA_FR = ('<p class="tax-note">Prix hors taxes. La TVA est déductible pour les indépendants et les entreprises.</p>',
          '<p class="tax-note">Prix hors taxes. La plupart des entreprises récupèrent la TVA ; ce n\'est pas le cas '
          'en franchise en base de TVA (micro-entrepreneurs) ni pour les activités exonérées, comme la santé.</p>')
TVA_ES = ('<p class="tax-note">Precios sin IVA. Para autónomos y empresas, el IVA es deducible.</p>',
          '<p class="tax-note">Precios sin IVA. La mayoría de autónomos y empresas pueden deducirlo; '
          'las actividades exentas de IVA, como las sanitarias, no.</p>')
TVA_EN = ('<p class="tax-note">Prices exclude VAT. VAT is deductible for freelancers and companies.</p>',
          '<p class="tax-note">Prices exclude Spanish VAT (IVA, 21%). Most autónomos and companies can deduct it; '
          'some activities that are exempt from VAT, such as healthcare, cannot.</p>')

# ─── 2. modifications ────────────────────────────────────────────────────────
SPA = [
    ('incluyendo modificaciones ilimitadas para adaptar tu web a medida que crece tu negocio.',
     'con una modificación al mes incluida para adaptar tu web a medida que crece tu negocio.'),
    ('incloent modificacions il·limitades per a adaptar la teua web a mesura que creix el teu negoci.',
     'amb una modificació al mes inclosa per a adaptar la teua web a mesura que creix el teu negoci.'),
    ('including unlimited modifications to adapt your website as your business grows.',
     'with one change a month included to adapt your website as your business grows.'),
]
METIERS = ['dentistas', 'psicologos', 'fontaneros', 'carpinteros', 'fisioterapeutas', 'reformas', 'electricistas']
METIER = ('<li>30 días de modificaciones ilimitadas</li>', '<li>1 modificación al mes incluida</li>')

# ─── 3 et 4. /fr/tarifs ──────────────────────────────────────────────────────
UNIQUE_AVANT = ("L'abonnement inclut en outre la maintenance continue, que le paiement unique ne couvre pas "
                "au-delà de la première année.")
UNIQUE_APRES = "Les deux formules comprennent les mêmes services, dont la maintenance et une modification par mois."
FR_TARIFS = [
    ('"description": "Site internet professionnel livré en paiement unique, hébergement et nom de domaine inclus la première année."',
     '"description": "Le même site en paiement unique, avec les mêmes services que l\'abonnement. Hébergement et SSL '
     'compris ; le nom de domaine se renouvelle à partir de la deuxième année, pour environ 12 € par an."'),
    ('<caption>Tarifs publics relevés le 5 septembre 2026, hors taxes.',
     '<caption>Tarifs publics français relevés le 23 septembre 2026, hors taxes (Wix : 16,80 € TTC publiés par '
     'Wix France, soit 14 € HT).'),
    ('<th>IONOS<br>Design S</th><th>Wix Core</th><th>Hostinger<br>Premium</th>',
     '<th>IONOS<br>pack S</th><th>Wix Light</th><th>Hostinger<br>Premium</th>'),
    ('<td>25 €, puis 40 €</td><td>20 € annuel</td>',
     '<td>45 €</td><td>14 € annuel</td>'),
    ('<td>Inclus</td><td>Offert 1re année, 8–15 €/an</td><td>Offert 1re année, 8–15 €/an</td>',
     '<td>Inclus</td><td>Offert 1re année, 15–25 €/an</td><td>Offert 1re année, 8–15 €/an</td>'),
    ('<td>Selon contrat</td><td>12 mois</td><td>48 mois</td>',
     '<td>12 mois</td><td>12 mois</td><td>48 mois</td>'),
    # IONOS : 199 + 45 x 24 = 1 279 € ; 2 h à 25 €/h -> 1 329 €
    ('data-base="1069"><strong>1' + NNBSP + '119 &euro;</strong>',
     'data-base="1279"><strong>1' + NNBSP + '329 &euro;</strong>'),
    # Wix Light : 14 x 24 + 15 (domaine 2e année) = 351 € ; 20 h à 25 €/h -> 851 €
    ('data-base="492"><strong>992 &euro;</strong>',
     'data-base="351"><strong>851 &euro;</strong>'),
]

# ─── 5. Hostinger Espagne ────────────────────────────────────────────────────
# 2,59 x 24 + 12 (domaine 2e année) = 74 € ; 27 h à 25 €/h -> 749 €
PRECIOS = [
    ('<td>2,99 € (48 meses)</td>', '<td>2,59 € (48 meses)</td>'),
    ('data-base="84"><strong>759 &euro;</strong>', 'data-base="74"><strong>749 &euro;</strong>'),
]
PRECIOS_DATE = ('Precios de tarifa sin IVA, consultados el 5 de septiembre de 2026.',
                'Precios de tarifa sin IVA, consultados el 5 de septiembre de 2026 (Hostinger, el 23 de septiembre).')
EN_PRICING = [
    ('<td>€2.99 (48 months)</td>', '<td>€2.59 (48 months)</td>'),
    ('data-base="84"><strong>€759</strong>', 'data-base="74"><strong>€749</strong>'),
    ('<caption>Public list prices checked on 5 September 2026, excluding VAT.',
     '<caption>Public list prices checked on 5 September 2026 (Hostinger on 23 September), excluding VAT.'),
]
ES_CMP = [
    ('Tarifas consultadas el 14 de septiembre de 2026, sin IVA.',
     'Tarifas consultadas entre el 14 y el 23 de septiembre de 2026, sin IVA.'),
    ('<td>2,99 €/mes*</td>', '<td>2,59 €/mes*</td>'),
    ('<td><strong>84 €</strong><br>+ tu tiempo</td>', '<td><strong>74 €</strong><br>+ tu tiempo</td>'),
    ('*El precio promocional de Hostinger exige contratar 48 meses; la renovación sube después a entre 11 y 25 €/mes.',
     '*El precio promocional de Hostinger exige pagar 48 meses por adelantado (124,32 €); la renovación sube después a 9,99 €/mes.'),
    ('Sobre el papel es imbatible: 2,99 € al mes.', 'Sobre el papel es imbatible: 2,59 € al mes.'),
    ('Ese precio exige contratar 48 meses por adelantado, y la renovación posterior sube a entre 11 y 25 € mensuales.',
     'Ese precio exige pagar 48 meses por adelantado, 124,32 €, y la renovación posterior sube a 9,99 € mensuales.'),
    ('84 € con Hostinger', '74 € con Hostinger'),
]


TOTAL_384 = 'data-col="1" data-base="372" data-h="0.5"><strong>%s</strong>'


def plan():
    """Retourne {chemin: [(ancien, nouveau, nombre attendu), ...]}."""
    p = {}
    add = lambda rel, a, b, n=1: p.setdefault(rel, []).append((a, b, n))
    for rel in ('fr/tarifs.html', 'fr/prestations.html', 'fr/questions.html'):
        add(rel, *TVA_FR)
    for rel in ('precios.html', 'servicios.html', 'preguntas.html', 'pide-tu-demo.html'):
        add(rel, *TVA_ES)
    add('en/faq.html', *TVA_EN)
    for a, b in SPA:
        add('index.html', a, b)
    for m in METIERS:
        add('%s/index.html' % m, *METIER)
    add('fr/tarifs.html', UNIQUE_AVANT, UNIQUE_APRES, 2)      # JSON-LD + <dd>
    for a, b in FR_TARIFS:
        add('fr/tarifs.html', a, b)
    for a, b in PRECIOS:
        add('precios.html', a, b)
    add('precios.html', PRECIOS_DATE[0], PRECIOS_DATE[1], 2)  # JSON-LD + <p>
    for a, b in EN_PRICING:
        add('en/pricing.html', a, b)
    for a, b in ES_CMP:
        add('mejores-creadores-paginas-web-autonomos.html', a, b)
    for rel, (a, b) in (('precios.html', ('384 &euro;', '385 &euro;')), ('fr/tarifs.html', ('384 &euro;', '385 &euro;')),
                        ('en/pricing.html', ('€384', '€385'))):
        add(rel, TOTAL_384 % a, TOTAL_384 % b)
    return p


def scripts_js(s):
    return [m.group(2) for m in re.finditer(r'<script(\s[^>]*)?>(.*?)</script>', s, re.S)
            if 'ld+json' not in (m.group(1) or '') and 'src=' not in (m.group(1) or '') and m.group(2).strip()]


def node_ok(codes):
    with tempfile.TemporaryDirectory() as tmp:
        for i, js in enumerate(codes):
            f = os.path.join(tmp, 's%d.js' % i)
            open(f, 'w', encoding='utf-8').write(js)
            r = subprocess.run(['node', '--check', f], capture_output=True, text=True)
            if r.returncode:
                return 'script %d : %s' % (i, r.stderr.strip()[:200])
    return None


def balises(s):
    v = re.sub(r'<!--.*?-->', '', s, flags=re.S)
    v = re.sub(r'<(script|style)\b.*?</\1>', '', v, flags=re.S)
    return {t: (len(re.findall(r'<%s[\s>]' % t, v)), v.count('</%s>' % t))
            for t in ('div', 'p', 'a', 'table', 'tr', 'td', 'th', 'ul', 'li', 'dl', 'dt', 'dd', 'h2', 'section')}


def main():
    os.chdir(ROOT)
    p = plan()
    nouveaux, err = {}, []
    for rel, rempl in p.items():
        if not os.path.isfile(rel):
            abandon('%s introuvable.' % rel)
        s0 = open(rel, encoding='utf-8').read()
        s = s0
        for a, b, n in rempl:
            k = s.count(a)
            if k != n:
                if s.count(b) == n:
                    err.append('%s : déjà corrigé (%s…)' % (rel, b[:50]))
                else:
                    err.append('%s : ancre trouvée %dx au lieu de %d : %s' % (rel, k, n, a[:70]))
                continue
            s = s.replace(a, b)
        if balises(s) != balises(s0):
            err.append('%s : équilibre des balises modifié' % rel)
        for bloc in re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
            try:
                json.loads(bloc)
            except ValueError as exc:
                err.append('%s : JSON-LD invalide (%s)' % (rel, exc))
        nouveaux[rel] = (s0, s)
    if err:
        abandon('vérifications :\n  - ' + '\n  - '.join(err))

    # scripts de la page d'accueil (SPA) et des pages à calculateur
    for rel in ('index.html', 'fr/tarifs.html', 'precios.html', 'en/pricing.html'):
        e = node_ok(scripts_js(nouveaux[rel][1]))
        if e:
            abandon('%s : JavaScript invalide après modification — %s' % (rel, e))

    stamp = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
    bak = os.path.expanduser('~/webautonomos-work/backups/corrections_prix_%s' % stamp)
    for rel in nouveaux:
        d = os.path.join(bak, rel)
        os.makedirs(os.path.dirname(d), exist_ok=True)
        shutil.copy2(rel, d)
    for rel, (_, s) in nouveaux.items():
        open(rel, 'w', encoding='utf-8').write(s)
        print('  ✓ %-46s %d correction(s)' % (rel, sum(n for _, _, n in p[rel])))
    print('\nOK — %d fichiers corrigés. Sauvegarde : %s' % (len(nouveaux), bak.replace(os.path.expanduser('~'), '~')))
    print('Étape suivante : npx wrangler deploy')


if __name__ == '__main__':
    main()
