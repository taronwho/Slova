"""Hrubé škatulky slov — proti pěticím se dvěma správnými odpověďmi.

Hráč nahlásil pětici *labuť, plachty, srnec, orel, had* s osou „čtyři z nich
jsou souhvězdí". Vetřelec měl být *srnec*, jenže *plachty* jsou stejně dobrá
odpověď: zbylá čtyři slova jsou **zvířata**. Hádanka měla dvě řešení a hráč
přišel o body za tu druhou.

Kdy se to stane, se dá spočítat. Vetřelec je vždycky jeden a čtveřice jedna,
takže vadí jediný případ: **škatulku sdílí právě čtyři slova a jedno z nich
je vetřelec.** Pak totiž ta čtveřice není ta, kterou má rodina na mysli —
je to tři slova zevnitř a vetřelec, a ukazuje na jiné slovo.

Když škatulku sdílí všech pět, nikoho nevyděluje.

Zbývá třetí případ a ten se dlouho pouštěl dál: **škatulku sdílí právě ta
čtveřice zevnitř a vetřelec do ní nepatří.** Odpověď z toho vyjde stejná
jako z osy rodiny, takže se to bralo za neškodné. Není. Hráč poslal pětici
*lavička, opice, tygr, drak, krysa* s osou „čtyři z nich jsou znamení
čínského zvěrokruhu" a napsal k tomu, že by stačilo říct, že kromě lavičky
jsou to všechno zvířata. Měl pravdu: o zvěrokruhu se nemusel dozvědět nic,
osa byla k ničemu a hádanka se vyřešila za vteřinu. Chytá to `hrubsi_osa`.

Rodinu to nezabije, jen ji donutí hledat vetřelce **ve stejném soudku**:
„čtyři z nich jsou psi" potřebuje vedle sebe jiné zvíře, ne hrnec. Bez toho
se neptá na psy, ale na zvířata.

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
buvol cikáda dalmatin chroust chrousta ještěrka kiwi krysa králík mlok
motýl nandu ovčák slavík svišť sysel upír úhoř špic
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
avokádo bambus brambor brambora brambory dřín hořčice hřebíček jablka
kardamom kurkuma mrkev muškát oliva pepř pískavice saturejka sezam trnka
švestky vanilka nové_koření
durman heřmánek jmelí kaktus konvalinka kopřiva ocún oleandr pampeliška
podběl proskurník rulík řebříček sasanka tabák trnovník třezalka vlčí_mák
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


def hrubsi_osa(four: list[str], odd: str) -> str | None:
    """Vyděluje vetřelce něco hrubšího, než na co se rodina ptá?

    Vrací jméno škatulky, kterou sdílí **všechna čtyři** slova zevnitř
    a vetřelec do ní nepatří. Taková pětice se dá vyřešit bez osy rodiny —
    stačí si všimnout, že čtyři věci žijí a pátá ne.

    Rodinám, které se na tu škatulku ptají samy („čtyři z nich jsou zvířata
    chovaná lidmi"), to nevadí a volající je nechává být: tam osa a škatulka
    splývají a hrubší pohled neexistuje.
    """
    for tag, words in SKATULKY.items():
        if _ve_skatulce(odd, words):
            continue
        if all(_ve_skatulce(w, words) for w in four):
            return tag
    return None


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
