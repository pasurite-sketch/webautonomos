# -*- coding: utf-8 -*-
"""Versions française et anglaise, à leur propre adresse, des pages
/diagnostico-automatizacion/ et /visibilidad-ia/ (plan SEO FR-EN, phase 1).

Pourquoi : ces deux pages affichaient le français et l'anglais via ?lang=fr et
?lang=en, sur la même adresse que l'espagnol, avec un canonical vers la version
espagnole. Pour Google, il n'existait donc ni diagnostic ni page « Visibilité
IA » en français ou en anglais.

Le script :
  1. génère, depuis la page espagnole (la seule qu'on modifie à la main) :
       /fr/diagnostic-automatisation/   /en/automation-diagnostic/
       /fr/visibilite-ia/               /en/ai-visibility/
     avec, pour chaque copie : lang, title, meta description, Open Graph,
     canonical vers elle-même, textes de la langue écrits dans le HTML
     (lisibles sans JavaScript), JSON-LD dans la langue (FAQ comprise), liens
     de navigation et messages WhatsApp dans la langue ;
  2. la première fois seulement, modifie les deux pages espagnoles :
     hreflang en/fr vers les nouvelles adresses ; ?lang=fr et ?lang=en y
     renvoient désormais (gclid et paramètres Ads conservés) ; le menu des
     langues y mène ; point documenté dans « MODIFICATIONS LOCALES » ;
  3. remplace dans tout le site les liens …?lang=fr / …?lang=en de ces deux
     pages par les nouvelles adresses (accueils /fr/ /en/, articles, pages,
     générateurs) ;
  4. apprend à generate_sitemap.py à lister fr/*/index.html et en/*/index.html.

Le valencien (?lang=ca) ne change pas.

À relancer après chaque modification des pages espagnoles :
    python3 _tools/build_i18n_pages.py            (puis generate_sitemap.py)
    python3 _tools/build_i18n_pages.py --check    (contrôle sans écrire)
Sauvegarde : ~/webautonomos-work/backups/i18n_pages_<date>/ avant écriture.

Retouches propres à une copie (23/10/2026) : RETOUCHES applique à T[lang]
des remplacements (clé, ancien, nouveau) avant d'écrire la copie, sans toucher
la page espagnole (version anglaise du diagnostic : SERPmantics Google et
ChatGPT). Le script s'arrête si un « ancien » n'est plus trouvé une fois.
"""
import datetime
import html
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'photos'))
from photos_lib import injecter as poser_photo  # photo prévue par _tools/photos/images.json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from origine_lead import poser as poser_origine  # script d'origine des leads (origine-lead.js), ne pas retirer
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from faq_statique import remplir_faq  # FAQ lisible sans JavaScript (04/10/2026)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = 'https://webautonomos.es'
LANGS = ('fr', 'en')

DIAG = {'es': '/diagnostico-automatizacion/', 'fr': '/fr/diagnostic-automatisation/',
        'en': '/en/automation-diagnostic/'}
VIS = {'es': '/visibilidad-ia/', 'fr': '/fr/visibilite-ia/', 'en': '/en/ai-visibility/'}

# Liens de navigation vers le reste du site (balises <a> seulement)
NAV = {
    'fr': [('https://webautonomos.es', BASE + '/fr/'),
           ('https://webautonomos.es/#que-incluye', BASE + '/fr/#inclus'),
           ('https://webautonomos.es/#precios', BASE + '/fr/tarifs'),
           ('https://webautonomos.es/#como-funciona', BASE + '/fr/#etapes'),
           ('https://webautonomos.es/#marketing', BASE + '/fr/#services'),
           ('https://webautonomos.es/#preguntas', BASE + '/fr/questions'),
           ('https://webautonomos.es/blog/', BASE + '/blog/#fr'),
           ('https://webautonomos.es/#contacto', BASE + '/demandez-votre-demo#pide-demo'),
           # pages legales de la langue (14/10/2026)
           ('https://webautonomos.es/aviso-legal/', BASE + '/fr/mentions-legales/'),
           ('https://webautonomos.es/privacidad/', BASE + '/fr/confidentialite/'),
           ('https://webautonomos.es/cookies/', BASE + '/fr/cookies/'),
           ('/aviso-legal/', '/fr/mentions-legales/'), ('/privacidad/', '/fr/confidentialite/'), ('/cookies/', '/fr/cookies/')],
    'en': [('https://webautonomos.es', BASE + '/en/'),
           ('https://webautonomos.es/#que-incluye', BASE + '/en/#included'),
           ('https://webautonomos.es/#precios', BASE + '/en/pricing'),
           ('https://webautonomos.es/#como-funciona', BASE + '/en/how'),
           ('https://webautonomos.es/#marketing', BASE + '/en/#services'),
           ('https://webautonomos.es/#preguntas', BASE + '/en/faq'),
           ('https://webautonomos.es/blog/', BASE + '/blog/#en'),
           ('https://webautonomos.es/#contacto', BASE + '/en/contact'),
           # pages legales de la langue (14/10/2026)
           ('https://webautonomos.es/aviso-legal/', BASE + '/en/legal-notice/'),
           ('https://webautonomos.es/privacidad/', BASE + '/en/privacy/'),
           ('https://webautonomos.es/cookies/', BASE + '/en/cookies/'),
           ('/aviso-legal/', '/en/legal-notice/'), ('/privacidad/', '/en/privacy/'), ('/cookies/', '/en/cookies/')],
}


def wa(txt):
    return re.sub(r'[^A-Za-z0-9]', lambda m: ''.join('%%%02X' % b for b in m.group(0).encode()), txt)


