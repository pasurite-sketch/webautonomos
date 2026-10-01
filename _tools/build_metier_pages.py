# -*- coding: utf-8 -*-
"""Pages métier en français et en anglais (plan SEO FR-EN, phase 2, 24/09/2026).

Une entrée par métier dans METIERS ; chaque métier a une page française
(marché français, francophones d'Espagne en renvoi), une page anglaise
(anglophones installés en Espagne) et une page espagnole existante (/psicologos/…)
avec laquelle elles forment un groupe hreflang.

Métiers :
  thérapeutes et psychologues (24/09/2026)
    /fr/site-internet-psychologue-therapeute
    /en/website-for-therapists-in-spain
    /psicologos/                               (espagnol, page existante)
  menuisiers et carpenters (24/09/2026)
    /fr/site-internet-menuisier                règles françaises : titre d'artisan,
                                               décennale, RGE, encart France Rénov'
                                               (1/10/2026), médiateur, dépannage
    /en/website-for-carpenters-in-spain        règles espagnoles : LSSI, devis écrits
                                               régionaux, réclamations (15 jours),
                                               IVA 10 %, avis (30 jours), langue, REA
    /carpinteros/                              (espagnol, page existante)
  kinésithérapeutes et physiotherapists (24/09/2026)
    /fr/site-internet-kinesitherapeute         règles françaises : référencement
                                               prioritaire interdit (R4321-123),
                                               honoraires sur le site (R4321-98),
                                               RPPS, spécificités reconnues, accès direct
    /en/website-for-physiotherapists-in-spain  règles espagnoles : colegiación, LSSI,
                                               autorisation sanitaire U.59 et n° de
                                               registre, RD 1907/1996, code du CGCFE
    /fisioterapeutas/                          (espagnol, page existante)
  chirurgiens-dentistes et dentists (24/09/2026)
    /fr/site-internet-dentiste                 règles françaises : référencement
                                               prioritaire interdit (R4127-217),
                                               honoraires (R4127-240), spécialités et
                                               formules ONCD, devis, centres de santé
    /en/website-for-dentists-in-spain          règles espagnoles : n° de registre C.2.5.1,
                                               pas de « especialista », marques de
                                               dispositifs interdites (RD 1591/2009),
                                               prix complets et TAE du financement
    /dentistas/                                (espagnol, page existante)
  plombiers et plumbers (28/09/2026)
    /fr/site-internet-plombier                 règles françaises : tarifs de dépannage et
                                               devis (arrêté du 24/01/2017), urgence
                                               (L221-10, L221-28), logos officiels
                                               (CPI L731-2), aides PAC (décret 2026-822),
                                               encart France Rénov', gaz, fluides, entretien
    /en/website-for-plumbers-in-spain          règles espagnoles : RITE, gaz (RD 919/2006),
                                               gaz fluorés (RD 115/2017), fontanería
                                               régionale, urgences (TRLGDCU art. 103),
                                               RD 58/1988
    /fontaneros/                               (espagnol, page existante)
  électriciens et electricians (28/09/2026)
    /fr/site-internet-electricien              règles françaises : dépannage, qualification
                                               (C. artisanat L121-1), Consuel (D342-19),
                                               IRVE (D353-2), photovoltaïque (S21, TVA
                                               5,5 %), diagnostic (CCH L271-6)
    /en/website-for-electricians-in-spain      règles espagnoles : empresa instaladora
                                               (REBT, ITC-BT-03, RD 770/2025), boletín,
                                               bornes (ITC-BT-52, LPH 17.5), autoconsumo,
                                               diplômes britanniques
    /electricistas/                            (espagnol, page existante)
  artisans du bâtiment et builders (28/09/2026)
    /fr/site-internet-artisan                  page mère des métiers du bâtiment (requête
                                               « création site internet artisan ») :
                                               qualification, mot « artisan », décennale,
                                               hors établissement, démarchage (opt-in au
                                               11/08/2026), RGE (L224-114), encart France
                                               Rénov', TVA réduite sans attestation, garanties
    /en/website-for-builders-in-spain          règles espagnoles : permis municipaux, LOE,
                                               amiante (RERA), déchets, IVA 10 %, espèces
                                               (Ley 7/2012), réclamations, devis
    /reformas/                                 (espagnol, page existante)

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
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'photos'))
from photos_lib import injecter as poser_photo  # photo prévue par _tools/photos/images.json

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build_lang_homes as H  # noqa: E402
import build_expat_pages as X  # noqa: E402  (styles, tarifs et avis communs)

BASE, E = H.BASE, H.E
ROOT = H.ROOT


def abandon(msg):
    sys.exit('ABANDON : %s\nRien n\'a été modifié.' % msg)


# ═════════════════════════ THÉRAPEUTES ET PSYCHOLOGUES ═════════════════════
# Lignes communes aux pages artisans FR (menuisier, plombier, électricien, artisan).
ROW_MENTIONS = ("Mentions légales", "LCEN, art. 1-1 et 19 ; Code de commerce, art. R526-27",
                "Nom précédé ou suivi de « EI » (ou « entrepreneur individuel ») si vous êtes entrepreneur "
                "individuel, ou forme, capital et siège pour une société, adresse, téléphone, e-mail, numéro "
                "d'immatriculation au RNE, numéro de TVA si vous en avez un, directeur de la publication, et nom, "
                "adresse et téléphone de l'hébergeur.")
FAQ_AVIS = ("Puis-je afficher mes avis Google sur mon site ?",
            "Oui. Près des avis, indiquez s'ils font ou non l'objet d'un contrôle, la date de chaque avis et celle "
            "de l'expérience du client, et la façon dont ils sont classés, l'ordre chronologique devant faire partie "
            "des critères. Dans une rubrique facile d'accès, précisez s'il y a eu une contrepartie en échange des "
            "avis, le délai maximal de publication et la durée de conservation d'un avis et, si vous les contrôlez, "
            "comment (Code de la consommation, art. L111-7-2, D111-10 et D111-11). Publier de faux avis, ou les "
            "modifier, est une pratique commerciale trompeuse.")

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
          "paiement unique</strong>, jusqu'à 4 langues sans supplément si vous le souhaitez, et la démo est prête en 24 heures.",
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
        ('Tous : mentions légales', 'LCEN, art. 1-1 et 19 ; Code de commerce, art. R526-27',
         "Nom précédé ou suivi de « EI » (ou « entrepreneur individuel ») si vous êtes entrepreneur individuel, "
         "adresse, téléphone, e-mail, numéro d'immatriculation, nom du directeur de la publication, nom, adresse et "
         "téléphone de l'hébergeur et, pour une profession réglementée, votre titre, le pays où il a été obtenu, "
         "l'organisme d'inscription et les règles professionnelles applicables."),
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
    price_note="Prix hors taxes : l'IVA espagnole de 21 % s'ajoute. Si vous êtes établi dans un autre pays de l'UE, "
               "en France par exemple, avec un numéro de TVA intracommunautaire, la facture est émise sans TVA "
               "(autoliquidation) ; les psychologues, exonérés, et les praticiens en franchise en base ne récupèrent "
               "pas cette TVA. Nom de domaine inclus la première année, puis environ 12 €/an.",
    extra=[
        ('contenu-site', 'Sur votre site', "Que mettre sur le site internet d&#x27;un psychologue ou d&#x27;un thérapeute ?",
         '<p class="legal-intro">Un site internet efficace pour un thérapeute ou un psychologue répond aux '
         'questions qu&#x27;une personne se pose avant un premier contact, dans un langage clair, sans jargon ni '
         'promesse de résultat.</p>'
         '<div class="why-g">'
         '<div class="aud-c"><div class="aud-i" aria-hidden="true">📝</div>'
         '<h3>Qui vous êtes, présenté simplement</h3>'
         '<p>Votre formation, votre titre et votre approche, résumés en quelques lignes pour qu&#x27;un visiteur '
         'sache tout de suite à qui il s&#x27;adresse.</p></div>'
         '<div class="aud-c"><div class="aud-i" aria-hidden="true">🗓️</div>'
         '<h3>Comment se passe une première séance</h3>'
         '<p>La durée d&#x27;une séance, le déroulement du premier rendez-vous, l&#x27;adresse et l&#x27;accès du '
         'cabinet ou le fonctionnement de la visio : ce qu&#x27;une personne veut savoir avant de vous appeler.</p></div>'
         '<div class="aud-c"><div class="aud-i" aria-hidden="true">✉️</div>'
         '<h3>Comment vous contacter</h3>'
         '<p>Un formulaire court (nom, coordonnées et créneau souhaité, sans motif de consultation), un bouton '
         'WhatsApp et votre numéro pour appeler directement.</p></div>'
         '<div class="aud-c"><div class="aud-i" aria-hidden="true">📱</div>'
         '<h3>Un site rapide sur tous les écrans</h3>'
         '<p>Beaucoup de visiteurs arrivent depuis leur téléphone : un site qui se charge rapidement et '
         's&#x27;affiche bien sur mobile compte autant pour eux que pour votre référencement.</p></div>'
         '</div>'
         '<p class="where">Pour aller plus loin, notre guide sur <a href="https://webautonomos.es/blog/fr/'
         'site-web-pour-psychologues-et-therapeutes">le site d&#x27;un psychologue ou d&#x27;un thérapeute</a> '
         'détaille chaque rubrique de contenu.</p>'),
        ('visibilite-therapeute', 'Se faire trouver',
         "Comment un thérapeute apparaît-il dans les recherches locales ?",
         '<p class="legal-intro">Quand une personne cherche un psychologue ou un thérapeute près de chez elle, des '
         'textes à jour, qui nomment votre activité et votre ville et restent cohérents avec votre fiche Google, '
         'aident votre site à apparaître dans ces recherches locales.</p>'
         '<div class="aud-g">'
         '<div class="aud-c"><div class="aud-i" aria-hidden="true">🔍</div>'
         '<h3>Le référencement de base, inclus</h3>'
         '<p>Des titres et des textes rédigés autour de votre activité et de votre secteur géographique, '
         'cohérents avec votre fiche Google : cette optimisation fait partie du prix de votre site, sans '
         'supplément à prévoir.</p></div>'
         '<div class="aud-c"><div class="aud-i" aria-hidden="true">📈</div>'
         '<h3>SEO local et fiche Google, en complément</h3>'
         '<p>Nous proposons aussi le référencement local (SEO local) pour 15 € HT par mois, et la gestion de '
         'votre fiche Google pour 29 € HT par mois, avec 49 € HT de création si vous n&#x27;en avez pas encore.'
         '</p></div>'
         '<div class="aud-c"><div class="aud-i" aria-hidden="true">🔗</div>'
         '<h3>Vos réseaux sociaux reliés à votre site</h3>'
         '<p>Si vous êtes présent sur les réseaux sociaux — Facebook, Instagram, LinkedIn — votre site internet '
         'renvoie vers vos profils : une présence en ligne cohérente, plutôt que des vitrines séparées.</p></div>'
         '</div>'
         '<p class="where">Nos guides sur le <a href="https://webautonomos.es/blog/fr/'
         'seo-local-independants-guide-complet">SEO local pour indépendants</a> et sur <a href="https://'
         'webautonomos.es/blog/fr/optimiser-sa-fiche-google-business-profile">l&#x27;optimisation de votre fiche '
         'Google</a> détaillent la démarche.</p>'),
        ('pourquoi-webautonomos', 'Notre différence',
         "Pourquoi un prix fixe de 15 € HT par mois plutôt qu&#x27;un devis d&#x27;agence ?",
         '<p class="legal-intro">Pour la création de votre site internet de psychologue ou de thérapeute, nous '
         'utilisons un système propre qui réutilise des composants déjà testés, sans bureaux coûteux ni commerciaux '
         'à commission : c&#x27;est ce qui permet un prix fixe, là où une agence classique construit son devis '
         'après un échange.</p>'
         '<div class="aud-g">'
         '<div class="aud-c"><div class="aud-i" aria-hidden="true">🧩</div>'
         '<h3>Des textes écrits pour votre pratique</h3>'
         '<p>Nous rédigeons vos textes à partir de vos informations — votre titre, votre approche, votre façon de '
         'recevoir — au lieu de vous laisser remplir un modèle vide.</p></div>'
         '<div class="aud-c"><div class="aud-i" aria-hidden="true">🛠️</div>'
         '<h3>Le suivi technique compris dans le prix</h3>'
         '<p>Hébergement, certificat SSL, sauvegardes quotidiennes et maintenance technique sont compris, avec une '
         'modification par mois après la mise en ligne, sans limite de durée.</p></div>'
         '<div class="aud-c"><div class="aud-i" aria-hidden="true">💬</div>'
         '<h3>Un accompagnement, pas un simple outil en ligne</h3>'
         '<p>Nous écrivons votre site avec vous : vous décrivez votre activité en quelques minutes, vous '
         'découvrez votre démo en moins de 24 heures, puis nous faisons ensemble les ajustements avant la mise '
         'en ligne.</p></div>'
         '</div>'
         '<p class="where">Vous voulez aussi vendre en ligne ? Une boutique en ligne n&#x27;est comprise dans '
         'aucune des deux formules : elle se fait <a href="https://webautonomos.es/fr/prestations">sur devis</a>.'
         '</p>'),
    ],
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
          "aussi des sites pour les francophones installés en Espagne."),
         ("Un nouveau site apparaît-il tout de suite dans les recherches ?",
          "Pas immédiatement. Le référencement de base, inclus avec votre site, aligne vos titres et vos textes "
          "sur votre activité et votre fiche Google ; mais le référencement local demande du temps pour "
          "progresser. Notre service de SEO local, à 15 € HT par mois, est pensé pour cette progression dans la "
          "durée.")],
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
          "and Spanish, plus up to two more languages (French, Catalan, Galician or Basque), at no extra cost. We work with you in English, and your demo is ready within 24 hours.",
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
                                     "and an SSL certificate (https) across the whole site."),
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
    extra=[
        ('website-content', 'On your website', 'What to put on your therapist or psychologist website',
         '<p class="legal-intro">When someone looking for a therapist lands on your website, they need to see '
         'quickly who you are, how you work and how to reach you, whatever screen they are using.</p>'
         '<div class="why-g">'
         '<div class="aud-c"><div class="aud-i" aria-hidden="true">📝</div>'
         '<h3>What you do, in plain language</h3>'
         '<p>Your approach and the type of session you offer, in person, online or both, described so a '
         'stranger can understand it, without jargon or a promise of a cure.</p></div>'
         '<div class="aud-c"><div class="aud-i" aria-hidden="true">🎓</div>'
         '<h3>Who you are, and why they can trust you</h3>'
         '<p>Your training, your years of experience and, if you are a psychologist, your Colegio and colegiado '
         'number (see <a href="#rules">the rules above</a>).</p></div>'
         '<div class="aud-c"><div class="aud-i" aria-hidden="true">✉️</div>'
         '<h3>How to get in touch</h3>'
         '<p>A contact form, a WhatsApp button or a phone number, so a visitor does not have to search for how '
         'to reach you.</p></div>'
         '<div class="aud-c"><div class="aud-i" aria-hidden="true">📱</div>'
         '<h3>A design that works on any screen</h3>'
         '<p>Many visitors will look at your site on their phone, so a design that looks good and works well on '
         'any screen matters, for them and for search engines.</p></div>'
         '</div>'
         '<p class="where">For a longer read on structuring this kind of site, see our blog guide on '
         '<a href="https://webautonomos.es/blog/en/website-for-psychologists-and-therapists">the essential '
         'sections of a psychology website</a>.</p>'),
        ('different-titles', 'Different titles, different rules',
         'Websites for psychologists, psychotherapists and counsellors',
         '<p class="legal-intro">The website itself works the same way for every title; what changes is which '
         'claims the rules above let you make.</p>'
         '<div class="aud-g">'
         '<div class="aud-c"><div class="aud-i" aria-hidden="true">🧠</div>'
         '<h3>If you are a psychologist</h3>'
         '<p>Show your Colegio and colegiado number, plus your practice&#8217;s registration number if you work '
         'as a health psychologist (see <a href="#rules">the rules above</a>).</p></div>'
         '<div class="aud-c"><div class="aud-i" aria-hidden="true">🗣️</div>'
         '<h3>If you are a psychotherapist</h3>'
         '<p>Describe your training and how a session works, without a promise of relief or cure: the bans on '
         'health claims in <a href="#rules">the rules above</a> apply to anyone who presents their work as '
         'health-related, whatever their title.</p></div>'
         '<div class="aud-c"><div class="aud-i" aria-hidden="true">💬</div>'
         '<h3>If you are a counsellor</h3>'
         '<p>Like coach and hypnotherapist, counsellor is not a regulated title in Spain: write about support '
         'and personal development, not treatment.</p></div>'
         '</div>'),
        ('getting-found', 'Local search', 'How your website helps you appear in local searches',
         '<p class="legal-intro">Getting found by someone searching for a therapist near them depends on more '
         'than the design: your copy and your Google Business Profile count too.</p>'
         '<div class="aud-g">'
         '<div class="aud-c"><div class="aud-i" aria-hidden="true">🔍</div>'
         '<h3>Basic SEO, included in your price</h3>'
         '<p>Titles and copy written around your services and your area, kept consistent with your Google '
         'Business Profile, come with your website at no extra cost.</p></div>'
         '<div class="aud-c"><div class="aud-i" aria-hidden="true">📈</div>'
         '<h3>SEO Local and your Google listing, if you want more</h3>'
         '<p>We also offer SEO Local for €15 + VAT a month, and managing your Google Business Profile for €29 '
         '+ VAT a month (€49 + VAT to set one up if you do not have a listing yet).</p></div>'
         '<div class="aud-c"><div class="aud-i" aria-hidden="true">📚</div>'
         '<h3>Guides to go further</h3>'
         '<p>Our blog has practical guides on <a href="https://webautonomos.es/blog/en/how-to-rank-your-website-'
         'in-local-google">ranking your website locally</a> and <a href="https://webautonomos.es/blog/en/'
         'optimise-your-google-business-profile">optimising your Google Business Profile</a>.</p></div>'
         '</div>'),
    ],
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
          "in English and Spanish, and in Catalan too if you need it, at no extra cost (up to four languages)."),
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

# ═════════════════════════ MENUISIERS ET CARPENTERS ════════════════════════
MENU = {}
MENU['fr'] = dict(
    html_lang='fr', og_locale='fr_FR', unit='mois', area=['FR', 'ES'],
    title="Site internet pour menuisier : 15 €/mois, démo en 24 h",
    description="Site internet pour menuisier bois, alu ou PVC : vos réalisations, décennale, médiateur, mentions "
                "légales et encart France Rénov'. Démo gratuite en 24 h, 15 €/mois HT.",
    service_name="Création de site internet pour menuisiers",
    audience="Menuisiers, ébénistes, poseurs de fenêtres et agenceurs de cuisine",
    crumb_home='Accueil', crumb='Menuisiers',
    badge='Menuisiers bois, alu et PVC, ébénistes, agenceurs',
    h1="Création de site internet pour <em>menuisiers</em> : montrez votre travail",
    lede="Vos réalisations en photos, vos zones d'intervention, un devis demandé en un clic, et les mentions que la "
         "loi impose dès que vous travaillez pour des particuliers. Nous l'écrivons pour vous et vous envoyons une démo "
         "gratuite en 24 heures.",
    pills=['Vos réalisations en valeur', 'Mentions obligatoires en ordre', 'Démo gratuite en 24 h'],
    cta='Recevoir ma démo gratuite', cta2='Ce que la loi impose',
    brief_t='En bref',
    brief="WebAutonomos crée des sites internet pour les menuisiers bois, alu et PVC, les ébénistes, les poseurs de "
          "fenêtres et les agenceurs de cuisine, en France et en Espagne. Nous mettons vos réalisations en valeur, "
          "rédigeons les textes et plaçons les mentions qu'impose le travail pour des particuliers : assurance, "
          "médiateur de la consommation, mentions légales et, si vous remplacez des fenêtres ou isolez, "
          "l'encart France Rénov' obligatoire à partir du 1<sup>er</sup> octobre 2026. Le site coûte "
          "<strong>15 € HT par mois</strong> sans frais d'installation ni engagement, ou <strong>349 € HT en "
          "paiement unique</strong>, jusqu'à 4 langues sans supplément si vous le souhaitez, et la démo est prête en "
          "24 heures.",
    legal_id='regles', legal_ey='Les règles', legal_t="Ce que votre site doit montrer",
    legal_intro="Un site de menuisier n'est pas qu'une vitrine : dès que vous travaillez pour des particuliers, le Code "
                "de la consommation vous impose quelques mentions, et la rénovation énergétique a ses propres règles. "
                "Voici l'essentiel pour une activité en France.",
    legal_cols=('Sujet', 'Texte', 'Ce que ça change pour vous'),
    legal_rows=[
        ("Le mot « artisan »", "Code de l'artisanat, art. L211-1, L241-1 et L241-2",
         "Réservé à ceux qui ont un CAP, un BEP, un titre équivalent ou trois ans d'expérience dans le métier : "
         "l'immatriculation seule ne suffit pas. L'usage abusif est puni de 7 500 € d'amende (37 500 € pour une "
         "société). « Maître artisan » est un titre délivré par la chambre de métiers, en général avec le brevet de "
         "maîtrise et deux ans de pratique."),
        ("Assurance", "Code des assurances, art. L241-1 et L243-2 ; Code de la consommation, art. R111-2",
         "Si vous êtes soumis à la décennale, l'attestation se joint à chaque devis et chaque facture. Avant tout "
         "contrat, le client doit aussi pouvoir connaître votre assurance, votre assureur et la couverture "
         "géographique : autant l'indiquer clairement dès le premier contact."),
        ("RGE et aides pour les fenêtres", "Code de la consommation, art. L121-4 ; décret n° 2026-822",
         "Afficher le logo RGE sans la qualification est une pratique commerciale trompeuse. Depuis le 1er septembre "
         "2026, MaPrimeRénov' « par geste » ne finance plus les fenêtres ; elles restent possibles dans une "
         "rénovation d'ampleur, et avec les CEE si elles remplacent du simple vitrage, par un professionnel RGE."),
        ("Encart France Rénov'", "Code de la consommation, art. L122-26 ; arrêté du 7 juillet 2026",
         "À partir du 1er octobre 2026, tout professionnel qui propose des travaux de rénovation énergétique sur son "
         "site ou dans sa publicité doit afficher le message officiel de France Rénov' dans un bandeau, avec un lien "
         "vers le service public. Amende jusqu'à 15 000 € (75 000 € pour une société)."),
        ("Médiateur de la consommation", "Code de la consommation, art. L616-1, R616-1 et L641-1",
         "Si vous travaillez pour des particuliers, le nom, les coordonnées et l'adresse du site de votre médiateur "
         "doivent apparaître clairement, par exemple en pied de page. Amende jusqu'à 3 000 € (15 000 € pour une société)."),
        ("Tarifs de dépannage et devis", "Arrêté du 24 janvier 2017",
         "Pour le dépannage, la réparation et l'entretien, menuiserie comprise : taux horaire TTC, mode de décompte du "
         "temps, frais de déplacement et conditions du devis doivent être facilement accessibles en ligne, et un "
         "devis détaillé est remis avant toute intervention."),
        ROW_MENTIONS,
    ],
    legal_note="Nouveau au 1er octobre 2026 : l'encart France Rénov' devient obligatoire pour les sites qui proposent "
               "le remplacement de fenêtres ou l'isolation. Et si vous affichez des avis clients, "
               "indiquez s'ils sont contrôlés et comment, avec leur date (Code de la consommation, art. L111-7-2). "
               "Informations générales à jour en septembre 2026, qui ne remplacent pas un conseil juridique.",
    legal_we_t='Ce que nous mettons en place',
    legal_we=["Votre qualité d'artisan, votre numéro RNE et votre assurance (assureur, couverture) indiqués "
              "clairement",
              "Le logo RGE seulement si vous êtes qualifié, avec les travaux qu'il couvre",
              "L'encart France Rénov' et son lien, si votre activité est concernée",
              "Vos tarifs de dépannage (taux horaire TTC, déplacement) sur une page dédiée, si vous faites de la "
              "réparation",
              "Les coordonnées de votre médiateur, des mentions légales complètes et des avis présentés avec leur "
              "date et leur mode de vérification"],
    spain_note="<strong>Vous travaillez en Espagne ?</strong> Les règles changent : droit du client à un devis écrit "
               "préalable dans plusieurs communautés (Valence, Madrid, Catalogne), sauf renonciation manuscrite, "
               "formulaires de réclamation régionaux, et IVA à 10 % sous conditions, pour la rénovation du logement "
               "d'un particulier notamment. Nous connaissons aussi ces règles : "
               "<a href=\"/fr/site-internet-francophones-espagne\">site internet pour francophones en Espagne</a>.",
    sources_t='Sources',
    why_ey='Pourquoi nous', why_t="Pensé pour les menuisiers",
    why=[('📸', 'Vos réalisations en valeur', "Cuisines, escaliers, fenêtres, dressings : vos photos de chantier "
                                            "classées par type de travaux, avec avant et après si vous en avez."),
         ('📝', 'Un devis en un clic', "Formulaire, WhatsApp ou téléphone : le particulier décrit son projet et vous "
                                      "recevez la demande directement."),
         ('📄', 'Les mentions en ordre', "Assurance, médiateur, mentions légales, encart France Rénov' : ce que la "
                                        "loi demande est en place, sans que vous ayez à le chercher."),
         ('📍', 'Trouvé près de chez vous', "Titres et textes pensés pour les recherches « menuisier + votre ville », "
                                           "et votre fiche Google si vous le souhaitez.")],
    where_t='En France et en Espagne',
    where="Nous travaillons à distance, en français, par e-mail, WhatsApp et visioconférence : que votre atelier soit "
          "en Bretagne, en Alsace ou sur la Costa Blanca, rien ne change.",
    sect_t='Pour qui',
    sectors=['🪵 Menuisiers bois', '🪟 Menuisiers alu et PVC', '🚪 Poseurs de portes et fenêtres', '🪑 Ébénistes',
             '🍳 Cuisinistes et agenceurs', '🪜 Escaliéteurs', '🏠 Charpentiers', '🟫 Parqueteurs'],
    how_t='Votre projet en trois étapes',
    steps=[('Vous décrivez votre activité', "Vos spécialités, votre zone d'intervention, quelques photos de "
                                           "chantier : deux minutes suffisent."),
           ('Nous préparons votre démo', "En moins de 24 heures, avec vos réalisations, vos textes et vos mentions "
                                        "légales."),
           ('Vous décidez', "Vous demandez les modifications que vous voulez. Si le site vous plaît, il est mis en "
                           "ligne ; sinon, vous ne payez rien.")],
    price_note="Prix hors taxes : l'IVA espagnole de 21 % s'ajoute. Si votre entreprise est établie dans un autre "
               "pays de l'UE, en France par exemple, avec un numéro de TVA intracommunautaire, la facture est émise "
               "sans TVA (autoliquidation). Nom de domaine inclus la première année, puis environ 12 €/an.",
    extra=[
        ('realisations', 'Ce qui convainc', 'Comment vos réalisations et votre secteur sont mis en avant',
         "<p class=\"legal-intro\">Un visiteur veut savoir vite si vous faites le type de travaux qu'il cherche, et "
         "si vous intervenez près de chez lui.</p>"
         "<div class=\"why-g\">"
         "<div class=\"aud-c\"><div class=\"aud-i\" aria-hidden=\"true\">📸</div>"
         "<h3>Une galerie classée par type de travaux</h3>"
         "<p>Vos photos de chantier sont regroupées par catégorie, pour qu'une personne intéressée par un dressing "
         "ne fasse pas défiler des photos d'escaliers avant de trouver ce qu'elle cherche. Nous partons de vos "
         "propres photos.</p></div>"
         "<div class=\"aud-c\"><div class=\"aud-i\" aria-hidden=\"true\">📍</div>"
         "<h3>Votre zone d'intervention, dite clairement</h3>"
         "<p>Nommer les villes où vous travaillez, Nantes, Rezé ou Saint-Herblain par exemple, permet au visiteur "
         "de savoir tout de suite si vous vous déplacez chez lui. C'est aussi vrai si vous travaillez en Espagne, "
         "sur la Costa Blanca ou ailleurs.</p></div>"
         "<div class=\"aud-c\"><div class=\"aud-i\" aria-hidden=\"true\">🏷️</div>"
         "<h3>Une légende sous chaque photo</h3>"
         "<p>Le matériau, le type de pose et la ville du chantier, en une ligne : le visiteur comprend ce qu'il "
         "regarde sans avoir à vous appeler.</p></div>"
         "</div>"
         "<p class=\"where\">Pour aller plus loin, consultez "
         "<a href=\"https://webautonomos.es/blog/fr/site-web-pour-menuisiers-et-renovation\">notre guide pratique "
         "pour menuisiers</a>.</p>"),
        ('visibilite', 'Se faire trouver', 'Comment apparaître dans les recherches locales',
         "<p class=\"legal-intro\">Commencez par des informations identiques partout : mêmes nom, adresse et "
         "téléphone sur votre site internet et sur votre fiche d'établissement. Une partie de ce travail est déjà "
         "comprise dans le prix ; le reste est un service à part.</p>"
         "<div class=\"why-g\">"
         "<div class=\"aud-c\"><div class=\"aud-i\" aria-hidden=\"true\">🔍</div>"
         "<h3>Le référencement de base, inclus dans le prix</h3>"
         "<p>Vos titres et vos textes mentionnent votre métier et votre zone : c'est compris dans les deux "
         "formules, sans supplément.</p></div>"
         "<div class=\"aud-c\"><div class=\"aud-i\" aria-hidden=\"true\">📈</div>"
         "<h3>Le SEO Local, un service à part</h3>"
         "<p>Nous proposons aussi le SEO Local pour 15 € HT par mois (quatre articles de blog par mois, mots-clés "
         "locaux et un rapport mensuel), et la gestion de votre fiche Google pour 29 € HT par mois (49 € HT de "
         "création si vous n'en avez pas encore). Ce sont des services séparés, à ajouter à l'abonnement ou même "
         "sans lui.</p></div>"
         "<div class=\"aud-c\"><div class=\"aud-i\" aria-hidden=\"true\">📚</div>"
         "<h3>Nos guides sur le sujet</h3>"
         "<p>Nos articles approfondissent ces sujets : comment "
         "<a href=\"https://webautonomos.es/blog/fr/optimiser-sa-fiche-google-business-profile\">mieux remplir "
         "votre fiche professionnelle</a> et comment "
         "<a href=\"https://webautonomos.es/blog/fr/obtenir-plus-avis-google-guide-complet\">obtenir plus "
         "d'avis</a>.</p></div>"
         "</div>"),
    ],
    faq_t='Questions fréquentes',
    faq=[("Un menuisier doit-il afficher son assurance décennale sur son site ?",
          "Aucun texte n'impose ce canal en particulier. Si vous êtes soumis à la décennale, l'attestation doit être "
          "jointe à chaque devis et chaque facture (Code des assurances, art. L243-2). Et avant tout contrat, le client "
          "doit pouvoir connaître votre assurance, votre assureur et la couverture géographique (Code de la "
          "consommation, art. R111-2) : l'indiquer dès votre page d'accueil est la façon la plus simple d'y répondre."),
         ("Puis-je me présenter comme artisan menuisier ?",
          "Oui si vous avez un CAP, un BEP, un titre équivalent ou trois ans d'expérience dans le métier : c'est ce qui "
          "donne la qualité d'artisan, pas la seule immatriculation. Utiliser le mot « artisan » sans y avoir droit "
          "est puni de 7 500 € d'amende. Si votre activité relève vraiment d'un métier d'art de la liste officielle, "
          "menuiserie ou ébénisterie d'art par exemple, vous pouvez demander la qualité d'artisan d'art : vérifiez-le "
          "auprès de votre chambre de métiers avant de l'afficher."),
         ("Le remplacement de fenêtres donne-t-il encore droit à MaPrimeRénov' ?",
          "Plus en « par geste » : depuis le 1er septembre 2026, ce parcours ne finance plus les fenêtres. Elles "
          "restent possibles dans une rénovation d'ampleur, ou avec les certificats "
          "d'économies d'énergie quand elles remplacent du simple vitrage, à condition de passer par un professionnel "
          "RGE. Restez précis dans vos annonces en ligne : une aide affichée à tort est une pratique commerciale "
          "trompeuse."),
         ("Qu'est-ce que l'encart France Rénov' obligatoire au 1er octobre 2026 ?",
          "À partir du 1er octobre 2026 (Code de la consommation, art. L122-26), tout professionnel qui propose des "
          "travaux de rénovation énergétique, en ligne ou dans sa publicité, doit afficher, dans un bandeau, le "
          "message officiel : « Avant de vous engager, le service public vous informe gratuitement pour préparer et "
          "sécuriser votre projet : www.france-renov.gouv.fr », avec un lien vers le service public. Amende jusqu'à "
          "15 000 € (75 000 € pour une société). Si vous posez des fenêtres ou isolez, vous êtes concerné ; nous "
          "ajoutons le bandeau."),
         ("Dois-je indiquer un médiateur de la consommation ?",
          "Oui, si vous travaillez pour des particuliers, quelle que soit la taille de votre entreprise. Son nom, ses "
          "coordonnées et l'adresse de son site internet doivent figurer de manière visible et lisible sur votre "
          "site, vos conditions générales et vos bons de commande. L'ancienne plateforme européenne de règlement "
          "des litiges a fermé en juillet 2025 : inutile d'y renvoyer."),
         ("Mes tarifs de dépannage doivent-ils être sur mon site ?",
          "Oui, si vous faites du dépannage, de la réparation ou de l'entretien : l'arrêté du 24 janvier 2017 couvre "
          "la menuiserie. Taux horaire TTC, mode de décompte du temps, frais de déplacement et conditions du devis "
          "doivent être facilement accessibles en ligne, et un devis détaillé est remis avant l'intervention."),
         FAQ_AVIS,
         ("Le SEO Local est-il inclus dans le prix, ou puis-je l'acheter à part ?",
          "Le référencement de base est inclus : titres et textes construits autour de votre métier. Le SEO Local "
          "(quatre articles de blog par mois, mots-clés locaux, rapport mensuel) est un service séparé à 15 € HT "
          "par mois, tout comme la gestion de votre fiche Google (29 € HT par mois, plus 49 € HT de création si "
          "vous n'avez pas encore de fiche) : les deux s'achètent indépendamment de l'abonnement."),
         ("Combien coûte un site pour menuisier ?",
          "15 € HT par mois sans frais d'installation ni engagement, ou 349 € HT en paiement unique, avec les mêmes "
          "services : conception, hébergement, nom de domaine la première année, mentions légales et une "
          "modification par mois. Le site peut être en plusieurs langues sans supplément (jusqu'à 4), et la démo est "
          "gratuite.")],
    final_t='Voyez votre site avant de payer quoi que ce soit',
    final_sd="Démo gratuite en 24 heures, avec vos réalisations et vos mentions légales. Sans frais d'installation, "
             "sans engagement.",
)

MENU['en'] = dict(
    html_lang='en', og_locale='en_GB', unit='month', area=['ES'],
    title="Websites for carpenters and joiners in Spain: €15/month",
    description="Websites for English-speaking carpenters, joiners and kitchen fitters in Spain: your work, your legal "
                "notice and Spanish consumer rules. Free demo in 24h, €15/month + VAT.",
    service_name="Web design for carpenters and joiners in Spain",
    audience="English-speaking carpenters, joiners, kitchen fitters and window installers in Spain",
    crumb_home='Home', crumb='Carpenters and joiners',
    badge='For carpenters, joiners and kitchen fitters in Spain',
    h1="Websites for <em>carpenters and joiners</em> in Spain",
    lede="Your projects in photos, the areas you cover, a quote request in one click, in English and Spanish, and the "
         "information Spanish consumer law expects. We write it for you and send you a free demo within 24 hours.",
    pills=['English and Spanish included', 'Spanish rules built in', 'Free demo in 24 hours'],
    cta='Get my free demo', cta2='What Spanish rules require',
    brief_t='In short',
    brief="WebAutonomos builds websites for English-speaking carpenters, joiners, kitchen fitters and window "
          "installers working in Spain. We show your projects, write the copy in English and Spanish (up to four languages) at no extra "
          "cost, and include what Spanish law expects: a legal notice with your NIF or NIE, prices for homeowners "
          "shown with VAT included, and the complaint information your region asks for. It costs <strong>€15 + VAT per "
          "month</strong> with no setup fee and no lock-in, or a <strong>one-off €349 + VAT</strong>. We work with "
          "you in English, and your demo is ready within 24 hours.",
    legal_id='rules', legal_ey='Spanish rules', legal_t='What your website and quotes have to get right',
    legal_intro="Carpentry isn't a regulated profession in Spain, but as soon as you work for homeowners, consumer law "
                "and your region's rules decide what your website, quotes and invoices must show. These are the points "
                "that matter.",
    legal_cols=('Topic', 'Law', 'What it means for you'),
    legal_rows=[
        ('Legal notice', 'LSSI (Ley 34/2002), art. 10',
         "Your name or company name, your address, your email and another direct contact detail (usually your "
         "phone), your NIF (for a foreign national, your NIE), your Registro Mercantil details if you trade as an "
         "S.L., and, if you show prices, whether they include VAT."),
        ('Written quotes', 'Comunitat Valenciana: Decreto 11/1995; Madrid: Decreto 35/1995; Catalonia: Consumer Code, '
                           'art. 251-3',
         "In these regions a homeowner is entitled to a detailed written quote with set contents before work starts, "
         "unless they waive it in their own handwriting and sign; a pre-printed waiver is not enough. Madrid's "
         "consumer office also expects renovation firms to offer a price information sheet on their website."),
        ('Complaints', 'Consumer law (TRLGDCU), art. 21.3; regional rules',
         "Tell customers where they can complain: at least through the channel your contract with them started on "
         "(WhatsApp or your web form, for example), by post, by phone and by an electronic channel. Since 28 "
         "December 2025 you must reply within 15 days at most (previously a month). Official complaint forms are "
         "regional: in Andalucía, businesses without premises must show a QR complaint poster on quotes, invoices "
         "and websites."),
        ('10% VAT', 'Ley 37/1992, art. 91.Uno.2.10º',
         "Renovation or repair of a home at least two years old, for an individual using it privately (not rented "
         "out) or a comunidad de propietarios, with materials costing no more than 40% of the price before VAT. "
         "Double glazing usually goes over that limit, and doors, windows or kitchen units supplied without fitting "
         "are always 21%."),
        ('Customer reviews', 'Consumer law (TRLGDCU), art. 20.4; Ley 3/1991, art. 27',
         "Say whether and how you check that reviews come from real customers. Since December 2025, reviews must "
         "relate to a job bought or used in the 30 days before the review; fake reviews have been banned since "
         "2022."),
        ('Language', 'Consumer law (TRLGDCU), art. 60.4',
         "Pre-contract information, quotes included, must be given at least in Spanish. In Catalonia, customers can "
         "ask for offers, quotes and invoices in Catalan."),
    ],
    legal_note="Rules on quotes and complaint forms are regional, so check your comunidad autónoma's consumer office. "
               "This is general information as of September 2026, not legal advice.",
    legal_we_t='What we set up for you',
    legal_we=["A proper legal notice with your name, NIF or NIE and contact details, plus your company details if you "
              "trade as an S.L.",
              "Your postal address, phone, email and WhatsApp shown together, so customers can reach you through the "
              "complaint channels consumer law requires",
              "Prices for homeowners shown with VAT included, and a price information page (expected in Madrid for "
              "renovation firms)",
              "The complaint information your region asks for, such as the QR poster in Andalucía",
              "Customer reviews shown with a note on how they are checked, and your site in up to four languages, English and Spanish included, at no "
              "extra cost"],
    spain_note='',
    sources_t='Sources',
    why_ey='Why us', why_t='Built for tradespeople who work in English',
    why=[('💬', 'We speak your language', "Email, WhatsApp or video call in English: no need to decode Spanish "
                                         "legal or technical jargon."),
         ('🌍', 'Up to four languages, one price', "English, Spanish and up to two more at no extra cost, so Spanish homeowners find you as "
                                           "easily as expats do."),
         ('📸', 'Your work, shown properly', "Kitchens, wardrobes, doors, staircases: your project photos organised "
                                            "by type of job."),
         ('📍', 'Found locally', "Titles and copy written for searches like “carpenter Jávea” or “kitchen fitter "
                                "Torrevieja”, in both languages.")],
    where_t='Anywhere in Spain',
    where="Costa Blanca, Costa del Sol, Valencia, Mallorca, Barcelona, Madrid or the Canary Islands: we work remotely, "
          "so your workshop's location does not change how we work with you.",
    sect_t='Who it is for',
    sectors=['🪵 Carpenters', '🪚 Joiners', '🍳 Kitchen fitters', '🚪 Door and window installers',
             '🗄️ Fitted wardrobes', '🪜 Staircase makers', '🪑 Cabinet makers', '🟫 Floor fitters'],
    how_t='Your website in three steps',
    steps=[('Tell us about your business', 'Your specialities, the areas you cover and a few project photos: '
                                           'it takes two minutes.'),
           ('We build your demo', 'Within 24 hours, with your projects, your copy in English and Spanish, and '
                                  'your legal pages.'),
           ('You decide', "Ask for any changes you want. If you like it, it goes live; if not, you pay nothing.")],
    price_note="Prices exclude VAT (21% IVA on the mainland and the Balearics; the Canary Islands, Ceuta and Melilla "
               "have their own taxes). As a VAT-registered autónomo you can normally deduct it. Domain name included "
               "for the first year, then about €12/year.",
    extra=[
        ('what-to-include', 'On your website', "What to put on your carpentry website",
         '<p class="legal-intro">A homeowner who lands on your website wants to see quickly whether you do the '
         'kind of work they need, in their area, and how to reach you. These are the parts that answer those '
         'questions and make it easier for them to ask you for a quote. In a clean, uncluttered layout, close-up '
         'photos of joints, grain and the finish on a staircase or worktop show your craftsmanship before anyone '
         'picks up the phone.</p>'
         '<div class="why-g">'
         '<div class="aud-c"><div class="aud-i" aria-hidden="true">\U0001F5C2️</div>'
         '<h3>A portfolio organised by project type</h3>'
         '<p>Kitchens, staircases, fitted wardrobes and bespoke furniture, grouped so a visitor looking for one type '
         'of work does not have to scroll past another. A good starting point is your own project photos: we '
         'build your site around them.</p></div>'
         '<div class="aud-c"><div class="aud-i" aria-hidden="true">\U0001F4CD</div>'
         '<h3>The areas you cover, stated clearly</h3>'
         '<p>Naming the towns you work in (Jávea, Torrevieja or Marbella, for example) helps both readers and '
         'Google understand who your site is for.</p></div>'
         '<div class="aud-c"><div class="aud-i" aria-hidden="true">\U0001F4AC</div>'
         '<h3>A quote request in one click</h3>'
         '<p>A form, WhatsApp button or phone number that a homeowner can use straight away, without hunting for '
         'your contact details.</p></div>'
         '<div class="aud-c"><div class="aud-i" aria-hidden="true">⭐</div>'
         '<h3>Google reviews, shown honestly</h3>'
         '<p>As the rules above set out, your website must say whether and how you check that reviews come from '
         'real customers. If you show reviews from your Google Business Profile, add a short note saying they '
         'come from Google and whether, and how, you check them.</p></div>'
         '</div>'
         '<p class="where">For a longer read on structuring a carpentry site, see our article on '
         '<a href="https://webautonomos.es/blog/en/website-for-carpenters-and-renovations">websites for carpenters '
         'and renovation companies</a>.</p>'),
        ('services-carpenters', 'Your work', 'Which services should you highlight?',
         '<p class="legal-intro">Grouping your services by type of job, rather than listing everything on one '
         'long page, helps a visitor find the right section faster.</p>'
         '<div class="why-g">'
         '<div class="aud-c"><div class="aud-i" aria-hidden="true">\U0001FA91</div>'
         '<h3>Bespoke furniture and fitted wardrobes</h3>'
         '<p>Custom pieces built to a room&#8217;s exact dimensions are a different decision for a homeowner than a '
         'quick repair, so give them their own section.</p></div>'
         '<div class="aud-c"><div class="aud-i" aria-hidden="true">\U0001F373</div>'
         '<h3>Kitchen fitting</h3>'
         '<p>Units, worktops and installation: homeowners comparing kitchen fitters want to see finished projects '
         'before they request a quote.</p></div>'
         '<div class="aud-c"><div class="aud-i" aria-hidden="true">\U0001F6AA</div>'
         '<h3>Doors, windows and staircases</h3>'
         '<p>Smaller jobs bring in work between larger projects, so give them a clear place on your site '
         'too, and say whether you fit them yourself or work with a specialist installer.</p></div>'
         '<div class="aud-c"><div class="aud-i" aria-hidden="true">\U0001F333</div>'
         '<h3>Decking and garden carpentry</h3>'
         '<p>Decking, pergolas and other outdoor work are a different job from indoor carpentry, so show them '
         'apart from your kitchens and wardrobes, with a short caption naming the wood or material used.</p></div>'
         '</div>'),
        ('local-search-help', 'Local search', 'How your website helps you appear in local searches',
         '<p class="legal-intro">Getting found in your area is not only about the website itself: homeowners also '
         'post jobs on directories, ask around, or search directly for a trusted tradesperson nearby.</p>'
         '<div class="why-g">'
         '<div class="aud-c"><div class="aud-i" aria-hidden="true">\U0001F50D</div>'
         '<h3>Basic SEO, included in your price</h3>'
         '<p>Titles and copy written around your trade and your area, kept consistent with your Google Business '
         'Profile, come with your website at no extra cost.</p></div>'
         '<div class="aud-c"><div class="aud-i" aria-hidden="true">\U0001F4C8</div>'
         '<h3>SEO Local and your Google listing, if you want more</h3>'
         '<p>We also offer SEO Local for €15 + VAT a month, and managing your Google Business Profile for €29 + '
         'VAT a month (€49 + VAT to set one up if you do not have a listing yet).</p></div>'
         '<div class="aud-c"><div class="aud-i" aria-hidden="true">\U0001F4DA</div>'
         '<h3>Guides to go further</h3>'
         '<p>Our blog has practical guides on '
         '<a href="https://webautonomos.es/blog/en/how-to-rank-your-website-in-local-google">ranking your website '
         'locally</a>, <a href="https://webautonomos.es/blog/en/optimise-your-google-business-profile">optimising '
         'your Google Business Profile</a> and <a href="https://webautonomos.es/blog/en/how-to-get-more-google-'
         'reviews">getting more Google reviews</a>.</p></div>'
         '</div>'),
        ('common-mistakes', 'What to avoid', 'Common mistakes on carpenter websites',
         '<p class="legal-intro">These are the gaps that often make a carpenter&#8217;s website less '
         'effective.</p>'
         '<div class="cmp-c them" style="max-width:640px;margin:0 auto;"><ul>'
         '<li>No project photos, or an unsorted gallery mixing every type of job</li>'
         '<li>No clear service area, so people cannot tell whether you cover their town</li>'
         '<li>No quick way to ask for a quote: a phone number buried in a footer, or no WhatsApp link</li>'
         '<li>An incomplete legal notice, missing the NIF or NIE that the LSSI requires</li>'
         '</ul></div>'
         '<div class="aud-c" style="max-width:640px;margin:24px auto 0;"><h3>How we help you avoid them</h3>'
         '<p>Your website is built around your own project photos, names your trade and the areas you cover in '
         'its titles and copy, and comes with a contact form, a WhatsApp button and legal pages (legal notice, '
         'privacy and cookies). You see it before you pay anything, you can ask for as many changes as you want '
         'before it goes live, and if you decide not to go ahead, you pay nothing.</p></div>'),
        ('directory-vs-website', 'Compare', 'Your own website compared to a directory listing',
         '<p class="legal-intro">If you already get work through a trade directory, here is what changes once you '
         'also have your own website.</p>'
         '<div class="cmp-g">'
         '<div class="cmp-c them"><h3>A directory listing</h3><ul>'
         '<li>Enquiries often go through the platform, not straight to you</li>'
         '<li>Homeowners post a job and receive quotes from several local tradespeople, yours among them</li>'
         '<li>You do not control the layout, or your own domain name</li>'
         '<li>Your contact details and project pictures live on someone else&#8217;s platform</li>'
         '</ul></div>'
         '<div class="cmp-c us"><h3>Your own website</h3><ul>'
         '<li>Every enquiry goes directly to your email and WhatsApp</li>'
         '<li>Only your own portfolio and projects are shown, with no competitors on the same page</li>'
         '<li>Your own .es domain name, included for the first year</li>'
         '<li>Designed around your own project images and the towns you cover</li>'
         '</ul></div>'
         '</div>'),
        ('technical-basics', 'Behind the scenes', 'What runs behind your website',
         '<p class="legal-intro">Alongside the pages you and your customers see, a few technical basics come '
         'with every website we build.</p>'
         '<div class="why-g">'
         '<div class="aud-c"><div class="aud-i" aria-hidden="true">\U0001F512</div>'
         '<h3>Hosting, SSL and daily backups</h3>'
         '<p>Your site includes hosting, an SSL certificate, daily backups and technical maintenance, so you do '
         'not have to think about the technical side.</p></div>'
         '<div class="aud-c"><div class="aud-i" aria-hidden="true">\U0001F517</div>'
         '<h3>Links to your social profiles</h3>'
         '<p>We add links to your Facebook, Instagram or other social profiles on the website, so visitors can '
         'also see the work you post there.</p></div>'
         '<div class="aud-c"><div class="aud-i" aria-hidden="true">✏️</div>'
         '<h3>One change a month, included</h3>'
         '<p>Once your site is live, you can ask for one change a month at no extra cost: updating a price, '
         'adding new project pictures, or requesting other small changes.</p></div>'
         '</div>'),
    ],
    faq_t='Frequently asked questions',
    faq=[("What must a carpenter's website in Spain show?",
          "Under article 10 of the LSSI: your name, an address in Spain, email and other contact details, your NIF "
          "(your NIE if you are not Spanish), your Registro Mercantil details if you trade as a company, and whether "
          "any prices shown include VAT. Carpentry is not a regulated profession, so there is no Colegio number to "
          "add."),
         ("Do I have to give customers a written quote?",
          "It depends on the region. In the Comunitat Valenciana, Madrid and Catalonia, homeowners are entitled to a "
          "detailed written quote before work starts, with set information such as materials, labour rates, dates and "
          "the total with VAT. They can only waive it in their own handwriting, with their signature (Valencia and "
          "Madrid prescribe the wording, such as “Renuncio al presupuesto previo y autorizo la reparación”). In "
          "Catalonia the quote is due whenever the customer can't work out the price themselves, and in Valencia you "
          "must be able to prove you offered one. Other regions have their own rules: a written quote is always the "
          "safe choice."),
         ("Can I charge 10% VAT on carpentry work?",
          "Mainly for renovation or repair of a home: the customer is an individual using it privately (not rented "
          "out) or a comunidad de propietarios, the home is at least two years old, and the materials you supply cost "
          "no more than 40% of the price before VAT. The Tax Agency notes that double glazing usually exceeds that "
          "limit, and doors, windows, wardrobes or kitchen units supplied without fitting are always taxed at 21%. "
          "New-build or rehabilitation work contracted directly with the developer, including kitchen units and "
          "fitted wardrobes supplied and installed, can also be at 10%. The invoice should state the cost of "
          "materials, or that they don't exceed 40% of the price before VAT."),
         ("Do I need to register in the REA?",
          "If you work as a contractor or subcontractor on a construction site where there is subcontracting, you "
          "must be registered in the REA, unless you're self-employed with no employees (Ley 32/2006). If you work "
          "directly for a homeowner, it only applies if you subcontract part of the job. There is no obligation to "
          "show an REA number on your website."),
         ("What do I need to do about complaints?",
          "Let customers complain at least through the channel your contract with them started on, by post, by phone "
          "and by an electronic channel, and reply within 15 days at most: a national rule since 28 December 2025 "
          "(previously a month). "
          "Carry your region's official complaint forms. In Andalucía, businesses without premises must show a QR "
          "complaint poster on quotes, invoices and their website; in Madrid, if you have no premises open to the "
          "public, a notice that complaint forms are available goes wherever you make offers."),
         ("Can I show customer reviews on my website?",
          "Yes, if you say whether and how you check them. Since December 2025, reviews must relate to a job done in "
          "the 30 days before the review, and adding or commissioning fake reviews has been banned outright since "
          "2022."),
         ("Do my quotes have to be in Spanish?",
          "Pre-contract information, including quotes, must be given at least in Spanish, so a bilingual quote is the "
          "safe choice even for British customers. Invoices can be in any language, although the Tax Agency may ask "
          "for a translation. Your website comes in English and Spanish, plus up to two more languages, at no extra cost."),
         ("How should I organise my project photos on the website?",
          "Group them by type of job (kitchens, staircases, fitted wardrobes, doors) rather than in one long "
          "gallery, so a homeowner looking for a fitted wardrobe sees relevant work straight away. We use the "
          "photos on your Google Business Profile and any others you send us."),
         ("Do I need Google Business Profile management as well as a website?",
          "No, it's optional. Your website already comes with basic SEO: titles and copy built around your trade and "
          "your area. If you want more, we also manage Google Business Profiles for €29 + VAT a month (€49 + VAT to "
          "set one up if you don't have one yet)."),
         ("How much does a website cost?",
          "€15 + VAT a month with no setup fee and no lock-in, or a one-off €349 + VAT, with the same services: "
          "design, hosting, a domain name for the first year, legal pages and one change a month. English and "
          "Spanish are included, and the demo is free."),
         ("Do I need my own website if I'm already on a trade directory?",
          "You don't have to choose: keep the directory profile for extra enquiries, and use your own website as "
          "the place customers land when they search for your business by name, with your whole portfolio and a "
          "direct way to contact you."),
         ("How do homeowners usually find a carpenter or joiner?",
          "Often by word of mouth, through a recommendation from family, friends or another trusted local "
          "tradesperson, and they may then look you up online before getting in touch. Others simply search for a "
          "joiner in their area. A website built around your own projects and service area helps in both cases: "
          "someone who heard about you can check your work there, and someone searching can find it."),
         ("Can I show before-and-after shots of a finished project?",
          "Yes, before-and-after shots of a kitchen fitting or a finished staircase can help a homeowner compare "
          "carpenters, as long as they're genuine pictures from your own projects. We build your gallery around "
          "whatever pictures you send us.")],
    final_t='See your website before you pay a thing',
    final_sd="Free demo within 24 hours, with your projects and legal pages. No setup fee, no lock-in.",
)

MENU_SOURCES = {
    'fr': [
        ("Code de l'artisanat, qualité d'artisan (Légifrance)",
         'https://www.legifrance.gouv.fr/codes/section_lc/LEGITEXT000006075116/LEGISCTA000047362410/'),
        ("Assurance décennale (Service-public)", 'https://entreprendre.service-public.gouv.fr/vosdroits/F2034'),
        ("MaPrimeRénov' au 1er septembre 2026 (Service-public)",
         'https://www.service-public.gouv.fr/particuliers/actualites/A18332'),
        ("Publicité et rénovation énergétique : référence obligatoire à France Rénov'",
         'https://france-renov.gouv.fr/actualites/publicite-pour-la-renovation-energetique-obligation-desormais-de-faire-reference-au'),
        ("Médiateur de la consommation (Service-public)", 'https://entreprendre.service-public.gouv.fr/vosdroits/F33338'),
        ("Arrêté du 24 janvier 2017, dépannage dans le bâtiment (Légifrance)",
         'https://www.legifrance.gouv.fr/loda/id/JORFTEXT000033935513'),
        ("Avis en ligne (DGCCRF)", 'https://www.economie.gouv.fr/dgccrf/les-fiches-pratiques/avis-en-ligne-attention-aux-faux-commentaires'),
    ],
    'en': [
        ("LSSI, art. 10 (BOE)", 'https://www.boe.es/buscar/act.php?id=BOE-A-2002-13758'),
        ("Spanish consumer law, TRLGDCU (BOE)", 'https://www.boe.es/buscar/act.php?id=BOE-A-2007-20555'),
        ("VAT on home repairs, FAQ (Tax Agency)",
         'https://sede.agenciatributaria.gob.es/Sede/iva/iva-operaciones-inmobiliarias/preguntas-frecuentes-sobre-obras-reparaciones-inmuebles.html'),
        ("Home renovations (Comunidad de Madrid)", 'https://www.comunidad.madrid/consumo/reformas-hogar'),
        ("Complaint rules in Andalucía (Consumo Responde)",
         'https://www.consumoresponde.es/art%C3%ADculos/obligaciones_de_las_empresas_en_materia_de_quejas_y_reclamaciones_en_andalucia'),
        ("Ley 32/2006 on construction subcontracting (BOE)", 'https://www.boe.es/buscar/act.php?id=BOE-A-2006-18205'),
    ],
}

# ═════════════════════════ KINÉSITHÉRAPEUTES ET PHYSIOTHERAPISTS ══════════
PRIX_FR_SANTE = ("Prix hors taxes. Vous exercez en France : donnez-nous votre numéro de TVA intracommunautaire, "
                 "obligatoire pour cet achat même si vos soins sont exonérés. La facture est alors émise sans TVA et "
                 "vous autoliquidez la TVA française de 20 %, que vous ne récupérez pas, soit 18 € par mois pour "
                 "l'abonnement. Sans ce numéro, ou si vous exercez en Espagne, l'IVA espagnole de 21 % s'ajoute. Nom de "
                 "domaine inclus la première année, puis environ 12 €/an.")
PRIX_EN_SANTE = ("Prices exclude VAT (21% IVA on the mainland and the Balearics; the Canary Islands, Ceuta and Melilla "
                 "have their own taxes). Your health services are VAT-exempt, so you usually can't deduct it: on the "
                 "mainland and the Balearics the monthly price comes to €18.15. Domain name included for the first "
                 "year, then about €12/year.")

KINE = {}
KINE['fr'] = dict(
    html_lang='fr', og_locale='fr_FR', unit='mois', area=['FR', 'ES'],
    title="Site internet pour kinésithérapeute : 15 €/mois",
    description="Site internet pour kinésithérapeute pensé pour le code de déontologie : RPPS, honoraires, "
                "spécificités reconnues, sans référencement interdit. Démo gratuite en 24 h, 15 €/mois HT.",
    service_name="Création de site internet pour masseurs-kinésithérapeutes",
    audience="Masseurs-kinésithérapeutes libéraux",
    crumb_home='Accueil', crumb='Kinésithérapeutes',
    badge='Masseurs-kinésithérapeutes libéraux',
    h1="Un site internet pour <em>kinésithérapeutes</em>, pensé pour votre code de déontologie",
    lede="Votre cabinet, vos spécificités, vos honoraires et votre agenda en ligne, présentés selon les "
         "recommandations de l'Ordre : un site qui informe, sans rien de commercial. Nous l'écrivons pour vous, vous "
         "validez chaque contenu, et la démo est gratuite en 24 heures.",
    pills=["Construit selon les recommandations de l'Ordre", 'RPPS et honoraires affichés', 'Démo gratuite en 24 h'],
    cta='Recevoir ma démo gratuite', cta2='Ce que le code impose',
    brief_t='En bref',
    brief="WebAutonomos crée des sites internet pour les masseurs-kinésithérapeutes libéraux, en France et en "
          "Espagne. Le site présente votre cabinet, vos spécificités reconnues par l'Ordre, vos honoraires et vos modes "
          "de paiement, avec votre numéro RPPS et votre numéro d'Ordre, comme l'exigent le code de déontologie et les "
          "recommandations de l'Ordre. Il reste "
          "informatif : pas de témoignages, pas de comparaison, et pas de référencement pour passer devant vos "
          "confrères, que le code interdit. Le site coûte <strong>15 € HT par mois</strong> sans frais d'installation "
          "ni engagement, ou <strong>349 € HT en paiement unique</strong>, et la démo est prête en 24 heures.",
    legal_id='regles', legal_ey='Le code de déontologie', legal_t="Ce que votre site doit respecter",
    legal_intro="Depuis 2020, un kinésithérapeute peut informer le public librement, y compris sur un site internet. "
                "Mais cette information est encadrée par le code de déontologie et par les recommandations de l'Ordre. "
                "Voici l'essentiel.",
    legal_cols=('Sujet', 'Texte', 'Ce que ça change sur votre site'),
    legal_rows=[
        ('Le titre', 'Code de la santé publique, art. L4323-5 ; Code pénal, art. 433-17',
         "« Masseur-kinésithérapeute » est un titre protégé ; l'usurper est puni d'un an de prison et de 15 000 € "
         "d'amende. L'Ordre traite « kiné », « kinésithérapeute » et « physiothérapeute » comme des dérivés du titre."),
        ('Ce que vous pouvez dire', 'Code de la santé publique, art. R4321-67-1',
         "Vos compétences, votre parcours et vos conditions d'exercice, de façon loyale et honnête : pas de témoignages "
         "de tiers, pas de comparaison avec d'autres kinés, pas d'incitation à des soins inutiles. L'Ordre demande un "
         "site sans caractère promotionnel ni lien commercial."),
        ('Référencement', 'Code de la santé publique, art. R4321-123',
         "Il est interdit d'obtenir, contre paiement ou par tout autre moyen, un référencement qui fasse apparaître "
         "votre site en priorité dans les résultats de recherche. L'Ordre étend l'interdiction à tout service, payant "
         "ou non, qui vise ce résultat."),
        ('Honoraires', 'Code de la santé publique, art. R4321-98',
         "Un site qui présente votre activité doit indiquer vos honoraires, les modes de paiement acceptés et les "
         "obligations d'accès aux soins sans discrimination, de façon claire, honnête, précise et non comparative. "
         "Des fourchettes sont possibles si vous en donnez les critères."),
        ('Spécificités et diplômes', "Code de la santé publique, art. R4321-67-1 ; avis du CNO n° 2023-02 ; "
                                     "recommandations de l'Ordre",
         "Seuls les diplômes universitaires reconnus par l'Ordre et les spécificités de sa liste peuvent figurer, avec "
         "leur libellé exact, par exemple « Kinésithérapie du sport ». Pas de « spécialiste », ni de marque ou de "
         "méthode présentée comme une spécificité."),
        ('Accès direct', 'Code de la santé publique, art. L4321-1',
         "Sans prescription, si vous exercez en établissement de santé ou médico-social, en maison ou centre de "
         "santé, en équipe de soins primaires ou spécialisés, ou en CPTS dans l'un des 20 départements de "
         "l'expérimentation (déclaration à l'ARS) : 8 séances au plus sans diagnostic médical. À n'indiquer que si "
         "vous êtes concerné, avec ces limites."),
        ('Mentions obligatoires', "Recommandations de l'Ordre ; LCEN, art. 1-1 et 19 ; Code de commerce, art. R526-27",
         "Numéro RPPS et numéro d'Ordre, titre, pays d'obtention, Ordre d'inscription et code de déontologie applicable, "
         "téléphone, e-mail et accessibilité du cabinet, nom précédé ou suivi de « EI » si vous êtes entrepreneur "
         "individuel, directeur de la publication et hébergeur."),
    ],
    legal_note="Pour un agenda en ligne, l'Ordre demande qu'il ne comporte aucune zone de texte libre ; un outil qui "
               "stocke des données de santé doit passer par un hébergeur certifié HDS. Informations générales à jour en "
               "septembre 2026, qui ne remplacent pas l'avis de votre conseil départemental de l'Ordre.",
    legal_we_t='Ce que nous mettons en place',
    legal_we=["Votre numéro RPPS, votre numéro d'Ordre, vos coordonnées, l'accessibilité du cabinet et les mentions "
              "légales complètes, avec le code de déontologie applicable",
              "Vos honoraires et modes de paiement sur une page claire, sans comparaison",
              "Seulement les spécificités et diplômes reconnus par l'Ordre, avec leur libellé exact",
              "Un lien vers votre agenda en ligne, et un formulaire sans champ libre sur l'état de santé",
              "Un site informatif, sans témoignages ni liens commerciaux, et sans prestation de référencement pour passer "
              "devant vos confrères"],
    spain_note="<strong>Vous exercez en Espagne ?</strong> Les règles changent : inscription obligatoire au Colegio de "
               "Fisioterapeutas, numéro de colegiado sur le site, cabinet autorisé comme centre sanitaire avec son "
               "numéro d'enregistrement dans la publicité, et dans certaines régions, comme Murcie, autorisation "
               "préalable de la publicité, site compris. Nous connaissons aussi ces règles : "
               "<a href=\"/fr/site-internet-francophones-espagne\">site internet pour francophones en Espagne</a>.",
    sources_t='Sources',
    why_ey='Pourquoi nous', why_t="Pensé pour les kinésithérapeutes",
    why=[('📋', "Les mentions de l'Ordre en place", "RPPS, numéro d'Ordre, honoraires et modes de paiement : ce que le "
                                                  "code et l'Ordre exigent d'un site."),
         ('🏷️', 'Des spécificités reconnues', "Seules les spécificités de la liste de l'Ordre, avec leur libellé exact, "
                                             "comme « Kinésithérapie du sport »."),
         ('📅', 'Un agenda sans champ libre', "Un lien vers votre prise de rendez-vous en ligne, sans zone de texte "
                                             "libre, comme le recommande l'Ordre."),
         ('⚖️', 'Rien de ce que le code interdit', "Pas de témoignages, pas de comparaison, pas de référencement pour passer "
                                            "devant vos confrères : nous ne vous le vendrons pas.")],
    where_t='En France et en Espagne',
    where="Nous travaillons à distance, en français, par e-mail, WhatsApp et visioconférence : que votre cabinet soit à "
          "Lille, à Toulouse ou à Alicante, rien ne change.",
    sect_t='Pour qui',
    sectors=['💆 Kinés libéraux', '🏃 Kinésithérapie du sport', '🫁 Kinésithérapie respiratoire',
             '🤰 Kinésithérapie en pelvi-périnéologie', '🧓 Kinésithérapie en gériatrie', '👶 Kinésithérapie en pédiatrie',
             '🏥 Cabinets de groupe', '🦴 Kinés ostéopathes'],
    how_t='Votre site en trois étapes',
    steps=[('Vous décrivez votre cabinet', "Vos spécificités reconnues, vos horaires, votre agenda en ligne, votre "
                                          "ville : deux minutes suffisent."),
           ('Nous préparons votre démo', "En moins de 24 heures, avec vos honoraires, votre RPPS et vos mentions "
                                        "légales."),
           ('Vous décidez', "Vous relisez et validez chaque contenu, et demandez les modifications que vous voulez. Si "
                           "le site vous plaît, il est mis en ligne ; sinon, vous ne payez rien.")],
    price_note=PRIX_FR_SANTE,
    faq_t='Questions fréquentes',
    faq=[("Un kinésithérapeute a-t-il le droit d'avoir un site internet ?",
          "Oui. Depuis la réforme de 2020, le code de déontologie permet d'informer le public par tout moyen, y compris "
          "sur un site internet, sur vos compétences, votre parcours et vos conditions d'exercice (art. R4321-67-1). "
          "L'information doit être loyale et honnête et tenir compte des recommandations de l'Ordre, qui demande un site "
          "sans caractère promotionnel ni commercial."),
         ("Mes honoraires doivent-ils figurer sur mon site ?",
          "Oui. Le code de déontologie (art. R4321-98) impose à un kiné qui présente son activité, notamment sur un site, "
          "d'y indiquer ses honoraires, les modes de paiement acceptés et les obligations d'accès aux soins sans "
          "discrimination. Des fourchettes sont possibles si vous en précisez les critères."),
         ("Puis-je payer pour être mieux référencé sur Google ?",
          "Non. L'article R4321-123 interdit d'obtenir, contre paiement ou par tout autre moyen, un référencement qui "
          "fasse apparaître votre site en priorité, et l'Ordre étend l'interdiction à tout service qui vise ce résultat. "
          "C'est pourquoi nous ne vendons ni référencement ni publicité aux kinés : le site est clair et bien construit, "
          "et Google l'indexe normalement."),
         ("Puis-je afficher les avis de mes patients ?",
          "Non : votre communication ne doit pas faire appel à des témoignages de tiers (art. R4321-67-1). Afficher ou "
          "intégrer des avis de patients sur votre site revient à utiliser ces témoignages."),
         ("Puis-je écrire « kiné du sport » ou « spécialiste » ?",
          "Seulement les spécificités reconnues par l'Ordre, avec leur libellé exact : « Kinésithérapie du sport », par "
          "exemple, si vous avez un diplôme reconnu ou au moins 80 heures de formation sur quatre ans. Le mot "
          "« spécialiste » est à éviter : l'Ordre parle d'exercice préférentiel."),
         ("Puis-je indiquer que les patients peuvent venir sans ordonnance ?",
          "Seulement si vous exercez en établissement de santé ou médico-social, en maison ou centre de santé, en "
          "équipe de soins primaires ou spécialisés, ou en CPTS dans l'un des 20 départements de l'expérimentation. "
          "Dans ce cas, précisez les limites : 8 séances au plus sans diagnostic médical, avec un bilan et un compte "
          "rendu adressés au patient et à son médecin traitant et versés au DMP."),
         ("Je suis aussi ostéopathe : comment l'indiquer ?",
          "Si vous avez le droit d'utiliser le titre, le site doit mentionner votre diplôme d'ostéopathie ainsi que votre "
          "diplôme d'État de masseur-kinésithérapeute, comme sur votre plaque."),
         ("Combien coûte un site pour kinésithérapeute ?",
          "15 € HT par mois sans frais d'installation ni engagement, ou 349 € HT en paiement unique, avec les mêmes "
          "services : conception, hébergement, nom de domaine la première année, mentions légales et une modification "
          "par mois. La démo est gratuite.")],
    final_t='Voyez votre site avant de payer quoi que ce soit',
    final_sd="Démo gratuite en 24 heures, honoraires et mentions obligatoires compris. Sans frais d'installation, sans "
             "engagement.",
    extra=[('contenu-site', 'Contenu du site', "Site internet kinésithérapeute : ce qu'il doit contenir",
            '<p class="legal-intro">Notre création de site internet pour kinésithérapeutes comprend la rédaction des '
            "textes à partir de vos informations, l'hébergement web et une modification par mois après la mise en "
            "ligne. Voici, concrètement, ce que vos pages contiennent.</p>"
            '<div class="legal-we"><ul>'
            "<li><span>Une présentation de votre cabinet et de votre parcours, sans témoignage ni comparaison</span></li>"
            "<li><span>Vos honoraires, vos modes de paiement et, le cas échéant, vos spécificités reconnues par le "
            "Conseil national de l'Ordre, présentés selon les règles rappelées plus haut</span></li>"
            "<li><span>Votre adresse, vos horaires et l'accessibilité du cabinet, avec un formulaire de contact sans "
            "champ libre sur l'état de santé et un bouton WhatsApp</span></li>"
            "<li><span>Un lien vers vos réseaux sociaux professionnels, si vous en avez</span></li>"
            "<li><span>Vos mentions légales complètes : numéro RPPS, numéro d'Ordre, hébergeur et directeur de la "
            "publication, comme le demandent la LCEN et les recommandations de l'Ordre</span></li>"
            '<li><span>Votre nom de domaine, en .fr si vous exercez en France, inclus la première année puis environ '
            '12 €/an, qui reste à vous si vous changez de prestataire</span></li>'
            '</ul></div>'
            '<p class="legal-intro"><strong>Création de site internet pour kiné : le même prix, en une ou plusieurs '
            "langues.</strong> Vous choisissez jusqu'à quatre langues au total, sans supplément, parmi le français, "
            "l'espagnol, l'anglais, le catalan, le valencien, le galicien et le basque : le prix reste de 15 € HT par "
            "mois sans frais d'installation ni engagement, ou de 349 € HT en paiement unique.</p>")],
)

KINE['en'] = dict(
    html_lang='en', og_locale='en_GB', unit='month', area=['ES'],
    title="Websites for physiotherapists in Spain: €15/month",
    description="Websites for English-speaking physiotherapists in Spain, built around Spanish Colegio, "
                "health-advertising and practice rules. Free demo in 24h, €15/month + VAT.",
    service_name="Web design for physiotherapists in Spain",
    audience="English-speaking physiotherapists practising in Spain",
    crumb_home='Home', crumb='Physiotherapists',
    badge='For physiotherapists in Spain',
    h1="Websites for <em>physiotherapists</em> in Spain",
    lede="Your practice, your treatments and how to book, in English and Spanish, written with Spain's rules on "
         "Colegio details, health advertising and practice authorisation in mind. We write it for you, you approve "
         "every word, and your free demo is ready within 24 hours.",
    pills=['English and Spanish included', 'Written with Spanish rules in mind', 'Free demo in 24 hours'],
    cta='Get my free demo', cta2='What Spanish rules require',
    brief_t='In short',
    brief="WebAutonomos builds websites for English-speaking physiotherapists practising in Spain. We write the copy in "
          "English and Spanish, plus up to two more languages if you need them, at no extra cost, show your Colegio, colegiado number and practice registration number, "
          "and keep promises of cure and patient testimonials off the site, as Spanish health-advertising rules "
          "require. Your site describes the treatments you offer, from manual therapy to rehabilitation, in plain "
          "language. It costs <strong>€15 + VAT per month</strong> "
          "with no setup fee and no lock-in, or a <strong>one-off €349 + VAT</strong>. We work with you in English, "
          "and your demo is ready within 24 hours.",
    legal_id='rules', legal_ey='Spanish rules', legal_t='What your website has to get right in Spain',
    legal_intro="Physiotherapy is a regulated health profession in Spain. That shapes what your website must show and "
                "what it may say. These are the points that matter.",
    legal_cols=('Topic', 'Law', 'What it means for your website'),
    legal_rows=[
        ('Colegio and legal notice', 'Ley 2/1974, art. 3; LSSI (Ley 34/2002), art. 10',
         "Membership of a Colegio de Fisioterapeutas is compulsory to practise. Your site must show your Colegio and "
         "colegiado number, your qualification, the country that issued it and any recognition in Spain, the "
         "professional rules that apply to you, and your NIF or NIE."),
        ('Practice authorisation', 'RD 1277/2003, art. 3 and 6.2',
         "A physiotherapy practice (usually type C.2.2, with the physiotherapy unit U.59) needs prior authorisation "
         "from your regional health department. Any "
         "advertising that suggests health care, your website included, must show the registration number it gives "
         "you. Madrid also requires an authorisation for home-visit-only practice."),
        ('Health advertising', 'Ley 44/2003, art. 44; RD 1907/1996, art. 4',
         "Advertising must be objective, prudent and truthful: no assurances of relief or cure, no patient "
         "testimonials used to attract clients, and no claims without scientific evidence."),
        ('Code of ethics', 'Código Deontológico of the Consejo General de Colegios de Fisioterapeutas, art. 76–81',
         "Present yourself only as a “Fisioterapeuta”: adding another title, such as “and osteopath”, goes against the "
         "code. Show your name, colegiado number and Colegio in your adverts, and don't attract clients with "
         "price-based advertising."),
        ('Foreign qualifications', 'RD 581/2017; RD 889/2022; RDL 38/2020, art. 4; Código Penal, art. 403',
         "An EU qualification is recognised by the Ministry of Health, on application; a new application for a UK "
         "one goes through homologation by the Ministry of Science, Innovation and Universities, with Spanish at B2 "
         "level. Practising without a title recognised in Spain is a criminal offence."),
        ('Data protection', 'GDPR, art. 9; LOPDGDD, art. 34',
         "Health details in a contact form are special-category data, so ask only for what you need. A physiotherapist "
         "working alone doesn't need a data protection officer; a clinic does."),
    ],
    legal_note="Physiotherapy is VAT-exempt when it treats or prevents an injury or illness; relaxing or beauty "
               "massage outside a treatment is taxed at 21%. Some regions, such as Murcia, also require prior "
               "authorisation of health advertising, websites included. This is general "
               "information as of September 2026, not legal advice: check with your Colegio and your regional "
               "health department.",
    legal_we_t='What we set up for you',
    legal_we=["Your Colegio, colegiado number, qualification and a link to the code of ethics, plus your NIF or NIE",
              "Your practice registration number wherever the site presents your services",
              "Copy written without promises of cure, patient testimonials or price-led offers",
              "A link to your booking tool, WhatsApp or phone, and a contact form that asks only what it needs",
              "Your site in up to four languages, English and Spanish included, at no extra cost"],
    spain_note='<strong>Working in the UK instead?</strong> UK rules are different. See '
               '<a href="https://webautonomos.es/en/physiotherapy-website-design">physiotherapy website '
               'design for UK clinics</a>.',
    sources_t='Sources',
    why_ey='Why us', why_t='Built for physiotherapists who work in English',
    why=[('💬', 'We speak your language', "Email, WhatsApp or video call in English: no need to decode Spanish legal "
                                         "or technical jargon."),
         ('🌍', 'Up to four languages, one price', "English, Spanish and up to two more at no extra cost, so local "
                                           "patients find you as easily as expats do."),
         ('📋', 'Colegio details in place', "Colegio, colegiado number and practice registration details shown the way "
                                           "Spain's rules expect."),
         ('📅', 'Easy to book', "A clear button to your online calendar, WhatsApp or phone, with clinic or home visits "
                               "stated plainly.")],
    where_t='Anywhere in Spain',
    where="Costa Blanca, Costa del Sol, Valencia, Mallorca, Barcelona, Madrid or the Canary Islands: we work remotely, "
          "so where your practice is makes no difference.",
    sect_t='Who it is for',
    sectors=['💆 Physiotherapists', '🏃 Sports physiotherapy', '🦴 Musculoskeletal', '🧓 Older adults',
             '🤰 Women’s health', '👶 Paediatrics', '🏠 Home visits', '🏥 Clinics'],
    how_t='Your website in three steps',
    steps=[('Tell us about your practice', 'Your treatments, clinic or home visits, your town: it takes two minutes.'),
           ('We build your demo', 'Within 24 hours, with your copy in English and Spanish and your legal pages.'),
           ('You decide', "You check every word and ask for any changes you want. If you like it, it goes live; if "
                         "not, you pay nothing.")],
    price_note=PRIX_EN_SANTE,
    extra=[
        ('on-your-website', 'On your website', 'What patients look for on a physiotherapy website',
         '<p class="legal-intro">When someone searches for a physiotherapist, they check a handful of things before '
         'getting in touch: what you treat, whether they can trust you, and how to reach you. These are the parts '
         'of your website that answer those questions.</p>'
         '<div class="why-g">'
         '<div class="aud-c"><div class="aud-i" aria-hidden="true">📝</div>'
         '<h3>Your treatments, in plain language</h3>'
         '<p>Manual therapy, sports physiotherapy, rehabilitation after an injury or an operation: described so a '
         'new patient understands what kind of session to expect, without a promise of relief or cure.</p></div>'
         '<div class="aud-c"><div class="aud-i" aria-hidden="true">🎓</div>'
         '<h3>Your training and registration</h3>'
         '<p>Your qualification and training, your years in practice, and your Colegio and colegiado number (see '
         '<a href="#rules">the rules above</a>), so a patient checking your credentials finds them straight '
         'away.</p></div>'
         '<div class="aud-c"><div class="aud-i" aria-hidden="true">✉️</div>'
         '<h3>How to get in touch</h3>'
         '<p>Your contact form asks only for what you need to reply, never for a patient&#8217;s medical history '
         'or the reason for the visit.</p></div>'
         '<div class="aud-c"><div class="aud-i" aria-hidden="true">📱</div>'
         '<h3>A site that works on any screen</h3>'
         '<p>Many patients look for a physiotherapist from their phone, so the design has to hold up there as '
         'well as on a desktop.</p></div>'
         '</div>'),
        ('treatment-areas', 'Areas of practice', 'Areas physiotherapists in Spain often cover',
         '<p class="legal-intro">Your website copy can set out the areas you work in — from sports and '
         'musculoskeletal therapy to paediatric and older-adult care — so a patient searching for a specific type '
         'of treatment recognises your practice.</p>'
         '<div class="aud-g">'
         '<div class="aud-c"><div class="aud-i" aria-hidden="true">🏃</div>'
         '<h3>Sports physiotherapy</h3>'
         '<p>Treatment after a sports injury, from the first assessment to a graded return to training.</p></div>'
         '<div class="aud-c"><div class="aud-i" aria-hidden="true">🦴</div>'
         '<h3>Musculoskeletal and manual therapy</h3>'
         '<p>Hands-on techniques for the neck, back and joints, alongside the exercises a patient does between '
         'sessions.</p></div>'
         '<div class="aud-c"><div class="aud-i" aria-hidden="true">🧠</div>'
         '<h3>Neurological physiotherapy</h3>'
         '<p>Rehabilitation for patients living with a neurological condition, with a focus on movement and daily '
         'life.</p></div>'
         '<div class="aud-c"><div class="aud-i" aria-hidden="true">🤰</div>'
         '<h3>Women’s health and pelvic physiotherapy</h3>'
         '<p>Pelvic floor treatment, including during pregnancy and after childbirth.</p></div>'
         '<div class="aud-c"><div class="aud-i" aria-hidden="true">👶</div>'
         '<h3>Paediatric physiotherapy</h3>'
         '<p>Treatment adapted to a child&#8217;s stage of development.</p></div>'
         '<div class="aud-c"><div class="aud-i" aria-hidden="true">🧓</div>'
         '<h3>Physiotherapy for older adults</h3>'
         '<p>Treatment focused on mobility, balance and reducing the risk of falls.</p></div>'
         '<div class="aud-c"><div class="aud-i" aria-hidden="true">🏠</div>'
         '<h3>Home visits</h3>'
         '<p>Stated plainly on your site, for patients who cannot travel to a clinic.</p></div>'
         '</div>'),
        ('getting-found', 'Local search', 'How your website helps patients find you',
         '<p class="legal-intro">Getting found by someone searching for a physiotherapist near them depends on '
         'more than the design: your copy and your Google Business Profile count too.</p>'
         '<div class="aud-g">'
         '<div class="aud-c"><div class="aud-i" aria-hidden="true">🔍</div>'
         '<h3>Basic SEO, included in your price</h3>'
         '<p>Titles and copy written around your treatments and your area — searches like “physiotherapist in '
         'Alicante” or “sports physio Valencia” — kept consistent with your Google Business Profile, at no extra '
         'cost.</p></div>'
         '<div class="aud-c"><div class="aud-i" aria-hidden="true">📈</div>'
         '<h3>SEO Local and your Google listing, if you want more</h3>'
         '<p>We also offer SEO Local for €15 + VAT a month, and managing your Google Business Profile for €29 + '
         'VAT a month (€49 + VAT to set one up if you do not have a listing yet).</p></div>'
         '<div class="aud-c"><div class="aud-i" aria-hidden="true">📚</div>'
         '<h3>Guides to go further</h3>'
         '<p>Our blog has practical guides on <a href="https://webautonomos.es/blog/en/how-to-rank-your-website-'
         'in-local-google">ranking your website locally</a> and <a href="https://webautonomos.es/blog/en/'
         'optimise-your-google-business-profile">optimising your Google Business Profile</a>.</p></div>'
         '<div class="aud-c"><div class="aud-i" aria-hidden="true">🔤</div>'
         '<h3>“Physiotherapy” or “physical therapy”?</h3>'
         '<p>British and Irish English say “physiotherapist”, American English “physical therapist”: we write '
         'your copy with the term your patients use.</p></div>'
         '</div>'),
        ('common-gaps', 'What to avoid', 'Common gaps on physiotherapy websites',
         '<p class="legal-intro">These are the gaps that often make a physiotherapy website less effective, or '
         'leave it short of what Spanish rules require.</p>'
         '<div class="cmp-c them" style="max-width:640px;margin:0 auto;"><ul>'
         '<li>No Colegio or colegiado number, or a registration number missing from an authorised practice</li>'
         '<li>A single vague page listing every treatment with no detail on what each one involves</li>'
         '<li>No clear way to book or ask a question: a phone number buried in a footer, no WhatsApp link</li>'
         '<li>Stock photos and generic text that could belong to any clinic, in any country</li>'
         '</ul></div>'
         '<div class="aud-c" style="max-width:640px;margin:24px auto 0;"><h3>How we help you avoid them</h3>'
         '<p>Your website sets out your Colegio and registration details in the right place, describes your '
         'treatments one by one, and comes with a contact form, a WhatsApp button and legal pages (legal notice, '
         'privacy policy and cookie policy). Whether you work alone or in a clinic team, patients can see what you '
         'offer, how to reach you and what to expect. You see your demo before you pay anything, ask for the '
         'changes you want, and if you decide not to go ahead, you pay nothing.</p></div>'),
        ('how-we-work', 'Working with us', 'What working with our team looks like',
         '<p class="legal-intro">Buying a website online can feel abstract, especially when English is your '
         'first language and legal Spanish is not. Here is how we work with you, before and after your site goes '
         'live.</p>'
         '<div class="aud-g">'
         '<div class="aud-c"><div class="aud-i" aria-hidden="true">📧</div>'
         '<h3>No meeting required</h3>'
         '<p>You send us the details by email or WhatsApp, in English, and we come back with questions if we '
         'need them.</p></div>'
         '<div class="aud-c"><div class="aud-i" aria-hidden="true">🗓️</div>'
         '<h3>A demo within 24 hours</h3>'
         '<p>Your demo is ready within 24 hours. Before your site goes live, you ask for any changes you want, '
         'and we reply the same day.</p></div>'
         '<div class="aud-c"><div class="aud-i" aria-hidden="true">🔐</div>'
         '<h3>HTTPS and legal pages from day one</h3>'
         '<p>Your site comes with an SSL certificate (HTTPS), daily backups and its legal pages: legal notice, '
         'privacy policy and cookie policy.</p></div>'
         '<div class="aud-c"><div class="aud-i" aria-hidden="true">🔄</div>'
         '<h3>Available if things change</h3>'
         '<p>New treatments, a change of address, different opening hours: one change a month is included, in '
         'every language on your site, and you reach us by email or WhatsApp, with a reply the same day.</p></div>'
         '</div>'),
    ],
    faq_t='Frequently asked questions',
    faq=[("Can I practise as a physiotherapist in Spain with a UK degree?",
          "Only once it is recognised. New applications for a UK degree now go through homologation by the Ministry "
          "of Science, Innovation and Universities, which requires Spanish at B2 level. Recognitions already granted, "
          "including those given under Spain's Brexit transition rules to people who began their studies before 2021, "
          "keep their effect. After that you still need to join a Colegio and practise from an authorised centre."),
         ("What must my website show?",
          "Under article 10 of the LSSI: your name, address and contact details, your NIF or NIE, your Colegio and "
          "colegiado number, your qualification and the country that issued it, any recognition in Spain, and the "
          "professional rules that apply to you. If you run an authorised practice, add its authorisation details, "
          "the regional health department that supervises it and its registration number; if you trade through a "
          "company, add its Registro Mercantil details."),
         ("Does my practice need to be registered as a health centre?",
          "Yes. A physiotherapy practice needs prior authorisation from the regional health department and goes on the "
          "regional register (RD 1277/2003). Madrid also requires an authorisation if you only do home visits. The "
          "registration number must appear in any advertising that suggests health care, including your website."),
         ("Can I show patient reviews or testimonials?",
          "Avoid them: Spanish health-advertising rules ban patient testimonials used to attract clients (RD "
          "1907/1996, art. 4.7). We build trust with your qualifications, your approach and practical details "
          "instead."),
         ("Can I call myself a physiotherapist and osteopath?",
          "Your Colegio's code of ethics asks you to present yourself only as a “Fisioterapeuta”, without adding another "
          "title. You can mention osteopathy among the techniques you are trained in. Osteopathy isn't a regulated "
          "profession in Spain."),
         ("Can a sports massage therapist offer treatment?",
          "No. Sports massage therapist and quiromasajista are not regulated health professions, so they can offer "
          "wellness or relaxation services but can't claim to treat or rehabilitate injuries. Only authorised health "
          "centres may use wording that suggests health care."),
         ("Is physiotherapy VAT-exempt?",
          "Yes, when the service treats or prevents an illness or injury and is provided by a health professional. "
          "Relaxing, beauty or slimming massage outside a treatment is taxed at 21%. Because your health services are "
          "exempt, you usually can't deduct the VAT on our invoice (only in part if you also sell taxed services or "
          "products)."),
         ("Do you set up online scheduling or appointment reminders?",
          "No. We don't integrate an appointment or scheduling system, and we don't send automated SMS or email "
          "reminders. We link to WhatsApp, your phone number or a scheduling tool you already use, and enquiries "
          "also arrive by email through your contact form."),
         ("Does my website need approval before it goes live?",
          "It depends on your region. Some regions, such as Murcia, require prior authorisation of health "
          "advertising, websites included: check with your regional health department before your site goes "
          "live."),
         ("Can I list areas such as sports or paediatric physiotherapy on my website?",
          "Yes. You don't need a separate licence for each area, but list only training you have actually "
          "completed and describe your experience in your own words. Don't add a title such as “specialist”: "
          "your Colegio's code of ethics asks you to present yourself only as a “Fisioterapeuta”."),
         ("Does it matter if I work alone or as part of a clinic team?",
          "Mostly in practical ways. A clinic site usually gives each physiotherapist a short profile with their "
          "own training and colegiado number, while a solo site focuses on one person. One rule does differ: a "
          "clinic needs a data protection officer, a physiotherapist working alone doesn't (LOPDGDD, art. 34)."),
         ("How much does a website cost?",
          "€15 + VAT a month with no setup fee and no lock-in, or a one-off €349 + VAT, with the same services: design, "
          "hosting, a domain name for the first year, legal pages and one change a month. English and Spanish are "
          "included, and the demo is free.")],
    final_t='See your website before you pay a thing',
    final_sd="Free demo within 24 hours, copy and legal pages included. No setup fee, no lock-in.",
)

KINE_SOURCES = {
    'fr': [
        ("Code de déontologie des masseurs-kinésithérapeutes (Ordre, 2026)",
         'https://deontologie.ordremk.fr/wp-content/uploads/2026/02/code-de-deontologie-avec-sommaire.pdf'),
        ("Recommandations de l'Ordre sur la communication",
         'https://www.ordremk.fr/wp-content/uploads/2025/04/guide_recommandationscom_cnomk_2024.pdf'),
        ("Spécificités d'exercice reconnues (avis CNO 2023-02)", 'https://www.ordremk.fr/wp-content/uploads/2024/01/avis-cno-2023-02.pdf'),
        ("Accès direct aux kinésithérapeutes (Ordre)", 'https://www.ordremk.fr/actualites/kines/acces-direct-aux-kinesitherapeutes/'),
        ("Obligation d'affichage des tarifs (Ordre)", 'https://www.ordremk.fr/actualites/kines/obligation-daffichage-des-tarifs/'),
    ],
    'en': [
        ("LSSI, art. 10 (BOE)", 'https://www.boe.es/buscar/act.php?id=BOE-A-2002-13758'),
        ("RD 1277/2003 on health centres (BOE)", 'https://www.boe.es/buscar/act.php?id=BOE-A-2003-19572'),
        ("RD 1907/1996 on health advertising (BOE)", 'https://www.boe.es/buscar/act.php?id=BOE-A-1996-18085'),
        ("Physiotherapists' code of ethics (Consejo General)",
         'https://www.consejo-fisioterapia.org/descargas/codigo-deontologico-cgcfe.pdf'),
        ("Homologation of physiotherapy degrees (Ministry of Science, Innovation and Universities)",
         'https://www.ciencia.gob.es/Universidades/validate/homologacion/fisioterapeuta.html'),
        ("AEPD FAQ for health professionals", 'https://www.aepd.es/preguntas-frecuentes/16-salud/2-profesionales-sanitarios'),
    ],
}

# ═════════════════════════ DENTISTES ET DENTISTS ═══════════════════════════
DENT = {}
DENT['fr'] = dict(
    html_lang='fr', og_locale='fr_FR', unit='mois', area=['FR', 'ES'],
    title="Site internet pour dentiste : 15 €/mois, démo en 24 h",
    description="Site internet pour chirurgien-dentiste pensé pour le code de déontologie et les recommandations de "
                "l'Ordre : honoraires, titres, sans avis ni référencement interdit. Démo gratuite en 24 h, 15 €/mois HT.",
    service_name="Création de site internet pour chirurgiens-dentistes",
    audience="Chirurgiens-dentistes libéraux",
    crumb_home='Accueil', crumb='Dentistes',
    badge='Chirurgiens-dentistes libéraux',
    h1="Création de site internet pour <em>dentiste</em>, selon les recommandations de l'Ordre",
    lede="Votre cabinet, vos soins, vos honoraires et votre prise de rendez-vous, présentés selon le code de "
         "déontologie : informer, sans promotion. Nous l'écrivons pour vous, vous validez chaque contenu, et la démo "
         "est gratuite en 24 heures.",
    pills=["Construit selon les recommandations de l'Ordre", 'Honoraires affichés', 'Démo gratuite en 24 h'],
    cta='Recevoir ma démo gratuite', cta2='Ce que le code impose',
    brief_t='En bref',
    brief="WebAutonomos crée des sites internet pour les chirurgiens-dentistes libéraux, en France et en Espagne. Le "
          "site présente votre cabinet, vos soins et votre équipe, avec vos honoraires, vos modalités de règlement et "
          "votre conventionnement, comme l'exigent le code de déontologie et l'arrêté du 30 mai 2018. Il suit les "
          "recommandations de l'Ordre de juin 2026 : "
          "pas d'avis ni de notes, pas de promotion, pas de photos avant/après, et pas de référencement pour passer "
          "devant vos confrères. Le site coûte <strong>15 € HT par mois</strong> sans frais d'installation ni "
          "engagement, ou <strong>349 € HT en un seul versement</strong>, et la démo est prête en 24 heures.",
    legal_id='regles', legal_ey='Le code de déontologie', legal_t="Ce que votre site doit respecter",
    legal_intro="Depuis 2020, un chirurgien-dentiste peut communiquer librement auprès du public, y compris sur un "
                "site internet. Cette communication reste encadrée par le code de déontologie et par les "
                "recommandations de l'Ordre, mises à jour en juin 2026. Voici l'essentiel.",
    legal_cols=('Sujet', 'Texte', 'Ce que ça change sur votre site'),
    legal_rows=[
        ('Le titre', 'Code de la santé publique, art. L4162-1 ; Code pénal, art. 433-17',
         "« Chirurgien-dentiste » est un titre protégé ; l'usurper est puni d'un an de prison et de 15 000 € "
         "d'amende."),
        ('Ce que vous pouvez dire', 'Code de la santé publique, art. R4127-215-1 ; recommandations de l\'Ordre (juin 2026)',
         "Vos compétences, votre parcours et vos conditions d'exercice, de façon loyale et honnête : pas de témoignages "
         "ni de notations, pas de comparaison de prix ou de pratiques, pas de promotion comme « 3 implants pour le prix "
         "de 2 ». L'Ordre déconseille les photos avant/après, qui suggèrent un résultat certain."),
        ('Référencement', 'Code de la santé publique, art. R4127-217',
         "Il est interdit d'obtenir, contre paiement ou par tout autre moyen, un référencement qui fasse apparaître "
         "votre site en priorité dans les résultats de recherche. Pour l'Ordre, le référencement prioritaire, payant ou "
         "non, est proscrit."),
        ('Honoraires', 'Code de la santé publique, art. R4127-240',
         "Un site qui présente votre activité doit indiquer vos honoraires, les modes de paiement acceptés et les "
         "obligations d'accès aux soins sans discrimination (CSS, AME). L'Ordre recommande d'indiquer au moins les "
         "honoraires des 5 à 10 actes les plus pratiqués."),
        ('Titres et spécialités', "Code de la santé publique, art. R4127-220 ; recommandations de l'Ordre",
         "Trois spécialités seulement : orthopédie dento-faciale, chirurgie orale, médecine bucco-dentaire, affichées par "
         "les seuls spécialistes qualifiés. Un omnipraticien doit employer les formules de l'Ordre, comme « oriente "
         "(ou limite) sa pratique aux actes d'orthodontie ». Diplômes universitaires : ceux que l'Ordre reconnaît ; "
         "une autre formation peut être citée avec la mention qu'elle n'est ni une spécialité ni un diplôme reconnu."),
        ('Devis et information écrite', "Arrêté du 30 mai 2018, art. 7 ; Code de la santé publique, art. L1111-3-2",
         "Information écrite préalable dès 70 € de dépassements d'honoraires, et devis type de la convention pour les "
         "prothèses et l'orthodontie, avec une alternative sans reste à charge ou à reste à charge modéré quand il y "
         "en a une."),
        ('Mentions obligatoires', "LCEN, art. 1-1 et 19 ; Code de commerce, art. R526-27 ; recommandations de l'Ordre",
         "Titre, pays d'obtention, Ordre d'inscription et code de déontologie applicable, nom précédé ou suivi de "
         "« EI » si vous êtes entrepreneur individuel, directeur de la publication et hébergeur. L'Ordre cite aussi "
         "le numéro RPPS et l'accessibilité du cabinet parmi les informations de base."),
    ],
    legal_note="Pas de lien vers le site d'une société commerciale ni de publicité pour un tiers : le code l'interdit "
               "(art. R4127-225). "
               "En centre de santé, toute publicité est interdite et le site doit identifier tous les praticiens "
               "(art. L6323-1-9 et L6323-1-5). Informations générales à jour en septembre 2026, qui ne remplacent pas "
               "l'avis de votre conseil départemental de l'Ordre.",
    legal_we_t='Ce que nous mettons en place',
    legal_we=["Vos honoraires pour les actes les plus pratiqués, vos modes de paiement, votre conventionnement et "
              "l'accès aux soins (CSS, AME)",
              "Vos titres et orientations avec les formules de l'Ordre, et vos diplômes dans leur libellé exact",
              "Un site sans avis, sans notes, sans photos avant/après et sans promotion",
              "Des mentions légales complètes, avec votre RPPS, votre Ordre, le code de déontologie et l'accessibilité "
              "du cabinet",
              "Aucune prestation de référencement pour passer devant vos confrères, et aucun lien commercial"],
    spain_note="<strong>Vous exercez en Espagne ?</strong> Les règles changent : inscription obligatoire au Colegio, "
               "clinique autorisée comme centre sanitaire avec son numéro d'enregistrement dans la publicité (et, dans "
               "certaines régions comme Murcie, autorisation préalable de la publicité, site compris), pas de "
               "« especialista » (l'Espagne n'a pas de spécialités dentaires officielles), et prix totaux dans les "
               "annonces. Nous connaissons aussi ces règles : "
               "<a href=\"/fr/site-internet-francophones-espagne\">site internet pour francophones en Espagne</a>.",
    sources_t='Sources',
    why_ey='Pourquoi nous', why_t="Pensé pour les chirurgiens-dentistes",
    why=[('📋', 'Les honoraires bien présentés', "Actes les plus pratiqués, modalités de règlement, conventionnement : ce que "
                                               "le code exige, lisible pour les patients."),
         ('🏷️', 'Les bons titres', "Spécialités qualifiées, orientations d'omnipraticien et diplômes reconnus, avec "
                                  "les formules de l'Ordre."),
         ('📅', 'Rendez-vous en un clic', "Un lien vers votre prise de rendez-vous en ligne et un formulaire réduit au "
                                         "strict nécessaire."),
         ('⚖️', "Rien de ce que l'Ordre écarte", "Pas d'avis, pas d'avant/après, pas de promotion, pas de référencement "
                                            "prioritaire : nous ne vous le vendrons pas.")],
    where_t='En France et en Espagne',
    where="Nous travaillons à distance, en français, par e-mail, WhatsApp et visioconférence : que votre cabinet soit à "
          "Bordeaux, à Strasbourg ou à Valence, en Espagne, rien ne change.",
    sect_t='Pour qui',
    sectors=['🦷 Omnipraticiens', '😁 Orthodontistes (ODF)', '🩻 Chirurgie orale', '🩺 Médecine bucco-dentaire',
             '👶 Odontologie pédiatrique', '🔩 Omnipraticiens (implantologie)', '🏥 Cabinets de groupe',
             '🪥 Parodontologie'],
    how_t='Votre site en trois étapes',
    steps=[('Vous décrivez votre cabinet', "Vos soins, votre équipe, vos horaires, votre prise de rendez-vous : deux "
                                          "minutes suffisent."),
           ('Nous préparons votre démo', "En moins de 24 heures, avec vos honoraires, vos titres et vos mentions "
                                        "légales."),
           ('Vous décidez', "Vous relisez et validez chaque contenu, et demandez les modifications que vous voulez. Si "
                           "le site vous plaît, il est mis en ligne ; sinon, vous ne payez rien.")],
    price_note=PRIX_FR_SANTE,
    extra=[
        ('contenu-site-dentiste', 'Sur votre site', "Ce que contient le site de votre cabinet dentaire",
         """<p class="legal-intro">Un patient qui cherche un dentiste dans sa ville, depuis son mobile ou son ordinateur, veut savoir en quelques secondes où vous trouver, comment vous contacter et à qui il aura affaire. Pour nous, la création de site internet pour dentiste commence par là : répondre clairement à ces questions, dans les limites du code de déontologie rappelées plus haut.</p>
