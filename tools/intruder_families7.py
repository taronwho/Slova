"""Sedmá várka rodin — osmdesát skrytých střech.

TENHLE SOUBOR PÍŠE SKRIPT. Ruční úpravy zmizí při dalším spuštění; opravovat
se má `tools/gen_families7.py`, kde stojí zadání i kontroly.

Všechny rodiny tady jsou **skryté**: nad pěticí není vidět střecha, takže se
hráč nemá čeho chytit, dokud souvislost nenajde sám. Rodiny s pravidlem
o písmenech si slova našel skript ve slovníku hry a pravidlo ověřil slovo po
slovu — dovnitř i ven. Znalostní rodiny (sýry, opery, stanice metra) mají
slova uvnitř psaná ručně, slova vně vybral skript z nudné zásoby a ověřil,
že ani jedno z nich neleží uvnitř žádné z osmdesáti rodin.
"""

FAMILIES7 = [
    {
        "id": "mech-abecedni-poradi",
        "roof": "slova, jejichž písmena jdou v abecedním pořadí",
        "level": "normal",
        "hidden": True,
        "inside": [
            "nůž", "most", "dělo", "déšť", "koš", "cent", "chips", "adept",
            "los", "kos", "nos", "dost",
        ],
        "outside": [
            "dřez", "guma", "hrábě", "hřebík", "kleště", "kolík", "konev",
            "krém", "kýbl", "mrkev", "pračka", "sud",
        ],
        "asks": [
            "mají písmena seřazená podle abecedy",
            "jsou v názvech večerníčků",
            "jsou to zároveň značky českého piva",
            "jsou v názvech Shakespearových her",
        ],
    },
    {
        "id": "mech-stejne-kraje",
        "roof": "slova, která začínají i končí stejným písmenem",
        "level": "normal",
        "hidden": True,
        "inside": [
            "okno", "vliv", "existence", "cizinec", "dohled", "režisér",
            "knoflík", "kotník", "maximum", "transport", "reportér", "servis",
        ],
        "outside": [
            "komoda", "konev", "peněženka", "police", "popelnice", "sešit",
            "silnice", "smeták", "záclona", "zápisník", "řetízek", "žehlička",
        ],
        "asks": [
            "začínají a končí stejným písmenem",
            "čtou se stejně zepředu i zezadu",
            "jsou to zároveň příjmení českých prezidentů",
            "jsou to zároveň značky nebo modely aut",
        ],
    },
    {
        "id": "mech-skryte-cislo",
        "roof": "slova, ve kterých se schovává číslo",
        "level": "normal",
        "hidden": True,
        "inside": [
            "střih", "stodola", "výstřih", "hustota", "kosmonaut", "dystopie",
            "manšestr", "mastodont", "místodržící", "podvazek", "stoh",
            "město",
        ],
        "outside": [
            "brambora", "hoblík", "kolík", "koště", "kýbl", "motyka",
            "náramek", "pouzdro", "pytel", "svěrák", "ubrus", "šroub",
        ],
        "skryte": {
            "dystopie": "sto",
            "hustota": "sto",
            "kosmonaut": "osm",
            "manšestr": "šest",
            "mastodont": "sto",
            "místodržící": "sto",
            "město": "sto",
            "podvazek": "dva",
            "stodola": "sto",
            "stoh": "sto",
            "střih": "tři",
            "výstřih": "tři",
        },
        "asks": [
            "mají v sobě schované číslo",
            "jsou to zároveň značky nebo modely aut",
            "čtou se stejně zepředu i zezadu",
            "mají v sobě dvě stejná písmena vedle sebe",
        ],
    },
    {
        "id": "mech-skryte-telo",
        "roof": "slova, ve kterých se schovává část těla",
        "level": "normal",
        "hidden": True,
        "inside": [
            "prsten", "rukavice", "protokol", "dokončení", "sucho",
            "dinosaurus", "pokolení", "dekret", "lopata", "hluchota",
            "ionosféra", "kabanos",
        ],
        "outside": [
            "guma", "houpačka", "hrnec", "hrneček", "kolík", "pinzeta",
            "pračka", "rohožka", "struhadlo", "vana", "žebřík", "žehlička",
        ],
        "skryte": {
            "dekret": "ret",
            "dinosaurus": "nos",
            "dokončení": "oko",
            "hluchota": "ucho",
            "ionosféra": "nos",
            "kabanos": "nos",
            "lopata": "pata",
            "pokolení": "oko",
            "protokol": "oko",
            "prsten": "prst",
            "rukavice": "ruka",
            "sucho": "ucho",
        },
        "asks": [
            "mají v sobě schovanou část těla",
            "jsou to zároveň příjmení českých prezidentů",
            "jsou to zároveň značky českého piva",
            "jsou v názvech večerníčků",
        ],
    },
    {
        "id": "mech-stejna-samohlaska",
        "roof": "slova, která mají ve všech slabikách stejnou samohlásku",
        "level": "normal",
        "hidden": True,
        "inside": [
            "pomoc", "nápad", "dveře", "doktor", "zpráva", "kamarád",
            "zábava", "děvče", "kolo", "okno", "ostrov", "motor",
        ],
        "outside": [
            "hadice", "hoblík", "hřebík", "komoda", "květináč", "lavička",
            "matrace", "peřina", "postel", "ramínko", "vařečka", "věšák",
        ],
        "asks": [
            "mají ve všech slabikách stejnou samohlásku",
            "čtou se stejně zepředu i zezadu",
            "mají v sobě dvě stejná písmena vedle sebe",
            "nemají v sobě ani jednu samohlásku",
        ],
    },
    {
        "id": "mech-samohlaska-kraje",
        "roof": "slova, která začínají i končí samohláskou",
        "level": "normal",
        "hidden": True,
        "inside": [
            "informace", "otázka", "osoba", "ulice", "okno", "alibi", "opice",
            "ovoce", "opatření", "úsilí", "otevření", "očekávání",
        ],
        "outside": [
            "batoh", "guma", "houpačka", "hrábě", "hřebík", "kolík", "mrkev",
            "náramek", "propiska", "ramínko", "řetízek", "šála",
        ],
        "asks": [
            "začínají i končí samohláskou",
            "jsou to zároveň značky nebo modely aut",
            "jsou to zároveň jména českých měst",
            "mají v sobě dvě stejná písmena vedle sebe",
        ],
    },
    {
        "id": "mech-tri-souhlasky",
        "roof": "slova se třemi souhláskami za sebou",
        "level": "normal",
        "hidden": True,
        "inside": [
            "srdce", "sestra", "zpráva", "prsten", "vzduch", "zdroj",
            "ostrov", "prsa", "strom", "mistr", "partner", "chleba",
        ],
        "outside": [
            "hodinky", "lavička", "lednička", "pekáč", "pilník", "police",
            "ponožka", "silnice", "sud", "tácek", "zahrada", "žebřík",
        ],
        "asks": [
            "mají v sobě tři souhlásky za sebou",
            "nemají v sobě ani jednu samohlásku",
            "jsou v názvech her Járy Cimrmana",
            "jsou to zároveň příjmení českých prezidentů",
        ],
    },
    {
        "id": "mech-dvojhlaska",
        "roof": "slova s dvojhláskou",
        "level": "normal",
        "hidden": True,
        "inside": [
            "autobus", "součást", "souboj", "spoušť", "trauma", "soubor",
            "trouba", "kloub", "automat", "inkoust", "soudkyně", "doutník",
        ],
        "outside": [
            "brýle", "hřeben", "lavička", "matrace", "motyka", "pinzeta",
            "silnice", "sušák", "ubrus", "vysavač", "věšák", "záclona",
        ],
        "asks": [
            "mají v sobě dvojhlásku ou, au nebo eu",
            "jsou to zároveň jména českých měst",
            "mají v sobě schované zvíře",
            "jsou v názvech večerníčků",
        ],
    },
    {
        "id": "mech-dvakrat-dvojice",
        "roof": "slova, ve kterých se dvojice písmen opakuje",
        "level": "normal",
        "hidden": True,
        "inside": [
            "štěstí", "odchod", "piknik", "příměří", "ničení", "informátor",
            "džentlmen", "ukázka", "učebnice", "recepce", "předsedkyně",
            "losos",
        ],
        "outside": [
            "branka", "dřez", "kolík", "komoda", "konev", "matice", "myčka",
            "pekáč", "pilník", "pravítko", "smeták", "truhlík",
        ],
        "asks": [
            "mají v sobě dvakrát tutéž dvojici písmen",
            "jsou v názvech večerníčků",
            "jsou to znamení zvěrokruhu",
            "jsou to zároveň značky českého piva",
        ],
    },
    {
        "id": "mech-vzacne-pismeno",
        "roof": "slova s písmenem, které je v češtině vzácné",
        "level": "normal",
        "hidden": True,
        "inside": [
            "informace", "legrace", "profesor", "fotka", "kufr", "funkce",
            "kolega", "gentleman", "existence", "fazole", "federace",
            "džungle",
        ],
        "outside": [
            "hoblík", "hrneček", "hrábě", "hřeben", "komoda", "krém",
            "lepidlo", "myčka", "naběračka", "náramek", "podnos", "vana",
        ],
        "asks": [
            "mají v sobě f, g, x nebo w",
            "jsou v názvech her Járy Cimrmana",
            "jsou v názvech Shakespearových her",
            "mají v sobě dvě stejná písmena vedle sebe",
        ],
    },
    {
        "id": "mech-vic-samohlasek",
        "roof": "slova, ve kterých je víc samohlásek než souhlásek",
        "level": "normal",
        "hidden": True,
        "inside": [
            "osoba", "ulice", "autobus", "alibi", "rádio", "opice", "ovoce",
            "úsilí", "očekávání", "využití", "galerie", "komedie",
        ],
        "outside": [
            "hrneček", "hřeben", "hřebík", "kompost", "naběračka", "náramek",
            "nůžky", "peněženka", "pilník", "ručník", "ubrus", "vařečka",
        ],
        "asks": [
            "mají víc samohlásek než souhlásek",
            "jsou to zároveň značky českého piva",
            "jsou v názvech her Járy Cimrmana",
            "jsou to zároveň jména českých měst",
        ],
    },
    {
        "id": "mech-ruzne-samohlasky",
        "roof": "slova, ve kterých se žádná samohláska neopakuje",
        "level": "normal",
        "hidden": True,
        "inside": [
            "hodiny", "informace", "většina", "obličej", "chování", "ulice",
            "znamení", "záležitost", "kalhoty", "skupina", "stanice",
            "noviny",
        ],
        "outside": [
            "houpačka", "kbelík", "lavička", "pekáč", "ponožka", "popelnice",
            "pračka", "silnice", "trakař", "truhlík", "vysavač", "zápisník",
        ],
        "asks": [
            "nemají v sobě dvakrát tutéž samohlásku",
            "jsou to zároveň jména českých měst",
            "jsou v názvech Shakespearových her",
            "jsou to zároveň příjmení českých prezidentů",
        ],
    },
    {
        "id": "mech-prvni-pulka",
        "roof": "slova z písmen první poloviny abecedy",
        "level": "hard",
        "hidden": True,
        "inside": [
            "klíč", "led", "lék", "dech", "ďábel", "alibi", "chleba",
            "chemie", "klec", "ambice", "chemikálie", "dědic",
        ],
        "outside": [
            "brambora", "kompost", "konev", "květináč", "lavička", "mýdlo",
            "polštář", "silnice", "struhadlo", "svěrák", "vysavač", "věšák",
        ],
        "asks": [
            "mají písmena jen z první poloviny abecedy",
            "jsou v názvech her Járy Cimrmana",
            "jsou to zároveň jména českých měst",
            "jsou to zároveň značky nebo modely aut",
        ],
    },
    {
        "id": "mech-bez-opakovani",
        "roof": "dlouhá slova, ve kterých se žádné písmeno neopakuje",
        "level": "hard",
        "hidden": True,
        "inside": [
            "informace", "většina", "obličej", "chování", "kalhoty",
            "skupina", "stanice", "krabice", "jednotka", "koncert", "příklad",
            "majitel",
        ],
        "outside": [
            "hrneček", "lepidlo", "lopatka", "náramek", "pilník", "ponožka",
            "pračka", "rohožka", "sporák", "svěrák", "zahrada", "zápisník",
        ],
        "asks": [
            "mají aspoň sedm písmen a ani jedno se v nich neopakuje",
            "jsou to zároveň příjmení českých prezidentů",
            "jsou v názvech her Járy Cimrmana",
            "jsou to zároveň jména českých měst",
        ],
    },
    {
        "id": "mech-sousedni-pismena",
        "roof": "slova se dvěma písmeny, která jdou po sobě i v abecedě",
        "level": "hard",
        "hidden": True,
        "inside": [
            "štěstí", "starý", "sestra", "cesta", "dopis", "klíč",
            "příležitost", "zábava", "stůl", "děvče", "víno", "prsten",
        ],
        "outside": [
            "guma", "hrnec", "hřeben", "kartáček", "nůžky", "ořezávátko",
            "peněženka", "police", "provaz", "silnice", "záclona", "řetízek",
        ],
        "asks": [
            "mají vedle sebe dvě písmena, která jdou po sobě i v abecedě",
            "jsou v názvech večerníčků",
            "čtou se stejně zepředu i zezadu",
            "nemají v sobě ani jednu samohlásku",
        ],
    },
    {
        "id": "mech-rimske-cislo",
        "roof": "slova jen z písmen římských číslic",
        "level": "hard",
        "hidden": True,
        "inside": [
            "vliv", "div", "mix", "civil", "lid", "cíl", "mim",
        ],
        "outside": [
            "guma", "hrnec", "motyka", "mýdlo", "peřina", "podnos", "provaz",
            "skříň", "smeták", "tácek", "utěrka", "žebřík",
        ],
        "asks": [
            "mají jen písmena, která se používají jako římské číslice",
            "jsou v názvech Shakespearových her",
            "mají v sobě schované zvíře",
            "mají v sobě dvě stejná písmena vedle sebe",
        ],
    },
    {
        "id": "mech-jedna-samohlaska",
        "roof": "slova, ve kterých je jen jedna samohláska",
        "level": "normal",
        "hidden": True,
        "inside": [
            "srdce", "dům", "svět", "loď", "bratr", "klíč", "vtip", "stůl",
            "slib", "prsten", "nůž", "vzduch",
        ],
        "outside": [
            "batoh", "deka", "guma", "hodinky", "kastrol", "kolík", "koště",
            "peřina", "trakař", "řetízek", "šroub", "šála",
        ],
        "asks": [
            "mají v sobě jen jednu jedinou samohlásku",
            "jsou v názvech her Járy Cimrmana",
            "jsou to zároveň příjmení českých prezidentů",
            "jsou to znamení zvěrokruhu",
        ],
    },
    {
        "id": "mech-skryty-stat",
        "roof": "slova, ve kterých se schovává jméno státu",
        "level": "hard",
        "hidden": True,
        "inside": [
            "inkubace", "maximalista", "román", "malina", "malinovka",
            "peruť", "kubatura",
        ],
        "outside": [
            "branka", "hadr", "kleště", "krém", "květináč", "matrace",
            "motyka", "ořezávátko", "polštář", "sklenice", "sušák", "šála",
        ],
        "skryte": {
            "inkubace": "kuba",
            "kubatura": "kuba",
            "malina": "mali",
            "malinovka": "mali",
            "maximalista": "mali",
            "peruť": "peru",
            "román": "omán",
        },
        "asks": [
            "mají v sobě schované jméno státu",
            "jsou to zároveň značky nebo modely aut",
            "čtou se stejně zepředu i zezadu",
            "jsou to znamení zvěrokruhu",
        ],
    },
    {
        "id": "skryte-metro",
        "roof": "slova, která jsou zároveň stanice pražského metra",
        "level": "normal",
        "hidden": True,
        "inside": [
            "anděl", "muzeum", "můstek", "skalka", "háje", "luka", "flora",
            "hůrka", "vyšehrad", "opatov", "motol", "pankrác",
        ],
        "outside": [
            "guma", "hrábě", "hřeben", "kleště", "lavička", "mísa", "nůžky",
            "pilník", "pravítko", "utěrka", "vařečka", "šroub",
        ],
        "asks": [
            "jsou to zároveň stanice pražského metra",
            "jsou v názvech Shakespearových her",
            "mají v sobě dvě stejná písmena vedle sebe",
            "mají v sobě schované zvíře",
        ],
    },
    {
        "id": "skryte-meny",
        "roof": "slova, která jsou zároveň měny",
        "level": "normal",
        "hidden": True,
        "inside": [
            "jen", "libra", "koruna", "real", "marka", "rubl", "dolar",
            "peso", "rand", "won",
        ],
        "outside": [
            "brýle", "kolík", "konev", "pilník", "pouzdro", "silnice", "sud",
            "sušák", "svěrák", "vařečka", "šroub", "žebřík",
        ],
        "asks": [
            "jsou to zároveň měny",
            "jsou to zároveň jména českých měst",
            "jsou to znamení zvěrokruhu",
            "jsou to zároveň značky nebo modely aut",
        ],
    },
    {
        "id": "skryte-recka-pismena",
        "roof": "slova, která jsou zároveň písmena řecké abecedy",
        "level": "normal",
        "hidden": True,
        "inside": [
            "delta", "gama", "beta", "alfa", "omega", "sigma", "jota",
            "kappa", "lambda", "théta",
        ],
        "outside": [
            "deka", "lavička", "matrace", "metr", "mísa", "police", "polštář",
            "postel", "sud", "sušák", "vana", "žebřík",
        ],
        "asks": [
            "jsou to zároveň písmena řecké abecedy",
            "jsou to znamení zvěrokruhu",
            "čtou se stejně zepředu i zezadu",
            "jsou v názvech her Járy Cimrmana",
        ],
    },
    {
        "id": "skryte-ostrovy",
        "roof": "slova, která jsou zároveň ostrovy",
        "level": "normal",
        "hidden": True,
        "inside": [
            "malta", "java", "kuba", "jersey", "man", "bali", "korfu",
            "rhodos", "kréta", "mallorca",
        ],
        "outside": [
            "batoh", "komoda", "kompost", "konev", "květináč", "matice",
            "mýdlo", "police", "pračka", "ručník", "vařečka", "vysavač",
        ],
        "asks": [
            "jsou to zároveň ostrovy",
            "jsou v názvech Shakespearových her",
            "jsou v názvech her Járy Cimrmana",
            "jsou to zároveň značky českého piva",
        ],
    },
    {
        "id": "skryte-karetni-hry",
        "roof": "slova, která jsou zároveň karetní hry",
        "level": "normal",
        "hidden": True,
        "inside": [
            "prší", "oko", "sedma", "žolík", "mariáš", "kanasta", "poker",
            "dáma", "vole", "kvarteto",
        ],
        "outside": [
            "dřez", "hadr", "hodinky", "metr", "mísa", "mýdlo", "polštář",
            "ponožka", "semínko", "sušák", "ubrus", "vysavač",
        ],
        "asks": [
            "jsou to zároveň karetní hry",
            "jsou to zároveň značky nebo modely aut",
            "jsou to zároveň značky českého piva",
            "jsou to znamení zvěrokruhu",
        ],
    },
    {
        "id": "skryte-casopisy",
        "roof": "slova, která jsou zároveň názvy českých časopisů",
        "level": "normal",
        "hidden": True,
        "inside": [
            "blesk", "květy", "respekt", "reflex", "instinkt", "vlasta",
            "mateřídouška", "sluníčko", "junák", "téma",
        ],
        "outside": [
            "bunda", "motyka", "myčka", "mýdlo", "pekáč", "peřina", "sešit",
            "smeták", "trakař", "ubrousek", "věšák", "zápisník",
        ],
        "asks": [
            "jsou to zároveň názvy českých časopisů",
            "jsou to znamení zvěrokruhu",
            "jsou to zároveň značky českého piva",
            "čtou se stejně zepředu i zezadu",
        ],
    },
    {
        "id": "skryte-kapely",
        "roof": "slova, která jsou zároveň názvy českých kapel",
        "level": "normal",
        "hidden": True,
        "inside": [
            "kabát", "katapult", "turbo", "lucie", "kryštof", "olympic",
            "buty", "traband",
        ],
        "outside": [
            "hřebík", "kbelík", "koště", "krém", "myčka", "pravítko", "pytel",
            "ručník", "semínko", "sklenice", "trakař", "utěrka",
        ],
        "asks": [
            "jsou to zároveň názvy českých kapel",
            "jsou to znamení zvěrokruhu",
            "jsou v názvech her Járy Cimrmana",
            "jsou v názvech Shakespearových her",
        ],
    },
    {
        "id": "skryte-hokej",
        "roof": "slova, která jsou zároveň názvy českých hokejových klubů",
        "level": "normal",
        "hidden": True,
        "inside": [
            "kometa", "motor", "energie", "piráti", "rytíři", "oceláři",
            "vlci", "berani", "draci", "indiáni",
        ],
        "outside": [
            "branka", "kbelík", "metr", "mrkev", "mýdlo", "polštář",
            "pouzdro", "provaz", "tácek", "utěrka", "vana", "šroub",
        ],
        "asks": [
            "jsou to zároveň názvy českých hokejových klubů",
            "jsou to znamení zvěrokruhu",
            "jsou to zároveň značky českého piva",
            "jsou v názvech Shakespearových her",
        ],
    },
    {
        "id": "skryte-motorky",
        "roof": "slova, která jsou zároveň názvy motorek a mopedů",
        "level": "normal",
        "hidden": True,
        "inside": [
            "pionýr", "babeta", "stadion", "jawa", "manet", "čezeta",
            "panelka", "kývačka",
        ],
        "outside": [
            "guma", "hoblík", "kýbl", "metr", "mrkev", "postel", "pytel",
            "ramínko", "rýč", "semínko", "sklenice", "smeták",
        ],
        "asks": [
            "jsou to zároveň názvy motorek nebo mopedů",
            "jsou to zároveň jména českých měst",
            "mají v sobě dvě stejná písmena vedle sebe",
            "jsou v názvech večerníčků",
        ],
    },
    {
        "id": "skryte-syry",
        "roof": "slova, která jsou zároveň názvy sýrů",
        "level": "normal",
        "hidden": True,
        "inside": [
            "niva", "hermelín", "lučina", "eidam", "primátor", "javor",
            "madeta", "vysočina", "kmotr", "moravan",
        ],
        "outside": [
            "brýle", "bunda", "houpačka", "kartáček", "květináč", "lavička",
            "naběračka", "pravítko", "rohožka", "rýč", "sklenice", "šroub",
        ],
        "asks": [
            "jsou to zároveň názvy sýrů",
            "jsou to zároveň příjmení českých prezidentů",
            "jsou to znamení zvěrokruhu",
            "mají v sobě dvě stejná písmena vedle sebe",
        ],
    },
    {
        "id": "skryte-tance",
        "roof": "slova, která jsou zároveň tance",
        "level": "normal",
        "hidden": True,
        "inside": [
            "polka", "beseda", "sousedská", "step", "tango", "valčík",
            "mazurka", "kalamajka", "furiant", "rejdovák",
        ],
        "outside": [
            "brýle", "bunda", "kleště", "komoda", "kompost", "květináč",
            "peněženka", "polštář", "pouzdro", "provaz", "semínko", "věšák",
        ],
        "asks": [
            "jsou to zároveň tance",
            "jsou v názvech večerníčků",
            "jsou to zároveň příjmení českých prezidentů",
            "čtou se stejně zepředu i zezadu",
        ],
    },
    {
        "id": "skryte-sladkosti",
        "roof": "slova, která jsou zároveň názvy sladkostí",
        "level": "normal",
        "hidden": True,
        "inside": [
            "míša", "horalka", "tatranka", "kofila", "lentilky", "banán",
            "deli", "fidorka",
        ],
        "outside": [
            "batoh", "bunda", "hoblík", "hrábě", "myčka", "pilník", "polštář",
            "pravítko", "rohožka", "sklenice", "sporák", "struhadlo",
        ],
        "asks": [
            "jsou to zároveň názvy českých sladkostí",
            "mají v sobě dvě stejná písmena vedle sebe",
            "jsou v názvech her Járy Cimrmana",
            "nemají v sobě ani jednu samohlásku",
        ],
    },
    {
        "id": "skryte-mluvnice",
        "roof": "slova, která jsou zároveň mluvnické pojmy",
        "level": "normal",
        "hidden": True,
        "inside": [
            "pád", "rod", "vid", "vzor", "kmen", "spona", "věta", "člen",
            "přípona", "předložka",
        ],
        "outside": [
            "deka", "hrnec", "květináč", "naběračka", "police", "provaz",
            "pytel", "sušák", "svěrák", "utěrka", "vrtačka", "šuplík",
        ],
        "asks": [
            "jsou to zároveň mluvnické pojmy",
            "jsou to znamení zvěrokruhu",
            "jsou v názvech večerníčků",
            "jsou v názvech her Járy Cimrmana",
        ],
    },
    {
        "id": "skryte-divadlo",
        "roof": "slova, která jsou zároveň divadelní pojmy",
        "level": "normal",
        "hidden": True,
        "inside": [
            "opona", "rampa", "prkna", "budka", "kulisa", "šatna", "lóže",
            "jeviště", "zákulisí", "premiéra",
        ],
        "outside": [
            "kleště", "komoda", "metr", "myčka", "mísa", "mýdlo", "peněženka",
            "silnice", "sporák", "ubrus", "řetízek", "šála",
        ],
        "asks": [
            "jsou to zároveň divadelní pojmy",
            "mají v sobě schované zvíře",
            "jsou to zároveň značky nebo modely aut",
            "jsou to znamení zvěrokruhu",
        ],
    },
    {
        "id": "skryte-ucho-oko",
        "roof": "slova, která jsou zároveň části ucha nebo oka",
        "level": "normal",
        "hidden": True,
        "inside": [
            "kladívko", "třmínek", "kovadlinka", "bubínek", "čočka",
            "duhovka", "sítnice", "hlemýžď", "zornice", "bělmo",
        ],
        "outside": [
            "hodinky", "hřeben", "kbelík", "kompost", "konev", "matrace",
            "mrkev", "postel", "pračka", "rohožka", "truhlík", "žebřík",
        ],
        "asks": [
            "jsou to zároveň části ucha nebo oka",
            "jsou to zároveň značky nebo modely aut",
            "mají v sobě schované zvíře",
            "jsou v názvech Shakespearových her",
        ],
    },
    {
        "id": "skryte-pocitac",
        "roof": "slova, která jsou zároveň počítačové pojmy",
        "level": "normal",
        "hidden": True,
        "inside": [
            "plocha", "koš", "složka", "schránka", "brána", "myš", "okno",
            "disk", "sítě", "jádro",
        ],
        "outside": [
            "deka", "hoblík", "hodinky", "kleště", "kolík", "lavička",
            "matrace", "mísa", "náramek", "nůžky", "ručník", "sud",
        ],
        "asks": [
            "jsou to zároveň počítačové pojmy",
            "mají v sobě schované zvíře",
            "nemají v sobě ani jednu samohlásku",
            "jsou v názvech Shakespearových her",
        ],
    },
    {
        "id": "skryte-fotbal",
        "roof": "slova, která jsou zároveň fotbalové pojmy",
        "level": "normal",
        "hidden": True,
        "inside": [
            "roh", "sudí", "brána", "vápno", "prapor", "karta", "hlavička",
            "zeď", "postavení", "nastavení",
        ],
        "outside": [
            "hřebík", "květináč", "lepidlo", "matrace", "náramek", "nůžky",
            "ramínko", "sporák", "vysavač", "věšák", "řetízek", "žehlička",
        ],
        "asks": [
            "jsou to zároveň fotbalové pojmy",
            "jsou to zároveň příjmení českých prezidentů",
            "mají v sobě dvě stejná písmena vedle sebe",
            "nemají v sobě ani jednu samohlásku",
        ],
    },
    {
        "id": "skryte-hory",
        "roof": "slova, která jsou zároveň české hory a vrchy",
        "level": "hard",
        "hidden": True,
        "inside": [
            "praděd", "lysá", "kleť", "boubín", "javorník", "ještěd",
            "radhošť", "klínovec", "čerchov", "smrk",
        ],
        "outside": [
            "dřez", "guma", "hrnec", "hrábě", "metr", "pinzeta", "police",
            "polštář", "skříň", "sud", "ubrousek", "vana",
        ],
        "asks": [
            "jsou to zároveň české hory nebo vrchy",
            "jsou to zároveň příjmení českých prezidentů",
            "jsou to znamení zvěrokruhu",
            "mají v sobě dvě stejná písmena vedle sebe",
        ],
    },
    {
        "id": "skryte-vetry",
        "roof": "slova, která jsou zároveň názvy větrů",
        "level": "hard",
        "hidden": True,
        "inside": [
            "fén", "pasát", "monzun", "bóra", "mistral", "sirocco", "chamsín",
            "buran",
        ],
        "outside": [
            "hadice", "kolík", "komoda", "koště", "pekáč", "peřina",
            "pouzdro", "semínko", "skříň", "smeták", "tácek", "utěrka",
        ],
        "asks": [
            "jsou to zároveň názvy větrů",
            "čtou se stejně zepředu i zezadu",
            "jsou v názvech Shakespearových her",
            "jsou to zároveň značky nebo modely aut",
        ],
    },
    {
        "id": "skryte-divadla",
        "roof": "slova, která jsou zároveň názvy pražských divadel",
        "level": "hard",
        "hidden": True,
        "inside": [
            "kalich", "semafor", "minor", "ypsilon", "rokoko", "disk",
            "studio", "hybernia", "broadway", "komedie",
        ],
        "outside": [
            "guma", "komoda", "květináč", "kýbl", "motyka", "podnos",
            "polštář", "ramínko", "svěrák", "tácek", "vana", "žehlička",
        ],
        "asks": [
            "jsou to zároveň názvy pražských divadel",
            "jsou to zároveň příjmení českých prezidentů",
            "jsou to zároveň jména českých měst",
            "jsou v názvech her Járy Cimrmana",
        ],
    },
    {
        "id": "skryte-nakladatelstvi",
        "roof": "slova, která jsou zároveň názvy nakladatelství",
        "level": "hard",
        "hidden": True,
        "inside": [
            "albatros", "argo", "odeon", "portál", "host", "academia",
            "paseka", "vyšehrad", "torst", "triton",
        ],
        "outside": [
            "bunda", "kompost", "motyka", "naběračka", "smeták", "truhlík",
            "ubrousek", "ubrus", "utěrka", "vrtačka", "záclona", "žebřík",
        ],
        "asks": [
            "jsou to zároveň názvy českých nakladatelství",
            "mají v sobě schované zvíře",
            "čtou se stejně zepředu i zezadu",
            "mají v sobě dvě stejná písmena vedle sebe",
        ],
    },
    {
        "id": "skryte-knihtisk",
        "roof": "slova, která jsou zároveň knihařské a tiskařské pojmy",
        "level": "hard",
        "hidden": True,
        "inside": [
            "hřbet", "patka", "obálka", "vazba", "sazba", "list", "verzálka",
            "korektura", "desky", "předsádka",
        ],
        "outside": [
            "deka", "hadr", "hoblík", "hodinky", "kompost", "koště", "police",
            "silnice", "smeták", "vana", "záclona", "šuplík",
        ],
        "asks": [
            "jsou to zároveň knihařské nebo tiskařské pojmy",
            "jsou to zároveň příjmení českých prezidentů",
            "čtou se stejně zepředu i zezadu",
            "jsou to zároveň značky českého piva",
        ],
    },
    {
        "id": "skryte-stavba",
        "roof": "slova, která jsou zároveň stavební pojmy",
        "level": "hard",
        "hidden": True,
        "inside": [
            "štít", "věnec", "překlad", "sokl", "krov", "žlab", "vazník",
            "ostění", "nadpraží", "podezdívka",
        ],
        "outside": [
            "hoblík", "hřebík", "konev", "krém", "mísa", "naběračka",
            "pravítko", "sud", "tácek", "vařečka", "vrtačka", "šála",
        ],
        "asks": [
            "jsou to zároveň stavební pojmy",
            "jsou v názvech her Járy Cimrmana",
            "jsou to znamení zvěrokruhu",
            "jsou to zároveň značky nebo modely aut",
        ],
    },
    {
        "id": "skryte-noty",
        "roof": "slova, která jsou zároveň značky v notách",
        "level": "hard",
        "hidden": True,
        "inside": [
            "klíč", "koruna", "křížek", "praporek", "tečka", "pomlka",
            "odrážka", "posuvka", "osnova", "taktovka",
        ],
        "outside": [
            "bunda", "hrnec", "hřeben", "mrkev", "police", "ponožka",
            "popelnice", "struhadlo", "svěrák", "ubrus", "věšák", "šroub",
        ],
        "asks": [
            "jsou to zároveň značky v notách",
            "čtou se stejně zepředu i zezadu",
            "mají v sobě dvě stejná písmena vedle sebe",
            "jsou to zároveň příjmení českých prezidentů",
        ],
    },
    {
        "id": "skryte-skladatele",
        "roof": "slova, která jsou zároveň příjmení českých skladatelů",
        "level": "hard",
        "hidden": True,
        "inside": [
            "smetana", "dvořák", "mysliveček", "zelenka", "benda", "fibich",
            "novák", "kalabis", "vejvoda", "zich",
        ],
        "outside": [
            "houpačka", "lepidlo", "nůžky", "polštář", "postel", "ramínko",
            "rohožka", "semínko", "sporák", "svěrák", "ubrus", "žebřík",
        ],
        "asks": [
            "jsou to zároveň příjmení českých skladatelů",
            "jsou to zároveň jména českých měst",
            "jsou v názvech večerníčků",
            "mají v sobě dvě stejná písmena vedle sebe",
        ],
    },
    {
        "id": "skryte-parky",
        "roof": "slova, která jsou zároveň pražské parky",
        "level": "hard",
        "hidden": True,
        "inside": [
            "stromovka", "letná", "kampa", "petřín", "ladronka", "vypich",
            "hvězda", "cibulka", "obora", "grébovka",
        ],
        "outside": [
            "dřez", "hoblík", "hodinky", "houpačka", "kleště", "kolík",
            "mrkev", "mýdlo", "pilník", "ručník", "silnice", "struhadlo",
        ],
        "asks": [
            "jsou to zároveň pražské parky",
            "jsou to zároveň příjmení českých prezidentů",
            "čtou se stejně zepředu i zezadu",
            "jsou to zároveň jména českých měst",
        ],
    },
    {
        "id": "skryte-anglicka",
        "roof": "česká slova, která jsou zároveň anglická slova",
        "level": "hard",
        "hidden": True,
        "inside": [
            "most", "led", "pole", "plot", "list", "rod", "pan", "sad", "let",
            "past",
        ],
        "outside": [
            "batoh", "deka", "hadr", "krém", "mrkev", "myčka", "pytel", "rýč",
            "sušák", "ubrus", "šroub", "šála",
        ],
        "asks": [
            "jsou zároveň anglická slova s jiným významem",
            "jsou v názvech her Járy Cimrmana",
            "nemají v sobě ani jednu samohlásku",
            "čtou se stejně zepředu i zezadu",
        ],
    },
    {
        "id": "skryte-kolo",
        "roof": "slova, která jsou zároveň součásti jízdního kola",
        "level": "hard",
        "hidden": True,
        "inside": [
            "vidlice", "náboj", "sedlo", "plášť", "rám", "blatník", "paprsek",
            "klika", "převodník", "brzda",
        ],
        "outside": [
            "branka", "myčka", "mísa", "peněženka", "popelnice", "rýč",
            "sklenice", "sud", "svěrák", "ubrousek", "utěrka", "vrtačka",
        ],
        "asks": [
            "jsou to zároveň součásti jízdního kola",
            "čtou se stejně zepředu i zezadu",
            "nemají v sobě ani jednu samohlásku",
            "jsou to zároveň značky nebo modely aut",
        ],
    },
    {
        "id": "skryte-bota",
        "roof": "slova, která jsou zároveň části boty",
        "level": "hard",
        "hidden": True,
        "inside": [
            "jazyk", "špička", "pata", "podrážka", "lem", "stélka", "svršek",
            "podpatek", "tkanička", "šněrování",
        ],
        "outside": [
            "kbelík", "mrkev", "pekáč", "pilník", "pouzdro", "silnice",
            "sušák", "vysavač", "věšák", "šuplík", "šála", "žehlička",
        ],
        "asks": [
            "jsou to zároveň části boty",
            "čtou se stejně zepředu i zezadu",
            "mají v sobě dvě stejná písmena vedle sebe",
            "jsou to zároveň značky českého piva",
        ],
    },
    {
        "id": "skryte-okno",
        "roof": "slova, která jsou zároveň části okna nebo dveří",
        "level": "hard",
        "hidden": True,
        "inside": [
            "křídlo", "klika", "práh", "zárubeň", "pant", "rám", "parapet",
            "kování", "zástrč", "sklo",
        ],
        "outside": [
            "bunda", "dřez", "hoblík", "kartáček", "kolík", "lednička",
            "nůžky", "semínko", "silnice", "sklenice", "smeták", "sud",
        ],
        "asks": [
            "jsou to zároveň části okna nebo dveří",
            "jsou to zároveň jména českých měst",
            "mají v sobě dvě stejná písmena vedle sebe",
            "jsou to znamení zvěrokruhu",
        ],
    },
    {
        "id": "skryte-housle",
        "roof": "slova, která jsou zároveň části houslí",
        "level": "hard",
        "hidden": True,
        "inside": [
            "kobylka", "duše", "krk", "hlemýžď", "kolíček", "struna", "šnek",
            "žabka", "smyčec", "hmatník",
        ],
        "outside": [
            "dřez", "krém", "kýbl", "metr", "peřina", "police", "ramínko",
            "rohožka", "smeták", "trakař", "vana", "zahrada",
        ],
        "asks": [
            "jsou to zároveň části houslí",
            "jsou to zároveň značky nebo modely aut",
            "jsou to znamení zvěrokruhu",
            "jsou to zároveň značky českého piva",
        ],
    },
    {
        "id": "nazev-potter",
        "roof": "slova z názvů dílů Harryho Pottera",
        "level": "normal",
        "hidden": True,
        "inside": [
            "kámen", "komnata", "vězeň", "pohár", "řád", "princ", "relikvie",
            "mudrc",
        ],
        "outside": [
            "brýle", "kartáček", "lednička", "matrace", "myčka", "mísa",
            "podnos", "postel", "pravítko", "pračka", "trakař", "šála",
        ],
        "asks": [
            "jsou v názvech dílů Harryho Pottera",
            "jsou to zároveň značky nebo modely aut",
            "čtou se stejně zepředu i zezadu",
            "nemají v sobě ani jednu samohlásku",
        ],
    },
    {
        "id": "nazev-prsten",
        "roof": "slova z názvů dílů Pána prstenů a Hobita",
        "level": "normal",
        "hidden": True,
        "inside": [
            "společenstvo", "prsten", "věž", "návrat", "král", "hobit",
            "poušť", "bitva",
        ],
        "outside": [
            "hřebík", "květináč", "peněženka", "peřina", "popelnice",
            "pravítko", "prostěradlo", "provaz", "pytel", "sud", "truhlík",
            "žehlička",
        ],
        "asks": [
            "jsou v názvech dílů Pána prstenů a Hobita",
            "čtou se stejně zepředu i zezadu",
            "jsou to zároveň příjmení českých prezidentů",
            "jsou to zároveň značky českého piva",
        ],
    },
    {
        "id": "nazev-star-wars",
        "roof": "slova z názvů dílů Star Wars",
        "level": "normal",
        "hidden": True,
        "inside": [
            "hrozba", "klon", "pomsta", "naděje", "impérium", "úder", "síla",
            "vzestup",
        ],
        "outside": [
            "branka", "deka", "hodinky", "kastrol", "lavička", "peřina",
            "pilník", "propiska", "ramínko", "ručník", "ubrus", "věšák",
        ],
        "asks": [
            "jsou v názvech dílů Star Wars",
            "mají v sobě schované zvíře",
            "jsou v názvech večerníčků",
            "jsou v názvech her Járy Cimrmana",
        ],
    },
    {
        "id": "nazev-disney",
        "roof": "slova z názvů disneyovek",
        "level": "normal",
        "hidden": True,
        "inside": [
            "sněhurka", "popelka", "růženka", "trpaslík", "víla", "kráska",
            "zvíře", "království",
        ],
        "outside": [
            "guma", "hřeben", "kleště", "kolík", "květináč", "lepidlo",
            "lopatka", "pekáč", "pravítko", "sud", "vysavač", "šroub",
        ],
        "asks": [
            "jsou v názvech disneyovek",
            "jsou to zároveň značky českého piva",
            "mají v sobě dvě stejná písmena vedle sebe",
            "jsou to znamení zvěrokruhu",
        ],
    },
    {
        "id": "nazev-andersen",
        "roof": "slova z názvů Andersenových pohádek",
        "level": "normal",
        "hidden": True,
        "inside": [
            "šaty", "káčátko", "vojáček", "královna", "hrášek", "slavík",
            "křesadlo", "palečka",
        ],
        "outside": [
            "brambora", "brýle", "bunda", "kleště", "kompost", "koště",
            "květináč", "lepidlo", "ramínko", "utěrka", "vysavač", "věšák",
        ],
        "asks": [
            "jsou v názvech Andersenových pohádek",
            "jsou v názvech her Járy Cimrmana",
            "mají v sobě schované zvíře",
            "nemají v sobě ani jednu samohlásku",
        ],
    },
    {
        "id": "nazev-grimm",
        "roof": "slova z názvů pohádek bratří Grimmů",
        "level": "normal",
        "hidden": True,
        "inside": [
            "karkulka", "husa", "stoleček", "muzikant", "kůzlátko",
            "chaloupka", "perník", "jeníček",
        ],
        "outside": [
            "brambora", "kbelík", "kleště", "kolík", "kompost", "ořezávátko",
            "peřina", "sklenice", "skříň", "utěrka", "záclona", "zápisník",
        ],
        "asks": [
            "jsou v názvech pohádek bratří Grimmů",
            "mají v sobě schované zvíře",
            "nemají v sobě ani jednu samohlásku",
            "jsou v názvech Shakespearových her",
        ],
    },
    {
        "id": "nazev-lindgren",
        "roof": "slova z názvů knih Astrid Lindgrenové",
        "level": "normal",
        "hidden": True,
        "inside": [
            "punčocha", "loupežník", "střecha", "srdce", "detektiv", "dcera",
            "bratr", "děti",
        ],
        "outside": [
            "batoh", "hrneček", "květináč", "matrace", "náramek", "pekáč",
            "ponožka", "pouzdro", "skříň", "smeták", "truhlík", "záclona",
        ],
        "asks": [
            "jsou v názvech knih Astrid Lindgrenové",
            "jsou v názvech her Járy Cimrmana",
            "jsou v názvech večerníčků",
            "mají v sobě dvě stejná písmena vedle sebe",
        ],
    },
    {
        "id": "nazev-pisnicky",
        "roof": "slova z názvů dětských písniček",
        "level": "normal",
        "hidden": True,
        "inside": [
            "kočka", "díra", "travička", "pec", "holka", "ovčák", "zelí",
            "nanynka",
        ],
        "outside": [
            "brambora", "bunda", "guma", "hadr", "kompost", "konev", "nůžky",
            "postel", "ubrousek", "zápisník", "řetízek", "žebřík",
        ],
        "asks": [
            "jsou v názvech dětských písniček",
            "nemají v sobě ani jednu samohlásku",
            "jsou to zároveň značky nebo modely aut",
            "jsou v názvech večerníčků",
        ],
    },
    {
        "id": "nazev-komedie",
        "roof": "slova z názvů českých filmových komedií",
        "level": "normal",
        "hidden": True,
        "inside": [
            "vrchní", "pero", "seno", "jahoda", "blesk", "samota", "vesnička",
            "kovboj",
        ],
        "outside": [
            "batoh", "brýle", "hodinky", "hřeben", "kartáček", "kleště",
            "komoda", "lednička", "mísa", "naběračka", "silnice", "trakař",
        ],
        "asks": [
            "jsou v názvech českých filmových komedií",
            "jsou to zároveň značky českého piva",
            "čtou se stejně zepředu i zezadu",
            "mají v sobě dvě stejná písmena vedle sebe",
        ],
    },
    {
        "id": "nazev-svetove-filmy",
        "roof": "slova z názvů slavných světových filmů",
        "level": "normal",
        "hidden": True,
        "inside": [
            "kmotr", "matrix", "čelisti", "psycho", "gladiátor", "pianista",
            "titanic", "avatar",
        ],
        "outside": [
            "batoh", "deka", "krém", "lavička", "lednička", "lepidlo",
            "peněženka", "postel", "rohožka", "sešit", "vrtačka", "šála",
        ],
        "asks": [
            "jsou v názvech slavných světových filmů",
            "nemají v sobě ani jednu samohlásku",
            "čtou se stejně zepředu i zezadu",
            "mají v sobě schované zvíře",
        ],
    },
    {
        "id": "nazev-serialy",
        "roof": "slova z názvů českých seriálů",
        "level": "normal",
        "hidden": True,
        "inside": [
            "nemocnice", "sanitka", "chalupář", "cirkus", "dětství", "pult",
            "případ", "návštěvník",
        ],
        "outside": [
            "branka", "hodinky", "hřeben", "kbelík", "krém", "metr", "myčka",
            "naběračka", "ramínko", "rýč", "ubrousek", "věšák",
        ],
        "asks": [
            "jsou v názvech českých seriálů",
            "jsou v názvech večerníčků",
            "jsou to znamení zvěrokruhu",
            "jsou to zároveň jména českých měst",
        ],
    },
    {
        "id": "nazev-gott",
        "roof": "slova z názvů písní Karla Gotta",
        "level": "normal",
        "hidden": True,
        "inside": [
            "trezor", "včelka", "káva", "zvonek", "růže", "štěstí", "srdce",
            "paganini",
        ],
        "outside": [
            "hadice", "hřebík", "komoda", "lepidlo", "matice", "mýdlo",
            "provaz", "rohožka", "ručník", "semínko", "smeták", "sušák",
        ],
        "asks": [
            "jsou v názvech písní Karla Gotta",
            "mají v sobě dvě stejná písmena vedle sebe",
            "jsou to zároveň značky českého piva",
            "jsou to zároveň jména českých měst",
        ],
    },
    {
        "id": "nazev-baje",
        "roof": "slova z rčení, která pocházejí z antických bájí",
        "level": "normal",
        "hidden": True,
        "inside": [
            "pata", "nit", "kůň", "skříňka", "meč", "chlév", "uzel", "jablko",
        ],
        "outside": [
            "brýle", "deka", "dřez", "hadice", "kleště", "lednička", "mrkev",
            "mýdlo", "podnos", "rýč", "silnice", "šála",
        ],
        "asks": [
            "jsou v rčeních z antických bájí",
            "jsou to zároveň značky nebo modely aut",
            "jsou v názvech Shakespearových her",
            "jsou v názvech her Járy Cimrmana",
        ],
    },
    {
        "id": "nazev-sindibad",
        "roof": "slova z příběhů Tisíce a jedné noci",
        "level": "normal",
        "hidden": True,
        "inside": [
            "lampa", "koberec", "sezam", "jeskyně", "loupežník", "duch",
            "plavba", "poklad",
        ],
        "outside": [
            "brambora", "hrnec", "peřina", "pinzeta", "ponožka", "rohožka",
            "ručník", "semínko", "sud", "svěrák", "věšák", "záclona",
        ],
        "asks": [
            "jsou v příbězích Tisíce a jedné noci",
            "jsou v názvech her Járy Cimrmana",
            "jsou to zároveň značky českého piva",
            "jsou to zároveň značky nebo modely aut",
        ],
    },
    {
        "id": "nazev-dumas",
        "roof": "slova z názvů knih Alexandra Dumase",
        "level": "normal",
        "hidden": True,
        "inside": [
            "mušketýr", "hrabě", "královna", "tulipán", "dáma", "vikomt",
            "maska", "kamélie",
        ],
        "outside": [
            "brýle", "guma", "hrneček", "hřeben", "kartáček", "koště",
            "matice", "nůžky", "podnos", "ponožka", "smeták", "žebřík",
        ],
        "asks": [
            "jsou v názvech knih Alexandra Dumase",
            "jsou v názvech her Járy Cimrmana",
            "jsou to znamení zvěrokruhu",
            "mají v sobě dvě stejná písmena vedle sebe",
        ],
    },
    {
        "id": "nazev-foglar",
        "roof": "slova z názvů knih Jaroslava Foglara",
        "level": "hard",
        "hidden": True,
        "inside": [
            "hoši", "řeka", "záhada", "hlavolam", "stínadla", "tajemství",
            "chata", "poklad", "delfín", "kotlina",
        ],
        "outside": [
            "bunda", "dřez", "květináč", "myčka", "náramek", "nůžky",
            "polštář", "postel", "utěrka", "věšák", "šála", "žehlička",
        ],
        "asks": [
            "jsou v názvech knih Jaroslava Foglara",
            "jsou to zároveň značky českého piva",
            "jsou v názvech večerníčků",
            "jsou to zároveň příjmení českých prezidentů",
        ],
    },
    {
        "id": "nazev-verne",
        "roof": "slova z názvů knih Julese Verna",
        "level": "hard",
        "hidden": True,
        "inside": [
            "cesta", "ostrov", "prázdniny", "kapitán", "střed", "balón",
            "míle", "ocel", "moře", "země",
        ],
        "outside": [
            "batoh", "hřeben", "kastrol", "kleště", "komoda", "květináč",
            "náramek", "sklenice", "sporák", "ubrus", "věšák", "žehlička",
        ],
        "asks": [
            "jsou v názvech knih Julese Verna",
            "čtou se stejně zepředu i zezadu",
            "jsou to znamení zvěrokruhu",
            "mají v sobě schované zvíře",
        ],
    },
    {
        "id": "nazev-neruda",
        "roof": "slova z názvů Malostranských povídek",
        "level": "hard",
        "hidden": True,
        "inside": [
            "hastrman", "lilie", "pěnovka", "žebrák", "mizina", "mše",
            "týden", "figurky", "dušičky", "kazisvět",
        ],
        "outside": [
            "brambora", "bunda", "hodinky", "konev", "květináč", "matice",
            "myčka", "náramek", "popelnice", "rohožka", "vařečka", "řetízek",
        ],
        "asks": [
            "jsou v názvech Nerudových Malostranských povídek",
            "mají v sobě schované zvíře",
            "čtou se stejně zepředu i zezadu",
            "jsou to zároveň značky českého piva",
        ],
    },
    {
        "id": "nazev-jirasek",
        "roof": "slova ze Starých pověstí českých",
        "level": "hard",
        "hidden": True,
        "inside": [
            "praotec", "dcera", "proroctví", "válka", "blaník", "kouzelník",
            "horymír", "bruncvík",
        ],
        "outside": [
            "deka", "hrnec", "hrneček", "komoda", "kompost", "mísa", "pekáč",
            "ponožka", "semínko", "svěrák", "trakař", "šroub",
        ],
        "asks": [
            "jsou v názvech Starých pověstí českých",
            "jsou v názvech večerníčků",
            "nemají v sobě ani jednu samohlásku",
            "čtou se stejně zepředu i zezadu",
        ],
    },
    {
        "id": "nazev-nemcova",
        "roof": "slova z názvů pohádek Boženy Němcové",
        "level": "hard",
        "hidden": True,
        "inside": [
            "krkavec", "meč", "měsíček", "sůl", "zlato", "horákyně", "bajaja",
            "větrník", "káča", "mikeš",
        ],
        "outside": [
            "hrneček", "hřebík", "komoda", "lednička", "motyka", "nůžky",
            "peněženka", "peřina", "popelnice", "pračka", "pytel", "věšák",
        ],
        "asks": [
            "jsou v názvech pohádek Boženy Němcové",
            "jsou v názvech her Járy Cimrmana",
            "jsou to znamení zvěrokruhu",
            "mají v sobě dvě stejná písmena vedle sebe",
        ],
    },
    {
        "id": "nazev-smetana",
        "roof": "slova z názvů Smetanových oper",
        "level": "hard",
        "hidden": True,
        "inside": [
            "nevěsta", "hubička", "tajemství", "stěna", "vdova", "braniboři",
            "viola", "dalibor",
        ],
        "outside": [
            "batoh", "guma", "kastrol", "koště", "květináč", "motyka",
            "peřina", "pinzeta", "svěrák", "utěrka", "vana", "šála",
        ],
        "asks": [
            "jsou v názvech Smetanových oper",
            "jsou v názvech her Járy Cimrmana",
            "jsou to zároveň jména českých měst",
            "mají v sobě dvě stejná písmena vedle sebe",
        ],
    },
    {
        "id": "nazev-dvorak",
        "roof": "slova z názvů oper Dvořáka a Janáčka",
        "level": "hard",
        "hidden": True,
        "inside": [
            "rusalka", "čert", "káča", "jakobín", "liška", "věc", "uhlíř",
            "palice", "výlet", "armida",
        ],
        "outside": [
            "batoh", "brýle", "houpačka", "motyka", "nůžky", "podnos",
            "pytel", "semínko", "skříň", "svěrák", "ubrousek", "vysavač",
        ],
        "asks": [
            "jsou v názvech oper Dvořáka a Janáčka",
            "mají v sobě schované zvíře",
            "jsou to zároveň značky českého piva",
            "jsou to zároveň značky nebo modely aut",
        ],
    },
    {
        "id": "nazev-hitchcock",
        "roof": "slova z názvů Hitchcockových filmů",
        "level": "hard",
        "hidden": True,
        "inside": [
            "ptáci", "okno", "dvůr", "lano", "závrať", "sever", "cizinec",
            "podezření", "stupně", "vlak",
        ],
        "outside": [
            "guma", "hrnec", "hrábě", "motyka", "mrkev", "pinzeta", "sešit",
            "silnice", "ubrus", "vařečka", "vysavač", "věšák",
        ],
        "asks": [
            "jsou v názvech Hitchcockových filmů",
            "mají v sobě dvě stejná písmena vedle sebe",
            "jsou to zároveň příjmení českých prezidentů",
            "čtou se stejně zepředu i zezadu",
        ],
    },
    {
        "id": "nazev-sverak",
        "roof": "slova z názvů Svěrákových filmů",
        "level": "hard",
        "hidden": True,
        "inside": [
            "kolja", "lahve", "škola", "svět", "strniště", "kuky",
            "akumulátor", "jízda", "sezóna", "bos",
        ],
        "outside": [
            "hřeben", "kastrol", "květináč", "lednička", "matrace",
            "popelnice", "pravítko", "propiska", "provaz", "ramínko",
            "truhlík", "ubrousek",
        ],
        "asks": [
            "jsou v názvech Svěrákových filmů",
            "nemají v sobě ani jednu samohlásku",
            "mají v sobě dvě stejná písmena vedle sebe",
            "jsou to znamení zvěrokruhu",
        ],
    },
    {
        "id": "nazev-muzikaly",
        "roof": "slova z názvů českých muzikálů",
        "level": "hard",
        "hidden": True,
        "inside": [
            "dracula", "bídníci", "krysař", "noc", "karlštejn", "kleopatra",
            "rebelové", "excalibur",
        ],
        "outside": [
            "hadr", "hoblík", "hřeben", "matice", "metr", "motyka", "myčka",
            "náramek", "pilník", "semínko", "ubrus", "věšák",
        ],
        "asks": [
            "jsou v názvech českých muzikálů",
            "čtou se stejně zepředu i zezadu",
            "jsou to zároveň značky českého piva",
            "jsou to znamení zvěrokruhu",
        ],
    },
    {
        "id": "nazev-kryl",
        "roof": "slova z názvů písní Karla Kryla",
        "level": "hard",
        "hidden": True,
        "inside": [
            "anděl", "vrátka", "salome", "veličenstvo", "kat", "karavana",
            "mrak", "bratříček", "revolta", "vojín",
        ],
        "outside": [
            "kastrol", "kbelík", "kolík", "lavička", "motyka", "nůžky",
            "pračka", "propiska", "rohožka", "ubrousek", "zahrada", "šroub",
        ],
        "asks": [
            "jsou v názvech písní Karla Kryla",
            "jsou to zároveň značky nebo modely aut",
            "mají v sobě dvě stejná písmena vedle sebe",
            "jsou to zároveň jména českých měst",
        ],
    },
    {
        "id": "nazev-nohavica",
        "roof": "slova z názvů písní Jaromíra Nohavici",
        "level": "hard",
        "hidden": True,
        "inside": [
            "kometa", "sarajevo", "hlídač", "kráva", "zima", "století",
            "voják", "věž",
        ],
        "outside": [
            "brýle", "bunda", "hoblík", "houpačka", "náramek", "nůžky",
            "pekáč", "pinzeta", "polštář", "truhlík", "vrtačka", "zahrada",
        ],
        "asks": [
            "jsou v názvech písní Jaromíra Nohavici",
            "mají v sobě dvě stejná písmena vedle sebe",
            "čtou se stejně zepředu i zezadu",
            "jsou v názvech večerníčků",
        ],
    },
    {
        "id": "nazev-werich",
        "roof": "slova z názvů pohádek z Fimfára",
        "level": "hard",
        "hidden": True,
        "inside": [
            "listí", "dub", "barka", "veterán", "koloběžka", "rozum",
            "štěstí", "paleček",
        ],
        "outside": [
            "brambora", "dřez", "hrneček", "kbelík", "kýbl", "lavička",
            "lednička", "mísa", "ořezávátko", "pilník", "silnice", "svěrák",
        ],
        "asks": [
            "jsou v názvech pohádek z Werichova Fimfára",
            "jsou v názvech Shakespearových her",
            "jsou to znamení zvěrokruhu",
            "jsou to zároveň značky českého piva",
        ],
    },
    {
        "id": "nazev-ota-pavel",
        "roof": "slova z názvů knih Oty Pavla",
        "level": "hard",
        "hidden": True,
        "inside": [
            "srnec", "ryba", "pohár", "bedna", "úhoř", "běh", "syn", "celer",
        ],
        "outside": [
            "batoh", "guma", "hadice", "hadr", "metr", "pekáč", "pračka",
            "smeták", "trakař", "věšák", "šroub", "šuplík",
        ],
        "asks": [
            "jsou v názvech knih Oty Pavla",
            "mají v sobě dvě stejná písmena vedle sebe",
            "jsou v názvech večerníčků",
            "nemají v sobě ani jednu samohlásku",
        ],
    },
    {
        "id": "nazev-basnici",
        "roof": "slova z názvů sbírek Nezvala a Seiferta",
        "level": "hard",
        "hidden": True,
        "inside": [
            "šáteček", "maminka", "píseň", "sloup", "deštník", "edison",
            "viktorka", "ruce", "jaro", "hrobař",
        ],
        "outside": [
            "hadice", "hrábě", "kolík", "matrace", "myčka", "mýdlo",
            "polštář", "semínko", "sešit", "trakař", "utěrka", "záclona",
        ],
        "asks": [
            "jsou v názvech sbírek Nezvala a Seiferta",
            "jsou v názvech Shakespearových her",
            "jsou v názvech her Járy Cimrmana",
            "jsou to zároveň značky českého piva",
        ],
    },
    {
        "id": "nazev-holmes",
        "roof": "slova z názvů případů Sherlocka Holmese",
        "level": "hard",
        "hidden": True,
        "inside": [
            "studie", "znamení", "karbunkule", "figurky", "údolí", "pás",
            "napoleon", "případ",
        ],
        "outside": [
            "bunda", "guma", "hoblík", "hřebík", "kompost", "myčka", "pilník",
            "postel", "pouzdro", "skříň", "vana", "žehlička",
        ],
        "asks": [
            "jsou v názvech případů Sherlocka Holmese",
            "jsou to znamení zvěrokruhu",
            "mají v sobě schované zvíře",
            "jsou to zároveň jména českých měst",
        ],
    },
]
