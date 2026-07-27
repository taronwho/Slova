"""Krok 5e — rozdělení základních tvarů na slabiky.

Slabikování češtiny má okraje, kde se neshodnou ani učebnice: „se-stra"
i „ses-tra" se dají obhájit. Hra si proto **nevybírá** — bere jen slova,
u kterých je dělení jednoznačné, a zbytek zahodí. Základních tvarů je
pětašedesát tisíc, takže si to může dovolit; špatně rozdělené slovo by hráče
učilo nesmysl.

Postup:

1. Slovo se rozloží na **jednotky**, ne na písmena. „ch" je jedna souhláska
   („po-cho-vat", ne „poc-ho-vat") a dvojhlásky ou/au/eu jedna samohláska.
2. Najdou se **jádra** slabik: samohlásky a slabikotvorné r/l mezi
   souhláskami („vlk", „krk", „bra-tr").
3. Mezi dvěma jádry se rozdělí souhlásková skupina:
   - jedna souhláska -> patří následující slabice (V-CV: „ko-lo"),
   - dvě a víc -> první zůstane vlevo, zbytek jde vpravo (VC-CV: „ok-no"),
     ale **jen když** celá skupina sama není přípustným začátkem slabiky.
     Když je („se-stra" / „ses-tra"), obě dělení se dají obhájit a slovo jde
     pryč.
4. Každá výsledná slabika musí mít tvar, který v češtině dává smysl —
   nepovinný začátek, jádro, nepovinná koda.

Výstup: tools/out/syllables.json  ->  {"slovo": ["ko", "lo"], ...}
"""

import json
import os
import re
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")

VOWELS = set("aáeéěiíoóuúůyý")
DIPHTHONGS = ("ou", "au", "eu")
CONSONANTS = set("bcčdďfghjklmnňpqrřsštťvwxzž")

# Skupiny, kterými česká slabika běžně začíná. Jednotky, ne písmena — „ch"
# je jeden prvek.
ONSETS = {
    ("b",), ("c",), ("č",), ("d",), ("ď",), ("f",), ("g",), ("h",), ("ch",),
    ("j",), ("k",), ("l",), ("m",), ("n",), ("ň",), ("p",), ("r",), ("ř",),
    ("s",), ("š",), ("t",), ("ť",), ("v",), ("z",), ("ž",),
    ("b", "l"), ("b", "r"), ("c", "l"), ("c", "r"), ("č", "l"), ("č", "r"),
    ("d", "l"), ("d", "r"), ("d", "v"), ("f", "l"), ("f", "r"),
    ("g", "l"), ("g", "r"), ("h", "l"), ("h", "r"), ("h", "v"),
    ("ch", "l"), ("ch", "r"), ("ch", "v"),
    ("k", "l"), ("k", "r"), ("k", "v"), ("m", "l"), ("m", "n"), ("m", "r"),
    ("p", "l"), ("p", "r"), ("p", "s"), ("p", "t"),
    ("s", "k"), ("s", "l"), ("s", "m"), ("s", "n"), ("s", "p"), ("s", "t"),
    ("s", "v"), ("š", "k"), ("š", "l"), ("š", "p"), ("š", "t"), ("š", "v"),
    ("t", "l"), ("t", "r"), ("t", "ř"), ("t", "v"),
    ("v", "l"), ("v", "r"), ("z", "l"), ("z", "n"), ("z", "v"),
    ("ž", "l"), ("ž", "r"),
    ("s", "k", "l"), ("s", "k", "r"), ("s", "p", "l"), ("s", "p", "r"),
    ("s", "t", "r"), ("s", "t", "ř"), ("š", "k", "r"), ("š", "t", "r"),
    ("z", "d", "r"), ("z", "l", "o"),
}

# Slabika: nepovinný začátek, jádro, nepovinná koda. Cokoli mimo je podezřelé.
SAFE_SYLLABLE = re.compile(
    r"^[bcčdďfghjklmnňprřsštťvzž]{0,3}"
    r"(?:ou|au|eu|[aáeéěiíoóuúůyý]|[rl])"
    r"[bcčdďfghjklmnňprřsštťvzž]{0,2}$"
)


def units(word: str):
    """Rozloží slovo na jednotky. Vrátí None, když narazí na cizí znak."""
    out = []
    i = 0
    while i < len(word):
        pair = word[i : i + 2]
        if pair == "ch":
            out.append(("ch", "C"))
            i += 2
        elif pair in DIPHTHONGS:
            out.append((pair, "V"))
            i += 2
        elif word[i] in VOWELS:
            out.append((word[i], "V"))
            i += 1
        elif word[i] in CONSONANTS:
            out.append((word[i], "C"))
            i += 1
        else:
            return None
    return out


def nuclei(parts):
    """Indexy jednotek, které nesou slabiku."""
    found = []
    for i, (text, kind) in enumerate(parts):
        if kind == "V":
            found.append(i)
            continue
        # Slabikotvorné r/l: souhláska vlevo a vpravo souhláska nebo konec.
        if text in ("r", "l") and i > 0 and parts[i - 1][1] == "C":
            if i + 1 == len(parts) or parts[i + 1][1] == "C":
                found.append(i)
    return found


def split_word(word: str):
    """Rozdělí slovo na slabiky, nebo vrátí None, když je dělení sporné."""
    parts = units(word)
    if parts is None:
        return None
    cores = nuclei(parts)
    if len(cores) < 2:
        return None

    onset = tuple(text for text, _ in parts[: cores[0]])
    if onset and onset not in ONSETS:
        return None

    cuts = [0]
    for left, right in zip(cores, cores[1:]):
        cluster = tuple(text for text, _ in parts[left + 1 : right])
        if not cluster:
            # Dvě jádra vedle sebe („na-u-čit") — hranice je sice jasná, ale
            # výslovnost sporná.
            return None
        if len(cluster) == 1:
            cut = left + 1
        else:
            # Celá skupina je přípustný začátek -> obě dělení se dají obhájit.
            if cluster in ONSETS:
                return None
            if cluster[1:] not in ONSETS:
                return None
            cut = left + 2
        cuts.append(cut)
    cuts.append(len(parts))

    out = ["".join(text for text, _ in parts[a:b]) for a, b in zip(cuts, cuts[1:])]
    if any(not piece for piece in out):
        return None
    if not all(SAFE_SYLLABLE.match(piece) for piece in out):
        return None
    if "".join(out) != word:
        return None
    return out


def fold(word: str) -> str:
    out = unicodedata.normalize("NFD", word.lower())
    return "".join(ch for ch in out if unicodedata.category(ch) != "Mn")


def main():
    base = json.load(open(os.path.join(OUT, "lexicon_base.json"), encoding="utf-8"))
    words = {}
    for length in base:
        for word, freq in base[length]:
            words[word] = freq

    split = {}
    dropped = 0
    for word in sorted(words):
        parts = split_word(word)
        if parts is None:
            dropped += 1
            continue
        split[word] = parts

    path = os.path.join(OUT, "syllables.json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(split, fh, ensure_ascii=False)

    counts = {}
    for parts in split.values():
        counts[len(parts)] = counts.get(len(parts), 0) + 1
    print(f"rozdělených slov: {len(split)}  (zahozeno {dropped})")
    for n in sorted(counts):
        print(f"  {n} slabiky: {counts[n]}")
    uniq = {s for parts in split.values() for s in parts}
    print(f"různých slabik: {len(uniq)}")
    print(f"\n-> {os.path.normpath(path)}")


if __name__ == "__main__":
    main()
