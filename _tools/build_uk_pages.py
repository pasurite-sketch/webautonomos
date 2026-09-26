# -*- coding: utf-8 -*-
"""Pages pour les cabinets britanniques (26/09/2026).

Angelino accepte des clients au Royaume-Uni (décision du 26/09/2026). Deux pages
dédiées, distinctes des pages métier « in Spain » de build_metier_pages.py (qui
visent les anglophones installés en Espagne) :
    /en/dental-website-design          cabinets dentaires britanniques
    /en/physiotherapy-website-design   kinésithérapeutes britanniques
Requêtes visées (Semrush Royaume-Uni, 26/09/2026) : « dental website design »
720/mois KD 15 ; « physiotherapy website design » 110/mois KD 3.

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
    badge='For dental practices in the UK',
    h1="Dental website design for <em>UK dental practices</em>",
    lede="Your practice, your team, your fees and how to book, set out the way the GDC's guidance on advertising "
         "expects. We write it for you in English, you approve every word, and your free demo is ready within "
         "24 hours.",
    pills=['Written around GDC guidance', 'Fees and NHS or private status shown clearly', 'Free demo in 24 hours'],
    brief="WebAutonomos designs websites for dental practices in the UK. We write the copy in English from your "
          "real details, show what the GDC's guidance on advertising asks a practice website to display "
          "(qualifications, GDC numbers, complaints procedure, the date of the last update) and keep the site "
          "clear of what UK advertising rules ban: specialist titles you don't hold, claims you can't back up, "
          "and prescription-only medicines such as Botox. " + PRIX_BRIEF,
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
    why_t='Built for UK dental practices',
    why=[('📋', 'GDC details in place',
          'Qualifications, GDC numbers, complaints procedure and last-updated date, set out where patients and '
          'the GDC guidance expect them.')] + WHY_COMMUNS,
    sectors=['🦷 General dental practices', '🏥 Mixed NHS and private practices', '✨ Private practices',
             '😁 Orthodontic practices', '🧑‍⚕️ Group practices'],
    steps=[('Tell us about your practice', 'Your treatments, your team, your fees and opening hours: it takes '
                                           'two minutes.'),
           ('We build your demo', 'Within 24 hours, with your copy in English and your legal pages.'),
           STEPS_FIN],
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
          "(regulation 20A). The CQC doesn't rate primary care dental services, so most dental practices have "
          "no rating to display.")] + FAQ_COMMUNES,
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
          "professional, such as a doctor or nurse, may need to register.")] + FAQ_COMMUNES,
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

PAGES = {
    'dental': dict(url='/en/dental-website-design', C=DENTAL, SOURCES=SRC_DENTAL,
                   llms='Dental website design for UK practices'),
    'physio': dict(url='/en/physiotherapy-website-design', C=PHYSIO, SOURCES=SRC_PHYSIO,
                   llms='Physiotherapy website design for UK clinics'),
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
    for n, (txt, who, tr) in enumerate(BM.trier_avis(LANG, BM.METIERS['dentistes']['avis_ordre'])):
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

    return f"""<!DOCTYPE html>
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
"""


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
