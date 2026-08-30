"""Krok 4 — generátor hádanek pro režim VOŠTINA.

Plástev se odvozuje od pangramu: vezme se slovo, jehož složený tvar (bez
diakritiky) obsahuje přesně sedm různých písmen — ta tvoří plástev. Pro každé
z nich jako povinný střed se pak spočítá kompletní množina řešení.

Řešitelnost je tím garantovaná konstrukcí: hádanka se do hry dostane jen když
má pangram a dost slov, a její seznam řešení je uložený celý.
"""

import glob
import json
import os
import random

OUT = os.path.join(os.path.dirname(__file__), "out")
DATA = os.path.join(os.path.dirname(__file__), "..", "public", "data", "hive")

# Lexikon omezený na základní tvary (krok 2b).
LEXICON = "lexicon_base.json"

FOLD = str.maketrans("áčďéěíňóřšťúůýž", "acdeeinorstuuyz")

MIN_LEN = 4
MAX_LEN = 9

# Delší slova se do cíle nedávají — plástev by měla mít řešení, na která se
# dá přijít —, ale **uznat se musí**. Hráč nahlásil, že Voština nezná slova,
# která zná: „lysiny" byly pod hranicí frekvence, „vyvýšeniny" nad devíti
# písmeny. Odmítnout slovo, které existuje a do plástve se vejde, je horší
# než ho uznat bez nároku na cíl.
MAX_LEN_UZNAT = 14
# Do řešení pustíme jen slova, která má hráč šanci znát.
SOLUTION_MIN_FREQ = 25
# Pangram musí být opravdu běžné slovo, jinak je hádanka frustrující.
PANGRAM_MIN_FREQ = 150

MIN_SOLUTIONS = 22
MAX_SOLUTIONS = 90
# Kolik slov v hádance musí být opravdu běžných, aby šla rozehrát.
MIN_EASY_WORDS = 10
EASY_FREQ = 800

HIVES_PER_PACK = 40
# Dělí se na třetiny, takže cíl je násobek tří: 834 na každou obtížnost.
TARGET_HIVES = 2502


def fold(word: str) -> str:
    return word.translate(FOLD)


def mask_of(folded: str) -> int:
    mask = 0
    for ch in folded:
        bit = ord(ch) - 97
        if bit < 0 or bit > 25:
            return -1
        mask |= 1 << bit
    return mask


def popcount(mask: int) -> int:
    return bin(mask).count("1")


def submasks(mask: int):
    sub = mask
    while True:
        yield sub
        if sub == 0:
            break
        sub = (sub - 1) & mask


def otisk(hive) -> str:
    """Id plástve odvozené z jejích písmen, ne z pořadí v sadě.

    Pořadová čísla (`h-0000`) se při každém přestavění dat přeházejí, takže
    tentýž identifikátor ukazoval po novém sestavení na jinou plástev.
    U Vetřelce to rozbilo souboje — dva telefony s různou verzí hry si pod
    týmž číslem našly jinou hádanku. Sedm písmen plástev určuje jednoznačně
    a nikam se nehnou.
    """
    return "h-" + hive["center"] + "".join(sorted(hive["outer"]))


