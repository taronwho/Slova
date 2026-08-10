"""Hrubé škatulky slov — proti pěticím se dvěma správnými odpověďmi.

Hráč nahlásil pětici *labuť, plachty, srnec, orel, had* s osou „čtyři z nich
jsou souhvězdí". Vetřelec měl být *srnec*, jenže *plachty* jsou stejně dobrá
odpověď: zbylá čtyři slova jsou **zvířata**. Hádanka měla dvě řešení a hráč
přišel o body za tu druhou.

Kdy se to stane, se dá spočítat. Vetřelec je vždycky jeden a čtveřice jedna,
takže vadí jediný případ: **škatulku sdílí právě čtyři slova a jedno z nich
je vetřelec.** Pak totiž ta čtveřice není ta, kterou má rodina na mysli —
je to tři slova zevnitř a vetřelec, a ukazuje na jiné slovo.

Když škatulku sdílí všech pět, nikoho nevyděluje. A když ji sdílí právě ta
čtveřice zevnitř, ukazuje na téhož vetřelce jako osa rodiny — dvě čtení,
jedna odpověď, žádná škoda. Proto se hlídá jen ten jeden případ; kdyby se
zakazovalo víc, přišly by rodiny jako „čtyři z nich jsou psi" o všechny
pětice, kde je vetřelec hrnec.

Škatulky jsou schválně hrubé a jen dvě. Nemají popisovat význam slov, jen
zachytit to, čeho si hráč všimne dřív než osy: že se něco hýbe a něco roste.
"""

# Zvíře je to, co hráč za zvíře považuje — včetně bájných (drak), plemen
# (jezevčík, ragdoll) a slov, která zvíře znamenají teprve v druhém významu
# (kobylka na houslích, žabka na smyčci). Škatulka má být raději širší:
# vadí přehlédnuté zvíře, ne zvíře navíc.
ZVIRATA = set("""
akvarijní_rybka andulka bažant beagle beran berani bernard beruška bobr
border_kolie brhlík britská_krátkosrstá brouk býk candát cejn činčila
chobotnice chrt cvrček čáp datel delfín dinosaurus drak draci emu had
havran holoubek holub humr husa husky hvězdice jaguár jelec jelen jestřáb
jezevčík jezevec ježdík ježek kachna kakapo kaloň kapr karas kasuár klíště
klokan kobylka kočka komár koroptev kos koza kozel kozoroh krab kráva
krevety krokodýl krtek křeček kuna kur kůň kůzlátko labuť lachtan ledňáček
lev liška los losos lín makrela manta medúza medvěd mník morče moucha
mravenec mrož murény mustang myš mšice netopýr nutrie okoun ondatra opice
orel ovce papoušek parma pavouk perlička perlorodka perská pes pijavice
platýs plch plotice poštolka prase pstruh ptakopysk ptáci pudl pštros racek
ragdoll rak retrívr ryba rybenka ryby rys siamská skřivan slepice slimák
slon sob sova srna srnec straka stonožka sumec sýkora sépie štika štír
škeble tuleň tučňák tygr velbloud velryba veverka vlaštovka vlci vlk vodník
volavka vosa vrabec vrápenec vydra výr vážka včela včelka vůl zajíc želva
žirafa žralok žába žížala žabka habešská mainská_mývalí mořský_ježek
mořský_koník larva_jepice
""".split())

# Rostlina včetně hub a plodů — pro hráče je to jedna hromada „něco, co
# roste". Stromy, koření i zelenina se počítají stejně.
ROSTLINY = set("""
akát anýz artyčok badyán bazalka bedla bez borovice borůvka broskev
brokolice brusinka bříza buk cedr celer chrpa chřest cibule cuketa cypřiš
česnek datle dobromysl douglaska dub dýně estragon fazole fenykl fiala
fialka habr hrách hrášek hruška hrušeň hřib hyacint jablko jahoda jalovec
jasan jedle jeřabina jeřáb jilm kapradí kaštan kdoule kleč klouzek kmín
konopí kopr kopretina koriandr kozák křemenáč křen kukuřice květák len
libeček lilek lilie lípa líska majoránka mango mech meduňka meloun meruňka
mišpule modřenec modřín muchomůrka muchovník mák máta narcis okurka olivy
olše orchidej oregano oskeruše ostružina paprika pastinák pažitka petržel
pivoňka platan pórek rebarbora rozmarýn růže ředkev ředkvička řepa sekvoj
slunečnice smrk sněženka sněženky sumak šafrán šalvěj šípek špenát švestka
tis topinambur topol tuje tulipán tuřín tymián třešeň václavka višeň vrba
zázvor žampion čočka jicama batáty černý_kořen bobkový_list
""".split())

# Víceslovná hesla se v seznamech píšou s podtržítkem, aby se dala rozdělit
# na slova. Pro porovnání se převedou zpátky na mezery.
SKATULKY = {
    "zvíře": {w.replace("_", " ") for w in ZVIRATA},
    "rostlina": {w.replace("_", " ") for w in ROSTLINY},
}

# Rodiny, které mají zvířata nebo rostliny přímo ve střeše, si škatulku
# doplní samy. Ručně psaný seznam nemůže být úplný — *upír* v něm chyběl
# a rodina „čtyři z nich umí aktivně létat" kvůli tomu přišla o všechny
# pětice: skript ji považoval za dvouřešitelnou, protože počítal tři
# zvířata místo čtyř. Střecha rodiny je spolehlivější zdroj než paměť.
STRECHY = {
    "zvíře": ("zvíř", "savc", "ptác", "hmyz", "živočich", "psí plemena"),
    "rostlina": ("strom", "houb", "květin", "zelenin", "ovoce", "koření"),
}


def doplnit(families: list[dict]) -> None:
    """Doplní škatulky o slova z rodin, které je mají přímo ve střeše."""
    for tag, marks in STRECHY.items():
        for family in families:
            roof = family.get("roof", "")
            # „slova, ve kterých se schovává zvíře" střecha není: ta slova
            # zvířata nejsou, jen je v sobě nesou.
            if roof.startswith("slova") or not any(m in roof for m in marks):
                continue
            SKATULKY[tag].update(family["inside"])
            SKATULKY[tag].update(family["outside"])


def _ve_skatulce(word: str, words: set[str]) -> bool:
    """Patří slovo do škatulky?

    Hesla bývají i víceslovná („netopýr velký", „mořský ježek"), a ta by se
    proti seznamu neshodla, i když je zvíře vidět na první pohled. Stačí
    proto, aby ve škatulce leželo kterékoli slovo z hesla.
    """
    return word in words or any(part in words for part in word.split())


def dve_reseni(four: list[str], odd: str) -> bool:
    """Má pětice druhou stejně dobrou odpověď?

    Vadí jen ten případ, kdy škatulku sdílí právě čtyři slova a **vetřelec
    je jedním z nich** — pak ta čtveřice ukazuje na jiné slovo než osa
    rodiny.
    """
    for words in SKATULKY.values():
        if _ve_skatulce(odd, words) and sum(_ve_skatulce(w, words) for w in four) == 3:
            return True
    return False