PAGES = [
    dict(
        nom='diagnostic', src='diagnostico-automatizacion/index.html', urls=DIAG,
        croise=('/visibilidad-ia/', VIS), ld_id='ld-graph',
        meta={
            'fr': dict(title="Automatisation des processus : calculez si c'est rentable",
                       desc="Calculez gratuitement le coût de vos tâches répétitives et s'il est rentable de les automatiser. Prix ferme, devis sous 48 h. 4 questions, 2 minutes.",
                       og_title="Automatisation des processus pour indépendants et PME : calculez si c'est rentable",
                       og_desc="Calculez gratuitement le coût de vos tâches répétitives et s'il est rentable de les automatiser. Prix ferme, devis sous 48 h. 4 questions, 2 minutes.",
                       locale='fr_FR', home='Accueil', crumb="Diagnostic d'automatisation",
                       app_desc="Outil gratuit qui calcule le coût annuel d'une tâche administrative et détermine s'il vaut la peine de l'automatiser, avec quelle technologie minimale et en combien de mois l'investissement est amorti.",
                       browser='Nécessite JavaScript', service_type="Conseil et développement d'automatisations",
                       catalog="Services d'automatisation",
                       offers=[("Diagnostic d'automatisation", "Calcul du coût annuel d'une tâche et de son potentiel d'automatisation."),
                               ("Développement d'une automatisation sur mesure", "Conception, développement, mise en production et maintenance.")],
                       area=['Spain', 'France']),
            'en': dict(title="Process automation for small businesses in Spain: free calculator",
                       desc="See for free what a repetitive task costs you a year: 4 questions, 2 minutes. Six more show if automating it pays off. Fixed quote within 48 h of the call.",
                       og_title="Process automation for freelancers and small businesses: does it pay off?",
                       og_desc="See for free what a repetitive task costs you a year: 4 questions, 2 minutes. Six more show if automating it pays off. Fixed quote within 48 h of the call.",
                       locale='en_GB', home='Home', crumb='Automation diagnostic',
                       app_desc="Free tool that calculates the annual cost of an admin task and whether automating it pays off, with the minimum technology needed and the payback period in months.",
                       browser='Requires JavaScript', service_type='Automation consulting and development',
                       catalog='Automation services',
                       offers=[('Automation diagnostic', "Annual cost of a task and its automation potential."),
                               ('Custom automation development', 'Design, development, deployment and maintenance.')],
                       area=['Spain']),
        },
        wa={'Hola%2C%20he%20hecho%20el%20diagn%C3%B3stico%20de%20automatizaci%C3%B3n':
                {'fr': wa("Bonjour, j'ai fait le diagnostic d'automatisation"),
                 'en': wa("Hello, I've done the automation diagnostic")},
            'Hola%2C%20me%20interesa%20el%20diagn%C3%B3stico%20de%20automatizaci%C3%B3n':
                {'fr': wa("Bonjour, le diagnostic d'automatisation m'intéresse"),
                 'en': wa("Hello, I'm interested in the automation diagnostic")},
            # bouton « Contar mi caso » de la colonne « Lo que no haces » (ajouté le 16/10/2026)
            'Hola%2C%20hay%20algo%20que%20no%20hago%20por%20falta%20de%20tiempo%20y%20me%20gustar%C3%ADa%20comentarlo':
                {'fr': wa("Bonjour, il y a quelque chose que je ne fais pas faute de temps et j'aimerais en parler"),
                 'en': wa("Hello, there's something I don't get round to for lack of time and I'd like to talk it through")}},
        point='10', ancre_comm='\n  Vérifié : 0px de débordement de 1300',
    ),
    dict(
        nom='visibilité IA', src='visibilidad-ia/index.html', urls=VIS,
        croise=('/diagnostico-automatizacion/', DIAG), ld_id='faq-schema',
        meta={
            'fr': dict(title="ChatGPT vous recommande-t-il ? Testez votre visibilité IA",
                       og_title="ChatGPT vous recommande-t-il quand on cherche votre métier dans votre ville ?",
                       og_desc="Découvrez gratuitement si ChatGPT, Gemini, Perplexity et Claude recommandent votre activité dans votre ville. Résultat en 24 h, sans engagement.",
                       locale='fr_FR'),
            'en': dict(title="Does ChatGPT recommend you? Check your AI visibility",
                       og_title="Does ChatGPT recommend you when someone looks for your trade in your city?",
                       og_desc="Find out for free whether ChatGPT, Gemini, Perplexity and Claude recommend your business in your city. Result within 24h, no strings attached.",
                       locale='en_GB'),
        },
        wa={'Hola%2C%20quiero%20comprobar%20si%20la%20IA%20recomienda%20mi%20negocio':
                {'fr': wa("Bonjour, je veux vérifier si l'IA recommande mon activité"),
                 'en': wa("Hello, I'd like to check whether AI recommends my business")}},
        point='7', ancre_comm='\n  Vérifié : 0px de débordement de barre',
    ),
]

