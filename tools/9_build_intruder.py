"""Krok 9 — pětice pro režim Vetřelec.

Čtyři slova něco spojuje, páté ne. Souvislost je vždycky jedna ze tří:

  * **jazyk původu** — čtyři z latiny, jedno z němčiny,
  * **počet slabik**,
  * **slovní druh**.

Aby byl vetřelec **právě jeden**, musí se pětice na zbylých dvou znacích
shodnout: když se hádá jazyk, mají všech pět stejný počet slabik i slovní
druh. Jinak by šlo ukázat na jiné slovo a mít taky pravdu.

Bere se ze stažených hesel Wikislovníku (krok 5c), kde je etymologie,
slovní druh i dělení na slabiky.

Výstup: public/data/intruder/puzzles.json
"""

import json
import os
import random
import re
import unicodedata

def fold(word: str) -> str:
    out = unicodedata.normalize("NFD", word.lower())
    return "".join(ch for ch in out if unicodedata.category(ch) != "Mn")


HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
OUT = os.path.join(HERE, "..", "public", "data", "intruder")

# Jazyk původu z první věty etymologie. Bere se jen ten **první** zmíněný —
# přes co slovo doputovalo dál, hráč posuzovat nemůže.
LANGS = {
    "latin": "latina",
    "řec": "řečtina",
    "něm": "němčina",
    "franc": "francouzština",
    "anglic": "angličtina",
    "italsk": "italština",
    "španěl": "španělština",
    "arabsk": "arabština",
    "hebrejsk": "hebrejština",
    "turec": "turečtina",
    "rusk": "ruština",
    "polsk": "polština",
    "maďarsk": "maďarština",
    "praslovansk": "praslovanština",
    "staroslověn": "staroslověnština",
}

POS_NAME = {"noun": "podstatné jméno", "adj": "přídavné jméno",
            "verb": "sloveso", "adv": "příslovce"}

# Rod a vid stojí v hesle jako kurzivní odrážka pod slovním druhem, takže
# se daly stáhnout už v kroku 5c. Jsou to tvrdé mluvnické údaje, ne odhad.
GENDERS = ("rod mužský neživotný", "rod mužský životný", "rod ženský", "rod střední")
ASPECTS = ("nedokonavé", "dokonavé")

# Jak slovo vzniklo. Pozná se z ustálených formulek na začátku etymologie
# a je to souvislost, kterou hráč vidí až po zamyšlení — ne z pravopisu.
FORMS = (
    ("zdrobnělina", r"zdrobněl"),
    ("přechýlené jméno", r"přechýlen"),
    ("složenina", r"složen|ze spojení|spojením slov"),
    ("odvozenina předponou", r"předpon"),
    ("odvozenina příponou", r"přípon"),
)

MIN_LEN, MAX_LEN = 4, 13
PER_KIND = 400


def origin(text: str) -> str | None:
    # Jen úplný začátek hesla. Dál v textu se jmenují jazyky, přes které
    # slovo jen prošlo, a to hráč posoudit nemůže.
    head = text[:45].lower()
    best = None
    for mark, name in LANGS.items():
        found = head.find(mark)
        if found >= 0 and (best is None or found < best[0]):
            best = (found, name)
    return best[1] if best else None


def century(text: str) -> str | None:
    """Století, ve kterém se slovo v češtině objevuje. Jen když ho heslo
    vysloveně uvádí — dohadovat se nebude."""
    found = re.search(r"\b(\d{1,2})\.\s*stolet", text[:200])
    return f"{found.group(1)}. století" if found else None


def load() -> list[dict]:
    cache = json.load(open(os.path.join(RAW, "etymology.json"), encoding="utf-8"))
    allowed = set(json.load(
        open(os.path.join(HERE, "..", "tests", "fixtures", "base-forms.json"), encoding="utf-8")
    ))
    words = []
    for word, entry in cache.items():
        if not entry or word not in allowed or not (MIN_LEN <= len(word) <= MAX_LEN):
            continue
        pos = (entry.get("pos") or [None])[0]
        syl = entry.get("syl")
        if pos not in POS_NAME or not syl or not re.fullmatch(r"[^\W\d_]+(-[^\W\d_]+)+", syl):
            continue
        kind = entry.get("kind") or ""
        story = entry.get("e") or ""
        low = story[:90].lower()
        words.append({
            "word": word,
            "pos": pos,
            "syl": syl.count("-") + 1,
            "lang": origin(story) if story else None,
            "gender": next((g for g in GENDERS if g in kind), None),
            "aspect": next((a for a in ASPECTS if a in kind), None),
            "form": next((name for name, mark in FORMS if re.search(mark, low)), None),
            "century": century(story) if story else None,
        })
    return words


