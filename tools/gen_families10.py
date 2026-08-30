"""Desátá várka rodin — sto skrytých os, a pokaždé jiná povaha.

Devátá várka ukázala, že Vetřelec neroste počtem pětic, ale počtem **různých
věcí, které musí hráč zkusit**, než souvislost najde. Tahle várka jde stejnou
cestou a přidává sto rodin, rozdělených do skupin, které si nejsou podobné:

* **tělo u věcí** — ucho hrnce, zuby pily, jazyk boty; slovo zná každý, ale
  že je to jedna a tatáž věc, dojde až po chvíli,
* **ustálená spojení** — těžký, horký, slepý, mrtvý, šedý, tvrdý,
* **řemesla a obory s vlastní řečí** — kovárna, huť, hasiči, filatelie,
  účetnictví, hornictví; slova jsou všední, druhý význam odborný,
* **části věcí** — květ, zub, houba, kytara, kamna, most, kniha, střecha,
* **písmena a mluvnice** — slabikotvorné r, koncovka -tel, háčky, kroužek,
  useknuté první písmeno; tady pravidlo hlídá stroj,
* **příroda podle chování** — co táhne, co spí zimu, co svléká kůži,
* **prameny názvů** — May, Havel, Kundera, Zeman, Chaplin, Dickens, Mucha,
  Menzel, Štorch,
* **vlastnosti a děje** — co saje vodu, co ji odpuzuje, co hasí, co unese
  vítr, co svítí jen odraženým světlem.

Slova vně jsou skoro všude psaná ručně a schválně **ze stejného soudku** jako
slova uvnitř: u tažných ptáků stojí vně ptáci stálí, u jedovatých rostlin
rostliny neškodné, u zapalovaných světel světla elektrická. Bez toho by osa
sklouzla na „čtyři jsou ptáci“ a hádanka by měla dvě řešení.

U rodin s pravidlem o písmenech ověřuje stroj obě strany naráz: každé slovo
uvnitř pravidlu vyhovět musí a každé slovo vně nesmí. Pravidlo je jeden
zdroj pravdy pro obojí, takže se nedá omylem rozejít.

Spuštění:  python3 tools/gen_families10.py
Výstup:    tools/intruder_families10.py
"""

import json
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from gen_families7 import VATA, decoys, zapis, zkontroluj_vetu  # noqa: E402

OUT = os.path.join(HERE, "intruder_families10.py")

FOLD = str.maketrans("áčďéěíňóřšťúůýž", "acdeeinorstuuyz")
SAMOHLASKY = set("aeiouy")


def fold(word: str) -> str:
    return word.lower().translate(FOLD)


def s(text: str) -> list[str]:
    return text.split()


def slovnik() -> set[str]:
    """Ověřená základní slova hry. Mimo build se sáhne po fixtuře testů."""
    cesta = os.path.join(HERE, "out", "lexicon_base.json")
    if os.path.exists(cesta):
        base = json.load(open(cesta, encoding="utf-8"))
        return {w for delka in base for w, _ in base[delka]}
    return set(json.load(open(
        os.path.join(HERE, "..", "tests", "fixtures", "base-forms.json"),
        encoding="utf-8")))


SLOVNIK = slovnik()


def sousedni(spec: dict, rodiny: list[dict], rng: random.Random) -> list[str]:
    """
    Vetřelci ze sousedních rodin téže skupiny.

    U řemesel a částí věcí je nudná zásoba domácích potřeb špatně: čtyři
    kovářské termíny a *prostěradlo* pozná hráč, aniž by o kovařině cokoli
    věděl. Vetřelec proto přichází z **jiného řemesla** — u kovárny je to
    třeba tkalcovská *osnova*. Věta „čtyři z nich jsou zároveň kovářské
    pojmy — osnova ne" pak platí doslova a hádanka se konečně ptá na to,
    na co se ptát chce: víš, co ke kterému řemeslu patří?

    Slovo, které leží uvnitř **dvou a víc** rodin skupiny, se za vetřelce
    nebere. *Měch* je díl varhan i kovářské náčiní a *obruč* patří k sudu
    i k bubnu; u takového slova by rozhodnutí nebylo jednoznačné a hráč by
    měl pravdu, i kdyby ukázal jinam.
    """
    skupina = [r for r in rodiny if r.get("skupina") == spec["skupina"]]
    kolikrat: dict[str, int] = {}
    for r in skupina:
        for w in set(r["inside"]):
            kolikrat[w] = kolikrat.get(w, 0) + 1
    doma = set(spec["inside"]) | set(spec.get("avoid", []))
    pool = sorted(
        w for r in skupina if r["id"] != spec["id"]
        for w in r["inside"]
        if kolikrat[w] == 1 and w not in doma
    )
    if len(pool) < 10:
        raise SystemExit(f"{spec['id']}: sousedních slov je jen {len(pool)}")
    return sorted(rng.sample(pool, 12))


def slabikotvorne(word: str) -> bool:
    """Nese r nebo l celou slabiku — je z obou stran mezi souhláskami."""
    f = fold(word)
    for i, ch in enumerate(f):
        if ch not in "rl":
            continue
        pred = i == 0 or f[i - 1] not in SAMOHLASKY
        za = i == len(f) - 1 or f[i + 1] not in SAMOHLASKY
        if pred and za:
            return True
    return False


