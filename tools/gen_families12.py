"""Dvanáctá várka rodin — sto os, poslední z velké série.

Skupiny jsou stejné povahy jako v předchozích várkách, jen z dalších soudků:

* **části věcí** — kotel, skříň, komín, studna, řeka, rybník, město,
  divadlo, klavír, trubka, brýle, motor, raketa, lyže, klobouk,
* **řemesla a obory** — kominictví, koželužna, tesařina, kamenictví,
  sochařství, grafika, čalounictví, sklenářství, topenářství, sladovna,
  rybníkářství, ovocnářství, chmelařství, ornitologie, entomologie,
  botanika, mineralogie, paleontologie, hydrologie, kosmonautika,
  telekomunikace, energetika, numismatika, kriminalistika, psychologie,
* **ustálená spojení** — hořký, čerstvý, plný, holý, planý, hluchý, křivý,
  rovný, mokrý, drahý,
* **písmena** — ypsilon, složené slovo ze dvou slov, dvě samohlásky vedle
  sebe, písmeno ě, koncovka -ník, koncovka -dlo, předpona pře-,
* **prameny názvů** — Hemingway, Kafka, Škvorecký, Kachyňa, Troška,
  Michal Tučný, trampské písně, symfonické básně, operety, pohádkové
  postavy,
* **vlastnosti a děje** — co se dá naskládat, zapíchnout, roztavit,
  recyklovat, co je z ropy, co je ze dřeva, co má datum spotřeby,
* **znalostní osy** — moře, káva, čaj, těstoviny, pečivo, prvky, evropské
  řeky, africké státy, americké státy, olympijská města, jazyky, čeští
  světci, čínský zvěrokruh, malířské barvy, odrůdy vína.

Spuštění:  python3 tools/gen_families12.py
Výstup:    tools/intruder_families12.py
"""

import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from gen_families7 import VATA, decoys, zapis, zkontroluj_vetu  # noqa: E402
from gen_families10 import SLOVNIK, fold, priklonka, s, sousedni  # noqa: E402

OUT = os.path.join(HERE, "intruder_families12.py")

SAMOHLASKY = set("aeiouy")


def slozene(word: str) -> bool:
    """Dá se rozdělit na dvě samostatná slova ze slovníku hry."""
    return any(word[:i] in SLOVNIK and word[i:] in SLOVNIK
               for i in range(3, len(word) - 2))


def dve_samohlasky(word: str) -> bool:
    f = fold(word)
    return any(f[i] in SAMOHLASKY and f[i + 1] in SAMOHLASKY
               for i in range(len(f) - 1))


PRAVIDLA = {
    "ypsilon": lambda w: "y" in w.lower() or "ý" in w.lower(),
    "slozene": slozene,
    "dve-samohlasky": dve_samohlasky,
    "e-hacek": lambda w: "ě" in w.lower(),
    "koncovka-nik": lambda w: fold(w).endswith("nik"),
    "koncovka-dlo": lambda w: fold(w).endswith("dlo"),
    "predpona-pre": lambda w: w.lower().startswith("pře"),
}


