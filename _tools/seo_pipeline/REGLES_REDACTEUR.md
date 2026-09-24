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
3. SERPmantics (outils `mcp__serpmantics__*`) :
   - `create_guides` pour la requête, moteur Google, dans la langue indiquée ;
   - `get_guides` pour obtenir les expressions attendues (avec leurs fourchettes),
     les expressions à éviter, les statistiques du top 10 (mots, titres, listes) ;
   - `create_score` sur le contenu ACTUEL de la page → note le score de départ.
4. Réécris selon la section 2.
5. `create_score` sur le nouveau contenu. Vise **le niveau médian du top 3**,
   plafonné à 80. Au-delà, tu bourres : arrête-toi.
6. Écris le rapport (section 4). Ne fais NI commit NI push : le script s'en charge.

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
- Expressions « à éviter » : retire-les si c'est sans perte ; **garde** prix et
  formules de paiement même si l'outil les juge « à éviter » (c'est l'argument
  commercial de WebAutonomos).
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
  "guide_serpmantics": "id ou url du guide",
  "score_avant": 0,
  "score_apres": 0,
  "cible_top3": 0,
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
signalés, relance `create_score`, mets à jour le rapport. Ne réécris pas tout.
