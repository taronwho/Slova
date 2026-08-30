"""Krok 2b — omezení lexikonu na základní tvary.

Hra smí pracovat jen se základními tvary: podstatná jména v 1. pádu, slovesa
v infinitivu, přídavná jména, číslovky, zájmena, příslovce a spojky. Jinak
hráč ve Voštině sbírá varianty jednoho slova místo aby hledal nová a ve Věži
se objeví „nemíříš", „agente" nebo „ovsa".

Filtr stojí na tom, že příznaky v cs_CZ.dic jsou **skloňovací a časovací
vzory**. Vzor se dá pověsit jedině na základní tvar — hunspell z něj celé
paradigma teprve odvozuje. Takže:

    hrad/HR      vzor „hrad"          -> 1. pád j. č., projde
    mířit/AN     časování             -> infinitiv, projde
    velký/Y      skloňování adjektiv  -> 1. pád m. r., projde
    agente       bez vzoru            -> neprojde
    ovsa         bez vzoru            -> neprojde
    stůj/N       jen předpona ne-     -> neprojde
    sťat/ON      jmenný tvar          -> neprojde
    moha/XN      přechodník           -> neprojde
    níže/E       jen předpona nej-    -> neprojde

Holá hesla bez vzoru jsou v cs_CZ.dic promíchaná: jsou mezi nimi příslovce
(„dnes"), spojky („ale") i nesklonná jména („alibi"), ale úplně stejně vypadá
2. pád („ovsa"), 5. pád („bože"), rozkaz („stůj") i zkratka („geol"). Rozlišit
je automaticky nejde, takže se zahazují všechna a ručně ověřený výběr se vrací
zpátky ze souboru base_extra.txt.

Druhá podmínka je **lemma se rovná slovu**: český hunspell má jako hesla
i ohýbané tvary („budu", „chce", „jdu"), a ty by vzor sám nezastavil.
Lemmatizér LemmaGen3 je odchytí.

Sám o sobě je ale nespolehlivý a hráč to poznal: ve Voštině neuznaná
*lysina*. Lemmatizér u ní tvrdí, že základní tvar je „lysin" — jenže žádné
takové slovo neexistuje, v hunspellu není a `lysina/ZQ` tam stojí jako
řádné heslo se skloňovacím vzorem. Slovo přesto vypadlo, protože se
lemmatizéru věřilo víc než slovníku. Takových bylo skoro dva tisíce:
*kuře, kotě, kalhoty, nůžky, játra, krém, trefa, želva, zmrzlina…*

Jeho nesouhlas se proto bere vážně jen tehdy, když **tvar, který navrhuje,
je sám heslem v .dic** („budu" → „být", „chce" → „chtít"). Když si ho
vymyslel, rozhoduje slovník. A protože si vymýšlí hlavně infinitivy
(„řeknu" → „řeknout", „napíšu" → „napsát"), pouští se zpátky jen slova se
jmenným nebo přídavným vzorem — časovaná slovesa zůstanou venku i tak.

Výstup: tools/out/lexicon_base.json
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from _base_form import je_zaklad  # noqa: E402
OUT = os.path.join(HERE, "out")
RAW = os.path.join(HERE, "raw")

# Příznaky, které jsou celým skloňovacím nebo časovacím vzorem. Pověsit se
# dají jedině na základní tvar.
#   P U H L S Z K M D I V  jmenné vzory
#   Q C                    krácení kmene a odvozování, také jen od 1. pádu
#   Y                      skloňování přídavných jmen
#   A B J T                časování sloves
BASE_FLAGS = set("PUHLSZKMDIVQCYABJT")

# Vzory jmenné a přídavné zvlášť od časovacích. Slovo, kterému lemmatizér
# vymyslel neexistující základní tvar, se vrací do hry jen v téhle skupině:
# u sloves si vymýšlí infinitivy („řeknu" → „řeknout") a vracet takový tvar
# by znamenalo pustit do hry časované sloveso.
JMENNE_FLAGS = set("PUHLSZKMDIVQCY")
SLOVESNE_FLAGS = set("ABJT")

# Naopak tyhle příznaky základní tvar nedokládají:
#   N E W F  jen předpony (ne-, nej-)
#   R        6. pád j. č. i odvozená příslovce — nerozlišitelné
#   O        jmenné tvary („sláb", „sťat")
#   X        přechodníky („moha", „nesa")
#   y í é    stupňování a cizí jména


def load_dic_flags(path):
    """slovo -> množina příznaků (jen malá písmena, vlastní jména do hry nepatří)"""
    flags = {}
    with open(path, encoding="utf-8") as fh:
        next(fh)
        for line in fh:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            word, _, fl = line.partition("/")
            if not word or not word.islower():
                continue
            flags.setdefault(word, set()).update(fl)
    return flags


def load_extra(path):
    words = set()
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.split("#")[0].strip()
            if line:
                words.add(line)
    return words


def main():
    from lemmagen3 import Lemmatizer

    dic = load_dic_flags(os.path.join(RAW, "cs_CZ.dic"))
    extra = load_extra(os.path.join(HERE, "base_extra.txt"))
    print(f"hesel v .dic: {len(dic)}, ručně ověřených navíc: {len(extra)}")

    unknown = sorted(w for w in extra if w not in dic)
    if unknown:
        print(f"  pozor, base_extra.txt má {len(unknown)} slov mimo .dic: {unknown[:20]}")

    lexicon = json.load(open(os.path.join(OUT, "lexicon.json"), encoding="utf-8"))
    lemmatizer = Lemmatizer("cs")

    def zaklad(word: str) -> bool:
        return je_zaklad(word, dic.get(word, set()), lemmatizer.lemmatize(word), dic, extra)

    base: dict[str, list] = {}
    vraceno = 0
    for length, entries in sorted(lexicon.items(), key=lambda kv: int(kv[0])):
        kept = []
        for word, freq in entries:
            if not zaklad(word):
                continue
            if lemmatizer.lemmatize(word) != word:
                vraceno += 1
            kept.append([word, freq])
        base[length] = kept
    print(f"  slov vrácených proti lemmatizéru (rozhodl slovník): {vraceno}")

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
