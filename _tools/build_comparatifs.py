# -*- coding: utf-8 -*-
"""Plan SEO FR-EN, phase 2 — comparatifs « meilleurs créateurs de sites » en
français et en anglais (23/09/2026).

Crée :
  en/best-website-builders-for-freelancers-in-spain.html
      marché espagnol (anglophones installés en Espagne), mêmes options que la
      page espagnole ; Hostinger revérifié le 23/09 (2,59 €, renouvellement
      9,99 €).
  fr/meilleurs-createurs-de-sites-pour-independants.html
      marché français : Wix, Hostinger, Jimdo, Webnode, Squarespace, et les
      services qui font le site (IONOS, Simplébo), tarifs relevés le 23/09 sur
      les sites des fournisseurs. Wix : 16,80 € TTC publiés par Wix France
      (mai 2026), soit 14 € HT.

Modifie :
  mejores-creadores-paginas-web-autonomos.html
      - hreflang es-ES / en / fr / x-default ;
      - Weebly : l'Espagne n'est PAS dans les 67 pays (la page laissait croire
        le contraire), section et FAQ corrigées ;
      - Webnode : le multilingue commence au forfait Standard, pas au gratuit ;
      - dateModified.
  precios.html, fr/tarifs.html, en/pricing.html
      - colonne 349 € : « Modificaciones / Modifications » = 1 par mois
        (décision d'Angelino du 23/09 : mêmes services que l'abonnement) ;
      - lien vers le comparatif de leur langue.
  fr/tarifs.html, fr/prestations.html, fr/questions.html, demandez-votre-demo.html
      - « Contact » du pied de page : /contacto (espagnol) -> formulaire FR.
  _tools/build_lang_homes.py
      - lien « Comparer toutes les options » sous le bloc Comparer de /fr/ et /en/.
  llms.txt
      - les trois comparatifs.

Puis relance build_lang_homes.py et generate_sitemap.py.

Sauvegarde : ~/webautonomos-work/backups/comparatifs_<date>/
Abandon total, rien d'écrit, si une vérification échoue.

À lancer depuis ~/webautonomos :
    python3 _tools/build_comparatifs.py
"""
import datetime
import html
import json
import os
import re
import shutil
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = 'https://webautonomos.es'

ES = 'mejores-creadores-paginas-web-autonomos.html'
FR = 'fr/meilleurs-createurs-de-sites-pour-independants.html'
EN = 'en/best-website-builders-for-freelancers-in-spain.html'
URL_ES = BASE + '/mejores-creadores-paginas-web-autonomos'
URL_FR = BASE + '/fr/meilleurs-createurs-de-sites-pour-independants'
URL_EN = BASE + '/en/best-website-builders-for-freelancers-in-spain'
WEEBLY = 'https://www.weebly.com/app/help/us/en/topics/changes-to-weebly-global-operations'
CODEUR = 'https://www.codeur.com/pages/quel-prix-site-vitrine'
DATE = '2026-09-23'

HREFLANG = '\n'.join([
    '<link rel="alternate" hreflang="es-ES" href="%s">' % URL_ES,
    '<link rel="alternate" hreflang="en" href="%s">' % URL_EN,
    '<link rel="alternate" hreflang="fr" href="%s">' % URL_FR,
    '<link rel="alternate" hreflang="x-default" href="%s">' % URL_ES,
])

ORG = {"@type": "Organization", "@id": BASE + "/#organization", "name": "WebAutonomos", "url": BASE + "/"}


def abandon(msg):
    sys.exit('ABANDON : %s\nRien n\'a été modifié.' % msg)


def lire(rel):
    return open(os.path.join(ROOT, rel), encoding='utf-8').read()


E = lambda x: html.escape(x, quote=True)

TRACK = """<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-MT6S7CH7N9"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-MT6S7CH7N9');
</script>
<!-- Microsoft Clarity -->
<script type="text/javascript">
  (function(c,l,a,r,i,t,y){
    c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};
    t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;
    y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);
  })(window, document, "clarity", "script", "wb9354sv4p");
</script>"""

CSS_PLUS = """<style>
.brief{background:#f4fbf7;border:1px solid #d1e8d9;border-radius:10px;padding:14px 16px;margin:0 0 24px;font-size:1rem;line-height:1.65;max-width:none}
.check p{margin-bottom:14px}
.updated{font-size:.85rem;color:#64748b;margin-top:28px}
.cmp.svc col.lbl{width:24%}.cmp.svc col.c{width:15.2%}.cmp.svc td:first-child{word-break:normal;overflow-wrap:normal;hyphens:none}
</style>"""

FOOTERS = {
    'en': ('/en/', [('/aviso-legal/', 'Legal notice'), ('/privacidad/', 'Privacy'),
                    ('/en/contact', 'Contact'), ('/blog/#en', 'Blog')]),
    'fr': ('/fr/', [('/aviso-legal/', 'Mentions légales'), ('/privacidad/', 'Confidentialité'),
                    ('/demandez-votre-demo#pide-demo', 'Contact'), ('/blog/#fr', 'Blog')]),
}


def footer(lang):
    home, links = FOOTERS[lang]
    return ('<footer>\n  <a class="fl" href="%s"><span>&#127760;</span> webautonomos.es</a>\n'
            '  <div class="flinks">\n%s\n  </div>\n'
            '  <address class="fnap">\n    <strong>WebAutonomos</strong>\n'
            '    <span>Calle Pintor Josep Segrelles, 26</span>\n    <span>46870 Ontinyent, Valencia</span>\n'
            '    <a href="tel:+34961877356">+34 961 877 356</a>\n'
            '    <a href="mailto:info@webautonomos.es">info@webautonomos.es</a>\n  </address>\n</footer>') % (
        home, '\n'.join('    <a href="%s">%s</a>' % (h, t) for h, t in links))


