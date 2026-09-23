# -*- coding: utf-8 -*-
"""Pages métier en français et en anglais (plan SEO FR-EN, phase 2, 24/09/2026).

Une entrée par métier dans METIERS ; chaque métier a une page française
(marché français, francophones d'Espagne en renvoi), une page anglaise
(anglophones installés en Espagne) et une page espagnole existante (/psicologos/…)
avec laquelle elles forment un groupe hreflang.

Premier métier : thérapeutes et psychologues.
  /fr/site-internet-psychologue-therapeute
  /en/website-for-therapists-in-spain
  /psicologos/                               (espagnol, page existante)

Faits juridiques vérifiés le 23-24/09/2026 (sources officielles, voir THERA_SOURCES),
puis relus par une vérification indépendante le 24/09/2026 :
  France  : titre de psychologue (loi 85-772 art. 44, C. pén. 433-17 : 1 an,
            15 000 €) ; bascule ADELI -> RPPS le 3/06/2024 (psychologues) et le
            11/10/2024 (psychothérapeutes) ; psychothérapeute (loi 2004-806
            art. 52, décret 2010-534 : 400 h + 5 mois de stage) ; allégations de
            guérison (C. conso L121-4 16°, L121-2) ; exercice illégal de la
            médecine (CSP L4161-1) ; DGCCRF 2022 : 66 % d'anomalies sur 381
            établissements (praticiens et centres de formation) ; CNIL : motif de consultation = donnée de santé, HDS
            (CSP L1111-8) ; Mon soutien psy : 12 séances/an à 50 €, accès direct
            depuis le 15/06/2024 ; LCEN art. 1-1 et 19.
  Espagne : colegiación obligatoire (loi 43/1979 art. 2) ; LSSI art. 10.1.d
            (colegio, n° de colegiado, titre, pays, homologation) ; psicólogo
            general sanitario (loi 33/2011 DA 7ª) ; centre sanitaire autorisé et
            n° de registre dans la publicité (RD 1277/2003 art. 6.2) ; publicité
            sanitaire, témoignages de patients interdits (RD 1907/1996 art. 4.7,
            art. 5.3) ; diplômes britanniques : procédure pays tiers depuis
            2021 ; intrusismo (C. pén. art. 403) ; AEPD : pas de DPD pour un
            professionnel de santé seul (LOPDGDD art. 34.1.l).

Le script est ré-exécutable : il régénère les pages, et n'applique les
modifications des autres fichiers que si elles manquent encore :
  - hreflang sur la page espagnole du métier ;
  - pages métier espagnoles : note Trustpilot 4,2/6 avis -> 4,3/8 avis ;
  - build_lang_homes.py : tags métier de /fr/ et /en/ liés aux pages métier ;
  - llms.txt : une ligne par page.
Puis il relance build_lang_homes.py et generate_sitemap.py.

Usage (depuis ~/webautonomos) :
    python3 _tools/build_metier_pages.py
    python3 _tools/build_metier_pages.py --check     (vérifie sans écrire)
"""
import datetime
import json
import os
import re
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build_lang_homes as H  # noqa: E402
import build_expat_pages as X  # noqa: E402  (styles, tarifs et avis communs)

BASE, E = H.BASE, H.E
ROOT = H.ROOT


def abandon(msg):
    sys.exit('ABANDON : %s\nRien n\'a été modifié.' % msg)


