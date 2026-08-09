"""Krok 9 — pětice pro režim Vetřelec.

Čtyři slova něco spojuje, páté ne. Souvislost je vždycky jedna ze tří:

  * **jazyk původu** — čtyři z latiny, jedno z němčiny,
  * **počet slabik**,
  * **slovní druh**.

Aby byl vetřelec **právě jeden**, musí se pětice na zbylých dvou znacích
shodnout: když se hádá jazyk, mají všech pět stejný počet slabik i slovní
druh. Jinak by šlo ukázat na jiné slovo a mít taky pravdu.

Bere se ze stažených hesel Wikislovníku (krok 5c), kde je etymologie,
slovní druh i dělení na slabiky.

Výstup: public/data/intruder/puzzles.json
"""

import json
import os
import random
import re
import sys
import unicodedata

def fold(word: str) -> str:
    out = unicodedata.normalize("NFD", word.lower())
    return "".join(ch for ch in out if unicodedata.category(ch) != "Mn")


HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from intruder_families import FAMILIES  # noqa: E402
RAW = os.path.join(HERE, "raw")
OUT = os.path.join(HERE, "..", "public", "data", "intruder")

# Jazyk původu z první věty etymologie. Bere se jen ten **první** zmíněný —
# přes co slovo doputovalo dál, hráč posuzovat nemůže.
LANGS = {
    "latin": "latina",
    "řec": "řečtina",
    "něm": "němčina",
    "franc": "francouzština",
    "anglic": "angličtina",
    "italsk": "italština",
    "španěl": "španělština",
    "arabsk": "arabština",
    "hebrejsk": "hebrejština",
    "turec": "turečtina",
    "rusk": "ruština",
    "polsk": "polština",
    "maďarsk": "maďarština",
    "praslovansk": "praslovanština",
    "staroslověn": "staroslověnština",
}

POS_NAME = {"noun": "podstatné jméno", "adj": "přídavné jméno",
            "verb": "sloveso", "adv": "příslovce"}

# Rod a vid stojí v hesle jako kurzivní odrážka pod slovním druhem, takže
# se daly stáhnout už v kroku 5c. Jsou to tvrdé mluvnické údaje, ne odhad.
GENDERS = ("rod mužský neživotný", "rod mužský životný", "rod ženský", "rod střední")
ASPECTS = ("nedokonavé", "dokonavé")

# Jak slovo vzniklo. Pozná se z ustálených formulek na začátku etymologie
# a je to souvislost, kterou hráč vidí až po zamyšlení — ne z pravopisu.
FORMS = (
    ("zdrobnělina", r"zdrobněl"),
    ("přechýlené jméno", r"přechýlen"),
    ("složenina", r"složenin|ze spojení|spojením slov|složením slov"),
    ("odvozenina předponou", r"předpon"),
    ("odvozenina příponou", r"přípon"),
)

MIN_LEN, MAX_LEN = 4, 13
PER_KIND = 400

# Kolik pětic připadne na kterou obtížnost. Rozpočet se pak rozdělí rovným
# dílem mezi rodiny, které do té obtížnosti patří — uvnitř jedné obtížnosti
# tak mají všechny rodiny přesně stejný podíl a žádná se nemůže tlačit
# dopředu. Součet je tři tisíce, tedy tolik, kolik se do hry balí: data se
# balí celá a v jednosouborové verzi navíc bobtnají na dvojnásobek.
LEVEL_BUDGET = {"easy": 1200, "normal": 800, "hard": 1000}


def origin(text: str) -> str | None:
    # Jen úplný začátek hesla. Dál v textu se jmenují jazyky, přes které
    # slovo jen prošlo, a to hráč posoudit nemůže.
    head = text[:45].lower()
    best = None
    for mark, name in LANGS.items():
        found = head.find(mark)
        if found >= 0 and (best is None or found < best[0]):
            best = (found, name)
    return best[1] if best else None


