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
            "korpus", "koryto", "krakorec", "loviště", "most", "nábřeží",
            "propadlo", "roubení", "střecha", "ventil", "záda", "šuplík",
        ],
        "asks": [
            "jsou to zároveň části kotle",
            "jsou to zároveň jména českých měst",
            "čtou se stejně zepředu i zezadu",
            "jsou to znamení zvěrokruhu",
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
            "komínovka", "korouhvička", "krakorec", "ladička", "okov",
            "podšívka", "roubení", "sklo", "struna", "vymetání", "vázání",
            "zákryt",
        ],
        "asks": [
            "jsou to zároveň části skříně",
            "mají v sobě dvě stejná písmena vedle sebe",
            "jsou v názvech Shakespearových her",
            "jsou to zároveň příjmení českých prezidentů",
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
            "blok", "hlediště", "kladívko", "kryt", "kádiště", "most",
            "obruba", "patka", "pedál", "předměstí", "roubení", "tryska",
        ],
        "asks": [
            "jsou to zároveň části komína",
            "jsou to zároveň jména českých měst",
            "jsou to zároveň značky českého piva",
            "jsou v názvech večerníčků",
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
            "břeh", "centrum", "hlediště", "kladívko", "korouhvička", "patka",
            "stranice", "strojivo", "ventil", "záda", "zákulisí", "čtvrť",
        ],
        "asks": [
            "jsou to zároveň části studny",
            "čtou se stejně zepředu i zezadu",
            "jsou to zároveň příjmení českých prezidentů",
            "mají v sobě schované zvíře",
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
            "hrana", "hráz", "jeviště", "kladívko", "krakorec", "opona",
            "patka", "sopouch", "stoupání", "stranice", "vymetání", "výměník",
        ],
        "asks": [
            "jsou to zároveň části řeky",
            "mají v sobě dvě stejná písmena vedle sebe",
            "jsou to zároveň jména českých měst",
            "jsou to zároveň značky českého piva",
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
            "hlediště", "kladívko", "nosič", "potítko", "rumpál", "stoupání",
            "stranice", "stupeň", "vačka", "vložka", "výměník", "zákulisí",
        ],
        "asks": [
            "jsou to zároveň části rybníka",
            "jsou to zároveň značky českého piva",
            "jsou to zároveň příjmení českých prezidentů",
            "jsou v názvech Shakespearových her",
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
            "korouhvička", "koryto", "obruba", "okov", "pedál", "průduch",
            "sklo", "sopouch", "stupeň", "vázání", "záda", "zákulisí",
        ],
        "asks": [
            "jsou to zároveň části města",
            "jsou v názvech Shakespearových her",
            "mají v sobě schované zvíře",
            "jsou v názvech her Járy Cimrmana",
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
            "kladívko", "krakorec", "náměstí", "ojnice", "periferie",
            "průduch", "roubení", "skruž", "strojivo", "vložka", "vázání",
            "šuplík",
        ],
        "asks": [
            "jsou to zároveň části divadla",
            "jsou v názvech her Járy Cimrmana",
            "jsou v názvech Shakespearových her",
            "jsou v názvech večerníčků",
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
            "balkon", "břeh", "centrum", "koryto", "krempa", "ladička",
            "pramen", "průduch", "sedlo", "stoka", "vačka", "výpusť",
        ],
        "asks": [
            "jsou to zároveň části klavíru",
            "jsou to zároveň jména českých měst",
            "jsou v názvech Shakespearových her",
            "mají v sobě schované zvíře",
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
            "hlediště", "jeviště", "komínovka", "koryto", "loviště", "most",
            "potítko", "průduch", "rumpál", "střecha", "tlumítko", "vymetání",
        ],
        "asks": [
            "jsou to zároveň části trubky",
            "čtou se stejně zepředu i zezadu",
            "jsou v názvech večerníčků",
            "jsou to zároveň značky nebo modely aut",
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
            "blok", "kladívko", "krakorec", "nábřeží", "okov", "patka",
            "sopouch", "stoupání", "střecha", "tlumítko", "ventil", "závěs",
        ],
        "asks": [
            "jsou to zároveň části brýlí",
            "jsou v názvech Shakespearových her",
            "jsou to zároveň značky českého piva",
            "jsou to zároveň jména českých měst",
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
            "břeh", "centrum", "hlediště", "hráz", "okov", "opona", "police",
            "průduch", "struna", "střecha", "výměník", "zákulisí",
        ],
        "asks": [
            "jsou to zároveň části motoru",
            "jsou to zároveň příjmení českých prezidentů",
            "čtou se stejně zepředu i zezadu",
            "jsou v názvech her Járy Cimrmana",
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
            "kladívko", "korouhvička", "ladička", "náměstí", "obruba",
            "pramen", "přeliv", "tůň", "ventil", "vázání", "výpusť", "závěs",
        ],
        "asks": [
            "jsou to zároveň části rakety",
            "nemají v sobě ani jednu samohlásku",
            "jsou to zároveň značky nebo modely aut",
            "jsou to zároveň jména českých měst",
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
            "břeh", "kádiště", "periferie", "pramen", "sedlo", "stranice",
            "struna", "tryska", "vymetání", "výměník", "ústí", "čtvrť",
        ],
        "asks": [
            "jsou to zároveň části lyže",
            "jsou v názvech her Járy Cimrmana",
            "jsou to zároveň značky českého piva",
            "jsou to znamení zvěrokruhu",
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
            "břeh", "klapka", "korpus", "nosič", "nožička", "opona", "stupeň",
            "vymetání", "víko", "výpusť", "záda", "čtvrť",
        ],
        "asks": [
            "jsou to zároveň části klobouku",
            "jsou to zároveň značky českého piva",
            "jsou v názvech večerníčků",
            "jsou to zároveň příjmení českých prezidentů",
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
            "dláto", "expanzní", "humno", "lept", "lišta", "nopa", "odlitek",
            "prořezávka", "roub", "slad", "vyčinění", "výlov",
        ],
        "asks": [
            "jsou to zároveň kominické pojmy",
            "čtou se stejně zepředu i zezadu",
            "nemají v sobě ani jednu samohlásku",
            "mají v sobě schované zvíře",
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
            "krokev", "lept", "obsádka", "odlitek", "otisk", "patina",
            "plátování", "prošívání", "sloup", "vymetání", "zavádění", "špic",
        ],
        "asks": [
            "jsou to zároveň koželužské pojmy",
            "čtou se stejně zepředu i zezadu",
            "jsou to zároveň značky českého piva",
            "jsou to zároveň jména českých měst",
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
            "odvzdušnění", "rmut", "rozdělovač", "révy", "saze", "slad",
            "sušárna", "tmel", "useň", "výhon", "zasklení", "štěpování",
        ],
        "asks": [
            "jsou to zároveň tesařské pojmy",
            "mají v sobě dvě stejná písmena vedle sebe",
            "jsou to zároveň příjmení českých prezidentů",
            "jsou v názvech her Járy Cimrmana",
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
            "komory", "konstrukce", "lept", "otisk", "patina", "reliéf",
            "sokl", "tmel", "výhon", "výlov", "zátah", "česání",
        ],
        "asks": [
            "jsou to zároveň kamenické pojmy",
            "jsou v názvech Shakespearových her",
            "mají v sobě schované zvíře",
            "jsou to zároveň značky českého piva",
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
            "hlávka", "kalení", "komory", "leštění", "molitan", "máčení",
            "roub", "rytina", "termostatická", "tříslo", "useň", "vazba",
        ],
        "asks": [
            "jsou to zároveň sochařské pojmy",
            "čtou se stejně zepředu i zezadu",
            "mají v sobě schované zvíře",
            "nemají v sobě ani jednu samohlásku",
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
            "blok", "kalení", "lišta", "líc", "model", "odlitek", "plátování",
            "reliéf", "rozpěra", "tabule", "výlov", "zátah",
        ],
        "asks": [
            "jsou to zároveň grafické pojmy",
            "jsou to zároveň příjmení českých prezidentů",
            "nemají v sobě ani jednu samohlásku",
            "jsou to zároveň značky nebo modely aut",
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
            "busta", "dláto", "expanzní", "kalení", "konstrukce", "lept",
            "lužení", "matrice", "oběh", "prořezávka", "termostatická",
            "tříslo",
        ],
        "asks": [
            "jsou to zároveň čalounické pojmy",
            "jsou v názvech večerníčků",
            "jsou to zároveň jména českých měst",
            "čtou se stejně zepředu i zezadu",
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
            "dláto", "hvozd", "lom", "máčení", "plátování", "popruh",
            "prořezávka", "roub", "sušárna", "vymetání", "vyčinění",
            "zavádění",
        ],
        "asks": [
            "jsou to zároveň sklenářské pojmy",
            "jsou to zároveň značky nebo modely aut",
            "jsou to znamení zvěrokruhu",
            "jsou to zároveň jména českých měst",
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
            "konstrukce", "osazení", "potah", "rmut", "slad", "sloup",
            "vazba", "vymetání", "zasklení", "řezák", "špic", "štěpování",
        ],
        "asks": [
            "jsou to zároveň topenářské pojmy",
            "nemají v sobě ani jednu samohlásku",
            "čtou se stejně zepředu i zezadu",
            "jsou v názvech Shakespearových her",
        ],
    },
    {
        "id": "v12-sladovna",
        "roof": "sladovnické pojmy",
        "level": "hard",
        "hidden": True,
        "inside": [
            "máčení", "klíčení", "hvozd", "humno", "slad", "rmut",
        ],
        "outside": [
            "kalení", "krokev", "leštění", "osazení", "patina", "pozednice",
            "prořezávka", "prošívání", "termostatická", "vymetání",
            "zavádění", "česání",
        ],
        "asks": [
            "jsou to zároveň sladovnické pojmy",
            "čtou se stejně zepředu i zezadu",
            "jsou to znamení zvěrokruhu",
            "mají v sobě schované zvíře",
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
            "blok", "lom", "odvzdušnění", "plátování", "prošívání", "revize",
            "sloup", "tabule", "useň", "vymetání", "špic", "štěpování",
        ],
        "asks": [
            "jsou to zároveň rybníkářské pojmy",
            "jsou v názvech her Járy Cimrmana",
            "jsou to zároveň značky českého piva",
            "jsou to zároveň jména českých měst",
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
            "expanzní", "máčení", "oběh", "plůdek", "popruh", "potah",
            "sloup", "sušárna", "tmel", "useň", "česání", "řezák",
        ],
        "asks": [
            "jsou to zároveň ovocnářské pojmy",
            "jsou v názvech večerníčků",
            "jsou v názvech Shakespearových her",
            "mají v sobě schované zvíře",
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
            "dláto", "hvozd", "koudel", "krokev", "matrice", "nopa",
            "rozdělovač", "rozpěra", "saze", "stoupačka", "řezák",
            "štěpování",
        ],
        "asks": [
            "jsou to zároveň chmelařské pojmy",
            "jsou to zároveň značky českého piva",
            "jsou v názvech večerníčků",
            "mají v sobě dvě stejná písmena vedle sebe",
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
            "dvojče", "oddenek", "otisk", "profil", "přenos", "ražba", "spád",
            "svlékání", "tvrdost", "vryp", "vývoj", "záloha",
        ],
        "asks": [
            "jsou to zároveň ornitologické pojmy",
            "jsou v názvech her Járy Cimrmana",
            "nemají v sobě ani jednu samohlásku",
            "jsou to zároveň značky českého piva",
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
            "druhohory", "linka", "podnět", "postoj", "profil",
            "rekonstrukce", "rušení", "sběr", "skafandr", "stopa", "výkon",
            "úžlabí",
        ],
        "asks": [
            "jsou to zároveň entomologické pojmy",
            "jsou v názvech her Járy Cimrmana",
            "jsou to zároveň příjmení českých prezidentů",
            "nemají v sobě ani jednu samohlásku",
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
            "daktyloskopie", "druhohory", "hnízdiště", "hrana", "obratel",
            "povodí", "rekonstrukce", "retence", "tah", "temperament",
            "vývoj", "špička",
        ],
        "asks": [
            "jsou to zároveň botanické pojmy",
            "nemají v sobě ani jednu samohlásku",
            "jsou to znamení zvěrokruhu",
            "jsou v názvech Shakespearových her",
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
            "daktyloskopie", "letorost", "linka", "oddenek", "patina",
            "ražba", "rušení", "snůška", "volavý", "vrstva", "vysílač",
            "zkamenělina",
        ],
        "asks": [
            "jsou to zároveň mineralogické pojmy",
            "jsou to zároveň značky nebo modely aut",
            "nemají v sobě ani jednu samohlásku",
            "čtou se stejně zepředu i zezadu",
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
            "larva", "modul", "nominál", "odtok", "patina", "profil",
            "retence", "rušení", "sosák", "tah", "tykadlo", "záloha",
        ],
        "asks": [
            "jsou to zároveň paleontologické pojmy",
            "mají v sobě schované zvíře",
            "jsou v názvech Shakespearových her",
            "jsou to zároveň příjmení českých prezidentů",
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
            "blok", "daktyloskopie", "dvojče", "hnízdiště", "lesk", "mláďata",
            "návratový", "opis", "sbírka", "sběr", "špička", "štěpnost",
        ],
        "asks": [
            "jsou to zároveň hydrologické pojmy",
            "jsou to znamení zvěrokruhu",
            "jsou v názvech večerníčků",
            "jsou to zároveň příjmení českých prezidentů",
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
            "druhohory", "hrana", "letorost", "obratel", "odtok", "ražba",
            "snůška", "vjem", "vodočet", "vryp", "výkon", "špička",
        ],
        "asks": [
            "jsou to zároveň kosmonautické pojmy",
            "mají v sobě schované zvíře",
            "jsou to zároveň jména českých měst",
            "jsou v názvech večerníčků",
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
            "dvojče", "kukla", "letorost", "mláďata", "naleziště", "oddenek",
            "rekonstrukce", "sběr", "skafandr", "stopa", "tykadlo", "volavý",
        ],
        "asks": [
            "jsou to zároveň telekomunikační pojmy",
            "jsou to znamení zvěrokruhu",
            "jsou v názvech večerníčků",
            "jsou to zároveň značky nebo modely aut",
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
            "cibule", "hrana", "letorost", "naleziště", "nominál", "oběžná",
            "paměť", "patina", "podnět", "přetížení", "rekonstrukce", "sosák",
        ],
        "asks": [
            "jsou to zároveň energetické pojmy",
            "čtou se stejně zepředu i zezadu",
            "jsou to zároveň značky českého piva",
            "jsou to zároveň příjmení českých prezidentů",
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
            "modul", "naleziště", "odtok", "postoj", "pásmo", "spád",
            "tykadlo", "volavý", "výkon", "zkamenělina", "úžlabí", "špička",
        ],
        "asks": [
            "jsou to zároveň numismatické pojmy",
            "jsou to zároveň jména českých měst",
            "mají v sobě schované zvíře",
            "jsou v názvech Shakespearových her",
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
            "blok", "kukla", "lesk", "letorost", "naleziště", "opis",
            "palist", "patina", "postoj", "přeslen", "záloha", "štěpnost",
        ],
        "asks": [
            "jsou to zároveň kriminalistické pojmy",
            "jsou to zároveň jména českých měst",
            "nemají v sobě ani jednu samohlásku",
            "jsou to zároveň příjmení českých prezidentů",
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
            "daktyloskopie", "hnízdiště", "larva", "modul", "obratel",
            "oběžná", "opis", "palist", "přenos", "retence", "sbírka", "sběr",
        ],
        "asks": [
            "jsou to zároveň psychologické pojmy",
            "jsou to znamení zvěrokruhu",
            "jsou to zároveň značky českého piva",
            "čtou se stejně zepředu i zezadu",
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
            "báječná", "cikán", "halelujá", "hvězdy", "jahody", "mlejn",
            "nora", "peklo", "sestřičky", "skřítek", "vodník", "zámek",
        ],
        "asks": [
            "jsou v názvech knih Ernesta Hemingwaye",
            "jsou to zároveň příjmení českých prezidentů",
            "nemají v sobě ani jednu samohlásku",
            "jsou v názvech Shakespearových her",
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
            "armáda", "baron", "lvíče", "netopýr", "ptáčník", "rodeo",
            "sněhu", "vdova", "zbraně", "zlatokop", "štěstí", "ženská",
        ],
        "asks": [
            "jsou v názvech díla Franze Kafky",
            "jsou v názvech Shakespearových her",
            "mají v sobě schované zvíře",
            "mají v sobě dvě stejná písmena vedle sebe",
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
            "báječná", "dopis", "hvězdy", "jahody", "niagara", "polednice",
            "republika", "ráj", "smrt", "vodník", "zbraně", "zlatokop",
        ],
        "asks": [
            "jsou v názvech knih Josefa Škvoreckého",
            "jsou to zároveň značky nebo modely aut",
            "jsou v názvech her Járy Cimrmana",
            "čtou se stejně zepředu i zezadu",
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
            "amerika", "blbec", "kotva", "krev", "mlejn", "netopýr", "nora",
            "proces", "proměna", "sezóna", "zbraně", "zámek",
        ],
        "asks": [
            "jsou v názvech filmů Karla Kachyni",
            "jsou to zároveň příjmení českých prezidentů",
            "mají v sobě dvě stejná písmena vedle sebe",
            "čtou se stejně zepředu i zezadu",
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
            "blaník", "hvězdy", "kotva", "netopýr", "polednice", "proces",
            "proměna", "rodeo", "stařec", "tank", "zbabělci", "zlatokop",
        ],
        "asks": [
            "jsou v názvech filmů Zdeňka Trošky",
            "jsou v názvech večerníčků",
            "nemají v sobě ani jednu samohlásku",
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
            "kotva", "netopýr", "nora", "pole", "republika", "skřítek",
            "smrt", "srnec", "stařec", "stopa", "údolí", "řeka",
        ],
        "asks": [
            "jsou v názvech písní Michala Tučného",
            "jsou to zároveň značky nebo modely aut",
            "mají v sobě dvě stejná písmena vedle sebe",
            "mají v sobě schované zvíře",
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
            "amerika", "halelujá", "lvíče", "netopýr", "nora", "ortel",
            "peklo", "polednice", "stařec", "vodník", "zbabělci", "šárka",
        ],
        "asks": [
            "jsou v názvech trampských písní",
            "mají v sobě schované zvíře",
            "jsou v názvech večerníčků",
            "jsou v názvech her Járy Cimrmana",
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
            "amerika", "baron", "kočár", "krev", "mlýn", "moře", "nora",
            "oheň", "proces", "republika", "sezóna", "zlatokop",
        ],
        "asks": [
            "jsou v názvech symfonických básní",
            "mají v sobě schované zvíře",
            "jsou to zároveň značky českého piva",
            "mají v sobě dvě stejná písmena vedle sebe",
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
            "amerika", "blaník", "halelujá", "hvězdy", "kamarád", "ortel",
            "příběh", "seno", "srnec", "stařec", "tank", "ženská",
        ],
        "asks": [
            "jsou v názvech slavných operet",
            "mají v sobě dvě stejná písmena vedle sebe",
            "mají v sobě schované zvíře",
            "jsou to zároveň značky nebo modely aut",
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
            "Pinocchio", "Bambi", "Mauglí", "Pipi", "Shrek", "Aladin",
            "Ariel", "Mickey",
        ],
        "asks": [
            "jsou to zároveň jména českých pohádkových postav",
            "jsou to zároveň příjmení českých prezidentů",
            "jsou v názvech večerníčků",
            "jsou to znamení zvěrokruhu",
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
            "Bodamské", "Ženevské", "Ladožské", "Oněžské", "Michiganské",
            "Aralské", "Bajkalské", "Huronské",
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
            "kakao", "punč", "grog", "mošt", "cider", "tonik", "limonáda",
            "burčák", "medovina", "kvas",
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
            "rooibos", "oolong", "maté", "matcha", "sencha", "darjeeling",
            "assam", "bancha",
        ],
        "outside": [
            "espreso", "ristretto", "cappuccino", "kakao", "punč", "grog",
            "mošt", "cider", "tonik", "burčák",
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
            "rizoto", "polenta", "focaccia", "pesto", "ragú", "tiramisu",
            "bruschetta", "carpaccio", "gnocchi", "mascarpone",
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
            "knedlík", "halušky", "palačinka", "lívanec", "kaše", "noky",
            "šišky", "taštička", "krupice", "omeleta",
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
            "oxid", "chlorid", "sulfid", "amoniak", "benzen", "acetylen",
            "peroxid", "uhličitan", "dusičnan", "síran",
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
            "Nil", "Kongo", "Amazonka", "Ganga", "Mekong", "Zambezi",
            "Missouri", "Jenisej",
        ],
        "asks": [
            "jsou to zároveň evropské řeky",
            "jsou to zároveň příjmení českých prezidentů",
            "jsou to znamení zvěrokruhu",
            "jsou v názvech večerníčků",
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
            "Nepál", "Laos", "Bhútán", "Ekvádor", "Guyana", "Surinam",
            "Paraguay", "Kambodža",
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
            "Alberta", "Manitoba", "Ontario", "Quebec", "Yukon", "Sonora",
            "Chiapas", "Durango",
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
            "Káhira", "Bombaj", "Lima", "Bogotá", "Manila", "Nairobi",
            "Bagdád", "Teherán",
        ],
        "asks": [
            "jsou to zároveň města letních olympiád",
            "jsou to znamení zvěrokruhu",
            "jsou to zároveň příjmení českých prezidentů",
            "čtou se stejně zepředu i zezadu",
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
            "Bohumil", "Květoslav", "Vlastimil", "Zbyněk", "Slavoj",
            "Radovan", "Miloslav", "Jaromír",
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
            "paleta", "šablona", "plátno", "grunt", "fixativ", "špachtle",
            "napínák", "rydlo", "malířské", "kalafuna",
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
            "burčák", "mošt", "medovina", "cider", "sekt", "vermut", "kvas",
            "punč", "grog", "svařák",
        ],
        "asks": [
            "jsou to zároveň odrůdy vína",
            "jsou v názvech Shakespearových her",
            "jsou v názvech her Járy Cimrmana",
            "jsou v názvech večerníčků",
        ],
    },
]