# ═════════════════════════ THÉRAPEUTES ET PSYCHOLOGUES ═════════════════════
THERA = {}
THERA['fr'] = dict(
    html_lang='fr', og_locale='fr_FR', unit='mois', area=['FR', 'ES'],
    title="Site internet pour psychologue et thérapeute : 15 €/mois",
    description="Site internet pour psychologue, psychothérapeute ou praticien : titre et RPPS, mentions légales, "
                "formulaire sans motif de consultation. Démo gratuite en 24 h, 15 €/mois HT.",
    service_name="Création de site internet pour psychologues et thérapeutes",
    audience="Psychologues, psychothérapeutes et praticiens de l'accompagnement",
    crumb_home='Accueil', crumb='Psychologues et thérapeutes',
    badge='Psychologues, psychothérapeutes et praticiens',
    h1="Un site internet pour <em>psychologues et thérapeutes</em>, prêt en 24 heures",
    lede="Votre site dit qui vous êtes, comment vous travaillez et comment prendre rendez-vous, dans le respect "
         "des règles de votre profession. Nous l'écrivons pour vous et vous envoyons une démo gratuite en 24 heures.",
    pills=['Titre et RPPS bien affichés', 'Formulaire réduit au strict nécessaire', 'Démo gratuite en 24 h'],
    cta='Recevoir ma démo gratuite', cta2='Ce que les règles imposent',
    brief_t='En bref',
    brief="WebAutonomos crée des sites internet pour les psychologues, psychothérapeutes et praticiens "
          "(sophrologues, hypnothérapeutes, praticiens bien-être), en France et en Espagne. Nous rédigeons les "
          "textes à partir de vos informations, affichons votre titre et votre numéro RPPS si vous en avez un, et "
          "prévoyons un formulaire de contact qui ne demande pas le motif de consultation. Le site coûte "
          "<strong>15 € HT par mois</strong> sans frais d'installation ni engagement, ou <strong>349 € HT en "
          "paiement unique</strong>, bilingue sans supplément si vous le souhaitez, et la démo est prête en 24 heures.",
    legal_id='regles', legal_ey='Les règles', legal_t="Ce que votre site doit respecter",
    legal_intro="Les règles changent selon votre titre. Un psychologue n'a pas les contraintes publicitaires d'un "
                "médecin, mais son titre est protégé ; un praticien non réglementé communique librement, sans "
                "jamais promettre de soigner. Voici l'essentiel pour une activité en France.",
    legal_cols=('Qui', 'Texte', 'Ce que ça change sur votre site'),
    legal_rows=[
        ('Psychologue', 'Loi n° 85-772, art. 44 ; Code pénal, art. 433-17',
         "Titre réservé aux titulaires des diplômes requis, qui doivent s'enregistrer auprès de l'ARS. Depuis juin "
         "2024, c'est le numéro RPPS qui vous identifie ; le numéro ADELI n'est plus attribué. Usurper le titre est "
         "puni d'un an de prison et de 15 000 € d'amende. Aucune loi n'impose le RPPS sur le site, mais la LCEN "
         "demande aux professions réglementées d'indiquer leur titre, l'État où il a été obtenu, l'organisme "
         "d'inscription et les règles professionnelles applicables."),
        ('Psychothérapeute', 'Loi n° 2004-806, art. 52 ; décret n° 2010-534',
         "Titre réservé aux professionnels inscrits au registre national des psychothérapeutes (RPPS depuis "
         "octobre 2024). L'inscription exige un doctorat en médecine ou un master de psychologie ou de "
         "psychanalyse, puis 400 heures de formation en psychopathologie clinique et cinq mois de stage, sauf "
         "dispense. Sans cette inscription, le mot « psychothérapeute » ne doit pas figurer sur le site."),
        ('Praticien non réglementé : sophrologue, hypnothérapeute, naturopathe, praticien bien-être',
         'Code de la consommation, art. L121-2 et L121-4 ; Code de la santé publique, art. L4161-1',
         "Le mot « thérapeute » n'est pas protégé. Mais affirmer faussement qu'une prestation guérit une maladie "
         "est une pratique commerciale trompeuse, poser un diagnostic ou traiter une maladie relève de l'exercice "
         "illégal de la médecine, et une formation privée ne se présente pas comme un diplôme d'État. Lors de son "
         "enquête 2020-2021, la DGCCRF a relevé un taux d'anomalie de 66 % parmi les 381 établissements contrôlés "
         "(praticiens et centres de formation)."),
        ('Tous : formulaire et rendez-vous', 'RGPD, art. 5 et 9 ; Code de la santé publique, art. L1111-8',
         "Le motif de consultation est une donnée de santé : mieux vaut ne pas le demander dans le formulaire "
         "(principe de minimisation). Nom, coordonnées et créneau souhaité suffisent. Un outil de réservation qui "
         "stocke des données de santé doit passer par un hébergeur certifié HDS."),
        ('Tous : mentions légales', 'LCEN, art. 1-1 et 19',
         "Nom (suivi de « EI » si vous êtes entrepreneur individuel), adresse, téléphone, e-mail, numéro "
         "d'immatriculation, nom du directeur de la publication, nom, adresse et téléphone de l'hébergeur et, pour "
         "une profession réglementée, votre titre et l'organisme d'inscription."),
    ],
    legal_note="Psychologue, vous pouvez faire de la publicité : l'assouplissement de 2020 concerne les professions "
               "de santé à ordre (médecins, dentistes, sages-femmes, infirmiers, kinés, pédicures-podologues), et "
               "les psychologues ne font pas partie des professions de santé du Code de la santé publique. Le code "
               "de déontologie de 2021, qui n'a pas de valeur réglementaire, demande de communiquer « avec mesure ». "
               "Informations générales à jour en septembre 2026, qui ne remplacent pas un conseil juridique : en cas "
               "de doute sur votre titre, interrogez votre ARS.",
    legal_we_t='Ce que nous mettons en place',
    legal_we=["Votre titre, votre numéro RPPS et votre organisme d'inscription affichés clairement, si vous êtes "
              "psychologue ou psychothérapeute",
              "Des textes sans promesse de guérison, rédigés à partir de votre approche et de votre parcours",
              "Un formulaire sans champ « motif de consultation », avec un rappel de ne pas y décrire sa situation",
              "Un lien vers votre outil de rendez-vous (Doctolib, Calendly ou autre) plutôt qu'une collecte de "
              "données sur le site",
              "Mentions légales, politique de confidentialité et gestion des cookies rédigées avec vos données"],
    spain_note="<strong>Vous exercez en Espagne ?</strong> Les règles changent : un psychologue doit être inscrit à "
               "un Colegio et afficher son numéro de colegiado sur son site, et un cabinet de psychologie de la santé "
               "doit être autorisé comme centre sanitaire. Nous connaissons aussi ces règles : "
               "<a href=\"/fr/site-internet-francophones-espagne\">site internet pour francophones en Espagne</a>.",
    sources_t='Sources',
    why_ey='Pourquoi nous', why_t="Pensé pour les métiers de l'accompagnement",
    why=[('🤫', "La discrétion d'abord", "Un formulaire réduit au strict nécessaire, sans motif de consultation ni "
                                        "question sur la santé, et un site entièrement en https."),
         ('📅', 'Rendez-vous en deux clics', "Un bouton vers votre agenda en ligne, WhatsApp ou le téléphone : la "
                                            "personne choisit ce qui la met à l'aise."),
         ('💻', 'Cabinet ou visio', "Séances au cabinet, en ligne ou les deux : c'est écrit clairement, avec vos "
                                   "tarifs si vous le souhaitez."),
         ('📍', 'Trouvé près de chez vous', "Titres et textes pensés pour les recherches « psychologue + votre "
                                           "ville », et votre fiche Google si vous le souhaitez.")],
    where_t='En France et en Espagne',
    where="Nous travaillons à distance, en français, par e-mail, WhatsApp et visioconférence : que votre cabinet "
          "soit à Nantes, à Lyon ou à Valence, rien ne change.",
    sect_t='Pour qui',
    sectors=['🧠 Psychologues', '🗣️ Psychothérapeutes', '🛋️ Psychanalystes', '🌬️ Sophrologues',
             '🌀 Hypnothérapeutes', '🌿 Naturopathes', '💆 Praticiens bien-être', '🧭 Coachs'],
    how_t='Votre site en trois étapes',
    steps=[('Vous décrivez votre pratique', "Votre titre, votre approche, cabinet ou visio, votre ville : deux "
                                           "minutes suffisent."),
           ('Nous préparons votre démo', "En moins de 24 heures, avec vos textes, vos photos si vous en avez et "
                                        "vos mentions légales."),
           ('Vous décidez', "Vous demandez les modifications que vous voulez. Si le site vous plaît, il est mis en "
                           "ligne ; sinon, vous ne payez rien.")],
    price_note="Prix hors taxes. En France, nous facturons sans TVA : vous déclarez vous-même la TVA française de "
               "20 % (autoliquidation), que les psychologues, exonérés, et les praticiens en franchise en base ne "
               "récupèrent pas. En Espagne, l'IVA de 21 % s'ajoute. Nom de domaine inclus la première année, puis "
               "environ 12 €/an.",
    faq_t='Questions fréquentes',
    faq=[("Un psychologue doit-il afficher son numéro RPPS sur son site ?",
          "Aucune loi ne l'impose expressément sur un site, mais c'est recommandé. La LCEN (art. 19) demande aux "
          "professions réglementées d'indiquer leur titre, l'État où il a été obtenu, l'organisme d'inscription et "
          "les règles professionnelles applicables. Et selon la Miviludes, sur 2022-2024, plus de 20 % des "
          "« psychologues » qui lui ont été signalés n'avaient aucun numéro RPPS identifiable. L'afficher permet à "
          "chacun de vous vérifier sur l'Annuaire santé."),
         ("Mon numéro ADELI est-il encore valable ?",
          "Il n'est plus attribué. Les psychologues ont basculé dans le répertoire RPPS le 3 juin 2024, les "
          "psychothérapeutes le 11 octobre 2024. C'est le numéro RPPS qu'il faut afficher."),
         ("Un sophrologue ou un hypnothérapeute peut-il se présenter comme thérapeute ?",
          "Le mot « thérapeute » n'est pas protégé, contrairement à « psychologue » et « psychothérapeute ». Il est "
          "en revanche interdit d'affirmer faussement qu'une prestation guérit une maladie (Code de la consommation, art. "
          "L121-4) et de poser un diagnostic ou de traiter une maladie (Code de la santé publique, art. L4161-1). "
          "Nous rédigeons vos textes en conséquence : ce que vous proposez et comment se passe une séance, sans "
          "promesse de résultat médical."),
         ("Puis-je demander le motif de consultation dans le formulaire de contact ?",
          "Mieux vaut pas. Le motif de consultation est une donnée de santé, et le RGPD impose de ne collecter que "
          "les données nécessaires : pour prendre rendez-vous, il n'est en général pas utile. Un outil qui stocke des "
          "données de santé pour vous doit passer par un hébergeur certifié HDS. Nos formulaires demandent seulement le nom, les "
          "coordonnées et le créneau souhaité."),
         ("Puis-je indiquer que je suis conventionné Mon soutien psy ?",
          "Nous n'avons trouvé aucune règle qui l'interdise ; veillez simplement à ce que ce soit exact. C'est un "
          "vrai critère de choix : depuis le 15 juin 2024, les patients peuvent vous consulter sans passer par un "
          "médecin, pour 12 séances par an au plus (sauf exceptions depuis juin 2026), à 50 € la séance, prises en "
          "charge à 60 % par l'Assurance maladie."),
         ("Un psychologue a-t-il le droit de faire de la publicité ?",
          "Oui. Les psychologues ne font pas partie des professions de santé du Code de la santé publique et ne sont "
          "pas soumis aux règles de publicité des professions de santé à ordre. Le code de déontologie de 2021, qui n'a pas de valeur réglementaire, "
          "demande de communiquer « avec mesure » et en référence à son titre : un site clair et factuel répond à "
          "cette exigence."),
         ("Combien coûte un site pour psychologue ou thérapeute ?",
          "15 € HT par mois sans frais d'installation ni engagement, ou 349 € HT en paiement unique, avec les mêmes "
          "services : conception, hébergement, nom de domaine la première année, mentions légales et une "
          "modification par mois. La démo est gratuite."),
         ("J'exerce en Espagne : les règles sont-elles les mêmes ?",
          "Non. En Espagne, un psychologue doit être inscrit à un Colegio et afficher son numéro de colegiado sur "
          "son site (LSSI, art. 10), et un cabinet de psychologie de la santé doit être autorisé comme centre "
          "sanitaire par sa communauté autonome, avec son numéro d'enregistrement dans sa publicité. Nous créons "
          "aussi des sites pour les francophones installés en Espagne.")],
    final_t='Voyez votre site avant de payer quoi que ce soit',
    final_sd="Démo gratuite en 24 heures, textes et mentions légales compris. Sans frais d'installation, sans "
             "engagement.",
)

