"""Krok 5 — generátor hádanek pro režim VĚŽ.

Věž je řetěz podpisů (setříděných písmen): sig3 ⊂ sig4 ⊂ … ⊂ sigN, kde každý
další vznikne přidáním jednoho písmene a ke každému existuje aspoň jedno platné
české slovo.

Odsud plyne garance řešitelnosti, a to velmi silná: protože hráč musí v každém
patře použít **všechna** dostupná písmena, má jakékoli jeho platné řešení
nutně tentýž podpis. Volba konkrétního slova tedy nemůže ovlivnit, jestli půjde
postavit další patro — budoucnost věže závisí jen na podpisu, který řídíme my.

Věž se staví shora dolů: nejdřív se najdou podpisy, ze kterých vede úplný
řetěz až na tři písmena.
"""

import glob
import json
import os
import random

OUT = os.path.join(os.path.dirname(__file__), "out")
DATA = os.path.join(os.path.dirname(__file__), "..", "public", "data", "tower")

# Lexikon omezený na základní tvary (krok 2b).
LEXICON = "lexicon_base.json"

# Věž se staví jen ze slov, která hráč reálně zná …
CORE_MIN_FREQ = 20
# … ale uznáváme i vzácnější platný anagram, když ho hráč vymyslí.
ACCEPT_MIN_FREQ = 2

# obtížnost -> nejvyšší patro
TOP_LEVEL = {"easy": 6, "normal": 7, "hard": 8}
BASE_LEVEL = 3

TOWERS_PER_DIFFICULTY = 900
TOWERS_PER_PACK = 60


def signature(word: str) -> str:
    return "".join(sorted(word))


def main():
    random.seed(20260724)
    os.makedirs(DATA, exist_ok=True)
    # Staré balíčky je nutné smazat — když jich nová sada vyrobí míň, osiřelý
    # soubor by zůstal ležet a index by mu neodpovídal.
    for stale in glob.glob(os.path.join(DATA, "pack-*.json")):
        os.remove(stale)
    lexicon = json.load(open(os.path.join(OUT, LEXICON), encoding="utf-8"))

    core: dict[str, list[str]] = {}
    accept: dict[str, list[str]] = {}
    freq_of: dict[str, int] = {}

    for length in range(BASE_LEVEL, max(TOP_LEVEL.values()) + 1):
        for word, freq in lexicon.get(str(length), []):
            if freq < ACCEPT_MIN_FREQ:
                continue
            if any(word[i] == word[i + 1] == word[i + 2] for i in range(len(word) - 2)):
                continue
            sig = signature(word)
            accept.setdefault(sig, []).append(word)
            freq_of[word] = freq
            if freq >= CORE_MIN_FREQ:
                core.setdefault(sig, []).append(word)

    by_level: dict[int, list[str]] = {}
    for sig in core:
        by_level.setdefault(len(sig), []).append(sig)

    # Pro každé patro: podpisy, ze kterých vede úplný řetěz dolů na BASE_LEVEL,
    # spolu se seznamem možných rodičů (podpis o patro níž).
    parents: dict[str, list[str]] = {}
    alive: dict[int, set[str]] = {BASE_LEVEL: set(by_level.get(BASE_LEVEL, []))}

    for level in range(BASE_LEVEL + 1, max(TOP_LEVEL.values()) + 1):
        alive[level] = set()
        for sig in by_level.get(level, []):
            options = []
            seen = set()
            for i in range(len(sig)):
                sub = sig[:i] + sig[i + 1 :]
                if sub in seen:
                    continue
                seen.add(sub)
                if sub in alive[level - 1]:
                    options.append(sub)
            if options:
                parents[sig] = options
                alive[level].add(sig)
        print(f"  patro {level}: {len(alive[level])} podpisů s úplným řetězem")

    def best_word(sig: str) -> str:
        return max(core.get(sig, accept[sig]), key=lambda w: freq_of.get(w, 0))

    def build_tower(top_sig: str) -> list[str] | None:
        chain = [top_sig]
        sig = top_sig
        while len(sig) > BASE_LEVEL:
            options = parents.get(sig)
            if not options:
                return None
            # Preferujeme rodiče s nejběžnějším slovem — věž pak drží úroveň.
            options = sorted(
                options, key=lambda s: -freq_of.get(best_word(s), 0)
            )[:3]
            sig = random.choice(options)
            chain.append(sig)
        return chain[::-1]

    all_towers = []
    for difficulty, top in TOP_LEVEL.items():
        candidates = sorted(alive[top])
        random.shuffle(candidates)
        made = []
        for top_sig in candidates:
            chain = build_tower(top_sig)
            if chain is None:
                continue
            levels = []
            ok = True
            for depth, sig in enumerate(chain):
                words = sorted(set(accept.get(sig, [])), key=lambda w: -freq_of.get(w, 0))
                if not words:
                    ok = False
                    break
                added = None
                if depth > 0:
                    prev = list(chain[depth - 1])
                    rest = list(sig)
                    for ch in prev:
                        rest.remove(ch)
                    added = rest[0]
                levels.append({"sig": sig, "added": added, "words": words})
            if not ok:
                continue
            made.append({"difficulty": difficulty, "levels": levels})
            if len(made) >= TOWERS_PER_DIFFICULTY:
                break
        print(f"{difficulty}: {len(made)} věží (patra {BASE_LEVEL}–{top})")
        all_towers.extend(made)

    random.shuffle(all_towers)

    index = []
    packs: list[list[dict]] = []
    for n, tower in enumerate(all_towers):
        tower_id = f"t-{n:04d}"
        pack_no = n // TOWERS_PER_PACK
        while len(packs) <= pack_no:
            packs.append([])
        entry = {"id": tower_id, "difficulty": tower["difficulty"], "levels": tower["levels"]}
        packs[pack_no].append(entry)
        index.append(
            {
                "id": tower_id,
                "pack": pack_no,
                "difficulty": tower["difficulty"],
                "top": len(tower["levels"]) + BASE_LEVEL - 1,
            }
        )

    for pack_no, pack in enumerate(packs):
        with open(
            os.path.join(DATA, f"pack-{pack_no:03d}.json"), "w", encoding="utf-8"
        ) as fh:
            json.dump(pack, fh, ensure_ascii=False, separators=(",", ":"))

    with open(os.path.join(DATA, "index.json"), "w", encoding="utf-8") as fh:
        json.dump(
            {"packSize": TOWERS_PER_PACK, "towers": index},
            fh,
            ensure_ascii=False,
            separators=(",", ":"),
        )

    print(f"\ncelkem {len(index)} věží v {len(packs)} balíčcích -> {DATA}")


if __name__ == "__main__":
    main()
