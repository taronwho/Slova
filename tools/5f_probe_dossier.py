#!/usr/bin/env python3
"""
Zkušební vzorek „spisu o slově" — podklad k rozhodnutí, ne součást buildu.

Detektiv dnes stojí na etymologii a naráží na to, že etymologické heslo je
psané pro někoho, kdo hledané slovo **už zná**. Nese jedinou skutečnou
informaci, totiž zdrojový tvar — a ten se před hráčem musí skrýt, takže po
zakrytí zbude gramatická vata.

Tenhle skript zkouší jinou stavbu indicie: místo výkladu původu **spis
o slově** poskládaný z toho, co Wikislovník u hesla vede navíc — slovní
druh, rod či vid, dělení na slabiky, příbuzná slova, a teprve jako poslední
řádek význam.

Význam se schválně **zkracuje na nadřazený pojem**. Slovníková definice je
psaná tak, aby slovo jednoznačně určila („věž vyzařující rotující světelný
kužel, který varuje projíždějící lodě"), což je přesný opak hádanky. Bere se
z ní proto jen ta obecnější část a podrobnosti, které by odpověď naservírovaly,
se zahazují.

Spouští se ručně:  python3 tools/5f_probe_dossier.py
"""

import json
import os
import re
import sys
import urllib.parse
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
_detective = __import__("5d_build_detective")
fold, mask = _detective.fold, _detective.mask

API = "https://cs.wiktionary.org/w/api.php"
# Hlavička se posílá jako latin-1, takže bez diakritiky.
AGENT = "SlovaBot/1.0 (https://taronwho.github.io/Slova/; game mode research)"
DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "public", "data")


def entries(titles: list[str]) -> dict[str, str]:
    """Stáhne zdrojový text hesel. Dvacet naráz, víc API nepustí."""
    out: dict[str, str] = {}
    for start in range(0, len(titles), 20):
        query = urllib.parse.urlencode(
            {
                "action": "query",
                "prop": "revisions",
                "rvprop": "content",
                "rvslots": "main",
                "titles": "|".join(titles[start:start + 20]),
                "format": "json",
                "formatversion": "2",
            }
        )
        request = urllib.request.Request(f"{API}?{query}", headers={"User-Agent": AGENT})
        with urllib.request.urlopen(request, timeout=60) as response:
            page_data = json.load(response)
        for page in page_data.get("query", {}).get("pages", []):
            revisions = page.get("revisions")
            if revisions:
                out[page["title"]] = revisions[0]["slots"]["main"]["content"]
    return out


def plain(text: str) -> str:
    """Ze zdrojového textu čitelnou větu."""
    # Poznámky pod čarou nesou celé odstavce ze slovníků — do hádanky nepatří.
    text = re.sub(r"<ref[^>]*>.*?</ref>", "", text, flags=re.S | re.I)
    text = re.sub(r"<ref[^>]*/?>", "", text, flags=re.I)
    text = re.sub(r"\{\{[^{}]*\}\}", "", text)
    text = re.sub(r"\[\[([^\]|]*\|)?([^\]]*)\]\]", r"\2", text)
    text = re.sub(r"'{2,}", "", text)
    return re.sub(r"\s+", " ", text).strip(" *#:;")


def section(text: str, name: str) -> str | None:
    found = re.search(rf"===+\s*{name}[^=]*===+(.*?)(?====|\Z)", text, re.I | re.S)
    return found.group(1) if found else None


def word_class(text: str) -> str | None:
    """Slovní druh i s rodem nebo videm — základ celého spisu."""
    head = re.search(
        r"===\s*(podstatné jméno|přídavné jméno|sloveso|příslovce)\s*===(.{0,220})",
        text,
        re.I | re.S,
    )
    if not head:
        return None
    kind = head.group(1).lower()
    detail = plain(head.group(2))
    for mark in (
        "rod mužský neživotný", "rod mužský životný", "rod ženský", "rod střední",
        "nedokonavé", "dokonavé",
    ):
        if mark in detail:
            return f"{kind}, {mark}"
    return kind


