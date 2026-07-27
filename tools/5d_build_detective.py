"""Krok 5d — hádanky pro Etymologického detektiva.

Ze stažených etymologií (krok 5c) se vyberou ty, které se dají použít jako
hádanka. Rozhoduje se o **použitelnosti, ne o pravdivosti** — text je tak jak
ho napsal Wikislovník, jen očištěný a zkrácený.

Vyhazuje se:

1. **Text, který slovo prozradí.** Nejčastější případ jsou složeniny:
   „Ze spojení jest-li" u hesla *jestli* nebo „Složením slov tak a hle"
   u *takhle*. Kontroluje se shoda podle základu slova bez diakritiky, obojím
   směrem, plus úvodní formulky složenin.
2. **Příliš krátký text.** „Z praslovanského *dobrъ." je pravda, ale hráči
   neřekne nic, z čeho by se dalo vyjít.
3. **Slovní druhy, které se nehádají.** Spojky a částice; zůstávají podstatná
   a přídavná jména, slovesa a příslovce.

Výstup: public/data/detective/puzzles.json
"""

import json
import os
import re
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
RAW = os.path.join(HERE, "raw")
DATA = os.path.join(HERE, "..", "public", "data", "detective")

MIN_TEXT, MAX_TEXT = 55, 300
# Kolik zamaskovaných míst text ještě unese, než přestane dávat smysl.
MAX_MASKS = 2
MASK = "…"
MIN_WORD, MAX_WORD = 4, 12
KEEP_POS = {"noun", "adj", "verb", "adv"}

# Úvody, po kterých následuje rozbor složeniny — ten slovo vždycky vyzradí.
COMPOUND_START = re.compile(
    r"^(složen|slozen|ze spojení|ze slovního spojení|slovním spojením|spojením"
    r"|z\s+spojení|zdrobněl)",
    re.I,
)


# Slovo včetně kombinujících znamének. V rekonstrukcích jsou navíc přízvuky
# („*mě̀sto"), a kdyby se braly jako hranice slova, rozpadlo by se hledané
# slovo na dva neškodně vypadající kousky a proklouzlo by.
TOKEN_RE = re.compile(r"([^\W\d_](?:[^\W\d_]|[\u0300-\u036f])*)", re.UNICODE)


def fold(word: str) -> str:
    out = unicodedata.normalize("NFD", word.lower())
    return "".join(ch for ch in out if unicodedata.category(ch) != "Mn")


def common_prefix(a: str, b: str) -> int:
    n = 0
    while n < len(a) and n < len(b) and a[n] == b[n]:
        n += 1
    return n


def gives_away(token: str, target: str) -> bool:
    """Prozradí tenhle výraz hledané slovo?

    Wikislovník hledané slovo běžně opakuje — ve významovém překladu („z
    praslovanského *město"), v odkazu na příbuzné slovo („souvisí se světlo")
    nebo v rozboru složeniny („pravý + -da"). Nejde o chybu textu, jen se to
    nesmí dostat k hráči.
    """
    if len(token) < 3:
        return False
    if token == target:
        return True
    # Část složeniny nebo naopak celé slovo uvnitř delšího výrazu.
    if len(token) >= 4 and (token in target or target in token):
        return True
    # Společný začátek. U krátkých slov stačí čtyři písmena, u delších pět —
    # „svět" a „světlo" ano, „vězení" a „vězet" ne.
    need = min(4, len(target)) if len(target) <= 6 else 5
    return common_prefix(token, target) >= need


def mask(word: str, text: str):
    """Zamaskuje prozrazující výrazy. Vrátí (text, použitelné?)."""
    if COMPOUND_START.search(text.strip()):
        return text, False

    target = fold(word)
    masks = 0
    out = []
    for piece in TOKEN_RE.split(text):
        if piece and TOKEN_RE.fullmatch(piece) and gives_away(fold(piece.lower()), target):
            masks += 1
            # Dvě zamaskovaná místa vedle sebe splynou v jedno.
            if out and out[-1] == MASK:
                continue
            out.append(MASK)
        else:
            out.append(piece)
    masked = re.sub(r"\s+", " ", "".join(out)).strip()
    masked = re.sub(r"\s+([,.;])", r"\1", masked)

    if masks > MAX_MASKS:
        return masked, False
    # Zamaskované slovo hned v úvodu ubere textu smysl („… z … je …").
    if masked.startswith(MASK):
        return masked, False
    return masked, len(masked) >= MIN_TEXT


def shorten(text: str) -> str:
    """Nejvýš dvě věty a rozumná délka — hádanka, ne heslo encyklopedie."""
    text = text.strip()
    if len(text) <= MAX_TEXT:
        return text
    sentences = re.split(r"(?<=[.!?])\s+", text)
    out = ""
    for sentence in sentences:
        if out and len(out) + len(sentence) + 1 > MAX_TEXT:
            break
        out = f"{out} {sentence}".strip()
    # Jedna dlouhá věta se nerozdělí — pak se ořízne natvrdo na hranici slova.
    if len(out) > MAX_TEXT:
        out = out[:MAX_TEXT].rsplit(" ", 1)[0] + "…"
    return out or text[:MAX_TEXT].rsplit(" ", 1)[0] + "…"


def difficulty(word: str) -> str:
    if len(word) <= 5:
        return "easy"
    return "normal" if len(word) <= 7 else "hard"


def main():
    cache = json.load(open(os.path.join(RAW, "etymology.json"), encoding="utf-8"))
    base = json.load(open(os.path.join(OUT, "lexicon_base.json"), encoding="utf-8"))
    allowed = {w for length in base for w, _ in base[length]}
    freq = {w: f for length in base for w, f in base[length]}

    puzzles = []
    dropped = {"pos": 0, "short": 0, "leak": 0, "mimo slovník": 0}

    for word, entry in cache.items():
        if not entry or not isinstance(entry, dict):
            continue
        if word not in allowed:
            dropped["mimo slovník"] += 1
            continue
        if not (MIN_WORD <= len(word) <= MAX_WORD):
            continue
        if not (set(entry.get("pos") or []) & KEEP_POS):
            dropped["pos"] += 1
            continue
        text = shorten(entry["e"])
        if len(text) < MIN_TEXT:
            dropped["short"] += 1
            continue
        text, usable = mask(word, text)
        if not usable:
            dropped["leak"] += 1
            continue
        puzzles.append(
            {
                "id": f"d-{len(puzzles):04d}",
                "word": word,
                "clue": text,
                "difficulty": difficulty(word),
            }
        )

    # Nejběžnější slova první — snadné úrovně mají být i ta známější.
    puzzles.sort(key=lambda p: -freq.get(p["word"], 0))
    for i, puzzle in enumerate(puzzles):
        puzzle["id"] = f"d-{i:04d}"

    os.makedirs(DATA, exist_ok=True)
    path = os.path.join(DATA, "puzzles.json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(puzzles, fh, ensure_ascii=False)

    print(f"hádanek: {len(puzzles)}")
    for reason, count in dropped.items():
        print(f"  zahozeno ({reason}): {count}")
    for level in ("easy", "normal", "hard"):
        print(f"  {level}: {sum(1 for p in puzzles if p['difficulty'] == level)}")
    print(f"\n-> {os.path.normpath(path)}")


if __name__ == "__main__":
    main()
