#!/usr/bin/env python3
"""
Postaví balík otázek pro Otázku dne z `quiz_bank.py`.

Kromě převodu do JSON dělá hlavně **kontroly**, protože u téhle hry se chyba
v datech nedá zahrát do autu — hráč dostane jednu otázku denně a když je
špatná, má zkažený celý den:

* **Únik odpovědi.** Indicie nesmí obsahovat odpověď ani žádný její alternativní
  tvar, ani ohnutý, ani bez diakritiky. Kdyby ano, hra by se dala vyhrát
  přečtením.
* **Odstupňování** se strojově zkontrolovat nedá a tenhle skript se o to ani
  nepokouší. Zkoušel to přes délku vět a hlásil jen plané poplachy — dlouhá
  věta není těžká indicie. Jestli je první pro znalce a třetí skoro prozradí,
  se pozná jedině přečtením, a je to ta část práce, kterou nejde odbýt.
  Hlídá se jen to, že indicie nejsou útržky o dvou slovech.
* **Vyváženost oborů.** Otázky se hráči podávají kolečkem přes obory, takže
  délka nejmenšího oboru určuje, za kolik dní se první otázka zopakuje.
  Když se obory rozejdou, cyklus se zkrátí — a to je přesně ta věc, kterou by
  si nikdo nevšiml, dokud by na ni nenarazil hráč.
"""

import json
import re
import sys
import unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from quiz_bank import BANK  # noqa: E402

OUT = Path("public/data/quiz/deck.json")

# Musí sedět s QUIZ_TOPICS v src/game/quiz.ts.
TOPICS = [
    "osobnost",
    "zemepis",
    "veda",
    "kultura",
    "historie",
    "priroda",
    "technika",
    "sport",
    "jazyk",
    "spolecnost",
]


def fold(text: str) -> str:
    """Bez diakritiky a bez velkých písmen — tak, jak se odpověď porovnává."""
    stripped = unicodedata.normalize("NFD", text.lower())
    return "".join(c for c in stripped if unicodedata.category(c) != "Mn")


def stem(word: str) -> str:
    """
    Hrubý kmen českého slova.

    Únik se nejčastěji schová v ohnutém tvaru — „Dvořák“ v indicii jako
    „Dvořákova“. Useknutí konce slova to odhalí, aniž by bylo potřeba tahat
    do buildu celý morfologický analyzátor.
    """
    return word[:-2] if len(word) > 6 else word[:-1] if len(word) > 4 else word


# Druhová slova, která odpověď jen zařazují do kategorie.
#
# „Bajkalské **jezero**" nebo „baskický **jazyk**" jsou uznávané tvary
# odpovědi, ale samo slovo nic neprozrazuje — nadpis otázky ho stejně říká
# nahlas. Kdyby se hlídala i tahle slova, kontrola by křičela u poloviny
# otázek a přestala by se číst, což je horší než ji nemít.
GENERIC = {
    "jazyk", "jazyka", "jazyky", "jazyku", "kniha", "knihy", "film", "filmu",
    "jezero", "hora",
    "stat", "statu", "spor", "sporu", "pruplav", "vodopad", "vodopady",
    "stupnice", "system", "vyroba", "pismo", "slovo", "slova", "svatek",
    "ustava", "stadium", "metr", "metru", "metru", "presmycka", "podzemni",
    "aditivni", "cocka", "cocky", "sifra", "mesto", "mesta", "reka", "reky",
    "ostrov", "sopka", "more", "prvek", "slouceniny", "sloucenina", "kyselina",
    "zvire", "strom", "rostlina", "ptak", "ryba", "hmyz", "savec", "houba",
    "hornina", "planeta", "hvezda", "kometa", "organizace", "instituce",
    "dokument", "deklarace", "pojem", "cena", "mena", "tradice", "zvyk",
    "sport", "klub", "trofej", "turnaj", "akce", "disciplina", "obecna",
    "obecny", "obrovsky", "velika", "velky", "velka", "cesky", "ceska",
    "ceske", "narodni", "mezinarodni", "svetovy", "svetova", "prava",
    "pravo", "praci", "prace", "republiky", "republika", "menšina",
    "mensina", "beh", "vynalez", "stroj", "technika", "termin", "jev",
    "abeceda", "rceni", "obdobi", "udalost", "bitva", "valka", "civilizace",
    "panovnik", "vladce", "moreplavec", "stavba", "album", "skupina",
    "kapela", "socha", "obraz", "hra", "serial", "muzikal", "nastroj",
    "malir", "spisovatel", "osobnost", "sportovec", "sportovkyne",
    "fotbalista", "videohra", "letadlo", "auto", "znacka", "lecivo",
    "jednotka", "teorie", "objev", "organ", "teleso", "poust", "vrchol",
    "pisma", "konference", "listina", "listiny", "svobod", "vlast",
    "mineral", "migrace", "vynalez", "objeveni", "dynastie", "rise",
    "most", "prehrada", "nadraz", "vez", "zamek", "hrad",
}


