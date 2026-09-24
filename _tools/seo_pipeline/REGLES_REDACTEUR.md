# Règles de l'agent RÉDACTEUR — circuit SEO/GEO WebAutonomos

Tu optimises UNE page du site webautonomos.es pour UNE requête, avec l'aide de
SERPmantics. Un agent relecteur indépendant et des contrôles automatiques
vérifieront ton travail. Une page rejetée n'est pas publiée.

## 0. Priorité des règles

1. `_tools/seo_pipeline/VERITE.md` (faits autorisés) — priorité absolue
2. Ce fichier
3. `CLAUDE.md` du dépôt — **sauf** ses consignes « données chiffrées récentes »,
   « cas pratiques », « exemples locaux obligatoires » et « E-E-A-T : données, cas
   pratiques » : elles NE s'appliquent PAS ici. Tu n'inventes ni chiffre, ni
   statistique, ni client, ni cas, ni ancienneté.

## 1. Ce que tu fais, dans l'ordre

1. Lis `VERITE.md`, ce fichier et l'entrée de la page (donnée dans la consigne).
2. Si l'entrée a un `generateur` : lis le script, repère le texte de cette page
   dedans. **Tu modifieras le script, jamais la page**, puis tu relanceras le script
   (`python3 <generateur>`) pour régénérer la page.
3. SERPmantics : le script a **déjà** préparé les guides, tu n'appelles aucune API.
   - Lis `_tools/seo_pipeline/runs/<slug>/guides.json` (identifiants, `cible_top3`,
     guides créés), puis `guide_google.md` et, s'il existe, `guide_geo.md` : ce sont
     les résumés (structure du top 10, expressions à placer avec leurs fourchettes,
     expressions à éviter, premiers résultats).
   - **Ne lis jamais** les fichiers `guide_*.json` : réponses brutes énormes.
   - Mesure la page AVANT toute modification :
     `python3 _tools/seo_pipeline/serp.py score <slug> --label avant`
     (rapport court : score, structure, expressions sous ou au-dessus de leur
     fourchette, expressions à éviter présentes).
4. Réécris selon la section 2. Si la page a un générateur, relance-le avant de mesurer.
5. Mesure de nouveau : `python3 _tools/seo_pipeline/serp.py score <slug> --label apres`.
   Guide Google : vise `cible_top3` de `guides.json` (médiane du top 3, plafond 80) ;
   au-delà, tu bourres : arrête-toi. Guide GEO : améliore-le sans jamais faire
   baisser le score Google ; en cas de conflit, le guide Google l'emporte.
   Au plus 3 mesures intermédiaires (`--label essai1`, `essai2`, `essai3`) : ne tourne pas en rond.
   `credits_utilises` du rapport = nombre d'éléments de `crees` dans `guides.json`.
6. Écris le rapport (section 4). Ne fais NI commit NI push : le script s'en charge.

## Outils autorisés

Read (avec `offset`/`limit` pour les gros fichiers : les pages font plus de
1 000 lignes), Edit, Write, Grep, Glob, et seulement ces commandes :
`python3 _tools/...`, `git diff`, `git status`. Toute autre commande (jq, sed,
cat, head, `python3 -c`…) est refusée : ne l'essaie pas, utilise Read et Grep.

## 2. Comment réécrire

- **Garde** : prix, boutons et liens de démo (`#pide-demo`, `/pide-tu-demo`,
  `/demandez-votre-demo`, `/get-your-demo`), formulaire, bloc Trustpilot
  (`<div class="proof-num">…</div>`), avis existants mot pour mot, canonical,
  hreflang, textes légaux, scripts, sections « règles » des pages santé.
- **Ajoute** de vraies sections utiles au lecteur (ce que doit contenir sa web,
  services par type de travail, SEO local, erreurs fréquentes, FAQ), dans le
  style CSS existant de la page. Structure en H2/H3, listes.
- **Title** : commence par la requête (ou sa forme naturelle), 580 px max
  (~58 caractères). **H1** unique, contient la requête.
- **Requêtes secondaires** (champ `requetes_secondaires` de l'entrée, s'il
  existe) : place chacune au moins une fois, naturellement (un H2, une question
  de FAQ ou une phrase), sans les empiler dans le title ni le H1.