def texte(x):
    return html.unescape(re.sub(r'<[^>]+>', '', x))


def table(head, rows, me_rows=(), caption='', cls='cmp'):
    cols = '<colgroup><col class="lbl">' + '<col class="c">' * (len(head) - 1) + '</colgroup>'
    th = ''.join('<th>%s</th>' % h for h in head)
    body = ''
    for n, r in enumerate(rows):
        tr = ' class="me"' if n in me_rows else ''
        body += '      <tr%s>%s</tr>\n' % (tr, ''.join('<td>%s</td>' % c for c in r))
    cap = '<caption>%s</caption>' % caption if caption else ''
    return ('  <div class="cmp-wrap">\n  <table class="%s">%s\n    %s\n    <thead><tr>%s</tr></thead>\n'
            '    <tbody>\n%s    </tbody>\n  </table>\n  </div>') % (cls, cap, cols, th, body)


def dl(faq):
    return '  <dl class="qa">\n' + '\n'.join('    <dt>%s</dt>\n    <dd>%s</dd>' % (q, a) for q, a in faq) + '\n  </dl>'


def page(lang, url, title, desc, locale, crumb, h1, body, faq, css):
    faq_ld = {"@context": "https://schema.org", "@type": "FAQPage", "inLanguage": lang,
              "mainEntity": [{"@type": "Question", "name": texte(q),
                              "acceptedAnswer": {"@type": "Answer", "text": texte(a)}} for q, a in faq]}
    art = {"@context": "https://schema.org", "@type": "Article", "headline": texte(h1),
           "description": desc, "datePublished": DATE, "dateModified": DATE, "inLanguage": lang,
           "mainEntityOfPage": {"@type": "WebPage", "@id": url}, "author": ORG, "publisher": ORG}
    home = BASE + FOOTERS[lang][0]
    bc = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": crumb[0], "item": home},
        {"@type": "ListItem", "position": 2, "name": crumb[1], "item": url}]}
    ld = '\n'.join('<script type="application/ld+json">\n%s\n</script>' % json.dumps(x, ensure_ascii=False, indent=2)
                   for x in (art, faq_ld, bc))
    return """<!DOCTYPE html>
<html lang="%(lang)s">
<head>
%(track)s
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%(title)s</title>
<meta name="description" content="%(desc)s">
<link rel="canonical" href="%(url)s">
%(hreflang)s
<meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large">
<meta property="og:type" content="article">
<meta property="og:url" content="%(url)s">
<meta property="og:title" content="%(title)s">
<meta property="og:description" content="%(desc)s">
<meta property="og:image" content="%(base)s/og-image.png">
<meta property="og:locale" content="%(locale)s">
<meta property="og:site_name" content="WebAutonomos">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,400;12..96,600;12..96,800&family=DM+Sans:wght@400;500;600&display=swap" rel="stylesheet">
%(css)s
%(css_plus)s
%(ld)s
</head>
<body>

<main>
  <p class="crumb"><a href="%(home_rel)s">%(c0)s</a> &rsaquo; %(c1)s</p>
  <h1>%(h1)s</h1>
%(body)s
</main>

%(footer)s
</body>
</html>
""" % dict(lang=lang, track=TRACK, title=E(title), desc=E(desc), url=url, hreflang=HREFLANG,
           base=BASE, locale=locale, css=css, css_plus=CSS_PLUS, ld=ld, home_rel=FOOTERS[lang][0],
           c0=E(crumb[0]), c1=E(crumb[1]), h1=h1, body=body, footer=footer(lang))


# ═══════════════════════════════ ANGLAIS (Espagne) ══════════════════════════
EN_FAQ = [
    ("What is the best way to get a website as a freelancer in Spain in 2026?",
     "It depends on your time. If you have ten to forty hours, a builder such as Wix or Hostinger is cheaper in money. "
     "If you don't, a done-for-you service costs less overall: WebAutonomos is €15 a month with no setup fee or lock-in, "
     "or €349 once, and we build the site in 24 hours."),
    ("Can I get a free website for my business?",
     "Yes. Webnode and Jimdo have genuinely free plans with no time limit. The catch is that you work on a subdomain, "
     "not your own domain name, and storage is limited. It is fine for testing; for a business that wants to appear "
     "on Google, it falls short."),
    ("How much does a website really cost over two years?",
     "With the domain included and excluding VAT: €74 with Hostinger, €361 with the WebAutonomos one-off payment, "
     "€372 with the WebAutonomos monthly plan, €492 with Wix Core, €1,069 with the IONOS Design Service and €2,200 "
     "to €10,800 with an agency. With Hostinger or Wix, add ten to forty hours of your own work."),
    ("Does my website need a Spanish legal notice if it is in English?",
     "Yes, if your business is established in Spain. The LSSI applies to service providers established in Spain "
     "whatever the language of the site: you need a legal notice (aviso legal), a privacy policy and cookie consent."),
    ("Is Weebly closing in Spain?",
     "No. Square is closing Weebly in 67 countries, with sites taken offline on 27 September 2026, but Spain and the "
     "United Kingdom are not on the list."),
]