# Na čem se musí pětice shodnout, aby byl vetřelec právě jeden: vždycky
# na tom, co se zrovna nehádá.
KEYS = {
    "lang": ("pos", "syl"),
    "syl": ("pos", "lang"),
    "pos": ("syl", "lang"),
    "gender": ("syl", "lang"),
    "aspect": ("syl", "lang"),
    "form": ("pos", "syl"),
    "century": ("pos", "syl"),
}

# Jak nápadný ten rozdíl je. Slovní druh a rod se poznají skoro na první
# pohled; jazyk původu a doba přejetí až po zamyšlení.
LEVEL = {
    "pos": "easy",
    "gender": "easy",
    "syl": "normal",
    "aspect": "normal",
    "form": "normal",
    "lang": "hard",
    "century": "hard",
}

LABEL = {
    "lang": "jazyk původu",
    "syl": "počet slabik",
    "pos": "slovní druh",
    "gender": "jmenný rod",
    "aspect": "vid slovesa",
    "form": "způsob vzniku",
    "century": "doba přejetí",
}


def build(words: list[dict], kind: str, rng: random.Random) -> list[dict]:
    """Pětice pro jeden druh souvislosti.

    `kind` říká, čím se vetřelec liší; na zbylých dvou znacích se všech pět
    shoduje, aby byla odpověď jednoznačná.
    """
    keys = KEYS[kind]
    buckets: dict[tuple, list[dict]] = {}
    for item in words:
        if item[kind] is None or any(item[k] is None for k in keys):
            continue
        buckets.setdefault(tuple(item[k] for k in keys), []).append(item)

    out = []
    for shared, group in buckets.items():
        by_value: dict[object, list[dict]] = {}
        for item in group:
            by_value.setdefault(item[kind], []).append(item)
        for value, four in by_value.items():
            others = [i for i in group if i[kind] != value]
            if len(four) < 4 or not others:
                continue
            rng.shuffle(four)
            rng.shuffle(others)
            for start in range(0, len(four) - 3, 4):
                odd = others[(start // 4) % len(others)]
                pick = four[start:start + 4]
                # Varianty téhož slova („kanoe" a „kánoe") vedle sebe stát
                # nesmí — vypadá to jako chyba a hráče to plete.
                stems = {re.sub(r"[^a-z]", "", fold(i["word"]))[:5] for i in pick + [odd]}
                if len(stems) < 5:
                    continue
                # Vetřelec nesmí trčet délkou — jinak se pozná od pohledu,
                # aniž by hráč o slovech přemýšlel.
                lengths = [len(i["word"]) for i in pick + [odd]]
                if max(lengths) - min(lengths) > 3:
                    continue
                out.append({
                    "kind": kind,
                    "words": [i["word"] for i in pick] + [odd["word"]],
                    "odd": odd["word"],
                    "shared": POS_NAME[value] if kind == "pos" else value,
                    "oddValue": POS_NAME[odd[kind]] if kind == "pos" else odd[kind],
                    "note": dict(zip(keys, shared)),
                })
    rng.shuffle(out)
    return out[:PER_KIND]


def main() -> int:
    rng = random.Random(7)
    words = load()
    puzzles = []
    for kind in KEYS:
        made = build(words, kind, rng)
        print(f"  {kind}: {len(made)}")
        puzzles += made
    rng.shuffle(puzzles)

    # Obtížnost podle toho, jak nápadný je rozdíl: slovní druh se pozná
    # nejsnáz, jazyk původu nejhůř.
    for i, puzzle in enumerate(puzzles):
        puzzle["id"] = f"i-{i:04d}"
        puzzle["difficulty"] = LEVEL[puzzle["kind"]]
        rng.shuffle(puzzle["words"])

    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, "puzzles.json")
    json.dump(puzzles, open(path, "w", encoding="utf-8"), ensure_ascii=False)
    print(f"pětic: {len(puzzles)} -> {os.path.normpath(path)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
