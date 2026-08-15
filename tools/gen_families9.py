"""Devátá várka rodin — sto os, a pokaždé jiné povahy.

Osmá várka ukázala, že na Vetřelci není cenné množství pětic, ale **kolik
různých věcí musí hráč zkusit**, než souvislost najde. Tahle várka na tom
staví dál a přidává sto rodin rozdělených do skupin, které se navzájem
nepodobají:

* **vlastnosti věcí a přírody** — co ta věc dělá, ne co to slovo znamená,
* **kalendář a zeměpis** — co v Česku platí a co je jen tak nastavené,
* **mluvnice a pravopis** — nepravidelné množné číslo, přesmyčky, rýmy,
* **ustálená spojení** — bílá vrána, suchý humor, hluboký talíř,
* **obory s vlastní řečí** — film, právo, tělocvik, pivovar, jeskyně,
* **další prameny názvů** — Malý princ, Alenka, Poe, pražské pověsti.

Slova vně jsou u rodin o **vlastnostech** psaná ručně: vetřelec musí být
věc, u které je vlastnost jistě opačná. U rodin o **oborech** stačí nudná
zásoba ze sedmé várky — hrnec ani koště nejsou pojem z práva ani z fyziky.
Kde by se nudné slovo přece jen trefilo (*lopatka* je kost, *matice* je
matematický pojem, *hřeben* je část hory), stojí v seznamu `avoid`.

Spuštění:  python3 tools/gen_families9.py
Výstup:    tools/intruder_families9.py
"""

import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from gen_families7 import VATA, decoys, zapis, zkontroluj_vetu  # noqa: E402
from gen_families10 import sousedni  # noqa: E402

OUT = os.path.join(HERE, "intruder_families9.py")


def s(text: str) -> list[str]:
    return text.split()


