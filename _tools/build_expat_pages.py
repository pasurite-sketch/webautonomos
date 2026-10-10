# -*- coding: utf-8 -*-
"""Pages « expatriés » (plan SEO FR-EN, phase 2, 23/09/2026).

  /fr/site-internet-francophones-espagne   francophones installés en Espagne
  /en/web-design-for-expats-in-spain       anglophones installés en Espagne

Pourquoi ces deux pages d'abord : sur ces publics, le domaine .es joue pour
nous, la concurrence est faible, et notre offre répond à leur vrai problème —
un site qui respecte la loi espagnole (aviso legal, RGPD, cookies) sans devoir
se débrouiller en espagnol. Angle distinct des accueils /fr/ et /en/ (offre
générale) : la conformité espagnole et la langue.

Faits juridiques vérifiés le 23/09/2026 :
  - LSSI (loi 34/2002), art. 10 : informations obligatoires, publiées « de
    forme permanente, facile, directe et gratuite » (lssi.digital.gob.es) ;
    art. 2 : s'applique aux prestataires établis en Espagne ;
  - sanctions LSSI : légères jusqu'à 30 000 €, graves 30 001 à 150 000 €,
    très graves 150 001 à 600 000 € (lssi.digital.gob.es, régime sanctionnateur) ;
  - cookies : art. 22.2 LSSI, consentement préalable pour tout cookie non
    nécessaire (guide AEPD sur les cookies, mis à jour en mai 2024).

Style, avis, en-tête, pied de page et JSON-LD : repris de build_lang_homes.py
(même dossier), pour rester identiques aux accueils /fr/ et /en/.

Usage (depuis ~/webautonomos) :
    python3 _tools/build_expat_pages.py            puis generate_sitemap.py
    python3 _tools/build_expat_pages.py --check
"""
import json
import os
import re
import sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'photos'))
from photos_lib import injecter as poser_photo  # photo prévue par _tools/photos/images.json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from origine_lead import poser as poser_origine  # script d'origine des leads (origine-lead.js), ne pas retirer

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build_lang_homes as H  # noqa: E402

BASE, E = H.BASE, H.E
ROOT = H.ROOT

PAGES = {
    'fr': '/fr/site-internet-francophones-espagne',
    'en': '/en/web-design-for-expats-in-spain',
}
SOURCES = [
    ('LSSI, obligations des prestataires (ministère espagnol)', 'Spanish Ministry — LSSI obligations',
     'https://lssi.digital.gob.es/lssi/la-ley/aspectos-basicos/obligaciones-y-responsabilidades-de-los-prestadores'),
    ('LSSI, régime de sanctions', 'LSSI — penalties',
     'https://lssi.digital.gob.es/lssi/la-ley/aspectos-basicos/regimen-sancionador'),
    ('AEPD, guide sur l’usage des cookies (2024)', 'AEPD cookie guide (2024)',
     'https://www.aepd.es/guias/guia-cookies.pdf'),
]

