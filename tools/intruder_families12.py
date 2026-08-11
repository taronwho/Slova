"""Dvanáctá várka rodin — sto skrytých střech.

TENHLE SOUBOR PÍŠE SKRIPT. Ruční úpravy zmizí při dalším spuštění; opravovat
se má `tools/gen_families12.py`, kde stojí zadání i kontroly.
"""

FAMILIES12 = [
    {
        "id": "v12-kotel",
        "roof": "části kotle",
        "level": "hard",
        "hidden": True,
        "inside": [
            "topeniště", "rošt", "popelník", "výměník", "komínovka", "dvířka",
        ],
        "outside": [
            "brambora", "lavička", "nůžky", "ořezávátko", "pouzdro",
            "semínko", "sklenice", "struhadlo", "sušák", "truhlík", "tácek",
            "utěrka", "vrtačka", "vysavač", "šuplík",
        ],
        "asks": [
            "jsou to zároveň části kotle",
            "jsou v názvech Shakespearových her",
            "jsou to zároveň příjmení českých prezidentů",
            "nemají v sobě ani jednu samohlásku",
        ],
    },
    {
        "id": "v12-skrin",
        "roof": "části skříně",
        "level": "normal",
        "hidden": True,
        "inside": [
            "police", "dvířka", "záda", "sokl", "závěs", "šuplík",
        ],
        "outside": [
            "brambora", "branka", "kastrol", "kbelík", "květináč", "matice",
            "mrkev", "nůžky", "pinzeta", "sporák", "trakař", "tácek", "vana",
            "zápisník", "řetízek",
        ],
        "asks": [
            "jsou to zároveň části skříně",
            "jsou v názvech Shakespearových her",
            "jsou to zároveň značky nebo modely aut",
            "jsou to znamení zvěrokruhu",
        ],
    },
    {
        "id": "v12-komin",
        "roof": "části komína",
        "level": "hard",
        "hidden": True,
        "inside": [
            "sopouch", "průduch", "hlava", "vymetání", "vložka", "krakorec",
        ],
        "outside": [
            "deštník", "kompost", "lavička", "naběračka", "nůžky", "parapet",
            "pinzeta", "plot", "pravítko", "prostěradlo", "ručník", "silnice",
            "sporák", "trouba", "vysavač",
        ],
        "asks": [
            "jsou to zároveň části komína",
            "jsou v názvech her Járy Cimrmana",
            "jsou to zároveň značky nebo modely aut",
            "jsou to zároveň jména českých měst",
        ],
    },
    {
        "id": "v12-studna",
        "roof": "části studny",
        "level": "hard",
        "hidden": True,
        "inside": [
            "roubení", "rumpál", "okov", "skruž", "zákryt", "vydatnost",
        ],
        "outside": [
            "branka", "bunda", "hrábě", "hřebík", "kolík", "krém", "květináč",
            "lavička", "plot", "police", "polštář", "sklenice", "trakař",
            "zápisník", "šuplík",
        ],
        "asks": [
            "jsou to zároveň části studny",
            "nemají v sobě ani jednu samohlásku",
            "jsou v názvech Shakespearových her",
            "jsou to zároveň značky nebo modely aut",
        ],
    },
    {
        "id": "v12-reka",
        "roof": "části řeky",
        "level": "normal",
        "hidden": True,
        "inside": [
            "koryto", "břeh", "meandr", "tůň", "ústí", "pramen", "jez",
        ],
        "outside": [
            "kabát", "kartáček", "kbelík", "kleště", "kompost", "koš",
            "lampa", "lednička", "motyka", "mrkev", "pravítko", "prostěradlo",
            "skříň", "smeták", "sporák",
        ],
        "asks": [
            "jsou to zároveň části řeky",
            "mají v sobě schované zvíře",
            "mají v sobě dvě stejná písmena vedle sebe",
            "jsou to zároveň jména českých měst",
        ],
    },
    {
        "id": "v12-rybnik",
        "roof": "části rybníka",
        "level": "hard",
        "hidden": True,
        "inside": [
            "hráz", "výpusť", "stoka", "kádiště", "přeliv", "loviště",
        ],
        "outside": [
            "hoblík", "houpačka", "kastrol", "kbelík", "kolík", "květináč",
            "naběračka", "nůžky", "ponožka", "postel", "pračka", "smeták",
            "trakař", "vrtačka", "žebřík",
        ],
        "asks": [
            "jsou to zároveň části rybníka",
            "mají v sobě dvě stejná písmena vedle sebe",
            "čtou se stejně zepředu i zezadu",
            "jsou v názvech her Járy Cimrmana",
        ],
    },
    {
        "id": "v12-mesto",
        "roof": "části města",
        "level": "normal",
        "hidden": True,
        "inside": [
            "náměstí", "čtvrť", "předměstí", "centrum", "periferie",
            "nábřeží",
        ],
        "outside": [
            "brambora", "brýle", "hodinky", "hrábě", "hřebík", "koberec",
            "krém", "mýdlo", "parapet", "podnos", "skříň", "struhadlo", "sud",
            "trakař", "truhlík",
        ],
        "asks": [
            "jsou to zároveň části města",
            "mají v sobě dvě stejná písmena vedle sebe",
            "jsou to zároveň značky nebo modely aut",
            "jsou v názvech Shakespearových her",
        ],
    },
    {
        "id": "v12-divadlo-casti",
        "roof": "části divadla",
        "level": "normal",
        "hidden": True,
        "inside": [
            "jeviště", "hlediště", "balkon", "opona", "zákulisí", "propadlo",
        ],
        "outside": [
            "hadice", "kleště", "lampa", "mrkev", "parapet", "pytel", "skříň",
            "struhadlo", "sud", "trouba", "ubrousek", "vana", "věšák",
            "zápisník", "řetízek",
        ],
        "asks": [
            "jsou to zároveň části divadla",
            "nemají v sobě ani jednu samohlásku",
            "jsou to zároveň příjmení českých prezidentů",
            "jsou v názvech Shakespearových her",
        ],
    },
    {
        "id": "v12-klavir",
        "roof": "části klavíru",
        "level": "normal",
        "hidden": True,
        "inside": [
            "kladívko", "struna", "pedál", "klapka", "tlumítko", "víko",
        ],
        "outside": [
            "batoh", "hrnec", "matrace", "motyka", "mrkev", "mísa", "podnos",
            "police", "pravítko", "silnice", "sklenice", "sud", "trakař",
            "zápisník", "řetízek",
        ],
        "asks": [
            "jsou to zároveň části klavíru",
            "mají v sobě dvě stejná písmena vedle sebe",
            "nemají v sobě ani jednu samohlásku",
            "jsou to zároveň značky českého piva",
        ],
    },
    {
        "id": "v12-trubka",
        "roof": "části trubky",
        "level": "hard",
        "hidden": True,
        "inside": [
            "nátrubek", "ventil", "korpus", "strojivo", "ladička",
            "korouhvička",
        ],
        "outside": [
            "deštník", "hřebík", "kleště", "koberec", "konev", "lednička",
            "lopata", "mrkev", "naběračka", "pilník", "plot", "silnice",
            "vana", "šroub", "šála",
        ],
        "asks": [
            "jsou to zároveň části trubky",
            "jsou to zároveň značky nebo modely aut",
            "čtou se stejně zepředu i zezadu",
            "jsou v názvech Shakespearových her",
        ],
    },
    {
        "id": "v12-bryle",
        "roof": "části brýlí",
        "level": "normal",
        "hidden": True,
        "inside": [
            "obruba", "sklo", "nožička", "most", "sedlo", "stranice",
        ],
        "outside": [
            "deštník", "guma", "hadr", "hodinky", "hrábě", "hřebík",
            "kompost", "lednička", "motyka", "mýdlo", "popelnice", "zahrada",
            "záclona", "zápisník", "šroub",
        ],
        "asks": [
            "jsou to zároveň části brýlí",
            "mají v sobě dvě stejná písmena vedle sebe",
            "jsou to zároveň jména českých měst",
            "jsou to zároveň značky nebo modely aut",
        ],
    },
    {
        "id": "v12-motor",
        "roof": "části motoru",
        "level": "hard",
        "hidden": True,
        "inside": [
            "blok", "hlava", "ojnice", "válec", "kliková", "vačka",
        ],
        "outside": [
            "branka", "deka", "deštník", "kabát", "kolík", "koště", "lavička",
            "mýdlo", "peněženka", "pilník", "pinzeta", "police", "pračka",
            "prostěradlo", "sud",
        ],
        "asks": [
            "jsou to zároveň části motoru",
            "jsou to zároveň jména českých měst",
            "jsou v názvech večerníčků",
            "mají v sobě dvě stejná písmena vedle sebe",
        ],
    },
    {
        "id": "v12-raketa",
        "roof": "části rakety",
        "level": "hard",
        "hidden": True,
        "inside": [
            "stupeň", "tryska", "kryt", "nosič", "palivo", "špička",
        ],
        "outside": [
            "hadice", "komoda", "krém", "lavička", "matrace", "motyka",
            "mísa", "pilník", "sporák", "stůl", "sušák", "svěrák", "trouba",
            "vysavač", "zápisník",
        ],
        "asks": [
            "jsou to zároveň části rakety",
            "čtou se stejně zepředu i zezadu",
            "nemají v sobě ani jednu samohlásku",
            "jsou v názvech večerníčků",
        ],
    },
    {
        "id": "v12-lyze-casti",
        "roof": "části lyže",
        "level": "normal",
        "hidden": True,
        "inside": [
            "skluznice", "hrana", "vázání", "špička", "patka", "stoupání",
        ],
        "outside": [
            "batoh", "branka", "brýle", "kompost", "květináč", "lopatka",
            "matrace", "náramek", "police", "propiska", "rýč", "schránka",
            "tácek", "řetízek", "žehlička",
        ],
        "asks": [
            "jsou to zároveň části lyže",
            "mají v sobě dvě stejná písmena vedle sebe",
            "mají v sobě schované zvíře",
            "nemají v sobě ani jednu samohlásku",
        ],
    },
    {
        "id": "v12-klobouk",
        "roof": "části klobouku",
        "level": "normal",
        "hidden": True,
        "inside": [
            "dýnko", "krempa", "stuha", "potítko", "podšívka", "střecha",
        ],
        "outside": [
            "deka", "krém", "květináč", "mrkev", "ořezávátko", "police",
            "postel", "rohožka", "ručník", "trakař", "truhlík", "vysavač",
            "řetízek", "šroub", "šuplík",
        ],
        "asks": [
            "jsou to zároveň části klobouku",
            "jsou v názvech večerníčků",
            "čtou se stejně zepředu i zezadu",
            "jsou v názvech Shakespearových her",
        ],
    },
    {
        "id": "v12-kominictvi",
        "roof": "kominické pojmy",
        "level": "hard",
        "hidden": True,
        "inside": [
            "saze", "vymetání", "sopouch", "koudel", "revize", "tah",
        ],
        "outside": [
            "deka", "dřez", "guma", "hoblík", "hrneček", "hřeben", "kabát",
            "kartáček", "lavička", "police", "postel", "trakař", "ubrus",
            "vrtačka", "zahrada",
        ],
        "asks": [
            "jsou to zároveň kominické pojmy",
            "jsou to zároveň značky českého piva",
            "jsou v názvech her Járy Cimrmana",
            "jsou to zároveň jména českých měst",
        ],
    },
    {
        "id": "v12-kozeluzna",
        "roof": "koželužské pojmy",
        "level": "hard",
        "hidden": True,
        "inside": [
            "useň", "tříslo", "lužení", "mízdření", "vyčinění", "líc",
        ],
        "outside": [
            "hodinky", "houpačka", "lavička", "lepidlo", "matice", "motyka",
            "popelnice", "pouzdro", "pračka", "sklenice", "skříň", "sporák",
            "vana", "záclona", "šuplík",
        ],
        "asks": [
            "jsou to zároveň koželužské pojmy",
            "čtou se stejně zepředu i zezadu",
            "jsou v názvech večerníčků",
            "mají v sobě schované zvíře",
        ],
    },
    {
        "id": "v12-tesarina",
        "roof": "tesařské pojmy",
        "level": "hard",
        "hidden": True,
        "inside": [
            "krokev", "vazba", "pozednice", "sloup", "rozpěra", "plátování",
        ],
        "outside": [
            "brýle", "hřeben", "hřebík", "motyka", "naběračka", "nůžky",
            "pilník", "podnos", "pračka", "propiska", "provaz", "semínko",
            "skříň", "svěrák", "trouba",
        ],
        "asks": [
            "jsou to zároveň tesařské pojmy",
            "čtou se stejně zepředu i zezadu",
            "mají v sobě dvě stejná písmena vedle sebe",
            "jsou v názvech večerníčků",
        ],
    },
    {
        "id": "v12-kamenictvi",
        "roof": "kamenické pojmy",
        "level": "hard",
        "hidden": True,
        "inside": [
            "špic", "dláto", "lom", "blok", "leštění", "osazení",
        ],
        "outside": [
            "chleba", "hřebík", "konev", "koš", "květináč", "kýbl", "metr",
            "mrkev", "mýdlo", "provaz", "svěrák", "trakař", "zahrada",
            "šroub", "žebřík",
        ],
        "asks": [
            "jsou to zároveň kamenické pojmy",
            "jsou to znamení zvěrokruhu",
            "mají v sobě dvě stejná písmena vedle sebe",
            "jsou to zároveň příjmení českých prezidentů",
        ],
    },
    {
        "id": "v12-socharstvi",
        "roof": "sochařské pojmy",
        "level": "normal",
        "hidden": True,
        "inside": [
            "model", "odlitek", "patina", "sokl", "busta", "reliéf",
        ],
        "outside": [
            "hodinky", "kabát", "kastrol", "kleště", "naběračka",
            "ořezávátko", "podnos", "propiska", "provaz", "sešit", "sklenice",
            "sušák", "truhlík", "řetízek", "žebřík",
        ],
        "asks": [
            "jsou to zároveň sochařské pojmy",
            "jsou v názvech her Járy Cimrmana",
            "jsou to zároveň jména českých měst",
            "jsou to zároveň značky českého piva",
        ],
    },
    {
        "id": "v12-grafika",
        "roof": "grafické pojmy",
        "level": "hard",
        "hidden": True,
        "inside": [
            "lept", "rytina", "matrice", "otisk", "tah", "náklad",
        ],
        "outside": [
            "batoh", "chleba", "deka", "hrnec", "hřeben", "lampa", "lopata",
            "lopatka", "motyka", "naběračka", "ořezávátko", "semínko", "stůl",
            "vana", "zápisník",
        ],
        "asks": [
            "jsou to zároveň grafické pojmy",
            "nemají v sobě ani jednu samohlásku",
            "jsou v názvech her Járy Cimrmana",
            "jsou to znamení zvěrokruhu",
        ],
    },
    {
        "id": "v12-calounictvi",
        "roof": "čalounické pojmy",
        "level": "hard",
        "hidden": True,
        "inside": [
            "popruh", "molitan", "potah", "nopa", "knoflíkování", "prošívání",
        ],
        "outside": [
            "brambora", "deštník", "hadice", "matice", "nůžky", "plot",
            "pouzdro", "pytel", "ručník", "sešit", "sklenice", "skříň",
            "struhadlo", "stůl", "trouba",
        ],
        "asks": [
            "jsou to zároveň čalounické pojmy",
            "jsou v názvech Shakespearových her",
            "jsou to zároveň značky českého piva",
            "jsou to zároveň příjmení českých prezidentů",
        ],
    },
    {
        "id": "v12-sklenarstvi",
        "roof": "sklenářské pojmy",
        "level": "normal",
        "hidden": True,
        "inside": [
            "tabule", "řezák", "tmel", "lišta", "zasklení", "kalení",
        ],
        "outside": [
            "brýle", "hadice", "hrneček", "kabát", "kolík", "motyka",
            "pilník", "podnos", "police", "ponožka", "pravítko", "schránka",
            "semínko", "skříň", "žehlička",
        ],
        "asks": [
            "jsou to zároveň sklenářské pojmy",
            "jsou to zároveň jména českých měst",
            "jsou to zároveň značky nebo modely aut",
            "jsou v názvech večerníčků",
        ],
    },
    {
        "id": "v12-topenarstvi",
        "roof": "topenářské pojmy",
        "level": "normal",
        "hidden": True,
        "inside": [
            "stoupačka", "odvzdušnění", "oběh", "rozdělovač", "termostatická",
            "expanzní",
        ],
        "outside": [
            "guma", "houpačka", "hřeben", "hřebík", "kladívko", "koberec",
            "mýdlo", "postel", "pravítko", "propiska", "stůl", "trouba",
            "ubrousek", "vrtačka", "šála",
        ],
        "asks": [
            "jsou to zároveň topenářské pojmy",
            "jsou to znamení zvěrokruhu",
            "jsou v názvech večerníčků",
            "jsou to zároveň příjmení českých prezidentů",
        ],
    },
    {
        "id": "v12-sladovna",
        "roof": "sladovnické pojmy",
        "level": "hard",
        "hidden": True,
        "inside": [
            "máčení", "klíčení", "hvozd", "zelený", "slad", "rmut",
        ],
        "outside": [
            "hodinky", "houpačka", "kleště", "motyka", "mrkev", "mísa",
            "peřina", "pinzeta", "plot", "propiska", "rýč", "svěrák",
            "trakař", "šroub", "šála",
        ],
        "asks": [
            "jsou to zároveň sladovnické pojmy",
            "nemají v sobě ani jednu samohlásku",
            "mají v sobě dvě stejná písmena vedle sebe",
            "jsou to zároveň značky nebo modely aut",
        ],
    },
    {
        "id": "v12-rybnikarstvi",
        "roof": "rybníkářské pojmy",
        "level": "hard",
        "hidden": True,
        "inside": [
            "výlov", "kádě", "plůdek", "obsádka", "zátah", "komory",
        ],
        "outside": [
            "batoh", "chleba", "deštník", "hrnec", "komoda", "matice", "mísa",
            "nůžky", "parapet", "pravítko", "prostěradlo", "provaz", "sud",
            "sušák", "záclona",
        ],
        "asks": [
            "jsou to zároveň rybníkářské pojmy",
            "jsou to zároveň značky českého piva",
            "jsou v názvech večerníčků",
            "jsou to zároveň značky nebo modely aut",
        ],
    },
    {
        "id": "v12-ovocnarstvi",
        "roof": "ovocnářské pojmy",
        "level": "normal",
        "hidden": True,
        "inside": [
            "podnož", "roub", "štěpování", "prořezávka", "koruna", "výhon",
        ],
        "outside": [
            "deka", "guma", "hřebík", "lednička", "lepidlo", "matice", "mísa",
            "mýdlo", "náramek", "peřina", "ramínko", "rýč", "sešit", "věšák",
            "šuplík",
        ],
        "asks": [
            "jsou to zároveň ovocnářské pojmy",
            "nemají v sobě ani jednu samohlásku",
            "jsou to zároveň značky nebo modely aut",
            "jsou v názvech večerníčků",
        ],
    },
    {
        "id": "v12-chmelarstvi",
        "roof": "chmelařské pojmy",
        "level": "hard",
        "hidden": True,
        "inside": [
            "česání", "konstrukce", "hlávka", "révy", "sušárna", "zavádění",
        ],
        "outside": [
            "koš", "kýbl", "lopatka", "pilník", "podnos", "police", "pračka",
            "propiska", "provaz", "rohožka", "ručník", "stůl", "sušák",
            "ubrousek", "utěrka",
        ],
        "asks": [
            "jsou to zároveň chmelařské pojmy",
            "jsou v názvech Shakespearových her",
            "jsou v názvech her Járy Cimrmana",
            "jsou to znamení zvěrokruhu",
        ],
    },
    {
        "id": "v12-ornitologie",
        "roof": "ornitologické pojmy",
        "level": "hard",
        "hidden": True,
        "inside": [
            "kroužkování", "snůška", "mláďata", "tah", "hnízdiště", "volavý",
        ],
        "outside": [
            "branka", "brýle", "dřez", "guma", "hodinky", "hrábě", "koště",
            "peřina", "pilník", "podnos", "semínko", "sud", "ubrousek",
            "řetízek", "šuplík",
        ],
        "asks": [
            "jsou to zároveň ornitologické pojmy",
            "jsou to zároveň jména českých měst",
            "jsou v názvech her Járy Cimrmana",
            "jsou to znamení zvěrokruhu",
        ],
    },
    {
        "id": "v12-entomologie",
        "roof": "entomologické pojmy",
        "level": "hard",
        "hidden": True,
        "inside": [
            "kukla", "larva", "krovky", "sosák", "tykadlo", "svlékání",
        ],
        "outside": [
            "hřebík", "kartáček", "kastrol", "kolík", "kompost", "lepidlo",
            "pinzeta", "ponožka", "pouzdro", "rýč", "sešit", "trakař",
            "truhlík", "vrtačka", "šuplík",
        ],
        "asks": [
            "jsou to zároveň entomologické pojmy",
            "čtou se stejně zepředu i zezadu",
            "jsou to zároveň jména českých měst",
            "jsou to zároveň značky nebo modely aut",
        ],
    },
    {
        "id": "v12-botanika",
        "roof": "botanické pojmy",
        "level": "normal",
        "hidden": True,
        "inside": [
            "palist", "oddenek", "cibule", "úžlabí", "letorost", "přeslen",
        ],
        "outside": [
            "bunda", "deka", "hřebík", "komoda", "koš", "koště", "krém",
            "peřina", "plot", "pravítko", "ramínko", "ručník", "sešit",
            "šroub", "šála",
        ],
        "asks": [
            "jsou to zároveň botanické pojmy",
            "jsou to znamení zvěrokruhu",
            "jsou to zároveň značky nebo modely aut",
            "čtou se stejně zepředu i zezadu",
        ],
    },
    {
        "id": "v12-mineralogie",
        "roof": "mineralogické pojmy",
        "level": "hard",
        "hidden": True,
        "inside": [
            "štěpnost", "tvrdost", "krystal", "vryp", "lesk", "dvojče",
        ],
        "outside": [
            "deka", "hrábě", "kladívko", "kolík", "koště", "krém", "lepidlo",
            "myčka", "peřina", "pytel", "schránka", "semínko", "stůl",
            "ubrus", "utěrka",
        ],
        "asks": [
            "jsou to zároveň mineralogické pojmy",
            "jsou v názvech večerníčků",
            "mají v sobě schované zvíře",
            "jsou to zároveň značky českého piva",
        ],
    },
    {
        "id": "v12-paleontologie",
        "roof": "paleontologické pojmy",
        "level": "hard",
        "hidden": True,
        "inside": [
            "otisk", "zkamenělina", "vrstva", "naleziště", "obratel",
            "druhohory",
        ],
        "outside": [
            "batoh", "kbelík", "kladívko", "krém", "lavička", "lopata",
            "matrace", "myčka", "mísa", "mýdlo", "postel", "pravítko",
            "rohožka", "ručník", "ubrus",
        ],
        "asks": [
            "jsou to zároveň paleontologické pojmy",
            "jsou to zároveň značky českého piva",
            "jsou to zároveň značky nebo modely aut",
            "čtou se stejně zepředu i zezadu",
        ],
    },
    {
        "id": "v12-hydrologie",
        "roof": "hydrologické pojmy",
        "level": "hard",
        "hidden": True,
        "inside": [
            "průtok", "povodí", "odtok", "vodočet", "spád", "retence",
        ],
        "outside": [
            "hoblík", "hrnec", "hrábě", "kartáček", "kladívko", "konev",
            "koš", "koště", "mísa", "plot", "popelnice", "pytel", "rýč",
            "svěrák", "věšák",
        ],
        "asks": [
            "jsou to zároveň hydrologické pojmy",
            "čtou se stejně zepředu i zezadu",
            "mají v sobě schované zvíře",
            "jsou to zároveň jména českých měst",
        ],
    },
    {
        "id": "v12-kosmonautika",
        "roof": "kosmonautické pojmy",
        "level": "normal",
        "hidden": True,
        "inside": [
            "oběžná", "modul", "spojení", "přetížení", "návratový",
            "skafandr",
        ],
        "outside": [
            "bunda", "deka", "dřez", "kabát", "nůžky", "polštář", "pouzdro",
            "propiska", "smeták", "svěrák", "trakař", "trouba", "truhlík",
            "vařečka", "zápisník",
        ],
        "asks": [
            "jsou to zároveň kosmonautické pojmy",
            "mají v sobě dvě stejná písmena vedle sebe",
            "čtou se stejně zepředu i zezadu",
            "nemají v sobě ani jednu samohlásku",
        ],
    },
    {
        "id": "v12-telekomunikace",
        "roof": "telekomunikační pojmy",
        "level": "hard",
        "hidden": True,
        "inside": [
            "linka", "ústředna", "přenos", "pásmo", "rušení", "vysílač",
        ],
        "outside": [
            "batoh", "dřez", "hadice", "květináč", "lopata", "motyka",
            "pinzeta", "ponožka", "postel", "prostěradlo", "provaz", "sušák",
            "vařečka", "záclona", "žebřík",
        ],
        "asks": [
            "jsou to zároveň telekomunikační pojmy",
            "mají v sobě dvě stejná písmena vedle sebe",
            "nemají v sobě ani jednu samohlásku",
            "jsou v názvech večerníčků",
        ],
    },
    {
        "id": "v12-energetika",
        "roof": "energetické pojmy",
        "level": "hard",
        "hidden": True,
        "inside": [
            "špička", "výkon", "soustava", "odběr", "blok", "záloha",
        ],
        "outside": [
            "branka", "hrnec", "kolík", "květináč", "plot", "pračka",
            "prostěradlo", "pytel", "rohožka", "schránka", "silnice", "skříň",
            "sud", "ubrus", "šála",
        ],
        "asks": [
            "jsou to zároveň energetické pojmy",
            "jsou to zároveň příjmení českých prezidentů",
            "mají v sobě dvě stejná písmena vedle sebe",
            "jsou to zároveň jména českých měst",
        ],
    },
    {
        "id": "v12-numismatika",
        "roof": "numismatické pojmy",
        "level": "hard",
        "hidden": True,
        "inside": [
            "ražba", "hrana", "opis", "nominál", "patina", "sbírka",
        ],
        "outside": [
            "brambora", "branka", "brýle", "deštník", "hoblík", "matice",
            "matrace", "naběračka", "ořezávátko", "provaz", "ramínko", "rýč",
            "vrtačka", "záclona", "žehlička",
        ],
        "asks": [
            "jsou to zároveň numismatické pojmy",
            "nemají v sobě ani jednu samohlásku",
            "mají v sobě dvě stejná písmena vedle sebe",
            "mají v sobě schované zvíře",
        ],
    },
    {
        "id": "v12-kriminalistika",
        "roof": "kriminalistické pojmy",
        "level": "hard",
        "hidden": True,
        "inside": [
            "stopa", "daktyloskopie", "rekonstrukce", "ohledání", "profil",
            "sběr",
        ],
        "outside": [
            "branka", "brýle", "hrnec", "kladívko", "kolík", "police",
            "polštář", "popelnice", "postel", "tácek", "ubrus", "utěrka",
            "věšák", "záclona", "žebřík",
        ],
        "asks": [
            "jsou to zároveň kriminalistické pojmy",
            "jsou v názvech Shakespearových her",
            "jsou to zároveň příjmení českých prezidentů",
            "nemají v sobě ani jednu samohlásku",
        ],
    },
    {
        "id": "v12-psychologie",
        "roof": "psychologické pojmy",
        "level": "normal",
        "hidden": True,
        "inside": [
            "vjem", "paměť", "podnět", "postoj", "vývoj", "temperament",
        ],
        "outside": [
            "branka", "dřez", "hadr", "kastrol", "kolík", "květináč", "kýbl",
            "myčka", "nůžky", "parapet", "plot", "popelnice", "rýč", "stůl",
            "ubrus",
        ],
        "asks": [
            "jsou to zároveň psychologické pojmy",
            "jsou to zároveň značky českého piva",
            "jsou to zároveň značky nebo modely aut",
            "jsou to zároveň příjmení českých prezidentů",
        ],
    },
    {
        "id": "v12-horky",
        "roof": "slova, která tvoří spojení se slovem hořký",
        "level": "normal",
        "hidden": True,
        "inside": [
            "pilulka", "čokoláda", "konec", "pravda", "mandle", "úsměv",
        ],
        "outside": [
            "sešit", "koště", "ubrus", "rohožka", "propiska", "záclona",
            "houpačka", "tácek", "ramínko", "ubrousek",
        ],
        "asks": [
            "tvoří se slovem hořký ustálené spojení",
            "jsou to zároveň jména českých měst",
            "jsou v názvech večerníčků",
            "nemají v sobě ani jednu samohlásku",
        ],
    },
    {
        "id": "v12-cerstvy",
        "roof": "slova, která tvoří spojení se slovem čerstvý",
        "level": "normal",
        "hidden": True,
        "inside": [
            "vzduch", "vítr", "novomanžel", "zpráva", "stopa", "síla",
        ],
        "outside": [
            "sešit", "koště", "ubrus", "rohožka", "propiska", "záclona",
            "houpačka", "tácek", "ramínko", "ubrousek",
        ],
        "asks": [
            "tvoří se slovem čerstvý ustálené spojení",
            "čtou se stejně zepředu i zezadu",
            "jsou to zároveň jména českých měst",
            "jsou to zároveň značky nebo modely aut",
        ],
    },
    {
        "id": "v12-plny",
        "roof": "slova, která tvoří spojení se slovem plný",
        "level": "normal",
        "hidden": True,
        "inside": [
            "úvazek", "moc", "měsíc", "žaludek", "plyn", "hrst",
        ],
        "outside": [
            "sešit", "koště", "ubrus", "rohožka", "propiska", "záclona",
            "houpačka", "tácek", "ramínko", "ubrousek",
        ],
        "asks": [
            "tvoří se slovem plný ustálené spojení",
            "jsou to zároveň příjmení českých prezidentů",
            "mají v sobě dvě stejná písmena vedle sebe",
            "jsou to zároveň značky českého piva",
        ],
    },
    {
        "id": "v12-holy",
        "roof": "slova, která tvoří spojení se slovem holý",
        "level": "normal",
        "hidden": True,
        "inside": [
            "věta", "nesmysl", "fakt", "zeď", "rukou", "hlava",
        ],
        "outside": [
            "sešit", "koště", "ubrus", "rohožka", "propiska", "záclona",
            "houpačka", "tácek", "ramínko", "ubrousek",
        ],
        "asks": [
            "tvoří se slovem holý ustálené spojení",
            "mají v sobě dvě stejná písmena vedle sebe",
            "jsou to zároveň značky nebo modely aut",
            "čtou se stejně zepředu i zezadu",
        ],
    },
    {
        "id": "v12-plany",
        "roof": "slova, která tvoří spojení se slovem planý",
        "level": "hard",
        "hidden": True,
        "inside": [
            "poplach", "řeči", "naděje", "výhonek", "hlásič", "růže",
        ],
        "outside": [
            "sešit", "koště", "ubrus", "rohožka", "propiska", "záclona",
            "houpačka", "tácek", "ramínko", "ubrousek",
        ],
        "asks": [
            "tvoří se slovem planý ustálené spojení",
            "nemají v sobě ani jednu samohlásku",
            "jsou to zároveň jména českých měst",
            "čtou se stejně zepředu i zezadu",
        ],
    },
    {
        "id": "v12-hluchy",
        "roof": "slova, která tvoří spojení se slovem hluchý",
        "level": "hard",
        "hidden": True,
        "inside": [
            "místo", "doba", "kout", "ucho", "okno", "kopřiva",
        ],
        "outside": [
            "sešit", "koště", "ubrus", "rohožka", "propiska", "záclona",
            "houpačka", "tácek", "ramínko", "ubrousek",
        ],
        "asks": [
            "tvoří se slovem hluchý ustálené spojení",
            "jsou v názvech Shakespearových her",
            "jsou to zároveň jména českých měst",
            "mají v sobě schované zvíře",
        ],
    },
    {
        "id": "v12-krivy",
        "roof": "slova, která tvoří spojení se slovem křivý",
        "level": "hard",
        "hidden": True,
        "inside": [
            "přísaha", "obvinění", "pohled", "zrcadlo", "úsměv", "záda",
        ],
        "outside": [
            "sešit", "koště", "ubrus", "rohožka", "propiska", "záclona",
            "houpačka", "tácek", "ramínko", "ubrousek",
        ],
        "asks": [
            "tvoří se slovem křivý ustálené spojení",
            "čtou se stejně zepředu i zezadu",
            "mají v sobě dvě stejná písmena vedle sebe",
            "jsou to znamení zvěrokruhu",
        ],
    },
    {
        "id": "v12-rovny",
        "roof": "slova, která tvoří spojení se slovem rovný",
        "level": "normal",
        "hidden": True,
        "inside": [
            "záda", "čára", "příležitost", "páteř", "dílec", "trať",
        ],
        "outside": [
            "sešit", "koště", "ubrus", "rohožka", "propiska", "záclona",
            "houpačka", "tácek", "ramínko", "ubrousek",
        ],
        "asks": [
            "tvoří se slovem rovný ustálené spojení",
            "čtou se stejně zepředu i zezadu",
            "jsou to zároveň značky českého piva",
            "jsou to zároveň značky nebo modely aut",
        ],
    },
    {
        "id": "v12-mokry",
        "roof": "slova, která tvoří spojení se slovem mokrý",
        "level": "normal",
        "hidden": True,
        "inside": [
            "hadr", "sníh", "kout", "proces", "vlasy", "oblečení",
        ],
        "outside": [
            "sešit", "koště", "ubrus", "rohožka", "propiska", "záclona",
            "houpačka", "tácek", "ramínko", "ubrousek",
        ],
        "asks": [
            "tvoří se slovem mokrý ustálené spojení",
            "jsou to zároveň značky českého piva",
            "mají v sobě dvě stejná písmena vedle sebe",
            "čtou se stejně zepředu i zezadu",
        ],
    },
    {
        "id": "v12-drahy",
        "roof": "slova, která tvoří spojení se slovem drahý",
        "level": "normal",
        "hidden": True,
        "inside": [
            "kámen", "kov", "přítel", "žert", "špás", "host",
        ],
        "outside": [
            "sešit", "koště", "ubrus", "rohožka", "propiska", "záclona",
            "houpačka", "tácek", "ramínko", "ubrousek",
        ],
        "asks": [
            "tvoří se slovem drahý ustálené spojení",
            "jsou v názvech her Járy Cimrmana",
            "jsou to zároveň jména českých měst",
            "jsou to zároveň značky českého piva",
        ],
    },
    {
        "id": "v12-ypsilon",
        "roof": "slova s ypsilonem",
        "level": "normal",
        "hidden": True,
        "inside": [
            "ryba", "byt", "mýdlo", "sýr", "jazyk", "myš", "zvyk", "výtah",
        ],
        "outside": [
            "kolo", "lampa", "police", "hrnec", "konev", "deka", "kniha",
            "provaz", "cihla", "ubrus",
        ],
        "asks": [
            "mají v sobě y",
            "jsou to zároveň jména českých měst",
            "jsou v názvech večerníčků",
            "jsou v názvech her Járy Cimrmana",
        ],
    },
    {
        "id": "v12-slozene",
        "roof": "slova složená ze dvou samostatných slov",
        "level": "hard",
        "hidden": True,
        "inside": [
            "autobus", "zločin", "zloděj", "hodnota", "program", "televize",
            "centrum", "půlnoc",
        ],
        "outside": [
            "lampa", "police", "hrnec", "deka", "kniha", "cihla", "motyka",
            "konev", "kolík", "koberec",
        ],
        "asks": [
            "se dají rozdělit na dvě samostatná slova",
            "jsou v názvech her Járy Cimrmana",
            "jsou to zároveň značky českého piva",
            "jsou to zároveň příjmení českých prezidentů",
        ],
    },
    {
        "id": "v12-dve-samohlasky",
        "roof": "slova se dvěma samohláskami vedle sebe",
        "level": "normal",
        "hidden": True,
        "inside": [
            "louka", "auto", "houba", "moucha", "pauza", "koule", "soutěž",
            "doupě",
        ],
        "outside": [
            "lampa", "police", "hrnec", "deka", "kniha", "provaz", "cihla",
            "ubrus", "motyka", "konev",
        ],
        "asks": [
            "mají v sobě dvě samohlásky vedle sebe",
            "jsou to znamení zvěrokruhu",
            "mají v sobě schované zvíře",
            "čtou se stejně zepředu i zezadu",
        ],
    },
    {
        "id": "v12-e-hacek",
        "roof": "slova s písmenem ě",
        "level": "normal",
        "hidden": True,
        "inside": [
            "věž", "pěna", "květ", "město", "těsto", "svět", "závěs", "oběd",
        ],
        "outside": [
            "lampa", "police", "hrnec", "deka", "kniha", "provaz", "cihla",
            "ubrus", "motyka", "kolík",
        ],
        "asks": [
            "mají v sobě písmeno ě",
            "jsou v názvech večerníčků",
            "jsou v názvech her Járy Cimrmana",
            "jsou to zároveň značky nebo modely aut",
        ],
    },
    {
        "id": "v12-nik",
        "roof": "slova končící na -ník",
        "level": "normal",
        "hidden": True,
        "inside": [
            "rybník", "deník", "chodník", "kominík", "zvoník", "rolník",
            "básník", "dělník",
        ],
        "outside": [
            "lampa", "police", "hrnec", "deka", "kniha", "provaz", "cihla",
            "ubrus", "motyka", "konev",
        ],
        "asks": [
            "končí na písmena ník",
            "jsou to zároveň značky českého piva",
            "čtou se stejně zepředu i zezadu",
            "jsou to znamení zvěrokruhu",
        ],
    },
    {
        "id": "v12-dlo",
        "roof": "slova končící na -dlo",
        "level": "normal",
        "hidden": True,
        "inside": [
            "mýdlo", "zrcadlo", "sedadlo", "kadidlo", "bidlo", "chodidlo",
            "křídlo", "prostěradlo",
        ],
        "outside": [
            "lampa", "police", "hrnec", "deka", "kniha", "provaz", "cihla",
            "ubrus", "motyka", "konev",
        ],
        "asks": [
            "končí na písmena dlo",
            "jsou v názvech večerníčků",
            "jsou to zároveň značky nebo modely aut",
            "jsou to zároveň značky českého piva",
        ],
    },
    {
        "id": "v12-pre",
        "roof": "slova začínající na pře-",
        "level": "normal",
        "hidden": True,
        "inside": [
            "přehrada", "přestávka", "převod", "překlad", "přesila",
            "přejezd", "přezka", "přeslička",
        ],
        "outside": [
            "lampa", "police", "hrnec", "deka", "kniha", "provaz", "cihla",
            "ubrus", "motyka", "konev",
        ],
        "asks": [
            "začínají na písmena pře",
            "jsou to zároveň značky českého piva",
            "mají v sobě dvě stejná písmena vedle sebe",
            "jsou to zároveň jména českých měst",
        ],
    },
    {
        "id": "v12-hemingway",
        "roof": "slova z názvů knih Ernesta Hemingwaye",
        "level": "hard",
        "hidden": True,
        "inside": [
            "stařec", "moře", "hrana", "armáda", "zbraně", "slunce", "ráj",
        ],
        "outside": [
            "chleba", "dřez", "hodinky", "konev", "mrkev", "peřina",
            "pravítko", "prostěradlo", "ručník", "schránka", "skříň", "sušák",
            "tácek", "vysavač", "zahrada",
        ],
        "asks": [
            "jsou v názvech knih Ernesta Hemingwaye",
            "nemají v sobě ani jednu samohlásku",
            "jsou v názvech Shakespearových her",
            "jsou to zároveň značky českého piva",
        ],
    },
    {
        "id": "v12-kafka",
        "roof": "slova z názvů díla Franze Kafky",
        "level": "hard",
        "hidden": True,
        "inside": [
            "proces", "zámek", "proměna", "amerika", "ortel", "dopis", "nora",
        ],
        "outside": [
            "batoh", "deštník", "hodinky", "hrnec", "koberec", "lopatka",
            "matice", "myčka", "mýdlo", "nůžky", "peřina", "police", "ručník",
            "vana", "žebřík",
        ],
        "asks": [
            "jsou v názvech díla Franze Kafky",
            "nemají v sobě ani jednu samohlásku",
            "jsou to zároveň příjmení českých prezidentů",
            "mají v sobě schované zvíře",
        ],
    },
    {
        "id": "v12-skvorecky",
        "roof": "slova z názvů knih Josefa Škvoreckého",
        "level": "hard",
        "hidden": True,
        "inside": [
            "zbabělci", "prapor", "sezóna", "mirákl", "lvíče", "příběh",
            "tank",
        ],
        "outside": [
            "dřez", "guma", "kastrol", "kleště", "krém", "kýbl", "lepidlo",
            "mrkev", "pilník", "pračka", "pytel", "ramínko", "schránka",
            "stůl", "vysavač",
        ],
        "asks": [
            "jsou v názvech knih Josefa Škvoreckého",
            "jsou v názvech večerníčků",
            "nemají v sobě ani jednu samohlásku",
            "jsou v názvech Shakespearových her",
        ],
    },
    {
        "id": "v12-kachyna",
        "roof": "slova z názvů filmů Karla Kachyni",
        "level": "hard",
        "hidden": True,
        "inside": [
            "ucho", "kočár", "srnec", "smrt", "republika", "sestřičky",
            "vlak",
        ],
        "outside": [
            "batoh", "branka", "bunda", "deka", "deštník", "dřez", "matice",
            "peřina", "podnos", "pravítko", "rohožka", "struhadlo", "vařečka",
            "vrtačka", "žebřík",
        ],
        "asks": [
            "jsou v názvech filmů Karla Kachyni",
            "jsou v názvech večerníčků",
            "jsou to zároveň příjmení českých prezidentů",
            "jsou v názvech her Járy Cimrmana",
        ],
    },
    {
        "id": "v12-troska",
        "roof": "slova z názvů filmů Zdeňka Trošky",
        "level": "normal",
        "hidden": True,
        "inside": [
            "slunce", "seno", "jahody", "princezna", "mlejn", "peklo",
            "štěstí", "skřítek",
        ],
        "outside": [
            "deka", "hřebík", "kabát", "lepidlo", "lopata", "metr", "pinzeta",
            "pravítko", "provaz", "sklenice", "smeták", "trakař", "truhlík",
            "vana", "věšák",
        ],
        "asks": [
            "jsou v názvech filmů Zdeňka Trošky",
            "mají v sobě dvě stejná písmena vedle sebe",
            "jsou v názvech her Járy Cimrmana",
            "jsou to zároveň značky českého piva",
        ],
    },
    {
        "id": "v12-tucny",
        "roof": "slova z názvů písní Michala Tučného",
        "level": "hard",
        "hidden": True,
        "inside": [
            "báječná", "ženská", "blbec", "sněhu", "kamarád", "rodeo",
            "halelujá", "zlatokop",
        ],
        "outside": [
            "bunda", "deka", "hadice", "houpačka", "lepidlo", "peřina",
            "pilník", "pravítko", "sud", "trakař", "ubrousek", "ubrus",
            "zahrada", "zápisník", "řetízek",
        ],
        "asks": [
            "jsou v názvech písní Michala Tučného",
            "nemají v sobě ani jednu samohlásku",
            "jsou to zároveň značky českého piva",
            "jsou v názvech večerníčků",
        ],
    },
    {
        "id": "v12-trampske",
        "roof": "slova z názvů trampských písní",
        "level": "normal",
        "hidden": True,
        "inside": [
            "vlak", "niagara", "oheň", "řeka", "údolí", "stopa", "hvězdy",
            "kotva",
        ],
        "outside": [
            "batoh", "deštník", "dřez", "hadr", "hrneček", "kolík", "motyka",
            "mýdlo", "pekáč", "peněženka", "pračka", "sklenice", "sušák",
            "trouba", "vana",
        ],
        "asks": [
            "jsou v názvech trampských písní",
            "jsou to zároveň příjmení českých prezidentů",
            "jsou v názvech her Járy Cimrmana",
            "mají v sobě dvě stejná písmena vedle sebe",
        ],
    },
    {
        "id": "v12-symfonicke-basne",
        "roof": "slova z názvů symfonických básní",
        "level": "hard",
        "hidden": True,
        "inside": [
            "vltava", "blaník", "šárka", "tábor", "lesy", "pole", "vodník",
            "polednice",
        ],
        "outside": [
            "batoh", "deštník", "lednička", "lopatka", "matrace", "mísa",
            "nůžky", "pekáč", "pinzeta", "plot", "podnos", "popelnice",
            "struhadlo", "vrtačka", "šála",
        ],
        "asks": [
            "jsou v názvech symfonických básní",
            "jsou to zároveň značky nebo modely aut",
            "jsou to zároveň příjmení českých prezidentů",
            "jsou to zároveň jména českých měst",
        ],
    },
    {
        "id": "v12-operety",
        "roof": "slova z názvů operet",
        "level": "hard",
        "hidden": True,
        "inside": [
            "netopýr", "vdova", "krev", "baron", "cikán", "princezna", "mlýn",
            "ptáčník",
        ],
        "outside": [
            "branka", "dřez", "houpačka", "hrnec", "koberec", "koště",
            "lopata", "motyka", "polštář", "provaz", "semínko", "sklenice",
            "svěrák", "zápisník", "řetízek",
        ],
        "asks": [
            "jsou v názvech slavných operet",
            "jsou v názvech Shakespearových her",
            "nemají v sobě ani jednu samohlásku",
            "jsou v názvech večerníčků",
        ],
    },
    {
        "id": "v12-pohadkove-postavy",
        "roof": "jména českých pohádkových postav",
        "level": "normal",
        "hidden": True,
        "inside": [
            "Otesánek", "Budulínek", "Smolíček", "Křemílek", "Rákosníček",
            "Hurvínek", "Bajaja", "Rumcajs",
        ],
        "outside": [
            "hadr", "kbelík", "komoda", "parapet", "peřina", "podnos",
            "police", "pouzdro", "prostěradlo", "provaz", "pytel", "rýč",
            "sklenice", "struhadlo", "trouba",
        ],
        "asks": [
            "jsou to zároveň jména českých pohádkových postav",
            "jsou to zároveň příjmení českých prezidentů",
            "mají v sobě dvě stejná písmena vedle sebe",
            "jsou v názvech večerníčků",
        ],
    },
    {
        "id": "v12-naskladat",
        "roof": "věci, které se dají naskládat na sebe",
        "level": "normal",
        "hidden": True,
        "inside": [
            "talíř", "židle", "krabice", "kelímek", "pneumatika", "paleta",
        ],
        "outside": [
            "koště", "žebřík", "hadice", "provaz", "lampa", "deštník",
            "kytara", "zrcadlo", "obraz", "vidlička",
        ],
        "asks": [
            "se dají naskládat na sebe do komína",
            "jsou to zároveň značky nebo modely aut",
            "jsou v názvech Shakespearových her",
            "jsou to zároveň příjmení českých prezidentů",
        ],
    },
    {
        "id": "v12-zapichnout",
        "roof": "věci, které se zapichují do země",
        "level": "normal",
        "hidden": True,
        "inside": [
            "kolík", "slunečník", "lopata", "cedule", "stan", "vidle",
        ],
        "outside": [
            "hrnec", "deka", "kniha", "lampa", "koberec", "zrcadlo",
            "polštář", "ubrus", "sklenice", "talíř",
        ],
        "asks": [
            "se zapichují do země",
            "nemají v sobě ani jednu samohlásku",
            "jsou v názvech Shakespearových her",
            "jsou v názvech večerníčků",
        ],
    },
    {
        "id": "v12-ropa",
        "roof": "věci vyráběné z ropy",
        "level": "hard",
        "hidden": True,
        "inside": [
            "benzin", "asfalt", "nylon", "vazelína", "plast", "parafín",
        ],
        "outside": [
            "papír", "vlna", "bavlna", "hlína", "sklo", "vápno", "kámen",
            "dřevo", "korek", "len",
        ],
        "asks": [
            "se vyrábějí z ropy",
            "jsou to zároveň značky českého piva",
            "jsou v názvech her Járy Cimrmana",
            "jsou to znamení zvěrokruhu",
        ],
    },
    {
        "id": "v12-drevo",
        "roof": "věci vyráběné ze dřeva",
        "level": "normal",
        "hidden": True,
        "inside": [
            "papír", "sirka", "tužka", "sud", "parkety", "korek",
        ],
        "outside": [
            "sklo", "beton", "ocel", "hliník", "guma", "porcelán", "cement",
            "asfalt", "nylon", "plast",
        ],
        "asks": [
            "se vyrábějí ze dřeva",
            "mají v sobě dvě stejná písmena vedle sebe",
            "čtou se stejně zepředu i zezadu",
            "jsou to zároveň značky nebo modely aut",
        ],
    },
    {
        "id": "v12-recyklace",
        "roof": "věci, které se dají recyklovat",
        "level": "normal",
        "hidden": True,
        "inside": [
            "papír", "sklo", "plech", "plast", "baterie", "olej",
        ],
        "outside": [
            "porcelán", "zrcadlo", "keramika", "žárovka", "guma",
            "pneumatika", "vata", "obinadlo", "tapeta", "molitan",
        ],
        "asks": [
            "se dají recyklovat",
            "jsou to zároveň příjmení českých prezidentů",
            "jsou to zároveň jména českých měst",
            "jsou to zároveň značky českého piva",
        ],
    },
    {
        "id": "v12-roztavit",
        "roof": "věci, které se dají roztavit a znovu ztuhnout",
        "level": "normal",
        "hidden": True,
        "inside": [
            "vosk", "cín", "olovo", "sklo", "čokoláda", "sýr",
        ],
        "outside": [
            "dřevo", "papír", "kámen", "cihla", "vápno", "beton", "písek",
            "hlína", "korek", "vlna",
        ],
        "asks": [
            "se dají roztavit a nechat znovu ztuhnout",
            "jsou v názvech her Járy Cimrmana",
            "nemají v sobě ani jednu samohlásku",
            "mají v sobě schované zvíře",
        ],
    },
    {
        "id": "v12-sbirka",
        "roof": "věci, které se sbírají do sbírek",
        "level": "normal",
        "hidden": True,
        "inside": [
            "známka", "mince", "pohlednice", "odznak", "autogram", "model",
        ],
        "outside": [
            "brambora", "mrkev", "cibule", "hrách", "rýže", "mouka", "sůl",
            "cukr", "krupice", "kroupy",
        ],
        "asks": [
            "se sbírají do sbírek",
            "čtou se stejně zepředu i zezadu",
            "jsou v názvech Shakespearových her",
            "jsou to zároveň jména českých měst",
        ],
    },
    {
        "id": "v12-spotreba",
        "roof": "věci s vytištěným datem spotřeby",
        "level": "normal",
        "hidden": True,
        "inside": [
            "jogurt", "mléko", "šunka", "léky", "vejce", "salát",
        ],
        "outside": [
            "kladivo", "hřebík", "lopata", "žebřík", "provaz", "cihla",
            "klíč", "prkno", "kolík", "drát",
        ],
        "asks": [
            "mají na obalu datum spotřeby",
            "jsou to zároveň značky českého piva",
            "mají v sobě dvě stejná písmena vedle sebe",
            "jsou v názvech Shakespearových her",
        ],
    },
    {
        "id": "v12-noc-zvuk",
        "roof": "tvorové, kteří se ozývají v noci",
        "level": "hard",
        "hidden": True,
        "inside": [
            "sova", "cvrček", "žába", "slavík", "netopýr", "vlk",
        ],
        "outside": [
            "skřivan", "vlaštovka", "kos", "čáp", "husa", "kůň", "kráva",
            "ovce", "beran", "kohout",
        ],
        "asks": [
            "se ozývají hlavně v noci",
            "jsou v názvech večerníčků",
            "jsou to znamení zvěrokruhu",
            "jsou v názvech Shakespearových her",
        ],
    },
    {
        "id": "v12-obloha-okem",
        "roof": "tělesa viditelná pouhým okem",
        "level": "normal",
        "hidden": True,
        "inside": [
            "měsíc", "venuše", "mars", "jupiter", "saturn", "kometa",
        ],
        "outside": [
            "neptun", "uran", "pluto", "ceres", "eris", "charon", "titan",
            "europa", "ganymed", "callisto",
        ],
        "asks": [
            "jsou na obloze vidět i bez dalekohledu",
            "mají v sobě schované zvíře",
            "jsou to zároveň jména českých měst",
            "jsou to zároveň značky nebo modely aut",
        ],
    },
    {
        "id": "v12-obiha-slunce",
        "roof": "tělesa obíhající kolem Slunce",
        "level": "hard",
        "hidden": True,
        "inside": [
            "země", "mars", "merkur", "planetka", "kometa", "jupiter",
        ],
        "outside": [
            "měsíc", "europa", "titan", "triton", "phobos", "deimos",
            "ganymed", "callisto", "charon", "io",
        ],
        "asks": [
            "obíhají kolem Slunce",
            "jsou v názvech večerníčků",
            "čtou se stejně zepředu i zezadu",
            "jsou to zároveň jména českých měst",
        ],
    },
    {
        "id": "v12-drogerie",
        "roof": "věci, které se koupí v drogerii",
        "level": "normal",
        "hidden": True,
        "inside": [
            "mýdlo", "šampon", "prášek", "zubní", "hřeben", "houba",
        ],
        "outside": [
            "kladivo", "hřebík", "lopata", "žebřík", "provaz", "cihla",
            "klíč", "prkno", "kolík", "drát",
        ],
        "asks": [
            "se prodávají v drogerii",
            "jsou v názvech Shakespearových her",
            "jsou to zároveň jména českých měst",
            "jsou v názvech večerníčků",
        ],
    },
    {
        "id": "v12-jednou-rocne",
        "roof": "věci, které se používají jednou za rok",
        "level": "normal",
        "hidden": True,
        "inside": [
            "stromeček", "kraslice", "adventní", "prskavka", "betlém",
            "maska",
        ],
        "outside": [
            "hrnec", "lžíce", "ručník", "kartáček", "hřeben", "ponožka",
            "klíč", "peněženka", "budík", "deka",
        ],
        "asks": [
            "se používají jen jednou za rok",
            "jsou to zároveň příjmení českých prezidentů",
            "jsou v názvech Shakespearových her",
            "jsou to znamení zvěrokruhu",
        ],
    },
    {
        "id": "v12-voni-spalene",
        "roof": "věci, které voní, když se spálí",
        "level": "hard",
        "hidden": True,
        "inside": [
            "kadidlo", "tabák", "jehličí", "kafr", "koření", "vonná",
        ],
        "outside": [
            "guma", "plast", "vlasy", "peří", "kůže", "olej", "dehet", "síra",
            "vlna", "papír",
        ],
        "asks": [
            "voní, teprve když se zapálí",
            "jsou v názvech her Járy Cimrmana",
            "jsou v názvech večerníčků",
            "čtou se stejně zepředu i zezadu",
        ],
    },
    {
        "id": "v12-na-prst",
        "roof": "věci, které se navlékají na prst",
        "level": "normal",
        "hidden": True,
        "inside": [
            "prsten", "náprstek", "gumička", "obvaz", "náplast", "rukavice",
        ],
        "outside": [
            "čepice", "šála", "opasek", "batoh", "brýle", "hodinky",
            "náhrdelník", "ponožka", "bunda", "kabát",
        ],
        "asks": [
            "se navlékají na prst",
            "jsou to zároveň jména českých měst",
            "mají v sobě schované zvíře",
            "jsou to zároveň příjmení českých prezidentů",
        ],
    },
    {
        "id": "v12-rozsvitit",
        "roof": "věci, které se dají rozsvítit",
        "level": "normal",
        "hidden": True,
        "inside": [
            "lampa", "baterka", "svíčka", "displej", "maják", "reflektor",
        ],
        "outside": [
            "zrcadlo", "okno", "sklenice", "hodinky", "kompas", "budík",
            "váhy", "teploměr", "brýle", "lupa",
        ],
        "asks": [
            "se dají rozsvítit",
            "jsou to zároveň jména českých měst",
            "čtou se stejně zepředu i zezadu",
            "nemají v sobě ani jednu samohlásku",
        ],
    },
    {
        "id": "v12-zamrazit",
        "roof": "jídlo, které se dá zamrazit",
        "level": "normal",
        "hidden": True,
        "inside": [
            "maso", "pečivo", "ovoce", "zelenina", "ryba", "těsto",
        ],
        "outside": [
            "salát", "okurka", "vejce", "majonéza", "jogurt", "smetana",
            "meloun", "ředkvička", "rajče", "tvaroh",
        ],
        "asks": [
            "se dá zamrazit a pak zase rozmrazit",
            "čtou se stejně zepředu i zezadu",
            "jsou to zároveň jména českých měst",
            "jsou to zároveň značky českého piva",
        ],
    },
    {
        "id": "v12-vyzehlit",
        "roof": "věci, které se dají vyžehlit",
        "level": "normal",
        "hidden": True,
        "inside": [
            "košile", "ubrus", "kapesník", "povlečení", "sukně", "záclona",
        ],
        "outside": [
            "svetr", "bunda", "rukavice", "pásek", "boty", "batoh", "čepice",
            "deka", "polštář", "koberec",
        ],
        "asks": [
            "se dají vyžehlit",
            "jsou to zároveň značky českého piva",
            "jsou v názvech večerníčků",
            "jsou to zároveň jména českých měst",
        ],
    },
    {
        "id": "v12-more",
        "roof": "názvy moří",
        "level": "normal",
        "hidden": True,
        "inside": [
            "Baltské", "Černé", "Rudé", "Jaderské", "Egejské", "Severní",
            "Karibské", "Sargasové",
        ],
        "outside": [
            "chleba", "deštník", "hrábě", "kartáček", "kolík", "konev", "koš",
            "parapet", "pilník", "propiska", "sklenice", "svěrák", "trouba",
            "vrtačka", "šála",
        ],
        "asks": [
            "jsou to zároveň názvy moří",
            "jsou to zároveň značky nebo modely aut",
            "jsou to zároveň jména českých měst",
            "jsou to zároveň značky českého piva",
        ],
    },
    {
        "id": "v12-kava",
        "roof": "druhy kávy",
        "level": "normal",
        "hidden": True,
        "inside": [
            "espreso", "latte", "cappuccino", "mocca", "americano",
            "ristretto", "turek", "frappé",
        ],
        "outside": [
            "brýle", "dřez", "hodinky", "hřebík", "koberec", "kolík", "koš",
            "lepidlo", "mísa", "nůžky", "pilník", "struhadlo", "utěrka",
            "šuplík", "žebřík",
        ],
        "asks": [
            "jsou to zároveň druhy kávy",
            "čtou se stejně zepředu i zezadu",
            "jsou to zároveň příjmení českých prezidentů",
            "jsou v názvech Shakespearových her",
        ],
    },
    {
        "id": "v12-caj",
        "roof": "druhy čaje",
        "level": "normal",
        "hidden": True,
        "inside": [
            "zelený", "černý", "bílý", "rooibos", "oolong", "maté", "matcha",
            "jasmínový",
        ],
        "outside": [
            "batoh", "brýle", "hrnec", "hrneček", "koberec", "lampa",
            "lopata", "podnos", "pračka", "pytel", "silnice", "truhlík",
            "ubrus", "vrtačka", "šroub",
        ],
        "asks": [
            "jsou to zároveň druhy čaje",
            "jsou v názvech večerníčků",
            "jsou to znamení zvěrokruhu",
            "jsou to zároveň jména českých měst",
        ],
    },
    {
        "id": "v12-testoviny",
        "roof": "druhy těstovin",
        "level": "normal",
        "hidden": True,
        "inside": [
            "špagety", "penne", "fusilli", "kolínka", "nudle", "vřetena",
            "lasagne", "tarhoňa",
        ],
        "outside": [
            "batoh", "brambora", "branka", "deka", "hadr", "hřeben",
            "kastrol", "kbelík", "kolík", "konev", "matice", "matrace",
            "pinzeta", "sporák", "struhadlo",
        ],
        "asks": [
            "jsou to zároveň druhy těstovin",
            "jsou v názvech večerníčků",
            "jsou v názvech Shakespearových her",
            "nemají v sobě ani jednu samohlásku",
        ],
    },
    {
        "id": "v12-pecivo",
        "roof": "druhy pečiva",
        "level": "normal",
        "hidden": True,
        "inside": [
            "rohlík", "houska", "dalamánek", "veka", "bageta", "kaiserka",
            "preclík", "bulka",
        ],
        "outside": [
            "brambora", "bunda", "guma", "hrnec", "kabát", "mísa", "pilník",
            "plot", "popelnice", "rohožka", "silnice", "stůl", "sud", "tácek",
            "utěrka",
        ],
        "asks": [
            "jsou to zároveň druhy pečiva",
            "jsou to zároveň příjmení českých prezidentů",
            "jsou v názvech Shakespearových her",
            "jsou to zároveň značky nebo modely aut",
        ],
    },
    {
        "id": "v12-prvky",
        "roof": "názvy chemických prvků",
        "level": "hard",
        "hidden": True,
        "inside": [
            "wolfram", "vanad", "kobalt", "gallium", "rhenium", "iridium",
            "thallium", "lanthan",
        ],
        "outside": [
            "batoh", "deka", "hadr", "kompost", "lepidlo", "lopatka",
            "parapet", "provaz", "silnice", "sušák", "trakař", "truhlík",
            "zahrada", "šroub", "šuplík",
        ],
        "asks": [
            "jsou to zároveň názvy chemických prvků",
            "jsou to zároveň značky českého piva",
            "jsou to znamení zvěrokruhu",
            "jsou to zároveň značky nebo modely aut",
        ],
    },
    {
        "id": "v12-evropske-reky",
        "roof": "evropské řeky",
        "level": "hard",
        "hidden": True,
        "inside": [
            "Seina", "Temže", "Pád", "Tibera", "Rhóna", "Ebro", "Visla",
            "Sáva",
        ],
        "outside": [
            "deka", "hadr", "kabát", "kbelík", "kladívko", "kleště",
            "kompost", "kýbl", "motyka", "mýdlo", "naběračka", "rohožka",
            "sud", "svěrák", "ubrus",
        ],
        "asks": [
            "jsou to zároveň evropské řeky",
            "jsou to zároveň příjmení českých prezidentů",
            "jsou to znamení zvěrokruhu",
            "mají v sobě dvě stejná písmena vedle sebe",
        ],
    },
    {
        "id": "v12-africke-staty",
        "roof": "africké státy",
        "level": "hard",
        "hidden": True,
        "inside": [
            "Ghana", "Zambie", "Angola", "Senegal", "Tunisko", "Súdán",
            "Uganda", "Namibie",
        ],
        "outside": [
            "guma", "kbelík", "kolík", "lopata", "mrkev", "mísa", "náramek",
            "parapet", "pekáč", "polštář", "popelnice", "semínko", "skříň",
            "sušák", "žebřík",
        ],
        "asks": [
            "jsou to zároveň africké státy",
            "jsou to zároveň značky českého piva",
            "jsou to zároveň značky nebo modely aut",
            "mají v sobě dvě stejná písmena vedle sebe",
        ],
    },
    {
        "id": "v12-americke-staty",
        "roof": "státy USA",
        "level": "hard",
        "hidden": True,
        "inside": [
            "Texas", "Utah", "Nevada", "Montana", "Ohio", "Alaska", "Oregon",
            "Idaho",
        ],
        "outside": [
            "brambora", "houpačka", "hřeben", "kabát", "kladívko", "komoda",
            "pekáč", "peněženka", "popelnice", "pouzdro", "propiska",
            "sklenice", "skříň", "sud", "žehlička",
        ],
        "asks": [
            "jsou to zároveň státy Spojených států",
            "jsou to zároveň jména českých měst",
            "jsou v názvech her Járy Cimrmana",
            "mají v sobě dvě stejná písmena vedle sebe",
        ],
    },
    {
        "id": "v12-olympijska-mesta",
        "roof": "města letních olympiád",
        "level": "hard",
        "hidden": True,
        "inside": [
            "Atlanta", "Sydney", "Barcelona", "Helsinky", "Antverpy",
            "Melbourne", "Mnichov", "Soul",
        ],
        "outside": [
            "hrnec", "lednička", "lopatka", "metr", "motyka", "mísa", "mýdlo",
            "nůžky", "popelnice", "provaz", "ramínko", "semínko", "smeták",
            "ubrus", "šroub",
        ],
        "asks": [
            "jsou to zároveň města letních olympiád",
            "jsou to znamení zvěrokruhu",
            "jsou to zároveň příjmení českých prezidentů",
            "čtou se stejně zepředu i zezadu",
        ],
    },
    {
        "id": "v12-jazyky",
        "roof": "názvy jazyků",
        "level": "normal",
        "hidden": True,
        "inside": [
            "baskičtina", "velština", "gruzínština", "sanskrt", "jidiš",
            "svahilština", "urdština", "tamilština",
        ],
        "outside": [
            "brýle", "hadr", "kastrol", "kleště", "lednička", "lopatka",
            "postel", "propiska", "prostěradlo", "schránka", "sud", "trouba",
            "věšák", "šroub", "šála",
        ],
        "asks": [
            "jsou to zároveň názvy jazyků",
            "jsou to znamení zvěrokruhu",
            "jsou v názvech her Járy Cimrmana",
            "jsou to zároveň značky nebo modely aut",
        ],
    },
    {
        "id": "v12-svetci",
        "roof": "čeští světci",
        "level": "hard",
        "hidden": True,
        "inside": [
            "Václav", "Ludmila", "Vojtěch", "Prokop", "Anežka", "Zdislava",
            "Jan", "Kliment",
        ],
        "outside": [
            "brambora", "chleba", "hadr", "hoblík", "hrábě", "hřebík",
            "kabát", "kolík", "motyka", "naběračka", "peřina", "propiska",
            "rýč", "ubrousek", "věšák",
        ],
        "asks": [
            "jsou to zároveň čeští světci",
            "jsou v názvech her Járy Cimrmana",
            "čtou se stejně zepředu i zezadu",
            "jsou to zároveň příjmení českých prezidentů",
        ],
    },
    {
        "id": "v12-cinsky-zverokruh",
        "roof": "znamení čínského zvěrokruhu",
        "level": "hard",
        "hidden": True,
        "inside": [
            "krysa", "buvol", "tygr", "králík", "drak", "had", "koza",
            "opice",
        ],
        "outside": [
            "bunda", "chleba", "deštník", "hoblík", "komoda", "krém",
            "květináč", "lavička", "nůžky", "ponožka", "sklenice", "ubrus",
            "vařečka", "šála", "žebřík",
        ],
        "asks": [
            "jsou to zároveň znamení čínského zvěrokruhu",
            "jsou to zároveň příjmení českých prezidentů",
            "jsou to zároveň značky nebo modely aut",
            "mají v sobě dvě stejná písmena vedle sebe",
        ],
    },
    {
        "id": "v12-malirske-barvy",
        "roof": "malířské barvy",
        "level": "hard",
        "hidden": True,
        "inside": [
            "okr", "umbra", "ultramarín", "karmín", "sépie", "indigo",
            "kobalt", "běloba",
        ],
        "outside": [
            "hodinky", "kabát", "matice", "motyka", "myčka", "mýdlo",
            "naběračka", "postel", "pračka", "rýč", "sklenice", "skříň",
            "stůl", "ubrousek", "šuplík",
        ],
        "asks": [
            "jsou to zároveň názvy malířských barev",
            "mají v sobě schované zvíře",
            "čtou se stejně zepředu i zezadu",
            "jsou to zároveň značky českého piva",
        ],
    },
    {
        "id": "v12-odrudy-vina",
        "roof": "odrůdy vína",
        "level": "hard",
        "hidden": True,
        "inside": [
            "ryzlink", "veltlín", "tramín", "frankovka", "sylvánské",
            "portugal", "müller", "merlot",
        ],
        "outside": [
            "batoh", "chleba", "dřez", "naběračka", "parapet", "pekáč",
            "rohožka", "ručník", "rýč", "silnice", "skříň", "stůl", "sušák",
            "trouba", "vrtačka",
        ],
        "asks": [
            "jsou to zároveň odrůdy vína",
            "jsou v názvech Shakespearových her",
            "jsou v názvech her Járy Cimrmana",
            "jsou v názvech večerníčků",
        ],
    },
]