EN_BODY = """  <p class="lede">There is no single right answer: it depends on how much time you have and whether you want to build the site yourself. We compare the website builders most used in Spain and the options where someone builds it for you, which most comparisons leave out. Prices checked between 14 and 23 September 2026, excluding Spanish VAT (IVA).</p>
  <p class="brief"><strong>In short:</strong> if you have ten to forty hours to spare, a builder is cheapest in money: Hostinger from €2.59 a month, Wix Core at €20. If you don't, a done-for-you service costs less overall: WebAutonomos builds your site for €15 a month with no setup fee or lock-in, or €349 once, with the legal pages Spanish law requires.</p>

%(table)s
  <p class="tax-note">*Hostinger's promotional price requires paying 48 months upfront (€124.32) and then renews at €9.99 a month. The 24-month cost includes the domain renewal in the second year (about €12), except for the free option, which uses a subdomain. Prices exclude VAT.</p>
  <p><a href="/en/pricing">Work out the real cost with your own hourly rate →</a></p>

  <h2>Best free option: Webnode or Jimdo</h2>
  <p>Both have a genuinely free plan with no time limit. Jimdo is the quickest: answer a few questions about your business and it hands you a site ready to adjust. Webnode lets you add a second language later, but multi-language starts with its Standard plan, not the free one. The limit is the same on both: you work on a subdomain such as yourbusiness.jimdosite.com, not your own domain name, and storage is limited. It is fine for testing, not for competing on Google.</p>

  <h2>Best paid builder: Wix Core</h2>
  <p>It is the most complete builder on the market, with the widest choice of templates. €20 a month on annual billing, €25 if you pay month to month, with the domain name free for the first year. In exchange, you build the site yourself: allow ten to thirty hours if you have never done it, and the result depends on your eye for design and on what you write.</p>

  <h2>Best price with hosting: Hostinger Premium</h2>
  <p>On paper it is unbeatable: €2.59 a month. The small print matters. That price requires paying 48 months upfront, €124.32, and the plan then renews at €9.99 a month. It is still the cheapest option in money, but you build the site yourself, and that means fifteen to forty hours of work.</p>

  <h2>Best done-for-you service: WebAutonomos</h2>
  <p>This is our own category, and we pick ourselves for one specific reason: among services where someone builds the website for you, €15 a month with no setup fee and no lock-in is the lowest price we have found in Spain. The IONOS Design Service, the most direct comparison, charges €199 to set up, then €25 a month for the first six months and €40 after that: €1,069 over two years, against €372. We write the copy from the real information on your Google Business Profile, add your photos and build the site within 24 hours. It is not a template you fill in yourself.</p>
  <p><a href="/en/services">See what the €15/month plan includes →</a></p>

  <h2>Best if you want to own it: the €349 one-off payment</h2>
  <p>If you would rather not pay monthly, the same website costs €349 once, with the same services. From the second year you only pay the domain renewal, about €12 a year. Over two years that is €361, eleven euros less than the monthly plan, and the gap widens from the third year. The trade-off is that you pay before you start using it, although the demo is still free.</p>

  <h2>Best for a custom project: a local agency</h2>
  <p>If you need an online shop with thousands of products, an integration with your management software or a full brand design, none of the options above will do. That is where an agency makes sense: €1,000 to €6,000 upfront, plus €50 to €200 a month for maintenance. It is not expensive for the sake of it; it is a different kind of job.</p>

  <h2>Three things English speakers in Spain should check</h2>
  <div class="check">
  <p><strong>The Spanish legal pages.</strong> If your business is established in Spain, your website must show a legal notice (aviso legal), a privacy policy and a cookie policy, whatever language it is in. A builder gives you the tools; the text with your NIF or NIE, your address and your registration details is still yours to write. <a href="/en/web-design-for-expats-in-spain">What they must contain</a>.</p>
  <p><strong>The language you get help in.</strong> Wix, Hostinger, Jimdo and Webnode all have an English interface. A local Spanish agency may not work in English, and a website project means a lot of back-and-forth.</p>
  <p><strong>A second language.</strong> Many customers in Spain will look for you in Spanish. If you need the site in two languages, check which plan includes it before you start: on Webnode, for example, it starts with the Standard plan.</p>
  </div>

  <h2>A note on Weebly</h2>
  <p>Square announced in June 2026 that it is closing Weebly in 67 countries, where sites are taken offline on 27 September 2026. Spain and the United Kingdom are not on the list, so Weebly sites in Spain keep working (<a href="%(weebly)s" rel="noopener">Weebly's announcement</a>). It is still a reminder of a real risk: if a platform closes or changes its terms, your website goes with it. With the domain name registered in your name, you at least keep your address.</p>

  <h2>How to choose in two questions</h2>
  <p>First: do you have ten to forty hours to spend on it? If you do, a builder is cheaper. If you don't, the builder's price is misleading, because the time you don't have also costs money. Second: do you want to be able to change provider without starting again? Then make sure the domain name is registered in your name, whichever option you choose.</p>

  <h2>Frequently asked questions</h2>
%(faq)s

  <div class="actions">
    <a class="btn btn-primary" href="/get-your-demo#pide-demo">Get my free demo</a>
    <a class="btn btn-ghost" href="/en/pricing">See our pricing</a>
  </div>
  <p class="updated">Updated: September 2026</p>"""

