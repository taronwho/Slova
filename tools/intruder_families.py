"""Rodiny pro Vetřelce — psané ručně, ne těžené z dat.

Každá rodina má **střechu** (co mají všechna slova společné) a **osu**
(čím se čtveřice liší od vetřelce). Střecha nemusí být taxonomická třída;
klidně to je „žijí ve vodě" napříč savci, rybami i korýši, nebo „najdeš to
v autě". Čím volnější střecha, tím víc práce svede osa.

`inside` jsou slova, která osu splňují, `outside` ta, která ne. Hádanka
vznikne výběrem čtyř zevnitř a jednoho zvenku, takže jedna rodina vydá na
stovky pětic a dvě po sobě vypadají jinak.

`asks` jsou tři věty do druhého kroku. **První je ta správná** — dělí
čtveřici od vetřelce. Zbylé dvě platí pro čtveřici i pro vetřelce, takže
nic nevydělují; hráč musí poznat, která z těch tří opravdu odděluje.

`level`: easy = osa je nápadná, hard = střecha je těsně kolem osy.
"""

FAMILIES = [
    {
        "id": "voda-sladka",
        "roof": "živočichové, kteří žijí ve vodě",
        "level": "hard",
        "inside": ["kapr", "štika", "sumec", "okoun", "bobr", "vydra", "rak", "pstruh",
                   "candát", "lín", "cejn", "úhoř", "škeble", "žába", "mlok", "perlorodka"],
        "outside": ["tuleň", "treska", "sardinka", "krab", "chobotnice", "delfín",
                    "velryba", "mořský koník", "medúza", "žralok", "makrela", "platýs"],
        "asks": ["žijí ve sladké vodě", "žijí ve vodě", "dají se ulovit"],
    },
    {
        "id": "auto-vybava",
        "roof": "věci, které se dají najít v autě",
        "level": "easy",
        "inside": ["volant", "brzda", "zrcátko", "tachometr", "spojka", "airbag", "výfuk",
                   "převodovka", "stěrač", "sedačka", "kapota", "klakson", "nárazník"],
        "outside": ["kufřík", "deka", "termoska", "mapa", "lékárnička", "dítě", "pes",
                    "nákup", "kanystr", "sněhová lopata"],
        "asks": ["jsou pevnou součástí auta", "najdeš je v autě", "vozí se s autem"],
    },
    {
        "id": "nastroje-smycce",
        "roof": "hudební nástroje se strunami",
        "level": "normal",
        "inside": ["housle", "viola", "violoncello", "kontrabas", "viola da gamba", "niněra"],
        "outside": ["kytara", "harfa", "loutna", "banjo", "cimbál", "mandolína",
                    "citera", "ukulele", "klavír"],
        "asks": ["hraje se na ně smyčcem", "mají struny", "hrají v orchestru"],
    },
    {
        "id": "koreni-semena",
        "roof": "koření",
        "level": "hard",
        "inside": ["pepř", "kmín", "koriandr", "muškát", "anýz", "hořčice", "fenykl",
                   "kardamom", "vanilka", "jalovec", "badyán", "paprika"],
        "outside": ["bazalka", "tymián", "oregano", "šalvěj", "petržel", "majoránka",
                    "rozmarýn", "libeček", "kopr", "máta"],
        "asks": ["je to plod nebo semeno", "voní", "používá se v kuchyni"],
    },
    {
        "id": "planety-kamenne",
        "roof": "planety sluneční soustavy",
        "level": "normal",
        "inside": ["Merkur", "Venuše", "Země", "Mars"],
        "outside": ["Jupiter", "Saturn", "Uran", "Neptun"],
        "asks": ["mají pevný povrch", "obíhají kolem Slunce", "jsou vidět dalekohledem"],
    },
    {
        "id": "sporty-mic",
        "roof": "sporty",
        "level": "easy",
        "inside": ["fotbal", "házená", "volejbal", "basketbal", "ragby", "vodní pólo",
                   "nohejbal", "softbal", "baseball", "kriket", "florbal", "tenis"],
        "outside": ["hokej", "šerm", "veslování", "krasobruslení", "box", "atletika",
                    "plavání", "cyklistika", "judo", "lukostřelba"],
        "asks": ["hraje se s míčem", "hrají se v družstvu", "mají mistrovství světa"],
    },
    {
        "id": "kov-drahy",
        "roof": "kovy",
        "level": "normal",
        "inside": ["zlato", "stříbro", "platina", "palladium", "rhodium", "iridium"],
        "outside": ["železo", "měď", "hliník", "olovo", "cín", "zinek", "nikl",
                    "chrom", "titan", "hořčík"],
        "asks": ["jsou to drahé kovy", "vedou elektřinu", "dají se tavit"],
    },
    {
        "id": "mesta-more",
        "roof": "evropská hlavní města",
        "level": "hard",
        "inside": ["Lisabon", "Athény", "Kodaň", "Stockholm", "Helsinky", "Dublin",
                   "Oslo", "Riga", "Tallinn", "Reykjavík", "Valletta", "Amsterodam"],
        "outside": ["Praha", "Vídeň", "Madrid", "Bern", "Budapešť", "Varšava",
                    "Bratislava", "Lucemburk", "Minsk", "Bělehrad", "Sofie", "Kyjev"],
        "asks": ["leží u moře", "jsou to hlavní města", "leží v Evropě"],
    },
    {
        "id": "babicka-postavy",
        "roof": "postavy z české klasické literatury",
        "level": "normal",
        "inside": ["babička", "Barunka", "Viktorka", "Kristla", "Mílo", "Adélka",
                   "kněžna", "Jan"],
        "outside": ["Maryša", "Švejk", "Cipísek", "Hordubal", "Jirásek", "Kolumbus"],
        "asks": ["vystupují v Babičce", "jsou to postavy z knihy", "vymyslel je český spisovatel"],
    },
    {
        "id": "stromy-jehlicnany",
        "roof": "stromy",
        "level": "easy",
        "inside": ["smrk", "borovice", "jedle", "modřín", "tis", "cedr", "cypřiš",
                   "douglaska", "sekvoj", "jalovec"],
        "outside": ["dub", "buk", "bříza", "javor", "lípa", "olše", "jasan",
                    "topol", "vrba", "habr", "jilm", "kaštan"],
        "asks": ["jsou to jehličnany", "rostou v lese", "dá se z nich získat dřevo"],
    },
    {
        "id": "kuchyne-rez",
        "roof": "kuchyňské náčiní",
        "level": "normal",
        "inside": ["nůž", "struhadlo", "škrabka", "kráječ", "sekáček", "kráječka",
                   "nůžky", "mandolína"],
        "outside": ["vařečka", "naběračka", "cedník", "metla", "prkénko", "obracečka",
                    "hrnec", "pánev", "mísa", "lžíce"],
        "asks": ["krájejí nebo strouhají", "patří do kuchyně", "myjí se po vaření"],
    },
    {
        "id": "staty-bezmore",
        "roof": "evropské státy",
        "level": "hard",
        "inside": ["Česko", "Rakousko", "Švýcarsko", "Maďarsko", "Slovensko", "Srbsko",
                   "Lucembursko", "Bělorusko", "Andorra", "Lichtenštejnsko",
                   "Severní Makedonie", "Moldavsko"],
        "outside": ["Polsko", "Chorvatsko", "Portugalsko", "Řecko", "Norsko", "Belgie",
                    "Nizozemsko", "Irsko", "Estonsko", "Albánie", "Itálie", "Finsko"],
        "asks": ["nemají přístup k moři", "leží v Evropě", "sousedí s několika státy"],
    },
    {
        "id": "ptaci-nelet",
        "roof": "ptáci",
        "level": "normal",
        "inside": ["pštros", "tučňák", "emu", "kiwi", "nandu", "kasuár", "kakapo"],
        "outside": ["orel", "vrabec", "labuť", "čáp", "sova", "racek", "vlaštovka",
                    "datel", "sýkora", "kos", "volavka", "jestřáb"],
        "asks": ["nelétají", "jsou to ptáci", "kladou vejce"],
    },
    {
        "id": "hodiny-cas",
        "roof": "věci, kterými se něco měří",
        "level": "easy",
        "inside": ["hodiny", "stopky", "budík", "přesýpací hodiny", "kalendář",
                   "orloj", "metronom", "sluneční hodiny"],
        "outside": ["metr", "váha", "teploměr", "kompas", "odměrka", "tlakoměr",
                    "posuvné měřítko", "vodováha", "rychloměr"],
        "asks": ["měří čas", "něco měří", "mají stupnici nebo číslice"],
    },
    {
        "id": "zelenina-koren",
        "roof": "zelenina",
        "level": "hard",
        "inside": ["mrkev", "petržel", "celer", "ředkvička", "řepa", "pastinák",
                   "křen", "tuřín", "brambor", "topinambur"],
        "outside": ["rajče", "okurka", "paprika", "cuketa", "dýně", "hrách",
                    "fazole", "lilek", "kukuřice", "brokolice"],
        "asks": ["jí se z nich podzemní část", "je to zelenina", "dá se to pěstovat na zahradě"],
    },
    {
        "id": "budovy-vira",
        "roof": "stavby, do kterých se chodí",
        "level": "normal",
        "inside": ["kostel", "katedrála", "kaple", "synagoga", "mešita", "klášter",
                   "chrám", "modlitebna"],
        "outside": ["divadlo", "nádraží", "knihovna", "radnice", "škola", "muzeum",
                    "nemocnice", "tržnice", "lázně"],
        "asks": ["slouží k bohoslužbě", "dá se do nich vejít", "bývají to historické budovy"],
    },
    {
        "id": "nemoci-virus",
        "roof": "nemoci",
        "level": "hard",
        "inside": ["chřipka", "neštovice", "spalničky", "zarděnky", "vzteklina",
                   "obrna", "žloutenka", "opar"],
        "outside": ["angína", "tuberkulóza", "tetanus", "borelióza", "salmonelóza",
                    "cholera", "mor", "syfilis"],
        "asks": ["způsobuje je virus", "jsou to nakažlivé nemoci", "existuje proti nim očkování"],
    },
    {
        "id": "napoje-kvaseni",
        "roof": "nápoje",
        "level": "normal",
        "inside": ["pivo", "víno", "cider", "medovina", "kvas", "šampaňské", "sake"],
        "outside": ["mléko", "džus", "limonáda", "čaj", "káva", "kakao",
                    "minerálka", "sirup"],
        "asks": ["vznikají kvašením", "dají se pít", "prodávají se v lahvích"],
    },
    {
        "id": "mesice-31",
        "roof": "měsíce v roce",
        "level": "easy",
        "inside": ["leden", "březen", "květen", "červenec", "srpen", "říjen", "prosinec"],
        "outside": ["únor", "duben", "červen", "září", "listopad"],
        "asks": ["mají jednatřicet dní", "jsou to měsíce", "mají v roce pevné pořadí"],
    },
    {
        "id": "sachy-figury",
        "roof": "šachové figury",
        "level": "normal",
        "inside": ["věž", "střelec", "dáma", "pěšec"],
        "outside": ["kůň", "král"],
        "asks": ["táhnou po přímé nebo šikmé řadě", "stojí na šachovnici", "dají se vyměnit"],
    },
]