THERA['en'] = dict(
    html_lang='en', og_locale='en_GB', unit='month', area=['ES'],
    title="Websites for therapists and psychologists in Spain: €15/month",
    description="Websites for English-speaking therapists, counsellors and psychologists in Spain, built around "
                "Spanish rules. Free demo in 24h, €15/month + VAT.",
    service_name="Web design for therapists and psychologists in Spain",
    audience="English-speaking therapists, counsellors and psychologists in Spain",
    crumb_home='Home', crumb='Therapists and psychologists',
    badge='For therapists, counsellors and psychologists in Spain',
    h1="Websites for <em>therapists and psychologists</em> in Spain",
    lede="Your website should say who you are, how you work and how to book, in English, while following Spanish "
         "rules on titles, health advertising and data. We write it for you and send you a free demo within 24 hours.",
    pills=['Spanish rules built in', 'We work in English', 'Free demo in 24 hours'],
    cta='Get my free demo', cta2='What Spanish rules require',
    brief_t='In short',
    brief="WebAutonomos builds websites for English-speaking psychologists, psychotherapists, counsellors, "
          "hypnotherapists and coaches practising in Spain. We write the copy from your information, show your "
          "Colegio and colegiado number if you are a psychologist, keep health claims and patient testimonials off "
          "the site, and use a contact form that doesn't ask for health details. It costs <strong>€15 + VAT per "
          "month</strong> with no setup fee and no lock-in, or a <strong>one-off €349 + VAT</strong>, in English "
          "and Spanish at no extra cost. We work with you in English, and your demo is ready within 24 hours.",
    legal_id='rules', legal_ey='Spanish rules', legal_t='What your website has to get right in Spain',
    legal_intro="In Spain, what you may say online depends on your title. A health psychologist is a regulated "
                "health professional; a counsellor or coach is not, and must not present their work as health "
                "care. These are the points that matter for a website.",
    legal_cols=('Who', 'Law', 'What it means for your website'),
    legal_rows=[
        ('Psychologist (psicólogo)', 'Ley 43/1979, art. 2; LSSI (Ley 34/2002), art. 10',
         "Membership of a Colegio Oficial de Psicólogos is compulsory to practise. Your website must show your "
         "Colegio and colegiado number, your official qualification, the country that issued it and, where it "
         "applies, its recognition in Spain, plus the professional rules that apply to you (such as your "
         "Colegio's code of ethics) and where to read them."),
        ('Health psychologist (psicólogo general sanitario)', 'Ley 33/2011, DA 7ª; RD 1277/2003, art. 6.2',
         "Health work requires the Máster en Psicología General Sanitaria (or the clinical specialist title) and a "
         "practice authorised by your regional health department. Any advertising that suggests health care, your "
         "website included, must show the registration number the region gives your practice."),
        ('Psychologist with a foreign degree', 'RD 581/2017; RD 889/2022; Código Penal, art. 403',
         "An EU qualification is recognised by the Ministry of Health; a non-EU one, including a UK one since 2021, "
         "must be homologated to the Máster en Psicología General Sanitaria by the Ministry of Science, Innovation "
         "and Universities (a bachelor's degree alone can't be). Practising as a psychologist without a title "
         "recognised in Spain is a criminal offence, and calling yourself one publicly makes it more serious."),
        ('Counsellor, coach, hypnotherapist', 'RD 1907/1996, art. 4 and 5.3; RD 1277/2003, art. 6.2',
         "These titles are not regulated, but your site can't present your work as health care: no promise of "
         "relief or cure, no claim to treat a condition, no patient testimonials used to attract clients. These "
         "bans also apply to anyone who presents their work as health-related."),
        ('Everyone: contact forms', 'GDPR, art. 5 and 9; LOPDGDD, art. 34',
         "Why someone wants to see you is health data. Your form should ask only for a name, contact details and "
         "a preferred time. A psychologist working alone doesn't need a data protection officer."),
    ],
    legal_note="Testimonials deserve a special mention: Spanish health-advertising rules ban patient testimonials "
               "used to attract clients (RD 1907/1996, art. 4.7). For a health practice, we build trust with your "
               "qualifications, your approach and practical details instead. This is general information as of "
               "September 2026, not legal advice: check with your Colegio and your regional health department.",
    legal_we_t='What we set up for you',
    legal_we=["Your Colegio, colegiado number, qualification and a link to your code of ethics shown clearly if "
              "you are a psychologist, plus the practice registration number and health authorisation details where "
              "they apply",
              "Copy written without health promises, patient testimonials or titles you don't hold",
              "A contact form with no 'reason for consultation' field, and a note asking people not to share health "
              "details",
              "A link to your booking tool, WhatsApp or phone, rather than collecting data on the site",
              "Legal notice, privacy and cookie policy written with your details, as for every business website "
              "in Spain"],
    spain_note='',
    sources_t='Sources',
    why_ey='Why us', why_t='Built for therapists who work in English',
    why=[('💬', 'We speak your language', "Email, WhatsApp or video call in English: no need to decode Spanish "
                                         "legal or technical jargon."),
         ('🤫', 'Discreet by design', "A contact form that asks only what it needs, with no health questions, "
                                     "and https across the whole site."),
         ('📅', 'Easy to book', "A clear button to your online calendar, WhatsApp or phone, with in-person or "
                               "online sessions stated plainly."),
         ('📍', 'Found by English speakers', "Titles and copy written for searches like “English-speaking "
                                            "therapist in Alicante” or “counsellor Valencia”.")],
    where_t='Anywhere in Spain',
    where="Costa Blanca, Valencia, Costa del Sol, Barcelona, Madrid, the Balearic or the Canary Islands: we work "
          "remotely, so where your practice is makes no difference.",
    sect_t='Who it is for',
    sectors=['🧠 Psychologists', '🗣️ Psychotherapists', '💬 Counsellors', '🌀 Hypnotherapists', '🧭 Coaches',
             '🌿 Wellbeing practitioners', '🧘 Yoga and meditation teachers', '🌱 Personal growth'],
    how_t='Your website in three steps',
    steps=[('Tell us about your practice', 'Your title, your approach, in person or online, your town: it takes '
                                           'two minutes.'),
           ('We build your demo', 'Within 24 hours, with your copy, your photos if you have some, and your legal '
                                  'pages.'),
           ('You decide', "Ask for any changes you want. If you like it, it goes live; if not, you pay nothing.")],
    price_note="Prices exclude VAT (21% IVA on the mainland and the Balearics; the Canary Islands, Ceuta and Melilla "
               "have their own taxes). Psychologists' health services are VAT-exempt, so they usually can't deduct "
               "it: on the mainland and the Balearics the monthly price comes to €18.15. Domain name included for "
               "the first year, then about €12/year.",
    faq_t='Frequently asked questions',
    faq=[("Can I call myself a psychologist in Spain with a UK degree?",
          "Only once it is recognised. Since 1 January 2021, UK qualifications follow the procedure for non-EU "
          "countries: homologation to the Máster en Psicología General Sanitaria by the Ministry of Science, "
          "Innovation and Universities, which requires a bachelor's and a master's degree (at least 300 ECTS) and "
          "Spanish at B2 level. Recognitions granted before 2021 keep their effect. Until then, describe your "
          "degree factually: practising as a psychologist without a title recognised in Spain is a criminal "
          "offence (Criminal Code, art. 403), and publicly calling yourself a psychologist raises the penalty to "
          "six months to two years in prison."),
         ("Do I need to show my colegiado number on my website?",
          "Yes, if you are a psychologist. Article 10 of the LSSI requires regulated professionals to show their "
          "Colegio, colegiado number, official qualification, the country that issued it and the professional "
          "rules that apply to them on their website. A health practice must also give its health authorisation "
          "details and the authority that supervises it."),
         ("Does my practice need to be registered as a health centre?",
          "For health psychology, yes: a private practice needs prior authorisation from the regional health "
          "department and goes on the regional register (RD 1277/2003). Its registration number must appear in any "
          "advertising that suggests health care, including your website. The rules for online-only practice are "
          "less clear, so check with your region."),
         ("Can a counsellor or coach offer therapy in Spain?",
          "Counsellor, coach and hypnotherapist are not regulated titles in Spain. You can offer support and "
          "personal development, but not health care: no diagnosis, no treatment of conditions, no promise of "
          "relief or cure, and no use of 'psychologist'. Spain's Ministry of Health has also classed some "
          "techniques, such as Ericksonian hypnosis, as pseudotherapies when they are offered for a health purpose."),
         ("Can I show client testimonials on my website?",
          "For a health practice, avoid them: Spanish health-advertising rules ban patient testimonials used to "
          "attract clients (RD 1907/1996, art. 4.7), and the ban extends to anyone who presents their work as health "
          "care. We build trust with your qualifications, your approach and practical details instead."),
         ("Does my website have to be in Spanish?",
          "No law requires the whole site in Spanish. Spanish consumer law does require pre-contract information, "
          "such as prices and terms, to be given at least in Spanish, and Madrid applies this to all information "
          "for consumers. In Catalonia, documents offering your services must also be available at least in "
          "Catalan. A short Spanish version of your prices and terms is the safe choice, and we build your site "
          "in English and Spanish at no extra cost."),
         ("What should my contact form ask?",
          "A name, a way to reach the person and a preferred time. Not the reason for the consultation: that is "
          "health data under the GDPR, and data should be limited to what is necessary. We add a short note asking "
          "people not to share health details in the form."),
         ("How much does a website cost?",
          "€15 + VAT a month with no setup fee and no lock-in, or a one-off €349 + VAT, with the same services: "
          "design, hosting, a domain name for the first year, legal pages and one change a month. The demo is "
          "free.")],
    final_t='See your website before you pay a thing',
    final_sd="Free demo within 24 hours, copy and legal pages included. No setup fee, no lock-in.",
)

