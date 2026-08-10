"""Generátor sedmé várky rodin pro Vetřelce — 80 skrytých střech.

Rodiny do střední a těžké obtížnosti se od těch lehkých liší tím, že nad
pěticí **není vidět střecha**: *kobylka, duše, hlemýžď, police, krk* vypadá
jako náhodná hromada, dokud hráč nepřijde na to, že čtyři z nich jsou části
houslí. Osmdesát takových rodin se špatně píše ručně — a hlavně se v nich
ručně špatně hlídají chyby, které hru rozbijí:

* slovo **vně** rodiny, které do ní ve skutečnosti patří (vetřelec, který
  není vetřelec — hádanka pak nemá řešení),
* **zavádějící věta**, která náhodou platí pro právě čtyři z pěti slov
  (hádanka má dvě řešení),
* **otázka**, která se opakuje v jiné rodině (podle otázky se pozná rodina,
  takže dvě stejné otázky splynou v jednu rodinu),
* **věta do vyhodnocení**, která nesedí do rámce „Čtyři z nich …".

Tenhle skript proto data nejen zapisuje, ale i kontroluje. Co jde ověřit
strojem, ověří strojem:

* **Mechanické rodiny** (pravidlo o písmenech) si slova hledá sám ve
  slovníku hry a pravidlo ověří slovo po slovu — dovnitř i ven.
* **Slova vně** bere z nudné zásoby, ze které předem vyhodí všechno, co leží
  uvnitř kterékoli rodiny — ani jedné z osmdesáti.
* **Zavádějící věty** bere z banky a ty, na které má pravidlo, ověří: věta
  nesmí platit ani pro jedno slovo v rodině.

Co strojem ověřit nejde — jestli je *hermelín* opravdu sýr — stojí
v seznamech níž a ručí za to autor.

Spuštění:  python3 tools/gen_families7.py
Výstup:    tools/intruder_families7.py
"""

import json
import os
import random
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
OUT = os.path.join(HERE, "intruder_families7.py")


def fold(word: str) -> str:
    """Slovo bez diakritiky a malými písmeny — na pravidla o písmenech."""
    out = unicodedata.normalize("NFD", word.lower())
    return "".join(ch for ch in out if unicodedata.category(ch) != "Mn")


# ---------------------------------------------------------------- slovník --

# Slova, která se do hádanky nehodí, i když je slovník zná. Jsou to vesměs
# slova, na která se rodina nemá hledat: hrubá, ponurá nebo tak abstraktní,
# že si pod nimi nikdo nic nepředstaví.
BLOCK = {
    "vražda", "porno", "mrtvola", "zbraň", "rakev", "smrt", "sebevražda",
    "parchant", "svině", "kurva", "nádor", "rakovina", "mučení", "otrok",
    "znásilnění", "poprava", "nacista", "teror", "terorista", "atentát",
    "válka", "granát", "pistole", "bomba", "jed", "opilec", "narkoman",
    "hnůj", "zvratky", "hovno", "moč", "krev", "úchyl", "idiot", "debil",
    "adaptabilita", "antisemitismus", "astigmatismus", "anachronismus",
    "altruismus", "automatismus", "antagonista", "antikomunista",
    "aktualizace", "administrativa",
}

# Doplněk k slovníku hry. Slovník je stavěný pro hádání slov, takže v něm
# chybí spousta krátkých všedních podstatných jmen — a zrovna ta jsou pro
# pravidla o písmenech nejcennější. Pravidlo si je stejně ověří samo, takže
# tenhle seznam nemůže nic pokazit; jen rozšiřuje výběr.
SUPPL = """
bota brána bunda cesta cibule cukr dárek dech deka deník dílna dlaň doba dolar
dopis drát duha dům dveře dýka fazole flétna forma fotka guma hlína hodiny
hora hospoda houba hrad hrnek hřeben chalupa chleba chodba jáma jehla kabát
kachna kalhoty kamna kapsa karta kastrol keř kladivo klec klíč kniha kolo
komín konev koš košile krabice kráva kruh křeslo kufr kytka lampa lavice led
lék les lístek loď lopata louka lyže máslo měsíc mince miska most motor
mouka mrak mýdlo nádraží nůž oblak obraz oheň okno ostrov palivo panev papír
pásek pero pila plachta plot police potok prkno provaz prsten pytel rádio
rám rukavice ryba řeka sáně sešit síť sklep sklo skříň slunce sníh sova
srdce stan strom stůl sud sukně svíčka šátek šňůra špendlík štětec talíř
tráva trouba truhla tužka učebnice ulice váha váza větev vidlička víno vlak
vlna voda vůz zahrada zámek zed zeď zrcadlo zvon žebřík židle
"""


def slovnik() -> list[str]:
    """Slova, ze kterých si mechanické rodiny berou — od nejběžnějších.

    Základ jsou podstatná jména z Detektiva: jsou v základním tvaru a mají
    u sebe slovní druh, takže se dá spolehlivě odsít všechno, co není
    podstatné jméno. Pořadí dělá četnost z korpusu — čím běžnější slovo,
    tím dřív na řadě, aby v hádankách stála slova, která hráč zná.
    """
    puzzles = json.load(
        open(os.path.join(ROOT, "public", "data", "detective", "puzzles.json"),
             encoding="utf-8"))
    words = {p["word"] for p in puzzles
             if p.get("grammar", "").startswith("podstatné")}
    words |= set(SUPPL.split())
    words -= BLOCK

    freq: dict[str, int] = {}
    with open(os.path.join(HERE, "raw", "cs_50k.txt"), encoding="utf-8") as fh:
        for i, line in enumerate(fh):
            freq.setdefault(line.split()[0], i)

    ok = [w for w in words if w.isalpha() and 3 <= len(w) <= 11]
    ok.sort(key=lambda w: (freq.get(w, 99_999), w))
    return ok


# ------------------------------------------------------- pravidla o tvaru --

SAMOHLASKY = set("aeiouy")

