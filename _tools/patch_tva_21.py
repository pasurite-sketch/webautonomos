# -*- coding: utf-8 -*-
"""TVA des clients français, précision d'Angelino du 24/09/2026 :
IVA espagnole de 21 %, SAUF si le client est une entreprise établie dans un
AUTRE pays de l'UE (la France, par exemple) avec un numéro de TVA
intracommunautaire : facture sans TVA, autoliquidation par le client. Un client
établi en Espagne paie l'IVA même s'il a un numéro intracommunautaire.

Corrige la mention posée le matin même par patch_tva_bilingue.py (« en France,
nous facturons sans TVA ») :
  - /fr/tarifs, /fr/prestations, /fr/questions : note sous les prix ;
  - /fr/ : note de prix (générateur build_lang_homes.py) ;
  - comparatif français : « ajoutez 20 % » -> « 20 à 21 % » (3 endroits) ;
  - pages expatriés (build_expat_pages.py) : « Sources : » -> « Sources: » en anglais.
La page thérapeutes est corrigée dans build_metier_pages.py (nouvelle version),
qui ajoute aussi les pages menuisiers.

Puis relance build_expat_pages.py et build_metier_pages.py (qui relance
build_lang_homes.py et generate_sitemap.py).

Sauvegarde : ~/webautonomos-work/backups/tva_21_<date>/
Abandon total, rien d'écrit, si une vérification échoue.

À lancer depuis ~/webautonomos, APRÈS avoir remplacé _tools/build_metier_pages.py :
    python3 _tools/patch_tva_21.py
"""
import datetime
import os
import shutil
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def abandon(msg):
    sys.exit('ABANDON : %s\nRien n\'a été modifié.' % msg)


NOTE_AVANT = ("Prix hors taxes. En France, nous facturons sans TVA : vous la déclarez vous-même (autoliquidation) "
              "et la récupérez, sauf en franchise en base ou pour une activité exonérée, comme la santé. En Espagne, "
              "l'IVA de 21 % s'ajoute.")
NOTE_APRES = ("Prix hors taxes. L'IVA espagnole de 21 % s'ajoute. Si votre entreprise est établie dans un autre pays "
              "de l'UE, en France par exemple, avec un numéro de TVA intracommunautaire, la facture est émise sans TVA "
              "et vous déclarez la TVA vous-même (autoliquidation).")

PATCHES = {
    'fr/tarifs.html': [(NOTE_AVANT, NOTE_APRES, 1)],
    'fr/prestations.html': [(NOTE_AVANT, NOTE_APRES, 1)],
    'fr/questions.html': [(NOTE_AVANT, NOTE_APRES, 1)],
    '_tools/build_lang_homes.py': [
        ('  price_note="Prix hors taxes. En France, facturés sans TVA (vous la déclarez en autoliquidation) ; en Espagne, '
         'IVA de 21 % en plus. Nom de domaine inclus la première année, puis environ 12 €/an.",',
         '  price_note="Prix hors taxes : IVA espagnole de 21 % en plus. Entreprise établie ailleurs dans l\'UE avec un '
         'numéro de TVA intracommunautaire : facture sans TVA (autoliquidation). Nom de domaine inclus la première '
         'année, puis environ 12 €/an.",', 1)],
    '_tools/build_expat_pages.py': [
        ("    <p class=\"srcs\">{E(c['sources_t'])} : {srcs}</p>",
         "    <p class=\"srcs\">{E(c['sources_t'])}{' :' if lang == 'fr' else ':'} {srcs}</p>", 1)],
    'fr/meilleurs-createurs-de-sites-pour-independants.html': [
        ('ajoutez 20 % à tous les montants', 'ajoutez 20 à 21 % à tous les montants', 1),
        ('ajoutez donc 20 % aux prix hors taxes', 'ajoutez donc 20 à 21 % aux prix hors taxes', 2)],
}


def main():
    os.chdir(ROOT)
    metier = open('_tools/build_metier_pages.py', encoding='utf-8').read()
    if "'menuisiers'" not in metier:
        abandon("_tools/build_metier_pages.py n'est pas la nouvelle version (pas de menuisiers) : remplace-le d'abord.")
    nouveaux, err = {}, []
    for rel, rempl in PATCHES.items():
        s = open(rel, encoding='utf-8').read()
        for a, b, n in rempl:
            if s.count(a) == n:
                s = s.replace(a, b)
            elif s.count(b) == n:
                err.append('%s : déjà corrigé' % rel)
            else:
                err.append('%s : ancre trouvée %dx au lieu de %d : %s' % (rel, s.count(a), n, a[:60]))
        if rel.endswith('.py'):
            try:
                compile(s, rel, 'exec')
            except SyntaxError as exc:
                err.append('%s : Python invalide (%s)' % (rel, exc))
        nouveaux[rel] = s
    if err:
        abandon('vérifications :\n  - ' + '\n  - '.join(err))

    stamp = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
    bak = os.path.expanduser('~/webautonomos-work/backups/tva_21_%s' % stamp)
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


if __name__ == '__main__':
    main()
