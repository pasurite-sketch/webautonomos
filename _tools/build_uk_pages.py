# -*- coding: utf-8 -*-
"""Pages pour les cabinets et les artisans britanniques (26 et 28/09/2026).

Angelino accepte des clients au Royaume-Uni (décision du 26/09/2026). Deux pages
dédiées, distinctes des pages métier « in Spain » de build_metier_pages.py (qui
visent les anglophones installés en Espagne) :
    /en/dental-website-design          cabinets dentaires britanniques
    /en/physiotherapy-website-design   kinésithérapeutes britanniques
Requêtes visées (Semrush Royaume-Uni, 26/09/2026) : « dental website design »
720/mois KD 15 ; « physiotherapy website design » 110/mois KD 3.

Artisans (décision d'Angelino du 28/09/2026, Semrush Royaume-Uni du même jour) :
    /en/web-design-for-tradesmen       « web design for tradesmen » 590/mois KD 3 (page mère)
    /en/web-design-for-plumbers        « web design for plumbers » 390/mois KD 9
    /en/web-design-for-electricians    « web design for electricians » 320/mois KD 7
Règles vérifiées le 28/09/2026 (legislation.gov.uk, gov.uk, HSE, Ofgem, CMA, ICO),
puis relues par une vérification indépendante. Les pages « in Spain » des mêmes
métiers (build_metier_pages.py) y renvoient, et inversement.

Prix : en euros, sans TVA ajoutée pour les clients britanniques, avec l'équivalent
indicatif en livres (VERITE.md §2 bis). Domaine .co.uk ou .uk, textes légaux
adaptés au droit britannique (UK GDPR) : décisions d'Angelino du 26/09/2026.

Pas de groupe hreflang : aucune page équivalente en espagnol ou en français. Les
pages « in Spain » renvoient vers celles-ci (spain_note de build_metier_pages.py)
et inversement.

Règles britanniques vérifiées le 26/09/2026 sur les sources officielles (GDC,
HCPC, CSP, CAP Code/ASA, legislation.gov.uk, CQC, ICO) : voir SOURCES_*.
À revoir quand le GDC aura adopté son « Framework for Professionalism »
(consultation close le 31/08/2026) : les références aux Standards de 2013
changeront.

Même gabarit que build_metier_pages.py (styles, avis, formulaire de démo).

Usage (depuis ~/webautonomos) :
    python3 _tools/build_uk_pages.py            écrit les pages, llms.txt, sitemap
    python3 _tools/build_uk_pages.py --check    vérifie sans écrire
Ré-exécutable : même entrée, même sortie.
"""
import json
import os
import re
import subprocess
import sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'photos'))
from photos_lib import injecter as poser_photo  # photo prévue par _tools/photos/images.json

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build_lang_homes as H  # noqa: E402
import build_expat_pages as X  # noqa: E402  (styles, avis communs)
import build_metier_pages as BM  # noqa: E402  (gabarit des pages métier)

BASE, E = H.BASE, H.E
ROOT = H.ROOT
LANG = 'en'
H.COUNTRY.setdefault('GB', 'United Kingdom')

# Équivalent indicatif en livres : 1 € = 0,8595 £ (exchange-rates.org, 25/09/2026)
TAUX, TAUX_DATE = 0.8595, '25 September 2026'
GBP_MOIS, GBP_UNIQUE = round(15 * TAUX), round(349 * TAUX)


def abandon(msg):
    sys.exit('ABANDON : %s\nRien n\'a été modifié.' % msg)


# ═════════════════════════ TEXTES COMMUNS ══════════════════════════════════
PLANS = [
    dict(name='Monthly', amt='€15', per='a month · about £%d · no VAT added' % GBP_MOIS, hl=True,
         badge='Most popular', pts=['No setup fee', 'No lock-in', 'Free demo before you pay']),
    dict(name='One-off', amt='€349', per='paid once · about £%d · no VAT added' % GBP_UNIQUE, hl=False,
         badge='', pts=['Same services included', 'A single payment', 'Legal pages included']),
]
PRICE_NOTE = ("Prices are set in euros, with no VAT added for UK clients. Pound amounts are approximate, at the "
              "rate of %s (€1 = £0.86), and change with the exchange rate. A .co.uk or .uk domain in your "
              "name is included for the first year." % TAUX_DATE)
PRIX_BRIEF = ("It costs <strong>€15 a month (about £%d)</strong> with no setup fee and no lock-in, or a "
              "<strong>one-off €349 (about £%d)</strong>, with no VAT added, and your demo is ready within "
              "24 hours." % (GBP_MOIS, GBP_UNIQUE))

ROW_AVIS = ('Reviews and testimonials', 'CAP Code, rules 3.44 to 3.50',
            "No fake reviews, no hiding negative reviews or giving positive ones more prominence, and say when a "
            "review was incentivised. Keep proof that each testimonial is genuine, and get permission before "
            "using it.")
ROW_DONNEES = ('Patient data', 'UK GDPR, art. 9; Data Protection Act 2018, s. 164A',
               "Health details sent through a contact form are special category data: you need a lawful basis and "
               "an Article 9 condition, and your privacy notice must explain them. Since 19 June 2026 you must "
               "also make it easy to complain about data protection and acknowledge each complaint within 30 days.")
ROW_COOKIES = ('Cookies and the ICO fee',
               'PECR, reg. 6 and Sch. A1; Data Protection (Charges and Information) Regulations 2018',
               "Advertising and tracking cookies need consent; some statistics and site-function cookies are "
               "exempt if visitors get clear information and a simple way to object. Organisations that handle "
               "personal data pay the ICO data protection fee unless exempt: £52 a year for the smallest tier.")

WHY_COMMUNS = [
    ('💷', 'A price a small practice can plan for',
     '€15 a month (about £%d) with no setup fee and no lock-in, or €349 (about £%d) once. No VAT added.'
     % (GBP_MOIS, GBP_UNIQUE)),
    ('👀', 'See it before you pay',
     "Your demo is ready within 24 hours. If it isn't right for you, you pay nothing."),
    ('💬', 'We work in English', 'Email, WhatsApp or video call, and we reply the same day.'),
]
WHERE_T = 'Anywhere in the UK'
WHERE = ("England, Scotland, Wales or Northern Ireland: we're based in Valencia, Spain, and work remotely, so "
         "where your practice is makes no difference.")
FAQ_AVIS = ("Can I show patient reviews on my website?",
            "Yes, if they are genuine and you have the patient's permission, and you don't hide negative reviews or "
            "give positive ones more prominence (CAP Code, rules 3.44 to 3.50). Keep evidence that each "
            "testimonial is real.")
FAQ_COMMUNES = [
    ("You're based in Spain: how do we work together?",
     "Remotely and in English, by email, WhatsApp or video call, and we reply the same day. You tell us about "
     "your practice, we build your demo within 24 hours, and you check every word before anything goes live."),
    ("How much does it cost, and do you add VAT?",
     "€15 a month (about £%d) with no setup fee and no lock-in, or a one-off €349 (about £%d), with the same "
     "services: design, hosting, a .co.uk or .uk domain in your name for the first year, legal pages adapted to "
     "UK law and one change a month. No VAT is added for UK clients. Prices are set in euros, so the amount in "
     "pounds depends on the exchange rate." % (GBP_MOIS, GBP_UNIQUE)),
    ("Who owns the website?",
     "With the one-off €349 payment, the website is yours. With the monthly plan, the domain is registered in "
     "your name and you keep it if you leave."),
]
STEPS_FIN = ('You decide', "You check every word and ask for any changes you want. If you like it, it goes live; "
                           "if not, you pay nothing.")
COMMUN = dict(
    html_lang='en', og_locale='en_GB', unit='month', area=['GB'],
    crumb_home='Home', cta='Get my free demo', cta2='What UK rules require', brief_t='In short',
    legal_id='rules', legal_ey='UK rules', legal_cols=('Topic', 'Source', 'What it means for your website'),
    legal_we_t='What we set up for you', sources_t='Sources', why_ey='Why us',
    where_t=WHERE_T, where=WHERE, sect_t='Who it is for', how_t='Your website in three steps',
    price_note=PRICE_NOTE, faq_t='Frequently asked questions',
    final_t='See your website before you pay a thing',
    final_sd='Free demo within 24 hours, copy and legal pages included. No setup fee, no lock-in.',
)
SRC_COMMUNES = [
    ('CAP Code, section 3', 'https://www.asa.org.uk/type/non_broadcast/code_section/03.html'),
    ('CAP Code, section 12', 'https://www.asa.org.uk/type/non_broadcast/code_section/12.html'),
    ('ICO, special category data',
     'https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/lawful-basis/a-guide-to-lawful-basis/special-category-data/'),
    ('Data Protection Act 2018, s. 164A', 'https://www.legislation.gov.uk/ukpga/2018/12/section/164A'),
    ('PECR, reg. 6', 'https://www.legislation.gov.uk/uksi/2003/2426/regulation/6'),
    ('ICO data protection fee',
     'https://ico.org.uk/for-organisations/data-protection-fee/changes-to-the-data-protection-fee/'),
]

