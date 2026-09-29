# Créer le GPT « Photos WebAutonomos » (5 minutes)

Dans ChatGPT : **Explorer les GPT → Créer → onglet Configurer**.

| Champ | Valeur |
|---|---|
| Nom | Photos WebAutonomos |
| Description | Génère la photo de la prochaine page du site webautonomos.es et la met en ligne. |
| Instructions | tout le contenu de `instructions.md` (`pbcopy < _tools/photos/gpt/instructions.md`) |
| Amorces de conversation | `suivante` · `ok` · `refaire` · `état` |
| Fonctionnalités | ✅ Génération d'images · ❌ Recherche web · ❌ Canvas · ❌ Interpréteur de code |

**Actions → Créer une action**

1. **Authentification** : *Clé API*, type *Bearer*. Coller la clé du fichier
   `~/webautonomos-work/photos-gpt/cle_api.txt` du Mac (`pbcopy < …`), qui ne
   figure nulle part dans le dépôt.
2. **Schéma** : tout le contenu de `openapi.json` (`pbcopy < _tools/photos/gpt/openapi.json`).
   L'éditeur de ChatGPT lit mal la version YAML (« Impossible de trouver une URL
   valide dans servers ») ; `openapi.yaml` reste la source, `openapi.json` en est
   la conversion (`ruby -ryaml -rjson -e 'puts JSON.pretty_generate(YAML.load_file("openapi.yaml"))'`).
3. **Politique de confidentialité** : inutile tant que le GPT reste privé.
4. Revenir avec la flèche **<** en haut à gauche de l'éditeur d'action, puis
   **Créer** (ou **Mettre à jour**) en haut à droite, partage **Moi seulement**.

Piège rencontré le 29/09 : coller la commande `pbcopy …` elle-même dans un champ
au lieu de son résultat. Exécuter la commande, puis coller.

## Utilisation

1. `suivante` : le GPT prend la page suivante, génère la photo et l'affiche.
   **Rien ne part sur le site à ce stade.**
2. Regarder la photo :
   - `ok` : elle est envoyée, contrôlée par le serveur (aucun texte toléré),
     réduite et publiée ; le GPT enchaîne aussitôt sur la page suivante ;
   - `refaire` : nouvelle photo pour la même page ;
   - `passer` : la page est laissée de côté.
3. `état` : combien de photos faites et restantes.

Au premier appel de chaque action, ChatGPT demande l'autorisation : choisir
**Toujours autoriser**.

Le 29/09, le GPT a généré une infographie sur les pneus au lieu de la scène
demandée : d'où la validation par `ok` et le refus automatique de toute image
contenant du texte.
