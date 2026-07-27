"""Krok 5f — balíček slabik pro Slabikový tetris.

Hra nemá připravené dávky. Padají v ní **náhodné dvojice slabik** a hráč z nich
skládá slova, tak jako v tetrisu padají kostky. Tenhle skript proto nestaví
hádanky, ale balíček:

    syllables  ~350 nejproduktivnějších slabik i s váhou, jak často padají
    pairs      dvojslabičná slova rozdělená na dvě slabiky — z nich se občas
               rozdá dvojice, která jde složit hned, jen ji správně otočit
    words      **všechna** slova, která z těch slabik jdou složit (2–3 vedle
               sebe); podle tohohle seznamu hra pozná, co je slovo

Dřív měla každá dávka vlastních dvanáct slabik a hráč pořád dokola viděl
totéž. Balíček je jeden a velký: devět tisíc slov ze tří set padesáti slabik,
takže dvě kola po sobě nevypadají stejně.

Seznam slov se staví z ověřených základních tvarů, takže platí totéž pravidlo
jako ve zbytku hry — jen 1. pád a infinitiv. A protože je předpočítaný, hra za
běhu nic neodhaduje: buď je složený tvar v seznamu, nebo to slovo není.

Výstup: public/data/tetris/deck.json
"""

import json
import os
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
DATA = os.path.join(HERE, "..", "public", "data", "tetris")

# Slabika musí být čitelná v malém poli.
MAX_SYLLABLE = 4
# Kolik slabik vedle sebe se ještě čte jako jedno slovo.
MAX_RUN = 3
# Kolik slabik se rozdává. Víc = pestřejší, ale řidší deska; tři sta padesát
# vyšlo ze zkoušení jako místo, kde je hra pestrá a pořád se dá skládat.
DEAL_POOL = 350
# Slabika se rozdává, jen když ji jazyk používá aspoň takhle často.
MIN_USE = 4
MIN_WORD, MAX_WORD = 3, 12


def load():
    split = json.load(open(os.path.join(OUT, "syllables.json"), encoding="utf-8"))
    base = json.load(open(os.path.join(OUT, "lexicon_base.json"), encoding="utf-8"))
    freq = {w: f for length in base for w, f in base[length]}
    return split, freq


def decompose(word, pool, limit=MAX_RUN):
    """Rozklady slova na 2–limit slabik z poolu. Vrací první nalezený."""
    found = []

    def walk(rest, acc):
        if found:
            return
        if not rest:
            if 2 <= len(acc) <= limit:
                found.append(tuple(acc))
            return
        if len(acc) >= limit:
            return
        for size in range(1, MAX_SYLLABLE + 1):
            head = rest[:size]
            if head in pool:
                acc.append(head)
                walk(rest[size:], acc)
                acc.pop()

    walk(word, [])
    return found[0] if found else None


def main():
    split, freq = load()
    allowed = set(freq)

    # Jak často se která slabika v jazyce vyskytuje — to je i váha při
    # rozdávání. Časté slabiky mají víc partnerů, takže se s nimi dá pracovat.
    used = defaultdict(int)
    for word, parts in split.items():
        if all(len(part) <= MAX_SYLLABLE for part in parts):
            for part in parts:
                used[part] += 1

    ranked = sorted(
        (syl for syl, count in used.items() if count >= MIN_USE),
        key=lambda syl: (-used[syl], syl),
    )
    pool = set(ranked[:DEAL_POOL])

    words = set()
    for word in allowed:
        if not (MIN_WORD <= len(word) <= MAX_WORD):
            continue
        if decompose(word, pool):
            words.add(word)

    # Dvojslabičná slova. Z nich se rozdává dvojice, kterou jde složit hned —
    # ale jen když ji hráč otočí správně, takže je to dárek s podmínkou.
    pairs = []
    for word in sorted(words):
        parts = decompose(word, pool, limit=2)
        if parts and len(parts) == 2:
            pairs.append(list(parts))

    # Váha: kolikrát se slabika vyskytne v šipkových slovech balíčku. Slabika,
    # se kterou se nedá nic složit, by na desce jen překážela.
    weight = defaultdict(int)
    for word in words:
        parts = decompose(word, pool)
        if not parts:
            continue
        for part in parts:
            weight[part] += 1

    syllables = sorted(
        ((syl, weight[syl]) for syl in pool if weight[syl] > 0),
        key=lambda item: (-item[1], item[0]),
    )

    deck = {
        "syllables": [[syl, count] for syl, count in syllables],
        "pairs": pairs,
        "words": sorted(words),
    }

    os.makedirs(DATA, exist_ok=True)
    path = os.path.join(DATA, "deck.json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(deck, fh, ensure_ascii=False)

    old = os.path.join(DATA, "puzzles.json")
    if os.path.exists(old):
        os.remove(old)

    size = os.path.getsize(path) // 1024
    print(f"slabik: {len(syllables)}  (rozdává se z {DEAL_POOL})")
    print(f"dvojic k okamžitému složení: {len(pairs)}")
    print(f"slov: {len(words)}")
    print(f"nejčastější slabiky: {', '.join(s for s, _ in syllables[:12])}")
    print(f"\n{size} kB -> {os.path.normpath(path)}")


if __name__ == "__main__":
    main()