# ─── Retouches de la version anglaise du diagnostic (23/10/2026) ─────────────
# Requête « process automation for small businesses » (en-gb), guides SERPmantics
# Google 6ac260bbed2c80ae82cb9dfc et ChatGPT 6acf6048aa073c5111f4f9da : Google
# repassé sous 100 (104 → 98), ChatGPT 16 → 24 (partie protection des données,
# sources ICO et AEPD). Appliquées à T["en"] lu dans la page espagnole, qui ne
# change pas : (clé, ancien, nouveau), dans cet ordre. Si un « ancien » n'est plus
# trouvé exactement une fois (texte anglais modifié dans la page espagnole), le
# script s'arrête : reporter la retouche dans la page espagnole ou la retirer d'ici.
RETOUCHES = {('diagnostic', 'en'): [
    ('c3p',
     'This does not cost hours: it costs money that never comes in.',
     'This does not take hours: it means money that never comes in.'),
    ('c3p',
     'This does not take hours: it means money that never comes in.',
     'The loss here is not time: it is money that never comes in.'),
    ('a2p',
     'Annual cost of bureaucracy per sole trader, per ATA.',
     'Yearly bill for paperwork per sole trader, per ATA.'),
    ('ex2s',
     'It has no current cost because it does not happen.',
     'Nobody pays for it today because it does not happen.'),
    ('ex2s',
     'And it is usually what leaves the most money on the table.',
     'And it can leave a lot of money on the table.'),
    ('ex2Note',
     'you cannot measure the cost of something you do not do',
     'you cannot put a figure on something you do not do'),
    ('pg3p',
     'And we tell you what to configure yourself, at no cost. A project that does not pay back is not a small project: it is a project not to do.',
     'And we tell you what to configure yourself, without charging you. Something that does not pay back is not a smaller version of a good idea: it is simply not worth doing.'),
    ('pg3p',
     'Something that does not pay back is not a smaller version of a good idea: it is simply not worth doing.',
     'Something that does not pay back is not a small win: it is a loss.'),
    ('faq',
     'With maintenance, we fix it at no extra cost.',
     'With maintenance, we fix it without an extra charge.'),
    ('faq',
     'Yes. The hourly cost you enter is then the value of your own time: what you bill per hour, or what you would stop billing if those hours went to client work.',
     'Yes. The hourly rate you enter is then the value of your own time: what you bill per hour, or what you would stop billing if that time went to clients.'),
    ('faq',
     'We ask for your name, company and email to send you the report;',
     'We ask for your name, company and email to send you the PDF;'),
    ('faq',
     'are used to produce the diagnostic and the report.',
     'are used to produce the diagnostic and the PDF.'),
    ('faq',
     'Either way, the PDF report reaches your inbox within one working day.',
     'Either way, the PDF reaches your inbox within one working day.'),
    ('faq',
     'With maintenance, we fix it without an extra charge.',
     'With maintenance, we fix it at no further charge.'),
    ('p4Eyebrow',
     'What doing nothing costs',
     'The price of doing nothing'),
    ('p4Title',
     'look at what automating it costs.',
     'look at the price of automating it.'),
    ('ex1h',
     'What you already do, and it costs you',
     'What you already do, and pay for'),
    ('heroHonest',
     'can free up 10 to 20 hours a month. Others free up none',
     'can give you back time every month. Others give back none'),
    ('g4b',
     'Most business platforms offer a free trial; test it on one workflow first.',
     'Many business platforms offer a trial period; test it on one workflow first.'),
    ('g4b',
     'you rarely need to start with the most expensive one',
     'you rarely need the most expensive one to begin with'),
    ('g4b',
     'filters that sort incoming email by sender and topic',
     'filters that sort incoming messages by sender and topic'),
    ('g4b',
     '<h4>Which tools fit which job</h4>',
     '<h4>Which tools fit which need</h4>'),
    ('g4b',
     'sending the customer an update when the job is done',
     'sending the customer an update once it is finished'),
    ('g4b',
     '<strong>Check the integration</strong> with the software you already use',
     '<strong>Check that an integration is available</strong> with the software you already use'),
    ('g4b',
     'Is there support in English, and does the provider understand Spanish compliance requirements such as electronic invoicing?',
     'Is support available in English, and does the provider understand Spanish compliance requirements and tax regulations, such as electronic invoicing?'),
    ('g4b',
     'bank feeds, recurring invoices and payment reminders, often with tax compliance features built in.',
     'bank feeds, recurring invoices and payment reminders; these often include tax compliance features.'),
    ('g4b',
     'when it makes sense to build around very specific processes or the handling of a lot of data.',
     'when it makes sense to build around very specific processes or a large volume of records.'),
    ('g4b',
     'or a large volume of records.',
     'or the handling of a large volume of records.'),
    ('g4b',
     'as long as the software handles Spanish invoicing and data protection requirements, which are not the same as in the UK.',
     "as long as the software handles Spanish invoicing and data protection requirements, which are not the same as in the UK; here, the guidance of the AEPD, Spain's data protection regulator, is the reference."),
    ('g4b',
     'Many business owners who moved here from the UK keep using the tools they knew there.',
     'Many business owners now living in Spain keep using the tools they knew in Britain.'),
    ('g4b',
     'Many business owners now living in Spain keep using the tools they knew in Britain.',
     'Many business owners now living in Spain keep using the tools they knew in the UK.'),
    ('gMidCta',
     'Price it in two minutes with the free diagnostic',
     'Price it in two minutes with the diagnostic'),
    ('g1b',
     'answering frequently asked questions about your services',
     'answering the same enquiries about your services'),
    ('g1b',
     '<h4>Three questions to find the right process</h4>',
     '<h4>Three checks to find the right process</h4>'),
    ('g1b',
     'currently involve manual data entry or cause errors',
     'currently involve typing things in by hand or cause errors'),
    ('g1b',
     'send each student a welcome email, with no manual data entry.',
     'send each student a welcome email, without anyone retyping it.'),
    ('g1b',
     'it is the right moment to review this process and check its compliance',
     'it is the right moment to look again at this process and check its compliance'),
    ('g1b',
     'preparing paperwork for your gestor',
     'preparing the paperwork your gestor needs to keep the books'),
    ('g1b',
     'currently involve typing things in by hand or cause errors',
     'currently involve manual typing or cause errors'),
    ('g1b',
     'send each student a welcome email, without anyone retyping it.',
     'send each student a welcome email, with no manual copying.'),
    ('g1b',
     'it is the right moment to look again at this process',
     'it is the right moment to revisit this process'),
    ('g1b',
     'moving the details from your website forms into your CRM',
     'moving enquiries from your website forms into your CRM'),
    ('g1b',
     'and send each customer an update automatically.',
     'and update each customer automatically.'),
    ('g1b',
     'sending payment reminders and reconciling payments with the bank, which keeps',
     'sending payment reminders with links to pay online and reconciling payments with the bank statement, which keeps'),
    ('g1b',
     'filing each supplier invoice, whether it arrives by email or by post, in the right folder, renaming files',
     'filing each supplier invoice, whether it arrives by email or by post, in the right folder where anyone can search for it later, renaming files'),
    ('g1b',
     'bringing sales, expenses and activity figures together in one dashboard',
     'bringing sales, expenses and other financial figures together in one dashboard'),
    ('g1b',
     'new enquiries logged in the CRM, follow-up emails scheduled, quotes generated from a template.',
     'new enquiries logged in the CRM, follow-up emails scheduled, quotes generated from a template and a request for feedback after each site visit.'),
    ('g1b',
     'invoices issued when a job is marked as done, payments matched with the bank feed, a weekly summary for the gestor.',
     'invoices issued, with the next number in the series, when a job is marked as done; payments matched with the bank feed; credit notes created when an order is returned; reminder letters ready to print for customers who never read their email; a weekly summary for the gestor.'),
    ('g1b',
     'onboarding checklists, holiday requests, shared calendars',
     'onboarding checklists, leave requests, shared calendars'),
    ('g1b',
     'create a job in the management software, with an alert if the customer does not reply within a few days.',
     'create a job in the management software, with the address and phone number filled in, and an alert if the customer does not reply within a few days.'),
    ('g1b',
     'credit notes created when an order is returned;',
     'credit notes raised when an order comes back under your returns policy;'),
    ('g1b',
     'onboarding checklists, leave requests, shared calendars and expense claims handled in one place.',
     'onboarding checklists, leave requests, insurance renewal dates, shared calendars and expense claims handled in one place.'),
    ('g1b',
     'For freelancers and small businesses, they are usually these:',
     'For freelancers and small businesses, they are often these:'),
    ('s2t',
     'With the questions, the figure right away',
     'Answer them and the figure appears at once'),
    ('s2t',
     'Answer them and the figure appears at once',
     'The figure appears as soon as you answer'),
    ('p1Lead',
     'on administrative work, against',
     'on administration, against'),
    ('p1Lead',
     'It goes between systems.',
     'It goes between platforms.'),
    ('p4Lead',
     'and that is before the rest of the repetitive work in the business.',
     'and that is before everything else that repeats in the business.'),
    ('p4Lead',
     '28 eight-hour days, close to a full working month.',
     '28 eight-hour days, nearly a whole month.'),
    ('s3p',
     "your opportunities in order, where to start and what might not work. If automating doesn't pay off, we tell you that too.",
     'your opportunities in order, where to begin and what might fail. If none of it pays off, we tell you that too.'),
    ('g8b',
     'is what weighs on you most, start by measuring it:',
     'is what weighs on you most, measure it first:'),
    ('g8b',
     'Before automating anything that touches invoices or personal data',
     'Before handing software anything that touches invoices or personal data'),
    ('g8b',
     '<p>Start small. This week,',
     '<p>Whatever your trade, start small. This week,'),
    ('g8b',
     'Once your first workflows are running, the next ones come faster.',
     'Once your first workflows are running, the learning curve flattens and the next ones come faster: you know what to improve.'),
    ('g2b',
     'every lead gets an email response the same business day',
     'every lead gets a response the same business day'),
    ('g2b',
     'the same teams handle more customers and more orders, and operations grow',
     'the same teams handle more customers and more orders, even at busy times, and operations grow'),
    ('g2b',
     'the same teams handle more customers and more orders, even at busy times,',
     'the same teams handle more customers and more orders, even when the order book is full,'),
    ('pxNote',
     'until one of your systems changes; we then charge repairs',
     'until one of your tools changes; we then charge repairs'),
    ('g5b',
     'An AI agent is rarely necessary: keep it',
     'An agent is rarely necessary: keep it'),
    ('g5b',
     "it can help lighten the load on your team's inbox: it sorts messages",
     'it can help lighten the load of incoming mail: it sorts messages'),
    ('g5b',
     'Even so, most processes in a small business can be handled',
     'Even so, many processes in a small business can be handled'),
    ('g5b',
     'and always keep a human check on anything that affects clients or payments.',
     'and take care with anything that affects clients or payments: always have a person check it.'),
    ('g5b',
     'Even so, many processes in a small business can be handled',
     'Even so, many processes in small businesses can be handled'),
    ('g5b',
     'always have a person check it.',
     'always have someone check it.'),
    ('g5b',
     'An agent is rarely necessary: keep it for the stages where it can add something, and take care with anything that affects clients or payments: always have someone check it.',
     'An agent is rarely necessary: keep it for the stages where it can add something. Take care with anything that affects clients or payments, and always have someone check it.'),
    ('p2Eyebrow',
     'How it works',
     'In practice'),
    ('pxLead',
     'Most tasks are solved at the first two.',
     'Many tasks are solved at the first two.'),
    ('g0b',
     'Most automation follows a simple pattern called a workflow.',
     'Automation often follows a simple pattern called a workflow.'),
    ('g0b',
     'most modern business software now includes automation features',
     'a great deal of modern business software now includes automation features'),
    ('g0b',
     'A trigger sets it off (an email arrives, a customer fills in a form, an invoice is issued)',
     'A trigger sets it off (an email arrives, a customer fills in a form or opens a support request, an invoice is issued)'),
    ('d1p',
     'In most cases, configuring what you already have',
     'Often, configuring what you already have'),
    ('d1p',
     'It costs four times less than an AI agent',
     'It costs much less than an AI agent'),
    ('g3b',
     '<strong>Describe the process as it is today</strong>: who does what',
     '<strong>Describe the current process</strong>: who does what'),
    ('g3b',
     'note what each automation does and who maintains it, and schedule a check every few months.',
     'note what each automation does and who maintains it, and schedule a check every few months to see what to improve.'),
    ('g3b',
     '<strong>Test it with your own data</strong>, under supervision,',
     '<strong>Test it several times with your own data</strong>, under supervision,'),
    ('ex1s',
     'There is a volume, a duration and an annual cost. The diagnostic prices them and tells you whether it is worth it.',
     'There is a volume, a duration and a yearly price. The diagnostic puts figures on them and tells you whether it is worth it.'),
    ('gCta',
     'Use the diagnostic on this page: four questions about one task, and it gives you a figure you can check.',
     'Use the diagnostic on this page: describe one task and it gives you its yearly cost, a figure you can check.'),
    ('gCta',
     'describe one task and it gives you its yearly cost, a figure you can check.',
     'describe one task and it puts a yearly figure on it, one you can check.'),
    ('pg1t',
     'A fixed quote within 48 hours',
     'A fixed quote within 48 hours of the call'),
    ('pg1p',
     'We scope the project and give you a fixed quote within 48 hours of the video call. Not a range',
     'We scope the project with you on the video call, then you get a fixed price in writing. Not a range'),
    ('s1p',
     'Or both, for the most accurate report.',
     'Or both, for the most accurate result.'),
    ('footLead',
     'If it points the other way, you save the money and we tell you that too.',
     'If it points the other way, you spend nothing and we tell you that too.'),
    ('g6b',
     'It is also worth comparing automation with taking on staff:',
     'It is also useful to compare automation with taking on staff:'),
    ('g6b',
     '<strong>Maintenance</strong>: fixes when a connected system changes.',
     '<strong>Maintenance</strong>: fixes when a connected system or service changes.'),
    ('g6b',
     '<strong>Training</strong>: a short session so that your staff know what the automation does.',
     '<strong>Training</strong>: a short session to help your staff understand what the automation does.'),
    ('g7b',
     'so you never know whether the automation saved time, and',
     'so you never know whether the automation saved time or improved anything, and'),
    ('g7b',
     '<h4>What official British guidance says</h4><p>Many readers of this page moved to Spain from Britain, so it can be useful to know where British public bodies stand. Their pages describe the law in Britain, not in Spain, where the GDPR applies and the Spanish data protection authority (AEPD) gives the advice; the principles still carry over well.</p>',
     '<h4>Data protection: what official guidance says</h4><p>Many readers of this page are British and living in Spain, so it helps to know both sides. In Spain, the GDPR and Spanish data protection law apply, and the AEPD, the Spanish data protection authority, publishes the guidance. British public bodies describe the law in Britain, but their pages are written for small organisations and the principles carry over well.</p>'),
    ('g7b',
     'people must be told about it and given easy ways to ask for someone to intervene or to challenge the decision, and the process must be checked regularly.</li>',
     'people must be told about it and given easy ways to ask for someone to intervene or to challenge the decision, and the process must be checked regularly. Its examples are the automatic refusal of an online credit application and recruitment without human intervention; because this processing is considered high-risk, an impact assessment (DPIA) is required first.</li>'),
    ('g7b',
     "<p>The practical lesson, in Spain as in Britain: keep someone in charge of any decision that affects a customer's finances or rights, collect only the personal data the workflow needs, and describe what the automation does in your privacy policy. Your gestor or a data protection adviser can check the legal and tax side.</p><p>Before you automate anything that handles personal data, three checks are worthwhile: what the law requires of you, which detailed guidance is available from the regulator in your country, and whether your privacy policy and terms still describe what you do. Financial records, tax documents and payment reminders deserve the closest attention, because errors there affect people directly. A short analysis on paper, before any software is involved, can improve the result more than the choice of platform. If you search the AEPD or ICO websites, both have published practical guidance for smaller organisations, free and public.</p>",
     "<h4>Five checks before you automate personal data</h4><p>A short analysis on paper, before any software is involved, can improve the result more than the choice of platform. In Spain as in Britain, check these points:</p><ul><li><strong>Collect only what the workflow needs</strong>: if a form asks for a tax identification number or a date of birth, there should be a reason for it.</li><li><strong>Transparency</strong>: your privacy notices should include, in plain terms, what the automation does with people's personal data.</li><li><strong>A person in charge of decisions that matter</strong>: the law restricts decisions made by software alone when they have legal or similarly significant effects, so keep someone involved before turning down an application or a request.</li><li><strong>Each tool's terms</strong>: check where the information is stored and that the provider signs a written agreement as your data processor.</li><li><strong>Financial records</strong>: invoices, bank statements and tax documents need care, because tax regulations set what they must contain and errors there affect people directly.</li></ul><p>Your gestor or a data protection adviser can check the legal and tax side. If you search the AEPD website, you will find detailed guidance and <a href='https://www.aepd.es/guias-y-herramientas/herramientas/facilita-rgpd' target='_blank' rel='noopener'>Facilita RGPD</a>, a tool for companies and professionals that handle low-risk personal data, such as customer or supplier records: it drafts a first set of documents, which you then adapt. Visit the ICO website for the British equivalent.</p>"),
    ('g7b',
     'so it helps to know both sides. In Spain, the GDPR and Spanish data protection law apply, and the AEPD, the Spanish data protection authority, publishes the guidance. British public bodies describe the law in Britain, but their pages are written for small organisations and the principles carry over well.',
     'so it is useful to know both sides. In Spain, the GDPR and the Spanish law that completes it apply, and the AEPD, the national regulator, has published the guidance. British public bodies describe the law in Britain, but their pages are written for small businesses and organisations, and the principles carry over well.'),
    ('g7b',
     'check where the information is stored and that the provider signs',
     'check where everything is stored and that the provider signs'),
    ('g7b',
     "If you search the AEPD website, you will find detailed guidance and <a href='https://www.aepd.es/guias-y-herramientas/herramientas/facilita-rgpd' target='_blank' rel='noopener'>Facilita RGPD</a>, a tool for companies and professionals that handle low-risk personal data, such as customer or supplier records: it drafts a first set of documents, which you then adapt.",
     "The AEPD website has detailed guidance and <a href='https://www.aepd.es/guias-y-herramientas/herramientas/facilita-rgpd' target='_blank' rel='noopener'>Facilita RGPD</a>, a tool for companies and professionals whose processing is low-risk, such as customer or supplier records: it drafts a first set of documents, which you then adapt."),
    ('g7b',
     'because this processing is considered high-risk, an impact assessment (DPIA) is required first.',
     'because this type of processing carries a high risk, an impact assessment (DPIA) is required first.'),
    ('g7b',
     'Your gestor or a data protection adviser can check the legal and tax side. The AEPD website',
     'Your gestor or a data protection adviser can give advice on the legal and tax side. The AEPD website'),
    ('g7b',
     'if a form asks for a tax identification number or a date of birth',
     'if a form asks for an identity number or a date of birth'),
    ('g7b',
     'your privacy notices should include, in plain terms,',
     'your privacy policy and notices should include, in plain terms,'),
    ('g7b',
     'so keep someone involved before turning down an application or a request.',
     'so keep someone involved in anything with financial or legal consequences for a customer.'),
    ('g7b',
     'if a form asks for an identity number or a date of birth',
     'if a form asks for a national identity number or a date of birth'),
    ('g7b',
     'can give advice on the legal and tax side.',
     'can give advice on the legal and accounting side.'),
    ('g7b',
     'a tool for companies and professionals whose processing is low-risk',
     'a tool for businesses and professionals whose processing is low-risk'),
    ('g7b',
     'and the AEPD, the national regulator, has published the guidance. British public bodies describe the law in Britain, but their pages are written for small businesses and organisations, and the principles carry over well.',
     'and the AEPD, the national regulator, publishes guidance on them. British public bodies describe the law in Britain, and the ICO writes much of its advice for small businesses and organisations; the principles carry over well.'),
    ('g7b',
     'says that when a decision with legal or similarly significant effects is made by software alone, people must be told about it',
     'says that when a decision with legal or similarly significant effects is made by software alone, transparency comes first: people must be told about it'),
    ('g7b',
     'instead of fixing it first, is the most frequent mistake. Next comes <strong>not measuring</strong>,',
     'instead of fixing it first, is a frequent mistake. So is <strong>not measuring</strong>,'),
    ('ctaHowSub',
     'Free, with no commitment. PDF report within one working day.',
     'Free, with no commitment. PDF within one working day.'),
    ('g7h',
     'Common mistakes',
     'Common mistakes and the GDPR'),
    ('gSom',
     "<li><a href='#guia-7'>Common mistakes</a></li>",
     "<li><a href='#guia-7'>Common mistakes and the GDPR</a></li>"),
]}



