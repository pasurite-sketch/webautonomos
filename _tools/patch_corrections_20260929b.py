# -*- coding: utf-8 -*-
"""Corrections du 29/09/2026 (2e passe), demandées par Angelino : « Fais toutes les corrections nécessaires ».

1. « Serveurs européens » retiré partout où le site l'affirmait (FAQ et listes « inclus »,
   y compris la FAQ de l'accueil dans le SPA, 4 langues). Rien dans VERITE.md ne l'établit,
   et les sites clients vérifiés le 29/09 (yosoynensi.es, anasaizpsicologia.com,
   sabineoliveira.fr, goexsoldaduras.com, casalotusazul.com, marcu-electric) répondent tous
   via Cloudflare, réseau mondial : la localisation « européenne » n'est pas démontrable.
   L'expression rejoint les interdits de VERITE.md §8.
2. Phrase sur l'IVA de /precios et /pide-tu-demo : « la mayoría de autónomos pueden
   deducirlo » (VERITE §8) -> seul le cas sûr, les activités exonérées ne déduisent pas.
   /precios était gelée jusqu'au 22/10 : Angelino a demandé la correction le 29/09 ;
   title, H1 et H2 inchangés, seule la note de prix change.
3. /reformas/ : « La mayoría de búsquedas del sector incluyen una ciudad » (sans source).
4. /en/contact : clients au Royaume-Uni acceptés depuis le 26/09 (VERITE §1) ; la page
   ne parlait que de l'Espagne.

index.html est le bundle Lovable : cette retouche scriptée s'ajoute à celles listées dans
CLAUDE.md et serait perdue à un ré-export.

Idempotent. Usage : python3 _tools/patch_corrections_20260929b.py [--check]
"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
CHECK = '--check' in sys.argv

IVA_A = ("Precios sin IVA. La mayoría de autónomos y empresas pueden deducirlo; las actividades exentas de IVA, "
         "como las sanitarias, no.")
IVA_B = "Precios sin IVA. Si tu actividad está exenta de IVA, como las sanitarias, no podrás deducirlo."

# (fichier, ancien, nouveau, nombre attendu)
R = [
    ('fr/tarifs.html', '<li>Hébergement haute vitesse, serveurs européens</li>', '<li>Hébergement haute vitesse</li>', 1),
    ('fr/questions.html', "l'hébergement sur serveurs européens, ", "l'hébergement, ", 2),
    ('en/pricing.html', '<li>Fast hosting on European servers</li>', '<li>Fast hosting</li>', 1),
    ('en/faq.html', 'high-speed hosting on European servers, ', 'high-speed hosting, ', 2),
    ('preguntas.html', 'hosting de alta velocidad en servidores europeos, ', 'hosting de alta velocidad, ', 2),
    ('index.html', 'hosting de alta velocidad en servidores europeos, ', 'hosting de alta velocidad, ', 3),
    ('index.html', "hosting d'alta velocitat en servidors europeus, ", "hosting d'alta velocitat, ", 1),
    ('index.html', 'high-speed hosting on European servers, ', 'high-speed hosting, ', 1),
    ('index.html', 'hébergement rapide sur des serveurs européens, ', 'hébergement rapide, ', 1),
    ('precios.html', IVA_A, IVA_B, 1),
    ('pide-tu-demo.html', IVA_A, IVA_B, 1),
    ('reformas/index.html', 'La mayoría de búsquedas del sector incluyen una ciudad o un barrio',
     'Muchas búsquedas del sector incluyen una ciudad o un barrio', 1),
    ('en/contact.html',
     'We work with freelancers and small businesses across the Valencian Community — Valencia, Alicante, Elda, '
     'Elche — and the rest of Spain. Tell us what you do and we will build a free demo of your website.',
     'We work remotely, by email, WhatsApp and video call, with freelancers and small businesses across Spain — '
     'from Valencia, Alicante, Elda and Elche to the rest of the country — and with businesses in the UK. Tell us '
     'what you do and we will build a free demo of your website within 24 hours.', 1),
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
        reste = [m for m in ('serveurs europ', 'European servers', 'servidores europ', 'servidors europ') if m in s]
        if reste:
            sys.exit('ABANDON : %s contient encore %s. Rien écrit.' % (rel, reste))
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
