"""Je to slovo základní tvar? Jedno rozhodnutí pro kroky 2b i 2c.

Stojí na tom, že příznaky v cs_CZ.dic jsou skloňovací a časovací vzory
a pověsit se dají jedině na základní tvar. Lemmatizér je druhý hlas: chytá
ohýbané tvary, které v hunspellu stojí jako samostatná hesla („budu",
„chce", „jdu").

Sám o sobě je ale nespolehlivý. Hráč nahlásil, že Voština neuznává
*lysinu* — lemmatizér u ní tvrdí, že základní tvar je „lysin", jenže žádné
takové slovo neexistuje a `lysina/ZQ` stojí v hunspellu jako řádné heslo se
vzorem. Slovo přesto vypadlo, a s ním skoro dva tisíce dalších (*kuře,
kotě, kalhoty, nůžky, játra, krém, trefa, želva, zmrzlina*).

Jeho nesouhlas se proto bere vážně jen tehdy, když **tvar, který navrhuje,
je sám heslem v .dic**. Když si ho vymyslel, rozhoduje slovník — a protože
si vymýšlí hlavně infinitivy („řeknu" → „řeknout", „napíšu" → „napsát"),
pouštějí se zpátky jen slova se jmenným nebo přídavným vzorem. Časovaná
slovesa zůstanou venku i tak.
"""

# Vzory, které dokládají základní tvar.
#   P U H L S Z K M D I V  jmenné vzory
#   Q C                    krácení kmene a odvozování, také jen od 1. pádu
#   Y                      skloňování přídavných jmen
#   A B J T                časování sloves
BASE_FLAGS = set("PUHLSZKMDIVQCYABJT")

# Jmenné a přídavné zvlášť od časovacích — viz úvod.
JMENNE_FLAGS = set("PUHLSZKMDIVQCY")
SLOVESNE_FLAGS = set("ABJT")


def je_zaklad(word, flags, lemma, dic, extra=frozenset()):
    """`flags` jsou příznaky slova, `lemma` výstup lemmatizéru, `dic` celý slovník."""
    if not (flags & BASE_FLAGS) and word not in extra:
        return False
    if lemma == word:
        return True
    # Lemmatizér nesouhlasí. Věří se mu, jen když tvar, který navrhuje,
    # v .dic doopravdy je — jinak si ho vymyslel a platí vzor u hesla.
    if lemma in dic:
        return False
    return bool(flags & JMENNE_FLAGS) and not (flags & SLOVESNE_FLAGS)
