"""Jedenáctá várka rodin — sto os, opět z jiných soudků.

Desátá várka ukázala, že se osy dají brát ze čtyř nezávislých zásobníků:
z **částí věcí**, z **řeči řemesel**, z **ustálených spojení** a z **pravidel
o písmenech**. Každý z nich je hluboký — řemesel jsou desítky, částí má
každá věc svoje —, takže jich sto dalších vydá, aniž se začnou opakovat.

Skupiny téhle várky:

* **části věcí** — strom, sud, pluh, mlýn, varhany, buben, meč, brnění,
  sedlo, deštník, zvon, postel, mikroskop, tunel, silnice, pila, nůžky,
  kladivo, stan, batoh,
* **řemesla a obory** — sklárna, mlýn, lihovar, cukrárna, řeznictví,
  klempířství, pokrývačství, zámečnictví, sedlářství, kolářství,
  bednářství, provaznictví, zlatnictví, optika, geodézie, archeologie,
  archiv, muzeum, hutě, slévárna, potápění, jachting, lékárna, zubní
  ordinace, statistika,
* **ustálená spojení** — zelený, modrý, sladký, měkký, lehký, krátký,
  vysoký, silný, prázdný, divoký,
* **písmena** — koncovka -ost, krajní písmena vedle sebe v abecedě, stejný
  počet samohlásek a souhlásek, useknuté poslední písmeno, slovo pozpátku,
  háčky nad sykavkami, slovo úplně bez diakritiky,
* **prameny názvů** — Vančura, Lada, Kästner, Twain, London, Kipling,
  Poláček, Chytilová, Kubrick, balety,
* **vlastnosti a děje** — co praská v ohni, co se táhne v teple, co pění,
  co dorůstá, co unese člověka, co chladí bez proudu,
* **znalostní osy** — pražské vrchy, slovenská města, evropské metropole,
  čeští panovníci, apoštolové, odrůdy jablek, uzly, severští bohové.

Spuštění:  python3 tools/gen_families11.py
Výstup:    tools/intruder_families11.py
"""

import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from gen_families7 import VATA, decoys, zapis, zkontroluj_vetu  # noqa: E402
from gen_families10 import SLOVNIK, fold, priklonka, s, sousedni  # noqa: E402

OUT = os.path.join(HERE, "intruder_families11.py")

SAMOHLASKY = set("aeiouy")


def samohlasky(word: str) -> int:
    return sum(c in SAMOHLASKY for c in fold(word))


PRAVIDLA = {
    "koncovka-ost": lambda w: fold(w).endswith("ost"),
    "kraje-abeceda": lambda w: abs(ord(fold(w)[0]) - ord(fold(w)[-1])) == 1,
    "pul-na-pul": lambda w: samohlasky(w) == len(fold(w)) - samohlasky(w),
    "bez-posledniho": lambda w: len(w) > 3 and w[:-1] in SLOVNIK,
    "pozpatku": lambda w: len(w) > 2 and w[::-1] in SLOVNIK and w[::-1] != w,
    "sykavky": lambda w: any(ch in w.lower() for ch in "čšž"),
    "bez-diakritiky": lambda w: fold(w) == w.lower(),
}