THERA_SOURCES = {
    'fr': [
        ("Loi n° 85-772, art. 44 (Légifrance)", 'https://www.legifrance.gouv.fr/loda/article_lc/LEGIARTI000033678864'),
        ("Bascule ADELI vers RPPS (Agence du numérique en santé)",
         'https://esante.gouv.fr/offres-services/annuaire-sante/bascule-des-professionnels-adeli-dans-le-rpps'),
        ("Loi n° 2004-806, art. 52 (Légifrance)", 'https://www.legifrance.gouv.fr/loda/article_lc/LEGIARTI000031930044'),
        ("DGCCRF, enquête sur les pratiques de soins non conventionnelles (2020-2021, publiée en 2022)",
         'https://www.economie.gouv.fr/dgccrf/laction-de-la-dgccrf/les-enquetes/attention-aux-risques-des-pratiques-de-soins-non'),
        ("DGCCRF, fiche pratique sur les soins non conventionnels (2026)",
         'https://www.economie.gouv.fr/dgccrf/les-fiches-pratiques/pratiques-de-soins-non-conventionnelles-soyez-attentif-aux-informations-fournies'),
        ("CNIL, qu'est-ce qu'une donnée de santé ?", 'https://www.cnil.fr/fr/quest-ce-ce-quune-donnee-de-sante'),
        ("Mon soutien psy (ameli.fr)",
         'https://www.ameli.fr/assure/remboursements/rembourse/remboursement-seance-psychologue-mon-soutien-psy'),
    ],
    'en': [
        ("LSSI, art. 10 (BOE)", 'https://www.boe.es/buscar/act.php?id=BOE-A-2002-13758'),
        ("Ley 33/2011, DA 7ª (BOE)", 'https://www.boe.es/buscar/act.php?id=BOE-A-2011-15623'),
        ("RD 1277/2003 (BOE)", 'https://www.boe.es/buscar/act.php?id=BOE-A-2003-19572'),
        ("RD 1907/1996 on health advertising (BOE)", 'https://www.boe.es/buscar/act.php?id=BOE-A-1996-18085'),
        ("Recognition of psychology degrees (Ministry of Science, Innovation and Universities)",
         'https://www.ciencia.gob.es/Universidades/validate/homologacion/psicologo.html'),
        ("AEPD guide for health professionals", 'https://www.aepd.es/guias/guia-profesionales-sector-sanitario.pdf'),
    ],
}

