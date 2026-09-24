# -*- coding: utf-8 -*-
"""Pages d'accueil statiques /fr/ et /en/ (plan SEO FR-EN, phase 1, 23/09/2026).

Pourquoi : l'accueil `/` est un SPA qui affiche les 4 langues sur une seule
adresse ; ses hreflang en et fr pointaient vers `/`. Google n'indexait donc que
l'espagnol. Ces deux pages donnent au français et à l'anglais une vraie adresse,
en HTML complet lisible sans JavaScript.

Cibles (décidées le 23/09/2026) :
  - fr : indépendants et artisans francophones, en France et en Espagne ;
  - en : anglophones qui ont une activité en Espagne.

Le style (CSS, logo, fenêtres « Mentions légales / Confidentialité », bouton
WhatsApp flottant) est repris à chaque génération dans les pages de démo de la
même langue (demandez-votre-demo.html, get-your-demo.html), pour que l'accueil
reste identique visuellement à la page d'atterrissage.

Les adresses internes sont centralisées dans URLS. Depuis le 23/09/2026 les
pages commerciales vivent sous /fr/ et /en/ (migrate_fr_en_pages.py).

Usage (depuis ~/webautonomos) :
    python3 _tools/build_lang_homes.py            # écrit fr/index.html et en/index.html
    python3 _tools/build_lang_homes.py --check    # contrôle sans écrire
"""
import html
import json
import os
import re
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = 'https://webautonomos.es'
E = lambda s: html.escape(s, quote=True)

# ─── adresses internes (un seul endroit à modifier) ─────────────────────────
URLS = {
    'fr': dict(home='/fr/', demo='/demandez-votre-demo', tarifs='/fr/tarifs',
               prestations='/fr/prestations', questions='/fr/questions', blog='/blog/#fr',
               diag='/fr/diagnostic-automatisation/',
               vis='/fr/visibilite-ia/',
               cmp='/fr/meilleurs-createurs-de-sites-pour-independants'),
    'en': dict(home='/en/', demo='/get-your-demo', tarifs='/en/pricing',
               prestations='/en/services', questions='/en/faq', blog='/blog/#en',
               how='/en/how', contact='/en/contact',
               diag='/en/automation-diagnostic/',
               vis='/en/ai-visibility/',
               cmp='/en/best-website-builders-for-freelancers-in-spain'),
}
SOURCE_DEMO = {'fr': 'demandez-votre-demo.html', 'en': 'get-your-demo.html'}
# Ancres des sections, dans la langue de la page (les pages commerciales y
# renvoient : /en/#pricing, /fr/#tarifs…).
# Tags métier de /fr/ et /en/ qui mènent vers une page métier.
# Tenu à jour par _tools/build_metier_pages.py.
SECTOR_LINKS = {"fr": {"🧠 Psychologues": "/fr/site-internet-psychologue-therapeute", "🌿 Thérapeutes bien-être": "/fr/site-internet-psychologue-therapeute", "🪵 Menuisiers": "/fr/site-internet-menuisier", "🪟 Aluminium et PVC": "/fr/site-internet-menuisier", "💆 Kinésithérapeutes": "/fr/site-internet-kinesitherapeute", "🦷 Dentistes": "/fr/site-internet-dentiste"}, "en": {"🧠 Psychologists": "/en/website-for-therapists-in-spain", "🌿 Wellbeing practitioners": "/en/website-for-therapists-in-spain", "🪵 Carpenters": "/en/website-for-carpenters-in-spain", "🪟 Aluminium & PVC": "/en/website-for-carpenters-in-spain", "💆 Physiotherapists": "/en/website-for-physiotherapists-in-spain", "🦷 Dentists": "/en/website-for-dentists-in-spain"}}

IDS = {
    'fr': dict(brief='en-bref', inc='inclus', steps='etapes', price='tarifs', aud='pour-qui',
               sect='metiers', rev='avis', cmp='comparer', add='services', faq='faq'),
    'en': dict(brief='in-short', inc='included', steps='steps', price='pricing', aud='who-we-help',
               sect='trades', rev='reviews', cmp='compare', add='services', faq='faq'),
}
TRUSTPILOT = 'https://www.trustpilot.com/review/webautonomos.es'
WHATSAPP = '34654239520'

# ─── avis Trustpilot (8 avis, note 4,3 — même source que l'accueil espagnol) ─
AVIS = {
 'fr': [
  ("Angelino a créé mon site rapidement et explique tout très bien. Quand on a une question, il répond toujours vite. Je recommande vivement de contacter Angelino à quiconque a besoin d'un site.", "Lee Robinson — Menuisier", "traduit de l'anglais"),
  ("Très bonne expérience avec Webautonomos. Angelino a réalisé mon site en tenant compte de mes demandes et observations. Ses conseils, sa patience et sa disponibilité m'ont été d'un grand soutien.", "Sabine O. — Praticienne bien-être", ""),
  ("Extrêmement satisfaite de WebAutonomos. Merci pour la création de mon magnifique site qui me représente si bien ! Merci pour votre réactivité et votre professionnalisme. Je le recommande sans hésiter.", "Amelle B.", ""),
  ("J'ai beaucoup aimé le travail d'Angelino pour mon site web. Il a été patient, il sait écouter puis concrétiser. Il offre un très bon service.", "Fabiana", "traduit de l'espagnol"),
  ("Très bon professionnel, très attentif et toujours prêt à vous aider pour tout ce dont vous avez besoin. Il a créé mon site web exactement comme je le voulais, avec toutes les modifications nécessaires et en me guidant à chaque étape.", "Ana Saiz — Psychologue", "traduit de l'espagnol"),
  ("Le travail d'Angelino pour la création de mon nouveau site web est vraiment recommandable. Merci pour ta patience et ton professionnalisme. Résultat impeccable. Je le recommande.", "Begoña Cid — Hypnothérapeute", "traduit de l'espagnol"),
  ("Après beaucoup de difficultés pour avoir mon site, avec WebAutonomos cela a été très simple et rapide. Avec un accueil aimable et proche. Je le recommande !", "Analía Juan Guillén — Psychologue", "traduit de l'espagnol"),
  ("Rapides et efficaces, j'ai beaucoup aimé le rendu du site, merci beaucoup.", "Inés — Croissance personnelle", "traduit de l'espagnol"),
 ],
 'en': [
  ("Angelino built my website quickly and explains everything very well. When you have any questions they are always answered promptly. Anyone needing a website made I would highly recommend contacting Angelino.", "Lee Robinson — Carpenter", ""),
  ("A very good experience with Webautonomos. Angelino built my website taking my requests and comments into account. His advice, his patience and his availability were a great support.", "Sabine O. — Wellbeing practitioner", "translated from French"),
  ("Extremely satisfied with WebAutonomos. Thank you for creating my wonderful website that represents me so well! Thank you for your responsiveness and professionalism. I recommend it without hesitation.", "Amelle B.", "translated from French"),
  ("I really liked Angelino's work on my website. He was patient, he knows how to listen and then make it happen. He offers a very good service.", "Fabiana", "translated from Spanish"),
  ("A very good professional, very attentive and always ready to help with whatever you need. He built my website exactly the way I wanted, with all the changes I needed and guiding me every step of the way.", "Ana Saiz — Psychologist", "translated from Spanish"),
  ("Angelino's work on creating my new website comes highly recommended. Thank you for your patience and professionalism. The result is impeccable. I recommend him.", "Begoña Cid — Hypnotherapist", "translated from Spanish"),
  ("After a lot of difficulty getting my website done, with WebAutonomos it was very easy and quick. Friendly and approachable service throughout. I recommend them!", "Analía Juan Guillén — Psychologist", "translated from Spanish"),
  ("Fast and efficient, I really liked how the website turned out, thank you very much.", "Inés — Personal growth", "translated from Spanish"),
 ],
}