def century(text: str) -> str | None:
    """Století, ve kterém se slovo v češtině objevuje. Jen když ho heslo
    vysloveně uvádí — dohadovat se nebude."""
    found = re.search(r"\b(\d{1,2})\.\s*stolet", text[:200])
    return f"{found.group(1)}. století" if found else None


def load() -> list[dict]:
    cache = json.load(open(os.path.join(RAW, "etymology.json"), encoding="utf-8"))
    allowed = set(json.load(
        open(os.path.join(HERE, "..", "tests", "fixtures", "base-forms.json"), encoding="utf-8")
    ))
    words = []
    for word, entry in cache.items():
        if not entry or word not in allowed or not (MIN_LEN <= len(word) <= MAX_LEN):
            continue
        pos = (entry.get("pos") or [None])[0]
        syl = entry.get("syl")
        if pos not in POS_NAME or not syl or not re.fullmatch(r"[^\W\d_]+(-[^\W\d_]+)+", syl):
            continue
        kind = entry.get("kind") or ""
        story = entry.get("e") or ""
        low = story[:90].lower()
        words.append({
            "word": word,
            "pos": pos,
            "syl": syl.count("-") + 1,
            "lang": origin(story) if story else None,
            "gender": next((g for g in GENDERS if g in kind), None),
            "aspect": next((a for a in ASPECTS if a in kind), None),
            "form": next((name for name, mark in FORMS if re.search(mark, low)), None),
            "century": century(story) if story else None,
        })
    return words


# Znaky, které se posuzují. Souvislostí je tolik co znaků; zbytek slouží
# ke kontrole, že pětice nenabízí druhou stejně dobrou odpověď.
TRAITS = ("lang", "syl", "pos", "gender", "aspect", "form", "century")

# Jak nápadný ten rozdíl je. Slovní druh a rod se poznají skoro na první
# pohled; jazyk původu a doba přejetí až po zamyšlení.
LEVEL = {
    "pos": "easy",
    "gender": "easy",
    "syl": "normal",
    "aspect": "normal",
    "form": "normal",
    "lang": "hard",
    "century": "hard",
}

LABEL = {
    "lang": "jazyk původu",
    "syl": "počet slabik",
    "pos": "slovní druh",
    "gender": "jmenný rod",
    "aspect": "vid slovesa",
    "form": "způsob vzniku",
    "century": "doba přejetí",
}


def only_answer(five: list[dict], kind: str) -> bool:
    """
    Nabízí pětice **jedinou** správnou odpověď?

    Ostatní znaky se shodovat nemusí — slova klidně můžou mít každé jiný
    počet slabik. Nesmí se ale stát, že by čtyři z nich sdílely hodnotu
    ještě nějakého jiného znaku: pak by šlo ukázat na páté slovo a mít taky
    pravdu. Když ji sdílí všech pět, nikoho to nevyděluje a vadí to.
    """
    for trait in TRAITS:
        if trait == kind:
            continue
        counts: dict[object, int] = {}
        for item in five:
            if item[trait] is not None:
                counts[item[trait]] = counts.get(item[trait], 0) + 1
        if any(count == 4 for count in counts.values()):
            return False
    return True