RODINY: list[dict] = [
    # ============================================ vlastnosti věcí a přírody ==
    dict(id="v9-bile", level="normal",
         roof="věci, které jsou vždycky bílé",
         ask="jsou vždycky bílé",
         inside=s("sníh mléko křída sůl mouka vata porcelán tvaroh"),
         outside=s("uhlí saze asfalt dehet čokoláda káva hlína rez inkoust rašelina")),
    dict(id="v9-kysele", level="normal",
         roof="jídlo, které je kyselé",
         ask="jsou kyselé",
         inside=s("citron ocet kefír zelí rebarbora jogurt šťovík brusinka"),
         outside=s("med cukr mléko chleba máslo banán mrkev olej rýže sádlo")),
    dict(id="v9-tekute", level="hard",
         roof="látky, které jsou při pokojové teplotě tekuté",
         # Rtuť je past naopak: kov, a přesto teče. Vosk a sádlo jsou past
         # opačná — vypadají měkce, ale tuhá jsou.
         ask="jsou při pokojové teplotě tekuté",
         inside=s("voda olej mléko líh rtuť ocet nafta glycerin"),
         outside=s("máslo vosk čokoláda sádlo parafín sklo margarín cukr sůl vazelína")),
    dict(id="v9-teplo", level="hard",
         roof="věci, které samy vydávají teplo",
         # Deka a svetr jsou past: hřejí, ale žádné teplo nevyrábějí.
         ask="samy vydávají teplo",
         inside=s("oheň kamna žehlička slunce svíčka radiátor motor pochodeň"),
         outside=s("deka svetr peřina termoska šála bunda spacák rukavice čepice ručník")),
    dict(id="v9-kvasi", level="normal",
         roof="věci, které kvasí",
         ask="kvasí",
         inside=s("pivo víno chleba zelí jogurt kvásek mošt kefír"),
         outside=s("mouka sůl olej voda čaj cukr rýže brambora ocet mýdlo")),
    dict(id="v9-kulate", level="normal",
         roof="věci, které jsou vždycky kulaté",
         ask="jsou vždycky kulaté",
         inside=s("míč koule mince talíř kolo planeta bublina obruč"),
         outside=s("cihla kniha stůl dveře krabice žebřík plot deka sešit prkno")),
    dict(id="v9-dira", level="normal",
         roof="věci, které mají díru uprostřed",
         ask="mají díru uprostřed",
         inside=s("prsten matice kroužek koblih pneumatika obruč podložka disk"),
         outside=s("talíř mince cihla kniha deka míč sklenice klíč prkno mýdlo")),
    dict(id="v9-ostre", level="normal",
         roof="věci, které jsou ostré",
         ask="jsou ostré",
         inside=s("nůž jehla sekera břitva hřebík střep dláto šipka"),
         outside=s("lžíce houba deka míč guma provaz polštář ručník kbelík mýdlo")),
    dict(id="v9-voda-potreba", level="normal",
         roof="věci, které bez vody nefungují",
         ask="bez vody nefungují",
         inside=s("pračka myčka sprcha akvárium fontána kotel mlýn vodárna"),
         outside=s("vysavač rádio lampa sekačka hodiny baterka větrák budík zvonek fén")),
    dict(id="v9-nabobtna", level="normal",
         roof="jídlo, které při vaření zvětší objem",
         ask="při vaření zvětší objem",
         inside=s("rýže těstoviny fazole kroupy čočka kuskus hrách bulgur"),
         outside=s("maso brambora mrkev cibule vejce houby cuketa řepa dýně pórek")),
    dict(id="v9-zkazi", level="hard",
         roof="jídlo, které se zkazí",
         # Med, sůl a cukr vydrží prakticky navěky — na tom se rodina láme.
         ask="se zkazí i v lednici",
         inside=s("mléko maso chleba jogurt ryba salát smetana vejce"),
         outside=s("med sůl cukr rýže ocet líh mouka luštěniny čaj koření")),
    dict(id="v9-stoupa", level="normal",
         roof="věci, které samy stoupají vzhůru",
         ask="samy stoupají vzhůru",
         inside=s("kouř pára balón bublina jiskra dým hélium popel"),
         outside=s("kámen déšť kroupy mince kotva písek cihla sníh kapka žalud")),
    dict(id="v9-slane", level="normal",
         roof="věci, které jsou slané",
         ask="jsou slané",
         inside=s("moře slzy pot šunka olivy sardinka sýr slanina"),
         outside=s("déšť jezero mléko med čaj jablko mouka rýže cukr limonáda")),
    dict(id="v9-letaji-bez-motoru", level="normal",
         roof="věci, které létají bez motoru",
         ask="létají bez motoru",
         inside=s("drak kluzák balón pírko list semínko bumerang šíp"),
         outside=s("letadlo vrtulník dron raketa loď vlak autobus tramvaj kolo motorka")),
    dict(id="v9-krehke-mraz", level="hard",
         roof="věci, které v mrazu popraskají",
         ask="v mrazu popraskají",
         inside=s("láhev vodovod hadice květináč sud kanystr sklenice konev"),
         outside=s("kámen plech drát klíč kladivo řetěz šroub provaz guma hadr")),

    # ================================================== kalendář a zeměpis ==
    dict(id="v9-zamknout", level="normal",
         roof="věci, které se dají zamknout na klíč",
         ask="se dají zamknout na klíč",
         inside=s("dveře auto kolo trezor kufr skříňka brána zámek"),
         outside=s("okno stůl police žebřík koberec lampa deka talíř sešit hrnec")),
    dict(id="v9-lekarnicka", level="normal",
         roof="věci, které musí být v autolékárničce",
         ask="musí být v autolékárničce",
         inside=s("obinadlo náplast rouška rukavice nůžky šátek obvaz špendlík"),
         outside=s("vesta trojúhelník lopata kanystr lano vozík plachta klíč pumpa zvedák")),
    dict(id="v9-morava", level="normal",
         roof="města, která leží na Moravě",
         ask="leží na Moravě",
         inside=s("Brno Olomouc Zlín Přerov Znojmo Kroměříž Vyškov Prostějov"),
         outside=s("Plzeň Liberec Kladno Beroun Tábor Písek Jičín Cheb Louny Mělník")),
    dict(id="v9-krajska", level="normal",
         roof="krajská města",
         ask="jsou to krajská města",
         inside=s("Jihlava Zlín Pardubice Liberec Olomouc Brno Plzeň Ostrava"),
         outside=s("Kolín Tábor Kroměříž Písek Jičín Beroun Louny Přerov Mělník Vyškov")),
    dict(id="v9-rakousko-uhersko", level="hard",
         roof="země, které byly v Rakousku-Uhersku",
         ask="patřily do Rakouska-Uherska",
         inside=s("Maďarsko Slovensko Chorvatsko Slovinsko Rakousko Bosna"),
         outside=s("Německo Rusko Švédsko Řecko Francie Španělsko Dánsko Norsko Belgie Portugalsko")),
    dict(id="v9-unesco", level="hard",
         roof="česká města na seznamu UNESCO",
         ask="jsou na seznamu UNESCO",
         inside=s("Telč Litomyšl Kroměříž Holašovice Lednice Třebíč Žďár Kladruby"),
         outside=s("Tábor Beroun Kolín Písek Jičín Louny Mělník Vyškov Rakovník Nymburk")),

    # =============================================== mluvnice a pravopis ==
    dict(id="v9-nepravidelne", level="hard",
         roof="slova s nepravidelným množným číslem",
         ask="mají nepravidelné množné číslo",
         inside=s("dítě oko ucho ruka člověk kůň noha přítel"),
         outside=s("stůl okno kniha lampa židle talíř klíč koš hrnec police")),
    dict(id="v9-presmycka", level="hard",
         roof="slova, ze kterých se přeskládáním písmen stane jiné slovo",
         # kos → sok, lom → mol, rak → kar, sud → dus, tón → not, veko → keov?
         ask="se dají přeskládat na jiné slovo",
         # kos→sok, lom→mol, rak→kar, vlas→sval, kapr→prak, brus→srub,
         # lak→kal, krb→brk, role→orel. Každou dvojici jsem ověřil ručně:
         # obě slova musí být běžná česká slova, jinak hráč přesmyčku
         # nenajde, ani když ví, co hledá.
         inside=s("kos lom rak vlas kapr brus lak krb role"),
         outside=s("hrnec police koště žebřík kastrol kbelík ubrus deštník koberec sešit")),
    dict(id="v9-rym-ice", level="normal",
         roof="slova, která se rýmují se slovem police",
         ask="se rýmují se slovem police",
         inside=s("ulice silnice sklenice hranice lavice vidlice nemocnice čepice"),
         outside=s("koberec žebřík hrnec deštník polštář kastrol pekáč trakař podnos batoh")),
    dict(id="v9-rym-ina", level="normal",
         roof="slova, která se rýmují se slovem hodina",
         ask="se rýmují se slovem hodina",
         inside=s("rodina novina bublina lavina dřevina slanina rostlina mýtina"),
         outside=s("koberec žebřík hrnec deštník polštář kastrol pekáč trakař podnos batoh")),

    # ================================================== ustálená spojení ==
    dict(id="v9-bily", level="hard",
         roof="slova, která tvoří dvojici se slovem bílý",
         ask="tvoří se slovem bílý ustálené spojení",
         inside=s("vrána maso místa paní sobota šum kůň prapor"),
         outside=s("police koberec žebřík mrkev talíř kbelík hrnec lampa sešit deštník")),
    dict(id="v9-suchy", level="hard",
         roof="slova, která tvoří dvojici se slovem suchý",
         ask="tvoří se slovem suchý ustálené spojení",
         inside=s("zip led humor období nit chleba stéblo"),
         outside=s("police koberec žebřík mrkev talíř kbelík hrnec lampa sešit deštník")),
    dict(id="v9-hluboky", level="normal",
         roof="slova, která tvoří dvojici se slovem hluboký",
         ask="tvoří se slovem hluboký ustálené spojení",
         inside=s("talíř spánek dojem mráz voda les úklona myšlenka"),
         outside=s("police koberec žebřík mrkev talíř kbelík hrnec lampa sešit deštník"),
         avoid=s("talíř")),
    dict(id="v9-ostry", level="normal",
         roof="slova, která tvoří dvojici se slovem ostrý",
         ask="tvoří se slovem ostrý ustálené spojení",
         inside=s("nůž jazyk zatáčka střelba sýr úhel zrak slovo"),
         outside=s("police koberec žebřík mrkev kbelík hrnec lampa sešit deštník ubrus")),
    dict(id="v9-tichy", level="hard",
         roof="slova, která tvoří dvojici se slovem tichý",
         ask="tvoří se slovem tichý ustálené spojení",
         inside=s("pošta souhlas domácnost společník voda oceán modlitba noc"),
         outside=s("police koberec žebřík mrkev kbelík hrnec lampa sešit deštník ubrus")),
    dict(id="v9-dlouhy", level="normal",
         roof="slova, která tvoří dvojici se slovem dlouhý",
         ask="tvoří se slovem dlouhý ustálené spojení",
         inside=s("vedení prsty chvíle nos vlna cesta doba čekání"),
         outside=s("police koberec žebřík mrkev kbelík hrnec lampa sešit deštník ubrus")),

    # ================================================ obory s vlastní řečí ==
    dict(id="v9-hory", skupina="obor", level="hard",
         roof="slova, která jsou zároveň části hory",
         ask="jsou to zároveň části hory",
         inside=s("sedlo hřeben štít úpatí kotlina sráz převis rokle"),
         avoid=s("hřeben")),
    dict(id="v9-film", skupina="obor", level="normal",
         roof="slova, která jsou zároveň filmařské pojmy",
         ask="jsou to zároveň filmařské pojmy",
         inside=s("klapka štáb záběr střih scéna role kaskadér dabing")),
    dict(id="v9-foto", skupina="obor", level="hard",
         roof="slova, která jsou zároveň fotografické pojmy",
         ask="jsou to zároveň fotografické pojmy",
         inside=s("clona závěrka ostření expozice hloubka stativ objektiv blesk")),
    dict(id="v9-pravo", skupina="obor", level="hard",
         roof="slova, která jsou zároveň právnické pojmy",
         ask="jsou to zároveň právnické pojmy",
         inside=s("žaloba odvolání spis líčení senát výrok důkaz obhajoba")),
    dict(id="v9-telocvik", skupina="obor", level="normal",
         roof="slova, která jsou zároveň tělocvičné nářadí",
         ask="jsou to zároveň tělocvičné nářadí",
         inside=s("hrazda kruhy koza kladina bradla švihadlo žíněnka lavička"),
         avoid=s("lavička")),
    dict(id="v9-fyzika", skupina="obor", level="hard",
         roof="slova, která jsou zároveň fyzikální veličiny",
         ask="jsou to zároveň fyzikální veličiny",
         inside=s("síla práce výkon tlak moment dráha tíha hmotnost"),
         avoid=s("metr")),
    dict(id="v9-matematika", skupina="obor", level="normal",
         roof="slova, která jsou zároveň matematické pojmy",
         ask="jsou to zároveň matematické pojmy",
         inside=s("mocnina odmocnina zlomek kořen osa úhel obsah rovnice"),
         avoid=s("matice")),
    dict(id="v9-kadernictvi", skupina="obor", level="normal",
         roof="slova, která jsou zároveň účesy a kadeřnické pojmy",
         ask="jsou to zároveň účesy nebo kadeřnické pojmy",
         inside=s("mikádo ofina culík drdol patka melír pěšinka trvalá"),
         avoid=s("hřeben nůžky")),
    dict(id="v9-myslivost", skupina="obor", level="hard",
         roof="slova, která jsou zároveň myslivecké pojmy",
         ask="jsou to zároveň myslivecké pojmy",
         inside=s("posed obora hon výřad šoulačka čekaná krmelec troubení")),
    dict(id="v9-lode", skupina="obor", level="hard",
         roof="slova, která jsou zároveň části lodi",
         ask="jsou to zároveň části lodi",
         inside=s("paluba kýl příď záď kotva plachta stěžeň kajuta")),
    dict(id="v9-letadlo", skupina="obor", level="normal",
         roof="slova, která jsou zároveň části letadla",
         ask="jsou to zároveň části letadla",
         inside=s("křídlo klapka trup podvozek ocas kokpit vztlak směrovka")),
    dict(id="v9-vlak", skupina="obor", level="normal",
         roof="slova, která jsou zároveň železniční pojmy",
         ask="jsou to zároveň železniční pojmy",
         inside=s("výhybka závora nástupiště návěstidlo posun vagon lokomotiva kolejnice")),
    dict(id="v9-skola", skupina="obor", level="normal",
         roof="slova, která jsou zároveň pojmy ze školy",
         ask="jsou to zároveň pojmy ze školy",
         inside=s("třída družina ředitelna sborovna zvonek žákovská tabule přestávka"),
         outside=s("hrnec koště plot kabát lampa konev ručník kýbl polštář koberec")),
    dict(id="v9-pivovar", skupina="obor", level="hard",
         roof="slova, která jsou zároveň pivovarské pojmy",
         ask="jsou to zároveň pivovarské pojmy",
         inside=s("várka chmel mladina spilka ležák sladovna kvasnice humna"),
         avoid=s("sud")),
    dict(id="v9-jeskyne", skupina="obor", level="hard",
         roof="slova, která jsou zároveň části jeskyně",
         ask="jsou to zároveň části jeskyně",
         inside=s("krápník dóm komín sifon propast síň závrt ponor")),
    dict(id="v9-hrad", skupina="obor", level="normal",
         roof="slova, která jsou zároveň části hradu",
         ask="jsou to zároveň části hradu",
         inside=s("val příkop brána hladomorna palác nádvoří cimbuří bašta")),
    dict(id="v9-noviny", skupina="obor", level="hard",
         roof="slova, která jsou zároveň novinářské pojmy",
         ask="jsou to zároveň novinářské pojmy",
         inside=s("titulek sloupek rubrika inzerát redakce uzávěrka glosa sazba")),
    dict(id="v9-mapa", skupina="obor", level="hard",
         roof="slova, která jsou zároveň pojmy z mapy",
         ask="jsou to zároveň pojmy z mapy",
         inside=s("měřítko legenda vrstevnice azimut poledník rovnoběžka kóta růžice"),
         avoid=s("metr")),
    dict(id="v9-cirkus", skupina="obor", level="normal",
         roof="slova, která jsou zároveň cirkusové pojmy",
         ask="jsou to zároveň cirkusové pojmy",
         inside=s("manéž šapitó artista drezura klaun provazochodec krotitel žonglér")),
    dict(id="v9-zahrada", skupina="obor", level="normal",
         roof="slova, která jsou zároveň zahradnické pojmy",
         ask="jsou to zároveň zahradnické pojmy",
         inside=s("záhon skleník pařeniště roubování sazenice postřik okopávka řízek"),
         outside=s("hrnec koště kabát lampa ručník kýbl polštář sešit talíř kastrol")),
    dict(id="v9-horolezectvi", skupina="obor", level="hard",
         roof="slova, která jsou zároveň horolezecké vybavení",
         ask="jsou to zároveň horolezecké vybavení",
         inside=s("sedák karabina skoba lano cepín mačky jistítko smyčka"),
         avoid=s("provaz")),
    dict(id="v9-les", skupina="obor", level="hard",
         roof="slova, která jsou zároveň lesnické pojmy",
         ask="jsou to zároveň lesnické pojmy",
         inside=s("paseka mýtina remízek houština polom průsek pařez školka")),
    dict(id="v9-tkani", skupina="obor", level="hard",
         roof="slova, která jsou zároveň tkalcovské pojmy",
         ask="jsou to zároveň tkalcovské pojmy",
         inside=s("osnova útek stav cívka člunek přádelna příze tkanina")),
    dict(id="v9-hrncirstvi", skupina="obor", level="normal",
         roof="slova, která jsou zároveň hrnčířské pojmy",
         ask="jsou to zároveň hrnčířské pojmy",
         inside=s("kruh glazura pec střep hlína výpal točení engoba")),
    dict(id="v9-kone", skupina="obor", level="normal",
         roof="slova, která jsou zároveň části koně a postroje",
         ask="jsou to zároveň části koně nebo postroje",
         inside=s("hříva ohlávka třmen sedlo podkova uzda kopyto otěže")),
    dict(id="v9-lekarstvi", skupina="obor", level="hard",
         roof="slova, která jsou zároveň lékařské pojmy",
         ask="jsou to zároveň lékařské pojmy",
         inside=s("odběr stěr snímek nález recept ambulance převaz injekce"),
         avoid=s("pinzeta")),
    dict(id="v9-banka", skupina="obor", level="hard",
         roof="slova, která jsou zároveň bankovní pojmy",
         ask="jsou to zároveň bankovní pojmy",
         inside=s("úrok splátka jistina výpis převod hypotéka spoření poplatek")),
    dict(id="v9-posta", skupina="obor", level="normal",
         roof="slova, která jsou zároveň poštovní pojmy",
         ask="jsou to zároveň poštovní pojmy",
         inside=s("dobírka zásilka razítko poštovné listonoš kurýr známka balík"),
         avoid=s("schránka")),
    dict(id="v9-pocasi-pojmy", skupina="obor", level="hard",
         roof="slova, která jsou zároveň meteorologické pojmy",
         ask="jsou to zároveň meteorologické pojmy",
         inside=s("fronta inverze srážky níže výše oblačnost bouřka přeháňka")),
    dict(id="v9-chemie", skupina="obor", level="normal",
         roof="slova, která jsou zároveň chemické pojmy",
         ask="jsou to zároveň chemické pojmy",
         inside=s("roztok sraženina kyselina zásada prvek sloučenina zkumavka kahan")),
    dict(id="v9-biologie", skupina="obor", level="hard",
         roof="slova, která jsou zároveň biologické pojmy",
         ask="jsou to zároveň biologické pojmy",
         inside=s("buňka tkáň orgán jádro dělení výtrus pletivo lýko")),
    dict(id="v9-armada", skupina="obor", level="normal",
         roof="slova, která jsou zároveň vojenské pojmy",
         ask="jsou to zároveň vojenské pojmy",
         inside=s("rota četa hlídka průzkum ležení poplach prapor kasárna")),
    dict(id="v9-knihovna", skupina="obor", level="hard",
         roof="slova, která jsou zároveň knihovnické pojmy",
         ask="jsou to zároveň knihovnické pojmy",
         inside=s("signatura výpůjčka katalog fond depozitář rešerše regál čtenář"),
         avoid=s("police")),
    dict(id="v9-sachy", skupina="obor", level="normal",
         roof="slova, která jsou zároveň šachové pojmy",
         ask="jsou to zároveň šachové pojmy",
         inside=s("rošáda mat pat oběť vidlička tempo koncovka zahájení")),
    dict(id="v9-hokej-pojmy", skupina="obor", level="normal",
         roof="slova, která jsou zároveň hokejové pojmy",
         ask="jsou to zároveň hokejové pojmy",
         inside=s("buly přesilovka vyloučení nájezd brankoviště střídačka hokejka puk")),
    dict(id="v9-atletika", skupina="obor", level="normal",
         roof="slova, která jsou zároveň atletické disciplíny a náčiní",
         ask="jsou to zároveň atletické disciplíny nebo náčiní",
         inside=s("štafeta koule oštěp disk kladivo překážky dálka výška")),
    dict(id="v9-lyze", skupina="obor", level="normal",
         roof="slova, která jsou zároveň lyžařské pojmy",
         ask="jsou to zároveň lyžařské pojmy",
         inside=s("vlek sjezdovka oblouk hrana stopa skluznice hůlky vázání")),
    dict(id="v9-hodinarstvi", skupina="obor", level="hard",
         roof="slova, která jsou zároveň části hodin",
         ask="jsou to zároveň části hodin",
         inside=s("setrvačka ciferník ručička korunka kyvadlo závaží strojek nepokoj"),
         avoid=s("hodinky")),
    dict(id="v9-pleteni", skupina="obor", level="normal",
         roof="slova, která jsou zároveň pojmy z pletení",
         ask="jsou to zároveň pojmy z pletení",
         inside=s("oko řada jehlice klubko příze vzorek nabírání uzavírání")),
    dict(id="v9-kosti", level="normal",
         roof="slova, která jsou zároveň kosti v lidském těle",
         ask="jsou to zároveň kosti v lidském těle",
         inside=s("lopatka pánev čéška kostrč kyčel žebro holeň lebka"),
         avoid=s("lopatka")),
    dict(id="v9-hvezdy-lidove", level="hard",
         roof="slova, která jsou zároveň lidová jména hvězd",
         ask="jsou to zároveň lidová jména hvězd a souhvězdí",
         inside=s("Polárka Večernice Jitřenka Kuřátka Vozka Kosy"),
         outside=s("Kasiopeja Orion Andromeda Perseus Herkules Lyra Pegas Kentaur")),
    dict(id="v9-vino", skupina="obor", level="normal",
         roof="slova, která jsou zároveň vinařské pojmy",
         ask="jsou to zároveň vinařské pojmy",
         inside=s("réva hrozen mošt burčák vinice sklizeň lis sklep"),
         avoid=s("sud")),
    dict(id="v9-tabor", skupina="obor", level="normal",
         roof="slova, která jsou zároveň táborové vybavení",
         ask="jsou to zároveň táborové vybavení",
         inside=s("stan ohniště totem kotlík celta spacák menážka ešus")),
    dict(id="v9-snih", level="normal",
         roof="slova, která jsou zároveň podoby sněhu a mrazu",
         ask="jsou to zároveň podoby sněhu nebo mrazu",
         inside=s("jinovatka náledí ledovka poprašek závěj břečka chumelenice plískanice")),
    dict(id="v9-televize", skupina="obor", level="normal",
         roof="slova, která jsou zároveň televizní pojmy",
         ask="jsou to zároveň televizní pojmy",
         inside=s("pořad znělka reklama přenos program vysílání titulky studio")),
    dict(id="v9-pekarna", skupina="obor", level="normal",
         roof="slova, která jsou zároveň pekařské pojmy",
         ask="jsou to zároveň pekařské pojmy",
         inside=s("kvásek těsto hnětení ošatka kynutí kůrka střída pomoučení"),
         avoid=s("pekáč trouba")),

    # ================================================= další prameny názvů ==
    dict(id="v9-maly-princ", skupina="nazvy", level="normal",
         roof="slova z Malého prince",
         ask="jsou v Malém princi",
         inside=s("růže liška had planeta baobab beránek lampář hvězdář"),
         # Zahrada plná růží v knize je, takže mezi vetřelce nesmí.
         avoid=s("zahrada")),
    dict(id="v9-alenka", skupina="nazvy", level="normal",
         roof="slova z Alenky v říši divů",
         ask="jsou v Alence v říši divů",
         inside=s("klobouk králík kočka čaj zrcadlo houba karty sen"),
         # Alenka padá kolem polic a proleze do zahrady — obojí v knize je.
         avoid=s("police zahrada")),
    dict(id="v9-narnie", skupina="nazvy", level="hard",
         roof="slova z názvů dílů Narnie",
         ask="jsou v názvech dílů Narnie",
         inside=s("lev čarodějnice skříň princ plavba kůň bitva synovec"),
         avoid=s("skříň lampa")),  # lampa u Narnie stojí hned za skříní
    dict(id="v9-ostrov-pokladu", skupina="nazvy", level="normal",
         roof="slova z Ostrova pokladů",
         ask="jsou v Ostrově pokladů",
         inside=s("poklad ostrov papoušek mapa truhla plachetnice pirát hospoda")),
    dict(id="v9-christie", skupina="nazvy", level="hard",
         roof="slova z názvů knih Agathy Christie",
         ask="jsou v názvech knih Agathy Christie",
         inside=s("expres Nil hodiny abeceda zkouška karty schůzka čas")),
    dict(id="v9-poe", skupina="nazvy", level="hard",
         roof="slova z názvů povídek Edgara Allana Poea",
         ask="jsou v názvech povídek Edgara Allana Poea",
         inside=s("havran jáma kyvadlo brouk dům maska srdce studna"),
         # „Sud vína amontilladského" je taky Poe.
         avoid=s("sud")),
    dict(id="v9-wells", skupina="nazvy", level="hard",
         roof="slova z názvů knih H. G. Wellse",
         ask="jsou v názvech knih H. G. Wellse",
         inside=s("stroj čas válka světy ostrov měsíc potrava lidé")),
    dict(id="v9-bible", skupina="nazvy", level="hard",
         roof="slova z biblických příběhů",
         ask="jsou v biblických příbězích",
         inside=s("archa potopa věž ráj holubice mana žebřík studna"),
         avoid=s("žebřík koš zahrada")),  # Mojžíš v koši, rajská zahrada
    dict(id="v9-sverak-uhlir", skupina="nazvy", level="normal",
         roof="slova z názvů písniček Svěráka a Uhlíře",
         ask="jsou v názvech písniček Svěráka a Uhlíře",
         inside=s("vítr dělání statistika mravenec ukolébavka tábor jaro barbora")),
    dict(id="v9-vw", skupina="nazvy", level="hard",
         roof="slova z názvů písní Voskovce a Wericha",
         ask="jsou v názvech písní Voskovce a Wericha",
         inside=s("náhoda klobouk křoví svět David Goliáš šaty nebe")),
    dict(id="v9-kapely-pisne", skupina="nazvy", level="normal",
         roof="slova z názvů písní českých rockových kapel",
         ask="jsou v názvech písní českých rockových kapel",
         inside=s("medvídek šrouby matice Amerika pohoda dáma Colorado tabáček"),
         avoid=s("matice")),
    dict(id="v9-prazske-povesti", skupina="nazvy", level="hard",
         roof="slova z pražských pověstí",
         ask="jsou v pražských pověstech",
         inside=s("golem orloj Faust čert poklad rytíř kohout vodník")),
    dict(id="v9-detske-hry", skupina="nazvy", level="normal",
         roof="slova z názvů dětských her",
         ask="jsou v názvech dětských her",
         inside=s("bába škatule kulička panák cukr káva limonáda schovávaná")),
    dict(id="v9-zvyky", level="normal",
         roof="slova z českých zvyků a obyčejů",
         ask="patří k českým zvykům a obyčejům",
         inside=s("pomlázka koleda masopust dušičky půlnoční vinšování stromeček kraslice")),

    # =============================================== ještě vlastnosti věcí ==
    dict(id="v9-rub-lic", level="hard",
         roof="věci, které mají rub a líc",
         ask="mají rub a líc",
         inside=s("mince medaile látka karta koberec list ponožka deska"),
         outside=s("cihla klíč hrnec žebřík kbelík lampa provaz míč sklenice kladivo")),
    dict(id="v9-kompost", level="normal",
         roof="věci, které patří na kompost",
         ask="patří na kompost",
         inside=s("slupky listí tráva skořápky plevel seno piliny lógr"),
         outside=s("sklo plast kov baterie olej guma polystyren hadr drát plechovka")),
    dict(id="v9-jedno-pouziti", level="normal",
         roof="věci na jedno použití",
         ask="jsou na jedno použití",
         inside=s("kapesník brčko kelímek ubrousek sirka plena párátko sáček"),
         outside=s("hrnek talíř lžíce ručník deka kabát kbelík židle konvice utěrka")),
    dict(id="v9-nabit", level="normal",
         roof="věci, které se dají nabít",
         ask="se dají nabít",
         inside=s("baterie mobil powerbanka notebook kartáček hodinky vrtačka koloběžka"),
         outside=s("kladivo deštník klíč hrnec deka žebřík kniha židle koště lopata")),
    dict(id="v9-bydlet", level="normal",
         roof="stavby, ve kterých se dá bydlet",
         ask="se dají obývat",
         inside=s("dům chata karavan hausbót jurta stan byt srub"),
         outside=s("garáž kůlna skleník seník dílna sklep maják stodola hangár kotelna")),
    dict(id="v9-prukaz", level="hard",
         roof="stroje, na které je potřeba průkaz",
         ask="potřebují k řízení průkaz",
         inside=s("auto motorka letadlo loď jeřáb kamion rypadlo traktor"),
         outside=s("kolo koloběžka sáně brusle lyže kánoe běžky skateboard tříkolka šlapadlo")),
    dict(id="v9-na-dalku", level="normal",
         roof="věci, které se ovládají na dálku",
         ask="se ovládají na dálku",
         inside=s("televize garáž dron závora klimatizace kotel žaluzie brána"),
         outside=s("kladivo deštník žebřík konev koště hrnec lopata žehlička kbelík pila")),
    dict(id="v9-naostrit", level="normal",
         roof="věci, které se musí ostřit",
         ask="se musí čas od času naostřit",
         inside=s("nůž sekera pila kosa dláto nůžky hoblík tužka"),
         outside=s("kladivo lopata hrábě kbelík provaz deka hrnec žebřík konev pytel")),
    dict(id="v9-oloupat", level="normal",
         roof="jídlo, které se před jídlem loupe",
         ask="se před jídlem loupou",
         inside=s("banán pomeranč cibule vejce kiwi mandarinka česnek ananas"),
         outside=s("jablko hruška rajče jahoda rybíz švestka třešeň malina angrešt borůvka")),
]


