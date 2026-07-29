"""Krok 8 — citáty pro režim Citát.

Zdrojem jsou české Wikicitáty (CC BY-SA), stažené jako dump. Bere se
z nich text výroku, autor (název stránky), jeho zařazení z úvodní věty
a jméno souboru s podobiznou, pokud ho stránka má.

Obrázek se **neukládá**, ukládá se jen jméno souboru — adresa se z něj
poskládá až v aplikaci. Wikimedia Commons drží stálou adresu
`Special:FilePath/<soubor>`, takže se nemusí nic stahovat ani ověřovat.

Spouští se ručně:
    curl -o tools/raw/cswikiquote.xml.bz2 \
      https://dumps.wikimedia.org/cswikiquote/latest/cswikiquote-latest-pages-articles.xml.bz2
    python3 tools/8_build_quotes.py
"""

import bz2
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
DUMP = os.path.join(HERE, "raw", "cswikiquote.xml.bz2")
OUT = os.path.join(HERE, "..", "public", "data", "quotes")

# Kolik slov citát unese. Pod pět je to heslo, ne výrok; nad čtrnáct se
# políčka na telefon nevejdou a hádání se protáhne.
MIN_WORDS, MAX_WORDS = 5, 14
MIN_LEN, MAX_LEN = 30, 110

# Zařazení autora podle kategorií stránky. Pořadí rozhoduje — kdo je herec
# i spisovatel, spadne k tomu, co je uvedené dřív.
TOPICS = [
    ("spisovatele", ("Spisovatelé", "Básníci", "Dramatici")),
    ("mysleni", ("Filozofové", "Vědci", "Matematici", "Fyzici", "Psychologové")),
    ("politici", ("Politici", "Panovníci", "Vojevůdci", "Prezidenti")),
    ("herci", ("Herci", "Hudebníci", "Režiséři", "Zpěváci", "Komici")),
]


def clean(text: str) -> str:
    text = re.sub(r"<ref[^>]*/>|<ref.*?</ref>|<!--.*?-->", "", text, flags=re.S)
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"\{\{[^{}]*\}\}", "", text)
    text = re.sub(r"\[\[([^\]|]*\|)?([^\]]*)\]\]", r"\2", text)
    text = text.replace("''", "").replace("&quot;", '"').replace("&amp;", "&")
    text = text.replace("&nbsp;", " ").replace("\u00a0", " ")
    return re.sub(r"\s+", " ", text).strip()


def intro(body: str) -> str | None:
    """Zařazení autora z úvodní věty — „byl český spisovatel a novinář"."""
    first = clean(re.split(r"\n==", body)[0])
    said = re.search(r"\b(?:byl|byla|je|jsou)\s+([^.;]{6,70})", first)
    if not said:
        return None
    note = said.group(1).strip(" ,;")
    # Delší výčty se seknou na první spojce, ať se vejdou do nápovědy.
    note = re.split(r",| a zároveň ", note)[0].strip()
    return note if 6 <= len(note) <= 60 else None


def main() -> int:
    with bz2.open(DUMP, "rt", encoding="utf-8") as handle:
        dump = handle.read()

    quotes = []
    seen = set()
    for title, body in re.findall(r"<title>(.*?)</title>.*?<text[^>]*>(.*?)</text>", dump, re.S):
        if ":" in title or body[:40].upper().startswith("#REDIRECT"):
            continue
        if not re.search(r"\[\[Kategorie:Osoby od", body):
            continue
        note = intro(body)
        art = re.search(r"\[\[Soubor:([^\]|]+)", body)
        for line in re.findall(r"^\*\s*(?!\*)([^\n]+)$", body, re.M):
            said = clean(line)
            # Za pomlčkou bývá překlad nebo poznámka, do hádanky nepatří.
            said = re.split(r" [-–—] ", said)[0].strip()
            # „Limonádový Joe: Noci jsou tu chladné?" — jméno mluvčího před
            # dvojtečkou je značka scénáře, ne část výroku.
            said = re.sub(r"^[A-ZÁ-Ž][^:]{1,28}:\s+", "", said)
            if said[-1:] not in ".!?" or re.search(r"[|=\[\]{}<>]", said):
                continue
            if not (MIN_LEN <= len(said) <= MAX_LEN):
                continue
            if not (MIN_WORDS <= len(said.split()) <= MAX_WORDS):
                continue
            key = said.lower()
            if key in seen:
                continue
            seen.add(key)
            topic = next(
                (name for name, marks in TOPICS
                 if any(f"[[Kategorie:{m}" in body for m in marks)),
                "osobnosti",
            )
            row = {"id": "", "text": said, "who": title, "topic": topic}
            if note:
                row["note"] = note
            if art:
                row["art"] = art.group(1).strip().replace(" ", "_")
            quotes.append(row)

    # Obtížnost podle délky: krátký výrok má míň písmen k odkrytí a hádá se
    # z něj hůř, ale zase je rychleji hotový — rozhoduje počet slov.
    quotes.sort(key=lambda q: (len(q["text"].split()), q["text"]))
    third = max(1, len(quotes) // 3)
    for i, quote in enumerate(quotes):
        quote["difficulty"] = "easy" if i < third else "normal" if i < 2 * third else "hard"
    quotes.sort(key=lambda q: (q["topic"], q["who"], q["text"]))
    for i, quote in enumerate(quotes):
        quote["id"] = f"q-{i:04d}"

    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, "deck.json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(quotes, fh, ensure_ascii=False)

    print(f"citátů: {len(quotes)}  s podobiznou: {sum(1 for q in quotes if q.get('art'))}"
          f"  se zařazením: {sum(1 for q in quotes if q.get('note'))}")
    for name in ("spisovatele", "mysleni", "politici", "herci", "osobnosti"):
        print(f"  {name}: {sum(1 for q in quotes if q['topic'] == name)}")
    print(f"-> {os.path.normpath(path)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