# ═════════════════════════ DENTISTES ═══════════════════════════════════════
DENTAL = dict(
    COMMUN,
    title="Dental website design for UK practices: €15/month",
    description="Dental website design for UK practices, built around GDC advertising guidance: GDC numbers, "
                "fees, NHS or private status. Free demo in 24h, €15/month.",
    service_name="Dental website design for UK practices",
    audience="Dental practice owners in the United Kingdom",
    crumb='Dental website design',
    badge='For dentists in the UK',
    h1="Dental website design for <em>UK dentists</em>",
    lede="Your practice, your team, your fees and how to book, set out the way the GDC's guidance on advertising "
         "expects. We write it for you in English, you approve every word, and your free demo is ready within "
         "24 hours.",
    pills=['Written around GDC guidance', 'Fees and NHS or private status shown clearly', 'Free demo in 24 hours'],
    brief="WebAutonomos designs websites for dentists in the UK. We write the content in "
          "English from your real details, show what the GDC's guidance on "
          "advertising asks a practice website to display (qualifications, GDC numbers, complaints procedure, "
          "the date of the last update), and keep the website clear of what UK advertising rules ban: "
          "specialist titles you don't hold, claims you can't back up, and prescription-only medicines such as "
          "Botox. " + PRIX_BRIEF,
    legal_t='What your dental website has to get right in the UK',
    legal_intro="Dentistry is regulated across the UK by the General Dental Council (GDC), and a practice website "
                "counts as advertising. These are the points that matter for your site.",
    legal_rows=[
        ('Who treats patients', 'GDC Guidance on advertising, “Websites”',
         "Every dental professional named on the site must show their professional qualification, the country it "
         "comes from, and their GDC registration number."),
        ('Practice details', 'GDC Guidance on advertising, “Websites”',
         "The site must show the practice name and the address where care is provided, a phone number and email "
         "address, the GDC's contact details or a link to its website, your complaints procedure with who "
         "patients can turn to next (the NHS body for NHS care, the Dental Complaints Service for private care), "
         "and the date the site was last updated. Keep staff and services up to date."),
        ('NHS or private', 'GDC Guidance on advertising, “Advertising services”; Standards for the Dental Team, 1.7.2',
         "Say whether the practice is NHS, mixed or wholly private. A mixed practice must make clear which "
         "treatments are available on the NHS and which only privately."),
        ('Fees', 'Standards for the Dental Team, 2.4.2; CAP Code, rules 3.17 and 3.18',
         "Give clear information on prices on your website: patients shouldn't have to ask for it. Quoted prices "
         "must include any fees that aren't optional and must not mislead."),
        ('Specialist titles', 'GDC Guidance on advertising, “Specialist titles”',
         "Only a dentist on a GDC specialist list can use “Specialist” or titles such as Orthodontist or "
         "Periodontist. Others may write “special interest in”, “experienced in” or “practice limited to”."),
        ('Claims and comparisons',
         'GDC Guidance on advertising, “Advertising services” and “Websites”; CAP Code, rules 3.7 and 12.1',
         "Back up claims with facts, avoid ambiguous statements and anything likely to create unjustified "
         "expectations about results; objective claims need evidence before you publish them. Don't compare "
         "your team's skills or qualifications with other professionals'."),
        ('Botox and other prescription medicines',
         'CAP Code, rule 12.12; Human Medicines Regulations 2012, reg. 284',
         "Prescription-only medicines, such as botulinum toxin, can't be advertised to the public, so facial "
         "aesthetics pages need careful wording."),
        ROW_AVIS,
        ('Patient photos', 'Standards for the Dental Team, 4.2.9; ASA advice “Dental: General”',
         "Photos and videos of patients are confidential and can't be taken without the patient's permission; "
         "before-and-after pictures must also be genuine and representative."),
        ('CQC rating (England)', 'Regulated Activities Regulations 2014, reg. 20A',
         "A provider that has received a CQC rating must show it on its website, with its date and where to find "
         "the report. The CQC doesn't rate primary care dental services, so most practices have no rating to "
         "display."),
        ROW_DONNEES,
        ROW_COOKIES,
    ],
    legal_note="In Wales, private dental practices must also publish their statement of purpose and patient "
               "information leaflet on their website (Private Dentistry (Wales) Regulations 2017, regs. 5 and 6). "
               "NHS contractors in England must keep their NHS.uk profile accurate and review it at least every "
               "90 days. The GDC consulted from June to August 2026 on replacing its Standards with a new "
               "“Framework for Professionalism”; until its Council decides, the 2013 Standards and advertising "
               "guidance apply. This is general information as of September 2026, not legal advice: check with "
               "the GDC, your indemnity provider or your professional association.",
    spain_note='<strong>Practising in Spain?</strong> Spanish rules are different. See '
               '<a href="https://webautonomos.es/en/website-for-dentists-in-spain">websites for dentists and '
               'dental clinics in Spain</a>.',
    legal_we=["Each dentist's qualification, the country it comes from and their GDC number, plus the practice "
              "details, complaints procedure and last-updated date the GDC guidance lists",
              "A clear NHS, mixed or private statement and your fees on the site",
              "Treatments described without promises of results, specialist titles you don't hold or "
              "prescription-only medicine names",
              "A privacy policy and cookie notice adapted to UK law (UK GDPR)",
              "A .co.uk or .uk domain in your name, hosting, an SSL certificate and daily backups"],
    why_t='Built for UK dentistry',
    why=[('📋', 'GDC details in place',
          'Qualifications, GDC numbers, complaints procedure and last-updated date, set out where patients and '
          'the GDC guidance expect them.')] + WHY_COMMUNS,
    sectors=['🦷 General dentistry', '🏥 Mixed NHS and private care', '✨ Private practices',
             '😁 Orthodontic care', '🧑‍⚕️ Group practices'],
    steps=[('Tell us about your practice', 'Your treatments, your team, your fees, your location and when '
                                           'you\'re open: it takes two minutes to share what we need for your '
                                           'website design.'),
           ('We build your demo', 'Within 24 hours, with your design, your copy in English and your legal '
                                  'pages, ready for you to check online.'),
           STEPS_FIN],
    extra=[
        ('website-content', 'Content', 'What to include on a dental practice website',
         '<p class="legal-intro">Patients choosing a dental practice want to find the same things quickly, '
         'however they land on your website: who treats them, what care is on offer, and how to get in touch. '
         'Good web design puts these first, instead of burying them under general information. We write this '
         'content for you in English, for you to check before it goes live.</p>'
         '<div class="why-g">'
         '<div class="aud-c"><div class="aud-i" aria-hidden="true">🦷</div>'
         '<h3>Your treatments, described plainly</h3>'
         '<p>General dentistry, hygiene, cosmetic work or orthodontics: each treatment written in plain '
         'language, without a promise of results (see the rules above), so a new patient understands what it '
         'involves before they book.</p></div>'
         '<div class="aud-c"><div class="aud-i" aria-hidden="true">🧑‍⚕️</div>'
         '<h3>Your team and their GDC registration</h3>'
         '<p>Every dental professional named on the page, introduced with the qualification, the country it comes '
         'from and the GDC number the rules above require, so patients know who is treating them and can look up '
         'their registration directly with the GDC.</p></div>'
         '<div class="aud-c"><div class="aud-i" aria-hidden="true">💷</div>'
         '<h3>Fees a patient can read before they call</h3>'
         '<p>Clear fees shown on your website, the way the rules above require, so patients don\'t have to '
         'phone or search elsewhere to find out what a visit or a course of treatment costs.</p></div>'
         '<div class="aud-c"><div class="aud-i" aria-hidden="true">📞</div>'
         '<h3>More than one way to get in touch</h3>'
         '<p>A contact form, a phone number and a WhatsApp button, plus a link to the booking tool you already '
         'use if you have one, so patients who find your website can reach the practice however suits them '
         'best.</p></div>'
         '<div class="aud-c"><div class="aud-i" aria-hidden="true">📍</div>'
         '<h3>Your location and when you\'re open</h3>'
         '<p>Your address and opening times, so a patient can check when the practice is open before they '
         'call or make the trip.</p></div>'
         '</div>'),
        ('good-design', 'Design', 'What good dental website design looks like',
         '<p class="legal-intro">Good dental website design isn\'t only about how the page looks or how well '
         'it performs for SEO; it\'s about whether a visitor finds the information they need and decides to '
         'get in touch.</p>'
         '<div class="why-g">'
         '<div class="aud-c"><div class="aud-i" aria-hidden="true">🎨</div>'
         '<h3>Clean, modern web design that loads fast</h3>'
         '<p>Professional web design pairs a clean, modern look with plain headings and short content, '
         'built to load fast on mobile as well as on desktop, so visitors don\'t give up '
         'looking before they reach your contact details.</p></div>'
         '<div class="aud-c"><div class="aud-i" aria-hidden="true">🧭</div>'
         '<h3>An easy path from visitor to enquiry</h3>'
         '<p>Every page leads somewhere: a clear button to your contact form, phone number or WhatsApp, so a '
         'visitor who\'s ready to book doesn\'t have to search for how.</p></div>'
         '<div class="aud-c"><div class="aud-i" aria-hidden="true">🤝</div>'
         '<h3>Design that builds trust</h3>'
         '<p>Genuine Google reviews, shown with each reviewer\'s permission and without hiding the negative ones '
         '(see the rules above), your GDC registration and straightforward fees do more for trust than '
         'decoration. Good design gives these details room instead of hiding them below a slideshow.</p></div>'
         '<div class="aud-c"><div class="aud-i" aria-hidden="true">🏷️</div>'
         '<h3>Branding that matches the rest of your practice</h3>'
         '<p>Your logo, colours and photos, carried through consistently, so your website matches your '
         'practice\'s wider online presence, from your Google Business Profile to social media.</p></div>'
         '</div>'),
        ('local-search-help', 'Local search', 'How patients search for a local dental practice',
         '<p class="legal-intro">Getting found by someone searching for a local dentist depends on more than '
         'your website design. Search engines and patients read the same pages, so make sure the essentials '
         'are easy to find.</p>'
         '<div class="why-g">'
         '<div class="aud-c"><div class="aud-i" aria-hidden="true">🔍</div>'
         '<h3>Basic SEO, included in your website</h3>'
         '<p>Page titles and copy built around your treatments and your local area, kept consistent with your '
         'Google Business Profile, come at no extra cost, helping your practice appear '
         'in relevant local search results.</p></div>'
         '<div class="aud-c"><div class="aud-i" aria-hidden="true">📈</div>'
         '<h3>Local SEO and your Google listing, if you want more</h3>'
         '<p>If you want to go further than the basic SEO included in your website, we also offer local SEO and '
         'help managing your Google Business Profile. Ask us for prices when you get your demo.</p></div>'
         '<div class="aud-c"><div class="aud-i" aria-hidden="true">📱</div>'
         '<h3>Searches your website should answer</h3>'
         '<p>Before they book, patients may search for things like:</p>'
         '<ul><li>an emergency dentist near them</li><li>a practice accepting new patients</li>'
         '<li>a dentist open on Saturdays or evenings</li><li>a well-reviewed dental practice nearby</li>'
         '</ul>'
         '<p>Many of these searches happen on mobile, so your website needs to read as well on a small screen '
         'as it does on a desktop.</p></div>'
         '</div>'),
        ('technical-basics', 'Behind the scenes', 'What runs behind your website',
         '<p class="legal-intro">Alongside the pages your patients read online, a few technical basics come '
         'with every website we build.</p>'
         '<div class="why-g">'
         '<div class="aud-c"><div class="aud-i" aria-hidden="true">🔒</div>'
         '<h3>Hosting, SSL and daily backups</h3>'
         '<p>Your website includes hosting, an SSL certificate, daily backups, 24/7 monitoring and technical '
         'maintenance, so the technical side isn\'t something you need to think about.</p></div>'
         '<div class="aud-c"><div class="aud-i" aria-hidden="true">🔗</div>'
         '<h3>Links to your social media</h3>'
         '<p>We add links to your Facebook, Instagram or other social media profiles on your website, so '
         'patients can move easily between your website and your social media.</p></div>'
         '<div class="aud-c"><div class="aud-i" aria-hidden="true">✏️</div>'
         '<h3>One change a month, included</h3>'
         '<p>Once your website is live, you can ask for one change a month at no extra cost, such as updating '
         'your team, your fees or anything you\'d like to improve. A full redesign or a large new section '
         'goes through a fixed quote agreed before any work starts.</p></div>'
         '<div class="aud-c"><div class="aud-i" aria-hidden="true">📄</div>'
         '<h3>Your policies, ready to publish</h3>'
         '<p>A privacy policy and cookie notice, adapted to UK law, are included with your website, and every '
         'word is written for you to check before it goes live.</p></div>'
         '</div>'),
        ('website-mistakes', 'What to avoid', 'Common mistakes on dental practice websites',
         '<p class="legal-intro">Some gaps show up again and again on dental websites, and they tend to cost new '
         'enquiries before anyone gets in touch.</p>'
         '<div class="cmp-c them" style="max-width:640px;margin:0 auto;"><ul>'
         '<li>A layout that is hard to read on mobile, so patients searching from their phone give up before '
         'they find your details</li>'
         '<li>Fees left out, so a visitor has to search elsewhere before they know what a course of treatment '
         'costs</li>'
         '<li>Stock photography and generic copy that could describe any dentist\'s website, not yours</li>'
         '<li>No visible GDC registration, complaints procedure or last-updated date, even though the GDC\'s '
         'guidance expects them</li>'
         '<li>A way to get in touch that is hard to spot, buried below several screens of content</li>'
         '</ul></div>'
         '<div class="aud-c" style="max-width:640px;margin:24px auto 0;"><h3>What to do instead</h3>'
         '<p>A simple, mobile-friendly layout, your own fees and treatments written in plain English, and the '
         'GDC details that patients and the regulator both expect. Together, they help a visitor who is just '
         'looking trust what they read and get in touch.</p></div>'),
        ('vs-general-website', 'Compare', 'How dental website design is different from a general business website',
         '<p class="legal-intro">General website builders and templates are not written with the GDC\'s '
         'advertising guidance in mind. Here is what changes when your website design starts from those rules, '
         'not a generic template.</p>'
         '<div class="cmp-g">'
         '<div class="cmp-c them"><h3>A general website builder</h3><ul>'
         '<li>A generic template you adapt yourself, with no reference to GDC advertising guidance</li>'
         '<li>You write and structure the content yourself, including the GDC numbers, fees and complaints '
         'procedure the rules require</li>'
         '<li>SEO settings such as page titles and descriptions, left for you to fill in yourself</li>'
         '<li>Support often starts with a help centre rather than a person who replies the same day</li>'
         '</ul></div>'
         '<div class="cmp-c us"><h3>Dental website design from WebAutonomos</h3><ul>'
         '<li>Content and layout designed around what the GDC\'s guidance on advertising expects, from the first '
         'draft</li>'
         '<li>Your treatments, fees and GDC numbers written for you in English, for you to check before anything '
         'goes live</li>'
         '<li>Basic SEO and a design made for mobile, included at no extra cost</li>'
         '<li>A direct reply the same day, by email or WhatsApp, whenever you have a question</li>'
         '</ul></div>'
         '</div>'
         '<p class="cmp-more"><a href="https://webautonomos.es/en/services">See everything included in your '
         'website →</a></p>'),
        ('website-experience', 'Experience', 'Why the experience on your website matters as much as the design',
         '<p class="legal-intro">Choosing a dentist often starts online, making the experience a visitor has on '
         'your website worth getting right from day one.</p>'
         '<div class="why-g">'
         '<div class="aud-c"><div class="aud-i" aria-hidden="true">⏱️</div><h3>Your fees and how to book, within '
         'seconds</h3><p>Good dental website design gets out of the way: a visitor should see your fees, your '
         'treatments and how to arrange an appointment within a few seconds, not after scrolling past everything '
         'else.</p></div>'
         '<div class="aud-c"><div class="aud-i" aria-hidden="true">📱</div><h3>The same experience on mobile as '
         'on desktop</h3><p>Many of your patients will look for you on their phone, so the mobile version of '
         'your website shows the same fees, the same GDC details and the same ways to get in touch as the '
         'desktop version.</p></div>'
         '<div class="aud-c"><div class="aud-i" aria-hidden="true">🎯</div><h3>A demo built from your details, '
         'not a template</h3><p>Every project starts the same way: we build the demo from your own details, you '
         'review it, and we change anything that isn\'t right before it goes live, so you never start from a '
         'blank page.</p></div>'
         '<div class="aud-c"><div class="aud-i" aria-hidden="true">📈</div><h3>Part of a wider marketing '
         'strategy</h3><p>Your website is usually the first stop, but not the only one: local SEO and your '
         'Google Business Profile often come next. For a small practice, it makes sense to get these basics '
         'right before spending on anything else.</p></div>'
         '</div>'
         '<p class="legal-intro">If you would like more background on getting the basics right, our '
         '<a href="https://webautonomos.es/blog/#en">blog</a> has practical guides on local SEO and improving '
         'your Google Business Profile.</p>'),
    ],
    faq=[("What must a dental practice website show?",
          "Under the GDC's guidance on advertising: each dental professional's qualification, the country it "
          "comes from and their GDC number; the practice name and address; a phone number and email; the GDC's "
          "contact details or a link to its website; your complaints procedure and who patients can contact "
          "next; and the date the site was last updated. You must also say whether the practice is NHS, mixed or "
          "private, and give clear information on fees."),
         ("Can I call myself a specialist?",
          "Only if you are on a GDC specialist list. Otherwise, avoid titles such as Orthodontist or "
          "Periodontist and wording like “specialising in”; the GDC allows “special interest in”, “experienced "
          "in” or “practice limited to”."),
         ("Can I mention Botox on my website?",
          "Botulinum toxin is a prescription-only medicine, and those can't be advertised to the public (CAP "
          "Code, rule 12.12). The ASA's advice on this is strict, so we keep product names out of your "
          "promotional copy."),
         FAQ_AVIS,
         ("Do I need to display a CQC rating?",
          "Only if the CQC has rated you: rated providers must show their latest rating on their website "
          "(regulation 20A). The CQC doesn't rate primary care dental services, so most dental providers have "
          "no rating to display."),
         ("Can patients book an appointment directly through my website?",
          "There's no booking system built into the website. If you already use a booking tool, we can add a link "
          "or button to it, next to your contact form and phone number, so patients still have a quick way "
          "to book. Otherwise, appointment requests reach you by email through the contact form or by "
          "WhatsApp."),
         ("Does website design really affect my results?",
          "Yes: a confusing first experience makes visitors leave before they see what you offer, however good "
          "the work behind it is. Simple design, clear fees and an easy way to get in touch give them what they "
          "need to decide to contact you."),
         ("Can a dental website help with marketing?",
          "Both plans include basic SEO, which helps your website appear online for relevant local searches. If "
          "you want to go further, we also offer local SEO and help managing your Google Business Profile: ask "
          "us for prices when you request your demo."),
         ("Do you offer digital marketing beyond the website itself?",
          "Yes, on request: alongside your website, we can help with paid advertising, such as Google Ads or "
          "Facebook ads, and with managing your social media. Ask us and we'll explain what's involved and the "
          "cost."),
         ("What makes a good dental website, beyond how it looks?",
          "A good dental website answers the questions a new patient has before they call: your fees, your "
          "treatments and how to get in touch, written and structured for you so you don't have to build or "
          "write any of it yourself.")] + FAQ_COMMUNES,
)
SRC_DENTAL = [
    ('GDC Guidance on advertising',
     'https://www.gdc-uk.org/standards-guidance/standards-and-guidance/gdc-guidance-for-dental-professionals/guidance-on-advertising'),
    ('GDC Standards for the Dental Team',
     'https://www.gdc-uk.org/standards-guidance/standards-and-guidance/standards-for-the-dental-team'),
    ('Regulation 20A', 'https://www.legislation.gov.uk/uksi/2014/2936/regulation/20A'),
    ('CQC, services we do not rate',
     'https://www.cqc.org.uk/guidance-regulation/providers/assessment/assessing-quality-and-performance/services-we-do-not-rate'),
    ('Private Dentistry (Wales) Regulations 2017', 'https://www.legislation.gov.uk/wsi/2017/202/regulation/5'),
] + SRC_COMMUNES

