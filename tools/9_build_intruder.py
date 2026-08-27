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


def velke(word: str) -> bool:
    """Vlastní jméno — poznají se podle velkého písmene na začátku."""
    return word[:1].isupper()


def frekvence() -> dict[str, int]:
    """Jak běžné které slovo je. Mimo build se vrátí prázdno a kontroly mlčí."""
    import json  # noqa: PLC0415

    cesta = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                         "out", "lexicon_base.json")
    if not os.path.exists(cesta):
        return {}
    base = json.load(open(cesta, encoding="utf-8"))
    return {w: f for delka in base for w, f in base[delka]}


HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from intruder_families import FAMILIES  # noqa: E402
from word_tags import SKATULKY, STRECHY, doplnit, dve_reseni, hrubsi_osa  # noqa: E402

doplnit(FAMILIES)
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
# dopředu. Rozpočet střední a těžké stoupá s tím, jak rodin přibývá: než
# přišly skryté várky, nesla střední dvanáct rodin, dneska pětaosmdesát.
# Kdyby rozpočet zůstal, vyšlo by na rodinu deset pětic a hráč by celou
# obtížnost prošel dřív, než by se stihl rozkoukat. Součet drží pod pěti
# tisíci — data se balí celá, takže víc už by bylo znát na velikosti
# stažení.
# Rozpočet se dělí rovným dílem mezi rodiny dané úrovně, takže s každou
# další rodinou ubude pěticím na rodinu — a při celočíselném dělení
# spadne rovnou o celý stupeň. Po dvou stovkách nových rodin vyšlo na
# rodinu šest pětic místo deseti a sada se scvrkla; čísla se proto zvedla
# tak, aby na každou skrytou rodinu vyšlo osm pětic.
LEVEL_BUDGET = {"easy": 1200, "normal": 2400, "hard": 2100}


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
    """Hesla Wikislovníku s etymologií, slabikami a slovním druhem.

    Zásoba se stahuje krokem 5c a do repozitáře nepatří (`tools/raw/` je
    v .gitignore). Když chybí, není to důvod build shodit: rodinné pětice,
    kterých je přes pět tisíc, na ní nestojí. Vrátí se prázdno a `main`
    si jazykové pětice převezme z minulého sestavení, ať se o ně sada
    nepřipraví jen proto, že se stavělo bez staženého slovníku.
    """
    cesta = os.path.join(RAW, "etymology.json")
    if not os.path.exists(cesta):
        print(f"POZOR: {os.path.normpath(cesta)} chybí — jazykové pětice se"
              " převezmou z minulého sestavení (obnoví je tools/5c_fetch_etymology.py)")
        return []
    cache = json.load(open(cesta, encoding="utf-8"))
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
        # Zvířata a rostliny umí vydělit vetřelce samy, i když se hádá
        # počet slabik — viz word_tags.py.
        if dve_reseni([i["word"] for i in four], odd["word"]):
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


def prezbroj(rng: random.Random) -> int:
    """
    Rodinám, které si braly vetřelce z nudné zásoby, dá sousedy téže skupiny.

    Novější várky si sousedy hledají samy už v generátoru, ale ručně psané
    rodiny z prvních dávek na to čekat nemusí: skupinu jde poznat z otázky.
    Kde je uvnitř odborná hantýrka („pomlka, odrážka, tečka, posuvka") a vně
    domácí potřeba („šroub"), pozná hráč vetřelce dřív, než si otázku
    přečte — a hádanka se ptá na vzhled místo na znalost.

    Sahá se **jen** na rodiny, které mají celou zásobu z nudné vaty. Kde je
    seznam vně psaný ručně, byl k tomu důvod a ten se nepřebíjí.
    """
    from gen_families7 import VATA  # noqa: PLC0415 — jen kvůli téhle kontrole

    vata = set(VATA.split())
    freq = frekvence()

    def bezne(word: str) -> bool:
        return not velke(word) and freq.get(word.lower(), 0) >= 300

    def skupina(family: dict) -> str | None:
        ask = family["asks"][0]
        podil = sum(bezne(w) for w in family["inside"]) / len(family["inside"])
        if ask.startswith("jsou v názvech"):
            return "nazvy"
        if ask.startswith("jsou to zároveň") and podil <= 0.34:
            return "obor"
        return None

    kam = {f["id"]: skupina(f) for f in FAMILIES}
    zmeneno = 0
    for family in FAMILIES:
        moje = kam[family["id"]]
        if moje is None or not set(family["outside"]) <= vata:
            continue
        sousedi = [f for f in FAMILIES if kam[f["id"]] == moje and f is not family]
        kolikrat: dict[str, int] = {}
        for one in sousedi + [family]:
            for word in set(one["inside"]):
                kolikrat[word] = kolikrat.get(word, 0) + 1
        doma = set(family["inside"])
        # Slovo ze dvou rodin naráz („měch" u varhan i v kovárně) by dělalo
        # vetřelce, o kterém by se dalo právem hádat.
        pool = sorted({w for one in sousedi for w in one["inside"]
                       if kolikrat[w] == 1 and w not in doma})
        if len(pool) < 12:
            continue
        family["outside"] = sorted(rng.sample(pool, 12))
        zmeneno += 1
    return zmeneno