def syllables(text: str) -> str | None:
    body = section(text, "dělení")
    if not body:
        return None
    first = plain(body).split()
    return first[0] if first and "-" in first[0] else None


def meanings(text: str) -> list[str]:
    body = section(text, "význam")
    if not body:
        return []
    out = []
    for line in body.splitlines():
        if line.strip().startswith("#") and not line.strip().startswith("#:"):
            said = plain(line)
            if len(said) > 8:
                out.append(said)
    return out


# Kde končí obecná část definice a začíná to, co odpověď prozradí.
# „ochranný předmět pokládaný pod něco" je hádanka, „věž vyzařující rotující
# světelný kužel, který varuje projíždějící lodě" je odpověď opsaná jinými slovy.
CUT = re.compile(r"\s*(?:,|;|\bkterý\b|\bkterá\b|\bkteré\b|\bjenž\b|\bsloužící\b|\burčený\b)")


def blur(sentence: str) -> str:
    """Zkrátí význam na obecnou část, aby zůstal vodítkem, ne odpovědí."""
    cut = CUT.split(sentence, maxsplit=1)[0].strip()
    return cut if len(cut) >= 12 else sentence


def dossier(word: str, text: str) -> dict | None:
    lines = []
    kind = word_class(text)
    if kind:
        lines.append(kind)
    split = syllables(text)
    if split:
        lines.append(f"{len(split.split('-'))} slabiky")
    sense = meanings(text)
    if not sense:
        return None
    short = blur(sense[0])
    origin = section(text, "etymologie")
    row = {
        "word": word,
        "mluvnice": " · ".join(lines) if lines else None,
        "vyznam_plny": sense[0],
        "vyznam_zkraceny": short,
        "pocet_vyznamu": len(sense),
        "puvod": plain(origin)[:150] if origin else None,
    }
    # Maskování ano, ale délkový limit ne: čtyřicet dva znaků je pravidlo
    # z etymologických textů. Ve spisu nese délku mluvnice a význam smí být
    # klidně dvouslovný — „nenasytný člověk" je přesně ta míra, kdy indicie
    # navádí, ale nedaruje.
    # Původ do indicie nejde. Prodlužuje ji a je to zpátky ta past, kvůli
    # které se celý režim předělává — u čivavy stačí „podle mexického státu
    # Chihuahua" a je po hádance.
    clue = short
    hidden, _ = mask(word, clue)
    row["po_zakryti"] = hidden
    row["pouzitelne"] = (
        len(hidden.replace("[?]", "").strip()) >= 12 and hidden.count("[?]") <= 1
    )
    return row


def main() -> int:
    puzzles = json.load(
        open(os.path.join(DATA, "detective", "puzzles.json"), encoding="utf-8")
    )
    # Ze střední a těžké police — na běžných slovech není co posuzovat.
    pool = [p["word"] for p in puzzles if p["difficulty"] in ("normal", "hard")]
    sample = pool[:: max(1, len(pool) // 40)][:40]

    print(f"Stahuji {len(sample)} hesel…\n")
    texts = entries(sample)
    shown = 0
    for word in sample:
        text = texts.get(word)
        if not text:
            continue
        row = dossier(word, text)
        if not row:
            continue
        shown += 1
        print(f"=== {row['word'].upper()}  ({len(row['word'])} písmen)")
        if row["mluvnice"]:
            print(f"    {row['mluvnice']}")
        print(f"    indicie:  {row['po_zakryti']}")
        if row["vyznam_plny"] != row["vyznam_zkraceny"]:
            print(f"    (plná definice: {row['vyznam_plny'][:110]})")
        if not row["pouzitelne"]:
            print("    ! po zakrytí by nezbylo dost — zahodit")
        print()
    print(f"Použitelných hesel: {shown} z {len(sample)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