EN_TABLE = table(
    ['Profile', 'Our pick', 'From', 'Who builds it', 'Your time', '24-month cost'],
    [['Start for free', 'Webnode or Jimdo', '€0', 'You', '10–20 h', '<strong>€0</strong><br>with a subdomain'],
     ['Paid builder', 'Wix Core', '€20/month, annual', 'You', '10–30 h', '<strong>€492</strong><br>+ your time'],
     ['Lowest price', 'Hostinger Premium', '€2.59/month*', 'You', '15–40 h', '<strong>€74</strong><br>+ your time'],
     ['Done for you', 'WebAutonomos', '€15/month', 'Us', '~30 minutes', '<strong>€372</strong>'],
     ['Pay once', 'WebAutonomos one-off', '€349 once', 'Us', '~30 minutes', '<strong>€361</strong>'],
     ['Custom project', 'Local agency', '€1,000–6,000', 'The agency', 'Meetings', '<strong>€2,200–10,800</strong>']],
    me_rows=(3, 4))

# ═══════════════════════════════ FRANÇAIS (France) ══════════════════════════
FR_FAQ = [
    ("Quel est le meilleur créateur de site pour un indépendant en 2026 ?",
     "Tout dépend de votre temps. Si vous avez dix à quarante heures, un créateur comme Wix ou Hostinger coûte moins "
     "cher en argent. Sinon, un service qui fait le site pour vous revient moins cher au total : WebAutonomos coûte "
     "15 € HT par mois sans frais de mise en service ni engagement, ou 349 € HT en une fois, et le site est prêt en 24 heures."),
    ("Peut-on créer un site internet gratuitement ?",
     "Oui. Jimdo et Webnode ont de vrais forfaits gratuits, sans limite de durée. La limite : vous travaillez avec un "
     "sous-domaine, pas avec votre propre nom de domaine, et le stockage est réduit. C'est bien pour essayer ; pour une "
     "activité qui veut apparaître sur Google, c'est insuffisant."),
    ("Combien coûte vraiment un site sur deux ans ?",
     "Nom de domaine compris et hors taxes : 84 € avec Hostinger, 351 € avec Wix Light, 361 € avec le paiement unique "
     "de WebAutonomos, 372 € avec son abonnement, 1 279 € avec le pack S d'IONOS, 1 600 € avec le pack Crédibilité de "
     "Simplébo, et 1 000 à 4 000 € avec un freelance, maintenance en plus. Avec Hostinger ou Wix, ajoutez dix à "
     "quarante heures de votre travail."),
    ("Faut-il comparer les prix HT ou TTC ?",
     "TTC si vous êtes en franchise en base de TVA, comme beaucoup de micro-entrepreneurs : vous ne récupérez pas la "
     "TVA, ajoutez donc 20 % aux prix hors taxes. HT si votre entreprise récupère la TVA."),
    ("Weebly ferme-t-il en France ?",
     "Non. Square ferme Weebly dans 67 pays, où les sites sont dépubliés le 27 septembre 2026, mais la France "
     "métropolitaine n'est pas concernée. La Polynésie française et la Nouvelle-Calédonie le sont."),
]