def _compte(v, a):
    return v.count(a) if isinstance(v, str) else sum(_compte(x, a) for x in v)


def _remplace(v, a, b):
    return v.replace(a, b) if isinstance(v, str) else [_remplace(x, a, b) for x in v]


def retoucher(p, lang, T):
    """T avec les retouches propres à la copie (p, lang) ; T n'est pas modifié."""
    liste = RETOUCHES.get((p['nom'], lang))
    if not liste:
        return T
    t = dict(T[lang])
    for cle, ancien, nouveau in liste:
        if _compte(t.get(cle, ''), ancien) != 1:
            abandon('retouche %s/%s de T.%s.%s : texte trouvé %dx (1 attendu) : %r'
                    % (p['nom'], lang, lang, cle, _compte(t.get(cle, ''), ancien), ancien[:80]))
        t[cle] = _remplace(t[cle], ancien, nouveau)
    T = dict(T)
    T[lang] = t
    return T


def retoucher_script(p, lang, s, T):
    """Mêmes retouches dans l'objet T écrit dans le script de la copie (bloc
    « lang:{ … } ») : au chargement, render() réécrit la page depuis T[lang], et la
    FAQ du JSON-LD est comparée à T[PAGE_LANG].faq. T = textes non retouchés."""
    liste = RETOUCHES.get((p['nom'], lang))
    if not liste:
        return s
    debut = '\n%s:{\n' % lang
    if s.count(debut) != 1:
        abandon('retouches %s/%s : bloc « %s:{ » trouvé %dx' % (p['nom'], lang, lang, s.count(debut)))
    a = s.index(debut)
    b = s.index('\n}\n,\n', a)
    bloc, cur = s[a:b], dict(T[lang])
    for cle, ancien, nouveau in liste:
        brut_a, brut_n = ancien, nouveau
        if cur.get(cle) == ancien:  # valeur entière : la clé lève l'ambiguïté (« How it works » est aussi nav3)
            brut_a, brut_n = '%s:"%s"' % (cle, ancien), '%s:"%s"' % (cle, nouveau)
        if bloc.count(brut_a) != 1:
            abandon('retouche %s/%s de T.%s.%s dans le script : trouvée %dx (1 attendu) : %r'
                    % (p['nom'], lang, lang, cle, bloc.count(brut_a), ancien[:80]))
        bloc = bloc.replace(brut_a, brut_n)
        cur[cle] = _remplace(cur[cle], ancien, nouveau)
    return s[:a] + bloc + s[b:]