def main():
    random.seed(20260724)
    os.makedirs(DATA, exist_ok=True)
    # Staré balíčky je nutné smazat — když jich nová sada vyrobí míň, osiřelý
    # soubor by zůstal ležet a index by mu neodpovídal.
    for stale in glob.glob(os.path.join(DATA, "pack-*.json")):
        os.remove(stale)
    lexicon = json.load(open(os.path.join(OUT, LEXICON), encoding="utf-8"))

    by_mask: dict[int, list[tuple[str, int]]] = {}
    # Slova, která pravidlům vyhovují, jen je skoro nikdo nepíše. Do cíle se
    # nepočítají, ale plástev je uzná — viz `extra` v HivePuzzle.
    extra_mask: dict[int, list[str]] = {}
    pangram_candidates: dict[int, list[tuple[str, int]]] = {}

    for length in range(MIN_LEN, MAX_LEN_UZNAT + 1):
        for word, freq in lexicon.get(str(length), []):
            if any(word[i] == word[i + 1] == word[i + 2] for i in range(len(word) - 2)):
                continue  # citoslovce typu „brrr"
            mask = mask_of(fold(word))
            if mask == -1:
                continue
            if freq < SOLUTION_MIN_FREQ or length > MAX_LEN:
                extra_mask.setdefault(mask, []).append(word)
                continue
            by_mask.setdefault(mask, []).append((word, freq))
            if popcount(mask) == 7 and freq >= PANGRAM_MIN_FREQ:
                pangram_candidates.setdefault(mask, []).append((word, freq))

    print(f"masek se slovy: {len(by_mask)}")
    print(f"kandidátů na plástev: {len(pangram_candidates)}")

    hives = []
    for hive_mask, pangrams in pangram_candidates.items():
        # Všechna slova, která se do plástve vejdou, seskupená podle písmene.
        pool: list[tuple[str, int, int]] = []
        for sub in submasks(hive_mask):
            for word, freq in by_mask.get(sub, []):
                pool.append((word, freq, sub))

        for bit in range(26):
            if not (hive_mask >> bit) & 1:
                continue
            center = chr(97 + bit)
            solutions = [(w, f) for w, f, m in pool if (m >> bit) & 1]
            if not (MIN_SOLUTIONS <= len(solutions) <= MAX_SOLUTIONS):
                continue
            easy = sum(1 for _, f in solutions if f >= EASY_FREQ)
            if easy < MIN_EASY_WORDS:
                continue
            hive_pangrams = [w for w, _ in solutions if mask_of(fold(w)) == hive_mask]
            if not hive_pangrams:
                continue
            if not any(f >= PANGRAM_MIN_FREQ for w, f in solutions if w in hive_pangrams):
                continue

            words = sorted(w for w, _ in solutions)
            # Vzácná slova, která do plástve taky patří. Hráč je smí napsat
            # a body za ně dostane; cíl „X z Y" o nich neví.
            extra = sorted(
                w
                for sub in submasks(hive_mask)
                if (sub >> bit) & 1
                for w in extra_mask.get(sub, [])
            )
            outer = sorted(chr(97 + b) for b in range(26) if (hive_mask >> b) & 1 and b != bit)
            hives.append(
                {
                    "center": center,
                    "outer": outer,
                    "solutions": words,
                    "extra": extra,
                    "pangrams": sorted(hive_pangrams),
                    "easy": easy,
                }
            )
    print(f"platných pláství: {len(hives)}")

    def difficulty(hive):
        count = len(hive["solutions"])
        if count <= 35:
            return "easy"
        return "normal" if count <= 60 else "hard"

    # Stratifikovaný výběr — ať jsou všechny tři obtížnosti zastoupené,
    # ne jen ty největší plástve, kterých je přirozeně nejvíc.
    buckets: dict[str, list[dict]] = {"easy": [], "normal": [], "hard": []}
    for hive in hives:
        buckets[difficulty(hive)].append(hive)
    print(
        "  k dispozici: "
        + ", ".join(f"{k} {len(v)}" for k, v in buckets.items())
    )

    per_bucket = TARGET_HIVES // 3
    hives = []
    shortfall = 0
    for name in ("easy", "normal", "hard"):
        pool = buckets[name]
        random.shuffle(pool)
        take = pool[: per_bucket + shortfall]
        shortfall = max(0, per_bucket + shortfall - len(take))
        hives.extend(take)
    random.shuffle(hives)

    index = []
    packs: list[list[dict]] = []
    for n, hive in enumerate(hives):
        hive_id = otisk(hive)
        pack_no = n // HIVES_PER_PACK
        while len(packs) <= pack_no:
            packs.append([])
        entry = {
            "id": hive_id,
            "center": hive["center"],
            "outer": hive["outer"],
            "solutions": hive["solutions"],
            "extra": hive["extra"],
            "pangrams": hive["pangrams"],
            "difficulty": difficulty(hive),
        }
        packs[pack_no].append(entry)
        index.append(
            {
                "id": hive_id,
                "pack": pack_no,
                "center": hive["center"],
                "outer": hive["outer"],
                "n": len(hive["solutions"]),
                "difficulty": entry["difficulty"],
            }
        )

    for pack_no, pack in enumerate(packs):
        path = os.path.join(DATA, f"pack-{pack_no:03d}.json")
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(pack, fh, ensure_ascii=False, separators=(",", ":"))

    with open(os.path.join(DATA, "index.json"), "w", encoding="utf-8") as fh:
        json.dump(
            {"packSize": HIVES_PER_PACK, "hives": index},
            fh,
            ensure_ascii=False,
            separators=(",", ":"),
        )

    counts = {}
    for entry in index:
        counts[entry["difficulty"]] = counts.get(entry["difficulty"], 0) + 1
    sizes = sorted(e["n"] for e in index)
    print(f"vyexportováno {len(index)} pláství v {len(packs)} balíčcích")
    print(f"  obtížnost {counts}")
    if sizes:
        print(
            f"  řešení: min {sizes[0]}, medián {sizes[len(sizes) // 2]}, max {sizes[-1]}"
        )


if __name__ == "__main__":
    main()