C = {}
C['fr'] = dict(
    html_lang='fr', og_locale='fr_FR', unit='mois', area=['ES'],
    title="Site internet pour francophones en Espagne : 15 €/mois",
    description="Votre site d'indépendant ou d'entreprise en Espagne, conforme à la loi espagnole (aviso legal, RGPD, cookies) et suivi en français. Démo gratuite en 24 h, 15 €/mois HT.",
    service_name="Création de site internet pour francophones installés en Espagne",
    crumb_home='Accueil', crumb='Francophones en Espagne',
    badge='Francophones installés en Espagne',
    h1='Site internet pour les francophones <span class="ul">qui travaillent en Espagne</span>',
    lede="Vous travaillez en Espagne, en français ou pas : votre site, lui, doit respecter la loi espagnole. Nous le créons pour vous, avec l'aviso legal, la politique de confidentialité et la gestion des cookies, et nous vous envoyons une démo gratuite en 24 heures.",
    pills=['Aviso legal et RGPD inclus', 'Suivi en français', 'Démo gratuite en 24 h'],
    cta='Recevoir ma démo gratuite', cta2='Ce que la loi exige',
    rating='<b>TrustScore %s/5</b> · %d avis sur Trustpilot' % (H.TP_SCORE, H.TP_NB),
    brief_t='En bref',
    brief="WebAutonomos crée des sites internet pour les indépendants (autónomos) et les petites entreprises francophones installés en Espagne. Chaque site comprend l'aviso legal, la politique de confidentialité et le consentement aux cookies qu'exige la loi espagnole (LSSI et RGPD), l'hébergement et un nom de domaine à votre nom, pour <strong>15 € HT par mois</strong> sans frais d'installation ni engagement, ou <strong>349 € HT en paiement unique</strong>. Votre site peut être en français et en espagnol, sans supplément. Nous travaillons avec vous en français, par e-mail, WhatsApp et visioconférence, et nous préparons une démo gratuite en 24 heures. L'agence est installée à Ontinyent (province de Valence) et travaille à distance dans toute l'Espagne.",
    legal_ey='La loi espagnole', legal_t="Ce que doit contenir le site d'une activité en Espagne",
    legal_intro="Si vous exercez en Espagne, comme autónomo ou via une société, votre site dépend de la loi espagnole, quelle que soit sa langue : la LSSI s'applique à tous les prestataires établis en Espagne. Trois éléments sont obligatoires.",
    legal_cols=('Obligation', 'Texte', 'Ce qu’il faut y mettre'),
    legal_rows=[
        ('Aviso legal (mentions légales)', 'LSSI, loi 34/2002, art. 10',
         "Votre nom complet ou votre raison sociale, votre NIF ou NIE, votre adresse et votre e-mail. Pour une société : les données d'inscription au registre du commerce. Pour une profession réglementée (psychologue, kiné, dentiste…) : votre ordre professionnel (colegio) et votre numéro d'inscription."),
        ('Politique de confidentialité', 'RGPD et loi organique 3/2018 (LOPDGDD)',
         "Qui traite les données envoyées par votre formulaire de contact, dans quel but, combien de temps elles sont conservées et comment exercer ses droits."),
        ('Consentement aux cookies', 'LSSI, art. 22.2 — contrôlé par l’AEPD',
         "Les cookies non nécessaires (statistiques, carte Google Maps intégrée, vidéos) ne peuvent se charger qu'après l'accord du visiteur."),
    ],
    legal_note="Les amendes prévues par la LSSI vont jusqu'à 30 000 € pour les infractions légères, et jusqu'à 600 000 € pour les plus graves. Ces informations doivent être accessibles en permanence, facilement et gratuitement : un site sans aviso legal se repère en quelques secondes.",
    legal_we_t='Ce que nous mettons en place pour vous',
    legal_we=["Aviso legal rédigé avec vos données (NIF ou NIE, adresse, ordre professionnel si besoin)",
              "Politique de confidentialité et politique de cookies",
              "Bandeau cookies : Google Maps et les statistiques restent bloqués tant que le visiteur n'a pas accepté",
              "Nom de domaine .es enregistré à votre nom"],
    sources_t='Sources',
    why_ey='Pourquoi nous', why_t="Pensé pour ceux qui travaillent en Espagne en français",
    why=[('💬', 'On vous parle en français', "E-mail, WhatsApp ou visioconférence : vous n'avez pas à décrypter le jargon technique ou administratif espagnol."),
         ('⚖️', 'Les règles espagnoles, on s’en occupe', "Aviso legal, confidentialité, cookies, domaine .es à votre nom : votre site est conforme dès sa mise en ligne."),
         ('📍', 'Trouvé par vos clients', "Carte Google Maps sur votre site, bouton WhatsApp et, si vous le souhaitez, gestion de votre fiche Google Business en Espagne."),
         ('🔓', 'Sans engagement', "15 €/mois, résiliable à tout moment. Le nom de domaine reste à vous si vous partez.")],
    where_t='Partout en Espagne',
    where="Barcelone, Valence, Alicante et la Costa Blanca, Madrid, Malaga et la Costa del Sol, les Baléares ou les Canaries : nous travaillons à distance, l'endroit où vous êtes installé ne change rien.",
    sect_t='Tous les métiers',
    sectors=['🔧 Artisans du bâtiment', '🏗️ Rénovation', '⚡ Électriciens', '🪵 Menuisiers',
             '🎨 Peintres', '❄️ Climatisation', '🧠 Psychologues', '💆 Kinésithérapeutes',
             '🦷 Dentistes', '🌿 Thérapeutes bien-être', '🖋️ Tatoueurs', '➕ Votre métier'],
    how_t='Votre site en trois étapes',
    steps=[('Vous décrivez votre activité', 'Votre métier, vos services, votre ville en Espagne : deux minutes suffisent.'),
           ('Nous construisons votre site', 'En moins de 24 h, votre démo est prête, avec vos photos, vos avis Google et vos pages légales.'),
           ('Vous décidez', 'Elle vous plaît : 15 €/mois et elle est en ligne. Sinon, vous ne payez rien.')],
    price_t='Un prix clair, deux façons de payer',
    plans=[dict(name='Abonnement', amt='15 €', per='HT / mois', hl=True, badge='Le plus choisi',
                pts=["Sans frais d'installation", 'Sans engagement', 'Démo gratuite avant de payer']),
           dict(name='Paiement unique', amt='349 €', per='HT, une seule fois', hl=False, badge='',
                pts=['Mêmes services inclus', 'Un seul versement', 'Pages légales comprises'])],
    price_note="Prix hors TVA espagnole (21 %). Nom de domaine inclus la première année, puis environ 12 €/an.",
    price_link='Voir le détail des tarifs',
    rev_t='Ce que disent nos clients', rev_count='TrustScore calculé par Trustpilot sur %d avis' % H.TP_NB,
    rev_link='Voir tous les avis sur Trustpilot', rev_aria='Avis',
    faq_t='Questions fréquentes',
    faq=[("Mon site peut-il être en français et en espagnol ?",
          "Oui, sans supplément. Nous rédigeons les deux versions : vos clients espagnols vous trouvent aussi, et vos prix et conditions existent en espagnol, comme le demande le droit espagnol de la consommation pour l'information précontractuelle."),
         ("Mon site en français doit-il respecter la loi espagnole ?",
          "Oui, si vous exercez en Espagne. La LSSI s'applique aux prestataires établis en Espagne, quelle que soit la langue du site : il vous faut un aviso legal, une politique de confidentialité et un consentement aux cookies."),
         ("Que doit indiquer l'aviso legal d'un site en Espagne ?",
          "Votre nom complet ou votre raison sociale, votre NIF ou NIE, votre adresse et votre e-mail. Une société ajoute ses données d'inscription au registre du commerce ; une profession réglementée ajoute son ordre professionnel (colegio) et son numéro d'inscription."),
         ("Faut-il un bandeau cookies sur mon site ?",
          "Oui, dès que le site utilise des cookies non nécessaires : statistiques, carte Google Maps, vidéos YouTube. Ils ne doivent se charger qu'après l'accord du visiteur. Nous configurons le bandeau pour qu'ils restent bloqués jusque-là."),
         ("Je suis autónomo avec un NIE : le site et le domaine peuvent-ils être à mon nom ?",
          "Oui. Le nom de domaine .es est enregistré à votre nom dès le premier jour. La première année est incluse, puis le renouvellement coûte environ 12 €/an."),
         ("Combien coûte un site avec WebAutonomos ?",
          "15 € HT par mois, sans frais d'installation ni engagement, ou 349 € HT en paiement unique. La TVA espagnole (21 %) s'ajoute. Les pages légales, l'hébergement et la maintenance sont compris."),
         ("Faut-il se rencontrer ?",
          "Non. Tout se fait à distance, en français, par e-mail, WhatsApp et visioconférence. L'agence est installée à Ontinyent, dans la province de Valence."),
         ("Pouvez-vous m'aider à apparaître sur Google Maps en Espagne ?",
          "Oui, avec la gestion de votre fiche Google Business : 29 €/mois, et 49 € pour la créer si vous n'en avez pas encore."),
         ("Que se passe-t-il si je veux arrêter ?",
          "Vous arrêtez de payer, sans durée minimale ni pénalité. Le domaine est à votre nom : vous le gardez, et nous vous aidons à le transférer.")],
    final_t='Voyez votre site avant de payer quoi que ce soit',
    final_sd="Démo gratuite en 24 heures, pages légales comprises. Sans frais d'installation, sans engagement.",
)

