#!/usr/bin/env bash
# Publie le prochain article dû du blog, régénère les fichiers, committe et pousse.
# Lancé par .github/workflows/publish-blog.yml (lundi et jeudi).
#
# Pourquoi des reprises (03/10/2026) : le run du jeudi 01/10 a échoué à l'étape
# du commit. Il avait démarré à 12:11 UTC sur 8ebdf91 ; photos-bot a poussé
# 4514b2a à 12:12, donc le push du blog a été refusé (main avait bougé) et
# l'article wix-o-wordpress n'est jamais sorti. photos-bot pousse toutes les
# 2 à 5 minutes, et GitHub lance les runs « 06:00 UTC » avec plusieurs heures
# de retard : la collision se reproduira.
#
# Un « git pull --rebase » ne suffit pas : photos-bot et la publication modifient
# la même ligne de index.html (les données du blog), donc le rebase échouerait
# en conflit. À chaque refus, on repart de origin/main et on refait toute la
# publication sur l'état à jour, puis on repousse (6 tentatives au plus).
#
# ATTENTION : fait des « git reset --hard » et « git clean ». Réservé au
# GitHub Action : refuse de tourner ailleurs (sauf ALLOW_LOCAL=1, pour un test
# dans une copie jetable).
set -uo pipefail

if [ -z "${GITHUB_ACTIONS:-}" ] && [ "${ALLOW_LOCAL:-}" != "1" ]; then
  echo "Réservé au GitHub Action (ce script fait git reset --hard). Rien n'a été fait."
  exit 1
fi

OUT_FINAL="${GITHUB_OUTPUT:-/dev/null}"
TENTATIVES="${TENTATIVES:-6}"
git config user.name "webautonomos-bot"
git config user.email "bot@users.noreply.github.com"

for i in $(seq 1 "$TENTATIVES"); do
  echo "── Tentative $i/$TENTATIVES"
  if ! git fetch --quiet origin main; then
    echo "git fetch a échoué, nouvel essai dans 15 s."
    sleep 15
    continue
  fi
  git reset --quiet --hard origin/main
  git clean -fdq

  TMP="$(mktemp)"
  if ! GITHUB_OUTPUT="$TMP" python3 _tools/publish_next.py; then
    echo "ÉCHEC de publish_next.py : rien n'a été poussé."
    exit 1
  fi
  if ! grep -q '^published=true' "$TMP"; then
    cat "$TMP" >> "$OUT_FINAL"      # aucun article dû : published=false
    exit 0
  fi
  SLUG="$(sed -n 's/^slug=//p' "$TMP" | tail -1)"

  # Fichiers statiques des articles (sinon l'URL répond 404), index /blog/ et sitemap.
  for script in generate_spa_articles generate_blog_index generate_sitemap; do
    if ! python3 "_tools/$script.py"; then
      echo "ÉCHEC de $script.py : rien n'a été poussé."
      exit 1
    fi
  done

  git add index.html sitemap.xml blog _tools/queue
  git commit --quiet -m "Blog auto : publication $SLUG"
  if git push origin HEAD:main; then
    cat "$TMP" >> "$OUT_FINAL"
    echo "✅ Publié et poussé à la tentative $i : $SLUG"
    exit 0
  fi
  ATTENTE=$(( (RANDOM % 20) + 10 * i ))
  echo "Push refusé : main a bougé pendant la publication. On recommence sur l'état à jour dans $ATTENTE s."
  sleep "$ATTENTE"
done

echo "ÉCHEC : push refusé $TENTATIVES fois de suite. Relancer le workflow à la main (Actions > Run workflow)."
exit 1