# Schované slovo se hledá **i s háčky a čárkami**, ne v přepisu bez
# diakritiky. Jinak by „povětří" prošlo jako slovo se schovanou trojkou
# („tří" místo „tři") a hráč by po vyhodnocení marně hledal, kde tam jaká
# trojka je. Co není vidět, to v hádance neplatí.
ZVIRATA = ["rak", "lev", "sob", "los", "myš", "pes", "had", "kos", "kůň",
           "vlk", "srna", "jelen", "kočka", "vůl", "beran", "orel"]
CISLA = ["sto", "tři", "pět", "osm", "dva", "šest", "sedm", "devět", "deset"]
TELO = ["oko", "nos", "ruka", "noha", "zub", "ucho", "krk", "pata", "prst",
        "brada", "ret", "ústa", "čelo", "dlaň"]
STATY = ["čína", "peru", "mali", "omán", "írán", "irák", "kuba", "laos",
         "nepál", "malta", "indie", "korea", "sýrie", "kongo"]
JMENA = ["ivan", "petr", "ivo", "vít", "adam", "roman", "lenka", "eva",
         "ota", "jan", "ida", "alena", "hana", "olga", "marek", "tomáš"]


def _samohlasky(word: str) -> list[str]:
    return [c for c in fold(word) if c in SAMOHLASKY]


def _obsahuje(word: str, seznam: list[str]) -> bool:
    """Schované slovo se počítá jen tehdy, když je ve slově doopravdy vidět.

    Slovo, které samo **je** tím hledaným (dlaň, pes), se nepočítá — schované
    není nic, co stojí celé na očích, a pětice by se prozradila.
    """
    low = word.lower()
    if low in seznam:
        return False
    return any(x in low for x in seznam)


# Pravidla jsou psaná tak, aby je šlo pustit na jakékoli slovo: podle nich
# se hledá dovnitř rodiny a týmž pravidlem se ověřuje, že slovo vně do
# rodiny nepatří. Jeden zdroj pravdy pro obě strany.
PRAVIDLA = {
    "abecedni-poradi": lambda w: all(fold(w)[i] <= fold(w)[i + 1]
                                     for i in range(len(fold(w)) - 1)),
    "stejne-kraje": lambda w: fold(w)[0] == fold(w)[-1],
    "skryte-cislo": lambda w: _obsahuje(w, CISLA),
    "skryte-telo": lambda w: _obsahuje(w, TELO),
    "stejna-samohlaska": lambda w: (len(_samohlasky(w)) >= 2
                                    and len(set(_samohlasky(w))) == 1),
    "samohlaska-kraje": lambda w: fold(w)[0] in SAMOHLASKY and fold(w)[-1] in SAMOHLASKY,
    "tri-souhlasky": lambda w: any(
        all(c not in SAMOHLASKY for c in fold(w)[i:i + 3])
        for i in range(len(fold(w)) - 2)),
    "dvojhlaska": lambda w: any(d in fold(w) for d in ("ou", "au", "eu")),
    "dvakrat-dvojice": lambda w: any(fold(w).count(fold(w)[i:i + 2]) > 1
                                     for i in range(len(fold(w)) - 1)),
    "vzacne-pismeno": lambda w: bool(set(fold(w)) & set("fgxwq")),
    "vic-samohlasek": lambda w: (sum(c in SAMOHLASKY for c in fold(w))
                                 > sum(c not in SAMOHLASKY for c in fold(w))),
    "ruzne-samohlasky": lambda w: (len(_samohlasky(w)) >= 3
                                   and len(set(_samohlasky(w))) == len(_samohlasky(w))),
    "prvni-pulka": lambda w: all(c in "abcdefghijklm" for c in fold(w)),
    "bez-opakovani": lambda w: len(fold(w)) >= 7 and len(set(fold(w))) == len(fold(w)),
    "sousedni-pismena": lambda w: any(ord(fold(w)[i + 1]) - ord(fold(w)[i]) == 1
                                      for i in range(len(fold(w)) - 1)),
    "rimske-cislo": lambda w: all(c in "ivxlcdm" for c in fold(w)),
    "skryty-stat": lambda w: _obsahuje(w, STATY),
    # Jedna samohláska na celé slovo — slabiku v něm často drží r nebo l
    # (srdce, prst). Souhláskové shluky jsou v češtině tak běžné, že si
    # toho hráč nevšimne, dokud slova nezačne číst po písmenech.
    "jedna-samohlaska": lambda w: sum(c in SAMOHLASKY for c in fold(w)) == 1,
    # Pravidla, která se neuplatní jako rodina, ale hlídají zavádějící věty
    # převzaté z dřívějších várek.
    "palindrom": lambda w: fold(w) == fold(w)[::-1],
    "bez-samohlasky": lambda w: not any(c in SAMOHLASKY for c in fold(w)),
    "zdvojene": lambda w: any(fold(w)[i] == fold(w)[i + 1]
                              for i in range(len(fold(w)) - 1)),
    "skryte-zvire": lambda w: _obsahuje(w, ZVIRATA),
    "skryte-jmeno": lambda w: _obsahuje(w, JMENA),
}


# ------------------------------------------------------ zavádějící věty ----

# Věty do druhého kroku. Ta správná je vždycky první otázka rodiny, tyhle
# mají hráče zmást — proto musí platit buď pro všech pět slov, nebo pro
# žádné. Nikdy pro právě čtyři: to by vydělily vetřelce samy a hádanka by
# měla dvě řešení.
BANKA = [
    "jsou to zároveň jména českých měst",
    "jsou v názvech Shakespearových her",
    "jsou to zároveň značky českého piva",
    "jsou to zároveň příjmení českých prezidentů",
    "jsou to zároveň značky nebo modely aut",
    "jsou v názvech her Járy Cimrmana",
    "jsou to znamení zvěrokruhu",
    "jsou v názvech večerníčků",
    "čtou se stejně zepředu i zezadu",
    "nemají v sobě ani jednu samohlásku",
    "mají v sobě dvě stejná písmena vedle sebe",
    "mají v sobě schované zvíře",
]

