"""Krok 3 — generátor hádanek pro režim ŘETĚZ.

Graf sousednosti se staví nad *celým* ověřeným lexikonem dané délky, aby hráč
nedostal „to slovo neznám" na běžné české slovo. Zadání se ale vybírají jen
z frekventovaných slov a navíc se kontroluje, že existuje cesta délky par
složená výhradně ze srozumitelných slov — hráč tedy nikdy není nucen uhodnout
exotický tvar.

Každá vyexportovaná hádanka nese ověřenou nejkratší cestu.
"""

import json
import os
import random
from collections import deque

OUT = os.path.join(os.path.dirname(__file__), "out")
DATA = os.path.join(os.path.dirname(__file__), "..", "public", "data", "chain")

# Slovo musí být aspoň takhle časté, aby smělo být startem nebo cílem.
ENDPOINT_MIN_FREQ = 500
# Slovo musí být aspoň takhle časté, aby se počítalo za „srozumitelné"
# při kontrole humánní cesty. Delší slova jsou přirozeně vzácnější, proto
# klesající práh podle délky.
HUMANE_MIN_FREQ = {4: 200, 5: 100, 6: 25}

# délka -> (obtížnost, rozsah par, kolik hádanek chceme)
PLAN = {
    4: ("easy", range(3, 6), 2500),
    5: ("normal", range(4, 8), 3500),
    6: ("hard", range(5, 10), 3000),
}

SOURCES_PER_LENGTH = 900


def build_graph(words):
    buckets = {}
    for i, word in enumerate(words):
        for pos in range(len(word)):
            key = (pos, word[:pos], word[pos + 1 :])
            buckets.setdefault(key, []).append(i)

    adj = [[] for _ in words]
    for bucket in buckets.values():
        for a in bucket:
            for b in bucket:
                if a != b:
                    adj[a].append(b)
    # Slova jsou seřazená od nejčastějšího, takže setříděním indexů vzestupně
    # dostaneme sousedy od nejběžnějšího. BFS pak přirozeně najde
    # nejsrozumitelnější z nejkratších cest — důležité pro nápovědy.
    for lst in adj:
        lst.sort()
    return adj


def bfs(adj, source, allowed=None):
    dist = [-1] * len(adj)
    dist[source] = 0
    queue = deque([source])
    while queue:
        node = queue.popleft()
        for nb in adj[node]:
            if dist[nb] == -1 and (allowed is None or allowed[nb]):
                dist[nb] = dist[node] + 1
                queue.append(nb)
    return dist


def shortest_path(adj, source, target):
    prev = [-1] * len(adj)
    seen = [False] * len(adj)
    seen[source] = True
    queue = deque([source])
    while queue:
        node = queue.popleft()
        if node == target:
            break
        for nb in adj[node]:
            if not seen[nb]:
                seen[nb] = True
                prev[nb] = node
                queue.append(nb)
    if not seen[target]:
        return None
    path = [target]
    while path[-1] != source:
        path.append(prev[path[-1]])
    return path[::-1]


def largest_component(adj):
    seen = [False] * len(adj)
    best = []
    for start in range(len(adj)):
        if seen[start]:
            continue
        comp = []
        stack = [start]
        seen[start] = True
        while stack:
            node = stack.pop()
            comp.append(node)
            for nb in adj[node]:
                if not seen[nb]:
                    seen[nb] = True
                    stack.append(nb)
        if len(comp) > len(best):
            best = comp
    return set(best)


def main():
    random.seed(20260724)
    os.makedirs(DATA, exist_ok=True)
    lexicon = json.load(open(os.path.join(OUT, "lexicon.json"), encoding="utf-8"))

    all_puzzles = []
    summary = {}

    for length, (difficulty, par_range, wanted) in PLAN.items():
        entries = lexicon[str(length)]  # už seřazené podle frekvence sestupně
        words = [w for w, _ in entries]
        freq = {w: f for w, f in entries}
        adj = build_graph(words)
        component = largest_component(adj)

        humane = [freq[w] >= HUMANE_MIN_FREQ[length] for w in words]
        endpoints = [
            i for i in component if freq[words[i]] >= ENDPOINT_MIN_FREQ and humane[i]
        ]
        print(
            f"délka {length}: slov {len(words)}, LCC {len(component)}, "
            f"koncových kandidátů {len(endpoints)}"
        )

        endpoint_set = set(endpoints)
        sources = random.sample(endpoints, min(SOURCES_PER_LENGTH, len(endpoints)))
        found = {}

        for source in sources:
            dist_full = bfs(adj, source)
            dist_humane = bfs(adj, source, allowed=humane)
            for target in endpoint_set:
                if target <= source:
                    continue
                par = dist_full[target]
                if par not in par_range:
                    continue
                # Musí existovat cesta délky par vedoucí jen srozumitelnými slovy.
                if dist_humane[target] != par:
                    continue
                found[(source, target)] = par

        print(f"  dvojic v rozsahu par: {len(found)}")

        pairs = list(found.items())
        random.shuffle(pairs)

        # Vyvážíme zastoupení jednotlivých hodnot par, ať nejsou skoro všechny
        # hádanky nejlehčí možné.
        per_par = {}
        quota = max(wanted // len(par_range), 1)
        chosen = []
        for (source, target), par in pairs:
            if per_par.get(par, 0) >= quota:
                continue
            per_par[par] = per_par.get(par, 0) + 1
            chosen.append((source, target, par))
            if len(chosen) >= wanted:
                break

        puzzles = []
        for n, (source, target, par) in enumerate(chosen):
            path = shortest_path(adj, source, target)
            assert path is not None and len(path) - 1 == par, "cesta neodpovídá par"
            puzzles.append(
                {
                    "id": f"c{length}-{n:04d}",
                    "len": length,
                    "start": words[source],
                    "target": words[target],
                    "par": par,
                    "difficulty": difficulty,
                    "path": [words[i] for i in path],
                }
            )

        dist = {}
        for p in puzzles:
            dist[p["par"]] = dist.get(p["par"], 0) + 1
        print(f"  vybráno {len(puzzles)}  rozložení par {dict(sorted(dist.items()))}")

        with open(
            os.path.join(DATA, f"words-{length}.json"), "w", encoding="utf-8"
        ) as fh:
            json.dump(words, fh, ensure_ascii=False, separators=(",", ":"))

        # Do hry jde štíhlý tvar — cestu si klient dopočítá vlastním BFS.
        slim = [[p["start"], p["target"], p["par"]] for p in puzzles]
        with open(
            os.path.join(DATA, f"puzzles-{length}.json"), "w", encoding="utf-8"
        ) as fh:
            json.dump(slim, fh, ensure_ascii=False, separators=(",", ":"))

        summary[str(length)] = {
            "words": len(words),
            "puzzles": len(puzzles),
            "difficulty": difficulty,
        }
        all_puzzles.extend(puzzles)

    with open(os.path.join(DATA, "index.json"), "w", encoding="utf-8") as fh:
        json.dump(summary, fh, ensure_ascii=False, indent=1)

    # Plná verze s ověřenými cestami zůstává mimo build — slouží testům.
    with open(os.path.join(OUT, "chain_verified.json"), "w", encoding="utf-8") as fh:
        json.dump(all_puzzles, fh, ensure_ascii=False, separators=(",", ":"))

    print(f"\ncelkem {len(all_puzzles)} hádanek -> {DATA}")


if __name__ == "__main__":
    main()