FR_BODY = """  <p class="lede">Il n'y a pas une seule bonne réponse : tout dépend du temps dont vous disposez et de votre envie de faire le site vous-même. Nous comparons les créateurs de sites les plus utilisés en France et les services qui font le site à votre place, que la plupart des comparatifs laissent de côté. Tarifs relevés sur les sites des fournisseurs le 23 septembre 2026, hors taxes sauf mention contraire.</p>
  <p class="brief"><strong>En bref :</strong> si vous avez dix à quarante heures devant vous, un créateur de site coûte le moins cher en argent : Hostinger dès 2,99 € HT par mois, Wix Light à 14 €. Sinon, un service qui fait le site pour vous revient moins cher au total : WebAutonomos le crée pour 15 € HT par mois, sans frais de mise en service ni engagement, ou pour 349 € en une fois. Les autres services de ce type que nous avons comparés démarrent à 45 € par mois.</p>

%(table)s
  <p class="tax-note">*Le prix promotionnel d'Hostinger impose de payer 48 mois d'avance (143,52 € HT) ; le forfait se renouvelle ensuite à 9,99 € par mois. Wix France publie 16,80 € TTC par mois pour le forfait Light en paiement annuel (mai 2026). Le coût sur 24 mois inclut le renouvellement du nom de domaine la deuxième année (12 à 15 € environ), sauf pour l'option gratuite, qui fonctionne avec un sous-domaine.</p>
  <p><a href="/fr/tarifs">Calculez le coût réel avec votre propre taux horaire →</a></p>

  <h2>Meilleure option gratuite : Jimdo ou Webnode</h2>
  <p>Les deux proposent un vrai forfait gratuit, sans limite de durée. Jimdo est le plus rapide : vous répondez à quelques questions sur votre activité et il vous livre un site prêt à retoucher. Webnode permet d'ajouter une deuxième langue plus tard, mais le multilingue commence au forfait Standard, pas au gratuit. La limite est la même chez les deux : vous travaillez avec un sous-domaine du type votreactivite.jimdosite.com, pas avec votre propre nom de domaine, et le stockage est réduit. Pour avoir votre nom de domaine, comptez 12,10 € TTC par mois chez Jimdo (forfait Start, sur 12 mois) ou 6,90 € HT par mois chez Webnode (forfait Mini, en paiement annuel). C'est bien pour essayer, pas pour se battre sur Google.</p>

  <h2>Meilleur créateur payant : Wix</h2>
  <p>C'est le plus complet du marché et celui qui propose le plus de modèles. Le forfait Light coûte 14 € HT par mois en paiement annuel (16,80 € TTC), nom de domaine offert la première année, puis 14,95 à 24,95 € par an. En contrepartie, c'est vous qui construisez le site : comptez dix à trente heures si vous ne l'avez jamais fait, et le résultat dépend de votre œil pour la mise en page et de ce que vous écrivez. Alternative plus sobre : Squarespace, dont le forfait Basic coûte 12 € HT par mois en paiement annuel, 17 € au mois, sans forfait gratuit.</p>

  <h2>Meilleur prix avec hébergement : Hostinger Premium</h2>
  <p>Sur le papier, imbattable : 2,99 € HT par mois. Les petites lignes comptent. Ce prix impose de payer 48 mois d'avance, soit 143,52 € HT, et le forfait se renouvelle ensuite à 9,99 € par mois. Cela reste l'option la moins chère en argent, mais le site, c'est vous qui le faites : quinze à quarante heures de travail.</p>

  <h2>Meilleur service qui fait le site pour vous : WebAutonomos</h2>
  <p>C'est notre catégorie, et nous nous y plaçons pour une raison précise : parmi les services dont le prix est public, 15 € HT par mois sans frais de mise en service ni engagement est le plus bas que nous ayons trouvé. Voici les offres comparables, relevées sur leurs sites le 23 septembre 2026 :</p>
%(table2)s
  <p class="tax-note">Prix hors taxes. Simplébo propose aussi une formule sans engagement à 60 € par mois, avec un préavis de 90 jours. Le coût sur 24 mois comprend les frais de mise en service et le nom de domaine.</p>
  <p>Soyons justes : Simplébo inclut des modifications illimitées, et les packs M et L d'IONOS montent à cinq et sept pages. Solocal, de son côté, démarre à 64 € par mois pour une offre qui associe site et visibilité locale ; engagement et frais sont communiqués sur devis. Chez nous, nous rédigeons les textes à partir des informations réelles de votre fiche Google, plaçons vos photos et livrons le site en 24 heures. Ce n'est pas un modèle à remplir vous-même.</p>
  <p><a href="/fr/prestations">Voir ce que comprend l'offre à 15 €/mois →</a></p>

  <h2>Meilleure option pour être propriétaire : le paiement unique de 349 €</h2>
  <p>Si vous préférez éviter l'abonnement, le même site coûte 349 € HT en un seul paiement, avec les mêmes services. À partir de la deuxième année, vous ne payez que le renouvellement du nom de domaine, environ 12 € par an. Sur deux ans, cela fait 361 €, onze euros de moins que l'abonnement, et l'écart se creuse à partir de la troisième année. La contrepartie : vous payez avant d'utiliser le site, même si la démonstration reste gratuite.</p>

  <h2>Meilleur choix pour un projet sur mesure : un freelance ou une agence</h2>
  <p>Boutique en ligne avec des centaines de références, connexion à votre logiciel de gestion, identité visuelle complète : aucune des options précédentes ne suffit. Là, un prestataire sur mesure a du sens. Selon <a href="%(codeur)s" rel="noopener">Codeur.com</a>, un site vitrine réalisé par un freelance coûte environ 1 000 € pour un site « carte de visite », et 1 500 à 4 000 € pour un site sur mesure sous WordPress. Ce n'est pas cher par caprice : c'est un autre travail.</p>

  <h2>Hors taxes ou TTC ?</h2>
  <p>Les prix de ce comparatif sont hors taxes, sauf mention contraire. Si vous êtes en franchise en base de TVA, comme beaucoup de micro-entrepreneurs, vous ne récupérez pas la TVA : ajoutez 20 %% à tous les montants pour comparer ce que vous paierez vraiment.</p>

  <h2>Vous êtes installé en Espagne ?</h2>
  <p>Les tarifs espagnols diffèrent un peu : Hostinger y affiche par exemple 2,59 € HT par mois au lieu de 2,99 €. Surtout, votre site dépend alors de la loi espagnole, quelle que soit sa langue : aviso legal, politique de confidentialité et consentement aux cookies. <a href="/fr/site-internet-francophones-espagne">Ce que doit contenir le site d'une activité en Espagne</a>.</p>

  <h2>Un mot sur Weebly</h2>
  <p>Square a annoncé en juin 2026 la fermeture de Weebly dans 67 pays, où les sites sont dépubliés le 27 septembre 2026. La France métropolitaine, la Belgique, la Suisse, le Canada et l'Espagne ne sont pas concernés ; la Polynésie française, la Nouvelle-Calédonie, le Maroc, l'Algérie ou le Sénégal, si (<a href="%(weebly)s" rel="noopener">annonce de Weebly</a>). La leçon vaut pour toutes les plateformes : si elle ferme ou change ses conditions, votre site part avec elle. Avec un nom de domaine à votre nom, vous gardez au moins votre adresse.</p>

  <h2>Choisir en deux questions</h2>
  <p>Première question : avez-vous dix à quarante heures à y consacrer ? Si oui, un créateur de site vous reviendra moins cher. Sinon, son prix est trompeur, car le temps que vous n'avez pas coûte aussi de l'argent. Deuxième question : voulez-vous pouvoir changer de prestataire sans tout refaire ? Alors vérifiez que le nom de domaine est enregistré à votre nom, quelle que soit l'option choisie.</p>

  <h2>Questions fréquentes</h2>
%(faq)s

  <div class="actions">
    <a class="btn btn-primary" href="/demandez-votre-demo#pide-demo">Demander ma démo gratuite</a>
    <a class="btn btn-ghost" href="/fr/tarifs">Voir nos tarifs</a>
  </div>
  <p class="updated">Mis à jour : septembre 2026</p>"""