# ═════════════════════════ KINÉSITHÉRAPEUTES ═══════════════════════════════
PHYSIO = dict(
    COMMUN,
    title="Physiotherapy website design for UK clinics: €15/month",
    description="Physiotherapy website design for UK clinics, built around HCPC standards and UK rules on health "
                "claims. Free demo in 24h, €15/month.",
    service_name="Physiotherapy website design for UK clinics",
    audience="Physiotherapists and physiotherapy clinic owners in the United Kingdom",
    crumb='Physiotherapy website design',
    badge='For physiotherapists and clinics in the UK',
    h1="Physiotherapy website design for <em>UK physiotherapists and clinics</em>",
    lede="Your clinic, your team, your treatments and how to book, written with HCPC standards and UK advertising "
         "rules in mind. We write it for you in English, you approve every word, and your free demo is ready "
         "within 24 hours.",
    pills=['Written around HCPC and CAP rules', "No health claims you can't back up", 'Free demo in 24 hours'],
    brief="WebAutonomos designs websites for physiotherapists and physiotherapy clinics in the UK. We write the "
          "copy in English from your real details, present your team with the titles they are entitled to use, "
          "and keep the site clear of what UK rules ban: health claims you can't back up, misuse of protected "
          "titles, and fake or cherry-picked reviews. " + PRIX_BRIEF,
    legal_t='What your physiotherapy website has to get right in the UK',
    legal_intro="Physiotherapy is a regulated profession across the UK: the titles are protected by law, and the "
                "Health and Care Professions Council (HCPC) sets the standards. Your website is advertising, so "
                "UK advertising rules apply too.",
    legal_rows=[
        ('Protected titles', 'Health Professions Order 2001, art. 39; SI 2003/1571, Sch. 1',
         "Only professionals registered with the HCPC may call themselves “physiotherapist” or “physical "
         "therapist”. Using a protected title, or claiming registration, with intent to deceive is a criminal "
         "offence."),
        ('Describing your services', 'HCPC, “Misuse of title”',
         "Describing a service as “physiotherapy” can imply the title, so it must be delivered by HCPC "
         "registrants. Someone who isn't registered can own the clinic."),
        ('“Chartered Physiotherapist”', 'CSP, “Using the CSP brand”',
         "The title isn't protected by law, but the Chartered Society of Physiotherapy reserves it for its "
         "qualified members. Clinics and businesses shouldn't use “chartered” in their name or publicity."),
        ('HCPC logo', 'HCPC logo terms and conditions',
         "Only an individual registrant can use the “HCPC registered” logo, next to their own name: never for "
         "the clinic or as part of a trading name."),
        ('Honest promotion', 'HCPC Standards of conduct, performance and ethics (2024), 9.2 and 9.3',
         "Be honest about experience, qualifications and skills, and make sure any promotion you take part in "
         "is accurate and not likely to mislead."),
        ('Health claims', 'CAP Code, rules 12.1, 12.2 and 3.7; ASA advice “Health: Physiotherapy”',
         "Claims to treat a condition need evidence before you publish them. The ASA's advice lists the "
         "conditions it is likely to accept for physiotherapy, such as back pain, joint pains and minor sports "
         "injuries; anything else needs documentary evidence, usually clinical trials."),
        ('No cure claims', 'CAP Code, rules 12.6 and 12.7',
         "Falsely claiming to treat a disease is banned, and wording such as “cure” is generally not "
         "acceptable."),
        ROW_AVIS,
        ('CQC (England)', 'Regulated Activities Regulations 2014, Sch. 1, para. 4',
         "A standalone physiotherapy practice doesn't need to register with the CQC. A clinic whose team "
         "includes a listed professional, such as a doctor or nurse, may have to."),
        ROW_DONNEES,
        ROW_COOKIES,
    ],
    legal_note="Patient stories and case studies need care: the HCPC standards only allow confidential "
               "information to be shared with the patient's permission or on other listed grounds (standard 5.2). "
               "A company or business name that includes a protected title needs the HCPC's letter of "
               "non-objection first. This is general information as of September 2026, not legal advice: check "
               "with the HCPC or your professional body.",
    spain_note='<strong>Working in Spain?</strong> Spanish rules are different. See '
               '<a href="https://webautonomos.es/en/website-for-physiotherapists-in-spain">websites for '
               'physiotherapists in Spain</a>.',
    legal_we=["Each physiotherapist's name with the protected title they hold, and “chartered” or the HCPC logo "
              "only where the rules allow them",
              "Treatments described without cure claims or conditions you can't back up with evidence",
              "A contact form that asks only what it needs",
              "A privacy policy and cookie notice adapted to UK law (UK GDPR)",
              "A .co.uk or .uk domain in your name, hosting, an SSL certificate and daily backups"],
    why_t='Built for UK physiotherapists',
    why=[('📋', 'Titles used correctly',
          'Protected titles, HCPC registration and CSP membership shown the way the rules allow.')] + WHY_COMMUNS,
    sectors=['💆 Private physiotherapy clinics', '🏃 Sports physiotherapy', '🧑‍⚕️ Independent physiotherapists',
             '🏠 Home-visit physiotherapists'],
    steps=[('Tell us about your clinic', 'Your treatments, your team, your fees and opening hours: it takes '
                                         'two minutes.'),
           ('We build your demo', 'Within 24 hours, with your copy in English and your legal pages.'),
           STEPS_FIN],
    faq=[("Who can call themselves a physiotherapist in the UK?",
          "Only professionals registered with the HCPC: “physiotherapist” and “physical therapist” are protected "
          "titles, and misusing them with intent to deceive is a criminal offence (Health Professions Order "
          "2001, art. 39)."),
         ("Can I call myself a Chartered Physiotherapist?",
          "Only if you are a qualified member of the Chartered Society of Physiotherapy. The title isn't "
          "protected by law, but the CSP reserves it for members, and clinics shouldn't use “chartered” in their "
          "name or publicity."),
         ("Which conditions can my website say I treat?",
          "The ASA's advice lists conditions it is likely to accept for physiotherapy, including back pain, joint "
          "pains, muscle spasms and minor sports injuries. For anything else, you need documentary evidence, "
          "usually clinical trials, before you make the claim (CAP Code, rule 12.1)."),
         FAQ_AVIS,
         ("Does my practice need to register with the CQC?",
          "Not if it is a standalone physiotherapy practice in England: physiotherapists aren't on the list of "
          "professionals whose treatment triggers registration. A clinic whose team includes a listed "
          "professional, such as a doctor or nurse, may need to register."),
         ("What if I want bigger changes later, like a new section on my site?",
          "For bigger changes, such as a redesign or a large new section, we give you a fixed-price quote first, so "
          "there are no surprises. One smaller change a month is already included in both plans, at no extra "
          "charge.")] + FAQ_COMMUNES,
    extra=[
        ('booking-enquiries', '', "Can patients book appointments through the website?",
         '<p class="legal-intro">The website isn\'t an online booking system, so there\'s no new software for you '
         'or your patients to learn.</p>\n  <div class="legal-we"><h3>How patients reach you</h3><ul>'
         '<li><span>A contact form that sends every enquiry straight to your own email inbox</span></li>'
         '<li><span>A WhatsApp button, for patients who prefer a faster reply</span></li>'
         '<li><span>A link to the booking tool you already use, if you have one</span></li></ul></div>'),
        ('seo-basics', '', "Does the website help me appear in Google searches?",
         '<p class="legal-intro">Both plans include basic search engine optimisation (SEO). It isn\'t ongoing '
         'local SEO work — if you want that, ask us and we\'ll explain what\'s involved.</p>\n  '
         '<div class="legal-we"><h3>What\'s included in your website\'s SEO</h3><ul>'
         '<li><span>Page titles and copy that name your treatments and your area</span></li>'
         '<li><span>Your details kept consistent across your website and your Google Business Profile</span></li>'
         '</ul></div>'),
        ('clinic-content', '', "Who writes the content for my physiotherapy website?",
         '<p class="legal-intro">We write all the content for you, in English, from the details you send us: '
         'your treatments, your team and your practice. It\'s tailored to you, never generic stock '
         'text, and written to be clear and easy for patients to read. You approve it before anything '
         'goes live. If your business changes later — new opening hours, a treatment you now offer — just '
         'tell us: one change a month is included in both plans.</p>'),
        ('worth-it', '', "Is a website worth it for a small physiotherapy business?",
         '<p class="legal-intro">Many patients look for a physio online, often from their phone, and check your '
         'website before they call, even when someone has recommended you by name. Even if you work alone, '
         'a clear, simple site does the job of a good reception desk, answering the questions patients would '
         'otherwise phone to ask.</p>\n  '
         '<div class="legal-we"><h3>What patients look for</h3><ul>'
         '<li><span>Your treatments and who provides them</span></li>'
         '<li><span>How to get in touch, by form, WhatsApp or phone</span></li>'
         '<li><span>Your fees and opening hours</span></li></ul></div>'),
    ],
)
SRC_PHYSIO = [
    ('Health Professions Order 2001, art. 39', 'https://www.legislation.gov.uk/uksi/2002/254/article/39'),
    ('HCPC, misuse of title', 'https://www.hcpc-uk.org/concerns/what-we-investigate/misuse-of-title/'),
    ('HCPC Standards of conduct, performance and ethics',
     'https://www.hcpc-uk.org/standards/standards-of-conduct-performance-and-ethics/'),
    ('HCPC logo terms', 'https://www.hcpc-uk.org/registration/your-registration/promote-your-registration/request-logo/'),
    ('CSP, using the CSP brand', 'https://www.csp.org.uk/about-csp/using-csp-brand'),
    ('ASA advice, physiotherapy', 'https://www.asa.org.uk/advice-online/health-physiotherapy.html'),
    ('Regulated Activities Regulations 2014, Sch. 1',
     'https://www.legislation.gov.uk/uksi/2014/2936/schedule/1/paragraph/4'),
] + SRC_COMMUNES

# ═════════════════════════ ARTISANS BRITANNIQUES (28/09/2026) ══════════════
# Trois pages décidées par Angelino le 28/09/2026 (Semrush Royaume-Uni, même jour) :
#   /en/web-design-for-tradesmen      « web design for tradesmen » 590/mois KD 3 (page mère)
#   /en/web-design-for-plumbers       « web design for plumbers » 390/mois KD 9
#   /en/web-design-for-electricians   « web design for electricians » 320/mois KD 7
# Règles vérifiées le 28/09/2026 sur legislation.gov.uk, gov.uk, HSE, Ofgem, CMA et ICO.
ROW_UK_DETAILS = ('Business details', 'Electronic Commerce Regulations 2002, reg. 6; Trading Disclosures '
                                      'Regulations 2015, regs 24 and 25',
                  "Your business name, a geographic address and an email address, plus, where they apply, your "
                  "Companies House (or other public register) number, your VAT number, the body that authorises "
                  "your trade, such as Gas Safe Register, and whether prices include VAT. A company also shows its "
                  "registered name, registered office and the part of the UK where it is registered.")