HLAVICKA = '''"""Devátá várka rodin — sto os, a pokaždé jiné povahy.

TENHLE SOUBOR PÍŠE SKRIPT. Ruční úpravy zmizí při dalším spuštění; opravovat
se má `tools/gen_families9.py`, kde stojí zadání i kontroly.

Skupiny: vlastnosti věcí a přírody, kalendář a zeměpis, mluvnice a pravopis,
ustálená spojení, obory s vlastní řečí (film, právo, tělocvik, pivovar,
jeskyně) a další prameny názvů (Malý princ, Alenka, Poe, pražské pověsti).
"""

FAMILIES9 = ['''


def main() -> int:
    rodiny = []
    for spec in RODINY:
        rng = random.Random(spec["id"])
        zkontroluj_vetu(spec["ask"])

        inside = list(spec["inside"])
        if len(set(inside)) != len(inside):
            raise SystemExit(f"{spec['id']}: slovo uvnitř dvakrát")
        # Řemesla, obory a prameny názvů si vetřelce berou od sousedů téže
        # skupiny — nudná zásoba domácích potřeb by mezi nimi trčela.
        zasoba = spec.get("outside")
        if zasoba is None and spec.get("skupina"):
            zasoba = sousedni(spec, RODINY, rng)
        volna = [w for w in (zasoba if zasoba is not None else VATA.split())
                 if w not in inside and w not in spec.get("avoid", [])]
        # Z nudné zásoby se bere vzorek, ne celá. Sto vetřelců na rodinu se
        # nedá při kontrole přečíst, a číst se musí: stroj nepozná, že
        # *lopatka* je taky kost.
        outside = (sorted(random.Random(spec["id"]).sample(volna, 15))
                   if zasoba is None and len(volna) > 15 else volna)
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


if __name__ == "__main__":
    raise SystemExit(main())