NB = ' '
FR_TABLE = table(
    ['Profil', 'Notre choix', 'À partir de', 'Qui fait le site', 'Votre temps', 'Coût sur 24 mois'],
    [['Commencer gratuitement', 'Jimdo ou Webnode', '0 €', 'Vous', '10–20 h', '<strong>0 €</strong><br>avec sous-domaine'],
     ['Créateur payant', 'Wix Light', '14 €/mois, annuel*', 'Vous', '10–30 h', '<strong>351 €</strong><br>+ votre temps'],
     ['Prix le plus bas', 'Hostinger Premium', '2,99 €/mois*', 'Vous', '15–40 h', '<strong>84 €</strong><br>+ votre temps'],
     ['Site fait pour vous', 'WebAutonomos', '15 €/mois', 'Nous', '~30 minutes', '<strong>372 €</strong>'],
     ['Être propriétaire', 'WebAutonomos, paiement unique', '349 € une fois', 'Nous', '~30 minutes', '<strong>361 €</strong>'],
     ['Projet sur mesure', 'Freelance ou agence', '1' + NB + '000–4' + NB + '000 €', 'Le prestataire', 'Rendez-vous',
      '<strong>1' + NB + '000–4' + NB + '000 €</strong><br>+ maintenance']],
    me_rows=(3, 4))

FR_TABLE2 = table(
    ['Service', 'Mise en service', 'Abonnement', 'Engagement', 'Modifications', 'Coût sur 24 mois'],
    [['WebAutonomos', '0 €', '15 €/mois', 'Aucun', '1 par mois', '<strong>372 €</strong>'],
     ['WebAutonomos, paiement unique', '349 €', 'Aucun', 'Aucun', '1 par mois', '<strong>361 €</strong>'],
     ['IONOS, pack S (3 pages)', '199 €', '45 €/mois', '12 mois', '1 par trimestre', '<strong>1' + NB + '279 €</strong>'],
     ['Simplébo, pack Crédibilité', '400 €', '50 €/mois, annuel', '12 mois', 'Illimitées', '<strong>1' + NB + '600 €</strong>']],
    me_rows=(0, 1), cls='cmp svc')

# ═══════════════════════════════ MODIFICATIONS ══════════════════════════════
ES_REMPL = [
    ('<link rel="canonical" href="%s">\n' % URL_ES,
     '<link rel="canonical" href="%s">\n%s\n' % (URL_ES, HREFLANG)),
    ('Webnode destaca si necesitas la web en dos idiomas, porque el multiidioma viene de serie.',
     'Webnode permite añadir un segundo idioma más adelante, pero el multiidioma empieza en el plan Standard, no en el gratuito.'),
    ('"text": "Square cierra Weebly en 67 países a partir del 27 de septiembre de 2026 y desde finales de junio ya no admite publicar páginas nuevas. Si una comparativa todavía la recomienda, no está actualizada."',
     '"text": "Square cierra Weebly en 67 países, donde las webs se despublican el 27 de septiembre de 2026, pero España no está en la lista: las webs de Weebly en España siguen funcionando."'),
    ('<p>Square anunció en junio de 2026 el cierre de Weebly en 67 países a partir del 27 de septiembre de 2026, y desde finales de junio ya no se pueden publicar páginas nuevas. Si estás leyendo una comparativa que todavía la recomienda, está desactualizada. Es el riesgo de elegir plataforma por una lista antigua.</p>',
     '<p>Square anunció en junio de 2026 el cierre de Weebly en 67 países, donde las webs se despublican el 27 de septiembre de 2026. España no está en la lista, así que las webs de Weebly en España siguen funcionando (<a href="%s" rel="noopener">anuncio de Weebly</a>). Aun así, muestra un riesgo real: si la plataforma cierra o cambia sus condiciones, tu web se va con ella. Con el dominio a tu nombre, al menos conservas tu dirección.</p>' % WEEBLY),
    ('"dateModified": "2026-09-14"', '"dateModified": "%s"' % DATE),
]

LIEN = '\n  <p><a href="%s">%s</a></p>'
TARIFS_REMPL = {
    'precios.html': [
        ('<td class="me">Ilimitadas 30 d.</td>', '<td class="me">1 al mes</td>'),
        ('<p class="calc-note">Cambia las horas o tu tarifa para ver el coste real de cada opción. El tiempo que dedicas a construir la web tú mismo también es dinero.</p>',
         '<p class="calc-note">Cambia las horas o tu tarifa para ver el coste real de cada opción. El tiempo que dedicas a construir la web tú mismo también es dinero.</p>'
         + LIEN % ('/mejores-creadores-paginas-web-autonomos', 'Ver la comparativa: mejores creadores de páginas web para autónomos en 2026 →')),
    ],
    'fr/tarifs.html': [
        ('<td class="me">Illimitées 30 j.</td>', '<td class="me">1 par mois</td>'),
        ("l'exercice, un constructeur fera très bien l'affaire. Sinon, déléguer coûte\n  moins cher que vous ne le pensez.</p>",
         "l'exercice, un constructeur fera très bien l'affaire. Sinon, déléguer coûte\n  moins cher que vous ne le pensez.</p>"
         + LIEN % ('/fr/meilleurs-createurs-de-sites-pour-independants',
                   'Comparer Wix, Hostinger, Jimdo, Simplébo et IONOS : les meilleurs créateurs de sites pour indépendants en 2026 →')),
    ],
    'en/pricing.html': [
        ('<td class="me">Unlimited for 30 days</td>', '<td class="me">1 per month</td>'),
        ('If not, handing it over costs less than you think.</p>',
         'If not, handing it over costs less than you think.</p>'
         + LIEN % ('/en/best-website-builders-for-freelancers-in-spain',
                   'Compare Wix, Hostinger, Jimdo, Webnode and IONOS: the best website builders for freelancers in Spain →')),
    ],
}
CONTACT_FR = ('<a href="https://webautonomos.es/contacto">Contact',
              '<a href="/demandez-votre-demo#pide-demo">Contact')