ROW_UK_CONTRATS = ('Jobs agreed at the customer\'s home', 'Consumer Contracts Regulations 2013, regs 19, 28, 29 '
                                                          'and 36',
                   "The customer can usually cancel within 14 days, and you can only start sooner if they ask on "
                   "paper or by email. Failing to give written cancellation information is a criminal offence. "
                   "There is no cancellation right for urgent repairs they called you out for, except for extra "
                   "work or other goods.")
ROW_UK_AVIS = ('Reviews, logos and approvals', 'Digital Markets, Competition and Consumers Act 2024, Sch. 20, '
                                               'paras 3, 4 and 13',
               "Under the DMCC Act, in force since 6 April 2025, it is banned outright to show a trust mark or "
               "quality mark you are not entitled to, to claim an approval you don't have, to post or buy fake "
               "reviews, to hide that a review was incentivised, or to hide negative reviews or give positive ones "
               "more prominence.")
FAQ_UK_CANCEL = ("Can customers cancel after an emergency call-out?",
                 "Not for the urgent repair itself: the Consumer Contracts Regulations 2013 (reg. 28) exclude "
                 "contracts where the customer specifically asked you to visit to carry out urgent repairs or "
                 "maintenance. The 14-day cancellation right still applies to extra work you agree during that "
                 "visit, and to goods other than the replacement parts you necessarily used.")
FAQ_UK_AVIS = ("Can I show reviews and trade body logos on my website?",
               "Yes, if they are genuine and you are entitled to them. Under the Digital Markets, Competition and "
               "Consumers Act 2024, in force since 6 April 2025, showing a trust mark or quality mark without "
               "authorisation, claiming an approval you don't have, posting or buying fake reviews and hiding "
               "negative reviews while publishing positive ones are all banned outright. After an investigation, the "
               "CMA can fine up to £300,000 or 10% of worldwide turnover, whichever is higher.")
WHY_TRADES = [
    ('💷', 'A price a sole trader can plan for',
     '€15 a month (about £%d) with no setup fee and no lock-in, or €349 (about £%d) once. No VAT added.'
     % (GBP_MOIS, GBP_UNIQUE)),
    ('👀', 'See it before you pay',
     "Your demo is ready within 24 hours. If it isn't right for you, you pay nothing."),
    ('💬', 'We work in English', 'Email, WhatsApp or video call, and we reply the same day.'),
]
FAQ_TRADES = [
    ("You're based in Spain: how do we work together?",
     "Remotely and in English, by email, WhatsApp or video call, and we reply the same day. You tell us about "
     "your business, we build your demo within 24 hours, and you check every word before anything goes live."),
    FAQ_COMMUNES[1],
    FAQ_COMMUNES[2],
]
STEPS_TRADES = [('Tell us about your business', 'Your trade, the areas you cover, your registrations and a few job '
                                                'photos: it takes two minutes.'),
                ('We build your demo', 'Within 24 hours, with your services, your copy in English and your legal '
                                       'pages, ready for you to check online.'),
                STEPS_FIN]
COMMUN_TRADES = dict(
    COMMUN,
    where="England, Scotland, Wales or Northern Ireland: we're based in Valencia, Spain, and work remotely, so "
          "where your business is makes no difference.",
    final_sd='Free demo within 24 hours, with your services and legal pages. No setup fee, no lock-in.',
)


def local_search_uk(trade):
    return ('local-search-help', 'Local search', 'How customers find a local %s' % trade,
            '<p class="legal-intro">Getting found by someone searching for a local %s depends on more than your '
            'website design. Search engines and customers read the same pages, so make sure the essentials are '
            'easy to find.</p>'
            '<div class="why-g">'
            '<div class="aud-c"><div class="aud-i" aria-hidden="true">🔍</div>'
            '<h3>Basic SEO, included in your website</h3>'
            '<p>Page titles and copy built around your services and the towns you cover, kept consistent with your '
            'Google Business Profile, come at no extra cost.</p></div>'
            '<div class="aud-c"><div class="aud-i" aria-hidden="true">📈</div>'
            '<h3>Local SEO and your Google listing, if you want more</h3>'
            '<p>If you want to go further than the basic SEO included in your website, we also offer local SEO and '
            'help managing your Google Business Profile. Ask us for prices when you get your demo.</p></div>'
            '<div class="aud-c"><div class="aud-i" aria-hidden="true">📱</div>'
            '<h3>Built for the phone in someone\'s hand</h3>'
            '<p>Many people look for a tradesperson on their phone, sometimes in a hurry. Your number, a call '
            'button and WhatsApp stay in view on every page.</p></div>'
            '</div>' % trade)


TRADES = dict(
    COMMUN_TRADES,
    title="Web design for tradesmen in the UK: €15/month",
    description="Web design for tradesmen in the UK: your services, registrations and legal pages, built around UK "
                "consumer rules. Free demo in 24h, €15/month, no VAT added.",
    service_name="Web design for tradesmen in the UK",
    audience="Tradespeople and small building firms in the United Kingdom",
    crumb='Web design for tradesmen',
    badge='For tradespeople and builders in the UK',
    h1="Web design for <em>tradesmen</em> in the UK",
    lede="Your services, the areas you cover, your registrations and a quote request in one tap, written with UK "
         "consumer rules in mind. We write it for you in English, you approve every word, and your free demo is "
         "ready within 24 hours.",
    pills=['Registrations shown as you hold them', 'Built around UK consumer rules', 'Free demo in 24 hours'],
    brief="WebAutonomos designs websites for tradespeople and small building firms in the UK: builders, plumbers, "
          "electricians, roofers, carpenters and more. We write the copy in English from your real details, show "
          "your trade body and scheme registrations as you hold them, and include the information UK law expects "
          "on a business website. " + PRIX_BRIEF,
    legal_t='What UK rules mean for a tradesman\'s website',
    legal_intro="Your website counts as advertising, and the quotes and jobs that come from it are consumer "
                "contracts. These are the rules that matter for tradespeople and builders.",
    legal_rows=[
        ROW_UK_DETAILS,
        ROW_UK_CONTRATS,
        ('What you say is binding', 'Consumer Rights Act 2015, ss. 49 to 52',
         "Work must be done with reasonable care and skill. What you tell a customer, on your website or in your "
         "quote, can become part of the contract if they rely on it; if no price or finish date was agreed, a "
         "reasonable price and a reasonable time apply."),
        ROW_UK_AVIS,
        ('Building regulations (England)', 'Building Regulations 2010, reg. 12 and Sch. 3',
         "Notifiable work, such as a new circuit, a consumer unit, a boiler or replacement windows, needs building "
         "control approval unless an installer registered with a competent person scheme self-certifies it. "
         "Homeowners can check scheme membership online."),
        ('Health and safety on home jobs', 'Construction (Design and Management) Regulations 2015, regs 7 and 15',
         "On a domestic job the client's duties pass to you as the contractor (or to the principal contractor if "
         "there are several), and you draw up a construction phase plan before work starts."),
        ('Asbestos', 'Control of Asbestos Regulations 2012, regs 8 and 9',
         "Higher-risk work, such as most work on asbestos insulating board, pipe lagging, sprayed coatings or loose "
         "fill, needs an HSE-licensed contractor, and some lower-risk work must be notified before it starts."),
        ('Construction waste (England)', 'Waste (England and Wales) Regulations 2011, reg. 24',
         "A builder who carries their own construction or demolition waste registers with the Environment Agency as "
         "an upper-tier waste carrier: the free lower tier doesn't cover it."),
        ROW_COOKIES,
    ],
    legal_note="Building control, waste and some other rules differ in Wales, Scotland and Northern Ireland: check "
               "the rules for your area. This is general information as of September 2026, not legal advice.",
    spain_note='<strong>Working in Spain?</strong> Spanish rules are different. See '
               '<a href="https://webautonomos.es/en/website-for-builders-in-spain">websites for builders and '
               'renovation companies in Spain</a>.',
    legal_we=["Your business details as the E-Commerce Regulations list them, plus your company details if you "
              "trade as a limited company",
              "Your trade body and scheme registrations shown as you hold them, with nothing you're not entitled to",
              "Reviews shown honestly: genuine, without hiding the negative ones or giving the positive ones more "
              "prominence",
              "A privacy policy and cookie notice adapted to UK law (UK GDPR and PECR)",
              "A .co.uk or .uk domain in your name, hosting, an SSL certificate and daily backups"],
    why_t='Built for UK trades',
    why=[('🧰', 'Your trade, your way', 'Services, areas covered, registrations and job photos, set out the way '
                                       'customers look for them.')] + WHY_TRADES,
    sectors=['🏗️ Builders', '🔧 Plumbers', '⚡ Electricians', '🏠 Roofers', '🪵 Carpenters and joiners',
             '🎨 Painters and decorators', '🟫 Tilers', '🌳 Landscapers'],
    steps=STEPS_TRADES,
    extra=[
        ('website-content', 'Content', "What to put on a tradesman's website",
         '<p class="legal-intro">Someone looking for a tradesperson wants to know three things quickly: do you do '
         'the job they need, do you cover their area, and how do they reach you? A tradesman\'s website answers '
         'those best with a contact form or phone number close by.</p>'
         '<div class="why-g">'
         '<div class="aud-c"><div class="aud-i" aria-hidden="true">🗂️</div>'
         '<h3>Your services, grouped by job</h3>'
         '<p>Extensions, bathrooms, rewires or roof repairs each get their own section, so a visitor finds their '
         'job without scrolling through everything else.</p></div>'
         '<div class="aud-c"><div class="aud-i" aria-hidden="true">📍</div>'
         '<h3>The towns you cover</h3>'
         '<p>Naming the towns and villages you cover tells a visitor straight away whether you\'ll come to them, '
         'and helps search engines find your site for local searches.</p></div>'
         '<div class="aud-c"><div class="aud-i" aria-hidden="true">✅</div>'
         '<h3>Registrations people can check</h3>'
         '<p>Gas Safe, NICEIC, NAPIT, TrustMark or a trade association: shown with your number where there is one, '
         'so a customer can check it, and only the ones you actually hold.</p></div>'
         '<div class="aud-c"><div class="aud-i" aria-hidden="true">📸</div>'
         '<h3>Photos of finished jobs</h3>'
         '<p>We build your site around your own job photos, grouped by type of work, with a '
         'one-line caption for each.</p></div>'
         '</div>'),
        ('by-trade', 'By trade', 'Trades website design that fits your rules',
         '<p class="legal-intro">Some trades have their own rules on what they can claim and who is qualified to '
         'carry out the job. We cover them page by page.</p>'
         '<div class="why-g">'
         '<div class="aud-c"><div class="aud-i" aria-hidden="true">🔧</div>'
         '<h3><a href="https://webautonomos.es/en/web-design-for-plumbers">Web design for plumbers</a></h3>'
         '<p>Gas Safe registration and logo rules, boilers and building regulations, unvented cylinders and the '
         'Boiler Upgrade Scheme.</p></div>'
         '<div class="aud-c"><div class="aud-i" aria-hidden="true">⚡</div>'
         '<h3><a href="https://webautonomos.es/en/web-design-for-electricians">Web design for electricians</a>'
         '</h3>'
         '<p>Part P and competent person schemes, landlord inspections, EV chargers and solar panels.</p></div>'
         '<div class="aud-c"><div class="aud-i" aria-hidden="true">🏗️</div>'
         '<h3>Builders and construction firms</h3>'
         '<p>Every rule in the table above applies to a building firm, including building control, CDM duties on '
         'home jobs, asbestos and waste. For construction website design, that means showing only the '
         'registrations and licences you actually hold, such as a waste carrier registration.</p></div>'
         '</div>'),
        local_search_uk('tradesperson'),
    ],
    faq=[("What must a tradesman's website show by law?",
          "Under the Electronic Commerce Regulations 2002 (reg. 6): your business name, a geographic address and "
          "an email address, plus, where they apply, your Companies House (or other public register) number, your "
          "VAT number, the body that authorises your trade, such as Gas Safe Register, and whether your prices "
          "include VAT. A company must also show its registered name, company number, registered office and the "
          "part of the UK where it is registered (Trading Disclosures Regulations 2015, regs 24 and 25)."),
         ("Can a customer cancel a job they agreed at home?",
          "Usually, yes: a contract agreed at the customer's home gives them 14 days to cancel (Consumer Contracts "
          "Regulations 2013). You can only start within those 14 days if they ask you to on a durable medium, such "
          "as paper or email, and if they then cancel they pay a proportionate amount for the work done, provided "
          "you gave them the cancellation information. Failing to give written "
          "cancellation information for such a contract is a criminal offence, and the cancellation period then "
          "extends by up to 12 months. Contracts of £42 or less are exempt."),
         ("Is my quote binding?",
          "What you say or write to a customer, including your quote, can become part of the contract if they "
          "rely on it (Consumer Rights Act 2015, ss. 50 to 52). If no price was agreed, they only have to pay a "
          "reasonable price, and if no finish date was agreed, the work must be done within a reasonable time."),
         FAQ_UK_AVIS,
         FAQ_UK_CANCEL,
         ("What are my health and safety duties on a home job?",
          "Under the Construction (Design and Management) Regulations 2015, a domestic client's duties pass to the "
          "contractor, or to the principal contractor if there is more than one, and the contractor draws up a "
          "construction phase plan before setting up the site."),
         ("Do builders need a waste carrier registration?",
          "In England, yes, if you carry your own construction or demolition waste: you need an upper-tier "
          "registration with the Environment Agency, because the free lower tier doesn't cover construction "
          "waste. Householders must check a carrier's registration before handing over their waste."),
         ("Is TrustMark compulsory?",
          "Not in general. TrustMark is the government-endorsed quality scheme for work in and around the home, "
          "and registration is required for some funded schemes, such as ECO4, which runs until 31 December 2026, "
          "and the Warm Homes: Local Grant in England."),
         ("Is there VAT on insulation, heat pumps and solar panels?",
          "Installing energy-saving materials in homes, such as insulation, heat pumps, solar panels and "
          "batteries, is zero-rated until 31 March 2027, then goes back to 5% (VAT Notice 708/6). Gas and oil "
          "boilers and ordinary central heating systems are not included; wood-fuelled boilers are.")] + FAQ_TRADES,
)
SRC_TRADES = [
    ('E-Commerce Regulations 2002, reg. 6', 'https://www.legislation.gov.uk/uksi/2002/2013/regulation/6'),
    ('Consumer Contracts Regulations 2013, reg. 28', 'https://www.legislation.gov.uk/uksi/2013/3134/regulation/28'),
    ('Consumer Rights Act 2015, s. 50', 'https://www.legislation.gov.uk/ukpga/2015/15/section/50'),
    ('DMCC Act 2024, Sch. 20', 'https://www.legislation.gov.uk/ukpga/2024/13/schedule/20'),
    ('Building regulations approval', 'https://www.gov.uk/building-regulations-approval'),
    ('HSE, CDM 2015 for domestic clients', 'https://www.hse.gov.uk/construction/cdm/2015/domestic-clients.htm'),
    ('HSE, licensed asbestos work', 'https://www.hse.gov.uk/asbestos/licensing/licensed-contractor.htm'),
    ('Waste carrier registration', 'https://www.gov.uk/register-renew-waste-carrier-broker-dealer-england'),
    ('VAT on energy-saving materials', 'https://www.gov.uk/guidance/vat-on-energy-saving-materials-and-heating-equipment-notice-7086'),
    ('PECR, reg. 6', 'https://www.legislation.gov.uk/uksi/2003/2426/regulation/6'),
]

