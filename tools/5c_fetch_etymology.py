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


HEADING = re.compile(r"^(={2,6})[ \t]*(.+?)[ \t]*\1[ \t]*$", re.M)


def sections(text):
    """
    Rozloží wikitext na `(úroveň, nadpis, tělo)`.

    Dřív se každá část hledala vlastním regulárním výrazem s pevným počtem
    rovnítek a to se rozbíjelo: „význam" je zanořený pod slovním druhem, takže
    má o jedno rovnítko víc než „etymologie". Jednou projít nadpisy je
    spolehlivější než hádat úroveň dopředu.
    """
    marks = list(HEADING.finditer(text))
    out = []
    for order, mark in enumerate(marks):
        stop = marks[order + 1].start() if order + 1 < len(marks) else len(text)
        out.append((len(mark.group(1)), mark.group(2).strip().lower(), text[mark.end():stop]))
    return out


def czech_section(text):
    """Jen část hesla pod `== čeština ==` — jinde jsou cizí jazyky."""
    marks = list(HEADING.finditer(text))
    for order, mark in enumerate(marks):
        if len(mark.group(1)) == 2 and mark.group(2).strip().lower() == "čeština":
            for later in marks[order + 1:]:
                if len(later.group(1)) == 2:
                    return text[mark.end():later.start()]
            return text[mark.end():]
    return None


def etymology_section(czech):
    for _, title, body in sections(czech):
        if title == "etymologie":
            return body
    return None


# Slovní druhy, které se ve hře hodí hádat. Částice a spojky sice etymologii
# mívají, ale „Ze spojení jest-li" není hádanka.
POS_HEADINGS = {
    "podstatné jméno": "noun",
    "přídavné jméno": "adj",
    "sloveso": "verb",
    "příslovce": "adv",
}


# Rod a vid stojí v těle sekce slovního druhu jako kurzivní odrážka.
MARKS = (
    "rod mužský neživotný", "rod mužský životný", "rod ženský", "rod střední",
    "nedokonavé", "dokonavé",
)


def senses(body):
    """Řádky významu z těla sekce `význam`."""
    out = []
    for line in body.splitlines():
        stripped = line.strip()
        # „#" je význam, „#:" a „#*" je příklad užití — ten do hádanky nepatří.
        if stripped.startswith("#") and not re.match(r"^#[:*]", stripped):
            said = clean(stripped)
            if len(said) > 8:
                out.append(said)
    return out


def meaning_section(czech):
    """
    Významy hesla — z nich se skládá hlavní část indicie.

    Etymologie je vzácná (má ji sotva každé dvacáté heslo) a po zakrytí
    zdrojového tvaru z ní často nic nezbude. Význam má naopak skoro každé
    heslo a nikdy neobsahuje popisované slovo, protože se tak slovníky
    prostě nepíšou. Proto se od téhle verze stahuje obojí.

    Bere se význam u prvního slovního druhu, který hru zajímá. Hesla jako
    „jeden" nesou vedle číslovky i zájmeno a míchat jejich definice by dalo
    nesourodou indicii.
    """
    wanted, spare = [], []
    kind = None
    for level, title, body in sections(czech):
        if title in POS_HEADINGS:
            kind = title
        elif level <= 3:
            kind = None
        if title == "význam":
            (wanted if kind else spare).append(senses(body))
    for group in wanted + spare:
        if group:
            return group
    return []


def grammar(czech):
    """Slovní druh s rodem či videm a dělení na slabiky."""
    out = {}
    for _, title, body in sections(czech):
        if title in POS_HEADINGS:
            detail = clean(body[:400])
            out["kind"] = next(
                (f"{title}, {mark}" for mark in MARKS if mark in detail), title
            )
            break
    for _, title, body in sections(czech):
        if title == "dělení":
            first = clean(body).split()
            if first and "-" in first[0]:
                out["syl"] = first[0]
            break
    return out


def parts_of_speech(czech):
    return list(dict.fromkeys(POS_HEADINGS[t] for _, t, _ in sections(czech) if t in POS_HEADINGS))


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

    lexicon = os.path.join(OUT, "lexicon_base.json")
    if os.path.exists(lexicon):
        base = json.load(open(lexicon, encoding="utf-8"))
        pool = []
        for length in sorted(base, key=int):
            if MIN_LEN <= int(length) <= MAX_LEN:
                pool.extend(base[length])
        pool.sort(key=lambda wf: (-wf[1], wf[0]))
        words = [w for w, _ in pool[:CANDIDATES]]
    else:
        # Bez mezivýstupů z kroku 2 se vezme ověřený seznam základních tvarů,
        # který drží testy. Pořadí podle frekvence, aby se běžná slova
        # stahovala dřív a přerušený běh měl použitelný začátek.
        forms = json.load(
            open(os.path.join(HERE, "..", "tests", "fixtures", "base-forms.json"),
                 encoding="utf-8")
        )
        ranks = {}
        freq = os.path.join(RAW, "cs_50k.txt")
        if os.path.exists(freq):
            for order, line in enumerate(open(freq, encoding="utf-8")):
                parts = line.split()
                if parts:
                    ranks.setdefault(parts[0], order)
        words = sorted(
            (w for w in forms if MIN_LEN <= len(w) <= MAX_LEN),
            key=lambda w: (ranks.get(w, len(ranks) + 1), w),
        )[:CANDIDATES]
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
            if not czech:
                cache[title] = None
                continue
            section = etymology_section(czech)
            senses = meaning_section(czech)
            # Heslo je k něčemu, když má aspoň jedno z obojího.
            if not section and not senses:
                cache[title] = None
                continue
            entry = {"pos": parts_of_speech(czech), **grammar(czech)}
            if section:
                entry["e"] = clean(section)
            if senses:
                entry["v"] = senses
            cache[title] = entry

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
