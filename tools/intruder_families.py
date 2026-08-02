"""Rodiny pro Vetřelce — psané ručně, ne těžené z dat.

Každá rodina má **střechu** (co mají všechna slova společné) a **osu**
(čím se čtveřice liší od vetřelce). Střecha nemusí být taxonomická třída;
klidně to je „žijí ve vodě" napříč savci, rybami i korýši, nebo „najdeš to
v autě". Čím volnější střecha, tím víc práce svede osa.

`inside` jsou slova, která osu splňují, `outside` ta, která ne. Hádanka
vznikne výběrem čtyř zevnitř a jednoho zvenku, takže jedna rodina vydá na
desítky pětic.

`asks` jsou tři věty do druhého kroku. **První je ta správná** — dělí
čtveřici od vetřelce. Zbylé dvě platí pro čtveřici i pro vetřelce, takže
nic nevydělují; hráč musí poznat, která z těch tří opravdu odděluje.

`level`: easy = osa je nápadná, hard = střecha je těsně kolem osy.
"""

FAMILIES = [
    {
        "id": "voda-sladka",
        "roof": "živočichové, kteří žijí ve vodě",
        "axis": "sladká voda proti slané",
        "level": "hard",
        "inside": ["kapr", "štika", "sumec", "okoun", "bobr", "vydra", "rak", "pstruh"],
        "outside": ["tuleň", "treska", "sardinka", "krab", "chobotnice", "delfín"],
        "asks": ["žijí ve sladké vodě", "žijí ve vodě", "dají se jíst"],
    },
    {
        "id": "auto-vybava",
        "roof": "věci, které se dají najít v autě",
        "axis": "součást auta proti tomu, co se do něj jen vozí",
        "level": "easy",
        "inside": ["volant", "brzda", "zrcátko", "tachometr", "spojka", "airbag", "výfuk"],
        "outside": ["kufřík", "deka", "termoska", "mapa", "lékárnička"],
        "asks": ["jsou pevnou součástí auta", "najdeš je v autě", "vyrábějí se z umělé hmoty"],
    },
    {
        "id": "nastroje-smycce",
        "roof": "hudební nástroje",
        "axis": "hraje se smyčcem",
        "level": "normal",
        "inside": ["housle", "viola", "violoncello", "kontrabas"],
        "outside": ["kytara", "harfa", "loutna", "banjo", "cimbál"],
        "asks": ["hraje se na ně smyčcem", "mají struny", "hrají v orchestru"],
    },
    {
        "id": "koreni-semena",
        "roof": "koření",
        "axis": "je to semeno nebo plod, ne list",
        "level": "hard",
        "inside": ["pepř", "kmín", "koriandr", "muškát", "anýz", "hořčice"],
        "outside": ["bazalka", "tymián", "oregano", "šalvěj", "petržel"],
        "asks": ["je to plod nebo semeno", "voní", "používá se v kuchyni"],
    },
    {
        "id": "planety-kamenne",
        "roof": "planety sluneční soustavy",
        "axis": "kamenná planeta proti plynnému obru",
        "level": "normal",
        "inside": ["Merkur", "Venuše", "Země", "Mars"],
        "outside": ["Jupiter", "Saturn", "Uran", "Neptun"],
        "asks": ["mají pevný povrch", "obíhají kolem Slunce", "jsou vidět dalekohledem"],
    },
    {
        "id": "sporty-mic",
        "roof": "sporty",
        "axis": "hraje se s míčem",
        "level": "easy",
        "inside": ["fotbal", "házená", "volejbal", "basketbal", "ragby", "vodní pólo"],
        "outside": ["hokej", "šerm", "veslování", "krasobruslení", "box"],
        "asks": ["hraje se s míčem", "hrají se v družstvu", "mají olympijský turnaj"],
    },
    {
        "id": "kov-drahy",
        "roof": "kovy",
        "axis": "drahý kov",
        "level": "normal",
        "inside": ["zlato", "stříbro", "platina", "palladium"],
        "outside": ["železo", "měď", "hliník", "olovo", "cín", "zinek"],
        "asks": ["jsou to drahé kovy", "vedou elektřinu", "dají se tavit"],
    },
    {
        "id": "mesta-more",
        "roof": "evropská hlavní města",
        "axis": "leží u moře",
        "level": "hard",
        "inside": ["Lisabon", "Athény", "Kodaň", "Stockholm", "Helsinky", "Dublin"],
        "outside": ["Praha", "Vídeň", "Madrid", "Bern", "Budapešť", "Varšava"],
        "asks": ["leží u moře", "jsou to hlavní města", "leží v Evropě"],
    },
    {
        "id": "babicka-postavy",
        "roof": "postavy z Babičky Boženy Němcové",
        "axis": "vystupuje v Babičce",
        "level": "normal",
        "inside": ["babička", "Barunka", "Viktorka", "Kristla", "Mílo"],
        "outside": ["Maryša", "Jirka", "Švejk", "Cipísek"],
        "asks": ["vystupují v Babičce", "jsou to postavy z knihy", "napsal je český autor"],
    },
    {
        "id": "stromy-jehlicnany",
        "roof": "stromy",
        "axis": "jehličnan",
        "level": "easy",
        "inside": ["smrk", "borovice", "jedle", "modřín", "tis"],
        "outside": ["dub", "buk", "bříza", "javor", "lípa", "olše"],
        "asks": ["jsou to jehličnany", "rostou v lese", "dřevo se z nich zpracovává"],
    },
    {
        "id": "kuchyne-rez",
        "roof": "kuchyňské náčiní",
        "axis": "krájí nebo strouhá",
        "level": "normal",
        "inside": ["nůž", "struhadlo", "škrabka", "kráječ", "sekáček"],
        "outside": ["vařečka", "naběračka", "cedník", "metla", "prkénko"],
        "asks": ["krájejí nebo strouhají", "patří do kuchyně", "myjí se po vaření"],
    },
    {
        "id": "staty-bezmore",
        "roof": "evropské státy",
        "axis": "nemá přístup k moři",
        "level": "hard",
        "inside": ["Česko", "Rakousko", "Švýcarsko", "Maďarsko", "Slovensko", "Srbsko"],
        "outside": ["Polsko", "Chorvatsko", "Portugalsko", "Řecko", "Norsko", "Belgie"],
        "asks": ["nemají přístup k moři", "leží v Evropě", "sousedí s několika státy"],
    },
    {
        "id": "ptaci-nelet",
        "roof": "ptáci",
        "axis": "nelétá",
        "level": "normal",
        "inside": ["pštros", "tučňák", "emu", "kiwi", "nandu"],
        "outside": ["orel", "vrabec", "labuť", "čáp", "sova", "racek"],
        "asks": ["nelétají", "jsou to ptáci", "kladou vejce"],
    },
    {
        "id": "hodiny-cas",
        "roof": "věci, kterými se měří",
        "axis": "měří čas",
        "level": "easy",
        "inside": ["hodiny", "stopky", "budík", "přesýpací hodiny", "kalendář"],
        "outside": ["metr", "váha", "teploměr", "kompas", "odměrka"],
        "asks": ["měří čas", "něco měří", "mají stupnici nebo číslice"],
    },
]