VAR_LANG = 'var lang = (new URLSearchParams(location.search).get("lang") || "es").toLowerCase();'


def snippet(urls):
    return ('/* Adresses par langue (build_i18n_pages.py). Une langue qui a sa propre\n'
            '   adresse s\'y affiche : ?lang=fr et ?lang=en y renvoient, en gardant les\n'
            '   autres paramètres (gclid, utm) ; le menu des langues y mène. Une langue\n'
            '   sans adresse propre (ca) s\'affiche sur la page espagnole en ?lang=. */\n'
            'var PAGE_LANG = "es";\n'
            'var PAGE_URLS = %s;\n'
            'function cibleLangue(l){\n'
            '  var u = PAGE_URLS[l], q = new URLSearchParams(location.search);\n'
            '  q.delete("lang");\n'
            '  if (!u){\n'
            '    if (location.pathname === PAGE_URLS.es) return null;\n'
            '    u = PAGE_URLS.es; q.set("lang", l);\n'
            '  }\n'
            '  if (u === location.pathname) return null;\n'
            '  var s = q.toString();\n'
            '  return u + (s ? "?" + s : "") + location.hash;\n'
            '}\n'
            'function allerA(l){ var c = cibleLangue(l); if (c) location.href = c; return !!c; }\n'
            '(function(){\n'
            '  var l = (new URLSearchParams(location.search).get("lang") || "").toLowerCase();\n'
            '  if (l && l !== PAGE_LANG && T[l]){ var c = cibleLangue(l); if (c) location.replace(c); }\n'
            '})();\n'
            'var lang = (new URLSearchParams(location.search).get("lang") || PAGE_LANG).toLowerCase();'
            % json.dumps(urls))


