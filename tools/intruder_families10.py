"""Desátá várka rodin — sto skrytých střech.

TENHLE SOUBOR PÍŠE SKRIPT. Ruční úpravy zmizí při dalším spuštění; opravovat
se má `tools/gen_families10.py`, kde stojí zadání i kontroly.

Rodiny s pravidlem o písmenech (slabikotvorné r, koncovka -tel, háčky,
kroužek, useknuté první písmeno) prošly strojem: každé slovo uvnitř pravidlu
vyhovuje a žádné slovo vně mu nevyhovuje. U ostatních rodin stojí slova vně
schválně ze stejného soudku jako slova uvnitř, aby osa nesklouzla na
„čtyři jsou ptáci".
"""

FAMILIES10 = [
    {
        "id": "v10-ucho",
        "roof": "věci, které mají ucho",
        "level": "normal",
        "hidden": True,
        "inside": [
            "jehla", "hrnec", "konev", "džbán", "taška", "kabelka", "kotel",
            "šálek",
        ],
        "outside": [
            "kniha", "lampa", "koberec", "prkno", "deka", "mýdlo", "sešit",
            "ručník", "provaz", "cihla", "svíčka", "zrcadlo",
        ],
        "asks": [
            "mají ucho, i když neslyší",
            "jsou to znamení zvěrokruhu",
            "jsou to zároveň značky českého piva",
            "jsou to zároveň příjmení českých prezidentů",
        ],
    },
    {
        "id": "v10-zuby",
        "roof": "věci, které mají zuby",
        "level": "normal",
        "hidden": True,
        "inside": [
            "hřeben", "pila", "hrábě", "vidlička", "klíč", "zip",
        ],
        "outside": [
            "lžíce", "deka", "míč", "provaz", "houba", "mýdlo", "ručník",
            "polštář", "sklenice", "svíčka", "koberec", "kniha",
        ],
        "asks": [
            "mají zuby, i když nic nejedí",
            "jsou to znamení zvěrokruhu",
            "mají v sobě dvě stejná písmena vedle sebe",
            "mají v sobě schované zvíře",
        ],
    },
    {
        "id": "v10-noha",
        "roof": "věci, které mají nohu",
        "level": "normal",
        "hidden": True,
        "inside": [
            "stůl", "židle", "postel", "houba", "klavír", "sklenka",
            "kružítko", "pohár",
        ],
        "outside": [
            "koberec", "deka", "kniha", "zrcadlo", "obraz", "hrnec", "koště",
            "mýdlo", "ručník", "provaz",
        ],
        "asks": [
            "mají nohu, i když nechodí",
            "jsou to zároveň značky nebo modely aut",
            "jsou v názvech večerníčků",
            "jsou v názvech her Járy Cimrmana",
        ],
    },
    {
        "id": "v10-jazyk",
        "roof": "věci, které mají jazyk",
        "level": "hard",
        "hidden": True,
        "inside": [
            "bota", "zvon", "plamen", "ledovec", "hoblík", "váha",
        ],
        "outside": [
            "čepice", "deka", "hrnec", "sešit", "lampa", "koberec", "klíč",
            "mýdlo", "provaz", "kniha",
        ],
        "asks": [
            "mají jazyk, i když nemluví",
            "jsou v názvech večerníčků",
            "jsou to zároveň značky nebo modely aut",
            "jsou to zároveň značky českého piva",
        ],
    },
    {
        "id": "v10-oko",
        "roof": "věci, které mají oko",
        "level": "hard",
        "hidden": True,
        "inside": [
            "síť", "polévka", "brambora", "řetěz", "bouře", "punčocha",
        ],
        "outside": [
            "cihla", "deka", "kniha", "lampa", "hrnec", "sešit", "mýdlo",
            "koště", "ručník", "židle",
        ],
        "asks": [
            "mají oko, i když nevidí",
            "jsou to znamení zvěrokruhu",
            "jsou to zároveň značky nebo modely aut",
            "jsou v názvech her Járy Cimrmana",
        ],
    },
    {
        "id": "v10-hlava",
        "roof": "věci, které mají hlavu",
        "level": "normal",
        "hidden": True,
        "inside": [
            "hřebík", "špendlík", "zelí", "česnek", "kladivo", "šroub",
        ],
        "outside": [
            "deka", "kniha", "lampa", "koberec", "hrnec", "ručník", "mýdlo",
            "sešit", "provaz", "sklenice",
        ],
        "asks": [
            "mají hlavu, i když nemají tělo",
            "jsou v názvech her Járy Cimrmana",
            "jsou to zároveň značky českého piva",
            "mají v sobě dvě stejná písmena vedle sebe",
        ],
    },
    {
        "id": "v10-kridla",
        "roof": "věci, které mají křídlo",
        "level": "hard",
        "hidden": True,
        "inside": [
            "dveře", "okno", "nos", "oltář", "vojsko", "budova",
        ],
        "outside": [
            "stůl", "kniha", "hrnec", "deka", "lampa", "koberec", "mýdlo",
            "sešit", "provaz", "kbelík",
        ],
        "asks": [
            "mají křídlo, i když nelétají",
            "jsou v názvech večerníčků",
            "jsou to zároveň jména českých měst",
            "jsou v názvech Shakespearových her",
        ],
    },
    {
        "id": "v10-tezky",
        "roof": "slova, která tvoří spojení se slovem těžký",
        "level": "normal",
        "hidden": True,
        "inside": [
            "váha", "kalibr", "srdce", "průmysl", "kov", "atletika",
        ],
        "outside": [
            "sešit", "koště", "ubrus", "rohožka", "propiska", "záclona",
            "houpačka", "tácek", "ramínko", "ubrousek",
        ],
        "asks": [
            "tvoří se slovem těžký ustálené spojení",
            "jsou to zároveň jména českých měst",
            "čtou se stejně zepředu i zezadu",
            "nemají v sobě ani jednu samohlásku",
        ],
    },
    {
        "id": "v10-horky",
        "roof": "slova, která tvoří spojení se slovem horký",
        "level": "normal",
        "hidden": True,
        "inside": [
            "linka", "brambor", "hlava", "kandidát", "novinka", "půda",
            "čokoláda",
        ],
        "outside": [
            "sešit", "koště", "ubrus", "rohožka", "propiska", "záclona",
            "houpačka", "tácek", "ramínko", "ubrousek",
        ],
        "asks": [
            "tvoří se slovem horký ustálené spojení",
            "jsou v názvech her Járy Cimrmana",
            "jsou to zároveň příjmení českých prezidentů",
            "jsou v názvech Shakespearových her",
        ],
    },
    {
        "id": "v10-slepy",
        "roof": "slova, která tvoří spojení se slovem slepý",
        "level": "normal",
        "hidden": True,
        "inside": [
            "ulička", "mapa", "střevo", "kolej", "pasažér", "rameno",
            "skvrna", "bába",
        ],
        "outside": [
            "sešit", "koště", "ubrus", "rohožka", "propiska", "záclona",
            "houpačka", "tácek", "ramínko", "ubrousek",
        ],
        "asks": [
            "tvoří se slovem slepý ustálené spojení",
            "jsou to zároveň značky českého piva",
            "mají v sobě schované zvíře",
            "jsou to zároveň značky nebo modely aut",
        ],
    },
    {
        "id": "v10-mrtvy",
        "roof": "slova, která tvoří spojení se slovem mrtvý",
        "level": "hard",
        "hidden": True,
        "inside": [
            "bod", "moře", "úhel", "sezona", "jazyk", "brouk",
        ],
        "outside": [
            "sešit", "koště", "ubrus", "rohožka", "propiska", "záclona",
            "houpačka", "tácek", "ramínko", "ubrousek",
        ],
        "asks": [
            "tvoří se slovem mrtvý ustálené spojení",
            "mají v sobě schované zvíře",
            "jsou to zároveň příjmení českých prezidentů",
            "jsou v názvech večerníčků",
        ],
    },
    {
        "id": "v10-sedy",
        "roof": "slova, která tvoří spojení se slovem šedý",
        "level": "hard",
        "hidden": True,
        "inside": [
            "zóna", "eminence", "kůra", "zákal", "ekonomika", "myš",
        ],
        "outside": [
            "sešit", "koště", "ubrus", "rohožka", "propiska", "záclona",
            "houpačka", "tácek", "ramínko", "ubrousek",
        ],
        "asks": [
            "tvoří se slovem šedý ustálené spojení",
            "nemají v sobě ani jednu samohlásku",
            "čtou se stejně zepředu i zezadu",
            "jsou v názvech večerníčků",
        ],
    },
    {
        "id": "v10-tvrdy",
        "roof": "slova, která tvoří spojení se slovem tvrdý",
        "level": "normal",
        "hidden": True,
        "inside": [
            "oříšek", "disk", "měna", "voda", "chleba", "spoluhláska",
            "alkohol",
        ],
        "outside": [
            "sešit", "koště", "ubrus", "rohožka", "propiska", "záclona",
            "houpačka", "tácek", "ramínko", "ubrousek",
        ],
        "asks": [
            "tvoří se slovem tvrdý ustálené spojení",
            "mají v sobě schované zvíře",
            "čtou se stejně zepředu i zezadu",
            "jsou to zároveň značky nebo modely aut",
        ],
    },
    {
        "id": "v10-kovarna",
        "roof": "kovářské pojmy",
        "level": "hard",
        "hidden": True,
        "inside": [
            "výheň", "kovadlina", "měch", "podkova", "kalení", "okuje",
            "výkovek",
        ],
        "outside": [
            "komoda", "kompost", "koš", "matrace", "metr", "mísa", "nůžky",
            "peněženka", "police", "prostěradlo", "silnice", "sklenice",
            "stůl", "truhlík", "šála",
        ],
        "asks": [
            "jsou to zároveň kovářské pojmy",
            "jsou to zároveň značky českého piva",
            "nemají v sobě ani jednu samohlásku",
            "jsou v názvech večerníčků",
        ],
    },
    {
        "id": "v10-hasici",
        "roof": "hasičské pojmy",
        "level": "hard",
        "hidden": True,
        "inside": [
            "proudnice", "savice", "hydrant", "stříkačka", "rozdělovač",
            "zásah", "útok",
        ],
        "outside": [
            "bunda", "hadr", "hrnec", "kastrol", "koberec", "kolík",
            "peněženka", "postel", "propiska", "pytel", "ubrus", "vana",
            "vysavač", "zahrada", "žehlička",
        ],
        "asks": [
            "jsou to zároveň hasičské pojmy",
            "jsou to zároveň příjmení českých prezidentů",
            "jsou to zároveň značky českého piva",
            "jsou to zároveň značky nebo modely aut",
        ],
    },
    {
        "id": "v10-truhlarna",
        "roof": "truhlářské pojmy",
        "level": "hard",
        "hidden": True,
        "inside": [
            "dláto", "dýha", "rašple", "čep", "hobliny", "fládr",
        ],
        "outside": [
            "chleba", "houpačka", "hřeben", "kolík", "konev", "lavička",
            "myčka", "mýdlo", "peřina", "propiska", "silnice", "smeták",
            "struhadlo", "sud", "tácek",
        ],
        "asks": [
            "jsou to zároveň truhlářské pojmy",
            "jsou v názvech večerníčků",
            "čtou se stejně zepředu i zezadu",
            "jsou to zároveň značky českého piva",
        ],
    },
    {
        "id": "v10-astronomie",
        "roof": "astronomické pojmy",
        "level": "hard",
        "hidden": True,
        "inside": [
            "mlhovina", "zákryt", "opozice", "fáze", "dráha", "hvězdokupa",
            "úplněk",
        ],
        "outside": [
            "brambora", "bunda", "deštník", "hoblík", "hrneček", "hřeben",
            "kladívko", "koberec", "kompost", "krém", "peněženka", "provaz",
            "sešit", "skříň", "sporák",
        ],
        "asks": [
            "jsou to zároveň astronomické pojmy",
            "jsou to zároveň značky nebo modely aut",
            "mají v sobě dvě stejná písmena vedle sebe",
            "jsou to zároveň jména českých měst",
        ],
    },
    {
        "id": "v10-geologie",
        "roof": "geologické pojmy",
        "level": "hard",
        "hidden": True,
        "inside": [
            "vrstva", "zlom", "žíla", "kra", "výchoz", "souvrství", "nános",
        ],
        "outside": [
            "hoblík", "hodinky", "houpačka", "kbelík", "koš", "lopata",
            "pekáč", "podnos", "popelnice", "pytel", "sešit", "silnice",
            "stůl", "truhlík", "ubrousek",
        ],
        "asks": [
            "jsou to zároveň geologické pojmy",
            "čtou se stejně zepředu i zezadu",
            "nemají v sobě ani jednu samohlásku",
            "jsou to znamení zvěrokruhu",
        ],
    },
    {
        "id": "v10-zemedelstvi",
        "roof": "zemědělské pojmy",
        "level": "normal",
        "hidden": True,
        "inside": [
            "brázda", "úhor", "osivo", "strniště", "mez", "orba", "hnojivo",
        ],
        "outside": [
            "hadr", "houpačka", "kolík", "koš", "koště", "matice",
            "ořezávátko", "police", "polštář", "rohožka", "stůl", "vana",
            "záclona", "šuplík", "žehlička",
        ],
        "asks": [
            "jsou to zároveň zemědělské pojmy",
            "nemají v sobě ani jednu samohlásku",
            "jsou v názvech Shakespearových her",
            "jsou to znamení zvěrokruhu",
        ],
    },
    {
        "id": "v10-serm",
        "roof": "šermířské pojmy",
        "level": "hard",
        "hidden": True,
        "inside": [
            "výpad", "kryt", "sek", "čepel", "garda", "kord",
        ],
        "outside": [
            "hadr", "hoblík", "kartáček", "kladívko", "naběračka", "nůžky",
            "parapet", "rohožka", "semínko", "sporák", "struhadlo", "utěrka",
            "zápisník", "řetízek", "žebřík",
        ],
        "asks": [
            "jsou to zároveň šermířské pojmy",
            "čtou se stejně zepředu i zezadu",
            "jsou to znamení zvěrokruhu",
            "jsou v názvech her Járy Cimrmana",
        ],
    },
    {
        "id": "v10-kvet",
        "roof": "části květu",
        "level": "hard",
        "hidden": True,
        "inside": [
            "kalich", "koruna", "tyčinka", "blizna", "čnělka", "pestík",
            "semeník", "stopka",
        ],
        "outside": [
            "chleba", "deka", "hrneček", "komoda", "koště", "mrkev", "podnos",
            "pračka", "prostěradlo", "rohožka", "semínko", "silnice",
            "smeták", "stůl", "šála",
        ],
        "asks": [
            "jsou to zároveň části květu",
            "jsou to zároveň příjmení českých prezidentů",
            "jsou to zároveň jména českých měst",
            "jsou to zároveň značky nebo modely aut",
        ],
    },
    {
        "id": "v10-zub",
        "roof": "části zubu",
        "level": "hard",
        "hidden": True,
        "inside": [
            "korunka", "krček", "kořen", "sklovina", "dřeň", "cement",
        ],
        "outside": [
            "batoh", "hadr", "kabát", "lepidlo", "mísa", "nůžky", "polštář",
            "ponožka", "rýč", "struhadlo", "sud", "sušák", "trakař",
            "ubrousek", "šála",
        ],
        "asks": [
            "jsou to zároveň části zubu",
            "jsou to zároveň značky nebo modely aut",
            "mají v sobě dvě stejná písmena vedle sebe",
            "jsou to znamení zvěrokruhu",
        ],
    },
    {
        "id": "v10-houba-casti",
        "roof": "části houby",
        "level": "normal",
        "hidden": True,
        "inside": [
            "klobouk", "třeň", "plodnice", "podhoubí", "výtrusy", "lupeny",
        ],
        "outside": [
            "batoh", "brýle", "bunda", "hadice", "lepidlo", "lopatka",
            "motyka", "ponožka", "pouzdro", "pytel", "sklenice", "sporák",
            "utěrka", "zápisník", "řetízek",
        ],
        "asks": [
            "jsou to zároveň části houby",
            "jsou to zároveň značky českého piva",
            "jsou to zároveň značky nebo modely aut",
            "jsou to znamení zvěrokruhu",
        ],
    },
    {
        "id": "v10-kytara",
        "roof": "části kytary",
        "level": "normal",
        "hidden": True,
        "inside": [
            "krk", "kobylka", "pražec", "struna", "hlavice", "sedlo",
        ],
        "outside": [
            "kleště", "lednička", "naběračka", "náramek", "nůžky", "podnos",
            "police", "pravítko", "schránka", "skříň", "utěrka", "vana",
            "vařečka", "šuplík", "šála",
        ],
        "asks": [
            "jsou to zároveň části kytary",
            "jsou to zároveň značky nebo modely aut",
            "mají v sobě schované zvíře",
            "jsou to zároveň jména českých měst",
        ],
    },
    {
        "id": "v10-kamna",
        "roof": "části kamen",
        "level": "normal",
        "hidden": True,
        "inside": [
            "rošt", "popelník", "dvířka", "komín", "tah", "plotna",
        ],
        "outside": [
            "brambora", "bunda", "hadice", "hadr", "kleště", "krém",
            "lopatka", "mýdlo", "pinzeta", "postel", "pračka", "prostěradlo",
            "smeták", "sušák", "zahrada",
        ],
        "asks": [
            "jsou to zároveň části kamen",
            "čtou se stejně zepředu i zezadu",
            "jsou to zároveň příjmení českých prezidentů",
            "jsou to znamení zvěrokruhu",
        ],
    },
    {
        "id": "v10-most",
        "roof": "části mostu",
        "level": "hard",
        "hidden": True,
        "inside": [
            "pilíř", "oblouk", "pole", "opěra", "mostovka", "zábradlí",
        ],
        "outside": [
            "deka", "deštník", "hoblík", "hrnec", "kabát", "kartáček",
            "matrace", "pinzeta", "plot", "pytel", "sušák", "tácek",
            "zápisník", "řetízek", "žehlička",
        ],
        "asks": [
            "jsou to zároveň části mostu",
            "jsou to zároveň příjmení českých prezidentů",
            "jsou to zároveň jména českých měst",
            "čtou se stejně zepředu i zezadu",
        ],
    },
    {
        "id": "v10-kniha-casti",
        "roof": "části knihy",
        "level": "normal",
        "hidden": True,
        "inside": [
            "hřbet", "desky", "vazba", "obálka", "kapitola", "rejstřík",
            "předsádka",
        ],
        "outside": [
            "hadice", "hadr", "hřeben", "kýbl", "metr", "peřina", "popelnice",
            "propiska", "semínko", "sporák", "sud", "trouba", "ubrousek",
            "záclona", "žehlička",
        ],
        "asks": [
            "jsou to zároveň části knihy",
            "jsou to znamení zvěrokruhu",
            "jsou v názvech her Járy Cimrmana",
            "mají v sobě dvě stejná písmena vedle sebe",
        ],
    },
    {
        "id": "v10-pojisteni",
        "roof": "pojišťovací pojmy",
        "level": "hard",
        "hidden": True,
        "inside": [
            "pojistka", "škoda", "plnění", "riziko", "spoluúčast", "smlouva",
        ],
        "outside": [
            "deštník", "dřez", "hoblík", "hodinky", "hřebík", "koberec",
            "květináč", "myčka", "parapet", "plot", "polštář", "propiska",
            "prostěradlo", "rýč", "sud",
        ],
        "asks": [
            "jsou to zároveň pojišťovací pojmy",
            "jsou v názvech her Járy Cimrmana",
            "jsou to zároveň jména českých měst",
            "jsou v názvech večerníčků",
        ],
    },
    {
        "id": "v10-ucetnictvi",
        "roof": "účetní pojmy",
        "level": "hard",
        "hidden": True,
        "inside": [
            "rozvaha", "saldo", "obrat", "závazek", "zisk", "položka",
        ],
        "outside": [
            "batoh", "guma", "hřeben", "kabát", "kastrol", "lampa", "matice",
            "parapet", "popelnice", "postel", "ramínko", "silnice", "stůl",
            "svěrák", "truhlík",
        ],
        "asks": [
            "jsou to zároveň účetní pojmy",
            "jsou v názvech večerníčků",
            "jsou to zároveň jména českých měst",
            "jsou to zároveň značky nebo modely aut",
        ],
    },
    {
        "id": "v10-lukostrelba",
        "roof": "lukostřelecké pojmy",
        "level": "normal",
        "hidden": True,
        "inside": [
            "tětiva", "terč", "hrot", "opeření", "toulec", "nátah",
        ],
        "outside": [
            "branka", "bunda", "kabát", "lednička", "myčka", "náramek",
            "peněženka", "pilník", "pinzeta", "police", "polštář", "pouzdro",
            "sušák", "zahrada", "šuplík",
        ],
        "asks": [
            "jsou to zároveň lukostřelecké pojmy",
            "jsou to zároveň jména českých měst",
            "mají v sobě schované zvíře",
            "jsou v názvech večerníčků",
        ],
    },
    {
        "id": "v10-filatelie",
        "roof": "filatelistické pojmy",
        "level": "hard",
        "hidden": True,
        "inside": [
            "známka", "zoubkování", "přetisk", "arch", "aršík", "obtisk",
        ],
        "outside": [
            "houpačka", "hřeben", "hřebík", "kabát", "kastrol", "kladívko",
            "lavička", "pinzeta", "pouzdro", "ramínko", "sklenice",
            "struhadlo", "trakař", "utěrka", "vysavač",
        ],
        "asks": [
            "jsou to zároveň filatelistické pojmy",
            "nemají v sobě ani jednu samohlásku",
            "jsou to zároveň příjmení českých prezidentů",
            "jsou to zároveň značky českého piva",
        ],
    },
    {
        "id": "v10-elektro",
        "roof": "elektrotechnické pojmy",
        "level": "hard",
        "hidden": True,
        "inside": [
            "vodič", "jistič", "zkrat", "uzemnění", "svorka", "cívka",
        ],
        "outside": [
            "brambora", "branka", "deka", "hrábě", "kbelík", "kolík",
            "kompost", "lopata", "náramek", "pravítko", "prostěradlo",
            "semínko", "sušák", "trakař", "šroub",
        ],
        "asks": [
            "jsou to zároveň elektrotechnické pojmy",
            "jsou to znamení zvěrokruhu",
            "nemají v sobě ani jednu samohlásku",
            "mají v sobě dvě stejná písmena vedle sebe",
        ],
    },
    {
        "id": "v10-mlekarna",
        "roof": "mlékárenské pojmy",
        "level": "hard",
        "hidden": True,
        "inside": [
            "syřidlo", "sýřenina", "podmáslí", "syrovátka", "zrání",
            "smetana",
        ],
        "outside": [
            "batoh", "branka", "hrábě", "kabát", "kladívko", "ořezávátko",
            "podnos", "ponožka", "ramínko", "ručník", "semínko", "sklenice",
            "sporák", "záclona", "šála",
        ],
        "asks": [
            "jsou to zároveň mlékárenské pojmy",
            "jsou to zároveň značky nebo modely aut",
            "mají v sobě dvě stejná písmena vedle sebe",
            "mají v sobě schované zvíře",
        ],
    },
    {
        "id": "v10-hornictvi",
        "roof": "hornické pojmy",
        "level": "hard",
        "hidden": True,
        "inside": [
            "šachta", "sloj", "štola", "výdřeva", "klec", "překop",
        ],
        "outside": [
            "guma", "hadr", "houpačka", "kleště", "konev", "koště", "lopatka",
            "myčka", "peřina", "ramínko", "ručník", "sklenice", "sud",
            "věšák", "šála",
        ],
        "asks": [
            "jsou to zároveň hornické pojmy",
            "nemají v sobě ani jednu samohlásku",
            "jsou v názvech her Járy Cimrmana",
            "jsou to zároveň příjmení českých prezidentů",
        ],
    },
    {
        "id": "v10-lazne",
        "roof": "české lázně",
        "level": "hard",
        "hidden": True,
        "inside": [
            "Teplice", "Poděbrady", "Jeseník", "Luhačovice", "Bechyně",
            "Darkov", "Bohdaneč", "Libverda",
        ],
        "outside": [
            "chleba", "guma", "nůžky", "pinzeta", "podnos", "pouzdro",
            "pračka", "ramínko", "semínko", "svěrák", "trouba", "tácek",
            "ubrus", "zahrada", "záclona",
        ],
        "asks": [
            "jsou to zároveň české lázně",
            "mají v sobě dvě stejná písmena vedle sebe",
            "nemají v sobě ani jednu samohlásku",
            "jsou to zároveň značky nebo modely aut",
        ],
    },
    {
        "id": "v10-chko",
        "roof": "chráněné krajinné oblasti",
        "level": "hard",
        "hidden": True,
        "inside": [
            "Pálava", "Blaník", "Beskydy", "Kokořínsko", "Broumovsko",
            "Poodří", "Křivoklátsko", "Žďársko",
        ],
        "outside": [
            "hoblík", "hrneček", "hřeben", "hřebík", "komoda", "matrace",
            "motyka", "postel", "pračka", "rohožka", "semínko", "tácek",
            "vrtačka", "šuplík", "žehlička",
        ],
        "asks": [
            "jsou to zároveň chráněné krajinné oblasti",
            "čtou se stejně zepředu i zezadu",
            "mají v sobě schované zvíře",
            "jsou to znamení zvěrokruhu",
        ],
    },
    {
        "id": "v10-slabikotvorne",
        "roof": "slova, ve kterých drží slabiku r nebo l",
        "level": "hard",
        "hidden": True,
        "inside": [
            "vrba", "slza", "srdce", "mlha", "brzda", "hrdlo", "krtek",
            "vlna", "prkno", "vrták",
        ],
        "outside": [
            "lampa", "kolo", "ruka", "sova", "malina", "police", "koleno",
            "motyka", "silnice", "konev",
        ],
        "asks": [
            "mají v sobě r nebo l, které drží celou slabiku",
            "jsou v názvech Shakespearových her",
            "jsou to zároveň jména českých měst",
            "jsou v názvech večerníčků",
        ],
    },
    {
        "id": "v10-tel",
        "roof": "slova končící na -tel",
        "level": "normal",
        "hidden": True,
        "inside": [
            "učitel", "ředitel", "spisovatel", "přítel", "kotel", "hotel",
            "majitel", "nositel",
        ],
        "outside": [
            "lampa", "koleno", "police", "sešit", "ubrus", "kbelík", "motyka",
            "konev", "kolík", "ručník",
        ],
        "asks": [
            "končí na písmena tel",
            "jsou v názvech her Járy Cimrmana",
            "mají v sobě schované zvíře",
            "mají v sobě dvě stejná písmena vedle sebe",
        ],
    },
    {
        "id": "v10-hacky",
        "roof": "slova s ď, ť nebo ň",
        "level": "normal",
        "hidden": True,
        "inside": [
            "kůň", "oheň", "loď", "zeď", "píseň", "dlaň", "síť", "poušť",
            "labuť",
        ],
        "outside": [
            "stůl", "lampa", "kniha", "koberec", "hrnec", "police", "sešit",
            "mýdlo", "provaz", "ručník",
        ],
        "asks": [
            "mají v sobě ď, ť nebo ň",
            "jsou to zároveň jména českých měst",
            "jsou to zároveň příjmení českých prezidentů",
            "mají v sobě dvě stejná písmena vedle sebe",
        ],
    },
    {
        "id": "v10-krouzek",
        "roof": "slova s kroužkovaným ů",
        "level": "normal",
        "hidden": True,
        "inside": [
            "stůl", "dům", "sůl", "vůz", "hůl", "kůže", "půda", "růže",
            "můra",
        ],
        "outside": [
            "police", "lampa", "koberec", "sešit", "hrnec", "konev", "motyka",
            "ručník", "kolík", "kbelík",
        ],
        "asks": [
            "mají v sobě ů s kroužkem",
            "jsou to zároveň příjmení českých prezidentů",
            "jsou v názvech her Járy Cimrmana",
            "jsou v názvech večerníčků",
        ],
    },
    {
        "id": "v10-bez-prvniho",
        "roof": "slova, ze kterých po useknutí prvního písmene zbude jiné slovo",
        "level": "hard",
        "hidden": True,
        "inside": [
            "mrak", "krok", "sled", "klín", "brod", "vlak", "kroj", "kluk",
            "klid", "kosa", "chlad", "krám",
        ],
        "outside": [
            "lampa", "police", "koberec", "sešit", "motyka", "konev",
            "ručník", "hrnec", "kbelík", "žebřík",
        ],
        "asks": [
            "po useknutí prvního písmene dají jiné slovo",
            "mají v sobě dvě stejná písmena vedle sebe",
            "jsou to zároveň značky českého piva",
            "jsou v názvech her Járy Cimrmana",
        ],
    },
    {
        "id": "v10-kvete-drive",
        "roof": "dřeviny, které kvetou dřív, než jim narostou listy",
        "level": "hard",
        "hidden": True,
        "inside": [
            "líska", "olše", "vrba", "dřín", "trnka", "topol", "jilm",
        ],
        "outside": [
            "lípa", "dub", "buk", "jeřáb", "akát", "bez", "kaštan", "hloh",
            "pámelník", "zimolez",
        ],
        "asks": [
            "kvetou dřív, než na nich narostou listy",
            "čtou se stejně zepředu i zezadu",
            "jsou to znamení zvěrokruhu",
            "jsou v názvech večerníčků",
        ],
    },
    {
        "id": "v10-tazni",
        "roof": "tažní ptáci",
        "level": "normal",
        "hidden": True,
        "inside": [
            "vlaštovka", "čáp", "špaček", "jiřička", "rorýs", "konipas",
            "kukačka", "slavík",
        ],
        "outside": [
            "vrabec", "sýkora", "straka", "havran", "sova", "datel", "brhlík",
            "holub", "koroptev", "bažant",
        ],
        "asks": [
            "odlétají na zimu do teplých krajů",
            "jsou v názvech her Járy Cimrmana",
            "jsou to zároveň jména českých měst",
            "nemají v sobě ani jednu samohlásku",
        ],
    },
    {
        "id": "v10-zimni-spanek",
        "roof": "zvířata, která spí zimní spánek",
        "level": "normal",
        "hidden": True,
        "inside": [
            "ježek", "plch", "sysel", "svišť", "netopýr", "křeček",
        ],
        "outside": [
            "liška", "srna", "zajíc", "veverka", "kuna", "jelen", "vlk",
            "rys",
        ],
        "asks": [
            "spí opravdový zimní spánek",
            "jsou to zároveň příjmení českých prezidentů",
            "jsou v názvech Shakespearových her",
            "mají v sobě schované zvíře",
        ],
    },
    {
        "id": "v10-svleka",
        "roof": "živočichové, kteří svlékají kůži",
        "level": "hard",
        "hidden": True,
        "inside": [
            "had", "ještěrka", "pavouk", "rak", "štír", "cikáda",
        ],
        "outside": [
            "ryba", "vrabec", "myš", "kočka", "netopýr", "ježek", "krtek",
            "veverka", "jelen", "srna",
        ],
        "asks": [
            "svlékají kůži",
            "jsou to zároveň značky nebo modely aut",
            "jsou to zároveň příjmení českých prezidentů",
            "nemají v sobě ani jednu samohlásku",
        ],
    },
    {
        "id": "v10-parazit",
        "roof": "organismy, které žijí na cizí úkor",
        "level": "hard",
        "hidden": True,
        "inside": [
            "klíště", "blecha", "veš", "jmelí", "tasemnice", "kukačka",
        ],
        "outside": [
            "včela", "mravenec", "motýl", "žížala", "slimák", "brouk",
            "pavouk", "dub", "kopřiva", "mech",
        ],
        "asks": [
            "žijí na úkor jiného živého tvora",
            "nemají v sobě ani jednu samohlásku",
            "mají v sobě dvě stejná písmena vedle sebe",
            "čtou se stejně zepředu i zezadu",
        ],
    },
    {
        "id": "v10-may",
        "roof": "slova z názvů knih Karla Maye",
        "level": "hard",
        "hidden": True,
        "inside": [
            "poklad", "jezero", "syn", "duch", "mustang", "princ", "lev",
            "odkaz",
        ],
        "outside": [
            "deštník", "hrneček", "kbelík", "lavička", "nůžky", "peřina",
            "podnos", "polštář", "sporák", "struhadlo", "stůl", "vařečka",
            "věšák", "zahrada", "šála",
        ],
        "asks": [
            "jsou v názvech knih Karla Maye",
            "jsou to zároveň příjmení českých prezidentů",
            "jsou to zároveň značky českého piva",
            "jsou v názvech her Járy Cimrmana",
        ],
    },
    {
        "id": "v10-havel",
        "roof": "slova z názvů her Václava Havla",
        "level": "hard",
        "hidden": True,
        "inside": [
            "slavnost", "audience", "vernisáž", "vyrozumění", "odcházení",
            "pokoušení", "spiklenci", "opera",
        ],
        "outside": [
            "brýle", "dřez", "hadr", "hřebík", "kabát", "lavička", "mrkev",
            "mýdlo", "pilník", "pinzeta", "ponožka", "popelnice", "postel",
            "tácek", "utěrka",
        ],
        "asks": [
            "jsou v názvech her Václava Havla",
            "jsou to znamení zvěrokruhu",
            "jsou v názvech večerníčků",
            "jsou to zároveň značky nebo modely aut",
        ],
    },
    {
        "id": "v10-kundera",
        "roof": "slova z názvů knih Milana Kundery",
        "level": "hard",
        "hidden": True,
        "inside": [
            "žert", "nesmrtelnost", "lehkost", "valčík", "nevědomost",
            "totožnost", "smích", "pomalost",
        ],
        "outside": [
            "guma", "hodinky", "hřebík", "kolík", "lepidlo", "metr",
            "polštář", "popelnice", "prostěradlo", "semínko", "sešit",
            "svěrák", "truhlík", "řetízek", "šála",
        ],
        "asks": [
            "jsou v názvech knih Milana Kundery",
            "jsou to zároveň příjmení českých prezidentů",
            "jsou v názvech večerníčků",
            "jsou to zároveň jména českých měst",
        ],
    },
    {
        "id": "v10-zeman",
        "roof": "slova z názvů filmů Karla Zemana",
        "level": "hard",
        "hidden": True,
        "inside": [
            "cesta", "pravěk", "vynález", "zkáza", "baron", "vzducholoď",
            "kronika",
        ],
        "outside": [
            "branka", "hodinky", "kartáček", "kastrol", "krém", "lopata",
            "matice", "pračka", "provaz", "skříň", "sporák", "stůl",
            "truhlík", "záclona", "šuplík",
        ],
        "asks": [
            "jsou v názvech filmů Karla Zemana",
            "jsou to zároveň značky českého piva",
            "jsou v názvech večerníčků",
            "mají v sobě schované zvíře",
        ],
    },
    {
        "id": "v10-chaplin",
        "roof": "slova z názvů Chaplinových filmů",
        "level": "hard",
        "hidden": True,
        "inside": [
            "světla", "velkoměsto", "doba", "opojení", "cirkus", "diktátor",
            "král", "rampa",
        ],
        "outside": [
            "batoh", "bunda", "houpačka", "hrábě", "komoda", "květináč",
            "motyka", "pilník", "police", "popelnice", "pouzdro", "rohožka",
            "skříň", "ubrousek", "šuplík",
        ],
        "asks": [
            "jsou v názvech Chaplinových filmů",
            "čtou se stejně zepředu i zezadu",
            "jsou to zároveň příjmení českých prezidentů",
            "mají v sobě schované zvíře",
        ],
    },
    {
        "id": "v10-dickens",
        "roof": "slova z názvů knih Charlese Dickense",
        "level": "hard",
        "hidden": True,
        "inside": [
            "koleda", "dům", "vyhlídky", "příběh", "časy", "kronika", "klub",
        ],
        "outside": [
            "batoh", "dřez", "hřebík", "kleště", "lampa", "lavička",
            "popelnice", "pračka", "rohožka", "smeták", "sporák", "trakař",
            "vana", "záclona", "šála",
        ],
        "asks": [
            "jsou v názvech knih Charlese Dickense",
            "nemají v sobě ani jednu samohlásku",
            "jsou to zároveň příjmení českých prezidentů",
            "jsou to zároveň značky nebo modely aut",
        ],
    },
    {
        "id": "v10-mucha",
        "roof": "slova z názvů obrazů Alfonse Muchy",
        "level": "hard",
        "hidden": True,
        "inside": [
            "jaro", "zima", "poezie", "tanec", "hvězda", "epopej",
        ],
        "outside": [
            "branka", "brýle", "hřeben", "kleště", "kolík", "matrace",
            "nůžky", "ořezávátko", "prostěradlo", "pytel", "sešit", "smeták",
            "sporák", "tácek", "vrtačka",
        ],
        "asks": [
            "jsou v názvech obrazů Alfonse Muchy",
            "nemají v sobě ani jednu samohlásku",
            "jsou to zároveň příjmení českých prezidentů",
            "jsou v názvech večerníčků",
        ],
    },
    {
        "id": "v10-menzel",
        "roof": "slova z názvů filmů Jiřího Menzela",
        "level": "hard",
        "hidden": True,
        "inside": [
            "skřivánci", "nit", "postřižiny", "slavnosti", "sněženky",
            "vesnička", "konec",
        ],
        "outside": [
            "brýle", "hadr", "kompost", "lampa", "matice", "mrkev", "náramek",
            "peněženka", "postel", "prostěradlo", "tácek", "vařečka",
            "zápisník", "šroub", "žehlička",
        ],
        "asks": [
            "jsou v názvech filmů Jiřího Menzela",
            "jsou v názvech večerníčků",
            "jsou to znamení zvěrokruhu",
            "mají v sobě dvě stejná písmena vedle sebe",
        ],
    },
    {
        "id": "v10-storch",
        "roof": "slova z názvů knih Eduarda Štorcha",
        "level": "hard",
        "hidden": True,
        "inside": [
            "lovci", "mamut", "osada", "havran", "bronz", "volání", "rod",
        ],
        "outside": [
            "batoh", "brambora", "chleba", "hodinky", "květináč", "metr",
            "mýdlo", "pekáč", "pinzeta", "pravítko", "semínko", "ubrousek",
            "vrtačka", "zápisník", "šroub",
        ],
        "asks": [
            "jsou v názvech knih Eduarda Štorcha",
            "jsou v názvech her Járy Cimrmana",
            "jsou v názvech Shakespearových her",
            "jsou v názvech večerníčků",
        ],
    },
    {
        "id": "v10-box",
        "roof": "boxerské pojmy",
        "level": "normal",
        "hidden": True,
        "inside": [
            "hák", "roh", "gong", "kolo", "provazy", "rukavice",
        ],
        "outside": [
            "hrnec", "hrábě", "koš", "lavička", "náramek", "nůžky", "ponožka",
            "pravítko", "pračka", "provaz", "ramínko", "rohožka", "truhlík",
            "věšák", "zahrada",
        ],
        "asks": [
            "jsou to zároveň boxerské pojmy",
            "jsou to zároveň jména českých měst",
            "jsou v názvech večerníčků",
            "jsou to zároveň příjmení českých prezidentů",
        ],
    },
    {
        "id": "v10-tenis",
        "roof": "tenisové pojmy",
        "level": "normal",
        "hidden": True,
        "inside": [
            "podání", "síť", "dvorec", "výhoda", "shoda", "čára",
        ],
        "outside": [
            "brýle", "deka", "dřez", "kabát", "koberec", "květináč",
            "lopatka", "myčka", "naběračka", "pinzeta", "police", "smeták",
            "vrtačka", "věšák", "řetízek",
        ],
        "asks": [
            "jsou to zároveň tenisové pojmy",
            "nemají v sobě ani jednu samohlásku",
            "jsou v názvech her Járy Cimrmana",
            "mají v sobě dvě stejná písmena vedle sebe",
        ],
    },
    {
        "id": "v10-skaut",
        "roof": "skautské pojmy",
        "level": "normal",
        "hidden": True,
        "inside": [
            "stezka", "slib", "družina", "oddíl", "uzel", "totem",
        ],
        "outside": [
            "guma", "koš", "lopatka", "motyka", "peřina", "podnos", "ponožka",
            "popelnice", "propiska", "prostěradlo", "svěrák", "trouba",
            "záclona", "šroub", "šuplík",
        ],
        "asks": [
            "jsou to zároveň skautské pojmy",
            "jsou to znamení zvěrokruhu",
            "jsou to zároveň značky nebo modely aut",
            "mají v sobě schované zvíře",
        ],
    },
    {
        "id": "v10-policie",
        "roof": "policejní pojmy",
        "level": "normal",
        "hidden": True,
        "inside": [
            "hlídka", "výslech", "stopa", "obušek", "cela", "pouta",
        ],
        "outside": [
            "branka", "hadr", "hodinky", "hřebík", "kabát", "kastrol",
            "kolík", "koš", "květináč", "lampa", "metr", "ponožka", "semínko",
            "trouba", "záclona",
        ],
        "asks": [
            "jsou to zároveň policejní pojmy",
            "nemají v sobě ani jednu samohlásku",
            "jsou v názvech večerníčků",
            "jsou v názvech her Járy Cimrmana",
        ],
    },
    {
        "id": "v10-heraldika",
        "roof": "heraldické pojmy",
        "level": "hard",
        "hidden": True,
        "inside": [
            "štít", "klenot", "přilba", "pole", "znak", "helma",
        ],
        "outside": [
            "batoh", "guma", "hadr", "hodinky", "hrábě", "lopata",
            "ořezávátko", "parapet", "podnos", "prostěradlo", "ručník",
            "silnice", "ubrus", "zápisník", "šála",
        ],
        "asks": [
            "jsou to zároveň heraldické pojmy",
            "mají v sobě dvě stejná písmena vedle sebe",
            "jsou to zároveň značky nebo modely aut",
            "jsou to zároveň značky českého piva",
        ],
    },
    {
        "id": "v10-burza",
        "roof": "burzovní pojmy",
        "level": "hard",
        "hidden": True,
        "inside": [
            "kurz", "medvěd", "býk", "propad", "akcie", "dividenda",
        ],
        "outside": [
            "chleba", "deštník", "dřez", "kastrol", "kolík", "koště", "lampa",
            "lepidlo", "náramek", "nůžky", "pilník", "pravítko", "struhadlo",
            "stůl", "utěrka",
        ],
        "asks": [
            "jsou to zároveň burzovní pojmy",
            "jsou to zároveň příjmení českých prezidentů",
            "jsou to zároveň značky českého piva",
            "mají v sobě dvě stejná písmena vedle sebe",
        ],
    },
    {
        "id": "v10-letiste",
        "roof": "letištní pojmy",
        "level": "normal",
        "hidden": True,
        "inside": [
            "brána", "pás", "věž", "odbavení", "plocha", "rukáv",
        ],
        "outside": [
            "hodinky", "koberec", "koš", "mrkev", "náramek", "podnos",
            "pouzdro", "silnice", "skříň", "stůl", "svěrák", "tácek",
            "utěrka", "záclona", "šuplík",
        ],
        "asks": [
            "jsou to zároveň letištní pojmy",
            "jsou to zároveň značky českého piva",
            "jsou to znamení zvěrokruhu",
            "mají v sobě schované zvíře",
        ],
    },
    {
        "id": "v10-hotel",
        "roof": "hotelové pojmy",
        "level": "normal",
        "hidden": True,
        "inside": [
            "recepce", "pokoj", "apartmá", "snídaně", "hvězdička", "lůžko",
        ],
        "outside": [
            "hoblík", "kabát", "kastrol", "kolík", "lepidlo", "mrkev",
            "naběračka", "nůžky", "ramínko", "svěrák", "tácek", "vana",
            "vařečka", "zápisník", "šroub",
        ],
        "asks": [
            "jsou to zároveň hotelové pojmy",
            "mají v sobě schované zvíře",
            "jsou v názvech večerníčků",
            "jsou to zároveň značky nebo modely aut",
        ],
    },
    {
        "id": "v10-restaurace",
        "roof": "restaurační pojmy",
        "level": "normal",
        "hidden": True,
        "inside": [
            "objednávka", "účet", "lístek", "chod", "obsluha", "spropitné",
        ],
        "outside": [
            "batoh", "chleba", "kbelík", "kladívko", "koště", "kýbl",
            "lednička", "lepidlo", "ramínko", "schránka", "silnice", "tácek",
            "utěrka", "šroub", "šuplík",
        ],
        "asks": [
            "jsou to zároveň restaurační pojmy",
            "jsou to zároveň jména českých měst",
            "jsou v názvech večerníčků",
            "jsou to zároveň značky českého piva",
        ],
    },
    {
        "id": "v10-autoskola",
        "roof": "pojmy z autoškoly",
        "level": "normal",
        "hidden": True,
        "inside": [
            "křižovatka", "přednost", "značka", "zkouška", "jízda", "testy",
        ],
        "outside": [
            "bunda", "deštník", "kartáček", "koberec", "lepidlo", "lopata",
            "mýdlo", "naběračka", "peněženka", "peřina", "pilník", "provaz",
            "ubrousek", "zahrada", "šuplík",
        ],
        "asks": [
            "jsou to zároveň pojmy z autoškoly",
            "jsou v názvech večerníčků",
            "nemají v sobě ani jednu samohlásku",
            "jsou v názvech her Járy Cimrmana",
        ],
    },
    {
        "id": "v10-schodiste",
        "roof": "části schodiště",
        "level": "normal",
        "hidden": True,
        "inside": [
            "stupeň", "madlo", "podesta", "sloupek", "rameno", "nášlap",
        ],
        "outside": [
            "deka", "hoblík", "kartáček", "květináč", "lampa", "mísa",
            "mýdlo", "náramek", "plot", "silnice", "sud", "vařečka",
            "zahrada", "řetízek", "šroub",
        ],
        "asks": [
            "jsou to zároveň části schodiště",
            "jsou to zároveň značky nebo modely aut",
            "čtou se stejně zepředu i zezadu",
            "jsou to zároveň značky českého piva",
        ],
    },
    {
        "id": "v10-kosile",
        "roof": "části košile",
        "level": "normal",
        "hidden": True,
        "inside": [
            "límec", "manžeta", "náprsenka", "knoflík", "rukáv", "sedlo",
        ],
        "outside": [
            "brambora", "hrnec", "kartáček", "kleště", "koberec", "kolík",
            "koště", "lednička", "naběračka", "nůžky", "postel", "sklenice",
            "trouba", "ubrousek", "věšák",
        ],
        "asks": [
            "jsou to zároveň části košile",
            "jsou to zároveň příjmení českých prezidentů",
            "mají v sobě dvě stejná písmena vedle sebe",
            "jsou v názvech Shakespearových her",
        ],
    },
    {
        "id": "v10-vodovod",
        "roof": "části vodovodu",
        "level": "hard",
        "hidden": True,
        "inside": [
            "kohout", "koleno", "přípojka", "sifon", "ventil", "těsnění",
        ],
        "outside": [
            "chleba", "hoblík", "hodinky", "kabát", "krém", "motyka", "mísa",
            "nůžky", "podnos", "prostěradlo", "ramínko", "stůl", "trakař",
            "věšák", "řetízek",
        ],
        "asks": [
            "jsou to zároveň části vodovodu",
            "jsou v názvech her Járy Cimrmana",
            "jsou to zároveň příjmení českých prezidentů",
            "jsou v názvech Shakespearových her",
        ],
    },
    {
        "id": "v10-strecha",
        "roof": "části střechy",
        "level": "normal",
        "hidden": True,
        "inside": [
            "hřeben", "taška", "krov", "okap", "úžlabí", "štít",
        ],
        "outside": [
            "deka", "hoblík", "houpačka", "kabát", "koš", "peřina", "plot",
            "polštář", "ponožka", "postel", "propiska", "prostěradlo",
            "ramínko", "svěrák", "zápisník",
        ],
        "asks": [
            "jsou to zároveň části střechy",
            "jsou to zároveň značky nebo modely aut",
            "jsou to zároveň příjmení českých prezidentů",
            "nemají v sobě ani jednu samohlásku",
        ],
    },
    {
        "id": "v10-vuz",
        "roof": "části koňského vozu",
        "level": "hard",
        "hidden": True,
        "inside": [
            "oj", "náprava", "loukoť", "korba", "ráf", "zápřah",
        ],
        "outside": [
            "branka", "hadice", "hoblík", "kladívko", "matice", "mrkev",
            "myčka", "peněženka", "peřina", "pinzeta", "podnos", "rohožka",
            "sušák", "vařečka", "šroub",
        ],
        "asks": [
            "jsou to zároveň části koňského vozu",
            "nemají v sobě ani jednu samohlásku",
            "jsou v názvech her Járy Cimrmana",
            "jsou v názvech večerníčků",
        ],
    },
    {
        "id": "v10-zamek",
        "roof": "části dveřního zámku",
        "level": "normal",
        "hidden": True,
        "inside": [
            "klika", "vložka", "závora", "jazýček", "zástrč", "štítek",
        ],
        "outside": [
            "batoh", "brýle", "hrábě", "koš", "matrace", "motyka", "parapet",
            "police", "ručník", "skříň", "struhadlo", "ubrousek", "vařečka",
            "zahrada", "šuplík",
        ],
        "asks": [
            "jsou to zároveň části dveřního zámku",
            "nemají v sobě ani jednu samohlásku",
            "mají v sobě dvě stejná písmena vedle sebe",
            "jsou v názvech her Járy Cimrmana",
        ],
    },
    {
        "id": "v10-francouzstina",
        "roof": "slova přejatá z francouzštiny",
        "level": "hard",
        "hidden": True,
        "inside": [
            "bujón", "garáž", "kostým", "žánr", "plakát", "bulvár", "parfém",
            "šampaňské",
        ],
        "outside": [
            "hadr", "hrneček", "kastrol", "kompost", "kýbl", "lopata",
            "matice", "plot", "police", "rýč", "sešit", "silnice", "trakař",
            "zápisník", "šála",
        ],
        "asks": [
            "jsou to slova přejatá z francouzštiny",
            "jsou v názvech večerníčků",
            "mají v sobě dvě stejná písmena vedle sebe",
            "jsou to zároveň značky českého piva",
        ],
    },
    {
        "id": "v10-arabstina",
        "roof": "slova přejatá z arabštiny",
        "level": "hard",
        "hidden": True,
        "inside": [
            "alkohol", "algebra", "cukr", "káva", "magazín", "admirál",
            "žirafa", "šafrán",
        ],
        "outside": [
            "dřez", "hoblík", "hrneček", "kladívko", "kleště", "koště",
            "lepidlo", "mrkev", "mýdlo", "pekáč", "ponožka", "vrtačka",
            "vysavač", "šuplík", "žehlička",
        ],
        "asks": [
            "jsou to slova přejatá z arabštiny",
            "čtou se stejně zepředu i zezadu",
            "mají v sobě schované zvíře",
            "jsou v názvech her Járy Cimrmana",
        ],
    },
    {
        "id": "v10-italstina",
        "roof": "slova přejatá z italštiny",
        "level": "hard",
        "hidden": True,
        "inside": [
            "banka", "konto", "opera", "piano", "salám", "karneval", "sonáta",
            "balkon",
        ],
        "outside": [
            "branka", "guma", "hadr", "hřeben", "konev", "koště", "matice",
            "metr", "parapet", "pilník", "silnice", "stůl", "vrtačka",
            "řetízek", "žebřík",
        ],
        "asks": [
            "jsou to slova přejatá z italštiny",
            "jsou v názvech večerníčků",
            "čtou se stejně zepředu i zezadu",
            "jsou to zároveň značky českého piva",
        ],
    },
    {
        "id": "v10-slozeniny",
        "roof": "složená slova",
        "level": "normal",
        "hidden": True,
        "inside": [
            "zeměkoule", "vodopád", "letopočet", "velkoměsto", "dřevorubec",
            "kolotoč", "hromosvod", "samoobsluha",
        ],
        "outside": [
            "batoh", "bunda", "deštník", "hadice", "hrábě", "kýbl", "lavička",
            "matrace", "metr", "mísa", "pilník", "ponožka", "provaz",
            "sklenice", "věšák",
        ],
        "asks": [
            "jsou složená ze dvou slov",
            "jsou to zároveň příjmení českých prezidentů",
            "jsou to zároveň značky českého piva",
            "jsou to zároveň jména českých měst",
        ],
    },
    {
        "id": "v10-podle-cloveka",
        "roof": "slova, která vznikla z jména člověka",
        "level": "hard",
        "hidden": True,
        "inside": [
            "bojkot", "sendvič", "silueta", "saxofon", "gilotina", "mecenáš",
            "lynč",
        ],
        "outside": [
            "brýle", "dřez", "kartáček", "kleště", "koberec", "koště", "krém",
            "lampa", "lednička", "peřina", "pravítko", "sešit", "struhadlo",
            "utěrka", "vrtačka",
        ],
        "asks": [
            "vznikla ze jména konkrétního člověka",
            "jsou to zároveň příjmení českých prezidentů",
            "jsou to zároveň značky českého piva",
            "čtou se stejně zepředu i zezadu",
        ],
    },
    {
        "id": "v10-zaroste",
        "roof": "věci, ze kterých vyroste rostlina",
        "level": "normal",
        "hidden": True,
        "inside": [
            "semínko", "hlíza", "cibule", "žalud", "pecka", "oddenek",
            "výhonek", "kaštan",
        ],
        "outside": [
            "kamínek", "cihla", "korálek", "knoflík", "mince", "hřebík",
            "sponka", "korek", "střep", "kolík",
        ],
        "asks": [
            "vyklíčí, když se zasadí",
            "jsou to zároveň značky nebo modely aut",
            "čtou se stejně zepředu i zezadu",
            "jsou to zároveň příjmení českých prezidentů",
        ],
    },
    {
        "id": "v10-zip",
        "roof": "věci, které se zapínají na zip",
        "level": "normal",
        "hidden": True,
        "inside": [
            "bunda", "batoh", "stan", "spacák", "penál", "kalhoty", "pouzdro",
            "sukně",
        ],
        "outside": [
            "ponožka", "šála", "rukavice", "klobouk", "deka", "ručník",
            "kapesník", "opasek", "čepice", "tílko",
        ],
        "asks": [
            "se zapínají na zip",
            "jsou v názvech her Járy Cimrmana",
            "čtou se stejně zepředu i zezadu",
            "jsou v názvech Shakespearových her",
        ],
    },
    {
        "id": "v10-zada",
        "roof": "věci, které se nosí na zádech",
        "level": "normal",
        "hidden": True,
        "inside": [
            "batoh", "krosna", "tlumok", "ranec", "vak", "nůše",
        ],
        "outside": [
            "taška", "kabelka", "kufr", "koš", "pytel", "kbelík", "bedna",
            "aktovka", "mošna", "truhla",
        ],
        "asks": [
            "se nosí na zádech",
            "mají v sobě dvě stejná písmena vedle sebe",
            "jsou v názvech večerníčků",
            "jsou to zároveň příjmení českých prezidentů",
        ],
    },
    {
        "id": "v10-lekarna",
        "roof": "věci, které se koupí v lékárně",
        "level": "normal",
        "hidden": True,
        "inside": [
            "obvaz", "náplast", "jód", "aspirin", "teploměr", "vata", "sirup",
            "kapky",
        ],
        "outside": [
            "kladivo", "hřebík", "provaz", "koště", "sešit", "propiska",
            "lampa", "kbelík", "hrábě", "motyka",
        ],
        "asks": [
            "se prodávají v lékárně",
            "jsou to zároveň značky nebo modely aut",
            "mají v sobě dvě stejná písmena vedle sebe",
            "jsou to zároveň jména českých měst",
        ],
    },
    {
        "id": "v10-ztvrdne",
        "roof": "látky, které po zaschnutí ztvrdnou",
        "level": "hard",
        "hidden": True,
        "inside": [
            "beton", "sádra", "lepidlo", "malta", "lak", "tmel", "hlína",
            "cement",
        ],
        "outside": [
            "voda", "olej", "mléko", "ocet", "líh", "benzín", "čaj", "sirup",
            "med", "glycerin",
        ],
        "asks": [
            "po zaschnutí ztvrdnou",
            "jsou to znamení zvěrokruhu",
            "jsou to zároveň značky nebo modely aut",
            "jsou v názvech večerníčků",
        ],
    },
    {
        "id": "v10-voni",
        "roof": "věci, které voní i po uschnutí",
        "level": "normal",
        "hidden": True,
        "inside": [
            "levandule", "seno", "skořice", "vanilka", "tabák", "chmel",
            "kadidlo", "máta",
        ],
        "outside": [
            "cihla", "sklo", "hřebík", "provaz", "kámen", "papír", "drát",
            "plech", "korek", "struska",
        ],
        "asks": [
            "voní i po uschnutí",
            "jsou to zároveň značky nebo modely aut",
            "jsou to zároveň značky českého piva",
            "jsou v názvech her Járy Cimrmana",
        ],
    },
    {
        "id": "v10-jedovate",
        "roof": "jedovaté věci",
        "level": "hard",
        "hidden": True,
        "inside": [
            "muchomůrka", "rulík", "tis", "konvalinka", "rtuť", "arsen",
            "olovo", "kurare",
        ],
        "outside": [
            "heřmánek", "máta", "lípa", "šípek", "jahoda", "borůvka",
            "křemen", "žula", "měď", "cín",
        ],
        "asks": [
            "jsou jedovaté",
            "čtou se stejně zepředu i zezadu",
            "jsou v názvech her Járy Cimrmana",
            "mají v sobě dvě stejná písmena vedle sebe",
        ],
    },
    {
        "id": "v10-zvetsuje",
        "roof": "věci, které zvětšují obraz",
        "level": "normal",
        "hidden": True,
        "inside": [
            "lupa", "mikroskop", "dalekohled", "brýle", "projektor", "čočka",
        ],
        "outside": [
            "zrcadlo", "okno", "sklenice", "hodinky", "lampa", "baterka",
            "kompas", "budík", "váhy", "teploměr",
        ],
        "asks": [
            "zvětšují obraz",
            "jsou to znamení zvěrokruhu",
            "jsou v názvech večerníčků",
            "nemají v sobě ani jednu samohlásku",
        ],
    },
    {
        "id": "v10-cisla",
        "roof": "věci, na kterých jsou čísla",
        "level": "normal",
        "hidden": True,
        "inside": [
            "hodiny", "teploměr", "kalendář", "pravítko", "telefon", "dres",
            "váha",
        ],
        "outside": [
            "koště", "deka", "ručník", "polštář", "koberec", "ubrus", "mýdlo",
            "houba", "provaz", "kbelík",
        ],
        "asks": [
            "mají na sobě čísla",
            "jsou v názvech Shakespearových her",
            "jsou to zároveň jména českých měst",
            "čtou se stejně zepředu i zezadu",
        ],
    },
    {
        "id": "v10-destnik",
        "roof": "věci, které chrání před deštěm",
        "level": "normal",
        "hidden": True,
        "inside": [
            "deštník", "pláštěnka", "střecha", "markýza", "přístřešek",
            "klobouk",
        ],
        "outside": [
            "brýle", "rukavice", "ponožka", "opasek", "kravata", "náramek",
            "hodinky", "prsten", "batoh", "tužka",
        ],
        "asks": [
            "chrání před deštěm",
            "jsou v názvech Shakespearových her",
            "jsou to zároveň příjmení českých prezidentů",
            "jsou to zároveň jména českých měst",
        ],
    },
    {
        "id": "v10-pecka",
        "roof": "ovoce s jednou velkou peckou",
        "level": "normal",
        "hidden": True,
        "inside": [
            "broskev", "švestka", "třešeň", "meruňka", "avokádo", "mango",
            "oliva", "datle",
        ],
        "outside": [
            "jablko", "hruška", "pomeranč", "meloun", "jahoda", "rybíz",
            "banán", "kiwi", "angrešt", "malina",
        ],
        "asks": [
            "mají uvnitř jednu velkou pecku",
            "jsou to zároveň značky českého piva",
            "nemají v sobě ani jednu samohlásku",
            "jsou v názvech her Járy Cimrmana",
        ],
    },
    {
        "id": "v10-odpuzuje",
        "roof": "látky, které odpuzují vodu",
        "level": "hard",
        "hidden": True,
        "inside": [
            "vosk", "olej", "teflon", "peří", "guma", "silikon", "lak",
        ],
        "outside": [
            "papír", "houba", "vata", "plátno", "hlína", "cukr", "sůl",
            "mouka", "dřevo", "vlna",
        ],
        "asks": [
            "odpuzují vodu",
            "jsou v názvech Shakespearových her",
            "čtou se stejně zepředu i zezadu",
            "jsou v názvech her Járy Cimrmana",
        ],
    },
    {
        "id": "v10-saje",
        "roof": "věci, které nasáknou vodu",
        "level": "normal",
        "hidden": True,
        "inside": [
            "houba", "vata", "papír", "hlína", "ručník", "plátno", "mech",
            "korek",
        ],
        "outside": [
            "sklo", "kov", "plast", "vosk", "guma", "olej", "mince", "klíč",
            "kámen", "drát",
        ],
        "asks": [
            "nasáknou vodu",
            "jsou v názvech večerníčků",
            "jsou to zároveň příjmení českých prezidentů",
            "nemají v sobě ani jednu samohlásku",
        ],
    },
    {
        "id": "v10-hasi",
        "roof": "věci, kterými se hasí oheň",
        "level": "normal",
        "hidden": True,
        "inside": [
            "voda", "písek", "pěna", "deka", "hlína", "sníh",
        ],
        "outside": [
            "benzín", "líh", "olej", "papír", "sláma", "dřevo", "uhlí",
            "seno", "vosk", "tuk",
        ],
        "asks": [
            "hasí oheň",
            "mají v sobě dvě stejná písmena vedle sebe",
            "jsou to zároveň značky nebo modely aut",
            "čtou se stejně zepředu i zezadu",
        ],
    },
    {
        "id": "v10-vitr",
        "roof": "věci, které uletí ve větru",
        "level": "normal",
        "hidden": True,
        "inside": [
            "list", "papír", "pírko", "prach", "pyl", "semínko",
        ],
        "outside": [
            "cihla", "kámen", "mince", "kladivo", "sklenice", "hrnec", "klíč",
            "kbelík", "sekera", "kovadlina",
        ],
        "asks": [
            "uletí ve větru",
            "mají v sobě schované zvíře",
            "mají v sobě dvě stejná písmena vedle sebe",
            "jsou to znamení zvěrokruhu",
        ],
    },
    {
        "id": "v10-odrazene-svetlo",
        "roof": "věci, které svítí jen odraženým světlem",
        "level": "hard",
        "hidden": True,
        "inside": [
            "měsíc", "planeta", "zrcadlo", "sníh", "hladina", "kometa",
        ],
        "outside": [
            "slunce", "hvězda", "oheň", "žárovka", "blesk", "svíčka",
            "světluška", "laser", "pochodeň", "jiskra",
        ],
        "asks": [
            "svítí jen odraženým světlem",
            "mají v sobě schované zvíře",
            "jsou to zároveň značky českého piva",
            "čtou se stejně zepředu i zezadu",
        ],
    },
    {
        "id": "v10-nadrze",
        "roof": "české přehradní nádrže",
        "level": "hard",
        "hidden": True,
        "inside": [
            "Orlík", "Lipno", "Slapy", "Nechranice", "Dalešice", "Rozkoš",
            "Švihov", "Hracholusky",
        ],
        "outside": [
            "hřeben", "kastrol", "kbelík", "květináč", "lopatka", "matrace",
            "metr", "naběračka", "pinzeta", "pouzdro", "pytel", "sešit",
            "tácek", "utěrka", "vařečka",
        ],
        "asks": [
            "jsou to zároveň české přehrady",
            "jsou to znamení zvěrokruhu",
            "mají v sobě dvě stejná písmena vedle sebe",
            "mají v sobě schované zvíře",
        ],
    },
    {
        "id": "v10-ctvrti",
        "roof": "pražské čtvrti",
        "level": "normal",
        "hidden": True,
        "inside": [
            "Dejvice", "Vinohrady", "Žižkov", "Karlín", "Smíchov", "Braník",
            "Vršovice", "Podolí",
        ],
        "outside": [
            "deštník", "hrneček", "koš", "koště", "květináč", "lednička",
            "mrkev", "pouzdro", "propiska", "provaz", "semínko", "sklenice",
            "smeták", "sud", "šroub",
        ],
        "asks": [
            "jsou to zároveň pražské čtvrti",
            "jsou v názvech večerníčků",
            "jsou to znamení zvěrokruhu",
            "mají v sobě schované zvíře",
        ],
    },
    {
        "id": "v10-par",
        "roof": "věci, které se prodávají v páru",
        "level": "normal",
        "hidden": True,
        "inside": [
            "boty", "ponožky", "rukavice", "brusle", "lyže", "náušnice",
        ],
        "outside": [
            "čepice", "šála", "opasek", "kabát", "sukně", "klobouk", "batoh",
            "deštník", "prsten", "hodinky",
        ],
        "asks": [
            "se prodávají vždycky po dvou",
            "jsou to zároveň jména českých měst",
            "čtou se stejně zepředu i zezadu",
            "jsou to zároveň značky českého piva",
        ],
    },
    {
        "id": "v10-origami",
        "roof": "věci, které se dají složit z papíru",
        "level": "normal",
        "hidden": True,
        "inside": [
            "vlaštovka", "loďka", "čepice", "harmonika", "žabka", "jeřáb",
        ],
        "outside": [
            "kladivo", "hrnec", "židle", "klíč", "mýdlo", "lampa", "provaz",
            "kbelík", "cihla", "sklenice",
        ],
        "asks": [
            "se dají složit z papíru",
            "jsou to zároveň jména českých měst",
            "jsou to zároveň značky nebo modely aut",
            "čtou se stejně zepředu i zezadu",
        ],
    },
    {
        "id": "v10-les-sber",
        "roof": "věci, které se sbírají v lese",
        "level": "normal",
        "hidden": True,
        "inside": [
            "houby", "borůvky", "maliny", "klestí", "mech", "šišky",
            "brusinky", "žaludy",
        ],
        "outside": [
            "mrkev", "brambora", "cibule", "řepa", "salát", "okurka",
            "ředkvička", "rajče", "hrách", "dýně",
        ],
        "asks": [
            "se sbírají v lese",
            "jsou to zároveň značky nebo modely aut",
            "nemají v sobě ani jednu samohlásku",
            "mají v sobě dvě stejná písmena vedle sebe",
        ],
    },
    {
        "id": "v10-trafika",
        "roof": "věci, které se koupí v trafice",
        "level": "normal",
        "hidden": True,
        "inside": [
            "noviny", "časopis", "známka", "jízdenka", "los", "zapalovač",
            "žvýkačka", "pohlednice",
        ],
        "outside": [
            "kladivo", "hrnec", "deka", "koště", "motyka", "žebřík", "pračka",
            "matrace", "konev", "hrábě",
        ],
        "asks": [
            "se prodávají v trafice",
            "jsou to zároveň jména českých měst",
            "jsou to zároveň značky nebo modely aut",
            "jsou v názvech Shakespearových her",
        ],
    },
    {
        "id": "v10-uzel",
        "roof": "věci, které se dají uvázat na uzel",
        "level": "normal",
        "hidden": True,
        "inside": [
            "provaz", "tkanička", "kravata", "šátek", "hadice", "lano", "nit",
        ],
        "outside": [
            "drát", "tyč", "prkno", "řetěz", "klacek", "trubka", "hřebík",
            "sklo", "cihla", "plech",
        ],
        "asks": [
            "se dají uvázat na uzel",
            "jsou to zároveň značky nebo modely aut",
            "jsou v názvech večerníčků",
            "jsou to zároveň příjmení českých prezidentů",
        ],
    },
    {
        "id": "v10-vede-teplo",
        "roof": "látky, které dobře vedou teplo",
        "level": "hard",
        "hidden": True,
        "inside": [
            "měď", "hliník", "železo", "stříbro", "ocel", "mosaz",
        ],
        "outside": [
            "dřevo", "korek", "vlna", "molitan", "plast", "papír", "guma",
            "pěna", "textil", "sláma",
        ],
        "asks": [
            "dobře vedou teplo",
            "jsou v názvech her Járy Cimrmana",
            "mají v sobě schované zvíře",
            "jsou v názvech Shakespearových her",
        ],
    },
]