# ─── contenu ────────────────────────────────────────────────────────────────
C = {}
C['fr'] = dict(
  html_lang='fr', og_locale='fr_FR',
  title="Site internet pour indépendants et artisans : 15 €/mois",
  description="Votre site pro créé en 24 h, avant tout paiement : 15 €/mois HT sans frais d'installation ni engagement. Indépendants en France et en Espagne.",
  nav=[('prestations', 'Prestations'), ('tarifs', 'Tarifs'), ('questions', 'Questions'), ('blog', 'Blog')],
  nav_cta='Démo gratuite', lang_label='Langue',
  badge='Indépendants et artisans · France et Espagne',
  h1='Site internet pour indépendants et artisans, <span class="ul">à 15 €/mois tout compris</span>',
  lede="Nous créons votre site professionnel avec vos services, vos photos et vos avis Google, et nous vous l'envoyons en 24 heures — avant que vous ne payiez quoi que ce soit. En France comme en Espagne.",
  pills=["Sans frais d'installation", 'Sans engagement', 'Démo gratuite en 24 h'],
  cta='Recevoir ma démo gratuite', cta2='Voir les tarifs',
  rating='<b>4,3/5</b> · 8 avis vérifiés sur Trustpilot',
  brief_t='En bref',
  brief="WebAutonomos crée des sites internet professionnels pour les indépendants et les artisans. Le site coûte <strong>15 € HT par mois</strong>, sans frais d'installation ni engagement, ou <strong>349 € HT en paiement unique</strong>. Ce prix comprend le design, l'hébergement, le certificat SSL, le nom de domaine la première année, les textes légaux et la maintenance. Nous préparons une démo gratuite en 24 heures ; vous ne payez que si elle vous plaît. L'agence est basée à Ontinyent (Valence, Espagne) et travaille à distance avec des indépendants en Espagne et en France.",
  inc_ey='Ce qui est inclus', inc_t='Tout est compris dans le prix',
  inc_sd='Pas de frais cachés, pas d\'options indispensables à payer en plus.',
  inc=['Design professionnel sur mesure', 'Ajustements illimités avant la mise en ligne',
       'Hébergement rapide et sécurisé', 'Certificat SSL (https)',
       'Nom de domaine à votre nom, inclus la 1<sup>re</sup> année', 'Site adapté au mobile',
       'Formulaire de contact vers votre e-mail', 'Bouton WhatsApp',
       'Mentions légales, confidentialité et cookies', 'Sauvegardes, surveillance 24 h/24 et maintenance',
       'Site bilingue sans supplément', 'Une modification par mois'],
  how_ey='Le déroulement', how_t='Votre site en trois étapes',
  how_sd='Sans contrat. Sans surprise. Sans jargon technique.',
  steps=[('Vous décrivez votre activité', 'Votre métier, vos services, votre ville : deux minutes suffisent.'),
         ('Nous construisons votre site', 'En moins de 24 h, votre démo est prête, avec vos photos et vos avis Google.'),
         ('Vous décidez', 'Elle vous plaît : 15 €/mois et elle est en ligne avec votre nom de domaine. Sinon, vous ne payez rien.')],
  price_ey='Tarifs', price_t='Un prix clair, deux façons de payer',
  price_sd='Les mêmes services dans les deux formules.',
  plans=[dict(name='Abonnement', amt='15 €', per='HT / mois', hl=True, badge='Le plus choisi',
              pts=["Sans frais d'installation", 'Sans engagement, résiliable à tout moment', 'Démo gratuite avant de payer']),
         dict(name='Paiement unique', amt='349 €', per='HT, une seule fois', hl=False, badge='',
              pts=['Mêmes services inclus', 'Un seul versement', 'Idéal si vous préférez ne plus y penser'])],
  price_note="Prix hors taxes : IVA espagnole de 21 % en plus. Entreprise établie ailleurs dans l'UE avec un numéro de TVA intracommunautaire : facture sans TVA (autoliquidation). Nom de domaine inclus la première année, puis environ 12 €/an.",
  price_link='Voir le détail et le coût réel sur 24 mois',
  aud_ey='Pour qui', aud_t='En France ou installé en Espagne',
  aud_sd='Nous travaillons à distance, par e-mail, WhatsApp et visioconférence.',
  aud=[('🇫🇷', 'Indépendants en France', "Artisans, thérapeutes, professions de santé : votre site est rédigé en français, pour vos clients, avec votre nom de domaine en .fr."),
       ('🇪🇸', 'Francophones installés en Espagne', "Vous travaillez en Espagne ? Nous connaissons les obligations d'un site espagnol (aviso legal, RGPD, cookies) et nous vous parlons en français.", '/fr/site-internet-francophones-espagne'),
       ('💬', 'Un doute sur votre projet ?', "Écrivez-nous sur WhatsApp : nous vous répondons dans la journée, en français.")],
  sect_ey='Métiers', sect_t='Tous les métiers, un seul prix',
  sectors=['⚡ Électriciens', '🔧 Plombiers', '🪵 Menuisiers', '🎨 Peintres', '🏗️ Rénovation',
           '❄️ Climatisation', '🔑 Serruriers', '🪟 Aluminium et PVC', '🦷 Dentistes',
           '💆 Kinésithérapeutes', '🦶 Podologues', '🧠 Psychologues', '🌿 Thérapeutes bien-être',
           '🖋️ Tatoueurs', '➕ Votre métier'],
  rev_ey='Avis clients', rev_t='Ce que disent nos clients',
  rev_count='Note moyenne sur 8 avis vérifiés Trustpilot', rev_link='Voir tous les avis sur Trustpilot',
  rev_aria='Avis',
  cmp_ey='Comparer', cmp_t='Pourquoi nous choisir ?',
  cmp_a='Avec une agence classique', cmp_b='Avec WebAutonomos',
  cmp_more='Comparer toutes les options : Wix, Hostinger, Jimdo, Simplébo…',
  cmp_others=["<strong>Prix gonflés :</strong> 500 €, 1 000 € ou plus pour un site vitrine simple.",
              "<strong>Des semaines d'attente :</strong> on vous annonce 2 semaines, il en faut 2 mois.",
              "<strong>Lié par un contrat :</strong> engagement de 12 mois, pénalités si vous résiliez."],
  cmp_us=["<strong>Prix fixe et clair :</strong> 15 €/mois, tout compris, sans petits caractères.",
          "<strong>Votre site en 24 heures :</strong> vous le voyez avant de payer, vous validez, il est en ligne.",
          "<strong>Sans engagement :</strong> vous résiliez quand vous voulez, sans pénalité ni justification."],
  add_ey='Pour aller plus loin', add_t='Services complémentaires',
  addons=[('SEO local', '+15 €/mois', 'Quatre articles par mois, mots-clés locaux et rapport mensuel pour être trouvé sur Google dans votre secteur.', None),
          ('Fiche Google Business', '+29 €/mois', 'Optimisation de votre fiche Google Maps, 4 publications par mois et réponse aux avis. Création de la fiche : 90 €.', None),
          ('Automatisation des tâches', 'Diagnostic gratuit', "Calculez ce que vous coûtent vos tâches répétitives et si les automatiser est rentable.", 'diag'),
          ('Visibilité IA', 'Audit', 'Savoir si ChatGPT, Gemini ou Perplexity recommandent votre activité, et comment y apparaître.', 'vis')],
  add_more='En savoir plus',
  faq_ey='Questions fréquentes', faq_t='Vos questions',
  faq=[("Combien coûte un site internet avec WebAutonomos ?",
        "15 € HT par mois, sans frais d'installation ni engagement, ou 349 € HT en paiement unique. Les deux formules comprennent les mêmes services : design, hébergement, SSL, nom de domaine la première année (environ 12 €/an ensuite), textes légaux et maintenance."),
       ("Puis-je voir mon site avant de payer ?",
        "Oui. Nous créons votre site avant tout paiement et vous envoyons un lien privé. Vous demandez les changements que vous voulez ; vous ne payez qu'après avoir validé le résultat."),
       ("Combien de temps faut-il pour avoir mon site ?",
        "La démo est prête en moins de 24 heures. Une fois le design validé, nous connectons votre nom de domaine et le site est en ligne."),
       ("Travaillez-vous avec des indépendants en France ?",
        "Oui. Nous créons des sites pour des indépendants en France comme en Espagne. Tout se fait à distance, par e-mail, WhatsApp et visioconférence."),
       ("Que se passe-t-il si je veux résilier ?",
        "Vous arrêtez de payer, sans durée minimale ni pénalité. Le nom de domaine est enregistré à votre nom dès le premier jour : vous le gardez et nous vous aidons à le transférer si besoin."),
       ("Le nom de domaine m'appartient-il ?",
        "Oui. Nous l'enregistrons à votre nom, en .fr ou en .es selon votre activité. La première année est incluse, le renouvellement coûte ensuite environ 12 €/an."),
       ("Faut-il des connaissances techniques ?",
        "Aucune. Vous nous dites ce que vous proposez et vous nous envoyez quelques photos si vous en avez ; nous nous occupons de tout le reste, y compris des mises à jour."),
       ("Puis-je modifier mon site plus tard ?",
        "Oui. Une modification par mois est incluse : textes, photos, horaires, services, prix ou nouvelle section. Vous nous écrivez par WhatsApp ou par e-mail.")],
  final_t='Voyez votre site avant de payer quoi que ce soit',
  final_sd="Démo gratuite en 24 heures. Sans frais d'installation, sans engagement.",
  foot_legal='Mentions légales', foot_privacy='Confidentialité', foot_blog='Blog',
  wa_text="Bonjour, je suis intéressé par un site pour mon activité",
  service_name='Création de site internet pour indépendants et artisans',
  area=['ES', 'FR'], unit='mois',
)

