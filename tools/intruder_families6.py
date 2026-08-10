"""Šestá várka rodin — samé skryté souvislosti.

Rozdíl proti psaným rodinám z předchozích souborů je zásadní a je to přesně
ten rozdíl, který dělí obtížnosti:

* **Psaná rodina má střechu.** Všech pět slov je vidět pohromadě — jsou to
  houby, jsou to psi, hraje se s nimi na hřišti. Hráč tu střechu uvidí na
  první pohled a hledá už jen osu uvnitř. To je lehká obtížnost.
* **Skrytá rodina střechu nemá.** Pětice vypadá jako náhodná hromada:
  *vodník, poklad, hrnec, vrba, lilie*. Dokud hráč nepřijde na to, že čtyři
  z nich stojí v obsahu Kytice, nemá se čeho chytit — a právě tohle hledání
  je celá hra. Tyhle rodiny nesou střední a těžkou obtížnost.

Skryté souvislosti jsou trojího druhu a várka je schválně míchá, aby si na
jeden nešlo zvyknout:

1. **Slovo je zároveň něco jiného.** *Kost* je hrad, *labuť* je souhvězdí,
   *mucha* je malíř.
2. **Slovo se schovává v názvu.** *Krakatit*, *matka*, *mlok* jsou knihy
   Karla Čapka; *klobouk* a *špagetka* jsou večerníčky.
3. **Skrytá je forma slova.** *Krk* a *smrk* nemají samohlásku, *panna*
   a *oddíl* mají dvě stejná písmena vedle sebe, v *rakvi* se schovává rak.

Slova vně (`outside`) jsou schválně nudná a z jiných soudků — nesmí mít nic
společného ani mezi sebou. Kdyby byla všechna ze stejné třídy, oddělil by je
hráč od čtveřice bez přemýšlení.
"""

# Slova, která se hodí jako vetřelec skoro všude: běžná, krátká, z domácnosti
# a bez jakékoli druhé identity. Opakují se napříč rodinami schválně — hráč
# si na ně nemá jak zvyknout, protože vetřelec je pokaždé jiný a nikdy není
# to, co je na pětici zajímavé.
VSEDNI = ["hrnec", "deštník", "police", "sešit", "koště", "plot",
          "kabát", "lampa", "konev", "žebřík", "ručník", "kýbl"]