def build(words: list[dict], kind: str, rng: random.Random) -> list[dict]:
    """Pětice pro jeden druh souvislosti."""
    by_value: dict[object, list[dict]] = {}
    for item in words:
        if item[kind] is not None:
            by_value.setdefault(item[kind], []).append(item)
    values = [v for v, group in by_value.items() if len(group) >= 4]
    if len(values) < 2:
        return []

    out: list[dict] = []
    seen: set[tuple] = set()
    for _ in range(PER_KIND * 120):
        if len(out) >= PER_KIND:
            break
        value = rng.choice(values)
        other = rng.choice([v for v in by_value if v != value])
        four = rng.sample(by_value[value], 4)
        odd = rng.choice(by_value[other])
        five = four + [odd]

        # Varianty téhož slova („kanoe" a „kánoe") vedle sebe stát nesmí,
        # a vetřelec nesmí trčet délkou — jinak se pozná od pohledu.
        stems = {re.sub(r"[^a-z]", "", fold(i["word"]))[:5] for i in five}
        lengths = [len(i["word"]) for i in five]
        if len(stems) < 5 or max(lengths) - min(lengths) > 3:
            continue
        if not only_answer(five, kind):
            continue
        key = tuple(sorted(i["word"] for i in five))
        if key in seen:
            continue
        seen.add(key)
        shared = POS_NAME[value] if kind == "pos" else value
        other = POS_NAME[odd[kind]] if kind == "pos" else odd[kind]
        answer = LABEL[kind]
        choices = [answer] + rng.sample([LABEL[k] for k in TRAITS if k != kind], 2)
        rng.shuffle(choices)
        out.append({
            "words": [i["word"] for i in five],
            "odd": odd["word"],
            "choices": choices,
            "answer": answer,
            "recap": f"Souvislost: {LABEL[kind]} — {shared}. U vetřelce: {other}.",
            "difficulty": LEVEL[kind],
            "family": f"jaz:{kind}",
        })
    return out


def level_of(family: dict) -> str:
    """Obtížnost rodiny — a je to jediné místo, kde se o ní rozhoduje.

    Pravidlo je jednoduché a drží celý režim pohromadě: **rodina se střechou
    je lehká**. Pětice, u které je na první pohled vidět, že jsou to všechno
    houby, dává hráči polovinu práce zadarmo — zbývá najít osu mezi pěti
    slovy jedné třídy. To je hezký rozcvičovací úkol, ale není to vetřelec.

    Střední a těžkou nesou jen **skryté** rodiny, kde pětice vypadá jako
    náhodná hromada a hráč nemá se čeho chytit, dokud souvislost nenajde.
    Mezi nimi obtížnost určuje, jak dlouho se hledá: zvěrokruh a karty zná
    každý, takže spadly na lehkou, kdežto Formanovy filmy nebo souhvězdí
    chtějí znalost.
    """
    return family["level"] if family.get("hidden") else "easy"