C['en'] = dict(
  html_lang='en', og_locale='en_GB',
  title="Websites for English-speaking businesses in Spain | €15/month",
  description="Your professional website built in 24 hours, before you pay: €15/month + VAT, no setup fee, no lock-in. Spanish legal pages included. Based in Valencia.",
  nav=[('prestations', "What's included"), ('tarifs', 'Pricing'), ('how', 'How it works'), ('questions', 'FAQ'), ('blog', 'Blog')],
  nav_cta='Free demo', lang_label='Language',
  badge='For English-speaking businesses in Spain',
  h1='Websites for <span style="white-space:nowrap">English-speaking</span> businesses in Spain, <span class="ul">€15/month all included</span>',
  lede="We build your professional website with your services, photos and Google reviews, and send it to you within 24 hours — before you pay anything. The legal pages every Spanish business website needs are included.",
  pills=['No setup fee', 'No lock-in', 'Free demo in 24 hours'],
  cta='Get my free demo', cta2='See pricing',
  rating='<b>4.3/5</b> · 8 verified reviews on Trustpilot',
  brief_t='In short',
  brief="WebAutonomos builds professional websites for freelancers (autónomos) and small businesses in Spain, including English-speaking business owners. A website costs <strong>€15 + VAT per month</strong> with no setup fee and no lock-in, or a <strong>one-off €349 + VAT</strong>. That price covers design, hosting, SSL, a domain name in your name for the first year, the legal pages required in Spain and ongoing maintenance. We build a free demo within 24 hours and you only pay if you like it. The agency is based in Ontinyent (Valencia) and works with businesses across Spain.",
  inc_ey="What's included", inc_t='Everything in one price',
  inc_sd='No hidden costs, no essential extras to pay for later.',
  inc=['Professional custom design', 'Unlimited adjustments before launch',
       'Fast, secure hosting', 'SSL certificate (https)',
       'Domain name in your name, first year included', 'Mobile-friendly site',
       'Contact form to your email', 'WhatsApp button',
       'Legal notice, privacy and cookie policy (Spanish law)', 'Daily backups, 24/7 monitoring and maintenance',
       'Bilingual site at no extra cost', 'One content change per month'],
  how_ey='How it works', how_t='Your website in three steps',
  how_sd='No contract. No surprises. No tech jargon.',
  steps=[('Tell us about your business', 'Your trade, your services, your town: it takes two minutes.'),
         ('We build your website', 'Within 24 hours your demo is ready, with your photos and your Google reviews.'),
         ('You decide', 'Like it? €15/month and it goes live on your domain. If not, you pay nothing.')],
  price_ey='Pricing', price_t='One clear price, two ways to pay',
  price_sd='Exactly the same services in both plans.',
  plans=[dict(name='Monthly', amt='€15', per='+ VAT / month', hl=True, badge='Most popular',
              pts=['No setup fee', 'No lock-in, cancel any time', 'Free demo before you pay']),
         dict(name='One-off', amt='€349', per='+ VAT, paid once', hl=False, badge='',
              pts=['Same services included', 'A single payment', 'Ideal if you prefer not to think about it again'])],
  price_note='Prices exclude VAT (21%). Domain name included for the first year, then about €12/year.',
  price_link='See full pricing details',
  aud_ey='Built for Spain', aud_t='Doing business in Spain, in English',
  aud_sd='We work with you remotely, by email, WhatsApp and video call.',
  aud=[('⚖️', 'Spanish legal pages included', 'Every business website in Spain must show a legal notice, a privacy policy and a cookie policy (LSSI and GDPR). We write them for you.', '/en/web-design-for-expats-in-spain'),
       ('📍', 'Found by local customers', 'A domain name in your name, Google Maps on your site and, if you want, a managed Google Business Profile.'),
       ('💬', 'Contact the Spanish way', 'A WhatsApp button and a contact form that lands in your inbox — how customers in Spain prefer to get in touch.')],
  sect_ey='Trades', sect_t='Every trade, one price',
  sectors=['⚡ Electricians', '🔧 Plumbers', '🪵 Carpenters', '🎨 Painters & decorators',
           '🏗️ Builders & renovations', '❄️ Air conditioning', '🔑 Locksmiths',
           '🪟 Aluminium & PVC', '🦷 Dentists', '💆 Physiotherapists', '🧠 Psychologists',
           '🌿 Wellbeing practitioners', '🖋️ Tattoo artists', '➕ Your trade'],
  rev_ey='Client reviews', rev_t='What our clients say',
  rev_count='Average rating from 8 verified Trustpilot reviews', rev_link='See all reviews on Trustpilot',
  rev_aria='Review',
  cmp_ey='Compare', cmp_t='Why choose us?',
  cmp_a='With a typical agency', cmp_b='With WebAutonomos',
  cmp_more='Compare every option: Wix, Hostinger, Jimdo, IONOS…',
  cmp_others=["<strong>Inflated prices:</strong> €500, €1,000 or more for a simple business website.",
              "<strong>Weeks of waiting:</strong> they say 2 weeks and it ends up being 2 months.",
              "<strong>Tied by contract:</strong> 12-month commitments and penalties if you cancel."],
  cmp_us=["<strong>A fixed, clear price:</strong> €15/month, all included, no fine print.",
          "<strong>Your website in 24 hours:</strong> you see it before you pay, approve it, and it goes live.",
          "<strong>No lock-in:</strong> cancel whenever you want, no penalties, no questions."],
  add_ey='Go further', add_t='Additional services',
  addons=[('Local SEO', '+€15/month', 'Four articles a month, local keywords and a monthly report so customers in your area find you on Google.', None),
          ('Google Business Profile', '+€29/month', 'Your Google Maps listing optimised, 4 posts a month and replies to reviews. Profile creation: €90.', None),
          ('Task automation', 'Free diagnostic', 'Work out what your repetitive tasks cost you each year and whether automating them pays off.', 'diag'),
          ('AI visibility', 'Audit', 'Find out whether ChatGPT, Gemini or Perplexity recommend your business, and how to get there.', 'vis')],
  add_more='Learn more',
  faq_ey='FAQ', faq_t='Your questions',
  faq=[("How much does a website with WebAutonomos cost?",
        "€15 + VAT per month with no setup fee and no lock-in, or a one-off €349 + VAT. Both plans include the same services: design, hosting, SSL, a domain name for the first year (about €12/year after that), Spanish legal pages and maintenance."),
       ("Do you work with English-speaking business owners?",
        "Yes. We build websites for English-speaking freelancers and small businesses across Spain and work with you in English, by email, WhatsApp and video call."),
       ("Does a business website in Spain need legal pages?",
        "Yes. Spanish law (the LSSI and the GDPR) requires a legal notice identifying the business, a privacy policy and a cookie policy. They are included in the price."),
       ("Can I see my website before paying?",
        "Yes. We build your website before you pay anything and send you a private link. You ask for any changes you want and only pay once you approve the result."),
       ("How long does it take?",
        "Your demo is ready within 24 hours. Once you approve the design, we connect your domain and the website goes live."),
       ("What if I want to cancel?",
        "You simply stop paying — no minimum term, no penalties. The domain is registered in your name from day one, so you keep it, and we help you transfer it if needed."),
       ("Do I need any technical knowledge?",
        "None. Tell us what you offer and send a few photos if you have them; we take care of everything else, including updates."),
       ("Can I change my website later?",
        "Yes. One content change per month is included: text, photos, opening hours, services, prices or a new section. Just message us on WhatsApp or by email.")],
  final_t="See your website before you pay a thing",
  final_sd='Free demo within 24 hours. No setup fee, no lock-in.',
  foot_legal='Legal notice', foot_privacy='Privacy', foot_blog='Blog',
  wa_text="Hello, I'm interested in a website for my business",
  service_name='Website design for English-speaking businesses in Spain',
  area=['ES'], unit='month',
)