FAMILIES6 = [
    # ---------- střední: souvislost jde najít, když se hráč zamyslí ----------
    {
        "id": "skryte-zvire-uvnitr",
        "roof": "slova, ve kterých se schovává zvíře",
        "level": "normal",
        "hidden": True,
        # rak v rakvi, lev v levanduli, sob v sobotě, los v kolosu.
        "inside": ["rakev", "raketa", "levandule", "levice", "sobota", "osoba",
                   "kolos", "myšlenka", "pestrý", "hadice", "kosatec"],
        # Co v kterém slově vězí. Stavěč sady podle toho hlídá, aby v jedné
        # pětici nestála dvě slova s týmž zvířetem — „rakev" a „raketa" nesou
        # obě raka a vypadalo by to jako přehlédnutí.
        "skryte": {"rakev": "rak", "raketa": "rak", "levandule": "lev",
                   "levice": "lev", "sobota": "sob", "osoba": "sob",
                   "kolos": "los", "myšlenka": "myš", "pestrý": "pes",
                   "hadice": "had", "kosatec": "kos"},
        # Ani v jednom z nich žádné zvíře není — ověřeno slovo po slovu.
        "outside": ["stůl", "okno", "zahrada", "polštář", "chleba", "sklenice",
                    "kabát", "silnice", "brambora", "koberec", "hrnec", "lampa"],
        "asks": [
            "mají v sobě schované zvíře",
            "jsou to zároveň jména českých měst",
            "jsou v názvech Shakespearových her",
            "jsou to zároveň značky českého piva",
            "čtou se stejně zepředu i zezadu",
        ],
    },
    {
        "id": "skryte-bez-samohlasky",
        "roof": "slova bez samohlásky",
        "level": "normal",
        "hidden": True,
        # Slabiku v nich drží r nebo l. Krátká slova jsou tu proto, že delší
        # bez samohlásky v češtině skoro nejsou — vetřelec proto taky musí
        # být krátký, jinak by trčel délkou a poznal by se bez přemýšlení.
        "inside": ["krk", "vlk", "smrk", "prst", "srst", "hrst", "krb", "chrt",
                   "trh", "vrch", "smrt", "brk"],
        "outside": ["most", "plot", "sad", "les", "vůz", "dům", "hrad", "mrak",
                    "klid", "zeď", "sůl", "sen"],
        "asks": [
            "nemají v sobě ani jednu samohlásku",
            "jsou to zároveň jména českých měst",
            "jsou v názvech her Járy Cimrmana",
            "jsou to zároveň příjmení českých prezidentů",
        ],
    },
    {
        "id": "skryte-vecernicky",
        "roof": "slova z názvů večerníčků",
        "level": "normal",
        "hidden": True,
        "inside": ["krtek", "bob", "bobek", "pat", "mat", "panenka", "víla",
                   "broučci", "klobouk", "špagetka", "štaflík", "rákosníček"],
        "outside": VSEDNI,
        "asks": [
            "jsou v názvech večerníčků",
            "jsou to zároveň jména českých měst",
            "čtou se stejně zepředu i zezadu",
            "jsou to zároveň značky nebo modely aut",
        ],
    },
    {
        "id": "skryte-jmeno-uvnitr",
        "roof": "slova, ve kterých se schovává křestní jméno",
        "level": "normal",
        "hidden": True,
        # Ivan v divanu, Petr v petrklíči, Lenka ve sklence, Roman v romanci.
        # Každé jméno musí ve slově stát celé a vcelku — kdyby se skládalo
        # přes hranici („čoko-láda"), hráč by to neuviděl ani po vyhodnocení
        # a připadalo by mu, že hra podvádí.
        # Jméno musí sedět i s háčky a čárkami: „svítilna" nese Víta, kdežto
        # „závit" jen „vit" bez délky — a to už není jméno, jen podobný shluk.
        "inside": ["divan", "petrklíč", "petržel", "pivo", "svítilna",
                   "madam", "romance", "sklenka", "poleva", "bota", "jantar",
                   "pyramida"],
        "skryte": {"divan": "Ivan", "petrklíč": "Petr", "petržel": "Petr",
                   "pivo": "Ivo", "svítilna": "Vít", "madam": "Adam",
                   "romance": "Roman", "sklenka": "Lenka", "poleva": "Eva",
                   "bota": "Ota", "jantar": "Jan", "pyramida": "Ida"},
        "outside": ["stůl", "okno", "zahrada", "hrnec", "koště", "plot",
                    "mrkev", "police", "sešit", "kabát", "lampa", "deštník"],
        "asks": [
            "mají v sobě schované křestní jméno",
            "jsou to zároveň jména českých měst",
            "jsou v názvech Shakespearových her",
            "jsou to znamení zvěrokruhu",
        ],
    },
    {
        "id": "skryte-kytice",
        "roof": "slova z názvů básní Erbenovy Kytice",
        "level": "normal",
        "hidden": True,
        "inside": ["vodník", "polednice", "holoubek", "poklad", "vrba", "lilie",
                   "kolovrat", "košile", "kletba", "kytice", "lože", "štědrý"],
        "outside": VSEDNI,
        "asks": [
            "jsou v názvech básní z Erbenovy Kytice",
            "jsou to zároveň jména českých měst",
            "jsou v názvech her Járy Cimrmana",
            "jsou to zároveň značky českého piva",
        ],
    },
    {
        "id": "skryte-koledy",
        "roof": "slova z názvů koled",
        "level": "normal",
        "hidden": True,
        "inside": ["noviny", "betlém", "večer", "pán", "ovce", "valaši",
                   "rolničky", "štěstí"],
        "outside": VSEDNI,
        "asks": [
            "jsou v názvech českých koled",
            "jsou to zároveň jména českých měst",
            "čtou se stejně zepředu i zezadu",
            "jsou to zároveň příjmení českých prezidentů",
        ],
    },
    {
        "id": "skryte-zdvojene",
        "roof": "slova se dvěma stejnými písmeny vedle sebe",
        "level": "normal",
        "hidden": True,
        "inside": ["panna", "denně", "ranní", "vinný", "cenný", "kamenný",
                   "oddíl", "poddaný", "bezzubý", "nejjasnější", "oddych", "vyšší"],
        "outside": ["stůl", "okno", "kniha", "zahrada", "hrnec", "plot",
                    "mrkev", "police", "sešit", "kabát", "lampa", "deštník"],
        "asks": [
            "mají v sobě dvě stejná písmena vedle sebe",
            "jsou to zároveň jména českých měst",
            "jsou v názvech Shakespearových her",
            "jsou to znamení zvěrokruhu",
        ],
    },
    {
        "id": "skryte-hrady",
        "roof": "slova, která jsou zároveň jména hradů",
        "level": "normal",
        "hidden": True,
        # Schválně jen ta jména, která jsou zároveň úplně běžná slova. Kdyby
        # mezi nimi stál Křivoklát nebo Bezděz, hráč pozná hrady na první
        # pohled a hádanka je pryč.
        "inside": ["kost", "loket", "houska", "trosky", "orlík", "rabí"],
        "outside": VSEDNI,
        "asks": [
            "jsou to zároveň jména českých hradů",
            "jsou v názvech Shakespearových her",
            "jsou to zároveň značky českého piva",
            "jsou to znamení zvěrokruhu",
        ],
    },

    # ---------- těžká: bez znalosti nebo pořádného všímání to nejde ----------
    {
        "id": "skryte-souhvezdi",
        "roof": "slova, která jsou zároveň souhvězdí",
        "level": "hard",
        "hidden": True,
        # Zvířata i věci naráz, a mezi vetřelci taky — jinak by se pětice
        # rozpadla na „zvířata proti nezvířatům" a osa by byla k ničemu.
        "inside": ["labuť", "orel", "drak", "had", "delfín", "pohár", "kompas",
                   "žirafa", "moucha", "ještěrka", "kýl", "plachty"],
        "outside": ["veverka", "kapr", "ježek", "hrnec", "židle", "mrkev",
                    "koště", "lampa", "klobouk", "srnec", "sešit", "konev"],
        "asks": [
            "jsou to zároveň souhvězdí",
            "jsou to zároveň jména českých měst",
            "jsou v názvech her Járy Cimrmana",
            "jsou to zároveň značky nebo modely aut",
        ],
    },
    {
        "id": "skryte-capek",
        "roof": "slova z názvů knih Karla Čapka",
        "level": "hard",
        "hidden": True,
        "inside": ["válka", "mlok", "matka", "krakatit", "továrna", "zahradník",
                   "nemoc", "loupežník", "povětroň", "hordubal", "dášeňka", "apokryf"],
        "outside": VSEDNI,
        "asks": [
            "jsou v názvech knih Karla Čapka",
            "jsou to zároveň jména českých měst",
            "čtou se stejně zepředu i zezadu",
            "jsou to zároveň značky českého piva",
        ],
    },
    {
        "id": "skryte-hrabal",
        "roof": "slova z názvů knih Bohumila Hrabala",
        "level": "hard",
        "hidden": True,
        "inside": ["král", "vlaky", "postřižiny", "sněženky", "perlička", "barbar",
                   "samota", "hodiny", "automat", "městečko"],
        "outside": VSEDNI,
        "asks": [
            "jsou v názvech knih Bohumila Hrabala",
            "jsou to zároveň jména českých měst",
            "jsou v názvech Shakespearových her",
            "jsou to znamení zvěrokruhu",
        ],
    },
    {
        "id": "skryte-forman",
        "roof": "slova z názvů Formanových filmů",
        "level": "hard",
        "hidden": True,
        "inside": ["vlasy", "přelet", "hnízdo", "lásky", "plavovláska", "panenka",
                   "petr", "konkurs", "amadeus", "měsíc"],
        "outside": VSEDNI,
        "asks": [
            "jsou v názvech filmů Miloše Formana",
            "jsou to zároveň jména českých měst",
            "jsou v názvech her Járy Cimrmana",
            "jsou to zároveň příjmení českých prezidentů",
        ],
    },
    {
        "id": "skryte-malir",
        "roof": "slova, která jsou zároveň příjmení malířů",
        "level": "hard",
        "hidden": True,
        "inside": ["mucha", "kupka", "slavíček", "zrzavý", "špála", "lada",
                   "aleš", "brožík", "filla"],
        "outside": ["veverka", "hrnec", "židle", "mrkev", "koště", "lampa",
                    "klobouk", "sešit", "konev", "plot", "police", "deštník"],
        "asks": [
            "jsou to zároveň příjmení českých malířů",
            "jsou to zároveň jména českých měst",
            "čtou se stejně zepředu i zezadu",
            "jsou to znamení zvěrokruhu",
        ],
    },
]