# Věty z banky, na které skript má pravidlo. U nich neručí autor, ale
# kontrola: než se věta k rodině přidá, projde všechna její slova.
OVERITELNE = {
    "čtou se stejně zepředu i zezadu": "palindrom",
    "nemají v sobě ani jednu samohlásku": "bez-samohlasky",
    "mají v sobě dvě stejná písmena vedle sebe": "zdvojene",
    "mají v sobě schované zvíře": "skryte-zvire",
}


# ------------------------------------------------------------ nudná vata --

# Slova vně rodin. Jsou schválně všední, konkrétní a z různých koutů —
# kdyby byla všechna z jedné třídy, oddělil by je hráč od čtveřice bez
# přemýšlení. Skript z nich před použitím vyhodí všechna slova, která leží
# uvnitř kterékoli rodiny.
VATA = """
hrnec deštník police sešit koště plot kabát lampa konev žebřík ručník kýbl
polštář koberec mrkev brambora sklenice chleba zahrada silnice stůl lopata
kastrol utěrka rohožka věšák popelnice vařečka struhadlo prostěradlo mýdlo
kartáček ubrus záclona parapet schránka bunda šála ponožka mísa vana sud
dřez trouba pekáč naběračka hrneček podnos tácek ubrousek koš hadr kbelík
smeták lopatka pytel provaz kolík hřebík šroub matice kladívko pilník
vrtačka svěrák hoblík kleště metr šuplík komoda skříň postel matrace deka
peřina ramínko lavička houpačka branka hadice trakař hrábě motyka rýč
truhlík květináč semínko kompost myčka lednička sporák žehlička vysavač
pračka sušák krém pinzeta nůžky hřeben zápisník propiska pravítko guma
ořezávátko lepidlo pouzdro batoh peněženka brýle hodinky náramek řetízek
"""


# ---------------------------------------------------------------- rodiny --

# Mechanické rodiny. Slova si skript najde sám podle pravidla; `ban` je
# ruční brzda na slova, která pravidlem projdou, ale v hádance by trčela
# (moc dlouhá, moc odborná, nebo je v nich osa vidět na první pohled).
MECH = [
    dict(id="mech-abecedni-poradi", level="normal", rule="abecedni-poradi",
         roof="slova, jejichž písmena jdou v abecedním pořadí",
         ask="mají písmena seřazená podle abecedy",
         extra=["most", "los", "kos", "nos", "dost", "cop", "akt", "dík",
                "mor", "knot", "dělo", "déšť"]),
    dict(id="mech-stejne-kraje", level="normal", rule="stejne-kraje",
         roof="slova, která začínají i končí stejným písmenem",
         ask="začínají a končí stejným písmenem",
         extra=["kolik", "krok", "kluk", "okno", "oko", "anténa", "abeceda",
                "krk", "radar", "rotor"]),
    dict(id="mech-skryte-cislo", level="normal", rule="skryte-cislo",
         roof="slova, ve kterých se schovává číslo",
         ask="mají v sobě schované číslo",
         ban=["pětky", "osmnáctka", "stolice", "sedmikráska", "osmák",
              "dvojka", "trojka", "pětka", "šestka", "sedmička", "osmička",
              "šestispřeží", "desetník", "stovka", "dvojče", "šestnáctka",
              "dvojice", "trojice", "pětina", "desetina", "setina"],
         extra=["město", "místo", "prostor", "čistota", "hustota", "stodola",
                "kosmos", "opět", "postoj", "listopad"]),
    dict(id="mech-skryte-telo", level="normal", rule="skryte-telo",
         roof="slova, ve kterých se schovává část těla",
         ask="mají v sobě schovanou část těla",
         ban=["nositel", "prstýnek", "zoubek", "ručička", "nožička"],
         extra=["okolí", "kokos", "pokoj", "okoun", "záruka", "zubr",
                "krkavec", "nohavice", "lopata", "sucho", "nosič"]),
    dict(id="mech-stejna-samohlaska", level="normal", rule="stejna-samohlaska",
         roof="slova, která mají ve všech slabikách stejnou samohlásku",
         ask="mají ve všech slabikách stejnou samohlásku"),
    dict(id="mech-samohlaska-kraje", level="normal", rule="samohlaska-kraje",
         roof="slova, která začínají i končí samohláskou",
         ask="začínají i končí samohláskou"),
    dict(id="mech-tri-souhlasky", level="normal", rule="tri-souhlasky",
         roof="slova se třemi souhláskami za sebou",
         ask="mají v sobě tři souhlásky za sebou"),
    dict(id="mech-dvojhlaska", level="normal", rule="dvojhlaska",
         roof="slova s dvojhláskou",
         ask="mají v sobě dvojhlásku ou, au nebo eu"),
    dict(id="mech-dvakrat-dvojice", level="normal", rule="dvakrat-dvojice",
         roof="slova, ve kterých se dvojice písmen opakuje",
         ask="mají v sobě dvakrát tutéž dvojici písmen"),
    dict(id="mech-vzacne-pismeno", level="normal", rule="vzacne-pismeno",
         roof="slova s písmenem, které je v češtině vzácné",
         ask="mají v sobě f, g, x nebo w"),
    dict(id="mech-vic-samohlasek", level="normal", rule="vic-samohlasek",
         roof="slova, ve kterých je víc samohlásek než souhlásek",
         ask="mají víc samohlásek než souhlásek"),
    dict(id="mech-ruzne-samohlasky", level="normal", rule="ruzne-samohlasky",
         roof="slova, ve kterých se žádná samohláska neopakuje",
         ask="nemají v sobě dvakrát tutéž samohlásku"),
    dict(id="mech-prvni-pulka", level="hard", rule="prvni-pulka",
         roof="slova z písmen první poloviny abecedy",
         ask="mají písmena jen z první poloviny abecedy"),
    dict(id="mech-bez-opakovani", level="hard", rule="bez-opakovani",
         roof="dlouhá slova, ve kterých se žádné písmeno neopakuje",
         ask="mají aspoň sedm písmen a ani jedno se v nich neopakuje"),
    dict(id="mech-sousedni-pismena", level="hard", rule="sousedni-pismena",
         roof="slova se dvěma písmeny, která jdou po sobě i v abecedě",
         ask="mají vedle sebe dvě písmena, která jdou po sobě i v abecedě"),
    dict(id="mech-rimske-cislo", level="hard", rule="rimske-cislo",
         roof="slova jen z písmen římských číslic",
         ask="mají jen písmena, která se používají jako římské číslice",
         extra=["div", "mix", "civil", "vliv", "lid", "cíl", "mim"]),
    dict(id="mech-jedna-samohlaska", level="normal", rule="jedna-samohlaska",
         roof="slova, ve kterých je jen jedna samohláska",
         ask="mají v sobě jen jednu jedinou samohlásku"),
    dict(id="mech-skryty-stat", level="hard", rule="skryty-stat",
         roof="slova, ve kterých se schovává jméno státu",
         ask="mají v sobě schované jméno státu",
         extra=["román", "malina", "malinovka", "peruť", "kubatura",
                "inkubace", "maximalista"]),
]

