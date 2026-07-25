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

2. **Záchyt propadlých tvarů.** LemmaGen vrací slova, která nezná, beze
   změny — a taková ohýbaná forma pak projde jako základní tvar. Přesně tak
   se do hry dostalo „agente" (5. pád), „agentek" a „tang" (2. pád množného
   čísla od „agentka" a „tanga").

   Záchyt stojí na dvou nezávislých znacích:

   a) Ohýbaný tvar má svůj základní tvar v lexikonu a ten je **častější**.

   b) Ohýbaný tvar **není heslem** v hunspellovém slovníku — hunspell si ho
      odvozuje z hesla příponovými pravidly. To je klíčová pojistka: chrání
      skutečné 1. pády, které by jinak pravidla omylem smetla („losos" kvůli
      častějšímu „lososa", „lít" kvůli „líto", „brigadýr" kvůli oslovení
      „brigadýre"). Samotné porovnání frekvence na tohle nestačí, protože
      v titulkovém korpusu bývá 5. pád běžnější než 1.

   Naopak hesla nestačí sama o sobě: hunspell nemá jako hesla například
   příslovce („dobře", „rychle"), takže se používají jen jako ochrana, ne
   jako podmínka pro zařazení.
"""

import json
import os

from lemmagen3 import Lemmatizer

HERE = os.path.dirname(__file__)
OUT = os.path.join(HERE, "out")
DIC = os.path.join(HERE, "raw", "cs_CZ.dic")

# Pravidla na tvary, které projdou lemmatizérem. Funkce vrací tvar, ze kterého
# by slovo mohlo být odvozené; slovo se zahodí jen tehdy, když takový tvar
# v lexikonu opravdu je a je častější.
LEAK_RULES: list[tuple[str, object]] = [
    # odebrání koncovky
    ("5. pád mužský (agente → agent)", lambda w: w[:-1] if w.endswith("e") else None),
    ("5./3. pád, 1. p. mn. č. (sloni → slon)", lambda w: w[:-1] if w.endswith("i") else None),
    ("3./6. pád a slovesné tvary (hradu → hrad)", lambda w: w[:-1] if w.endswith("u") else None),
    ("5. pád ženský (babo → baba)", lambda w: w[:-1] + "a" if w.endswith("o") else None),
    ("2. p. mn. č. na -ek (agentek → agentka)", lambda w: w[:-2] + "ka" if w.endswith("ek") else None),
    # 2. pád množného čísla je holý kmen, základní tvar má koncovku navíc
    ("2. p. mn. č. ženský (klobás → klobása)", lambda w: w + "a"),
    ("2. p. mn. č. střední (tang → tango)", lambda w: w + "o"),
    ("2. p. mn. č. měkký (opic → opice)", lambda w: w + "e"),
]


def hunspell_headwords() -> set[str]:
    words = set()
    with open(DIC, encoding="utf-8") as fh:
        next(fh, None)  # první řádek je počet hesel
        for line in fh:
            word = line.split("/")[0].strip()
            if word:
                words.add(word)
    return words


def main():
    lemmatizer = Lemmatizer("cs")
    lexicon = json.load(open(os.path.join(OUT, "lexicon.json"), encoding="utf-8"))
    headwords = hunspell_headwords()

    # 1. stupeň — lemma se rovná slovu
    first: dict[str, list] = {}
    for length, entries in sorted(lexicon.items(), key=lambda kv: int(kv[0])):
        first[length] = [[w, f] for w, f in entries if lemmatizer.lemmatize(w) == w]

    print(f"po lemmatizaci: {sum(len(v) for v in first.values())} slov")

    # 2. stupeň — záchyt tvarů, které lemmatizér propustil
    freq = {w: f for entries in first.values() for w, f in entries}

    def leaked(word: str) -> bool:
        # Heslo hunspellu je skutečný slovníkový tvar — ten se nezahazuje.
        if word in headwords:
            return False
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
