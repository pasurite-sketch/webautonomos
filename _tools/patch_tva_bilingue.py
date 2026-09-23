# -*- coding: utf-8 -*-
"""TVA des clients français et offre bilingue (24/09/2026, décisions d'Angelino).

1. TVA — clients installés en France : factures SANS TVA ; le client déclare
   la TVA française lui-même (autoliquidation). Clients en Espagne : IVA 21 %.
   Pages : /fr/tarifs, /fr/prestations, /fr/questions (note sous les prix),
   /fr/ (générateur build_lang_homes.py), page thérapeutes FR
   (build_metier_pages.py). La page francophones en Espagne dit déjà « la TVA
   espagnole (21 %) s'ajoute » : inchangée.
2. Site bilingue sans supplément — ajouté :
   - listes « inclus » de /fr/, /en/ (build_lang_homes.py), /fr/tarifs,
     /en/pricing et /en/services (deux lignes fusionnées pour garder un nombre
     pair de cases) ;
   - pages expatriés FR et EN (build_expat_pages.py) : « En bref » et une
     question de FAQ ;
   - pages thérapeutes FR et EN (build_metier_pages.py) : « En bref », et la
     question anglaise sur la langue ;
   - comparatif anglais (paragraphe « A second language ») ;
   - llms.txt (section Oferta).
   Au passage, /fr/tarifs : « Modifications de contenu à la demande » devient
   « Une modification de contenu par mois » (l'offre).

Puis relance build_expat_pages.py et build_metier_pages.py (qui relance
build_lang_homes.py et generate_sitemap.py).

Sauvegarde : ~/webautonomos-work/backups/tva_bilingue_<date>/
Abandon total, rien d'écrit, si une vérification échoue.

À lancer depuis ~/webautonomos :
    python3 _tools/patch_tva_bilingue.py
"""
import datetime
import os
import re
import shutil
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def abandon(msg):
    sys.exit('ABANDON : %s\nRien n\'a été modifié.' % msg)


TVA_FR_AVANT = ("Prix hors taxes. La plupart des entreprises récupèrent la TVA ; ce n'est pas le cas en franchise en "
                "base de TVA (micro-entrepreneurs) ni pour les activités exonérées, comme la santé.")
TVA_FR_APRES = ("Prix hors taxes. En France, nous facturons sans TVA : vous la déclarez vous-même (autoliquidation) "
                "et la récupérez, sauf en franchise en base ou pour une activité exonérée, comme la santé. En Espagne, "
                "l'IVA de 21 % s'ajoute.")

