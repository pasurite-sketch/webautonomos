# -*- coding: utf-8 -*-
"""Blog (ES/EN/FR/VAL, fichiers statiques + données SPA de index.html) : retire les
promesses fausses sur l'offre, validé par Angelino le 25/09/2026 au soir.

- SEO local « inclus dans les 15 €/mois » : faux. Le site comprend un SEO de base ;
  SEO Local 15 €/mois + IVA et fiche Google 29 €/mois + IVA sont des services à part.
- « modifications illimitées » : faux, une modification par mois.
- « intégrations avancées incluses sans coût » : faux, phrase retirée.
- email professionnel « inclus sans rien payer de plus » : faux, sur demande.
- FR : domaine « compris » sans préciser qu'il l'est la première année.
- /fr/tarifs : « Le prix affiché est le prix payé » → prix hors taxes.
Rien d'autre n'est touché dans le blog. Idempotent. Depuis la racine du dépôt.
"""
import glob
import json
import re

R = [
    # --- ES
    ('En WebAutonomos ofrecemos SEO local incluido en nuestra tarifa de 15€/mes: optimización de tu ficha de Google, web optimizada para búsquedas locales y posicionamiento en tu zona.',
     'En WebAutonomos, tu web ya incluye una optimización SEO básica, y ofrecemos SEO Local por 15 €/mes + IVA (4 artículos al mes, palabras clave locales e informe mensual) y la gestión de tu ficha de Google por 29 €/mes + IVA.'),
    ('En WebAutonomos incluimos SEO local en nuestro servicio de 15€/mes, y también ofrecemos gestión de Google My Business para que aparezcas en Google Maps.',
     'En WebAutonomos, la web de 15 €/mes incluye una optimización SEO básica; el SEO Local (15 €/mes + IVA) y la gestión de tu ficha de Google (29 €/mes + IVA) son servicios aparte.'),
    ('incluyendo modificaciones ilimitadas para adaptar tu web', 'con una modificación al mes incluida para adaptar tu web'),
    (' Las integraciones avanzadas están incluidas en nuestro servicio de modificaciones, sin coste adicional. Solo tienes que pedirlo.', ''),
    ('En WebAutonomos configuramos tu correo profesional como parte del servicio de creación de tu sitio web, en los 15€/mes. No pagas nada extra.',
     'No está incluido en los 15 €/mes, pero podemos configurarlo con tu dominio si nos lo pides.'),
    # --- EN
    ('At WebAutonomos we offer local SEO included in our €15/month rate: Google Business Profile optimization, locally-optimized website and positioning in your area.',
     'At WebAutonomos your website already includes basic SEO, and we offer Local SEO for €15/month + VAT (4 blog articles a month, local keywords and a monthly report) and Google Business Profile management for €29/month + VAT.'),
    ('At WebAutonomos we include local SEO in our €15/month service, and we also offer Google My Business management so you appear on Google Maps.',
     'At WebAutonomos the €15/month website includes basic SEO; Local SEO (€15/month + VAT) and Google Business Profile management (€29/month + VAT) are separate services.'),
    ('including unlimited modifications to adapt your website', 'with one change a month included to adapt your website'),
    (' Advanced integrations are included in our modification service, at no additional cost. Just ask for it.', ''),
    ('At WebAutonomos we set up your professional email as part of the website creation service, in the €15/month. You pay nothing extra.',
     'It is not included in the €15/month, but we can set it up with your domain if you ask us.'),
    # --- FR
    ('Chez WebAutonomos, le SEO local est inclus dans notre forfait à 15 €/mois : optimisation de votre fiche Google, site optimisé pour les recherches locales et positionnement dans votre zone.',
     'Chez WebAutonomos, votre site comprend déjà une optimisation SEO de base, et nous proposons le SEO local à 15 €/mois HT (4 articles de blog par mois, mots-clés locaux et rapport mensuel) et la gestion de votre fiche Google à 29 €/mois HT.'),
    ('Chez WebAutonomos, le SEO local est compris dans notre offre à 15 €/mois, et nous proposons aussi la gestion de Google My Business pour apparaître sur Google Maps.',
     'Chez WebAutonomos, le site à 15 €/mois comprend une optimisation SEO de base ; le SEO local (15 €/mois HT) et la gestion de votre fiche Google (29 €/mois HT) sont des services à part.'),
    ('modifications illimitées comprises pour faire évoluer', 'avec une modification par mois comprise pour faire évoluer'),
    (' Les intégrations avancées font partie de notre service de modifications, sans coût supplémentaire. Il suffit de le demander.', ''),
    ('Chez WebAutonomos, nous configurons la vôtre dans le cadre de la création de votre site, dans les 15 €/mois. Vous ne payez rien de plus.',
     'Elle n’est pas comprise dans les 15 €/mois, mais nous pouvons la configurer avec votre domaine si vous nous le demandez.'),
    ('Avec WebAutonomos, le domaine est compris dans votre abonnement à 15 €/mois :',
     'Avec WebAutonomos, le domaine est compris la première année dans votre abonnement à 15 €/mois (environ 12 €/an ensuite) :'),
    ('15 € par mois chez WebAutonomos, maintenance comprise. Le prix affiché est le prix payé.',
     '15 € par mois chez WebAutonomos, maintenance comprise. Les prix affichés sont hors taxes.'),
    # --- VAL
    ('En WebAutonomos oferim SEO local inclòs en la nostra tarifa de 15€/mes: optimització de la teua fitxa de Google, web optimitzada per a cerques locals i posicionament en la teua zona.',
     'En WebAutonomos, la teua web ja inclou una optimització SEO bàsica, i oferim SEO Local per 15 €/mes + IVA (4 articles al mes, paraules clau locals i informe mensual) i la gestió de la teua fitxa de Google per 29 €/mes + IVA.'),
    ('incloent modificacions il·limitades per a adaptar', 'amb una modificació al mes inclosa per a adaptar'),
    (' Les integracions avançades estan incloses en el nostre servei de modificacions, sense cost addicional. Només has de demanar-ho.', ''),
    ('En WebAutonomos configurem el teu correu professional com a part del servei de creació del teu lloc web, en els 15€/mes. No pagues res extra.',
     'No està inclòs en els 15 €/mes, però podem configurar-lo amb el teu domini si ens ho demanes.'),
]

FICHIERS = sorted(glob.glob('blog/*/*.html')) + ['index.html', 'fr/tarifs.html']
total = 0
for f in FICHIERS:
    s = open(f, encoding='utf-8').read()
    avant = s
    for ancien, nouveau in R:
        n = s.count(ancien)
        if n:
            s = s.replace(ancien, nouveau)
            total += n
            print(f'{n} remplacé(s)  {f} : {ancien[:70]}')
    if s != avant:
        if f != 'index.html':  # les JSON-LD des fichiers statiques doivent rester valides
            for m in re.findall(r'(?is)<script type="application/ld\+json">(.*?)</script>', s):
                json.loads(m)
        open(f, 'w', encoding='utf-8').write(s)
print('total :', total)