C['en'] = dict(
    html_lang='en', og_locale='en_GB', unit='month', area=['ES'],
    title="English-speaking web designer in Spain: web design for expats",
    description="English-speaking web designer in Spain for expat businesses: custom web design, Spanish legal pages, free demo in 24h, €15/month + VAT.",
    service_name="English-speaking web design for expat businesses in Spain",
    crumb_home='Home', crumb='Web design for expats in Spain',
    badge='For self-employed expats in Spain',
    h1='English-speaking web designer in Spain <span class="ul">for expats running a business</span>',
    lede="You run your business in English; your website still has to follow Spanish law. We design it, build it and write the legal texts it needs, then send you a demo within 24 hours.",
    pills=['Spanish legal pages included', 'Support in English', 'Free demo in 24 hours'],
    cta='Get my free demo', cta2='What the law requires',
    rating='<b>TrustScore %s/5</b> · %d reviews on Trustpilot' % (H.TP_SCORE.replace(',', '.'), H.TP_NB),
    brief_t='In short',
    brief="WebAutonomos is an English-speaking web design team in Valencia province that creates websites for expats running a business in Spain: freelancers (autónomos) and small companies. We handle the design and development, write your content in English and Spanish, and add the legal texts Spanish law requires (the LSSI and the GDPR). All our websites come with hosting, a domain name in your name, a contact form, a WhatsApp button, links to your social media profiles and basic SEO built around your trade and the area you serve, for <strong>€15 + VAT per month</strong> with no setup fee and no lock-in, or a <strong>one-off €349 + VAT</strong>. Your demo is ready within 24 hours, and we work remotely with businesses anywhere in Spain. Local SEO and Google Business Profile management are separate, optional services; <a href=\"/en/services\">explore every service in detail</a>. How much does web design cost in Spain? A freelance web designer typically charges €800 to €2,000 for a professional website, and a web design agency €1,500 to €4,000, both excluding maintenance (<a href=\"https://www.socialmediapymes.com/cuanto-cuesta-una-web/\">Social Media Pymes, 2026</a>). Our <a href=\"/en/pricing\">pricing page</a> compares these options with ours, and if you would rather do it yourself, see our <a href=\"/en/best-website-builders-for-freelancers-in-spain\">comparison of DIY website builders such as Wix and Squarespace</a>.",
    legal_ey='Spanish law', legal_t='What your website in Spain must include',
    legal_intro="If you trade in Spain, as an autónomo or through a company, your website falls under Spanish law whatever language it is written in: the LSSI applies to every service provider established in Spain. Three things are mandatory.",
    legal_cols=('Requirement', 'Law', 'What it must contain'),
    legal_rows=[
        ('Legal notice (aviso legal)', 'LSSI, Law 34/2002, art. 10',
         "Your full name or company name, your NIF or NIE, your address and your email. Companies add their Mercantile Registry details; regulated professions (psychologists, physiotherapists, dentists…) add their professional association (colegio) and membership number."),
        ('Privacy policy', 'GDPR and Organic Law 3/2018 (LOPDGDD)',
         "Who processes the data submitted through your website, why, how long it is kept and how people can exercise their rights."),
        ('Cookie consent', 'LSSI, art. 22.2 — enforced by the AEPD',
         "Non-essential cookies (analytics, an embedded Google Map, videos) may only load after the visitor agrees."),
    ],
    legal_note="Fines under the LSSI reach €30,000 for minor infringements and up to €600,000 for the most serious ones. The information must be available permanently, easily and free of charge — a site with no legal notice is spotted in seconds.",
    legal_we_t='What we set up for you',
    legal_we=["A legal notice written with your details (NIF or NIE, address, professional association if needed)",
              "Privacy policy and cookie policy",
              "Cookie banner that keeps Google Maps and analytics blocked until the visitor accepts",
              ".es domain name registered in your name"],
    sources_t='Sources',
    why_ey='Why us', why_t='Web design and development made simple',
    why_intro="You don't need any web design experience, and you don't have to understand Spanish web law: we design your pages, take care of the development and the technology behind them, write your legal texts and talk to you in English from start to finish.",
    why=[('💬', 'Clear communication', "No Spanish technical or legal jargon to decode: we explain each step plainly, by message or video call."),
         ('⚖️', 'Spanish requirements handled', "Your legal notice, cookie consent and other legal texts, plus an .es domain in your name, from day one."),
         ('🎨', 'Custom web design', "Websites designed around your services, with your real details and photos, on a mobile-friendly layout."),
         ('🛠️', 'Web development and hosting', "We build it with our own system, host it securely with SSL and provide ongoing support."),
         ('🌍', 'Bilingual at no extra cost', "Up to four languages, each version written by us, for local and international customers."),
         ('👀', 'See it before you pay', "Your demo is delivered within 24 hours. If it doesn't meet your expectations, you pay nothing."),
         ('📍', 'Found by your customers', "Basic SEO for your trade and area, to help people searching for what you do find you."),
         ('🔓', 'No lock-in', "€15/month, cancel any time. The domain stays yours if you leave.")],
    where_t='Anywhere in Spain',
    where="Costa Blanca, Valencia, Málaga and the Costa del Sol, Barcelona, Madrid, the Balearic or the Canary Islands: we work remotely, so where your business is based makes no difference.",
    sect_t='Web design for every trade',
    sect_intro="We design websites for businesses in every trade, from building and renovations to wellbeing and healthcare, each one shaped around the services you actually offer, using your own details and photos.",
    sectors=['🔧 Builders & trades', '🏗️ Renovations', '⚡ Electricians', '🪵 Carpenters',
             '🎨 Painters & decorators', '❄️ Air conditioning', '🧠 Psychologists', '💆 Physiotherapists',
             '🦷 Dentists', '🌿 Wellbeing practitioners', '🖋️ Tattoo artists', '➕ Your trade'],
    how_t='Our web design process in three steps',
    steps_intro="Our approach is simple: you see your website before you pay. The demo is ready within 24 hours of your first message, and nothing goes online unless you decide to go ahead.",
    steps=[('Tell us what you need', 'Your trade, your services, your town in Spain: it takes two minutes.'),
           ('We design your website', 'Within 24 hours your demo is ready, with your photos, your reviews and your legal texts.'),
           ('You decide', 'Like it? €15/month and it goes live. If not, you pay nothing.')],
    price_t='One clear price, two ways to pay',
    plans=[dict(name='Monthly', amt='€15', per='+ VAT / month', hl=True, badge='Most popular',
                pts=['No setup fee', 'No lock-in', 'Free demo before you pay']),
           dict(name='One-off', amt='€349', per='+ VAT, paid once', hl=False, badge='',
                pts=['Same services included', 'A single payment', 'Legal pages included'])],
    price_note='Prices exclude Spanish VAT (21%). Domain name included for the first year, then about €12/year.',
    price_link='See full pricing details',
    rev_t='What our clients say', rev_count='TrustScore calculated by Trustpilot from %d reviews' % H.TP_NB,
    rev_link='See all reviews on Trustpilot', rev_aria='Review',
    faq_t='Frequently asked questions',
    faq=[("Why work with an English-speaking web designer in Spain?",
          "So you can explain your business, agree on the design and understand every page in your own language, while the Spanish version and the legal requirements are handled for you. With WebAutonomos, the whole experience is in English, by email, WhatsApp or video call. The team is based in Ontinyent, in Valencia province, and works remotely with clients anywhere in Spain, so there is no need to meet in person."),
         ("Do I need to speak Spanish to get a website in Spain?",
          "No. We communicate with you in English and write the Spanish version of your website ourselves, so you never have to brief anyone in Spanish."),
         ("Can my website be in English and Spanish?",
          "Yes, at no extra cost, and in up to four languages. We write each version, so Spanish-speaking customers find you too, and your prices and terms are available in Spanish, as Spanish consumer law requires for pre-contract information."),
         ("Does my English-language website have to comply with Spanish law?",
          "Yes, if you are established in Spain. The LSSI applies to service providers established in Spain whatever language the site is in: you need a legal notice, a privacy policy and cookie consent."),
         ("Do I need a cookie banner?",
          "Yes, as soon as the site uses non-essential cookies: analytics, an embedded map, YouTube videos. They may only load after the visitor agrees. We set the banner up so they stay blocked until then."),
         ("I'm an autónomo with an NIE. Can the website and domain be in my name?",
          "Yes. The .es domain is registered in your name from day one, at no cost for the first year; renewal then costs about €12 a year."),
         ("How much does web design cost with WebAutonomos?",
          "€15 + VAT per month with no setup fee and no lock-in, or a one-off €349 + VAT, with exactly the same services in both. Spanish VAT is 21%. Legal texts, hosting and maintenance are part of the price; extras such as an online shop or a redesign are quoted as separate projects."),
         ("Why is the price fixed rather than a custom quote?",
          "We use our own system, which reuses tested components, and we don't pay for a luxury office or for a sales team on commission. That is what lets us publish a fixed price instead of starting a custom development from zero and preparing a quote for every project."),
         ("Do you build websites on WordPress?",
          "We build your site with our own system, made from already-tested components, so there is no platform such as WordPress or Wix for you to learn and no plugins for you to keep updated. Hosting, an SSL certificate, daily backups and 24/7 monitoring come with both plans, and we reply to support requests the same day."),
         ("Could I build the website myself instead, with a tool like Wix or Squarespace?",
          "You could, but you would have to prepare the legal notice, cookie consent and other legal texts yourself, whatever tool you use (Wix, Squarespace, WordPress or any other), because the requirement comes from Spanish law, not from the tool. With WebAutonomos, those texts are written for you and part of the price."),
         ("How does a web design project go from first message to launch?",
          "You share a few details about your business, your services and the towns you cover, plus some photos. Our team writes the content, designs your pages and adds your legal texts, and we create your demo within 24 hours. View it on your mobile and your computer, tell us what to change (adjustments before launch are unlimited), and go ahead only if you like it."),
         ("Does the website include SEO?",
          "Yes, basic SEO comes with all our websites at no extra cost: titles and text built around your trade and the area you serve, so people searching for what you offer can find you. No one can promise a ranking in the search results, and search engines need time to notice a new site. Local SEO — four blog articles of local content a month, local keywords and a monthly report — is optional and sold separately, for €15 + VAT a month."),
         ("Can you manage my Google Business Profile?",
          "Yes: we optimise your profile, publish four posts a month and reply to your reviews, for €29 + VAT a month, plus €49 + VAT to create the profile if you don't have one yet. Like Local SEO, you can take it with or without the website."),
         ("Do you handle digital marketing and social media too, not just web design?",
          "Yes, on request. The €15 + VAT a month or €349 + VAT price covers your website, hosting, basic SEO and legal texts, and we can also help with social media management or Facebook and Google Ads campaigns: just ask us. A simple strategy is to start with the website, the one place you control, and point your social posts and any advertising back to it."),
         ("Do you build e-commerce websites?",
          "Yes, on request, for businesses that want to sell online. An online shop (e-commerce) is a more complex project: it is quoted separately and is not part of either plan. Tell us what you want to sell and we will give you a quote."),
         ("Can I make changes to my website after it goes live?",
          "Yes — one change a month comes at no extra cost, whatever plan you choose, for as long as your site is online, and the change is made in every version of the site. Use it for content updates such as new photos, prices or recent projects. Anything bigger, such as a redesign or a new major section, is quoted separately with a fixed price agreed in advance."),
         ("What if I want to cancel?",
          "You tell us and stop paying — no minimum term, no penalties, whether you stay for months or years. With the monthly plan, your site goes offline when you stop paying; the domain is in your name, so you keep it, and we assist with the transfer.")],
    final_t='See your website before you pay a thing',
    final_sd='Free demo within 24 hours, legal pages included. No setup fee, no lock-in.',
)