PAGES_CONTACT_FR = ['fr/tarifs.html', 'fr/prestations.html', 'fr/questions.html', 'demandez-votre-demo.html']

HOMES = '_tools/build_lang_homes.py'
HOMES_REMPL = [
    ("               vis='/fr/visibilite-ia/'),",
     "               vis='/fr/visibilite-ia/',\n               cmp='/fr/meilleurs-createurs-de-sites-pour-independants'),"),
    ("               vis='/en/ai-visibility/'),",
     "               vis='/en/ai-visibility/',\n               cmp='/en/best-website-builders-for-freelancers-in-spain'),"),
    ("  cmp_a='Avec une agence classique', cmp_b='Avec WebAutonomos',",
     "  cmp_a='Avec une agence classique', cmp_b='Avec WebAutonomos',\n"
     "  cmp_more='Comparer toutes les options : Wix, Hostinger, Jimdo, Simplébo…',"),
    ("  cmp_a='With a typical agency', cmp_b='With WebAutonomos',",
     "  cmp_a='With a typical agency', cmp_b='With WebAutonomos',\n"
     "  cmp_more='Compare every option: Wix, Hostinger, Jimdo, IONOS…',"),
    ("    <div class=\"cmp-c us\"><h3>{E(c['cmp_b'])}</h3><ul>{us}</ul></div>\n  </div>\n</section>",
     "    <div class=\"cmp-c us\"><h3>{E(c['cmp_b'])}</h3><ul>{us}</ul></div>\n  </div>\n"
     "  <p class=\"cmp-more\"><a href=\"{L('cmp')}\">{E(c['cmp_more'])} →</a></p>\n</section>"),
    (".cmp-c.us li::before { content:'✓'; color:var(--green-dark); }",
     ".cmp-c.us li::before { content:'✓'; color:var(--green-dark); }\n"
     ".cmp-more { text-align:center; margin-top:28px; font-size:.97rem; }\n"
     ".cmp-more a { color:var(--blue); font-weight:600; text-decoration:none; }"),
]

LLMS_REMPL = [
    ('- [Cuánto cuesta una página web para autónomos en 2026](https://webautonomos.es/blog/es/cuanto-cuesta-pagina-web-autonomos-espana)\n',
     '- [Cuánto cuesta una página web para autónomos en 2026](https://webautonomos.es/blog/es/cuanto-cuesta-pagina-web-autonomos-espana)\n'
     '- [Mejores creadores de páginas web para autónomos 2026](%s)\n' % URL_ES),
    ('- [Web design for expats in Spain](https://webautonomos.es/en/web-design-for-expats-in-spain)\n',
     '- [Web design for expats in Spain](https://webautonomos.es/en/web-design-for-expats-in-spain)\n'
     '- [Best website builders for freelancers in Spain 2026](%s)\n' % URL_EN),
    ('- [Site internet pour francophones en Espagne](https://webautonomos.es/fr/site-internet-francophones-espagne)\n',
     '- [Site internet pour francophones en Espagne](https://webautonomos.es/fr/site-internet-francophones-espagne)\n'
     '- [Meilleurs créateurs de sites pour indépendants 2026](%s)\n' % URL_FR),
]


def appliquer(rel, s, rempl):
    for a, b in rempl:
        n = s.count(a)
        if n != 1:
            abandon('%s : ancre trouvée %dx : %s' % (rel, n, a.strip()[:80]))
        s = s.replace(a, b)
    return s


VIDES = {'meta', 'link', 'br', 'img', 'input', 'col', 'hr', 'source', 'wbr'}


def equilibre(s):
    v = re.sub(r'<!--.*?-->', '', s, flags=re.S)
    v = re.sub(r'<(script|style)\b.*?</\1>', '', v, flags=re.S)
    res = {}
    for tag in ('div', 'p', 'a', 'table', 'tr', 'td', 'th', 'ul', 'li', 'dl', 'dt', 'dd', 'h1', 'h2', 'main', 'footer'):
        res[tag] = (len(re.findall(r'<%s[\s>]' % tag, v)), v.count('</%s>' % tag))
    return res


def controler_page(rel, s):
    err = []
    for tag, (o, f) in equilibre(s).items():
        if o != f:
            err.append('<%s> : %d ouvertures, %d fermetures' % (tag, o, f))
    if len(re.findall(r'<h1\b', s)) != 1:
        err.append('il faut exactement un <h1>')
    for bloc in re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
        try:
            json.loads(bloc)
        except ValueError as exc:
            err.append('JSON-LD invalide : %s' % exc)
    for h in re.findall(r'<a [^>]*href="(/[^"#?]*)', s):
        p = h.strip('/')
        if p and not any(os.path.isfile(os.path.join(ROOT, c)) for c in (p + '.html', os.path.join(p, 'index.html'))):
            err.append('lien interne introuvable : %s' % h)
    t = re.search(r'<title>(.*?)</title>', s).group(1)
    if len(html.unescape(t)) > 65:
        err.append('title trop long (%d)' % len(t))
    if err:
        abandon('%s :\n  - %s' % (rel, '\n  - '.join(err)))


