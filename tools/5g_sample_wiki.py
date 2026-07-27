#!/usr/bin/env python3
"""Vytáhne z dumpu pár ukázek zadaných infoboxů, ať je vidět, jaká nesou pole."""

import bz2
import re
import sys
from collections import defaultdict

DUMP = "tools/raw/cswiki.xml.bz2"
WANT = [w.lower() for w in sys.argv[1:]] or ["osoba"]
PER = 3
LIMIT = 120_000

TITLE = re.compile(r"<title>(.*?)</title>")
NS = re.compile(r"<ns>(\d+)</ns>")


def infobox(text: str, name: str):
    """Vrátí tělo infoboxu daného jména, se správně spárovanými závorkami."""
    start = text.lower().find("{{infobox - " + name)
    if start < 0:
        return None
    depth = 0
    i = start
    while i < len(text) - 1:
        if text[i : i + 2] == "{{":
            depth += 1
            i += 2
        elif text[i : i + 2] == "}}":
            depth -= 1
            i += 2
            if depth == 0:
                return text[start:i]
        else:
            i += 1
    return None


found = defaultdict(list)
seen = 0

with bz2.open(DUMP, "rt", encoding="utf-8", errors="replace") as f:
    title, ns, body, inside = None, None, [], False
    for line in f:
        if "<title>" in line:
            m = TITLE.search(line)
            title = m.group(1) if m else None
        elif "<ns>" in line:
            m = NS.search(line)
            ns = int(m.group(1)) if m else None
        elif "<text" in line:
            inside, body = True, [line]
        elif inside:
            body.append(line)
            if "</text>" in line:
                inside = False
                if ns == 0 and title and ":" not in title:
                    text = "".join(body)
                    low = text.lower()
                    for want in WANT:
                        if len(found[want]) < PER and "{{infobox - " + want in low:
                            box = infobox(text, want)
                            if box:
                                found[want].append((title, box))
                    seen += 1
                    if seen >= LIMIT or all(len(found[w]) >= PER for w in WANT):
                        break
                body = []

for want in WANT:
    print(f"\n{'=' * 70}\n### {want}\n{'=' * 70}")
    for title, box in found[want]:
        print(f"\n--- {title} ---")
        print(box[:1800])