COUNTRY = {'ES': 'Spain', 'FR': 'France'}


# ─── extraction depuis la page de démo de la même langue ────────────────────
def bloc_div(s, debut):
    """Retourne le <div …>…</div> équilibré qui commence à l'index `debut`."""
    d, i = 0, debut
    for m in re.finditer(r'<div\b|</div>', s[debut:]):
        d += 1 if m.group(0) == '<div' else -1
        if d == 0:
            return s[debut:debut + m.end()]
    return None


def source(lang):
    s = open(os.path.join(ROOT, SOURCE_DEMO[lang]), encoding='utf-8').read()
    out = {}
    m = re.search(r'<style>(.*?)</style>', s, re.S)
    out['css'] = m.group(1) if m else None
    m = re.search(r'<a class="logo".*?</a>', s, re.S)
    out['logo'] = m.group(0) if m else None
    out['modals'] = []
    for mid in ('modal-aviso', 'modal-privacidad'):
        m = re.search(r'<div class="modal-overlay"[^>]*id="%s"' % mid, s)
        out['modals'].append(bloc_div(s, m.start()) if m else None)
    m = re.search(r'<a class="float-wa".*?</a>', s, re.S)
    out['float_wa'] = m.group(0) if m else None
    manquants = [k for k, v in out.items() if not v or (isinstance(v, list) and not all(v))]
    if manquants:
        sys.exit('ABANDON : %s introuvable(s) dans %s.' % (', '.join(manquants), SOURCE_DEMO[lang]))
    # les liens du logo et du modal pointent vers l'accueil espagnol : on les
    # renvoie vers l'accueil de la langue
    out['logo'] = out['logo'].replace('href="https://webautonomos.es/"',
                                      'href="%s%s"' % (BASE, URLS[lang]['home']))
    return out