CSS_PAGE = """
/* ─── pages expatriés (build_expat_pages.py) ─── */
.crumbs { padding:14px 6% 0; font-size:.85rem; color:var(--gray); }
.crumbs a { color:var(--blue); text-decoration:none; }
.legal-w { max-width:1000px; margin:0 auto; }
.legal-intro { max-width:760px; margin:0 auto 28px; text-align:center; color:#334155; line-height:1.7; }
.lt-wrap { overflow-x:auto; border:1.5px solid var(--border); border-radius:16px; background:var(--white); }
table.lt { width:100%; border-collapse:collapse; font-size:.93rem; min-width:620px; }
table.lt th, table.lt td { padding:14px 16px; text-align:left; vertical-align:top; border-bottom:1px solid var(--border); line-height:1.55; }
table.lt thead th { background:var(--off); font-weight:700; font-size:.85rem; text-transform:uppercase; letter-spacing:.04em; color:var(--text); }
table.lt tbody th { font-weight:700; color:var(--text); width:24%; }
table.lt td.law { color:var(--gray); width:22%; font-size:.86rem; }
table.lt tr:last-child th, table.lt tr:last-child td { border-bottom:none; }
.legal-note { margin:18px auto 0; max-width:760px; background:#fff8e6; border:1.5px solid #f3d98b; border-radius:12px; padding:14px 18px; font-size:.93rem; color:#5b4a14; line-height:1.6; }
.legal-we { max-width:760px; margin:26px auto 0; }
.legal-we h3 { font-family:'Bricolage Grotesque',sans-serif; font-size:1.1rem; margin-bottom:12px; text-align:center; }
.legal-we ul { list-style:none; padding:0; display:grid; gap:10px; }
.legal-we li { background:var(--white); border:1.5px solid var(--border); border-radius:12px; padding:12px 16px; display:flex; gap:10px; }
.legal-we li::before { content:'✓'; color:var(--green-dark); font-weight:800; }
.srcs { max-width:760px; margin:18px auto 0; font-size:.8rem; color:var(--gray); line-height:1.7; }
.srcs a { color:var(--gray); }
.where { max-width:760px; margin:26px auto 0; text-align:center; color:#334155; line-height:1.7; }
.where strong { display:block; font-family:'Bricolage Grotesque',sans-serif; font-size:1.1rem; color:var(--text); margin-bottom:6px; }
.why-g { max-width:1100px; margin:0 auto; display:grid; grid-template-columns:repeat(4,1fr); gap:16px; }
@media (max-width:1000px) { .why-g { grid-template-columns:repeat(2,1fr); } }
@media (max-width:640px) { .why-g { grid-template-columns:1fr; } table.lt tbody th, table.lt td.law { width:auto; } }
/* 2, 3 ou 5 cartes : pas de colonne vide à droite sur grand écran */
@media (min-width:1001px) {
  .why-g:has(> :nth-child(2):last-child) { grid-template-columns:repeat(2,1fr); max-width:760px; }
  .why-g:has(> :nth-child(3):last-child), .why-g:has(> :nth-child(5):last-child) { grid-template-columns:repeat(3,1fr); max-width:900px; }
}
"""


