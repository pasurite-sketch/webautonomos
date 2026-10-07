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
4. Jusqu'à 2 corrections si « réviser ». Si la page n'est toujours pas approuvée
   (ou si le relecteur « rejette » parce qu'une décision d'Angelino est
   nécessaire), le travail n'est plus jeté : il part en **PR brouillon
   « [À REVOIR] »** avec les remarques du relecteur (non fusionnable en l'état).
   Après décision (VERITE.md mis à jour) : `run_page.sh <slug> --reparer` repart
   de cette version et des remarques, sans refaire la rédaction.
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

## Passage de nuit (depuis le 26/09/2026)

`install_cron.sh` (une fois, utilisateur `seo`) active la fusion automatique des
pages non santé (`AUTO_MERGE=1`) et programme `run_nuit.sh` chaque nuit à 3h17 :

1. `pipeline.py sync` : relit sur GitHub les PR fusionnées ou fermées ;
2. **affinage** (`run_page.sh <slug> --affiner`) : mesure gratuite des pages
   publiées ; celles qui ne sont pas au vert (score Google < 50, ou GEO < 50 pour
   les pages `"objectif_geo": "vert"`) reçoivent une retouche minimale, relue,
   puis PR (au plus `MAX_AFFINAGES`, 3 par défaut) ;
   depuis le 07/10/2026 (voie 1 de l'audit du 06/10), les pages qui ont un
   `"objectif_google"` dans `pages.json` passent en premier, avec ce seuil à la
   place de 50 : 85 pour cinq pages métier espagnoles (psicólogos, reformas,
   fontaneros, electricistas, carpinteros). Une note
   au-dessus de 100 (gris, sur-optimisation) les fait aussi retoucher ;
3. nouvelles pages (`N_NOUVELLES`, 2 par défaut).

Coût : 0 € de plus (mesures SERPmantics gratuites, guides réutilisés, Claude sur
l'abonnement). Journal : `~/nuit.log` sur le VPS.

## Relevé complet (depuis le 04/10/2026)

`releve.py` mesure en une fois toutes les pages qui ont des guides, sur chaque moteur
(Google, AI Overview, ChatGPT, Gemini…), et enregistre la mesure dans les guides :
la liste de SERPmantics affiche ensuite les mêmes notes. Mesurer est gratuit.
Résultat : `releve.json` et `releve.csv` (une ligne par page et par moteur, avec la
note précédente, les images et les mots de la page face au top 10).
Sur le VPS, il tourne aussi depuis le compte `ubuntu` (copie de la clé dans son
`~/.seo_pipeline.env`, faite par Angelino le 04/10), sur un export de `origin/main`.

Pages hors circuit : `requetes_site.json` donne la requête que vise chaque page du
sitemap absente de `pages.json` (articles du blog, outils, FAQ…), par phase.
`releve.py creer --phase N` crée les guides manquants (Google par défaut) puis le relevé
les mesure. Limites constatées le 04/10/2026 :
- quota API : 200 guides créés par mois (période du 24 au 24), même avec les crédits
  illimités ; lecture et mesures gratuites ; `creer` garde 6 guides pour le circuit ;
  les guides créés à la main dans l'interface comptent aussi (essai du 04/10 : 3 guides,
  compteur passé de 193 à 196) ;
- au plus 20 guides en cours de création (« Too many guides in progress ») : `creer`
  envoie 5 requêtes toutes les 20 s et réessaie ;
- langues : ni le catalan (les 58 articles valenciens sont exclus) ni `en-es` : les
  guides anglais sont en `en-gb`.
Phase 1 (04/10) : 60 guides Google, pages espagnoles. Phase 2 (à partir du 24/10) :
pages anglaises et françaises ; les requêtes « null » sont à choisir avant.
Sources GEO : `sources_geo` dans pages.json ; `serp.py sources` liste celles que
SERPmantics propose (AI Overview de Google, ChatGPT, Gemini…).