def from_families(rng: random.Random, per_family: dict[str, int]) -> list[dict]:
    """Hádanky z ručně psaných rodin — páteř režimu.

    Čtyři slova zevnitř, jedno zvenku. Otázky do druhého kroku jsou psané
    k rodině: ta správná dělí čtveřici od vetřelce, zbylé dvě platí pro
    všech pět, takže nic nevydělují.
    """
    out = []
    osy_skatulek = {f["id"] for f in rodiny_se_skatulkou()}
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
            # Dvě slova z jednoho kořene vedle sebe („malina" a „malinovka")
            # vypadají jako přehlédnutí, i když jsou obě uvnitř právem.
            koreny = {fold(w)[:5] for w in four + [odd]}
            if len(koreny) < 5:
                continue
            # Vetřelec nesmí trčet už tím, **jak vypadá**. Když jsou čtyři
            # slova vlastní jména (Jan, Václav, Anežka, Kliment) a páté je
            # obyčejné podstatné jméno (*kolík*), pozná ho hráč, aniž by
            # o ose cokoli věděl — a těžká hádanka se vyřeší za vteřinu.
            # Hlásili to hráči hned dvakrát, u českých světců a u chemických
            # prvků; obojí bylo v těžké úrovni.
            if velke(odd) != any(velke(w) for w in four):
                continue
            # A pětice nesmí nabízet druhou stejně dobrou odpověď: kdyby byl
            # vetřelec zvíře a byla mezi pěticí zvířata právě čtyři, ukazuje
            # ta čtveřice na jiné slovo než osa rodiny (viz word_tags.py).
            if dve_reseni(four, odd):
                continue
            # A nesmí jít vyřešit **hruběji, než se ptá**. Čtyři zvířata
            # a lavička jsou hádanka o zvířatech, ne o čínském zvěrokruhu:
            # osa je k ničemu a hráč to pozná dřív než ji. Rodinám, které
            # se na tu škatulku ptají samy, to nevadí — tam nic hrubšího
            # není.
            if family["id"] not in osy_skatulek and hrubsi_osa(four, odd):
                continue
            # U rodin se schovaným slovem musí čtveřice schovávat čtyři
            # **různé** věci. Jinak vyjde pětice jako *malinovka,
            # maximalista, román, peruť*, kde dvě slova nesou totéž Mali —
            # osa sedí, ale vypadá to jako přehlédnutí.
            skryte = family.get("skryte")
            if skryte:
                nasady = [skryte[w] for w in four if w in skryte]
                if len(set(nasady)) < len(nasady):
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


def rodiny_se_skatulkou() -> list[dict]:
    """Rodiny, jejichž osa **je** hrubá škatulka.

    U nich je „čtyři zvířata a jedna lavička" správně položená otázka, ne
    zlevnělá: nic hrubšího než zvíře už nad ní není. Všude jinde takovou
    pětici `hrubsi_osa` zamítne.
    """
    return [
        f for f in FAMILIES
        if not f.get("roof", "").startswith("slova")
        and any(m in f.get("roof", "") for marks in STRECHY.values() for m in marks)
    ]


def drive_jazykove() -> list[dict]:
    """Jazykové pětice z minulého sestavení.

    Poznají se podle `family`, které u nich začíná na `jaz:` — rodinné
    pětice tam mají celou otázku. Bez staženého slovníku by se jinak
    ztratily, a to je horší než je pár sestavení nést s sebou.
    """
    path = os.path.join(OUT, "puzzles.json")
    if not os.path.exists(path):
        return []
    stare = json.load(open(path, encoding="utf-8"))
    return [dict(p) for p in stare if str(p.get("family", "")).startswith("jaz:")]


def main() -> int:
    rng = random.Random(7)
    words = load()

    # Starším ručně psaným rodinám se dohledají vetřelci ze stejného soudku.
    print(f"rodin, kterým se doplnili sousedé místo nudné vaty: {prezbroj(rng)}")

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
    if words:
        for kind in TRAITS:
            rows = build(words, kind, rng)[: per_family[LEVEL[kind]]]
            print(f"  {kind}: {len(rows)}")
            made += rows
    else:
        made = drive_jazykove()
        print(f"  jazykové z minulého sestavení: {len(made)}")

    from_fam = from_families(rng, per_family)
    for one in from_fam:
        one.pop("hidden", None)
    print(f"  z rodin: {len(from_fam)}")

    puzzles = made + from_fam
    rng.shuffle(puzzles)
    for i, puzzle in enumerate(puzzles):
        puzzle["id"] = f"i-{i:04d}"
        rng.shuffle(puzzle["words"])

    # Škatulky si odnese i test, aby se dvě řešení nemohla vrátit zadními
    # vrátky. Do hry se nebalí — hráč je nikdy neuvidí, slouží jen ke
    # kontrole hotové sady.
    fixture = os.path.join(HERE, "..", "tests", "fixtures", "word-tags.json")
    json.dump({
        "skatulky": {tag: sorted(words) for tag, words in SKATULKY.items()},
        # A co se v kterém slově schovává — podle toho test pozná, že
        # v jedné pětici nestojí dvě slova s toutéž schovanou věcí.
        "skryte": {f["asks"][0]: f["skryte"] for f in FAMILIES if f.get("skryte")},
        # Osy, které samy jsou hrubou škatulkou. Test podle nich pozná,
        # kde je „čtyři zvířata a jeden hrnec" v pořádku a kde je to
        # hádanka, která se dá vyřešit, aniž by se o ose cokoli vědělo.
        "osy_skatulek": sorted({f["asks"][0] for f in rodiny_se_skatulkou()}),
    }, open(fixture, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, "puzzles.json")
    json.dump(puzzles, open(path, "w", encoding="utf-8"), ensure_ascii=False)
    print(f"pětic: {len(puzzles)} -> {os.path.normpath(path)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
