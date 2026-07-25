"""Krok 2b — omezení lexikonu na základní tvary.

Bez tohohle kroku hra uznává i pádové a časované tvary („šerifa", „ozdobu",
„vodkou"), což hlavně u Voštiny znamená, že hráč lopotně sbírá varianty
jednoho slova místo aby hledal nová.

Základní tvar se pozná tak, že se slovo lemmatizuje a výsledek se rovná
původnímu slovu. Pokrývá to podstatná jména v 1. pádu jednotného čísla,
slovesa v infinitivu, přídavná jména v základním tvaru, číslovky, zájmena,
příslovce i spojky.

Lemmatizér je LemmaGen3. Zvažoval jsem simplemma, ale ta má pro češtinu
špatnou kvalitu — lemmatizuje „dobrý" na „dokonavý" a „dělat" na „udělat",
takže by filtr propouštěl nesmysly a mazal správné tvary.

Co tenhle krok NEUMÍ: oddělit 1. pád množného čísla („hrady") od ostatních
pádů („hradu", „hradem"). Na to je potřeba morfologie se značkami pádu
(MorfFlex a spol.), a ta v tomhle prostředí není dostupná. Množná čísla se
proto do lexikonu základních tvarů nedostanou.

Výstup: tools/out/lexicon_base.json
"""

import json
import os

from lemmagen3 import Lemmatizer

OUT = os.path.join(os.path.dirname(__file__), "out")


def main():
    lemmatizer = Lemmatizer("cs")
    lexicon = json.load(open(os.path.join(OUT, "lexicon.json"), encoding="utf-8"))

    first: dict[str, list] = {}
    for length, entries in sorted(lexicon.items(), key=lambda kv: int(kv[0])):
        first[length] = [[w, f] for w, f in entries if lemmatizer.lemmatize(w) == w]

    # 5. pád jednotného čísla ženských jmen („babo", „osobo") lemmatizér
    # nepozná a propustí ho jako základní tvar. Pozná se ale spolehlivě podle
    # toho, že po záměně koncového -o za -a vznikne 1. pád, který v seznamu
    # základních tvarů už je. Podmínka je záměrně přísná, aby nepadla běžná
    # slova na -o jako „jitro" nebo „kilo", u kterých tvar na -a mezi
    # základními tvary není.
    all_base = {w for entries in first.values() for w, _ in entries}
    dropped = 0

    base: dict[str, list] = {}
    for length, entries in first.items():
        kept = []
        for w, f in entries:
            if w.endswith("o") and w[:-1] + "a" in all_base:
                dropped += 1
                continue
            kept.append([w, f])
        base[length] = kept
    print(f"  odebráno {dropped} pravděpodobných 5. pádů")

    for length in sorted(base, key=int):
        kept = base[length]
        total = len(lexicon[length])
        print(f"  délka {length}: {len(kept):>6} z {total:>6}  ({100 * len(kept) / max(total, 1):.0f} %)")

    path = os.path.join(OUT, "lexicon_base.json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(base, fh, ensure_ascii=False)

    total = sum(len(v) for v in base.values())
    print(f"\ncelkem {total} základních tvarů -> {path}")


if __name__ == "__main__":
    main()
