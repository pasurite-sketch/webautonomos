# -*- coding: utf-8 -*-
"""FAQ commerciales hors circuit alignées sur VERITE.md (29/09/2026).

Pages faites à la main, que le circuit SEO ne traite pas : /fr/questions, /en/faq,
/preguntas, /servicios, /en/how. Chaque correction remplace une phrase contraire
à VERITE.md, dans le texte visible et dans le JSON-LD FAQPage (même phrase aux
deux endroits, d'où les comptes attendus).

  - « modifications sans facture » -> une modification par mois (VERITE §2) ;
  - « la majorité des recherches se font sur mobile » : aucun chiffre sourcé (§7) ;
  - « la plupart de nos clients » / « hors d'Espagne » : clients en France
    et au Royaume-Uni acceptés (§1), aucune affirmation sur les clients (§6) ;
  - « site retiré à la fin du mois » : non écrit dans VERITE ; résiliation = prévenir
    par email ou WhatsApp et arrêter de payer (§2) ;
  - « aucun coût caché » sans le renouvellement du domaine (~12 €/an, §2) ;
    « garantizamos » / « guaranteed » (§4) ; services facturés à part (§5) ;
  - « la mayoría de / most autónomos pueden deducir el IVA » (§8) ;
  - « professional images » quand le client n'a pas de photos (§2 : photos du client).

/precios porte la même phrase sur l'IVA mais reste gelée jusqu'au 22/10/2026
(pages.json) : à corriger après ce contrôle.

Idempotent. Usage : python3 _tools/patch_faq_verite_20260929.py [--check]
"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
CHECK = '--check' in sys.argv

# (fichier, ancien, nouveau, nombre attendu)
R = [
    # /fr/questions
    ('fr/questions.html',
     "Aucun, et c'est vérifiable ligne par ligne. Les 15 €/mois couvrent la conception graphique sur mesure, "
     "l'hébergement sur serveurs européens, le nom de domaine la première année, le certificat SSL, la maintenance "
     "technique, les sauvegardes automatiques et l'assistance par courriel et WhatsApp. Il n'y a ni frais "
     "d'installation, ni frais d'activation, ni option facturée en supplément.",
     "Aucun, et c'est vérifiable ligne par ligne. Les 15 €/mois couvrent la conception graphique sur mesure, "
     "l'hébergement sur serveurs européens, le nom de domaine la première année (ensuite environ 12 € par an), le "
     "certificat SSL, la maintenance technique, les sauvegardes quotidiennes et l'assistance par email et WhatsApp. "
     "Il n'y a ni frais d'installation ni frais d'activation. Les services à part, comme le SEO Local ou la gestion "
     "de votre fiche Google, ne sont facturés que si vous les demandez.", 2),
    ('fr/questions.html',
     "pas de clause de résiliation : vous cessez de payer et le site est retiré à la fin du mois en cours.",
     "pas de clause de résiliation : vous nous prévenez par email ou WhatsApp et vous cessez de payer.", 2),
    ('fr/questions.html',
     "Oui, et c'est compris dans l'abonnement. Vous nous envoyez un message avec ce qu'il faut changer — un tarif, "
     "une photo, un horaire, une prestation — et nous le faisons. Pas de facture à la modification, pas de forfait "
     "d'heures à consommer.",
     "Oui : une modification par mois est comprise, dans les deux formules et sans limite de durée. Vous nous "
     "envoyez un message avec ce qu'il faut changer — un tarif, une photo, un horaire, une prestation — et nous le "
     "faisons. Un changement plus important, comme une refonte ou une nouvelle grande section, se fait sur devis "
     "fermé.", 2),
    ('fr/questions.html',
     "Oui, et c'est même la priorité de conception. La majorité des recherches de services locaux se font sur "
     "mobile : le bouton d'appel",
     "Oui, et c'est même la priorité de conception. Beaucoup de vos clients vous chercheront depuis leur "
     "téléphone : le bouton d'appel", 2),
    ('fr/questions.html',
     "Notre activité est installée dans la Communauté valencienne et la plupart de nos clients y exercent. "
     "Écrivez-nous pour tout projet situé ailleurs : nous vous dirons honnêtement si nous sommes le bon "
     "interlocuteur pour votre marché.",
     "Oui. Nous sommes installés dans la province de Valencia et nous travaillons à distance, par email, WhatsApp "
     "et visioconférence, avec des entreprises en Espagne, en France et au Royaume-Uni. Pour une entreprise "
     "installée en France, le site utilise un nom de domaine en .fr, compris la première année.", 2),
    # /en/faq
    ('en/faq.html', "None, guaranteed. The", "None. The", 2),
    ('en/faq.html', "a .es domain for the first year,", "a .es domain for the first year (then about €12 a year),", 2),
    ('en/faq.html',
     "Most autónomos and companies can deduct it; some activities that are exempt from VAT, such as healthcare, "
     "cannot.",
     "If your activity is exempt from VAT, as healthcare is, you cannot deduct it.", 1),
    # /preguntas et /servicios
    ('preguntas.html', "Ninguno, te lo garantizamos. Los", "Ninguno. Los", 2),
    ('preguntas.html', "dominio .es el primer año,", "dominio .es el primer año (después, unos 12 €/año),", 2),
    ('preguntas.html',
     "La mayoría de autónomos y empresas pueden deducirlo; las actividades exentas de IVA, como las sanitarias, no.",
     "Si tu actividad está exenta de IVA, como las sanitarias, no podrás deducirlo.", 1),
    ('servicios.html',
     "La mayoría de autónomos y empresas pueden deducirlo; las actividades exentas de IVA, como las sanitarias, no.",
     "Si tu actividad está exenta de IVA, como las sanitarias, no podrás deducirlo.", 1),
    # /en/how
    ('en/how.html',
     "and we use your photos if you have some. If you don't, we use professional images.",
     "and we use your photos: the ones on your Google Business Profile or the ones you send us.", 2),
]


def main():
    fichiers = {}
    for rel, a, b, n in R:
        s = fichiers.get(rel) or open(rel, encoding='utf-8').read()
        na, nb = s.count(a), s.count(b)
        if na == n:
            s = s.replace(a, b)
        elif not (na == 0 and nb >= n):
            sys.exit('ABANDON : %s : « %s… » trouvé %dx (attendu %d). Rien écrit.' % (rel, a[:50], na, n))
        fichiers[rel] = s
    for rel, s in fichiers.items():
        if open(rel, encoding='utf-8').read() == s:
            print('  = %s déjà à jour' % rel)
        elif CHECK:
            print('  ✓ %s à modifier — non écrit' % rel)
        else:
            open(rel, 'w', encoding='utf-8').write(s)
            print('  ✓ %s modifié' % rel)


if __name__ == '__main__':
    main()
