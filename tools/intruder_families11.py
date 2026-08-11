"""Jedenáctá várka rodin — sto skrytých střech.

TENHLE SOUBOR PÍŠE SKRIPT. Ruční úpravy zmizí při dalším spuštění; opravovat
se má `tools/gen_families11.py`, kde stojí zadání i kontroly.
"""

FAMILIES11 = [
    {
        "id": "v11-strom",
        "roof": "části stromu",
        "level": "normal",
        "hidden": True,
        "inside": [
            "kmen", "koruna", "větev", "kůra", "letokruh", "lýko", "běl",
            "dřeň",
        ],
        "outside": [
            "deštník", "hodinky", "kastrol", "komoda", "motyka", "myčka",
            "mísa", "pinzeta", "postel", "prostěradlo", "rýč", "struhadlo",
            "trouba", "vrtačka", "zahrada",
        ],
        "asks": [
            "jsou to zároveň části stromu",
            "jsou v názvech her Járy Cimrmana",
            "jsou v názvech večerníčků",
            "jsou to zároveň jména českých měst",
        ],
    },
    {
        "id": "v11-sud",
        "roof": "části sudu",
        "level": "hard",
        "hidden": True,
        "inside": [
            "dno", "dužina", "obruč", "čep", "víko", "zátka",
        ],
        "outside": [
            "houpačka", "koberec", "kolík", "koš", "koště", "lepidlo",
            "lopata", "mýdlo", "nůžky", "pytel", "ramínko", "rýč", "sušák",
            "zahrada", "šála",
        ],
        "asks": [
            "jsou to zároveň části sudu",
            "jsou to zároveň značky nebo modely aut",
            "jsou to zároveň příjmení českých prezidentů",
            "mají v sobě dvě stejná písmena vedle sebe",
        ],
    },
    {
        "id": "v11-pluh",
        "roof": "části pluhu",
        "level": "hard",
        "hidden": True,
        "inside": [
            "radlice", "krojidlo", "hřídel", "odhrnovačka", "slupice",
            "patka",
        ],
        "outside": [
            "chleba", "houpačka", "hrnec", "kbelík", "komoda", "kompost",
            "konev", "kýbl", "myčka", "nůžky", "schránka", "smeták",
            "struhadlo", "záclona", "žebřík",
        ],
        "asks": [
            "jsou to zároveň části pluhu",
            "mají v sobě dvě stejná písmena vedle sebe",
            "jsou to zároveň značky českého piva",
            "jsou to znamení zvěrokruhu",
        ],
    },
    {
        "id": "v11-mlyn",
        "roof": "části mlýna",
        "level": "hard",
        "hidden": True,
        "inside": [
            "kámen", "koleso", "násypka", "moučnice", "náhon", "lopatka",
        ],
        "outside": [
            "chleba", "kabát", "kolík", "konev", "myčka", "peřina", "pinzeta",
            "police", "popelnice", "pouzdro", "ručník", "schránka", "sešit",
            "sklenice", "vařečka",
        ],
        "asks": [
            "jsou to zároveň části mlýna",
            "nemají v sobě ani jednu samohlásku",
            "jsou to zároveň jména českých měst",
            "jsou v názvech Shakespearových her",
        ],
    },
    {
        "id": "v11-varhany",
        "roof": "části varhan",
        "level": "hard",
        "hidden": True,
        "inside": [
            "píšťala", "měch", "rejstřík", "manuál", "pedál", "traktura",
        ],
        "outside": [
            "dřez", "konev", "koš", "lednička", "myčka", "mísa", "parapet",
            "peněženka", "polštář", "pouzdro", "prostěradlo", "ramínko",
            "struhadlo", "ubrus", "utěrka",
        ],
        "asks": [
            "jsou to zároveň části varhan",
            "nemají v sobě ani jednu samohlásku",
            "jsou to zároveň příjmení českých prezidentů",
            "jsou to zároveň značky nebo modely aut",
        ],
    },
    {
        "id": "v11-buben",
        "roof": "části bubnu",
        "level": "normal",
        "hidden": True,
        "inside": [
            "blána", "obruč", "plášť", "palička", "napínák", "struník",
        ],
        "outside": [
            "hoblík", "hřeben", "kompost", "koš", "květináč", "matrace",
            "ořezávátko", "podnos", "pravítko", "pytel", "struhadlo",
            "truhlík", "ubrus", "věšák", "žehlička",
        ],
        "asks": [
            "jsou to zároveň části bubnu",
            "jsou to zároveň příjmení českých prezidentů",
            "jsou to znamení zvěrokruhu",
            "mají v sobě dvě stejná písmena vedle sebe",
        ],
    },
    {
        "id": "v11-mec",
        "roof": "části meče",
        "level": "normal",
        "hidden": True,
        "inside": [
            "čepel", "jílec", "hlavice", "záštita", "ostří", "hrot",
        ],
        "outside": [
            "branka", "bunda", "deštník", "houpačka", "krém", "mýdlo",
            "pouzdro", "pravítko", "semínko", "sešit", "trouba", "vana",
            "vařečka", "vysavač", "žebřík",
        ],
        "asks": [
            "jsou to zároveň části meče",
            "nemají v sobě ani jednu samohlásku",
            "jsou to zároveň jména českých měst",
            "jsou v názvech Shakespearových her",
        ],
    },
    {
        "id": "v11-brneni",
        "roof": "části brnění",
        "level": "hard",
        "hidden": True,
        "inside": [
            "přilba", "kyrys", "náloketník", "náholenice", "kroužky",
            "rukavice",
        ],
        "outside": [
            "brambora", "kabát", "kladívko", "krém", "lednička", "motyka",
            "mísa", "náramek", "nůžky", "parapet", "peřina", "podnos",
            "postel", "ubrus", "šroub",
        ],
        "asks": [
            "jsou to zároveň části brnění",
            "jsou v názvech her Járy Cimrmana",
            "jsou v názvech večerníčků",
            "jsou v názvech Shakespearových her",
        ],
    },
    {
        "id": "v11-sedlo",
        "roof": "části jezdeckého sedla",
        "level": "hard",
        "hidden": True,
        "inside": [
            "třmen", "podbřišník", "hruška", "kožka", "popruh", "sedlisko",
        ],
        "outside": [
            "bunda", "hřebík", "koberec", "kolík", "konev", "lednička",
            "nůžky", "pravítko", "prostěradlo", "pytel", "schránka",
            "silnice", "ubrousek", "vana", "záclona",
        ],
        "asks": [
            "jsou to zároveň části jezdeckého sedla",
            "jsou to zároveň značky nebo modely aut",
            "mají v sobě schované zvíře",
            "jsou to zároveň příjmení českých prezidentů",
        ],
    },
    {
        "id": "v11-destnik-casti",
        "roof": "části deštníku",
        "level": "normal",
        "hidden": True,
        "inside": [
            "kostra", "potah", "hůl", "hrot", "rukojeť", "pero",
        ],
        "outside": [
            "houpačka", "hřeben", "kabát", "kartáček", "kladívko", "kleště",
            "kompost", "naběračka", "náramek", "parapet", "plot", "sešit",
            "sud", "vysavač", "šuplík",
        ],
        "asks": [
            "jsou to zároveň části deštníku",
            "mají v sobě dvě stejná písmena vedle sebe",
            "jsou v názvech večerníčků",
            "jsou v názvech her Járy Cimrmana",
        ],
    },
    {
        "id": "v11-zvon",
        "roof": "části zvonu",
        "level": "hard",
        "hidden": True,
        "inside": [
            "srdce", "koruna", "věnec", "plášť", "čepec", "límec",
        ],
        "outside": [
            "hrábě", "krém", "kýbl", "lampa", "matrace", "motyka",
            "ořezávátko", "peněženka", "pinzeta", "postel", "skříň",
            "struhadlo", "trakař", "ubrousek", "žebřík",
        ],
        "asks": [
            "jsou to zároveň části zvonu",
            "jsou to zároveň příjmení českých prezidentů",
            "nemají v sobě ani jednu samohlásku",
            "jsou v názvech Shakespearových her",
        ],
    },
    {
        "id": "v11-postel",
        "roof": "části postele",
        "level": "normal",
        "hidden": True,
        "inside": [
            "rošt", "čelo", "rám", "nohy", "matrace", "bočnice",
        ],
        "outside": [
            "hoblík", "houpačka", "kleště", "kolík", "květináč", "lednička",
            "metr", "mrkev", "myčka", "police", "ručník", "sklenice",
            "utěrka", "vysavač", "zahrada",
        ],
        "asks": [
            "jsou to zároveň části postele",
            "jsou to zároveň jména českých měst",
            "mají v sobě dvě stejná písmena vedle sebe",
            "čtou se stejně zepředu i zezadu",
        ],
    },
    {
        "id": "v11-mikroskop",
        "roof": "části mikroskopu",
        "level": "hard",
        "hidden": True,
        "inside": [
            "okulár", "objektiv", "stolek", "zrcátko", "tubus", "revolver",
        ],
        "outside": [
            "dřez", "guma", "hoblík", "hrneček", "kleště", "koberec",
            "komoda", "lednička", "metr", "naběračka", "police", "ponožka",
            "propiska", "sešit", "záclona",
        ],
        "asks": [
            "jsou to zároveň části mikroskopu",
            "jsou v názvech her Járy Cimrmana",
            "jsou v názvech Shakespearových her",
            "čtou se stejně zepředu i zezadu",
        ],
    },
    {
        "id": "v11-tunel",
        "roof": "části tunelu",
        "level": "hard",
        "hidden": True,
        "inside": [
            "portál", "ostění", "klenba", "čelba", "počva", "ražba",
        ],
        "outside": [
            "brýle", "hrnec", "koberec", "krém", "květináč", "kýbl",
            "naběračka", "peněženka", "plot", "sešit", "sušák", "trakař",
            "vana", "žebřík", "žehlička",
        ],
        "asks": [
            "jsou to zároveň části tunelu",
            "jsou to zároveň jména českých měst",
            "jsou v názvech Shakespearových her",
            "mají v sobě dvě stejná písmena vedle sebe",
        ],
    },
    {
        "id": "v11-silnice",
        "roof": "části silnice",
        "level": "normal",
        "hidden": True,
        "inside": [
            "krajnice", "vozovka", "svodidlo", "násep", "příkop", "obrubník",
        ],
        "outside": [
            "guma", "houpačka", "hrneček", "kabát", "kastrol", "koberec",
            "koš", "matice", "matrace", "prostěradlo", "provaz", "ručník",
            "ubrousek", "vrtačka", "šroub",
        ],
        "asks": [
            "jsou to zároveň části silnice",
            "jsou to znamení zvěrokruhu",
            "jsou v názvech večerníčků",
            "jsou v názvech her Járy Cimrmana",
        ],
    },
    {
        "id": "v11-pila",
        "roof": "části pily",
        "level": "normal",
        "hidden": True,
        "inside": [
            "list", "zub", "rozvod", "plátno", "rukojeť", "rám",
        ],
        "outside": [
            "guma", "hrnec", "lavička", "matice", "naběračka", "náramek",
            "nůžky", "pekáč", "pinzeta", "pravítko", "pytel", "stůl",
            "utěrka", "vrtačka", "šroub",
        ],
        "asks": [
            "jsou to zároveň části pily",
            "jsou to znamení zvěrokruhu",
            "nemají v sobě ani jednu samohlásku",
            "jsou v názvech her Járy Cimrmana",
        ],
    },
    {
        "id": "v11-nuzky",
        "roof": "části nůžek",
        "level": "normal",
        "hidden": True,
        "inside": [
            "břit", "oko", "šroub", "hrot", "rameno", "čelist",
        ],
        "outside": [
            "hadice", "houpačka", "hrábě", "kýbl", "lepidlo", "mýdlo",
            "pouzdro", "rýč", "silnice", "trouba", "truhlík", "vana", "věšák",
            "záclona", "žebřík",
        ],
        "asks": [
            "jsou to zároveň části nůžek",
            "mají v sobě dvě stejná písmena vedle sebe",
            "jsou to zároveň příjmení českých prezidentů",
            "nemají v sobě ani jednu samohlásku",
        ],
    },
    {
        "id": "v11-kladivo",
        "roof": "části kladiva",
        "level": "normal",
        "hidden": True,
        "inside": [
            "hlava", "násada", "klín", "ploška", "nos", "oko",
        ],
        "outside": [
            "hrábě", "lednička", "lopatka", "motyka", "myčka", "mísa",
            "pravítko", "pračka", "provaz", "ramínko", "sklenice",
            "struhadlo", "stůl", "truhlík", "šála",
        ],
        "asks": [
            "jsou to zároveň části kladiva",
            "jsou to zároveň příjmení českých prezidentů",
            "jsou to znamení zvěrokruhu",
            "jsou to zároveň značky nebo modely aut",
        ],
    },
    {
        "id": "v11-stan",
        "roof": "části stanu",
        "level": "normal",
        "hidden": True,
        "inside": [
            "celta", "tropiko", "kolík", "tyč", "podlážka", "napínák",
        ],
        "outside": [
            "batoh", "bunda", "hodinky", "kabát", "kastrol", "kladívko",
            "koberec", "konev", "krém", "lavička", "metr", "pekáč",
            "prostěradlo", "trakař", "šroub",
        ],
        "asks": [
            "jsou to zároveň části stanu",
            "jsou v názvech Shakespearových her",
            "jsou to zároveň značky českého piva",
            "jsou v názvech her Járy Cimrmana",
        ],
    },
    {
        "id": "v11-batoh",
        "roof": "části batohu",
        "level": "normal",
        "hidden": True,
        "inside": [
            "popruh", "přezka", "nosič", "kapsa", "poutko", "stahovák",
        ],
        "outside": [
            "hadr", "kartáček", "kompost", "kýbl", "lednička", "lepidlo",
            "lopata", "naběračka", "nůžky", "ořezávátko", "podnos", "sešit",
            "sporák", "vařečka", "šroub",
        ],
        "asks": [
            "jsou to zároveň části batohu",
            "jsou to zároveň příjmení českých prezidentů",
            "mají v sobě dvě stejná písmena vedle sebe",
            "jsou v názvech večerníčků",
        ],
    },
    {
        "id": "v11-sklarna",
        "roof": "sklářské pojmy",
        "level": "hard",
        "hidden": True,
        "inside": [
            "píšťala", "huť", "brus", "střep", "pánev", "tavba",
        ],
        "outside": [
            "deka", "kartáček", "koště", "krém", "lopata", "myčka",
            "naběračka", "parapet", "police", "provaz", "struhadlo", "trakař",
            "trouba", "truhlík", "ubrus",
        ],
        "asks": [
            "jsou to zároveň sklářské pojmy",
            "nemají v sobě ani jednu samohlásku",
            "jsou to zároveň příjmení českých prezidentů",
            "jsou to zároveň jména českých měst",
        ],
    },
    {
        "id": "v11-mlynarstvi",
        "roof": "mlynářské pojmy",
        "level": "hard",
        "hidden": True,
        "inside": [
            "otruby", "šrot", "krupice", "vejražka", "pytlování", "složení",
        ],
        "outside": [
            "brýle", "guma", "hadice", "hrábě", "kabát", "kladívko", "komoda",
            "koš", "lopatka", "pilník", "plot", "podnos", "semínko", "tácek",
            "žehlička",
        ],
        "asks": [
            "jsou to zároveň mlynářské pojmy",
            "jsou to zároveň jména českých měst",
            "čtou se stejně zepředu i zezadu",
            "jsou v názvech her Járy Cimrmana",
        ],
    },
    {
        "id": "v11-lihovar",
        "roof": "lihovarnické pojmy",
        "level": "hard",
        "hidden": True,
        "inside": [
            "zápara", "kvas", "úkap", "dokap", "kotel", "destilát",
        ],
        "outside": [
            "deštník", "hoblík", "kýbl", "lopata", "metr", "pilník",
            "pinzeta", "popelnice", "pravítko", "propiska", "ručník",
            "schránka", "trouba", "vrtačka", "záclona",
        ],
        "asks": [
            "jsou to zároveň lihovarnické pojmy",
            "jsou to zároveň značky nebo modely aut",
            "jsou to zároveň jména českých měst",
            "jsou to zároveň příjmení českých prezidentů",
        ],
    },
    {
        "id": "v11-cukrarna",
        "roof": "cukrářské pojmy",
        "level": "normal",
        "hidden": True,
        "inside": [
            "poleva", "korpus", "krém", "marcipán", "šlehačka", "piškot",
        ],
        "outside": [
            "hrábě", "kartáček", "kastrol", "kladívko", "kleště", "lednička",
            "lepidlo", "lopata", "mrkev", "myčka", "pračka", "schránka",
            "sušák", "svěrák", "vana",
        ],
        "asks": [
            "jsou to zároveň cukrářské pojmy",
            "jsou to zároveň značky českého piva",
            "čtou se stejně zepředu i zezadu",
            "jsou v názvech Shakespearových her",
        ],
    },
    {
        "id": "v11-reznictvi",
        "roof": "řeznické pojmy",
        "level": "normal",
        "hidden": True,
        "inside": [
            "bourání", "výsek", "špek", "střívko", "kýta", "plec",
        ],
        "outside": [
            "hřebík", "kompost", "kýbl", "lednička", "lopata", "parapet",
            "peřina", "pinzeta", "plot", "police", "pytel", "ramínko",
            "svěrák", "ubrousek", "ubrus",
        ],
        "asks": [
            "jsou to zároveň řeznické pojmy",
            "jsou to znamení zvěrokruhu",
            "jsou to zároveň značky nebo modely aut",
            "jsou to zároveň jména českých měst",
        ],
    },
    {
        "id": "v11-klempirstvi",
        "roof": "klempířské pojmy",
        "level": "hard",
        "hidden": True,
        "inside": [
            "falc", "lem", "svod", "okap", "úžlabí", "lišta",
        ],
        "outside": [
            "kbelík", "parapet", "pilník", "pinzeta", "polštář", "popelnice",
            "rohožka", "sešit", "sporák", "trakař", "tácek", "ubrus",
            "utěrka", "věšák", "žehlička",
        ],
        "asks": [
            "jsou to zároveň klempířské pojmy",
            "jsou to znamení zvěrokruhu",
            "jsou to zároveň značky českého piva",
            "mají v sobě dvě stejná písmena vedle sebe",
        ],
    },
    {
        "id": "v11-pokryvacstvi",
        "roof": "pokrývačské pojmy",
        "level": "hard",
        "hidden": True,
        "inside": [
            "latě", "bobrovka", "hřebenáč", "šindel", "došek", "plech",
        ],
        "outside": [
            "brambora", "hadice", "kabát", "kastrol", "kladívko", "lepidlo",
            "metr", "polštář", "propiska", "prostěradlo", "rohožka", "sešit",
            "smeták", "vana", "věšák",
        ],
        "asks": [
            "jsou to zároveň pokrývačské pojmy",
            "jsou to zároveň příjmení českých prezidentů",
            "jsou to zároveň jména českých měst",
            "čtou se stejně zepředu i zezadu",
        ],
    },
    {
        "id": "v11-zamecnictvi",
        "roof": "zámečnické pojmy",
        "level": "normal",
        "hidden": True,
        "inside": [
            "závit", "zápich", "výpalek", "ohýbačka", "nýtování", "dořez",
        ],
        "outside": [
            "bunda", "dřez", "kastrol", "koš", "koště", "krém", "lopatka",
            "mísa", "mýdlo", "naběračka", "peněženka", "pouzdro", "pytel",
            "sešit", "šuplík",
        ],
        "asks": [
            "jsou to zároveň zámečnické pojmy",
            "jsou to zároveň značky nebo modely aut",
            "jsou to zároveň jména českých měst",
            "jsou v názvech her Járy Cimrmana",
        ],
    },
    {
        "id": "v11-sedlarstvi",
        "roof": "sedlářské pojmy",
        "level": "hard",
        "hidden": True,
        "inside": [
            "useň", "řemen", "dratev", "šídlo", "přezka", "podšívka",
        ],
        "outside": [
            "batoh", "brýle", "hadr", "houpačka", "kartáček", "koberec",
            "kompost", "lepidlo", "metr", "myčka", "peněženka", "postel",
            "pouzdro", "struhadlo", "šála",
        ],
        "asks": [
            "jsou to zároveň sedlářské pojmy",
            "mají v sobě dvě stejná písmena vedle sebe",
            "jsou to zároveň značky nebo modely aut",
            "nemají v sobě ani jednu samohlásku",
        ],
    },
    {
        "id": "v11-kolarstvi",
        "roof": "kolářské pojmy",
        "level": "hard",
        "hidden": True,
        "inside": [
            "loukoť", "ráf", "paprsek", "náboj", "obruč", "šprušle",
        ],
        "outside": [
            "brýle", "hadice", "kleště", "koberec", "kompost", "krém", "metr",
            "myčka", "náramek", "semínko", "sešit", "silnice", "sklenice",
            "sporák", "šuplík",
        ],
        "asks": [
            "jsou to zároveň kolářské pojmy",
            "jsou to zároveň jména českých měst",
            "mají v sobě dvě stejná písmena vedle sebe",
            "jsou v názvech Shakespearových her",
        ],
    },
    {
        "id": "v11-bednarstvi",
        "roof": "bednářské pojmy",
        "level": "hard",
        "hidden": True,
        "inside": [
            "dužina", "obruč", "věnec", "stahování", "opalování",
            "drážkování",
        ],
        "outside": [
            "chleba", "hadr", "kastrol", "koš", "matice", "naběračka",
            "pekáč", "plot", "police", "struhadlo", "svěrák", "trakař",
            "ubrousek", "věšák", "žebřík",
        ],
        "asks": [
            "jsou to zároveň bednářské pojmy",
            "jsou to znamení zvěrokruhu",
            "jsou v názvech večerníčků",
            "mají v sobě dvě stejná písmena vedle sebe",
        ],
    },
    {
        "id": "v11-provaznictvi",
        "roof": "provaznické pojmy",
        "level": "hard",
        "hidden": True,
        "inside": [
            "pramen", "splétání", "konopí", "očko", "oplet", "stáčení",
        ],
        "outside": [
            "branka", "kastrol", "konev", "krém", "lednička", "myčka",
            "peněženka", "pilník", "rohožka", "rýč", "sklenice", "svěrák",
            "ubrus", "zahrada", "šroub",
        ],
        "asks": [
            "jsou to zároveň provaznické pojmy",
            "jsou to zároveň značky nebo modely aut",
            "jsou to zároveň značky českého piva",
            "mají v sobě dvě stejná písmena vedle sebe",
        ],
    },
    {
        "id": "v11-zlatnictvi",
        "roof": "zlatnické pojmy",
        "level": "hard",
        "hidden": True,
        "inside": [
            "ryzost", "puncovní", "zapuštění", "filigrán", "pájka", "lůžko",
        ],
        "outside": [
            "brambora", "deštník", "hřebík", "kleště", "lopata", "myčka",
            "ořezávátko", "parapet", "plot", "popelnice", "pravítko", "stůl",
            "sušák", "zahrada", "zápisník",
        ],
        "asks": [
            "jsou to zároveň zlatnické pojmy",
            "jsou to zároveň jména českých měst",
            "jsou to zároveň značky nebo modely aut",
            "jsou to zároveň příjmení českých prezidentů",
        ],
    },
    {
        "id": "v11-optika",
        "roof": "optické pojmy",
        "level": "hard",
        "hidden": True,
        "inside": [
            "čočka", "ohnisko", "clona", "hranol", "zrcadlo", "lom",
        ],
        "outside": [
            "branka", "deštník", "guma", "hadice", "květináč", "kýbl",
            "lampa", "myčka", "mýdlo", "ořezávátko", "propiska", "sešit",
            "vrtačka", "zápisník", "šuplík",
        ],
        "asks": [
            "jsou to zároveň optické pojmy",
            "mají v sobě dvě stejná písmena vedle sebe",
            "jsou to zároveň jména českých měst",
            "nemají v sobě ani jednu samohlásku",
        ],
    },
    {
        "id": "v11-geodezie",
        "roof": "geodetické pojmy",
        "level": "hard",
        "hidden": True,
        "inside": [
            "nivelace", "polygon", "záměra", "převýšení", "vytyčení", "bod",
        ],
        "outside": [
            "branka", "hrnec", "kabát", "koberec", "květináč", "lampa",
            "lavička", "mrkev", "myčka", "peněženka", "pračka", "rohožka",
            "skříň", "stůl", "žehlička",
        ],
        "asks": [
            "jsou to zároveň geodetické pojmy",
            "mají v sobě schované zvíře",
            "čtou se stejně zepředu i zezadu",
            "jsou to zároveň příjmení českých prezidentů",
        ],
    },
    {
        "id": "v11-archeologie",
        "roof": "archeologické pojmy",
        "level": "hard",
        "hidden": True,
        "inside": [
            "sonda", "vrstva", "mohyla", "střep", "nález", "datace",
        ],
        "outside": [
            "brýle", "dřez", "kbelík", "kladívko", "kleště", "koberec",
            "komoda", "koš", "koště", "mrkev", "nůžky", "peněženka",
            "rohožka", "skříň", "vana",
        ],
        "asks": [
            "jsou to zároveň archeologické pojmy",
            "mají v sobě schované zvíře",
            "jsou to zároveň jména českých měst",
            "jsou v názvech her Járy Cimrmana",
        ],
    },
    {
        "id": "v11-archiv",
        "roof": "archivní pojmy",
        "level": "hard",
        "hidden": True,
        "inside": [
            "fond", "skartace", "inventář", "karton", "signatura",
            "badatelna",
        ],
        "outside": [
            "brambora", "brýle", "hoblík", "kleště", "koberec", "kolík",
            "kýbl", "lampa", "matrace", "pilník", "plot", "podnos", "postel",
            "skříň", "žehlička",
        ],
        "asks": [
            "jsou to zároveň archivní pojmy",
            "čtou se stejně zepředu i zezadu",
            "mají v sobě schované zvíře",
            "jsou to zároveň jména českých měst",
        ],
    },
    {
        "id": "v11-muzeum",
        "roof": "muzejní pojmy",
        "level": "normal",
        "hidden": True,
        "inside": [
            "sbírka", "vitrína", "depozitář", "popiska", "kurátor",
            "akvizice",
        ],
        "outside": [
            "brambora", "houpačka", "hřeben", "kladívko", "konev",
            "ořezávátko", "pekáč", "podnos", "pravítko", "prostěradlo",
            "pytel", "struhadlo", "svěrák", "ubrousek", "vrtačka",
        ],
        "asks": [
            "jsou to zároveň muzejní pojmy",
            "jsou v názvech her Járy Cimrmana",
            "jsou to zároveň příjmení českých prezidentů",
            "jsou v názvech večerníčků",
        ],
    },
    {
        "id": "v11-hute",
        "roof": "hutnické pojmy",
        "level": "hard",
        "hidden": True,
        "inside": [
            "vysoká", "struska", "koks", "vsázka", "surovina", "odpich",
        ],
        "outside": [
            "deštník", "dřez", "hrneček", "hřeben", "kýbl", "naběračka",
            "náramek", "parapet", "pouzdro", "semínko", "sešit", "sud",
            "sušák", "šroub", "šála",
        ],
        "asks": [
            "jsou to zároveň hutnické pojmy",
            "jsou v názvech Shakespearových her",
            "jsou to zároveň jména českých měst",
            "jsou v názvech večerníčků",
        ],
    },
    {
        "id": "v11-slevarna",
        "roof": "slévárenské pojmy",
        "level": "hard",
        "hidden": True,
        "inside": [
            "forma", "jádro", "model", "licí", "nálitek", "kokila",
        ],
        "outside": [
            "brýle", "bunda", "hrnec", "kartáček", "komoda", "lampa",
            "matrace", "myčka", "peněženka", "ponožka", "silnice", "trouba",
            "utěrka", "zahrada", "šuplík",
        ],
        "asks": [
            "jsou to zároveň slévárenské pojmy",
            "čtou se stejně zepředu i zezadu",
            "jsou to zároveň značky nebo modely aut",
            "mají v sobě dvě stejná písmena vedle sebe",
        ],
    },
    {
        "id": "v11-potapeni",
        "roof": "potápěčské pojmy",
        "level": "normal",
        "hidden": True,
        "inside": [
            "ploutve", "maska", "automatika", "zátěž", "lahev", "výstup",
        ],
        "outside": [
            "deštník", "guma", "hřebík", "kladívko", "koberec", "lopata",
            "motyka", "mísa", "pilník", "rýč", "struhadlo", "tácek", "vana",
            "vrtačka", "zápisník",
        ],
        "asks": [
            "jsou to zároveň potápěčské pojmy",
            "jsou v názvech Shakespearových her",
            "jsou to zároveň značky nebo modely aut",
            "jsou to znamení zvěrokruhu",
        ],
    },
    {
        "id": "v11-jachting",
        "roof": "jachtařské pojmy",
        "level": "hard",
        "hidden": True,
        "inside": [
            "otěž", "kýl", "ráhno", "obrat", "hals", "kosatka",
        ],
        "outside": [
            "batoh", "bunda", "hodinky", "hřebík", "kabát", "kladívko",
            "konev", "květináč", "matice", "matrace", "metr", "motyka",
            "myčka", "police", "prostěradlo",
        ],
        "asks": [
            "jsou to zároveň jachtařské pojmy",
            "jsou v názvech večerníčků",
            "čtou se stejně zepředu i zezadu",
            "jsou to zároveň příjmení českých prezidentů",
        ],
    },
    {
        "id": "v11-lekarna",
        "roof": "lékárnické pojmy",
        "level": "normal",
        "hidden": True,
        "inside": [
            "recept", "výdej", "tinktura", "mast", "čípek", "magistraliter",
        ],
        "outside": [
            "guma", "hrábě", "kabát", "kladívko", "lavička", "matrace",
            "myčka", "nůžky", "polštář", "postel", "prostěradlo", "ramínko",
            "smeták", "ubrousek", "žebřík",
        ],
        "asks": [
            "jsou to zároveň lékárnické pojmy",
            "nemají v sobě ani jednu samohlásku",
            "jsou v názvech Shakespearových her",
            "mají v sobě dvě stejná písmena vedle sebe",
        ],
    },
    {
        "id": "v11-zubar",
        "roof": "zubařské pojmy",
        "level": "normal",
        "hidden": True,
        "inside": [
            "plomba", "můstek", "kaz", "vrtačka", "otisk", "korunka",
        ],
        "outside": [
            "batoh", "chleba", "deštník", "hadice", "hřebík", "lednička",
            "metr", "podnos", "ručník", "semínko", "sešit", "trakař",
            "trouba", "vysavač", "šroub",
        ],
        "asks": [
            "jsou to zároveň zubařské pojmy",
            "nemají v sobě ani jednu samohlásku",
            "jsou v názvech Shakespearových her",
            "jsou v názvech her Járy Cimrmana",
        ],
    },
    {
        "id": "v11-statistika",
        "roof": "statistické pojmy",
        "level": "hard",
        "hidden": True,
        "inside": [
            "medián", "průměr", "rozptyl", "výběr", "četnost", "odchylka",
        ],
        "outside": [
            "branka", "deštník", "hoblík", "kolík", "matrace", "motyka",
            "myčka", "mýdlo", "náramek", "podnos", "popelnice", "propiska",
            "ručník", "schránka", "sklenice",
        ],
        "asks": [
            "jsou to zároveň statistické pojmy",
            "nemají v sobě ani jednu samohlásku",
            "jsou to zároveň jména českých měst",
            "jsou to zároveň značky českého piva",
        ],
    },
    {
        "id": "v11-zeleny",
        "roof": "slova, která tvoří spojení se slovem zelený",
        "level": "normal",
        "hidden": True,
        "inside": [
            "čtvrtek", "vlna", "kácení", "karta", "střecha", "zelí",
        ],
        "outside": [
            "sešit", "koště", "ubrus", "rohožka", "propiska", "záclona",
            "houpačka", "tácek", "ramínko", "ubrousek",
        ],
        "asks": [
            "tvoří se slovem zelený ustálené spojení",
            "nemají v sobě ani jednu samohlásku",
            "jsou to zároveň značky českého piva",
            "mají v sobě dvě stejná písmena vedle sebe",
        ],
    },
    {
        "id": "v11-modry",
        "roof": "slova, která tvoří spojení se slovem modrý",
        "level": "normal",
        "hidden": True,
        "inside": [
            "krev", "pondělí", "kód", "hodina", "helma", "velryba",
        ],
        "outside": [
            "sešit", "koště", "ubrus", "rohožka", "propiska", "záclona",
            "houpačka", "tácek", "ramínko", "ubrousek",
        ],
        "asks": [
            "tvoří se slovem modrý ustálené spojení",
            "jsou to zároveň značky českého piva",
            "mají v sobě schované zvíře",
            "jsou v názvech večerníčků",
        ],
    },
    {
        "id": "v11-sladky",
        "roof": "slova, která tvoří spojení se slovem sladký",
        "level": "normal",
        "hidden": True,
        "inside": [
            "život", "spánek", "řeči", "brambor", "voda", "odplata",
        ],
        "outside": [
            "sešit", "koště", "ubrus", "rohožka", "propiska", "záclona",
            "houpačka", "tácek", "ramínko", "ubrousek",
        ],
        "asks": [
            "tvoří se slovem sladký ustálené spojení",
            "mají v sobě schované zvíře",
            "čtou se stejně zepředu i zezadu",
            "jsou v názvech her Járy Cimrmana",
        ],
    },
    {
        "id": "v11-mekky",
        "roof": "slova, která tvoří spojení se slovem měkký",
        "level": "normal",
        "hidden": True,
        "inside": [
            "srdce", "voda", "souhláska", "podnebí", "přistání", "nábytek",
        ],
        "outside": [
            "sešit", "koště", "ubrus", "rohožka", "propiska", "záclona",
            "houpačka", "tácek", "ramínko", "ubrousek",
        ],
        "asks": [
            "tvoří se slovem měkký ustálené spojení",
            "nemají v sobě ani jednu samohlásku",
            "čtou se stejně zepředu i zezadu",
            "jsou to zároveň značky českého piva",
        ],
    },
    {
        "id": "v11-lehky",
        "roof": "slova, která tvoří spojení se slovem lehký",
        "level": "normal",
        "hidden": True,
        "inside": [
            "váha", "průmysl", "atletika", "spánek", "zbraň", "dívka",
        ],
        "outside": [
            "sešit", "koště", "ubrus", "rohožka", "propiska", "záclona",
            "houpačka", "tácek", "ramínko", "ubrousek",
        ],
        "asks": [
            "tvoří se slovem lehký ustálené spojení",
            "jsou to znamení zvěrokruhu",
            "jsou v názvech Shakespearových her",
            "jsou to zároveň příjmení českých prezidentů",
        ],
    },
    {
        "id": "v11-kratky",
        "roof": "slova, která tvoří spojení se slovem krátký",
        "level": "normal",
        "hidden": True,
        "inside": [
            "spoj", "proces", "paměť", "konec", "vlna", "slámka",
        ],
        "outside": [
            "sešit", "koště", "ubrus", "rohožka", "propiska", "záclona",
            "houpačka", "tácek", "ramínko", "ubrousek",
        ],
        "asks": [
            "tvoří se slovem krátký ustálené spojení",
            "jsou to zároveň příjmení českých prezidentů",
            "jsou v názvech večerníčků",
            "mají v sobě dvě stejná písmena vedle sebe",
        ],
    },
    {
        "id": "v11-vysoky",
        "roof": "slova, která tvoří spojení se slovem vysoký",
        "level": "normal",
        "hidden": True,
        "inside": [
            "napětí", "škola", "pec", "sazba", "tlak", "společnost",
        ],
        "outside": [
            "sešit", "koště", "ubrus", "rohožka", "propiska", "záclona",
            "houpačka", "tácek", "ramínko", "ubrousek",
        ],
        "asks": [
            "tvoří se slovem vysoký ustálené spojení",
            "mají v sobě schované zvíře",
            "mají v sobě dvě stejná písmena vedle sebe",
            "jsou to znamení zvěrokruhu",
        ],
    },
    {
        "id": "v11-silny",
        "roof": "slova, která tvoří spojení se slovem silný",
        "level": "normal",
        "hidden": True,
        "inside": [
            "kafe", "stránka", "kuřák", "žaludek", "slovo", "proud",
        ],
        "outside": [
            "sešit", "koště", "ubrus", "rohožka", "propiska", "záclona",
            "houpačka", "tácek", "ramínko", "ubrousek",
        ],
        "asks": [
            "tvoří se slovem silný ustálené spojení",
            "jsou to zároveň značky nebo modely aut",
            "mají v sobě dvě stejná písmena vedle sebe",
            "jsou to zároveň příjmení českých prezidentů",
        ],
    },
    {
        "id": "v11-prazdny",
        "roof": "slova, která tvoří spojení se slovem prázdný",
        "level": "normal",
        "hidden": True,
        "inside": [
            "slib", "žaludek", "hlava", "kapsa", "hrozba", "schránka",
        ],
        "outside": [
            "sešit", "koště", "ubrus", "rohožka", "propiska", "záclona",
            "houpačka", "tácek", "ramínko", "ubrousek",
        ],
        "asks": [
            "tvoří se slovem prázdný ustálené spojení",
            "čtou se stejně zepředu i zezadu",
            "nemají v sobě ani jednu samohlásku",
            "mají v sobě dvě stejná písmena vedle sebe",
        ],
    },
    {
        "id": "v11-divoky",
        "roof": "slova, která tvoří spojení se slovem divoký",
        "level": "normal",
        "hidden": True,
        "inside": [
            "západ", "kachna", "voda", "víno", "karta", "stávka",
        ],
        "outside": [
            "sešit", "koště", "ubrus", "rohožka", "propiska", "záclona",
            "houpačka", "tácek", "ramínko", "ubrousek",
        ],
        "asks": [
            "tvoří se slovem divoký ustálené spojení",
            "jsou v názvech her Járy Cimrmana",
            "mají v sobě schované zvíře",
            "mají v sobě dvě stejná písmena vedle sebe",
        ],
    },
    {
        "id": "v11-ost",
        "roof": "slova končící na -ost",
        "level": "normal",
        "hidden": True,
        "inside": [
            "radost", "mladost", "kost", "most", "starost", "rychlost",
            "moudrost", "vlhkost",
        ],
        "outside": [
            "lampa", "police", "koberec", "sešit", "motyka", "konev",
            "ručník", "hrnec", "kbelík", "žebřík",
        ],
        "asks": [
            "končí na písmena ost",
            "jsou v názvech Shakespearových her",
            "jsou to znamení zvěrokruhu",
            "jsou to zároveň jména českých měst",
        ],
    },
    {
        "id": "v11-kraje-abeceda",
        "roof": "slova, jejichž první a poslední písmeno jdou v abecedě po sobě",
        "level": "hard",
        "hidden": True,
        "inside": [
            "dítě", "dveře", "svět", "smrt", "duše", "pivo", "král", "právo",
        ],
        "outside": [
            "lampa", "police", "koberec", "motyka", "konev", "ručník",
            "hrnec", "kbelík", "žebřík", "kolík",
        ],
        "asks": [
            "mají první a poslední písmeno vedle sebe v abecedě",
            "čtou se stejně zepředu i zezadu",
            "jsou to znamení zvěrokruhu",
            "jsou to zároveň značky nebo modely aut",
        ],
    },
    {
        "id": "v11-pul-na-pul",
        "roof": "slova s stejným počtem samohlásek a souhlásek",
        "level": "hard",
        "hidden": True,
        "inside": [
            "kolo", "nota", "ruka", "voda", "pila", "míra", "husa", "vosa",
        ],
        "outside": [
            "koberec", "žebřík", "propiska", "prostěradlo", "struhadlo",
            "naběračka", "záclona", "rohožka", "koště", "hrneček",
        ],
        "asks": [
            "mají stejně samohlásek jako souhlásek",
            "mají v sobě dvě stejná písmena vedle sebe",
            "jsou to zároveň značky nebo modely aut",
            "jsou v názvech Shakespearových her",
        ],
    },
    {
        "id": "v11-bez-posledniho",
        "roof": "slova, ze kterých po useknutí posledního písmene zbude jiné slovo",
        "level": "hard",
        "hidden": True,
        "inside": [
            "hrad", "sklon", "prst", "lesk", "sport", "past", "radar",
        ],
        "outside": [
            "lampa", "police", "koberec", "sešit", "motyka", "konev",
            "kbelík", "žebřík", "kolík", "provaz",
        ],
        "asks": [
            "po useknutí posledního písmene dají jiné slovo",
            "mají v sobě schované zvíře",
            "mají v sobě dvě stejná písmena vedle sebe",
            "jsou v názvech her Járy Cimrmana",
        ],
    },
    {
        "id": "v11-pozpatku",
        "roof": "slova, která pozpátku dají jiné slovo",
        "level": "hard",
        "hidden": True,
        "inside": [
            "kos", "sok", "tak", "kat", "mol", "lom", "los", "sol", "kus",
            "suk", "kar", "rak", "vor",
        ],
        "outside": [
            "lampa", "police", "koberec", "sešit", "motyka", "konev",
            "ručník", "hrnec", "kbelík", "žebřík",
        ],
        "asks": [
            "pozpátku dají jiné slovo",
            "jsou v názvech Shakespearových her",
            "jsou to znamení zvěrokruhu",
            "nemají v sobě ani jednu samohlásku",
        ],
    },
    {
        "id": "v11-sykavky",
        "roof": "slova s č, š nebo ž",
        "level": "normal",
        "hidden": True,
        "inside": [
            "čaj", "šála", "žula", "kožich", "čep", "šroub", "žebřík", "kaše",
        ],
        "outside": [
            "lampa", "police", "koberec", "motyka", "konev", "hrnec", "kolík",
            "deka", "provaz", "kniha",
        ],
        "asks": [
            "mají v sobě č, š nebo ž",
            "jsou v názvech her Járy Cimrmana",
            "jsou to zároveň jména českých měst",
            "jsou to zároveň značky nebo modely aut",
        ],
    },
    {
        "id": "v11-bez-diakritiky",
        "roof": "slova bez jediné čárky a háčku",
        "level": "normal",
        "hidden": True,
        "inside": [
            "kolo", "lampa", "okno", "strom", "ruka", "voda", "hlava",
            "kniha",
        ],
        "outside": [
            "žebřík", "záclona", "rohožka", "šuplík", "ručník", "kýbl",
            "košík", "věšák", "hřebík", "příbor",
        ],
        "asks": [
            "nemají v sobě jedinou čárku ani háček",
            "jsou v názvech večerníčků",
            "nemají v sobě ani jednu samohlásku",
            "jsou to zároveň značky nebo modely aut",
        ],
    },
    {
        "id": "v11-vancura",
        "roof": "slova z názvů knih Vladislava Vančury",
        "level": "hard",
        "hidden": True,
        "inside": [
            "pekař", "léto", "luk", "královna", "pole", "konec", "útěk",
        ],
        "outside": [
            "brambora", "brýle", "dřez", "hrábě", "kolík", "lopata",
            "ořezávátko", "semínko", "silnice", "sporák", "trouba", "utěrka",
            "zahrada", "zápisník", "žebřík",
        ],
        "asks": [
            "jsou v názvech knih Vladislava Vančury",
            "jsou to zároveň značky českého piva",
            "mají v sobě dvě stejná písmena vedle sebe",
            "jsou v názvech her Járy Cimrmana",
        ],
    },
    {
        "id": "v11-lada",
        "roof": "slova z názvů knih Josefa Lady",
        "level": "normal",
        "hidden": True,
        "inside": [
            "mikeš", "bubáci", "hastrmani", "liška", "kmotra", "vzpomínky",
            "kalendář",
        ],
        "outside": [
            "branka", "guma", "kbelík", "kleště", "koberec", "koště", "krém",
            "lednička", "lopata", "matice", "metr", "pinzeta", "police",
            "trakař", "řetízek",
        ],
        "asks": [
            "jsou v názvech knih Josefa Lady",
            "jsou to znamení zvěrokruhu",
            "jsou v názvech večerníčků",
            "jsou v názvech Shakespearových her",
        ],
    },
    {
        "id": "v11-kastner",
        "roof": "slova z názvů knih Ericha Kästnera",
        "level": "normal",
        "hidden": True,
        "inside": [
            "detektivové", "třída", "luisa", "lotka", "bod", "muž",
            "trpaslík",
        ],
        "outside": [
            "houpačka", "hrnec", "kleště", "koberec", "koště", "krém", "kýbl",
            "lampa", "lopatka", "mrkev", "mísa", "pytel", "rýč", "sešit",
            "záclona",
        ],
        "asks": [
            "jsou v názvech knih Ericha Kästnera",
            "jsou to znamení zvěrokruhu",
            "mají v sobě dvě stejná písmena vedle sebe",
            "jsou to zároveň značky nebo modely aut",
        ],
    },
    {
        "id": "v11-twain",
        "roof": "slova z názvů knih Marka Twaina",
        "level": "normal",
        "hidden": True,
        "inside": [
            "dobrodružství", "princ", "chuďas", "yankee", "dvůr", "žabák",
            "deník",
        ],
        "outside": [
            "brambora", "houpačka", "hrneček", "kastrol", "lopatka", "metr",
            "motyka", "naběračka", "pinzeta", "sešit", "sklenice", "sporák",
            "svěrák", "trouba", "řetízek",
        ],
        "asks": [
            "jsou v názvech knih Marka Twaina",
            "jsou v názvech her Járy Cimrmana",
            "mají v sobě schované zvíře",
            "jsou to znamení zvěrokruhu",
        ],
    },
    {
        "id": "v11-london",
        "roof": "slova z názvů knih Jacka Londona",
        "level": "hard",
        "hidden": True,
        "inside": [
            "tesák", "volání", "divočina", "vlk", "tulák", "hvězdy", "oheň",
        ],
        "outside": [
            "deka", "hadr", "hoblík", "kabát", "kbelík", "naběračka",
            "podnos", "pouzdro", "prostěradlo", "pytel", "struhadlo",
            "truhlík", "ubrousek", "utěrka", "vysavač",
        ],
        "asks": [
            "jsou v názvech knih Jacka Londona",
            "jsou to znamení zvěrokruhu",
            "mají v sobě dvě stejná písmena vedle sebe",
            "čtou se stejně zepředu i zezadu",
        ],
    },
    {
        "id": "v11-kipling",
        "roof": "slova z názvů knih Rudyarda Kiplinga",
        "level": "hard",
        "hidden": True,
        "inside": [
            "džungle", "kniha", "statečný", "kapitán", "světlo", "hoch",
            "pohádky",
        ],
        "outside": [
            "bunda", "deka", "deštník", "dřez", "hrábě", "kolík", "krém",
            "lopatka", "polštář", "postel", "pravítko", "ramínko", "smeták",
            "trouba", "šála",
        ],
        "asks": [
            "jsou v názvech knih Rudyarda Kiplinga",
            "jsou v názvech večerníčků",
            "nemají v sobě ani jednu samohlásku",
            "jsou v názvech her Járy Cimrmana",
        ],
    },
    {
        "id": "v11-polacek",
        "roof": "slova z názvů knih Karla Poláčka",
        "level": "hard",
        "hidden": True,
        "inside": [
            "muži", "město", "hostinec", "stůl", "dům", "bylo", "kámen",
        ],
        "outside": [
            "dřez", "hadice", "hadr", "kompost", "metr", "motyka",
            "ořezávátko", "plot", "pouzdro", "propiska", "skříň", "sporák",
            "svěrák", "řetízek", "šuplík",
        ],
        "asks": [
            "jsou v názvech knih Karla Poláčka",
            "čtou se stejně zepředu i zezadu",
            "mají v sobě dvě stejná písmena vedle sebe",
            "jsou v názvech her Járy Cimrmana",
        ],
    },
    {
        "id": "v11-chytilova",
        "roof": "slova z názvů filmů Věry Chytilové",
        "level": "hard",
        "hidden": True,
        "inside": [
            "sedmikrásky", "ovoce", "stromy", "panelstory", "kalamita",
            "faunovo", "pasti",
        ],
        "outside": [
            "bunda", "hrnec", "hřebík", "kartáček", "konev", "koště",
            "lopatka", "ořezávátko", "postel", "rohožka", "schránka",
            "ubrousek", "ubrus", "šála", "žebřík",
        ],
        "asks": [
            "jsou v názvech filmů Věry Chytilové",
            "jsou to znamení zvěrokruhu",
            "jsou v názvech Shakespearových her",
            "jsou to zároveň jména českých měst",
        ],
    },
    {
        "id": "v11-kubrick",
        "roof": "slova z názvů filmů Stanleyho Kubricka",
        "level": "hard",
        "hidden": True,
        "inside": [
            "odysea", "pomeranč", "vesmír", "lesk", "sláva", "oči",
            "zabijáci",
        ],
        "outside": [
            "brambora", "chleba", "hadr", "hodinky", "hrneček", "hrábě",
            "kabát", "kastrol", "kolík", "matice", "pekáč", "ponožka",
            "postel", "sud", "utěrka",
        ],
        "asks": [
            "jsou v názvech filmů Stanleyho Kubricka",
            "jsou to zároveň značky českého piva",
            "jsou to zároveň jména českých měst",
            "mají v sobě dvě stejná písmena vedle sebe",
        ],
    },
    {
        "id": "v11-balety",
        "roof": "slova z názvů baletů",
        "level": "normal",
        "hidden": True,
        "inside": [
            "jezero", "louskáček", "růženka", "petruška", "spartakus",
            "labuť", "šípková",
        ],
        "outside": [
            "brýle", "guma", "hrábě", "kabát", "kladívko", "kleště",
            "kompost", "mrkev", "náramek", "ponožka", "stůl", "truhlík",
            "ubrus", "utěrka", "vysavač",
        ],
        "asks": [
            "jsou v názvech slavných baletů",
            "jsou v názvech večerníčků",
            "jsou to zároveň značky nebo modely aut",
            "jsou to zároveň jména českých měst",
        ],
    },
    {
        "id": "v11-praska",
        "roof": "věci, které v ohni praskají",
        "level": "normal",
        "hidden": True,
        "inside": [
            "kaštan", "kukuřice", "bambus", "jalovec", "vejce", "brambora",
        ],
        "outside": [
            "kámen", "cihla", "písek", "hlína", "sklo", "kov", "beton",
            "popel", "struska", "vápno",
        ],
        "asks": [
            "v ohni praskají",
            "jsou to zároveň značky českého piva",
            "jsou to zároveň jména českých měst",
            "jsou v názvech her Járy Cimrmana",
        ],
    },
    {
        "id": "v11-tahne",
        "roof": "věci, které se v teple táhnou",
        "level": "normal",
        "hidden": True,
        "inside": [
            "sýr", "karamel", "guma", "vosk", "asfalt", "žvýkačka",
        ],
        "outside": [
            "sklo", "kámen", "cihla", "kov", "porcelán", "dřevo", "papír",
            "písek", "křída", "sůl",
        ],
        "asks": [
            "se v teple táhnou",
            "nemají v sobě ani jednu samohlásku",
            "mají v sobě dvě stejná písmena vedle sebe",
            "jsou to zároveň jména českých měst",
        ],
    },
    {
        "id": "v11-peni",
        "roof": "věci, které pění",
        "level": "normal",
        "hidden": True,
        "inside": [
            "mýdlo", "pivo", "šampon", "sodovka", "bílek", "moře",
        ],
        "outside": [
            "olej", "med", "sirup", "mléko", "čaj", "rtuť", "petrolej",
            "ocet", "líh", "glycerin",
        ],
        "asks": [
            "pění",
            "nemají v sobě ani jednu samohlásku",
            "jsou v názvech večerníčků",
            "jsou to znamení zvěrokruhu",
        ],
    },
    {
        "id": "v11-lepi",
        "roof": "věci, které lepí",
        "level": "normal",
        "hidden": True,
        "inside": [
            "med", "pryskyřice", "žvýkačka", "lepidlo", "dehet", "karamel",
        ],
        "outside": [
            "písek", "mouka", "sůl", "cukr", "rýže", "krupice", "popel",
            "vápno", "křída", "struska",
        ],
        "asks": [
            "lepí",
            "čtou se stejně zepředu i zezadu",
            "jsou to zároveň příjmení českých prezidentů",
            "mají v sobě dvě stejná písmena vedle sebe",
        ],
    },
    {
        "id": "v11-sviti-po-nasviceni",
        "roof": "věci, které svítí po nasvícení",
        "level": "hard",
        "hidden": True,
        "inside": [
            "ciferník", "hvězdička", "nálepka", "vypínač", "značka",
            "náramek",
        ],
        "outside": [
            "zrcadlo", "sklenice", "mince", "klíč", "lžíce", "brýle",
            "hodinky", "prsten", "knoflík", "sponka",
        ],
        "asks": [
            "svítí ve tmě, když se předtím nasvítí",
            "čtou se stejně zepředu i zezadu",
            "mají v sobě dvě stejná písmena vedle sebe",
            "jsou v názvech večerníčků",
        ],
    },
    {
        "id": "v11-doroste",
        "roof": "části těla, které dorostou",
        "level": "normal",
        "hidden": True,
        "inside": [
            "nehet", "vlas", "paroh", "ocas", "zub", "chlup",
        ],
        "outside": [
            "oko", "ucho", "prst", "noha", "ruka", "koleno", "rameno",
            "loket", "palec", "brada",
        ],
        "asks": [
            "dorostou, když se ustřihnou nebo ztratí",
            "mají v sobě dvě stejná písmena vedle sebe",
            "jsou to zároveň značky českého piva",
            "jsou v názvech večerníčků",
        ],
    },
    {
        "id": "v11-unese",
        "roof": "věci, které unesou dospělého člověka",
        "level": "normal",
        "hidden": True,
        "inside": [
            "led", "lano", "žebřík", "větev", "most", "houpačka",
        ],
        "outside": [
            "nit", "vlas", "papír", "pavučina", "stéblo", "pírko", "bublina",
            "sklo", "sirka", "slámka",
        ],
        "asks": [
            "unesou dospělého člověka",
            "mají v sobě dvě stejná písmena vedle sebe",
            "jsou v názvech her Járy Cimrmana",
            "jsou to zároveň značky nebo modely aut",
        ],
    },
    {
        "id": "v11-chladi",
        "roof": "věci, které chladí bez proudu",
        "level": "hard",
        "hidden": True,
        "inside": [
            "studna", "sklep", "džbán", "vějíř", "stín", "průvan",
        ],
        "outside": [
            "lednička", "mrazák", "klimatizace", "ventilátor", "chladič",
            "kompresor", "výparník", "kryostat", "termostat", "čerpadlo",
        ],
        "asks": [
            "chladí, i když do nich neteče proud",
            "jsou v názvech večerníčků",
            "mají v sobě dvě stejná písmena vedle sebe",
            "jsou v názvech Shakespearových her",
        ],
    },
    {
        "id": "v11-rozpusti-v-ustech",
        "roof": "věci, které se rozpustí v ústech",
        "level": "normal",
        "hidden": True,
        "inside": [
            "čokoláda", "karamel", "cukr", "lentilka", "pastilka", "zmrzlina",
        ],
        "outside": [
            "mrkev", "oříšek", "chleba", "jablko", "sýr", "maso", "rýže",
            "suchar", "sušenka", "kůrka",
        ],
        "asks": [
            "se rozpustí v ústech",
            "jsou to zároveň příjmení českých prezidentů",
            "mají v sobě dvě stejná písmena vedle sebe",
            "nemají v sobě ani jednu samohlásku",
        ],
    },
    {
        "id": "v11-namocit",
        "roof": "věci, které se před použitím namočí",
        "level": "normal",
        "hidden": True,
        "inside": [
            "fazole", "houby", "štětec", "hlína", "špejle", "sádra",
        ],
        "outside": [
            "hřebík", "šroub", "kladivo", "pilník", "klíč", "nůžky", "kolík",
            "matice", "provaz", "drát",
        ],
        "asks": [
            "se před použitím musí namočit",
            "jsou v názvech her Járy Cimrmana",
            "jsou to zároveň značky nebo modely aut",
            "jsou v názvech večerníčků",
        ],
    },
    {
        "id": "v11-naviji",
        "roof": "věci, které se navíjejí na cívku",
        "level": "normal",
        "hidden": True,
        "inside": [
            "nit", "drát", "film", "lano", "páska", "vlasec",
        ],
        "outside": [
            "cihla", "kámen", "mince", "klíč", "hrnec", "sklenice", "deska",
            "talíř", "prkno", "bedna",
        ],
        "asks": [
            "se navíjejí na cívku",
            "nemají v sobě ani jednu samohlásku",
            "mají v sobě schované zvíře",
            "jsou to znamení zvěrokruhu",
        ],
    },
    {
        "id": "v11-skorapka",
        "roof": "věci, které mají skořápku",
        "level": "normal",
        "hidden": True,
        "inside": [
            "vejce", "ořech", "kokos", "mandle", "pistácie", "hlemýžď",
        ],
        "outside": [
            "jahoda", "hruška", "mrkev", "okurka", "salát", "rajče",
            "brambora", "cibule", "dýně", "řepa",
        ],
        "asks": [
            "mají skořápku",
            "jsou v názvech her Járy Cimrmana",
            "jsou to znamení zvěrokruhu",
            "mají v sobě dvě stejná písmena vedle sebe",
        ],
    },
    {
        "id": "v11-podzim",
        "roof": "plodiny, které se sklízejí na podzim",
        "level": "normal",
        "hidden": True,
        "inside": [
            "brambory", "řepa", "dýně", "jablka", "švestky", "kukuřice",
        ],
        "outside": [
            "ředkvička", "jahoda", "salát", "hrášek", "špenát", "třešně",
            "rebarbora", "kedluben", "cibulka", "bylinky",
        ],
        "asks": [
            "se sklízejí až na podzim",
            "mají v sobě schované zvíře",
            "jsou to zároveň jména českých měst",
            "nemají v sobě ani jednu samohlásku",
        ],
    },
    {
        "id": "v11-soli",
        "roof": "jídla, která se solí",
        "level": "normal",
        "hidden": True,
        "inside": [
            "polévka", "brambory", "maso", "vejce", "chleba", "okurka",
        ],
        "outside": [
            "kompot", "povidla", "marmeláda", "perník", "čokoláda", "pudink",
            "zmrzlina", "bábovka", "koláč", "piškot",
        ],
        "asks": [
            "se solí, ne sladí",
            "mají v sobě dvě stejná písmena vedle sebe",
            "mají v sobě schované zvíře",
            "jsou to zároveň příjmení českých prezidentů",
        ],
    },
    {
        "id": "v11-tone",
        "roof": "věci, které v čisté vodě klesnou ke dnu",
        "level": "hard",
        "hidden": True,
        "inside": [
            "kámen", "mince", "hřebík", "cihla", "sklo", "klíč",
        ],
        "outside": [
            "korek", "dřevo", "pěna", "led", "vosk", "plast", "pírko",
            "sláma", "bublina", "papír",
        ],
        "asks": [
            "v čisté vodě klesnou ke dnu",
            "mají v sobě schované zvíře",
            "jsou to zároveň příjmení českých prezidentů",
            "jsou to zároveň značky nebo modely aut",
        ],
    },
    {
        "id": "v11-prazske-vrchy",
        "roof": "pražské vrchy",
        "level": "hard",
        "hidden": True,
        "inside": [
            "Petřín", "Vítkov", "Vyšehrad", "Bohdalec", "Ládví", "Hanspaulka",
            "Barrandov", "Vidoule",
        ],
        "outside": [
            "batoh", "bunda", "deka", "houpačka", "hrneček", "lavička",
            "lopatka", "police", "ponožka", "ramínko", "rohožka", "sešit",
            "truhlík", "záclona", "zápisník",
        ],
        "asks": [
            "jsou to zároveň pražské vrchy",
            "nemají v sobě ani jednu samohlásku",
            "jsou to zároveň příjmení českých prezidentů",
            "jsou to znamení zvěrokruhu",
        ],
    },
    {
        "id": "v11-slovenska-mesta",
        "roof": "slovenská města",
        "level": "hard",
        "hidden": True,
        "inside": [
            "Nitra", "Trnava", "Prešov", "Žilina", "Martin", "Levoča",
            "Poprad", "Zvolen",
        ],
        "outside": [
            "brambora", "deka", "kleště", "matice", "pekáč", "peněženka",
            "peřina", "pravítko", "pračka", "provaz", "rohožka", "semínko",
            "tácek", "zahrada", "řetízek",
        ],
        "asks": [
            "jsou to zároveň slovenská města",
            "mají v sobě dvě stejná písmena vedle sebe",
            "jsou v názvech her Járy Cimrmana",
            "jsou to znamení zvěrokruhu",
        ],
    },
    {
        "id": "v11-metropole",
        "roof": "evropská hlavní města",
        "level": "normal",
        "hidden": True,
        "inside": [
            "Vídeň", "Lisabon", "Oslo", "Helsinky", "Dublin", "Sofie", "Riga",
            "Valletta",
        ],
        "outside": [
            "hřebík", "kolík", "kompost", "lampa", "motyka", "mrkev", "mísa",
            "náramek", "nůžky", "pekáč", "rýč", "schránka", "sešit", "sud",
            "utěrka",
        ],
        "asks": [
            "jsou to zároveň hlavní města evropských států",
            "jsou to zároveň značky českého piva",
            "jsou v názvech her Járy Cimrmana",
            "jsou v názvech večerníčků",
        ],
    },
    {
        "id": "v11-panovnici",
        "roof": "jména českých panovníků",
        "level": "normal",
        "hidden": True,
        "inside": [
            "Václav", "Boleslav", "Vladislav", "Přemysl", "Jiří", "Ferdinand",
            "Rudolf", "Leopold",
        ],
        "outside": [
            "bunda", "deka", "deštník", "hrábě", "kabát", "konev", "koš",
            "lavička", "podnos", "polštář", "rohožka", "schránka", "trouba",
            "vana", "šála",
        ],
        "asks": [
            "jsou to zároveň jména českých panovníků",
            "jsou to zároveň jména českých měst",
            "jsou v názvech Shakespearových her",
            "jsou v názvech her Járy Cimrmana",
        ],
    },
    {
        "id": "v11-apostolove",
        "roof": "jména apoštolů",
        "level": "hard",
        "hidden": True,
        "inside": [
            "Petr", "Pavel", "Jakub", "Ondřej", "Tomáš", "Filip", "Matouš",
            "Šimon",
        ],
        "outside": [
            "bunda", "hodinky", "koš", "lampa", "lednička", "lopatka",
            "motyka", "pravítko", "pračka", "ramínko", "sešit", "trakař",
            "ubrousek", "vana", "žehlička",
        ],
        "asks": [
            "jsou to zároveň jména apoštolů",
            "jsou to zároveň jména českých měst",
            "jsou to znamení zvěrokruhu",
            "nemají v sobě ani jednu samohlásku",
        ],
    },
    {
        "id": "v11-jablka",
        "roof": "odrůdy jablek",
        "level": "hard",
        "hidden": True,
        "inside": [
            "Jonatán", "Šampion", "Panenské", "Croncelské", "Průsvitné",
            "Boskoopské", "Rubín", "Bohemia",
        ],
        "outside": [
            "brýle", "kbelík", "květináč", "lampa", "lednička", "matice",
            "mrkev", "ořezávátko", "plot", "silnice", "sporák", "struhadlo",
            "stůl", "ubrousek", "šroub",
        ],
        "asks": [
            "jsou to zároveň odrůdy jablek",
            "jsou to zároveň značky českého piva",
            "jsou to znamení zvěrokruhu",
            "jsou to zároveň jména českých měst",
        ],
    },
    {
        "id": "v11-uzly",
        "roof": "názvy uzlů",
        "level": "hard",
        "hidden": True,
        "inside": [
            "osmička", "dračí", "ambulanční", "lodní", "škrtič", "rybářský",
            "zkracovačka", "plochá",
        ],
        "outside": [
            "kastrol", "kolík", "květináč", "lampa", "lednička", "mrkev",
            "mísa", "pilník", "plot", "polštář", "pytel", "ramínko", "sporák",
            "zápisník", "šroub",
        ],
        "asks": [
            "jsou to zároveň názvy uzlů",
            "mají v sobě dvě stejná písmena vedle sebe",
            "jsou v názvech Shakespearových her",
            "jsou to zároveň značky českého piva",
        ],
    },
    {
        "id": "v11-severni-bohove",
        "roof": "jména severských bohů",
        "level": "hard",
        "hidden": True,
        "inside": [
            "Ódin", "Thór", "Loki", "Freya", "Baldr", "Heimdall", "Frigg",
            "Týr",
        ],
        "outside": [
            "deka", "hoblík", "hrábě", "metr", "mísa", "parapet", "pekáč",
            "peřina", "polštář", "svěrák", "tácek", "ubrousek", "vana",
            "vysavač", "zápisník",
        ],
        "asks": [
            "jsou to zároveň jména severských bohů",
            "nemají v sobě ani jednu samohlásku",
            "mají v sobě schované zvíře",
            "čtou se stejně zepředu i zezadu",
        ],
    },
    {
        "id": "v11-brambory",
        "roof": "odrůdy brambor",
        "level": "hard",
        "hidden": True,
        "inside": [
            "Adéla", "Dita", "Karin", "Marabel", "Agria", "Cimrman", "Bella",
            "Impala",
        ],
        "outside": [
            "bunda", "chleba", "houpačka", "hrnec", "kartáček", "kompost",
            "matrace", "myčka", "peněženka", "polštář", "ponožka", "ramínko",
            "vrtačka", "vysavač", "řetízek",
        ],
        "asks": [
            "jsou to zároveň odrůdy brambor",
            "jsou to zároveň značky nebo modely aut",
            "nemají v sobě ani jednu samohlásku",
            "jsou to zároveň značky českého piva",
        ],
    },
    {
        "id": "v11-planety-mesice",
        "roof": "měsíce planet sluneční soustavy",
        "level": "hard",
        "hidden": True,
        "inside": [
            "Titan", "Europa", "Ganymed", "Callisto", "Io", "Triton",
            "Phobos", "Deimos",
        ],
        "outside": [
            "kolík", "koště", "květináč", "lavička", "lednička", "mrkev",
            "mísa", "peněženka", "pouzdro", "pravítko", "pytel", "semínko",
            "záclona", "žebřík", "žehlička",
        ],
        "asks": [
            "jsou to zároveň měsíce planet",
            "jsou v názvech večerníčků",
            "nemají v sobě ani jednu samohlásku",
            "jsou v názvech Shakespearových her",
        ],
    },
    {
        "id": "v11-recke-bohyne",
        "roof": "jména řeckých bohyň",
        "level": "hard",
        "hidden": True,
        "inside": [
            "Héra", "Athéna", "Artemis", "Afrodíté", "Démétér", "Hestia",
            "Níké", "Iris",
        ],
        "outside": [
            "brambora", "kýbl", "matrace", "metr", "motyka", "mýdlo", "plot",
            "pravítko", "rohožka", "ručník", "sešit", "sporák", "ubrousek",
            "šála", "žebřík",
        ],
        "asks": [
            "jsou to zároveň jména řeckých bohyň",
            "jsou to zároveň jména českých měst",
            "mají v sobě dvě stejná písmena vedle sebe",
            "jsou v názvech Shakespearových her",
        ],
    },
    {
        "id": "v11-kameny",
        "roof": "drahé a polodrahé kameny",
        "level": "normal",
        "hidden": True,
        "inside": [
            "granát", "opál", "safír", "smaragd", "ametyst", "topaz",
            "jaspis", "achát",
        ],
        "outside": [
            "branka", "guma", "hadr", "hrneček", "hrábě", "kladívko", "konev",
            "lednička", "myčka", "peněženka", "pouzdro", "pravítko",
            "struhadlo", "vana", "zahrada",
        ],
        "asks": [
            "jsou to zároveň drahé kameny",
            "mají v sobě dvě stejná písmena vedle sebe",
            "jsou v názvech Shakespearových her",
            "jsou v názvech večerníčků",
        ],
    },
    {
        "id": "v11-bylinky",
        "roof": "kuchyňské bylinky",
        "level": "normal",
        "hidden": True,
        "inside": [
            "bazalka", "tymián", "rozmarýn", "saturejka", "libeček",
            "dobromysl", "estragon", "šalvěj",
        ],
        "outside": [
            "brýle", "hrábě", "hřeben", "komoda", "lavička", "metr",
            "náramek", "nůžky", "peněženka", "pouzdro", "struhadlo", "sušák",
            "utěrka", "vařečka", "šála",
        ],
        "asks": [
            "jsou to zároveň kuchyňské bylinky",
            "jsou to zároveň příjmení českých prezidentů",
            "jsou to zároveň značky českého piva",
            "nemají v sobě ani jednu samohlásku",
        ],
    },
]