def bez_prvniho(word: str) -> bool:
    """Po useknutí prvního písmene zbude jiné slovo ze slovníku hry."""
    return len(word) > 3 and word[1:] in SLOVNIK


PRAVIDLA = {
    "slabikotvorne": slabikotvorne,
    "koncovka-tel": lambda w: fold(w).endswith("tel"),
    "hacky": lambda w: any(ch in w.lower() for ch in "ďťň"),
    "krouzek": lambda w: "ů" in w.lower(),
    "bez-prvniho": bez_prvniho,
}


RODINY: list[dict] = [
    # ================================================== tělo u věcí (7) ====
    dict(id="v10-ucho", level="normal",
         roof="věci, které mají ucho",
         ask="mají ucho, i když neslyší",
         inside=s("jehla hrnec konev džbán taška kabelka kotel šálek"),
         outside=s("kniha lampa koberec prkno deka mýdlo sešit ručník provaz"
                   " cihla svíčka zrcadlo")),
    dict(id="v10-zuby", level="normal",
         roof="věci, které mají zuby",
         ask="mají zuby, i když nic nejedí",
         inside=s("hřeben pila hrábě vidlička klíč zip"),
         outside=s("lžíce deka míč provaz houba mýdlo ručník polštář"
                   " sklenice svíčka koberec kniha")),
    dict(id="v10-noha", level="normal",
         roof="věci, které mají nohu",
         ask="mají nohu, i když nechodí",
         inside=s("stůl židle postel houba klavír sklenka kružítko pohár"),
         outside=s("koberec deka kniha zrcadlo obraz hrnec koště mýdlo"
                   " ručník provaz")),
    dict(id="v10-jazyk", level="hard",
         roof="věci, které mají jazyk",
         ask="mají jazyk, i když nemluví",
         inside=s("bota zvon plamen ledovec hoblík váha"),
         outside=s("čepice deka hrnec sešit lampa koberec klíč mýdlo"
                   " provaz kniha")),
    dict(id="v10-oko", level="hard",
         roof="věci, které mají oko",
         ask="mají oko, i když nevidí",
         inside=s("síť polévka brambora řetěz bouře punčocha"),
         outside=s("cihla deka kniha lampa hrnec sešit mýdlo koště"
                   " ručník židle")),
    dict(id="v10-hlava", level="normal",
         roof="věci, které mají hlavu",
         ask="mají hlavu, i když nemají tělo",
         inside=s("hřebík špendlík zelí česnek kladivo šroub"),
         outside=s("deka kniha lampa koberec hrnec ručník mýdlo sešit"
                   " provaz sklenice")),
    dict(id="v10-kridla", level="hard",
         roof="věci, které mají křídlo",
         ask="mají křídlo, i když nelétají",
         inside=s("dveře okno nos oltář vojsko budova"),
         outside=s("stůl kniha hrnec deka lampa koberec mýdlo sešit"
                   " provaz kbelík")),

    # ========================================== ustálená spojení (6) =======
    dict(id="v10-tezky", level="normal",
         roof="slova, která tvoří spojení se slovem těžký",
         ask="tvoří se slovem těžký ustálené spojení",
         inside=s("váha kalibr srdce průmysl kov atletika"),
         outside=s("sešit koště ubrus rohožka propiska záclona houpačka"
                   " tácek ramínko ubrousek")),
    dict(id="v10-horky", level="normal",
         roof="slova, která tvoří spojení se slovem horký",
         ask="tvoří se slovem horký ustálené spojení",
         inside=s("linka brambor hlava kandidát novinka půda čokoláda"),
         outside=s("sešit koště ubrus rohožka propiska záclona houpačka"
                   " tácek ramínko ubrousek")),
    dict(id="v10-slepy", level="normal",
         roof="slova, která tvoří spojení se slovem slepý",
         ask="tvoří se slovem slepý ustálené spojení",
         inside=s("ulička mapa střevo kolej pasažér rameno skvrna bába"),
         outside=s("sešit koště ubrus rohožka propiska záclona houpačka"
                   " tácek ramínko ubrousek")),
    dict(id="v10-mrtvy", level="hard",
         roof="slova, která tvoří spojení se slovem mrtvý",
         ask="tvoří se slovem mrtvý ustálené spojení",
         inside=s("bod moře úhel sezona jazyk brouk"),
         outside=s("sešit koště ubrus rohožka propiska záclona houpačka"
                   " tácek ramínko ubrousek")),
    dict(id="v10-sedy", level="hard",
         roof="slova, která tvoří spojení se slovem šedý",
         ask="tvoří se slovem šedý ustálené spojení",
         inside=s("zóna eminence kůra zákal ekonomika myš"),
         outside=s("sešit koště ubrus rohožka propiska záclona houpačka"
                   " tácek ramínko ubrousek")),
    dict(id="v10-tvrdy", level="normal",
         roof="slova, která tvoří spojení se slovem tvrdý",
         ask="tvoří se slovem tvrdý ustálené spojení",
         inside=s("oříšek disk měna voda chleba spoluhláska alkohol"),
         outside=s("sešit koště ubrus rohožka propiska záclona houpačka"
                   " tácek ramínko ubrousek")),

    # ============================================ řemesla a obory (21) =====
    dict(id="v10-kovarna", skupina="obor", level="hard",
         roof="kovářské pojmy",
         ask="jsou to zároveň kovářské pojmy",
         inside=s("výheň kovadlina měch podkova kalení okuje výkovek"),
         avoid=s("kleště kladívko hřebík pilník svěrák šroub matice")),
    dict(id="v10-hasici", skupina="obor", level="hard",
         roof="hasičské pojmy",
         ask="jsou to zároveň hasičské pojmy",
         inside=s("proudnice savice hydrant stříkačka rozdělovač zásah útok"),
         avoid=s("hadice žebřík kbelík kýbl")),
    dict(id="v10-truhlarna", skupina="obor", level="hard",
         roof="truhlářské pojmy",
         ask="jsou to zároveň truhlářské pojmy",
         inside=s("dláto dýha rašple čep hobliny fládr"),
         avoid=s("hoblík svěrák kleště pilník vrtačka kladívko šuplík"
                 " komoda skříň")),
    dict(id="v10-astronomie", skupina="obor", level="hard",
         roof="astronomické pojmy",
         ask="jsou to zároveň astronomické pojmy",
         inside=s("mlhovina zákryt opozice fáze dráha hvězdokupa úplněk")),
    dict(id="v10-geologie", skupina="obor", level="hard",
         roof="geologické pojmy",
         ask="jsou to zároveň geologické pojmy",
         inside=s("vrstva zlom žíla kra výchoz souvrství nános")),
    dict(id="v10-zemedelstvi", skupina="obor", level="normal",
         roof="zemědělské pojmy",
         ask="jsou to zároveň zemědělské pojmy",
         inside=s("brázda úhor osivo strniště mez orba hnojivo"),
         avoid=s("motyka rýč hrábě trakař kompost semínko zahrada")),
    dict(id="v10-serm", skupina="obor", level="hard",
         roof="šermířské pojmy",
         ask="jsou to zároveň šermířské pojmy",
         inside=s("výpad kryt sek čepel garda kord")),
    dict(id="v10-kvet", skupina="casti", level="hard",
         roof="části květu",
         ask="jsou to zároveň části květu",
         inside=s("kalich koruna tyčinka blizna čnělka pestík semeník stopka")),
    dict(id="v10-zub", skupina="casti", level="hard",
         roof="části zubu",
         ask="jsou to zároveň části zubu",
         inside=s("korunka krček kořen sklovina dřeň cement")),
    dict(id="v10-houba-casti", skupina="casti", level="normal",
         roof="části houby",
         ask="jsou to zároveň části houby",
         inside=s("klobouk třeň plodnice podhoubí výtrusy lupeny")),
    dict(id="v10-kytara", skupina="casti", level="normal",
         roof="části kytary",
         ask="jsou to zároveň části kytary",
         inside=s("krk kobylka pražec struna hlavice sedlo"),
         avoid=s("kolík")),
    dict(id="v10-kamna", skupina="casti", level="normal",
         roof="části kamen",
         ask="jsou to zároveň části kamen",
         inside=s("rošt popelník dvířka komín tah plotna")),
    dict(id="v10-most", skupina="casti", level="hard",
         roof="části mostu",
         ask="jsou to zároveň části mostu",
         inside=s("pilíř oblouk pole opěra mostovka zábradlí")),
    dict(id="v10-kniha-casti", skupina="casti", level="normal",
         roof="části knihy",
         ask="jsou to zároveň části knihy",
         inside=s("hřbet desky vazba obálka kapitola rejstřík předsádka"),
         avoid=s("sešit zápisník pouzdro")),
    dict(id="v10-pojisteni", skupina="sluzby", level="hard",
         roof="pojišťovací pojmy",
         ask="jsou to zároveň pojišťovací pojmy",
         inside=s("pojistka škoda plnění riziko spoluúčast smlouva")),
    dict(id="v10-ucetnictvi", skupina="sluzby", level="hard",
         roof="účetní pojmy",
         ask="jsou to zároveň účetní pojmy",
         inside=s("rozvaha saldo obrat závazek zisk položka")),
    dict(id="v10-lukostrelba", skupina="obor", level="normal",
         roof="lukostřelecké pojmy",
         ask="jsou to zároveň lukostřelecké pojmy",
         inside=s("tětiva terč hrot opeření toulec nátah"),
         avoid=s("kolík provaz")),
    dict(id="v10-filatelie", skupina="sluzby", level="hard",
         roof="filatelistické pojmy",
         ask="jsou to zároveň filatelistické pojmy",
         inside=s("známka zoubkování přetisk arch aršík obtisk"),
         avoid=s("schránka")),
    dict(id="v10-elektro", skupina="obor", level="hard",
         roof="elektrotechnické pojmy",
         ask="jsou to zároveň elektrotechnické pojmy",
         inside=s("vodič jistič zkrat uzemnění svorka cívka"),
         avoid=s("lampa vysavač pračka myčka lednička žehlička sporák")),
    dict(id="v10-mlekarna", skupina="obor", level="hard",
         roof="mlékárenské pojmy",
         ask="jsou to zároveň mlékárenské pojmy",
         inside=s("syřidlo sýřenina podmáslí syrovátka zrání smetana")),
    dict(id="v10-hornictvi", skupina="obor", level="hard",
         roof="hornické pojmy",
         ask="jsou to zároveň hornické pojmy",
         inside=s("šachta sloj štola výdřeva klec překop"),
         avoid=s("lopata kbelík")),

    # =========================================== Česko na mapě (2) =========
    dict(id="v10-lazne", level="hard",
         roof="české lázně",
         ask="jsou to zároveň české lázně",
         inside=s("Teplice Poděbrady Jeseník Luhačovice Bechyně Darkov"
                  " Bohdaneč Libverda"),
         outside=s("Kolín Náchod Vsetín Rakovník Přerov Chrudim Beroun Blansko Havířov Písek"),
         avoid_asks=["jsou to zároveň jména českých měst"]),
    dict(id="v10-chko", level="hard",
         roof="chráněné krajinné oblasti",
         ask="jsou to zároveň chráněné krajinné oblasti",
         inside=s("Pálava Blaník Beskydy Kokořínsko Broumovsko Poodří"
                  " Křivoklátsko Žďársko"),
         outside=s("Krkonoše Podyjí Vysočina Polabí Haná Slovácko Valašsko Chodsko Posázaví Podkrkonoší"),
         avoid_asks=["jsou to zároveň jména českých měst"]),

    # ============================================ písmena a mluvnice (5) ===
    dict(id="v10-slabikotvorne", level="hard", rule="slabikotvorne",
         roof="slova, ve kterých drží slabiku r nebo l",
         ask="mají v sobě r nebo l, které drží celou slabiku",
         inside=s("vrba slza srdce mlha brzda hrdlo krtek vlna prkno vrták"),
         outside=s("lampa kolo ruka sova malina police koleno motyka"
                   " silnice konev")),
    dict(id="v10-tel", level="normal", rule="koncovka-tel",
         roof="slova končící na -tel",
         ask="končí na písmena tel",
         inside=s("učitel ředitel spisovatel přítel kotel hotel majitel"
                  " nositel"),
         outside=s("lampa koleno police sešit ubrus kbelík motyka konev"
                   " kolík ručník")),
    dict(id="v10-hacky", level="normal", rule="hacky",
         roof="slova s ď, ť nebo ň",
         ask="mají v sobě ď, ť nebo ň",
         inside=s("kůň oheň loď zeď píseň dlaň síť poušť labuť"),
         outside=s("stůl lampa kniha koberec hrnec police sešit mýdlo"
                   " provaz ručník")),
    dict(id="v10-krouzek", level="normal", rule="krouzek",
         roof="slova s kroužkovaným ů",
         ask="mají v sobě ů s kroužkem",
         inside=s("stůl dům sůl vůz hůl kůže půda růže můra"),
         outside=s("police lampa koberec sešit hrnec konev motyka ručník"
                   " kolík kbelík")),
    dict(id="v10-bez-prvniho", level="hard", rule="bez-prvniho",
         roof="slova, ze kterých po useknutí prvního písmene zbude jiné slovo",
         ask="po useknutí prvního písmene dají jiné slovo",
         inside=s("mrak krok sled klín brod vlak kroj kluk klid kosa"
                  " chlad krám"),
         outside=s("lampa police koberec sešit motyka konev ručník hrnec"
                   " kbelík žebřík")),

    # ======================================= příroda podle chování (5) =====
    dict(id="v10-kvete-drive", level="hard",
         roof="dřeviny, které kvetou dřív, než jim narostou listy",
         ask="kvetou dřív, než na nich narostou listy",
         inside=s("líska olše vrba dřín trnka topol jilm"),
         outside=s("lípa dub buk jeřáb akát bez kaštan hloh pámelník zimolez")),
    dict(id="v10-tazni", level="normal",
         roof="tažní ptáci",
         ask="odlétají na zimu do teplých krajů",
         inside=s("vlaštovka čáp špaček jiřička rorýs konipas kukačka slavík"),
         outside=s("vrabec sýkora straka havran sova datel brhlík holub"
                   " koroptev bažant")),
    dict(id="v10-zimni-spanek", level="normal",
         roof="zvířata, která spí zimní spánek",
         ask="spí opravdový zimní spánek",
         inside=s("ježek plch sysel svišť netopýr křeček"),
         outside=s("liška srna zajíc veverka kuna jelen vlk rys")),
    # Souš na obou stranách. S rakem uvnitř a rybou vně se pětice dala
    # přečíst jako „čtyři žijí na souši, ryba ve vodě" — jiná osa, tentýž
    # vetřelec, a o svlékání kůže se hráč nemusel dozvědět nic. Vně stojí
    # vedle savců i bezobratlí, kteří kůži nesvlékají (žížala, slimák),
    # aby se pětice nedala rozseknout ani na „obratlovce a ty ostatní".
    dict(id="v10-svleka", level="hard",
         roof="živočichové, kteří svlékají kůži",
         ask="svlékají kůži",
         inside=s("had ještěrka pavouk štír cikáda stonožka kobylka"),
         outside=s("žížala slimák myš kočka netopýr ježek krtek veverka"
                   " jelen srna")),
    dict(id="v10-parazit", level="hard",
         roof="organismy, které žijí na cizí úkor",
         ask="žijí na úkor jiného živého tvora",
         inside=s("klíště blecha veš jmelí tasemnice kukačka"),
         outside=s("včela mravenec motýl žížala slimák brouk pavouk dub"
                   " kopřiva mech")),

    # ============================================== prameny názvů (9) ======
    dict(id="v10-may", skupina="nazvy", level="hard",
         roof="slova z názvů knih Karla Maye",
         ask="jsou v názvech knih Karla Maye",
         inside=s("poklad jezero syn duch mustang princ lev odkaz")),
    dict(id="v10-havel", skupina="nazvy", level="hard",
         roof="slova z názvů her Václava Havla",
         ask="jsou v názvech her Václava Havla",
         inside=s("slavnost audience vernisáž vyrozumění odcházení pokoušení"
                  " spiklenci opera")),
    dict(id="v10-kundera", skupina="nazvy", level="hard",
         roof="slova z názvů knih Milana Kundery",
         ask="jsou v názvech knih Milana Kundery",
         inside=s("žert nesmrtelnost lehkost valčík nevědomost totožnost"
                  " smích pomalost")),
    dict(id="v10-zeman", skupina="nazvy", level="hard",
         roof="slova z názvů filmů Karla Zemana",
         ask="jsou v názvech filmů Karla Zemana",
         inside=s("cesta pravěk vynález zkáza baron vzducholoď kronika")),
    dict(id="v10-chaplin", skupina="nazvy", level="hard",
         roof="slova z názvů Chaplinových filmů",
         ask="jsou v názvech Chaplinových filmů",
         inside=s("světla velkoměsto doba opojení cirkus diktátor král"
                  " rampa")),
    dict(id="v10-dickens", skupina="nazvy", level="hard",
         roof="slova z názvů knih Charlese Dickense",
         ask="jsou v názvech knih Charlese Dickense",
         inside=s("koleda dům vyhlídky příběh časy kronika klub")),
    dict(id="v10-mucha", skupina="nazvy", level="hard",
         roof="slova z názvů obrazů Alfonse Muchy",
         ask="jsou v názvech obrazů Alfonse Muchy",
         inside=s("jaro zima poezie tanec hvězda epopej")),
    dict(id="v10-menzel", skupina="nazvy", level="hard",
         roof="slova z názvů filmů Jiřího Menzela",
         ask="jsou v názvech filmů Jiřího Menzela",
         inside=s("skřivánci nit postřižiny slavnosti sněženky vesnička"
                  " konec")),
    dict(id="v10-storch", skupina="nazvy", level="hard",
         roof="slova z názvů knih Eduarda Štorcha",
         ask="jsou v názvech knih Eduarda Štorcha",
         inside=s("lovci mamut osada havran bronz volání rod")),

    # ================================================ obory podruhé (10) ===
    dict(id="v10-box", skupina="sluzby", level="normal",
         roof="boxerské pojmy",
         ask="jsou to zároveň boxerské pojmy",
         inside=s("hák roh gong kolo provazy rukavice"),
         avoid=s("hřebík")),
    dict(id="v10-tenis", skupina="sluzby", level="normal",
         roof="tenisové pojmy",
         ask="jsou to zároveň tenisové pojmy",
         inside=s("podání síť dvorec výhoda shoda čára")),
    dict(id="v10-skaut", skupina="sluzby", level="normal",
         roof="skautské pojmy",
         ask="jsou to zároveň skautské pojmy",
         inside=s("stezka slib družina oddíl uzel totem")),
    dict(id="v10-policie", skupina="sluzby", level="normal",
         roof="policejní pojmy",
         ask="jsou to zároveň policejní pojmy",
         inside=s("hlídka výslech stopa obušek cela pouta")),
    dict(id="v10-heraldika", skupina="obor", level="hard",
         roof="heraldické pojmy",
         ask="jsou to zároveň heraldické pojmy",
         inside=s("štít klenot přilba pole znak helma")),
    dict(id="v10-burza", skupina="sluzby", level="hard",
         roof="burzovní pojmy",
         ask="jsou to zároveň burzovní pojmy",
         inside=s("kurz medvěd býk propad akcie dividenda")),
    dict(id="v10-letiste", skupina="sluzby", level="normal",
         roof="letištní pojmy",
         ask="jsou to zároveň letištní pojmy",
         inside=s("brána pás věž odbavení plocha rukáv")),
    dict(id="v10-hotel", skupina="sluzby", level="normal",
         roof="hotelové pojmy",
         ask="jsou to zároveň hotelové pojmy",
         inside=s("recepce pokoj apartmá snídaně hvězdička lůžko"),
         avoid=s("postel matrace peřina polštář deka")),
    dict(id="v10-restaurace", skupina="sluzby", level="normal",
         roof="restaurační pojmy",
         ask="jsou to zároveň restaurační pojmy",
         inside=s("objednávka účet lístek chod obsluha spropitné")),
    dict(id="v10-autoskola", skupina="sluzby", level="normal",
         roof="pojmy z autoškoly",
         ask="jsou to zároveň pojmy z autoškoly",
         inside=s("křižovatka přednost značka zkouška jízda testy")),

    # ================================================= části věcí (6) ======
    dict(id="v10-schodiste", skupina="casti", level="normal",
         roof="části schodiště",
         ask="jsou to zároveň části schodiště",
         inside=s("stupeň madlo podesta sloupek rameno nášlap"),
         avoid=s("žebřík lavička")),
    dict(id="v10-kosile", skupina="casti", level="normal",
         roof="části košile",
         ask="jsou to zároveň části košile",
         inside=s("límec manžeta náprsenka knoflík rukáv sedlo"),
         avoid=s("bunda kabát šála ponožka ramínko")),
    dict(id="v10-vodovod", skupina="casti", level="hard",
         roof="části vodovodu",
         ask="jsou to zároveň části vodovodu",
         inside=s("kohout koleno přípojka sifon ventil těsnění"),
         avoid=s("hadice konev dřez vana kbelík kýbl")),
    dict(id="v10-strecha", skupina="casti", level="normal",
         roof="části střechy",
         ask="jsou to zároveň části střechy",
         inside=s("hřeben taška krov okap úžlabí štít"),
         avoid=s("žebřík hřeben")),
    dict(id="v10-vuz", skupina="casti", level="hard",
         roof="části koňského vozu",
         ask="jsou to zároveň části koňského vozu",
         inside=s("oj náprava loukoť korba ráf zápřah"),
         avoid=s("trakař")),
    dict(id="v10-zamek", skupina="casti", level="normal",
         roof="části dveřního zámku",
         ask="jsou to zároveň části dveřního zámku",
         inside=s("klika vložka závora jazýček zástrč štítek"),
         avoid=s("věšák schránka")),

    # ================================================ slova a původ (5) ====
    dict(id="v10-francouzstina", level="hard",
         roof="slova přejatá z francouzštiny",
         ask="jsou to slova přejatá z francouzštiny",
         inside=s("bujón garáž kostým žánr plakát bulvár parfém šampaňské")),
    dict(id="v10-arabstina", level="hard",
         roof="slova přejatá z arabštiny",
         ask="jsou to slova přejatá z arabštiny",
         inside=s("alkohol algebra cukr káva magazín admirál žirafa šafrán")),
    dict(id="v10-italstina", level="hard",
         roof="slova přejatá z italštiny",
         ask="jsou to slova přejatá z italštiny",
         inside=s("banka konto opera piano salám karneval sonáta balkon")),
    dict(id="v10-slozeniny", level="normal",
         roof="složená slova",
         ask="jsou složená ze dvou slov",
         inside=s("zeměkoule vodopád letopočet velkoměsto dřevorubec kolotoč"
                  " hromosvod samoobsluha")),
    dict(id="v10-podle-cloveka", level="hard",
         roof="slova, která vznikla z jména člověka",
         ask="vznikla ze jména konkrétního člověka",
         inside=s("bojkot sendvič silueta saxofon gilotina mecenáš lynč")),

    # ============================================= vlastnosti a děje (16) ==
    dict(id="v10-zaroste", level="normal",
         roof="věci, ze kterých vyroste rostlina",
         ask="vyklíčí, když se zasadí",
         inside=s("semínko hlíza cibule žalud pecka oddenek výhonek kaštan"),
         outside=s("kamínek cihla korálek knoflík mince hřebík sponka korek"
                   " střep kolík")),
    dict(id="v10-zip", level="normal",
         roof="věci, které se zapínají na zip",
         ask="se zapínají na zip",
         inside=s("bunda batoh stan spacák penál kalhoty pouzdro sukně"),
         outside=s("ponožka šála rukavice klobouk deka ručník kapesník"
                   " opasek čepice tílko")),
    dict(id="v10-zada", level="normal",
         roof="věci, které se nosí na zádech",
         ask="se nosí na zádech",
         inside=s("batoh krosna tlumok ranec vak nůše"),
         outside=s("taška kabelka kufr koš pytel kbelík bedna aktovka"
                   " mošna truhla")),
    dict(id="v10-lekarna", level="normal",
         roof="věci, které se koupí v lékárně",
         ask="se prodávají v lékárně",
         inside=s("obvaz náplast jód aspirin teploměr vata sirup kapky"),
         outside=s("kladivo hřebík provaz koště sešit propiska lampa kbelík"
                   " hrábě motyka")),
    dict(id="v10-ztvrdne", level="hard",
         roof="látky, které po zaschnutí ztvrdnou",
         ask="po zaschnutí ztvrdnou",
         inside=s("beton sádra lepidlo malta lak tmel hlína cement"),
         outside=s("voda olej mléko ocet líh benzín čaj sirup med glycerin")),
    dict(id="v10-voni", level="normal",
         roof="věci, které voní i po uschnutí",
         ask="voní i po uschnutí",
         inside=s("levandule seno skořice vanilka tabák chmel kadidlo máta"),
         outside=s("cihla sklo hřebík provaz kámen papír drát plech korek"
                   " struska")),
    dict(id="v10-jedovate", level="hard",
         roof="jedovaté věci",
         ask="jsou jedovaté",
         inside=s("muchomůrka rulík tis konvalinka rtuť arsen olovo kurare"),
         outside=s("heřmánek máta lípa šípek jahoda borůvka křemen žula"
                   " měď cín")),
    dict(id="v10-zvetsuje", level="normal",
         roof="věci, které zvětšují obraz",
         ask="zvětšují obraz",
         inside=s("lupa mikroskop dalekohled brýle projektor čočka"),
         outside=s("zrcadlo okno sklenice hodinky lampa baterka kompas"
                   " budík váhy teploměr")),
    dict(id="v10-cisla", level="normal",
         roof="věci, na kterých jsou čísla",
         ask="mají na sobě čísla",
         inside=s("hodiny teploměr kalendář pravítko telefon dres váha"),
         outside=s("koště deka ručník polštář koberec ubrus mýdlo houba"
                   " provaz kbelík")),
    dict(id="v10-destnik", level="normal",
         roof="věci, které chrání před deštěm",
         ask="chrání před deštěm",
         inside=s("deštník pláštěnka střecha markýza přístřešek klobouk"),
         outside=s("brýle rukavice ponožka opasek kravata náramek hodinky"
                   " prsten batoh tužka")),
    dict(id="v10-pecka", level="normal",
         roof="ovoce s jednou velkou peckou",
         ask="mají uvnitř jednu velkou pecku",
         inside=s("broskev švestka třešeň meruňka avokádo mango oliva datle"),
         outside=s("jablko hruška pomeranč meloun jahoda rybíz banán kiwi"
                   " angrešt malina")),
    dict(id="v10-odpuzuje", level="hard",
         roof="látky, které odpuzují vodu",
         ask="odpuzují vodu",
         inside=s("vosk olej teflon peří guma silikon lak"),
         outside=s("papír houba vata plátno hlína cukr sůl mouka dřevo"
                   " vlna")),
    dict(id="v10-saje", level="normal",
         roof="věci, které nasáknou vodu",
         ask="nasáknou vodu",
         inside=s("houba vata papír hlína ručník plátno mech korek"),
         outside=s("sklo kov plast vosk guma olej mince klíč kámen drát")),
    dict(id="v10-hasi", level="normal",
         roof="věci, kterými se hasí oheň",
         ask="hasí oheň",
         inside=s("voda písek pěna deka hlína sníh"),
         outside=s("benzín líh olej papír sláma dřevo uhlí seno vosk tuk")),
    dict(id="v10-vitr", level="normal",
         roof="věci, které uletí ve větru",
         ask="uletí ve větru",
         inside=s("list papír pírko prach pyl semínko"),
         outside=s("cihla kámen mince kladivo sklenice hrnec klíč kbelík"
                   " sekera kovadlina")),
    dict(id="v10-odrazene-svetlo", level="hard",
         roof="věci, které svítí jen odraženým světlem",
         ask="svítí jen odraženým světlem",
         inside=s("měsíc planeta zrcadlo sníh hladina kometa"),
         outside=s("slunce hvězda oheň žárovka blesk svíčka světluška"
                   " laser pochodeň jiskra")),

    # ================================================ poslední hrst (8) ====
    dict(id="v10-nadrze", level="hard",
         roof="české přehradní nádrže",
         ask="jsou to zároveň české přehrady",
         inside=s("Orlík Lipno Slapy Nechranice Dalešice Rozkoš Švihov"
                  " Hracholusky"),
         outside=s("Rožmberk Bezdrev Svět Horusický Dvořiště Staňkovský Dářko Nesyt"),
         avoid_asks=["jsou to zároveň jména českých měst"]),
    dict(id="v10-ctvrti", level="normal",
         roof="pražské čtvrti",
         ask="jsou to zároveň pražské čtvrti",
         inside=s("Dejvice Vinohrady Žižkov Karlín Smíchov Braník Vršovice"
                  " Podolí"),
         outside=s("Bohunice Židenice Líšeň Komín Slatina Poruba Zábřeh Hrabůvka Přívoz Vítkovice"),
         avoid_asks=["jsou to zároveň jména českých měst",
                     "jsou to zároveň značky českého piva"]),
    dict(id="v10-par", level="normal",
         roof="věci, které se prodávají v páru",
         ask="se prodávají vždycky po dvou",
         inside=s("boty ponožky rukavice brusle lyže náušnice"),
         outside=s("čepice šála opasek kabát sukně klobouk batoh deštník"
                   " prsten hodinky")),
    dict(id="v10-origami", level="normal",
         roof="věci, které se dají složit z papíru",
         ask="se dají složit z papíru",
         inside=s("vlaštovka loďka čepice harmonika žabka jeřáb"),
         outside=s("kladivo hrnec židle klíč mýdlo lampa provaz kbelík"
                   " cihla sklenice")),
    dict(id="v10-les-sber", level="normal",
         roof="věci, které se sbírají v lese",
         ask="se sbírají v lese",
         inside=s("houby borůvky maliny klestí mech šišky brusinky žaludy"),
         outside=s("mrkev brambora cibule řepa salát okurka ředkvička"
                   " rajče hrách dýně")),
    dict(id="v10-trafika", level="normal",
         roof="věci, které se koupí v trafice",
         ask="se prodávají v trafice",
         inside=s("noviny časopis známka jízdenka los zapalovač žvýkačka"
                  " pohlednice"),
         outside=s("kladivo hrnec deka koště motyka žebřík pračka matrace"
                   " konev hrábě")),
    dict(id="v10-uzel", level="normal",
         roof="věci, které se dají uvázat na uzel",
         ask="se dají uvázat na uzel",
         inside=s("provaz tkanička kravata šátek hadice lano nit"),
         outside=s("drát tyč prkno řetěz klacek trubka hřebík sklo cihla"
                   " plech")),
    dict(id="v10-vede-teplo", level="hard",
         roof="látky, které dobře vedou teplo",
         ask="dobře vedou teplo",
         inside=s("měď hliník železo stříbro ocel mosaz"),
         outside=s("dřevo korek vlna molitan plast papír guma pěna textil"
                   " sláma")),
]


