"""Krok 2c — dogenerování 1. pádu množného čísla.

Základní tvar podstatného jména je pro hru i jeho množné číslo v 1. pádě
(„pes / psi", „kniha / knihy"). Krok 2b takové tvary zahodí, protože je
hunspell odvozuje příponou. Tenhle krok je vrátí — ale jen je.

Postup:

1. Z cs_CZ.aff se načtou příponová pravidla. Příznak = deklinační vzor,
   v _plural_rules.py je u každého vzoru vypsaná buňka „1. pád mn. č.".
2. Z cs_CZ.dic se vezmou hesla a jejich příznaky. Heslo musí být samo
   základní tvar (lemma se rovná slovu), jinak by se stavělo na nesmyslu.
3. Pravidlo se aplikuje, sedí-li jeho podmínka na konec hesla.
4. Vygenerovaný tvar projde, jen když ho zná hunspell (je v lexicon.json)
   a když ho lemmatizér vrátí zpátky na heslo. To je poslední pojistka
   proti chybě ve vzoru.

Výsledek se přimíchá do lexicon_base.json (s frekvencí z lexicon.json).

Použití:
    python3 tools/2c_plural.py            # zapíše lexicon_base.json
    python3 tools/2c_plural.py --vzorek   # jen vypíše ukázky pravidel
"""

import json
import os
import re
import sys
from collections import defaultdict

from _plural_rules import NEEDS_NOUN_FLAG, NOM_PL, NOUN_FLAGS

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
RAW = os.path.join(HERE, "raw")


def load_rules(path):
    """příznak -> [(odtrhni, přidej, regulární výraz podmínky)]"""
    rules = defaultdict(list)
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            if not line.startswith("SFX "):
                continue
            parts = line.split("#")[0].split()
            if len(parts) < 5:
                continue  # hlavička SFX X Y 24
            _, flag, strip, add, cond = parts[:5]
            add = add.split("/")[0]
            if add == "0":
                add = ""
            rules[flag].append((strip, add, re.compile(cond + "$")))
    return rules


def load_dic(path):
    """slovo -> množina příznaků"""
    entries = {}
    with open(path, encoding="utf-8") as fh:
        next(fh)  # počet hesel
        for line in fh:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            word, _, flags = line.partition("/")
            if not word or not word.islower():
                continue  # vlastní jména a zkratky do hry nepatří
            entries[word] = set(flags)
    return entries


def generate(rules, entries):
    """(tvar, heslo, příznak, pravidlo) pro každý 1. pád mn. č."""
    made = []
    for word, flags in entries.items():
        has_noun_flag = bool(flags & NOUN_FLAGS)
        for flag in flags:
            wanted = NOM_PL.get(flag)
            if wanted is None:
                continue
            if flag in NEEDS_NOUN_FLAG and not has_noun_flag:
                continue
            for strip, add, cond in rules[flag]:
                if (strip, add or "0") not in wanted:
                    continue
                # Vzor U tvoří 1. pád mn. č. koncovkou -i („muž -> muži"),
                # jenže jména na -tel ho mají na -é (příznak D navíc)
                # a „učiteli" je jen 3./5./6. pád jednotného čísla.
                if flag == "U" and strip == "0" and add == "i":
                    if "D" in flags or word.endswith("l"):
                        continue
                # Vzor S má 1. pád mn. č. na -e („stroj -> stroje"), jenže
                # jména na -en jdou podle „kámen" a mají -y („kmen -> kmeny",
                # ne „kmene", což je 2. pád jednotného čísla).
                if flag == "S" and strip == "0" and add == "e" and word.endswith("n"):
                    continue
                if strip != "0" and not word.endswith(strip):
                    continue
                if not cond.search(word):
                    continue
                stem = word[: -len(strip)] if strip != "0" else word
                made.append((stem + add, word, flag, f"{strip}->{add}"))
    return made


def conflicts(rules, entries):
    """Slova, u kterých v jednom vzoru zabraly dvě různá pravidla.

    Každý vzor má 1. pád mn. č. jen jeden, takže dvě pravidla znamenají, že
    je jedno z nich pro tenhle konec slova špatně — přesně tak vzniklo
    „kmen -> kmene" vedle správného „kmen -> kmeny".
    """
    found = defaultdict(set)
    for form, word, flag, rule in generate(rules, entries):
        found[(word, flag)].add((rule, form))
    return {k: v for k, v in found.items() if len(v) > 1}