EXTRACT = r"""
const fs=require('fs');
let src=fs.readFileSync(process.argv[2],'utf8');
let i=src.search(/(?:var|const|let)\s+T\s*=\s*\{/);
if(i<0){console.error('objet T introuvable');process.exit(2);}
i=src.indexOf('{',i);
let d=0,j=i,q=null;
for(;j<src.length;j++){
  const c=src[j], pv=src[j-1];
  if(q){ if(c===q&&pv!=='\\')q=null; continue; }
  if(c==='"'||c==="'"||c==='`'){q=c;continue;}
  if(c==='/'&&src[j+1]==='/'){j=src.indexOf('\n',j);continue;}
  if(c==='/'&&src[j+1]==='*'){j=src.indexOf('*/',j)+1;continue;}
  if(c==='{')d++; else if(c==='}'&&--d===0){j++;break;}
}
let obj; eval('obj='+src.slice(i,j));
fs.writeFileSync(process.argv[3], JSON.stringify(obj));
"""


def textes(path):
    with tempfile.TemporaryDirectory() as tmp:
        js, out = os.path.join(tmp, 'x.js'), os.path.join(tmp, 'o.json')
        open(js, 'w', encoding='utf-8').write(EXTRACT)
        r = subprocess.run(['node', js, path, out], capture_output=True, text=True)
        if r.returncode:
            abandon('lecture de T dans %s : %s' % (path, r.stderr.strip()[:200]))
        return json.load(open(out, encoding='utf-8'))


def abandon(msg):
    sys.exit('ABANDON : %s\nRien n\'a été modifié.' % msg)


def lire(rel):
    return open(os.path.join(ROOT, rel), encoding='utf-8').read()


def une_fois(s, ancien, nouveau, quoi):
    n = s.count(ancien)
    if n != 1:
        abandon('%s : trouvé %dx (1 attendu)' % (quoi, n))
    return s.replace(ancien, nouveau)


def remplacer_balise(s, motif, nouveau, quoi):
    ms = list(re.finditer(motif, s))
    if len(ms) != 1:
        abandon('%s : trouvé %dx (1 attendu)' % (quoi, len(ms)))
    return s[:ms[0].start()] + nouveau + s[ms[0].end():]


def zones_commentaires(s):
    return [(m.start(), m.end()) for m in re.finditer(r'<!--.*?-->', s, re.S)]


def remplir_data_t(s, tr):
    """Remplace le contenu de chaque élément data-t="clé" par tr[clé] (hors
    commentaires), en suivant l'imbrication des balises de même nom."""
    com = zones_commentaires(s)
    dans_com = lambda i: any(a <= i < b for a, b in com)
    out, pos, n = [], 0, 0
    for m in re.finditer(r'<(\w+)\b[^>]*\bdata-t="([\w.]+)"[^>]*>', s):
        if m.start() < pos or dans_com(m.start()):
            continue
        tag, cle = m.group(1), m.group(2)
        val = tr.get(cle)
        if not isinstance(val, str):
            continue
        d, fin = 1, None
        for t in re.finditer(r'<%s\b|</%s>' % (tag, tag), s[m.end():]):
            d += 1 if not t.group(0).startswith('</') else -1
            if d == 0:
                fin = m.end() + t.start()
                break
        if fin is None:
            abandon('balise <%s data-t="%s"> non refermée' % (tag, cle))
        out.append(s[pos:m.end()]); out.append(val); pos = fin; n += 1
    out.append(s[pos:])
    s = ''.join(out)
    # placeholders
    def ph(m):
        val = tr.get(m.group(2))
        if not isinstance(val, str):
            return m.group(0)
        t = m.group(0)
        v = html.escape(val, quote=True)
        if re.search(r'\bplaceholder="[^"]*"', t):
            return re.sub(r'\bplaceholder="[^"]*"', 'placeholder="%s"' % v, t)
        return t[:-1] + ' placeholder="%s">' % v if not t.endswith('/>') else t[:-2] + ' placeholder="%s"/>' % v
    s = re.sub(r'<(\w+)\b[^>]*\bdata-tph="([\w.]+)"[^>]*>', ph, s)
    return s, n


def liens_a(s, paires):
    """Remplace href="ancien" par href="nouveau" dans les balises <a> seulement."""
    def balise(m):
        t = m.group(0)
        for a, b in paires:
            t = t.replace('href="%s"' % a, 'href="%s"' % b)
        return t
    return re.sub(r'<a\b[^>]*>', balise, s)


def hreflang_bloc(urls, page_es):
    return ('<link rel="alternate" hreflang="es-ES" href="%s%s">\n'
            '<link rel="alternate" hreflang="ca-ES" href="%s%s?lang=ca">\n'
            '<link rel="alternate" hreflang="en" href="%s%s">\n'
            '<link rel="alternate" hreflang="fr" href="%s%s">\n'
            '<link rel="alternate" hreflang="x-default" href="%s%s">'
            % (BASE, urls['es'], BASE, page_es, BASE, urls['en'], BASE, urls['fr'], BASE, urls['es']))


HREFLANG_RE = r'<link rel="alternate" hreflang="es-ES"[^>]*>\s*<link rel="alternate" hreflang="ca-ES"[^>]*>\s*<link rel="alternate" hreflang="en"[^>]*>\s*<link rel="alternate" hreflang="fr"[^>]*>\s*<link rel="alternate" hreflang="x-default"[^>]*>'


def patch_source(p, s):
    """Modifications (une seule fois) de la page espagnole."""
    if 'var PAGE_LANG' in s:
        return s, False
    s = remplacer_balise(s, HREFLANG_RE, hreflang_bloc(p['urls'], p['urls']['es']), p['src'] + ' hreflang')
    s = une_fois(s, VAR_LANG, snippet(p['urls']), p['src'] + ' ligne var lang')
    s, k = re.subn(r'(function choisir\(l\)\{\n)(\s*)lang = l;', r'\1\2if (allerA(l)) return;\n\2lang = l;', s)
    if k != 1:
        abandon('%s : fonction choisir() trouvée %dx' % (p['src'], k))
    note = ('\n  %s. Versions FR et EN à leur propre adresse (23/09/2026, build_i18n_pages.py) :\n'
            '       %s   %s\n'
            '     Elles sont GÉNÉRÉES depuis cette page : modifier ici, puis relancer\n'
            '     python3 _tools/build_i18n_pages.py. Ici : hreflang en/fr vers ces\n'
            '     adresses ; PAGE_LANG / PAGE_URLS / allerA() juste avant « var lang » :\n'
            '     ?lang=fr et ?lang=en redirigent (gclid, utm conservés), le menu des\n'
            '     langues y mène. Le valencien reste en ?lang=ca sur cette adresse.\n'
            % (p['point'], p['urls']['fr'], p['urls']['en']))
    s = une_fois(s, p['ancre_comm'], note + p['ancre_comm'], p['src'] + ' commentaire')
    return s, True