def leaks(answer: str, clue: str) -> str | None:
    """
    Vrátí uniklé slovo, pokud se odpověď dá z indicie vyčíst.

    Porovnává se přes hrubý kmen a bez diakritiky, aby prošel i ohnutý tvar
    („Dvořákova“ prozrazuje Dvořáka stejně jako „Dvořák“).
    """
    words = [
        w
        for w in re.split(r"[^a-z0-9]+", fold(answer))
        if len(w) >= 4 and w not in GENERIC
    ]
    # Porovnává se po slovech, ne přes celý řetězec. Podřetězec hlásil plané
    # poplachy — „Vídeň" se schová uvnitř slova „pravidelně" a taková hláška
    # kontrolu jen znevěrohodní.
    hay = [w for w in re.split(r"[^a-z0-9]+", fold(clue)) if w]
    for word in words:
        root = stem(word)
        if root and any(w.startswith(root) for w in hay):
            return word
    return None


# Slova, kterými se v češtině říká „tohle je na světě jediné svého druhu".
#
# V první indicii jsou skoro vždycky chybou: superlativ je právě to, co si
# s odpovědí spojí každý, takže „měří 4 000 kilometrů na délku, ale jen 180
# na šířku" prozradí Chile dřív, než dočteš větu. Patří na třetí místo. Build
# je nezakazuje — někdy je superlativ opravdu okrajový („nejnižší tělesná
# teplota ze všech placentálních savců") —, ale vypíše je, aby se dalo projít,
# jestli je každý z nich obhajitelný.
SUPERLATIVES = (
    "nejvyšš", "nejniž", "největš", "nejmenš", "nejdelš", "nejkratš",
    "nejstarš", "nejmladš", "nejrychlej", "nejtěžš", "nejlehč", "nejhlub",
    "nejlidnatě", "nejvodnatě", "nejúspěšně", "nejznámě", "nejbohat",
    "jako jediný", "jako jediná", "jako jediné", "jediný na světě",
    "jediná na světě", "jediné na světě", "první na světě", "na světě první",
)


def superlative(clue: str) -> str | None:
    low = clue.lower()
    for word in SUPERLATIVES:
        if word in low:
            return word
    return None


# Předložky, které z odpovědi dělají spojení dvou podstatných jmen.
PREPOSITIONS = {
    "za", "na", "o", "v", "u", "do", "z", "ze", "pro", "k", "ke", "s", "se",
    "po", "přes", "od", "bez", "při", "mezi", "proti",
}

# Zájmena, kterými indicie ukazuje na něco, co v ní samotné nestojí.
LONE_PRONOUNS = re.compile(
    r"(?<![\wá-ž])(ji|jí|ní|ním|ně|něm|ho|jej|jeho|její|jejím|nich|nimi)(?![\wá-ž])",
    re.IGNORECASE,
)


def dangling(answer: str, clue: str) -> str | None:
    """
    Ukazuje indicie zájmenem na odpověď, která je spojením dvou jmen?

    U odpovědi typu „Odpovědnost za škodu" se v indicii objevilo „Kdo **ji**
    způsobí" — a to už je o škodě, ne o odpovědnosti. Nikdo nezpůsobí
    odpovědnost. Hráč si toho všimne a právem: věta o odpovědi nemluví.

    Zkouška je jednoduchá a dá se udělat i hlavou: **dosaď za zájmeno celou
    odpověď**. „Kdo odpovědnost za škodu způsobí" je nesmysl, „Zvítězil
    v bitvě u Hastingsu" dává smysl. Stroj tenhle rozdíl nepozná — je
    významový, ne tvarový —, takže se sem jen vypíšou k přečtení ty indicie,
    kde takové zájmeno je. U jednoslovné odpovědi se hlásit nemusí: tam
    zájmeno nemá na co jiného ukázat.

    Falešných hlášek je většina a to je v pořádku. Levnější je přečíst
    čtyřicet vět než nechat hráče narazit na jednu, která nedává smysl.
    """
    words = answer.split()
    if len(words) < 2:
        return None
    if not any(word.lower() in PREPOSITIONS for word in words):
        return None
    found = LONE_PRONOUNS.search(clue)
    return found.group(0) if found else None


