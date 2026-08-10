"""Osmá várka rodin — padesát os, které tu ještě nebyly.

Dosavadní rodiny stály na třech nápadech: pravidlo o písmenech, slovo má
druhý význam, slovo stojí v názvu. Padesát dalších rodin téhož ražení by
sadu nafouklo, ale hru by nezměnilo — hráč by pořád hledal jednu ze tří
věcí a čtvrté kolo by se hrálo jako první.

Tahle várka proto přidává **pět nových druhů osy**:

1. **Fyzikální vlastnost.** *korek, dřevo, led, olej, kámen* — čtyři plavou.
   Souvislost není v tom, co ta slova znamenají, ale co ty věci dělají, a
   hráč ji ověří v hlavě, ne pamětí.
2. **Praktické použití.** Vejde se do kapsy, teče z toho voda, potřebuje to
   aspoň dva lidi. Osa ze života, ne ze slovníku.
3. **Mluvnice.** Slova jen v množném čísle (*dveře, kalhoty, housle*),
   nesklonná (*kupé, tabu, taxi*), slova, ze kterých po odtržení předpony
   zbude jiné slovo (*podnos → nos*).
4. **Ustálené spojení.** Čtyři z nich tvoří dvojici se slovem *zlatý*:
   zlatý déšť, zlatá horečka, zlaté ručičky, zlatý řez.
5. **Text, který zná každý.** Slova z české hymny, z přísloví, z pranostik.

Slova vně se u většiny rodin **nedají brát z nudné zásoby**. U rodiny „čtyři
z nich plavou" musí vetřelec být věc, která se potopí — ne *deštník*, o kterém
nikdo neví, jak to s ním je. Proto má skoro každá rodina vlastní seznam
vetřelců, u kterých je vlastnost jistě opačná.

Kontroly (jedinečná otázka, rámec věty do vyhodnocení, ověřitelné zavádějící
věty) jsou tytéž jako v sedmé várce a berou se odtud.

Spuštění:  python3 tools/gen_families8.py
Výstup:    tools/intruder_families8.py
"""

import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from gen_families7 import VATA, decoys, zapis, zkontroluj_vetu  # noqa: E402

OUT = os.path.join(HERE, "intruder_families8.py")


def s(text: str) -> list[str]:
    """Slova oddělená mezerou. Víceslovná hesla se sem nevejdou a nemají."""
    return text.split()