def main():
    os.chdir(ROOT)
    for rel in (FR, EN):
        if os.path.exists(rel):
            abandon('%s existe déjà (script déjà lancé ?).' % rel)
    es = lire(ES)
    if 'hreflang' in es:
        abandon('%s contient déjà des hreflang (script déjà lancé ?).' % ES)

    # CSS : on reprend les styles de la page espagnole
    css = '\n'.join(re.findall(r'<style>.*?</style>', es.split('</head>')[0], re.S))
    if '.cmp-wrap' not in css or 'footer' not in css:
        abandon('styles de la page espagnole introuvables.')

    ecrits = {}
    ecrits[EN] = page('en', URL_EN, 'Best website builders for freelancers in Spain (2026)',
                      'Wix, Hostinger, Jimdo, a done-for-you service or an agency: six ways to get a business website '
                      'in Spain, with the real cost over 24 months. Prices ex. VAT.',
                      'en_GB', ('Home', 'Best website builders'),
                      'Best website builders for freelancers in Spain in 2026',
                      EN_BODY % dict(table=EN_TABLE, faq=dl(EN_FAQ), weebly=WEEBLY), EN_FAQ, css)
    ecrits[FR] = page('fr', URL_FR, 'Meilleurs créateurs de sites pour indépendants en 2026',
                      'Wix, Hostinger, Jimdo, Simplébo, IONOS ou un freelance : les options pour le site d\'un '
                      'indépendant en France, avec le coût réel sur 24 mois. Tarifs HT.',
                      'fr_FR', ('Accueil', 'Meilleurs créateurs de sites'),
                      'Meilleurs créateurs de sites pour indépendants en 2026',
                      FR_BODY % dict(table=FR_TABLE, table2=FR_TABLE2, faq=dl(FR_FAQ), weebly=WEEBLY, codeur=CODEUR),
                      FR_FAQ, css)
    for rel, s in ecrits.items():
        controler_page(rel, s)
        if not re.search(r'<table class="cmp[" ]', s) or re.search(r'<table class="(?!cmp)', s):
            abandon('%s : classe des tableaux incorrecte.' % rel)

    # page espagnole
    avant = equilibre(es)
    es2 = appliquer(ES, es, ES_REMPL)
    if equilibre(es2) != avant:
        # un seul <a> ajouté (anuncio de Weebly)
        d = {k: (equilibre(es2)[k][0] - avant[k][0]) for k in avant}
        if {k: v for k, v in d.items() if v} != {'a': 1}:
            abandon('%s : équilibre des balises modifié %s' % (ES, d))
    modifs = {ES: es2}

    # tableaux de prix, liens vers les comparatifs, contact FR
    for rel, rempl in TARIFS_REMPL.items():
        modifs[rel] = appliquer(rel, lire(rel), rempl)
    for rel in PAGES_CONTACT_FR:
        s = modifs.get(rel) or lire(rel)
        modifs[rel] = appliquer(rel, s, [CONTACT_FR])
    for rel in list(modifs):
        if rel == ES:
            continue
        a, b = equilibre(lire(rel)), equilibre(modifs[rel])
        diff = {k: (b[k][0] - a[k][0], b[k][1] - a[k][1]) for k in a if a[k] != b[k]}
        attendu = {'p': (1, 1), 'a': (1, 1)} if rel in TARIFS_REMPL else {}
        if diff != attendu:
            abandon('%s : équilibre des balises inattendu %s' % (rel, diff))

    # générateur des accueils et llms.txt
    homes = lire(HOMES)
    if "cmp_more" in homes:
        abandon('build_lang_homes.py contient déjà cmp_more.')
    homes2 = appliquer(HOMES, homes, HOMES_REMPL)
    try:
        compile(homes2, HOMES, 'exec')
    except SyntaxError as exc:
        abandon('build_lang_homes.py invalide après modification : %s' % exc)
    modifs[HOMES] = homes2
    modifs['llms.txt'] = appliquer('llms.txt', lire('llms.txt'), LLMS_REMPL)

    # sauvegarde puis écriture
    stamp = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
    bak = os.path.expanduser('~/webautonomos-work/backups/comparatifs_%s' % stamp)
    for rel in modifs:
        d = os.path.join(bak, rel)
        os.makedirs(os.path.dirname(d), exist_ok=True)
        shutil.copy2(rel, d)
    for rel, s in list(ecrits.items()) + list(modifs.items()):
        open(rel, 'w', encoding='utf-8').write(s)
    for rel in ecrits:
        print('  ✓ %s créé (%d octets)' % (rel, len(ecrits[rel].encode())))
    print('  ✓ %s : hreflang, Weebly et Webnode corrigés' % ES)
    print('  ✓ precios, fr/tarifs, en/pricing : colonne 349 € = 1 modification par mois, lien vers le comparatif')
    print('  ✓ contact FR -> formulaire français sur %d pages' % len(PAGES_CONTACT_FR))
    print('  ✓ build_lang_homes.py et llms.txt mis à jour')
    print('Sauvegarde : %s\n' % bak.replace(os.path.expanduser('~'), '~'))

    for script in ('_tools/build_lang_homes.py', '_tools/generate_sitemap.py'):
        print('→ %s' % script)
        r = subprocess.run([sys.executable, script], cwd=ROOT)
        if r.returncode:
            sys.exit('ÉCHEC de %s : les pages sont écrites, relance-le à la main après correction.' % script)
    print('\nOK — étape suivante : npx wrangler deploy')


if __name__ == '__main__':
    main()