METIERS = {
    'therapeutes': dict(
        es='/psicologos/',
        fr='/fr/site-internet-psychologue-therapeute',
        en='/en/website-for-therapists-in-spain',
        C=THERA, SOURCES=THERA_SOURCES,
        # avis des métiers proches en premier
        avis_ordre=['Sabine O.', 'Ana Saiz', 'Analía', 'Begoña Cid', 'Inés', 'Fabiana', 'Amelle B.', 'Lee Robinson'],
        llms={'fr': ("- [Site internet pour francophones en Espagne](https://webautonomos.es/fr/site-internet-francophones-espagne)",
                     "Site internet pour psychologues et thérapeutes"),
              'en': ("- [Web design for expats in Spain](https://webautonomos.es/en/web-design-for-expats-in-spain)",
                     "Websites for therapists and psychologists in Spain")},
        tags={'fr': ['🧠 Psychologues', '🌿 Thérapeutes bien-être'],
              'en': ['🧠 Psychologists', '🌿 Wellbeing practitioners']},
    ),
}

CSS_METIER = """
/* ─── pages métier (build_metier_pages.py) ─── */
.spain-note { max-width:760px; margin:18px auto 0; background:var(--off); border:1.5px solid var(--border); border-radius:12px; padding:14px 18px; font-size:.93rem; color:#334155; line-height:1.6; }
.spain-note a { color:var(--blue); font-weight:600; }
"""