def jsonld_diag(g, lang, url, T, m):
    t = T[lang]
    for n in g['@graph']:
        typ = n.get('@type')
        if typ == 'WebPage':
            n.update({'@id': url + '#webpage', 'url': url, 'name': m['title'], 'description': m['og_desc'],
                      'inLanguage': lang})
        elif typ == 'BreadcrumbList':
            n['itemListElement'] = [
                {"@type": "ListItem", "position": 1, "name": m['home'], "item": BASE + '/%s/' % lang},
                {"@type": "ListItem", "position": 2, "name": m['crumb'], "item": url}]
        elif typ == 'WebApplication':
            n.update({'@id': url + '#app', 'url': url, 'name': m['crumb'], 'description': m['app_desc'],
                      'browserRequirements': m['browser']})
        elif typ == 'Service':
            n['name'] = re.sub(r'<[^>]+>', '', t['h1']).rstrip('.')
            n['serviceType'] = m['service_type']
            n['areaServed'] = [{"@type": "Country", "name": a} for a in m['area']]
            cat = n.get('hasOfferCatalog')
            if cat:
                cat['name'] = m['catalog']
                for item, (nom, desc) in zip(cat['itemListElement'], m['offers']):
                    item['itemOffered']['name'] = nom
                    item['itemOffered']['description'] = desc
        elif typ == 'FAQPage':
            n['inLanguage'] = lang
            n['mainEntity'] = [{"@type": "Question", "name": q[0],
                                "acceptedAnswer": {"@type": "Answer", "text": q[1]}} for q in t['faq']]
    return g


def copie(p, src, lang, T):
    m, url = p['meta'][lang], BASE + p['urls'][lang]
    s = retoucher_script(p, lang, src, T)  # retouches propres à la copie (RETOUCHES)
    T = retoucher(p, lang, T)
    s = une_fois(s, 'var PAGE_LANG = "es";', 'var PAGE_LANG = "%s";' % lang, 'PAGE_LANG')
    s = une_fois(s, '<html lang="es">', '<html lang="%s">' % lang, 'balise html')
    s = une_fois(s, '<head>\n', '<head>\n<!-- Page GÉNÉRÉE par _tools/build_i18n_pages.py depuis %s (version %s).\n'
                 '     Ne pas modifier : modifier la page espagnole, puis relancer le script. -->\n'
                 % (p['src'], lang), '<head>')
    t = T[lang]
    title = m.get('title') or t['metaTitle']
    desc = m.get('desc') or t['metaDesc']
    E = lambda x: html.escape(x, quote=True)
    s = remplacer_balise(s, r'<title>[^<]*</title>', '<title>%s</title>' % E(title), 'title')
    s = remplacer_balise(s, r'<meta name="description" content="[^"]*">', '<meta name="description" content="%s">' % E(desc), 'description')
    s = remplacer_balise(s, r'<link rel="canonical" href="[^"]*">', '<link rel="canonical" href="%s">' % url, 'canonical')
    s = remplacer_balise(s, HREFLANG_RE, hreflang_bloc(p['urls'], p['urls']['es']), 'hreflang')
    s = remplacer_balise(s, r'<meta property="og:url" content="[^"]*">', '<meta property="og:url" content="%s">' % url, 'og:url')
    s = remplacer_balise(s, r'<meta property="og:title" content="[^"]*">', '<meta property="og:title" content="%s">' % E(m['og_title']), 'og:title')
    s = remplacer_balise(s, r'<meta property="og:description" content="[^"]*">', '<meta property="og:description" content="%s">' % E(m['og_desc']), 'og:description')
    s = remplacer_balise(s, r'<meta property="og:locale" content="[^"]*">', '<meta property="og:locale" content="%s">' % m['locale'], 'og:locale')
    if '<meta name="twitter:title"' in s:
        s = remplacer_balise(s, r'<meta name="twitter:title" content="[^"]*">', '<meta name="twitter:title" content="%s">' % E(m['og_title']), 'twitter:title')
    if '<meta name="twitter:description"' in s:
        s = remplacer_balise(s, r'<meta name="twitter:description" content="[^"]*">', '<meta name="twitter:description" content="%s">' % E(m.get('tw_desc') or m['og_desc']), 'twitter:description')
    # JSON-LD
    mo = re.search(r'(<script type="application/ld\+json" id="%s">)(.*?)(</script>)' % p['ld_id'], s, re.S)
    if not mo:
        abandon('%s : JSON-LD #%s introuvable' % (p['src'], p['ld_id']))
    g = json.loads(mo.group(2))
    if p['ld_id'] == 'ld-graph':
        g = jsonld_diag(g, lang, url, T, m)
    else:
        g['inLanguage'] = lang
        g['mainEntity'] = [{"@type": "Question", "name": q[0],
                            "acceptedAnswer": {"@type": "Answer", "text": q[1]}} for q in t['faq']]
    s = s[:mo.start(2)] + '\n' + json.dumps(g, ensure_ascii=False, indent=2) + '\n' + s[mo.end(2):]
    # le contrôle d'intégrité compare le JSON-LD écrit à la FAQ de la page
    s = s.replace('T.es.faq', 'T[PAGE_LANG].faq')
    # textes
    s, n = remplir_data_t(s, t)
    # questions de la FAQ dans le HTML, dans la langue de la copie
    s, _ = remplir_faq(s, t['faq'], 'faq-list' if p['ld_id'] == 'faq-schema' else 'faq')
    # liens
    ancien, cible = p['croise']
    s = liens_a(s, NAV[lang] + [(ancien, cible[lang])])
    # libellés du pied de page légal dans la langue de la copie (14/10/2026)
    LIBELLES = {'fr': {'mentions-legales/': 'Mentions légales', 'confidentialite/': 'Confidentialité'},
                'en': {'legal-notice/': 'Legal notice', 'privacy/': 'Privacy'}}
    for chemin, lib in LIBELLES[lang].items():
        s = re.sub(r'(<a href="/%s/%s">)(Aviso legal|Privacidad)(</a>)' % (lang, re.escape(chemin)),
                   lambda mo: mo.group(1) + lib + mo.group(3), s)
    for es_txt, trad in p['wa'].items():
        s = s.replace('?text=' + es_txt + '"', '?text=' + trad[lang] + '"')
    return s, n