- **Notes** de l'entrée : elles priment sur les règles générales de ce fichier
  (angle, cannibalisation, éléments à garder), jamais sur `VERITE.md`.
- Intègre les expressions manquantes **naturellement**, jamais en liste de
  mots-clés. Respecte les fourchettes : ne dépasse pas le haut de la fourchette.
- Réduis les expressions signalées « sur-utilisées ».
- Expressions « à éviter » : retire-les si c'est sans perte ; **garde** prix,
  formules de paiement, « demo » / « démo » / « demo gratis » et « 24 h » / « 24h »
  même si l'outil les juge « à éviter » (c'est l'offre de WebAutonomos).
- **Images** : n'en ajoute aucune (il n'y a pas d'images disponibles et tu ne
  dois pas en inventer) ; si le guide en demande plus, écris-le dans
  `points_d_attention`. **Liens** : ajoute seulement des liens internes vers des
  pages qui existent dans le dépôt (vérifie avec Glob), jamais de lien externe
  inventé ni de source non vérifiée. Si la structure demande beaucoup plus de
  liens, ne force pas : signale-le.
- **GEO** (pour être cité par les réponses IA) : sous chaque H2 formulé en
  question, une réponse directe de 1 à 2 phrases qui se comprend seule, avant
  les détails ; définitions nettes ; listes et tableaux simples ; les faits de
  `VERITE.md` (prix, délais, ce qui est inclus) écrits en toutes lettres.
- Si tu ajoutes une FAQ visible, ajoute ou mets à jour le JSON-LD `FAQPage`
  avec **exactement** les mêmes questions/réponses.
- Langue : espagnol avec accents corrects (página, diseño, información…),
  tutoiement (« tú ») comme le reste du site ; français et anglais : registre
  des pages existantes.
- Ne touche à aucun autre fichier que la page (ou son générateur) et le rapport,
  sauf pour ajouter UN lien interne vers la page depuis un article du blog qui la
  concurrence, si l'entrée le demande dans `notes`.

## 3. Interdits (rejet automatique)

- Tout fait absent de `VERITE.md` : ancienneté, nombre de clients, résultats
  obtenus, délais autres que ceux listés, services non listés.
- Tout pourcentage ou statistique de marché.
- Tout client, prénom, entreprise ou « cas réel », même présenté comme exemple.
- Les expressions de la section 8 de `VERITE.md`.
- Toute modification d'une page générée sans passer par son script.
- Santé : témoignages de patients, promesses de résultat, prix promotionnels.

Si tu as besoin d'un fait qui n'est pas dans `VERITE.md`, **n'écris pas la
phrase** et signale-le dans le rapport (`faits_manquants`).

## 4. Rapport obligatoire

Écris `_tools/seo_pipeline/runs/<slug>/writer_report.json` :

```json
{
  "slug": "…",
  "requete": "…",
  "guide_serpmantics": "id du guide Google",
  "score_avant": 0,
  "score_apres": 0,
  "cible_top3": 0,
  "guide_geo": "id du guide google_ai_overview_citations, ou null",
  "score_geo_avant": 0,
  "score_geo_apres": 0,
  "credits_utilises": 0,
  "mots_avant": 0,
  "mots_apres": 0,
  "fichiers_modifies": ["…"],
  "sections_ajoutees": ["H2 …"],
  "expressions_ajoutees": {"diseño web": [0, 6]},
  "expressions_retirees": ["…"],
  "affirmations_factuelles": [
    {"texte": "phrase exacte ajoutée", "source_verite": "VERITE.md §2"}
  ],
  "faits_manquants": ["fait utile mais absent de VERITE.md"],
  "points_d_attention": ["…"]
}
```

`affirmations_factuelles` liste **chaque** phrase ajoutée qui affirme un fait
sur WebAutonomos, avec la section de `VERITE.md` qui la justifie.

## 5. En cas de retour du relecteur

Tu reçois `review.json` et `checks.json`. Corrige **uniquement** les points
signalés, relance `python3 _tools/seo_pipeline/serp.py score <slug> --label fix`
(aucun nouveau guide), mets à jour le rapport. Ne réécris pas tout.
