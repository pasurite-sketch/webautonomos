# -*- coding: utf-8 -*-
"""Voie 1 de l'audit du 06/10 : liens entrants vers les pages métier (07/10/2026).

Méthode appliquée à /psicologos/, /reformas/ et /fontaneros/ : chaque page reçoit au moins
5 liens dans le texte, depuis l'accueil (boutons « Para quién »), son guide du blog (bloc
<!-- lien-page-metier -->, patch_guides_metier_20261007.py) et trois articles du blog où le
lien a un sens. Avant ce script, seul le guide du métier liait la page dans son texte ; les
autres liens venaient du pied de page commun.

Ancres : la requête de la page (« páginas web para psicólogos », « páginas web para empresas
de reformas », « diseño web para fontaneros »). Chaque phrase ne dit que ce que la page métier
dit déjà (formulaire sans motif de consulta, textes rédigés par WebAutonomos, zone de
cobertura visible) ; voir _tools/seo_pipeline/VERITE.md.

Idempotent (marqueur <!-- lien-voie1 --> ou phrase déjà présente) ; --dry-run pour afficher
sans écrire.
"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = 'https://webautonomos.es'
MARQUEUR = '<!-- lien-voie1 -->'
P = '<p class="text-gray-700 leading-relaxed mb-4">'


def lien(page, ancre):
    return '<a href="%s/%s/" style="color:#2563eb;">%s</a>' % (BASE, page, ancre)


PSICO = lien('psicologos', 'páginas web para psicólogos')
REFORMAS = lien('reformas', 'páginas web para empresas de reformas')
FONTANEROS = lien('fontaneros', 'diseño web para fontaneros')
# Variante d'ancre pour l'article « qué debe tener » : avec « diseño web », sa note passait de 88 à 97.
FONTANEROS_PAGINAS = lien('fontaneros', 'páginas web para fontaneros')

# (fichier, texte repère présent une seule fois, balise qui le ferme, ajout)
# Un ajout qui commence par <p> devient un nouveau paragraphe après l'élément repère ;
# sinon, il est placé à la fin de cet élément, juste avant sa balise fermante.
AJOUTS = [
    ('blog/es/que-debe-tener-web-profesional-autonomo.html',
     'un taller de Elche explicaría qué reparaciones hace y cómo pedir cita.', '</p>',
     P + 'Cada oficio añade lo suyo: el colegio y el número de colegiado en las %s, las fotos de '
     'obras terminadas en las %s o la zona de cobertura en las %s.</p>' % (PSICO, REFORMAS, FONTANEROS_PAGINAS)),
    ('blog/es/backlinks-locales-como-conseguir.html',
     'Y si quieres repasar qué debe tener la página de tu oficio, tienes guías para', '</p>',
     P + 'Si prefieres que te la hagamos, mira nuestras %s, las %s o el %s: ves una demo gratis '
     'antes de pagar.</p>' % (PSICO, REFORMAS, FONTANEROS)),
    ('blog/es/reservas-online-autonomos-2026.html',
     'Evita los datos de salud en la reserva: la normativa de protección de datos (RGPD) los trata '
     'como especialmente sensibles.', '</li>',
     ' Por eso, en nuestras %s, el formulario no pregunta el motivo de consulta.' % PSICO),
    ('blog/es/crear-contenido-web-sin-saber-escribir.html',
     'Imagina una empresa de reformas de Elda que presenta la reforma de baños.', '</p>',
     P + 'Si prefieres no escribirlo tú, en nuestras %s redactamos el contenido a partir de tus '
     'datos y de tus fotos.</p>' % REFORMAS),
    ('blog/es/como-posicionar-web-en-google-local.html',
     'Un fontanero de Alicante, por ejemplo, puede crear una para la reparación de averías', '</p>',
     P + 'Si prefieres que te preparemos la web, así es nuestro %s: tus servicios explicados uno a '
     'uno y tu zona bien visible.</p>' % FONTANEROS),
]


def main():
    ecrire = '--dry-run' not in sys.argv
    for rel, repere, fin, ajout in AJOUTS:
        chemin = os.path.join(ROOT, rel)
        s = open(chemin, encoding='utf-8').read()
        texte = ajout[len(P):] if ajout.startswith(P) else ajout
        if texte in s:
            print('déjà fait :', rel)
            continue
        if s.count(repere) != 1:
            sys.exit('repère introuvable ou ambigu (%d) : %s' % (s.count(repere), rel))
        i = s.index(repere)
        j = s.index(fin, i)
        if ajout.startswith(P):
            k = j + len(fin)
            s = s[:k] + '\n            %s\n            %s' % (MARQUEUR, ajout) + s[k:]
        else:
            s = s[:j] + ajout + s[j:]
        print('lien ajouté :', rel)
        if ecrire:
            open(chemin, 'w', encoding='utf-8').write(s)


if __name__ == '__main__':
    main()