# Znalostní rodiny. Slova uvnitř píše autor, slova vně doplní skript
# z vaty. `avoid` je seznam slov z vaty, která by do rodiny mohla patřit —
# stroj to nepozná, autor ano.
#
# Uvnitř smí stát jen slovo, které je **samo o sobě všední**. Kdyby mezi
# stanicemi metra stálo Kobylisy nebo mezi ostrovy Sumatra, pozná hráč osu
# podle jediného slova a hledat nemusí. Proto: anděl, muzeum, můstek — a
# malta, java, kuba.
ZNALOSTNI: list[dict] = [
    # ---------------------------------------------------------- střední --
    dict(id="skryte-metro", level="normal",
         roof="slova, která jsou zároveň stanice pražského metra",
         ask="jsou to zároveň stanice pražského metra",
         inside=["anděl", "muzeum", "můstek", "skalka", "háje", "luka",
                 "flora", "hůrka", "vyšehrad", "opatov", "motol", "pankrác"]),
    dict(id="skryte-meny", level="normal",
         roof="slova, která jsou zároveň měny",
         ask="jsou to zároveň měny",
         inside=["jen", "libra", "koruna", "real", "marka", "rubl", "dolar",
                 "peso", "rand", "won"]),
    dict(id="skryte-recka-pismena", level="normal",
         roof="slova, která jsou zároveň písmena řecké abecedy",
         ask="jsou to zároveň písmena řecké abecedy",
         inside=["delta", "gama", "beta", "alfa", "omega", "sigma", "jota",
                 "kappa", "lambda", "théta"]),
    dict(id="skryte-ostrovy", level="normal",
         roof="slova, která jsou zároveň ostrovy",
         ask="jsou to zároveň ostrovy",
         inside=["malta", "java", "kuba", "jersey", "man", "bali", "korfu",
                 "rhodos", "kréta", "mallorca"]),
    dict(id="skryte-karetni-hry", level="normal",
         roof="slova, která jsou zároveň karetní hry",
         ask="jsou to zároveň karetní hry",
         inside=["prší", "oko", "sedma", "žolík", "mariáš", "kanasta",
                 "poker", "dáma", "vole", "kvarteto"]),
    dict(id="skryte-casopisy", level="normal",
         roof="slova, která jsou zároveň názvy českých časopisů",
         ask="jsou to zároveň názvy českých časopisů",
         inside=["blesk", "květy", "respekt", "reflex", "instinkt", "vlasta",
                 "mateřídouška", "sluníčko", "junák", "téma"]),
    dict(id="skryte-kapely", level="normal",
         roof="slova, která jsou zároveň názvy českých kapel",
         ask="jsou to zároveň názvy českých kapel",
         inside=["kabát", "katapult", "turbo", "lucie", "kryštof", "olympic",
                 "buty", "traband"]),
    dict(id="skryte-hokej", level="normal",
         roof="slova, která jsou zároveň názvy českých hokejových klubů",
         ask="jsou to zároveň názvy českých hokejových klubů",
         inside=["kometa", "motor", "energie", "piráti", "rytíři", "oceláři",
                 "vlci", "berani", "draci", "indiáni"]),
    dict(id="skryte-motorky", level="normal",
         roof="slova, která jsou zároveň názvy motorek a mopedů",
         ask="jsou to zároveň názvy motorek nebo mopedů",
         inside=["pionýr", "babeta", "stadion", "jawa", "manet", "čezeta",
                 "panelka", "kývačka"]),
    dict(id="skryte-syry", level="normal",
         roof="slova, která jsou zároveň názvy sýrů",
         ask="jsou to zároveň názvy sýrů",
         inside=["niva", "hermelín", "lučina", "eidam", "primátor", "javor",
                 "madeta", "vysočina", "kmotr", "moravan"]),
    dict(id="skryte-tance", level="normal",
         roof="slova, která jsou zároveň tance",
         ask="jsou to zároveň tance",
         inside=["polka", "beseda", "sousedská", "step", "tango", "valčík",
                 "mazurka", "kalamajka", "furiant", "rejdovák"]),
    dict(id="skryte-sladkosti", level="normal",
         roof="slova, která jsou zároveň názvy sladkostí",
         ask="jsou to zároveň názvy českých sladkostí",
         inside=["míša", "horalka", "tatranka", "kofila", "lentilky", "banán",
                 "deli", "fidorka"]),
    dict(id="skryte-mluvnice", level="normal",
         roof="slova, která jsou zároveň mluvnické pojmy",
         ask="jsou to zároveň mluvnické pojmy",
         inside=["pád", "rod", "vid", "vzor", "kmen", "spona", "věta", "člen",
                 "přípona", "předložka"]),
    dict(id="skryte-divadlo", level="normal",
         roof="slova, která jsou zároveň divadelní pojmy",
         ask="jsou to zároveň divadelní pojmy",
         inside=["opona", "rampa", "prkna", "budka", "kulisa", "šatna",
                 "lóže", "jeviště", "zákulisí", "premiéra"]),
    dict(id="skryte-ucho-oko", level="normal",
         roof="slova, která jsou zároveň části ucha nebo oka",
         ask="jsou to zároveň části ucha nebo oka",
         inside=["kladívko", "třmínek", "kovadlinka", "bubínek", "čočka",
                 "duhovka", "sítnice", "hlemýžď", "zornice", "bělmo"]),
    dict(id="skryte-pocitac", level="normal",
         roof="slova, která jsou zároveň počítačové pojmy",
         ask="jsou to zároveň počítačové pojmy",
         inside=["plocha", "koš", "složka", "schránka", "brána", "myš",
                 "okno", "disk", "sítě", "jádro"],
         avoid=["koš", "schránka", "police"]),
    dict(id="skryte-fotbal", level="normal",
         roof="slova, která jsou zároveň fotbalové pojmy",
         ask="jsou to zároveň fotbalové pojmy",
         avoid=["branka"],
         inside=["roh", "sudí", "brána", "vápno", "prapor", "karta", "hlavička",
                 "zeď", "postavení", "nastavení"]),

    # ------------------------------------------------------------ těžká --
    dict(id="skryte-hory", level="hard",
         roof="slova, která jsou zároveň české hory a vrchy",
         ask="jsou to zároveň české hory nebo vrchy",
         inside=["praděd", "lysá", "kleť", "boubín", "javorník", "ještěd",
                 "radhošť", "klínovec", "čerchov", "smrk"]),
    dict(id="skryte-vetry", level="hard",
         roof="slova, která jsou zároveň názvy větrů",
         ask="jsou to zároveň názvy větrů",
         inside=["fén", "pasát", "monzun", "bóra", "mistral", "sirocco",
                 "chamsín", "buran"]),
    dict(id="skryte-divadla", level="hard",
         roof="slova, která jsou zároveň názvy pražských divadel",
         ask="jsou to zároveň názvy pražských divadel",
         inside=["kalich", "semafor", "minor", "ypsilon", "rokoko", "disk",
                 "studio", "hybernia", "broadway", "komedie"]),
    dict(id="skryte-nakladatelstvi", level="hard",
         roof="slova, která jsou zároveň názvy nakladatelství",
         ask="jsou to zároveň názvy českých nakladatelství",
         inside=["albatros", "argo", "odeon", "portál", "host", "academia",
                 "paseka", "vyšehrad", "torst", "triton"]),
    dict(id="skryte-knihtisk", level="hard",
         roof="slova, která jsou zároveň knihařské a tiskařské pojmy",
         ask="jsou to zároveň knihařské nebo tiskařské pojmy",
         inside=["hřbet", "patka", "obálka", "vazba", "sazba", "list",
                 "verzálka", "korektura", "desky", "předsádka"]),
    dict(id="skryte-stavba", level="hard",
         roof="slova, která jsou zároveň stavební pojmy",
         ask="jsou to zároveň stavební pojmy",
         inside=["štít", "věnec", "překlad", "sokl", "krov", "žlab", "vazník",
                 "ostění", "nadpraží", "podezdívka"]),
    dict(id="skryte-noty", level="hard",
         roof="slova, která jsou zároveň značky v notách",
         ask="jsou to zároveň značky v notách",
         inside=["klíč", "koruna", "křížek", "praporek", "tečka", "pomlka",
                 "odrážka", "posuvka", "osnova", "taktovka"]),
    dict(id="skryte-skladatele", level="hard",
         roof="slova, která jsou zároveň příjmení českých skladatelů",
         ask="jsou to zároveň příjmení českých skladatelů",
         inside=["smetana", "dvořák", "mysliveček", "zelenka", "benda",
                 "fibich", "novák", "kalabis", "vejvoda", "zich"]),
    dict(id="skryte-parky", level="hard",
         roof="slova, která jsou zároveň pražské parky",
         ask="jsou to zároveň pražské parky",
         inside=["stromovka", "letná", "kampa", "petřín", "ladronka",
                 "vypich", "hvězda", "cibulka", "obora", "grébovka"]),
    dict(id="skryte-anglicka", level="hard",
         roof="česká slova, která jsou zároveň anglická slova",
         ask="jsou zároveň anglická slova s jiným významem",
         inside=["most", "led", "pole", "plot", "list", "rod", "pan", "sad",
                 "let", "past"],
         avoid=["plot", "police"]),
    dict(id="skryte-kolo", level="hard",
         roof="slova, která jsou zároveň součásti jízdního kola",
         ask="jsou to zároveň součásti jízdního kola",
         inside=["vidlice", "náboj", "sedlo", "plášť", "rám", "blatník",
                 "paprsek", "klika", "převodník", "brzda"]),
    dict(id="skryte-bota", level="hard",
         roof="slova, která jsou zároveň části boty",
         ask="jsou to zároveň části boty",
         inside=["jazyk", "špička", "pata", "podrážka", "lem", "stélka",
                 "svršek", "podpatek", "tkanička", "šněrování"]),
    dict(id="skryte-okno", level="hard",
         roof="slova, která jsou zároveň části okna nebo dveří",
         ask="jsou to zároveň části okna nebo dveří",
         inside=["křídlo", "klika", "práh", "zárubeň", "pant", "rám",
                 "parapet", "kování", "zástrč", "sklo"],
         avoid=["parapet"]),
    dict(id="skryte-housle", level="hard",
         roof="slova, která jsou zároveň části houslí",
         ask="jsou to zároveň části houslí",
         inside=["kobylka", "duše", "krk", "hlemýžď", "kolíček", "struna",
                 "šnek", "žabka", "smyčec", "hmatník"]),

    # ------ slovo stojí v názvu — název utrhne slovo z jakéhokoli soudku --
    #
    # Nejvydatnější druh skryté rodiny: v názvu knihy může stát cokoli, od
    # *celeru* po *koloběžku*, takže pětice vypadá jako náhodná hromada
    # i tomu, kdo všechny ty knihy četl. Souvislost se hledá po paměti, ne
    # po významu — a to je přesně ta práce, kterou má Vetřelec dávat.
    dict(id="nazev-potter", level="normal",
         roof="slova z názvů dílů Harryho Pottera",
         ask="jsou v názvech dílů Harryho Pottera",
         inside=["kámen", "komnata", "vězeň", "pohár", "řád", "princ",
                 "relikvie", "mudrc"]),
    dict(id="nazev-prsten", level="normal",
         roof="slova z názvů dílů Pána prstenů a Hobita",
         ask="jsou v názvech dílů Pána prstenů a Hobita",
         inside=["společenstvo", "prsten", "věž", "návrat", "král", "hobit",
                 "poušť", "bitva"]),
    dict(id="nazev-star-wars", level="normal",
         roof="slova z názvů dílů Star Wars",
         ask="jsou v názvech dílů Star Wars",
         inside=["hrozba", "klon", "pomsta", "naděje", "impérium", "úder",
                 "síla", "vzestup"]),
    dict(id="nazev-disney", level="normal",
         roof="slova z názvů disneyovek",
         ask="jsou v názvech disneyovek",
         inside=["sněhurka", "popelka", "růženka", "trpaslík", "víla",
                 "kráska", "zvíře", "království"]),
    dict(id="nazev-andersen", level="normal",
         roof="slova z názvů Andersenových pohádek",
         ask="jsou v názvech Andersenových pohádek",
         inside=["šaty", "káčátko", "vojáček", "královna", "hrášek",
                 "slavík", "křesadlo", "palečka"]),
    dict(id="nazev-grimm", level="normal",
         roof="slova z názvů pohádek bratří Grimmů",
         ask="jsou v názvech pohádek bratří Grimmů",
         inside=["karkulka", "husa", "stoleček", "muzikant", "kůzlátko",
                 "chaloupka", "perník", "jeníček"]),
    dict(id="nazev-lindgren", level="normal",
         roof="slova z názvů knih Astrid Lindgrenové",
         ask="jsou v názvech knih Astrid Lindgrenové",
         inside=["punčocha", "loupežník", "střecha", "srdce", "detektiv",
                 "dcera", "bratr", "děti"]),
    dict(id="nazev-pisnicky", level="normal",
         roof="slova z názvů dětských písniček",
         ask="jsou v názvech dětských písniček",
         inside=["kočka", "díra", "travička", "pec", "holka", "ovčák",
                 "zelí", "nanynka"]),
    dict(id="nazev-komedie", level="normal",
         roof="slova z názvů českých filmových komedií",
         ask="jsou v názvech českých filmových komedií",
         inside=["vrchní", "pero", "seno", "jahoda", "blesk", "samota",
                 "vesnička", "kovboj"]),
    dict(id="nazev-svetove-filmy", level="normal",
         roof="slova z názvů slavných světových filmů",
         ask="jsou v názvech slavných světových filmů",
         inside=["kmotr", "matrix", "čelisti", "psycho", "gladiátor",
                 "pianista", "titanic", "avatar"]),
    dict(id="nazev-serialy", level="normal",
         roof="slova z názvů českých seriálů",
         ask="jsou v názvech českých seriálů",
         inside=["nemocnice", "sanitka", "chalupář", "cirkus", "dětství",
                 "pult", "případ", "návštěvník"]),
    dict(id="nazev-gott", level="normal",
         roof="slova z názvů písní Karla Gotta",
         ask="jsou v názvech písní Karla Gotta",
         inside=["trezor", "včelka", "káva", "zvonek", "růže", "štěstí",
                 "srdce", "paganini"]),
    dict(id="nazev-baje", level="normal",
         roof="slova z rčení, která pocházejí z antických bájí",
         ask="jsou v rčeních z antických bájí",
         inside=["pata", "nit", "kůň", "skříňka", "meč", "chlév", "uzel",
                 "jablko"]),
    dict(id="nazev-sindibad", level="normal",
         roof="slova z příběhů Tisíce a jedné noci",
         ask="jsou v příbězích Tisíce a jedné noci",
         inside=["lampa", "koberec", "sezam", "jeskyně", "loupežník", "duch",
                 "plavba", "poklad"]),
    dict(id="nazev-dumas", level="normal",
         roof="slova z názvů knih Alexandra Dumase",
         ask="jsou v názvech knih Alexandra Dumase",
         inside=["mušketýr", "hrabě", "královna", "tulipán", "dáma",
                 "vikomt", "maska", "kamélie"]),

    dict(id="nazev-foglar", level="hard",
         roof="slova z názvů knih Jaroslava Foglara",
         ask="jsou v názvech knih Jaroslava Foglara",
         inside=["hoši", "řeka", "záhada", "hlavolam", "stínadla",
                 "tajemství", "chata", "poklad", "delfín", "kotlina"]),
    dict(id="nazev-verne", level="hard",
         roof="slova z názvů knih Julese Verna",
         ask="jsou v názvech knih Julese Verna",
         inside=["cesta", "ostrov", "prázdniny", "kapitán", "střed", "balón",
                 "míle", "ocel", "moře", "země"]),
    dict(id="nazev-neruda", level="hard",
         roof="slova z názvů Malostranských povídek",
         ask="jsou v názvech Nerudových Malostranských povídek",
         inside=["hastrman", "lilie", "pěnovka", "žebrák", "mizina", "mše",
                 "týden", "figurky", "dušičky", "kazisvět"]),
    dict(id="nazev-jirasek", level="hard",
         roof="slova ze Starých pověstí českých",
         ask="jsou v názvech Starých pověstí českých",
         inside=["praotec", "dcera", "proroctví", "válka", "blaník",
                 "kouzelník", "horymír", "bruncvík"]),
    dict(id="nazev-nemcova", level="hard",
         roof="slova z názvů pohádek Boženy Němcové",
         ask="jsou v názvech pohádek Boženy Němcové",
         inside=["krkavec", "meč", "měsíček", "sůl", "zlato", "horákyně",
                 "bajaja", "větrník", "káča", "mikeš"]),
    dict(id="nazev-smetana", level="hard",
         roof="slova z názvů Smetanových oper",
         ask="jsou v názvech Smetanových oper",
         inside=["nevěsta", "hubička", "tajemství", "stěna", "vdova",
                 "braniboři", "viola", "dalibor"]),
    dict(id="nazev-dvorak", level="hard",
         roof="slova z názvů oper Dvořáka a Janáčka",
         ask="jsou v názvech oper Dvořáka a Janáčka",
         inside=["rusalka", "čert", "káča", "jakobín", "liška", "věc",
                 "uhlíř", "palice", "výlet", "armida"]),
    dict(id="nazev-hitchcock", level="hard",
         roof="slova z názvů Hitchcockových filmů",
         ask="jsou v názvech Hitchcockových filmů",
         inside=["ptáci", "okno", "dvůr", "lano", "závrať", "sever",
                 "cizinec", "podezření", "stupně", "vlak"]),
    dict(id="nazev-sverak", level="hard",
         roof="slova z názvů Svěrákových filmů",
         ask="jsou v názvech Svěrákových filmů",
         inside=["kolja", "lahve", "škola", "svět", "strniště", "kuky",
                 "akumulátor", "jízda", "sezóna", "bos"]),
    dict(id="nazev-muzikaly", level="hard",
         roof="slova z názvů českých muzikálů",
         ask="jsou v názvech českých muzikálů",
         inside=["dracula", "bídníci", "krysař", "noc", "karlštejn",
                 "kleopatra", "rebelové", "excalibur"]),
    dict(id="nazev-kryl", level="hard",
         roof="slova z názvů písní Karla Kryla",
         ask="jsou v názvech písní Karla Kryla",
         inside=["anděl", "vrátka", "salome", "veličenstvo", "kat",
                 "karavana", "mrak", "bratříček", "revolta", "vojín"]),
    dict(id="nazev-nohavica", level="hard",
         roof="slova z názvů písní Jaromíra Nohavici",
         ask="jsou v názvech písní Jaromíra Nohavici",
         inside=["kometa", "sarajevo", "hlídač", "kráva", "zima", "století",
                 "voják", "věž"]),
    dict(id="nazev-werich", level="hard",
         roof="slova z názvů pohádek z Fimfára",
         ask="jsou v názvech pohádek z Werichova Fimfára",
         inside=["listí", "dub", "barka", "veterán", "koloběžka", "rozum",
                 "štěstí", "paleček"]),
    dict(id="nazev-ota-pavel", level="hard",
         roof="slova z názvů knih Oty Pavla",
         ask="jsou v názvech knih Oty Pavla",
         inside=["srnec", "ryba", "pohár", "bedna", "úhoř", "běh", "syn",
                 "celer"]),
    dict(id="nazev-basnici", level="hard",
         roof="slova z názvů sbírek Nezvala a Seiferta",
         ask="jsou v názvech sbírek Nezvala a Seiferta",
         inside=["šáteček", "maminka", "píseň", "sloup", "deštník", "edison",
                 "viktorka", "ruce", "jaro", "hrobař"]),
    dict(id="nazev-holmes", level="hard",
         roof="slova z názvů případů Sherlocka Holmese",
         ask="jsou v názvech případů Sherlocka Holmese",
         inside=["studie", "znamení", "karbunkule", "figurky", "údolí",
                 "pás", "napoleon", "případ"]),
]