RODINY: list[dict] = [
    # ==================================================== části věcí (20) ==
    dict(id="v11-strom", skupina="casti", level="normal",
         roof="části stromu",
         ask="jsou to zároveň části stromu",
         inside=s("kmen koruna větev kůra letokruh lýko běl dřeň"),
         avoid=s("květináč semínko truhlík")),
    dict(id="v11-sud", skupina="casti", level="hard",
         roof="části sudu",
         ask="jsou to zároveň části sudu",
         inside=s("dno dužina obruč čep víko zátka"),
         avoid=s("sud kbelík kýbl")),
    dict(id="v11-pluh", skupina="casti", level="hard",
         roof="části pluhu",
         ask="jsou to zároveň části pluhu",
         inside=s("radlice krojidlo hřídel odhrnovačka slupice patka"),
         avoid=s("motyka rýč hrábě trakař lopata")),
    dict(id="v11-mlyn", skupina="casti", level="hard",
         roof="části mlýna",
         ask="jsou to zároveň části mlýna",
         inside=s("kámen koleso násypka moučnice náhon lopatka"),
         avoid=s("lopatka struhadlo")),
    dict(id="v11-varhany", skupina="casti", level="hard",
         roof="části varhan",
         ask="jsou to zároveň části varhan",
         inside=s("píšťala měch rejstřík manuál pedál traktura"),
         avoid=s("hadice")),
    dict(id="v11-buben", skupina="casti", level="normal",
         roof="části bubnu",
         ask="jsou to zároveň části bubnu",
         inside=s("blána obruč plášť palička napínák struník"),
         avoid=s("provaz kolík")),
    dict(id="v11-mec", skupina="casti", level="normal",
         roof="části meče",
         ask="jsou to zároveň části meče",
         inside=s("čepel jílec hlavice záštita ostří hrot"),
         avoid=s("nůžky pilník")),
    dict(id="v11-brneni", skupina="casti", level="hard",
         roof="části brnění",
         ask="jsou to zároveň části brnění",
         inside=s("přilba kyrys náloketník náholenice kroužky rukavice"),
         avoid=s("bunda šála ponožka")),
    dict(id="v11-sedlo", skupina="casti", level="hard",
         roof="části jezdeckého sedla",
         ask="jsou to zároveň části jezdeckého sedla",
         inside=s("třmen podbřišník hruška kožka popruh sedlisko"),
         avoid=s("provaz řetízek náramek")),
    dict(id="v11-destnik-casti", skupina="casti", level="normal",
         roof="části deštníku",
         ask="jsou to zároveň části deštníku",
         inside=s("kostra potah hůl hrot rukojeť pero"),
         avoid=s("deštník hřebík kolík propiska")),
    dict(id="v11-zvon", skupina="casti", level="hard",
         roof="části zvonu",
         ask="jsou to zároveň části zvonu",
         inside=s("srdce koruna věnec plášť čepec límec"),
         avoid=s("šála bunda")),
    dict(id="v11-postel", skupina="casti", level="normal",
         roof="části postele",
         ask="jsou to zároveň části postele",
         inside=s("rošt čelo rám nohy matrace bočnice"),
         avoid=s("postel matrace peřina polštář deka prostěradlo")),
    dict(id="v11-mikroskop", skupina="casti", level="hard",
         roof="části mikroskopu",
         ask="jsou to zároveň části mikroskopu",
         inside=s("okulár objektiv stolek zrcátko tubus revolver"),
         avoid=s("brýle")),
    dict(id="v11-tunel", skupina="casti", level="hard",
         roof="části tunelu",
         ask="jsou to zároveň části tunelu",
         inside=s("portál ostění klenba čelba počva ražba")),
    dict(id="v11-silnice", skupina="casti", level="normal",
         roof="části silnice",
         ask="jsou to zároveň části silnice",
         inside=s("krajnice vozovka svodidlo násep příkop obrubník"),
         avoid=s("silnice plot")),
    dict(id="v11-pila", skupina="casti", level="normal",
         roof="části pily",
         ask="jsou to zároveň části pily",
         inside=s("list zub rozvod plátno rukojeť rám"),
         avoid=s("pilník hoblík kleště")),
    dict(id="v11-nuzky", skupina="casti", level="normal",
         roof="části nůžek",
         ask="jsou to zároveň části nůžek",
         inside=s("břit oko šroub hrot rameno čelist"),
         avoid=s("nůžky kleště šroub matice")),
    dict(id="v11-kladivo", skupina="casti", level="normal",
         roof="části kladiva",
         ask="jsou to zároveň části kladiva",
         inside=s("hlava násada klín ploška nos oko"),
         avoid=s("kladívko hřebík")),
    dict(id="v11-stan", skupina="casti", level="normal",
         roof="části stanu",
         ask="jsou to zároveň části stanu",
         inside=s("celta tropiko kolík tyč podlážka napínák"),
         avoid=s("kolík provaz hřebík")),
    dict(id="v11-batoh", skupina="casti", level="normal",
         roof="části batohu",
         ask="jsou to zároveň části batohu",
         inside=s("popruh přezka nosič kapsa poutko stahovák"),
         avoid=s("batoh peněženka pouzdro")),

    # ================================================ řemesla a obory (25) ==
    dict(id="v11-sklarna", skupina="obor", level="hard",
         roof="sklářské pojmy",
         ask="jsou to zároveň sklářské pojmy",
         inside=s("píšťala huť brus střep pánev tavba"),
         avoid=s("sklenice")),
    dict(id="v11-mlynarstvi", skupina="obor", level="hard",
         roof="mlynářské pojmy",
         ask="jsou to zároveň mlynářské pojmy",
         inside=s("otruby šrot krupice vejražka pytlování složení"),
         avoid=s("pytel struhadlo")),
    dict(id="v11-lihovar", skupina="obor", level="hard",
         roof="lihovarnické pojmy",
         ask="jsou to zároveň lihovarnické pojmy",
         inside=s("zápara kvas úkap dokap kotel destilát"),
         avoid=s("kastrol hrnec")),
    dict(id="v11-cukrarna", skupina="obor", level="normal",
         roof="cukrářské pojmy",
         ask="jsou to zároveň cukrářské pojmy",
         inside=s("poleva korpus krém marcipán šlehačka piškot"),
         avoid=s("krém pekáč mísa")),
    dict(id="v11-reznictvi", skupina="obor", level="normal",
         roof="řeznické pojmy",
         ask="jsou to zároveň řeznické pojmy",
         inside=s("bourání výsek špek střívko kýta plec"),
         avoid=s("pekáč mísa")),
    dict(id="v11-klempirstvi", skupina="obor", level="hard",
         roof="klempířské pojmy",
         ask="jsou to zároveň klempířské pojmy",
         inside=s("falc lem svod okap úžlabí lišta"),
         avoid=s("plot")),
    dict(id="v11-pokryvacstvi", skupina="obor", level="hard",
         roof="pokrývačské pojmy",
         ask="jsou to zároveň pokrývačské pojmy",
         inside=s("latě bobrovka hřebenáč šindel došek plech"),
         avoid=s("prkno")),
    dict(id="v11-zamecnictvi", skupina="obor", level="normal",
         roof="zámečnické pojmy",
         ask="jsou to zároveň zámečnické pojmy",
         inside=s("závit zápich výpalek ohýbačka nýtování dořez"),
         avoid=s("kleště pilník svěrák šroub matice vrtačka")),
    dict(id="v11-sedlarstvi", skupina="obor", level="hard",
         roof="sedlářské pojmy",
         ask="jsou to zároveň sedlářské pojmy",
         inside=s("useň řemen dratev šídlo přezka podšívka"),
         avoid=s("provaz kolík")),
    dict(id="v11-kolarstvi", skupina="obor", level="hard",
         roof="kolářské pojmy",
         ask="jsou to zároveň kolářské pojmy",
         inside=s("loukoť ráf paprsek náboj obruč šprušle"),
         avoid=s("trakař")),
    dict(id="v11-bednarstvi", skupina="obor", level="hard",
         roof="bednářské pojmy",
         ask="jsou to zároveň bednářské pojmy",
         inside=s("dužina obruč věnec stahování opalování drážkování"),
         avoid=s("sud kbelík")),
    dict(id="v11-provaznictvi", skupina="obor", level="hard",
         roof="provaznické pojmy",
         ask="jsou to zároveň provaznické pojmy",
         inside=s("pramen splétání konopí očko oplet stáčení"),
         avoid=s("provaz")),
    dict(id="v11-zlatnictvi", skupina="obor", level="hard",
         roof="zlatnické pojmy",
         ask="jsou to zároveň zlatnické pojmy",
         inside=s("ryzost puncovní zapuštění filigrán pájka lůžko"),
         avoid=s("náramek řetízek")),
    dict(id="v11-optika", skupina="sluzby", level="hard",
         roof="optické pojmy",
         ask="jsou to zároveň optické pojmy",
         inside=s("čočka ohnisko clona hranol zrcadlo lom"),
         avoid=s("brýle")),
    dict(id="v11-geodezie", skupina="sluzby", level="hard",
         roof="geodetické pojmy",
         ask="jsou to zároveň geodetické pojmy",
         inside=s("nivelace polygon záměra převýšení vytyčení bod"),
         avoid=s("metr pravítko")),
    dict(id="v11-archeologie", skupina="sluzby", level="hard",
         roof="archeologické pojmy",
         ask="jsou to zároveň archeologické pojmy",
         inside=s("sonda vrstva mohyla střep nález datace"),
         avoid=s("lopata rýč")),
    dict(id="v11-archiv", skupina="sluzby", level="hard",
         roof="archivní pojmy",
         ask="jsou to zároveň archivní pojmy",
         inside=s("fond skartace inventář karton signatura badatelna"),
         avoid=s("zápisník pouzdro")),
    dict(id="v11-muzeum", skupina="sluzby", level="normal",
         roof="muzejní pojmy",
         ask="jsou to zároveň muzejní pojmy",
         inside=s("sbírka vitrína depozitář popiska kurátor akvizice"),
         avoid=s("police")),
    dict(id="v11-hute", skupina="obor", level="hard",
         roof="hutnické pojmy",
         ask="jsou to zároveň hutnické pojmy",
         inside=s("vysoká struska koks vsázka surovina odpich"),
         avoid=s("pekáč")),
    dict(id="v11-slevarna", skupina="obor", level="hard",
         roof="slévárenské pojmy",
         ask="jsou to zároveň slévárenské pojmy",
         inside=s("forma jádro model licí nálitek kokila"),
         avoid=s("pekáč mísa")),
    dict(id="v11-potapeni", skupina="sluzby", level="normal",
         roof="potápěčské pojmy",
         ask="jsou to zároveň potápěčské pojmy",
         inside=s("ploutve maska automatika zátěž lahev výstup"),
         avoid=s("láhev")),
    dict(id="v11-jachting", skupina="sluzby", level="hard",
         roof="jachtařské pojmy",
         ask="jsou to zároveň jachtařské pojmy",
         inside=s("otěž kýl ráhno obrat hals kosatka"),
         avoid=s("provaz")),
    dict(id="v11-lekarna", skupina="sluzby", level="normal",
         roof="lékárnické pojmy",
         ask="jsou to zároveň lékárnické pojmy",
         inside=s("recept výdej tinktura mast čípek magistraliter"),
         avoid=s("krém pinzeta")),
    dict(id="v11-zubar", skupina="sluzby", level="normal",
         roof="zubařské pojmy",
         ask="jsou to zároveň zubařské pojmy",
         inside=s("plomba můstek kaz vrtačka otisk korunka"),
         avoid=s("vrtačka kartáček")),
    dict(id="v11-statistika", skupina="sluzby", level="hard",
         roof="statistické pojmy",
         ask="jsou to zároveň statistické pojmy",
         inside=s("medián průměr rozptyl výběr četnost odchylka"),
         avoid=s("metr")),

    # ========================================== ustálená spojení (10) ======
    dict(id="v11-zeleny", level="normal",
         roof="slova, která tvoří spojení se slovem zelený",
         ask="tvoří se slovem zelený ustálené spojení",
         inside=s("čtvrtek vlna kácení karta střecha zelí"),
         outside=s("sešit koště ubrus rohožka propiska záclona houpačka"
                   " tácek ramínko ubrousek")),
    dict(id="v11-modry", level="normal",
         roof="slova, která tvoří spojení se slovem modrý",
         ask="tvoří se slovem modrý ustálené spojení",
         inside=s("krev pondělí kód hodina helma velryba"),
         outside=s("sešit koště ubrus rohožka propiska záclona houpačka"
                   " tácek ramínko ubrousek")),
    dict(id="v11-sladky", level="normal",
         roof="slova, která tvoří spojení se slovem sladký",
         ask="tvoří se slovem sladký ustálené spojení",
         inside=s("život spánek řeči brambor voda odplata"),
         outside=s("sešit koště ubrus rohožka propiska záclona houpačka"
                   " tácek ramínko ubrousek")),
    dict(id="v11-mekky", level="normal",
         roof="slova, která tvoří spojení se slovem měkký",
         ask="tvoří se slovem měkký ustálené spojení",
         inside=s("srdce voda souhláska podnebí přistání nábytek"),
         outside=s("sešit koště ubrus rohožka propiska záclona houpačka"
                   " tácek ramínko ubrousek")),
    dict(id="v11-lehky", level="normal",
         roof="slova, která tvoří spojení se slovem lehký",
         ask="tvoří se slovem lehký ustálené spojení",
         inside=s("váha průmysl atletika spánek zbraň dívka"),
         outside=s("sešit koště ubrus rohožka propiska záclona houpačka"
                   " tácek ramínko ubrousek")),
    dict(id="v11-kratky", level="normal",
         roof="slova, která tvoří spojení se slovem krátký",
         ask="tvoří se slovem krátký ustálené spojení",
         inside=s("spoj proces paměť konec vlna slámka"),
         outside=s("sešit koště ubrus rohožka propiska záclona houpačka"
                   " tácek ramínko ubrousek")),
    dict(id="v11-vysoky", level="normal",
         roof="slova, která tvoří spojení se slovem vysoký",
         ask="tvoří se slovem vysoký ustálené spojení",
         inside=s("napětí škola pec sazba tlak společnost"),
         outside=s("sešit koště ubrus rohožka propiska záclona houpačka"
                   " tácek ramínko ubrousek")),
    dict(id="v11-silny", level="normal",
         roof="slova, která tvoří spojení se slovem silný",
         ask="tvoří se slovem silný ustálené spojení",
         inside=s("kafe stránka kuřák žaludek slovo proud"),
         outside=s("sešit koště ubrus rohožka propiska záclona houpačka"
                   " tácek ramínko ubrousek")),
    dict(id="v11-prazdny", level="normal",
         roof="slova, která tvoří spojení se slovem prázdný",
         ask="tvoří se slovem prázdný ustálené spojení",
         inside=s("slib žaludek hlava kapsa hrozba schránka"),
         outside=s("sešit koště ubrus rohožka propiska záclona houpačka"
                   " tácek ramínko ubrousek")),
    dict(id="v11-divoky", level="normal",
         roof="slova, která tvoří spojení se slovem divoký",
         ask="tvoří se slovem divoký ustálené spojení",
         inside=s("západ kachna voda víno karta stávka"),
         outside=s("sešit koště ubrus rohožka propiska záclona houpačka"
                   " tácek ramínko ubrousek")),

    # ================================================= písmena (7) =========
    dict(id="v11-ost", level="normal", rule="koncovka-ost",
         roof="slova končící na -ost",
         ask="končí na písmena ost",
         inside=s("radost mladost kost most starost rychlost moudrost"
                  " vlhkost"),
         outside=s("lampa police koberec sešit motyka konev ručník hrnec"
                   " kbelík žebřík")),
    dict(id="v11-kraje-abeceda", level="hard", rule="kraje-abeceda",
         roof="slova, jejichž první a poslední písmeno jdou v abecedě po sobě",
         ask="mají první a poslední písmeno vedle sebe v abecedě",
         inside=s("dítě dveře svět smrt duše pivo král právo"),
         outside=s("lampa police koberec motyka konev ručník hrnec kbelík"
                   " žebřík kolík")),
    dict(id="v11-pul-na-pul", level="hard", rule="pul-na-pul",
         roof="slova s stejným počtem samohlásek a souhlásek",
         ask="mají stejně samohlásek jako souhlásek",
         inside=s("kolo nota ruka voda pila míra husa vosa"),
         outside=s("koberec žebřík propiska prostěradlo struhadlo"
                   " naběračka záclona rohožka koště hrneček")),
    dict(id="v11-bez-posledniho", level="hard", rule="bez-posledniho",
         roof="slova, ze kterých po useknutí posledního písmene zbude jiné slovo",
         ask="po useknutí posledního písmene dají jiné slovo",
         inside=s("hrad sklon prst lesk sport past radar"),
         outside=s("lampa police koberec sešit motyka konev kbelík"
                   " žebřík kolík provaz")),
    dict(id="v11-pozpatku", level="hard", rule="pozpatku",
         roof="slova, která pozpátku dají jiné slovo",
         ask="pozpátku dají jiné slovo",
         inside=s("kos sok tak kat mol lom los sol kus suk kar rak vor"),
         outside=s("lampa police koberec sešit motyka konev ručník hrnec"
                   " kbelík žebřík")),
    dict(id="v11-sykavky", level="normal", rule="sykavky",
         roof="slova s č, š nebo ž",
         ask="mají v sobě č, š nebo ž",
         inside=s("čaj šála žula kožich čep šroub žebřík kaše"),
         outside=s("lampa police koberec motyka konev hrnec kolík deka"
                   " provaz kniha")),
    dict(id="v11-bez-diakritiky", level="normal", rule="bez-diakritiky",
         roof="slova bez jediné čárky a háčku",
         ask="nemají v sobě jedinou čárku ani háček",
         inside=s("kolo lampa okno strom ruka voda hlava kniha"),
         outside=s("žebřík záclona rohožka šuplík ručník kýbl košík"
                   " věšák hřebík příbor")),

    # ============================================== prameny názvů (10) =====
    dict(id="v11-vancura", skupina="nazvy", level="hard",
         roof="slova z názvů knih Vladislava Vančury",
         ask="jsou v názvech knih Vladislava Vančury",
         inside=s("pekař léto luk královna pole konec útěk")),
    dict(id="v11-lada", skupina="nazvy", level="normal",
         roof="slova z názvů knih Josefa Lady",
         ask="jsou v názvech knih Josefa Lady",
         inside=s("mikeš bubáci hastrmani liška kmotra vzpomínky kalendář")),
    dict(id="v11-kastner", skupina="nazvy", level="normal",
         roof="slova z názvů knih Ericha Kästnera",
         ask="jsou v názvech knih Ericha Kästnera",
         inside=s("detektivové třída luisa lotka bod muž trpaslík")),
    dict(id="v11-twain", skupina="nazvy", level="normal",
         roof="slova z názvů knih Marka Twaina",
         ask="jsou v názvech knih Marka Twaina",
         inside=s("dobrodružství princ chuďas yankee dvůr žabák deník")),
    dict(id="v11-london", skupina="nazvy", level="hard",
         roof="slova z názvů knih Jacka Londona",
         ask="jsou v názvech knih Jacka Londona",
         inside=s("tesák volání divočina vlk tulák hvězdy oheň")),
    dict(id="v11-kipling", skupina="nazvy", level="hard",
         roof="slova z názvů knih Rudyarda Kiplinga",
         ask="jsou v názvech knih Rudyarda Kiplinga",
         inside=s("džungle kniha statečný kapitán světlo hoch pohádky")),
    dict(id="v11-polacek", skupina="nazvy", level="hard",
         roof="slova z názvů knih Karla Poláčka",
         ask="jsou v názvech knih Karla Poláčka",
         inside=s("muži město hostinec stůl dům bylo kámen")),
    dict(id="v11-chytilova", skupina="nazvy", level="hard",
         roof="slova z názvů filmů Věry Chytilové",
         ask="jsou v názvech filmů Věry Chytilové",
         inside=s("sedmikrásky ovoce stromy panelstory kalamita faunovo"
                  " pasti")),
    dict(id="v11-kubrick", skupina="nazvy", level="hard",
         roof="slova z názvů filmů Stanleyho Kubricka",
         ask="jsou v názvech filmů Stanleyho Kubricka",
         inside=s("odysea pomeranč vesmír lesk sláva oči zabijáci")),
    dict(id="v11-balety", skupina="nazvy", level="normal",
         roof="slova z názvů baletů",
         ask="jsou v názvech slavných baletů",
         inside=s("jezero louskáček růženka petruška spartakus labuť"
                  " šípková")),

    # ============================================ vlastnosti a děje (15) ===
    dict(id="v11-praska", level="normal",
         roof="věci, které v ohni praskají",
         ask="v ohni praskají",
         inside=s("kaštan kukuřice bambus jalovec vejce brambora"),
         outside=s("kámen cihla písek hlína sklo kov beton popel struska"
                   " vápno")),
    dict(id="v11-tahne", level="normal",
         roof="věci, které se v teple táhnou",
         ask="se v teple táhnou",
         inside=s("sýr karamel guma vosk asfalt žvýkačka"),
         outside=s("sklo kámen cihla kov porcelán dřevo papír písek"
                   " křída sůl")),
    dict(id="v11-peni", level="normal",
         roof="věci, které pění",
         ask="pění",
         inside=s("mýdlo pivo šampon sodovka bílek moře"),
         outside=s("olej med sirup mléko čaj rtuť petrolej ocet líh"
                   " glycerin")),
    dict(id="v11-lepi", level="normal",
         roof="věci, které lepí",
         ask="lepí",
         inside=s("med pryskyřice žvýkačka lepidlo dehet karamel"),
         outside=s("písek mouka sůl cukr rýže krupice popel vápno křída"
                   " struska")),
    dict(id="v11-sviti-po-nasviceni", level="hard",
         roof="věci, které svítí po nasvícení",
         ask="svítí ve tmě, když se předtím nasvítí",
         inside=s("ciferník hvězdička nálepka vypínač značka náramek"),
         outside=s("zrcadlo sklenice mince klíč lžíce brýle hodinky"
                   " prsten knoflík sponka")),
    dict(id="v11-doroste", level="normal",
         roof="části těla, které dorostou",
         ask="dorostou, když se ustřihnou nebo ztratí",
         inside=s("nehet vlas paroh ocas zub chlup"),
         outside=s("oko ucho prst noha ruka koleno rameno loket palec"
                   " brada")),
    dict(id="v11-unese", level="normal",
         roof="věci, které unesou dospělého člověka",
         ask="unesou dospělého člověka",
         inside=s("led lano žebřík větev most houpačka"),
         outside=s("nit vlas papír pavučina stéblo pírko bublina sklo"
                   " sirka slámka")),
    dict(id="v11-chladi", level="hard",
         roof="věci, které chladí bez proudu",
         ask="chladí, i když do nich neteče proud",
         inside=s("studna sklep džbán vějíř stín průvan"),
         outside=s("lednička mrazák klimatizace ventilátor chladič"
                   " kompresor výparník kryostat termostat čerpadlo")),
    dict(id="v11-rozpusti-v-ustech", level="normal",
         roof="věci, které se rozpustí v ústech",
         ask="se rozpustí v ústech",
         inside=s("čokoláda karamel cukr lentilka pastilka zmrzlina"),
         outside=s("mrkev oříšek chleba jablko sýr maso rýže suchar"
                   " sušenka kůrka")),
    dict(id="v11-namocit", level="normal",
         roof="věci, které se před použitím namočí",
         ask="se před použitím musí namočit",
         inside=s("fazole houby štětec hlína špejle sádra"),
         outside=s("hřebík šroub kladivo pilník klíč nůžky kolík matice"
                   " provaz drát")),
    dict(id="v11-naviji", level="normal",
         roof="věci, které se navíjejí na cívku",
         ask="se navíjejí na cívku",
         inside=s("nit drát film lano páska vlasec"),
         outside=s("cihla kámen mince klíč hrnec sklenice deska talíř"
                   " prkno bedna")),
    dict(id="v11-skorapka", level="normal",
         roof="věci, které mají skořápku",
         ask="mají skořápku",
         inside=s("vejce ořech kokos mandle pistácie hlemýžď"),
         outside=s("jahoda hruška mrkev okurka salát rajče brambora"
                   " cibule dýně řepa")),
    dict(id="v11-podzim", level="normal",
         roof="plodiny, které se sklízejí na podzim",
         ask="se sklízejí až na podzim",
         inside=s("brambory řepa dýně jablka švestky kukuřice"),
         outside=s("ředkvička jahoda salát hrášek špenát třešně rebarbora"
                   " kedluben cibulka bylinky")),
    dict(id="v11-soli", level="normal",
         roof="jídla, která se solí",
         ask="se solí, ne sladí",
         inside=s("polévka brambory maso vejce chleba okurka"),
         outside=s("kompot povidla marmeláda perník čokoláda pudink"
                   " zmrzlina bábovka koláč piškot")),
    dict(id="v11-tone", level="hard",
         roof="věci, které v čisté vodě klesnou ke dnu",
         ask="v čisté vodě klesnou ke dnu",
         inside=s("kámen mince hřebík cihla sklo klíč"),
         outside=s("korek dřevo pěna led vosk plast pírko sláma bublina"
                   " papír")),

    # ============================================== znalostní osy (13) =====
    dict(id="v11-prazske-vrchy", level="hard",
         roof="pražské vrchy",
         ask="jsou to zároveň pražské vrchy",
         inside=s("Petřín Vítkov Vyšehrad Bohdalec Ládví Hanspaulka"
                  " Barrandov Vidoule"),
         outside=s("Říp Blaník Kleť Radhošť Ještěd Bezděz Boubín Sněžník"),
         avoid_asks=["jsou to zároveň jména českých měst"]),
    dict(id="v11-slovenska-mesta", level="hard",
         roof="slovenská města",
         ask="jsou to zároveň slovenská města",
         inside=s("Nitra Trnava Prešov Žilina Martin Levoča Poprad Zvolen"),
         outside=s("Krakov Lodž Lublin Gdaňsk Szeged Pécs Debrecín Miskolc"),
         avoid_asks=["jsou to zároveň jména českých měst"]),
    dict(id="v11-metropole", level="normal",
         roof="evropská hlavní města",
         ask="jsou to zároveň hlavní města evropských států",
         inside=s("Vídeň Lisabon Oslo Helsinky Dublin Sofie Riga Valletta"),
         outside=s("Hamburk Lyon Miláno Porto Rotterdam Bergen Antverpy Bilbao"),
         avoid_asks=["jsou to zároveň jména českých měst"]),
    dict(id="v11-panovnici", level="normal",
         roof="jména českých panovníků",
         ask="jsou to zároveň jména českých panovníků",
         inside=s("Václav Boleslav Vladislav Přemysl Jiří Ferdinand"
                  " Rudolf Leopold"),
         outside=s("Bohumil Dalibor Květoslav Vlastimil Miloš Radovan Slavoj Zbyněk"),
         avoid_asks=["jsou to zároveň příjmení českých prezidentů"]),
    dict(id="v11-apostolove", level="hard",
         roof="jména apoštolů",
         ask="jsou to zároveň jména apoštolů",
         inside=s("Petr Pavel Jakub Ondřej Tomáš Filip Matouš Šimon"),
         outside=s("Abrahám Izák Mojžíš Áron David Šalomoun Daniel Samson")),
    dict(id="v11-jablka", level="hard",
         roof="odrůdy jablek",
         ask="jsou to zároveň odrůdy jablek",
         inside=s("Jonatán Šampion Panenské Croncelské Průsvitné Boskoopské"
                  " Rubín Bohemia"),
         outside=s("Williams Konference Boscova Špendlík Blumka Renkloda Karlatka Durancie")),
    dict(id="v11-uzly", level="hard",
         roof="názvy uzlů",
         ask="jsou to zároveň názvy uzlů",
         inside=s("osmička dračí ambulanční lodní škrtič rybářský"
                  " zkracovačka plochá"),
         avoid=s("provaz")),
    dict(id="v11-severni-bohove", level="hard",
         roof="jména severských bohů",
         ask="jsou to zároveň jména severských bohů",
         inside=s("Ódin Thór Loki Freya Baldr Heimdall Frigg Týr"),
         outside=s("Áres Hádes Hermés Merkur Vulkán Neptun Apollón Dionýsos")),
    dict(id="v11-brambory", level="hard",
         roof="odrůdy brambor",
         ask="jsou to zároveň odrůdy brambor",
         inside=s("Adéla Dita Karin Marabel Agria Cimrman Bella Impala"),
         outside=s("Božena Vlasta Jarmila Ludmila Květa Blažena Radka Zdena"),
         avoid_asks=["jsou v názvech her Járy Cimrmana"]),
    dict(id="v11-planety-mesice", level="hard",
         roof="měsíce planet sluneční soustavy",
         ask="jsou to zároveň měsíce planet",
         inside=s("Titan Europa Ganymed Callisto Io Triton Phobos Deimos"),
         outside=s("Vega Sirius Antares Rigel Betelgeuze Aldebaran Deneb Polárka")),
    dict(id="v11-recke-bohyne", level="hard",
         roof="jména řeckých bohyň",
         ask="jsou to zároveň jména řeckých bohyň",
         inside=s("Héra Athéna Artemis Afrodíté Démétér Hestia Níké Iris"),
         outside=s("Juno Minerva Diana Ceres Vesta Flora Fortuna Aurora")),
    dict(id="v11-kameny", level="normal",
         roof="drahé a polodrahé kameny",
         ask="jsou to zároveň drahé kameny",
         inside=s("granát opál safír smaragd ametyst topaz jaspis achát"),
         avoid=s("křemen")),
    dict(id="v11-bylinky", level="normal",
         roof="kuchyňské bylinky",
         ask="jsou to zároveň kuchyňské bylinky",
         inside=s("bazalka tymián rozmarýn saturejka libeček dobromysl"
                  " estragon šalvěj"),
         avoid=s("mrkev brambora zahrada semínko")),
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


HLAVICKA = '''"""Jedenáctá várka rodin — sto skrytých střech.

TENHLE SOUBOR PÍŠE SKRIPT. Ruční úpravy zmizí při dalším spuštění; opravovat
se má `tools/gen_families11.py`, kde stojí zadání i kontroly.
"""

FAMILIES11 = ['''


if __name__ == "__main__":
    raise SystemExit(main())
