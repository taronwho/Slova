"""Krok 2b — omezení lexikonu na základní tvary.

Bez tohohle kroku hra uznává i pádové a časované tvary („šerifa", „ozdobu",
„vodkou"), což hlavně u Voštiny znamená, že hráč lopotně sbírá varianty
jednoho slova místo aby hledal nová.

Filtr má dva stupně.

1. **Lemmatizace.** Slovo je základní tvar, když se jeho lemma rovná jemu
   samému. Pokrývá to podstatná jména v 1. pádu jednotného čísla, slovesa
   v infinitivu, přídavná jména, číslovky, zájmena, příslovce i spojky.

   Lemmatizér je LemmaGen3. Zvažoval jsem simplemma, ale ta má pro češtinu
   špatnou kvalitu — lemmatizuje „dobrý" na „dokonavý" a „dělat" na „udělat".
   Nestačí ani hesla z hunspellového .dic: obsahují i ohýbané tvary („boha",
   „bohu", „bohů").

2. **Záchyt propadlých tvarů.** LemmaGen vrací slova, která nezná, beze
   změny — a taková ohýbaná forma pak projde jako základní tvar. Přesně tak
   se do hry dostalo „agente" (5. pád) nebo „agentek" (2. pád množného čísla).

   Pozná se to bez lemmatizéru: ohýbaný tvar má svůj základní tvar v lexikonu
   a ten je **častější**. Porovnání frekvence je tu podstatné — chrání
   slova jako „země", kde tvar po odebrání koncovky („zem") sice existuje,
   ale je mnohem vzácnější, takže „země" zůstane.

Výstup: tools/out/lexicon_base.json
"""

import json
import os

from lemmagen3 import Lemmatizer

OUT = os.path.join(os.path.dirname(__file__), "out")

# Pravidla na tvary, které projdou lemmatizérem. Funkce vrací základní tvar,
# ze kterého by slovo mohlo být odvozené; slovo se zahodí jen tehdy, když
# takový tvar v lexikonu opravdu je a je častější.
LEAK_RULES: list[tuple[str, object]] = [
    ("5. pád mužský (agente → agent)", lambda w: w[:-1] if w.endswith("e") else None),
    ("5./3. pád, 1. pád mn. č. (sloni → slon)", lambda w: w[:-1] if w.endswith("i") else None),
    ("3./6. pád a slovesné tvary (hradu → hrad)", lambda w: w[:-1] if w.endswith("u") else None),
    ("5. pád ženský (babo → baba)", lambda w: w[:-1] + "a" if w.endswith("o") else None),
    ("2. pád mn. č. (agentek → agentka)", lambda w: w[:-2] + "ka" if w.endswith("ek") else None),
]


def main():
    lemmatizer = Lemmatizer("cs")
    lexicon = json.load(open(os.path.join(OUT, "lexicon.json"), encoding="utf-8"))

    # 1. stupeň — lemma se rovná slovu
    first: dict[str, list] = {}
    for length, entries in sorted(lexicon.items(), key=lambda kv: int(kv[0])):
        first[length] = [[w, f] for w, f in entries if lemmatizer.lemmatize(w) == w]

    after_lemma = sum(len(v) for v in first.values())
    print(f"po lemmatizaci: {after_lemma} slov")

    # 2. stupeň — záchyt tvarů, které lemmatizér propustil
    freq = {w: f for entries in first.values() for w, f in entries}

    def leaked(word: str) -> bool:
        for _, stem_of in LEAK_RULES:
            stem = stem_of(word)
            if stem and stem in freq and freq[stem] > freq[word]:
                return True
        return False

    base: dict[str, list] = {}
    removed = 0
    for length, entries in first.items():
        kept = []
        for w, f in entries:
            if leaked(w):
                removed += 1
                continue
            kept.append([w, f])
        base[length] = kept

    print(f"záchyt propadlých tvarů: −{removed} slov\n")

    for length in sorted(base, key=int):
        kept = base[length]
        total = len(lexicon[length])
        share = 100 * len(kept) / max(total, 1)
        print(f"  délka {length}: {len(kept):>6} z {total:>6}  ({share:.0f} %)")

    path = os.path.join(OUT, "lexicon_base.json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(base, fh, ensure_ascii=False)

    total = sum(len(v) for v in base.values())
    print(f"\ncelkem {total} základních tvarů -> {path}")


if __name__ == "__main__":
    main()
