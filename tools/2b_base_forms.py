"""Krok 2b — omezení lexikonu na základní tvary.

Hra smí pracovat jen se základními tvary: podstatná jména v 1. pádu jednotného
čísla, slovesa v infinitivu, přídavná jména, číslovky, zájmena, příslovce
a spojky. Jinak hráč ve Voštině sbírá varianty jednoho slova místo aby hledal
nová a ve Věži se objeví „nemíříš" nebo „agente".

Slovo projde, jen když splní **obě** podmínky:

1. **Hunspell ho umí přečíst bez jediné přípony a předpony.** Tím pádem je to
   přímo heslo slovníku, ne tvar odvozený příponovým pravidlem. Analýza je
   přesná, ne odhadovaná — hunspell u každého slova řekne, z jakého hesla
   a jakým příznakem ho odvodil:

       dobře   ← dobrý  příponou R
       nemíříš ← mířit  příponou A a předponou N
       agente  ← agent  příponou P
       tang    ← tango  příponou Q
       míše    ← mícha  příponou Z
       pes     ← bez přípony  (heslo)

   Dřívější pokusy stály na ručních pravidlech nad koncovkami a porovnání
   frekvencí. Vždycky něco proklouzlo, protože čeština má tvarů víc, než se
   dá pokrýt seznamem pravidel.

   Příznak R by šlo považovat za příslovce („dobře ← dobrý"), jenže stejným
   příznakem vzniká i 6. pád („roce ← rok", „autě ← auto"). Rozlišit je nejde,
   takže se nepouští ani jedno — hra tím přichází o odvozená příslovce jako
   „dobře" nebo „rychle", ale nepustí do sebe pádový tvar.

2. **Lemma se rovná slovu.** Samotné heslo nestačí: český hunspell má jako
   hesla i ohýbané tvary („boha", „bohu", „bohů"). Lemmatizér LemmaGen3 je
   odchytí.

Výstup: tools/out/lexicon_base.json
"""

import json
import multiprocessing as mp
import os
import time

HERE = os.path.dirname(__file__)
OUT = os.path.join(HERE, "out")
RAW = os.path.join(HERE, "raw")

_lookuper = None
_captype = None


def _init():
    global _lookuper, _captype
    from spylls.hunspell import Dictionary
    from spylls.hunspell.algo.capitalization import Type as CapType

    _lookuper = Dictionary.from_files(os.path.join(RAW, "cs_CZ")).lookuper
    _captype = CapType.NO


def _headwords(chunk):
    """Vrátí slova, která hunspell přečte bez přípony i předpony."""
    out = []
    for word in chunk:
        for form in _lookuper.affix_forms(word, _captype):
            if form.suffix is None and form.prefix is None:
                out.append(word)
                break
    return out


def chunked(items, size):
    for i in range(0, len(items), size):
        yield items[i : i + size]


def main():
    from lemmagen3 import Lemmatizer

    lexicon = json.load(open(os.path.join(OUT, "lexicon.json"), encoding="utf-8"))
    words = [w for length in lexicon for w, _ in lexicon[length]]
    print(f"kandidátů: {len(words)}")

    started = time.time()
    headwords = set()
    with mp.Pool(processes=mp.cpu_count(), initializer=_init) as pool:
        for result in pool.imap_unordered(_headwords, chunked(words, 2000)):
            headwords.update(result)
    print(
        f"hesel bez přípony: {len(headwords)}  ({time.time() - started:.0f}s)"
    )

    lemmatizer = Lemmatizer("cs")
    base: dict[str, list] = {}
    for length, entries in sorted(lexicon.items(), key=lambda kv: int(kv[0])):
        kept = [
            [w, f]
            for w, f in entries
            if w in headwords and lemmatizer.lemmatize(w) == w
        ]
        base[length] = kept

    print()
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
