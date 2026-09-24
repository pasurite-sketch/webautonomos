# Circuit SEO/GEO automatisé — webautonomos.es

Optimise les pages commerciales une par une avec SERPmantics et Claude Code,
sans publier d'affirmation fausse.

## Le circuit, pour chaque page

1. **Guides** (`serp.py`, sans IA) : 2 guides SERPmantics (Google pour le SEO,
   pages citées par les réponses IA de Google pour le GEO), réutilisés s'ils
   existent, résumés en quelques lignes pour l'agent.
   **Rédacteur** (Claude, `WRITER_MODEL`) : lit les résumés → réécriture (page ou
   script générateur) → mesure avec `serp.py score` → rapport.
2. **Contrôles automatiques** (`checks.py`, sans IA) : périmètre, scripts
   générateurs, HTML, JSON-LD, FAQ, title, H1, prix, liens de démo, Trustpilot,
   nombres et expressions interdits, accents.
3. **Relecteur** (Claude, `REVIEWER_MODEL`, indépendant, lecture seule) :
   faits contre `VERITE.md`, qualité, cannibalisation, santé → approuver /
   réviser / rejeter.
4. Jusqu'à 2 corrections si « réviser ». « Rejeter » = abandon, rien n'est publié.
5. **Pull request** GitHub avec un résumé de 5 lignes. Fusion automatique
   seulement si `AUTO_MERGE=1` et page en mode `auto`. Pages santé : toujours
   ton clic.

## Fichiers

| Fichier | Rôle | Qui le modifie |
|---|---|---|
| `VERITE.md` | Seuls faits autorisés, chiffres, interdits | **Angelino** |
| `pages.json` | Les 30 pages : requête, fichier, mode, statut | Angelino / Claude |
| `REGLES_REDACTEUR.md` | Consignes de l'agent rédacteur | Claude |
| `REGLES_RELECTEUR.md` | Grille de l'agent relecteur | Claude |
| `checks.py` | Contrôles automatiques | Claude |
| `pipeline.py` | Consignes, état, résumé de PR | Claude |
| `run_page.sh` | Traite une page | — |
| `run_batch.sh` | Traite les N suivantes (cron) | — |
| `mcp.json` | Connexion SERPmantics | — |
| `runs/` | Journaux, rapports, état (non versionné) | automatique |

Installation : `INSTALL_VPS.md`.

## Avant le premier passage

- Trancher les points **À CONFIRMER** de `VERITE.md` (section 10).
- Pages marquées `requete_a_confirmer: true` : sautées tant qu'aucun volume
  ne confirme la requête (au 24/09 : 6 pages FR et 5 pages EN).
- Liste du 24/09/2026 : vague 1 = 11 pages (priorité 1 : 7 ES, 1 EN et les
  3 pages FR dont les requêtes viennent du relevé de volumes), puis
  `en-home`, `en-services` et `en-therapists` (priorité 2) ; `/servicios` retirée du circuit.