def page(lang):
    c, u, src, i = C[lang], H.URLS[lang], H.source(lang), H.IDS[lang]
    L = lambda k: BASE + u[k]
    url = BASE + PAGES[lang]
    demo = L('demo') + '#pide-demo'
    home = L('home')
    autre = 'en' if lang == 'fr' else 'fr'
    langs = [('es', 'ES', BASE + '/'), ('fr', 'FR', BASE + PAGES['fr']), ('en', 'EN', BASE + PAGES['en'])]
    nav_links = ''.join('<a href="%s">%s</a>' % (L(k), E(t)) for k, t in H.C[lang]['nav'])
    lang_links = ''.join('<a href="%s" hreflang="%s" lang="%s"%s>%s</a>' % (
        h, code, code, ' aria-current="page"' if code == lang else '', lab) for code, lab, h in langs)
    pills = ''.join('<span class="pill">✓ %s</span>' % E(p) for p in c['pills'])
    rows = ''.join('<tr><th scope="row">%s</th><td class="law">%s</td><td>%s</td></tr>' % (E(a), E(b), E(d))
                   for a, b, d in c['legal_rows'])
    we = ''.join('<li><span>%s</span></li>' % E(x) for x in c['legal_we'])
    srcs = ' · '.join('<a href="%s" rel="noopener" target="_blank">%s</a>' % (h, E(fr if lang == 'fr' else en))
                      for fr, en, h in SOURCES)
    why = ''.join('<div class="aud-c"><div class="aud-i" aria-hidden="true">%s</div><h3>%s</h3><p>%s</p></div>'
                  % (ic, E(t), E(d)) for ic, t, d in c['why'])
    why_intro = '<p class="legal-intro">%s</p>\n  ' % E(c['why_intro']) if c.get('why_intro') else ''
    steps_intro = '<p class="legal-intro">%s</p>\n  ' % E(c['steps_intro']) if c.get('steps_intro') else ''
    sect_intro = '<p class="legal-intro">%s</p>\n  ' % E(c['sect_intro']) if c.get('sect_intro') else ''
    sectors = ''.join('<span class="stag">%s</span>' % E(s) for s in c['sectors'])
    steps = ''.join('<div class="step%s"><div class="sn">%d</div><div class="stit">%s</div><div class="sinf">%s</div></div>'
                    % (' ft' if n == 1 else '', n + 1, E(t), E(d)) for n, (t, d) in enumerate(c['steps']))
    plans = ''
    for p in c['plans']:
        plans += ('<div class="pc%s">%s<div class="pc-n">%s</div><div class="pc-a">%s</div>'
                  '<div class="pc-p">%s</div><ul>%s</ul></div>') % (
            ' hl' if p['hl'] else '', '<span class="pc-b">%s</span>' % E(p['badge']) if p['badge'] else '',
            E(p['name']), E(p['amt']), E(p['per']), ''.join('<li>%s</li>' % E(x) for x in p['pts']))
    slides, dots = '', ''
    avis = H.AVIS[lang]
    for n, (txt, who, tr) in enumerate(avis):
        slides += ('<div class="tp-slide"><div class="tp-card"><div class="tp-stars" aria-hidden="true">★★★★★</div>'
                   '<blockquote>%s</blockquote><div class="tp-who">— %s%s</div></div></div>') % (
            ('«\u00a0%s\u00a0»' if lang == 'fr' else '“%s”') % E(txt), E(who), '<span class="tp-tr">%s</span>' % E(tr) if tr else '')
        dots += '<button class="tp-dot%s" onclick="tpGo(%d)" aria-label="%s %d"></button>' % (
            ' on' if n == 0 else '', n, E(c['rev_aria']), n + 1)
    faq = ''.join('<details><summary>%s</summary><p>%s</p></details>' % (E(q), E(a)) for q, a in c['faq'])
    hreflang = ('<link rel="alternate" hreflang="fr" href="%s%s">\n'
                '<link rel="alternate" hreflang="en" href="%s%s">\n'
                '<link rel="alternate" hreflang="x-default" href="%s%s">'
                % (BASE, PAGES['fr'], BASE, PAGES['en'], BASE, PAGES['en']))
    # JSON-LD : même graphe que les accueils + fil d'Ariane
    jc = dict(title=c['title'], description=c['description'], html_lang=c['html_lang'],
              service_name=c['service_name'], area=c['area'], plans=c['plans'], unit=c['unit'], faq=c['faq'])
    g = json.loads(H.jsonld(lang, jc, dict(home=PAGES[lang])))
    for n in g['@graph']:
        if n.get('@type') == 'Service':
            n['audience'] = {"@type": "Audience", "audienceType":
                             "Francophones exerçant en Espagne" if lang == 'fr'
                             else "English-speaking business owners in Spain"}
    g['@graph'].append({"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": c['crumb_home'], "item": home},
        {"@type": "ListItem", "position": 2, "name": c['crumb'], "item": url}]})
    ld = json.dumps(g, ensure_ascii=False, indent=1)
    wa = re.sub(r'href="https://wa\.me/[^"]*"', 'href="https://wa.me/%s?text=%s"' % (
        H.WHATSAPP, re.sub(r'[^A-Za-z0-9]', lambda m: ''.join('%%%02X' % b for b in m.group(0).encode()),
                           H.C[lang]['wa_text'])), src['float_wa'])
    legal_js = "event.preventDefault();document.getElementById('%s').style.display='flex'"
    foot_langs = '<a href="%s%s" hreflang="%s">%s</a>' % (BASE, PAGES[autre], autre, autre.upper())

    return H.alterner_fonds(f"""<!DOCTYPE html>
<html lang="{c['html_lang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<!-- Page générée par _tools/build_expat_pages.py : ne pas modifier à la main, relancer le script. -->
<title>{E(c['title'])}</title>
<meta name="description" content="{E(c['description'])}">
<meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large">
<link rel="canonical" href="{url}">
{hreflang}
<meta property="og:type" content="website">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{E(c['title'])}">
<meta property="og:description" content="{E(c['description'])}">
<meta property="og:image" content="{BASE}/og-image.png">
<meta property="og:locale" content="{c['og_locale']}">
<meta property="og:site_name" content="WebAutonomos">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,400;12..96,600;12..96,800&family=DM+Sans:wght@400;500;600&display=swap" rel="stylesheet">
<style>{src['css']}{H.EXTRA_CSS}{CSS_PAGE}</style>
<script type="application/ld+json">
{ld}
</script>
{H.TRACKING}
</head>
<body>
<nav>
  {src['logo']}
  <div class="nav-r">
    <div class="nav-links">{nav_links}</div>
    <div class="lang" aria-label="{E(H.C[lang]['lang_label'])}">{lang_links}</div>
    <a class="nav-cta" href="{demo}">{E(H.C[lang]['nav_cta'])}</a>
  </div>
</nav>
<main>
<section class="hero">
  <div class="hero-c">
    <div class="badge"><span class="dot"></span> {E(c['badge'])}</div>
    <h1>{c['h1']}</h1>
    <p class="hdesc">{E(c['lede'])}</p>
    <div class="pills">{pills}</div>
    <div class="hero-acts">
      <a class="hero-cta" href="{demo}">{E(c['cta'])} →</a>
      <a class="hero-2" href="#{'loi' if lang == 'fr' else 'law'}">{E(c['cta2'])}</a>
    </div>
    <p class="rating"><span class="st" aria-hidden="true">★★★★★</span>{c['rating']}</p>
  </div>
</section>
<p class="crumbs"><a href="{home}">{E(c['crumb_home'])}</a> › {E(c['crumb'])}</p>

<section class="brief" id="{i['brief']}">
  <div class="brief-c">
    <h2>{E(c['brief_t'])}</h2>
    <p>{c['brief']}</p>
  </div>
</section>

<section class="blk" id="{'loi' if lang == 'fr' else 'law'}">
  <p class="ey">{E(c['legal_ey'])}</p>
  <h2>{E(c['legal_t'])}</h2>
  <div class="legal-w">
    <p class="legal-intro">{E(c['legal_intro'])}</p>
    <div class="lt-wrap"><table class="lt">
      <thead><tr><th scope="col">{E(c['legal_cols'][0])}</th><th scope="col">{E(c['legal_cols'][1])}</th><th scope="col">{E(c['legal_cols'][2])}</th></tr></thead>
      <tbody>{rows}</tbody>
    </table></div>
    <p class="legal-note">{E(c['legal_note'])}</p>
    <div class="legal-we"><h3>{E(c['legal_we_t'])}</h3><ul>{we}</ul></div>
    <p class="srcs">{E(c['sources_t'])}{' :' if lang == 'fr' else ':'} {srcs}</p>
  </div>
</section>

<section class="blk alt" id="{i['aud']}">
  <p class="ey">{E(c['why_ey'])}</p>
  <h2 style="margin-bottom:36px">{E(c['why_t'])}</h2>
  {why_intro}<div class="why-g">{why}</div>
  <p class="where"><strong>{E(c['where_t'])}</strong>{E(c['where'])}</p>
</section>

<section class="ss blk" id="{i['steps']}">
  <h2 style="margin-bottom:36px">{E(c['how_t'])}</h2>
  {steps_intro}<div class="sw">{steps}</div>
</section>

<section class="blk alt" id="{i['price']}">
  <h2 style="margin-bottom:36px">{E(c['price_t'])}</h2>
  <div class="pc-g">{plans}</div>
  <p class="p-note">{E(c['price_note'])}</p>
  <a class="p-link" href="{L('tarifs')}">{E(c['price_link'])} →</a>
</section>

<section class="secs" id="{i['sect']}">
  <h2 style="margin-bottom:24px">{E(c['sect_t'])}</h2>
  {sect_intro}<div class="sg">{sectors}</div>
</section>

<section class="proof" id="{i['rev']}">
  <h2>{E(c['rev_t'])}</h2>
  <div class="tp">
    <div class="tp-head"><span class="tp-score">{H.TP_SCORE if lang == 'fr' else H.TP_SCORE.replace(',', '.')}</span><span class="tp-of">/ 5</span><span class="tp-count">{E(c['rev_count'])}</span></div>
    <div class="tp-view"><div class="tp-track" id="tpTrack">{slides}</div></div>
    <div class="tp-dots" id="tpDots">{dots}</div>
    <a class="tp-link" href="{H.TRUSTPILOT}" target="_blank" rel="noopener noreferrer">{E(c['rev_link'])} →</a>
  </div>
</section>

<section class="blk alt" id="{i['faq']}">
  <h2 style="margin-bottom:36px">{E(c['faq_t'])}</h2>
  <div class="faq-l">{faq}</div>
</section>

<section class="final">
  <h2>{E(c['final_t'])}</h2>
  <p class="sd">{E(c['final_sd'])}</p>
  <a class="hero-cta" href="{demo}">{E(c['cta'])} →</a>
</section>
</main>

<footer>
  <a class="fl" href="{home}"><span>🌐</span> webautonomos.es</a>
  <div class="flinks">
    <a href="{BASE}/aviso-legal/" onclick="{legal_js % 'modal-aviso'}">{E(H.C[lang]['foot_legal'])}</a>
    <a href="{BASE}/privacidad/" onclick="{legal_js % 'modal-privacidad'}">{E(H.C[lang]['foot_privacy'])}</a>
    <a href="{L('blog')}">{E(H.C[lang]['foot_blog'])}</a>
    {foot_langs}
  </div>
  <address class="fnap">
    <strong>WebAutonomos</strong>
    <span>Calle Pintor Josep Segrelles, 26</span>
    <span>46870 Ontinyent, Valencia</span>
    <a href="tel:+34961877356">+34 961 877 356</a>
    <a href="mailto:info@webautonomos.es">info@webautonomos.es</a>
  </address>
</footer>

{src['modals'][0]}
{src['modals'][1]}
{wa}
<script>
{H.CAROUSEL_JS}
</script>
</body>
</html>
""")