def trier_avis(lang, ordre):
    avis = list(H.AVIS[lang])
    rang = lambda a: next((n for n, p in enumerate(ordre) if a[1].startswith(p)), len(ordre))
    return sorted(avis, key=rang)


def page(m, lang):
    M = METIERS[m]
    c, u, src, i = M['C'][lang], H.URLS[lang], H.source(lang), H.IDS[lang]
    x = X.C[lang]   # tarifs, avis : textes communs avec les pages expatriés
    L = lambda k: BASE + u[k]
    url = BASE + M[lang]
    demo = L('demo') + '#pide-demo'
    home = L('home')
    autre = 'en' if lang == 'fr' else 'fr'
    langs = [('es', 'ES', BASE + M['es']), ('fr', 'FR', BASE + M['fr']), ('en', 'EN', BASE + M['en'])]
    nav_links = ''.join('<a href="%s">%s</a>' % (L(k), E(t)) for k, t in H.C[lang]['nav'])
    lang_links = ''.join('<a href="%s" hreflang="%s" lang="%s"%s>%s</a>' % (
        h, code, code, ' aria-current="page"' if code == lang else '', lab) for code, lab, h in langs)
    pills = ''.join('<span class="pill">✓ %s</span>' % E(p) for p in c['pills'])
    rows = ''.join('<tr><th scope="row">%s</th><td class="law">%s</td><td>%s</td></tr>' % (E(a), E(b), E(d))
                   for a, b, d in c['legal_rows'])
    we = ''.join('<li><span>%s</span></li>' % E(t) for t in c['legal_we'])
    srcs = ' · '.join('<a href="%s" rel="noopener" target="_blank">%s</a>' % (h, E(t)) for t, h in M['SOURCES'][lang])
    spain = '<p class="spain-note">%s</p>' % c['spain_note'] if c['spain_note'] else ''
    why = ''.join('<div class="aud-c"><div class="aud-i" aria-hidden="true">%s</div><h3>%s</h3><p>%s</p></div>'
                  % (ic, E(t), E(d)) for ic, t, d in c['why'])
    sectors = ''.join('<span class="stag">%s</span>' % E(s) for s in c['sectors'])
    steps = ''.join('<div class="step%s"><div class="sn">%d</div><div class="stit">%s</div><div class="sinf">%s</div></div>'
                    % (' ft' if n == 1 else '', n + 1, E(t), E(d)) for n, (t, d) in enumerate(c['steps']))
    plans = ''
    for p in x['plans']:
        plans += ('<div class="pc%s">%s<div class="pc-n">%s</div><div class="pc-a">%s</div>'
                  '<div class="pc-p">%s</div><ul>%s</ul></div>') % (
            ' hl' if p['hl'] else '', '<span class="pc-b">%s</span>' % E(p['badge']) if p['badge'] else '',
            E(p['name']), E(p['amt']), E(p['per']), ''.join('<li>%s</li>' % E(t) for t in p['pts']))
    slides, dots = '', ''
    for n, (txt, who, tr) in enumerate(trier_avis(lang, M['avis_ordre'])):
        slides += ('<div class="tp-slide"><div class="tp-card"><div class="tp-stars" aria-hidden="true">★★★★★</div>'
                   '<blockquote>« %s »</blockquote><div class="tp-who">— %s%s</div></div></div>') % (
            E(txt), E(who), '<span class="tp-tr">%s</span>' % E(tr) if tr else '')
        dots += '<button class="tp-dot%s" onclick="tpGo(%d)" aria-label="%s %d"></button>' % (
            ' on' if n == 0 else '', n, E(x['rev_aria']), n + 1)
    faq = ''.join('<details><summary>%s</summary><p>%s</p></details>' % (E(q), E(a)) for q, a in c['faq'])
    hreflang = '\n'.join('<link rel="alternate" hreflang="%s" href="%s%s">' % (h, BASE, M[k]) for h, k in
                         (('es-ES', 'es'), ('fr', 'fr'), ('en', 'en'), ('x-default', 'es')))
    jc = dict(title=c['title'], description=c['description'], html_lang=c['html_lang'],
              service_name=c['service_name'], area=c['area'], plans=x['plans'], unit=c['unit'], faq=c['faq'])
    g = json.loads(H.jsonld(lang, jc, dict(home=M[lang])))
    for n in g['@graph']:
        if n.get('@type') == 'Service':
            n['audience'] = {"@type": "Audience", "audienceType": c['audience']}
    g['@graph'].append({"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": c['crumb_home'], "item": home},
        {"@type": "ListItem", "position": 2, "name": c['crumb'], "item": url}]})
    ld = json.dumps(g, ensure_ascii=False, indent=1)
    wa = re.sub(r'href="https://wa\.me/[^"]*"', 'href="https://wa.me/%s?text=%s"' % (
        H.WHATSAPP, re.sub(r'[^A-Za-z0-9]', lambda mm: ''.join('%%%02X' % b for b in mm.group(0).encode()),
                           H.C[lang]['wa_text'])), src['float_wa'])
    legal_js = "event.preventDefault();document.getElementById('%s').style.display='flex'"
    foot_langs = '<a href="%s%s" hreflang="%s">%s</a>' % (BASE, M[autre], autre, autre.upper())

    return f"""<!DOCTYPE html>
<html lang="{c['html_lang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<!-- Page générée par _tools/build_metier_pages.py : ne pas modifier à la main, relancer le script. -->
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
<style>{src['css']}{H.EXTRA_CSS}{X.CSS_PAGE}{CSS_METIER}</style>
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
    {spain}
    <div class="legal-we"><h3>{E(c['legal_we_t'])}</h3><ul>{we}</ul></div>
    <p class="srcs">{E(c['sources_t'])} : {srcs}</p>
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
  <a class="p-link" href="{L('tarifs')}">{E(x['price_link'])} →</a>
</section>

<section class="secs" id="{i['sect']}">
  <h2 style="margin-bottom:24px">{E(c['sect_t'])}</h2>
  <div class="sg">{sectors}</div>
</section>

<section class="proof" id="{i['rev']}">
  <h2>{E(x['rev_t'])}</h2>
  <div class="tp">
    <div class="tp-head"><span class="tp-score">{'4,3' if lang == 'fr' else '4.3'}</span><span class="tp-of">/ 5</span><span class="tp-count">{E(x['rev_count'])}</span></div>
    <div class="tp-view"><div class="tp-track" id="tpTrack">{slides}</div></div>
    <div class="tp-dots" id="tpDots">{dots}</div>
    <a class="tp-link" href="{H.TRUSTPILOT}" target="_blank" rel="noopener noreferrer">{E(x['rev_link'])} →</a>
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
"""