# Druhá dávka: doplňky do rodin výše a rodiny nové. Drží se zvlášť, aby
# se první dávka nemusela přepisovat pokaždé, když něco přibude.
from intruder_families2 import EXTRA, MORE, MORE_ASKS  # noqa: E402

for _family in FAMILIES:
    _more = MORE.get(_family["id"])
    if not _more:
        continue
    for _side in ("inside", "outside"):
        _seen = set(_family[_side])
        _family[_side] += [w for w in _more.get(_side, []) if w not in _seen]

from intruder_families3 import EXTRA3  # noqa: E402
from intruder_families4 import EXTRA4  # noqa: E402
from intruder_families5 import HIDDEN  # noqa: E402
from intruder_families6 import FAMILIES6  # noqa: E402
from intruder_families7 import FAMILIES7  # noqa: E402
from intruder_families8 import FAMILIES8  # noqa: E402
from intruder_families9 import FAMILIES9  # noqa: E402
from intruder_families10 import FAMILIES10  # noqa: E402

FAMILIES += (EXTRA + EXTRA3 + EXTRA4 + HIDDEN + FAMILIES6 + FAMILIES7
             + FAMILIES8 + FAMILIES9 + FAMILIES10)

# Zavádějící věty se přidávají ke všem rodinám, i k těm z druhé dávky.
for _family in FAMILIES:
    _family["asks"] = _family["asks"] + [
        a for a in MORE_ASKS.get(_family["id"], []) if a not in _family["asks"]
    ]