def sample(rules, entries, per_rule=12):
    made = generate(rules, entries)
    lexicon = json.load(open(os.path.join(OUT, "lexicon.json"), encoding="utf-8"))
    known = {w for length in lexicon for w, _ in lexicon[length]}

    by_rule = defaultdict(list)
    for form, word, flag, rule in made:
        if form in known:
            by_rule[(flag, rule)].append((word, form))

    for key in sorted(by_rule):
        pairs = by_rule[key]
        step = max(1, len(pairs) // per_rule)
        shown = pairs[::step][:per_rule]
        print(f"\n{key[0]} {key[1]}  ({len(pairs)}x)")
        print("   " + ",  ".join(f"{a} -> {b}" for a, b in shown))


def main():
    from lemmagen3 import Lemmatizer

    rules = load_rules(os.path.join(RAW, "cs_CZ.aff"))
    entries = load_dic(os.path.join(RAW, "cs_CZ.dic"))
    print(f"hesel: {len(entries)}")

    if "--vzorek" in sys.argv:
        sample(rules, entries)
        return

    clash = conflicts(rules, entries)
    if clash:
        print(f"KOLIZE: {len(clash)} slov, kde jeden vzor dal dva tvary")
        for (word, flag), variants in sorted(clash.items())[:20]:
            print(f"  {word} [{flag}] -> {sorted(variants)}")
        raise SystemExit("oprav _plural_rules.py, než se data vygenerují")

    lemmatizer = Lemmatizer("cs")
    lexicon = json.load(open(os.path.join(OUT, "lexicon.json"), encoding="utf-8"))
    freq = {w: f for length in lexicon for w, f in lexicon[length]}

    # Heslo musí být samo lemma, jinak by se množné číslo stavělo na
    # ohnutém tvaru („boha" je v cs_CZ.dic taky heslo).
    lemmas = {w for w in entries if lemmatizer.lemmatize(w) == w}
    print(f"hesel, která jsou lemma: {len(lemmas)}")

    plurals = {}
    source = {}
    for form, word, _flag, _rule in generate(rules, entries):
        if word not in lemmas or form == word:
            continue
        if form not in freq:
            continue
        if lemmatizer.lemmatize(form) != word:
            continue
        plurals[form] = max(plurals.get(form, 0), freq[form])
        source.setdefault(form, word)
    print(f"1. pád mn. č.: {len(plurals)}")

    base = json.load(open(os.path.join(OUT, "lexicon_base.json"), encoding="utf-8"))
    added = 0
    for form, f in plurals.items():
        length = str(len(form))
        if length not in base:
            continue  # délka mimo rozsah hry
        if any(w == form for w, _ in base[length]):
            continue
        base[length].append([form, f])
        added += 1

    for length in base:
        base[length].sort(key=lambda wf: (-wf[1], wf[0]))

    print()
    for length in sorted(base, key=int):
        print(f"  délka {length}: {len(base[length]):>6}")

    path = os.path.join(OUT, "lexicon_base.json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(base, fh, ensure_ascii=False)
    total = sum(len(v) for v in base.values())
    print(f"\npřidáno {added} tvarů, celkem {total} -> {path}")

    # Fixtura pro testy dat musí odpovídat slovníku, ze kterého se hádanky
    # generují — proto se píše tady, ne ručně.
    # Mapa tvar -> výchozí heslo. Věž ji používá, aby nad sebou nestavěla
    # jednotné a hned množné číslo téhož slova („trajekt", „trajekty").
    with open(os.path.join(OUT, "plurals.json"), "w", encoding="utf-8") as fh:
        json.dump(source, fh, ensure_ascii=False)

    fixture = os.path.join(HERE, "..", "tests", "fixtures", "base-forms.json")
    os.makedirs(os.path.dirname(fixture), exist_ok=True)
    with open(fixture, "w", encoding="utf-8") as fh:
        json.dump(sorted({w for v in base.values() for w, _ in v}), fh, ensure_ascii=False)
    print(f"fixtura -> {os.path.normpath(fixture)}")


if __name__ == "__main__":
    main()