def main():
    check = '--check' in sys.argv
    pages = {}
    for lang in ('fr', 'en'):
        s = page(lang)
        H.controles(lang, s)
        pages[lang] = s
    for lang, s in pages.items():
        rel = PAGES[lang].lstrip('/') + '.html'
        dest = os.path.join(ROOT, rel)
        if check:
            print('  ✓ %s valide (%d octets) — non écrit' % (rel, len(s.encode())))
            continue
        open(dest, 'w', encoding='utf-8').write(poser_origine(poser_photo(dest, s)))
        print('  ✓ %s écrit (%d octets)' % (rel, len(s.encode())))
    # llms.txt : une ligne par page, une seule fois
    llms_p = os.path.join(ROOT, 'llms.txt')
    llms = open(llms_p, encoding='utf-8').read()
    ajouts = [('- [Get a free demo](https://webautonomos.es/get-your-demo)',
               '- [Web design for expats in Spain](https://webautonomos.es%s)' % PAGES['en']),
              ('- [Demander une démo gratuite](https://webautonomos.es/demandez-votre-demo)',
               '- [Site internet pour francophones en Espagne](https://webautonomos.es%s)' % PAGES['fr'])]
    neuf = llms
    for ancre, ligne in ajouts:
        if ligne not in neuf and neuf.count(ancre) == 1:
            neuf = neuf.replace(ancre, ligne + '\n' + ancre)
    if neuf != llms:
        if check:
            print('  ✓ llms.txt : 2 lignes à ajouter — non écrit')
        else:
            open(llms_p, 'w', encoding='utf-8').write(neuf)
            print('  ✓ llms.txt : 2 lignes ajoutées')


if __name__ == '__main__':
    main()