# Otázky, které se za „Čtyři z nich" nedají přilepit tak, jak jsou.
#
# Otázky u rodin jsou psané jako samostatné věty o jednom slově („je to
# polévka", „sedá se na ně"). Ve vyhodnocení ale stojí za podmětem „Čtyři
# z nich" a tam přestanou sedět ze tří důvodů:
#
# * **číslo.** „Čtyři z nich je to polévka" — sloveso i jmenná část musí do
#   množného čísla: „jsou polévky".
# * **příklonka.** V češtině se „se" váže na druhé místo ve větě, takže po
#   podmětu jde hned ono: ne „Čtyři z nich čtou se stejně", ale „Čtyři
#   z nich se čtou stejně".
# * **zdvojený odkaz.** „sedá se na ně", „vaří se v tom", „máme je v páru" —
#   to „ně / to / je" je zástupka za táž slova, která už stojí v podmětu,
#   takže se ve větě říká dvakrát. Tyhle otázky se musí přepsat celé.
#
# Vlevo je otázka tak, jak ji má rodina, vpravo tvar do věty. Ostatní
# otázky projdou beze změny, jen se jim ubere „to" po „jsou".
RECAP = {
    # příklonka patří hned za podmět
    "chovají se pro užitek": "se chovají pro užitek",
    "hodí se do zimy a mokra": "se hodí do zimy a mokra",
    "hraje se s míčem": "se hrají s míčem",
    "hraje se s raketou nebo pálkou": "se hrají s raketou nebo pálkou",
    "hrají se s kartami": "se hrají s kartami",
    "nosí se na hlavě": "se nosí na hlavě",
    "pečou se v troubě": "se pečou v troubě",
    "používá se dodnes": "se používají dodnes",
    "tančí se ve dvojici": "se tančí ve dvojici",
    "vyrábějí se z mléka": "se vyrábějí z mléka",
    "čtou se stejně zepředu i zezadu": "se čtou stejně zepředu i zezadu",
    # jednotné číslo do množného
    "je to dobrá vlastnost": "jsou dobré vlastnosti",
    "je to mince, ne bankovka": "jsou mince, ne bankovky",
    "je to obytná místnost uvnitř": "jsou obytné místnosti uvnitř",
    "je to plod nebo semeno": "jsou plody nebo semena",
    "je to polévka": "jsou polévky",
    "je to poušť": "jsou pouště",
    "je to přírodní vlákno": "jsou přírodní vlákna",
    "má přes sto tisíc obyvatel": "mají přes sto tisíc obyvatel",
    "nosí se to na dolní polovině těla": "se nosí na dolní polovině těla",
    "něco to zakazuje nebo přikazuje": "něco zakazují nebo přikazují",
    "pečuje to o tělo a vzhled": "pečují o tělo a vzhled",
    "vychází to tištěné na papíře": "vycházejí tištěné na papíře",
    # zástupka navíc — otázka se říká jinak
    "hraje se na ně dechem": "jsou dechové",
    "hraje se na ně smyčcem": "jsou smyčcové",
    "hraje se na to pomocí kláves": "jsou klávesové",
    "je to celá stovka nebo víc": "znamenají sto a víc",
    "je to voda v pevném stavu": "jsou zmrzlá voda",
    "jí se z nich podzemní část": "mají jedlou podzemní část",
    "loví a pohybují se v noci": "jsou aktivní v noci",
    "máme je v páru": "máme v páru",
    "nahradilo je euro nebo jím jsou": "patří do eurozóny",
    "najdeš je v duze": "najdeš v duze",
    "napsal je český autor": "napsal český autor",
    "sedá se na ně": "jsou na sezení",
    "vaří se v tom na sporáku": "se dávají na sporák",
    "voda v nich stojí, neteče": "mají stojatou vodu",
    "způsobuje je virus": "způsobuje virus",
}


def in_sentence(ask: str) -> str:
    """Otázka přeskládaná do věty „Čtyři z nich …".

    Otázky jsou psané tak, aby stály samy o sobě („jsou to zároveň jména
    českých měst"), jenže ve vyhodnocení se lepí za „Čtyři z nich" a z toho
    vyleze „Čtyři z nich jsou to zároveň jména". To „to" tam po podmětu
    nemá co dělat, takže se cestou do věty zahodí. Otázky, kterým nestačí
    tohle jedno škrtnutí, mají tvar napsaný v tabulce RECAP.
    """
    if ask in RECAP:
        return RECAP[ask]
    return "jsou " + ask[len("jsou to "):] if ask.startswith("jsou to ") else ask