PATCHES = {
    'fr/tarifs.html': [
        (TVA_FR_AVANT, TVA_FR_APRES),
        ('    <li>Sauvegardes automatiques quotidiennes</li>\n    <li>Maintenance technique et mises à jour</li>\n',
         '    <li>Sauvegardes quotidiennes, maintenance et mises à jour</li>\n'
         '    <li>Site bilingue sans supplément (français et espagnol, par exemple)</li>\n'),
        ('    <li>Modifications de contenu à la demande</li>\n', '    <li>Une modification de contenu par mois</li>\n'),
    ],
    'fr/prestations.html': [(TVA_FR_AVANT, TVA_FR_APRES)],
    'fr/questions.html': [(TVA_FR_AVANT, TVA_FR_APRES)],
    'en/pricing.html': [
        ('    <li>Daily automatic backups</li>\n    <li>Technical maintenance and updates</li>\n',
         '    <li>Daily backups, maintenance and updates</li>\n'
         '    <li>Bilingual site in English and Spanish at no extra cost</li>\n'),
    ],
    'en/services.html': [
        ('    <li>Hosting and domain name in your name</li>\n    <li>SSL certificate (https)</li>\n',
         '    <li>Hosting, SSL and a domain name in your name</li>\n'
         '    <li>English and Spanish at no extra cost</li>\n'),
    ],
    'en/best-website-builders-for-freelancers-in-spain.html': [
        ('on Webnode, for example, it starts with the Standard plan.</p>',
         'on Webnode, for example, it starts with the Standard plan. At WebAutonomos, a site in English and Spanish '
         'costs nothing extra.</p>'),
    ],
    'llms.txt': [
        ('- Entrega: 24 horas\n', '- Entrega: 24 horas\n- Web bilingüe (dos idiomas) sin coste adicional\n'),
    ],
    '_tools/build_lang_homes.py': [
        ("       'Mentions légales, confidentialité et cookies', 'Sauvegardes quotidiennes',\n"
         "       'Surveillance 24 h/24 et maintenance technique', 'Une modification par mois'],",
         "       'Mentions légales, confidentialité et cookies', 'Sauvegardes, surveillance 24 h/24 et maintenance',\n"
         "       'Site bilingue sans supplément', 'Une modification par mois'],"),
        ("       'Legal notice, privacy and cookie policy (Spanish law)', 'Daily backups',\n"
         "       '24/7 monitoring and technical maintenance', 'One content change per month'],",
         "       'Legal notice, privacy and cookie policy (Spanish law)', 'Daily backups, 24/7 monitoring and maintenance',\n"
         "       'Bilingual site at no extra cost', 'One content change per month'],"),
        ('  price_note="Prix hors TVA. Nom de domaine inclus la première année, puis environ 12 €/an.",',
         '  price_note="Prix hors taxes. En France, facturés sans TVA (vous la déclarez en autoliquidation) ; en Espagne, '
         'IVA de 21 % en plus. Nom de domaine inclus la première année, puis environ 12 €/an.",'),
    ],
    '_tools/build_expat_pages.py': [
        ("Nous travaillons avec vous en français, par e-mail, WhatsApp et visioconférence, et nous préparons une démo "
         "gratuite en 24 heures. ",
         "Votre site peut être en français et en espagnol, sans supplément. Nous travaillons avec vous en français, "
         "par e-mail, WhatsApp et visioconférence, et nous préparons une démo gratuite en 24 heures. "),
        ("We work with you in English, by email, WhatsApp and video call, and build a free demo within 24 hours. ",
         "Your site can be in English and Spanish at no extra cost. We work with you in English, by email, WhatsApp "
         "and video call, and build a free demo within 24 hours. "),
        ('    faq=[("Mon site en français doit-il respecter la loi espagnole ?",\n',
         '    faq=[("Mon site peut-il être en français et en espagnol ?",\n'
         '          "Oui, sans supplément. Nous rédigeons les deux versions : vos clients espagnols vous trouvent aussi, '
         'et vos prix et conditions existent en espagnol, comme le demande le droit espagnol de la consommation pour '
         'l\'information précontractuelle."),\n'
         '         ("Mon site en français doit-il respecter la loi espagnole ?",\n'),
        ('    faq=[("Does my English-language website have to comply with Spanish law?",\n',
         '    faq=[("Can my website be in English and Spanish?",\n'
         '          "Yes, at no extra cost. We write both versions, so Spanish-speaking customers find you too, and your '
         'prices and terms are available in Spanish, as Spanish consumer law requires for pre-contract information."),\n'
         '         ("Does my English-language website have to comply with Spanish law?",\n'),
    ],
    '_tools/build_metier_pages.py': [
        ('''    price_note="Prix hors taxes. Les psychologues sont exonérés de TVA et beaucoup de praticiens sont en franchise "
               "en base : la plupart ne récupèrent pas la TVA, comptez donc 20 à 21 % de plus selon votre situation. "
               "Nom de domaine inclus la première année, puis environ 12 €/an.",''',
         '''    price_note="Prix hors taxes. En France, nous facturons sans TVA : vous déclarez vous-même la TVA française de "
               "20 % (autoliquidation), que les psychologues, exonérés, et les praticiens en franchise en base ne "
               "récupèrent pas. En Espagne, l'IVA de 21 % s'ajoute. Nom de domaine inclus la première année, puis "
               "environ 12 €/an.",'''),
        ('''          "<strong>15 € HT par mois</strong> sans frais d'installation ni engagement, ou <strong>349 € HT en "
          "paiement unique</strong>, et la démo est prête en 24 heures.",''',
         '''          "<strong>15 € HT par mois</strong> sans frais d'installation ni engagement, ou <strong>349 € HT en "
          "paiement unique</strong>, bilingue sans supplément si vous le souhaitez, et la démo est prête en 24 heures.",'''),
        ('''          "month</strong> with no setup fee and no lock-in, or a <strong>one-off €349 + VAT</strong>. We work "
          "with you in English, and your demo is ready within 24 hours.",''',
         '''          "month</strong> with no setup fee and no lock-in, or a <strong>one-off €349 + VAT</strong>, in English "
          "and Spanish at no extra cost. We work with you in English, and your demo is ready within 24 hours.",'''),
        ('''          "Catalan. A short Spanish version of your prices and terms is the safe choice."),''',
         '''          "Catalan. A short Spanish version of your prices and terms is the safe choice, and we build your site "
          "in English and Spanish at no extra cost."),'''),
    ],
}


def main():
    os.chdir(ROOT)
    nouveaux, err = {}, []
    for rel, rempl in PATCHES.items():
        s0 = open(rel, encoding='utf-8').read()
        s = s0
        for a, b in rempl:
            if s.count(a) == 1:
                s = s.replace(a, b)
            elif s.count(b) == 1:
                err.append('%s : déjà corrigé (%s…)' % (rel, b.strip()[:50]))
            else:
                err.append('%s : ancre trouvée %dx : %s' % (rel, s.count(a), a.strip()[:70]))
        if rel.endswith('.py'):
            try:
                compile(s, rel, 'exec')
            except SyntaxError as exc:
                err.append('%s : Python invalide après modification (%s)' % (rel, exc))
        if rel.endswith('.html'):
            for t in ('li', 'p', 'ul', 'a'):
                if len(re.findall(r'<%s[\s>]' % t, s)) - s.count('</%s>' % t) != \
                        len(re.findall(r'<%s[\s>]' % t, s0)) - s0.count('</%s>' % t):
                    err.append('%s : balises <%s> déséquilibrées' % (rel, t))
        nouveaux[rel] = s
    if err:
        abandon('vérifications :\n  - ' + '\n  - '.join(err))

    stamp = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
    bak = os.path.expanduser('~/webautonomos-work/backups/tva_bilingue_%s' % stamp)
    for rel in nouveaux:
        d = os.path.join(bak, rel)
        os.makedirs(os.path.dirname(d), exist_ok=True)
        shutil.copy2(rel, d)
    for rel, s in nouveaux.items():
        open(rel, 'w', encoding='utf-8').write(s)
        print('  ✓ %s' % rel)
    print('Sauvegarde : %s\n' % bak.replace(os.path.expanduser('~'), '~'))

    for script in ('_tools/build_expat_pages.py', '_tools/build_metier_pages.py'):
        print('→ %s' % script)
        r = subprocess.run([sys.executable, script], cwd=ROOT)
        if r.returncode:
            sys.exit('ÉCHEC de %s : relance-le à la main après correction.' % script)
    print('\nOK — étape suivante : npx wrangler deploy')


if __name__ == '__main__':
    main()