def controles(rel, s, src, lang, p):
    err = []
    if re.findall(r'<link rel="canonical" href="([^"]+)"', s) != [BASE + p['urls'][lang]]:
        err.append('canonical')
    if '<html lang="%s">' % lang not in s:
        err.append('lang')
    alt = sorted(re.findall(r'<link rel="alternate" hreflang="([^"]+)" href="([^"]+)"', s))
    alt_src = sorted(re.findall(r'<link rel="alternate" hreflang="([^"]+)" href="([^"]+)"', src))
    if alt != alt_src:
        err.append('hreflang différents de la page espagnole')
    for bloc in re.findall(r'<script type="application/ld\+json"[^>]*>(.*?)</script>', s, re.S):
        try:
            json.loads(bloc)
        except ValueError as exc:
            err.append('JSON-LD invalide (%s)' % exc)
    scripts = [m.group(2) for m in re.finditer(r'<script(\s[^>]*)?>(.*?)</script>', s, re.S)
               if 'ld+json' not in (m.group(1) or '') and m.group(2).strip()]
    with tempfile.TemporaryDirectory() as tmp:
        for k, js in enumerate(scripts):
            f = os.path.join(tmp, 's%d.js' % k)
            open(f, 'w', encoding='utf-8').write(js)
            r = subprocess.run(['node', '--check', f], capture_output=True, text=True)
            if r.returncode:
                err.append('script %d invalide (%s)' % (k, r.stderr.strip()[:120]))

    def ecart(x, tag):
        v = re.sub(r'<!--.*?-->', '', x, flags=re.S)
        v = re.sub(r'<script.*?</script>', '', v, flags=re.S)
        return len(re.findall(r'<%s[\s>]' % tag, v)) - v.count('</%s>' % tag)
    for tag in ('div', 'section', 'a', 'p', 'h1', 'h2', 'h3', 'span', 'button', 'li', 'ul'):
        if ecart(s, tag) != ecart(src, tag):
            err.append('équilibre des <%s> modifié' % tag)
    liens = ' '.join(re.findall(r'<a\b[^>]*>', s))
    if 'href="https://webautonomos.es"' in liens or 'href="%s"' % p['croise'][0] in liens:
        err.append('lien encore vers une page espagnole')
    if err:
        abandon('%s : %s' % (rel, ' ; '.join(err)))


# ─── remplacements dans le reste du site ─────────────────────────────────────
def remplacements_site():
    r = []
    for urls in (DIAG, VIS):
        for l in LANGS:
            r.append((BASE + urls['es'] + '?lang=' + l, BASE + urls[l]))
            r.append(('"' + urls['es'] + '?lang=' + l, '"' + urls[l]))
            r.append(("'" + urls['es'] + '?lang=' + l, "'" + urls[l]))
    return r


SITEMAP_ANCRE = "    return [v for _, v in sorted(list(roots.items()) + list(dirs.items())\n"
SITEMAP_AJOUT = ("    # Pages FR/EN en dossier (fr/diagnostic-automatisation/index.html…),\n"
                 "    # generees par build_i18n_pages.py : servies sous /fr/<dossier>/.\n"
                 "    for lang in ('fr', 'en'):\n"
                 "        for path in sorted(glob.glob(os.path.join(ROOT, lang, '*', 'index.html'))):\n"
                 "            d = os.path.basename(os.path.dirname(path))\n"
                 "            subs['%s/%s/' % (lang, d)] = ('/%s/%s/' % (lang, d), path)\n\n")


def main():
    check = '--check' in sys.argv
    os.chdir(ROOT)
    ecrire = {}          # rel -> contenu
    rapport = []
    sources = {}
    for p in PAGES:
        s0 = lire(p['src'])
        s, modif = patch_source(p, s0)
        sources[p['src']] = s
        if modif:
            ecrire[p['src']] = s
            rapport.append('  ✓ %-38s hreflang, redirection ?lang=, menu (1re fois)' % p['src'])
    # les copies se construisent sur les sources à jour
    for p in PAGES:
        src = sources[p['src']]
        with tempfile.TemporaryDirectory() as tmp:
            f = os.path.join(tmp, 'src.html')
            open(f, 'w', encoding='utf-8').write(src)
            T = textes(f)
        for lang in LANGS:
            rel = p['urls'][lang].strip('/') + '/index.html'
            s, n = copie(p, src, lang, T)
            controles(rel, s, src, lang, p)
            ecrire[rel] = s
            rapport.append('  ✓ %-38s %3d textes en %s' % (rel, n, lang))
    # liens ?lang=fr / ?lang=en dans le reste du site
    remp = remplacements_site()
    exclus = ('.git', 'node_modules', '.wrangler', 'scripts', '.github')
    candidats = []
    for dp, dn, fn in os.walk(ROOT):
        dn[:] = [d for d in dn if d not in exclus]
        for f in fn:
            rel = os.path.relpath(os.path.join(dp, f), ROOT)
            if rel.endswith('.html') or rel in ('_tools/generate_spa_articles.py', '_tools/build_lang_homes.py', 'llms.txt'):
                candidats.append(rel)
    total = 0
    for rel in sorted(candidats):
        s = ecrire.get(rel) or lire(rel)
        s2 = s
        for a, b in remp:
            s2 = s2.replace(a, b)
        if s2 != s:
            k = sum(s.count(a) for a, _ in remp)
            total += k
            ecrire[rel] = s2
            rapport.append('  ✓ %-38s %3d liens ?lang= remplacés' % (rel, k))
    # sitemap
    sm = lire('_tools/generate_sitemap.py')
    if "glob.glob(os.path.join(ROOT, lang, '*', 'index.html'))" not in sm:
        if sm.count(SITEMAP_ANCRE) != 1:
            abandon('ancre introuvable dans generate_sitemap.py')
        ecrire['_tools/generate_sitemap.py'] = sm.replace(SITEMAP_ANCRE, SITEMAP_AJOUT + SITEMAP_ANCRE)
        rapport.append('  ✓ generate_sitemap.py : pages en dossier sous /fr/ et /en/')
    for rel in ('_tools/generate_sitemap.py', '_tools/generate_spa_articles.py', '_tools/build_lang_homes.py'):
        if rel in ecrire:
            try:
                compile(ecrire[rel], rel, 'exec')
            except SyntaxError as exc:
                abandon('%s invalide : %s' % (rel, exc))
    # rien d'ancien ne doit rester
    for rel, s in ecrire.items():
        for a, _ in remp:
            if a in s:
                abandon('%s : %s subsiste' % (rel, a))
    # écriture (seulement ce qui change réellement)
    ecrire = {r: poser_origine(poser_photo(r, s)) for r, s in ecrire.items()}
    ecrire = {r: s for r, s in ecrire.items() if not os.path.exists(r) or lire(r) != s}
    print('\n'.join(rapport))
    if check:
        print('\n--check : %d fichiers seraient écrits, rien n\'a été modifié.' % len(ecrire))
        return
    if not ecrire:
        print('\nRien à écrire : tout est déjà à jour.')
        return
    stamp = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
    bak = os.path.expanduser('~/webautonomos-work/backups/i18n_pages_%s' % stamp)
    for rel in ecrire:
        if os.path.exists(rel):
            d = os.path.join(bak, rel)
            os.makedirs(os.path.dirname(d), exist_ok=True)
            shutil.copy2(rel, d)
    for rel, s in ecrire.items():
        os.makedirs(os.path.dirname(rel) or '.', exist_ok=True)
        open(rel, 'w', encoding='utf-8').write(s)
    print('\nOK — %d fichiers écrits. Sauvegarde : %s'
          % (len(ecrire), bak.replace(os.path.expanduser('~'), '~')))


if __name__ == '__main__':
    main()