def from_families(rng: random.Random, per_family: dict[str, int]) -> list[dict]:
    """Hádanky z ručně psaných rodin — páteř režimu.

    Čtyři slova zevnitř, jedno zvenku. Otázky do druhého kroku jsou psané
    k rodině: ta správná dělí čtveřici od vetřelce, zbylé dvě platí pro
    všech pět, takže nic nevydělují.
    """
    out = []
    for family in FAMILIES:
        # Strop je pro všechny rodiny téže obtížnosti stejný.
        #
        # Dřív dostávaly skryté rodiny sto padesát pětic a ostatní pětačtyřicet,
        # takže z hotové sady byla každá osmá pětice zvěrokruh nebo karty —
        # hráč je potkával pořád dokola a hlásil to. O rozestup mezi stejnými
        # rodinami se pak stará ještě hra sama.
        want = min(per_family[level_of(family)],
                   len(family["inside"]) * len(family["outside"]))
        seen = set()
        for _ in range(want * 20):
            if len(seen) >= want:
                break
            four = rng.sample(family["inside"], 4)
            odd = rng.choice(family["outside"])
            key = tuple(sorted(four)) + (odd,)
            if key in seen:
                continue
            seen.add(key)
            # Ze zásoby zavádějících vět se berou dvě — nabídka se tím mění
            # kolo od kola a nedá se zapamatovat, že správná bývá ta první.
            #
            # Věta nemusí platit pro všech pět slov. Vadí jediný případ:
            # kdyby platila pro právě čtyři, vydělila by pátého sama a
            # hádanka by měla dvě řešení. Tři z pěti ani dva z pěti nikoho
            # nevydělují, zato nutí hráče věty doopravdy zvažovat.
            five = set(four + [odd])
            pool = family["asks"][1:] + [
                loose["text"]
                for loose in family.get("loose", [])
                if len(five & set(loose["words"])) != 4
            ]
            choices = [family["asks"][0]] + rng.sample(pool, 2)
            rng.shuffle(choices)
            out.append({
                "words": rng.sample(four + [odd], 5),
                "odd": odd,
                "choices": choices,
                "answer": family["asks"][0],
                # U skryté rodiny je střecha totéž co osa, takže by se věta
                # opakovala („slova, která jsou znamením zvěrokruhu. Čtyři
                # z nich jsou to znamení zvěrokruhu").
                "recap": (
                    f"Čtyři z nich {in_sentence(family['asks'][0])} — {odd} ne."
                    if family.get("hidden")
                    else f"Všech pět: {family['roof']}. Čtyři z nich "
                         f"{in_sentence(family['asks'][0])} — {odd} ne."
                ),
                "difficulty": level_of(family),
                "hidden": bool(family.get("hidden")),
                # Klíč rodiny. První otázka je napříč rodinami jedinečná,
                # takže z ní jde udělat značku, aniž by ji někdo psal ručně.
                "family": family["asks"][0],
            })
    return out


def main() -> int:
    rng = random.Random(7)
    words = load()

    # Tabulka přepisů má hlídat sama sebe: kdyby se otázka v rodině
    # přeformulovala a v RECAP zůstal starý tvar, tichounce by se přestal
    # používat a ve vyhodnocení by se zase objevila rozbitá věta.
    stale = set(RECAP) - {family["asks"][0] for family in FAMILIES}
    if stale:
        print("RECAP míří na otázky, které už nikde nejsou: " + ", ".join(sorted(stale)))
        return 1

    # Kolik pětic připadne na jednu rodinu.
    #
    # Rozpočet obtížnosti se dělí rovným dílem mezi rodiny, které do ní
    # patří. Lehkou nese osmdesát rodin se střechou, takže na každou vyjde
    # pár desítek; střední a těžkou nese hrstka skrytých, takže každá z nich
    # dostane víc. Uvnitř jedné obtížnosti mají ale všechny stejně — a to je
    # jediné, na čem hráči záleží, protože obtížnost si vybírá sám.
    families: dict[str, int] = {}
    for family in FAMILIES:
        families[level_of(family)] = families.get(level_of(family), 0) + 1
    for kind in TRAITS:
        families[LEVEL[kind]] = families.get(LEVEL[kind], 0) + 1
    per_family = {level: LEVEL_BUDGET[level] // count for level, count in families.items()}
    for level in sorted(per_family):
        print(f"  {level}: {families[level]} rodin po {per_family[level]} pěticích")

    made = []
    for kind in TRAITS:
        rows = build(words, kind, rng)[: per_family[LEVEL[kind]]]
        print(f"  {kind}: {len(rows)}")
        made += rows

    from_fam = from_families(rng, per_family)
    for one in from_fam:
        one.pop("hidden", None)
    print(f"  z rodin: {len(from_fam)}")

    puzzles = made + from_fam
    rng.shuffle(puzzles)
    for i, puzzle in enumerate(puzzles):
        puzzle["id"] = f"i-{i:04d}"
        rng.shuffle(puzzle["words"])

    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, "puzzles.json")
    json.dump(puzzles, open(path, "w", encoding="utf-8"), ensure_ascii=False)
    print(f"pětic: {len(puzzles)} -> {os.path.normpath(path)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