# ------------------------------------------------------------- stavitel ---

def zkontroluj_vetu(ask: str) -> None:
    """Otázka musí sedět do věty „Čtyři z nich …".

    Rozbíjejí to tři věci: jednotné číslo („je to polévka"), příklonka na
    špatném místě („čtou se stejně" místo „se čtou stejně") a zástupka za
    slovo, které už stojí v podmětu („sedá se na ně").
    """
    # „jsou to …" je v pořádku: stavitel sady si to „to" po podmětu sám
    # ubere (viz in_sentence v 9_build_intruder.py), takže se kontroluje až
    # zbytek věty.
    zbytek = ask[len("jsou to "):] if ask.startswith("jsou to ") else ask
    spatne = ["je to ", "bývá to ", " to ", " je ", " ně ", " jim "]
    for kus in spatne:
        if zbytek.startswith(kus.lstrip()) or kus in zbytek:
            raise SystemExit(f"otázka nesedí do rámce Čtyři z nich: {ask!r} ({kus!r})")


def decoys(rodina: dict, slova: list[str], rng: random.Random) -> list[str]:
    """Tři zavádějící věty, u kterých je jisté, že nevydělují vetřelce."""
    out = []
    for ask in rng.sample(BANKA, len(BANKA)):
        if ask == rodina["ask"] or ask in rodina.get("avoid_asks", []):
            continue
        rule = OVERITELNE.get(ask)
        if rule and any(PRAVIDLA[rule](w) for w in slova):
            continue
        out.append(ask)
        if len(out) == 3:
            break
    if len(out) < 3:
        raise SystemExit(f"{rodina['id']}: nezbyly tři zavádějící věty")
    return out