RODINY: list[dict] = [
    # ==================================================== části věcí (15) ==
    dict(id="v12-kotel", skupina="casti", level="hard",
         roof="části kotle",
         ask="jsou to zároveň části kotle",
         inside=s("topeniště rošt popelník výměník komínovka dvířka"),
         avoid=s("kastrol hrnec pekáč")),
    dict(id="v12-skrin", skupina="casti", level="normal",
         roof="části skříně",
         ask="jsou to zároveň části skříně",
         inside=s("police dvířka záda sokl závěs šuplík"),
         avoid=s("police šuplík komoda skříň věšák ramínko")),
    dict(id="v12-komin", skupina="casti", level="hard",
         roof="části komína",
         ask="jsou to zároveň části komína",
         inside=s("sopouch průduch hlava vymetání vložka krakorec")),
    dict(id="v12-studna", skupina="casti", level="hard",
         roof="části studny",
         ask="jsou to zároveň části studny",
         inside=s("roubení rumpál okov skruž zákryt vydatnost"),
         avoid=s("kbelík kýbl konev")),
    dict(id="v12-reka", skupina="casti", level="normal",
         roof="části řeky",
         ask="jsou to zároveň části řeky",
         inside=s("koryto břeh meandr tůň ústí pramen jez")),
    dict(id="v12-rybnik", skupina="casti", level="hard",
         roof="části rybníka",
         ask="jsou to zároveň části rybníka",
         inside=s("hráz výpusť stoka kádiště přeliv loviště")),
    dict(id="v12-mesto", skupina="casti", level="normal",
         roof="části města",
         ask="jsou to zároveň části města",
         inside=s("náměstí čtvrť předměstí centrum periferie nábřeží"),
         avoid=s("silnice")),
    dict(id="v12-divadlo-casti", skupina="casti", level="normal",
         roof="části divadla",
         ask="jsou to zároveň části divadla",
         inside=s("jeviště hlediště balkon opona zákulisí propadlo"),
         avoid=s("záclona")),
    dict(id="v12-klavir", skupina="casti", level="normal",
         roof="části klavíru",
         ask="jsou to zároveň části klavíru",
         inside=s("kladívko struna pedál klapka tlumítko víko"),
         avoid=s("kladívko")),
    dict(id="v12-trubka", skupina="casti", level="hard",
         roof="části trubky",
         ask="jsou to zároveň části trubky",
         inside=s("nátrubek ventil korpus strojivo ladička korouhvička"),
         avoid=s("hadice")),
    dict(id="v12-bryle", skupina="casti", level="normal",
         roof="části brýlí",
         ask="jsou to zároveň části brýlí",
         inside=s("obruba sklo nožička most sedlo stranice"),
         avoid=s("brýle sklenice")),
    dict(id="v12-motor", skupina="casti", level="hard",
         roof="části motoru",
         ask="jsou to zároveň části motoru",
         inside=s("blok hlava ojnice válec kliková vačka"),
         avoid=s("šroub matice")),
    dict(id="v12-raketa", skupina="casti", level="hard",
         roof="části rakety",
         ask="jsou to zároveň části rakety",
         inside=s("stupeň tryska kryt nosič palivo špička")),
    dict(id="v12-lyze-casti", skupina="casti", level="normal",
         roof="části lyže",
         ask="jsou to zároveň části lyže",
         inside=s("skluznice hrana vázání špička patka stoupání"),
         avoid=s("kolík")),
    dict(id="v12-klobouk", skupina="casti", level="normal",
         roof="části klobouku",
         ask="jsou to zároveň části klobouku",
         inside=s("dýnko krempa stuha potítko podšívka střecha"),
         avoid=s("šála bunda ramínko")),

    # ================================================ řemesla a obory (25) ==
    dict(id="v12-kominictvi", skupina="obor", level="hard",
         roof="kominické pojmy",
         ask="jsou to zároveň kominické pojmy",
         inside=s("saze vymetání sopouch koudel revize tah"),
         avoid=s("koště smeták")),
    dict(id="v12-kozeluzna", skupina="obor", level="hard",
         roof="koželužské pojmy",
         ask="jsou to zároveň koželužské pojmy",
         inside=s("useň tříslo lužení mízdření vyčinění líc")),
    dict(id="v12-tesarina", skupina="obor", level="hard",
         roof="tesařské pojmy",
         ask="jsou to zároveň tesařské pojmy",
         inside=s("krokev vazba pozednice sloup rozpěra plátování"),
         avoid=s("prkno kladívko")),
    dict(id="v12-kamenictvi", skupina="obor", level="hard",
         roof="kamenické pojmy",
         ask="jsou to zároveň kamenické pojmy",
         inside=s("špic dláto lom blok leštění osazení"),
         avoid=s("kladívko pilník")),
    dict(id="v12-socharstvi", skupina="obor", level="normal",
         roof="sochařské pojmy",
         ask="jsou to zároveň sochařské pojmy",
         inside=s("model odlitek patina sokl busta reliéf")),
    dict(id="v12-grafika", skupina="obor", level="hard",
         roof="grafické pojmy",
         ask="jsou to zároveň grafické pojmy",
         inside=s("lept rytina matrice otisk tah náklad"),
         avoid=s("propiska")),
    dict(id="v12-calounictvi", skupina="obor", level="hard",
         roof="čalounické pojmy",
         ask="jsou to zároveň čalounické pojmy",
         inside=s("popruh molitan potah nopa knoflíkování prošívání"),
         avoid=s("polštář matrace deka peřina")),
    dict(id="v12-sklenarstvi", skupina="obor", level="normal",
         roof="sklenářské pojmy",
         ask="jsou to zároveň sklenářské pojmy",
         inside=s("tabule řezák tmel lišta zasklení kalení"),
         avoid=s("sklenice")),
    dict(id="v12-topenarstvi", skupina="obor", level="normal",
         roof="topenářské pojmy",
         ask="jsou to zároveň topenářské pojmy",
         inside=s("stoupačka odvzdušnění oběh rozdělovač termostatická"
                  " expanzní"),
         avoid=s("hadice")),
    dict(id="v12-sladovna", skupina="obor", level="hard",
         roof="sladovnické pojmy",
         ask="jsou to zároveň sladovnické pojmy",
         inside=s("máčení klíčení hvozd humno slad rmut")),
    dict(id="v12-rybnikarstvi", skupina="obor", level="hard",
         roof="rybníkářské pojmy",
         ask="jsou to zároveň rybníkářské pojmy",
         inside=s("výlov kádě plůdek obsádka zátah komory"),
         avoid=s("kbelík")),
    dict(id="v12-ovocnarstvi", skupina="obor", level="normal",
         roof="ovocnářské pojmy",
         ask="jsou to zároveň ovocnářské pojmy",
         inside=s("podnož roub štěpování prořezávka koruna výhon"),
         avoid=s("zahrada semínko")),
    dict(id="v12-chmelarstvi", skupina="obor", level="hard",
         roof="chmelařské pojmy",
         ask="jsou to zároveň chmelařské pojmy",
         inside=s("česání konstrukce hlávka révy sušárna zavádění"),
         avoid=s("truhlík")),
    dict(id="v12-ornitologie", skupina="sluzby", level="hard",
         roof="ornitologické pojmy",
         ask="jsou to zároveň ornitologické pojmy",
         inside=s("kroužkování snůška mláďata tah hnízdiště volavý")),
    dict(id="v12-entomologie", skupina="sluzby", level="hard",
         roof="entomologické pojmy",
         ask="jsou to zároveň entomologické pojmy",
         inside=s("kukla larva krovky sosák tykadlo svlékání")),
    dict(id="v12-botanika", skupina="sluzby", level="normal",
         roof="botanické pojmy",
         ask="jsou to zároveň botanické pojmy",
         inside=s("palist oddenek cibule úžlabí letorost přeslen"),
         avoid=s("semínko truhlík")),
    dict(id="v12-mineralogie", skupina="sluzby", level="hard",
         roof="mineralogické pojmy",
         ask="jsou to zároveň mineralogické pojmy",
         inside=s("štěpnost tvrdost krystal vryp lesk dvojče")),
    dict(id="v12-paleontologie", skupina="sluzby", level="hard",
         roof="paleontologické pojmy",
         ask="jsou to zároveň paleontologické pojmy",
         inside=s("otisk zkamenělina vrstva naleziště obratel druhohory")),
    dict(id="v12-hydrologie", skupina="sluzby", level="hard",
         roof="hydrologické pojmy",
         ask="jsou to zároveň hydrologické pojmy",
         inside=s("průtok povodí odtok vodočet spád retence")),
    dict(id="v12-kosmonautika", skupina="sluzby", level="normal",
         roof="kosmonautické pojmy",
         ask="jsou to zároveň kosmonautické pojmy",
         inside=s("oběžná modul spojení přetížení návratový skafandr")),
    dict(id="v12-telekomunikace", skupina="sluzby", level="hard",
         roof="telekomunikační pojmy",
         ask="jsou to zároveň telekomunikační pojmy",
         inside=s("linka ústředna přenos pásmo rušení vysílač")),
    dict(id="v12-energetika", skupina="sluzby", level="hard",
         roof="energetické pojmy",
         ask="jsou to zároveň energetické pojmy",
         inside=s("špička výkon soustava odběr blok záloha")),
    dict(id="v12-numismatika", skupina="sluzby", level="hard",
         roof="numismatické pojmy",
         ask="jsou to zároveň numismatické pojmy",
         inside=s("ražba hrana opis nominál patina sbírka"),
         avoid=s("mince")),
    dict(id="v12-kriminalistika", skupina="sluzby", level="hard",
         roof="kriminalistické pojmy",
         ask="jsou to zároveň kriminalistické pojmy",
         inside=s("stopa daktyloskopie rekonstrukce ohledání profil sběr"),
         avoid=s("pinzeta")),
    dict(id="v12-psychologie", skupina="sluzby", level="normal",
         roof="psychologické pojmy",
         ask="jsou to zároveň psychologické pojmy",
         inside=s("vjem paměť podnět postoj vývoj temperament")),

    # ========================================== ustálená spojení (10) ======
    dict(id="v12-horky", level="normal",
         roof="slova, která tvoří spojení se slovem hořký",
         ask="tvoří se slovem hořký ustálené spojení",
         inside=s("pilulka čokoláda konec pravda mandle úsměv"),
         outside=s("sešit koště ubrus rohožka propiska záclona houpačka"
                   " tácek ramínko ubrousek")),
    dict(id="v12-cerstvy", level="normal",
         roof="slova, která tvoří spojení se slovem čerstvý",
         ask="tvoří se slovem čerstvý ustálené spojení",
         inside=s("vzduch vítr novomanžel zpráva stopa síla"),
         outside=s("sešit koště ubrus rohožka propiska záclona houpačka"
                   " tácek ramínko ubrousek")),
    dict(id="v12-plny", level="normal",
         roof="slova, která tvoří spojení se slovem plný",
         ask="tvoří se slovem plný ustálené spojení",
         inside=s("úvazek moc měsíc žaludek plyn hrst"),
         outside=s("sešit koště ubrus rohožka propiska záclona houpačka"
                   " tácek ramínko ubrousek")),
    dict(id="v12-holy", level="normal",
         roof="slova, která tvoří spojení se slovem holý",
         ask="tvoří se slovem holý ustálené spojení",
         inside=s("věta nesmysl fakt zeď rukou hlava"),
         outside=s("sešit koště ubrus rohožka propiska záclona houpačka"
                   " tácek ramínko ubrousek")),
    dict(id="v12-plany", level="hard",
         roof="slova, která tvoří spojení se slovem planý",
         ask="tvoří se slovem planý ustálené spojení",
         inside=s("poplach řeči naděje výhonek hlásič růže"),
         outside=s("sešit koště ubrus rohožka propiska záclona houpačka"
                   " tácek ramínko ubrousek")),
    dict(id="v12-hluchy", level="hard",
         roof="slova, která tvoří spojení se slovem hluchý",
         ask="tvoří se slovem hluchý ustálené spojení",
         inside=s("místo doba kout ucho okno kopřiva"),
         outside=s("sešit koště ubrus rohožka propiska záclona houpačka"
                   " tácek ramínko ubrousek")),
    dict(id="v12-krivy", level="hard",
         roof="slova, která tvoří spojení se slovem křivý",
         ask="tvoří se slovem křivý ustálené spojení",
         inside=s("přísaha obvinění pohled zrcadlo úsměv záda"),
         outside=s("sešit koště ubrus rohožka propiska záclona houpačka"
                   " tácek ramínko ubrousek")),
    dict(id="v12-rovny", level="normal",
         roof="slova, která tvoří spojení se slovem rovný",
         ask="tvoří se slovem rovný ustálené spojení",
         inside=s("záda čára příležitost páteř dílec trať"),
         outside=s("sešit koště ubrus rohožka propiska záclona houpačka"
                   " tácek ramínko ubrousek")),
    dict(id="v12-mokry", level="normal",
         roof="slova, která tvoří spojení se slovem mokrý",
         ask="tvoří se slovem mokrý ustálené spojení",
         inside=s("hadr sníh kout proces vlasy oblečení"),
         outside=s("sešit koště ubrus rohožka propiska záclona houpačka"
                   " tácek ramínko ubrousek")),
    dict(id="v12-drahy", level="normal",
         roof="slova, která tvoří spojení se slovem drahý",
         ask="tvoří se slovem drahý ustálené spojení",
         inside=s("kámen kov přítel žert špás host"),
         outside=s("sešit koště ubrus rohožka propiska záclona houpačka"
                   " tácek ramínko ubrousek")),

    # ================================================= písmena (7) =========
    dict(id="v12-ypsilon", level="normal", rule="ypsilon",
         roof="slova s ypsilonem",
         ask="mají v sobě y",
         inside=s("ryba byt mýdlo sýr jazyk myš zvyk výtah"),
         outside=s("kolo lampa police hrnec konev deka kniha provaz cihla"
                   " ubrus")),
    dict(id="v12-slozene", level="hard", rule="slozene",
         roof="slova složená ze dvou samostatných slov",
         ask="se dají rozdělit na dvě samostatná slova",
         inside=s("autobus zločin zloděj hodnota program televize centrum"
                  " půlnoc"),
         outside=s("lampa police hrnec deka kniha cihla motyka konev kolík"
                   " koberec")),
    dict(id="v12-dve-samohlasky", level="normal", rule="dve-samohlasky",
         roof="slova se dvěma samohláskami vedle sebe",
         ask="mají v sobě dvě samohlásky vedle sebe",
         inside=s("louka auto houba moucha pauza koule soutěž doupě"),
         outside=s("lampa police hrnec deka kniha provaz cihla ubrus"
                   " motyka konev")),
    dict(id="v12-e-hacek", level="normal", rule="e-hacek",
         roof="slova s písmenem ě",
         ask="mají v sobě písmeno ě",
         inside=s("věž pěna květ město těsto svět závěs oběd"),
         outside=s("lampa police hrnec deka kniha provaz cihla ubrus"
                   " motyka kolík")),
    dict(id="v12-nik", level="normal", rule="koncovka-nik",
         roof="slova končící na -ník",
         ask="končí na písmena ník",
         inside=s("rybník deník chodník kominík zvoník rolník básník"
                  " dělník"),
         outside=s("lampa police hrnec deka kniha provaz cihla ubrus"
                   " motyka konev")),
    dict(id="v12-dlo", level="normal", rule="koncovka-dlo",
         roof="slova končící na -dlo",
         ask="končí na písmena dlo",
         inside=s("mýdlo zrcadlo sedadlo kadidlo bidlo chodidlo křídlo"
                  " prostěradlo"),
         outside=s("lampa police hrnec deka kniha provaz cihla ubrus"
                   " motyka konev")),
    dict(id="v12-pre", level="normal", rule="predpona-pre",
         roof="slova začínající na pře-",
         ask="začínají na písmena pře",
         inside=s("přehrada přestávka převod překlad přesila přejezd"
                  " přezka přeslička"),
         outside=s("lampa police hrnec deka kniha provaz cihla ubrus"
                   " motyka konev")),

    # ============================================== prameny názvů (10) =====
    dict(id="v12-hemingway", skupina="nazvy", level="hard",
         roof="slova z názvů knih Ernesta Hemingwaye",
         ask="jsou v názvech knih Ernesta Hemingwaye",
         inside=s("stařec moře hrana armáda zbraně slunce ráj")),
    dict(id="v12-kafka", skupina="nazvy", level="hard",
         roof="slova z názvů díla Franze Kafky",
         ask="jsou v názvech díla Franze Kafky",
         inside=s("proces zámek proměna amerika ortel dopis nora")),
    dict(id="v12-skvorecky", skupina="nazvy", level="hard",
         roof="slova z názvů knih Josefa Škvoreckého",
         ask="jsou v názvech knih Josefa Škvoreckého",
         inside=s("zbabělci prapor sezóna mirákl lvíče příběh tank")),
    dict(id="v12-kachyna", skupina="nazvy", level="hard",
         roof="slova z názvů filmů Karla Kachyni",
         ask="jsou v názvech filmů Karla Kachyni",
         inside=s("ucho kočár srnec smrt republika sestřičky vlak")),
    dict(id="v12-troska", skupina="nazvy", level="normal",
         roof="slova z názvů filmů Zdeňka Trošky",
         ask="jsou v názvech filmů Zdeňka Trošky",
         inside=s("slunce seno jahody princezna mlejn peklo štěstí"
                  " skřítek")),
    dict(id="v12-tucny", skupina="nazvy", level="hard",
         roof="slova z názvů písní Michala Tučného",
         ask="jsou v názvech písní Michala Tučného",
         inside=s("báječná ženská blbec sněhu kamarád rodeo halelujá"
                  " zlatokop")),
    dict(id="v12-trampske", skupina="nazvy", level="normal",
         roof="slova z názvů trampských písní",
         ask="jsou v názvech trampských písní",
         inside=s("vlak niagara oheň řeka údolí stopa hvězdy kotva")),
    dict(id="v12-symfonicke-basne", skupina="nazvy", level="hard",
         roof="slova z názvů symfonických básní",
         ask="jsou v názvech symfonických básní",
         inside=s("vltava blaník šárka tábor lesy pole vodník polednice")),
    dict(id="v12-operety", skupina="nazvy", level="hard",
         roof="slova z názvů operet",
         ask="jsou v názvech slavných operet",
         inside=s("netopýr vdova krev baron cikán princezna mlýn ptáčník")),
    dict(id="v12-pohadkove-postavy", level="normal",
         roof="jména českých pohádkových postav",
         ask="jsou to zároveň jména českých pohádkových postav",
         inside=s("Otesánek Budulínek Smolíček Křemílek Rákosníček"
                  " Hurvínek Bajaja Rumcajs"),
         outside=s("Pinocchio Bambi Mauglí Pipi Shrek Aladin Ariel Mickey")),

    # ============================================ vlastnosti a děje (18) ===
    dict(id="v12-naskladat", level="normal",
         roof="věci, které se dají naskládat na sebe",
         ask="se dají naskládat na sebe do komína",
         inside=s("talíř židle krabice kelímek pneumatika paleta"),
         outside=s("koště žebřík hadice provaz lampa deštník kytara"
                   " zrcadlo obraz vidlička")),
    dict(id="v12-zapichnout", level="normal",
         roof="věci, které se zapichují do země",
         ask="se zapichují do země",
         inside=s("kolík slunečník lopata cedule stan vidle"),
         outside=s("hrnec deka kniha lampa koberec zrcadlo polštář ubrus"
                   " sklenice talíř")),
    dict(id="v12-ropa", level="hard",
         roof="věci vyráběné z ropy",
         ask="se vyrábějí z ropy",
         inside=s("benzin asfalt nylon vazelína plast parafín"),
         outside=s("papír vlna bavlna hlína sklo vápno kámen dřevo korek"
                   " len")),
    dict(id="v12-drevo", level="normal",
         roof="věci vyráběné ze dřeva",
         ask="se vyrábějí ze dřeva",
         inside=s("papír sirka tužka sud parkety korek"),
         outside=s("sklo beton ocel hliník guma porcelán cement asfalt"
                   " nylon plast")),
    dict(id="v12-recyklace", level="normal",
         roof="věci, které se dají recyklovat",
         ask="se dají recyklovat",
         inside=s("papír sklo plech plast baterie olej"),
         outside=s("porcelán zrcadlo keramika žárovka guma pneumatika"
                   " vata obinadlo tapeta molitan")),
    dict(id="v12-roztavit", level="normal",
         roof="věci, které se dají roztavit a znovu ztuhnout",
         ask="se dají roztavit a nechat znovu ztuhnout",
         inside=s("vosk cín olovo sklo čokoláda sýr"),
         outside=s("dřevo papír kámen cihla vápno beton písek hlína"
                   " korek vlna")),
    dict(id="v12-sbirka", level="normal",
         roof="věci, které se sbírají do sbírek",
         ask="se sbírají do sbírek",
         inside=s("známka mince pohlednice odznak autogram model"),
         outside=s("brambora mrkev cibule hrách rýže mouka sůl cukr"
                   " krupice kroupy")),
    dict(id="v12-spotreba", level="normal",
         roof="věci s vytištěným datem spotřeby",
         ask="mají na obalu datum spotřeby",
         inside=s("jogurt mléko šunka léky vejce salát"),
         outside=s("kladivo hřebík lopata žebřík provaz cihla klíč prkno"
                   " kolík drát")),
    dict(id="v12-noc-zvuk", level="hard",
         roof="tvorové, kteří se ozývají v noci",
         ask="se ozývají hlavně v noci",
         inside=s("sova cvrček žába slavík netopýr vlk"),
         outside=s("skřivan vlaštovka kos čáp husa kůň kráva ovce beran"
                   " kohout")),
    dict(id="v12-obloha-okem", level="normal",
         roof="tělesa viditelná pouhým okem",
         ask="jsou na obloze vidět i bez dalekohledu",
         inside=s("měsíc venuše mars jupiter saturn kometa"),
         outside=s("neptun uran pluto ceres eris charon titan europa"
                   " ganymed callisto")),
    dict(id="v12-obiha-slunce", level="hard",
         roof="tělesa obíhající kolem Slunce",
         ask="obíhají kolem Slunce",
         inside=s("země mars merkur planetka kometa jupiter"),
         outside=s("měsíc europa titan triton phobos deimos ganymed"
                   " callisto charon io")),
    dict(id="v12-drogerie", level="normal",
         roof="věci, které se koupí v drogerii",
         ask="se prodávají v drogerii",
         inside=s("mýdlo šampon prášek zubní hřeben houba"),
         outside=s("kladivo hřebík lopata žebřík provaz cihla klíč prkno"
                   " kolík drát")),
    dict(id="v12-jednou-rocne", level="normal",
         roof="věci, které se používají jednou za rok",
         ask="se používají jen jednou za rok",
         inside=s("stromeček kraslice adventní prskavka betlém maska"),
         outside=s("hrnec lžíce ručník kartáček hřeben ponožka klíč"
                   " peněženka budík deka")),
    dict(id="v12-voni-spalene", level="hard",
         roof="věci, které voní, když se spálí",
         ask="voní, teprve když se zapálí",
         inside=s("kadidlo tabák jehličí kafr koření vonná"),
         outside=s("guma plast vlasy peří kůže olej dehet síra vlna"
                   " papír")),
    dict(id="v12-na-prst", level="normal",
         roof="věci, které se navlékají na prst",
         ask="se navlékají na prst",
         inside=s("prsten náprstek gumička obvaz náplast rukavice"),
         outside=s("čepice šála opasek batoh brýle hodinky náhrdelník"
                   " ponožka bunda kabát")),
    dict(id="v12-rozsvitit", level="normal",
         roof="věci, které se dají rozsvítit",
         ask="se dají rozsvítit",
         inside=s("lampa baterka svíčka displej maják reflektor"),
         outside=s("zrcadlo okno sklenice hodinky kompas budík váhy"
                   " teploměr brýle lupa")),
    dict(id="v12-zamrazit", level="normal",
         roof="jídlo, které se dá zamrazit",
         ask="se dá zamrazit a pak zase rozmrazit",
         inside=s("maso pečivo ovoce zelenina ryba těsto"),
         outside=s("salát okurka vejce majonéza jogurt smetana meloun"
                   " ředkvička rajče tvaroh")),
    dict(id="v12-vyzehlit", level="normal",
         roof="věci, které se dají vyžehlit",
         ask="se dají vyžehlit",
         inside=s("košile ubrus kapesník povlečení sukně záclona"),
         outside=s("svetr bunda rukavice pásek boty batoh čepice deka"
                   " polštář koberec")),

    # ============================================== znalostní osy (15) =====
    dict(id="v12-more", level="normal",
         roof="názvy moří",
         ask="jsou to zároveň názvy moří",
         inside=s("Baltské Černé Rudé Jaderské Egejské Severní Karibské"
                  " Sargasové"),
         outside=s("Bodamské Ženevské Ladožské Oněžské Michiganské Aralské Bajkalské Huronské")),
    dict(id="v12-kava", level="normal",
         roof="druhy kávy",
         ask="jsou to zároveň druhy kávy",
         inside=s("espreso latte cappuccino mocca americano ristretto"
                  " turek frappé"),
         outside=s("kakao punč grog mošt cider tonik limonáda burčák"
                   " medovina kvas")),
    dict(id="v12-caj", level="normal",
         roof="druhy čaje",
         ask="jsou to zároveň druhy čaje",
         inside=s("rooibos oolong maté matcha sencha darjeeling assam"
                  " bancha"),
         outside=s("espreso ristretto cappuccino kakao punč grog mošt"
                   " cider tonik burčák")),
    dict(id="v12-testoviny", level="normal",
         roof="druhy těstovin",
         ask="jsou to zároveň druhy těstovin",
         inside=s("špagety penne fusilli kolínka nudle vřetena lasagne"
                  " tarhoňa"),
         outside=s("rizoto polenta focaccia pesto ragú tiramisu bruschetta"
                   " carpaccio gnocchi mascarpone")),
    dict(id="v12-pecivo", level="normal",
         roof="druhy pečiva",
         ask="jsou to zároveň druhy pečiva",
         inside=s("rohlík houska dalamánek veka bageta kaiserka preclík"
                  " bulka"),
         outside=s("knedlík halušky palačinka lívanec kaše noky šišky"
                   " taštička krupice omeleta")),
    dict(id="v12-prvky", level="hard",
         roof="názvy chemických prvků",
         ask="jsou to zároveň názvy chemických prvků",
         inside=s("wolfram vanad kobalt gallium rhenium iridium thallium"
                  " lanthan"),
         outside=s("oxid chlorid sulfid amoniak benzen acetylen peroxid"
                   " uhličitan dusičnan síran")),
    dict(id="v12-evropske-reky", level="hard",
         roof="evropské řeky",
         ask="jsou to zároveň evropské řeky",
         inside=s("Seina Temže Pád Tibera Rhóna Ebro Visla Sáva"),
         outside=s("Nil Kongo Amazonka Ganga Mekong Zambezi Missouri Jenisej"),
         avoid_asks=["jsou to zároveň jména českých měst"]),
    dict(id="v12-africke-staty", level="hard",
         roof="africké státy",
         ask="jsou to zároveň africké státy",
         inside=s("Ghana Zambie Angola Senegal Tunisko Súdán Uganda"
                  " Namibie"),
         outside=s("Nepál Laos Bhútán Ekvádor Guyana Surinam Paraguay Kambodža")),
    dict(id="v12-americke-staty", level="hard",
         roof="státy USA",
         ask="jsou to zároveň státy Spojených států",
         inside=s("Texas Utah Nevada Montana Ohio Alaska Oregon Idaho"),
         outside=s("Alberta Manitoba Ontario Quebec Yukon Sonora Chiapas Durango")),
    dict(id="v12-olympijska-mesta", level="hard",
         roof="města letních olympiád",
         ask="jsou to zároveň města letních olympiád",
         inside=s("Atlanta Sydney Barcelona Helsinky Antverpy Melbourne"
                  " Mnichov Soul"),
         outside=s("Káhira Bombaj Lima Bogotá Manila Nairobi Bagdád Teherán"),
         avoid_asks=["jsou to zároveň jména českých měst"]),
    dict(id="v12-svetci", level="hard",
         roof="čeští světci",
         ask="jsou to zároveň čeští světci",
         inside=s("Václav Ludmila Vojtěch Prokop Anežka Zdislava Jan"
                  " Kliment"),
         outside=s("Bohumil Květoslav Vlastimil Zbyněk Slavoj Radovan Miloslav Jaromír")),
    dict(id="v12-cinsky-zverokruh", level="hard",
         roof="znamení čínského zvěrokruhu",
         ask="jsou to zároveň znamení čínského zvěrokruhu",
         inside=s("krysa buvol tygr králík drak had koza opice")),
    dict(id="v12-malirske-barvy", level="hard",
         roof="malířské barvy",
         ask="jsou to zároveň názvy malířských barev",
         inside=s("okr umbra ultramarín karmín sépie indigo kobalt"
                  " běloba"),
         outside=s("paleta šablona plátno grunt fixativ špachtle napínák"
                   " rydlo malířské kalafuna")),
    dict(id="v12-odrudy-vina", level="hard",
         roof="odrůdy vína",
         ask="jsou to zároveň odrůdy vína",
         inside=s("ryzlink veltlín tramín frankovka sylvánské portugal"
                  " müller merlot"),
         outside=s("burčák mošt medovina cider sekt vermut kvas punč"
                   " grog svařák")),
]


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
        outside = (sorted(random.Random(spec["id"]).sample(volna, 15))
                   if zasoba is None and len(volna) > 15 else volna)

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


HLAVICKA = '''"""Dvanáctá várka rodin — sto skrytých střech.

TENHLE SOUBOR PÍŠE SKRIPT. Ruční úpravy zmizí při dalším spuštění; opravovat
se má `tools/gen_families12.py`, kde stojí zadání i kontroly.
"""

FAMILIES12 = ['''


if __name__ == "__main__":
    raise SystemExit(main())
