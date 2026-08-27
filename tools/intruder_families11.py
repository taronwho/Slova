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
            "bočnice", "kožka", "kyrys", "matrace", "moučnice", "násypka",
            "okulár", "rameno", "rukavice", "vozovka", "víko", "zrcátko",
        ],
        "asks": [
            "jsou to zároveň části stromu",
            "mají v sobě schované zvíře",
            "mají v sobě dvě stejná písmena vedle sebe",
            "jsou to zároveň značky českého piva",
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
            "celta", "kapsa", "kolík", "krajnice", "límec", "nos", "ostění",
            "ploška", "rošt", "sedlisko", "svodidlo", "záštita",
        ],
        "asks": [
            "jsou to zároveň části sudu",
            "jsou to znamení zvěrokruhu",
            "jsou v názvech Shakespearových her",
            "nemají v sobě ani jednu samohlásku",
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
            "hlavice", "hůl", "koleso", "list", "matrace", "měch", "pero",
            "ploška", "svodidlo", "vozovka", "víko", "čelo",
        ],
        "asks": [
            "jsou to zároveň části pluhu",
            "jsou v názvech Shakespearových her",
            "jsou to zároveň příjmení českých prezidentů",
            "jsou to zároveň jména českých měst",
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
            "běl", "břit", "dužina", "hlava", "hruška", "klín", "kmen",
            "list", "nos", "potah", "srdce", "čepec",
        ],
        "asks": [
            "jsou to zároveň části mlýna",
            "mají v sobě dvě stejná písmena vedle sebe",
            "jsou to zároveň příjmení českých prezidentů",
            "jsou to zároveň značky českého piva",
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
            "hlava", "hůl", "krojidlo", "letokruh", "list", "lýko",
            "moučnice", "náhon", "násep", "stolek", "zub", "zátka",
        ],
        "asks": [
            "jsou to zároveň části varhan",
            "jsou to znamení zvěrokruhu",
            "jsou v názvech večerníčků",
            "jsou v názvech her Járy Cimrmana",
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
            "kůra", "lopatka", "matrace", "okulár", "patka", "podbřišník",
            "přilba", "rozvod", "tyč", "třmen", "zub", "čepec",
        ],
        "asks": [
            "jsou to zároveň části bubnu",
            "mají v sobě dvě stejná písmena vedle sebe",
            "jsou to zároveň značky nebo modely aut",
            "jsou to znamení zvěrokruhu",
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
            "bočnice", "břit", "hruška", "list", "lýko", "nos", "náloketník",
            "násypka", "stahovák", "vozovka", "zátka", "čelo",
        ],
        "asks": [
            "jsou to zároveň části meče",
            "nemají v sobě ani jednu samohlásku",
            "jsou to zároveň značky nebo modely aut",
            "jsou to zároveň značky českého piva",
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
            "dužina", "klenba", "matrace", "nos", "odhrnovačka", "portál",
            "poutko", "rozvod", "slupice", "tubus", "zrcátko", "čelo",
        ],
        "asks": [
            "jsou to zároveň části brnění",
            "mají v sobě schované zvíře",
            "jsou to zároveň značky nebo modely aut",
            "jsou to zároveň značky českého piva",
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
            "hlava", "kapsa", "kostra", "límec", "moučnice", "nohy", "nos",
            "náloketník", "ostří", "plátno", "portál", "zub",
        ],
        "asks": [
            "jsou to zároveň části jezdeckého sedla",
            "jsou v názvech večerníčků",
            "jsou v názvech her Járy Cimrmana",
            "jsou to zároveň značky nebo modely aut",
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
            "běl", "celta", "dno", "manuál", "měch", "násada", "obrubník",
            "počva", "radlice", "stahovák", "víko", "čepec",
        ],
        "asks": [
            "jsou to zároveň části deštníku",
            "jsou v názvech večerníčků",
            "jsou to znamení zvěrokruhu",
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
            "dřeň", "hřídel", "letokruh", "odhrnovačka", "rameno", "ražba",
            "rejstřík", "stolek", "struník", "svodidlo", "čelba", "čelist",
        ],
        "asks": [
            "jsou to zároveň části zvonu",
            "jsou v názvech Shakespearových her",
            "mají v sobě schované zvíře",
            "jsou to znamení zvěrokruhu",
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
            "břit", "hřídel", "klín", "krojidlo", "podbřišník", "přilba",
            "příkop", "radlice", "rukavice", "traktura", "třmen", "věnec",
        ],
        "asks": [
            "jsou to zároveň části postele",
            "jsou to zároveň značky českého piva",
            "jsou v názvech Shakespearových her",
            "mají v sobě dvě stejná písmena vedle sebe",
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
            "běl", "břit", "jílec", "manuál", "nos", "náloketník", "násypka",
            "obrubník", "příkop", "radlice", "rameno", "rejstřík",
        ],
        "asks": [
            "jsou to zároveň části mikroskopu",
            "mají v sobě schované zvíře",
            "jsou to znamení zvěrokruhu",
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
            "blána", "břit", "dno", "hlavice", "hřídel", "jílec", "náhon",
            "tubus", "věnec", "čelist", "čepec", "čepel",
        ],
        "asks": [
            "jsou to zároveň části tunelu",
            "jsou v názvech her Járy Cimrmana",
            "jsou to znamení zvěrokruhu",
            "mají v sobě schované zvíře",
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
            "hlavice", "hůl", "kostra", "letokruh", "objektiv", "ostění",
            "ostří", "plátno", "portál", "potah", "píšťala", "rošt",
        ],
        "asks": [
            "jsou to zároveň části silnice",
            "nemají v sobě ani jednu samohlásku",
            "jsou to zároveň jména českých měst",
            "jsou to zároveň značky nebo modely aut",
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
            "blána", "kostra", "násypka", "objektiv", "ploška", "potah",
            "poutko", "píšťala", "sedlisko", "čelist", "čelo", "šroub",
        ],
        "asks": [
            "jsou to zároveň části pily",
            "jsou to zároveň značky českého piva",
            "jsou v názvech večerníčků",
            "mají v sobě dvě stejná písmena vedle sebe",
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
            "hruška", "hůl", "kámen", "límec", "matrace", "náhon", "násep",
            "sedlisko", "srdce", "stolek", "svodidlo", "traktura",
        ],
        "asks": [
            "jsou to zároveň části nůžek",
            "jsou to zároveň značky českého piva",
            "nemají v sobě ani jednu samohlásku",
            "jsou v názvech her Járy Cimrmana",
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
            "krajnice", "lopatka", "náholenice", "náloketník", "podlážka",
            "potah", "srdce", "tropiko", "tubus", "třmen", "větev", "čelba",
        ],
        "asks": [
            "jsou to zároveň části kladiva",
            "jsou to zároveň značky českého piva",
            "mají v sobě dvě stejná písmena vedle sebe",
            "mají v sobě schované zvíře",
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
            "dřeň", "hlavice", "kapsa", "kroužky", "límec", "nos", "objektiv",
            "podbřišník", "potah", "příkop", "sedlisko", "stolek",
        ],
        "asks": [
            "jsou to zároveň části stanu",
            "mají v sobě schované zvíře",
            "mají v sobě dvě stejná písmena vedle sebe",
            "čtou se stejně zepředu i zezadu",
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
            "břit", "hřídel", "krajnice", "letokruh", "lýko", "okulár",
            "patka", "potah", "zrcátko", "zátka", "záštita", "šroub",
        ],
        "asks": [
            "jsou to zároveň části batohu",
            "jsou v názvech her Járy Cimrmana",
            "mají v sobě dvě stejná písmena vedle sebe",
            "jsou to znamení zvěrokruhu",
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
            "destilát", "dořez", "krém", "loukoť", "model", "náboj",
            "nýtování", "piškot", "plech", "splétání", "závit", "šprušle",
        ],
        "asks": [
            "jsou to zároveň sklářské pojmy",
            "jsou v názvech her Járy Cimrmana",
            "jsou to zároveň značky českého piva",
            "mají v sobě schované zvíře",
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
            "dořez", "došek", "model", "poleva", "pramen", "pájka", "ryzost",
            "střep", "střívko", "výpalek", "šindel", "šídlo",
        ],
        "asks": [
            "jsou to zároveň mlynářské pojmy",
            "mají v sobě dvě stejná písmena vedle sebe",
            "jsou v názvech her Járy Cimrmana",
            "jsou to zároveň značky českého piva",
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
            "bobrovka", "filigrán", "forma", "kýta", "lišta", "ohýbačka",
            "plec", "surovina", "tavba", "vejražka", "úžlabí", "řemen",
        ],
        "asks": [
            "jsou to zároveň lihovarnické pojmy",
            "jsou v názvech večerníčků",
            "jsou to zároveň příjmení českých prezidentů",
            "jsou to znamení zvěrokruhu",
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
            "hřebenáč", "kvas", "kýta", "nálitek", "okap", "očko", "střívko",
            "tavba", "vejražka", "vysoká", "výpalek", "zápara",
        ],
        "asks": [
            "jsou to zároveň cukrářské pojmy",
            "jsou to zároveň příjmení českých prezidentů",
            "jsou to zároveň značky nebo modely aut",
            "jsou to znamení zvěrokruhu",
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
            "destilát", "došek", "forma", "krém", "nálitek", "odpich",
            "puncovní", "ryzost", "splétání", "svod", "zápich", "závit",
        ],
        "asks": [
            "jsou to zároveň řeznické pojmy",
            "jsou to zároveň příjmení českých prezidentů",
            "nemají v sobě ani jednu samohlásku",
            "jsou v názvech večerníčků",
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
            "destilát", "filigrán", "forma", "kvas", "kýta", "latě", "licí",
            "nálitek", "odpich", "pytlování", "přezka", "surovina",
        ],
        "asks": [
            "jsou to zároveň klempířské pojmy",
            "jsou to zároveň příjmení českých prezidentů",
            "jsou v názvech večerníčků",
            "jsou to znamení zvěrokruhu",
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
            "dokap", "drážkování", "konopí", "lem", "lišta", "náboj",
            "piškot", "složení", "svod", "výpalek", "zápara", "šídlo",
        ],
        "asks": [
            "jsou to zároveň pokrývačské pojmy",
            "nemají v sobě ani jednu samohlásku",
            "jsou to zároveň příjmení českých prezidentů",
            "jsou v názvech večerníčků",
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
            "destilát", "dokap", "marcipán", "opalování", "očko", "plec",
            "poleva", "pánev", "složení", "surovina", "šprušle", "šrot",
        ],
        "asks": [
            "jsou to zároveň zámečnické pojmy",
            "jsou to zároveň značky českého piva",
            "jsou to znamení zvěrokruhu",
            "jsou to zároveň příjmení českých prezidentů",
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
            "bourání", "dužina", "hřebenáč", "loukoť", "model", "ohýbačka",
            "okap", "pánev", "vejražka", "výsek", "úkap", "úžlabí",
        ],
        "asks": [
            "jsou to zároveň sedlářské pojmy",
            "mají v sobě schované zvíře",
            "jsou to zároveň značky nebo modely aut",
            "jsou v názvech Shakespearových her",
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
            "destilát", "huť", "kokila", "korpus", "nýtování", "otruby",
            "surovina", "svod", "vsázka", "vysoká", "výpalek", "šlehačka",
        ],
        "asks": [
            "jsou to zároveň kolářské pojmy",
            "jsou to znamení zvěrokruhu",
            "mají v sobě dvě stejná písmena vedle sebe",
            "jsou to zároveň jména českých měst",
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
            "brus", "dořez", "filigrán", "korpus", "kýta", "licí", "lůžko",
            "plech", "podšívka", "pájka", "stáčení", "svod",
        ],
        "asks": [
            "jsou to zároveň bednářské pojmy",
            "jsou to znamení zvěrokruhu",
            "mají v sobě schované zvíře",
            "čtou se stejně zepředu i zezadu",
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
            "drážkování", "kokila", "korpus", "kvas", "latě", "náboj",
            "střívko", "tavba", "vejražka", "výpalek", "zapuštění", "šídlo",
        ],
        "asks": [
            "jsou to zároveň provaznické pojmy",
            "nemají v sobě ani jednu samohlásku",
            "mají v sobě dvě stejná písmena vedle sebe",
            "jsou to zároveň značky nebo modely aut",
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
            "bourání", "dořez", "kokila", "korpus", "krupice", "krém", "licí",
            "odpich", "složení", "střep", "vysoká", "úkap",
        ],
        "asks": [
            "jsou to zároveň zlatnické pojmy",
            "jsou v názvech Shakespearových her",
            "mají v sobě dvě stejná písmena vedle sebe",
            "jsou v názvech večerníčků",
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
            "automatika", "bod", "depozitář", "lahev", "popiska", "skartace",
            "tinktura", "vrstva", "výběr", "výstup", "záměra", "zátěž",
        ],
        "asks": [
            "jsou to zároveň optické pojmy",
            "čtou se stejně zepředu i zezadu",
            "jsou to zároveň jména českých měst",
            "jsou to zároveň značky českého piva",
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
            "akvizice", "clona", "fond", "hals", "karton", "korunka",
            "recept", "sbírka", "tinktura", "vitrína", "výběr", "zátěž",
        ],
        "asks": [
            "jsou to zároveň geodetické pojmy",
            "nemají v sobě ani jednu samohlásku",
            "jsou to zároveň značky nebo modely aut",
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
            "badatelna", "fond", "hals", "maska", "mast", "obrat", "odchylka",
            "ploutve", "popiska", "převýšení", "výstup", "četnost",
        ],
        "asks": [
            "jsou to zároveň archeologické pojmy",
            "čtou se stejně zepředu i zezadu",
            "jsou to zároveň značky českého piva",
            "mají v sobě dvě stejná písmena vedle sebe",
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
            "bod", "clona", "depozitář", "hals", "hranol", "obrat", "plomba",
            "průměr", "převýšení", "rozptyl", "výběr", "čočka",
        ],
        "asks": [
            "jsou to zároveň archivní pojmy",
            "nemají v sobě ani jednu samohlásku",
            "jsou v názvech večerníčků",
            "mají v sobě schované zvíře",
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
            "clona", "hranol", "kýl", "lahev", "nález", "obrat", "otisk",
            "ploutve", "polygon", "skartace", "zrcadlo", "zátěž",
        ],
        "asks": [
            "jsou to zároveň muzejní pojmy",
            "jsou v názvech her Járy Cimrmana",
            "jsou v názvech večerníčků",
            "jsou to zároveň jména českých měst",
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
            "bourání", "destilát", "filigrán", "jádro", "nýtování",
            "opalování", "paprsek", "piškot", "plech", "podšívka", "ráf",
            "stahování",
        ],
        "asks": [
            "jsou to zároveň hutnické pojmy",
            "jsou to znamení zvěrokruhu",
            "čtou se stejně zepředu i zezadu",
            "jsou to zároveň příjmení českých prezidentů",
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
            "bobrovka", "dratev", "krupice", "krém", "lem", "ohýbačka",
            "očko", "piškot", "poleva", "výpalek", "výsek", "zápara",
        ],
        "asks": [
            "jsou to zároveň slévárenské pojmy",
            "jsou to zároveň značky českého piva",
            "jsou v názvech večerníčků",
            "nemají v sobě ani jednu samohlásku",
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
            "fond", "karton", "kurátor", "medián", "mohyla", "obrat",
            "plomba", "popiska", "střep", "výdej", "zrcadlo", "záměra",
        ],
        "asks": [
            "jsou to zároveň potápěčské pojmy",
            "jsou to zároveň jména českých měst",
            "jsou v názvech večerníčků",
            "mají v sobě dvě stejná písmena vedle sebe",
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
            "automatika", "bod", "lahev", "mast", "ploutve", "polygon",
            "popiska", "recept", "sbírka", "tinktura", "vrstva", "vrtačka",
        ],
        "asks": [
            "jsou to zároveň jachtařské pojmy",
            "jsou v názvech Shakespearových her",
            "nemají v sobě ani jednu samohlásku",
            "jsou to zároveň jména českých měst",
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
            "bod", "clona", "depozitář", "kosatka", "odchylka", "plomba",
            "převýšení", "rozptyl", "ráhno", "sbírka", "skartace", "vrstva",
        ],
        "asks": [
            "jsou to zároveň lékárnické pojmy",
            "jsou to znamení zvěrokruhu",
            "čtou se stejně zepředu i zezadu",
            "jsou to zároveň příjmení českých prezidentů",
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
            "automatika", "datace", "hals", "mohyla", "nález", "ploutve",
            "polygon", "převýšení", "skartace", "sonda", "vitrína", "výběr",
        ],
        "asks": [
            "jsou to zároveň zubařské pojmy",
            "jsou to zároveň jména českých měst",
            "jsou to zároveň značky nebo modely aut",
            "mají v sobě dvě stejná písmena vedle sebe",
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
            "akvizice", "datace", "hals", "korunka", "kurátor", "lahev",
            "můstek", "otisk", "polygon", "signatura", "výdej", "zrcadlo",
        ],
        "asks": [
            "jsou to zároveň statistické pojmy",
            "mají v sobě dvě stejná písmena vedle sebe",
            "čtou se stejně zepředu i zezadu",
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
            "deník", "dům", "faunovo", "kniha", "luisa", "pohádky", "růženka",
            "stůl", "tesák", "třída", "vzpomínky", "šípková",
        ],
        "asks": [
            "jsou v názvech knih Vladislava Vančury",
            "mají v sobě schované zvíře",
            "jsou to zároveň značky českého piva",
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
            "bylo", "chuďas", "dobrodružství", "faunovo", "luk", "město",
            "ovoce", "sedmikrásky", "statečný", "stromy", "vesmír", "yankee",
        ],
        "asks": [
            "jsou v názvech knih Josefa Lady",
            "mají v sobě schované zvíře",
            "čtou se stejně zepředu i zezadu",
            "nemají v sobě ani jednu samohlásku",
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
            "chuďas", "deník", "dobrodružství", "dům", "kniha", "luk", "oheň",
            "pole", "vzpomínky", "útěk", "šípková", "žabák",
        ],
        "asks": [
            "jsou v názvech knih Ericha Kästnera",
            "jsou to zároveň značky nebo modely aut",
            "nemají v sobě ani jednu samohlásku",
            "jsou v názvech Shakespearových her",
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
            "faunovo", "hvězdy", "labuť", "lesk", "liška", "luk", "město",
            "pasti", "pohádky", "sedmikrásky", "statečný", "třída",
        ],
        "asks": [
            "jsou v názvech knih Marka Twaina",
            "jsou to zároveň jména českých měst",
            "jsou to zároveň značky českého piva",
            "čtou se stejně zepředu i zezadu",
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
            "chuďas", "jezero", "kámen", "labuť", "lesk", "lotka", "muž",
            "ovoce", "pohádky", "růženka", "třída", "žabák",
        ],
        "asks": [
            "jsou v názvech knih Jacka Londona",
            "jsou to znamení zvěrokruhu",
            "mají v sobě schované zvíře",
            "jsou to zároveň značky českého piva",
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
            "bod", "divočina", "konec", "labuť", "luisa", "léto", "oči",
            "tesák", "volání", "vzpomínky", "zabijáci", "útěk",
        ],
        "asks": [
            "jsou v názvech knih Rudyarda Kiplinga",
            "čtou se stejně zepředu i zezadu",
            "nemají v sobě ani jednu samohlásku",
            "jsou to znamení zvěrokruhu",
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
            "královna", "louskáček", "odysea", "ovoce", "oči", "pole",
            "růženka", "sedmikrásky", "světlo", "vesmír", "vlk", "šípková",
        ],
        "asks": [
            "jsou v názvech knih Karla Poláčka",
            "jsou to zároveň jména českých měst",
            "jsou v názvech her Járy Cimrmana",
            "jsou v názvech večerníčků",
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
            "bod", "bylo", "deník", "jezero", "kmotra", "lesk", "louskáček",
            "luk", "odysea", "vlk", "volání", "vzpomínky",
        ],
        "asks": [
            "jsou v názvech filmů Věry Chytilové",
            "jsou v názvech Shakespearových her",
            "jsou to zároveň příjmení českých prezidentů",
            "jsou to zároveň značky nebo modely aut",
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
            "chuďas", "dobrodružství", "dvůr", "faunovo", "kmotra", "konec",
            "královna", "labuť", "město", "pekař", "tulák", "útěk",
        ],
        "asks": [
            "jsou v názvech filmů Stanleyho Kubricka",
            "jsou to zároveň jména českých měst",
            "jsou to zároveň značky nebo modely aut",
            "jsou v názvech večerníčků",
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
            "chuďas", "džungle", "faunovo", "kalamita", "kmotra", "mikeš",
            "město", "pekař", "pole", "sláva", "třída", "vesmír",
        ],
        "asks": [
            "jsou v názvech slavných baletů",
            "jsou v názvech Shakespearových her",
            "mají v sobě dvě stejná písmena vedle sebe",
            "nemají v sobě ani jednu samohlásku",
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
            "Říp", "Blaník", "Kleť", "Radhošť", "Ještěd", "Bezděz", "Boubín",
            "Sněžník",
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
            "Krakov", "Lodž", "Lublin", "Gdaňsk", "Szeged", "Pécs",
            "Debrecín", "Miskolc",
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
            "Hamburk", "Lyon", "Miláno", "Porto", "Rotterdam", "Bergen",
            "Antverpy", "Bilbao",
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
            "Bohumil", "Dalibor", "Květoslav", "Vlastimil", "Miloš",
            "Radovan", "Slavoj", "Zbyněk",
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
            "Abrahám", "Izák", "Mojžíš", "Áron", "David", "Šalomoun",
            "Daniel", "Samson",
        ],
        "asks": [
            "jsou to zároveň jména apoštolů",
            "mají v sobě schované zvíře",
            "jsou to zároveň jména českých měst",
            "jsou to znamení zvěrokruhu",
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
            "Williams", "Konference", "Boscova", "Špendlík", "Blumka",
            "Renkloda", "Karlatka", "Durancie",
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
            "Áres", "Hádes", "Hermés", "Merkur", "Vulkán", "Neptun",
            "Apollón", "Dionýsos",
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
            "Božena", "Vlasta", "Jarmila", "Ludmila", "Květa", "Blažena",
            "Radka", "Zdena",
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
            "Vega", "Sirius", "Antares", "Rigel", "Betelgeuze", "Aldebaran",
            "Deneb", "Polárka",
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
            "Juno", "Minerva", "Diana", "Ceres", "Vesta", "Flora", "Fortuna",
            "Aurora",
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
            "bříza", "dub", "smrk", "borovice", "javor", "lípa", "vrba",
            "jasan", "kaštan", "akát", "kopretina", "sněženka", "tulipán",
            "narcis", "pivoňka", "chrpa",
        ],
        "asks": [
            "jsou to zároveň kuchyňské bylinky",
            "jsou to zároveň příjmení českých prezidentů",
            "jsou to zároveň značky českého piva",
            "čtou se stejně zepředu i zezadu",
        ],
    },
]