# Pravidlo -> seznam, ve kterém se hledá. Jen pro pravidla, která něco
# schovávají; ostatní (počet samohlásek, pořadí písmen) žádnou násadu nemají.
NASADA_PRAVIDLA = {
    "skryte-cislo": lambda: CISLA,
    "skryte-telo": lambda: TELO,
    "skryty-stat": lambda: STATY,
}


def nasada(rule: str, word: str) -> str | None:
    """Co se v tom slově schovává — nejdelší shoda, ať sedí i „deset" proti „set"."""
    seznam = NASADA_PRAVIDLA.get(rule)
    if not seznam:
        return None
    low = word.lower()
    hits = [x for x in seznam() if x in low]
    return max(hits, key=len) if hits else None


def postav(rng: random.Random) -> list[dict]:
    slovnik_slov = slovnik()
    vata = VATA.split()

    # Nejdřív se poskládají slova uvnitř všech rodin — teprve pak se z vaty
    # vybírají slova vně, aby se dalo vyhodit všechno, co uvnitř někde leží.
    hotove = []
    for spec in MECH:
        pravidlo = PRAVIDLA[spec["rule"]]
        ban = set(spec.get("ban", []))
        nasel = [w for w in slovnik_slov if w not in ban and pravidlo(w)]
        for w in spec.get("extra", []):
            if pravidlo(w) and w not in nasel and w not in ban:
                nasel.append(w)
            elif not pravidlo(w):
                raise SystemExit(f"{spec['id']}: ruční slovo {w!r} pravidlu nevyhovuje")
        hotove.append(dict(spec, inside=nasel[:spec.get("want", 12)]))
    for spec in ZNALOSTNI:
        hotove.append(dict(spec, inside=list(spec["inside"])))

    uvnitr = {w for r in hotove for w in r["inside"]}

    rodiny = []
    for r in hotove:
        if len(r["inside"]) < 6:
            raise SystemExit(f"{r['id']}: jen {len(r['inside'])} slov uvnitř")
        zkontroluj_vetu(r["ask"])

        volna = [w for w in vata
                 if w not in uvnitr and w not in r.get("avoid", [])]
        if "rule" in r:
            volna = [w for w in volna if not PRAVIDLA[r["rule"]](w)]

        # Vetřelec nesmí trčet délkou. Rodiny s pravidlem o písmenech mají
        # slova často krátká (krk, díl, most) a kdyby k nim skript přisadil
        # „prostěradlo", pozná ho hráč, aniž by o pravidle věděl.
        kratke = min(len(w) for w in r["inside"])
        dlouhe = max(len(w) for w in r["inside"])
        vlastni = random.Random(r["id"])
        for rezerva in (1, 2, 3, 99):
            sedi = [w for w in volna if kratke - rezerva <= len(w) <= dlouhe + rezerva]
            if len(sedi) >= 12:
                break
        outside = vlastni.sample(sedi, min(12, len(sedi)))
        if len(outside) < 8:
            raise SystemExit(f"{r['id']}: jen {len(outside)} slov vně")

        skryte = {}
        for w in r["inside"]:
            found = nasada(r.get("rule", ""), w)
            if found:
                skryte[w] = found

        rodiny.append({
            "id": r["id"],
            "roof": r["roof"],
            "level": r["level"],
            "hidden": True,
            "inside": r["inside"],
            "outside": sorted(outside),
            "asks": [r["ask"]] + decoys(r, r["inside"] + outside, vlastni),
            **({"skryte": skryte} if skryte else {}),
        })
    return rodiny


