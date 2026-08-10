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
            "hoblík", "hřeben", "kolík", "kýbl", "lampa", "pračka", "provaz",
            "ručník", "sud", "sušák", "trakař", "vana",
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
            "hodinky", "lednička", "metr", "mýdlo", "nůžky", "police",
            "pouzdro", "rohožka", "sešit", "sklenice", "ubrousek", "řetízek",
        ],
        "asks": [
            "začínají a končí stejným písmenem",
            "jsou to zároveň jména českých měst",
            "čtou se stejně zepředu i zezadu",
            "jsou to zároveň příjmení českých prezidentů",
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
            "brýle", "koberec", "kolík", "koště", "mýdlo", "ořezávátko",
            "pilník", "pytel", "ručník", "smeták", "trakař", "vrtačka",
        ],
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
            "hrnec", "kastrol", "konev", "lednička", "pekáč", "ponožka",
            "popelnice", "propiska", "pytel", "ramínko", "sušák", "žehlička",
        ],
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
            "deka", "houpačka", "kolík", "peřina", "postel", "ramínko",
            "rohožka", "skříň", "svěrák", "truhlík", "věšák", "šuplík",
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
            "brýle", "deka", "hadice", "hodinky", "hřeben", "lepidlo",
            "polštář", "propiska", "provaz", "pytel", "ramínko", "záclona",
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
            "brambora", "bunda", "hodinky", "hřeben", "koberec", "konev",
            "mísa", "pekáč", "peřina", "police", "sud", "šroub",
        ],
        "asks": [
            "mají v sobě tři souhlásky za sebou",
            "čtou se stejně zepředu i zezadu",
            "nemají v sobě ani jednu samohlásku",
            "jsou to zároveň jména českých měst",
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
            "batoh", "kartáček", "mýdlo", "peřina", "pinzeta", "sklenice",
            "skříň", "sporák", "sušák", "trakař", "utěrka", "vysavač",
        ],
        "asks": [
            "mají v sobě dvojhlásku ou, au nebo eu",
            "jsou to zároveň jména českých měst",
            "jsou v názvech večerníčků",
            "jsou to znamení zvěrokruhu",
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
            "hadr", "hrábě", "lampa", "lavička", "metr", "mísa", "pytel",
            "semínko", "vana", "zápisník", "řetízek", "šroub",
        ],
        "asks": [
            "mají v sobě dvakrát tutéž dvojici písmen",
            "jsou v názvech her Járy Cimrmana",
            "jsou v názvech večerníčků",
            "jsou to znamení zvěrokruhu",
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
            "brýle", "dřez", "hadice", "metr", "naběračka", "pekáč",
            "pinzeta", "ponožka", "pravítko", "pračka", "semínko", "vrtačka",
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
            "brýle", "dřez", "krém", "květináč", "mýdlo", "pekáč", "pinzeta",
            "pouzdro", "provaz", "věšák", "šroub", "žebřík",
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
            "bunda", "deka", "houpačka", "matrace", "myčka", "nůžky",
            "rohožka", "sklenice", "sporák", "trakař", "ubrousek", "vana",
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
            "koberec", "květináč", "kýbl", "lampa", "peřina", "pilník",
            "popelnice", "rýč", "sklenice", "sporák", "struhadlo", "utěrka",
        ],
        "asks": [
            "mají písmena jen z první poloviny abecedy",
            "jsou v názvech her Járy Cimrmana",
            "jsou to zároveň jména českých měst",
            "jsou to zároveň značky nebo modely aut",
        ],
    },
    {
        "id": "mech-leva-ruka",
        "roof": "slova, která se napíšou jen levou rukou na české klávesnici",
        "level": "hard",
        "hidden": True,
        "inside": [
            "srdce", "dveře", "svět", "bratr", "starý", "sestra", "cesta",
            "děvče", "ryba", "déšť", "tráva", "tvar",
        ],
        "outside": [
            "guma", "hrábě", "motyka", "myčka", "náramek", "pekáč", "police",
            "polštář", "silnice", "sud", "sušák", "šuplík",
        ],
        "asks": [
            "se dají napsat jen levou rukou na české klávesnici",
            "jsou to zároveň značky českého piva",
            "mají v sobě dvě stejná písmena vedle sebe",
            "jsou v názvech večerníčků",
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
            "hřeben", "kompost", "matice", "naběračka", "náramek",
            "ořezávátko", "sklenice", "smeták", "utěrka", "vrtačka",
            "vysavač", "záclona",
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
            "batoh", "brambora", "hrnec", "kartáček", "krém", "police",
            "pouzdro", "pravítko", "smeták", "vařečka", "zápisník", "řetízek",
        ],
        "asks": [
            "mají vedle sebe dvě písmena, která jdou po sobě i v abecedě",
            "čtou se stejně zepředu i zezadu",
            "jsou v názvech večerníčků",
            "mají v sobě schované zvíře",
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
            "deka", "guma", "hrnec", "hrábě", "kbelík", "komoda", "konev",
            "mrkev", "myčka", "podnos", "pytel", "věšák",
        ],
        "asks": [
            "mají jen písmena, která se používají jako římské číslice",
            "jsou v názvech her Járy Cimrmana",
            "jsou v názvech Shakespearových her",
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
            "branka", "bunda", "hodinky", "kolík", "koště", "lepidlo",
            "matrace", "nůžky", "pilník", "postel", "pytel", "šála",
        ],
        "asks": [
            "mají v sobě jen jednu jedinou samohlásku",
            "jsou to zároveň příjmení českých prezidentů",
            "jsou v názvech her Járy Cimrmana",
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
            "kýbl", "lavička", "motyka", "mrkev", "pravítko", "pračka",
            "skříň", "svěrák", "trakař", "tácek", "vysavač", "záclona",
        ],
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
            "hadice", "kolík", "krém", "peřina", "pinzeta", "propiska",
            "silnice", "svěrák", "věšák", "zápisník", "šroub", "šála",
        ],
        "asks": [
            "jsou to zároveň stanice pražského metra",
            "jsou v názvech Shakespearových her",
            "mají v sobě dvě stejná písmena vedle sebe",
            "jsou to zároveň příjmení českých prezidentů",
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
            "brýle", "kolík", "konev", "krém", "lampa", "mrkev", "mísa",
            "pilník", "pouzdro", "pytel", "vysavač", "šroub",
        ],
        "asks": [
            "jsou to zároveň měny",
            "jsou to zároveň značky českého piva",
            "jsou to zároveň jména českých měst",
            "jsou to znamení zvěrokruhu",
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
            "brýle", "komoda", "konev", "kýbl", "mísa", "peřina", "police",
            "ponožka", "postel", "skříň", "vysavač", "šála",
        ],
        "asks": [
            "jsou to zároveň písmena řecké abecedy",
            "nemají v sobě ani jednu samohlásku",
            "jsou v názvech her Járy Cimrmana",
            "jsou to znamení zvěrokruhu",
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
            "hřebík", "květináč", "lampa", "lepidlo", "metr", "police", "rýč",
            "sporák", "vařečka", "věšák", "žebřík", "žehlička",
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
            "bunda", "hoblík", "kýbl", "mýdlo", "peněženka", "sporák",
            "truhlík", "tácek", "vana", "vařečka", "vysavač", "šála",
        ],
        "asks": [
            "jsou to zároveň karetní hry",
            "jsou to zároveň značky nebo modely aut",
            "jsou to zároveň značky českého piva",
            "mají v sobě schované zvíře",
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
            "branka", "hadr", "nůžky", "podnos", "semínko", "sešit",
            "struhadlo", "sud", "trakař", "ubrus", "utěrka", "řetízek",
        ],
        "asks": [
            "jsou to zároveň názvy českých časopisů",
            "jsou v názvech večerníčků",
            "jsou to znamení zvěrokruhu",
            "jsou to zároveň značky českého piva",
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
            "branka", "koště", "mrkev", "pračka", "provaz", "semínko",
            "silnice", "smeták", "truhlík", "ubrousek", "zápisník", "žebřík",
        ],
        "asks": [
            "jsou to zároveň názvy českých kapel",
            "jsou to znamení zvěrokruhu",
            "jsou v názvech her Járy Cimrmana",
            "mají v sobě schované zvíře",
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
            "guma", "hoblík", "kolík", "kýbl", "lavička", "lopatka",
            "náramek", "polštář", "ponožka", "silnice", "ubrousek", "věšák",
        ],
        "asks": [
            "jsou to zároveň názvy českých hokejových klubů",
            "jsou to zároveň značky nebo modely aut",
            "jsou to znamení zvěrokruhu",
            "jsou to zároveň značky českého piva",
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
            "deka", "hadr", "hoblík", "hrábě", "mrkev", "náramek", "polštář",
            "propiska", "ručník", "smeták", "truhlík", "vrtačka",
        ],
        "asks": [
            "jsou to zároveň názvy motorek nebo mopedů",
            "jsou to znamení zvěrokruhu",
            "jsou to zároveň jména českých měst",
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
            "batoh", "dřez", "hrábě", "kastrol", "kolík", "náramek", "peřina",
            "ramínko", "rýč", "struhadlo", "ubrus", "zápisník",
        ],
        "asks": [
            "jsou to zároveň názvy sýrů",
            "jsou v názvech Shakespearových her",
            "jsou to zároveň příjmení českých prezidentů",
            "jsou to znamení zvěrokruhu",
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
            "batoh", "květináč", "kýbl", "lopatka", "metr", "ořezávátko",
            "pouzdro", "rýč", "truhlík", "ubrus", "utěrka", "řetízek",
        ],
        "asks": [
            "jsou to zároveň tance",
            "jsou to znamení zvěrokruhu",
            "jsou v názvech večerníčků",
            "jsou to zároveň příjmení českých prezidentů",
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
            "hadice", "kastrol", "kýbl", "lepidlo", "mrkev", "myčka",
            "popelnice", "semínko", "ubrus", "vrtačka", "zápisník", "šroub",
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
            "dřez", "hrnec", "kleště", "lopatka", "matice", "pilník",
            "police", "postel", "rýč", "silnice", "smeták", "vysavač",
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
            "hoblík", "hodinky", "metr", "myčka", "mýdlo", "náramek",
            "pouzdro", "semínko", "svěrák", "vařečka", "záclona", "šála",
        ],
        "asks": [
            "jsou to zároveň divadelní pojmy",
            "jsou v názvech Shakespearových her",
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
            "hrábě", "kastrol", "komoda", "konev", "květináč", "lampa",
            "peněženka", "pinzeta", "polštář", "skříň", "ubrousek",
            "žehlička",
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
            "brýle", "krém", "mísa", "peněženka", "peřina", "postel", "pytel",
            "skříň", "svěrák", "vrtačka", "šála", "žebřík",
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
            "brýle", "deka", "guma", "hodinky", "krém", "lednička", "provaz",
            "rýč", "skříň", "sporák", "utěrka", "řetízek",
        ],
        "asks": [
            "jsou to zároveň fotbalové pojmy",
            "nemají v sobě ani jednu samohlásku",
            "jsou to zároveň příjmení českých prezidentů",
            "mají v sobě schované zvíře",
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
            "hadice", "hoblík", "hrnec", "kýbl", "mísa", "podnos", "police",
            "ponožka", "propiska", "sušák", "vana", "šuplík",
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
            "guma", "hadr", "houpačka", "hrneček", "koště", "matrace", "metr",
            "náramek", "pytel", "silnice", "sud", "truhlík",
        ],
        "asks": [
            "jsou to zároveň názvy větrů",
            "jsou to znamení zvěrokruhu",
            "čtou se stejně zepředu i zezadu",
            "jsou v názvech Shakespearových her",
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
            "deka", "hrneček", "kýbl", "lednička", "metr", "naběračka",
            "pilník", "ponožka", "propiska", "ručník", "rýč", "trakař",
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
            "dřez", "hadr", "kartáček", "konev", "květináč", "matice",
            "motyka", "mýdlo", "podnos", "silnice", "trakař", "ubrus",
        ],
        "asks": [
            "jsou to zároveň názvy českých nakladatelství",
            "čtou se stejně zepředu i zezadu",
            "mají v sobě dvě stejná písmena vedle sebe",
            "jsou to zároveň příjmení českých prezidentů",
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
            "hadr", "kartáček", "kleště", "koště", "květináč", "peněženka",
            "police", "ponožka", "postel", "sklenice", "tácek", "vrtačka",
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
            "dřez", "hrneček", "lampa", "matice", "mísa", "pračka", "provaz",
            "vrtačka", "věšák", "záclona", "zápisník", "šála",
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
            "bunda", "hrnec", "kolík", "mýdlo", "pilník", "pinzeta", "police",
            "polštář", "popelnice", "rohožka", "ubrus", "utěrka",
        ],
        "asks": [
            "jsou to zároveň značky v notách",
            "čtou se stejně zepředu i zezadu",
            "mají v sobě dvě stejná písmena vedle sebe",
            "mají v sobě schované zvíře",
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
            "deka", "guma", "kastrol", "komoda", "konev", "krém", "kýbl",
            "myčka", "mýdlo", "pilník", "ramínko", "truhlík",
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
            "mísa", "peněženka", "polštář", "popelnice", "pytel", "ramínko",
            "sklenice", "svěrák", "vařečka", "vrtačka", "šroub", "žebřík",
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
            "batoh", "bunda", "guma", "hadr", "kolík", "kýbl", "mýdlo",
            "nůžky", "pekáč", "sušák", "tácek", "šála",
        ],
        "asks": [
            "jsou zároveň anglická slova s jiným významem",
            "jsou v názvech Shakespearových her",
            "čtou se stejně zepředu i zezadu",
            "jsou to zároveň příjmení českých prezidentů",
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
            "hrábě", "lavička", "matice", "mrkev", "mísa", "pilník", "podnos",
            "pouzdro", "rohožka", "semínko", "silnice", "šála",
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
            "kleště", "lednička", "ořezávátko", "polštář", "sklenice",
            "sporák", "sud", "ubrousek", "utěrka", "vysavač", "záclona",
            "šroub",
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
            "hadr", "kompost", "krém", "mrkev", "mísa", "pytel", "sklenice",
            "truhlík", "ubrus", "vana", "vařečka", "vrtačka",
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
            "brambora", "branka", "deka", "hadr", "hoblík", "kastrol",
            "matrace", "police", "ponožka", "pračka", "ručník", "vana",
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
            "batoh", "branka", "komoda", "kompost", "naběračka", "semínko",
            "skříň", "struhadlo", "záclona", "zápisník", "šála", "žehlička",
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
            "lednička", "lopatka", "matrace", "motyka", "mísa", "pouzdro",
            "provaz", "rohožka", "rýč", "smeták", "vařečka", "zápisník",
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
            "deka", "hřeben", "lavička", "matrace", "mýdlo", "peněženka",
            "peřina", "postel", "utěrka", "zahrada", "šroub", "žebřík",
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
            "guma", "kbelík", "kolík", "mísa", "pinzeta", "propiska", "pytel",
            "rýč", "sporák", "sud", "svěrák", "zápisník",
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
            "batoh", "deka", "koberec", "koště", "květináč", "náramek",
            "pravítko", "silnice", "sporák", "svěrák", "ubrus", "utěrka",
        ],
        "asks": [
            "jsou v názvech Andersenových pohádek",
            "čtou se stejně zepředu i zezadu",
            "jsou v názvech her Járy Cimrmana",
            "mají v sobě dvě stejná písmena vedle sebe",
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
            "kartáček", "koberec", "květináč", "matrace", "mrkev", "náramek",
            "nůžky", "pravítko", "pytel", "silnice", "svěrák", "šuplík",
        ],
        "asks": [
            "jsou v názvech pohádek bratří Grimmů",
            "jsou to zároveň značky nebo modely aut",
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
            "brýle", "hadr", "kartáček", "lepidlo", "motyka", "ořezávátko",
            "pekáč", "rýč", "skříň", "sud", "řetízek", "šuplík",
        ],
        "asks": [
            "jsou v názvech knih Astrid Lindgrenové",
            "jsou to zároveň příjmení českých prezidentů",
            "jsou v názvech her Járy Cimrmana",
            "jsou v názvech večerníčků",
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
            "hodinky", "koberec", "komoda", "konev", "krém", "květináč",
            "lampa", "nůžky", "podnos", "propiska", "tácek", "ubrus",
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
            "batoh", "branka", "dřez", "kompost", "lepidlo", "metr",
            "peněženka", "pinzeta", "sklenice", "struhadlo", "svěrák", "šála",
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
            "guma", "kastrol", "komoda", "kompost", "lepidlo", "matice",
            "náramek", "peřina", "postel", "pračka", "sešit", "záclona",
        ],
        "asks": [
            "jsou v názvech slavných světových filmů",
            "mají v sobě schované zvíře",
            "nemají v sobě ani jednu samohlásku",
            "čtou se stejně zepředu i zezadu",
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
            "deka", "dřez", "hoblík", "hrábě", "lavička", "peněženka",
            "pinzeta", "podnos", "pračka", "semínko", "ubrousek", "utěrka",
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
            "hadr", "houpačka", "hřebík", "kastrol", "lopatka", "metr",
            "pravítko", "provaz", "truhlík", "vařečka", "vysavač", "žebřík",
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
            "houpačka", "hrábě", "kompost", "pekáč", "polštář", "postel",
            "pouzdro", "sklenice", "svěrák", "vana", "věšák", "záclona",
        ],
        "asks": [
            "jsou v rčeních z antických bájí",
            "jsou to zároveň značky nebo modely aut",
            "jsou v názvech Shakespearových her",
            "jsou v názvech her Járy Cimrmana",
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
            "batoh", "bunda", "hadr", "hřebík", "konev", "koště", "krém",
            "naběračka", "pekáč", "pinzeta", "propiska", "struhadlo",
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
            "brýle", "komoda", "krém", "kýbl", "lednička", "rýč", "semínko",
            "silnice", "ubrus", "utěrka", "vana", "záclona",
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
            "brýle", "lednička", "lepidlo", "mrkev", "myčka", "mýdlo",
            "náramek", "pinzeta", "rýč", "svěrák", "utěrka", "zahrada",
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
            "brýle", "hodinky", "hřebík", "kastrol", "koberec", "lampa",
            "peněženka", "rohožka", "rýč", "semínko", "ubrus", "věšák",
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
            "branka", "bunda", "hrnec", "kolík", "květináč", "metr", "pekáč",
            "pilník", "postel", "vana", "řetízek", "šála",
        ],
        "asks": [
            "jsou v názvech Starých pověstí českých",
            "čtou se stejně zepředu i zezadu",
            "jsou v názvech večerníčků",
            "nemají v sobě ani jednu samohlásku",
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
            "kompost", "krém", "matrace", "metr", "pekáč", "pouzdro",
            "provaz", "rohožka", "smeták", "trakař", "utěrka", "žehlička",
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
            "koště", "lepidlo", "matrace", "motyka", "pilník", "ponožka",
            "propiska", "silnice", "sušák", "trakař", "zahrada", "záclona",
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
            "krém", "lepidlo", "náramek", "pekáč", "podnos", "pouzdro",
            "ramínko", "smeták", "sporák", "trakař", "truhlík", "šuplík",
        ],
        "asks": [
            "jsou v názvech oper Dvořáka a Janáčka",
            "jsou v názvech her Járy Cimrmana",
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
            "hadice", "hrnec", "mýdlo", "polštář", "propiska", "sešit",
            "sklenice", "sporák", "sušák", "trakař", "utěrka", "věšák",
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
            "deka", "hřeben", "kompost", "lopatka", "motyka", "pinzeta",
            "podnos", "rohožka", "rýč", "skříň", "zahrada", "zápisník",
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
            "brýle", "hoblík", "hřebík", "mýdlo", "pinzeta", "semínko",
            "trakař", "truhlík", "tácek", "utěrka", "vrtačka", "šroub",
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
            "brambora", "hřeben", "kastrol", "kolík", "krém", "peřina",
            "podnos", "pytel", "trakař", "ubrousek", "zahrada", "žehlička",
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
            "batoh", "brambora", "brýle", "krém", "kýbl", "matice", "motyka",
            "ramínko", "sud", "sušák", "ubrus", "vrtačka",
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
            "koberec", "kompost", "pekáč", "peřina", "pilník", "pravítko",
            "ručník", "sklenice", "ubrousek", "vana", "šroub", "šála",
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
            "batoh", "branka", "brýle", "dřez", "guma", "hadice", "hřebík",
            "kbelík", "kleště", "metr", "sporák", "tácek",
        ],
        "asks": [
            "jsou v názvech knih Oty Pavla",
            "jsou to zároveň značky českého piva",
            "mají v sobě dvě stejná písmena vedle sebe",
            "jsou v názvech večerníčků",
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
            "branka", "hadice", "houpačka", "kartáček", "kýbl", "náramek",
            "pytel", "sešit", "silnice", "skříň", "truhlík", "vařečka",
        ],
        "asks": [
            "jsou v názvech sbírek Nezvala a Seiferta",
            "nemají v sobě ani jednu samohlásku",
            "jsou v názvech Shakespearových her",
            "jsou v názvech her Járy Cimrmana",
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
            "komoda", "květináč", "lednička", "ořezávátko", "ponožka",
            "propiska", "provaz", "semínko", "ubrus", "vrtačka", "šroub",
            "šuplík",
        ],
        "asks": [
            "jsou v názvech případů Sherlocka Holmese",
            "jsou to znamení zvěrokruhu",
            "mají v sobě schované zvíře",
            "jsou to zároveň jména českých měst",
        ],
    },
]
