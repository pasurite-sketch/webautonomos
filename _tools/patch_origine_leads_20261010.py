#!/usr/bin/env python3
"""Origine des leads (10/10/2026) : inclut /origine-lead.js dans le <head> de toutes les pages, index.html et blog
compris, et branche les 3 formulaires « Visibilidad IA » qui construisent leurs données à la main.

Pourquoi : le scénario Make « Leads WebAutonomos » attend referrer, landing_page et form_page (colonnes de la feuille,
section « Origen del lead » de l'e-mail), mais aucun formulaire ne les envoyait ; gclid et utm_* n'étaient captés que
sur les 3 pages de démo. Le script origine-lead.js note l'arrivée du visiteur et ajoute ces champs à chaque envoi.

Idempotent (repère <!-- origine-lead --> et « origineLead » dans les pages Visibilidad IA). La balise est posée par
_tools/origine_lead.py, que les générateurs appellent aussi avant d'écrire leurs pages : les nouvelles pages l'ont
d'office. À relancer après un ré-export Lovable d'index.html, pour une page écrite à la main, et au dégel de l'article
ES « cuanto-cuesta » (contrôle du 22/10) : retirer alors son nom de GELES.
Blog ajouté le 10/10 au soir, à la demande d'Angelino : un visiteur venu de Google sur un article garde son origine.
Usage : python3 _tools/patch_origine_leads_20261010.py [--dry-run]
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from origine_lead import REPERE, poser  # noqa: E402

RACINE = Path(__file__).resolve().parents[1]
GELES = {"blog/es/cuanto-cuesta-pagina-web-autonomos-espana.html"}  # gelé jusqu'au contrôle du 22/10
VISIBILITE = ["visibilidad-ia/index.html", "en/ai-visibility/index.html", "fr/visibilite-ia/index.html"]
W3F_AVANT = "      body: JSON.stringify(data)\n"
W3F_APRES = ("      // origine du lead (origine-lead.js, _tools/patch_origine_leads_20261010.py)\n"
             "      body: JSON.stringify(Object.assign({}, window.origineLead ? window.origineLead() : {}, data))\n")


def pages():
    for f in sorted(RACINE.rglob("*.html")):
        rel = f.relative_to(RACINE)
        if rel.parts[0] in {"_tools", "scripts", "node_modules", ".git", ".wrangler"} or str(rel) in GELES:
            continue
        yield f, str(rel)


def main(dry):
    modifiees = []
    for f, rel in pages():
        s = f.read_text(encoding="utf-8")
        t = poser(s)
        if REPERE not in t:
            print(f"⚠️ {rel} : pas de </head>, page ignorée")
            continue
        if rel in VISIBILITE and "origineLead" not in t.split("function pushWeb3Forms", 1)[-1][:600]:
            if t.count(W3F_AVANT) != 1:
                print(f"⚠️ {rel} : envoi Web3Forms introuvable ou ambigu, formulaire non branché")
            else:
                t = t.replace(W3F_AVANT, W3F_APRES)
        if t != s:
            modifiees.append(rel)
            if not dry:
                f.write_text(t, encoding="utf-8")
    print(f"{'(simulation) ' if dry else ''}{len(modifiees)} page(s) modifiée(s)")
    for rel in modifiees:
        print("  " + rel)


if __name__ == "__main__":
    main("--dry-run" in sys.argv)