<div class="why-g">
<div class="aud-c"><div class="aud-i" aria-hidden="true">📍</div><h3>Votre cabinet, votre équipe, votre adresse</h3><p>Nous rédigeons la présentation de votre cabinet dentaire et de chaque praticien de votre équipe à partir de vos informations, avec votre adresse et vos horaires bien visibles dès la page d'accueil.</p></div>
<div class="aud-c"><div class="aud-i" aria-hidden="true">☎️</div><h3>Contact en un geste</h3><p>Votre numéro de téléphone, un bouton WhatsApp et un formulaire de contact qui envoie directement la demande à votre adresse email : le patient choisit ce qui lui convient.</p></div>
<div class="aud-c"><div class="aud-i" aria-hidden="true">🔎</div><h3>Cohérent avec votre fiche Google</h3><p>Les titres et les textes du site reprennent vos soins et votre ville, et restent cohérents avec votre fiche Google : c'est inclus dans le prix.</p></div>
<div class="aud-c"><div class="aud-i" aria-hidden="true">🌍</div><h3>Jusqu'à quatre langues, sans supplément</h3><p>Si votre patientèle inclut des résidents ou des visiteurs étrangers, votre site peut être rédigé en français et dans jusqu'à trois autres langues parmi l'anglais, l'espagnol, le catalan, le valencien, le galicien et le basque, sans coût supplémentaire.</p></div>
</div>
<p class="where">Votre cabinet dentaire partage ses locaux avec des kinésithérapeutes, par exemple dans une maison de santé ? Leur communication est elle aussi encadrée par leur code de déontologie : voir notre page <a href="https://webautonomos.es/fr/site-internet-kinesitherapeute">site internet pour kinésithérapeute</a>.</p>"""),
        ('specialise-dentiste', 'Pensé pour un dentiste', "Pourquoi une création de site internet spécifique aux dentistes",
         """<p class="legal-intro">Une agence généraliste peut créer un site internet correct pour n'importe quelle activité. La création de site internet pour dentiste demande autre chose : connaître le code de déontologie, les formules autorisées par l'Ordre et les limites propres au secteur médical. Omnipraticien, orthodontiste ou chirurgien oral, chaque activité dentaire a ses propres usages, mais la communication du cabinet doit rester loyale et honnête sur chaque page du site.</p>