PLUMB_UK = dict(
    COMMUN_TRADES,
    title="Web design for plumbers in the UK: €15/month",
    description="Web design for plumbers and heating engineers in the UK: Gas Safe details, services and legal "
                "pages, built around UK rules. Free demo in 24h, €15/month.",
    service_name="Web design for plumbers and heating engineers in the UK",
    audience="Plumbers, heating engineers and gas engineers in the United Kingdom",
    crumb='Web design for plumbers',
    badge='For plumbers and heating engineers in the UK',
    h1="Web design for <em>plumbers</em> and heating engineers",
    lede="Your services, your Gas Safe details, the areas you cover and a call or WhatsApp in one tap, written "
         "with UK rules in mind. We write it for you in English, you approve every word, and your free demo is "
         "ready within 24 hours.",
    pills=['Gas Safe details shown as you hold them', 'Call and WhatsApp in one tap', 'Free demo in 24 hours'],
    brief="WebAutonomos designs websites for plumbers, heating engineers and gas engineers in the UK. We write the "
          "copy in English from your real details, show your Gas Safe registration and other schemes as you hold "
          "them, and include the information UK law expects on a business website. " + PRIX_BRIEF,
    legal_t='What UK rules mean for a plumbing and heating website',
    legal_intro="Gas work is one of the few trades where the law says who may do the job, and your website is where "
                "customers check. These are the rules that matter for plumbers and heating engineers.",
    legal_rows=[
        ('Gas Safe registration', 'Gas Safety (Installation and Use) Regulations 1998, reg. 3',
         "Any business doing gas work for payment must be on the Gas Safe Register, and falsely pretending to be "
         "registered is an offence. Northern Ireland has the same rule under its 2004 regulations."),
        ('The Gas Safe logo', 'Gas Safe Register brand enforcement policy; DMCC Act 2024, Sch. 20, para. 3',
         "Only registered businesses may display the Gas Safe logo or a registration number, and only with their "
         "registered trading name. Showing a quality mark you're not entitled to is also banned outright."),
        ('Boiler replacements', 'Building Regulations 2010, Sch. 3 and Sch. 4',
         "Replacing a gas boiler is notifiable building work. A Gas Safe registered installer can self-certify "
         "it, and the homeowner receives a Building Regulations compliance certificate."),
        ('Unvented hot water cylinders', 'Building Regulations 2010, reg. 12 and Sch. 4, para. 1(l); Approved '
                                         'Document G, paras 3.40 to 3.42',
         "Fitting an unvented cylinder of more than 15 litres is notifiable work. Approved Document G says it "
         "should be done by someone competent, for example a scheme member or a holder of a current unvented "
         "skills card."),
        ('Heat pumps', 'Boiler Upgrade Scheme (England and Wales) Regulations 2022, as amended in 2026',
         "The Boiler Upgrade Scheme gives £7,500 towards an air source or ground source heat pump and £2,500 "
         "towards an air-to-air heat pump, in England and Wales. Only an MCS-certified installer can apply for "
         "the customer."),
        ('F-gas', 'Regulation (EU) 517/2014 as it applies in Great Britain, art. 11; Fluorinated Greenhouse Gases '
                  'Regulations 2015',
         "Installing a split system that contains F-gas refrigerant needs an engineer with an F-gas certificate "
         "working for a certified company, and split units can only be sold to householders with proof of "
         "certified installation."),
        ROW_UK_CONTRATS,
        ROW_UK_AVIS,
        ROW_UK_DETAILS,
        ROW_COOKIES,
    ],
    legal_note="Building control and water rules differ in Wales, Scotland and Northern Ireland, and the Boiler "
               "Upgrade Scheme only covers England and Wales. This is general information as of September 2026, not legal "
               "advice.",
    spain_note='<strong>Working in Spain?</strong> Spanish rules are different. See '
               '<a href="https://webautonomos.es/en/website-for-plumbers-in-spain">websites for plumbers and '
               'heating engineers in Spain</a>.',
    legal_we=["Your Gas Safe registration number and trading name, only if you're registered, with a link to the "
              "public register",
              "Your other schemes (MCS, WaterSafe, competent person schemes) shown as you hold them",
              "Emergency call-out details and a call button that stay in view on mobile",
              "A privacy policy and cookie notice adapted to UK law (UK GDPR and PECR)",
              "A .co.uk or .uk domain in your name, hosting, an SSL certificate and daily backups"],
    why_t='Built for plumbing and heating businesses',
    why=[('🔥', 'Gas Safe details in place', 'Your registration number and trading name, where customers look for '
                                            'them and can check them.')] + WHY_TRADES,
    sectors=['🔧 Plumbers', '🔥 Gas engineers', '♨️ Heating engineers', '🌡️ Heat pump installers',
             '🚿 Bathroom fitters', '🚰 Emergency plumbers', '🛠️ Boiler servicing', '💧 Drainage'],
    steps=STEPS_TRADES,
    extra=[
        ('website-content', 'Content', 'What a plumber website design should show',
         '<p class="legal-intro">A good plumber website design answers a worried visitor quickly: can you fix '
         'their problem, do you cover their area, are you Gas Safe registered, and how do they reach you now? '
         'Websites for plumbers perform best when those answers sit near the top.</p>'
         '<div class="why-g">'
         '<div class="aud-c"><div class="aud-i" aria-hidden="true">🚨</div>'
         '<h3>Emergency call-outs first</h3>'
         '<p>Your hours, the towns you cover and a call button at the top of the page, for the customer with a '
         'leak who won\'t read further.</p></div>'
         '<div class="aud-c"><div class="aud-i" aria-hidden="true">🔥</div>'
         '<h3>Your Gas Safe details</h3>'
         '<p>Your registration number, shown with your registered trading name, so a customer can check it on the '
         'public register before they hire you.</p></div>'
         '<div class="aud-c"><div class="aud-i" aria-hidden="true">🗂️</div>'
         '<h3>One section per service</h3>'
         '<p>Boiler installation and servicing, bathrooms, drain unblocking, heat pumps and landlord gas safety '
         'checks each get their own section in your plumbing website design.</p></div>'
         '<div class="aud-c"><div class="aud-i" aria-hidden="true">🏠</div>'
         '<h3>Landlords as regular customers</h3>'
         '<p>Landlords must have gas appliances and flues checked at least every 12 months (Gas Safety '
         'Regulations, reg. 36): a page for them brings in repeat business.</p></div>'
         '</div>'
         '<p class="where">Working as a gas engineer? The same gas engineer website design applies: registration '
         'first, then services. For more on what to include, see our <a href="https://webautonomos.es/blog/en/'
         'website-for-plumbers-complete-guide">guide to getting more calls from your website</a>.</p>'),
        ('good-design', 'Design', 'What good web design looks like for a plumbing business',
         '<p class="legal-intro">Good web design for a plumbing business isn\'t only about how the page looks: '
         'it is about whether a visitor finds what they need fast enough to call, especially with a leak or a '
         'boiler that won\'t start.</p>'
         '<div class="why-g">'
         '<div class="aud-c"><div class="aud-i" aria-hidden="true">🎨</div>'
         '<h3>A clear, mobile-first layout</h3>'
         '<p>Someone searching in a hurry won\'t wait for a slow page or zoom in to read it, so a professional '
         'layout keeps things simple, the copy short and the page fast to load, just as readable on a small screen '
         'as on a desktop.</p></div>'
         '<div class="aud-c"><div class="aud-i" aria-hidden="true">🧭</div>'
         '<h3>An easy path to a call or a quote</h3>'
         '<p>Every page leads somewhere: a clear call button, WhatsApp link or contact form, so someone who wants '
         'to book doesn\'t have to search for how.</p></div>'
         '<div class="aud-c"><div class="aud-i" aria-hidden="true">🤝</div>'
         '<h3>Layout that earns trust</h3>'
         '<p>Genuine feedback shown without hiding anything negative (see the rules above), your Gas Safe '
         'registration and straightforward pricing do more for trust than decoration.</p></div>'
         '<div class="aud-c"><div class="aud-i" aria-hidden="true">🏷️</div>'
         '<h3>Branding that matches the rest of your business</h3>'
         '<p>Your logo, colours and photos of your own jobs, carried through consistently, so your site matches '
         'your van, your invoices and your social media.</p></div>'
         '</div>'),
        ('website-mistakes', 'What to avoid', 'Common mistakes on plumbing websites',
         '<p class="legal-intro">Some gaps show up again and again on plumbing websites, and each one can send a '
         'visitor off to call someone else.</p>'
         '<div class="cmp-c them" style="max-width:640px;margin:0 auto;"><ul>'
         '<li>A layout that is hard to read on mobile, so a visitor searching from their phone with a leak gives '
         'up before they find how to contact you</li>'
         '<li>No visible Gas Safe registration, so a visitor cannot check you on the public register before '
         'agreeing to gas work</li>'
         '<li>Stock photography and generic copy that could describe any plumbing business, not yours</li>'
         '<li>A call button or way to get a quote that is buried below several screens of content</li>'
         '<li>A slow site that takes too long to load, especially on a mobile connection</li>'
         '</ul></div>'
         '<div class="aud-c" style="max-width:640px;margin:24px auto 0;"><h3>What to do instead</h3>'
         '<p>A simple, professional, mobile-friendly layout, photos of your own jobs and the Gas Safe registration '
         'a visitor can check. Together, they help someone who is just browsing trust what they see and get in '
         'touch.</p></div>'),
        ('vs-general-website', 'Compare', 'Built around your business, not a generic template',
         '<p class="legal-intro">A general website builder gives you a template to adapt, even one aimed at '
         'your industry, but your Gas Safe registration and your own services are still yours to add. Here is '
         'what changes when the design starts from your registration and services, not a generic template.</p>'
         '<div class="cmp-g">'
         '<div class="cmp-c them"><h3>A general website builder</h3><ul>'
         '<li>A generic template you adapt yourself, with no reference to your Gas Safe registration or the jobs '
         'you take on</li>'
         '<li>You write and structure the content yourself, including your services, the areas you cover and how '
         'to contact you</li>'
         '<li>Search engine optimisation (SEO) settings, such as page titles and descriptions, left for you to '
         'fill in yourself</li>'
         '<li>Support often means searching a knowledge base rather than a person who replies the same day</li>'
         '</ul></div>'
         '<div class="cmp-c us"><h3>What WebAutonomos builds for a plumbing business</h3><ul>'
         '<li>Content and layout designed to earn trust from the first visit, based on your services, your Gas '
         'Safe registration and how a visitor can contact you</li>'
         '<li>Your services, registrations and legal pages written for you in English, for you to check before '
         'anything goes live</li>'
         '<li>Basic SEO and hosting included at no extra charge, with a professional layout made for mobile</li>'
         '<li>A direct reply the same day, by email or WhatsApp, whenever you need support</li>'
         '</ul></div>'
         '</div>'
         '<p class="cmp-more"><a href="https://webautonomos.es/en/services">See everything included in your '
         'website →</a></p>'
         '<p class="legal-intro">Need a wider trades website, or cover more than one trade? See '
         '<a href="https://webautonomos.es/en/web-design-for-tradesmen">web design for tradesmen</a> or '
         '<a href="https://webautonomos.es/en/web-design-for-electricians">web design for electricians</a>.</p>'),
        ('landlords', 'Landlords', 'Serving landlords and letting agents',
         '<p class="legal-intro">Landlords and letting agents are a source of ongoing jobs for many plumbing and '
         'heating companies, and a dedicated page makes it easy for them to see you\'re set up for it.</p>'
         '<div class="why-g">'
         '<div class="aud-c"><div class="aud-i" aria-hidden="true">📅</div>'
         '<h3>Annual gas safety checks, made clear</h3>'
         '<p>Landlords must have every gas appliance and flue they provide checked at least every 12 months (Gas '
         'Safety Regulations, reg. 36). A short, clear page explaining what the check covers and how to arrange '
         'one answers their questions before they call.</p></div>'
         '<div class="aud-c"><div class="aud-i" aria-hidden="true">🏘️</div>'
         '<h3>Several properties, one call</h3>'
         '<p>A landlord or letting agent managing several properties in the same local area often prefers one '
         'company they can call for every gas safety check, rather than searching again each time.</p></div>'
         '<div class="aud-c"><div class="aud-i" aria-hidden="true">📄</div>'
         '<h3>The gas safety record, sorted</h3>'
         '<p>Landlords have to give their tenants the gas safety record after each check. Saying on your page how '
         'you send it to them is one less thing for them to chase.</p></div>'
         '</div>'),
        local_search_uk('plumber'),
        ('local-trust-plumbers', 'Local & trust', 'Local search and trust for small plumbing companies',
         '<p class="legal-intro">Many customers find a local plumber through a search, and what they see once they '
         'land decides whether they call. A small plumbing company doesn\'t need a marketing team for that: a few '
         'concrete details do the work.</p>'
         '<div class="why-g">'
         '<div class="aud-c"><div class="aud-i" aria-hidden="true">📍</div><h3>Jobs you\'ve done nearby</h3>'
         '<p>A few photos of your own jobs, each with the town where you did it, show a visitor that you already '
         'work in their area.</p></div>'
         '<div class="aud-c"><div class="aud-i" aria-hidden="true">⭐</div><h3>Reviews a visitor can check</h3>'
         '<p>A link to your Google reviews lets a visitor read them in full, where they were posted, rather than '
         'taking a few quotes on trust.</p></div>'
         '<div class="aud-c"><div class="aud-i" aria-hidden="true">🤝</div><h3>Who will knock on the door</h3>'
         '<p>Your name, a photo of you or your van and how you prefer to be contacted: someone deciding who to let '
         'into their home wants to know who is coming.</p></div>'
         '</div>'
         '<p class="where">More on ranking locally in <a href="https://webautonomos.es/blog/en/'
         'how-to-rank-your-website-in-local-google">how to rank your website locally on Google</a>.</p>'),
        ('website-speed-plumbers', 'Performance', 'Website speed and Core Web Vitals for a plumbing website',
         '<p class="legal-intro">A visitor calling about a leak won\'t wait for a slow page, and Google measures '
         'loading speed too: Core Web Vitals, including Largest Contentful Paint, are part of the page experience '
         'signals it looks at alongside the content itself.</p>'
         '<div class="why-g">'
         '<div class="aud-c"><div class="aud-i" aria-hidden="true">⚡</div><h3>Largest Contentful Paint</h3>'
         '<p>It measures how long the largest element on screen, often your main photo or heading, takes to appear. '
         'A light, well-compressed main photo helps it appear sooner, on a phone as much as on a desktop.</p></div>'
         '<div class="aud-c"><div class="aud-i" aria-hidden="true">🔎</div><h3>Test it yourself</h3>'
         '<p>Google\'s free PageSpeed Insights tool shows how quickly your homepage loads on a phone and on a '
         'desktop, and which images or scripts slow it down. Try it before you choose what to change.</p></div>'
         '<div class="aud-c"><div class="aud-i" aria-hidden="true">🛠️</div><h3>Included, not managed by you</h3>'
         '<p>Hosting, an SSL certificate, daily backups, 24/7 monitoring and technical maintenance are part of both '
         'plans, so the technical side of your website isn\'t something you have to manage yourself.</p></div>'
         '</div>'
         '<p class="where">More detail in <a href="https://webautonomos.es/blog/en/website-speed-and-search-'
         'rankings">why your website\'s speed affects your Google ranking</a>.</p>'),
        ('plumbing-website-cost', 'Pricing', 'What does a plumbing website cost?',
         '<p class="legal-intro">A plumbing website\'s cost depends on what\'s bundled in, not only on the design '
         'itself: hosting, legal pages, ongoing changes and support are billed separately with some providers.</p>'
         '<div class="why-g">'
         '<div class="aud-c"><div class="aud-i" aria-hidden="true">📄</div><h3>What\'s included in one price</h3>'
         '<ul style="list-style:none;padding:0;display:grid;gap:6px;text-align:left;font-size:.92rem;color:#334155">'
         '<li>Design, copy and your Gas Safe details written for you</li>'
         '<li>Hosting, an SSL certificate and legal pages</li>'
         '<li>One change a month, with no lock-in</li>'
         '</ul>'
         '<p style="margin-top:10px">With WebAutonomos, all of it sits under one price: €15 a month (about £%d) '
         'with no setup fee, or €349 (about £%d) once, no VAT added. Pound amounts depend on the exchange '
         'rate.</p></div>'
         '<div class="aud-c"><div class="aud-i" aria-hidden="true">🔧</div><h3>Bigger changes, quoted separately</h3>'
         '<p>A full redesign or a large new section is quoted once you know what you need, rather than folded into '
         'a monthly price that would have to cover every possibility.</p></div>'
         '<div class="aud-c"><div class="aud-i" aria-hidden="true">📊</div><h3>Comparing quotes from other providers</h3>'
         '<p>What a website costs varies widely by provider. Three things usually explain the difference:</p>'
         '<ul style="list-style:none;padding:0;display:grid;gap:6px;text-align:left;font-size:.92rem;color:#334155">'
         '<li>How much of the design and copy you write yourself</li>'
         '<li>Whether you pay a one-off fee, a monthly fee, or both</li>'
         '<li>How the site is built, and how easy it is to update afterwards</li>'
         '</ul></div>'
         '</div>' % (GBP_MOIS, GBP_UNIQUE)),
    ],
    faq=[("Do I need to be Gas Safe registered?",
          "Yes, for any business doing gas work for payment: the Gas Safety (Installation and Use) Regulations 1998 (reg. 3) "
          "require it, and falsely pretending to be registered is a separate offence. Gas Safe Register replaced "
          "CORGI in 2009 in Great Britain and in 2010 in Northern Ireland, so avoid “CORGI registered” on your "
          "website."),
         ("Can I show the Gas Safe logo on my website?",
          "Only if your business is registered, and only with your registered trading name, under Gas Safe "
          "Register's brand rules. Customers can check your number on the Gas Safe website or by phone, and can "
          "ask to see your engineer's ID card, which lists the types of gas work they are qualified for."),
         ("Do homeowners have to service their boiler every year?",
          "No law requires owner-occupiers to service their own boiler, but the HSE strongly advises having gas "
          "appliances serviced at least once a year. Landlords are different: they must have every gas appliance "
          "and flue they provide checked at least every 12 months and give tenants the gas safety record."),
         ("What grants are there for heat pumps?",
          "In England and Wales, the Boiler Upgrade Scheme gives £7,500 towards an air source or ground source heat "
          "pump and £2,500 towards an air-to-air heat pump, with £9,000 for an air or ground source heat pump in "
          "homes heated by oil or LPG with no mains gas, until March 2027. Only an MCS-certified installer can apply for the customer, and installing heat pumps in "
          "homes is zero-rated for VAT until 31 March 2027."),
         ("Do I need an F-gas certificate to fit heat pumps?",
          "For split systems that contain F-gas refrigerant, yes: the engineer needs a personal F-gas certificate "
          "and must work for an F-gas certified company. Split units can only be sold to householders with proof "
          "that a certified company will install them."),
         ("Who can fit an unvented hot water cylinder?",
          "Someone competent: Approved Document G gives as examples a member of a competent person scheme, who can "
          "self-certify the work, or a holder of a current skills card for unvented hot water systems. Fitting a cylinder of more than 15 litres is "
          "notifiable building work, so without a scheme member, building control must be told before work "
          "starts."),
         ("Do I need to join WaterSafe or another approved contractor scheme?",
          "It isn't compulsory. In England and Wales, members of approved contractor schemes can skip advance "
          "notice to the water company for some jobs, certify their work, and their certificate gives the "
          "customer a legal defence under the Water Supply (Water Fittings) Regulations 1999."),
         FAQ_UK_CANCEL,
         FAQ_UK_AVIS,
         ("Does website design really affect my results?",
          "Yes: a confusing first experience makes visitors leave before they see what you offer, however good the "
          "job itself is. A simple design, straightforward pricing information and an easy way to get a quote or "
          "make a call give them what they need to decide to contact you."),
         ("Can a plumbing website support marketing?",
          "Yes: both plans include basic SEO, with page titles and copy built around your services and the areas "
          "you cover. If you want to go further, we also offer local SEO and managing your Google Business "
          "Profile: ask us and we'll explain what it covers."),
         ("Do you offer digital marketing beyond the website itself?",
          "Yes, if you ask: alongside your website, we can assist with paid advertising, such as Google Ads or "
          "Facebook ads, and with managing your social media. Ask us and we'll explain what's involved."),
         ("What makes a good plumbing website, beyond how it looks?",
          "A good website answers the questions someone has before they call: your services, your Gas Safe "
          "registration and how to reach you. We write and structure all of this for you, so you don't have to "
          "build or write any of it yourself."),
         ("Does website speed affect a plumbing website's Google ranking?",
          "Yes: Core Web Vitals, including Largest Contentful Paint, are part of Google's page experience signals, "
          "and a slow page also loses visitors before they call. Hosting, an SSL certificate, 24/7 monitoring and "
          "technical maintenance are included in both plans, so you don't have to manage the technical side "
          "yourself."),
         ("What should a service area page cover?",
          "The towns and postcodes you actually cover, so a visitor and Google both know if you're near them. If "
          "you regularly cover several areas, a short list on your main services page usually does the job, "
          "without needing a separate page for every town."),
         ("Do I need a privacy policy on my plumbing website?",
          "Yes: UK GDPR requires a privacy policy explaining what you do with visitors' data, and the Privacy and "
          "Electronic Communications Regulations (PECR) cover cookies. Both plans include a privacy policy and "
          "cookie notice adapted to UK law, ready before your site goes live.")] + FAQ_TRADES,
)
SRC_PLUMB_UK = [
    ('Gas Safety (Installation and Use) Regulations 1998, reg. 3',
     'https://www.legislation.gov.uk/uksi/1998/2451/regulation/3'),
    ('HSE, domestic gas safety FAQs', 'https://www.hse.gov.uk/gas/domestic/faqs.htm'),
    ('Approved Document G', 'https://assets.publishing.service.gov.uk/media/66f6c6ce3b919067bb4828cc/ADG_with_2024_amendments.pdf'),
    ('Boiler Upgrade Scheme', 'https://www.gov.uk/apply-boiler-upgrade-scheme/what-you-can-get'),
    ('F-gas qualifications', 'https://www.gov.uk/guidance/qualifications-required-to-work-on-equipment-containing-f-gas'),
    ('Water Fittings Regulations 1999, reg. 7', 'https://www.legislation.gov.uk/uksi/1999/1148/regulation/7'),
    ('Consumer Contracts Regulations 2013, reg. 28', 'https://www.legislation.gov.uk/uksi/2013/3134/regulation/28'),
    ('DMCC Act 2024, Sch. 20', 'https://www.legislation.gov.uk/ukpga/2024/13/schedule/20'),
    ('E-Commerce Regulations 2002, reg. 6', 'https://www.legislation.gov.uk/uksi/2002/2013/regulation/6'),
]