RODINY = [
    # ------------------------------------------------ fyzikální vlastnost --
    dict(id="vlast-plavou", level="normal",
         roof="věci, které plavou na vodě",
         ask="plavou na vodě",
         inside=s("korek dřevo led olej polystyren pěna sláma vosk"),
         outside=s("kámen cihla hřebík mince klíč sekera podkova žehlička kladivo kotva")),
    dict(id="vlast-rozpusti", level="normal",
         roof="věci, které se rozpustí ve vodě",
         ask="se rozpustí ve vodě",
         inside=s("sůl cukr soda med sirup mýdlo bonbon želatina"),
         outside=s("písek olej sklo vosk korek plast dřevo štěrk kámen křída")),
    dict(id="vlast-magnet", level="normal",
         roof="věci, které přitáhne magnet",
         ask="přitáhne magnet",
         inside=s("hřebík sponka šroub jehla plech podkova pilník konzerva"),
         outside=s("guma sklo dřevo papír plast hliník měď keramika provaz korek")),
    dict(id="vlast-proud", level="hard",
         roof="látky, které vedou elektřinu",
         ask="vedou elektřinu",
         inside=s("měď hliník železo stříbro zlato ocel mosaz grafit"),
         outside=s("sklo guma dřevo plast papír keramika korek vosk porcelán vzduch")),
    dict(id="vlast-hori", level="normal",
         roof="věci, které hoří",
         ask="hoří",
         inside=s("papír dřevo sláma vosk uhlí líh benzin seno"),
         outside=s("kámen sklo písek cihla beton hlína voda plech keramika mramor")),
    dict(id="vlast-roztaji", level="normal",
         roof="věci, které roztají v teple",
         ask="roztají v teple",
         inside=s("led čokoláda máslo sníh vosk zmrzlina sádlo parafín"),
         outside=s("kámen sklo dřevo mince guma křída cukr sůl cihla hřebík")),
    dict(id="vlast-pruhledne", level="normal",
         roof="věci, které jsou průhledné",
         ask="jsou průhledné",
         inside=s("sklo led voda celofán křišťál plexisklo bublina igelit"),
         outside=s("cihla dřevo plech papír kámen keramika guma korek plátno beton")),
    dict(id="vlast-rezavi", level="normal",
         roof="věci, které rezaví",
         ask="rezaví",
         inside=s("hřebík plech řetěz sekera kotva kolejnice brnění pilník"),
         outside=s("sklo plast dřevo guma keramika papír korek kámen hliník zlato")),
    dict(id="vlast-svetlo", level="hard",
         roof="věci, které vydávají vlastní světlo",
         ask="vydávají vlastní světlo",
         # Měsíc mezi vetřelci schválně: svítí jen odraženým světlem, a je to
         # past, na kterou hráč skočí, dokud si nevzpomene proč.
         inside=s("hvězda oheň blesk světluška svíčka láva slunce výboj"),
         outside=s("měsíc zrcadlo sklo sníh mrak hladina stříbro led okno mince")),
    dict(id="vlast-ohnout", level="normal",
         roof="věci, které se dají ohnout, aniž prasknou",
         ask="se dají ohnout, aniž prasknou",
         inside=s("drát guma provaz plech proutek hadice papír kůže"),
         outside=s("sklo cihla křída keramika led talíř žárovka dlaždice prkno beton")),
    dict(id="vlast-dute", level="hard",
         roof="věci, které jsou uvnitř duté",
         ask="jsou uvnitř duté",
         inside=s("trubka míč sud láhev buben zvon komín brčko"),
         outside=s("cihla kámen prkno kladivo klíč mince špalek dlaždice sekera žehlička")),
    dict(id="vlast-nafouknout", level="normal",
         roof="věci, které se dají nafouknout",
         ask="se dají nafouknout",
         inside=s("balón duše pneumatika matrace míč bublina plíce člun"),
         outside=s("cihla kámen prkno hrnec židle kniha klíč talíř lopata žebřík")),

    # ------------------------------------------------- praktické použití --
    dict(id="vlast-kapsa", level="normal",
         roof="věci, které se vejdou do kapsy",
         ask="se vejdou do kapsy",
         inside=s("klíč mince zápalky hřeben kapesník propiska mobil sponka"),
         outside=s("žebřík koberec pračka židle kolo dveře matrace lampa žehlička kufr")),
    dict(id="vlast-syrove", level="normal",
         roof="jídlo, které se dá jíst syrové",
         ask="se dají jíst syrové",
         inside=s("mrkev jablko okurka ořech rajče med salát hruška"),
         outside=s("brambora fazole rýže těstoviny mouka čočka kroupy hrách krupice pohanka")),
    dict(id="vlast-bez-proudu", level="normal",
         roof="věci, které fungují bez proudu i baterií",
         ask="fungují bez proudu i baterií",
         inside=s("kompas kladivo brýle kolo deštník píšťalka lopata žebřík"),
         outside=s("mobil rádio vysavač žehlička baterka notebook lednička mikrovlnka sekačka pračka")),
    dict(id="vlast-bez-dilu", level="hard",
         roof="věci, které nemají žádný pohyblivý díl",
         ask="nemají žádný pohyblivý díl",
         inside=s("cihla sklenice talíř prkno deka hrnec kbelík dlaždice"),
         outside=s("nůžky klika hodinky kolo dveře pumpa zip jeřáb váha pila")),
    dict(id="vlast-dva-lidi", level="normal",
         roof="věci, které potřebují aspoň dva lidi",
         ask="potřebují aspoň dva lidi",
         inside=s("šachy tenis rozhovor tanec souboj přetahovaná svatba badminton"),
         outside=s("čtení běh plavání šití kreslení spánek pletení rybaření žonglování luštění")),
    dict(id="vlast-srolovat", level="normal",
         roof="věci, které se dají složit nebo srolovat",
         ask="se dají složit nebo srolovat",
         inside=s("deka mapa deštník stan noviny koberec spacák plátno"),
         outside=s("sklenice cihla hrnec klíč žehlička talíř kladivo zrcadlo žárovka police")),
    dict(id="vlast-strecha", level="hard",
         roof="věci, které jsou na střeše domu",
         ask="jsou na střeše domu",
         inside=s("komín anténa hromosvod okap korouhvička vikýř satelit taška"),
         outside=s("sklep práh schod koberec klika kamna vana umyvadlo plot dlažba")),
    dict(id="vlast-voda-tece", level="normal",
         roof="věci, ze kterých teče voda",
         ask="teče z nich voda",
         inside=s("kohoutek hadice sprcha konev okap fontána pramen konvice"),
         outside=s("lampa koš polštář kniha židle zrcadlo žebřík koberec hřebík mísa")),

    # ------------------------------------------------------------ mluvnice --
    dict(id="mluv-pomnozna", level="normal",
         roof="slova, která se používají jen v množném čísle",
         ask="se používají jen v množném čísle",
         inside=s("dveře kalhoty nůžky housle brýle kamna vrata sáně narozeniny kleště"),
         outside=s("stůl okno kniha lampa židle talíř klíč koš hrnec police")),
    dict(id="mluv-spodoba", level="hard",
         roof="slova, která se na konci vyslovují jinak, než píšou",
         ask="se na konci vyslovují jinak, než se píšou",
         inside=s("dub led plod vůz nůž hrad mráz sad obraz sníh"),
         outside=s("stůl okno klíč lampa kniha most pes list koš papír")),
    dict(id="mluv-predpona", level="hard",
         roof="slova, ze kterých po odtržení předpony zbude jiné slovo",
         # podnos → nos, výlet → let, zápas → pas, nádech → dech,
         # příklad → klad, útok → tok, rozum → um, odchod → chod
         ask="po odtržení předpony z nich zbude jiné slovo",
         inside=s("podnos výlet zápas nádech příklad útok rozum odchod"),
         outside=s("koberec sklenice lampa žebřík mrkev police talíř kniha hrnec zahrada")),
    dict(id="mluv-nesklonna", level="hard",
         roof="slova, která se neskloňují",
         # Kino, metro a rádio mezi vetřelci: vypadají stejně cize, ale
         # skloňují se (do kina, v metru), a na tom se rodina láme.
         ask="se neskloňují",
         inside=s("kupé tabu taxi menu alibi whisky kakadu iglú"),
         outside=s("auto kino metro rádio sako víno pero okno sklo lano")),
    dict(id="mluv-prijmeni", level="hard",
         roof="slova, která jsou zároveň běžná česká příjmení",
         ask="jsou to zároveň běžná česká příjmení",
         inside=s("kovář kolář sedlák mlynář král zima kříž mráz"),
         outside=s("hrnec deštník police koště lampa žebřík koberec mrkev talíř kbelík")),
    dict(id="mluv-zdrobnelina", level="hard",
         roof="slova, jejichž zdrobnělina znamená něco jiného",
         # hlavička šroubu, ručička hodin, kobylka na houslích, žabka na
         # smyčci, panenka oka, ouško jehly, kolénko trubky, hřebíček koření
         ask="jejich zdrobnělina znamená něco úplně jiného",
         inside=s("hlava ruka kobyla žába panna ucho koleno hřebík"),
         outside=s("stůl okno police koberec lampa talíř žebřík kbelík mrkev hrnec")),
    dict(id="mluv-vyjmenovana", level="normal",
         roof="vyjmenovaná slova",
         ask="jsou to vyjmenovaná slova",
         inside=s("nábytek kopyto mlýn plyn lyže pytel sýr hmyz mýto chmýří"),
         outside=s("stůl okno police koberec lampa talíř žebřík kbelík mrkev hrnec")),

    # -------------------------------------------------- ustálená spojení --
    dict(id="spoj-zlaty", level="hard",
         roof="slova, která tvoří dvojici se slovem zlatý",
         ask="tvoří se slovem zlatý ustálené spojení",
         inside=s("déšť horečka ručičky řez hřeb klec svatba důl"),
         outside=s("police koberec žebřík mrkev talíř kbelík hrnec lampa sešit deštník")),
    dict(id="spoj-cerny", level="normal",
         roof="slova, která tvoří dvojici se slovem černý",
         ask="tvoří se slovem černý ustálené spojení",
         inside=s("díra humor skříňka pasažér svědomí hodinka kašel listina"),
         outside=s("police koberec žebřík mrkev talíř kbelík hrnec lampa sešit deštník")),
    dict(id="spoj-volny", level="normal",
         roof="slova, která tvoří dvojici se slovem volný",
         ask="tvoří se slovem volný ustálené spojení",
         inside=s("pád čas noha ruka styl místo chvíle vstup"),
         outside=s("police koberec žebřík mrkev talíř kbelík hrnec lampa sešit deštník")),
    dict(id="spoj-studena", level="hard",
         roof="slova, která tvoří dvojici se slovem studený",
         ask="tvoří se slovem studený ustálené spojení",
         inside=s("válka sprcha kuchyně hlava bufet start čaj zbraň"),
         outside=s("police koberec žebřík mrkev talíř kbelík hrnec lampa sešit deštník")),

    # ----------------------------------------------- text, který zná každý --
    dict(id="text-hymna", level="hard",
         roof="slova z české hymny",
         ask="jsou v české hymně",
         inside=s("domov voda bory sad jaro květ ráj země"),
         outside=s("police koberec žebřík mrkev talíř kbelík hrnec lampa sešit deštník")),
    dict(id="text-prislovi", level="normal",
         roof="slova z českých přísloví",
         # Kdo jinému jámu kopá; Bez práce nejsou koláče; Tichá voda břehy
         # mele; Ranní ptáče dál doskáče; Jablko nepadá daleko od stromu;
         # Každý hrnec si najde svou pokličku; Narazila kosa na kámen.
         ask="stojí v českých příslovích",
         inside=s("jáma koláč břeh ptáče jablko poklička kosa kámen"),
         outside=s("police žebřík mrkev talíř kbelík lampa sešit deštník koberec ubrus")),
    dict(id="text-pranostiky", level="hard",
         roof="slova z pranostik",
         # Únor bílý, pole sílí; Březen, za kamna vlezem; Medardova kápě;
         # Studený máj, v stodole ráj; Na svatého Řehoře šelma sedlák.
         ask="stojí v pranostikách",
         inside=s("pole kamna kápě stodola sedlák ráj máj led"),
         outside=s("police žebřík mrkev talíř kbelík lampa sešit deštník koberec ubrus")),

    # ------------------------------------- slovo je zároveň něco jiného --
    dict(id="obor-kostel", level="hard",
         roof="slova, která jsou zároveň části kostela",
         ask="jsou to zároveň části kostela",
         inside=s("loď věž kůr oltář zvonice klenba sloup kříž"),
         outside=s("police žebřík mrkev talíř kbelík lampa sešit deštník koberec ubrus")),
    dict(id="obor-vcely", level="hard",
         roof="slova, která jsou zároveň včelařské pojmy",
         ask="jsou to zároveň včelařské pojmy",
         inside=s("matka roj plást úl rámek medomet dýmák vosk"),
         outside=s("police žebřík mrkev talíř kbelík lampa sešit deštník koberec ubrus")),
    dict(id="obor-siti", level="normal",
         roof="slova, která jsou zároveň pojmy ze šití",
         ask="jsou to zároveň pojmy ze šití",
         inside=s("jehla náprstek steh lem špendlík střih náplet knoflík"),
         outside=s("police žebřík mrkev talíř kbelík lampa sešit deštník koberec ubrus"),
         avoid=s("nůžky")),
    dict(id="obor-ryby", level="hard",
         roof="slova, která jsou zároveň rybářské pojmy",
         ask="jsou to zároveň rybářské pojmy",
         inside=s("muška prut splávek naviják podběrák návnada třpytka olůvko"),
         outside=s("police žebřík mrkev talíř kbelík lampa sešit deštník koberec ubrus")),
    dict(id="obor-obloha", level="normal",
         roof="slova, která jsou zároveň úkazy na obloze",
         ask="jsou to zároveň úkazy na obloze",
         inside=s("duha blesk zatmění kometa záře meteor halo mlhovina"),
         outside=s("police žebřík mrkev talíř kbelík lampa sešit deštník koberec ubrus")),
    dict(id="obor-rybniky", level="hard",
         roof="slova, která jsou zároveň jména jihočeských rybníků",
         ask="jsou to zároveň jména jihočeských rybníků",
         inside=s("svět naděje rožmberk bezdrev dvořiště staňkovský"),
         outside=s("police žebřík mrkev talíř kbelík lampa sešit deštník koberec ubrus")),

    # ------------------------------------------- další vlastnosti věcí ----
    dict(id="vlast-krehke", level="normal",
         roof="věci, které se rozbijí, když spadnou",
         ask="se rozbijí, když spadnou",
         inside=s("sklenice talíř vejce žárovka zrcadlo váza hrnek porcelán"),
         outside=s("guma plech provaz polštář deka klíč kladivo míč bota kabát")),
    dict(id="vlast-vzduch", level="hard",
         roof="věci, které bez vzduchu nefungují",
         ask="bez vzduchu nefungují",
         inside=s("oheň plachetnice drak větrník píšťala plíce vrtule bublina"),
         outside=s("baterka hodinky kámen magnet sklo klíč zrcadlo provaz mince cihla")),
    dict(id="vlast-nit", level="hard",
         roof="věci, které se dají navléknout na nit",
         ask="se dají navléknout na nit",
         inside=s("korálek knoflík perla těstovina jeřabina prsten matice kroužek"),
         outside=s("cihla talíř deka sklenice kniha lampa mrkev provaz hrnec koberec")),
    dict(id="vlast-studene", level="hard",
         roof="věci, které jsou na dotek studené i v teple",
         ask="jsou na dotek studené i v teplé místnosti",
         inside=s("kov kámen dlaždice sklo zrcadlo klika mince keramika"),
         outside=s("dřevo vlna papír polštář deka koberec korek kabát ručník sláma")),
    dict(id="vlast-natahnout", level="normal",
         roof="věci, které se dají natáhnout",
         ask="se dají natáhnout",
         inside=s("guma žvýkačka těsto pružina ponožka prak punčocha lano"),
         outside=s("sklo cihla klíč talíř prkno hřebík kámen sklenice lžíce zrcadlo")),
    dict(id="vlast-nuzky", level="normal",
         roof="věci, které se dají přestřihnout nůžkami",
         ask="se dají přestřihnout nůžkami",
         inside=s("papír látka provaz nit vlasy stuha fólie lepenka"),
         outside=s("drát plech sklo prkno cihla klíč kámen trubka hřebík dlaždice")),
    dict(id="vlast-toci", level="normal",
         roof="věci, které se točí dokola",
         ask="se točí dokola",
         inside=s("kolo vrtule gramodeska ruleta mlýn kolotoč zeměkoule setrvačník"),
         outside=s("žebřík police most plot koberec cihla lampa komín schod plaňka")),
    dict(id="vlast-pruzina", level="hard",
         roof="věci, které mají v sobě pružinu",
         ask="mají v sobě pružinu",
         inside=s("matrace propiska kolíček past hodinky trampolína váha zapalovač"),
         outside=s("talíř cihla sklenice koberec deka kniha hrnec žebřík mrkev ubrus")),
    dict(id="vlast-hrebik", level="normal",
         roof="věci, které se věší na hřebík",
         ask="se věší na hřebík",
         inside=s("obraz zrcadlo kalendář kabát hodiny klíče věnec ručník"),
         outside=s("koberec cihla sporák vana postel lednička gauč stůl kamna dlažba")),
    dict(id="vlast-cinkaji", level="normal",
         roof="věci, které chrastí nebo cinkají",
         ask="chrastí nebo cinkají",
         inside=s("rolnička klíče řetěz zvonek chrastítko mince náramek plechovka"),
         outside=s("polštář deka houba koberec kniha mrkev ručník papír provaz chleba")),
]