def priklonka(ask: str) -> None:
    """Zvratné „se" patří na druhé místo věty, ne za sloveso.

    Rámec zní „Čtyři z nich …", takže sloveso je ve větě až třetí a příklonka
    se před ně musí přesunout: „Čtyři z nich **se** sbírají v lese", ne
    „Čtyři z nich sbírají se v lese". Sdílená kontrola tohle nechytí, protože
    hlídá jen podobu otázky samotné, a ta zní správně obojím způsobem.

    Výjimka je „tvoří **se slovem** ostrý ustálené spojení" — tam „se" není
    příklonka, ale předložka, a přesunout se nesmí.
    """
    kusy = ask.split()
    if len(kusy) > 2 and kusy[1] == "se" and kusy[2] != "slovem":
        raise SystemExit(f"příklonka patří dopředu: {ask!r}")
    # „Čtyři z nich vyroste z nich rostlina" — podmět už ve větě stojí,
    # takže druhý odkaz na něj je navíc.
    if "z nich" in ask:
        raise SystemExit(f"otázka opakuje podmět: {ask!r}")


def main() -> int:
    rodiny = []
    for spec in RODINY:
        rng = random.Random(spec["id"])
        zkontroluj_vetu(spec["ask"])
        priklonka(spec["ask"])

        inside = list(spec["inside"])
        if len(set(inside)) != len(inside):
            raise SystemExit(f"{spec['id']}: slovo uvnitř dvakrát")

        # Řemesla a části věcí si vetřelce berou od sousedů, ne z nudné
        # zásoby domácích potřeb — jinak trčí už tím, jak vypadá.
        zasoba = spec.get("outside")
        if zasoba is None and spec.get("skupina"):
            zasoba = sousedni(spec, RODINY, rng)
        volna = [w for w in (zasoba if zasoba is not None else VATA.split())
                 if w not in inside and w not in spec.get("avoid", [])]
        # Z nudné zásoby se bere vzorek, ne celá: sto vetřelců na rodinu se
        # při ruční kontrole nedá přečíst, a přečíst se musí — stroj nepozná,
        # že *lopatka* je taky kost.
        outside = (sorted(random.Random(spec["id"]).sample(volna, 15))
                   if zasoba is None and len(volna) > 15 else volna)

        # Pravidlo o písmenech platí pro obě strany naráz. Tohle je jediné
        # místo, kde se dá rodina rozejít sama se sebou, a proto se tvrdě
        # hlásí — radši spadlý build než hádanka bez řešení.
        rule = spec.get("rule")
        if rule:
            splnuje = PRAVIDLA[rule]
            for w in inside:
                if not splnuje(w):
                    raise SystemExit(f"{spec['id']}: {w!r} pravidlu nevyhovuje")
            for w in outside:
                if splnuje(w):
                    raise SystemExit(f"{spec['id']}: vetřelec {w!r} pravidlu vyhovuje")

        if len(inside) < 6:
            raise SystemExit(f"{spec['id']}: jen {len(inside)} slov uvnitř")
        if len(outside) < 8:
            raise SystemExit(f"{spec['id']}: jen {len(outside)} slov vně")
        spolecna = set(inside) & set(outside)
        if spolecna:
            raise SystemExit(f"{spec['id']}: {sorted(spolecna)} stojí uvnitř i vně")

        rodiny.append({
            "id": spec["id"],
            "roof": spec["roof"],
            "level": spec["level"],
            "hidden": True,
            "inside": inside,
            "outside": outside,
            "asks": [spec["ask"]] + decoys(spec, inside + outside, rng),
        })

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
    print(f"-> {os.path.normpath(OUT)}")
    return 0


HLAVICKA = '''"""Desátá várka rodin — sto skrytých střech.

TENHLE SOUBOR PÍŠE SKRIPT. Ruční úpravy zmizí při dalším spuštění; opravovat
se má `tools/gen_families10.py`, kde stojí zadání i kontroly.

Rodiny s pravidlem o písmenech (slabikotvorné r, koncovka -tel, háčky,
kroužek, useknuté první písmeno) prošly strojem: každé slovo uvnitř pravidlu
vyhovuje a žádné slovo vně mu nevyhovuje. U ostatních rodin stojí slova vně
schválně ze stejného soudku jako slova uvnitř, aby osa nesklouzla na
„čtyři jsou ptáci".
"""

FAMILIES10 = ['''


if __name__ == "__main__":
    raise SystemExit(main())
