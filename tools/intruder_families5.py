"""Pátá dávka — **skryté** rodiny.

Tady čtyři slova na první pohled vůbec nesouvisí. Nespojuje je význam ani
mluvnice, ale něco, na co se musí přijít: že jsou v názvech oscarových
filmů, že se čtou stejně pozpátku, že jsou to zároveň česká města. Páté
slovo je obyčejné slovo, které do té skryté souvislosti nepatří.

Zavádějící věty jsou tu jiné než u ostatních rodin: nabízejí **jiné
skryté souvislosti**, které pro tu pětici prostě neplatí. Nevydělují tedy
nikoho a hádanku nerozbijí — jen se hráč musí rozhodnout, která z těch
tří nabídek na těch pět slov opravdu sedí.

`hidden` značí rodinu tohohle druhu; generátor jich do hry pouští
zhruba polovinu ze všech hádanek.
"""

HIDDEN = [
    {
        "id": "skryte-oscar",
        "roof": "slova z názvů filmů oceněných Oscarem za nejlepší film",
        "level": "hard",
        "hidden": True,
        "inside": ["návrat", "parazit", "mlčení", "gladiátor", "kmotr", "pacient",
                   "četa", "umělec", "tanec", "řidič", "krása", "moonlight"],
        "outside": ["polštář", "kohoutek", "závěs", "šroubovák", "tráva", "mrkev",
                    "vidlička", "cihla", "provaz", "kotva", "svetr", "police"],
        "asks": [
            "jsou v názvech filmů, které dostaly Oscara za nejlepší film",
            "jsou v názvech her Járy Cimrmana",
            "jsou to zároveň česká města",
            "čtou se stejně zepředu i zezadu",
            "jsou v názvech Shakespearových her",
            "jsou to příjmení českých prezidentů",
        ],
    },
    {
        "id": "skryte-palindrom",
        "roof": "slova, která se čtou stejně pozpátku",
        "level": "hard",
        "hidden": True,
        "inside": ["kajak", "oko", "radar", "krk", "tahat", "potop", "kuk",
                   "madam", "nepochopen", "kobylka? ne", "kajaky? ne"],
        "outside": ["stůl", "kniha", "zahrada", "polštář", "mrkev", "obraz",
                    "vlak", "chleba", "brambora", "kabát", "sklenice", "lampa"],
        "asks": [
            "čtou se stejně zepředu i zezadu",
            "jsou to zároveň česká města",
            "jsou v názvech oscarových filmů",
            "jsou to znamení zvěrokruhu",
            "jsou to příjmení českých prezidentů",
            "jsou v názvech her Járy Cimrmana",
        ],
    },
    {
        "id": "skryte-cimrman",
        "roof": "slova z názvů her Járy Cimrmana",
        "level": "hard",
        "hidden": True,
        "inside": ["blaník", "švestka", "záskok", "lijavec", "posel", "dobytí",
                   "hospoda", "vyšetřování", "afrika", "němý"],
        "outside": ["koberec", "zrcadlo", "hrábě", "svíčka", "meloun", "trakař",
                    "žebřík", "konev", "plot", "kastrol", "rohožka", "buchta"],
        "asks": [
            "jsou v názvech her Járy Cimrmana",
            "jsou v názvech oscarových filmů",
            "jsou to zároveň česká města",
            "jsou to znamení zvěrokruhu",
            "čtou se stejně zepředu i zezadu",
            "jsou v názvech Shakespearových her",
        ],
    },
    {
        "id": "skryte-mesta",
        "roof": "slova, která jsou zároveň jménem českého města",
        "level": "hard",
        "hidden": True,
        "inside": ["písek", "most", "brod", "lom", "police", "ostrov", "kamenice",
                   "bystřice", "jesenice", "bílina", "kout", "hora"],
        "outside": ["polštář", "vidlička", "žárovka", "šroub", "koště", "hrnec",
                    "svetr", "ubrus", "propiska", "žehlička", "kravata", "deštník"],
        "asks": [
            "jsou to zároveň jména českých měst",
            "jsou v názvech oscarových filmů",
            "čtou se stejně zepředu i zezadu",
            "jsou to znamení zvěrokruhu",
            "jsou v názvech her Járy Cimrmana",
            "jsou to příjmení českých prezidentů",
        ],
    },
    {
        "id": "skryte-prezidenti",
        "roof": "slova, která jsou zároveň příjmením českého prezidenta",
        "level": "hard",
        "hidden": True,
        "inside": ["svoboda", "havel", "pavel", "zeman", "beneš", "klaus",
                   "hácha", "masaryk", "husák", "novotný"],
        "outside": ["novák", "dvořák", "procházka", "kučera", "veselý", "horák",
                    "němec", "pokorný", "marek", "urban", "sedlák", "fiala"],
        "asks": [
            "jsou to zároveň příjmení českých prezidentů",
            "jsou to zároveň jména českých měst",
            "jsou v názvech oscarových filmů",
            "čtou se stejně zepředu i zezadu",
            "jsou to znamení zvěrokruhu",
            "jsou v názvech her Járy Cimrmana",
        ],
    },
    {
        "id": "skryte-zverokruh",
        "roof": "slova, která jsou zároveň znamením zvěrokruhu",
        # Zvěrokruh zná každý. Mezi zvířaty trčí „panna" a „váhy" na první
        # pohled, takže to není střední obtížnost, ať je souvislost jakkoli
        # skrytá — skrytá znamená „nevidíš ji z toho, co ta slova znamenají",
        # ne „je těžká".
        "level": "easy",
        "hidden": True,
        "inside": ["býk", "rak", "lev", "panna", "štír", "váhy", "blíženci",
                   "ryby", "beran", "kozoroh", "vodnář", "střelec"],
        "outside": ["vlk", "medvěd", "kůň", "liška", "veverka", "sova", "kapr",
                    "tygr", "orel", "zajíc", "myš", "husa"],
        "asks": [
            "jsou to znamení zvěrokruhu",
            "jsou to zároveň jména českých měst",
            "jsou v názvech oscarových filmů",
            "čtou se stejně zepředu i zezadu",
            "jsou to příjmení českých prezidentů",
            "jsou v názvech Shakespearových her",
        ],
    },
    {
        "id": "skryte-shakespeare",
        "roof": "slova z názvů Shakespearových her",
        "level": "hard",
        "hidden": True,
        "inside": ["bouře", "sen", "kupec", "zkrocení", "večer", "veselé",
                   "komedie", "omylů", "král", "zimní"],
        "outside": ["hrneček", "utěrka", "žebřík", "batoh", "kolotoč", "kbelík",
                    "punčocha", "trumpeta", "šuplík", "podložka", "vějíř", "sud"],
        "asks": [
            "jsou v názvech Shakespearových her",
            "jsou v názvech oscarových filmů",
            "jsou v názvech her Járy Cimrmana",
            "jsou to zároveň jména českých měst",
            "čtou se stejně zepředu i zezadu",
            "jsou to znamení zvěrokruhu",
        ],
    },
    {
        "id": "skryte-znacky-aut",
        "roof": "slova, která jsou zároveň značkou nebo modelem auta",
        "level": "hard",
        "hidden": True,
        "inside": ["škoda", "tatra", "jaguár", "mustang", "beruška", "fabie",
                   "octavie", "avia", "zetor", "praga"],
        "outside": ["polička", "hrnek", "rukavice", "koláč", "kapesník", "lopata",
                    "žehlicí prkno", "papír", "obálka", "kartáč", "ponožka", "váza"],
        "asks": [
            "jsou to zároveň značky nebo modely aut",
            "jsou to zároveň jména českých měst",
            "jsou v názvech oscarových filmů",
            "jsou to znamení zvěrokruhu",
            "čtou se stejně zepředu i zezadu",
            "jsou v názvech her Járy Cimrmana",
        ],
    },
    {
        "id": "skryte-pohadky",
        "roof": "slova z názvů českých filmových pohádek",
        "level": "normal",
        "hidden": True,
        "inside": ["popelka", "princezna", "oříšky", "mrazík", "pyšná", "sedmikrásky? ne",
                   "šípková", "růženka", "královna", "sůl"],
        "outside": ["kladivo", "šroubovák", "termoska", "kravata", "sekačka",
                    "regál", "trouba", "koberec", "kroužek", "špendlík", "provázek"],
        "asks": [
            "jsou v názvech českých filmových pohádek",
            "jsou v názvech oscarových filmů",
            "jsou to zároveň jména českých měst",
            "jsou to znamení zvěrokruhu",
            "čtou se stejně zepředu i zezadu",
            "jsou v názvech Shakespearových her",
        ],
    },
    {
        "id": "skryte-karty",
        "roof": "slova, která jsou zároveň barvou nebo figurou v kartách",
        # Srdce, kule, žaludy, listy — mariáš zná každý a čtveřice se pozná
        # dřív, než ji hráč stihne přečíst. Skrytá souvislost sama o sobě
        # obtížnost nedělá; dělá ji to, jak dlouho se hledá.
        "level": "easy",
        "hidden": True,
        "inside": ["srdce", "kule", "žaludy", "listy", "eso", "král", "dáma",
                   "spodek", "kříže", "piky"],
        "outside": ["hřebík", "svetr", "polička", "meloun", "kbelík", "ubrousek",
                    "lampa", "váleček", "hadr", "koště", "police", "sluchátka"],
        "asks": [
            "jsou to zároveň barvy nebo figury v kartách",
            "jsou to znamení zvěrokruhu",
            "jsou v názvech oscarových filmů",
            "jsou to zároveň jména českých měst",
            "čtou se stejně zepředu i zezadu",
            "jsou to příjmení českých prezidentů",
        ],
    },
    {
        "id": "skryte-znamky",
        "roof": "slova, která jsou zároveň značkou českého piva",
        "level": "hard",
        "hidden": True,
        "inside": ["kozel", "bernard", "radegast", "svijany", "primátor", "krakonoš",
                   "poutník", "rychtář", "hostan"],
        "outside": ["mixér", "žebřík", "kolébka", "pravítko", "sponka", "korek",
                    "násada", "ubrus", "šátek", "nůžky", "sklo", "koš"],
        "asks": [
            "jsou to zároveň značky českého piva",
            "jsou to zároveň jména českých měst",
            "jsou to příjmení českých prezidentů",
            "jsou v názvech oscarových filmů",
            "jsou to znamení zvěrokruhu",
            "čtou se stejně zepředu i zezadu",
        ],
    },
    {
        "id": "skryte-planety-bohove",
        "roof": "slova, která jsou jménem antického boha i planety",
        "level": "hard",
        "hidden": True,
        "inside": ["Mars", "Venuše", "Jupiter", "Merkur", "Saturn", "Neptun", "Uran"],
        "outside": ["Sirius", "Vega", "Polárka", "Kasiopeja", "Andromeda", "Orion",
                    "Pegas", "Herkules", "Drak"],
        "asks": [
            "jsou to zároveň planety i antičtí bohové",
            "jsou to znamení zvěrokruhu",
            "jsou to zároveň jména českých měst",
            "jsou v názvech oscarových filmů",
            "čtou se stejně zepředu i zezadu",
            "jsou v názvech her Járy Cimrmana",
        ],
    },
]

# Vyčištění: slova s poznámkou „? ne" byla při psaní zamítnuta.
for _f in HIDDEN:
    _f["inside"] = [w for w in _f["inside"] if "? ne" not in w]
    _f["outside"] = [w for w in _f["outside"] if "? ne" not in w]