EXTRA_CSS = """
/* ─── accueil /fr/ /en/ (build_lang_homes.py) ─── */
.nav-r { display:flex; align-items:center; gap:22px; }
.nav-links { display:flex; gap:20px; }
.nav-links a { font-size:0.92rem; font-weight:500; color:#374151; text-decoration:none; transition:color .2s; }
.nav-links a:hover { color:var(--blue); }
.lang { display:flex; gap:2px; }
.lang a { font-size:0.78rem; font-weight:700; color:#64748b; text-decoration:none; padding:5px 7px; border-radius:7px; }
.lang a:hover { color:var(--text); }
.lang a[aria-current="page"] { background:var(--off); color:var(--text); border:1px solid var(--border); }
.nav-cta { background:var(--grad); color:#fff; font-weight:600; font-size:0.88rem; padding:9px 16px;
  border-radius:10px; text-decoration:none; white-space:nowrap; box-shadow:0 4px 14px rgba(15,32,96,.18); }
.hero-c { max-width:760px; }
.hero-acts { display:flex; flex-wrap:wrap; align-items:center; gap:14px 22px; margin-top:32px; }
.hero-acts .hero-cta { margin-top:0; }
.hero-2 { color:#fff; font-weight:600; text-decoration:underline; text-underline-offset:4px; }
.rating { margin-top:22px; color:rgba(255,255,255,.82); font-size:.9rem; }
.rating .st { color:#fff; letter-spacing:2px; margin-right:6px; }
.rating b { color:#fff; }
.brief { padding:56px 6%; background:var(--off); position:relative; }
.brief::before { content:''; position:absolute; top:0; left:0; right:0; height:3px; background:var(--grad); }
.brief-c { max-width:780px; margin:0 auto; }
.brief h2 { font-size:1.35rem; text-align:left; margin-bottom:10px; }
.brief p { font-size:1.04rem; line-height:1.75; color:var(--text); }
.blk { padding:80px 6%; background:var(--white); }
.blk.alt { background:var(--off); }
.inc-g { max-width:980px; margin:0 auto; padding:0; list-style:none;
  display:grid; grid-template-columns:repeat(auto-fit,minmax(260px,1fr)); gap:12px; }
.inc-g li { background:var(--white); border:1.5px solid var(--border); border-radius:12px;
  padding:14px 16px; font-size:.95rem; display:flex; gap:10px; align-items:flex-start; }
.inc-g li::before { content:'✓'; color:var(--green-dark); font-weight:800; }
.blk.alt .inc-g li { background:var(--white); }
.pc-g { max-width:780px; margin:0 auto; display:grid; grid-template-columns:1fr 1fr; gap:18px; }
.pc { background:var(--white); border:1.5px solid var(--border); border-radius:18px; padding:30px 26px; text-align:center; position:relative; }
.pc.hl { background:var(--grad); border-color:transparent; color:#fff; box-shadow:0 16px 44px rgba(15,32,96,.2); }
.pc-b { position:absolute; top:-12px; left:50%; transform:translateX(-50%); background:#fff; color:var(--blue-dark);
  font-size:.72rem; font-weight:700; letter-spacing:.06em; text-transform:uppercase; padding:4px 12px;
  border-radius:100px; border:1.5px solid var(--border); white-space:nowrap; }
.pc-n { font-weight:700; font-size:.95rem; margin-bottom:6px; }
.pc-a { font-family:'Bricolage Grotesque',sans-serif; font-weight:800; font-size:3rem; line-height:1.05; }
.pc-p { font-size:.85rem; opacity:.8; margin-bottom:16px; }
.pc ul { list-style:none; padding:0; margin:0; text-align:left; display:grid; gap:8px; font-size:.92rem; }
.pc li::before { content:'✓ '; font-weight:800; }
.p-note { text-align:center; color:var(--gray); font-size:.85rem; margin:18px auto 0; max-width:620px; }
.p-link { display:block; text-align:center; margin-top:10px; font-weight:600; color:var(--blue); }
.aud-g { max-width:1000px; margin:0 auto; display:grid; grid-template-columns:repeat(auto-fit,minmax(250px,1fr)); gap:16px; }
.add-g { max-width:1100px; margin:0 auto; display:grid; grid-template-columns:repeat(4,1fr); gap:16px; }
@media (max-width:1000px) { .add-g { grid-template-columns:repeat(2,1fr); } }
.aud-c, .add-c { background:var(--white); border:1.5px solid var(--border); border-radius:16px; padding:24px 22px; }
.aud-i { font-size:1.6rem; margin-bottom:8px; }
.aud-c h3, .add-c h3 { font-family:'Bricolage Grotesque',sans-serif; font-weight:700; font-size:1.05rem; margin-bottom:6px; color:var(--text); }
.aud-c p, .add-c p { font-size:.92rem; line-height:1.6; color:var(--gray); }
.add-p { display:inline-block; font-size:.78rem; font-weight:700; color:var(--green-dark); background:var(--off);
  border:1px solid var(--border); border-radius:100px; padding:3px 10px; margin-bottom:10px; }
.add-c a { display:inline-block; margin-top:10px; font-weight:600; font-size:.9rem; color:var(--blue); }
.cmp-g { max-width:900px; margin:0 auto; display:grid; grid-template-columns:1fr 1fr; gap:18px; }
.cmp-c { border-radius:16px; padding:26px 24px; border:1.5px solid var(--border); background:var(--white); }
.cmp-c.us { border-color:var(--green-mid); box-shadow:0 10px 32px rgba(34,197,94,.12); }
.cmp-c h3 { font-family:'Bricolage Grotesque',sans-serif; font-weight:700; font-size:1.05rem; margin-bottom:12px; }
.cmp-c ul { list-style:none; padding:0; display:grid; gap:10px; font-size:.93rem; line-height:1.55; color:#334155; }
.cmp-c li { padding-left:24px; position:relative; }
.cmp-c li::before { position:absolute; left:0; font-weight:800; }
.cmp-c.them li::before { content:'✕'; color:#dc2626; }
.cmp-c.us li::before { content:'✓'; color:var(--green-dark); }
.cmp-more { text-align:center; margin-top:28px; font-size:.97rem; }
.cmp-more a { color:var(--blue); font-weight:600; text-decoration:none; }
a.stag { text-decoration:none; }
a.stag:hover { border-color:var(--green-mid); }
.faq-l { max-width:780px; margin:0 auto; display:grid; gap:10px; }
.faq-l details { background:var(--white); border:1.5px solid var(--border); border-radius:12px; }
.faq-l summary { cursor:pointer; padding:16px 18px; font-weight:600; list-style:none;
  display:flex; justify-content:space-between; align-items:flex-start; gap:14px; }
.faq-l summary::-webkit-details-marker { display:none; }
.faq-l summary::after { content:'+'; flex-shrink:0; color:var(--gray); font-weight:700; }
.faq-l details[open] summary::after { content:'–'; }
.faq-l details p { padding:0 18px 16px; color:#334155; line-height:1.65; font-size:.95rem; }
.final { padding:80px 6%; background:var(--grad); text-align:center; }
.final h2 { color:#fff; }
.final .sd { color:rgba(255,255,255,.75); margin-bottom:28px; }
.final .hero-cta { margin-top:0; }
@media (max-width:980px) { .nav-links { display:none; } }
@media (max-width:640px) {
  .pc-g, .cmp-g, .add-g { grid-template-columns:1fr; }
  .pc-g { gap:26px; }
  .blk, .final { padding:56px 5%; }
  .brief { padding:44px 5%; }
  .nav-cta { display:none; }
  .hero-acts { flex-direction:column; align-items:stretch; text-align:center; }
}
"""