# ═════════════════════════ AUTRES FICHIERS (une seule fois) ════════════════
NOTE_ES = [('<div class="proof-num">4,2★</div>', '<div class="proof-num">4,3★</div>'),
           ('<div class="proof-label">Valoración media sobre<br>6 opiniones en Trustpilot</div>',
            '<div class="proof-label">Valoración media sobre<br>8 opiniones en Trustpilot</div>')]
PAGES_ES = ['psicologos', 'dentistas', 'fisioterapeutas', 'electricistas', 'fontaneros', 'carpinteros', 'reformas']

HOMES = '_tools/build_lang_homes.py'
HOMES_CODE = [
    ("    sectors = ''.join('<span class=\"stag\">%s</span>' % E(s) for s in c['sectors'])",
     "    # tags liés à une page métier (build_metier_pages.py, 24/09/2026)\n"
     "    sectors = ''.join('<a class=\"stag\" href=\"%s%s\">%s</a>' % (BASE, SECTOR_LINKS[lang][s], E(s))\n"
     "                      if s in SECTOR_LINKS.get(lang, {}) else '<span class=\"stag\">%s</span>' % E(s)\n"
     "                      for s in c['sectors'])"),
    ("\nIDS = {",
     "\n# Tags métier de /fr/ et /en/ qui mènent vers une page métier.\n"
     "# Tenu à jour par _tools/build_metier_pages.py.\n"
     "SECTOR_LINKS = {'fr': {}, 'en': {}}\n\nIDS = {"),
    (".cmp-more a { color:var(--blue); font-weight:600; text-decoration:none; }",
     ".cmp-more a { color:var(--blue); font-weight:600; text-decoration:none; }\n"
     "a.stag { text-decoration:none; }\n"
     "a.stag:hover { border-color:var(--green-mid); }"),
]


