#!/usr/bin/env python3
"""Průzkum dumpu české Wikipedie — co se v něm dá použít na Otázku dne.

Pouštět jen ručně. Projde zadaný počet článků a spočítá, jaké infoboxy a jaké
kategorie jsou dost časté na to, aby se z nich dal postavit obor otázek.
"""

import bz2
import re
import sys
from collections import Counter

DUMP = "tools/raw/cswiki.xml.bz2"
LIMIT = int(sys.argv[1]) if len(sys.argv) > 1 else 200_000

TITLE = re.compile(r"<title>(.*?)</title>")
NS = re.compile(r"<ns>(\d+)</ns>")
INFOBOX = re.compile(r"\{\{\s*(Infobox[^|}\n]*)", re.IGNORECASE)
CATEGORY = re.compile(r"\[\[Kategorie:\s*([^\]|]+)")

boxes = Counter()
cats = Counter()
seen = 0

with bz2.open(DUMP, "rt", encoding="utf-8", errors="replace") as f:
    title = None
    ns = None
    body = []
    inside = False
    for line in f:
        if "<title>" in line:
            m = TITLE.search(line)
            title = m.group(1) if m else None
        elif "<ns>" in line:
            m = NS.search(line)
            ns = int(m.group(1)) if m else None
        elif "<text" in line:
            inside = True
            body = [line]
        elif inside:
            body.append(line)
            if "</text>" in line:
                inside = False
                if ns == 0 and title and ":" not in title:
                    text = "".join(body)
                    for m in INFOBOX.finditer(text):
                        boxes[m.group(1).strip().lower()] += 1
                    for m in CATEGORY.finditer(text):
                        cats[m.group(1).strip()] += 1
                    seen += 1
                    if seen >= LIMIT:
                        break
                body = []

print(f"článků: {seen}\n")
print("=== nejčastější infoboxy ===")
for name, n in boxes.most_common(60):
    print(f"{n:6d}  {name}")
print("\n=== nejčastější kategorie ===")
for name, n in cats.most_common(60):
    print(f"{n:6d}  {name}")
