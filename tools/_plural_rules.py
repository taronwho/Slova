"""Pravidla pro 1. pád množného čísla nad českým hunspellem.

Český hunspell (cs_CZ.aff) má příznaky, které fungují jako deklinační vzory:
jeden příznak = jedno paradigma a v něm sada přípon. Nás zajímá jediná
„buňka" každého paradigmatu — 1. pád množného čísla. Ta se dá určit přesně,
protože přípona i podmínka jsou ve slovníku napsané:

    SFX H   0   y   [^ey]      hrad  -> hrady
    SFX Z   a   y   [^...]a    žena  -> ženy
    SFX M   o   a   [^c]o      město -> města
    SFX I   ch  ši  ch         hoch  -> hoši

Seznam níž je ruční, ale ověřený: skript tools/2c_plural.py u každého
pravidla vypíše vzorek vygenerovaných dvojic k namátkové kontrole.

Příznaky, které se *nepoužívají*, a proč:

    P  1. pád mn. č. nemá (hrad-typ životný ho tvoří příznakem I)
    Q  2. pád mn. č. bez koncovky („služba -> služeb", „tango -> tang")
    R  6. pád j. č. a odvozená příslovce — nerozlišitelné
    Y  skloňování přídavných jmen
    A B J T O X  časování sloves a příčestí
    C  směs odvozování a měkkého ženského vzoru — nespolehlivé
    y í é  stupňování a cizí jména
"""

# příznak -> množina dvojic (odtrhni, přidej); "0" znamená „neodtrhávej nic"
NOM_PL: dict[str, set[tuple[str, str]]] = {
    # --- mužský rod životný ---------------------------------------------
    # I a V jsou celé v 1. pádě mn. č. (-i s alternací, -ové). Jediná
    # výjimka je I o->i: to nepatří mužům, ale středním („koleno -> koleni"
    # je 6. pád j. č., 1. pád mn. č. je „kolena").
    "I": {
        ("0", "i"), ("a", "i"), ("k", "ci"), ("ek", "ci"), ("el", "li"),
        ("h", "zi"), ("ch", "ši"), ("r", "ři"), ("re", "ři"),
        ("ď", "di"), ("ň", "ni"), ("ť", "ti"),
        ("děk", "ďci"), ("něk", "ňci"), ("těk", "ťci"),
    },
    "V": {
        ("0", "ové"), ("0", "vé"), ("a", "ové"), ("e", "ové"),
        ("ek", "kové"), ("el", "lové"), ("eň", "ňové"),
    },
    "U": {("ec", "ci"), ("0", "i"), ("a", "ové"), ("e", "i")},
    "D": {("0", "é"), ("a", "é"), ("us", "ové"), ("us", "i"), ("us", "y")},
    # --- mužský rod neživotný -------------------------------------------
    "H": {("0", "y"), ("e", "y")},
    "L": {("0", "y"), ("ek", "ky"), ("en", "ny")},
    "S": {("0", "e"), ("ec", "ce"), ("ť", "tě"), ("eň", "ně"), ("ň", "ně"), ("0", "y")},
    # --- ženský rod ------------------------------------------------------
    "Z": {
        ("a", "y"),
        ("eň", "ně"),
        ("ň", "ně"),
        ("ev", "ve"),
        ("ec", "ce"),
        ("ť", "tě"),
        ("ď", "dě"),
        ("0", "e"),
        ("0", "ě"),
    },
    "K": {
        ("0", "i"),
        ("ď", "di"),
        ("ť", "ti"),
        ("ý", "osti"),
        ("í", "osti"),
        ("e", "ata"),
        ("ě", "ata"),
        ("ně", "ňata"),
        ("tě", "ťata"),
        ("dě", "ďata"),
        ("es", "si"),
    },
    # --- střední rod -----------------------------------------------------
    "M": {("o", "a"), ("co", "ka"), ("on", "a"), ("um", "a")},
}

# Vzory podstatných jmen. Příznaky I, V a D se přidávají k některému z nich
# a samy o sobě nic neurčují — hunspell jimi obsluhuje i číslovky
# („deset/I" -> „deseti") a slovesa („být/IN"). Bez souseda z tohohle
# seznamu se proto nepoužijí.
NOUN_FLAGS = {"P", "U", "H", "L", "S", "Z", "K", "M"}
NEEDS_NOUN_FLAG = {"I", "V", "D"}
