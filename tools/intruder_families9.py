"""Devátá várka rodin — sto os, a pokaždé jiné povahy.

TENHLE SOUBOR PÍŠE SKRIPT. Ruční úpravy zmizí při dalším spuštění; opravovat
se má `tools/gen_families9.py`, kde stojí zadání i kontroly.

Skupiny: vlastnosti věcí a přírody, kalendář a zeměpis, mluvnice a pravopis,
ustálená spojení, obory s vlastní řečí (film, právo, tělocvik, pivovar,
jeskyně) a další prameny názvů (Malý princ, Alenka, Poe, pražské pověsti).
"""

FAMILIES9 = [
    {
        "id": "v9-bile",
        "roof": "věci, které jsou vždycky bílé",
        "level": "normal",
        "hidden": True,
        "inside": [
            "sníh", "mléko", "křída", "sůl", "mouka", "vata", "porcelán",
            "tvaroh",
        ],
        "outside": [
            "uhlí", "saze", "asfalt", "dehet", "čokoláda", "káva", "hlína",
            "rez", "inkoust", "rašelina",
        ],
        "asks": [
            "jsou vždycky bílé",
            "jsou to zároveň příjmení českých prezidentů",
            "jsou to znamení zvěrokruhu",
            "mají v sobě dvě stejná písmena vedle sebe",
        ],
    },
    {
        "id": "v9-kysele",
        "roof": "jídlo, které je kyselé",
        "level": "normal",
        "hidden": True,
        "inside": [
            "citron", "ocet", "kefír", "zelí", "rebarbora", "jogurt",
            "šťovík", "brusinka",
        ],
        "outside": [
            "med", "cukr", "mléko", "chleba", "máslo", "banán", "mrkev",
            "olej", "rýže", "sádlo",
        ],
        "asks": [
            "jsou kyselé",
            "čtou se stejně zepředu i zezadu",
            "mají v sobě dvě stejná písmena vedle sebe",
            "jsou to zároveň značky nebo modely aut",
        ],
    },
    {
        "id": "v9-tekute",
        "roof": "látky, které jsou při pokojové teplotě tekuté",
        "level": "hard",
        "hidden": True,
        "inside": [
            "voda", "olej", "mléko", "líh", "rtuť", "ocet", "nafta",
            "glycerin",
        ],
        "outside": [
            "máslo", "vosk", "čokoláda", "sádlo", "parafín", "sklo",
            "margarín", "cukr", "sůl", "vazelína",
        ],
        "asks": [
            "jsou při pokojové teplotě tekuté",
            "čtou se stejně zepředu i zezadu",
            "jsou v názvech večerníčků",
            "jsou to znamení zvěrokruhu",
        ],
    },
    {
        "id": "v9-teplo",
        "roof": "věci, které samy vydávají teplo",
        "level": "hard",
        "hidden": True,
        "inside": [
            "oheň", "kamna", "žehlička", "slunce", "svíčka", "radiátor",
            "motor", "pochodeň",
        ],
        "outside": [
            "deka", "svetr", "peřina", "termoska", "šála", "bunda", "spacák",
            "rukavice", "čepice", "ručník",
        ],
        "asks": [
            "samy vydávají teplo",
            "jsou to znamení zvěrokruhu",
            "čtou se stejně zepředu i zezadu",
            "jsou to zároveň příjmení českých prezidentů",
        ],
    },
    {
        "id": "v9-kvasi",
        "roof": "věci, které kvasí",
        "level": "normal",
        "hidden": True,
        "inside": [
            "pivo", "víno", "chleba", "zelí", "jogurt", "kvásek", "mošt",
            "kefír",
        ],
        "outside": [
            "mouka", "sůl", "olej", "voda", "čaj", "cukr", "rýže", "brambora",
            "ocet", "mýdlo",
        ],
        "asks": [
            "kvasí",
            "jsou to zároveň příjmení českých prezidentů",
            "jsou v názvech her Járy Cimrmana",
            "nemají v sobě ani jednu samohlásku",
        ],
    },
    {
        "id": "v9-kulate",
        "roof": "věci, které jsou vždycky kulaté",
        "level": "normal",
        "hidden": True,
        "inside": [
            "míč", "koule", "mince", "talíř", "kolo", "planeta", "bublina",
            "obruč",
        ],
        "outside": [
            "cihla", "kniha", "stůl", "dveře", "krabice", "žebřík", "plot",
            "deka", "sešit", "prkno",
        ],
        "asks": [
            "jsou vždycky kulaté",
            "mají v sobě dvě stejná písmena vedle sebe",
            "čtou se stejně zepředu i zezadu",
            "jsou v názvech večerníčků",
        ],
    },
    {
        "id": "v9-dira",
        "roof": "věci, které mají díru uprostřed",
        "level": "normal",
        "hidden": True,
        "inside": [
            "prsten", "matice", "kroužek", "koblih", "pneumatika", "obruč",
            "podložka", "disk",
        ],
        "outside": [
            "talíř", "mince", "cihla", "kniha", "deka", "míč", "sklenice",
            "klíč", "prkno", "mýdlo",
        ],
        "asks": [
            "mají díru uprostřed",
            "jsou to znamení zvěrokruhu",
            "jsou to zároveň značky nebo modely aut",
            "jsou to zároveň příjmení českých prezidentů",
        ],
    },
    {
        "id": "v9-ostre",
        "roof": "věci, které jsou ostré",
        "level": "normal",
        "hidden": True,
        "inside": [
            "nůž", "jehla", "sekera", "břitva", "hřebík", "střep", "dláto",
            "šipka",
        ],
        "outside": [
            "lžíce", "houba", "deka", "míč", "guma", "provaz", "polštář",
            "ručník", "kbelík", "mýdlo",
        ],
        "asks": [
            "jsou ostré",
            "čtou se stejně zepředu i zezadu",
            "mají v sobě dvě stejná písmena vedle sebe",
            "jsou to zároveň jména českých měst",
        ],
    },
    {
        "id": "v9-voda-potreba",
        "roof": "věci, které bez vody nefungují",
        "level": "normal",
        "hidden": True,
        "inside": [
            "pračka", "myčka", "sprcha", "akvárium", "fontána", "kotel",
            "mlýn", "vodárna",
        ],
        "outside": [
            "vysavač", "rádio", "lampa", "sekačka", "hodiny", "baterka",
            "větrák", "budík", "zvonek", "fén",
        ],
        "asks": [
            "bez vody nefungují",
            "nemají v sobě ani jednu samohlásku",
            "jsou v názvech Shakespearových her",
            "jsou to zároveň značky nebo modely aut",
        ],
    },
    {
        "id": "v9-nabobtna",
        "roof": "jídlo, které při vaření zvětší objem",
        "level": "normal",
        "hidden": True,
        "inside": [
            "rýže", "těstoviny", "fazole", "kroupy", "čočka", "kuskus",
            "hrách", "bulgur",
        ],
        "outside": [
            "maso", "brambora", "mrkev", "cibule", "vejce", "houby", "cuketa",
            "řepa", "dýně", "pórek",
        ],
        "asks": [
            "při vaření zvětší objem",
            "jsou to znamení zvěrokruhu",
            "mají v sobě dvě stejná písmena vedle sebe",
            "jsou to zároveň jména českých měst",
        ],
    },
    {
        "id": "v9-zkazi",
        "roof": "jídlo, které se zkazí",
        "level": "hard",
        "hidden": True,
        "inside": [
            "mléko", "maso", "chleba", "jogurt", "ryba", "salát", "smetana",
            "vejce",
        ],
        "outside": [
            "med", "sůl", "cukr", "rýže", "ocet", "líh", "mouka", "luštěniny",
            "čaj", "koření",
        ],
        "asks": [
            "se zkazí i v lednici",
            "jsou to zároveň příjmení českých prezidentů",
            "mají v sobě schované zvíře",
            "jsou v názvech her Járy Cimrmana",
        ],
    },
    {
        "id": "v9-stoupa",
        "roof": "věci, které samy stoupají vzhůru",
        "level": "normal",
        "hidden": True,
        "inside": [
            "kouř", "pára", "balón", "bublina", "jiskra", "dým", "hélium",
            "popel",
        ],
        "outside": [
            "kámen", "déšť", "kroupy", "mince", "kotva", "písek", "cihla",
            "sníh", "kapka", "žalud",
        ],
        "asks": [
            "samy stoupají vzhůru",
            "jsou v názvech večerníčků",
            "jsou to zároveň značky nebo modely aut",
            "jsou v názvech Shakespearových her",
        ],
    },
    {
        "id": "v9-slane",
        "roof": "věci, které jsou slané",
        "level": "normal",
        "hidden": True,
        "inside": [
            "moře", "slzy", "pot", "šunka", "olivy", "sardinka", "sýr",
            "slanina",
        ],
        "outside": [
            "déšť", "jezero", "mléko", "med", "čaj", "jablko", "mouka",
            "rýže", "cukr", "limonáda",
        ],
        "asks": [
            "jsou slané",
            "jsou v názvech Shakespearových her",
            "nemají v sobě ani jednu samohlásku",
            "jsou to zároveň jména českých měst",
        ],
    },
    {
        "id": "v9-letaji-bez-motoru",
        "roof": "věci, které létají bez motoru",
        "level": "normal",
        "hidden": True,
        "inside": [
            "drak", "kluzák", "balón", "pírko", "list", "semínko", "bumerang",
            "šíp",
        ],
        "outside": [
            "letadlo", "vrtulník", "dron", "raketa", "loď", "vlak", "autobus",
            "tramvaj", "kolo", "motorka",
        ],
        "asks": [
            "létají bez motoru",
            "jsou v názvech her Járy Cimrmana",
            "jsou to zároveň značky nebo modely aut",
            "jsou to znamení zvěrokruhu",
        ],
    },
    {
        "id": "v9-krehke-mraz",
        "roof": "věci, které v mrazu popraskají",
        "level": "hard",
        "hidden": True,
        "inside": [
            "láhev", "vodovod", "hadice", "květináč", "sud", "kanystr",
            "sklenice", "konev",
        ],
        "outside": [
            "kámen", "plech", "drát", "klíč", "kladivo", "řetěz", "šroub",
            "provaz", "guma", "hadr",
        ],
        "asks": [
            "v mrazu popraskají",
            "jsou to zároveň značky českého piva",
            "čtou se stejně zepředu i zezadu",
            "jsou to znamení zvěrokruhu",
        ],
    },
    {
        "id": "v9-zamknout",
        "roof": "věci, které se dají zamknout na klíč",
        "level": "normal",
        "hidden": True,
        "inside": [
            "dveře", "auto", "kolo", "trezor", "kufr", "skříňka", "brána",
            "zámek",
        ],
        "outside": [
            "okno", "stůl", "police", "žebřík", "koberec", "lampa", "deka",
            "talíř", "sešit", "hrnec",
        ],
        "asks": [
            "se dají zamknout na klíč",
            "mají v sobě schované zvíře",
            "jsou to zároveň značky nebo modely aut",
            "jsou v názvech večerníčků",
        ],
    },
    {
        "id": "v9-lekarnicka",
        "roof": "věci, které musí být v autolékárničce",
        "level": "normal",
        "hidden": True,
        "inside": [
            "obinadlo", "náplast", "rouška", "rukavice", "nůžky", "šátek",
            "obvaz", "špendlík",
        ],
        "outside": [
            "vesta", "trojúhelník", "lopata", "kanystr", "lano", "vozík",
            "plachta", "klíč", "pumpa", "zvedák",
        ],
        "asks": [
            "musí být v autolékárničce",
            "jsou to zároveň jména českých měst",
            "čtou se stejně zepředu i zezadu",
            "jsou v názvech her Járy Cimrmana",
        ],
    },
    {
        "id": "v9-morava",
        "roof": "města, která leží na Moravě",
        "level": "normal",
        "hidden": True,
        "inside": [
            "Brno", "Olomouc", "Zlín", "Přerov", "Znojmo", "Kroměříž",
            "Vyškov", "Prostějov",
        ],
        "outside": [
            "Plzeň", "Liberec", "Kladno", "Beroun", "Tábor", "Písek", "Jičín",
            "Cheb", "Louny", "Mělník",
        ],
        "asks": [
            "leží na Moravě",
            "jsou to zároveň značky českého piva",
            "jsou v názvech Shakespearových her",
            "jsou to zároveň příjmení českých prezidentů",
        ],
    },
    {
        "id": "v9-krajska",
        "roof": "krajská města",
        "level": "normal",
        "hidden": True,
        "inside": [
            "Jihlava", "Zlín", "Pardubice", "Liberec", "Olomouc", "Brno",
            "Plzeň", "Ostrava",
        ],
        "outside": [
            "Kolín", "Tábor", "Kroměříž", "Písek", "Jičín", "Beroun", "Louny",
            "Přerov", "Mělník", "Vyškov",
        ],
        "asks": [
            "jsou to krajská města",
            "jsou v názvech Shakespearových her",
            "mají v sobě schované zvíře",
            "jsou to zároveň jména českých měst",
        ],
    },
    {
        "id": "v9-rakousko-uhersko",
        "roof": "země, které byly v Rakousku-Uhersku",
        "level": "hard",
        "hidden": True,
        "inside": [
            "Maďarsko", "Slovensko", "Chorvatsko", "Slovinsko", "Rakousko",
            "Bosna",
        ],
        "outside": [
            "Německo", "Rusko", "Švédsko", "Řecko", "Francie", "Španělsko",
            "Dánsko", "Norsko", "Belgie", "Portugalsko",
        ],
        "asks": [
            "patřily do Rakouska-Uherska",
            "jsou to znamení zvěrokruhu",
            "jsou to zároveň značky českého piva",
            "jsou v názvech Shakespearových her",
        ],
    },
    {
        "id": "v9-unesco",
        "roof": "česká města na seznamu UNESCO",
        "level": "hard",
        "hidden": True,
        "inside": [
            "Telč", "Litomyšl", "Kroměříž", "Holašovice", "Lednice", "Třebíč",
            "Žďár", "Kladruby",
        ],
        "outside": [
            "Tábor", "Beroun", "Kolín", "Písek", "Jičín", "Louny", "Mělník",
            "Vyškov", "Rakovník", "Nymburk",
        ],
        "asks": [
            "jsou na seznamu UNESCO",
            "jsou to znamení zvěrokruhu",
            "jsou v názvech her Járy Cimrmana",
            "jsou v názvech Shakespearových her",
        ],
    },
    {
        "id": "v9-nepravidelne",
        "roof": "slova s nepravidelným množným číslem",
        "level": "hard",
        "hidden": True,
        "inside": [
            "dítě", "oko", "ucho", "ruka", "člověk", "kůň", "noha", "přítel",
        ],
        "outside": [
            "stůl", "okno", "kniha", "lampa", "židle", "talíř", "klíč", "koš",
            "hrnec", "police",
        ],
        "asks": [
            "mají nepravidelné množné číslo",
            "jsou v názvech večerníčků",
            "jsou to znamení zvěrokruhu",
            "nemají v sobě ani jednu samohlásku",
        ],
    },
    {
        "id": "v9-presmycka",
        "roof": "slova, ze kterých se přeskládáním písmen stane jiné slovo",
        "level": "hard",
        "hidden": True,
        "inside": [
            "kos", "lom", "rak", "vlas", "kapr", "brus", "lak", "krb", "role",
        ],
        "outside": [
            "hrnec", "police", "koště", "žebřík", "kastrol", "kbelík",
            "ubrus", "deštník", "koberec", "sešit",
        ],
        "asks": [
            "se dají přeskládat na jiné slovo",
            "jsou v názvech her Járy Cimrmana",
            "mají v sobě schované zvíře",
            "jsou to zároveň příjmení českých prezidentů",
        ],
    },
    {
        "id": "v9-rym-ice",
        "roof": "slova, která se rýmují se slovem police",
        "level": "normal",
        "hidden": True,
        "inside": [
            "ulice", "silnice", "sklenice", "hranice", "lavice", "vidlice",
            "nemocnice", "čepice",
        ],
        "outside": [
            "koberec", "žebřík", "hrnec", "deštník", "polštář", "kastrol",
            "pekáč", "trakař", "podnos", "batoh",
        ],
        "asks": [
            "se rýmují se slovem police",
            "jsou to zároveň značky českého piva",
            "jsou to znamení zvěrokruhu",
            "nemají v sobě ani jednu samohlásku",
        ],
    },
    {
        "id": "v9-rym-ina",
        "roof": "slova, která se rýmují se slovem hodina",
        "level": "normal",
        "hidden": True,
        "inside": [
            "rodina", "novina", "bublina", "lavina", "dřevina", "slanina",
            "rostlina", "mýtina",
        ],
        "outside": [
            "koberec", "žebřík", "hrnec", "deštník", "polštář", "kastrol",
            "pekáč", "trakař", "podnos", "batoh",
        ],
        "asks": [
            "se rýmují se slovem hodina",
            "čtou se stejně zepředu i zezadu",
            "nemají v sobě ani jednu samohlásku",
            "jsou v názvech Shakespearových her",
        ],
    },
    {
        "id": "v9-bily",
        "roof": "slova, která tvoří dvojici se slovem bílý",
        "level": "hard",
        "hidden": True,
        "inside": [
            "vrána", "maso", "místa", "paní", "sobota", "šum", "kůň",
            "prapor",
        ],
        "outside": [
            "police", "koberec", "žebřík", "mrkev", "talíř", "kbelík",
            "hrnec", "lampa", "sešit", "deštník",
        ],
        "asks": [
            "tvoří se slovem bílý ustálené spojení",
            "mají v sobě dvě stejná písmena vedle sebe",
            "jsou to zároveň jména českých měst",
            "jsou to znamení zvěrokruhu",
        ],
    },
    {
        "id": "v9-suchy",
        "roof": "slova, která tvoří dvojici se slovem suchý",
        "level": "hard",
        "hidden": True,
        "inside": [
            "zip", "led", "humor", "období", "nit", "chleba", "stéblo",
        ],
        "outside": [
            "police", "koberec", "žebřík", "mrkev", "talíř", "kbelík",
            "hrnec", "lampa", "sešit", "deštník",
        ],
        "asks": [
            "tvoří se slovem suchý ustálené spojení",
            "jsou to zároveň příjmení českých prezidentů",
            "jsou v názvech večerníčků",
            "mají v sobě schované zvíře",
        ],
    },
    {
        "id": "v9-hluboky",
        "roof": "slova, která tvoří dvojici se slovem hluboký",
        "level": "normal",
        "hidden": True,
        "inside": [
            "talíř", "spánek", "dojem", "mráz", "voda", "les", "úklona",
            "myšlenka",
        ],
        "outside": [
            "police", "koberec", "žebřík", "mrkev", "kbelík", "hrnec",
            "lampa", "sešit", "deštník",
        ],
        "asks": [
            "tvoří se slovem hluboký ustálené spojení",
            "jsou to znamení zvěrokruhu",
            "jsou v názvech her Járy Cimrmana",
            "jsou v názvech Shakespearových her",
        ],
    },
    {
        "id": "v9-ostry",
        "roof": "slova, která tvoří dvojici se slovem ostrý",
        "level": "normal",
        "hidden": True,
        "inside": [
            "nůž", "jazyk", "zatáčka", "střelba", "sýr", "úhel", "zrak",
            "slovo",
        ],
        "outside": [
            "police", "koberec", "žebřík", "mrkev", "kbelík", "hrnec",
            "lampa", "sešit", "deštník", "ubrus",
        ],
        "asks": [
            "tvoří se slovem ostrý ustálené spojení",
            "nemají v sobě ani jednu samohlásku",
            "mají v sobě dvě stejná písmena vedle sebe",
            "čtou se stejně zepředu i zezadu",
        ],
    },
    {
        "id": "v9-tichy",
        "roof": "slova, která tvoří dvojici se slovem tichý",
        "level": "hard",
        "hidden": True,
        "inside": [
            "pošta", "souhlas", "domácnost", "společník", "voda", "oceán",
            "modlitba", "noc",
        ],
        "outside": [
            "police", "koberec", "žebřík", "mrkev", "kbelík", "hrnec",
            "lampa", "sešit", "deštník", "ubrus",
        ],
        "asks": [
            "tvoří se slovem tichý ustálené spojení",
            "jsou to zároveň jména českých měst",
            "nemají v sobě ani jednu samohlásku",
            "mají v sobě dvě stejná písmena vedle sebe",
        ],
    },
    {
        "id": "v9-dlouhy",
        "roof": "slova, která tvoří dvojici se slovem dlouhý",
        "level": "normal",
        "hidden": True,
        "inside": [
            "vedení", "prsty", "chvíle", "nos", "vlna", "cesta", "doba",
            "čekání",
        ],
        "outside": [
            "police", "koberec", "žebřík", "mrkev", "kbelík", "hrnec",
            "lampa", "sešit", "deštník", "ubrus",
        ],
        "asks": [
            "tvoří se slovem dlouhý ustálené spojení",
            "jsou v názvech her Járy Cimrmana",
            "jsou to znamení zvěrokruhu",
            "jsou to zároveň jména českých měst",
        ],
    },
    {
        "id": "v9-hory",
        "roof": "slova, která jsou zároveň části hory",
        "level": "hard",
        "hidden": True,
        "inside": [
            "sedlo", "hřeben", "štít", "úpatí", "kotlina", "sráz", "převis",
            "rokle",
        ],
        "outside": [
            "bašta", "depozitář", "fronta", "inzerát", "legenda", "ležák",
            "sazba", "smyčka", "tempo", "výkon", "záhon", "četa",
        ],
        "asks": [
            "jsou to zároveň části hory",
            "jsou to zároveň značky českého piva",
            "jsou v názvech her Járy Cimrmana",
            "mají v sobě dvě stejná písmena vedle sebe",
        ],
    },
    {
        "id": "v9-film",
        "roof": "slova, která jsou zároveň filmařské pojmy",
        "level": "normal",
        "hidden": True,
        "inside": [
            "klapka", "štáb", "záběr", "střih", "scéna", "role", "kaskadér",
            "dabing",
        ],
        "outside": [
            "buňka", "glosa", "kóta", "měřítko", "oštěp", "pořad", "prvek",
            "práce", "roztok", "sloupek", "točení", "výřad",
        ],
        "asks": [
            "jsou to zároveň filmařské pojmy",
            "jsou v názvech Shakespearových her",
            "jsou to znamení zvěrokruhu",
            "čtou se stejně zepředu i zezadu",
        ],
    },
    {
        "id": "v9-foto",
        "roof": "slova, která jsou zároveň fotografické pojmy",
        "level": "hard",
        "hidden": True,
        "inside": [
            "clona", "závěrka", "ostření", "expozice", "hloubka", "stativ",
            "objektiv", "blesk",
        ],
        "outside": [
            "kóta", "mýtina", "pomoučení", "převis", "přádelna", "rubrika",
            "sklizeň", "stav", "střídačka", "závrt", "úpatí", "útek",
        ],
        "asks": [
            "jsou to zároveň fotografické pojmy",
            "jsou v názvech večerníčků",
            "jsou to zároveň značky českého piva",
            "jsou v názvech her Járy Cimrmana",
        ],
    },
    {
        "id": "v9-pravo",
        "roof": "slova, která jsou zároveň právnické pojmy",
        "level": "hard",
        "hidden": True,
        "inside": [
            "žaloba", "odvolání", "spis", "líčení", "senát", "výrok", "důkaz",
            "obhajoba",
        ],
        "outside": [
            "ciferník", "cimbuří", "korunka", "kruhy", "kóta", "oběť",
            "polom", "program", "regál", "sraženina", "vzorek", "várka",
        ],
        "asks": [
            "jsou to zároveň právnické pojmy",
            "mají v sobě dvě stejná písmena vedle sebe",
            "jsou to zároveň značky nebo modely aut",
            "nemají v sobě ani jednu samohlásku",
        ],
    },
    {
        "id": "v9-telocvik",
        "roof": "slova, která jsou zároveň tělocvičné nářadí",
        "level": "normal",
        "hidden": True,
        "inside": [
            "hrazda", "kruhy", "koza", "kladina", "bradla", "švihadlo",
            "žíněnka", "lavička",
        ],
        "outside": [
            "hmotnost", "objektiv", "ponor", "přesilovka", "převis",
            "signatura", "skleník", "sloučenina", "spis", "titulek", "uzda",
            "zkumavka",
        ],
        "asks": [
            "jsou to zároveň tělocvičné nářadí",
            "čtou se stejně zepředu i zezadu",
            "jsou to zároveň jména českých měst",
            "jsou to zároveň příjmení českých prezidentů",
        ],
    },
    {
        "id": "v9-fyzika",
        "roof": "slova, která jsou zároveň fyzikální veličiny",
        "level": "hard",
        "hidden": True,
        "inside": [
            "síla", "práce", "výkon", "tlak", "moment", "dráha", "tíha",
            "hmotnost",
        ],
        "outside": [
            "cimbuří", "hnětení", "hokejka", "kaskadér", "legenda",
            "signatura", "zkumavka", "záď", "úpatí", "člunek", "štáb", "štít",
        ],
        "asks": [
            "jsou to zároveň fyzikální veličiny",
            "jsou to znamení zvěrokruhu",
            "mají v sobě schované zvíře",
            "jsou v názvech Shakespearových her",
        ],
    },
    {
        "id": "v9-matematika",
        "roof": "slova, která jsou zároveň matematické pojmy",
        "level": "normal",
        "hidden": True,
        "inside": [
            "mocnina", "odmocnina", "zlomek", "kořen", "osa", "úhel", "obsah",
            "rovnice",
        ],
        "outside": [
            "dabing", "hřeben", "hříva", "návěstidlo", "program", "převod",
            "rota", "střídačka", "tkanina", "vidlička", "vinice", "závaží",
        ],
        "asks": [
            "jsou to zároveň matematické pojmy",
            "jsou v názvech Shakespearových her",
            "jsou to zároveň značky českého piva",
            "čtou se stejně zepředu i zezadu",
        ],
    },
    {
        "id": "v9-kadernictvi",
        "roof": "slova, která jsou zároveň účesy a kadeřnické pojmy",
        "level": "normal",
        "hidden": True,
        "inside": [
            "mikádo", "ofina", "culík", "drdol", "patka", "melír", "pěšinka",
            "trvalá",
        ],
        "outside": [
            "kvasnice", "lavička", "pařeniště", "pařez", "pletivo",
            "podvozek", "posed", "puk", "sklep", "vázání", "výpůjčka",
            "záhon",
        ],
        "asks": [
            "jsou to zároveň účesy nebo kadeřnické pojmy",
            "jsou v názvech večerníčků",
            "jsou to zároveň značky nebo modely aut",
            "jsou to zároveň jména českých měst",
        ],
    },
    {
        "id": "v9-myslivost",
        "roof": "slova, která jsou zároveň myslivecké pojmy",
        "level": "hard",
        "hidden": True,
        "inside": [
            "posed", "obora", "hon", "výřad", "šoulačka", "čekaná", "krmelec",
            "troubení",
        ],
        "outside": [
            "artista", "hlína", "kolejnice", "listonoš", "manéž", "oštěp",
            "sloučenina", "smyčka", "uzavírání", "vztlak", "výrok", "závora",
        ],
        "asks": [
            "jsou to zároveň myslivecké pojmy",
            "jsou to zároveň značky nebo modely aut",
            "čtou se stejně zepředu i zezadu",
            "jsou v názvech her Járy Cimrmana",
        ],
    },
    {
        "id": "v9-lode",
        "roof": "slova, která jsou zároveň části lodi",
        "level": "hard",
        "hidden": True,
        "inside": [
            "paluba", "kýl", "příď", "záď", "kotva", "plachta", "stěžeň",
            "kajuta",
        ],
        "outside": [
            "clona", "kahan", "kaskadér", "klubko", "ležení", "objektiv",
            "ohlávka", "pletivo", "přenos", "rubrika", "trup", "šapitó",
        ],
        "asks": [
            "jsou to zároveň části lodi",
            "jsou to zároveň jména českých měst",
            "jsou v názvech večerníčků",
            "jsou to zároveň příjmení českých prezidentů",
        ],
    },
    {
        "id": "v9-letadlo",
        "roof": "slova, která jsou zároveň části letadla",
        "level": "normal",
        "hidden": True,
        "inside": [
            "křídlo", "klapka", "trup", "podvozek", "ocas", "kokpit",
            "vztlak", "směrovka",
        ],
        "outside": [
            "hladomorna", "hlídka", "kotva", "mat", "mladina", "obsah",
            "paseka", "sedák", "tkanina", "totem", "útek", "šapitó",
        ],
        "asks": [
            "jsou to zároveň části letadla",
            "mají v sobě schované zvíře",
            "jsou to zároveň jména českých měst",
            "jsou v názvech her Járy Cimrmana",
        ],
    },
    {
        "id": "v9-vlak",
        "roof": "slova, která jsou zároveň železniční pojmy",
        "level": "normal",
        "hidden": True,
        "inside": [
            "výhybka", "závora", "nástupiště", "návěstidlo", "posun", "vagon",
            "lokomotiva", "kolejnice",
        ],
        "outside": [
            "dráha", "kynutí", "obora", "podvozek", "pořad", "příkop",
            "splátka", "sraženina", "titulek", "zásada", "člunek", "šapitó",
        ],
        "asks": [
            "jsou to zároveň železniční pojmy",
            "mají v sobě schované zvíře",
            "nemají v sobě ani jednu samohlásku",
            "jsou to zároveň jména českých měst",
        ],
    },
    {
        "id": "v9-skola",
        "roof": "slova, která jsou zároveň pojmy ze školy",
        "level": "normal",
        "hidden": True,
        "inside": [
            "třída", "družina", "ředitelna", "sborovna", "zvonek", "žákovská",
            "tabule", "přestávka",
        ],
        "outside": [
            "hrnec", "koště", "plot", "kabát", "lampa", "konev", "ručník",
            "kýbl", "polštář", "koberec",
        ],
        "asks": [
            "jsou to zároveň pojmy ze školy",
            "mají v sobě dvě stejná písmena vedle sebe",
            "mají v sobě schované zvíře",
            "jsou v názvech Shakespearových her",
        ],
    },
    {
        "id": "v9-pivovar",
        "roof": "slova, která jsou zároveň pivovarské pojmy",
        "level": "hard",
        "hidden": True,
        "inside": [
            "várka", "chmel", "mladina", "spilka", "ležák", "sladovna",
            "kvasnice", "humna",
        ],
        "outside": [
            "azimut", "bradla", "drezura", "dráha", "inzerát", "kurýr",
            "legenda", "nádvoří", "plachta", "poplach", "vlek", "záhon",
        ],
        "asks": [
            "jsou to zároveň pivovarské pojmy",
            "jsou v názvech her Járy Cimrmana",
            "mají v sobě dvě stejná písmena vedle sebe",
            "mají v sobě schované zvíře",
        ],
    },
    {
        "id": "v9-jeskyne",
        "roof": "slova, která jsou zároveň části jeskyně",
        "level": "hard",
        "hidden": True,
        "inside": [
            "krápník", "dóm", "komín", "sifon", "propast", "síň", "závrt",
            "ponor",
        ],
        "outside": [
            "brankoviště", "burčák", "hnětení", "hůlky", "listonoš", "orgán",
            "převis", "uzavírání", "vrstevnice", "výtrus", "člunek", "žaloba",
        ],
        "asks": [
            "jsou to zároveň části jeskyně",
            "jsou v názvech večerníčků",
            "mají v sobě schované zvíře",
            "jsou v názvech Shakespearových her",
        ],
    },
    {
        "id": "v9-hrad",
        "roof": "slova, která jsou zároveň části hradu",
        "level": "normal",
        "hidden": True,
        "inside": [
            "val", "příkop", "brána", "hladomorna", "palác", "nádvoří",
            "cimbuří", "bašta",
        ],
        "outside": [
            "klubko", "kóta", "osa", "otěže", "plachta", "poplatek", "spilka",
            "točení", "výtrus", "znělka", "úpatí", "útek",
        ],
        "asks": [
            "jsou to zároveň části hradu",
            "jsou to zároveň značky nebo modely aut",
            "nemají v sobě ani jednu samohlásku",
            "čtou se stejně zepředu i zezadu",
        ],
    },
    {
        "id": "v9-noviny",
        "roof": "slova, která jsou zároveň novinářské pojmy",
        "level": "hard",
        "hidden": True,
        "inside": [
            "titulek", "sloupek", "rubrika", "inzerát", "redakce", "uzávěrka",
            "glosa", "sazba",
        ],
        "outside": [
            "ciferník", "drdol", "kajuta", "komín", "kyselina", "mýtina",
            "odběr", "pletivo", "propast", "střídačka", "zásada", "šoulačka",
        ],
        "asks": [
            "jsou to zároveň novinářské pojmy",
            "jsou to znamení zvěrokruhu",
            "jsou v názvech večerníčků",
            "jsou to zároveň příjmení českých prezidentů",
        ],
    },
    {
        "id": "v9-mapa",
        "roof": "slova, která jsou zároveň pojmy z mapy",
        "level": "hard",
        "hidden": True,
        "inside": [
            "měřítko", "legenda", "vrstevnice", "azimut", "poledník",
            "rovnoběžka", "kóta", "růžice",
        ],
        "outside": [
            "burčák", "expozice", "fronta", "kasárna", "mošt", "oko",
            "program", "spoření", "srážky", "studio", "vzorek", "švihadlo",
        ],
        "asks": [
            "jsou to zároveň pojmy z mapy",
            "jsou to znamení zvěrokruhu",
            "nemají v sobě ani jednu samohlásku",
            "jsou v názvech her Járy Cimrmana",
        ],
    },
    {
        "id": "v9-cirkus",
        "roof": "slova, která jsou zároveň cirkusové pojmy",
        "level": "normal",
        "hidden": True,
        "inside": [
            "manéž", "šapitó", "artista", "drezura", "klaun", "provazochodec",
            "krotitel", "žonglér",
        ],
        "outside": [
            "dráha", "dóm", "kasárna", "kladina", "kokpit", "poštovné",
            "přesilovka", "sklep", "snímek", "stěr", "titulek", "vinice",
        ],
        "asks": [
            "jsou to zároveň cirkusové pojmy",
            "jsou v názvech Shakespearových her",
            "nemají v sobě ani jednu samohlásku",
            "jsou to zároveň příjmení českých prezidentů",
        ],
    },
    {
        "id": "v9-zahrada",
        "roof": "slova, která jsou zároveň zahradnické pojmy",
        "level": "normal",
        "hidden": True,
        "inside": [
            "záhon", "skleník", "pařeniště", "roubování", "sazenice",
            "postřik", "okopávka", "řízek",
        ],
        "outside": [
            "hrnec", "koště", "kabát", "lampa", "ručník", "kýbl", "polštář",
            "sešit", "talíř", "kastrol",
        ],
        "asks": [
            "jsou to zároveň zahradnické pojmy",
            "jsou to zároveň značky nebo modely aut",
            "jsou to zároveň příjmení českých prezidentů",
            "nemají v sobě ani jednu samohlásku",
        ],
    },
    {
        "id": "v9-horolezectvi",
        "roof": "slova, která jsou zároveň horolezecké vybavení",
        "level": "hard",
        "hidden": True,
        "inside": [
            "sedák", "karabina", "skoba", "lano", "cepín", "mačky",
            "jistítko", "smyčka",
        ],
        "outside": [
            "bašta", "hlína", "lis", "mikádo", "ohlávka", "osnova", "paseka",
            "střída", "tempo", "vagon", "četa", "štáb",
        ],
        "asks": [
            "jsou to zároveň horolezecké vybavení",
            "mají v sobě schované zvíře",
            "čtou se stejně zepředu i zezadu",
            "jsou to zároveň příjmení českých prezidentů",
        ],
    },
    {
        "id": "v9-les",
        "roof": "slova, která jsou zároveň lesnické pojmy",
        "level": "hard",
        "hidden": True,
        "inside": [
            "paseka", "mýtina", "remízek", "houština", "polom", "průsek",
            "pařez", "školka",
        ],
        "outside": [
            "dráha", "hon", "inverze", "klubko", "mocnina", "práce", "rošáda",
            "ručička", "stav", "vázání", "výhybka", "štafeta",
        ],
        "asks": [
            "jsou to zároveň lesnické pojmy",
            "jsou v názvech her Járy Cimrmana",
            "jsou v názvech Shakespearových her",
            "jsou to zároveň značky českého piva",
        ],
    },
    {
        "id": "v9-tkani",
        "roof": "slova, která jsou zároveň tkalcovské pojmy",
        "level": "hard",
        "hidden": True,
        "inside": [
            "osnova", "útek", "stav", "cívka", "člunek", "přádelna", "příze",
            "tkanina",
        ],
        "outside": [
            "celta", "kotva", "manéž", "melír", "poplach", "sborovna",
            "sloučenina", "strojek", "tabule", "totem", "vrstevnice",
            "výhybka",
        ],
        "asks": [
            "jsou to zároveň tkalcovské pojmy",
            "jsou to zároveň jména českých měst",
            "mají v sobě dvě stejná písmena vedle sebe",
            "jsou v názvech večerníčků",
        ],
    },
    {
        "id": "v9-hrncirstvi",
        "roof": "slova, která jsou zároveň hrnčířské pojmy",
        "level": "normal",
        "hidden": True,
        "inside": [
            "kruh", "glazura", "pec", "střep", "hlína", "výpal", "točení",
            "engoba",
        ],
        "outside": [
            "blesk", "drdol", "drezura", "nález", "návěstidlo", "patka",
            "ponor", "přesilovka", "skleník", "tempo", "těsto", "vztlak",
        ],
        "asks": [
            "jsou to zároveň hrnčířské pojmy",
            "čtou se stejně zepředu i zezadu",
            "jsou v názvech večerníčků",
            "jsou v názvech Shakespearových her",
        ],
    },
    {
        "id": "v9-kone",
        "roof": "slova, která jsou zároveň části koně a postroje",
        "level": "normal",
        "hidden": True,
        "inside": [
            "hříva", "ohlávka", "třmen", "sedlo", "podkova", "uzda", "kopyto",
            "otěže",
        ],
        "outside": [
            "dálka", "kokpit", "křídlo", "lano", "legenda", "manéž", "posun",
            "pěšinka", "přenos", "sráz", "titulky", "řízek",
        ],
        "asks": [
            "jsou to zároveň části koně nebo postroje",
            "jsou v názvech her Járy Cimrmana",
            "mají v sobě schované zvíře",
            "jsou to zároveň příjmení českých prezidentů",
        ],
    },
    {
        "id": "v9-lekarstvi",
        "roof": "slova, která jsou zároveň lékařské pojmy",
        "level": "hard",
        "hidden": True,
        "inside": [
            "odběr", "stěr", "snímek", "nález", "recept", "ambulance",
            "převaz", "injekce",
        ],
        "outside": [
            "brána", "ešus", "kotlík", "kyvadlo", "mýtina", "patka",
            "podvozek", "převod", "reklama", "sifon", "vyloučení", "čekaná",
        ],
        "asks": [
            "jsou to zároveň lékařské pojmy",
            "jsou to zároveň příjmení českých prezidentů",
            "jsou v názvech večerníčků",
            "mají v sobě schované zvíře",
        ],
    },
    {
        "id": "v9-banka",
        "roof": "slova, která jsou zároveň bankovní pojmy",
        "level": "hard",
        "hidden": True,
        "inside": [
            "úrok", "splátka", "jistina", "výpis", "převod", "hypotéka",
            "spoření", "poplatek",
        ],
        "outside": [
            "azimut", "dělení", "kajuta", "oblouk", "ohniště", "okopávka",
            "pletivo", "postřik", "průsek", "přestávka", "titulky", "žonglér",
        ],
        "asks": [
            "jsou to zároveň bankovní pojmy",
            "jsou v názvech večerníčků",
            "jsou to zároveň značky českého piva",
            "mají v sobě dvě stejná písmena vedle sebe",
        ],
    },
    {
        "id": "v9-posta",
        "roof": "slova, která jsou zároveň poštovní pojmy",
        "level": "normal",
        "hidden": True,
        "inside": [
            "dobírka", "zásilka", "razítko", "poštovné", "listonoš", "kurýr",
            "známka", "balík",
        ],
        "outside": [
            "celta", "objektiv", "oblouk", "odvolání", "oko", "orgán",
            "propast", "spis", "stěžeň", "závaží", "závrt", "úrok",
        ],
        "asks": [
            "jsou to zároveň poštovní pojmy",
            "jsou to zároveň jména českých měst",
            "mají v sobě schované zvíře",
            "jsou to znamení zvěrokruhu",
        ],
    },
    {
        "id": "v9-pocasi-pojmy",
        "roof": "slova, která jsou zároveň meteorologické pojmy",
        "level": "hard",
        "hidden": True,
        "inside": [
            "fronta", "inverze", "srážky", "níže", "výše", "oblačnost",
            "bouřka", "přeháňka",
        ],
        "outside": [
            "cepín", "hypotéka", "kladina", "kotva", "mocnina", "ohniště",
            "oko", "sifon", "smyčka", "tkáň", "tlak", "šoulačka",
        ],
        "asks": [
            "jsou to zároveň meteorologické pojmy",
            "jsou v názvech Shakespearových her",
            "nemají v sobě ani jednu samohlásku",
            "jsou v názvech večerníčků",
        ],
    },
    {
        "id": "v9-chemie",
        "roof": "slova, která jsou zároveň chemické pojmy",
        "level": "normal",
        "hidden": True,
        "inside": [
            "roztok", "sraženina", "kyselina", "zásada", "prvek",
            "sloučenina", "zkumavka", "kahan",
        ],
        "outside": [
            "ciferník", "disk", "engoba", "klaun", "lýko", "mladina", "mošt",
            "patka", "rovnice", "útek", "řízek", "švihadlo",
        ],
        "asks": [
            "jsou to zároveň chemické pojmy",
            "jsou v názvech her Járy Cimrmana",
            "nemají v sobě ani jednu samohlásku",
            "jsou to znamení zvěrokruhu",
        ],
    },
    {
        "id": "v9-biologie",
        "roof": "slova, která jsou zároveň biologické pojmy",
        "level": "hard",
        "hidden": True,
        "inside": [
            "buňka", "tkáň", "orgán", "jádro", "dělení", "výtrus", "pletivo",
            "lýko",
        ],
        "outside": [
            "fond", "jehlice", "kajuta", "kolejnice", "okopávka", "ostření",
            "propast", "razítko", "recept", "signatura", "výkon", "štít",
        ],
        "asks": [
            "jsou to zároveň biologické pojmy",
            "nemají v sobě ani jednu samohlásku",
            "jsou to zároveň jména českých měst",
            "jsou v názvech večerníčků",
        ],
    },
    {
        "id": "v9-armada",
        "roof": "slova, která jsou zároveň vojenské pojmy",
        "level": "normal",
        "hidden": True,
        "inside": [
            "rota", "četa", "hlídka", "průzkum", "ležení", "poplach",
            "prapor", "kasárna",
        ],
        "outside": [
            "depozitář", "inverze", "kladina", "kladivo", "krápník",
            "listonoš", "patka", "prvek", "spis", "střep", "tlak", "řada",
        ],
        "asks": [
            "jsou to zároveň vojenské pojmy",
            "čtou se stejně zepředu i zezadu",
            "jsou to znamení zvěrokruhu",
            "jsou to zároveň značky nebo modely aut",
        ],
    },
    {
        "id": "v9-knihovna",
        "roof": "slova, která jsou zároveň knihovnické pojmy",
        "level": "hard",
        "hidden": True,
        "inside": [
            "signatura", "výpůjčka", "katalog", "fond", "depozitář",
            "rešerše", "regál", "čtenář",
        ],
        "outside": [
            "dobírka", "krmelec", "ležák", "mocnina", "oblačnost", "pěšinka",
            "sráz", "střep", "tabule", "tkanina", "totem", "val",
        ],
        "asks": [
            "jsou to zároveň knihovnické pojmy",
            "jsou v názvech večerníčků",
            "jsou to zároveň příjmení českých prezidentů",
            "mají v sobě schované zvíře",
        ],
    },
    {
        "id": "v9-sachy",
        "roof": "slova, která jsou zároveň šachové pojmy",
        "level": "normal",
        "hidden": True,
        "inside": [
            "rošáda", "mat", "pat", "oběť", "vidlička", "tempo", "koncovka",
            "zahájení",
        ],
        "outside": [
            "kasárna", "krápník", "oblačnost", "ohniště", "otěže", "převod",
            "réva", "vrstevnice", "záběr", "záhon", "ředitelna", "šapitó",
        ],
        "asks": [
            "jsou to zároveň šachové pojmy",
            "jsou to znamení zvěrokruhu",
            "jsou to zároveň značky nebo modely aut",
            "čtou se stejně zepředu i zezadu",
        ],
    },
    {
        "id": "v9-hokej-pojmy",
        "roof": "slova, která jsou zároveň hokejové pojmy",
        "level": "normal",
        "hidden": True,
        "inside": [
            "buly", "přesilovka", "vyloučení", "nájezd", "brankoviště",
            "střídačka", "hokejka", "puk",
        ],
        "outside": [
            "kaskadér", "kolejnice", "kůrka", "nepokoj", "oko", "okopávka",
            "posed", "ručička", "síla", "vidlička", "výtrus", "žákovská",
        ],
        "asks": [
            "jsou to zároveň hokejové pojmy",
            "mají v sobě schované zvíře",
            "jsou to zároveň značky nebo modely aut",
            "nemají v sobě ani jednu samohlásku",
        ],
    },
    {
        "id": "v9-atletika",
        "roof": "slova, která jsou zároveň atletické disciplíny a náčiní",
        "level": "normal",
        "hidden": True,
        "inside": [
            "štafeta", "koule", "oštěp", "disk", "kladivo", "překážky",
            "dálka", "výška",
        ],
        "outside": [
            "glazura", "kasárna", "kruh", "legenda", "mladina", "měřítko",
            "objektiv", "postřik", "ručička", "sklizeň", "tkáň", "val",
        ],
        "asks": [
            "jsou to zároveň atletické disciplíny nebo náčiní",
            "jsou to zároveň příjmení českých prezidentů",
            "jsou v názvech večerníčků",
            "mají v sobě dvě stejná písmena vedle sebe",
        ],
    },
    {
        "id": "v9-lyze",
        "roof": "slova, která jsou zároveň lyžařské pojmy",
        "level": "normal",
        "hidden": True,
        "inside": [
            "vlek", "sjezdovka", "oblouk", "hrana", "stopa", "skluznice",
            "hůlky", "vázání",
        ],
        "outside": [
            "bašta", "hypotéka", "inverze", "koule", "ofina", "oštěp",
            "provazochodec", "práce", "razítko", "strojek", "závrt",
            "štafeta",
        ],
        "asks": [
            "jsou to zároveň lyžařské pojmy",
            "jsou to zároveň jména českých měst",
            "jsou v názvech her Járy Cimrmana",
            "mají v sobě dvě stejná písmena vedle sebe",
        ],
    },
    {
        "id": "v9-hodinarstvi",
        "roof": "slova, která jsou zároveň části hodin",
        "level": "hard",
        "hidden": True,
        "inside": [
            "setrvačka", "ciferník", "ručička", "korunka", "kyvadlo",
            "závaží", "strojek", "nepokoj",
        ],
        "outside": [
            "fond", "hladomorna", "mat", "odmocnina", "poledník", "přádelna",
            "příď", "reklama", "sborovna", "střep", "zlomek", "řízek",
        ],
        "asks": [
            "jsou to zároveň části hodin",
            "jsou v názvech večerníčků",
            "jsou to zároveň značky nebo modely aut",
            "jsou v názvech her Járy Cimrmana",
        ],
    },
    {
        "id": "v9-pleteni",
        "roof": "slova, která jsou zároveň pojmy z pletení",
        "level": "normal",
        "hidden": True,
        "inside": [
            "oko", "řada", "jehlice", "klubko", "příze", "vzorek", "nabírání",
            "uzavírání",
        ],
        "outside": [
            "brána", "lýko", "otěže", "pletivo", "postřik", "prvek",
            "přádelna", "rošáda", "snímek", "srážky", "vinice", "šapitó",
        ],
        "asks": [
            "jsou to zároveň pojmy z pletení",
            "jsou v názvech Shakespearových her",
            "jsou to zároveň značky nebo modely aut",
            "jsou to znamení zvěrokruhu",
        ],
    },
    {
        "id": "v9-kosti",
        "roof": "slova, která jsou zároveň kosti v lidském těle",
        "level": "normal",
        "hidden": True,
        "inside": [
            "lopatka", "pánev", "čéška", "kostrč", "kyčel", "žebro", "holeň",
            "lebka",
        ],
        "outside": [
            "deka", "hoblík", "kladívko", "kýbl", "matice", "metr", "mísa",
            "parapet", "plot", "pravítko", "pytel", "sklenice", "trakař",
            "tácek", "vana",
        ],
        "asks": [
            "jsou to zároveň kosti v lidském těle",
            "jsou v názvech her Járy Cimrmana",
            "jsou v názvech večerníčků",
            "nemají v sobě ani jednu samohlásku",
        ],
    },
    {
        "id": "v9-hvezdy-lidove",
        "roof": "slova, která jsou zároveň lidová jména hvězd",
        "level": "hard",
        "hidden": True,
        "inside": [
            "Polárka", "Večernice", "Jitřenka", "Kuřátka", "Vozka", "Kosy",
        ],
        "outside": [
            "Kasiopeja", "Orion", "Andromeda", "Perseus", "Herkules", "Lyra",
            "Pegas", "Kentaur",
        ],
        "asks": [
            "jsou to zároveň lidová jména hvězd a souhvězdí",
            "jsou v názvech her Járy Cimrmana",
            "mají v sobě dvě stejná písmena vedle sebe",
            "jsou to zároveň značky nebo modely aut",
        ],
    },
    {
        "id": "v9-vino",
        "roof": "slova, která jsou zároveň vinařské pojmy",
        "level": "normal",
        "hidden": True,
        "inside": [
            "réva", "hrozen", "mošt", "burčák", "vinice", "sklizeň", "lis",
            "sklep",
        ],
        "outside": [
            "kotlina", "kotva", "kurýr", "kynutí", "podvozek", "pomoučení",
            "poplatek", "přenos", "převod", "příď", "sloučenina", "zkumavka",
        ],
        "asks": [
            "jsou to zároveň vinařské pojmy",
            "jsou v názvech Shakespearových her",
            "jsou to zároveň značky nebo modely aut",
            "jsou v názvech her Járy Cimrmana",
        ],
    },
    {
        "id": "v9-tabor",
        "roof": "slova, která jsou zároveň táborové vybavení",
        "level": "normal",
        "hidden": True,
        "inside": [
            "stan", "ohniště", "totem", "kotlík", "celta", "spacák",
            "menážka", "ešus",
        ],
        "outside": [
            "engoba", "jistítko", "kotva", "krotitel", "ohlávka", "program",
            "přestávka", "převaz", "stopa", "točení", "tíha", "řada",
        ],
        "asks": [
            "jsou to zároveň táborové vybavení",
            "mají v sobě schované zvíře",
            "jsou to zároveň značky českého piva",
            "jsou to znamení zvěrokruhu",
        ],
    },
    {
        "id": "v9-snih",
        "roof": "slova, která jsou zároveň podoby sněhu a mrazu",
        "level": "normal",
        "hidden": True,
        "inside": [
            "jinovatka", "náledí", "ledovka", "poprašek", "závěj", "břečka",
            "chumelenice", "plískanice",
        ],
        "outside": [
            "deka", "hadice", "hodinky", "koš", "metr", "mísa", "mýdlo",
            "pekáč", "podnos", "police", "ponožka", "pravítko", "ramínko",
            "schránka", "záclona",
        ],
        "asks": [
            "jsou to zároveň podoby sněhu nebo mrazu",
            "jsou to znamení zvěrokruhu",
            "jsou to zároveň značky nebo modely aut",
            "jsou to zároveň jména českých měst",
        ],
    },
    {
        "id": "v9-televize",
        "roof": "slova, která jsou zároveň televizní pojmy",
        "level": "normal",
        "hidden": True,
        "inside": [
            "pořad", "znělka", "reklama", "přenos", "program", "vysílání",
            "titulky", "studio",
        ],
        "outside": [
            "bašta", "engoba", "krmelec", "přestávka", "příkop", "stopa",
            "tempo", "vyloučení", "várka", "výrok", "úhel", "žaloba",
        ],
        "asks": [
            "jsou to zároveň televizní pojmy",
            "mají v sobě schované zvíře",
            "jsou to zároveň příjmení českých prezidentů",
            "čtou se stejně zepředu i zezadu",
        ],
    },
    {
        "id": "v9-pekarna",
        "roof": "slova, která jsou zároveň pekařské pojmy",
        "level": "normal",
        "hidden": True,
        "inside": [
            "kvásek", "těsto", "hnětení", "ošatka", "kynutí", "kůrka",
            "střída", "pomoučení",
        ],
        "outside": [
            "azimut", "bradla", "cimbuří", "dabing", "fronta", "hloubka",
            "pat", "pořad", "přádelna", "skleník", "třmen", "vázání",
        ],
        "asks": [
            "jsou to zároveň pekařské pojmy",
            "jsou to zároveň značky nebo modely aut",
            "jsou to znamení zvěrokruhu",
            "jsou to zároveň jména českých měst",
        ],
    },
    {
        "id": "v9-maly-princ",
        "roof": "slova z Malého prince",
        "level": "normal",
        "hidden": True,
        "inside": [
            "růže", "liška", "had", "planeta", "baobab", "beránek", "lampář",
            "hvězdář",
        ],
        "outside": [
            "Colorado", "Nil", "dělání", "havran", "jaro", "kočka", "kulička",
            "káva", "orloj", "statistika", "zrcadlo", "šrouby",
        ],
        "asks": [
            "jsou v Malém princi",
            "jsou v názvech Shakespearových her",
            "jsou to znamení zvěrokruhu",
            "jsou v názvech večerníčků",
        ],
    },
    {
        "id": "v9-alenka",
        "roof": "slova z Alenky v říši divů",
        "level": "normal",
        "hidden": True,
        "inside": [
            "klobouk", "králík", "kočka", "čaj", "zrcadlo", "houba", "karty",
            "sen",
        ],
        "outside": [
            "David", "barbora", "havran", "hodiny", "kulička", "křoví",
            "matice", "svět", "tabáček", "válka", "vítr", "věž",
        ],
        "asks": [
            "jsou v Alence v říši divů",
            "čtou se stejně zepředu i zezadu",
            "jsou to zároveň jména českých měst",
            "mají v sobě schované zvíře",
        ],
    },
    {
        "id": "v9-narnie",
        "roof": "slova z názvů dílů Narnie",
        "level": "hard",
        "hidden": True,
        "inside": [
            "lev", "čarodějnice", "skříň", "princ", "plavba", "kůň", "bitva",
            "synovec",
        ],
        "outside": [
            "Colorado", "abeceda", "archa", "hodiny", "holubice", "kočka",
            "kulička", "křoví", "ráj", "stroj", "škatule", "šrouby",
        ],
        "asks": [
            "jsou v názvech dílů Narnie",
            "jsou v názvech večerníčků",
            "jsou to zároveň jména českých měst",
            "čtou se stejně zepředu i zezadu",
        ],
    },
    {
        "id": "v9-ostrov-pokladu",
        "roof": "slova z Ostrova pokladů",
        "level": "normal",
        "hidden": True,
        "inside": [
            "poklad", "ostrov", "papoušek", "mapa", "truhla", "plachetnice",
            "pirát", "hospoda",
        ],
        "outside": [
            "Nil", "abeceda", "baobab", "kohout", "kulička", "limonáda",
            "medvídek", "planeta", "schůzka", "synovec", "tabáček",
            "ukolébavka",
        ],
        "asks": [
            "jsou v Ostrově pokladů",
            "jsou v názvech Shakespearových her",
            "jsou v názvech her Járy Cimrmana",
            "jsou v názvech večerníčků",
        ],
    },
    {
        "id": "v9-christie",
        "roof": "slova z názvů knih Agathy Christie",
        "level": "hard",
        "hidden": True,
        "inside": [
            "expres", "Nil", "hodiny", "abeceda", "zkouška", "karty",
            "schůzka", "čas",
        ],
        "outside": [
            "houba", "jaro", "kohout", "králík", "křoví", "lev", "mana",
            "medvídek", "ráj", "sen", "tabáček", "vodník",
        ],
        "asks": [
            "jsou v názvech knih Agathy Christie",
            "jsou to zároveň příjmení českých prezidentů",
            "jsou to znamení zvěrokruhu",
            "jsou v názvech her Járy Cimrmana",
        ],
    },
    {
        "id": "v9-poe",
        "roof": "slova z názvů povídek Edgara Allana Poea",
        "level": "hard",
        "hidden": True,
        "inside": [
            "havran", "jáma", "kyvadlo", "brouk", "dům", "maska", "srdce",
            "studna",
        ],
        "outside": [
            "golem", "hodiny", "kočka", "lampář", "liška", "mravenec",
            "plavba", "stroj", "světy", "tabáček", "tábor", "čert",
        ],
        "asks": [
            "jsou v názvech povídek Edgara Allana Poea",
            "jsou to zároveň značky českého piva",
            "jsou to znamení zvěrokruhu",
            "jsou to zároveň příjmení českých prezidentů",
        ],
    },
    {
        "id": "v9-wells",
        "roof": "slova z názvů knih H. G. Wellse",
        "level": "hard",
        "hidden": True,
        "inside": [
            "stroj", "čas", "válka", "světy", "ostrov", "měsíc", "potrava",
            "lidé",
        ],
        "outside": [
            "Amerika", "cukr", "dům", "golem", "holubice", "jáma", "křoví",
            "medvídek", "papoušek", "růže", "vodník", "šrouby",
        ],
        "asks": [
            "jsou v názvech knih H. G. Wellse",
            "jsou to zároveň příjmení českých prezidentů",
            "jsou v názvech her Járy Cimrmana",
            "čtou se stejně zepředu i zezadu",
        ],
    },
    {
        "id": "v9-bible",
        "roof": "slova z biblických příběhů",
        "level": "hard",
        "hidden": True,
        "inside": [
            "archa", "potopa", "věž", "ráj", "holubice", "mana", "žebřík",
            "studna",
        ],
        "outside": [
            "Nil", "bitva", "expres", "hospoda", "hvězdář", "orloj", "panák",
            "pirát", "rytíř", "sen", "světy", "válka",
        ],
        "asks": [
            "jsou v biblických příbězích",
            "mají v sobě dvě stejná písmena vedle sebe",
            "jsou to zároveň jména českých měst",
            "jsou v názvech her Járy Cimrmana",
        ],
    },
    {
        "id": "v9-sverak-uhlir",
        "roof": "slova z názvů písniček Svěráka a Uhlíře",
        "level": "normal",
        "hidden": True,
        "inside": [
            "vítr", "dělání", "statistika", "mravenec", "ukolébavka", "tábor",
            "jaro", "barbora",
        ],
        "outside": [
            "Nil", "bitva", "hodiny", "králík", "mana", "náhoda", "orloj",
            "panák", "papoušek", "růže", "schůzka", "věž",
        ],
        "asks": [
            "jsou v názvech písniček Svěráka a Uhlíře",
            "jsou to zároveň značky českého piva",
            "mají v sobě schované zvíře",
            "jsou to zároveň značky nebo modely aut",
        ],
    },
    {
        "id": "v9-vw",
        "roof": "slova z názvů písní Voskovce a Wericha",
        "level": "hard",
        "hidden": True,
        "inside": [
            "náhoda", "klobouk", "křoví", "svět", "David", "Goliáš", "šaty",
            "nebe",
        ],
        "outside": [
            "dům", "expres", "havran", "jáma", "králík", "maska", "medvídek",
            "papoušek", "plavba", "růže", "vítr", "zrcadlo",
        ],
        "asks": [
            "jsou v názvech písní Voskovce a Wericha",
            "jsou to zároveň značky českého piva",
            "jsou v názvech her Járy Cimrmana",
            "jsou to znamení zvěrokruhu",
        ],
    },
    {
        "id": "v9-kapely-pisne",
        "roof": "slova z názvů písní českých rockových kapel",
        "level": "normal",
        "hidden": True,
        "inside": [
            "medvídek", "šrouby", "matice", "Amerika", "pohoda", "dáma",
            "Colorado", "tabáček",
        ],
        "outside": [
            "archa", "cukr", "hodiny", "houba", "jáma", "nebe", "pirát",
            "plavba", "růže", "schovávaná", "vítr", "škatule",
        ],
        "asks": [
            "jsou v názvech písní českých rockových kapel",
            "nemají v sobě ani jednu samohlásku",
            "jsou to znamení zvěrokruhu",
            "jsou to zároveň jména českých měst",
        ],
    },
    {
        "id": "v9-prazske-povesti",
        "roof": "slova z pražských pověstí",
        "level": "hard",
        "hidden": True,
        "inside": [
            "golem", "orloj", "Faust", "čert", "poklad", "rytíř", "kohout",
            "vodník",
        ],
        "outside": [
            "bába", "cukr", "had", "havran", "hodiny", "hospoda", "mapa",
            "panák", "plavba", "tábor", "vítr", "zrcadlo",
        ],
        "asks": [
            "jsou v pražských pověstech",
            "jsou to zároveň příjmení českých prezidentů",
            "nemají v sobě ani jednu samohlásku",
            "mají v sobě dvě stejná písmena vedle sebe",
        ],
    },
    {
        "id": "v9-detske-hry",
        "roof": "slova z názvů dětských her",
        "level": "normal",
        "hidden": True,
        "inside": [
            "bába", "škatule", "kulička", "panák", "cukr", "káva", "limonáda",
            "schovávaná",
        ],
        "outside": [
            "Goliáš", "dům", "expres", "králík", "mana", "měsíc", "náhoda",
            "plavba", "potopa", "svět", "čaj", "šaty",
        ],
        "asks": [
            "jsou v názvech dětských her",
            "jsou to zároveň značky českého piva",
            "čtou se stejně zepředu i zezadu",
            "jsou to znamení zvěrokruhu",
        ],
    },
    {
        "id": "v9-zvyky",
        "roof": "slova z českých zvyků a obyčejů",
        "level": "normal",
        "hidden": True,
        "inside": [
            "pomlázka", "koleda", "masopust", "dušičky", "půlnoční",
            "vinšování", "stromeček", "kraslice",
        ],
        "outside": [
            "deštník", "dřez", "hadice", "hrnec", "konev", "koště",
            "lednička", "lepidlo", "metr", "parapet", "pinzeta", "popelnice",
            "rýč", "trakař", "záclona",
        ],
        "asks": [
            "patří k českým zvykům a obyčejům",
            "mají v sobě dvě stejná písmena vedle sebe",
            "jsou v názvech her Járy Cimrmana",
            "jsou to zároveň příjmení českých prezidentů",
        ],
    },
    {
        "id": "v9-rub-lic",
        "roof": "věci, které mají rub a líc",
        "level": "hard",
        "hidden": True,
        "inside": [
            "mince", "medaile", "látka", "karta", "koberec", "list",
            "ponožka", "deska",
        ],
        "outside": [
            "cihla", "klíč", "hrnec", "žebřík", "kbelík", "lampa", "provaz",
            "míč", "sklenice", "kladivo",
        ],
        "asks": [
            "mají rub a líc",
            "jsou to znamení zvěrokruhu",
            "mají v sobě dvě stejná písmena vedle sebe",
            "jsou to zároveň jména českých měst",
        ],
    },
    {
        "id": "v9-kompost",
        "roof": "věci, které patří na kompost",
        "level": "normal",
        "hidden": True,
        "inside": [
            "slupky", "listí", "tráva", "skořápky", "plevel", "seno",
            "piliny", "lógr",
        ],
        "outside": [
            "sklo", "plast", "kov", "baterie", "olej", "guma", "polystyren",
            "hadr", "drát", "plechovka",
        ],
        "asks": [
            "patří na kompost",
            "jsou to zároveň jména českých měst",
            "jsou v názvech Shakespearových her",
            "jsou to zároveň příjmení českých prezidentů",
        ],
    },
    {
        "id": "v9-jedno-pouziti",
        "roof": "věci na jedno použití",
        "level": "normal",
        "hidden": True,
        "inside": [
            "kapesník", "brčko", "kelímek", "ubrousek", "sirka", "plena",
            "párátko", "sáček",
        ],
        "outside": [
            "hrnek", "talíř", "lžíce", "ručník", "deka", "kabát", "kbelík",
            "židle", "konvice", "utěrka",
        ],
        "asks": [
            "jsou na jedno použití",
            "jsou to znamení zvěrokruhu",
            "jsou v názvech večerníčků",
            "jsou to zároveň značky českého piva",
        ],
    },
    {
        "id": "v9-nabit",
        "roof": "věci, které se dají nabít",
        "level": "normal",
        "hidden": True,
        "inside": [
            "baterie", "mobil", "powerbanka", "notebook", "kartáček",
            "hodinky", "vrtačka", "koloběžka",
        ],
        "outside": [
            "kladivo", "deštník", "klíč", "hrnec", "deka", "žebřík", "kniha",
            "židle", "koště", "lopata",
        ],
        "asks": [
            "se dají nabít",
            "jsou v názvech večerníčků",
            "jsou to zároveň jména českých měst",
            "nemají v sobě ani jednu samohlásku",
        ],
    },
    {
        "id": "v9-bydlet",
        "roof": "stavby, ve kterých se dá bydlet",
        "level": "normal",
        "hidden": True,
        "inside": [
            "dům", "chata", "karavan", "hausbót", "jurta", "stan", "byt",
            "srub",
        ],
        "outside": [
            "garáž", "kůlna", "skleník", "seník", "dílna", "sklep", "maják",
            "stodola", "hangár", "kotelna",
        ],
        "asks": [
            "se dají obývat",
            "jsou to znamení zvěrokruhu",
            "jsou to zároveň značky nebo modely aut",
            "jsou v názvech her Járy Cimrmana",
        ],
    },
    {
        "id": "v9-prukaz",
        "roof": "stroje, na které je potřeba průkaz",
        "level": "hard",
        "hidden": True,
        "inside": [
            "auto", "motorka", "letadlo", "loď", "jeřáb", "kamion", "rypadlo",
            "traktor",
        ],
        "outside": [
            "kolo", "koloběžka", "sáně", "brusle", "lyže", "kánoe", "běžky",
            "skateboard", "tříkolka", "šlapadlo",
        ],
        "asks": [
            "potřebují k řízení průkaz",
            "mají v sobě dvě stejná písmena vedle sebe",
            "jsou v názvech her Járy Cimrmana",
            "čtou se stejně zepředu i zezadu",
        ],
    },
    {
        "id": "v9-na-dalku",
        "roof": "věci, které se ovládají na dálku",
        "level": "normal",
        "hidden": True,
        "inside": [
            "televize", "garáž", "dron", "závora", "klimatizace", "kotel",
            "žaluzie", "brána",
        ],
        "outside": [
            "kladivo", "deštník", "žebřík", "konev", "koště", "hrnec",
            "lopata", "žehlička", "kbelík", "pila",
        ],
        "asks": [
            "se ovládají na dálku",
            "jsou v názvech her Járy Cimrmana",
            "nemají v sobě ani jednu samohlásku",
            "jsou to zároveň jména českých měst",
        ],
    },
    {
        "id": "v9-naostrit",
        "roof": "věci, které se musí ostřit",
        "level": "normal",
        "hidden": True,
        "inside": [
            "nůž", "sekera", "pila", "kosa", "dláto", "nůžky", "hoblík",
            "tužka",
        ],
        "outside": [
            "kladivo", "lopata", "hrábě", "kbelík", "provaz", "deka", "hrnec",
            "žebřík", "konev", "pytel",
        ],
        "asks": [
            "se musí čas od času naostřit",
            "jsou to znamení zvěrokruhu",
            "jsou v názvech Shakespearových her",
            "jsou to zároveň značky českého piva",
        ],
    },
    {
        "id": "v9-oloupat",
        "roof": "jídlo, které se před jídlem loupe",
        "level": "normal",
        "hidden": True,
        "inside": [
            "banán", "pomeranč", "cibule", "vejce", "kiwi", "mandarinka",
            "česnek", "ananas",
        ],
        "outside": [
            "jablko", "hruška", "rajče", "jahoda", "rybíz", "švestka",
            "třešeň", "malina", "angrešt", "borůvka",
        ],
        "asks": [
            "se před jídlem loupou",
            "jsou to zároveň značky českého piva",
            "jsou to zároveň značky nebo modely aut",
            "jsou v názvech Shakespearových her",
        ],
    },
]