<div class="why-g">
<div class="aud-c"><div class="aud-i" aria-hidden="true">⚙️</div><h3>Une gestion technique que vous n'avez pas à suivre</h3><p>Hébergement, certificat de sécurité, sauvegardes quotidiennes et surveillance du site restent de notre côté après la mise en ligne. Les fonctionnalités utiles à vos patients — formulaire de contact, bouton WhatsApp, liens vers vos réseaux sociaux — sont incluses sans supplément.</p></div>
<div class="aud-c"><div class="aud-i" aria-hidden="true">✏️</div><h3>Une modification par mois, sans limite de durée</h3><p>Après la mise en ligne, vous pouvez demander une modification par mois, par exemple pour mettre à jour vos honoraires ou vos horaires. Pour un changement plus important, nous vous remettons un devis fermé.</p></div>
</div>"""),
    ],
    faq_t='Questions fréquentes',
    faq=[("Mes honoraires doivent-ils figurer sur mon site ?",
          "Oui. Le code de déontologie (art. R4127-240) impose à un dentiste qui présente son activité, notamment sur un "
          "site, d'y indiquer ses honoraires, les modes de paiement acceptés et les obligations d'accès aux soins sans "
          "discrimination. L'Ordre recommande d'indiquer au moins les honoraires des 5 à 10 actes les plus "
          "pratiqués."),
         ("Puis-je afficher les avis de mes patients ou une note Google ?",
          "Non. Le code interdit les témoignages de tiers (art. R4127-215-1), et l'Ordre précise qu'une communication "
          "loyale et honnête ne fait appel ni à des témoignages ni à des notations. Répondre publiquement à un avis "
          "nominatif peut aussi violer le secret professionnel."),
         ("Puis-je montrer des photos avant/après ?",
          "L'Ordre les déconseille : elles suggèrent au patient un résultat positif certain et tendent à être une "
          "information trompeuse. Aucun texte ne les interdit expressément, mais le risque disciplinaire existe."),
         ("Puis-je payer pour être mieux référencé sur Google ?",
          "Non. L'article R4127-217 interdit d'obtenir, contre paiement ou par tout autre moyen, un référencement qui "
          "fasse apparaître votre site en priorité ; l'Ordre proscrit le référencement prioritaire, payant ou non. Nous "
          "ne proposons donc aucun référencement prioritaire ni aucune publicité aux dentistes : le site est clair et "
          "bien construit, et Google l'indexe normalement."),
         ("Puis-je écrire « spécialiste en implantologie » ?",
          "Non. Il n'existe que trois spécialités, réservées aux spécialistes qualifiés : orthopédie dento-faciale, "
          "chirurgie orale et médecine bucco-dentaire. Un omnipraticien doit utiliser les formules de l'Ordre, comme "
          "« oriente sa pratique aux actes d'odontologie chirurgicale ». Vous pouvez citer l'implantologie parmi vos "
          "pratiques, sans la présenter comme relevant de la spécialité de chirurgie orale."),
         ("Quand dois-je remettre un devis ?",
          "Une information écrite préalable est obligatoire dès que les dépassements d'honoraires atteignent 70 € "
          "(arrêté du 30 mai 2018). Pour les prothèses et l'orthodontie, le devis suit le modèle de la convention et "
          "propose "
          "une alternative sans reste à charge ou à reste à charge modéré quand il y en a une."),
         ("Un centre de santé peut-il avoir un site ?",
          "Oui, sans aucune publicité en faveur du centre (art. L6323-1-9), et son gestionnaire doit y afficher "
          "l'identité et les fonctions de tous les médecins et chirurgiens-dentistes qui y exercent (art. "
          "L6323-1-5)."),
         ("Combien coûte un site pour dentiste ?",
          "15 € HT par mois sans frais d'installation ni engagement, ou 349 € HT en paiement unique, avec les mêmes "
          "services : conception, hébergement, nom de domaine la première année, mentions légales et une modification "
          "par mois. La démo est gratuite."),
         ("Mon site inclut-il des liens vers mes réseaux sociaux ?",
          "Oui, si vous en avez : le site inclut des liens vers vos profils professionnels sur les réseaux sociaux. Le "
          "code de déontologie encadre votre communication « par tout moyen » (art. R4127-215-1) : ces profils suivent "
          "donc les mêmes règles que votre site."),
         ("Mon site peut-il être proposé en plusieurs langues ?",
          "Oui, jusqu'à quatre langues au total, sans supplément, et nous rédigeons chaque version nous-mêmes.")],
    final_t='Voyez votre site avant de payer quoi que ce soit',
    final_sd="Démo gratuite en 24 heures, honoraires et mentions obligatoires compris. Sans frais d'installation, sans "
             "engagement.",
)

DENT['en'] = dict(
    html_lang='en', og_locale='en_GB', unit='month', area=['ES'],
    title="Websites for dentists and dental clinics in Spain: €15/month",
    description="Websites for English-speaking dentists and dental clinics in Spain, built around Spanish rules on "
                "health advertising, prices and titles. Free demo in 24h, €15/month + VAT.",
    service_name="Web design for dentists and dental clinics in Spain",
    audience="English-speaking dentists and dental clinic owners in Spain",
    crumb_home='Home', crumb='Dentists',
    badge='For dentists and dental clinics in Spain',
    h1="Websites for <em>dentists and dental clinics</em> in Spain",
    lede="Your clinic, your treatments and how to book, in English and Spanish, with prices, titles and registration "
         "details set out with Spanish rules in mind. We write it for you, you approve every word, and your free demo "
         "is ready within 24 hours.",
    pills=['English and Spanish included', 'Written with Spanish rules in mind', 'Free demo in 24 hours'],
    cta='Get my free demo', cta2='What the rules require',
    brief_t='In short',
    brief="WebAutonomos builds websites for English-speaking dentists and dental clinics in Spain. We write the copy in "
          "English and Spanish, plus up to two more languages if you need them, at no extra cost, show your Colegio, "
          "colegiado number, qualification and clinic registration number, and keep the site clear of what Spanish "
          "rules ban: patient testimonials, promises of results, implant or "
          "aligner brand names, and “especialista” titles that don't exist in Spain. It costs <strong>€15 + VAT per "
          "month</strong> with no setup fee and no lock-in, or a <strong>one-off €349 + VAT</strong>, and your demo is "
          "ready within 24 hours.",
    legal_id='rules', legal_ey='Spanish rules', legal_t='What your website has to get right in Spain',
    legal_intro="Dentistry is a regulated health profession in Spain, and dental advertising has been under close "
                "watch since the iDental and Dentix collapses. These are the points that matter for a website.",
    legal_cols=('Topic', 'Law', 'What it means for your website'),
    legal_rows=[
        ('Colegio and legal notice', 'Ley 2/1974, art. 3; LSSI (Ley 34/2002), art. 10',
         "Membership of a Colegio de Odontólogos y Estomatólogos is compulsory. Your site must show your Colegio and "
         "colegiado number, your qualification, the country that issued it and any recognition in Spain, the "
         "professional rules that apply, your NIF and the clinic's authorisation details."),
        ('Clinic authorisation', 'RD 1277/2003, art. 6.2; RD 1594/1994, art. 3',
         "A dental clinic (type C.2.5.1) needs regional authorisation, and its registration number must appear in any "
         "advertising, your website included. A dental practice must be run directly and personally by a dentist."),
        ('Health advertising', 'Ley 44/2003, art. 44; RD 1907/1996, art. 4',
         "Advertising must be objective, prudent and truthful: no assurances of results, and no testimonials from "
         "patients or famous people used to attract clients."),
        ('Titles', 'Ley 44/2003, 2nd additional provision; Consejo General code of ethics, art. 56',
         "Spain has no official dental specialties, so titles such as “especialista en implantes” or “orthodontic "
         "specialist” can't be used. Use only the titles you actually hold."),
        ('Brands and “free”', 'RD 1591/2009, art. 38.9; Ley 3/1991, art. 22.5',
         "Advertising to the public of medical devices that dentists apply, such as implant or aligner brands, is "
         "banned. Calling something “free” is misleading if the patient has to pay anything."),
        ('Prices and financing', 'Consumer law (TRLGDCU), art. 20.1.c; Ley 16/2011, art. 9',
         "Advertised prices must be the full final price. Any advert that mentions financing costs must give a "
         "representative example with the APR (TAE); “0% interest” finance arranged through the clinic still counts "
         "as a consumer credit."),
        ('Foreign qualifications', 'RD 581/2017; RD 889/2022; RDL 38/2020, art. 4; Código Penal, art. 403',
         "EU dental degrees benefit from automatic recognition, but you still apply to the Ministry of Health; a new "
         "application for a UK degree goes through homologation, with Spanish at B2 level. Practising without a "
         "recognised title is a criminal offence."),
    ],
    legal_note="Regional rules add detail: in Madrid, consumer law, as the COEM's decalogue explains, requires the "
               "total price of a treatment rather than “from €X” and the previous price next to any discount; "
               "Catalonia's Colegio rules out “first visit free”. Some regions, such as Murcia, require prior "
               "authorisation of health advertising, websites included. "
               "Dental clinics must appoint a data protection officer; a dentist practising alone, as an individual, "
               "doesn't have to. This is general information as of September 2026, not legal advice: check with your "
               "Colegio and your regional health department.",
    legal_we_t='What we set up for you',
    legal_we=["Your Colegio, colegiado number, qualification and a link to the code of ethics, plus the clinic's "
              "registration number and authorisation details",
              "Treatments described without promises of results, testimonials, brand names or “especialista” titles",
              "Prices shown as full final prices, and any financing with its representative example",
              "A link to your booking tool, WhatsApp or phone, and a contact form that asks only what it needs",
              "Your site in up to four languages, English and Spanish included, at no extra cost"],
    spain_note='<strong>Practising in the UK instead?</strong> UK rules are different. See '
               '<a href="https://webautonomos.es/en/dental-website-design">dental website design for UK '
               'practices</a>.',
    sources_t='Sources',
    why_ey='Why us', why_t='Built for practices that work in English',
    why=[('💬', 'We speak your language', "We work with you in English by email, WhatsApp or video call: no need "
                                         "to decode Spanish legal or technical jargon."),
         ('🌍', 'Up to four languages, one price', "English, Spanish and up to two more at no extra cost, so local patients find you as "
                                           "easily as expats do."),
         ('📋', 'Registration details in place', "Colegio, colegiado number and clinic registration number shown "
                                                "the way Spanish rules expect."),
         ('📅', 'Easy to book', "A clear button to your online calendar, WhatsApp or phone.")],
    where_t='Anywhere in Spain',
    where="Costa Blanca, Costa del Sol, Valencia, Mallorca, Barcelona, Madrid or the Canary Islands: we work remotely, "
          "so where your clinic is makes no difference.",
    sect_t='Who it is for',
    sectors=['🦷 General dentistry', '😁 Orthodontics', '🦷 Implant dentistry', '👶 Children’s dentistry',
             '🪥 Periodontics', '✨ Cosmetic dentistry', '🏥 Dental clinics', '🧑‍⚕️ Group practices'],
    how_t='Get started in three steps',
    steps=[('Tell us about your clinic', 'Your treatments, your team, your opening hours, your town: it takes two '
                                         'minutes.'),
           ('We build your demo', 'Within 24 hours, with your copy in both languages and your legal pages.'),
           ('You decide', "You check every word and ask for any changes you want. If you like it, it goes live; if "
                         "not, you pay nothing.")],
    price_note=PRIX_EN_SANTE,
    extra=[
        ('website-content', 'Content', "What to put on your dental clinic's site",
         '<p class="legal-intro">Patients choosing a dentist want to see quickly who treats them, which '
         'treatments the clinic offers and how to book an appointment.</p>'
         '<div class="why-g">'
         '<div class="aud-c"><div class="aud-i" aria-hidden="true">🦷</div>'
         '<h3>Your treatments, described plainly</h3>'
         '<p>General dentistry, implants, orthodontics or oral care, described without a promise of '
         'results (see the rules above), so patients understand what each treatment involves.</p></div>'
         '<div class="aud-c"><div class="aud-i" aria-hidden="true">🧑‍⚕️</div>'
         '<h3>Your team and their qualifications</h3>'
         '<p>Your clinical team, introduced with the qualifications they actually hold and the treatments each of '
         'them carries out, so patients know who will treat them. Registration details appear as set out in '
         'the rules above.</p></div>'
         '<div class="aud-c"><div class="aud-i" aria-hidden="true">📅</div>'
         '<h3>Your schedule and how to book</h3>'
         '<p>Your opening hours and a clear way to request an appointment, through your contact form, WhatsApp '
         'or phone, so patients do not have to search for how to reach you.</p></div>'
         '<div class="aud-c"><div class="aud-i" aria-hidden="true">🌍</div>'
         '<h3>Care for international patients</h3>'
         '<p>Say which languages your clinical team and front desk speak during appointments, not only which '
         'languages your pages are written in, so patients who have moved to Spain know they will be understood '
         'at the clinic.</p></div>'
         '</div>'),
        ('local-search-help', 'Local search', 'How English-speaking patients find you online',
         '<p class="legal-intro">Getting found by someone searching for a dentist depends on '
         'more than the design of the site.</p>'
         '<div class="why-g">'
         '<div class="aud-c"><div class="aud-i" aria-hidden="true">🔍</div>'
         '<h3>Basic SEO, included in your price</h3>'
         '<p>Titles and copy written around your treatments and your area, kept consistent with your Google '
         'Business Profile, are included at no extra cost.</p></div>'
         '<div class="aud-c"><div class="aud-i" aria-hidden="true">📈</div>'
         '<h3>SEO Local and your Google listing, if you want more</h3>'
         '<p>We also offer SEO Local for €15 + VAT a month, and managing your Google Business Profile for €29 '
         '+ VAT a month (€49 + VAT to set one up if you do not have a listing yet).</p></div>'
         '<div class="aud-c"><div class="aud-i" aria-hidden="true">📍</div>'
         '<h3>Patients searching in English</h3>'
         '<p>Expats who have just moved to Spain often search in their own language, typing “English-speaking '
         'dentist Marbella” or “dentist in Malaga who speaks English”. With copy in both languages, your site can '
         'answer these searches as well as the local ones.</p></div>'
         '<div class="aud-c"><div class="aud-i" aria-hidden="true">📚</div>'
         '<h3>Guides to go further</h3>'
         '<p>Our blog has practical guides on '
         '<a href="https://webautonomos.es/blog/en/how-to-rank-your-website-in-local-google">ranking your '
         'website locally</a> and <a href="https://webautonomos.es/blog/en/optimise-your-google-business-'
         'profile">optimising your Google Business Profile</a>.</p></div>'
         '</div>'),
        ('technical-basics', 'Behind the scenes', 'The technical side, handled for you',
         '<p class="legal-intro">Alongside the pages you and your patients see, a few technical basics come '
         'with every site we build.</p>'
         '<div class="why-g">'
         '<div class="aud-c"><div class="aud-i" aria-hidden="true">🔒</div>'
         '<h3>Hosting, SSL and daily backups</h3>'
         '<p>Your site includes hosting, an SSL certificate, daily backups, 24/7 monitoring and technical '
         'maintenance, so you do not have to think about the technical side.</p></div>'
         '<div class="aud-c"><div class="aud-i" aria-hidden="true">🔗</div>'
         '<h3>Links to your social profiles</h3>'
         '<p>We add links to your Facebook, Instagram or other social profiles on your site, so patients can '
         'also see what you post there.</p></div>'
         '<div class="aud-c"><div class="aud-i" aria-hidden="true">✏️</div>'
         '<h3>One change a month, included</h3>'
         '<p>Once your site is live, you can ask for one change a month at no extra cost, such as updating your '
         'team or adding a new treatment. A full redesign or a large new section goes through a fixed quote '
         'agreed before any work starts.</p></div>'
         '<div class="aud-c"><div class="aud-i" aria-hidden="true">📄</div>'
         '<h3>Legal pages included</h3>'
         '<p>Your legal notice, privacy policy and cookie policy are included.</p></div>'
         '</div>'),
    ],
    faq_t='Frequently asked questions',
    faq=[("Can I practise as a dentist in Spain with a UK degree?",
          "Only once it is recognised. New applications for a UK degree now go through homologation by the Ministry "
          "of Science, Innovation and Universities, which requires Spanish at B2 level. Recognitions already granted, "
          "including those given under Spain's Brexit transition rules to people who began their studies before 2021, "
          "keep their effect. EU dental degrees benefit from automatic recognition, but you still apply to the "
          "Ministry of Health."),
         ("What must my clinic's site show?",
          "Under article 10 of the LSSI: your name or company name (with its Registro Mercantil details), address, "
          "email and NIF, your Colegio and colegiado number, your qualification and the country that issued it, any "
          "recognition in Spain, the professional rules that apply, and the clinic's authorisation details, including "
          "the regional health department that supervises it. The clinic's registration number must "
          "also appear in any advertising (RD 1277/2003, art. 6.2)."),
         ("Can I call myself a specialist in implants or orthodontics?",
          "Spain has no officially recognised dental specialties, and the law bars titles that could be confused with "
          "official ones. Describe what you do, for example “implant treatment” or “orthodontic treatment”, and use only "
          "the titles you actually hold."),
         ("Can I mention Invisalign or an implant brand?",
          "Not in advertising aimed at patients: Spanish rules ban advertising to the public of medical devices that "
          "dentists apply themselves (RD 1591/2009, art. 38.9). Describe the treatment instead, such as “clear "
          "aligners”."),
         ("Can I show patient reviews or before-and-after photos?",
          "Avoid patient testimonials: health-advertising rules ban them as a way to attract clients (RD 1907/1996, "
          "art. 4.7). There is no specific rule on before-and-after photos, but they are judged under the same bans on "
          "testimonials and misleading claims, and need the patient's explicit consent."),
         ("How should I show prices and financing?",
          "As full final prices: the Madrid Colegio's decalogue treats “from €X” and “free implants” as misleading, "
          "and discounts must show the previous price. If an advert mentions financing costs, it must include a representative "
          "example with the APR (TAE), even for “0%” finance arranged through the clinic."),
         ("Do I have to give patients a written quote?",
          "A dentist must provide a written estimate of the treatment and its cost when the patient asks for one (RD "
          "1594/1994, art. 4). In Catalonia a written quote is compulsory unless the patient waives it in their own "
          "handwriting, and it must include the clinic's registration number."),
         ("Can patients book an appointment directly through the site?",
          "Not on the site itself: we don't integrate calendar or booking tools such as Doctoralia or Bookitit, or "
          "clinic management software, and there are no automatic SMS or email reminders. If you already use an "
          "online booking tool, we can add a link or button to it; patients can also request appointments through "
          "your contact form, WhatsApp button or phone, the same way any other enquiry reaches you."),
         ("How much does a website cost?",
          "€15 + VAT a month with no setup fee and no lock-in, or a one-off €349 + VAT, with the same services: design, "
          "hosting, a domain name for the first year, legal pages and one change a month. Dental services, whitening "
          "included, are VAT-exempt, so you usually can't deduct the VAT on our invoice (only in part if you also sell "
          "taxed services or products).")],
    final_t='See your website before you pay a thing',
    final_sd="Free demo within 24 hours, copy and legal pages included. No setup fee, no lock-in.",
)

DENT_SOURCES = {
    'fr': [
        ("Code de déontologie, communication des chirurgiens-dentistes (Légifrance)",
         'https://www.legifrance.gouv.fr/codes/section_lc/LEGITEXT000006072665/LEGISCTA000006196413/'),
        ("Recommandations de l'Ordre sur la communication (juin 2026)",
         'https://www.ordre-chirurgiens-dentistes.fr/download/109355/'),
        ("Affichages réglementaires (Ordre)",
         'https://www.ordre-chirurgiens-dentistes.fr/pour-le-chirurgien-dentiste/affichages-reglementaires-rgpd/'),
        ("Devis obligatoire (ameli.fr)",
         'https://www.ameli.fr/chirurgien-dentiste/exercice-liberal/facturation-remuneration/tarifs-conventionnels/devis-obligatoire'),
        ("Arrêté du 30 mai 2018 sur l'information des patients (Légifrance)",
         'https://www.legifrance.gouv.fr/loda/id/JORFTEXT000037032490'),
    ],
    'en': [
        ("LSSI, art. 10 (BOE)", 'https://www.boe.es/buscar/act.php?id=BOE-A-2002-13758'),
        ("RD 1277/2003 on health centres (BOE)", 'https://www.boe.es/buscar/act.php?id=BOE-A-2003-19572'),
        ("RD 1907/1996 on health advertising (BOE)", 'https://www.boe.es/buscar/act.php?id=BOE-A-1996-18085'),
        ("Dental advertising decalogue (Colegio de Dentistas de Madrid)",
         'https://coem.org.es/wp-content/uploads/2025/11/DECALOGO_PUBLICIDAD_COEM.pdf'),
        ("Dental clinics: consumer rights (Comunidad de Madrid)",
         'https://www.comunidad.madrid/consumo/clinicas-dentales-derechos-consumidores'),
        ("Homologation of dental degrees (Ministry of Science, Innovation and Universities)",
         'https://www.ciencia.gob.es/Universidades/validate/homologacion/dentista.html'),
    ],
}

# ═════════════════════════ PLOMBIERS ET PLUMBERS (28/09/2026) ═════════════
PRIX_FR_BAT = ("Prix hors taxes : l'IVA espagnole de 21 % s'ajoute. Si votre entreprise est établie dans un autre "
               "pays de l'UE, en France par exemple, avec un numéro de TVA intracommunautaire, la facture est émise "
               "sans TVA (autoliquidation). Nom de domaine inclus la première année, puis environ 12 €/an.")
PRIX_EN_BAT = ("Prices exclude VAT (21% IVA on the mainland and the Balearics; the Canary Islands, Ceuta and Melilla "
               "have their own taxes). As a VAT-registered autónomo you can normally deduct it. Domain name included "
               "for the first year, then about €12/year.")

# Textes communs aux pages bâtiment : médiateur, avis, mentions légales, services complémentaires.
ROW_MEDIATEUR = ("Médiateur de la consommation", "Code de la consommation, art. L616-1, R616-1 et L641-1",
                 "Si vous travaillez pour des particuliers, le nom, les coordonnées et l'adresse du site de votre "
                 "médiateur doivent apparaître de manière visible et lisible sur votre site. Amende jusqu'à 3 000 € "
                 "(15 000 € pour une société).")
ROW_ASSURANCE = ("Assurance", "Code des assurances, art. L241-1 et L243-2 ; Code de la consommation, art. R111-2",
                 "Si vous êtes soumis à la décennale, l'attestation se joint à chaque devis et chaque facture. Avant "
                 "tout contrat, le client doit aussi pouvoir connaître votre assurance, votre assureur et la "
                 "couverture géographique : autant l'indiquer dès le premier contact.")
FAQ_MEDIATEUR = ("Dois-je indiquer un médiateur de la consommation ?",
                 "Oui, si vous travaillez pour des particuliers, quelle que soit la taille de votre entreprise. Son "
                 "nom, ses coordonnées et l'adresse de son site internet doivent figurer de manière visible et lisible "
                 "sur votre site, vos conditions générales et vos bons de commande. L'ancienne plateforme européenne "
                 "de règlement des litiges a fermé en juillet 2025 : inutile d'y renvoyer.")
FAQ_SEO = ("Le SEO Local est-il inclus dans le prix, ou puis-je l'acheter à part ?",
           "Le référencement de base est inclus : titres et textes construits autour de votre métier et de votre "
           "zone. Le SEO Local (quatre articles de blog par mois, mots-clés locaux, rapport mensuel) est un service "
           "séparé à 15 € HT par mois, tout comme la gestion de votre fiche Google (29 € HT par mois, plus 49 € HT "
           "de création si vous n'avez pas encore de fiche) : les deux s'achètent indépendamment de l'abonnement.")


def faq_prix_fr(metier):
    return ("Combien coûte un site pour %s ?" % metier,
            "15 € HT par mois sans frais d'installation ni engagement, ou 349 € HT en paiement unique, avec les "
            "mêmes services : conception, hébergement, nom de domaine la première année, mentions légales et une "
            "modification par mois. Le site peut être en plusieurs langues sans supplément (jusqu'à 4), et la démo "
            "est gratuite.")


def visibilite_fr(h2, guide):
    return ('visibilite', 'Se faire trouver', h2,
            "<p class=\"legal-intro\">Commencez par des informations identiques partout : mêmes nom, adresse et "
            "téléphone sur votre site internet et sur votre fiche d'établissement. Une partie de ce travail est déjà "
            "comprise dans le prix ; le reste est un service à part.</p>"
            "<div class=\"why-g\">"
            "<div class=\"aud-c\"><div class=\"aud-i\" aria-hidden=\"true\">🔍</div>"
            "<h3>Le référencement de base, inclus dans le prix</h3>"
            "<p>Vos titres et vos textes mentionnent votre métier et les villes où vous intervenez : c'est compris "
            "dans les deux formules, sans supplément.</p></div>"
            "<div class=\"aud-c\"><div class=\"aud-i\" aria-hidden=\"true\">📈</div>"
            "<h3>Le SEO Local, un service à part</h3>"
            "<p>Nous proposons aussi le SEO Local pour 15 € HT par mois (quatre articles de blog par mois, mots-clés "
            "locaux et un rapport mensuel), et la gestion de votre fiche Google pour 29 € HT par mois (49 € HT de "
            "création si vous n'en avez pas encore). Ce sont des services séparés, à ajouter à l'abonnement ou même "
            "sans lui.</p></div>"
            "<div class=\"aud-c\"><div class=\"aud-i\" aria-hidden=\"true\">📚</div>"
            "<h3>Nos guides sur le sujet</h3>"
            "<p>Nos articles approfondissent ces sujets : " + guide + "comment "
            "<a href=\"https://webautonomos.es/blog/fr/optimiser-sa-fiche-google-business-profile\">mieux remplir "
            "votre fiche professionnelle</a> et comment "
            "<a href=\"https://webautonomos.es/blog/fr/obtenir-plus-avis-google-guide-complet\">obtenir plus "
            "d'avis</a>.</p></div>"
            "</div>")


ROW_EN_NOTICE = ('Legal notice', 'LSSI (Ley 34/2002), art. 10',
                 "Your name or company name, your address, your email and another direct contact detail (usually "
                 "your phone), your NIF (for a foreign national, your NIE), your Registro Mercantil details if you "
                 "trade as an S.L., and, if you show prices, whether they include VAT.")
ROW_EN_QUOTES = ('Written quotes', 'Comunitat Valenciana: Decreto 11/1995; Madrid: Decreto 35/1995; Catalonia: '
                                   'Consumer Code, art. 251-3',
                 "In these regions a homeowner is entitled to a detailed written quote with set contents before "
                 "work starts (in Catalonia, when they cannot work out the price themselves), unless they waive it in "
                 "their own handwriting and sign; a pre-printed waiver is not enough.")
ROW_EN_COMPLAINTS = ('Complaints', 'Consumer law (TRLGDCU), art. 21.3; regional rules',
                     "Tell customers where they can complain: at least through the channel your contract with them "
                     "started on (WhatsApp or your web form, for example), by post, by phone and by an electronic "
                     "channel. Since 28 December 2025 you must reply within 15 days at most (previously a month). "
                     "Official complaint forms are regional: in Andalucía, businesses without premises must show a QR "
                     "complaint poster on quotes, invoices and websites.")
FAQ_EN_QUOTE = ("Do I have to give customers a written quote?",
                "It depends on the region. In the Comunitat Valenciana, Madrid and Catalonia, homeowners are "
                "entitled to a detailed written quote before work starts, with set information such as materials, "
                "labour rates, dates and the total with VAT; in Catalonia, whenever the customer can't work out the "
                "price themselves. They can only waive it in their own handwriting, with their signature. In the "
                "Balearics, customers are entitled to a free written quote whenever the price can't be set directly; "
                "it is valid for the period it states or, if none is stated, at least 15 days. Other regions have "
                "their own rules: a written quote is always the safe choice.")
FAQ_EN_COMPLAINTS = ("What do I need to do about complaints?",
                     "Let customers complain at least through the channel your contract with them started on, by "
                     "post, by phone and by an electronic channel, and reply within 15 days at most: a national rule "
                     "since 28 December 2025 (previously a month). Carry your region's official complaint forms. In Andalucía, businesses "
                     "without premises must show a QR complaint poster on quotes, invoices and their website.")
FAQ_EN_REVIEWS = ("Can I show customer reviews on my website?",
                  "Yes, if you say whether and how you check them. Since December 2025, reviews must relate to a job "
                  "done in the 30 days before the review, and adding or commissioning fake reviews has been banned "
                  "outright since 2022.")
FAQ_EN_LANGUAGE = ("Do my quotes have to be in Spanish?",
                   "Pre-contract information, including quotes, must be given at least in Spanish, so a bilingual "
                   "quote is the safe choice even for British customers. Where there is a co-official language "
                   "(Catalonia, the Valencian Community, the Balearics…), customers can ask for it in that language "
                   "too; in Catalonia they are entitled to quotes and invoices in Catalan. Your website comes in English and Spanish, plus up to two more "
                   "languages, at no extra cost.")
FAQ_EN_GBP = ("Do I need Google Business Profile management as well as a website?",
              "No, it's optional. Your website already comes with basic SEO: titles and copy built around your trade "
              "and your area. If you want more, we also manage Google Business Profiles for €29 + VAT a month (€49 + "
              "VAT to set one up if you don't have one yet), and offer SEO Local for €15 + VAT a month.")
FAQ_EN_PRICE = ("How much does a website cost?",
                "€15 + VAT a month with no setup fee and no lock-in, or a one-off €349 + VAT, with the same services: "
                "design, hosting, a domain name for the first year, legal pages and one change a month. English and "
                "Spanish are included, and the demo is free.")
FAQ_EN_UK = ("Are UK qualifications recognised in Spain?",
             "Not automatically. Since 1 January 2021 the UK counts as a third country for professional "
             "qualifications, so a City & Guilds or NVQ certificate does not by itself make you an authorised "
             "installer. For plumbing and heating work, the routes include your region's exam for gas installers, "
             "a recognised course or experience in an installer company plus a regional exam for the carné "
             "profesional RITE, an approved F-gas course, homologation of your qualification, accreditation of your "
             "work experience (legal residence and at least three years, with at least 2,000 hours worked, in the "
             "last 15 years), an ENAC-accredited certification or a Spanish qualification.")


def local_search_en(guide):
    return ('local-search-help', 'Local search', 'How your website helps you appear in local searches',
            '<p class="legal-intro">Getting found in your area is not only about the website itself: homeowners '
            'also ask around, post jobs on directories, or search directly for a trusted tradesperson nearby.</p>'
            '<div class="why-g">'
            '<div class="aud-c"><div class="aud-i" aria-hidden="true">\U0001F50D</div>'
            '<h3>Basic SEO, included in your price</h3>'
            '<p>Titles and copy written around your trade and the towns you cover, kept consistent with your Google '
            'Business Profile, come with your website at no extra cost.</p></div>'
            '<div class="aud-c"><div class="aud-i" aria-hidden="true">\U0001F4C8</div>'
            '<h3>SEO Local and your Google listing, if you want more</h3>'
            '<p>We also offer SEO Local for €15 + VAT a month, and managing your Google Business Profile for €29 + '
            'VAT a month (€49 + VAT to set one up if you do not have a listing yet).</p></div>'
            '<div class="aud-c"><div class="aud-i" aria-hidden="true">\U0001F4DA</div>'
            '<h3>Guides to go further</h3>'
            '<p>Our blog has practical guides on ' + guide +
            '<a href="https://webautonomos.es/blog/en/how-to-rank-your-website-in-local-google">ranking your '
            'website locally</a> and <a href="https://webautonomos.es/blog/en/optimise-your-google-business-'
            'profile">optimising your Google Business Profile</a>.</p></div>'
            '</div>')


PLOMB = {}
PLOMB['fr'] = dict(
    html_lang='fr', og_locale='fr_FR', unit='mois', area=['FR', 'ES'],
    title="Création de site internet pour plombier : 15 €/mois",
    description="Création de site internet pour plombier et chauffagiste : tarifs de dépannage, devis, pompes à "
                "chaleur, encart France Rénov', mentions légales. Démo gratuite en 24 h, 15 €/mois HT.",
    service_name="Création de site internet pour plombiers et chauffagistes",
    audience="Plombiers, chauffagistes, installateurs de pompes à chaleur et dépanneurs sanitaires",
    crumb_home='Accueil', crumb='Plombiers',
    badge='Plombiers, chauffagistes, installateurs de pompes à chaleur',
    h1="Création de site internet pour <em>plombier</em> et chauffagiste",
    lede="Vos services, vos zones d'intervention, un appel ou un message WhatsApp en un geste, et vos tarifs de "
         "dépannage présentés selon l'arrêté du 24 janvier 2017. Nous l'écrivons pour vous et vous envoyons une démo gratuite "
         "en 24 heures.",
    pills=['Tarifs de dépannage accessibles', 'Appel et WhatsApp en un geste', 'Démo gratuite en 24 h'],
    cta='Recevoir ma démo gratuite', cta2='Ce que la loi impose',
    brief_t='En bref',
    brief="WebAutonomos crée des sites internet pour les plombiers, les chauffagistes et les installateurs de pompes "
          "à chaleur, en France et en Espagne. Nous rédigeons vos textes, présentons vos services (dépannage, salle "
          "de bains, chauffage, entretien) et plaçons, à partir des informations que vous nous donnez, ce que la loi "
          "demande à un professionnel du dépannage : taux "
          "horaires TTC, frais de déplacement et conditions du devis accessibles en ligne, médiateur de la "
          "consommation, mentions légales et, si vous proposez des pompes à chaleur, un chauffe-eau solaire ou "
          "thermodynamique, l'encart France Rénov' obligatoire à partir du 1<sup>er</sup> octobre 2026. Le site coûte <strong>15 € HT par mois</strong> sans "
          "frais d'installation ni engagement, ou <strong>349 € HT en paiement unique</strong>, jusqu'à 4 langues "
          "sans supplément si vous le souhaitez, et la démo est prête en 24 heures.",
    legal_id='regles', legal_ey='Les règles', legal_t="Ce que votre site doit montrer",
    legal_intro="Le dépannage est l'un des rares métiers où un texte dit ce que votre site doit afficher : l'arrêté "
                "du 24 janvier 2017 vise nommément la plomberie, les sanitaires et le génie climatique. S'y ajoutent "
                "les règles des contrats conclus chez le client et celles de la rénovation énergétique. Voici "
                "l'essentiel pour une activité en France.",
    legal_cols=('Sujet', 'Texte', 'Ce que ça change pour vous'),
    legal_rows=[
        ("Tarifs de dépannage", "Arrêté du 24 janvier 2017, art. 2 et 3 ; Code de la consommation, art. L131-5",
         "Taux horaires TTC, mode de décompte du temps, prix forfaitaires, frais de déplacement et caractère gratuit "
         "ou payant du devis doivent être aisément accessibles sur tout espace en ligne dédié à votre entreprise, "
         "votre site compris. Amende jusqu'à 3 000 € (15 000 € pour une société)."),
        ("Devis et note", "Arrêté du 24 janvier 2017, art. 4 et 5",
         "Un devis détaillé est remis avant toute prestation de dépannage, de réparation ou d'entretien, sans seuil "
         "de montant ni exception pour l'urgence. Le client est informé qu'il peut garder les pièces remplacées, et "
         "une note détaillée lui est remise avant le paiement."),
        ("Urgence au domicile", "Code de la consommation, art. L221-10 et L221-28",
         "Pour une réparation urgente que le client vous a expressément demandée chez lui, pas de délai de "
         "rétractation ni d'attente de 7 jours avant le paiement, mais seulement pour les pièces et travaux "
         "strictement nécessaires à l'urgence. Pour le reste, un contrat signé chez lui ouvre 14 jours de "
         "rétractation, sans aucun paiement pendant 7 jours."),
        ("Logos et mentions officielles", "Code de la propriété intellectuelle, art. L731-2 et L731-3 ; Code de la "
                                          "consommation, art. L121-4",
         "Dans une publicité de dépannage, utiliser sans autorisation les signes ou coordonnées d'un service public "
         "est passible d'une amende administrative jusqu'à 100 000 €. Se dire « agréé » sans l'être, ou afficher un label qu'on n'a "
         "pas, est une pratique commerciale trompeuse."),
        ROW_ASSURANCE,
        ("RGE et aides au chauffage", "Décret n° 2026-822 ; Code de la consommation, art. L224-114 et L242-51",
         "Depuis le 1er septembre 2026, MaPrimeRénov' « par geste » finance encore les pompes à chaleur air/eau, "
         "géothermiques et solarothermiques, mais plus les chaudières bois ni les chauffe-eau thermodynamiques. Quand "
         "l'aide exige un label, RGE en général, vous indiquez par écrit avant le contrat, et dans le contrat, si vous "
         "le détenez, avec le justificatif. Sinon : jusqu'à 75 000 € d'amende et contrat nul."),
        ("Encart France Rénov'", "Code de la consommation, art. L122-26 ; arrêté du 7 juillet 2026",
         "À partir du 1er octobre 2026, un site qui propose des pompes à chaleur, un chauffe-eau solaire ou d'autres "
         "travaux de rénovation énergétique affiche une bannière avec le message officiel de France Rénov', "
         "cliquable vers le service public. Amende jusqu'à 15 000 € (75 000 € pour une société)."),
        ROW_MEDIATEUR,
        ("Qualification et mot « artisan »", "Code de l'artisanat, art. L121-1, R121-1, R121-3, L151-2, R211-1 et L241-2",
         "La plomberie, le chauffage et le gaz ne s'exercent qu'avec une qualification (CAP, BEP, titre "
         "équivalent ou trois ans d'expérience) ou sous le contrôle effectif et permanent d'une personne qualifiée : "
         "7 500 € d'amende sinon. Le mot « artisan » suppose la qualité d'artisan, sous peine de 7 500 € d'amende."),
        ROW_MENTIONS,
    ],
    legal_note="Nouveau au 1er octobre 2026 : l'encart France Rénov' devient obligatoire pour les sites qui proposent "
               "des pompes à chaleur ou d'autres travaux de rénovation énergétique. Et si vous affichez des avis "
               "clients, indiquez s'ils sont contrôlés et comment, avec leur date (Code de la consommation, "
               "art. L111-7-2). Vous nous fournissez ces informations et validez chaque contenu. Informations "
               "générales à jour en septembre 2026, qui ne remplacent pas un conseil juridique.",
    legal_we_t='Ce que nous mettons en place',
    legal_we=["Une page de tarifs avec votre taux horaire TTC, votre décompte du temps, vos frais de déplacement et "
              "les conditions de votre devis, accessible depuis chaque page",
              "Un bouton d'appel et un bouton WhatsApp toujours visibles sur mobile, pour les demandes urgentes",
              "Votre qualité d'artisan si vous l'avez, votre numéro RNE et votre assurance (assureur, couverture) "
              "indiqués clairement",
              "Le logo RGE ou l'appellation « Professionnel du Gaz » seulement si vous les détenez, et l'encart "
              "France Rénov' si vous proposez des pompes à chaleur, un chauffe-eau solaire ou thermodynamique",
              "Les coordonnées de votre médiateur, des mentions légales complètes et des avis présentés avec leur "
              "date et leur mode de contrôle"],
    spain_note="<strong>Vous travaillez en Espagne ?</strong> Les règles changent : le chauffage, l'eau chaude et la "
               "climatisation y sont réservés aux entreprises habilitées au titre du RITE, le gaz à une empresa "
               "instaladora de gas, et plusieurs communautés (Valence, Madrid, Catalogne) donnent au client droit à "
               "un devis écrit préalable. Nous connaissons aussi ces règles : "
               "<a href=\"/fr/site-internet-francophones-espagne\">site internet pour francophones en Espagne</a>.",
    sources_t='Sources',
    why_ey='Pourquoi nous', why_t="Pensé pour les plombiers et chauffagistes",
    why=[('📞', 'Joignable en un geste', "Bouton d'appel et WhatsApp toujours visibles sur mobile : la personne qui a "
                                        "une fuite vous contacte sans chercher votre numéro."),
         ('💶', 'Des tarifs clairs', "Taux horaire, déplacement, devis : vos conditions sont présentées comme "
                                    "l'arrêté de 2017 le demande, avant même le premier appel."),
         ('🔥', 'Chauffage et pompes à chaleur', "Installation et maintenance : chaque service a sa section, "
                                                "avec l'encart France Rénov' quand il est requis."),
         ('📍', 'Trouvé près de chez vous', "Titres et textes pensés pour les recherches « plombier + votre ville », "
                                           "et votre fiche Google si vous le souhaitez.")],
    where_t='En France et en Espagne',
    where="Nous travaillons à distance, en français, par e-mail, WhatsApp et visioconférence : que vous interveniez à "
          "Lyon, à Toulouse ou sur la Costa del Sol, rien ne change.",
    sect_t='Pour qui',
    sectors=['🔧 Plombiers', '🔥 Chauffagistes', '♨️ Pompes à chaleur', '🚿 Salles de bains',
             '🚰 Recherche de fuites', '🧰 Entretien de chaudières', '❄️ Climatisation', '🪠 Débouchage'],
    how_t='Votre projet en trois étapes',
    steps=[('Vous décrivez votre activité', "Vos services, votre zone d'intervention, vos tarifs de dépannage et "
                                           "quelques photos de chantier : deux minutes suffisent."),
           ('Nous préparons votre démo', "En moins de 24 heures, avec votre page de tarifs et vos "
                                        "mentions légales."),
           ('Vous décidez', "Vous demandez les modifications que vous voulez. Si le site vous plaît, il est mis en "
                           "ligne ; sinon, vous ne payez rien.")],
    price_note=PRIX_FR_BAT,
    extra=[
        ('page-tarifs', 'Vos tarifs', "Que mettre sur la page de tarifs d'un plombier ?",
         "<p class=\"legal-intro\">Tout ce que l'arrêté du 24 janvier 2017 demande, en langage simple : chacun sait "
         "ce que coûte un déplacement avant de vous appeler. Nous la rédigeons à partir de vos prix, et vous "
         "validez chaque ligne.</p>"
         "<div class=\"why-g\">"
         "<div class=\"aud-c\"><div class=\"aud-i\" aria-hidden=\"true\">🕒</div>"
         "<h3>Taux horaire et forfaits TTC</h3>"
         "<p>Votre taux horaire toutes taxes comprises, le mode de décompte du temps (par demi-heure, par quart "
         "d'heure) et vos prestations au forfait, comme un débouchage ou la réparation d'un mécanisme de chasse "
         "d'eau.</p></div>"
         "<div class=\"aud-c\"><div class=\"aud-i\" aria-hidden=\"true\">🚐</div>"
         "<h3>Frais de déplacement</h3>"
         "<p>Un montant fixe, ou un prix par zone : nommer les communes couvertes évite les mauvaises surprises et "
         "les appels de clients trop éloignés.</p></div>"
         "<div class=\"aud-c\"><div class=\"aud-i\" aria-hidden=\"true\">📄</div>"
         "<h3>Devis gratuit ou payant</h3>"
         "<p>Dites-le clairement, avec son prix s'il est payant et, le cas échéant, s'il est déduit de la facture "
         "en cas d'acceptation des travaux.</p></div>"
         "</div>"),
        ('services', 'Vos services', "Dépannage, installation, chauffage : une section par service",
         "<p class=\"legal-intro\">Une personne qui cherche un chauffagiste pour sa pompe à chaleur ne lit pas la "
         "même page que celle qui a une fuite sous l'évier. Nous séparons vos services pour que chacun trouve vite "
         "le sien.</p>"
         "<div class=\"why-g\">"
         "<div class=\"aud-c\"><div class=\"aud-i\" aria-hidden=\"true\">🚰</div>"
         "<h3>Dépannage et fuites</h3>"
         "<p>Vos horaires d'intervention, les communes couvertes et un bouton d'appel en haut de la section : c'est "
         "ce que recherche une personne pressée.</p></div>"
         "<div class=\"aud-c\"><div class=\"aud-i\" aria-hidden=\"true\">🚿</div>"
         "<h3>Salles de bains et sanitaires</h3>"
         "<p>Vos réalisations en photos, classées par type de travaux : douche à l'italienne, pose de "
         "baignoire, sanitaires. Nous partons de vos propres photos de chantier.</p></div>"
         "<div class=\"aud-c\"><div class=\"aud-i\" aria-hidden=\"true\">🧰</div>"
         "<h3>Entretien de chaudière et de pompe à chaleur</h3>"
         "<p>L'entretien d'une chaudière de 4 à 400 kW est obligatoire chaque année, celui d'une pompe à chaleur de "
         "4 à 70 kW au moins tous les deux ans. Une section dédiée le rappelle à vos clients.</p></div>"
         "</div>"
         "<p class=\"where\">Pour aller plus loin, consultez "
         "<a href=\"https://webautonomos.es/blog/fr/site-web-pour-plombiers-guide-complet\">notre guide pour "
         "recevoir plus d'appels</a>.</p>"),
        visibilite_fr("Référencement du site internet d'un plombier : ce qui est inclus",
                      "<a href=\"https://webautonomos.es/blog/fr/positionner-son-site-dans-le-google-local\">"
                      "positionner votre site dans la recherche locale</a>, "),
    ],
    faq_t='Questions fréquentes',
    faq=[("Un plombier doit-il afficher ses tarifs sur son site internet ?",
          "Oui, s'il fait du dépannage, de la réparation ou de l'entretien : l'arrêté du 24 janvier 2017 vise la "
          "plomberie, les sanitaires et le génie climatique. Taux horaires TTC, mode de décompte du temps, prix "
          "forfaitaires, frais de déplacement et caractère gratuit ou payant du devis doivent être aisément "
          "accessibles sur tout espace en ligne dédié à l'entreprise. Amende jusqu'à 3 000 € (15 000 € pour une "
          "société)."),
         ("Le devis est-il obligatoire pour un dépannage urgent ?",
          "Oui. L'arrêté du 24 janvier 2017 impose un devis détaillé avant toute prestation de dépannage, de "
          "réparation ou d'entretien, sans seuil de montant ni exception pour l'urgence. Les prestations payées au "
          "forfait dans le cadre d'un contrat d'entretien ou de garantie en sont exclues. Le client doit aussi être "
          "informé qu'il peut garder les pièces remplacées."),
         ("Le client peut-il se rétracter après une intervention en urgence ?",
          "Non, pour une réparation urgente qu'il a expressément demandée à son domicile, et seulement pour les "
          "pièces et travaux strictement nécessaires à l'urgence (Code de la consommation, art. L221-28) ; vous "
          "pouvez alors être payé tout de suite (art. L221-10). Pour des travaux supplémentaires proposés sur place, "
          "les règles habituelles s'appliquent : 14 jours de rétractation et aucun paiement pendant 7 jours."),
         ("Qu'est-ce que l'encart France Rénov' obligatoire au 1er octobre 2026 ?",
          "À partir du 1er octobre 2026 (Code de la consommation, art. L122-26, et arrêté du 7 juillet 2026), tout "
          "professionnel qui propose des travaux de rénovation énergétique ou de production d'énergie renouvelable "
          "dans un logement, en ligne ou dans sa publicité, affiche le message officiel : « Avant de vous engager, le "
          "service public vous informe gratuitement pour préparer et sécuriser votre projet : "
          "www.france-renov.gouv.fr ». Sur un site, c'est une bannière cliquable vers le service public. Amende "
          "jusqu'à 15 000 € (75 000 € pour une société). Si vous installez des pompes à chaleur, vous êtes "
          "concerné ; nous ajoutons la bannière."),
         ("Quelles aides pour une pompe à chaleur depuis septembre 2026 ?",
          "Pour les demandes déposées depuis le 1er septembre 2026 (décret n° 2026-822), MaPrimeRénov' « par geste » "
          "finance encore les pompes à chaleur air/eau, géothermiques et solarothermiques, et le raccordement à un "
          "réseau de chaleur ; les chaudières bois et les chauffe-eau thermodynamiques n'y sont plus. Les "
          "certificats d'économies d'énergie restent une autre piste. Dans les deux cas, les travaux sont faits par "
          "un professionnel RGE."),
         ("Un plombier peut-il écrire « agréé » sur son site ?",
          "Seulement s'il a réellement reçu un agrément, en nommant l'organisme qui l'a délivré : une certification "
          "ou une qualification (RGE, PG) n'est pas un agrément. Se dire agréé à tort, ou afficher un label comme RGE "
          "sans l'avoir obtenu, est une pratique commerciale trompeuse (Code de la consommation, art. L121-4). L'appellation « Professionnel du Gaz » (PG) est volontaire : affichez-la si vous la "
          "détenez. Pour le gaz, c'est le certificat de conformité, établi par l'installateur et visé par un "
          "organisme habilité, qui compte pour chaque installation neuve ou modifiée."),
         ("Faut-il une attestation pour poser une pompe à chaleur ou une climatisation ?",
          "Oui, dès que l'installation touche au circuit de fluide frigorigène, pour un appareil en split par "
          "exemple : l'entreprise doit détenir une attestation de capacité, une par établissement (Code de "
          "l'environnement, art. R543-78 et R543-99). Exception : un équipement hermétique préchargé contenant moins de 2 kg de "
          "fluide, dont la mise en service se limite à un raccordement."),
         ("L'entretien des chaudières et des pompes à chaleur est-il obligatoire ?",
          "Oui. Une chaudière de 4 à 400 kW s'entretient chaque année civile, avec une attestation remise au client "
          "dans les 15 jours (Code de l'environnement, art. R224-41-4 à R224-41-8). Une pompe à chaleur de 4 à "
          "70 kW s'entretient au moins tous les deux ans (art. R224-44-3). Rappeler ces échéances sur votre site "
          "aide vos clients à y penser."),
         FAQ_MEDIATEUR,
         FAQ_AVIS,
         ("Un site internet aide-t-il vraiment un plombier à trouver des clients ?",
          "Oui, s'il dit clairement ce que vous faites, où vous intervenez et comment vous joindre. Ses titres et "
          "ses textes nomment votre métier et vos communes : c'est ce qui l'aide à apparaître dans Google quand "
          "quelqu'un tape « plombier » suivi du nom de sa ville. Le bouton WhatsApp et le formulaire de contact "
          "transforment ensuite une visite en demande de devis. Le site complète aussi le bouche-à-oreille : la "
          "personne à qui l'on a recommandé votre entreprise de plomberie peut y vérifier vos prestations avant de "
          "vous contacter. Aucun site ne garantit un nombre de demandes : votre place dans Google dépend aussi de "
          "la concurrence locale et de vos avis."),
         FAQ_SEO,
         faq_prix_fr('plombier')],
    final_t='Voyez votre site avant de payer quoi que ce soit',
    final_sd="Démo gratuite en 24 heures, avec votre page de tarifs et vos mentions légales. Sans frais "
             "d'installation, sans engagement.",
)

PLOMB['en'] = dict(
    html_lang='en', og_locale='en_GB', unit='month', area=['ES'],
    title="Websites for plumbers in Spain: €15/month, free demo",
    description="Websites for English-speaking plumbers and heating engineers in Spain: RITE, gas and F-gas rules, "
                "call-outs, legal notice. Free demo in 24h, €15/month + VAT.",
    service_name="Web design for plumbers and heating engineers in Spain",
    audience="English-speaking plumbers, heating engineers, gas engineers and air-conditioning installers in Spain",
    crumb_home='Home', crumb='Plumbers and heating engineers',
    badge='For plumbers and heating engineers in Spain',
    h1="Websites for <em>plumbers</em> and heating engineers in Spain",
    lede="Your services, the areas you cover, a call or a WhatsApp message in one tap, in English and Spanish, and "
         "the information Spanish rules expect from a plumbing and heating business. We write it for you and send "
         "you a free demo within 24 hours.",
    pills=['English and Spanish included', 'Spanish rules built in', 'Free demo in 24 hours'],
    cta='Get my free demo', cta2='What Spanish rules require',
    brief_t='In short',
    brief="WebAutonomos builds websites for English-speaking plumbers, heating engineers, gas engineers and "
          "air-conditioning installers working in Spain. We present your services, write the copy in English and "
          "Spanish (up to four languages) at no extra cost, and include the information Spanish law expects on a "
          "business website, such as a legal notice with your NIF or NIE, prices for homeowners shown with VAT included, and the complaint information your region "
          "asks for. It costs <strong>€15 + VAT per month</strong> with no setup fee and no lock-in, or a "
          "<strong>one-off €349 + VAT</strong>. We work with you in English, and your demo is ready within 24 hours.",
    legal_id='rules', legal_ey='Spanish rules', legal_t='What your business and your website have to get right',
    legal_intro="Plumbing on its own is lightly regulated in Spain, but heating, hot water, gas and air conditioning "
                "are not: they need an authorised company. Consumer law then sets the rules for call-outs, quotes and "
                "complaints. These are the points that matter.",
    legal_cols=('Topic', 'Law', 'What it means for you'),
    legal_rows=[
        ('Heating, hot water and air conditioning', 'RITE (RD 1027/2007), arts. 19 and 36 to 42',
         "Fixed heating, cooling, ventilation and hot-water installations must be carried out by an empresa "
         "instaladora habilitada. It files a declaración responsable with the region, holds at least €300,000 of "
         "civil liability cover, and has at least one staff member with the carné profesional RITE."),
        ('Gas', 'RD 919/2006, ITC-ICG 07 and 09',
         "Gas installations are carried out by an empresa instaladora de gas (category A, B or C), which issues the "
         "certificado de instalación. Homes on mains gas are inspected every five years, by the distributor or by a "
         "gas installer the customer chooses."),
        ('F-gases', 'RD 115/2017, arts. 3 and 9',
         "Installing split air conditioning or heat pumps with fluorinated refrigerant requires staff with an F-gas "
         "certificate, working within an authorised company (empresa habilitada). Pre-charged split units can only "
         "be sold to end users with proof that an authorised company will install them."),
        ('Water installations', 'CTE DB HS4; regional rules',
         "There is no national plumbing licence, but some regions have their own rules: in Madrid, registering a "
         "water installation requires the certificate of a registered plumbing installer (empresa instaladora de "
         "fontanería). Check with your region's industry department."),
        ('Urgent call-outs', 'Consumer law (TRLGDCU), art. 103',
         "There is no 14-day right of withdrawal when the customer called you out for an urgent repair or "
         "maintenance job. The right still applies to any extra services, and to goods other than the spare parts "
         "you necessarily used."),
        ROW_EN_QUOTES,
        ROW_EN_COMPLAINTS,
        ROW_EN_NOTICE,
    ],
    legal_note="Rules on quotes, complaint forms and water installations are regional, so check with your comunidad "
               "autónoma. This is general information as of September 2026, not legal advice.",
    legal_we_t='What we set up for you',
    legal_we=["A proper legal notice with your name, NIF or NIE and contact details, plus your company details if you "
              "trade as an S.L.",
              "Your call-out terms and your prices for homeowners shown with VAT included",
              "The work you are authorised for (heating, gas, air conditioning) described accurately, and nothing "
              "more",
              "The complaint information your region asks for, such as the QR poster in Andalucía",
              "A call button and WhatsApp always visible on mobile, and your site in up to four languages, English "
              "and Spanish included, at no extra cost"],
    spain_note='<strong>Working in the UK instead?</strong> UK rules are different. See '
               '<a href="https://webautonomos.es/en/web-design-for-plumbers">web design for plumbers and heating engineers in the UK</a>.',
    sources_t='Sources',
    why_ey='Why us', why_t='Built for tradespeople who work in English',
    why=[('💬', 'We speak your language', "Email, WhatsApp or video call in English: no need to decode Spanish legal "
                                         "or technical jargon."),
         ('🌍', 'Up to four languages, one price', "English, Spanish and up to two more at no extra cost, so Spanish "
                                                   "homeowners find you as easily as expats do."),
         ('📞', 'One tap to call you', "A call button and WhatsApp always in view on mobile: someone with a leak "
                                      "reaches you without hunting for your number."),
         ('📍', 'Found locally', "Titles and copy written for searches like “plumber Jávea” or “fontanero "
                                "Torrevieja”, in both languages.")],
    where_t='Anywhere in Spain',
    where="Costa Blanca, Costa del Sol, Valencia, Mallorca, Barcelona, Madrid or the Canary Islands: we work "
          "remotely, so where your van is based does not change how we work with you.",
    sect_t='Who it is for',
    sectors=['🔧 Plumbers', '🔥 Heating engineers', '♨️ Heat pumps and aerothermal', '🚿 Bathroom fitters',
             '🚰 Leak detection', '🧰 Boiler servicing', '❄️ Air conditioning', '🔥 Gas engineers'],
    how_t='Your website in three steps',
    steps=[('Tell us about your business', 'Your services, the areas you cover and a few job photos: it takes two '
                                           'minutes.'),
           ('We build your demo', 'Within 24 hours, with your services, your copy in English and Spanish, and your '
                                  'legal pages.'),
           ('You decide', "Ask for any changes you want. If you like it, it goes live; if not, you pay nothing.")],
    price_note=PRIX_EN_BAT,
    extra=[
        ('what-to-include', 'On your website', "What should a plumber's website in Spain show?",
         '<p class="legal-intro">A homeowner wants to know quickly whether you handle their problem, whether you '
         'cover their town, and how to reach you. These are the parts that answer those questions.</p>'
         '<div class="why-g">'
         '<div class="aud-c"><div class="aud-i" aria-hidden="true">\U0001F5C2️</div>'
         '<h3>Services grouped by type of job</h3>'
         '<p>Emergency repairs, bathrooms, heating and air conditioning each get their own section, so a visitor '
         'with a leak does not scroll past heat pumps to find your number.</p></div>'
         '<div class="aud-c"><div class="aud-i" aria-hidden="true">✅</div>'
         '<h3>Your authorisations, stated accurately</h3>'
         '<p>If your company is authorised for heating, gas or F-gas work, say so, with the category that applies. '
         'Claiming an authorisation you do not hold is misleading advertising.</p></div>'
         '<div class="aud-c"><div class="aud-i" aria-hidden="true">\U0001F4B6</div>'
         '<h3>Clear call-out terms</h3>'
         '<p>Your call-out charge and hourly rate, shown with VAT included for homeowners, so customers know what to '
         'expect before they ring.</p></div>'
         '<div class="aud-c"><div class="aud-i" aria-hidden="true">\U0001F4CD</div>'
         '<h3>The towns you cover</h3>'
         '<p>Naming the towns you work in (Jávea, Torrevieja or Fuengirola, for example) helps both readers and '
         'Google understand who your site is for.</p></div>'
         '</div>'
         '<p class="where">For a longer read, see our guide to '
         '<a href="https://webautonomos.es/blog/en/website-for-plumbers-complete-guide">getting more calls from '
         'a plumber&#8217;s website</a>.</p>'),
        local_search_en(''),
    ],
    faq_t='Frequently asked questions',
    faq=[("Do I need to be registered to install heating or air conditioning in Spain?",
          "Yes. Fixed heating, cooling, ventilation and hot-water installations must be carried out by an empresa "
          "instaladora habilitada under the RITE (RD 1027/2007): it files a declaración responsable with the region, "
          "holds at least €300,000 of civil liability cover, and has at least one staff member with the carné "
          "profesional RITE. Installing split air conditioning or heat pumps also needs staff with an F-gas "
          "certificate (RD 115/2017)."),
         FAQ_EN_UK,
         ("Who carries out the five-yearly gas inspection?",
          "For homes on mains gas, the distributor arranges it every five years and must give three months' notice; "
          "the customer can instead have it done by an authorised gas installer of their choice. Whoever carries out "
          "the inspection may not also repair the faults it finds. The Comunidad de Madrid warns that the "
          "distributor sends individual written notice, that maintenance contracts sold as compulsory are not, and "
          "that nothing is paid in hand to the distributor's inspector: the charge comes on the next gas bill."),
         ("Can customers cancel after an emergency call-out?",
          "Not for the urgent repair itself. Under article 103 of the consumer law (TRLGDCU), there is no right of "
          "withdrawal when the customer specifically asked you to visit for an urgent repair or maintenance job. "
          "The 14-day right still applies to extra services you provide during that visit, and to goods other than "
          "the spare parts you necessarily used."),
         FAQ_EN_QUOTE,
         ("How often must boilers and air conditioning be serviced in Spain?",
          "The RITE sets minimum intervals for homes: every two years for gas wall-mounted boilers up to 70 kW, "
          "every four years for air conditioning and hot-water heat pumps up to 12 kW, and every five years for gas "
          "water heaters up to 24.4 kW. Installations from 5 kW are maintained by an authorised maintenance company "
          "(empresa mantenedora)."),
         ("What guarantee do I owe on a repair?",
          "For the repair, installation or maintenance of household appliances, Royal Decree 58/1988 sets a "
          "guarantee of at least three months, an itemised invoice showing parts, labour and call-out charge, and "
          "the customer's right to a written quote valid for at least 30 days, which they can waive in writing. Its "
          "wording covers any durable household appliance, whatever energy it uses. For other work, legal minimums "
          "still apply: parts and equipment you supply and install carry the 3-year legal guarantee, gas work is "
          "guaranteed for 4 years against faulty workmanship, and Catalonia requires at least 6 months on services. "
          "Put your guarantee in writing."),
         FAQ_EN_COMPLAINTS,
         FAQ_EN_REVIEWS,
         FAQ_EN_LANGUAGE,
         FAQ_EN_GBP,
         FAQ_EN_PRICE],
    final_t='See your website before you pay a thing',
    final_sd="Free demo within 24 hours, with your services and legal pages. No setup fee, no lock-in.",
)

PLOMB_SOURCES = {
    'fr': [
        ("Arrêté du 24 janvier 2017, dépannage dans le bâtiment (Légifrance)",
         'https://www.legifrance.gouv.fr/loda/id/JORFTEXT000033935513'),
        ("Dépannage à domicile : choisir le bon professionnel (DGCCRF)",
         'https://www.economie.gouv.fr/dgccrf/les-fiches-pratiques/plomberie-serrurerie-chauffage-choisir-le-bon-professionnel-pour-un-depannage-domicile'),
        ("Arrêté du 7 juillet 2026, message France Rénov' (Légifrance)",
         'https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000054569418'),
        ("Décret n° 2026-822, MaPrimeRénov' (Légifrance)", 'https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000054750363'),
        ("Arrêté du 23 février 2018, installations de gaz, art. 21 (Légifrance)",
         'https://www.legifrance.gouv.fr/loda/article_lc/LEGIARTI000043233805'),
        ("Assurance décennale (Service-public)", 'https://entreprendre.service-public.gouv.fr/vosdroits/F2034'),
        ("Médiateur de la consommation (Service-public)", 'https://entreprendre.service-public.gouv.fr/vosdroits/F33338'),
    ],
    'en': [
        ("RITE, RD 1027/2007 (BOE)", 'https://www.boe.es/buscar/act.php?id=BOE-A-2007-15820'),
        ("Gas regulation, RD 919/2006 (BOE)", 'https://www.boe.es/buscar/act.php?id=BOE-A-2006-15345'),
        ("F-gases, RD 115/2017 (BOE)", 'https://www.boe.es/buscar/act.php?id=BOE-A-2017-1679'),
        ("Spanish consumer law, TRLGDCU (BOE)", 'https://www.boe.es/buscar/act.php?id=BOE-A-2007-20555'),
        ("Repairs to household appliances, RD 58/1988 (BOE)", 'https://www.boe.es/buscar/act.php?id=BOE-A-1988-2809'),
        ("Fake gas inspections (Comunidad de Madrid)", 'https://www.comunidad.madrid/consumo/fraudes-inspecciones-revisiones-gas'),
        ("LSSI, art. 10 (BOE)", 'https://www.boe.es/buscar/act.php?id=BOE-A-2002-13758'),
    ],
}

# ═════════════════════════ ÉLECTRICIENS ET ELECTRICIANS (28/09/2026) ══════
ELEC = {}
ELEC['fr'] = dict(
    html_lang='fr', og_locale='fr_FR', unit='mois', area=['FR', 'ES'],
    title="Création de site internet pour électricien : 15 €/mois",
    description="Création de site internet pour électricien : tarifs de dépannage, Consuel, bornes de recharge, "
                "photovoltaïque, encart France Rénov'. Démo gratuite en 24 h, 15 €/mois HT.",
    service_name="Création de site internet pour électriciens",
    audience="Électriciens, installateurs de bornes de recharge et de panneaux photovoltaïques",
    crumb_home='Accueil', crumb='Électriciens',
    badge='Électriciens, bornes de recharge, photovoltaïque',
    h1="Création de site internet pour <em>électricien</em> : vos chantiers, vos qualifications",
    lede="Vos services, de la mise en sécurité aux bornes de recharge, vos zones d'intervention, vos qualifications "
         "présentées telles que vous les détenez et vos tarifs de dépannage accessibles comme la loi le demande. Nous l'écrivons "
         "pour vous et vous envoyons une démo gratuite en 24 heures.",
    pills=['Vos qualifications en avant', 'Tarifs de dépannage accessibles', 'Démo gratuite en 24 h'],
    cta='Recevoir ma démo gratuite', cta2='Ce que la loi impose',
    brief_t='En bref',
    brief="WebAutonomos crée des sites internet pour les électriciens et les installateurs de bornes de recharge et "
          "de panneaux photovoltaïques, en France et en Espagne. Nous rédigeons vos textes, présentons vos services "
          "et vos qualifications (IRVE, RGE, Qualifelec) telles que vous les détenez, et plaçons, à partir des "
          "informations que vous nous donnez, ce que la loi demande : tarifs de dépannage accessibles en ligne, médiateur de la consommation, mentions légales et, si "
          "vous proposez du photovoltaïque ou d'autres travaux de rénovation énergétique, l'encart France Rénov' "
          "obligatoire à partir du 1<sup>er</sup> octobre 2026. Le site coûte <strong>15 € HT par mois</strong> sans "
          "frais d'installation ni engagement, ou <strong>349 € HT en paiement unique</strong>, jusqu'à 4 langues "
          "sans supplément si vous le souhaitez, et la démo est prête en 24 heures.",
    legal_id='regles', legal_ey='Les règles', legal_t="Ce que votre site doit montrer",
    legal_intro="Un électricien a plus de règles à respecter qu'il n'y paraît : l'arrêté du 24 janvier 2017 pour le "
                "dépannage, le Consuel pour la mise en service, une qualification propre aux bornes de recharge, et "
                "celles des aides au photovoltaïque. Voici l'essentiel pour une activité en France.",
    legal_cols=('Sujet', 'Texte', 'Ce que ça change pour vous'),
    legal_rows=[
        ("Tarifs de dépannage et devis", "Arrêté du 24 janvier 2017 ; Code de la consommation, art. L131-5",
         "L'électricité est visée. Taux horaires TTC, décompte du temps, forfaits, frais de déplacement et "
         "caractère gratuit ou payant du devis doivent être aisément accessibles sur votre site, et un devis détaillé "
         "est remis avant toute intervention de dépannage, de réparation ou d'entretien. Amende jusqu'à 3 000 € (15 000 € pour une société)."),
        ("Qualification et mot « artisan »", "Code de l'artisanat, art. L121-1, R121-1, R121-3, L151-2, R211-1 et L241-2",
         "Les installations électriques ne s'exercent qu'avec une qualification (CAP, BEP, titre équivalent ou trois "
         "ans d'expérience) ou sous le contrôle effectif et permanent d'une personne qualifiée : 7 500 € d'amende "
         "sinon. Le mot « artisan » suppose la qualité d'artisan, sous peine de 7 500 € d'amende."),
        ROW_ASSURANCE,
        ("Consuel", "Code de l'énergie, art. D342-19 et D342-20",
         "Avant la mise sous tension d'une installation neuve, d'une installation entièrement rénovée mise hors "
         "tension par le distributeur, ou d'une production photovoltaïque qui modifie l'installation intérieure : "
         "attestation de conformité établie par l'installateur et visée par Consuel."),
        ("Bornes de recharge", "Code de l'énergie, art. D353-2",
         "Hors installations de 3,7 kW ou moins dans un logement privé, une borne est posée par un professionnel "
         "titulaire d'une qualification IRVE délivrée par un organisme agréé. Le crédit d'impôt borne ne s'applique "
         "plus aux dépenses payées depuis le 1er janvier 2026."),
        ("Photovoltaïque", "Arrêté du 6 octobre 2021, art. 1 et annexe 5 ; CGI, art. 278-0 bis P",
         "Pour vendre son électricité avec l'obligation d'achat, l'installation doit être réalisée par un "
         "installateur qualifié ou certifié. Même condition pour la TVA à 5,5 % des installations de 9 kWc ou moins "
         "sur un logement, depuis le 1er octobre 2025, avec des équipements conformes aux critères fixés par "
         "arrêté."),
        ("Labels et qualifications", "Code de la consommation, art. L121-4",
         "Afficher un certificat, un label ou une qualification (Qualifelec, IRVE, RGE) sans l'avoir obtenu est une "
         "pratique commerciale trompeuse. Montrez chaque qualification avec le domaine qu'elle couvre."),
        ("Encart France Rénov'", "Code de la consommation, art. L122-26 ; arrêté du 7 juillet 2026",
         "À partir du 1er octobre 2026, un site qui propose du photovoltaïque, une pompe à chaleur ou d'autres "
         "travaux de rénovation énergétique d'un logement affiche une bannière avec le message officiel de France "
         "Rénov', cliquable vers le service public. Amende jusqu'à 15 000 € (75 000 € pour une société)."),
        ROW_MEDIATEUR,
        ROW_MENTIONS,
    ],
    legal_note="Nouveau au 1er octobre 2026 : l'encart France Rénov' devient obligatoire pour les sites qui proposent "
               "du photovoltaïque ou d'autres travaux de rénovation énergétique. Et si vous affichez des avis clients, "
               "indiquez s'ils sont contrôlés et comment, avec leur date (Code de la consommation, art. L111-7-2). "
               "Vous nous fournissez ces informations et validez chaque contenu. Informations générales à jour en "
               "septembre 2026, qui ne remplacent pas un conseil juridique.",
    legal_we_t='Ce que nous mettons en place',
    legal_we=["Une page de tarifs avec votre taux horaire TTC, vos frais de déplacement et les conditions de votre "
              "devis, si vous faites du dépannage",
              "Vos qualifications (Qualifelec, IRVE, RGE) avec leur domaine, seulement celles que vous détenez",
              "Votre qualité d'artisan si vous l'avez, votre numéro RNE et votre assurance (assureur, couverture) "
              "indiqués clairement",
              "L'encart France Rénov' et son lien, si vous proposez du photovoltaïque, des pompes à chaleur ou "
              "d'autres travaux d'économies d'énergie",
              "Les coordonnées de votre médiateur, des mentions légales complètes et des avis présentés avec leur "
              "date et leur mode de contrôle"],
    spain_note="<strong>Vous travaillez en Espagne ?</strong> Les règles changent : seule une empresa instaladora en "
               "baja tensión, déclarée auprès de la communauté autonome, peut réaliser une installation électrique et "
               "délivrer le certificat d'installation (le « boletín »), et plusieurs communautés (Valence, Madrid, "
               "Catalogne) donnent au client droit à un devis écrit préalable. Nous connaissons aussi ces règles : "
               "<a href=\"/fr/site-internet-francophones-espagne\">site internet pour francophones en Espagne</a>.",
    sources_t='Sources',
    why_ey='Pourquoi nous', why_t="Pensé pour les électriciens",
    why=[('🔌', 'Vos spécialités bien rangées', "Dépannage, rénovation, bornes de recharge, photovoltaïque : une "
                                              "section par service, pour que chacun trouve le sien."),
         ('🏅', 'Vos qualifications en avant', "Qualifelec, IRVE, RGE : chaque qualification apparaît avec son "
                                              "domaine, et seulement celles que vous détenez."),
         ('📞', 'Joignable en un geste', "Bouton d'appel et WhatsApp toujours visibles sur mobile, pour les coupures "
                                        "et les pannes qui n'attendent pas."),
         ('📍', 'Trouvé près de chez vous', "Titres et textes pensés pour les recherches « électricien + votre ville », "
                                           "et votre fiche Google si vous le souhaitez.")],
    where_t='En France et en Espagne',
    where="Nous travaillons à distance, en français, par e-mail, WhatsApp et visioconférence : que vous interveniez à "
          "Bordeaux, à Lille ou sur la Costa Blanca, rien ne change.",
    sect_t='Pour qui',
    sectors=['⚡ Électriciens', '🔌 Dépannage électrique', '🏠 Rénovation électrique', '🚗 Bornes de recharge',
             '☀️ Photovoltaïque', '💡 Éclairage', '🏢 Électricité tertiaire', '📶 Domotique et réseaux'],
    how_t='Votre projet en trois étapes',
    steps=[('Vous décrivez votre activité', "Vos services, vos qualifications, votre zone d'intervention et quelques "
                                           "photos de chantier : deux minutes suffisent."),
           ('Nous préparons votre démo', "En moins de 24 heures, avec vos services, vos qualifications et vos "
                                        "mentions légales."),
           ('Vous décidez', "Vous demandez les modifications que vous voulez. Si le site vous plaît, il est mis en "
                           "ligne ; sinon, vous ne payez rien.")],
    price_note=PRIX_FR_BAT,
    extra=[
        ('specialites', 'Vos services', "Quels services mettre en avant sur le site d'un électricien ?",
         "<p class=\"legal-intro\">Chaque service répond à un besoin différent, avec ses propres règles : les "
         "présenter séparément aide le visiteur et vous évite les promesses approximatives.</p>"
         "<div class=\"why-g\">"
         "<div class=\"aud-c\"><div class=\"aud-i\" aria-hidden=\"true\">🔌</div>"
         "<h3>Dépannage et mise en sécurité</h3>"
         "<p>Vos horaires d'intervention, les communes couvertes, un bouton d'appel et un lien vers vos tarifs de "
         "dépannage : l'essentiel pour une panne.</p></div>"
         "<div class=\"aud-c\"><div class=\"aud-i\" aria-hidden=\"true\">🏠</div>"
         "<h3>Rénovation et mise en conformité</h3>"
         "<p>Tableau électrique, remise aux normes, rénovation complète : précisez quand vous vous chargez de "
         "l'attestation Consuel, exigée avant la remise sous tension d'une installation entièrement rénovée que le "
         "distributeur a mise hors tension à la demande du client.</p>"
         "</div>"
         "<div class=\"aud-c\"><div class=\"aud-i\" aria-hidden=\"true\">🚗</div>"
         "<h3>Bornes de recharge</h3>"
         "<p>Votre qualification IRVE, les puissances que vous posez, et le cas de la copropriété : le syndicat des "
         "copropriétaires ne peut s'opposer sans motif sérieux et légitime à l'équipement d'une place privative, "
         "aux frais du demandeur (« droit à la prise »).</p></div>"
         "<div class=\"aud-c\"><div class=\"aud-i\" aria-hidden=\"true\">☀️</div>"
         "<h3>Photovoltaïque</h3>"
         "<p>Vos qualifications, les démarches que vous prenez en charge (Consuel, raccordement) et l'encart France "
         "Rénov' obligatoire à partir du 1er octobre 2026.</p></div>"
         "</div>"
         "<p class=\"where\">Pour aller plus loin, consultez "
         "<a href=\"https://webautonomos.es/blog/fr/site-web-pour-electriciens\">notre guide : ce qu'il vous faut "
         "et par où commencer</a>.</p>"),
        visibilite_fr("Référencement du site d'un électricien : ce qui est inclus",
                      "<a href=\"https://webautonomos.es/blog/fr/map-pack-google-comment-y-figurer\">figurer dans "
                      "les résultats de Google Maps</a>, "),
    ],
    faq_t='Questions fréquentes',
    faq=[("Un électricien doit-il afficher ses tarifs sur son site internet ?",
          "Oui, s'il fait du dépannage, de la réparation ou de l'entretien : l'arrêté du 24 janvier 2017 vise "
          "l'électricité. Taux horaires TTC, mode de décompte du temps, prix forfaitaires, frais de déplacement et "
          "caractère gratuit ou payant du devis doivent être aisément accessibles sur tout espace en ligne dédié à "
          "l'entreprise, et un devis détaillé est remis avant l'intervention. Amende jusqu'à 3 000 € (15 000 € pour "
          "une société)."),
         ("Faut-il une qualification pour être électricien ?",
          "Oui. Les installations électriques font partie des activités qui ne peuvent être exercées que par une "
          "personne qualifiée, ou sous son contrôle effectif et permanent (Code de l'artisanat, art. L121-1) : CAP, "
          "BEP ou titre équivalent, ou trois ans d'expérience dans le métier. Exercer sans cette qualification est "
          "puni de 7 500 € d'amende."),
         ("Quand l'attestation Consuel est-elle obligatoire ?",
          "Avant la mise sous tension d'une installation électrique neuve raccordée au réseau, d'une installation "
          "entièrement rénovée que le distributeur a mise hors tension à la demande du client, et d'une installation "
          "de production, photovoltaïque par exemple, qui modifie l'installation intérieure (Code de l'énergie, "
          "art. D342-19). L'installateur établit l'attestation et la fait viser par Consuel."),
         ("Quelle qualification pour installer une borne de recharge ?",
          "Une qualification IRVE délivrée par un organisme agréé, dès que la borne dépasse 3,7 kW ou qu'elle est "
          "installée ailleurs que dans un logement privé (Code de l'énergie, art. D353-2). Pour les dépenses payées "
          "depuis le 1er janvier 2026, le crédit d'impôt borne n'existe plus ; en immeuble collectif, le programme "
          "Advenir peut encore aider les copropriétés et leurs résidents."),
         ("Un électricien peut-il réaliser le diagnostic électrique d'une vente ?",
          "Non. Le diagnostic de l'installation électrique exigé pour une vente est réalisé par un diagnostiqueur "
          "certifié, qui ne doit avoir aucun lien avec une entreprise pouvant faire des travaux sur l'installation "
          "(Code de la construction et de l'habitation, art. L271-6). Vous pouvez en revanche proposer la mise en "
          "sécurité ou la mise aux normes qui suit le diagnostic."),
         ("Le photovoltaïque est-il concerné par l'encart France Rénov' ?",
          "Oui. L'arrêté du 7 juillet 2026 vise les travaux de rénovation énergétique des logements « en vue de la "
          "réalisation d'économies d'énergie ou de production d'énergie renouvelable ». À partir du 1er octobre 2026, "
          "un site qui propose des panneaux photovoltaïques sur des logements affiche donc la bannière officielle, "
          "cliquable vers le service public. Amende jusqu'à 15 000 € (75 000 € pour une société)."),
         ("Faut-il être qualifié pour installer du photovoltaïque ?",
          "Pour que votre client puisse vendre son électricité avec l'obligation d'achat, oui : l'installateur doit "
          "être qualifié ou certifié (arrêté du 6 octobre 2021, annexe 5). La TVA à 5,5 % des installations de "
          "9 kWc ou moins sur un logement, en vigueur depuis le 1er octobre 2025, suppose aussi une installation "
          "réalisée par un professionnel qualifié ou certifié, avec des équipements conformes aux critères fixés par "
          "arrêté."),
         ("Mes qualifications doivent-elles figurer sur mon site ?",
          "Ce n'est pas obligatoire, mais si vous les affichez, elles doivent être exactes : afficher un certificat, "
          "un label ou une qualification sans l'avoir obtenu est une pratique commerciale trompeuse (Code de la "
          "consommation, art. L121-4). Nous présentons chaque qualification avec le domaine qu'elle couvre."),
         FAQ_MEDIATEUR,
         FAQ_AVIS,
         FAQ_SEO,
         faq_prix_fr('électricien')],
    final_t='Voyez votre site avant de payer quoi que ce soit',
    final_sd="Démo gratuite en 24 heures, avec vos services, vos qualifications et vos mentions légales. Sans frais "
             "d'installation, sans engagement.",
)

ELEC['en'] = dict(
    html_lang='en', og_locale='en_GB', unit='month', area=['ES'],
    title="Websites for electricians in Spain: €15/month, free demo",
    description="Websites for English-speaking electricians in Spain: empresa instaladora rules, the boletín, EV "
                "chargers, solar, legal notice. Free demo in 24h, €15/month + VAT.",
    service_name="Web design for electricians in Spain",
    audience="English-speaking electricians, EV charger installers and solar installers in Spain",
    crumb_home='Home', crumb='Electricians',
    badge='For electricians working in Spain',
    h1="Websites for <em>electricians</em> in Spain",
    lede="Your services, the areas you cover, a call or a WhatsApp message in one tap, in English and Spanish, and "
         "your authorisation presented accurately. We write it for you and send you a free demo "
         "within 24 hours.",
    pills=['English and Spanish included', 'Spanish rules built in', 'Free demo in 24 hours'],
    cta='Get my free demo', cta2='What Spanish rules require',
    brief_t='In short',
    brief="WebAutonomos builds websites for English-speaking electricians, EV charger installers and solar installers "
          "working in Spain. We present your services, write the copy in English and Spanish (up to four languages) "
          "at no extra cost, and include the information Spanish law expects on a business website, such as a legal "
          "notice with your NIF or NIE, prices for "
          "homeowners shown with VAT included, and the complaint information your region asks for. It costs "
          "<strong>€15 + VAT per month</strong> with no setup fee and no lock-in, or a <strong>one-off €349 + "
          "VAT</strong>. We work with you in English, and your demo is ready within 24 hours.",
    legal_id='rules', legal_ey='Spanish rules', legal_t='What your business and your website have to get right',
    legal_intro="In Spain, electrical work is reserved to registered installation companies, and only they can sign "
                "the certificate that gets an installation connected. Consumer law then sets the rules for quotes, "
                "call-outs and complaints. These are the points that matter.",
    legal_cols=('Topic', 'Law', 'What it means for you'),
    legal_rows=[
        ('Empresa instaladora', 'REBT (RD 842/2002), art. 22; ITC-BT-03',
         "Only an empresa instaladora en baja tensión may install, maintain or repair low-voltage installations. You "
         "file a declaración responsable with the region where you are established; it is valid across Spain with "
         "no expiry date, and the region gives you a number and sends your details to the Registro Integrado "
         "Industrial."),
        ('Requirements', 'ITC-BT-03, §3, §4, §5.8 and Appendix I',
         "At least one qualified instalador en baja tensión for your category (básica or especialista), under any "
         "type of contract since September 2025, and civil liability cover of at least €600,000 per claim for "
         "básica or €900,000 for especialista."),
        ('Installation certificate (boletín)', 'ITC-BT-04, §5.4 and 5.5; ITC-BT-03, §5.9',
         "Only the company that did the work issues the certificado de instalación, signed by one of its own "
         "installers, and the supplier will not connect without it. Supplying certificates for work the company did "
         "not do is prohibited."),
        ('Working without registration', 'Ley 21/1992 de Industria, arts. 31 and 34',
         "Carrying out installations without filing the declaración responsable is a serious offence under the "
         "Industry Act. Catalonia has its own regime, which treats it as very serious."),
        ('EV chargers', 'ITC-BT-52 (RD 1053/2014); ITC-BT-03, §3; Ley de Propiedad Horizontal, art. 17.5',
         "Any empresa instaladora may install a charger: the básica category is enough. In a comunidad, an owner "
         "installing one in their own parking space only has to notify the community beforehand."),
        ('Solar self-consumption', 'RD 244/2019; ITC-BT-03, §3',
         "Installed by an empresa instaladora: básica for generators under 10 kW, especialista from 10 kW. For "
         "low-voltage systems under 100 kW, the region registers the installation itself once the installation "
         "certificate is filed."),
        ROW_EN_QUOTES,
        ROW_EN_COMPLAINTS,
        ROW_EN_NOTICE,
    ],
    legal_note="Registration is handled by your region's industry department, and rules on quotes and complaint forms "
               "are regional too. This is general information as of September 2026, not legal advice.",
    legal_we_t='What we set up for you',
    legal_we=["A proper legal notice with your name, NIF or NIE and contact details, plus your company details if you "
              "trade as an S.L.",
              "Your authorisation described accurately: empresa instaladora category, and only the work it covers",
              "Your call-out terms and your prices for homeowners shown with VAT included",
              "The complaint information your region asks for, such as the QR poster in Andalucía",
              "A call button and WhatsApp always visible on mobile, and your site in up to four languages, English "
              "and Spanish included, at no extra cost"],
    spain_note='<strong>Working in the UK instead?</strong> UK rules are different. See '
               '<a href="https://webautonomos.es/en/web-design-for-electricians">web design for electricians in the UK</a>.',
    sources_t='Sources',
    why_ey='Why us', why_t='Built for tradespeople who work in English',
    why=[('💬', 'We speak your language', "Email, WhatsApp or video call in English: no need to decode Spanish legal "
                                         "or technical jargon."),
         ('🌍', 'Up to four languages, one price', "English, Spanish and up to two more at no extra cost, so Spanish "
                                                   "homeowners find you as easily as expats do."),
         ('🔌', 'Every service in its place', "Repairs, rewires, EV chargers and solar each get their own section, "
                                             "with the authorisation that applies."),
         ('📍', 'Found locally', "Titles and copy written for searches like “electrician Jávea” or “electricista "
                                "Marbella”, in both languages.")],
    where_t='Anywhere in Spain',
    where="Costa Blanca, Costa del Sol, Valencia, Mallorca, Barcelona, Madrid or the Canary Islands: we work "
          "remotely, so where your van is based does not change how we work with you.",
    sect_t='Who it is for',
    sectors=['⚡ Electricians', '🔌 Repairs and fault finding', '🏠 Rewires and upgrades', '🚗 EV chargers',
             '☀️ Solar installers', '💡 Lighting', '🏢 Commercial electrical work', '📶 Smart home and networks'],
    how_t='Your website in three steps',
    steps=[('Tell us about your business', 'Your services, the areas you cover and a few job photos: it takes two '
                                           'minutes.'),
           ('We build your demo', 'Within 24 hours, with your services, your copy in English and Spanish, and your '
                                  'legal pages.'),
           ('You decide', "Ask for any changes you want. If you like it, it goes live; if not, you pay nothing.")],
    price_note=PRIX_EN_BAT,
    extra=[
        ('what-to-include', 'On your website', "What should an electrician's website in Spain show?",
         '<p class="legal-intro">A homeowner wants to see what you do, whether you cover their town, and whether you '
         'can legally sign off the work. These are the parts that answer those questions.</p>'
         '<div class="why-g">'
         '<div class="aud-c"><div class="aud-i" aria-hidden="true">✅</div>'
         '<h3>Your authorisation, stated accurately</h3>'
         '<p>That your business is a registered empresa instaladora, with its category (básica or especialista), '
         'is what tells a customer you can issue the boletín their supplier will ask for.</p></div>'
         '<div class="aud-c"><div class="aud-i" aria-hidden="true">\U0001F5C2️</div>'
         '<h3>Services grouped by type of job</h3>'
         '<p>Repairs and fault finding, rewires, EV chargers and solar each get their own section, so a visitor '
         'finds the work they need without scrolling through everything else.</p></div>'
         '<div class="aud-c"><div class="aud-i" aria-hidden="true">\U0001F4B6</div>'
         '<h3>Clear call-out terms</h3>'
         '<p>Your call-out charge and hourly rate, shown with VAT included for homeowners, so customers know what to '
         'expect before they ring.</p></div>'
         '<div class="aud-c"><div class="aud-i" aria-hidden="true">\U0001F4CD</div>'
         '<h3>The towns you cover</h3>'
         '<p>Naming the towns you work in (Jávea, Marbella or Santa Pola, for example) helps both readers and Google '
         'understand who your site is for.</p></div>'
         '</div>'
         '<p class="where">For a longer read, see our guide to '
         '<a href="https://webautonomos.es/blog/en/website-for-electricians">what an electrician&#8217;s website '
         'needs</a>.</p>'),
        local_search_en(''),
    ],
    faq_t='Frequently asked questions',
    faq=[("Do I need to be registered to work as an electrician in Spain?",
          "Yes. Only an empresa instaladora en baja tensión may install, maintain or repair low-voltage "
          "installations (REBT, art. 22). As a sole trader or company, you file a declaración responsable with the "
          "region where you are established, with at least one qualified installer and civil liability cover of at "
          "least €600,000 per claim for the básica category. Working without it is a serious offence under the "
          "Industry Act (Ley 21/1992), and a very serious one in Catalonia."),
         ("Can I work as an electrician in Spain with UK qualifications?",
          "Not on the strength of the UK certificate alone. Since 1 January 2021 the UK counts as a third country for "
          "qualifications, and there is no regional exam for electricians. The routes are homologation of your "
          "qualification, accreditation of your work experience (legal residence and at least three years, with at "
          "least 2,000 hours worked, in the last 15 years), an ENAC-accredited personal certification, or a Spanish qualification such "
          "as the certificado de profesionalidad ELEE0109."),
         ("What is a boletín and who can issue it?",
          "The boletín is the certificado de instalación eléctrica (CIE). Only the empresa instaladora that did the "
          "work issues it, signed by one of its own qualified installers, and it is filed with the region; the "
          "electricity supplier will not connect a new installation without it. A company may not supply "
          "certificates for work it did not carry out."),
         ("Can I install EV chargers in Spain?",
          "Yes, if your business is a registered empresa instaladora: the básica category covers chargers (ITC-BT-03, "
          "§3). Under ITC-BT-04, a charging installation needs a project above 50 kW, outdoors above 10 kW, or for mode 4 charging. In a comunidad de "
          "propietarios, an owner installing a charger in their own parking space only has to notify the community "
          "beforehand (Ley de Propiedad Horizontal, art. 17.5)."),
         ("Can my customers deduct the cost of a charger or solar panels from income tax?",
          "For 2026, yes, within limits. Homeowners can deduct 15% of the cost of a charger installed by "
          "31 December 2026 in a property they own, on a base of up to €4,000, and a new deduction covers solar "
          "self-consumption installed in 2026: 10%, or 20% in a residential building, on a base of up to €5,000, "
          "with the installation certificate. Payment must be by card, transfer, nominative cheque or bank deposit, "
          "never in cash. Point "
          "customers to the Agencia Tributaria for the details that apply to them."),
         ("When does an installation need an OCA inspection?",
          "Only for the types listed in ITC-BT-05: for example premises open to the public, installations with fire "
          "or explosion risk, swimming pools above 10 kW, or EV charging that needs a project. Under the national "
          "rules, an ordinary home installation does not need an initial inspection by an OCA."),
         FAQ_EN_QUOTE,
         ("Can customers cancel after an emergency call-out?",
          "Not for the urgent repair itself. Under article 103 of the consumer law (TRLGDCU), there is no right of "
          "withdrawal when the customer specifically asked you to visit for an urgent repair or maintenance job. "
          "The 14-day right still applies to extra services you provide during that visit, and to goods other than "
          "the spare parts you necessarily used."),
         FAQ_EN_REVIEWS,
         FAQ_EN_LANGUAGE,
         FAQ_EN_GBP,
         FAQ_EN_PRICE],
    final_t='See your website before you pay a thing',
    final_sd="Free demo within 24 hours, with your services and legal pages. No setup fee, no lock-in.",
)

ELEC_SOURCES = {
    'fr': [
        ("Arrêté du 24 janvier 2017, dépannage dans le bâtiment (Légifrance)",
         'https://www.legifrance.gouv.fr/loda/id/JORFTEXT000033935513'),
        ("Code de l'énergie, art. D342-19, Consuel (Légifrance)",
         'https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000050741348'),
        ("Code de l'énergie, art. D353-2, bornes de recharge (Légifrance)",
         'https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000049851527'),
        ("Arrêté du 6 octobre 2021, obligation d'achat photovoltaïque (Légifrance)",
         'https://www.legifrance.gouv.fr/loda/id/JORFTEXT000044173060'),
        ("Arrêté du 7 juillet 2026, message France Rénov' (Légifrance)",
         'https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000054569418'),
        ("Code de l'artisanat, art. L121-1, qualification (Légifrance)",
         'https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000047362238'),
        ("Médiateur de la consommation (Service-public)", 'https://entreprendre.service-public.gouv.fr/vosdroits/F33338'),
    ],
    'en': [
        ("Low-voltage regulation, REBT (BOE)", 'https://www.boe.es/buscar/act.php?id=BOE-A-2002-18099'),
        ("Industry Act, Ley 21/1992 (BOE)", 'https://www.boe.es/buscar/act.php?id=BOE-A-1992-17363'),
        ("Industrial registry search (Ministerio de Industria)",
         'https://industria.gob.es/registros-industriales/RII/Paginas/consultas-publicas.aspx'),
        ("Self-consumption, RD 244/2019 (BOE)", 'https://www.boe.es/buscar/act.php?id=BOE-A-2019-5089'),
        ("Ley de Propiedad Horizontal (BOE)", 'https://www.boe.es/buscar/act.php?id=BOE-A-1960-10906'),
        ("UK qualifications in Spain (Ministerio de Educación)",
         'https://www.educacionfpydeportes.gob.es/reinounido/en/brexit/titulos-britanicos-en-espan-a.html'),
        ("Spanish consumer law, TRLGDCU (BOE)", 'https://www.boe.es/buscar/act.php?id=BOE-A-2007-20555'),
    ],
}

# ═════════════════════════ ARTISANS DU BÂTIMENT ET BUILDERS (28/09/2026) ══
ARTI = {}
ARTI['fr'] = dict(
    html_lang='fr', og_locale='fr_FR', unit='mois', area=['FR', 'ES'],
    title="Création de site internet pour artisan : 15 €/mois",
    description="Création de site internet pour artisan du bâtiment : réalisations, devis, assurance, médiateur, "
                "encart France Rénov'. Démo gratuite en 24 h, 15 €/mois HT, sans engagement.",
    service_name="Création de site internet pour artisans du bâtiment",
    audience="Artisans du bâtiment et de la rénovation : maçons, peintres, carreleurs, plaquistes, couvreurs, "
             "plombiers, électriciens et menuisiers",
    crumb_home='Accueil', crumb='Artisans du bâtiment',
    badge='Artisans du bâtiment et de la rénovation',
    h1="Création de site internet pour <em>artisan</em> du bâtiment",
    lede="Vos réalisations, vos métiers, les communes où vous intervenez, une demande de devis en un clic, et les "
         "mentions que la loi impose dès que vous travaillez pour des particuliers. Nous l'écrivons pour vous et vous "
         "envoyons une démo gratuite en 24 heures.",
    pills=['Un site vitrine clé en main', 'Mentions obligatoires en ordre', 'Démo gratuite en 24 h'],
    cta='Recevoir ma démo gratuite', cta2='Ce que la loi impose',
    brief_t='En bref',
    brief="WebAutonomos crée des sites internet pour les artisans du bâtiment et de la rénovation (maçons, peintres, "
          "carreleurs, plaquistes, couvreurs, plombiers, électriciens, menuisiers), en France et en Espagne. Nous "
          "mettons vos réalisations en valeur, rédigeons les textes et plaçons, à partir des informations que vous "
          "nous donnez, ce que la loi demande quand vous travaillez pour des particuliers : assurance, médiateur de la consommation, mentions légales et, si vous "
          "proposez de l'isolation ou d'autres travaux de rénovation énergétique, l'encart France Rénov' obligatoire "
          "à partir du 1<sup>er</sup> octobre 2026. Le site coûte <strong>15 € HT par mois</strong> sans frais "
          "d'installation ni engagement, ou <strong>349 € HT en paiement unique</strong>, jusqu'à 4 langues sans "
          "supplément si vous le souhaitez, et la démo est prête en 24 heures.",
    legal_id='regles', legal_ey='Les règles', legal_t="Ce que votre site et vos devis doivent montrer",
    legal_intro="Dès que vous travaillez pour des particuliers, le Code de l'artisanat, le Code des assurances et le "
                "Code de la consommation disent ce que votre site, vos devis et vos factures doivent montrer, et "
                "comment vous pouvez trouver des clients. Voici l'essentiel pour une entreprise du bâtiment en France.",
    legal_cols=('Sujet', 'Texte', 'Ce que ça change pour vous'),
    legal_rows=[
        ("Qualification", "Code de l'artisanat, art. L121-1, R121-1, R121-3 et L151-2",
         "La construction, l'entretien et la réparation des bâtiments ne s'exercent qu'avec une qualification dans "
         "chaque métier exercé (CAP, BEP, titre équivalent ou trois ans d'expérience) ou sous le contrôle effectif et "
         "permanent d'une personne qualifiée. Sinon : 7 500 € d'amende."),
        ("Le mot « artisan »", "Code de l'artisanat, art. L211-1, R211-1, L241-1 et L241-2",
         "Réservé à ceux qui ont la qualité d'artisan : un CAP, un BEP, un titre équivalent ou trois ans "
         "d'expérience dans le métier. L'immatriculation seule ne suffit pas. L'usage abusif du mot dans votre nom, "
         "votre enseigne ou votre publicité est puni de 7 500 € d'amende."),
        ("Assurance décennale", "Code des assurances, art. L241-1, L243-2 et L243-3 ; Code de la consommation, "
                                "art. R111-2",
         "L'attestation se joint à chaque devis et chaque facture, et le client doit pouvoir connaître avant le "
         "contrat votre assureur et la couverture géographique. Travailler sans l'assurance obligatoire est puni de "
         "6 mois de prison et 75 000 € d'amende."),
        ("Devis signé chez le client", "Code de la consommation, art. L221-2, L221-9, L221-10 et L221-18",
         "Un contrat signé au domicile du client lui ouvre 14 jours de rétractation, avec le formulaire type à "
         "remettre, et vous ne pouvez recevoir aucun paiement ni acompte pendant 7 jours. Exceptions : les "
         "réparations urgentes qu'il vous a expressément demandées chez lui, la construction neuve et la "
         "transformation importante d'un bâtiment."),
        ("Démarchage", "Code de la consommation, art. L223-1 et L223-8",
         "Depuis le 11 août 2026, appeler un particulier suppose son accord préalable, sauf contrat en cours. Pour la "
         "rénovation énergétique, les énergies renouvelables et l'adaptation du logement au vieillissement ou au "
         "handicap, l'appel est interdit même avec son accord, comme les SMS, courriels et réseaux sociaux depuis "
         "juillet 2025 : laissez le client venir à vous."),
        ("RGE, labels et aides", "Code de la consommation, art. L121-4, L224-114 et L242-51 ; décret n° 2026-822",
         "Afficher RGE, Qualibat ou un autre label sans l'avoir obtenu est une pratique commerciale trompeuse. Quand "
         "une aide exige un label, vous indiquez par écrit avant le contrat, et dans le contrat, si vous le détenez, "
         "avec le justificatif. Depuis le 1er septembre 2026, MaPrimeRénov' « par geste » ne finance plus "
         "l'isolation, qui reste aidée dans une rénovation d'ampleur."),
        ("Encart France Rénov'", "Code de la consommation, art. L122-26 ; arrêté du 7 juillet 2026",
         "À partir du 1er octobre 2026, un site qui propose de l'isolation, un changement de fenêtres, une pompe à "
         "chaleur ou d'autres travaux de rénovation énergétique d'un logement affiche une bannière avec le message "
         "officiel de France Rénov', cliquable vers le service public. Amende jusqu'à 15 000 € (75 000 € pour une "
         "société)."),
        ROW_MEDIATEUR,
        ROW_MENTIONS,
    ],
    legal_note="Nouveau au 1er octobre 2026 : l'encart France Rénov' devient obligatoire pour les sites qui proposent "
               "des travaux de rénovation énergétique. Si vous faites du dépannage, de la réparation ou de "
               "l'entretien, vos tarifs doivent aussi être accessibles en ligne (arrêté du 24 janvier 2017). Et si "
               "vous affichez des avis clients, indiquez s'ils sont contrôlés et comment, avec leur date (Code de la "
               "consommation, art. L111-7-2). Vous nous fournissez ces informations et validez chaque contenu. "
               "Informations générales à jour en septembre 2026, qui ne remplacent pas un conseil juridique.",
    legal_we_t='Ce que nous mettons en place',
    legal_we=["Votre qualité d'artisan si vous l'avez, votre numéro RNE et votre assurance (assureur, couverture "
              "géographique) indiqués clairement",
              "Les labels (RGE, Qualibat…) seulement si vous les détenez, avec les travaux qu'ils couvrent",
              "L'encart France Rénov' et son lien, si vous proposez de l'isolation ou d'autres travaux de "
              "rénovation énergétique",
              "Un formulaire de demande de devis, un bouton WhatsApp et votre téléphone, pour que le client vous "
              "contacte directement",
              "Les coordonnées de votre médiateur, des mentions légales complètes et des avis présentés avec leur "
              "date et leur mode de contrôle"],
    spain_note="<strong>Vous travaillez en Espagne ?</strong> Les règles changent : droit du client à un devis écrit "
               "préalable dans plusieurs communautés (Valence, Madrid, Catalogne), sauf renonciation manuscrite, "
               "formulaires de réclamation régionaux, permis de travaux délivrés par la mairie, et IVA à 10 % sous "
               "conditions pour la rénovation du logement d'un particulier. Nous connaissons aussi ces règles : "
               "<a href=\"/fr/site-internet-francophones-espagne\">site internet pour francophones en Espagne</a>.",
    sources_t='Sources',
    why_ey='Pourquoi nous', why_t="Pensé pour les artisans du bâtiment",
    why=[('📸', 'Vos chantiers en photos', "Salles de bains, façades, toitures, cloisons : vos réalisations "
                                          "classées par type de travaux, avec avant et après si vous en avez."),
         ('📝', 'Une demande de devis simple', "Formulaire, WhatsApp ou téléphone : le particulier décrit son projet "
                                              "et vous recevez la demande directement."),
         ('📄', 'Les mentions à jour', "Assurance, médiateur, mentions légales, encart France Rénov' : ce que la loi "
                                      "demande est en place, et vous validez chaque contenu."),
         ('📍', 'Trouvé près de chez vous', "Titres et textes pensés pour les recherches « votre métier + votre "
                                           "ville », et votre fiche Google si vous le souhaitez.")],
    where_t='En France et en Espagne',
    where="Nous travaillons à distance, en français, par e-mail, WhatsApp et visioconférence : que votre entreprise "
          "soit en Normandie, en Provence ou sur la Costa Blanca, rien ne change.",
    sect_t='Pour qui',
    sectors=['🧱 Maçons', '🎨 Peintres', '🟫 Carreleurs', '🧰 Plaquistes', '🏠 Couvreurs', '🔧 Plombiers',
             '⚡ Électriciens', '🪵 Menuisiers'],
    how_t='Votre projet en trois étapes',
    steps=[('Vous décrivez votre activité', "Vos métiers, votre zone d'intervention, quelques photos de chantier : "
                                           "deux minutes suffisent."),
           ('Nous préparons votre démo', "En moins de 24 heures, avec vos réalisations, vos textes et vos mentions "
                                        "légales."),
           ('Vous décidez', "Vous demandez les modifications que vous voulez. Si le site vous plaît, il est mis en "
                           "ligne ; sinon, vous ne payez rien.")],
    price_note=PRIX_FR_BAT,
    extra=[
        ('site-vitrine', 'Ce qui convainc', "Que doit contenir le site vitrine d'un artisan ?",
         "<p class=\"legal-intro\">Un site vitrine d'artisan répond à trois questions : faites-vous le type de "
         "travaux que je cherche, intervenez-vous chez moi, et comment vous joindre ? Tout le reste vient en "
         "appui.</p>"
         "<div class=\"why-g\">"
         "<div class=\"aud-c\"><div class=\"aud-i\" aria-hidden=\"true\">📸</div>"
         "<h3>Des réalisations classées par type de travaux</h3>"
         "<p>Une personne qui cherche un ravalement de façade ne veut pas faire défiler des photos de salles de "
         "bains. Nous regroupons vos photos par catégorie, avec une légende : matériau, type de travaux, "
         "ville.</p></div>"
         "<div class=\"aud-c\"><div class=\"aud-i\" aria-hidden=\"true\">📍</div>"
         "<h3>Votre zone d'intervention, nommée</h3>"
         "<p>Citer les communes où vous travaillez permet au visiteur de savoir tout de suite si vous vous "
         "déplacez chez lui, et aide Google à comprendre à qui s'adresse votre site.</p></div>"
         "<div class=\"aud-c\"><div class=\"aud-i\" aria-hidden=\"true\">🛡️</div>"
         "<h3>Votre assurance et vos qualifications</h3>"
         "<p>Votre assureur et votre couverture géographique, que le client doit pouvoir connaître avant le "
         "contrat, et les labels que vous avez réellement obtenus : autant les montrer dès la page d'accueil.</p>"
         "</div>"
         "</div>"
         "<p class=\"where\">Pour aller plus loin, consultez "
         "<a href=\"https://webautonomos.es/blog/fr/site-web-pour-menuisiers-et-renovation\">notre guide pour les "
         "entreprises de rénovation</a>.</p>"),
        ('par-metier', 'Par métier', "Un site d'artisan adapté aux règles de votre métier",
         "<p class=\"legal-intro\">Certains métiers ont leurs propres obligations en ligne. Nous les détaillons "
         "page par page.</p>"
         "<div class=\"why-g\">"
         "<div class=\"aud-c\"><div class=\"aud-i\" aria-hidden=\"true\">🔧</div>"
         "<h3><a href=\"https://webautonomos.es/fr/site-internet-plombier\">Plombiers et chauffagistes</a></h3>"
         "<p>Tarifs de dépannage accessibles en ligne, devis avant intervention, gaz, pompes à chaleur et entretien "
         "des chaudières.</p></div>"
         "<div class=\"aud-c\"><div class=\"aud-i\" aria-hidden=\"true\">⚡</div>"
         "<h3><a href=\"https://webautonomos.es/fr/site-internet-electricien\">Électriciens</a></h3>"
         "<p>Consuel, qualification IRVE pour les bornes de recharge, photovoltaïque et tarifs de dépannage.</p>"
         "</div>"
         "<div class=\"aud-c\"><div class=\"aud-i\" aria-hidden=\"true\">🪵</div>"
         "<h3><a href=\"https://webautonomos.es/fr/site-internet-menuisier\">Menuisiers</a></h3>"
         "<p>Fenêtres et aides, encart France Rénov', réalisations bois, alu et PVC.</p></div>"
         "</div>"),
        visibilite_fr("SEO pour artisans : ce qui est inclus et ce qui est en plus",
                      "<a href=\"https://webautonomos.es/blog/fr/positionner-son-site-dans-le-google-local\">"
                      "positionner votre site dans la recherche locale</a>, "),
    ],
    faq_t='Questions fréquentes',
    faq=[("Que doit contenir le site internet d'un artisan ?",
          "Vos métiers et vos réalisations, les communes où vous intervenez, un moyen simple de demander un devis, et "
          "les mentions obligatoires : identité, coordonnées, numéro d'immatriculation, hébergeur, médiateur de la "
          "consommation si vous travaillez pour des particuliers, et vos tarifs si vous faites du dépannage. Votre "
          "assureur et votre couverture géographique doivent être communiqués avant le contrat : le site est le moyen "
          "le plus simple. Si vous proposez des travaux de rénovation énergétique, ajoutez l'encart France Rénov' à "
          "partir du 1er octobre 2026."),
         ("Puis-je me présenter comme artisan sur mon site ?",
          "Oui si vous avez la qualité d'artisan : un CAP, un BEP, un titre de niveau équivalent ou trois ans "
          "d'expérience dans le métier, en plus de l'immatriculation (Code de l'artisanat, art. R211-1). Utiliser le "
          "mot « artisan » ou un dérivé dans votre nom, votre enseigne ou votre publicité sans y avoir droit est puni "
          "de 7 500 € d'amende (art. L241-2)."),
         ("Faut-il une qualification pour travailler dans le bâtiment ?",
          "Oui. La construction, l'entretien et la réparation des bâtiments, comme les installations électriques, de "
          "gaz et de chauffage, ne peuvent être exercés que par une personne qualifiée ou sous son contrôle effectif "
          "et permanent (Code de l'artisanat, art. L121-1) : CAP, BEP, titre équivalent ou trois ans d'expérience, "
          "pour chaque métier exercé. Sinon : 7 500 € d'amende."),
         ("L'assurance décennale doit-elle figurer sur mon site ?",
          "Aucun texte n'impose ce canal. L'attestation doit être jointe à chaque devis et chaque facture (Code des "
          "assurances, art. L243-2), et le client doit pouvoir connaître votre assureur et la couverture "
          "géographique avant le contrat (Code de la consommation, art. R111-2) : l'indiquer sur votre site est la "
          "façon la plus simple d'y répondre."),
         ("Un client peut-il annuler un devis signé chez lui ?",
          "Oui : un contrat conclu au domicile du client lui ouvre 14 jours de rétractation, avec le formulaire type "
          "joint au contrat, et vous ne pouvez recevoir aucun paiement ni acompte pendant 7 jours (Code de la "
          "consommation, art. L221-9, L221-10 et L221-18). Si le client demande expressément, par écrit, que le "
          "chantier commence avant la fin du délai et se rétracte ensuite, il paie le travail déjà fait (art. L221-25). "
          "Les réparations urgentes qu'il vous a demandées chez lui sont exclues, comme la construction neuve et la "
          "transformation importante d'un bâtiment (art. L221-2)."),
         ("Ai-je le droit de démarcher des clients par téléphone ?",
          "Depuis le 11 août 2026, seulement les particuliers qui y ont consenti au préalable, sauf contrat en cours "
          "(Code de la consommation, art. L223-1). Pour la rénovation énergétique, les énergies renouvelables et "
          "l'adaptation du logement au vieillissement ou au handicap, l'appel est interdit même avec leur accord, et "
          "la prospection par SMS, messagerie, courriel ou réseaux sociaux l'est depuis juillet 2025 (art. L223-8). "
          "Sanctions : jusqu'à 75 000 € d'amende (375 000 € pour une société), et le contrat est nul (art. L242-16 "
          "et L242-16-1)."),
         ("Qu'est-ce que l'encart France Rénov' obligatoire au 1er octobre 2026 ?",
          "À partir du 1er octobre 2026 (Code de la consommation, art. L122-26, et arrêté du 7 juillet 2026), tout "
          "professionnel qui propose des travaux de rénovation énergétique d'un logement, en ligne ou dans sa "
          "publicité, affiche le message officiel : « Avant de vous engager, le service public vous informe "
          "gratuitement pour préparer et sécuriser votre projet : www.france-renov.gouv.fr ». Sur un site, c'est une "
          "bannière cliquable vers le service public. Amende jusqu'à 15 000 € (75 000 € pour une société)."),
         ("L'isolation est-elle encore aidée par MaPrimeRénov' ?",
          "Plus « par geste » : pour les demandes déposées depuis le 1er septembre 2026 (décret n° 2026-822), ce "
          "parcours ne finance plus l'isolation des murs ni des combles. Elle reste aidée dans une rénovation "
          "d'ampleur, pour un logement classé E, F ou G qui gagne au moins deux classes, avec Mon Accompagnateur "
          "Rénov' et au moins deux gestes d'isolation. Les travaux sont faits par une entreprise RGE."),
         ("Faut-il encore une attestation de TVA pour les travaux à taux réduit ?",
          "Non : depuis la loi de finances pour 2025, l'attestation n'est plus obligatoire. Pour la TVA à 10 % ou 5,5 % dans un "
          "logement achevé depuis plus de deux ans, le client certifie sur le devis ou la facture que les travaux "
          "portent sur un tel logement (Code général des impôts, art. 279-0 bis et 278-0 bis A). Pour une réparation "
          "ou un entretien de moins de 1 000 € TTC, cette mention n'est pas exigée, mais la facture indique le nom et "
          "l'adresse du client et de l'immeuble, la nature des travaux et l'ancienneté du logement."),
         ("Quelles garanties dois-je à mes clients après les travaux ?",
          "Pour des travaux qui constituent un ouvrage (construction, rénovation lourde), à partir de leur réception : "
          "un an de garantie de parfait achèvement pour les désordres "
          "signalés (Code civil, art. 1792-6), au moins deux ans de garantie de bon fonctionnement pour les "
          "équipements dissociables (art. 1792-3), et dix ans de garantie décennale pour les dommages qui "
          "compromettent la solidité de l'ouvrage ou le rendent impropre à sa destination (art. 1792)."),
         ("La facture électronique me concerne-t-elle ?",
          "Oui, pour les factures entre entreprises. Depuis le 1er septembre 2026, toutes les entreprises, artisans "
          "compris, doivent pouvoir recevoir des factures électroniques ; pour les TPE et PME, l'émission devient "
          "obligatoire le 1er septembre 2027. Pour les travaux facturés à des particuliers, c'est la transmission "
          "des données de vente à l'administration qui s'applique, à la même date."),
         FAQ_AVIS,
         ("Le SEO pour artisans est-il inclus dans le prix ?",
          "Le référencement de base est inclus : titres et textes construits autour de vos métiers et des communes "
          "où vous intervenez. Le SEO Local (quatre articles de blog par mois, mots-clés locaux, rapport mensuel) est "
          "un service séparé à 15 € HT par mois, tout comme la gestion de votre fiche Google (29 € HT par mois, plus "
          "49 € HT de création si vous n'avez pas encore de fiche) : les deux s'achètent indépendamment de "
          "l'abonnement."),
         faq_prix_fr('artisan')],
    final_t='Voyez votre site avant de payer quoi que ce soit',
    final_sd="Démo gratuite en 24 heures, avec vos réalisations et vos mentions légales. Sans frais d'installation, "
             "sans engagement.",
)

ARTI['en'] = dict(
    html_lang='en', og_locale='en_GB', unit='month', area=['ES'],
    title="Websites for builders in Spain: €15/month, free demo",
    description="Websites for English-speaking builders and renovation companies in Spain: permits, quotes, 10% VAT, "
                "asbestos, legal notice. Free demo in 24h, €15/month + VAT.",
    service_name="Web design for builders and renovation companies in Spain",
    audience="English-speaking builders, renovation companies, painters, tilers and roofers in Spain",
    crumb_home='Home', crumb='Builders and renovations',
    badge='For builders and renovation companies in Spain',
    h1="Websites for <em>builders</em> and renovation companies in Spain",
    lede="Your projects in photos, the areas you cover, a quote request in one click, in English and Spanish, and the "
         "information Spanish consumer law expects. We write it for you and send you a free demo within 24 hours.",
    pills=['English and Spanish included', 'Spanish rules built in', 'Free demo in 24 hours'],
    cta='Get my free demo', cta2='What Spanish rules require',
    brief_t='In short',
    brief="WebAutonomos builds websites for English-speaking builders, renovation companies, painters, tilers and "
          "roofers working in Spain. We show your projects, write the copy in English and Spanish (up to four "
          "languages) at no extra cost, and include the information Spanish law expects on a business website, such "
          "as a legal notice with your NIF or NIE, "
          "prices for homeowners shown with VAT included, and the complaint information your region asks for. It "
          "costs <strong>€15 + VAT per month</strong> with no setup fee and no lock-in, or a <strong>one-off €349 + "
          "VAT</strong>. We work with you in English, and your demo is ready within 24 hours.",
    legal_id='rules', legal_ey='Spanish rules', legal_t='What your business and your website have to get right',
    legal_intro="Building work in Spain is not a licensed trade in itself, but permits, consumer law, tax and a few "
                "specific rules, such as asbestos, decide what you can advertise and how you quote. These are the "
                "points that matter.",
    legal_cols=('Topic', 'Law', 'What it means for you'),
    legal_rows=[
        ('Building permits', 'TRLSRU (RDLeg 7/2015), art. 11.3; regional planning laws',
         "Works need either a licencia de obra or a declaración responsable filed with the town hall, depending on "
         "their size. The owner usually files it, but regional laws (Madrid, Valencia, Andalucía) can also fine the "
         "builder and have the site stopped when works go ahead without one."),
        ROW_EN_QUOTES,
        ('Contracts signed at the customer\'s home', 'Consumer law (TRLGDCU), arts. 99.3, 102 and 103',
         "The customer has 14 days to cancel, or 30 days if your visit was not requested. Work can start earlier "
         "only at their express request on a durable medium, and there is no right to cancel an urgent repair they "
         "called you out for."),
        ('Asbestos (uralita)', 'RD 396/2006, arts. 11, 12 and 17',
         "Only companies registered in the RERA may remove asbestos-cement roofs or pipes, with a work plan approved "
         "by the regional labour authority before each job (or a general plan for short, unplanned jobs). Don't advertise uralita removal unless you are "
         "registered."),
        ('Construction waste', 'RD 105/2008, arts. 2 and 5 and DA 1ª; Ley 7/2022',
         "On larger jobs you are the legal holder of the waste: use an authorised waste manager and keep the delivery "
         "records for five years. Rubble from minor home repairs follows the town hall's bylaws."),
        ('10% VAT', 'Ley 37/1992, art. 91.Uno.2.10º',
         "Renovation or repair of a home at least two years old, for an individual using it privately (not rented "
         "out) or a comunidad de propietarios, with materials costing no more than 40% of the price before VAT."),
        ('Cash payments', 'Ley 7/2012, art. 7',
         "A job worth €1,000 or more cannot be paid in cash, and instalments on the same job count together. The "
         "limit is €10,000 for private individuals whose tax residence is outside Spain."),
        ROW_EN_COMPLAINTS,
        ROW_EN_NOTICE,
    ],
    legal_note="Permits are municipal, and rules on quotes and complaint forms are regional, so check with your town "
               "hall and your comunidad autónoma. This is general information as of September 2026, not legal "
               "advice.",
    legal_we_t='What we set up for you',
    legal_we=["A proper legal notice with your name, NIF or NIE and contact details, plus your company details if you "
              "trade as an S.L.",
              "Prices for homeowners shown with VAT included, and your services described accurately, including "
              "any registration they need",
              "The complaint information your region asks for, such as the QR poster in Andalucía",
              "A quote request form, a WhatsApp button and your phone number, so customers contact you directly",
              "Customer reviews shown with a note on how they are checked, and your site in up to four languages, "
              "English and Spanish included, at no extra cost"],
    spain_note='<strong>Working in the UK instead?</strong> UK rules are different. See '
               '<a href="https://webautonomos.es/en/web-design-for-tradesmen">web design for tradesmen in the UK</a>.',
    sources_t='Sources',
    why_ey='Why us', why_t='Built for builders who work in English',
    why=[('💬', 'We speak your language', "Email, WhatsApp or video call in English: no need to decode Spanish legal "
                                         "or technical jargon."),
         ('🌍', 'Up to four languages, one price', "English, Spanish and up to two more at no extra cost, so Spanish "
                                                   "homeowners find you as easily as expats do."),
         ('📸', 'Your projects, shown properly', "Kitchens, bathrooms, full renovations, roofs: your project photos "
                                                "organised by type of job."),
         ('📍', 'Found locally', "Titles and copy written for searches like “builder Jávea” or “reformas "
                                "Torrevieja”, in both languages.")],
    where_t='Anywhere in Spain',
    where="Costa Blanca, Costa del Sol, Valencia, Mallorca, Barcelona, Madrid or the Canary Islands: we work "
          "remotely, so where your yard is does not change how we work with you.",
    sect_t='Who it is for',
    sectors=['🏗️ Builders', '🏠 Renovation companies', '🎨 Painters and decorators', '🟫 Tilers',
             '🏘️ Roofers', '🧱 Bricklayers', '🛁 Kitchen and bathroom fitters', '🏊 Pool builders'],
    how_t='Your website in three steps',
    steps=[('Tell us about your business', 'Your trades, the areas you cover and a few project photos: it takes two '
                                           'minutes.'),
           ('We build your demo', 'Within 24 hours, with your projects, your copy in English and Spanish, and your '
                                  'legal pages.'),
           ('You decide', "Ask for any changes you want. If you like it, it goes live; if not, you pay nothing.")],
    price_note=PRIX_EN_BAT,
    extra=[
        ('what-to-include', 'On your website', "What should a builder's website in Spain show?",
         '<p class="legal-intro">A homeowner comparing builders wants to see finished work like theirs, know that '
         'you cover their town, and find a simple way to ask for a quote.</p>'
         '<div class="why-g">'
         '<div class="aud-c"><div class="aud-i" aria-hidden="true">\U0001F5C2️</div>'
         '<h3>A portfolio organised by type of job</h3>'
         '<p>Kitchens, bathrooms, full renovations, roofs and pools, grouped so a visitor looking for one type of '
         'work does not scroll past the others. We build it from your own project photos.</p></div>'
         '<div class="aud-c"><div class="aud-i" aria-hidden="true">\U0001F4CD</div>'
         '<h3>The areas you cover, stated clearly</h3>'
         '<p>Naming the towns you work in (Jávea, Torrevieja or Marbella, for example) helps both readers and '
         'Google understand who your site is for.</p></div>'
         '<div class="aud-c"><div class="aud-i" aria-hidden="true">\U0001F4DD</div>'
         '<h3>How you quote and get paid</h3>'
         '<p>A written quote, a clear payment schedule and payment by transfer: saying so on your website reassures '
         'customers who have heard about renovation problems.</p></div>'
         '</div>'
         '<p class="where">For a longer read, see our article on '
         '<a href="https://webautonomos.es/blog/en/website-for-carpenters-and-renovations">websites for carpenters '
         'and renovation companies</a>.</p>'),
        ('by-trade', 'By trade', 'A website that fits the rules of your trade',
         '<p class="legal-intro">Some trades have their own rules in Spain. We cover them page by page.</p>'
         '<div class="why-g">'
         '<div class="aud-c"><div class="aud-i" aria-hidden="true">\U0001F527</div>'
         '<h3><a href="https://webautonomos.es/en/website-for-plumbers-in-spain">Plumbers and heating '
         'engineers</a></h3>'
         '<p>RITE authorisation for heating and air conditioning, gas installers, F-gas certificates and urgent '
         'call-outs.</p></div>'
         '<div class="aud-c"><div class="aud-i" aria-hidden="true">⚡</div>'
         '<h3><a href="https://webautonomos.es/en/website-for-electricians-in-spain">Electricians</a></h3>'
         '<p>Registration as an empresa instaladora, the boletín, EV chargers and solar self-consumption.</p></div>'
         '<div class="aud-c"><div class="aud-i" aria-hidden="true">\U0001FAB5</div>'
         '<h3><a href="https://webautonomos.es/en/website-for-carpenters-in-spain">Carpenters and joiners</a></h3>'
         '<p>Written quotes, 10% VAT on home renovation, and when you need to register in the REA.</p></div>'
         '</div>'),
        local_search_en(''),
    ],
    faq_t='Frequently asked questions',
    faq=[("Who has to get the building permit, me or the homeowner?",
          "The owner, as promoter of the works, usually files the licencia de obra or declaración responsable with "
          "the town hall. But regional planning laws also hold the builder responsible: in the Comunidad de Madrid, "
          "the Comunitat Valenciana and Andalucía, the builder who carries out works without the required permit can "
          "be fined and see the site stopped. Check that the permit exists before you start."),
         ("Do the LOE 1, 3 and 10-year guarantees apply to renovation work?",
          "Only to new builds and to works that change a building's architectural configuration: a full refurbishment, "
          "essential changes to the façade, volume or structure, or a change of use (Ley 38/1999, arts. 2 and 17). "
          "Those works, and works on protected buildings, need a project, signed by an architect for homes (art. 10). An ordinary kitchen or bathroom refit falls "
          "outside the LOE; consumer law and your contract apply instead."),
         ("Can I remove uralita (asbestos) roofing?",
          "Only if your company is registered in the RERA, the register of companies working with asbestos, and the "
          "regional labour authority has approved a work plan for that job (RD 396/2006, arts. 11, 12 and 17). "
          "Otherwise, leave it to a registered specialist and don't advertise the service."),
         ("Can I charge 10% VAT on renovation work?",
          "Mainly for renovation or repair of a home: the customer is an individual using it privately (not rented "
          "out) or a comunidad de propietarios, the home is at least two years old, and the materials you supply "
          "cost no more than 40% of the price before VAT. Otherwise the rate is 21%. It's good practice to state the "
          "cost of materials, or that they don't exceed 40% of the price before VAT."),
         ("Can my customers claim tax relief on energy-efficiency work?",
          "For work paid by 31 December 2026, homeowners can deduct 20% or 40% of energy-efficiency works from income "
          "tax, and 60% for works on a whole residential building until the end of 2027. They need energy "
          "certificates before and after the works, issued by a qualified technician (the one after the works "
          "before 1 January 2027 for the 20% and 40% deductions), and must pay by card, transfer, nominative cheque "
          "or bank deposit, never in cash. Equipment running on fossil fuels, such as gas boilers, does not count."),
         ("Can customers pay me in cash?",
          "Not if the job is worth €1,000 or more, and splitting the price into smaller cash payments doesn't help: "
          "they are added together (Ley 7/2012, art. 7). For private individuals whose tax residence is outside Spain, the limit is €10,000. Payment by "
          "bank transfer also leaves the record your customer needs for any tax deduction."),
         FAQ_EN_QUOTE,
         ("Do I need to register in the REA?",
          "If you work as a contractor or subcontractor on a construction site where there is subcontracting, you "
          "must be registered in the REA, unless you're self-employed with no employees (Ley 32/2006). There is no "
          "obligation to show an REA number on your website."),
         FAQ_EN_COMPLAINTS,
         FAQ_EN_REVIEWS,
         FAQ_EN_LANGUAGE,
         FAQ_EN_GBP,
         FAQ_EN_PRICE],
    final_t='See your website before you pay a thing',
    final_sd="Free demo within 24 hours, with your projects and legal pages. No setup fee, no lock-in.",
)

ARTI_SOURCES = {
    'fr': [
        ("Code de l'artisanat, art. L121-1, qualification (Légifrance)",
         'https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000047362238'),
        ("Assurance décennale (Service-public)", 'https://entreprendre.service-public.gouv.fr/vosdroits/F2034'),
        ("Arrêté du 7 juillet 2026, message France Rénov' (Légifrance)",
         'https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000054569418'),
        ("Décret n° 2026-822, MaPrimeRénov' (Légifrance)", 'https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000054750363'),
        ("MaPrimeRénov' rénovation d'ampleur (France Rénov')",
         'https://france-renov.gouv.fr/aides/maprimerenov-renovation-ampleur'),
        ("Médiateur de la consommation (Service-public)", 'https://entreprendre.service-public.gouv.fr/vosdroits/F33338'),
        ("Facturation électronique : calendrier (impots.gouv.fr)",
         'https://www.impots.gouv.fr/professionnel/questions/partir-de-quand-suis-je-concerne-par-la-reforme-de-la-facturation'),
    ],
    'en': [
        ("Land and urban planning law, TRLSRU (BOE)", 'https://www.boe.es/buscar/act.php?id=BOE-A-2015-11723'),
        ("Building Act, Ley 38/1999 (BOE)", 'https://www.boe.es/buscar/act.php?id=BOE-A-1999-21567'),
        ("Asbestos, RD 396/2006 (BOE)", 'https://www.boe.es/buscar/act.php?id=BOE-A-2006-6474'),
        ("Construction waste, RD 105/2008 (BOE)", 'https://www.boe.es/buscar/act.php?id=BOE-A-2008-2486'),
        ("VAT on home repairs, FAQ (Tax Agency)",
         'https://sede.agenciatributaria.gob.es/Sede/iva/iva-operaciones-inmobiliarias/preguntas-frecuentes-sobre-obras-reparaciones-inmuebles.html'),
        ("Home renovations (Comunidad de Madrid)", 'https://www.comunidad.madrid/consumo/reformas-hogar'),
        ("Spanish consumer law, TRLGDCU (BOE)", 'https://www.boe.es/buscar/act.php?id=BOE-A-2007-20555'),
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
    'menuisiers': dict(
        es='/carpinteros/',
        fr='/fr/site-internet-menuisier',
        en='/en/website-for-carpenters-in-spain',
        C=MENU, SOURCES=MENU_SOURCES,
        avis_ordre=['Lee Robinson', 'Amelle B.', 'Fabiana', 'Sabine O.', 'Ana Saiz', 'Analía', 'Begoña Cid', 'Inés'],
        llms={'fr': ("- [Site internet pour psychologues et thérapeutes](https://webautonomos.es/fr/site-internet-psychologue-therapeute)",
                     "Site internet pour menuisiers"),
              'en': ("- [Websites for therapists and psychologists in Spain](https://webautonomos.es/en/website-for-therapists-in-spain)",
                     "Websites for carpenters and joiners in Spain")},
        tags={'fr': ['🪵 Menuisiers', '🪟 Aluminium et PVC'],
              'en': ['🪵 Carpenters', '🪟 Aluminium & PVC']},
    ),
    'kines': dict(
        es='/fisioterapeutas/',
        fr='/fr/site-internet-kinesitherapeute',
        en='/en/website-for-physiotherapists-in-spain',
        C=KINE, SOURCES=KINE_SOURCES,
        avis_ordre=['Ana Saiz', 'Analía', 'Sabine O.', 'Begoña Cid', 'Inés', 'Fabiana', 'Amelle B.', 'Lee Robinson'],
        llms={'fr': ("- [Site internet pour menuisiers](https://webautonomos.es/fr/site-internet-menuisier)",
                     "Site internet pour kinésithérapeutes"),
              'en': ("- [Websites for carpenters and joiners in Spain](https://webautonomos.es/en/website-for-carpenters-in-spain)",
                     "Websites for physiotherapists in Spain")},
        tags={'fr': ['💆 Kinésithérapeutes'],
              'en': ['💆 Physiotherapists']},
    ),
    'dentistes': dict(
        es='/dentistas/',
        fr='/fr/site-internet-dentiste',
        en='/en/website-for-dentists-in-spain',
        C=DENT, SOURCES=DENT_SOURCES,
        avis_ordre=['Ana Saiz', 'Analía', 'Sabine O.', 'Begoña Cid', 'Inés', 'Fabiana', 'Amelle B.', 'Lee Robinson'],
        llms={'fr': ("- [Site internet pour kinésithérapeutes](https://webautonomos.es/fr/site-internet-kinesitherapeute)",
                     "Site internet pour chirurgiens-dentistes"),
              'en': ("- [Websites for physiotherapists in Spain](https://webautonomos.es/en/website-for-physiotherapists-in-spain)",
                     "Websites for dentists and dental clinics in Spain")},
        tags={'fr': ['🦷 Dentistes'],
              'en': ['🦷 Dentists']},
    ),
    'plombiers': dict(
        es='/fontaneros/',
        fr='/fr/site-internet-plombier',
        en='/en/website-for-plumbers-in-spain',
        C=PLOMB, SOURCES=PLOMB_SOURCES,
        avis_ordre=['Lee Robinson', 'Amelle B.', 'Fabiana', 'Sabine O.', 'Ana Saiz', 'Analía', 'Begoña Cid', 'Inés'],
        llms={'fr': ("- [Site internet pour chirurgiens-dentistes](https://webautonomos.es/fr/site-internet-dentiste)",
                     "Site internet pour plombiers et chauffagistes"),
              'en': ("- [Websites for dentists and dental clinics in Spain](https://webautonomos.es/en/website-for-dentists-in-spain)",
                     "Websites for plumbers and heating engineers in Spain")},
        tags={'fr': ['🔧 Plombiers', '❄️ Climatisation'],
              'en': ['🔧 Plumbers', '❄️ Air conditioning']},
    ),
    'electriciens': dict(
        es='/electricistas/',
        fr='/fr/site-internet-electricien',
        en='/en/website-for-electricians-in-spain',
        C=ELEC, SOURCES=ELEC_SOURCES,
        avis_ordre=['Lee Robinson', 'Amelle B.', 'Fabiana', 'Sabine O.', 'Ana Saiz', 'Analía', 'Begoña Cid', 'Inés'],
        llms={'fr': ("- [Site internet pour plombiers et chauffagistes](https://webautonomos.es/fr/site-internet-plombier)",
                     "Site internet pour électriciens"),
              'en': ("- [Websites for plumbers and heating engineers in Spain](https://webautonomos.es/en/website-for-plumbers-in-spain)",
                     "Websites for electricians in Spain")},
        tags={'fr': ['⚡ Électriciens'],
              'en': ['⚡ Electricians']},
    ),
    'artisans': dict(
        es='/reformas/',
        fr='/fr/site-internet-artisan',
        en='/en/website-for-builders-in-spain',
        C=ARTI, SOURCES=ARTI_SOURCES,
        avis_ordre=['Lee Robinson', 'Amelle B.', 'Fabiana', 'Sabine O.', 'Ana Saiz', 'Analía', 'Begoña Cid', 'Inés'],
        llms={'fr': ("- [Site internet pour électriciens](https://webautonomos.es/fr/site-internet-electricien)",
                     "Site internet pour artisans du bâtiment"),
              'en': ("- [Websites for electricians in Spain](https://webautonomos.es/en/website-for-electricians-in-spain)",
                     "Websites for builders and renovation companies in Spain")},
        tags={'fr': ['🏗️ Rénovation', '🎨 Peintres'],
              'en': ['🏗️ Builders & renovations', '🎨 Painters & decorators']},
    ),
}

CSS_METIER = """
/* ─── pages métier (build_metier_pages.py) ─── */
.spain-note { max-width:760px; margin:18px auto 0; background:var(--off); border:1.5px solid var(--border); border-radius:12px; padding:14px 18px; font-size:.93rem; color:#334155; line-height:1.6; }
.spain-note a { color:var(--blue); font-weight:600; }
/* tableau des règles en fiches sur mobile : la 3e colonne restait hors écran (24/09/2026) */
@media (max-width:640px) {
  .lt-wrap { overflow:visible; }
  table.lt { min-width:0; }
  table.lt thead { display:none; }
  table.lt tr { display:block; padding:14px 16px; border-bottom:1px solid var(--border); }
  table.lt tr:last-child { border-bottom:none; }
  table.lt tbody th, table.lt td { display:block; padding:0; border:none; }
  table.lt td.law { margin:4px 0 8px; font-size:.82rem; }
}
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
    # sections supplémentaires facultatives (contenu utile ajouté par le rédacteur, cf. REGLES_REDACTEUR.md §2)
    # (la classe alt posée ici est provisoire : H.alterner_fonds recalcule les fonds de toute la page)
    extra_html = ''.join(
        '\n\n<section class="blk%s" id="%s">\n  %s<h2 style="margin-bottom:36px">%s</h2>\n  %s\n</section>'
        % (' alt' if idx % 2 == 0 else '', eid, '<p class="ey">%s</p>\n  ' % E(ey) if ey else '', h2, body)
        for idx, (eid, ey, h2, body) in enumerate(c.get('extra', [])))
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

    return H.alterner_fonds(f"""<!DOCTYPE html>
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
    <p class="srcs">{E(c['sources_t'])}{' :' if lang == 'fr' else ':'} {srcs}</p>
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
        open(rel, 'w', encoding='utf-8').write(poser_photo(rel, s))
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
