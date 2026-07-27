"""Krok 5c — stažení etymologií z Wikislovníku.

Etymologie se **nevymýšlejí**. Berou se z české sekce Wikislovníku, kde jsou
psané lidmi a opatřené odkazy na zdroje (Rejzek, Naše řeč, Ottův slovník).
Skript je jen stáhne, očistí od wikitextu a uloží; posuzování obsahu na sebe
nebere.

Stahuje se po padesáti heslech na dotaz, s pauzou mezi dávkami, a výsledek se
ukládá do `tools/raw/etymology.json`. Ten soubor je cache: druhé spuštění už
sáhne po síti jen pro hesla, která v něm nejsou. Wikislovník je pod licencí
CC BY-SA, což je v README uvedené.

Použití:
    python3 tools/5c_fetch_etymology.py            # doplní, co chybí
    python3 tools/5c_fetch_etymology.py --limit 500
"""

import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
RAW = os.path.join(HERE, "raw")
CACHE = os.path.join(RAW, "etymology.json")

API = "https://cs.wiktionary.org/w/api.php"
# Hlavičky se posílají v latin-1, takže tady žádná diakritika.
AGENT = "SlovaWordGame/1.0 (https://github.com/taronwho/Slova; etymology collection)"
BATCH = 50
PAUSE = 0.4

# Kandidáti: běžná slova rozumné délky. Krátká slova mají etymologii zřídka.
# Horní hranice sahá až ke čtrnácti písmenům schválně — právě u dlouhých
# přejatých slov („demokracie", „gramofon") mívá Wikislovník etymologii
# nejčastěji, a bez nich by hádanek bylo o třetinu míň.
MIN_LEN, MAX_LEN = 4, 14
CANDIDATES = 100000


def fetch(titles):
    query = urllib.parse.urlencode(
        {
            "action": "query",
            "prop": "revisions",
            "rvprop": "content",
            "rvslots": "main",
            "format": "json",
            "formatversion": "2",
            "titles": "|".join(titles),
        }
    )
    request = urllib.request.Request(f"{API}?{query}", headers={"User-Agent": AGENT})
    with urllib.request.urlopen(request, timeout=60) as response:
        return json.load(response)


def czech_section(text):
    """Jen část hesla pod `== čeština ==` — jinde jsou cizí jazyky."""
    match = re.search(r"^==\s*čeština\s*==\s*$", text, re.M)
    if not match:
        return None
    rest = text[match.end() :]
    end = re.search(r"^==\s*[^=].*==\s*$", rest, re.M)
    return rest[: end.start()] if end else rest


def etymology_section(text):
    match = re.search(r"^===\s*etymologie\s*===\s*$", text, re.M)
    if not match:
        return None
    rest = text[match.end() :]
    end = re.search(r"^==+\s*[^=].*==+\s*$", rest, re.M)
    return rest[: end.start()] if end else rest


# Slovní druhy, které se ve hře hodí hádat. Částice a spojky sice etymologii
# mívají, ale „Ze spojení jest-li" není hádanka.
POS_HEADINGS = {
    "podstatné jméno": "noun",
    "přídavné jméno": "adj",
    "sloveso": "verb",
    "příslovce": "adv",
}


def parts_of_speech(czech):
    found = []
    for heading, code in POS_HEADINGS.items():
        if re.search(rf"^===\s*{heading}\s*===\s*$", czech, re.M):
            found.append(code)
    return found


def strip_templates(text):
    """Odstraní {{...}} včetně vnořených — v etymologii jsou to samé citace."""
    out = []
    depth = 0
    i = 0
    while i < len(text):
        if text.startswith("{{", i):
            depth += 1
            i += 2
        elif text.startswith("}}", i):
            depth = max(0, depth - 1)
            i += 2
        else:
            if depth == 0:
                out.append(text[i])
            i += 1
    return "".join(out)


def clean(text):
    text = re.sub(r"<ref[^>]*/>", "", text)
    text = re.sub(r"<ref.*?</ref>", "", text, flags=re.S)
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    text = strip_templates(text)
    text = re.sub(r"<[^>]+>", "", text)
    # [[heslo|zobrazený text]] -> zobrazený text
    text = re.sub(r"\[\[[^\]|]*\|([^\]]*)\]\]", r"\1", text)
    text = re.sub(r"\[\[([^\]]*)\]\]", r"\1", text)
    text = re.sub(r"'{2,}", "", text)
    text = text.replace("&nbsp;", " ")
    text = re.sub(r"^[*#:;]+\s*", "", text, flags=re.M)
    text = re.sub(r"\s+", " ", text).strip()
    # Osamocená interpunkce po vyhozených citacích
    text = re.sub(r"\s+([,.;])", r"\1", text)
    text = re.sub(r"\(\s*\)", "", text)
    return text.strip()


def main():
    limit = None
    if "--limit" in sys.argv:
        limit = int(sys.argv[sys.argv.index("--limit") + 1])

    base = json.load(open(os.path.join(OUT, "lexicon_base.json"), encoding="utf-8"))
    pool = []
    for length in sorted(base, key=int):
        if MIN_LEN <= int(length) <= MAX_LEN:
            pool.extend(base[length])
    pool.sort(key=lambda wf: (-wf[1], wf[0]))
    words = [w for w, _ in pool[:CANDIDATES]]
    if limit:
        words = words[:limit]

    os.makedirs(RAW, exist_ok=True)
    cache = {}
    if os.path.exists(CACHE):
        cache = json.load(open(CACHE, encoding="utf-8"))

    todo = [w for w in words if w not in cache]
    print(f"kandidátů: {len(words)}, v cache: {len(words) - len(todo)}, ke stažení: {len(todo)}")

    for start in range(0, len(todo), BATCH):
        chunk = todo[start : start + BATCH]
        try:
            data = fetch(chunk)
        except Exception as cause:  # síť občas selže; zbytek se dotáhne příště
            print(f"  chyba u dávky {start // BATCH}: {cause}")
            time.sleep(3)
            continue

        for page in data.get("query", {}).get("pages", []):
            title = page.get("title")
            if "revisions" not in page:
                cache[title] = None
                continue
            text = page["revisions"][0]["slots"]["main"]["content"]
            czech = czech_section(text)
            section = etymology_section(czech) if czech else None
            if not section:
                cache[title] = None
                continue
            cache[title] = {"e": clean(section), "pos": parts_of_speech(czech)}

        # Hesla, která API vůbec nevrátilo (neexistují), ať se nezkoušejí znovu
        for word in chunk:
            cache.setdefault(word, None)

        done = start + len(chunk)
        found = sum(1 for w in todo[:done] if cache.get(w))
        print(f"  {done}/{len(todo)}  s etymologií: {found}")
        with open(CACHE, "w", encoding="utf-8") as fh:
            json.dump(cache, fh, ensure_ascii=False)
        time.sleep(PAUSE)

    have = [w for w in words if cache.get(w)]
    print(f"\nhotovo: {len(have)} slov s etymologií z {len(words)} -> {os.path.normpath(CACHE)}")


if __name__ == "__main__":
    main()
