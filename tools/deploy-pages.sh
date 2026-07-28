#!/usr/bin/env bash
#
# Nasazení `dist/` na větev gh-pages.
#
# Dělá se to v odděleném pracovním stromu, ne přepnutím větve v projektu.
# Důvod je praktický: gh-pages nemá .gitignore (a mít ho nemusí, leží na ní
# jen hotový web), takže `git add -A` po přepnutí větve nabere i node_modules,
# tools a src, které v pracovním stromu zůstaly ležet. Stalo se to dvakrát.
# Oddělený strom o zdrojích neví a nabrat je nemůže.
#
# Použití:  bash tools/deploy-pages.sh "Nasazení 1250 otázek"

set -euo pipefail

MESSAGE="${1:-Nasazení}"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TREE="$(mktemp -d)"

if [ ! -f "$ROOT/dist/index.html" ]; then
  echo "dist/index.html chybí — nejdřív npm run build" >&2
  exit 1
fi

cd "$ROOT"
git worktree add -q "$TREE" gh-pages
# Smaže se všechno staré, ať po sobě nezůstávají osiřelé soubory z minulých
# buildů — jména s otiskem obsahu se mění a jinak by se vrstvily.
git -C "$TREE" rm -rq .
cp -r "$ROOT/dist/." "$TREE/"
git -C "$TREE" add -A
git -C "$TREE" commit -q -m "$MESSAGE"
git -C "$TREE" push origin gh-pages

cd "$ROOT"
git worktree remove --force "$TREE"
echo "nasazeno: $(git ls-tree -r --name-only gh-pages | wc -l) souborů"