ELEC_UK = dict(
    COMMUN_TRADES,
    title="Web design for electricians in the UK: €15/month",
    description="Web design for electricians in the UK: scheme registration, services and legal pages, built around "
                "Part P and UK consumer rules. Free demo in 24h, €15/month.",
    service_name="Web design for electricians in the UK",
    audience="Electricians and electrical contractors in the United Kingdom",
    crumb='Web design for electricians',
    badge='For electricians in the UK',
    h1="Web design for <em>electricians</em> in the UK",
    lede="Your services, your scheme registration, the areas you cover and a call or WhatsApp in one tap, written "
         "with Part P and UK consumer rules in mind. We write it for you in English, you approve every word, and "
         "your free demo is ready within 24 hours.",
    pills=['Scheme registration shown as you hold it', 'Built around Part P', 'Free demo in 24 hours'],
    brief="WebAutonomos designs websites for electricians and electrical contractors in the UK. We write the copy "
          "in English from your real details, show your competent person scheme registration as you hold it, and "
          "include the information UK law expects on a business website. " + PRIX_BRIEF,
    legal_t='What UK rules mean for an electrician website',
    legal_intro="Anyone can call themselves an electrician in the UK, so what customers look for is your scheme "
                "registration. These are the rules that matter for your website.",
    legal_rows=[
        ('Notifiable work (England)', 'Building Regulations 2010, reg. 12(6A)',
         "A new circuit, replacing a consumer unit, or any addition or alteration to circuits in a special location, "
         "such as the space around a bath or shower, needs building control approval, unless a registered competent "
         "person self-certifies it."),
        ('Competent person schemes', 'Building Regulations 2010, Sch. 3',
         "For electrical work in homes, the authorised schemes are NICEIC (run by Certsure), NAPIT, Blue Flame "
         "and OFTEC. ELECSA and Stroma no longer run schemes for this work."),
        ('Electrical work in Wales', 'Building Regulations 2010, Sch. 4 (Wales)',
         "The rule is wider: electrical work in a home is notifiable unless it's on a short exempt list, so adding "
         "to circuits in a kitchen or outdoors, or work on a generator such as solar panels, is notifiable."),
        ('BS 7671', 'Electricity at Work Regulations 1989; HSE, HSR25, para. 9',
         "BS 7671 isn't law in itself, but the HSE says following it is likely to achieve compliance with the "
         "Electricity at Work Regulations. Amendment 4 was published in April 2026."),
        ('Rented homes (England)', 'Electrical Safety Standards in the Private Rented Sector and Social Rented '
                                   'Sector (England) Regulations 2020',
         "Landlords, social landlords included, must have the electrics inspected and tested by a qualified person "
         "at least every 5 years. Wales and Scotland have their own 5-year rules."),
        ('EV chargers', 'Electric Vehicles (Smart Charge Points) Regulations 2021; OZEV grant guidance',
         "Home chargers sold in Great Britain must be smart chargers. OZEV grants of up to £500, for flat owners and "
         "renters with off-street parking or for homes with on-street parking, run until 31 March 2027, through an "
         "OZEV-authorised installer."),
        ROW_UK_CONTRATS,
        ROW_UK_AVIS,
        ROW_UK_DETAILS,
        ROW_COOKIES,
    ],
    legal_note="Scotland uses building warrants and approved certifiers of construction, and Northern Ireland's "
               "building regulations have no domestic electrical safety part. This is general information as of "
               "September 2026, not legal advice.",
    spain_note='<strong>Working in Spain?</strong> Spanish rules are different. See '
               '<a href="https://webautonomos.es/en/website-for-electricians-in-spain">websites for electricians '
               'in Spain</a>.',
    legal_we=["Your competent person scheme and registration number, only if you're registered, so customers can "
              "check them",
              "Your services grouped by type of job, from consumer units to EV chargers",
              "A page for landlords, if you carry out electrical inspections for rented homes",
              "A privacy policy and cookie notice adapted to UK law (UK GDPR and PECR)",
              "A .co.uk or .uk domain in your name, hosting, an SSL certificate and daily backups"],
    why_t='Built for electricians',
    why=[('⚡', 'Your registration in place', 'Your scheme and number, where customers look for them and can check '
                                            'them.')] + WHY_TRADES,
    sectors=['⚡ Domestic electricians', '🏢 Electrical contractors', '🔌 Rewires and consumer units',
             '🚗 EV charger installers', '☀️ Solar PV installers', '📋 Landlord inspections', '💡 Lighting',
             '📶 Smart home and data'],
    steps=STEPS_TRADES,
    extra=[
        ('website-content', 'Content', 'What an electrician website design should show',
         '<p class="legal-intro">A customer looking for an electrician website wants to see what you do, whether '
         'you cover their area, and whether you can sign off the work. Good electrician website design puts those '
         'first.</p>'
         '<div class="why-g">'
         '<div class="aud-c"><div class="aud-i" aria-hidden="true">✅</div>'
         '<h3>Your scheme registration</h3>'
         '<p>NICEIC, NAPIT or another authorised scheme, with your registration number, so a customer can check it '
         'on the Competent Persons Register before booking notifiable work.</p></div>'
         '<div class="aud-c"><div class="aud-i" aria-hidden="true">🗂️</div>'
         '<h3>One section per type of job</h3>'
         '<p>Fault finding, rewires, consumer units, EV chargers and solar each get their own section, so a '
         'visitor finds their job without scrolling past the rest.</p></div>'
         '<div class="aud-c"><div class="aud-i" aria-hidden="true">🏠</div>'
         '<h3>A page for landlords</h3>'
         '<p>Landlords need their electrics inspected at least every 5 years, and since 2025–26 that includes social '
         'housing: a page for them brings in recurring work.</p></div>'
         '<div class="aud-c"><div class="aud-i" aria-hidden="true">📸</div>'
         '<h3>Photos of your own work</h3>'
         '<p>Neat consumer units and finished installations, from your own photos, with a one-line caption for '
         'each job.</p></div>'
         '</div>'),
        ('good-design', 'Design', 'What a good electrician website looks like',
         '<p class="legal-intro">A good electrician website is about more than how it looks: it is about '
         'whether a visitor finds what they need and gets in touch.</p>'
         '<div class="why-g">'
         '<div class="aud-c"><div class="aud-i" aria-hidden="true">🎨</div>'
         '<h3>A clear, mobile-first layout</h3>'
         '<p>Many people search for an electrician on their phone, so professional web design keeps the layout '
         'simple, the copy short and the site fast to load: it reads just as well on a small screen as on a '
         'desktop.</p></div>'
         '<div class="aud-c"><div class="aud-i" aria-hidden="true">🧭</div>'
         '<h3>An easy path to a quote</h3>'
         '<p>Every page on your site leads somewhere: a clear way to get a quote, call you or contact you on '
         'WhatsApp, so a visitor who is ready to book does not have to search for how.</p></div>'
         '<div class="aud-c"><div class="aud-i" aria-hidden="true">🤝</div>'
         '<h3>Design that earns trust</h3>'
         '<p>Genuine Google reviews, shown without hiding the negative ones (see the rules above), your scheme '
         'registration and straightforward pricing do more for trust than decoration.</p></div>'
         '<div class="aud-c"><div class="aud-i" aria-hidden="true">🏷️</div>'
         '<h3>Branding that matches the rest of your business</h3>'
         '<p>Your logo, colours and photos of your best finished jobs, carried through consistently, so your '
         'website matches your van, your invoices and your social media.</p></div>'
         '</div>'),
        ('website-mistakes', 'What to avoid', 'Common mistakes on electrician websites',
         '<p class="legal-intro">Some gaps show up again and again on electrician websites, and each one can '
         'send a visitor off to call someone else.</p>'
         '<div class="cmp-c them" style="max-width:640px;margin:0 auto;"><ul>'
         '<li>A layout that is hard to read on mobile, so a visitor searching from their phone gives up before '
         'they find how to contact you</li>'
         '<li>No visible scheme registration, so a visitor cannot check you on the Competent Persons Register '
         'before booking</li>'
         '<li>Stock photography and generic copy that could describe any electrician\'s website, not yours</li>'
         '<li>A way to get a quote that is buried below several screens of content</li>'
         '<li>A slow site that takes too long to load, especially on a mobile connection</li>'
         '</ul></div>'
         '<div class="aud-c" style="max-width:640px;margin:24px auto 0;"><h3>What to do instead</h3>'
         '<p>A simple, professional, mobile-friendly layout, photos of your own jobs and the scheme registration '
         'details a visitor can check. Together, they help someone who is just browsing trust what they see and '
         'get a quote.</p></div>'),
        ('vs-general-website', 'Compare', 'How electrician website design differs from a general website builder',
         '<p class="legal-intro">A general website builder gives you a template to adapt, even one labelled for '
         'electricians, but your scheme registration and your own services are still yours to add. Here is what '
         'changes when your website design starts from your registrations and services, not a generic '
         'template.</p>'
         '<div class="cmp-g">'
         '<div class="cmp-c them"><h3>A general website builder</h3><ul>'
         '<li>A generic template you adapt yourself, with no reference to your scheme registration or the jobs '
         'you take on</li>'
         '<li>You write and structure the content yourself, including your services, the areas you cover and how '
         'to contact you</li>'
         '<li>Basic search engine optimisation (SEO) settings, such as page titles and descriptions, left for you '
         'to fill in yourself</li>'
         '<li>Support often means searching a knowledge base rather than a person who replies the same day</li>'
         '</ul></div>'
         '<div class="cmp-c us"><h3>Electrician website design from WebAutonomos</h3><ul>'
         '<li>Content and layout designed to earn trust from the first visit, based on your services, your '
         'scheme registration and how a visitor can contact you</li>'
         '<li>Your services, registrations and legal pages written for you in English, for you to check before '
         'anything goes live</li>'
         '<li>Basic SEO and hosting included at no extra charge, with a professional design made for mobile</li>'
         '<li>A direct reply the same day, by email or WhatsApp, whenever you need support</li>'
         '</ul></div>'
         '</div>'
         '<p class="cmp-more"><a href="https://webautonomos.es/en/services">See everything included in your '
         'website →</a></p>'),
        local_search_uk('electrician'),
    ],
    faq=[("Do electricians need a licence in the UK?",
          "There's no legal licence or protected title for electricians, but the law still requires competence "
          "for electrical work (Electricity at Work Regulations 1989, reg. 16). In England and Wales, registration "
          "with a competent person scheme lets you self-certify notifiable work in homes instead of going through "
          "building control, and it is what customers can check."),
         ("What electrical work is notifiable in England?",
          "Under the Building Regulations 2010 (reg. 12(6A)): installing a new circuit, replacing a consumer unit, "
          "and any addition or alteration to existing circuits in a special location, such as the space around a "
          "bath or shower, or a room with a swimming pool or sauna heater. Wales has a wider rule, with only a short list of exempt work."),
         ("Which schemes can I join to self-certify?",
          "For electrical work in homes, the competent person schemes listed in the Building Regulations are "
          "NICEIC (run by Certsure), NAPIT, Blue Flame and OFTEC. ELECSA and Stroma no longer run schemes for this work, "
          "so an old logo from either should come off your website."),
         ("Is BS 7671 a legal requirement?",
          "Not in itself: it's a non-statutory standard, but the HSE says following it is likely to achieve "
          "compliance with the relevant parts of the Electricity at Work Regulations 1989, and the rented-home "
          "rules refer to it directly. The current version is BS 7671:2018 with Amendment 4, published in April "
          "2026; Amendment 3 remains usable until about mid-October 2026."),
         ("How often do landlords need an electrical inspection?",
          "In England, at least every 5 years, carried out by a qualified and competent person, and since "
          "2025–26 the rule covers social housing too. Wales requires an electrical condition report at least "
          "every 5 years, and Scotland an inspection before the tenancy starts and at most 5 years apart."),
         ("Can I fit EV chargers for the OZEV grant?",
          "Only as an OZEV-authorised installer. There are two grants of up to £500: one for flat owners and "
          "renters with private off-street parking, and one for homes with on-street parking, using a "
          "cross-pavement solution. This is their final year: they end on 31 March 2027. Home chargers sold in "
          "Great Britain must also meet the smart charge point regulations."),
         ("Do solar panels fall under Part P?",
          "Solar PV on a roof is electrical work covered by Part P. In England it is usually notifiable, as it "
          "normally needs a new circuit, and in Wales it always is; microgeneration installers can self-certify "
          "through their own schemes. Installing solar panels and batteries in homes is zero-rated "
          "for VAT until 31 March 2027."),
         FAQ_UK_CANCEL,
         FAQ_UK_AVIS,
         ("Does website design really affect my results?",
          "Yes: a confusing first experience makes visitors leave before they see what you offer, however good "
          "the job itself is. A simple design, straightforward pricing information and an easy way to get a "
          "quote give them what they need to decide to contact you."),
         ("Can an electrician website support marketing?",
          "Yes: both plans include basic SEO, with page titles and copy built around your services and the towns "
          "you cover. If you want to go further, we also offer local SEO and managing your Google Business "
          "Profile: ask us for prices when you get your demo."),
         ("Do you offer digital marketing beyond the website itself?",
          "Yes, if you ask: alongside your website, we can assist with paid advertising, such as Google Ads or "
          "Facebook ads, and with managing your social media. Ask us and we'll explain what's involved."),
         ("What makes a good electrician website, beyond how it looks?",
          "A good electrician website answers the questions a new customer has before they call: your services, "
          "your scheme registration and how to reach you. We write and structure all of this for you, so you "
          "don't have to build or write any of it yourself.")] + FAQ_TRADES,
)
SRC_ELEC_UK = [
    ('Building Regulations 2010, reg. 12', 'https://www.legislation.gov.uk/uksi/2010/2214/regulation/12'),
    ('Competent person schemes', 'https://www.gov.uk/guidance/competent-person-scheme-current-schemes-and-how-schemes-are-authorised'),
    ('HSE, HSR25', 'https://www.hse.gov.uk/pubns/priced/hsr25.pdf'),
    ('Electrical safety standards in rented homes',
     'https://www.gov.uk/government/publications/electrical-safety-standards-in-the-private-and-social-rented-sectors-guidance/electrical-safety-standards-in-the-private-and-social-rented-sectors-guidance'),
    ('EV chargepoint grants', 'https://www.gov.uk/guidance/electric-vehicle-chargepoint-grants'),
    ('Smart Charge Points Regulations 2021', 'https://www.legislation.gov.uk/uksi/2021/1467/regulation/4'),
    ('Consumer Contracts Regulations 2013, reg. 28', 'https://www.legislation.gov.uk/uksi/2013/3134/regulation/28'),
    ('DMCC Act 2024, Sch. 20', 'https://www.legislation.gov.uk/ukpga/2024/13/schedule/20'),
    ('E-Commerce Regulations 2002, reg. 6', 'https://www.legislation.gov.uk/uksi/2002/2013/regulation/6'),
]