CAROUSEL_JS = """(function(){
  var track=document.getElementById('tpTrack');
  if(!track) return;
  var dots=document.querySelectorAll('#tpDots .tp-dot');
  var n=track.children.length, i=0, timer=null;
  window.tpGo=function(k){
    i=(k+n)%n;
    track.style.transform='translateX(-'+(i*100)+'%)';
    dots.forEach(function(d,j){ d.classList.toggle('on', j===i); });
  };
  function play(){ timer=setInterval(function(){ tpGo(i+1); }, 6000); }
  function stop(){ clearInterval(timer); }
  play();
  var wrap=track.closest('.tp');
  wrap.addEventListener('mouseenter', stop);
  wrap.addEventListener('mouseleave', play);
})();"""

TRACKING = """<script async src="https://www.googletagmanager.com/gtag/js?id=G-MT6S7CH7N9"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-MT6S7CH7N9');
</script>
<script type="text/javascript">
  (function(c,l,a,r,i,t,y){
    c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};
    t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;
    y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);
  })(window, document, "clarity", "script", "wb9354sv4p");
</script>"""


def texte(s):
    """HTML -> texte brut (pour le JSON-LD)."""
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', '', s))).strip()


def jsonld(lang, c, u):
    url = BASE + u['home']
    org = {"@type": "ProfessionalService", "@id": BASE + "/#organization",
           "name": "WebAutonomos", "url": BASE + "/", "logo": BASE + "/favicon-512.png",
           "image": BASE + "/og-image.png",
           "email": "info@webautonomos.es", "telephone": "+34961877356",
           "address": {"@type": "PostalAddress", "streetAddress": "Calle Pintor Josep Segrelles, 26",
                       "postalCode": "46870", "addressLocality": "Ontinyent",
                       "addressRegion": "Valencia", "addressCountry": "ES"},
           "areaServed": [{"@type": "Country", "name": COUNTRY[a]} for a in c['area']],
           "knowsLanguage": ["es", "ca", "en", "fr"],
           "sameAs": [TRUSTPILOT]}
    page = {"@type": "WebPage", "@id": url + "#webpage", "url": url, "name": c['title'],
            "description": c['description'], "inLanguage": c['html_lang'],
            "isPartOf": {"@type": "WebSite", "@id": BASE + "/#website", "url": BASE + "/",
                         "name": "WebAutonomos"},
            "about": {"@id": BASE + "/#organization"}}
    service = {"@type": "Service", "@id": url + "#service", "name": c['service_name'],
               "provider": {"@id": BASE + "/#organization"}, "inLanguage": c['html_lang'],
               "areaServed": [{"@type": "Country", "name": COUNTRY[a]} for a in c['area']],
               "offers": [
                   {"@type": "Offer", "name": c['plans'][0]['name'], "priceCurrency": "EUR",
                    "priceSpecification": {"@type": "UnitPriceSpecification", "price": 15,
                                           "priceCurrency": "EUR", "unitText": c['unit'],
                                           "valueAddedTaxIncluded": False}},
                   {"@type": "Offer", "name": c['plans'][1]['name'], "price": 349,
                    "priceCurrency": "EUR",
                    "priceSpecification": {"@type": "PriceSpecification", "price": 349,
                                           "priceCurrency": "EUR", "valueAddedTaxIncluded": False}}]}
    faq = {"@type": "FAQPage", "@id": url + "#faq", "inLanguage": c['html_lang'],
           "mainEntity": [{"@type": "Question", "name": q,
                           "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in c['faq']]}
    return json.dumps({"@context": "https://schema.org", "@graph": [org, page, service, faq]},
                      ensure_ascii=False, indent=1)


def page(lang):
    c, u, src, i = C[lang], URLS[lang], source(lang), IDS[lang]
    L = lambda k: BASE + u[k]
    url = L('home')
    demo = L('demo') + '#pide-demo'
    langs = [('es', 'ES', BASE + '/'), ('fr', 'FR', BASE + URLS['fr']['home']),
             ('en', 'EN', BASE + URLS['en']['home'])]

    nav_links = ''.join('<a href="%s">%s</a>' % (L(k), E(t)) for k, t in c['nav'])
    lang_links = ''.join('<a href="%s" hreflang="%s" lang="%s"%s>%s</a>' % (
        h, code, code, ' aria-current="page"' if code == lang else '', lab) for code, lab, h in langs)
    pills = ''.join('<span class="pill">✓ %s</span>' % E(p) for p in c['pills'])
    inc = ''.join('<li><span>%s</span></li>' % i for i in c['inc'])
    steps = ''.join('<div class="step%s"><div class="sn">%d</div><div class="stit">%s</div><div class="sinf">%s</div></div>'
                    % (' ft' if n == 1 else '', n + 1, E(t), E(d)) for n, (t, d) in enumerate(c['steps']))
    plans = ''
    for p in c['plans']:
        plans += ('<div class="pc%s">%s<div class="pc-n">%s</div><div class="pc-a">%s</div>'
                  '<div class="pc-p">%s</div><ul>%s</ul></div>') % (
            ' hl' if p['hl'] else '', '<span class="pc-b">%s</span>' % E(p['badge']) if p['badge'] else '',
            E(p['name']), E(p['amt']), E(p['per']), ''.join('<li>%s</li>' % E(x) for x in p['pts']))
    # 4e élément facultatif : lien vers une page dédiée (pages expatriés, 23/09/2026)
    aud = ''.join('<div class="aud-c"><div class="aud-i" aria-hidden="true">%s</div><h3>%s</h3><p>%s</p>%s</div>'
                  % (a[0], E(a[1]), E(a[2]),
                     '<p style="margin-top:10px"><a href="%s%s" style="font-weight:600;color:var(--blue)">%s →</a></p>'
                     % (BASE, a[3], E(c['add_more'])) if len(a) > 3 else '')
                  for a in c['aud'])
    # tags liés à une page métier (build_metier_pages.py, 24/09/2026)
    sectors = ''.join('<a class="stag" href="%s%s">%s</a>' % (BASE, SECTOR_LINKS[lang][s], E(s))
                      if s in SECTOR_LINKS.get(lang, {}) else '<span class="stag">%s</span>' % E(s)
                      for s in c['sectors'])
    slides, dots = '', ''
    for n, (txt, who, tr) in enumerate(AVIS[lang]):
        slides += ('<div class="tp-slide"><div class="tp-card"><div class="tp-stars" aria-hidden="true">★★★★★</div>'
                   '<blockquote>« %s »</blockquote><div class="tp-who">— %s%s</div></div></div>') % (
            E(txt), E(who), '<span class="tp-tr">%s</span>' % E(tr) if tr else '')
        dots += '<button class="tp-dot%s" onclick="tpGo(%d)" aria-label="%s %d"></button>' % (
            ' on' if n == 0 else '', n, E(c['rev_aria']), n + 1)
    others = ''.join('<li>%s</li>' % x for x in c['cmp_others'])
    us = ''.join('<li>%s</li>' % x for x in c['cmp_us'])
    addons = ''
    for t, p, d, k in c['addons']:
        addons += '<div class="add-c"><span class="add-p">%s</span><h3>%s</h3><p>%s</p>%s</div>' % (
            E(p), E(t), E(d), '<a href="%s">%s →</a>' % (L(k), E(c['add_more'])) if k else '')
    faq = ''.join('<details><summary>%s</summary><p>%s</p></details>' % (E(q), E(a)) for q, a in c['faq'])
    hreflang = '\n'.join('<link rel="alternate" hreflang="%s" href="%s">' % (code, h) for code, _, h in langs)
    hreflang += '\n<link rel="alternate" hreflang="x-default" href="%s/">' % BASE
    wa = 'https://wa.me/%s?text=%s' % (WHATSAPP, re.sub(r'[^A-Za-z0-9]', lambda m: ''.join(
        '%%%02X' % b for b in m.group(0).encode()), c['wa_text']))
    float_wa = re.sub(r'href="https://wa\.me/[^"]*"', 'href="%s"' % wa, src['float_wa'])
    legal_js = "event.preventDefault();document.getElementById('%s').style.display='flex'"

    return f"""<!DOCTYPE html>
<html lang="{c['html_lang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<!-- Page générée par _tools/build_lang_homes.py : ne pas modifier à la main, relancer le script. -->
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
<style>{src['css']}{EXTRA_CSS}</style>
<script type="application/ld+json">
{jsonld(lang, c, u)}
</script>
{TRACKING}
</head>
<body>
<nav>
  {src['logo']}
  <div class="nav-r">
    <div class="nav-links">{nav_links}</div>
    <div class="lang" aria-label="{E(c['lang_label'])}">{lang_links}</div>
    <a class="nav-cta" href="{demo}">{E(c['nav_cta'])}</a>
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
      <a class="hero-2" href="{L('tarifs')}">{E(c['cta2'])}</a>
    </div>
    <p class="rating"><span class="st" aria-hidden="true">★★★★★</span>{c['rating']}</p>
  </div>
</section>

<section class="brief" id="{i['brief']}">
  <div class="brief-c">
    <h2>{E(c['brief_t'])}</h2>
    <p>{c['brief']}</p>
  </div>
</section>

<section class="blk" id="{i['inc']}">
  <p class="ey">{E(c['inc_ey'])}</p>
  <h2>{E(c['inc_t'])}</h2>
  <p class="sd">{E(c['inc_sd'])}</p>
  <ul class="inc-g">{inc}</ul>
</section>

<section class="ss blk alt" id="{i['steps']}">
  <p class="ey">{E(c['how_ey'])}</p>
  <h2>{E(c['how_t'])}</h2>
  <p class="sd">{E(c['how_sd'])}</p>
  <div class="sw">{steps}</div>
</section>

<section class="blk" id="{i['price']}">
  <p class="ey">{E(c['price_ey'])}</p>
  <h2>{E(c['price_t'])}</h2>
  <p class="sd">{E(c['price_sd'])}</p>
  <div class="pc-g">{plans}</div>
  <p class="p-note">{E(c['price_note'])}</p>
  <a class="p-link" href="{L('tarifs')}">{E(c['price_link'])} →</a>
</section>

<section class="blk alt" id="{i['aud']}">
  <p class="ey">{E(c['aud_ey'])}</p>
  <h2>{E(c['aud_t'])}</h2>
  <p class="sd">{E(c['aud_sd'])}</p>
  <div class="aud-g">{aud}</div>
</section>

<section class="secs" id="{i['sect']}">
  <p class="ey">{E(c['sect_ey'])}</p>
  <h2 style="margin-bottom:24px">{E(c['sect_t'])}</h2>
  <div class="sg">{sectors}</div>
</section>

<section class="proof" id="{i['rev']}">
  <p class="ey">{E(c['rev_ey'])}</p>
  <h2>{E(c['rev_t'])}</h2>
  <div class="tp">
    <div class="tp-head"><span class="tp-score">{'4,3' if lang == 'fr' else '4.3'}</span><span class="tp-of">/ 5</span><span class="tp-count">{E(c['rev_count'])}</span></div>
    <div class="tp-view"><div class="tp-track" id="tpTrack">{slides}</div></div>
    <div class="tp-dots" id="tpDots">{dots}</div>
    <a class="tp-link" href="{TRUSTPILOT}" target="_blank" rel="noopener noreferrer">{E(c['rev_link'])} →</a>
  </div>
</section>

<section class="blk alt" id="{i['cmp']}">
  <p class="ey">{E(c['cmp_ey'])}</p>
  <h2 style="margin-bottom:36px">{E(c['cmp_t'])}</h2>
  <div class="cmp-g">
    <div class="cmp-c them"><h3>{E(c['cmp_a'])}</h3><ul>{others}</ul></div>
    <div class="cmp-c us"><h3>{E(c['cmp_b'])}</h3><ul>{us}</ul></div>
  </div>
  <p class="cmp-more"><a href="{L('cmp')}">{E(c['cmp_more'])} →</a></p>
</section>

<section class="blk" id="{i['add']}">
  <p class="ey">{E(c['add_ey'])}</p>
  <h2 style="margin-bottom:36px">{E(c['add_t'])}</h2>
  <div class="add-g">{addons}</div>
</section>

<section class="blk alt" id="{i['faq']}">
  <p class="ey">{E(c['faq_ey'])}</p>
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
  <a class="fl" href="{url}"><span>🌐</span> webautonomos.es</a>
  <div class="flinks">
    <a href="{BASE}/aviso-legal/" onclick="{legal_js % 'modal-aviso'}">{E(c['foot_legal'])}</a>
    <a href="{BASE}/privacidad/" onclick="{legal_js % 'modal-privacidad'}">{E(c['foot_privacy'])}</a>
    <a href="{L('blog')}">{E(c['foot_blog'])}</a>
    {('<a href="%s">Contact</a>' % L('contact')) if 'contact' in u else ''}
    {''.join('<a href="%s" hreflang="%s">%s</a>' % (h, code, lab) for code, lab, h in langs if code != lang)}
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
{float_wa}
<script>
{CAROUSEL_JS}
</script>
</body>
</html>
"""


def controles(nom, s):
    err = []
    visible = re.sub(r'<!--.*?-->', '', s, flags=re.S)
    visible = re.sub(r'<script.*?</script>', '', visible, flags=re.S)
    visible = re.sub(r'<style>.*?</style>', '', visible, flags=re.S)
    if len(re.findall(r'<h1\b', visible)) != 1:
        err.append('il faut exactement un <h1>')
    for tag in ('div', 'section', 'p', 'ul', 'li', 'a', 'details', 'nav', 'footer', 'main', 'h2', 'h3'):
        o = len(re.findall(r'<%s[\s>]' % tag, visible)); f = visible.count('</%s>' % tag)
        if o != f:
            err.append('<%s> déséquilibré : %d ouvertures, %d fermetures' % (tag, o, f))
    for interdit in ('Plus de 40', 'More than 40', 'tp-score">4,2', 'tp-score">4.2', ' 6 avis', ' 6 verified'):
        if interdit in s:
            err.append('mention périmée : %s' % interdit)
    for bloc in re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
        try:
            json.loads(bloc)
        except ValueError as exc:
            err.append('JSON-LD invalide : %s' % exc)
    scripts = [m.group(2) for m in re.finditer(r'<script(\s[^>]*)?>(.*?)</script>', s, re.S)
               if 'ld+json' not in (m.group(1) or '') and m.group(2).strip()]
    with tempfile.TemporaryDirectory() as tmp:
        for i, js in enumerate(scripts):
            f = os.path.join(tmp, 's%d.js' % i)
            open(f, 'w', encoding='utf-8').write(js)
            r = subprocess.run(['node', '--check', f], capture_output=True, text=True)
            if r.returncode:
                err.append('script %d : %s' % (i, r.stderr.strip()[:200]))
    if err:
        sys.exit('ABANDON (%s) :\n  - %s\nRien écrit.' % (nom, '\n  - '.join(err)))


# ─── hreflang réciproques sur l'accueil espagnol (index.html, SPA) ──────────
# `/` déclarait en et fr vers lui-même. Il doit désormais pointer vers /en/ et
# /fr/, sinon Google ignore le groupe (hreflang non réciproques). Opération
# idempotente : ne touche index.html que si l'ancienne forme est présente.
HREFLANG_ANCIENS = {
    'en': '<link rel="alternate" hreflang="en" href="https://webautonomos.es/">',
    'fr': '<link rel="alternate" hreflang="fr" href="https://webautonomos.es/">',
}


def hreflang_accueil(check):
    path = os.path.join(ROOT, 'index.html')
    s = open(path, encoding='utf-8').read()
    avant = s
    for lang, ancien in HREFLANG_ANCIENS.items():
        nouveau = ancien.replace('href="https://webautonomos.es/"',
                                 'href="%s%s"' % (BASE, URLS[lang]['home']))
        n_old, n_new = s.count(ancien), s.count(nouveau)
        if n_old == 1 and n_new == 0:
            s = s.replace(ancien, nouveau)
        elif not (n_old == 0 and n_new == 1):
            sys.exit('ABANDON : hreflang %s de index.html inattendu '
                     '(ancien %dx, nouveau %dx). Rien écrit.' % (lang, n_old, n_new))
    if s == avant:
        print('  ✓ index.html : hreflang en/fr déjà à jour')
    elif check:
        print('  ✓ index.html : hreflang en/fr à mettre à jour — non écrit')
    else:
        open(path, 'w', encoding='utf-8').write(s)
        print('  ✓ index.html : hreflang en → /en/, fr → /fr/')


def main():
    check = '--check' in sys.argv
    pages = {}
    for lang in ('fr', 'en'):
        s = page(lang)
        controles(lang, s)
        pages[lang] = s
    for lang, s in pages.items():
        dest = os.path.join(ROOT, lang, 'index.html')
        if check:
            print('  ✓ %s/index.html valide (%d octets) — non écrit' % (lang, len(s.encode())))
            continue
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        open(dest, 'w', encoding='utf-8').write(s)
        print('  ✓ %s/index.html écrit (%d octets)' % (lang, len(s.encode())))
    hreflang_accueil(check)


if __name__ == '__main__':
    main()
