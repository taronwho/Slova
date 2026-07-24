"""Krok 2 — kurace lexikonu.

Z ověřených slov (krok 1) postaví lexikon rozdělený podle délky, s frekvencí
a příznakem "běžné slovo". Odfiltruje vulgarismy a hanlivé výrazy.

Výstup: tools/out/lexicon.json
"""

import json
import os
import re

OUT = os.path.join(os.path.dirname(__file__), "out")

# Kmeny, jejichž odvozeniny do slovní hry nepatří (vulgarismy, nadávky,
# hanlivé a citlivé výrazy). Porovnává se na začátku slova.
BLOCK_PREFIXES = [
    "kurv", "piča", "pičo", "píč", "hovn", "hovno", "sra", "sral", "sračk",
    "prdel", "prdět", "prděl", "zkurv", "vyser", "vysra", "nasra", "nasr",
    "posra", "posr", "mrdat", "mrd", "šuká", "šukat", "šukal", "čurák",
    "čůrák", "kokot", "debil", "idiot", "kretén", "mrzák", "zmrd", "buzer",
    "buzn", "teplouš", "cigán", "cikán", "žid", "negr", "čmoud", "hajzl",
    "svin", "prasák", "děvka", "šlapka", "kunda", "koza", "vagín", "penis",
    "šourek", "varlat", "onanie", "masturb", "znásiln", "mrdk", "hajzlík",
]

BLOCK_EXACT = {"koza", "kozy", "kozu", "kozou", "kozám", "kozách"}


def blocked(word: str) -> bool:
    if word in BLOCK_EXACT:
        return True
    return any(word.startswith(p) for p in BLOCK_PREFIXES)


def main():
    words = []
    with open(os.path.join(OUT, "words.tsv"), encoding="utf-8") as fh:
        for line in fh:
            word, freq = line.rstrip("\n").split("\t")
            words.append((word, int(freq)))

    print(f"načteno {len(words)} slov")

    kept = [(w, f) for w, f in words if not blocked(w)]
    print(f"po blocklistu {len(kept)}  (odebráno {len(words) - len(kept)})")

    by_len: dict[int, list] = {}
    for word, freq in kept:
        by_len.setdefault(len(word), []).append([word, freq])

    for length in sorted(by_len):
        entries = by_len[length]
        entries.sort(key=lambda e: (-e[1], e[0]))
        freqs = [e[1] for e in entries]
        common = sum(1 for f in freqs if f >= 500)
        print(
            f"  délka {length}: {len(entries):>6}  "
            f"běžných(freq>=500) {common:>5}  max_freq {freqs[0]}"
        )

    path = os.path.join(OUT, "lexicon.json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump({str(k): v for k, v in sorted(by_len.items())}, fh, ensure_ascii=False)
    print(f"-> {path}")


if __name__ == "__main__":
    main()
