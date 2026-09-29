# Créer le GPT « Photos WebAutonomos » (5 minutes)

Dans ChatGPT : **Explorer les GPT → Créer → onglet Configurer**.

| Champ | Valeur |
|---|---|
| Nom | Photos WebAutonomos |
| Description | Génère la photo de la prochaine page du site webautonomos.es et la met en ligne. |
| Instructions | copier tout le contenu de `instructions.md` |
| Amorces de conversation | `suivante` · `3 suivantes` · `refaire` · `état` |
| Fonctionnalités | ✅ Génération d'images · ❌ Recherche web · ❌ Canvas · ❌ Interpréteur de code |

**Actions → Créer une action**

1. **Authentification** : *Clé API*, type *Bearer*. Coller la clé du fichier
   `~/webautonomos-work/photos-gpt/cle_api.txt` du Mac (elle ne figure nulle part
   dans le dépôt).
2. **Schéma** : copier tout le contenu de `openapi.yaml`.
3. **Politique de confidentialité** : inutile tant que le GPT reste privé.

**Partager** : *Moi uniquement*. Puis **Créer**.

## Première utilisation

1. Taper `suivante`.
2. Au premier appel de chaque action, ChatGPT demande l'autorisation : choisir
   **Toujours autoriser** (une fois pour `obtenirSuivante`, une fois pour
   `envoyerPhoto`).
3. Le GPT génère la photo, rédige les textes et l'envoie ; il répond par le titre
   de la page et « en ligne dans 2 minutes environ ».

## Commandes

- `suivante` : une photo.
- `3 suivantes` (5 au plus) : plusieurs à la suite.
- `refaire` : nouvelle variante pour la dernière page, qui remplace la précédente.
- `passer` : laisse la page de côté.
- `état` : combien de photos faites et restantes.
