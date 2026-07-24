#!/usr/bin/env bash
# Krok 0 — stažení zdrojových slovníkových dat.
#
# Zdroje:
#   cs_full.txt      frekvenční seznam češtiny z titulků (hermitdave/FrequencyWords)
#   cs_CZ.dic/.aff   hunspellový slovník češtiny (LibreOffice/dictionaries)
#
# Stažené soubory se nesledují v gitu — jsou velké a snadno obnovitelné.

set -euo pipefail

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/raw"
mkdir -p "$DIR"

fetch() {
  local url="$1" out="$2"
  if [ -s "$DIR/$out" ]; then
    echo "  $out už existuje, přeskakuji"
    return
  fi
  echo "  stahuji $out"
  curl -fsSL -o "$DIR/$out" "$url"
}

echo "Stahuji zdrojová data do $DIR"
fetch "https://raw.githubusercontent.com/hermitdave/FrequencyWords/master/content/2018/cs/cs_full.txt" cs_full.txt
fetch "https://raw.githubusercontent.com/LibreOffice/dictionaries/master/cs_CZ/cs_CZ.dic" cs_CZ.dic
fetch "https://raw.githubusercontent.com/LibreOffice/dictionaries/master/cs_CZ/cs_CZ.aff" cs_CZ.aff
echo "Hotovo."
