#!/usr/bin/env bash
#
# Spustí emulátor Firebase (databáze + přihlášení) se **skutečnými pravidly**
# z `tools/firebase/database.rules.json`.
#
# Proč: databáze projektu je z tohohle stroje za bránou, takže se souboje
# nedaly odehrát a chyby se musely hádat z hlášek. Emulátor je tatáž databáze
# i tatáž pravidla, jen běží tady — dá se do ní zapsat, číst z ní a hlavně
# odehrát celý souboj dvou hráčů proti sobě.
#
# Proxy se emulátoru musí sebrat: firebase-tools i Java by přes ni posílaly
# i dotazy na 127.0.0.1 a brána je odmítne.
#
# Použití:  bash tools/emu.sh start | stop | stav

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DIR="${SLOVA_EMU_DIR:-/tmp/slova-emu}"
LOG="$DIR/emulator.log"
NS='slova-b0176-default-rtdb'

priprav() {
  mkdir -p "$DIR"
  cp "$ROOT/tools/firebase/database.rules.json" "$DIR/database.rules.json"
  cat > "$DIR/firebase.json" <<'JSON'
{
  "database": { "rules": "database.rules.json" },
  "emulators": {
    "auth": { "host": "127.0.0.1", "port": 9099 },
    "database": { "host": "127.0.0.1", "port": 9000 },
    "ui": { "enabled": false }
  }
}
JSON
}

case "${1:-start}" in
  start)
    priprav
    nohup env -u HTTPS_PROXY -u https_proxy -u HTTP_PROXY -u http_proxy \
      -u ALL_PROXY -u all_proxy -u JAVA_TOOL_OPTIONS \
      "$ROOT/node_modules/.bin/firebase" emulators:start \
      --only database,auth --project slova-b0176 \
      --config "$DIR/firebase.json" > "$LOG" 2>&1 &
    disown || true
    for _ in $(seq 1 60); do
      if curl -s --noproxy '*' -m 3 "http://127.0.0.1:9000/.json?ns=$NS" > /dev/null 2>&1; then
        echo "emulátor běží (databáze 9000, přihlášení 9099)"
        exit 0
      fi
      sleep 1
    done
    echo "emulátor nenaskočil, log: $LOG" >&2
    tail -20 "$LOG" >&2
    exit 1
    ;;
  stop)
    # Pozor na `pkill -f`: vzorec nesmí sedět na tenhle skript, jinak si
    # podřízne větev pod sebou.
    pgrep -f 'emulators:start' | grep -v "^$$\$" | xargs -r kill 2>/dev/null || true
    pgrep -f 'firebase-database-emulator' | xargs -r kill 2>/dev/null || true
    echo 'emulátor zastaven'
    ;;
  stav)
    curl -s --noproxy '*' -m 5 "http://127.0.0.1:9000/.json?ns=$NS" \
      -w ' [databáze %{http_code}]\n' || echo 'databáze neodpovídá'
    ;;
  *)
    echo "použití: bash tools/emu.sh start|stop|stav" >&2
    exit 2
    ;;
esac
