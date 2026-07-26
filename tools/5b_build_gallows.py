"""Krok 5b — slova pro Šibenici.

Šibenice je z celé hry nejjednodušší na řešitelnost: hádané slovo je jedno
jediné a bere se z už ověřeného seznamu základních tvarů, takže dohratelné je
z definice. Zato je nejcitlivější na to, jestli slovo hráč **zná** — u řetězu
se dá dojít oklikou a v plástvi se slovo dá minout, ale tady buď slovo znáš,
nebo visíš. Proto se nevybírá podle délky, ale hlavně podle frekvence.

Obtížnost:

    snadná   4–5 písmen, nejběžnější slova
    střední  6–7 písmen
    těžká    8–9 písmen

Diakritika se hádá po základním písmeni („u" odhalí i „ů"), takže se slova
s háčky a čárkami nijak netrestají a vybírat se dají volně.

Výstup: public/data/gallows/puzzles.json
"""

import json
import os
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
DATA = os.path.join(HERE, "..", "public", "data", "gallows")

# délky a kolik nejčastějších slov z každé délky vzít
BANDS = {
    "easy": ([4, 5], 700),
    "normal": ([6, 7], 700),
    "hard": ([8, 9], 700),
}

# Slovo, ve kterém je jen pár různých písmen, se uhodne po dvou tazích;
# slovo se skoro samými různými písmeny je zase nuda. Tohle je rozumné pásmo.
MIN_DISTINCT = 3

FOLD = str.maketrans("áčďéěíňóřšťúůýž", "acdeeinorstuuyz")


def distinct(word: str) -> int:
    return len(set(word.translate(FOLD)))


def main():
    base = json.load(open(os.path.join(OUT, "lexicon_base.json"), encoding="utf-8"))

    picked = defaultdict(list)
    for difficulty, (lengths, limit) in BANDS.items():
        pool = []
        for length in lengths:
            pool.extend(base.get(str(length), []))
        # lexicon_base je setříděný podle frekvence sestupně už uvnitř délky,
        # ale spojením dvou délek se pořadí rozbije — proto znovu.
        pool.sort(key=lambda wf: (-wf[1], wf[0]))
        for word, freq in pool:
            if distinct(word) < MIN_DISTINCT:
                continue
            picked[difficulty].append(word)
            if len(picked[difficulty]) >= limit:
                break

    os.makedirs(DATA, exist_ok=True)
    puzzles = []
    for difficulty in ("easy", "normal", "hard"):
        for i, word in enumerate(picked[difficulty]):
            puzzles.append({"id": f"g-{difficulty[0]}{i:04d}", "word": word, "difficulty": difficulty})

    path = os.path.join(DATA, "puzzles.json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(puzzles, fh, ensure_ascii=False)

    for difficulty in ("easy", "normal", "hard"):
        words = picked[difficulty]
        lengths = sorted({len(w) for w in words})
        print(f"{difficulty:>7}: {len(words):>4} slov, délky {lengths}, např. {', '.join(words[:6])}")
    print(f"\ncelkem {len(puzzles)} hádanek -> {os.path.normpath(path)}")


if __name__ == "__main__":
    main()