PAGES = {
    'dental': dict(url='/en/dental-website-design', C=DENTAL, SOURCES=SRC_DENTAL,
                   llms='Dental website design for UK practices'),
    'physio': dict(url='/en/physiotherapy-website-design', C=PHYSIO, SOURCES=SRC_PHYSIO,
                   llms='Physiotherapy website design for UK clinics'),
    'tradesmen': dict(url='/en/web-design-for-tradesmen', C=TRADES, SOURCES=SRC_TRADES,
                      llms='Web design for tradesmen in the UK', avis='menuisiers'),
    'plumbers': dict(url='/en/web-design-for-plumbers', C=PLUMB_UK, SOURCES=SRC_PLUMB_UK,
                     llms='Web design for plumbers and heating engineers in the UK', avis='menuisiers'),
    'electricians': dict(url='/en/web-design-for-electricians', C=ELEC_UK, SOURCES=SRC_ELEC_UK,
                         llms='Web design for electricians in the UK', avis='menuisiers'),
}


# ═════════════════════════ GABARIT ═════════════════════════════════════════
def page(P):
    c, u, src, i = P['C'], H.URLS[LANG], H.source(LANG), H.IDS[LANG]
    x = X.C[LANG]
    L = lambda k: BASE + u[k]
    url = BASE + P['url']
    demo = L('demo') + '#pide-demo'
    home = L('home')
    langs = [('es', 'ES', BASE + '/'), ('fr', 'FR', BASE + '/fr/'), ('en', 'EN', url)]
    nav_links = ''.join('<a href="%s">%s</a>' % (L(k), E(t)) for k, t in H.C[LANG]['nav'])
    lang_links = ''.join('<a href="%s" hreflang="%s" lang="%s"%s>%s</a>' % (
        h, code, code, ' aria-current="page"' if code == LANG else '', lab) for code, lab, h in langs)
    pills = ''.join('<span class="pill">✓ %s</span>' % E(p) for p in c['pills'])
    rows = ''.join('<tr><th scope="row">%s</th><td class="law">%s</td><td>%s</td></tr>' % (E(a), E(b), E(d))
                   for a, b, d in c['legal_rows'])
    we = ''.join('<li><span>%s</span></li>' % E(t) for t in c['legal_we'])
    srcs = ' · '.join('<a href="%s" rel="noopener" target="_blank">%s</a>' % (h, E(t)) for t, h in P['SOURCES'])
    note_esp = '<p class="spain-note">%s</p>' % c['spain_note'] if c['spain_note'] else ''
    why = ''.join('<div class="aud-c"><div class="aud-i" aria-hidden="true">%s</div><h3>%s</h3><p>%s</p></div>'
                  % (ic, E(t), E(d)) for ic, t, d in c['why'])
    sectors = ''.join('<span class="stag">%s</span>' % E(s) for s in c['sectors'])
    steps = ''.join('<div class="step%s"><div class="sn">%d</div><div class="stit">%s</div><div class="sinf">%s</div></div>'
                    % (' ft' if n == 1 else '', n + 1, E(t), E(d)) for n, (t, d) in enumerate(c['steps']))
    plans = ''
    for p in PLANS:
        plans += ('<div class="pc%s">%s<div class="pc-n">%s</div><div class="pc-a">%s</div>'
                  '<div class="pc-p">%s</div><ul>%s</ul></div>') % (
            ' hl' if p['hl'] else '', '<span class="pc-b">%s</span>' % E(p['badge']) if p['badge'] else '',
            E(p['name']), E(p['amt']), E(p['per']), ''.join('<li>%s</li>' % E(t) for t in p['pts']))
    slides, dots = '', ''
    for n, (txt, who, tr) in enumerate(BM.trier_avis(LANG, BM.METIERS[P.get('avis', 'dentistes')]['avis_ordre'])):
        slides += ('<div class="tp-slide"><div class="tp-card"><div class="tp-stars" aria-hidden="true">★★★★★</div>'
                   '<blockquote>« %s »</blockquote><div class="tp-who">— %s%s</div></div></div>') % (
            E(txt), E(who), '<span class="tp-tr">%s</span>' % E(tr) if tr else '')
        dots += '<button class="tp-dot%s" onclick="tpGo(%d)" aria-label="%s %d"></button>' % (
            ' on' if n == 0 else '', n, E(x['rev_aria']), n + 1)
    faq = ''.join('<details><summary>%s</summary><p>%s</p></details>' % (E(q), E(a)) for q, a in c['faq'])
    # sections supplémentaires facultatives (contenu utile ajouté par le rédacteur du circuit SEO)
    extra_html = ''.join(
        '\n\n<section class="blk%s" id="%s">\n  %s<h2 style="margin-bottom:36px">%s</h2>\n  %s\n</section>'
        % (' alt' if idx % 2 == 0 else '', eid, '<p class="ey">%s</p>\n  ' % E(ey) if ey else '', h2, body)
        for idx, (eid, ey, h2, body) in enumerate(c.get('extra', [])))
    jc = dict(title=c['title'], description=c['description'], html_lang=c['html_lang'],
              service_name=c['service_name'], area=c['area'], plans=PLANS, unit=c['unit'], faq=c['faq'])
    g = json.loads(H.jsonld(LANG, jc, dict(home=P['url'])))
    for n in g['@graph']:
        if n.get('@type') == 'Service':
            n['audience'] = {"@type": "Audience", "audienceType": c['audience']}
            for o in n.get('offers', []):   # aucune TVA ajoutée pour les clients britanniques
                o.get('priceSpecification', {}).pop('valueAddedTaxIncluded', None)
        if n.get('@type') == 'ProfessionalService':
            n['areaServed'] = [{"@type": "Country", "name": H.COUNTRY[a]} for a in ('ES', 'FR', 'GB')]
    g['@graph'].append({"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": c['crumb_home'], "item": home},
        {"@type": "ListItem", "position": 2, "name": c['crumb'], "item": url}]})
    ld = json.dumps(g, ensure_ascii=False, indent=1)
    wa = re.sub(r'href="https://wa\.me/[^"]*"', 'href="https://wa.me/%s?text=%s"' % (
        H.WHATSAPP, re.sub(r'[^A-Za-z0-9]', lambda mm: ''.join('%%%02X' % b for b in mm.group(0).encode()),
                           H.C[LANG]['wa_text'])), src['float_wa'])
    legal_js = "event.preventDefault();document.getElementById('%s').style.display='flex'"
    foot_langs = '<a href="%s/" hreflang="es">ES</a>\n    <a href="%s/fr/" hreflang="fr">FR</a>' % (BASE, BASE)

    return H.alterner_fonds(f"""<!DOCTYPE html>
<html lang="{c['html_lang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<!-- Page générée par _tools/build_uk_pages.py : ne pas modifier à la main, relancer le script. -->
<title>{E(c['title'])}</title>
<meta name="description" content="{E(c['description'])}">
<meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large">
<link rel="canonical" href="{url}">
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
<style>{src['css']}{H.EXTRA_CSS}{X.CSS_PAGE}{BM.CSS_METIER}</style>
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
    <div class="lang" aria-label="{E(H.C[LANG]['lang_label'])}">{lang_links}</div>
    <a class="nav-cta" href="{demo}">{E(H.C[LANG]['nav_cta'])}</a>
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
      <a class="hero-2" href="#{c['legal_id']}">{E(c['cta2'])}</a>
    </div>
    <p class="rating"><span class="st" aria-hidden="true">★★★★★</span>{x['rating']}</p>
  </div>
</section>
<p class="crumbs"><a href="{home}">{E(c['crumb_home'])}</a> › {E(c['crumb'])}</p>

<section class="brief" id="{i['brief']}">
  <div class="brief-c">
    <h2>{E(c['brief_t'])}</h2>
    <p>{c['brief']}</p>
  </div>
</section>

<section class="blk" id="{c['legal_id']}">
  <p class="ey">{E(c['legal_ey'])}</p>
  <h2>{E(c['legal_t'])}</h2>
  <div class="legal-w">
    <p class="legal-intro">{E(c['legal_intro'])}</p>
    <div class="lt-wrap"><table class="lt">
      <thead><tr><th scope="col">{E(c['legal_cols'][0])}</th><th scope="col">{E(c['legal_cols'][1])}</th><th scope="col">{E(c['legal_cols'][2])}</th></tr></thead>
      <tbody>{rows}</tbody>
    </table></div>
    <p class="legal-note">{E(c['legal_note'])}</p>
    {note_esp}
    <div class="legal-we"><h3>{E(c['legal_we_t'])}</h3><ul>{we}</ul></div>
    <p class="srcs">{E(c['sources_t'])}: {srcs}</p>
  </div>
</section>

<section class="blk alt" id="{i['aud']}">
  <p class="ey">{E(c['why_ey'])}</p>
  <h2 style="margin-bottom:36px">{E(c['why_t'])}</h2>
  <div class="why-g">{why}</div>
  <p class="where"><strong>{E(c['where_t'])}</strong>{E(c['where'])}</p>
</section>

<section class="ss blk" id="{i['steps']}">
  <h2 style="margin-bottom:36px">{E(c['how_t'])}</h2>
  <div class="sw">{steps}</div>
</section>

<section class="blk alt" id="{i['price']}">
  <h2 style="margin-bottom:36px">{E(x['price_t'])}</h2>
  <div class="pc-g">{plans}</div>
  <p class="p-note">{E(c['price_note'])}</p>
</section>

<section class="secs" id="{i['sect']}">
  <h2 style="margin-bottom:24px">{E(c['sect_t'])}</h2>
  <div class="sg">{sectors}</div>
</section>

<section class="proof" id="{i['rev']}">
  <h2>{E(x['rev_t'])}</h2>
  <div class="tp">
    <div class="tp-head"><span class="tp-score">4.3</span><span class="tp-of">/ 5</span><span class="tp-count">{E(x['rev_count'])}</span></div>
    <div class="tp-view"><div class="tp-track" id="tpTrack">{slides}</div></div>
    <div class="tp-dots" id="tpDots">{dots}</div>
    <a class="tp-link" href="{H.TRUSTPILOT}" target="_blank" rel="noopener noreferrer">{E(x['rev_link'])} →</a>
  </div>
</section>
{extra_html}
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
    <a href="{BASE}/aviso-legal/" onclick="{legal_js % 'modal-aviso'}">{E(H.C[LANG]['foot_legal'])}</a>
    <a href="{BASE}/privacidad/" onclick="{legal_js % 'modal-privacidad'}">{E(H.C[LANG]['foot_privacy'])}</a>
    <a href="{L('blog')}">{E(H.C[LANG]['foot_blog'])}</a>
    {foot_langs}
  </div>
  <address class="fnap">
    <strong>WebAutonomos</strong>
    <span>Calle Pintor Josep Segrelles, 26</span>
    <span>46870 Ontinyent, Valencia, Spain</span>
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


# ═════════════════════════ ÉCRITURE ════════════════════════════════════════
def main():
    check = '--check' in sys.argv
    os.chdir(ROOT)
    ecrits = {}
    for k, P in PAGES.items():
        s = page(P)
        H.controles('uk/%s' % k, s)
        ecrits[P['url'].lstrip('/') + '.html'] = s
    # llms.txt : une ligne par page, après la page « dentists in Spain »
    llms = open('llms.txt', encoding='utf-8').read()
    neuf = llms
    ancre = '- [%s](%s%s)' % (BM.METIERS['dentistes']['llms']['en'][1], BASE, BM.METIERS['dentistes']['en'])
    for k, P in PAGES.items():
        ligne = '- [%s](%s%s)' % (P['llms'], BASE, P['url'])
        if ligne not in neuf:
            if neuf.count(ancre + '\n') != 1:
                abandon('llms.txt : ancre introuvable : %s' % ancre[:70])
            neuf = neuf.replace(ancre + '\n', ancre + '\n' + ligne + '\n')
        ancre = ligne

    if check:
        for rel, s in ecrits.items():
            print('  ✓ %s valide (%d octets) — non écrit' % (rel, len(s.encode())))
        if neuf != llms:
            print('  ✓ llms.txt à modifier — non écrit')
        return
    for rel, s in ecrits.items():
        s = poser_photo(rel, s)
        ancien = open(rel, encoding='utf-8').read() if os.path.exists(rel) else None
        if ancien != s:
            open(rel, 'w', encoding='utf-8').write(s)
            print('  ✓ %s écrit (%d octets)' % (rel, len(s.encode())))
    if neuf != llms:
        open('llms.txt', 'w', encoding='utf-8').write(neuf)
        print('  ✓ llms.txt modifié')
    r = subprocess.run([sys.executable, '_tools/generate_sitemap.py'], cwd=ROOT)
    if r.returncode:
        sys.exit('ÉCHEC de generate_sitemap.py : les pages sont écrites, relance-le à la main après correction.')


if __name__ == '__main__':
    main()