HLAVICKA = '''"""Osmá várka rodin — padesát os, které tu ještě nebyly.

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

FAMILIES8 = ['''


def main() -> int:
    rodiny = []
    for spec in RODINY:
        rng = random.Random(spec["id"])
        zkontroluj_vetu(spec["ask"])

        inside = list(spec["inside"])
        outside = [w for w in spec.get("outside", VATA.split())
                   if w not in inside and w not in spec.get("avoid", [])]
        if len(inside) < 6:
            raise SystemExit(f"{spec['id']}: jen {len(inside)} slov uvnitř")
        if len(outside) < 8:
            raise SystemExit(f"{spec['id']}: jen {len(outside)} slov vně")

        rodiny.append({
            "id": spec["id"],
            "roof": spec["roof"],
            "level": spec["level"],
            "hidden": True,
            "inside": inside,
            "outside": outside,
            "asks": [spec["ask"]] + decoys(spec, inside + outside, rng),
        })

    # Otázka je klíč rodiny a nesmí se opakovat. Sada tuhle várku už může
    # obsahovat (je do ní zapojená), takže se vlastní rodiny vyjmou.
    from intruder_families import FAMILIES as STARE  # noqa: E402
    moje = {r["id"] for r in rodiny}
    stare = {f["asks"][0] for f in STARE if f["id"] not in moje}
    videne = set()
    for r in rodiny:
        ask = r["asks"][0]
        if ask in stare:
            raise SystemExit(f"{r['id']}: otázka už patří jiné rodině — {ask!r}")
        if ask in videne:
            raise SystemExit(f"dvě rodiny mají tutéž otázku: {ask!r}")
        videne.add(ask)

    zapis(rodiny, OUT, HLAVICKA)
    po_urovni: dict[str, int] = {}
    for r in rodiny:
        po_urovni[r["level"]] = po_urovni.get(r["level"], 0) + 1
    print(f"rodin: {len(rodiny)}  " + "  ".join(
        f"{k}: {v}" for k, v in sorted(po_urovni.items())))
    for r in rodiny:
        print(f"  {r['id']:22} {r['level']:6} {len(r['inside']):3} uvnitř, "
              f"{len(r['outside']):3} vně   {' '.join(r['inside'][:6])}")
    print(f"-> {os.path.normpath(OUT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
