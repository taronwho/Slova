"""Krok 5f — dávky slabik pro Slabikový tetris.

Dávka **není náhodná hromada slabik**. Vybírá se tak, aby se slabiky
navzájem snášely: staví se graf, ve kterém vede hrana mezi dvěma slabikami,
když spolu dávají platné slovo, a z něj se vezme hustý kus. Každá slabika
v dávce tak má na desce co dělat — a co je důležitější, má to co dělat
s několika sousedy, ne jen s jedním.

První pokus stavěl dávku z celých slov (rozsyp slovo na slabiky a zamíchej).
Vypadalo to hezky, ale nehrálo se to: každá slabika měla jediného partnera,
a jakmile se ti dva na desce minuli, zůstaly obě ležet. Simulace tehdy
vyčistila desku v šestnácti procentech dávek, teď je to násobně víc.

Ke každé dávce se navíc dopředu spočítá **seznam všech slov**, která z jejích
slabik jdou složit (dvě nebo tři vedle sebe). Hra tak při hraní nic
neodhaduje: buď je složený tvar v tom seznamu, nebo to slovo není. Seznam se
staví z ověřených základních tvarů, takže platí totéž pravidlo jako ve
zbytku hry — jen 1. pád a infinitiv.

Obtížnost mění šířku desky a velikost dávky, ne slovní zásobu:

    lehká     5×6, 12 slabik ze šesti různých
    normální  5×7, 18 slabik z osmi různých
    těžká     6×7, 24 slabik z deseti různých

Výstup: public/data/tetris/puzzles.json
"""

import json
import os
import random

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
DATA = os.path.join(HERE, "..", "public", "data", "tetris")

# Slabika musí být čitelná v malém poli, takže žádné pětipísmenné obludy.
MAX_SYLLABLE = 4
# Kolik slabik vedle sebe se ještě čte jako jedno slovo.
MAX_RUN = 3
LEVELS = {
    # `stock` je počet slabik v dávce, `pool` kolik různých slabik se do ní
    # vybere. Míň různých slabik = víc opakování = snazší hra.
    "easy": {"cols": 5, "rows": 6, "stock": 12, "pool": 6},
    "normal": {"cols": 5, "rows": 7, "stock": 18, "pool": 8},
    "hard": {"cols": 6, "rows": 7, "stock": 24, "pool": 10},
}
PER_LEVEL = 220


def load():
    split = json.load(open(os.path.join(OUT, "syllables.json"), encoding="utf-8"))
    base = json.load(open(os.path.join(OUT, "lexicon_base.json"), encoding="utf-8"))
    freq = {w: f for length in base for w, f in base[length]}
    allowed = set(freq)
    return split, freq, allowed


def solutions(inventory, allowed):
    """Všechna povolená slova, která jdou složit z 2–3 slabik dávky.

    Bere se v potaz, kolikrát která slabika v dávce je: dvouslabičné slovo ze
    dvou stejných slabik projde jen tehdy, když je slabika v dávce dvakrát.
    """
    counts = {}
    for syl in inventory:
        counts[syl] = counts.get(syl, 0) + 1
    uniq = sorted(counts)

    found = set()

    def walk(prefix, used, depth):
        if depth >= 2 and prefix in allowed:
            found.add(prefix)
        if depth == MAX_RUN:
            return
        for syl in uniq:
            if used.get(syl, 0) >= counts[syl]:
                continue
            used[syl] = used.get(syl, 0) + 1
            walk(prefix + syl, used, depth + 1)
            used[syl] -= 1

    walk("", {}, 0)
    return sorted(found)


def partners(split, allowed):
    """Graf slabik: hrana tam, kde dvě slabiky dají platné slovo."""
    used = {}
    for word, parts in split.items():
        if not all(len(p) <= MAX_SYLLABLE for p in parts):
            continue
        for part in parts:
            used[part] = used.get(part, 0) + 1

    # Jen slabiky, které se v jazyce opravdu vyskytují — jednorázovky by graf
    # zaplevelily a ve hře by se pak potkaly jednou za uherský rok.
    common = [syl for syl, count in used.items() if count >= 8]
    edges = {syl: set() for syl in common}
    for a in common:
        for b in common:
            if a + b in allowed:
                edges[a].add(b)
                edges[b].add(a)
    return {syl: partners for syl, partners in edges.items() if partners}


def main():
    split, freq, allowed = load()
    rng = random.Random(20260727)
    graph = partners(split, allowed)
    seeds = sorted(graph, key=lambda syl: (-len(graph[syl]), syl))[:400]

    puzzles = []
    for level, conf in LEVELS.items():
        made = 0
        guard = 0
        while made < PER_LEVEL and guard < PER_LEVEL * 60:
            guard += 1
            start = rng.choice(seeds)
            chosen = [start]
            # Přibírá se slabika, která má nejvíc vazeb na to, co už v dávce
            # je. Dávka tím drží pohromadě místo aby byla pytel náhod.
            while len(chosen) < conf["pool"]:
                have = set(chosen)
                candidates = {
                    syl
                    for pick in chosen
                    for syl in graph.get(pick, ())
                    if syl not in have
                }
                if not candidates:
                    break
                ranked = sorted(
                    candidates,
                    key=lambda syl: (-len(graph[syl] & have), -len(graph[syl]), syl),
                )
                chosen.append(rng.choice(ranked[:4]))
            if len(chosen) < conf["pool"]:
                continue

            # Zásoba: každá slabika aspoň jednou, zbytek se dolosuje podle
            # toho, kolik má vazeb — časté slabiky se objeví víckrát.
            inventory = list(chosen)
            weights = [len(graph[syl] & set(chosen)) + 1 for syl in chosen]
            while len(inventory) < conf["stock"]:
                inventory.append(rng.choices(chosen, weights=weights)[0])

            words = solutions(inventory, allowed)
            # Dávka musí nabízet opravdu bohatý výběr, jinak se nedá dohrát.
            if len(words) < conf["pool"] * 2:
                continue
            # A každá slabika v ní musí mít co dělat.
            if any(not any(syl in word for word in words) for syl in chosen):
                continue

            queue = inventory[:]
            rng.shuffle(queue)
            puzzles.append(
                {
                    "id": f"t-{level[0]}{made:04d}",
                    "difficulty": level,
                    "cols": conf["cols"],
                    "rows": conf["rows"],
                    "queue": queue,
                    "words": words,
                    # Nejdelší slova dávky — ukážou se po kole jako „šlo i tohle".
                    "seed": sorted(words, key=lambda w: (-len(w), w))[:6],
                }
            )
            made += 1

    seen = set()
    unique = []
    for puzzle in puzzles:
        key = tuple(sorted(puzzle["queue"]))
        if key in seen:
            continue
        seen.add(key)
        unique.append(puzzle)
    for i, puzzle in enumerate(unique):
        puzzle["id"] = f"t-{i:04d}"

    os.makedirs(DATA, exist_ok=True)
    path = os.path.join(DATA, "puzzles.json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(unique, fh, ensure_ascii=False)

    print(f"dávek: {len(unique)}")
    for level in LEVELS:
        pack = [p for p in unique if p["difficulty"] == level]
        if not pack:
            continue
        avg = sum(len(p["words"]) for p in pack) / len(pack)
        print(f"  {level}: {len(pack)}  slabik {len(pack[0]['queue'])}  slov průměrně {avg:.0f}")
    print(f"\n-> {os.path.normpath(path)}")


if __name__ == "__main__":
    main()