HLAVICKA = '''"""Sedmá várka rodin — osmdesát skrytých střech.

TENHLE SOUBOR PÍŠE SKRIPT. Ruční úpravy zmizí při dalším spuštění; opravovat
se má `tools/gen_families7.py`, kde stojí zadání i kontroly.

Všechny rodiny tady jsou **skryté**: nad pěticí není vidět střecha, takže se
hráč nemá čeho chytit, dokud souvislost nenajde sám. Rodiny s pravidlem
o písmenech si slova našel skript ve slovníku hry a pravidlo ověřil slovo po
slovu — dovnitř i ven. Znalostní rodiny (sýry, opery, stanice metra) mají
slova uvnitř psaná ručně, slova vně vybral skript z nudné zásoby a ověřil,
že ani jedno z nich neleží uvnitř žádné z osmdesáti rodin.
"""

FAMILIES7 = ['''


def zapis(rodiny: list[dict]) -> None:
    kusy = [HLAVICKA]
    for r in rodiny:
        kusy.append("    {")
        kusy.append(f"        \"id\": {r['id']!r},")
        kusy.append(f"        \"roof\": {r['roof']!r},")
        kusy.append(f"        \"level\": {r['level']!r},")
        kusy.append("        \"hidden\": True,")
        for klic in ("inside", "outside"):
            kusy.append(f"        \"{klic}\": [")
            radek = "           "
            for w in r[klic]:
                kus = f" {w!r},"
                if len(radek) + len(kus) > 78:
                    kusy.append(radek)
                    radek = "           "
                radek += kus
            kusy.append(radek)
            kusy.append("        ],")
        if r.get("skryte"):
            kusy.append("        \"skryte\": {")
            for w, n in sorted(r["skryte"].items()):
                kusy.append(f"            {w!r}: {n!r},")
            kusy.append("        },")
        kusy.append("        \"asks\": [")
        for a in r["asks"]:
            kusy.append(f"            {a!r},")
        kusy.append("        ],")
        kusy.append("    },")
    kusy.append("]")
    text = "\n".join(kusy).replace("'", '"') + "\n"
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write(text)


