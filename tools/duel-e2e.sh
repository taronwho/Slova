#!/usr/bin/env bash
#
# Souboj dvou hráčů proti skutečné databázi — od začátku do konce.
#
# Postaví hru v podobě, která mluví s emulátorem Firebase, pustí emulátor se
# **skutečnými pravidly** z `tools/firebase/database.rules.json`, obojí
# propojí a odehraje celou cestu ve dvou prohlížečích naráz.
#
# Proč to nejde jednodušeji: databáze projektu je z vývojového stroje za
# bránou. Bez emulátoru se souboje nedaly vyzkoušet vůbec a chyby se musely
# hádat z hlášek na snímcích od hráče — což stálo několik kol dohadování.
#
# Použití:  npm run audit:duel:e2e

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PORT=4174
OUT="$ROOT/dist-emu"
DB='http://127.0.0.1:9000'
AUTH='http://127.0.0.1:9099'

cd "$ROOT"

echo '— emulátor'
bash tools/emu.sh start

echo '— sestavení pro emulátor'
SLOVA_EMU=1 npx vite build --outDir dist-emu > /dev/null

# Zásada obsahu pouští jen vlastní adresu a databázi projektu; emulátor běží
# jinde, takže se do ní pro tenhle build doplní. Produkční `index.html` se
# nemění — tohle je jiný, jednorázový výstup.
node -e "
const fs = require('node:fs')
const cesta = '$OUT/index.html'
let html = fs.readFileSync(cesta, 'utf8')
html = html.replace(\"connect-src 'self'\", \"connect-src 'self' $DB ws://127.0.0.1:9000 $AUTH\")
html = html.replace(/script-src 'self'[^;]*/, \"script-src 'self' $DB\")
fs.writeFileSync(cesta, html)
"

# Data hádanek se do emulátorového buildu kopírují z běžného, ať se nemusí
# generovat dvakrát.
if [ -d "$ROOT/dist/data" ]; then
  rm -rf "$OUT/data"
  cp -r "$ROOT/dist/data" "$OUT/data"
fi

echo '— server'
python3 -m http.server "$PORT" --directory "$OUT" > /dev/null 2>&1 &
SERVER=$!
trap 'kill $SERVER 2>/dev/null || true' EXIT
sleep 1

echo '— souboj'
EMU_URL="http://localhost:$PORT/" node tools/audit-duel-e2e.mjs
