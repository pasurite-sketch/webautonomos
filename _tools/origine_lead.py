"""Balise du script d'origine des leads (/origine-lead.js), posée juste avant le </head> de chaque page (10/10/2026).

Appelée par les générateurs juste avant d'écrire leurs pages, comme poser_photo, et par
_tools/patch_origine_leads_20261010.py pour les pages déjà en place. Ne pas retirer ces appels : sans eux, une
régénération efface le suivi de l'origine des leads de la page. Idempotent (repère <!-- origine-lead -->).
"""
import re

REPERE = "<!-- origine-lead -->"
BALISE = REPERE + '\n<script src="/origine-lead.js" defer></script>\n'


def poser(h):
    """Page `h` avec la balise du script, insérée devant le </head> qui précède <body> (certaines pages citent
    </head> dans un commentaire plus haut). Page inchangée si la balise y est déjà ou s'il n'y a pas de </head>."""
    if REPERE in h:
        return h
    m = re.search(r'</head>\s*<body', h)
    i = m.start() if m else h.rfind('</head>')
    if i < 0:
        return h
    return h[:i] + BALISE + h[i:]