def main() -> int:
    rng = random.Random(11)
    rodiny = postav(rng)

    # Otázka je klíč rodiny, takže se nesmí opakovat ani uvnitř várky, ani
    # proti rodinám, které v sadě už jsou.
    sys.path.insert(0, HERE)
    from intruder_families import FAMILIES as STARE  # noqa: E402
    # Sada už tuhle várku obsahuje (je do ní zapojená), takže se při
    # porovnávání musí vyjmout — jinak by si každá rodina překážela sama.
    moje = {r["id"] for r in rodiny}
    stare = {f["asks"][0] for f in STARE if f["id"] not in moje}
    videne = set()
    for r in rodiny:
        ask = r["asks"][0]
        if ask in stare:
            raise SystemExit(f"{r['id']}: otázka už patří jiné rodině — {ask!r}")
        if ask in videne:
            raise SystemExit(f"dvě rodiny mají tutéž otázku: {ask!r}")
        videne.add(ask)

    zapis(rodiny)
    po_urovni: dict[str, int] = {}
    for r in rodiny:
        po_urovni[r["level"]] = po_urovni.get(r["level"], 0) + 1
    print(f"rodin: {len(rodiny)}  " + "  ".join(
        f"{k}: {v}" for k, v in sorted(po_urovni.items())))
    for r in rodiny:
        print(f"  {r['id']:26} {r['level']:6} {len(r['inside']):3} uvnitř, "
              f"{len(r['outside']):3} vně   {' '.join(r['inside'][:8])}")
    print(f"-> {os.path.normpath(OUT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
