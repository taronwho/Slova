"""Osmá várka rodin — padesát os, které tu ještě nebyly.

TENHLE SOUBOR PÍŠE SKRIPT. Ruční úpravy zmizí při dalším spuštění; opravovat
se má `tools/gen_families8.py`, kde stojí zadání i kontroly.

Pět nových druhů souvislosti: fyzikální vlastnost (čtyři z nich plavou),
praktické použití (vejdou se do kapsy), mluvnice (jen v množném čísle),
ustálené spojení (zlatý déšť, zlatá horečka) a text, který zná každý (česká
hymna, přísloví, pranostiky).

Slova vně tu nejsou nudná náhodou: u rodiny „čtyři z nich plavou" musí být
vetřelec věc, která se **jistě potopí**. Kdyby tam stál deštník, hráč netuší,
jak to s ním je, a hádanka se rozpadne na dohady.
"""

FAMILIES8 = [
    {
        "id": "vlast-plavou",
        "roof": "věci, které plavou na vodě",
        "level": "normal",
        "hidden": True,
        "inside": [
            "korek", "dřevo", "led", "olej", "polystyren", "pěna", "sláma",
            "vosk",
        ],
        "outside": [
            "kámen", "cihla", "hřebík", "mince", "klíč", "sekera", "podkova",
            "žehlička", "kladivo", "kotva",
        ],
        "asks": [
            "plavou na vodě",
            "jsou v názvech Shakespearových her",
            "nemají v sobě ani jednu samohlásku",
            "jsou v názvech večerníčků",
        ],
    },
    {
        "id": "vlast-rozpusti",
        "roof": "věci, které se rozpustí ve vodě",
        "level": "normal",
        "hidden": True,
        "inside": [
            "sůl", "cukr", "soda", "med", "sirup", "mýdlo", "bonbon",
            "želatina",
        ],
        "outside": [
            "písek", "olej", "sklo", "vosk", "korek", "plast", "dřevo",
            "štěrk", "kámen", "křída",
        ],
        "asks": [
            "se rozpustí ve vodě",
            "jsou to zároveň jména českých měst",
            "jsou v názvech Shakespearových her",
            "jsou to znamení zvěrokruhu",
        ],
    },
    {
        "id": "vlast-magnet",
        "roof": "věci, které přitáhne magnet",
        "level": "normal",
        "hidden": True,
        "inside": [
            "hřebík", "sponka", "šroub", "jehla", "plech", "podkova",
            "pilník", "konzerva",
        ],
        "outside": [
            "guma", "sklo", "dřevo", "papír", "plast", "hliník", "měď",
            "keramika", "provaz", "korek",
        ],
        "asks": [
            "přitáhne magnet",
            "čtou se stejně zepředu i zezadu",
            "jsou v názvech večerníčků",
            "jsou v názvech her Járy Cimrmana",
        ],
    },
    {
        "id": "vlast-proud",
        "roof": "látky, které vedou elektřinu",
        "level": "hard",
        "hidden": True,
        "inside": [
            "měď", "hliník", "železo", "stříbro", "zlato", "ocel", "mosaz",
            "grafit",
        ],
        "outside": [
            "sklo", "guma", "dřevo", "plast", "papír", "keramika", "korek",
            "vosk", "porcelán", "vzduch",
        ],
        "asks": [
            "vedou elektřinu",
            "jsou to zároveň příjmení českých prezidentů",
            "nemají v sobě ani jednu samohlásku",
            "jsou to znamení zvěrokruhu",
        ],
    },
    {
        "id": "vlast-hori",
        "roof": "věci, které hoří",
        "level": "normal",
        "hidden": True,
        "inside": [
            "papír", "dřevo", "sláma", "vosk", "uhlí", "líh", "benzin",
            "seno",
        ],
        "outside": [
            "kámen", "sklo", "písek", "cihla", "beton", "hlína", "voda",
            "plech", "keramika", "mramor",
        ],
        "asks": [
            "hoří",
            "mají v sobě schované zvíře",
            "jsou to zároveň značky českého piva",
            "čtou se stejně zepředu i zezadu",
        ],
    },
    {
        "id": "vlast-roztaji",
        "roof": "věci, které roztají v teple",
        "level": "normal",
        "hidden": True,
        "inside": [
            "led", "čokoláda", "máslo", "sníh", "vosk", "zmrzlina", "sádlo",
            "parafín",
        ],
        "outside": [
            "kámen", "sklo", "dřevo", "mince", "guma", "křída", "cukr", "sůl",
            "cihla", "hřebík",
        ],
        "asks": [
            "roztají v teple",
            "jsou to znamení zvěrokruhu",
            "jsou to zároveň značky českého piva",
            "jsou to zároveň jména českých měst",
        ],
    },
    {
        "id": "vlast-pruhledne",
        "roof": "věci, které jsou průhledné",
        "level": "normal",
        "hidden": True,
        "inside": [
            "sklo", "led", "voda", "celofán", "křišťál", "plexisklo",
            "bublina", "igelit",
        ],
        "outside": [
            "cihla", "dřevo", "plech", "papír", "kámen", "keramika", "guma",
            "korek", "plátno", "beton",
        ],
        "asks": [
            "jsou průhledné",
            "čtou se stejně zepředu i zezadu",
            "mají v sobě dvě stejná písmena vedle sebe",
            "jsou to znamení zvěrokruhu",
        ],
    },
    {
        "id": "vlast-rezavi",
        "roof": "věci, které rezaví",
        "level": "normal",
        "hidden": True,
        "inside": [
            "hřebík", "plech", "řetěz", "sekera", "kotva", "kolejnice",
            "brnění", "pilník",
        ],
        "outside": [
            "sklo", "plast", "dřevo", "guma", "keramika", "papír", "korek",
            "kámen", "hliník", "zlato",
        ],
        "asks": [
            "rezaví",
            "jsou v názvech Shakespearových her",
            "jsou v názvech her Járy Cimrmana",
            "jsou to znamení zvěrokruhu",
        ],
    },
    {
        "id": "vlast-svetlo",
        "roof": "věci, které vydávají vlastní světlo",
        "level": "hard",
        "hidden": True,
        "inside": [
            "hvězda", "oheň", "blesk", "světluška", "svíčka", "láva",
            "slunce", "výboj",
        ],
        "outside": [
            "měsíc", "zrcadlo", "sklo", "sníh", "mrak", "hladina", "stříbro",
            "led", "okno", "mince",
        ],
        "asks": [
            "vydávají vlastní světlo",
            "jsou to zároveň značky nebo modely aut",
            "jsou to zároveň příjmení českých prezidentů",
            "jsou v názvech Shakespearových her",
        ],
    },
    {
        "id": "vlast-ohnout",
        "roof": "věci, které se dají ohnout, aniž prasknou",
        "level": "normal",
        "hidden": True,
        "inside": [
            "drát", "guma", "provaz", "plech", "proutek", "hadice", "papír",
            "kůže",
        ],
        "outside": [
            "sklo", "cihla", "křída", "keramika", "led", "talíř", "žárovka",
            "dlaždice", "prkno", "beton",
        ],
        "asks": [
            "se dají ohnout, aniž prasknou",
            "jsou to zároveň jména českých měst",
            "nemají v sobě ani jednu samohlásku",
            "jsou to znamení zvěrokruhu",
        ],
    },
    {
        "id": "vlast-dute",
        "roof": "věci, které jsou uvnitř duté",
        "level": "hard",
        "hidden": True,
        "inside": [
            "trubka", "míč", "sud", "láhev", "buben", "zvon", "komín",
            "brčko",
        ],
        "outside": [
            "cihla", "kámen", "prkno", "kladivo", "klíč", "mince", "špalek",
            "dlaždice", "sekera", "žehlička",
        ],
        "asks": [
            "jsou uvnitř duté",
            "jsou to zároveň značky nebo modely aut",
            "jsou v názvech her Járy Cimrmana",
            "mají v sobě dvě stejná písmena vedle sebe",
        ],
    },
    {
        "id": "vlast-nafouknout",
        "roof": "věci, které se dají nafouknout",
        "level": "normal",
        "hidden": True,
        "inside": [
            "balón", "duše", "pneumatika", "matrace", "míč", "bublina",
            "plíce", "člun",
        ],
        "outside": [
            "cihla", "kámen", "prkno", "hrnec", "židle", "kniha", "klíč",
            "talíř", "lopata", "žebřík",
        ],
        "asks": [
            "se dají nafouknout",
            "jsou v názvech Shakespearových her",
            "jsou to zároveň příjmení českých prezidentů",
            "mají v sobě dvě stejná písmena vedle sebe",
        ],
    },
    {
        "id": "vlast-kapsa",
        "roof": "věci, které se vejdou do kapsy",
        "level": "normal",
        "hidden": True,
        "inside": [
            "klíč", "mince", "zápalky", "hřeben", "kapesník", "propiska",
            "mobil", "sponka",
        ],
        "outside": [
            "žebřík", "koberec", "pračka", "židle", "kolo", "dveře",
            "matrace", "lampa", "žehlička", "kufr",
        ],
        "asks": [
            "se vejdou do kapsy",
            "jsou to zároveň jména českých měst",
            "mají v sobě dvě stejná písmena vedle sebe",
            "nemají v sobě ani jednu samohlásku",
        ],
    },
    {
        "id": "vlast-syrove",
        "roof": "jídlo, které se dá jíst syrové",
        "level": "normal",
        "hidden": True,
        "inside": [
            "mrkev", "jablko", "okurka", "ořech", "rajče", "med", "salát",
            "hruška",
        ],
        "outside": [
            "brambora", "fazole", "rýže", "těstoviny", "mouka", "čočka",
            "kroupy", "hrách", "krupice", "pohanka",
        ],
        "asks": [
            "se dají jíst syrové",
            "mají v sobě schované zvíře",
            "jsou to zároveň značky nebo modely aut",
            "jsou to zároveň jména českých měst",
        ],
    },
    {
        "id": "vlast-bez-proudu",
        "roof": "věci, které fungují bez proudu i baterií",
        "level": "normal",
        "hidden": True,
        "inside": [
            "kompas", "kladivo", "brýle", "kolo", "deštník", "píšťalka",
            "lopata", "žebřík",
        ],
        "outside": [
            "mobil", "rádio", "vysavač", "žehlička", "baterka", "notebook",
            "lednička", "mikrovlnka", "sekačka", "pračka",
        ],
        "asks": [
            "fungují bez proudu i baterií",
            "jsou v názvech Shakespearových her",
            "jsou to znamení zvěrokruhu",
            "jsou v názvech večerníčků",
        ],
    },
    {
        "id": "vlast-bez-dilu",
        "roof": "věci, které nemají žádný pohyblivý díl",
        "level": "hard",
        "hidden": True,
        "inside": [
            "cihla", "sklenice", "talíř", "prkno", "deka", "hrnec", "kbelík",
            "dlaždice",
        ],
        "outside": [
            "nůžky", "klika", "hodinky", "kolo", "dveře", "pumpa", "zip",
            "jeřáb", "váha", "pila",
        ],
        "asks": [
            "nemají žádný pohyblivý díl",
            "mají v sobě schované zvíře",
            "jsou to zároveň značky nebo modely aut",
            "čtou se stejně zepředu i zezadu",
        ],
    },
    {
        "id": "vlast-dva-lidi",
        "roof": "věci, které potřebují aspoň dva lidi",
        "level": "normal",
        "hidden": True,
        "inside": [
            "šachy", "tenis", "rozhovor", "tanec", "souboj", "přetahovaná",
            "svatba", "badminton",
        ],
        "outside": [
            "čtení", "běh", "plavání", "šití", "kreslení", "spánek",
            "pletení", "rybaření", "žonglování", "luštění",
        ],
        "asks": [
            "potřebují aspoň dva lidi",
            "jsou v názvech večerníčků",
            "čtou se stejně zepředu i zezadu",
            "jsou to znamení zvěrokruhu",
        ],
    },
    {
        "id": "vlast-srolovat",
        "roof": "věci, které se dají složit nebo srolovat",
        "level": "normal",
        "hidden": True,
        "inside": [
            "deka", "mapa", "deštník", "stan", "noviny", "koberec", "spacák",
            "plátno",
        ],
        "outside": [
            "sklenice", "cihla", "hrnec", "klíč", "žehlička", "talíř",
            "kladivo", "zrcadlo", "žárovka", "police",
        ],
        "asks": [
            "se dají složit nebo srolovat",
            "jsou v názvech Shakespearových her",
            "jsou to znamení zvěrokruhu",
            "čtou se stejně zepředu i zezadu",
        ],
    },
    {
        "id": "vlast-strecha",
        "roof": "věci, které jsou na střeše domu",
        "level": "hard",
        "hidden": True,
        "inside": [
            "komín", "anténa", "hromosvod", "okap", "korouhvička", "vikýř",
            "satelit", "taška",
        ],
        "outside": [
            "sklep", "práh", "schod", "koberec", "klika", "kamna", "vana",
            "umyvadlo", "plot", "dlažba",
        ],
        "asks": [
            "jsou na střeše domu",
            "jsou to zároveň značky českého piva",
            "mají v sobě schované zvíře",
            "jsou v názvech Shakespearových her",
        ],
    },
    {
        "id": "vlast-voda-tece",
        "roof": "věci, ze kterých teče voda",
        "level": "normal",
        "hidden": True,
        "inside": [
            "kohoutek", "hadice", "sprcha", "konev", "okap", "fontána",
            "pramen", "konvice",
        ],
        "outside": [
            "lampa", "koš", "polštář", "kniha", "židle", "zrcadlo", "žebřík",
            "koberec", "hřebík", "mísa",
        ],
        "asks": [
            "teče z nich voda",
            "jsou to znamení zvěrokruhu",
            "nemají v sobě ani jednu samohlásku",
            "čtou se stejně zepředu i zezadu",
        ],
    },
    {
        "id": "mluv-pomnozna",
        "roof": "slova, která se používají jen v množném čísle",
        "level": "normal",
        "hidden": True,
        "inside": [
            "dveře", "kalhoty", "nůžky", "housle", "brýle", "kamna", "vrata",
            "sáně", "narozeniny", "kleště",
        ],
        "outside": [
            "stůl", "okno", "kniha", "lampa", "židle", "talíř", "klíč", "koš",
            "hrnec", "police",
        ],
        "asks": [
            "se používají jen v množném čísle",
            "jsou to zároveň jména českých měst",
            "jsou v názvech Shakespearových her",
            "mají v sobě schované zvíře",
        ],
    },
    {
        "id": "mluv-spodoba",
        "roof": "slova, která se na konci vyslovují jinak, než píšou",
        "level": "hard",
        "hidden": True,
        "inside": [
            "dub", "led", "plod", "vůz", "nůž", "hrad", "mráz", "sad",
            "obraz", "sníh",
        ],
        "outside": [
            "stůl", "okno", "klíč", "lampa", "kniha", "most", "pes", "list",
            "koš", "papír",
        ],
        "asks": [
            "se na konci vyslovují jinak, než se píšou",
            "jsou to znamení zvěrokruhu",
            "jsou v názvech večerníčků",
            "jsou to zároveň příjmení českých prezidentů",
        ],
    },
    {
        "id": "mluv-predpona",
        "roof": "slova, ze kterých po odtržení předpony zbude jiné slovo",
        "level": "hard",
        "hidden": True,
        "inside": [
            "podnos", "výlet", "zápas", "nádech", "příklad", "útok", "rozum",
            "odchod",
        ],
        "outside": [
            "koberec", "sklenice", "lampa", "žebřík", "mrkev", "police",
            "talíř", "kniha", "hrnec", "zahrada",
        ],
        "asks": [
            "po odtržení předpony z nich zbude jiné slovo",
            "čtou se stejně zepředu i zezadu",
            "jsou to zároveň značky českého piva",
            "jsou v názvech Shakespearových her",
        ],
    },
    {
        "id": "mluv-nesklonna",
        "roof": "slova, která se neskloňují",
        "level": "hard",
        "hidden": True,
        "inside": [
            "kupé", "tabu", "taxi", "menu", "alibi", "whisky", "kakadu",
            "iglú",
        ],
        "outside": [
            "auto", "kino", "metro", "rádio", "sako", "víno", "pero", "okno",
            "sklo", "lano",
        ],
        "asks": [
            "se neskloňují",
            "jsou to zároveň značky českého piva",
            "jsou to zároveň jména českých měst",
            "jsou to znamení zvěrokruhu",
        ],
    },
    {
        "id": "mluv-prijmeni",
        "roof": "slova, která jsou zároveň běžná česká příjmení",
        "level": "hard",
        "hidden": True,
        "inside": [
            "kovář", "kolář", "sedlák", "mlynář", "král", "zima", "kříž",
            "mráz",
        ],
        "outside": [
            "hrnec", "deštník", "police", "koště", "lampa", "žebřík",
            "koberec", "mrkev", "talíř", "kbelík",
        ],
        "asks": [
            "jsou to zároveň běžná česká příjmení",
            "nemají v sobě ani jednu samohlásku",
            "mají v sobě schované zvíře",
            "jsou v názvech her Járy Cimrmana",
        ],
    },
    {
        "id": "mluv-zdrobnelina",
        "roof": "slova, jejichž zdrobnělina znamená něco jiného",
        "level": "hard",
        "hidden": True,
        "inside": [
            "hlava", "ruka", "kobyla", "žába", "panna", "ucho", "koleno",
            "hřebík",
        ],
        "outside": [
            "stůl", "okno", "police", "koberec", "lampa", "talíř", "žebřík",
            "kbelík", "mrkev", "hrnec",
        ],
        "asks": [
            "jejich zdrobnělina znamená něco úplně jiného",
            "čtou se stejně zepředu i zezadu",
            "jsou v názvech Shakespearových her",
            "jsou v názvech her Járy Cimrmana",
        ],
    },
    {
        "id": "mluv-vyjmenovana",
        "roof": "vyjmenovaná slova",
        "level": "normal",
        "hidden": True,
        "inside": [
            "nábytek", "kopyto", "mlýn", "plyn", "lyže", "pytel", "sýr",
            "hmyz", "mýto", "chmýří",
        ],
        "outside": [
            "stůl", "okno", "police", "koberec", "lampa", "talíř", "žebřík",
            "kbelík", "mrkev", "hrnec",
        ],
        "asks": [
            "jsou to vyjmenovaná slova",
            "jsou to zároveň jména českých měst",
            "čtou se stejně zepředu i zezadu",
            "jsou to zároveň značky nebo modely aut",
        ],
    },
    {
        "id": "spoj-zlaty",
        "roof": "slova, která tvoří dvojici se slovem zlatý",
        "level": "hard",
        "hidden": True,
        "inside": [
            "déšť", "horečka", "ručičky", "řez", "hřeb", "klec", "svatba",
            "důl",
        ],
        "outside": [
            "police", "koberec", "žebřík", "mrkev", "talíř", "kbelík",
            "hrnec", "lampa", "sešit", "deštník",
        ],
        "asks": [
            "tvoří se slovem zlatý ustálené spojení",
            "nemají v sobě ani jednu samohlásku",
            "jsou v názvech večerníčků",
            "jsou to zároveň značky českého piva",
        ],
    },
    {
        "id": "spoj-cerny",
        "roof": "slova, která tvoří dvojici se slovem černý",
        "level": "normal",
        "hidden": True,
        "inside": [
            "díra", "humor", "skříňka", "pasažér", "svědomí", "hodinka",
            "kašel", "listina",
        ],
        "outside": [
            "police", "koberec", "žebřík", "mrkev", "talíř", "kbelík",
            "hrnec", "lampa", "sešit", "deštník",
        ],
        "asks": [
            "tvoří se slovem černý ustálené spojení",
            "jsou to zároveň značky českého piva",
            "jsou to zároveň značky nebo modely aut",
            "jsou v názvech her Járy Cimrmana",
        ],
    },
    {
        "id": "spoj-volny",
        "roof": "slova, která tvoří dvojici se slovem volný",
        "level": "normal",
        "hidden": True,
        "inside": [
            "pád", "čas", "noha", "ruka", "styl", "místo", "chvíle", "vstup",
        ],
        "outside": [
            "police", "koberec", "žebřík", "mrkev", "talíř", "kbelík",
            "hrnec", "lampa", "sešit", "deštník",
        ],
        "asks": [
            "tvoří se slovem volný ustálené spojení",
            "jsou to zároveň značky nebo modely aut",
            "mají v sobě schované zvíře",
            "jsou to znamení zvěrokruhu",
        ],
    },
    {
        "id": "spoj-studena",
        "roof": "slova, která tvoří dvojici se slovem studený",
        "level": "hard",
        "hidden": True,
        "inside": [
            "válka", "sprcha", "kuchyně", "hlava", "bufet", "start", "čaj",
            "zbraň",
        ],
        "outside": [
            "police", "koberec", "žebřík", "mrkev", "talíř", "kbelík",
            "hrnec", "lampa", "sešit", "deštník",
        ],
        "asks": [
            "tvoří se slovem studený ustálené spojení",
            "jsou v názvech her Járy Cimrmana",
            "jsou to zároveň příjmení českých prezidentů",
            "jsou v názvech večerníčků",
        ],
    },
    {
        "id": "text-hymna",
        "roof": "slova z české hymny",
        "level": "hard",
        "hidden": True,
        "inside": [
            "domov", "voda", "bory", "sad", "jaro", "květ", "ráj", "země",
        ],
        "outside": [
            "police", "koberec", "žebřík", "mrkev", "talíř", "kbelík",
            "hrnec", "lampa", "sešit", "deštník",
        ],
        "asks": [
            "jsou v české hymně",
            "nemají v sobě ani jednu samohlásku",
            "mají v sobě dvě stejná písmena vedle sebe",
            "čtou se stejně zepředu i zezadu",
        ],
    },
    {
        "id": "text-prislovi",
        "roof": "slova z českých přísloví",
        "level": "normal",
        "hidden": True,
        "inside": [
            "jáma", "koláč", "břeh", "ptáče", "jablko", "poklička", "kosa",
            "kámen",
        ],
        "outside": [
            "police", "žebřík", "mrkev", "talíř", "kbelík", "lampa", "sešit",
            "deštník", "koberec", "ubrus",
        ],
        "asks": [
            "stojí v českých příslovích",
            "jsou to zároveň jména českých měst",
            "jsou to zároveň příjmení českých prezidentů",
            "mají v sobě dvě stejná písmena vedle sebe",
        ],
    },
    {
        "id": "text-pranostiky",
        "roof": "slova z pranostik",
        "level": "hard",
        "hidden": True,
        "inside": [
            "pole", "kamna", "kápě", "stodola", "sedlák", "ráj", "máj", "led",
        ],
        "outside": [
            "police", "žebřík", "mrkev", "talíř", "kbelík", "lampa", "sešit",
            "deštník", "koberec", "ubrus",
        ],
        "asks": [
            "stojí v pranostikách",
            "jsou v názvech Shakespearových her",
            "mají v sobě schované zvíře",
            "nemají v sobě ani jednu samohlásku",
        ],
    },
    {
        "id": "obor-kostel",
        "roof": "slova, která jsou zároveň části kostela",
        "level": "hard",
        "hidden": True,
        "inside": [
            "loď", "věž", "kůr", "oltář", "zvonice", "klenba", "sloup",
            "kříž",
        ],
        "outside": [
            "police", "žebřík", "mrkev", "talíř", "kbelík", "lampa", "sešit",
            "deštník", "koberec", "ubrus",
        ],
        "asks": [
            "jsou to zároveň části kostela",
            "jsou to zároveň jména českých měst",
            "jsou to zároveň značky nebo modely aut",
            "jsou v názvech večerníčků",
        ],
    },
    {
        "id": "obor-vcely",
        "roof": "slova, která jsou zároveň včelařské pojmy",
        "level": "hard",
        "hidden": True,
        "inside": [
            "matka", "roj", "plást", "úl", "rámek", "medomet", "dýmák",
            "vosk",
        ],
        "outside": [
            "police", "žebřík", "mrkev", "talíř", "kbelík", "lampa", "sešit",
            "deštník", "koberec", "ubrus",
        ],
        "asks": [
            "jsou to zároveň včelařské pojmy",
            "mají v sobě schované zvíře",
            "jsou to zároveň příjmení českých prezidentů",
            "jsou to zároveň značky nebo modely aut",
        ],
    },
    {
        "id": "obor-siti",
        "roof": "slova, která jsou zároveň pojmy ze šití",
        "level": "normal",
        "hidden": True,
        "inside": [
            "jehla", "náprstek", "steh", "lem", "špendlík", "střih", "náplet",
            "knoflík",
        ],
        "outside": [
            "police", "žebřík", "mrkev", "talíř", "kbelík", "lampa", "sešit",
            "deštník", "koberec", "ubrus",
        ],
        "asks": [
            "jsou to zároveň pojmy ze šití",
            "čtou se stejně zepředu i zezadu",
            "jsou to zároveň značky nebo modely aut",
            "mají v sobě schované zvíře",
        ],
    },
    {
        "id": "obor-ryby",
        "roof": "slova, která jsou zároveň rybářské pojmy",
        "level": "hard",
        "hidden": True,
        "inside": [
            "muška", "prut", "splávek", "naviják", "podběrák", "návnada",
            "třpytka", "olůvko",
        ],
        "outside": [
            "police", "žebřík", "mrkev", "talíř", "kbelík", "lampa", "sešit",
            "deštník", "koberec", "ubrus",
        ],
        "asks": [
            "jsou to zároveň rybářské pojmy",
            "jsou v názvech večerníčků",
            "jsou to znamení zvěrokruhu",
            "nemají v sobě ani jednu samohlásku",
        ],
    },
    {
        "id": "obor-obloha",
        "roof": "slova, která jsou zároveň úkazy na obloze",
        "level": "normal",
        "hidden": True,
        "inside": [
            "duha", "blesk", "zatmění", "kometa", "záře", "meteor", "halo",
            "mlhovina",
        ],
        "outside": [
            "police", "žebřík", "mrkev", "talíř", "kbelík", "lampa", "sešit",
            "deštník", "koberec", "ubrus",
        ],
        "asks": [
            "jsou to zároveň úkazy na obloze",
            "jsou to zároveň značky nebo modely aut",
            "mají v sobě dvě stejná písmena vedle sebe",
            "jsou to zároveň značky českého piva",
        ],
    },
    {
        "id": "obor-rybniky",
        "roof": "slova, která jsou zároveň jména jihočeských rybníků",
        "level": "hard",
        "hidden": True,
        "inside": [
            "svět", "naděje", "rožmberk", "bezdrev", "dvořiště", "staňkovský",
        ],
        "outside": [
            "police", "žebřík", "mrkev", "talíř", "kbelík", "lampa", "sešit",
            "deštník", "koberec", "ubrus",
        ],
        "asks": [
            "jsou to zároveň jména jihočeských rybníků",
            "jsou v názvech her Járy Cimrmana",
            "jsou v názvech Shakespearových her",
            "jsou v názvech večerníčků",
        ],
    },
    {
        "id": "vlast-krehke",
        "roof": "věci, které se rozbijí, když spadnou",
        "level": "normal",
        "hidden": True,
        "inside": [
            "sklenice", "talíř", "vejce", "žárovka", "zrcadlo", "váza",
            "hrnek", "porcelán",
        ],
        "outside": [
            "guma", "plech", "provaz", "polštář", "deka", "klíč", "kladivo",
            "míč", "bota", "kabát",
        ],
        "asks": [
            "se rozbijí, když spadnou",
            "jsou v názvech her Járy Cimrmana",
            "jsou to zároveň příjmení českých prezidentů",
            "jsou v názvech večerníčků",
        ],
    },
    {
        "id": "vlast-vzduch",
        "roof": "věci, které bez vzduchu nefungují",
        "level": "hard",
        "hidden": True,
        "inside": [
            "oheň", "plachetnice", "drak", "větrník", "píšťala", "plíce",
            "vrtule", "bublina",
        ],
        "outside": [
            "baterka", "hodinky", "kámen", "magnet", "sklo", "klíč",
            "zrcadlo", "provaz", "mince", "cihla",
        ],
        "asks": [
            "bez vzduchu nefungují",
            "nemají v sobě ani jednu samohlásku",
            "jsou v názvech večerníčků",
            "mají v sobě dvě stejná písmena vedle sebe",
        ],
    },
    {
        "id": "vlast-nit",
        "roof": "věci, které se dají navléknout na nit",
        "level": "hard",
        "hidden": True,
        "inside": [
            "korálek", "knoflík", "perla", "těstovina", "jeřabina", "prsten",
            "matice", "kroužek",
        ],
        "outside": [
            "cihla", "talíř", "deka", "sklenice", "kniha", "lampa", "mrkev",
            "provaz", "hrnec", "koberec",
        ],
        "asks": [
            "se dají navléknout na nit",
            "jsou to znamení zvěrokruhu",
            "jsou to zároveň značky nebo modely aut",
            "jsou to zároveň jména českých měst",
        ],
    },
    {
        "id": "vlast-studene",
        "roof": "věci, které jsou na dotek studené i v teple",
        "level": "hard",
        "hidden": True,
        "inside": [
            "kov", "kámen", "dlaždice", "sklo", "zrcadlo", "klika", "mince",
            "keramika",
        ],
        "outside": [
            "dřevo", "vlna", "papír", "polštář", "deka", "koberec", "korek",
            "kabát", "ručník", "sláma",
        ],
        "asks": [
            "jsou na dotek studené i v teplé místnosti",
            "jsou to zároveň značky nebo modely aut",
            "jsou v názvech večerníčků",
            "mají v sobě dvě stejná písmena vedle sebe",
        ],
    },
    {
        "id": "vlast-natahnout",
        "roof": "věci, které se dají natáhnout",
        "level": "normal",
        "hidden": True,
        "inside": [
            "guma", "žvýkačka", "těsto", "pružina", "ponožka", "prak",
            "punčocha", "lano",
        ],
        "outside": [
            "sklo", "cihla", "klíč", "talíř", "prkno", "hřebík", "kámen",
            "sklenice", "lžíce", "zrcadlo",
        ],
        "asks": [
            "se dají natáhnout",
            "jsou to zároveň značky českého piva",
            "jsou v názvech her Járy Cimrmana",
            "jsou v názvech večerníčků",
        ],
    },
    {
        "id": "vlast-nuzky",
        "roof": "věci, které se dají přestřihnout nůžkami",
        "level": "normal",
        "hidden": True,
        "inside": [
            "papír", "látka", "provaz", "nit", "vlasy", "stuha", "fólie",
            "lepenka",
        ],
        "outside": [
            "drát", "plech", "sklo", "prkno", "cihla", "klíč", "kámen",
            "trubka", "hřebík", "dlaždice",
        ],
        "asks": [
            "se dají přestřihnout nůžkami",
            "jsou to zároveň jména českých měst",
            "jsou v názvech Shakespearových her",
            "jsou to znamení zvěrokruhu",
        ],
    },
    {
        "id": "vlast-toci",
        "roof": "věci, které se točí dokola",
        "level": "normal",
        "hidden": True,
        "inside": [
            "kolo", "vrtule", "gramodeska", "ruleta", "mlýn", "kolotoč",
            "zeměkoule", "setrvačník",
        ],
        "outside": [
            "žebřík", "police", "most", "plot", "koberec", "cihla", "lampa",
            "komín", "schod", "plaňka",
        ],
        "asks": [
            "se točí dokola",
            "jsou to zároveň značky českého piva",
            "jsou v názvech Shakespearových her",
            "nemají v sobě ani jednu samohlásku",
        ],
    },
    {
        "id": "vlast-pruzina",
        "roof": "věci, které mají v sobě pružinu",
        "level": "hard",
        "hidden": True,
        "inside": [
            "matrace", "propiska", "kolíček", "past", "hodinky", "trampolína",
            "váha", "zapalovač",
        ],
        "outside": [
            "talíř", "cihla", "sklenice", "koberec", "deka", "kniha", "hrnec",
            "žebřík", "mrkev", "ubrus",
        ],
        "asks": [
            "mají v sobě pružinu",
            "jsou to zároveň příjmení českých prezidentů",
            "jsou to zároveň značky českého piva",
            "jsou v názvech večerníčků",
        ],
    },
    {
        "id": "vlast-hrebik",
        "roof": "věci, které se věší na hřebík",
        "level": "normal",
        "hidden": True,
        "inside": [
            "obraz", "zrcadlo", "kalendář", "kabát", "hodiny", "klíče",
            "věnec", "ručník",
        ],
        "outside": [
            "koberec", "cihla", "sporák", "vana", "postel", "lednička",
            "gauč", "stůl", "kamna", "dlažba",
        ],
        "asks": [
            "se věší na hřebík",
            "jsou to zároveň značky nebo modely aut",
            "mají v sobě dvě stejná písmena vedle sebe",
            "mají v sobě schované zvíře",
        ],
    },
    {
        "id": "vlast-cinkaji",
        "roof": "věci, které chrastí nebo cinkají",
        "level": "normal",
        "hidden": True,
        "inside": [
            "rolnička", "klíče", "řetěz", "zvonek", "chrastítko", "mince",
            "náramek", "plechovka",
        ],
        "outside": [
            "polštář", "deka", "houba", "koberec", "kniha", "mrkev", "ručník",
            "papír", "provaz", "chleba",
        ],
        "asks": [
            "chrastí nebo cinkají",
            "jsou v názvech večerníčků",
            "mají v sobě schované zvíře",
            "jsou to zároveň příjmení českých prezidentů",
        ],
    },
]