def maj_homes(s):
    """Installe SECTOR_LINKS si besoin, puis y met les tags de chaque métier."""
    if 'SECTOR_LINKS' not in s:
        for a, b in HOMES_CODE:
            if s.count(a) != 1:
                abandon('%s : ancre trouvée %dx : %s' % (HOMES, s.count(a), a.strip()[:70]))
            s = s.replace(a, b)
    liens = {'fr': {}, 'en': {}}
    for M in METIERS.values():
        for lang in ('fr', 'en'):
            for t in M['tags'][lang]:
                if t not in H.C[lang]['sectors']:
                    abandon('tag « %s » absent des métiers de /%s/.' % (t, lang))
                liens[lang][t] = M[lang]
    ligne = 'SECTOR_LINKS = %s\n' % json.dumps(liens, ensure_ascii=False)
    s2, n = re.subn(r'^SECTOR_LINKS = .*\n', lambda _: ligne, s, count=1, flags=re.M)
    if n != 1:
        abandon('%s : ligne SECTOR_LINKS introuvable.' % HOMES)
    return s2


def main():
    check = '--check' in sys.argv
    os.chdir(ROOT)
    ecrits, modifs = {}, {}
    for m, M in METIERS.items():
        for lang in ('fr', 'en'):
            s = page(m, lang)
            H.controles('%s/%s' % (m, lang), s)
            ecrits[M[lang].lstrip('/') + '.html'] = s
        # hreflang sur la page espagnole du métier
        rel = M['es'].strip('/') + '/index.html'
        es = modifs.get(rel) or open(rel, encoding='utf-8').read()
        canon = '<link rel="canonical" href="%s%s">' % (BASE, M['es'])
        bloc = '\n'.join('<link rel="alternate" hreflang="%s" href="%s%s">' % (h, BASE, M[k]) for h, k in
                         (('es-ES', 'es'), ('fr', 'fr'), ('en', 'en'), ('x-default', 'es')))
        if bloc not in es:
            if 'hreflang=' in es.split('</head>')[0]:
                abandon('%s : des hreflang différents existent déjà, à vérifier à la main.' % rel)
            if es.count(canon) != 1:
                abandon('%s : canonical introuvable.' % rel)
            modifs[rel] = es.replace(canon, canon + '\n' + bloc)
    # note Trustpilot des pages métier espagnoles
    for p in PAGES_ES:
        rel = p + '/index.html'
        s = modifs.get(rel) or open(rel, encoding='utf-8').read()
        s2 = s
        for a, b in NOTE_ES:
            if s2.count(a) == 1:
                s2 = s2.replace(a, b)
            elif s2.count(b) != 1:
                abandon('%s : note Trustpilot introuvable (%s).' % (rel, a[:40]))
        if s2 != s:
            modifs[rel] = s2
    # générateur des accueils
    homes = open(HOMES, encoding='utf-8').read()
    homes2 = maj_homes(homes)
    if homes2 != homes:
        try:
            compile(homes2, HOMES, 'exec')
        except SyntaxError as exc:
            abandon('build_lang_homes.py invalide après modification : %s' % exc)
        modifs[HOMES] = homes2
    # llms.txt
    llms = open('llms.txt', encoding='utf-8').read()
    neuf = llms
    for m, M in METIERS.items():
        for lang in ('fr', 'en'):
            ancre, titre = M['llms'][lang]
            ligne = '- [%s](%s%s)' % (titre, BASE, M[lang])
            if ligne not in neuf:
                if neuf.count(ancre + '\n') != 1:
                    abandon('llms.txt : ancre introuvable : %s' % ancre[:60])
                neuf = neuf.replace(ancre + '\n', ancre + '\n' + ligne + '\n')
    if neuf != llms:
        modifs['llms.txt'] = neuf

    if check:
        for rel, s in ecrits.items():
            print('  ✓ %s valide (%d octets) — non écrit' % (rel, len(s.encode())))
        for rel in modifs:
            print('  ✓ %s à modifier — non écrit' % rel)
        return

    if modifs:
        stamp = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
        bak = os.path.expanduser('~/webautonomos-work/backups/metier_pages_%s' % stamp)
        for rel in modifs:
            d = os.path.join(bak, rel)
            os.makedirs(os.path.dirname(d), exist_ok=True)
            shutil.copy2(rel, d)
    for rel, s in list(ecrits.items()) + list(modifs.items()):
        open(rel, 'w', encoding='utf-8').write(s)
    for rel, s in ecrits.items():
        print('  ✓ %s écrit (%d octets)' % (rel, len(s.encode())))
    for rel in modifs:
        print('  ✓ %s modifié' % rel)
    if modifs:
        print('Sauvegarde : %s' % bak.replace(os.path.expanduser('~'), '~'))
    print()
    for script in ('_tools/build_lang_homes.py', '_tools/generate_sitemap.py'):
        print('→ %s' % script)
        r = subprocess.run([sys.executable, script], cwd=ROOT)
        if r.returncode:
            sys.exit('ÉCHEC de %s : les pages sont écrites, relance-le à la main après correction.' % script)
    print('\nOK — étape suivante : npx wrangler deploy')


if __name__ == '__main__':
    main()