def main() -> int:
    problems: list[str] = []
    loud: list[str] = []
    vague: list[str] = []
    deck: dict[str, list] = {}
    ids: set[str] = set()

    for topic in TOPICS:
        rows = BANK.get(topic)
        if not rows:
            problems.append(f"obor {topic} je prázdný")
            deck[topic] = []
            continue

        out = []
        # Dvakrát napsaná odpověď se při psaní po stovkách neuhlídá pamětí:
        # dvě různě formulované otázky na Nový Zéland vypadají každá zvlášť
        # v pořádku a chyba se ukáže až hráči, kterému přijde stejná odpověď
        # dvakrát za rok.
        seen_answers: dict[str, int] = {}
        for i, row in enumerate(rows):
            ask, answer, alt, clues = row
            qid = f"{topic}-{i + 1:04d}"
            where = f"{topic} #{i + 1} ({answer})"

            key = fold(answer).strip()
            if key in seen_answers:
                problems.append(
                    f"{where}: stejnou odpověď má už #{seen_answers[key]}"
                )
            else:
                seen_answers[key] = i + 1

            # Rozepsaná poznámka v poli odpovědi. Stalo se to při psaní ve
            # velkém dvakrát a nic jiného to nechytilo — odpověď vypadala
            # věrohodně a s indiciemi se nekřížila.
            if "…" in answer or " tedy " in answer:
                problems.append(f"{where}: odpověď vypadá jako nedopsaná poznámka")

            if len(clues) != 3:
                problems.append(f"{where}: indicií není přesně tři")
                continue
            if qid in ids:
                problems.append(f"{where}: klíč {qid} je dvakrát")
            ids.add(qid)

            for n, clue in enumerate(clues, start=1):
                if len(clue.split()) < 4:
                    problems.append(f"{where}: {n}. indicie je příliš krátká")
                for candidate in [answer, *alt]:
                    hit = leaks(candidate, clue)
                    if hit:
                        problems.append(
                            f"{where}: {n}. indicie prozrazuje odpověď („{hit}“)"
                        )
                        break

            hint = superlative(clues[0])
            if hint:
                loud.append(f"{where}: 1. indicie nese superlativ („{hint}…“)")

            for n, clue in enumerate(clues, start=1):
                word = dangling(answer, clue)
                if word:
                    vague.append(f"{where}: {n}. indicie ukazuje zájmenem („{word}“)")

            entry = {
                "id": qid,
                "topic": topic,
                "ask": ask,
                "clues": list(clues),
                "answer": answer,
            }
            if alt:
                entry["alt"] = list(alt)
            out.append(entry)

        deck[topic] = out

    sizes = {topic: len(deck[topic]) for topic in TOPICS}
    smallest = min(sizes.values())
    cycle = smallest * len(TOPICS)

    print("otázky po oborech:")
    for topic in TOPICS:
        print(f"  {topic:12s} {sizes[topic]:4d}")
    print(f"\ncelkem      {sum(sizes.values())}")
    print(f"bez opakování {cycle} dní ({cycle / 365:.1f} roku)")

    if loud:
        print(f"\nK PŘEČTENÍ ({len(loud)}) — superlativ v první indicii bývá prozrazení:")
        for note in loud:
            print(f"  ? {note}")

    if vague:
        print(
            f"\nK PŘEČTENÍ ({len(vague)}) — dosaď za zájmeno celou odpověď;"
            " když věta přestane dávat smysl, mluví indicie o něčem jiném:"
        )
        for note in vague:
            print(f"  ? {note}")

    if problems:
        print(f"\nNÁLEZY ({len(problems)}):")
        for p in problems:
            print(f"  • {p}")
        return 1

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(
        json.dumps(deck, ensure_ascii=False, separators=(",", ":")),
        encoding="utf-8",
    )
    print(f"\n-> {OUT} ({OUT.stat().st_size / 1024:.0f} kB)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
