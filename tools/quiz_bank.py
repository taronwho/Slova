#!/usr/bin/env python3
"""
Banka otázek pro Otázku dne.

Formát jednoho záznamu:

    ("nadpis", "odpověď", ["alt", …], ("indicie 1", "indicie 2", "indicie 3"))

**Indicie jsou odstupňované a na pořadí záleží.** Je to jediné pravidlo, na
kterém celá hra stojí:

1. **Malá — a opravdu malá.** Nesmí obsahovat **to jedno**, co si s odpovědí
   spojí každý. „Fujitova stupnice" u tornáda nebo „jediný sladkovodní tuleň"
   u Bajkalu jsou přesně ty věty, které patří do třetí indicie, ne do první.
   Sem se píše fakt **stranou hlavního příběhu**: co se s tím dělo potom,
   jaké mělo číslo, kdo u toho ještě byl, kde to leželo. Kdo předmět zná
   doopravdy, uhodne; kdo o něm jen slyšel, nemá se čeho chytit. Tady se
   vydělává trojnásobek, tak to musí být těžké.
2. **Návodnější.** Zúží pole na hrstku možností — obor, země, doba, role.
3. **Velká.** Skoro prozradí. To, co si s odpovědí spojí každý.

Odpověď se v indiciích nesmí objevit, ani její část; hlídá to `5g_build_quiz.py`
a stěžuje si, když se to poruší.
"""

BANK: dict[str, list] = {}

# --------------------------------------------------------------------------
# Osobnosti
# --------------------------------------------------------------------------
BANK["osobnost"] = [
    ("Poznej známou osobnost.", "Karel Čapek", ["Čapek"], (
        "V letech 1921 až 1938 psal sloupky do Lidových novin a byl prvním předsedou českého PEN klubu.",
        "Byl to český spisovatel a novinář, který zemřel na zápal plic těsně před Vánocemi 1938.",
        "Do světových jazyků se přes jeho hru R.U.R. dostalo slovo robot, které mu poradil jeho bratr.",
    )),
    ("Poznej známou osobnost.", "Nikola Tesla", ["Tesla"], (
        "Poslední roky žil v newyorském hotelu, kde krmil holuby, a roku 1943 zemřel bez majetku.",
        "Byl to srbsko-americký vynálezce, který prosazoval střídavý proud proti Edisonovu stejnosměrnému.",
        "Nese jeho jméno jednotka magnetické indukce i americká automobilka elektromobilů.",
    )),
    ("Poznej známou osobnost.", "Marie Curie", ["Marie Curie-Sklodowská", "Marie Skłodowska-Curie", "Curie"], (
        "Za první světové války objížděla frontu s pojízdnými rentgenovými vozy, které sama pomáhala vybavit.",
        "Byla to fyzička a chemička, první žena, která přednášela na pařížské Sorbonně.",
        "Jako jediná získala Nobelovu cenu ve dvou různých vědních oborech; objevila polonium a radium.",
    )),
    ("Poznej známou osobnost.", "Antonín Dvořák", ["Dvořák"], (
        "Byl náruživý pozorovatel lokomotiv a chodíval si na nádraží zapisovat jejich čísla.",
        "Byl to český skladatel, který tři roky vedl konzervatoř v New Yorku.",
        "Jeho Symfonie č. 9 se jmenuje Z Nového světa.",
    )),
    ("Poznej známou osobnost.", "Alan Turing", ["Turing"], (
        "Ve volném čase závodně běhal a jeho maratonský čas zaostával za olympijským vítězem z roku 1948 jen o pár minut.",
        "Byl to britský matematik, který za války v Bletchley Parku pomáhal luštit německou šifru Enigma.",
        "Nese jeho jméno test, kterým se zkouší, zda se stroj dokáže vydávat za člověka.",
    )),
    ("Poznej známou osobnost.", "Emil Zátopek", ["Zátopek"], (
        "Po roce 1968 podepsal Dva tisíce slov, byl vyloučen ze strany a léta pak pracoval u vrtné soupravy.",
        "Byl to československý atlet, jehož ženou byla olympijská vítězka v hodu oštěpem.",
        "Na olympiádě v Helsinkách 1952 vyhrál pětku, desítku i maraton, který běžel poprvé v životě.",
    )),
    ("Poznej známou osobnost.", "Frida Kahlo", ["Kahlo"], (
        "Její dům v Coyoacánu s modrými zdmi je dnes muzeem — narodila se v něm i zemřela.",
        "Byla to mexická malířka, manželka mnohem staršího muralisty Diega Rivery.",
        "Proslula autoportréty se srostlým obočím; roku 2002 ji ve filmu zahrála Salma Hayek.",
    )),
    ("Poznej známou osobnost.", "Ludwig van Beethoven", ["Beethoven"], (
        "Dochovaly se po stovkách jeho konverzační sešity, do kterých mu návštěvy psaly, co mu chtějí říct.",
        "Byl to německý skladatel, který postupně ohluchl, ale komponoval dál.",
        "Jeho Devátá symfonie končí Ódou na radost, dnešní hymnou Evropské unie.",
    )),
    ("Poznej známou osobnost.", "Édith Piaf", ["Piaf"], (
        "Její životní láska, boxer Marcel Cerdan, zahynul roku 1949 při letecké nehodě.",
        "Byla to francouzská zpěvačka, která zemřela ve stejný den jako její krajan Jean Cocteau.",
        "Proslavila se pod pseudonymem, který v překladu do češtiny znamená „vrabčák“, a písní Non, je ne regrette rien.",
    )),
    ("Poznej známou osobnost.", "Jan Amos Komenský", ["Komenský", "Comenius"], (
        "Jeho hrob se našel až roku 1929 v kostelíku v nizozemském Naardenu, kde je dnes české muzeum.",
        "Byl to poslední biskup Jednoty bratrské a nazývá se učitelem národů.",
        "Napsal Labyrint světa a ráj srdce a obrázkovou učebnici Orbis pictus.",
    )),
    ("Poznej známou osobnost.", "Leonardo da Vinci", ["Leonardo", "da Vinci"], (
        "Poslední léta strávil ve Francii na zámku Clos Lucé, kam ho pozval král František I.",
        "Byl to italský renesanční malíř a vynálezce, který psal poznámky zrcadlově obráceně.",
        "Namaloval Poslední večeři a Monu Lisu.",
    )),
    ("Poznej známou osobnost.", "Winston Churchill", ["Churchill"], (
        "Byl posedlý zednictvím a na svém venkovském sídle Chartwell vlastnoručně vyzdil stovky metrů zdí.",
        "Byl to britský premiér, který se v roce 1945 sešel se Stalinem a Rooseveltem na Jaltě.",
        "Proslul projevem o krvi, dřině, slzách a potu a symbolem vítězství ze dvou prstů.",
    )),
    ("Poznej známou osobnost.", "Vincent van Gogh", ["van Gogh"], (
        "Malovat začal až v sedmadvaceti letech a za necelých deset let vytvořil kolem dvou tisíc děl.",
        "Byl to nizozemský malíř, který si v Arles po hádce s Gauguinem uřízl kus ucha.",
        "Namaloval Slunečnice a Hvězdnou noc.",
    )),
    ("Poznej známou osobnost.", "Božena Němcová", ["Němcová"], (
        "Provdala se v sedmnácti za o patnáct let staršího finančního komisaře a s ním se pak stěhovala po Čechách i Uhrách.",
        "Byla to česká spisovatelka doby národního obrození, která sbírala pohádky.",
        "Napsala Babičku, podle níž se v Ratibořicích jmenuje celé údolí.",
    )),
    ("Poznej známou osobnost.", "Isaac Newton", ["Newton"], (
        "Poslední léta strávil jako správce britské mincovny a nemilosrdně stíhal penězokazce.",
        "Byl to anglický fyzik a matematik, který se spolu s Leibnizem přel o prvenství v objevu integrálního počtu.",
        "Nese jeho jméno jednotka síly a k jeho jménu se váže historka s padajícím jablkem.",
    )),
    ("Poznej známou osobnost.", "Jára Cimrman", ["Cimrman"], (
        "Jeho existenci poprvé ohlásil rozhlasový pořad Nealkoholická vinárna U Pavouka roku 1966.",
        "Je to fiktivní český génius, kterého vymysleli Ladislav Smoljak, Zdeněk Svěrák a Jiří Šebánek.",
        "V anketě o největšího Čecha roku 2005 vyhrál, ale byl vyřazen, protože neexistuje.",
    )),
    ("Poznej známou osobnost.", "Wolfgang Amadeus Mozart", ["Mozart"], (
        "Jeho sestře přezdívali Nannerl a jako děti spolu koncertovali; skladatelem byl i jeho vlastní syn.",
        "Byl to rakouský skladatel, který jako dítě koncertoval po evropských dvorech.",
        "V Praze měla premiéru jeho opera Don Giovanni a jeho život zfilmoval Miloš Forman ve snímku s osmi Oscary.",
    )),
    ("Poznej známou osobnost.", "Jan Železný", ["Železný"], (
        "Po kariéře se dal na trenéřinu a vedl mimo jiné indického olympijského vítěze Neeradže Čopru.",
        "Je to český atlet, trojnásobný olympijský vítěz z let 1992, 1996 a 2000.",
        "Drží dosud světový rekord v hodu oštěpem — 98,48 metru z roku 1996.",
    )),
    ("Poznej známou osobnost.", "Nelson Mandela", ["Mandela"], (
        "Jeho rodné jméno znělo Rolihlahla, což se překládá jako „ten, kdo tahá za větev“ — tedy výtržník.",
        "Byl to jihoafrický politik, který dostal roku 1993 Nobelovu cenu míru.",
        "Stal se prvním černošským prezidentem Jihoafrické republiky po pádu apartheidu.",
    )),
    ("Poznej známou osobnost.", "Galileo Galilei", ["Galileo", "Galilei"], (
        "Poslední léta strávil v domácím vězení ve vile v Arcetri u Florencie a oslepl.",
        "Byl to italský astronom, kterého inkvizice donutila odvolat učení o pohybu Země.",
        "Dalekohledem objevil čtyři největší měsíce Jupiteru, které se po něm dodnes jmenují.",
    )),
    ("Poznej známou osobnost.", "Agatha Christie", ["Christie"], (
        "Za války pracovala v lékárně a znalost jedů odtud pak využila ve svých knihách; druhého manžela měla archeologa.",
        "Byla to britská spisovatelka detektivek, nejprodávanější autorka všech dob.",
        "Vymyslela belgického detektiva Hercula Poirota a slečnu Marplovou.",
    )),
    ("Poznej známou osobnost.", "Tomáš Garrigue Masaryk", ["Masaryk", "T. G. Masaryk", "TGM"], (
        "Jako chlapce ho dali do učení k zámečníkovi a ke kováři dřív, než ho poslali na gymnázium.",
        "Byl to filozof a politik, který se v Rukopisném sporu postavil na stranu odpůrců pravosti.",
        "Stal se prvním československým prezidentem a říkalo se mu tatíček.",
    )),
    ("Poznej známou osobnost.", "Charlie Chaplin", ["Chaplin"], (
        "Roku 1975 ho královna povýšila do rytířského stavu, tři roky nato mu neznámí pachatelé ukradli rakev.",
        "Byl to britský komik němého filmu, spoluzakladatel studia United Artists.",
        "Proslavil se postavou tuláka v buřince s hůlčičkou a knírkem.",
    )),
    ("Poznej známou osobnost.", "Jan Hus", ["Hus"], (
        "Poslední měsíce před koncilem strávil na Kozím hrádku a na hradě Krakovci.",
        "Byl to český kazatel, který kázal v pražské Betlémské kapli.",
        "Roku 1415 byl v Kostnici upálen; výročí jeho smrti je český státní svátek.",
    )),
    ("Poznej známou osobnost.", "Věra Čáslavská", ["Čáslavská"], (
        "Před olympiádou roku 1968 se tři týdny skrývala v horách u Šumperka a trénovala na louce s kládou místo kladiny.",
        "Byla to česká sportovní gymnastka, jedna z prvních signatářek manifestu Dva tisíce slov.",
        "Získala sedm olympijských zlatých medailí a v Mexiku se vdávala přímo na místě.",
    )),
]

# --------------------------------------------------------------------------
# Zeměpis
# --------------------------------------------------------------------------
BANK["zemepis"] = [
    ("Hlavní město kterého státu?", "Austrálie", [], (
        "Vzniklo od zeleného stolu roku 1913 jako kompromis mezi dvěma rivalskými městy.",
        "Není to největší město země, ačkoli si to hodně lidí myslí — ta dvě větší leží u moře.",
        "Jmenuje se Canberra a leží v zemi, jejímž největším městem je Sydney.",
    )),
    ("Poznej stát.", "Turecko", [], (
        "Do roku 1923 z jeho území vládla dynastie, která držela chalífát.",
        "Leží na dvou světadílech a hlavní město nemá u moře, ale ve vnitrozemí.",
        "Jeho největším městem je Istanbul, rozdělený průlivem Bospor.",
    )),
    ("Poznej evropskou řeku.", "Dunaj", ["Donau"], (
        "Od roku 1992 ho s Rýnem spojuje průplav přes Mohan, takže se dá po vodě dojet z Rotterdamu až k Černému moři.",
        "Protéká deseti státy — víc než kterákoli jiná řeka na světě.",
        "Vídeň, Bratislava, Budapešť i Bělehrad leží na jeho březích.",
    )),
    ("Poznej německé lázeňské město.", "Baden-Baden", [], (
        "Místní mezinárodní letiště sdílí s blízkým městem Karlsruhe.",
        "Leží na severozápadním okraji Schwarzwaldu, nedaleko hranic s Francií.",
        "Jeho název tvoří dvě stejná slova spojená spojovníkem.",
    )),
    ("V tomto francouzském městě…", "Toulouse", [], (
        "vznikla počátkem 70. let první „univerzita třetího věku“.",
        "přemosťuje známý Pont-Neuf řeku Garonnu.",
        "se nachází ústředí výrobce letadel Airbus.",
    )),
    ("Poznej ostrov.", "Island", [], (
        "Nemá armádu a jeho obyvatelé nemají příjmení v našem smyslu — používají jméno po otci.",
        "Leží na rozhraní dvou litosférických desek, takže se každý rok o pár centimetrů rozšiřuje.",
        "Jeho hlavním městem je Reykjavík a v roce 2010 tu sopka Eyjafjallajökull zastavila leteckou dopravu v Evropě.",
    )),
    ("Poznej horu.", "Mount Everest", ["Everest", "Sagarmatha", "Čomolungma"], (
        "Jeho výška se od prvního měření roku 1856 několikrát opravovala, naposledy roku 2020 na dnešní hodnotu.",
        "Leží na hranici Nepálu a Číny a jeho evropské jméno nese britského geodeta.",
        "Je nejvyšší horou světa, měří 8 849 metrů.",
    )),
    ("Poznej moře.", "Mrtvé moře", [], (
        "Jeho hladina klesá zhruba o metr ročně, protože se voda z hlavního přítoku odebírá na zavlažování.",
        "Leží mezi Izraelem a Jordánskem a ústí do něj řeka Jordán.",
        "Kvůli extrémní slanosti v něm člověk plave, i když se o to nesnaží, a nežijí v něm ryby.",
    )),
    ("Poznej české město.", "Kutná Hora", [], (
        "Ve 14. století se tu razil pražský groš a město bylo po Praze druhé nejbohatší v zemi.",
        "Leží ve Středočeském kraji a její historické jádro je od roku 1995 na seznamu UNESCO.",
        "Stojí tu chrám svaté Barbory a nedaleká kostnice v Sedlci vyzdobená lidskými kostmi.",
    )),
    ("Poznej stát.", "Kanada", [], (
        "Jeho nejsevernější trvale obydlená osada leží jen 800 kilometrů od pólu a mívá poštu jednou týdně.",
        "Je to druhý největší stát světa a má dva úřední jazyky.",
        "Na její vlajce je javorový list a jejím hlavním městem je Ottawa.",
    )),
    ("Poznej poušť.", "Sahara", [], (
        "Ještě před šesti tisíci lety tu byla savana s jezery; dokládají to skalní malby s plavci ve Wádí Súra.",
        "Rozkládá se přes deset afrických států a na jihu ji lemuje pás Sahel.",
        "Je největší horkou pouští světa, zhruba tak velká jako Spojené státy.",
    )),
    ("Poznej hlavní město.", "Brasília", ["Brasilia"], (
        "Postavilo se od nuly na prázdné náhorní plošině a otevřelo se roku 1960.",
        "Jeho hlavní architekt Oscar Niemeyer je z téže země, jejíž největší město je São Paulo.",
        "Půdorys má připomínat letadlo nebo motýla a je celé na seznamu UNESCO.",
    )),
    ("Poznej jezero.", "Bajkal", ["Bajkalské jezero"], (
        "V zimě zamrzá do hloubky přes metr a za rusko-japonské války po jeho ledu vedla provizorní železnice.",
        "Leží na jihu Sibiře a napájí ho víc než tři sta řek, ale odtéká z něj jediná — Angara.",
        "Je nejhlubší jezero světa a je v něm asi pětina veškeré sladké povrchové vody planety.",
    )),
    ("Poznej stát.", "Nepál", [], (
        "Jeho pásmový čas se od světového liší o pět hodin a pětačtyřicet minut, což jinde na světě není.",
        "Leží mezi Indií a Čínou a jeho hlavním městem je Káthmándú.",
        "Leží na jeho území osm z deseti nejvyšších hor světa.",
    )),
    ("Poznej průplav.", "Panamský průplav", ["Panama"], (
        "Práce na něm nejdřív začali Francouzi pod vedením stavitele Suezského průplavu a zkrachovali.",
        "Otevřel se roku 1914 a spojuje dva oceány přes nejužší místo pevniny.",
        "Lodě v něm zdvihá soustava zdymadel a jmenuje se po středoamerickém státě, kterým vede.",
    )),
    ("Poznej vodopád.", "Niagarské vodopády", ["Niagara"], (
        "Roku 1848 se na třicet hodin téměř zastavily, když jejich přítok ucpala ledová zácpa.",
        "Leží na hranici USA a Kanady mezi jezery Erie a Ontario.",
        "Nejznámější z nich se pro svůj tvar jmenuje Podkova a k jeho úpatí vozí turisty loď Panna mlhy.",
    )),
    ("Poznej stát.", "Švýcarsko", [], (
        "Poslední z jeho kantonů zavedl volební právo žen v místních věcech až roku 1990, a to na příkaz soudu.",
        "Nemá přístup k moři, není v Evropské unii a má čtyři úřední jazyky.",
        "Sídlí tu Mezinárodní olympijský výbor i Červený kříž a proslulo bankami, hodinkami a čokoládou.",
    )),
    ("Poznej českou řeku.", "Vltava", [], (
        "V místě, kde se stéká s Labem, je vodnatější a delší než ono — přesto se dál říká Labe.",
        "Pramení na Šumavě a je nejdelší řekou Česka.",
        "Protéká Prahou a Bedřich Smetana o ní napsal symfonickou báseň.",
    )),
    ("Poznej sopku.", "Vesuv", [], (
        "Jeho výbuch roku 79 popsal v dopisech očitý svědek Plinius mladší.",
        "Leží v Itálii nad Neapolským zálivem a je to jediná činná sopka na evropské pevnině.",
        "Popelem zasypal města Pompeje a Herculaneum.",
    )),
    ("Poznej stát.", "Bhútán", ["Bhutan"], (
        "Televizi a internet tu povolili až roku 1999, jako v poslední zemi světa.",
        "Je to buddhistické království v Himálaji mezi Indií a Čínou.",
        "Na jeho vlajce je drak a domácí jméno země znamená „země hromového draka“.",
    )),
    ("Poznej hlavní město.", "Ottawa", [], (
        "Za sídlo vlády ho roku 1857 vybrala královna Viktorie jako kompromis mezi anglickou a francouzskou částí země.",
        "Leží na hranici dvou provincií, na řece stejného jména.",
        "Je hlavním městem Kanady, ačkoli Toronto i Montreal jsou větší.",
    )),
    ("Poznej ostrov.", "Madagaskar", [], (
        "Od pevniny se oddělil zhruba před 88 miliony let, takže devět desetin jeho živočichů nežije nikde jinde.",
        "Je čtvrtým největším ostrovem světa a leží v Indickém oceánu u pobřeží Afriky.",
        "Žijí tu lemuři a roku 2005 podle něj vznikl animovaný film.",
    )),
    ("Poznej český vrchol.", "Sněžka", [], (
        "Na jejím vrcholu stojí kaple svatého Vavřince z konce 17. století.",
        "Leží v Krkonoších na hranici s Polskem a vede na ni lanovka z Pece.",
        "Je nejvyšší horou Česka, měří 1 603 metrů.",
    )),
    ("Poznej město.", "Benátky", ["Venezia", "Benátky v Itálii"], (
        "Jejich zvonice na hlavním náměstí se roku 1902 zřítila a postavila se znovu podle původních plánů.",
        "Jejich republika se po staletí zvala Nejjasnější a v čele stál dóže.",
        "Místo ulic tu jsou kanály, po kterých jezdí gondoly, a hlavní náměstí nese jméno svatého Marka.",
    )),
    ("Poznej stát.", "Chile", [], (
        "Roku 2010 tu z hloubky přes 600 metrů vytáhli po dvou měsících 33 zavalených horníků.",
        "Leží na západním pobřeží Jižní Ameriky a patří mu Velikonoční ostrov.",
        "Měří přes 4 000 kilometrů na délku, ale v průměru jen 180 na šířku.",
    )),
]

# --------------------------------------------------------------------------
# Věda
# --------------------------------------------------------------------------
BANK["veda"] = [
    ("Poznej chemickou sloučeninu.", "Kyselina sírová", ["H2SO4", "sírová"], (
        "Ve světě se jí vyrobí víc než kterékoli jiné průmyslové chemikálie a spotřeba bývala měřítkem vyspělosti hospodářství.",
        "Je to bezbarvá olejovitá kapalina, která silně pohlcuje vodu a přitom se zahřívá.",
        "Její vzorec je H₂SO₄ a je náplní olověných autobaterií.",
    )),
    ("Poznej chemický prvek.", "Rtuť", ["Hg"], (
        "Klobouky se z něj dřív klížily a otrava z toho postihovala kloboučníky natolik, že vešla do jazyka i do literatury.",
        "Je to jediný kov, který je za pokojové teploty kapalný.",
        "Býval v teploměrech a nese jméno stejné jako planeta nejblíž Slunci.",
    )),
    ("Poznej chemický prvek.", "Helium", ["He"], (
        "Získává se ze zemního plynu v několika málo nalezištích a jeho světové zásoby jsou omezené natolik, že se řeší jejich šetření.",
        "Je to druhý nejlehčí prvek a jediný, který nejde zmrazit za normálního tlaku.",
        "Plní se jím balonky a po nadechnutí zvýší hlas.",
    )),
    ("Poznej jednotku.", "Newton", ["N"], (
        "Zavedla ji až Generální konference pro váhy a míry roku 1948; do té doby se v technice počítalo s kilopondem.",
        "Měří se jí veličina, kterou popisují tři pohybové zákony.",
        "Jmenuje se po anglickém fyzikovi a měří sílu.",
    )),
    ("Poznej vědecký objev.", "DNA", ["deoxyribonukleová kyselina"], (
        "Její stavební prvky se párují vždy dvojice k dvojici a poměr jejich počtů popsal Erwin Chargaff už v roce 1950.",
        "Její strukturu popsali roku 1953 James Watson a Francis Crick.",
        "Má tvar dvoušroubovice a nese genetickou informaci.",
    )),
    ("Poznej planetu.", "Venuše", [], (
        "Sovětský program Veněra na ni jako první dopravil přístroj, který z povrchu poslal snímky a po pár desítkách minut se roztavil.",
        "Je Zemi nejbližší planetou a hustá atmosféra oxidu uhličitého na ní drží přes 460 °C.",
        "Ze Země je nejjasnějším objektem po Slunci a Měsíci; říká se jí Jitřenka nebo Večernice.",
    )),
    ("Poznej meteorologický jev.", "Tornádo", [], (
        "Vzniká pod bouřkovým oblakem takzvané supercely a předchází mu otáčivý proud, kterému se říká mezocyklóna.",
        "Místem jeho zvýšeného výskytu je středozápad Spojených států.",
        "Má ho jako součást uměleckého pseudonymu zpěvačka ve filmu Limonádový Joe.",
    )),
    ("Poznej teplotní stupnici.", "Fahrenheitova stupnice", ["Fahrenheit"], (
        "Nulu na ní její autor položil podle nejnižší teploty, které dosáhl směsí ledu, vody a salmiaku.",
        "Pojmenována je podle německého fyzika, který zdokonalil rtuťový teploměr.",
        "Dodnes se používá ve Spojených státech a v pár závislých územích.",
    )),
    ("Poznej vědeckou teorii.", "Teorie relativity", ["relativita", "speciální teorie relativity"], (
        "Matematický aparát pro její obecnou podobu autorovi pomáhal zvládnout jeho spolužák Marcel Grossmann.",
        "Vychází z ní, že čas plyne pomaleji, čím rychleji se pozorovatel pohybuje.",
        "Autorem je Albert Einstein a nejznámější vzorec z ní je E = mc².",
    )),
    ("Poznej lidský orgán.", "Játra", [], (
        "Protéká jimi zhruba čtvrtina veškeré krve v těle a ve staré fyziologii platily za sídlo jedné ze čtyř tělesných šťáv.",
        "Váží zhruba půldruhého kilogramu a produkují žluč.",
        "Poškozuje je alkohol a jejich onemocnění se jmenuje cirhóza.",
    )),
    ("Poznej vesmírné těleso.", "Halleyova kometa", ["Halley"], (
        "Roku 1986 k ní zamířila sonda Giotto Evropské kosmické agentury a přiblížila se na necelých šest set kilometrů.",
        "Vrací se zhruba jednou za 76 let, naposledy roku 1986.",
        "Zachycuje ji tapiserie z Bayeux jako znamení před bitvou u Hastingsu roku 1066.",
    )),
    ("Poznej chemický prvek.", "Uhlík", ["C"], (
        "Roku 1985 objevili tři chemici jeho dutou kulovou molekulu o šedesáti atomech a dostali za to Nobelovu cenu.",
        "Tvoří základ všech organických sloučenin a v přírodě se vyskytuje ve dvou velmi odlišných podobách.",
        "Jednou z nich je grafit v tužce, druhou diamant.",
    )),
    ("Poznej vědce.", "Gregor Johann Mendel", ["Mendel"], (
        "Zkoušel své pokusy zopakovat i na jestřábníku, kde mu výsledky nevycházely, což ho na dlouho odradilo.",
        "Byl to opat, který svá zjištění zveřejnil roku 1866 a za života nezískal uznání.",
        "Zakladatel genetiky; jeho pravidla se učí jako zákony dědičnosti a pracoval s hrachem.",
    )),
    ("Poznej jev.", "Polární záře", ["aurora"], (
        "Objevuje se v pásu kolem magnetického pólu a zesiluje ji porucha, kterou měří takzvaný index Kp.",
        "Zelenou barvu jí dává kyslík, načervenalou a fialovou dusík.",
        "Nejlépe je vidět v pásu kolem magnetického pólu — třeba na Islandu nebo v severním Norsku.",
    )),
    ("Poznej léčivo.", "Penicilin", [], (
        "K jeho hromadné výrobě pomohla roku 1941 plíseň nalezená na melounu na trhu ve státě Illinois.",
        "Za jeho objev a výrobu dostali roku 1945 tři vědci Nobelovu cenu.",
        "Byl to první antibiotikum a jeho objevitelem je Alexander Fleming.",
    )),
    ("Poznej chemickou sloučeninu.", "Amoniak", ["NH3", "čpavek"], (
        "Ve velkých chladírnách a zimních stadionech slouží jako chladivo označované E717.",
        "Jeho vodný roztok je zásaditý a slouží jako základ pro dusíkatá hnojiva.",
        "Má vzorec NH₃ a je cítit štiplavě, jako čisticí prostředky nebo zvířecí močůvka.",
    )),
    ("Poznej hvězdu.", "Sirius", ["Sírius"], (
        "Staří Egypťané podle jeho ranního východu určovali začátek roku a nástup záplav.",
        "Leží v souhvězdí Velkého psa, asi 8,6 světelného roku od nás.",
        "Je to nejjasnější hvězda noční oblohy.",
    )),
    ("Poznej stupnici.", "Richterova stupnice", ["Richter"], (
        "Její autor ji sestavil roku 1935 pro jižní Kalifornii a počítal ji z výchylky na přístroji Wood-Andersonova typu.",
        "Zavedl ji roku 1935 americký seismolog a dnes ji odborníci nahradili momentovým měřítkem.",
        "Měří se jí síla zemětřesení.",
    )),
    ("Poznej živočicha.", "Ptakopysk", ["ptakopysk podivný"], (
        "První kůži, která doputovala do Evropy, měli tamní přírodovědci za podvrh slepený z několika zvířat.",
        "Žije ve východní Austrálii a na Tasmánii a je to savec, který klade vejce.",
        "Má zobák jako kachna, ocas jako bobr a plovací blány.",
    )),
    ("Poznej chemický prvek.", "Zlato", ["Au"], (
        "Veškeré množství, které kdy lidé vytěžili, by se vešlo do krychle o hraně zhruba dvaadvaceti metrů.",
        "Je to jeden z nejtěžších a nejlépe tvárných kovů; z gramu se dá vytáhnout drát dlouhý přes dva kilometry.",
        "Má protonové číslo 79 a dostávají ho olympijští vítězové.",
    )),
]

# --------------------------------------------------------------------------
# Kultura
# --------------------------------------------------------------------------
BANK["kultura"] = [
    ("V této slavné knize…", "Plechový bubínek", ["Plechový bubínek (kniha)"], (
        "se hlavní hrdina Oskar Matzerath ve třech letech rozhodne, že přestane růst.",
        "dostane právě ke třetím narozeninám předmět z názvu knihy.",
        "poprvé předvedl své prozaické umění spisovatel Günter Grass.",
    )),
    ("Poznej film podle hlášek.", "Vrať se do hrobu", ["Vrať se do hrobu!"], (
        "„Valná většina maturující mládeže již má zodpovědný přístup k životu, existuje však ještě nejméně 50 % těch, kteří zodpovědný přístup nemají.“",
        "„Jsou dány dvě kružnice, z nichž jedné kouká z kapsy bagr.“",
        "„Málková, a što vy dělajetě v svobodnoje vremja zimoj?“ „Zimoj… já něguljaju.“",
    )),
    ("Poznej videohru.", "Pong", [], (
        "Její první automat postavili do baru v kalifornském Sunnyvale a po pár dnech přestal fungovat, protože se přeplnil mincemi.",
        "Byla to první hra vyvinutá společností Atari.",
        "Figurují v ní dvě plošinky, které se snaží odrážet míč pohybující se mezi nimi.",
    )),
    ("Poznej hudební skupinu.", "Pink Floyd", [], (
        "Jejich album z roku 1973 se drželo v americkém žebříčku bez přestávky přes čtrnáct let.",
        "Jejich prvního frontmana museli nahradit poté, co se psychicky zhroutil.",
        "Album The Dark Side of the Moon má na obalu hranol rozkládající světlo.",
    )),
    ("Poznej obraz.", "Křik", ["Výkřik", "The Scream"], (
        "Dvě z jeho verzí byly ukradeny — jedna roku 1994 v den zahájení zimní olympiády, druhá roku 2004 za bílého dne.",
        "Namaloval ho Nor Edvard Munch a existuje ve čtyřech verzích.",
        "Je na něm postava, která si drží hlavu a otevírá ústa na můstku pod krvavým nebem.",
    )),
    ("Poznej film.", "Vetřelec", ["Alien"], (
        "Herci ve slavné scéně u stolu nevěděli, co se stane, a jejich zděšení je skutečné.",
        "Režíroval ho Ridley Scott a hlavní hrdinku Ripleyovou hraje Sigourney Weaverová.",
        "Slogan zněl „ve vesmíru vás nikdo neslyší křičet“ a nejslavnější scéna se odehraje u jídelního stolu.",
    )),
    ("Poznej českou pohádku.", "Tři oříšky pro Popelku", ["Tři oříšky pro Popelku (film)"], (
        "Šlo o československo-východoněmeckou koprodukci a norský dabing z roku 1975 namluvil jediný herec za všechny postavy.",
        "Hlavní roli hraje Libuše Šafránková, prince Pavel Trávníček.",
        "Hrdinka dostane od holoubků kouzelné dárky, na plese ztratí střevíček a umí střílet z kuše.",
    )),
    ("Poznej muzikál.", "Kočky", ["Cats"], (
        "Na Broadwayi se hrálo osmnáct let a byl to tam nejdéle uváděný titul, než ho předstihl jiný kus téhož skladatele.",
        "Napsal ho Andrew Lloyd Webber a nejznámější píseň se jmenuje Memory.",
        "Herci v něm celý večer vystupují v kostýmech koček.",
    )),
    ("Poznej spisovatele.", "Franz Kafka", ["Kafka"], (
        "Podílel se na normách pro bezpečnost práce a bývá mu připisován návrh vylepšení ochranné přilby.",
        "Byl to pražský německy píšící autor, který svému příteli odkázal spálit rukopisy — a ten to neudělal.",
        "Napsal Proces, Zámek a Proměnu, v níž se hrdina probudí jako hmyz.",
    )),
    ("Poznej stavbu.", "Eiffelova věž", ["Eiffelovka"], (
        "V horku se prodlužuje zhruba o patnáct centimetrů a nahoře je malý byt, který si nechal postavit její konstruktér.",
        "Zachránilo ji, že se hodila jako anténa pro radiotelegrafii.",
        "Měří přes tři sta metrů a stojí v Paříži.",
    )),
    ("Poznej film.", "Kmotr", ["The Godfather"], (
        "Kočka, kterou hlavní herec v úvodní scéně drží, se na place jen tak potulovala a do scénáře nepatřila.",
        "Natočil ho roku 1972 Francis Ford Coppola podle románu Maria Puza.",
        "Marlon Brando v něm hraje dona Vita Corleoneho a padne tu věta o nabídce, která se nedá odmítnout.",
    )),
    ("Poznej hudební album.", "Abbey Road", [], (
        "Fotograf měl na pořízení obalu deset minut a policista mezitím zastavil provoz; použil se pátý z šesti snímků.",
        "Druhou stranu tvoří skoro souvislá směs kratších skladeb.",
        "Na obalu přechází čtveřice po přechodu pro chodce před londýnským studiem.",
    )),
    ("Poznej českého malíře.", "Alfons Mucha", ["Mucha"], (
        "Navrhoval první československé bankovky i poštovní známky a dělal to zdarma.",
        "Je nejznámějším představitelem secese a v Paříži navrhoval plakáty, šperky i výstavní pavilon Bosny.",
        "Dvacet let maloval cyklus dvaceti velkoformátových pláten Slovanská epopej.",
    )),
    ("Poznej divadelní hru.", "Hamlet", [], (
        "Je to nejdelší hra svého autora — má skoro čtyři tisíce veršů a v úplném znění se hraje přes čtyři hodiny.",
        "Napsal ji Shakespeare a odehrává se na hradě Elsinor.",
        "Zaznívá v ní věta „Být, či nebýt“ a hlavní hrdina drží lebku šaška Yoricka.",
    )),
    ("Poznej seriál.", "Přátelé", ["Friends"], (
        "Fontána z úvodní znělky nestojí v městě, kde se seriál odehrává, ale ve studiovém areálu v Burbanku.",
        "Vysílal se v letech 1994 až 2004 a odehrává se hlavně v newyorské kavárně Central Perk.",
        "Znělku Iʼll Be There for You zpívají The Rembrandts.",
    )),
    ("Poznej sochu.", "David", ["Davidova socha"], (
        "Roku 1991 jí návštěvník kladivem poškodil nohu; blok mramoru, ze kterého vznikla, ležel před tím čtyřicet let ladem.",
        "Vznikla v letech 1501 až 1504 ve Florencii a dnes stojí v Galerii dell'Accademia.",
        "Autorem je Michelangelo a socha zobrazuje biblického mladíka s prakem.",
    )),
    ("Poznej film.", "Pelíšky", [], (
        "Natáčelo se z velké části v jednom domě v pražských Střešovicích a hudbu k němu složil Petr Ostrouchov.",
        "Režíroval ho Jan Hřebejk; hrají Miroslav Donutil a Jiří Kodet jako sousedi z protilehlých bytů.",
        "Zůstala z něj hláška o lžičkách, které se ve východoněmeckém plastu rozpustí v čaji.",
    )),
    ("Poznej knihu.", "Malý princ", ["Le Petit Prince"], (
        "Autorovy vlastní akvarely v ní nejsou ilustrace navíc — text se na ně přímo odvolává.",
        "Vypravěč potká hrdinu po havárii na Sahaře; hrdina pochází z planetky B 612.",
        "Napsal ji Antoine de Saint-Exupéry a je v ní liška, která učí, že správně vidíme jen srdcem.",
    )),
    ("Poznej hudební nástroj.", "Theremin", ["theremin"], (
        "Jeho vynálezce ho předváděl Leninovi a později v Americe pracoval pro sovětskou rozvědku.",
        "Ovládá se dvěma anténami, které snímají polohu rukou.",
        "Je to jediný nástroj, na který se hraje, aniž by se ho člověk dotkl.",
    )),
    ("Poznej českou kapelu.", "Olympic", [], (
        "Jméno si vypůjčila od psacího stroje a v šedesátých letech hrála i v pražském Rokoku.",
        "Jejím frontmanem je Petr Janda a v šedesátých letech vydala album Želva.",
        "Zpívá se v jejích písních o jasné zprávě a o dárku, který si dáme k Vánocům.",
    )),
]

# --------------------------------------------------------------------------
# Historie
# --------------------------------------------------------------------------
BANK["historie"] = [
    ("Která konference?", "Jaltská konference", ["Jalta"], (
        "Setkání mělo krycí jméno Argonaut a řešily se na něm i podrobnosti vzniku OSN a polská otázka.",
        "Proběhlo mezi 4. a 11. únorem 1945; hlavními představiteli byla trojice Churchill–Roosevelt–Stalin.",
        "Uskutečnilo se v bývalém carském Livadijském paláci v nejznámějším letovisku ukrajinského Krymu.",
    )),
    ("Co bylo předmětem sporu?", "Rukopisy", ["Rukopis královédvorský a zelenohorský", "rukopisný spor"], (
        "Pochybnosti o pravosti určitého díla jako jeden z prvních razantně vyslovil Josef Dobrovský roku 1824.",
        "Osobnostmi na opačné straně barikády byli Václav Hanka a Josef Linda, kteří byli označeni za původce díla.",
        "Později se do sporu vložilo velké množství osobností a vědců, například Jan Gebauer nebo Tomáš Garrigue Masaryk.",
    )),
    ("Poznej bitvu.", "Bitva na Bílé hoře", ["Bílá hora"], (
        "Rozhodlo o ní dopoledne jediného listopadového dne roku 1620 a trvalo to zhruba dvě hodiny.",
        "Po ní následovala poprava sedmadvaceti českých pánů na Staroměstském náměstí.",
        "Znamenala porážku českých stavů a začátek doby, které se říká temno.",
    )),
    ("Poznej událost.", "Sametová revoluce", ["sametová revoluce v Československu"], (
        "Průvod, po jehož rozehnání se všechno rozběhlo, byl původně povolený jako vzpomínka na uzavření vysokých škol roku 1939.",
        "Vzniklo při ní Občanské fórum a lidé na náměstích cinkali klíči.",
        "Skončila pádem komunistického režimu a prezidentem se stal Václav Havel.",
    )),
    ("Poznej stavbu.", "Berlínská zeď", ["berlínská zeď"], (
        "Vedla i vodou a hřbitovy, měřila přes 150 kilometrů a jeden z posledních lidí, kdo u ní zahynul, se pokusil přeletět v balonu.",
        "Nejznámější přechod mezi jejími stranami se jmenoval Checkpoint Charlie.",
        "Padla 9. listopadu 1989 a rozdělovala hlavní město Německa.",
    )),
    ("Poznej panovníka.", "Karel IV.", ["Karel Čtvrtý"], (
        "Sepsal vlastní životopis a byl čtyřikrát ženatý; poslední manželka byla o pětadvacet let mladší.",
        "Byl to český král a římský císař, který vydal roku 1356 Zlatou bulu.",
        "Založil pražskou univerzitu, Nové Město pražské a hrad Karlštejn.",
    )),
    ("Poznej lodní katastrofu.", "Titanic", [], (
        "Vrak se našel až roku 1985 a leží ve dvou kusech téměř čtyři kilometry hluboko.",
        "Potopila se v noci na 15. dubna 1912 na cestě ze Southamptonu do New Yorku.",
        "O katastrofě natočil roku 1997 James Cameron film s Leonardem DiCapriem.",
    )),
    ("Poznej událost.", "Pád Cařihradu", ["dobytí Konstantinopole", "pád Konstantinopole"], (
        "Obránci natáhli přes vjezd do přístavu železný řetěz, útočníci proto přetáhli lodě po souši na namaštěných kládách.",
        "Stalo se to 29. května 1453 a znamenalo konec Byzantské říše.",
        "Město poté přejmenovali a dnes se jmenuje Istanbul.",
    )),
    ("Poznej období.", "Zlatá horečka", ["kalifornská zlatá horečka"], (
        "Nejvíc na ní vydělali obchodníci — jeden z nich uvedl na trh kalhoty se snýtovanými kapsami.",
        "Za rok se do oblasti sjelo přes tři sta tisíc lidí, kterým se říkalo devětačtyřicátníci.",
        "Odehrála se v Kalifornii a připomíná ji přezdívka fotbalového týmu San Francisco 49ers.",
    )),
    ("Poznej vládce.", "Napoleon Bonaparte", ["Napoleon"], (
        "Měřil kolem 168 centimetrů, což byl na svou dobu průměr; pověst o jeho malé postavě vznikla z britské karikatury.",
        "Byl to francouzský císař, který roku 1805 zvítězil u Slavkova na Moravě.",
        "Jeho tažení skončilo porážkou u Waterloo a nechal sestavit občanský zákoník, který nese jeho jméno.",
    )),
    ("Poznej událost.", "Mnichovská dohoda", ["Mnichov"], (
        "Zprostředkoval ji italský vůdce a jednalo se v budově, kterou dnes využívá hudební škola.",
        "Britský premiér Neville Chamberlain po ní mluvil o míru pro naši dobu.",
        "Československo po ní přišlo o pohraničí a v Česku se jí říká zrada.",
    )),
    ("Poznej vynález.", "Knihtisk", [], (
        "Jeho vynálezce prohrál soud se svým věřitelem Fustem a přišel o dílnu i o většinu prvního nákladu.",
        "Zavedl ho kolem roku 1450 v Mohuči Johannes Gutenberg.",
        "První velkou tištěnou knihou byla dvaačtyřicetiřádková bible.",
    )),
    ("Poznej událost.", "Přistání na Měsíci", ["Apollo 11", "první přistání na Měsíci"], (
        "Pojistky proti selhání bylo tak málo, že si posádka nechala předem napsat projev pro případ, že se nevrátí.",
        "Stalo se to 20. července 1969 a modul se jmenoval Eagle.",
        "Neil Armstrong u toho pronesl větu o malém kroku pro člověka.",
    )),
    ("Poznej civilizaci.", "Mayové", ["mayská civilizace"], (
        "Jejich města byla opuštěna už kolem roku 900, tedy dávno před příchodem Španělů, a příčina se dodnes probírá.",
        "Žili na území dnešního Mexika, Guatemaly a Belize; jejich města jsou Tikal nebo Chichén Itzá.",
        "Roku 2012 se hodně mluvilo o konci jejich kalendáře jako o konci světa.",
    )),
    ("Poznej dokument.", "Magna charta", ["Magna Charta Libertatum", "Velká listina svobod"], (
        "Ze zhruba šedesáti článků platí v Anglii dodnes tři a jeden z nich se týká svobod londýnského města.",
        "Papež ji o pár měsíců později prohlásil za neplatnou, ale znovu se potvrzovala po celé století.",
        "Je to anglická listina, kterou dodnes citují jako první krok k omezení moci panovníka.",
    )),
    ("Poznej válku.", "Stoletá válka", [], (
        "Rozhodujícím zbraňovým systémem první poloviny byl dlouhý luk z tisového dřeva, který dokázal probít brnění.",
        "Vedly ji Anglie a Francie o nástupnictví na francouzský trůn.",
        "Objevila se v ní Jana z Arku a Angličané v ní zvítězili u Kresčaku a Azincourtu.",
    )),
    ("Poznej osobnost.", "Kryštof Kolumbus", ["Kolumbus", "Columbus"], (
        "Nabídku na financování odmítli Portugalci i dvakrát Španělé, než mu ji potřetí schválili.",
        "Vyplul roku 1492 se třemi loděmi, z nichž největší se jmenovala Santa María.",
        "Do smrti věřil, že doplul do Indie; podle toho se dodnes říká původním obyvatelům Ameriky.",
    )),
    ("Poznej období.", "Pražské jaro", [], (
        "V červnu toho roku se zrušila cenzura a v novinách vyšel manifest, který podepsalo přes sedmdesát osobností.",
        "V čele stál Alexander Dubček a mluvilo se o socialismu s lidskou tváří.",
        "Skončilo v noci na 21. srpna 1968 vpádem vojsk Varšavské smlouvy.",
    )),
    ("Poznej mořeplavce.", "Fernão de Magalhães", ["Magalhães", "Magellan"], (
        "Z 270 mužů se domů vrátilo osmnáct a při návratu zjistili, že jim v lodním deníku chybí jeden den.",
        "Byl to Portugalec ve španělských službách; z pěti lodí se vrátila jediná, Victoria.",
        "Jeho výprava jako první obeplula svět a nese jeho jméno průliv u jižního cípu Ameriky.",
    )),
    ("Poznej stavbu.", "Velká čínská zeď", ["čínská zeď"], (
        "Malta na její stavbu se místy míchala s rýžovou kaší, což jí dodalo pevnost, kterou má dodnes.",
        "Měří i s odbočkami přes 21 000 kilometrů.",
        "Rozšířená pověra tvrdí, že je vidět z vesmíru pouhým okem — není.",
    )),
]

# --------------------------------------------------------------------------
# Příroda
# --------------------------------------------------------------------------
BANK["priroda"] = [
    ("Poznej zvíře.", "Chameleon", ["chameleoni"], (
        "Barvu mu nedělá barvivo, ale mřížka nanokrystalů v kůži, jejíž rozestupy zvíře mění.",
        "Barvu nemění hlavně kvůli maskování, ale kvůli náladě a teplotě.",
        "Loví dlouhým vystřelovacím jazykem a většina druhů žije na Madagaskaru.",
    )),
    ("Poznej strom.", "Sekvojovec obrovský", ["sekvojovec", "sekvoje"], (
        "Jeho kůra je až půl metru silná a obsahuje tříslovinu, která ho chrání před hmyzem i před ohněm.",
        "Roste jen na západních svazích pohoří Sierra Nevada v Kalifornii.",
        "Největší žijící exemplář se jmenuje General Sherman a je to objemově největší strom světa.",
    )),
    ("Poznej ptáka.", "Kolibřík", ["kolibříci"], (
        "Někteří jeho zástupci přeletí Mexický záliv bez zastávky, tedy přes osm set kilometrů nad vodou.",
        "Žije jen v Americe a je jediným ptákem, který umí letět pozadu.",
        "Je to nejmenší pták světa a křídly kmitá tak rychle, že vydávají bzučivý zvuk.",
    )),
    ("Poznej rostlinu.", "Mucholapka podivná", ["mucholapka", "Dionaea muscipula"], (
        "Jedna past se dokáže zavřít jen několikrát za život a pak odumře; rostlina jich vytváří stále nové.",
        "Roste v přírodě jen na malém území v Severní a Jižní Karolíně.",
        "Je to nejznámější masožravá rostlina a její list vypadá jako zubatá čelist.",
    )),
    ("Poznej živočicha.", "Medvídek koala", ["koala"], (
        "Mládě se po odstavu krmí zvláštní matčinou stolicí, aby dostalo bakterie potřebné k trávení.",
        "Prospí až dvacet hodin denně, protože jeho potrava má málo energie a je jedovatá pro většinu zvířat.",
        "Živí se listy blahovičníku a žije v Austrálii.",
    )),
    ("Poznej houbu.", "Muchomůrka zelená", ["muchomůrka"], (
        "Do Ameriky a Austrálie se dostala až s dovezenými sazenicemi dubů a šíří se tam dodnes.",
        "Má bílé lupeny, prsten a na bázi třeně pochvu — nedá se splést s pravou žampionem, kdo se dívá.",
        "Je to nejjedovatější houba u nás a má na svědomí většinu smrtelných otrav houbami.",
    )),
    ("Poznej rybu.", "Žralok velrybí", ["žralok obrovský"], (
        "Jeho kůže je až patnáct centimetrů silná, nejsilnější na světě, a i oční bulvy má chráněné drobnými zoubky.",
        "Živí se planktonem, který cedí z vody, a člověku nebezpečný není.",
        "Je to největší ryba světa; dorůstá přes dvanáct metrů.",
    )),
    ("Poznej hmyz.", "Včela medonosná", ["včela"], (
        "Aby vzniklo půl kila jejího produktu, musí nálety pokrýt vzdálenost srovnatelnou s několika oblety Země.",
        "Královna klade až dva tisíce vajíček denně a žije několik let, dělnice v létě jen pár týdnů.",
        "Vyrábí med a stavějí šestiúhelníkové plástve.",
    )),
    ("Poznej savce.", "Vorvaň obrovský", ["vorvaň"], (
        "V hlavě má nádrž s voskovitou látkou, kterou ohříváním a chlazením patrně řídí svůj vztlak při ponoru.",
        "Potápí se za potravou přes kilometr hluboko a hledá ji echolokací.",
        "Je hlavní postavou románu Moby Dick a získávala se z něj ambra.",
    )),
    ("Poznej rostlinu.", "Bambus", [], (
        "Jeho stébla obsahují oxid křemičitý, takže tupí nástroje, a duté články se dají použít jako potrubí.",
        "Je to ve skutečnosti tráva, ne strom, a některé druhy kvetou jednou za desítky let — všechny naráz.",
        "Živí se jím panda velká a v Asii se z něj staví lešení.",
    )),
    ("Poznej živočicha.", "Krtek obecný", ["krtek"], (
        "Má dvakrát víc červených krvinek než jiní savci podobné velikosti, aby vydržel v ovzduší chudém na kyslík.",
        "Denně sní potravu o hmotnosti blízké své vlastní a bez jídla vydrží jen pár hodin.",
        "Hrabe pod zemí chodby a vyhazuje hromádky; Zdeněk Miler o něm nakreslil večerníček.",
    )),
    ("Poznej strom.", "Ginkgo biloba", ["jinan dvoulaločný", "ginkgo", "jinan"], (
        "Nemá pravé plody, ale semena, jejichž dužnatý obal páchne po kyselině máselné, takže se sázejí jen samčí stromy.",
        "Je to jediný žijící zástupce celé rostlinné třídy; říká se mu živoucí fosilie.",
        "Má listy ve tvaru vějíře s výřezem uprostřed a jeho výtažek se prodává na paměť.",
    )),
    ("Poznej zvíře.", "Mravenečník velký", ["mravenečník"], (
        "Má nejnižší tělesnou teplotu ze všech placentálních savců, kolem 32 stupňů.",
        "Žije ve Střední a Jižní Americe a chodí po hřbetech předních tlap, aby si nezničil drápy.",
        "Sní denně desetitisíce mravenců a termitů, které vybírá z rozhrabaných hnízd.",
    )),
    ("Poznej přírodní úkaz.", "Zatmění Slunce", ["úplné zatmění Slunce"], (
        "Měsíc se od nás vzdaluje zhruba o čtyři centimetry ročně, takže za stamiliony let už tenhle úkaz nebude možný.",
        "Na jednom a témž místě na Zemi se v celé své podobě opakuje průměrně jednou za zhruba 375 let.",
        "Během něj se objeví koróna a na pár minut se zešeří jako v noci.",
    )),
    ("Poznej zvíře.", "Tučňák císařský", ["tučňák"], (
        "Kolonie se dají počítat z družicových snímků podle skvrn trusu, které jsou vidět z oběžné dráhy.",
        "Je největším ze všech svých příbuzných a měří přes metr.",
        "Jeho hnízdění zachytil oceněný francouzský dokument z roku 2005; žije jen v Antarktidě.",
    )),
    ("Poznej rostlinu.", "Kopřiva dvoudomá", ["kopřiva"], (
        "Živí se na ní housenky babočky paví oko a babočky síťkované, které bez ní nemají kde vyrůst.",
        "Používá se v kuchyni na polévku a její vlákna se dřív spřádala na látku.",
        "Kdo se jí dotkne, dostane pupínky a pálí to; roste u plotů a na hnojišti.",
    )),
    ("Poznej živočicha.", "Chobotnice", ["chobotnice pobřežní", "chobotnice obecná"], (
        "Samice po nakladení vajíček přestane přijímat potravu a po jejich vylíhnutí hyne.",
        "Dvě třetiny jejích neuronů jsou v ramenech, ne v mozku, takže rameno „myslí“ samo.",
        "Má osm ramen s přísavkami a při útěku vypouští oblak inkoustu.",
    )),
    ("Poznej horninu.", "Vápenec", [], (
        "Vznikl většinou ze schránek mořských organismů a jeho přeměnou za tlaku vzniká mramor.",
        "Rozpouští se v dešťové vodě, takže se v něm tvoří jeskyně a krasové útvary.",
        "Je z něj Český kras s Koněpruskými jeskyněmi a pálí se z něj vápno.",
    )),
    ("Poznej zvíře.", "Lenochod", ["lenochodi"], (
        "Má o dva až tři krční obratle víc než ostatní savci, takže otočí hlavu skoro dokola.",
        "Trávení jednoho listu mu trvá i měsíc a na záchod leze dolů zhruba jednou týdně.",
        "Visí hlavou dolů ze stromů ve Střední a Jižní Americe a pohybuje se velmi pomalu.",
    )),
    ("Poznej ptáka.", "Sova pálená", ["sova"], (
        "Nestaví hnízdo a vývržky, které vyvrhuje, se rozebírají ve školách při určování drobných savců.",
        "Náběžná hrana jejích per je roztřepená, takže letí prakticky neslyšně.",
        "Má bílý srdcovitý obličej a hnízdí ve věžích a stodolách.",
    )),
]

# --------------------------------------------------------------------------
# Technika
# --------------------------------------------------------------------------
BANK["technika"] = [
    ("Který slavný konstruktér zbraní?", "John Browning", ["Browning"], (
        "Ve svém oboru je držitelem 128 patentů a první zbraň zkonstruoval ve třinácti letech v otcově dílně.",
        "Jeho nejznámější pistole se u americké armády udržela ve výzbroji přes sedmdesát let.",
        "Výrobek jeho konstrukce použil nechvalně proslulý Gavrilo Princip při útoku na Františka Ferdinanda d'Este.",
    )),
    ("Poznej vynález.", "Rentgen", ["rentgenové záření", "paprsky X"], (
        "Jeho objevitel si na svůj objev nenechal udělit patent, aby ho mohl využívat kdokoli.",
        "První snímek zachycoval ruku manželky objevitele s prstenem.",
        "Za jeho objev udělili roku 1901 vůbec první Nobelovu cenu za fyziku.",
    )),
    ("Poznej dopravní prostředek.", "Zeppelin", ["vzducholoď"], (
        "Plynové komory se šily z blan hovězích střev; na jednu velkou loď jich padly statisíce.",
        "Hélium mu Spojené státy odmítly prodat, takže se plnil vodíkem.",
        "Éru jeho slávy ukončila roku 1937 katastrofa lodi Hindenburg v Lakehurstu.",
    )),
    ("Poznej vynález.", "Suchý zip", ["velcro"], (
        "Průmysl o to osm let nejevil zájem; prosadilo se to teprve tehdy, když si to oblíbila NASA a lyžařské oděvy.",
        "Švýcar George de Mestral si ho nechal patentovat roku 1955.",
        "Tvoří ho dva pásky — jeden s háčky, druhý se smyčkami — a při odtržení to zapraská.",
    )),
    ("Poznej auto.", "Volkswagen Brouk", ["Brouk", "VW Brouk", "Volkswagen Beetle"], (
        "Po válce ho Britové nabídli zdarma i s továrnou, ale jejich vlastní odborníci ho posoudili jako komerčně bezcenný.",
        "Motor má vzadu, chlazený vzduchem, a vyráběl se přes šedesát let prakticky beze změny tvaru.",
        "Ve filmu Herbie má číslo 53 a jeho lidová přezdívka odkazuje k hmyzu.",
    )),
    ("Poznej vynález.", "Mikrovlnná trouba", ["mikrovlnka"], (
        "Kov se do ní nesmí, protože na hranách vzniká elektrický oblouk; hladká lžíce ve vodě přitom problém nedělá.",
        "Ohřívá tak, že rozkmitá molekuly vody v potravině.",
        "První model z roku 1947 vážil přes 300 kilo a stál jako auto; dnes je skoro v každé kuchyni.",
    )),
    ("Poznej stroj.", "Parní stroj", [], (
        "Jeho starší podoba se od začátku 18. století používala hlavně k čerpání vody z dolů a hltala uhlí přímo na místě.",
        "Jeho výkon se dodnes připomíná jednotkou, kterou Watt zavedl, aby ho porovnal s tažnými zvířaty.",
        "Poháněl první lokomotivy a rozjel průmyslovou revoluci.",
    )),
    ("Poznej techniku.", "GPS", ["Global Positioning System"], (
        "Pro civilní použití se signál dlouho úmyslně zhoršoval a přesnost se uvolnila až rozhodnutím z roku 2000.",
        "Původně to byl vojenský systém americké armády, pro civilisty dlouho úmyslně zhoršený.",
        "Určuje polohu a jeho evropskou obdobou je Galileo.",
    )),
    ("Poznej vynález.", "Dynamit", [], (
        "Předčasně otištěný nekrolog, který jeho vynálezce označil za obchodníka se smrtí, ho prý přiměl přepsat závěť.",
        "Jeho vynálezce z výnosů založil nadaci, která uděluje nejznámější světové ceny.",
        "Patentoval ho roku 1867 Alfred Nobel.",
    )),
    ("Poznej dopravní stavbu.", "Metro", ["podzemní dráha"], (
        "V Praze se o něm rozhodovalo desítky let a projekt se nakonec změnil z podpovrchové tramvaje na plnohodnotný systém.",
        "V Praze začalo jezdit roku 1974 a má tři linky označené písmeny.",
        "Je to podzemní kolejová doprava ve velkých městech.",
    )),
    ("Poznej techniku.", "3D tisk", ["aditivní výroba"], (
        "Základní patent na metodu s taveným vláknem vypršel roku 2009 a odstartoval tím celé domácí odvětví.",
        "Nejrozšířenější domácí metoda taví plastovou strunu a klade ji po vrstvách.",
        "Česká firma Průša patří k jeho světovým výrobcům.",
    )),
    ("Poznej vynález.", "Kardiostimulátor", ["pacemaker"], (
        "Vydrží zhruba deset let, pak se vyměňuje celý; podle typu se jeho nositel musí vyhýbat magnetické rezonanci.",
        "Napájí ho baterie, která vydrží zhruba deset let, pak se mění celý přístroj.",
        "Zavádí se pod kůži na hrudi a udržuje pravidelný tep srdce.",
    )),
    ("Poznej vynález.", "Fotoaparát", ["kamera obscura", "fotografie"], (
        "Jeho nejrozšířenější kinofilmový formát 24 × 36 milimetrů vznikl tak, že se zdvojnásobilo políčko filmového pásu.",
        "Princip vychází z temné komory, kterou popisovali už středověcí učenci.",
        "Dnes ho má každý v telefonu a dřív se do něj zakládal film.",
    )),
    ("Poznej českou značku.", "Tatra", [], (
        "Je to jedna z nejstarších dosud vyrábějících automobilek na světě; začínala s kočáry a jmenovala se Nesselsdorfer.",
        "Sídlí v Kopřivnici a vyráběla i luxusní vozy s aerodynamickou zádí.",
        "Jejími vozy jezdí Rallye Dakar a model 815 zná v Česku každý ze stavby.",
    )),
    ("Poznej vynález.", "Kontaktní čočka", ["kontaktní čočky"], (
        "Patent na tuhle československou technologii prodal stát do zahraničí za zlomek pozdějších výnosů.",
        "Materiál se jmenuje HEMA a patent skončil v cizích rukou.",
        "Nosí se místo brýlí přímo na oku.",
    )),
    ("Poznej techniku.", "Šifra Enigma", ["Enigma"], (
        "Přístroj měl kolem sto padesáti kvintilionů možných nastavení, ale jednu vlastnost, která počet reálných možností drasticky srazila.",
        "Klíčovou slabinou bylo, že písmeno se nikdy nezašifrovalo samo na sebe.",
        "Používal ji za druhé světové války Wehrmacht a luštil ji Alan Turing v Bletchley Parku.",
    )),
    ("Poznej stavbu.", "Suezský průplav", ["Suez"], (
        "Po znárodnění roku 1956 kvůli němu vypukla válka a osm let byl úplně uzavřený; uvízlo v něm čtrnáct lodí s posádkami.",
        "Otevřel se roku 1869 podle projektu Ferdinanda de Lesseps.",
        "Roku 2021 ho na šest dní zablokovala loď Ever Given.",
    )),
    ("Poznej vynález.", "Žárovka", [], (
        "V kalifornském Livermoru svítí od roku 1901 kus, který se stal kuriozitou a má vlastní webovou kameru.",
        "Thomas Edison ji nevynalezl jako první, ale jako první ji udělal prakticky použitelnou.",
        "Dnes ji nahradily úspornější LED diody.",
    )),
    ("Poznej techniku.", "Bluetooth", [], (
        "Pracuje v pásmu 2,4 GHz a přeskakuje mezi kanály stokrát za sekundu, aby se vyhnul rušení.",
        "Jeho značka je runová ligatura iniciál toho krále.",
        "Bezdrátově spojuje sluchátka, reproduktory a telefony na krátkou vzdálenost.",
    )),
    ("Poznej stroj.", "Jaderný reaktor", ["atomový reaktor"], (
        "V Gabonu se našlo místo, kde něco takového běželo samo od sebe před dvěma miliardami let.",
        "Štěpení zpomalují regulační tyče, obvykle z bóru nebo kadmia.",
        "V Česku jsou dvě elektrárny s takovými stroji — Dukovany a Temelín.",
    )),
]

# --------------------------------------------------------------------------
# Sport
# --------------------------------------------------------------------------
BANK["sport"] = [
    ("V této atletické disciplíně…", "Maraton", ["maratonský běh", "běh na 42 195 m"], (
        "dokázal obhájit olympijský titul Waldemar Cierpinski.",
        "dokázal obhájit olympijský titul Abebe Bikila.",
        "nedokázal obhájit olympijský titul Emil Zátopek — vyhrál ho jedinkrát, v Helsinkách 1952.",
    )),
    ("Poznej sportovní klub.", "Real Madrid", ["Real"], (
        "Za občanské války mu zahynul předseda a klub málem zanikl; obnovoval se od nuly roku 1939.",
        "Hraje na stadionu Santiago Bernabéu a jeho největší rival je z hlavního města Katalánska.",
        "Je to nejúspěšnější klub v historii Ligy mistrů a hrál za něj Cristiano Ronaldo.",
    )),
    ("Poznej sport.", "Curling", [], (
        "Sport má vlastní pravidlo cti — hráč sám přizná, když se kamene dotkne, i když to nikdo neviděl.",
        "Hráči před kamenem zametají led, aby upravili jeho dráhu a rychlost.",
        "Je to zimní olympijský sport a v Česku ho zpopularizovaly hlavně smíšené páry.",
    )),
    ("Poznej sportovce.", "Jaromír Jágr", ["Jágr"], (
        "Do zámoří odešel roku 1990 jako první Čech, který k tomu nepotřeboval emigraci.",
        "Je odchovancem Kladna, jehož klub později koupil.",
        "Je nejproduktivnějším Evropanem v historii NHL a získal Stanley Cup s Pittsburghem.",
    )),
    ("Poznej sportovní akci.", "Tour de France", [], (
        "Za války se nekonala a v padesátých letech se v ní jezdilo za národní týmy, ne za obchodní stáje.",
        "Proto má vedoucí závodník žlutý dres; puntíkovaný patří nejlepšímu vrchaři.",
        "Je to nejslavnější cyklistický závod a končí na pařížské Champs-Élysées.",
    )),
    ("Poznej sport.", "Baseball", [], (
        "Míč má přesně 108 dvojitých stehů a musel se dlouho ručně sešívat.",
        "Hřiště má tvar výseče se čtyřmi metami a zápas má devět směn.",
        "Nejslavnější soutěž se hraje v USA a Japonsku a její vyvrcholení nese název Světová série.",
    )),
    ("Poznej sportovkyni.", "Martina Navrátilová", ["Navrátilová"], (
        "Vyhrála přes sto sedmdesát turnajů ve dvouhře, víc než kdokoli v otevřené éře, muže nevyjímaje.",
        "Získala devět wimbledonských titulů ve dvouhře, nejvíc v historii.",
        "Je to česko-americká tenistka, jejíž největší soupeřkou byla Chris Evertová.",
    )),
    ("Poznej fotbalistu.", "Josef Masopust", ["Masopust"], (
        "Po kariéře trénoval mimo jiné v Indonésii a v Zambii.",
        "Hrál za Duklu Praha a vstřelil první gól ve finále mistrovství světa v Chile.",
        "Byl vyhlášen českým fotbalistou století a nese jeho jméno i typický útočný manévr se dvěma přihrávkami.",
    )),
    ("Poznej sport.", "Biatlon", [], (
        "Vznikl z vojenských hlídkových závodů a na olympiádě se v původní podobě objevil poprvé roku 1924 jako ukázka.",
        "Střílí se vleže i vstoje na terče vzdálené padesát metrů.",
        "Spojuje běh na lyžích a střelbu z malorážky; v Česku ho proslavila Gabriela Soukalová.",
    )),
    ("Poznej stadion.", "Wembley", ["Wembley Stadium"], (
        "Pod trávníkem vede vytápění a celý povrch se vyměňuje zhruba desetkrát za rok kvůli koncertům.",
        "Starou podobu poznal každý podle dvou bílých věží.",
        "Je to národní fotbalový stadion Anglie v Londýně.",
    )),
    ("Poznej sportovce.", "Usain Bolt", ["Bolt"], (
        "Jako kluk hrál kriket jako nadhazovač a k atletice ho přivedl trenér, kterému se zalíbila jeho rychlost mezi metami.",
        "Pochází z Jamajky a jeho oslavné gesto připomíná lučištníka.",
        "Drží světové rekordy na 100 i 200 metrů z Berlína 2009.",
    )),
    ("Poznej sport.", "Šerm", [], (
        "Zásah se od roku 1936 vyhodnocuje elektricky; do té doby o něm rozhodovali čtyři pomocní rozhodčí okem.",
        "Ty zbraně se jmenují fleret, kord a šavle.",
        "Je jedním z pěti sportů, které byly na programu všech novodobých olympiád.",
    )),
    ("Poznej sportovní trofej.", "Stanley Cup", ["Stanleyův pohár"], (
        "Několikrát se ztratila i utopila; jednou ji hráči nechali na kraji silnice a jindy skončila v bazénu.",
        "Darovaný roku 1892 generálním guvernérem Kanady a je to nejstarší trofej severoamerického profesionálního sportu.",
        "Získává ji vítěz play off NHL.",
    )),
    ("Poznej olympijský sport.", "Moderní pětiboj", ["pětiboj"], (
        "Zakladatel novodobých olympijských her ho sestavil podle představy o schopnostech kurýra za nepřátelskou linií.",
        "Jednou z pěti částí bývala jízda na neznámém koni, kterou po sporech v Tokiu 2020 nahradila překážková dráha.",
        "Zbylé části jsou šerm, plavání, běh a střelba — a Češi v něm mají olympijské zlato Davida Svobody.",
    )),
    ("Poznej sportovce.", "Muhammad Ali", ["Ali", "Cassius Clay"], (
        "Zlatou medaili z olympiády v Římě roku 1960 podle vlastního vyprávění hodil do řeky.",
        "Zápas v Kinshase roku 1974 proti Georgi Foremanovi vešel do dějin jako Rachot v džungli.",
        "Byl to boxer, který o sobě říkal, že se vznáší jako motýl a bodá jako včela.",
    )),
    ("Poznej sport.", "Ragby", ["rugby"], (
        "Nejstarší mezinárodní trofej na světě v kolektivním sportu se v něm hraje mezi Anglií a Skotskem od roku 1879.",
        "Podle legendy vzniklo, když žák anglické školy popadl při fotbale míč do rukou a rozběhl se.",
        "Nejslavnější soutěž je Světový pohár a hraje se s oválným míčem.",
    )),
    ("Poznej fotbalový turnaj.", "Mistrovství světa ve fotbale", ["MS ve fotbale", "světový pohár"], (
        "V prvním finále se hrálo každý poločas jiným míčem, protože se soupeři nedohodli, čí použít.",
        "Trofej ve své první podobě jednou ukradli a našel ji pes jménem Pickles.",
        "Koná se každé čtyři roky a nejvíc titulů má Brazílie.",
    )),
    ("Poznej sportovkyni.", "Ester Ledecká", ["Ledecká"], (
        "Její dědeček byl hokejista a otec hudebník; sama se dlouho odmítala rozhodnout mezi dvěma sporty.",
        "Je vnučkou hokejisty Jana Klapáče a dcerou známého českého zpěváka a kytaristy.",
        "Na jedné olympiádě vyhrála super-G na lyžích i paralelní obří slalom na snowboardu.",
    )),
    ("Poznej sport.", "Judo", [], (
        "Pásy se v něm barevně odlišují teprve od dvacátých let 20. století; původně byly jen bílé a černé.",
        "Vítězství se dá získat naráz technikou zvanou ippon.",
        "Závodí se v kimonu a v Česku ho proslavil olympijský vítěz Lukáš Krpálek.",
    )),
    ("Poznej hokejový turnaj.", "Nagano 1998", ["olympiáda v Naganu", "Nagano"], (
        "Turnaj se hrál na širším evropském kluzišti, na které většina zámořských hráčů nebyla zvyklá.",
        "Ve finále padl jediný gól, ve čtvrtfinále rozhodly nájezdy proti Kanadě.",
        "Češi na něm vyhráli hokejové zlato a brankářem byl Dominik Hašek.",
    )),
]

# --------------------------------------------------------------------------
# Jazyk
# --------------------------------------------------------------------------
BANK["jazyk"] = [
    ("Doplňte společný přívlastek.", "turecký", ["turecké", "turecká"], (
        "Prohlubeň klínové kosti lebky, ve které je uložena hypofýza, se jmenuje jeho přívlastkem a sedlem.",
        "Klavírní sonáta A dur Wolfganga Amadea Mozarta se tak jmenuje podle svého třetího věty.",
        "Určitá káva se připravuje z jemně mleté kávy zalité vroucí vodou přímo v šálku.",
    )),
    ("Poznej příjmení.", "Wright", [], (
        "Měl ho klávesista skupiny Pink Floyd, kterého ostatní členové roku 1979 vyhodili a pak najali jako placeného hráče.",
        "Nosil ho i slavný americký architekt Frank Lloyd.",
        "Proslavili ho také bratři Wilbur a Orville, průkopníci letectví.",
    )),
    ("Poznej jazyk.", "Baskičtina", ["baskicky", "baskický jazyk"], (
        "Za Francova režimu se s ním nesmělo na úřadech ani ve školách a zachránily ho podzemní školy zvané ikastolak.",
        "Mluví se jím na pomezí Španělska a Francie kolem Biskajského zálivu.",
        "Sami mu mluvčí říkají euskara a hovoří jím zhruba tři čtvrtě milionu lidí.",
    )),
    ("Poznej slovo podle původu.", "Robot", [], (
        "Do angličtiny to slovo přeložil roku 1923 Paul Selver a jeho překlad hry cestou vypustil celou jednu postavu.",
        "Do světových jazyků ho dostala divadelní hra z roku 1920.",
        "Autorovi ho poradil jeho bratr Josef a dnes tak říkáme strojům, které pracují místo lidí.",
    )),
    ("Poznej písmo.", "Hlaholice", [], (
        "Má znaků víc než čtyřicet a v jedné z jejích pozdějších podob se psalo v Chorvatsku ještě ve 20. století.",
        "Její tvary se odvozují od řecké minuskule a znaky mají i číselnou hodnotu.",
        "Používali ji na Velké Moravě Cyril a Metoděj; později ji vytlačila cyrilice.",
    )),
    ("Poznej jazykový jev.", "Palindrom", [], (
        "Nejstarší doložený příklad se našel jako nápis v Herculaneu a čte se z každé strany i po sloupcích.",
        "Latinský příklad zní „sator arepo tenet opera rotas“ a dá se číst i po sloupcích.",
        "Je to slovo nebo věta, která zní stejně zepředu i zezadu — třeba „kobyla má malý bok“.",
    )),
    ("Poznej pravopisný jev.", "Vyjmenovaná slova", ["vyjmenovaná slova po B"], (
        "Souvisejí s hláskou, která v češtině zanikla kolem 14. století, ale pravopis si ji podržel.",
        "Souvisejí s tím, že se v dávné výslovnosti lišila dvě písmena, která dnes zní stejně.",
        "Školáci se je učí zpaměti v řadách jako „být, bydlit, obyvatel, byt, příbytek…“.",
    )),
    ("Poznej slovo.", "Ostrov", [], (
        "Ve Středočeském i Karlovarském kraji je město s tímhle jménem a v obou případech leží u vody.",
        "Ve Středočeském kraji i v Karlovarském kraji je město s tímhle jménem.",
        "Je to souš ze všech stran obklopená vodou.",
    )),
    ("Poznej jazyk.", "Esperanto", [], (
        "Jeho autor byl oční lékař z Bialystoku a jazyk sestavil proto, že ve městě žilo vedle sebe několik znesvářených národností.",
        "Podstatná jména v něm končí na -o, přídavná na -a a nemá výjimky.",
        "Je to nejrozšířenější umělý jazyk a vytvořil ho Ludvík Lazar Zamenhof.",
    )),
    ("Poznej rčení.", "Mít máslo na hlavě", ["máslo na hlavě"], (
        "Obdobu má i němčina a maďarština, což naznačuje, že se to k nám dostalo z jednoho společného zdroje.",
        "Znamená to nést vlastní vinu, kterou by si člověk měl uvědomit dřív, než ukáže prstem na někoho jiného.",
        "Říká se to o někom, kdo obviňuje ostatní z něčeho, co má na svědomí sám.",
    )),
    ("Poznej termín.", "Pangram", [], (
        "Sazeči je používají odjakživa jako vzorek písma a v počítačích se podle nich zkoušelo, jestli je font úplný.",
        "Český příklad zní „příliš žluťoučký kůň úpěl ďábelské ódy“.",
        "Je to věta, ve které se objeví všechna písmena abecedy.",
    )),
    ("Poznej abecedu.", "Braillovo písmo", ["Braille", "braillovo písmo"], (
        "Jeho autor přišel o zrak v dětství, když si hrál v otcově sedlářské dílně s nástrojem na kůži.",
        "Autor ho vytvořil ve svých patnácti letech, sám nevidomý po úrazu z dětství.",
        "Je to písmo pro nevidomé, sestavené ze šesti vyvýšených bodů.",
    )),
    ("Poznej slovo podle původu.", "Pistole", [], (
        "Podle jednoho výkladu za jeho jméno může husitské město v jižních Čechách, podle jiného italská mince.",
        "Do němčiny se dostalo skoro beze změny a odtud se rozšířilo do celého světa.",
        "Je to krátká ruční palná zbraň.",
    )),
    ("Poznej jazyk.", "Latina", [], (
        "Ve středověku se z ní vyvinula podoba, které se říká kuchyňská, a v ní se psaly i české listiny.",
        "Vznikla v kraji Latium a rozšířila ji říše, jejímž hlavním městem byl Řím.",
        "Vycházejí z ní románské jazyky a používá se v biologickém a lékařském názvosloví.",
    )),
    ("Poznej termín.", "Anagram", ["přesmyčka"], (
        "Galileo i Huygens jím zašifrovali své objevy, aby si zajistili prvenství a přitom je ještě neprozradili.",
        "V češtině se mu říká přesmyčka a je základem hry Věž.",
        "Vznikne přeházením písmen jednoho slova tak, že vyjde slovo jiné.",
    )),
    ("Poznej slovo.", "Tunel", [], (
        "Nejdelší silniční na světě měří přes 24 kilometrů a vede v Norsku mezi Lærdalem a Aurlandem.",
        "V češtině devadesátých let se z něj stalo sloveso pro vyvádění peněz z firmy.",
        "Původně a hlavně je to podzemní chodba pro dopravu.",
    )),
    ("Poznej jazyk.", "Islandština", ["islandsky"], (
        "Zvláštní výbor v té zemi schvaluje, jaká jména smějí rodiče dát dětem, aby se dala skloňovat.",
        "Nová slova se v ní zásadně netvoří přejímáním, ale skládáním domácích kořenů.",
        "Mluví se jí na severoatlantském ostrově s hlavním městem Reykjavík.",
    )),
    ("Poznej jev.", "Homonymum", [], (
        "Jazyky s nepravopisným písmem jich mívají mnohem víc; v čínštině na tom stojí celá řada slovních hříček.",
        "Klasický český příklad je slovo „kolej“ nebo „raketa“.",
        "Jsou to slova, která znějí stejně, ale znamenají něco úplně jiného.",
    )),
    ("Poznej jazyk.", "Sanskrt", [], (
        "Objev jeho příbuznosti s evropskými jazyky ohlásil roku 1786 v Kalkatě soudce William Jones.",
        "Objev jeho podobnosti s řečtinou a latinou v 18. století založil srovnávací jazykovědu.",
        "Je to posvátný jazyk hinduismu, ve kterém je napsána Bhagavadgíta.",
    )),
    ("Poznej termín.", "Idiom", ["frazém", "ustálené spojení"], (
        "Jazykovědci jich v běžné češtině napočítali desítky tisíc a mají pro ně vlastní slovník.",
        "Bývá to nejtěžší část jazyka pro cizince a strojový překlad ho často zkazí.",
        "Patří sem třeba „házet flintu do žita“ nebo „mít hlavu v oblacích“.",
    )),
]

# --------------------------------------------------------------------------
# Společnost
# --------------------------------------------------------------------------
BANK["spolecnost"] = [
    ("Poznej organizaci.", "Červený kříž", ["Mezinárodní červený kříž"], (
        "Jeho zakladatel skončil v chudobinci a Nobelovu cenu, kterou pak dostal, celou rozdal.",
        "Jeho znak je obrácená vlajka Švýcarska a v muslimských zemích se používá jiný symbol.",
        "Stará se o raněné ve válce a jeho sídlo je v Ženevě.",
    )),
    ("Poznej dokument.", "Všeobecná deklarace lidských práv", ["deklarace lidských práv"], (
        "Osm států se při hlasování zdrželo a mezi nimi bylo i Československo.",
        "Na jejím vzniku měla velký podíl Eleanor Rooseveltová.",
        "Je to nejpřekládanější dokument světa a začíná větou, že všichni lidé se rodí svobodní a rovní.",
    )),
    ("Poznej cenu.", "Nobelova cena", [], (
        "Matematika mezi jejími obory chybí a historky o tom, proč, jsou podle badatelů výmysl.",
        "Tu za mír uděluje jako jedinou norský výbor, ostatní švédské instituce.",
        "Předává se každý rok 10. prosince, v den úmrtí zakladatele.",
    )),
    ("Poznej svátek.", "Velikonoce", [], (
        "Východní a západní křesťané je slaví v různé dny, protože počítají podle různých kalendářů.",
        "Křesťané při nich slaví zmrtvýchvstání a předchází jim čtyřicetidenní půst.",
        "V Česku k nim patří pomlázka, kraslice a Velký pátek.",
    )),
    ("Poznej instituci.", "Evropský parlament", [], (
        "Stěhování mezi dvěma sídly stojí ročně stovky milionů eur a zakotvila ho mezistátní smlouva, takže se nedá jen tak zrušit.",
        "Ta města jsou Brusel a Štrasburk, sekretariát sídlí v Lucemburku.",
        "Jeho poslance volí občané členských států unie přímo, jednou za pět let.",
    )),
    ("Poznej zvyk.", "Podávání ruky", ["potřesení rukou", "handshake"], (
        "Ve starém Řecku se jím stvrzovala dohoda a zobrazuje ho i řada náhrobních reliéfů.",
        "V Japonsku ho z velké části nahrazuje úklona, v arabském světě má vlastní pravidla.",
        "Je to nejběžnější evropský pozdrav při setkání i uzavření dohody.",
    )),
    ("Poznej pojem.", "Demokracie", [], (
        "V Athénách se většina úřadů neobsazovala volbou, ale losem, protože volba se považovala za výhodu pro bohaté.",
        "Její přímou podobu praktikovaly Athény v 5. století př. n. l., ale bez žen a otroků.",
        "Dnes se jí říká vláda lidu a jejím základem jsou svobodné volby.",
    )),
    ("Poznej měnu.", "Euro", [], (
        "Rub mincí si každý stát navrhuje sám, ale platí se jimi všude; jeden ministát na ně dává portrét svého knížete.",
        "Na bankovkách jsou schválně smyšlené stavby, aby nezvýhodnily žádnou zemi.",
        "Platí jím většina států Evropské unie a jeho symbol vychází z řeckého písmene epsilon.",
    )),
    ("Poznej instituci.", "UNESCO", [], (
        "Spojené státy z ní vystoupily už podruhé a jednou se zase vrátily; důvodem byly spory o rozpočet a politiku.",
        "Sídlí v Paříži a vzniklo roku 1945 s myšlenkou, že mír se buduje v myslích lidí.",
        "Vede seznam světového dědictví, na kterém je z Česka Praha, Český Krumlov nebo Kutná Hora.",
    )),
    ("Poznej pojem.", "Inflace", [], (
        "Podle jednoho z výkladů ji pohání očekávání samotných lidí, takže se do měření zahrnují i průzkumy nálad.",
        "Její extrémní podoba postihla Německo roku 1923, kdy se ceny zdvojnásobovaly každé dva dny.",
        "Je to růst cenové hladiny — za stejné peníze si člověk koupí míň než dřív.",
    )),
    ("Poznej svátek.", "Svátek práce", ["1. máj", "První máj"], (
        "Ve Spojených státech, kde má původ, se dnes slaví jiný svátek práce a v jiný den.",
        "V Česku je zároveň dnem, kdy se líbá pod rozkvetlou třešní.",
        "Připadá na začátek května a v Česku je to státní svátek.",
    )),
    ("Poznej pojem.", "Gramotnost", [], (
        "V českých zemích byla díky povinné školní docházce od roku 1774 dlouho jedna z nejvyšších v Evropě.",
        "Světový den se jí věnuje 8. září a UNESCO ji sleduje jako klíčový ukazatel rozvoje.",
        "Základem je umět číst a psát.",
    )),
    ("Poznej organizaci.", "NATO", ["Severoatlantická aliance"], (
        "Francie z jejího vojenského velení na čtyřicet let vystoupila a vrátila se až roku 2009.",
        "Slavný článek 5 říká, že útok na jednoho je útokem na všechny; poprvé se uplatnil po 11. září 2001.",
        "Česko do ní vstoupilo roku 1999 a jejím sídlem je Brusel.",
    )),
    ("Poznej pojem.", "Volební právo žen", ["ženské volební právo"], (
        "V Británii se za něj bojovalo tak ostře, že se demonstrantky přivazovaly k zábradlí a jedna z nich zahynula na dostihové dráze.",
        "V Československu platilo od ústavy roku 1920, ve Švýcarsku na federální úrovni až od roku 1971.",
        "Znamená, že ženy smějí volit stejně jako muži.",
    )),
    ("Poznej pojem.", "Sčítání lidu", ["cenzus"], (
        "Roku 2011 se v Česku k jedné z nabízených kolonek přihlásilo přes patnáct tisíc lidí jako k rytířům Jediů.",
        "V Česku ho provádí Český statistický úřad a koná se jednou za deset let.",
        "Zjišťuje, kolik lidí kde žije a jak.",
    )),
    ("Poznej tradici.", "Masopust", ["karneval"], (
        "Jeho průvody mívají ustálené masky — medvěda, kobylu, ženušku — a v některých vsích se pořadí i trasa nesmí měnit.",
        "V Hlinecku je zapsán na seznamu nehmotného dědictví UNESCO.",
        "Je to období zabijaček, průvodů v maskách a veselí před postem.",
    )),
    ("Poznej pojem.", "Sociální síť", ["sociální sítě"], (
        "Sociolog Stanley Milgram v šedesátých letech pokusem s dopisy ukázal, jak krátké mezi lidmi bývají řetězy známostí.",
        "První velkou internetovou podobu měla SixDegrees.com z roku 1997, pojmenovaná podle teorie šesti kroků.",
        "Dnes si pod tím každý představí Facebook nebo Instagram.",
    )),
    ("Poznej dokument.", "Ústava České republiky", ["česká ústava", "Ústava ČR"], (
        "Nejčastěji se měnila v souvislosti se vstupem do mezinárodních struktur a s přímou volbou hlavy státu.",
        "Skládá se z preambule a osmi hlav a mluví o svobodných a odpovědných občanech.",
        "Platí od 1. ledna 1993 a stojí na jejím vrcholu Ústavní soud v Brně.",
    )),
    ("Poznej instituci.", "Vatikán", ["Vatikánský městský stát", "Svatý stolec"], (
        "Má vlastní železniční stanici s nejkratší mezinárodní tratí na světě a poštu, kterou hojně využívají i sousedé.",
        "Střeží ho Švýcarská garda a jeho jediným úředním jazykem je latina.",
        "Sídlí tu papež a stojí zde Sixtinská kaple.",
    )),
    ("Poznej pojem.", "Menšina", ["národnostní menšina"], (
        "Rámcová úmluva Rady Evropy z roku 1995 nechává na každém státu, koho za ni uzná — a některé neuznávají žádnou.",
        "V Česku má zákonem uznaných čtrnáct takových skupin a zastupuje je vládní rada.",
        "Je to skupina, která se v zemi odlišuje od většiny a má právo na svá práva.",
    )),
]

# ==========================================================================
# Druhá dávka
# ==========================================================================

BANK["osobnost"] += [
    ("Poznej známou osobnost.", "Jan Werich", ["Werich"], (
        "Poslední léta bydlel na Kampě v domě, kde je dnes muzeum, a psal do Plamene.",
        "S Jiřím Voskovcem tvořil dvojici Osvobozeného divadla a za války spolu emigrovali do USA.",
        "Namluvil Chocholouška v Císařově pekaři a hrál medvídka v Byl jednou jeden král.",
    )),
    ("Poznej známou osobnost.", "Sigmund Freud", ["Freud"], (
        "Celý dospělý život vykouřil kolem dvaceti doutníků denně a přes třicet operací čelisti ho toho neodnaučilo.",
        "Byl to rakouský neurolog, který zavedl pojmy jako ono, já a nadjá.",
        "Zakladatel psychoanalýzy; pacienty nechával ležet na pohovce a vykládal jim sny.",
    )),
    ("Poznej známou osobnost.", "Amelia Earhartová", ["Earhartová", "Amelia Earhart"], (
        "Před létáním pracovala jako zdravotní sestra a studovala medicínu.",
        "Byla to americká letkyně, která jako první žena přeletěla Atlantik sama.",
        "Roku 1937 se ztratila nad Tichým oceánem při pokusu obletět svět a nenašla se dodnes.",
    )),
    ("Poznej známou osobnost.", "Emil Holub", ["Holub"], (
        "Vystudoval medicínu v Praze a v Africe se živil jako lékař diamantových kopáčů.",
        "Byl to český cestovatel, který přivezl domů tisíce afrických předmětů a nikdo je nechtěl vystavovat.",
        "Prozkoumal Viktoriiny vodopády a jeho sbírky skončily roztroušené po muzeích Evropy.",
    )),
    ("Poznej známou osobnost.", "Ludwig Wittgenstein", ["Wittgenstein"], (
        "Pocházel z nejbohatší vídeňské rodiny a celé dědictví rozdal; pak učil na vesnické škole.",
        "Byl to rakouský filozof, který v Cambridgi působil vedle Bertranda Russella.",
        "Jeho Tractatus končí větou o tom, o čem nelze mluvit, o tom se musí mlčet.",
    )),
    ("Poznej známou osobnost.", "Jan Palach", ["Palach"], (
        "Byl studentem Filozofické fakulty a předtím studoval ekonomii ve Vysoké škole ekonomické.",
        "Jeho pohřeb se v lednu 1969 změnil v tichou demonstraci proti okupaci.",
        "Zapálil se na Václavském náměstí a jeho jméno dnes nese náměstí u Rudolfina.",
    )),
    ("Poznej známou osobnost.", "Rosa Parksová", ["Rosa Parks", "Parksová"], (
        "Pracovala jako švadlena a byla tajemnicí místní pobočky organizace NAACP.",
        "Její čin roku 1955 v Montgomery odstartoval bojkot, který trval přes rok.",
        "Odmítla v autobuse uvolnit místo bílému cestujícímu a stala se symbolem boje proti segregaci.",
    )),
    ("Poznej známou osobnost.", "Jaroslav Seifert", ["Seifert"], (
        "V roce 1929 ho vyloučili z komunistické strany za podpis manifestu proti novému vedení.",
        "Byl to český básník, který podepsal Chartu 77 a cenu si kvůli nemoci nepřevzal osobně.",
        "Roku 1984 získal jako jediný Čech Nobelovu cenu za literaturu.",
    )),
    ("Poznej známou osobnost.", "Salvador Dalí", ["Dalí"], (
        "Navrhl logo pro známé lízátko a spolupracoval s Waltem Disneym na krátkém filmu.",
        "Byl to katalánský malíř, který si nechal narůst charakteristický nakroucený knír.",
        "Namaloval tekoucí hodinky v obraze Persistence paměti.",
    )),
    ("Poznej známou osobnost.", "Milada Horáková", ["Horáková"], (
        "Za války ji zatklo gestapo a přežila Terezín i věznění v Německu.",
        "Byla to česká právnička a poslankyně, popravená v politickém procesu roku 1950.",
        "Za její život se marně přimlouvali Einstein i Churchill; jméno má dnes pražská třída.",
    )),
    ("Poznej známou osobnost.", "Marco Polo", ["Polo"], (
        "Své vyprávění nadiktoval spoluvězni v janovském žaláři, kde skončil po námořní bitvě.",
        "Byl to benátský kupec, který strávil sedmnáct let ve službách Kublajchána.",
        "Jeho cestopis se pro množství neuvěřitelných čísel přezdíval Milion.",
    )),
    ("Poznej známou osobnost.", "Rudolf II.", ["Rudolf Druhý"], (
        "Vychovali ho na španělském dvoře a nikdy se neoženil, ačkoli měl několik nemanželských dětí.",
        "Přenesl své sídlo do Prahy a shromáždil tu obrovskou sbírku umění a kuriozit.",
        "Zval si alchymisty a hvězdáře; sloužili u něj Tycho Brahe i Johannes Kepler.",
    )),
    ("Poznej známou osobnost.", "Anne Franková", ["Anne Frank", "Franková"], (
        "K narozeninám roku 1942 dostala sešit s červenobílým kostkovaným přebalem.",
        "Byla to židovská dívka, která se s rodinou dva roky skrývala v zadním traktu amsterodamského domu.",
        "Zemřela v Bergen-Belsenu a její deník vydal po válce otec, jediný přeživší z rodiny.",
    )),
    ("Poznej známou osobnost.", "Zdeněk Miler", ["Miler"], (
        "Studoval na uměleckoprůmyslové škole a za války se dostal k animaci ve Zlíně.",
        "Byl to český výtvarník a režisér kreslených filmů, který pracoval ve studiu Bratři v triku.",
        "Vymyslel postavičku, která se poprvé objevila roku 1957 ve filmu Jak krtek ke kalhotkám přišel.",
    )),
    ("Poznej známou osobnost.", "Michail Gorbačov", ["Gorbačov"], (
        "Vystudoval práva a jako mladý pracoval na kombajnu, za což dostal řád Rudého praporu práce.",
        "Byl to poslední vůdce Sovětského svazu; roku 1990 dostal Nobelovu cenu míru.",
        "Zavedl perestrojku a glasnosť a za jeho vlády padla berlínská zeď.",
    )),
    ("Poznej známou osobnost.", "Jane Goodallová", ["Jane Goodall", "Goodallová"], (
        "Do Afriky odjela bez vysokoškolského vzdělání jako sekretářka paleontologa Louise Leakeyho.",
        "Britská badatelka, která svým zvířatům dávala jména místo čísel, což vědci tehdy odsuzovali.",
        "V Gombe pozorovala šimpanze a zjistila, že si vyrábějí nástroje.",
    )),
    ("Poznej známou osobnost.", "Karel Gott", ["Gott"], (
        "Vyučil se elektromontérem a na konzervatoř se dostal až napodruhé.",
        "Byl to nejúspěšnější český zpěvák, čtyřicetkrát Zlatý slavík.",
        "V Německu ho proslavila znělka k seriálu o včelce Máje.",
    )),
    ("Poznej známou osobnost.", "Alexander Fleming", ["Fleming"], (
        "Před medicínou pracoval čtyři roky v přepravní kanceláři a za války sloužil v polním špitálu.",
        "Byl to skotský bakteriolog, který roku 1945 sdílel Nobelovu cenu s Floreyem a Chainem.",
        "Objevil, že plíseň na jeho Petriho misce zabíjí bakterie — tak vznikl penicilin.",
    )),
    ("Poznej známou osobnost.", "Jan Evangelista Purkyně", ["Purkyně"], (
        "Než se dal na medicínu, byl piaristickým novicem a živil se jako domácí učitel.",
        "Byl to český fyziolog, který v Breslau založil první fyziologický ústav na světě.",
        "Nesou jeho jméno buňky v mozečku i jev, kdy se za šera mění vnímání barev.",
    )),
    ("Poznej známou osobnost.", "Vincenc Priessnitz", ["Priessnitz"], (
        "Jako chlapec ho přejel povoz a zlomená žebra si prý srovnal sám s pomocí vody a dýchání.",
        "Byl to selský syn ze Slezska, kterého lékaři žalovali za nedovolené léčitelství — a soud vyhrál.",
        "Založil v Jeseníku první vodoléčebný ústav na světě a nese jeho jméno obklad.",
    )),
]

BANK["zemepis"] += [
    ("Poznej stát.", "Japonsko", [], (
        "Jeho nejvyšší hora je od 17. století v soukromém majetku šintoistické svatyně a stát to musel uznat i u soudu.",
        "Leží na styku čtyř litosférických desek, takže tu ročně zaznamenají přes tisíc otřesů.",
        "Jeho vlajka je bílá s červeným kruhem a hlavním městem je Tokio.",
    )),
    ("Poznej hlavní město.", "Kanberra", ["Canberra"], (
        "Jeho podobu vybrali roku 1912 v mezinárodní soutěži; vyhráli ji Američané Griffinovi.",
        "Leží ve vlastním federálním území mezi dvěma největšími městy země, aby se ani jedno neurazilo.",
        "Je hlavním městem Austrálie, ačkoli Sydney i Melbourne jsou mnohem větší.",
    )),
    ("Poznej pohoří.", "Andy", [], (
        "V jejich údolích se vyšlechtily brambory — dodnes se tu pěstují stovky odrůd, které jinde nikdo nezná.",
        "Je to nejdelší pohoří světa na souši, dlouhé přes sedm tisíc kilometrů.",
        "Vede jimi hřeben Jižní Ameriky a žijí tu lamy a kondoři.",
    )),
    ("Poznej řeku.", "Nil", [], (
        "Jeho hladinu měřily už ve starověku kamenné studny se stupnicí, podle kterých se vyměřovala daň.",
        "Vzniká soutokem dvou ramen v súdánském Chartúmu a protéká jedenácti státy.",
        "Je to nejdelší nebo druhá nejdelší řeka světa a na jeho březích vznikl starověký Egypt.",
    )),
    ("Poznej město.", "Petra", ["Petra v Jordánsku"], (
        "Evropě ji roku 1812 ukázal Švýcar Johann Ludwig Burckhardt, který se vydával za muslimského poutníka.",
        "Vytesali ji Nabatejci do růžového pískovce a přiváděli sem vodu důmyslným systémem kanálů.",
        "Vede k ní úzká soutěska Sík a natáčel se tu Indiana Jones a poslední křížová výprava.",
    )),
    ("Poznej stát.", "Mongolsko", [], (
        "Jeho obyvatelé dodnes z velké části žijí ve válcových stanech, kterým se říká jurta nebo ger.",
        "Leží mezi Ruskem a Čínou a přes třetina jeho obyvatel žije v hlavním městě.",
        "Rozkládá se tu poušť Gobi a ve 13. století odsud vyrazil Čingischán.",
    )),
    ("Poznej moře.", "Sargasové moře", ["Sargasové", "Sargassum"], (
        "Kolem roku 1492 jím proplouval Kryštof Kolumbus a jeho posádka se děsila, že loď uvázne.",
        "Leží v Atlantiku a je součástí oblasti známé jako Bermudský trojúhelník.",
        "Jako jediné moře na světě nemá břehy, jen mořské proudy — a míří sem třít úhoři z celé Evropy.",
    )),
    ("Poznej český hrad.", "Karlštejn", [], (
        "Roku 1422 ho sedm měsíců marně obléhali husité a metali dovnitř i nádoby s výkaly.",
        "Nechal ho postavit ve 14. století císař k uložení korunovačních klenotů.",
        "Leží nedaleko Prahy nad Berounkou a je v něm kaple svatého Kříže vykládaná drahokamy.",
    )),
    ("Poznej stát.", "Egypt", [], (
        "Jeho panovníkům se říkalo faraon, což původně znamenalo prostě „velký dům“ — tedy palác, ne osobu.",
        "Leží na dvou světadílech a Sinajský poloostrov už patří do Asie.",
        "Stojí tu pyramidy v Gíze a Velká sfinga.",
    )),
    ("Poznej jezero.", "Kaspické moře", ["Kaspik"], (
        "Právní spor o to, jestli je to moře nebo jezero, se táhl přes dvacet let kvůli dělení ropy.",
        "Hraničí s ním pět států a jeho hladina leží pod úrovní světového oceánu.",
        "Je to největší jezero světa a loví se v něm jeseter kvůli kaviáru.",
    )),
    ("Poznej ostrov.", "Grónsko", [], (
        "Jeho obyvatelé si roku 2009 vyhlasovali rozšířenou samosprávu a inuitština se stala jediným úředním jazykem.",
        "Je autonomní součástí Dánského království a roku 1985 vystoupilo z Evropského společenství.",
        "Jméno mu dal Erik Rudý, aby přilákal osadníky; je to největší ostrov světa a pokrývá ho mohutný ledovcový štít.",
    )),
    ("Poznej město.", "Istanbul", ["Cařihrad", "Konstantinopol"], (
        "Jeho dnešní jméno se úředně ustálilo až roku 1930, kdy pošta přestala doručovat na jiná.",
        "Leží na dvou světadílech a spojují je tři mosty přes Bospor.",
        "Stojí tu chrám Hagia Sofia i Modrá mešita a bývalo hlavním městem dvou říší.",
    )),
    ("Poznej stát.", "Nový Zéland", [], (
        "Jako první stát na světě dal roku 1893 volební právo ženám a dodnes na to bývá hrdý.",
        "Tvoří ho dva hlavní ostrovy a jeho původní obyvatelé se nazývají Maorové.",
        "Natáčel se tu Pán prstenů a jeho symbolem je nelétavý pták kiwi.",
    )),
    ("Poznej českou pamětihodnost.", "Lednicko-valtický areál", ["Lednice", "Lednice a Valtice"], (
        "Rod Lichtenštejnů ho po staletí upravoval do podoby, které se říká zahrada Evropy.",
        "Je to největší člověkem vytvořená krajina v Evropě, přes 280 kilometrů čtverečních.",
        "Leží na jižní Moravě u hranic s Rakouskem a je na seznamu UNESCO.",
    )),
    ("Poznej zemi.", "Portugalsko", [], (
        "Má nejstarší dosud platnou hranici v Evropě, ustálenou už ve 13. století.",
        "Jeho jazyk je po španělštině druhým nejrozšířenějším románským na světě.",
        "Odsud vyplouvali Vasco da Gama i Magalhães a hlavním městem je Lisabon.",
    )),
    ("Poznej horu.", "Kilimandžáro", ["Kilimandzaro"], (
        "Tvoří ho tři vyhaslé sopečné kužely a nejvyšší z nich se jmenuje Kibo.",
        "Leží v Tanzanii nedaleko rovníku a přesto má na vrcholu ledovec, který rychle mizí.",
        "Je nejvyšší horou Afriky a stojí osaměle nad savanou.",
    )),
    ("Poznej město.", "Petrohrad", ["Sankt Petěrburg", "Leningrad"], (
        "Vzniklo roku 1703 na bažinách a za jeho stavby zahynuly desetitisíce nevolníků.",
        "Za druhé světové války vydrželo obléhání dlouhé skoro devět set dní.",
        "Stojí tu Ermitáž a v létě sem lidé jezdí na bílé noci.",
    )),
    ("Poznej průsmyk.", "Gibraltar", ["Gibraltarský průliv"], (
        "Podle pověsti si ho Britové udrží jen do té doby, dokud tu bude žít místní zvěř dovezená z Afriky.",
        "Území patří Británii, ačkoli leží na Pyrenejském poloostrově, a Španělsko si na ně činí nárok.",
        "Je to skalní útes na jižním cípu Pyrenejského poloostrova a volně tu žijí makakové, jinde v Evropě nevídaní.",
    )),
    ("Poznej řeku.", "Amazonka", [], (
        "V ústí se dvakrát denně valí proti proudu vlna zvaná pororoca, na které se dá surfovat.",
        "Nevede přes ni po celé délce jediný most a žije v ní sladkovodní delfín.",
        "Je nejvodnatější řekou světa a protéká největším deštným pralesem.",
    )),
    ("Poznej stát.", "Indonésie", [], (
        "Její hlavní město se propadá tak rychle, že vláda staví nové na jiném ostrově.",
        "Tvoří ji přes sedmnáct tisíc ostrovů a je to nejlidnatější muslimská země světa.",
        "Leží tu Bali, Jáva i Sumatra a roku 1883 tu vybuchla sopka Krakatoa.",
    )),
]

BANK["veda"] += [
    ("Poznej chemický prvek.", "Fosfor", ["P"], (
        "Objevil ho roku 1669 alchymista Hennig Brand, když odpařoval velké množství moči a hledal kámen mudrců.",
        "V jedné své podobě samovolně vzplane na vzduchu, proto se skladuje pod vodou.",
        "Škrtátko na krabičce zápalek je z jeho červené odrůdy a v těle ho máme hlavně v kostech.",
    )),
    ("Poznej jednotku.", "Pascal", ["Pa"], (
        "V technice se dlouho místo ní počítalo v atmosférách a v milimetrech rtuťového sloupce.",
        "Jmenuje se po francouzském matematikovi, který jako první změřil, jak veličina klesá s nadmořskou výškou.",
        "Meteorologové ji v tisícinásobku hlásí u tlaku vzduchu — normální hodnota je 1013.",
    )),
    ("Poznej lidský orgán.", "Slinivka břišní", ["pankreas", "slinivka"], (
        "Její Langerhansovy ostrůvky tvoří jen zhruba dvě procenta její hmoty, ale rozhodují o celém metabolismu.",
        "Vytváří trávicí enzymy a zároveň dva hormony s opačným účinkem.",
        "Když přestane vyrábět inzulin, propukne cukrovka.",
    )),
    ("Poznej vesmírné těleso.", "Saturn", [], (
        "Jeho hustota je nižší než hustota vody, takže by na dostatečně velkém oceánu plaval.",
        "Sonda Cassini u něj strávila třináct let a nakonec ji úmyslně navedli do atmosféry.",
        "Je to planeta s nejnápadnějším prstencem, který objevil Christiaan Huygens.",
    )),
    ("Poznej živočicha.", "Tardigrada", ["želvuška", "želvušky"], (
        "Přežije vysušení, tlak šesti tisíc atmosfér i pobyt ve vakuu, protože dokáže nahradit vodu v buňkách cukrem.",
        "Měří kolem půl milimetru, žije v mechu a lezoucí pohyb jí vynesl jméno podle medvěda.",
        "Poslali ji do vesmíru a v otevřeném prostoru přežila; česky se jí říká podle želvy.",
    )),
    ("Poznej fyzikální jev.", "Dopplerův jev", ["Doppler"], (
        "Popsal ho roku 1842 rakouský fyzik, který část života učil v Praze; ověřovali ho trubači na jedoucím vlaku.",
        "Astronomové podle něj poznají, že se galaxie vzdalují — jejich světlo se posouvá k červené.",
        "Slyšíš ho pokaždé, když kolem tebe projede sanitka a tón houkačky náhle klesne.",
    )),
    ("Poznej chemickou sloučeninu.", "Chlorid sodný", ["sůl", "kuchyňská sůl", "NaCl"], (
        "Ve starém Římě z něj měli vojáci část žoldu; odtud pochází slovo salár, tedy plat.",
        "Jeho krystal má krychlovou mřížku, ve které se pravidelně střídají dva druhy iontů.",
        "Stojí na každém stole vedle pepře a bez ní nechutná nic.",
    )),
    ("Poznej vědce.", "Nikolaus Koperník", ["Koperník", "Kopernik"], (
        "Živil se jako kanovník ve Fromborku, spravoval majetek kapituly a napsal i pojednání o měnové reformě.",
        "Své hlavní dílo mu vytiskli až na smrtelné posteli, s předmluvou, která ho vydávala za pouhý početní model.",
        "Postavil Slunce do středu a Zemi mezi planety.",
    )),
    ("Poznej léčivo.", "Aspirin", ["kyselina acetylsalicylová"], (
        "Německá firma o jeho značku po první světové válce přišla — patřila k válečným reparacím.",
        "Účinná látka se dřív získávala z vrbové kůry a odvar z ní doporučoval už Hippokratés.",
        "Bere se proti bolesti a horečce a v malých dávkách na ředění krve.",
    )),
    ("Poznej planetu.", "Jupiter", [], (
        "Sonda Juno kolem něj obíhá po protáhlé dráze, aby se pásem tvrdého záření prolétla co nejkratší dobu.",
        "Má hmotnost dvaapůlkrát větší než všechny ostatní planety soustavy dohromady.",
        "Je na něm Velká rudá skvrna, bouře větší než Země, a Galileo u něj objevil čtyři měsíce.",
    )),
    ("Poznej chemický prvek.", "Železo", ["Fe"], (
        "V jádru Země ho je tolik, že tvoří planetární magnetické pole; do zemské kůry se ho dostalo poměrně málo.",
        "Jeho značka pochází z latinského ferrum a slitina s uhlíkem se jmenuje ocel.",
        "Rezaví, přitahuje magnet a je v hemoglobinu, který barví krev na červeno.",
    )),
    ("Poznej vědce.", "Charles Darwin", ["Darwin"], (
        "Na plavbu ho vzali hlavně proto, aby měl kapitán s kým večeřet — společenský styk s posádkou se nehodil.",
        "Před hlavním dílem strávil osm let studiem svijonožců, aby si udělal jméno jako systematik.",
        "Napsal O původu druhů a jeho výprava se plavila na lodi Beagle.",
    )),
    ("Poznej jev.", "Duha", [], (
        "Její barvy roztřídil na sedm Isaac Newton, aby jich bylo tolik jako tónů v hudební stupnici.",
        "Vzniká lomem a odrazem světla v kapkách vody a pozorovatel ji vždycky vidí pod úhlem kolem 42 stupňů.",
        "Objeví se po dešti proti slunci a její barvy jdou od červené po fialovou.",
    )),
    ("Poznej lidskou tkáň.", "Zubní sklovina", ["sklovina"], (
        "Neobsahuje živé buňky, takže se po poškození sama neobnoví — na rozdíl od kosti i kůže.",
        "Je z devadesáti sedmi procent nerostná a tvoří ji hydroxyapatit.",
        "Je to nejtvrdší hmota v lidském těle a chrání to, čím koušeš, před kazem.",
    )),
    ("Poznej vesmírné těleso.", "Měsíc", [], (
        "Vzdaluje se od nás zhruba o čtyři centimetry za rok a měří se to odrazem laseru od zrcadel, která tam nechaly výpravy.",
        "Otáčí se kolem osy stejně dlouho, jako obíhá kolem Země, takže z něj vidíme pořád tutéž stranu.",
        "Způsobuje příliv a odliv a lidé na něm stanuli roku 1969.",
    )),
    ("Poznej chemický prvek.", "Vodík", ["H"], (
        "Tvoří tři čtvrtiny hmotnosti vesmíru a v laboratoři ho poprvé oddělil Henry Cavendish roku 1766.",
        "Je to nejlehčí prvek s protonovým číslem 1 a plnily se jím vzducholodě.",
        "Se dvěma atomy na jeden kyslík dává vodu.",
    )),
    ("Poznej jev.", "Fata morgána", ["zrcadlení", "fata morgana"], (
        "Jméno má po víle z artušovských legend, kterou Italové vinili z přeludů v Messinské úžině.",
        "Vzniká lomem světla ve vrstvách vzduchu o různé teplotě, které se chovají jako čočka.",
        "Poutník kvůli ní na poušti vidí vodu, která tam není.",
    )),
    ("Poznej vědce.", "Louis Pasteur", ["Pasteur"], (
        "Nebyl to lékař a nesměl léčit; první očkování proti vzteklině dělal na chlapci s vypůjčenou lékařskou asistencí.",
        "Vyvrátil představu, že se život rodí sám ze sebe, pokusem s baňkami s labutím hrdlem.",
        "Nese jeho jméno postup, kterým se šetrným ohřevem prodlužuje trvanlivost mléka.",
    )),
    ("Poznej stavbu těla.", "Bránice", [], (
        "Při nádechu se stahuje a klesá, takže se hrudní dutina rozšíří — na rozdíl od intuitivní představy se nezvedá.",
        "Prochází jí jícen, aorta a dolní dutá žíla, každá vlastním otvorem.",
        "Její prudké stahy způsobují škytavku a odděluje hrudník od břicha.",
    )),
    ("Poznej materiál.", "Sklo", [], (
        "Není to pevná látka v běžném smyslu — jeho atomy jsou uspořádané nepravidelně jako v kapalině.",
        "Vyrábí se tavením křemenného písku se sodou a vápencem při teplotách kolem 1500 stupňů.",
        "Fouká se z něj a v Čechách se z něj brousí proslulé lustry a vázy.",
    )),
]

BANK["kultura"] += [
    ("Poznej film.", "Čelisti", ["Jaws"], (
        "Mechanický model, kterému štáb říkal Bruce, se pořád kazil, takže se točilo z pohledu tvora — a bylo to lepší.",
        "Režíroval ho roku 1975 Steven Spielberg a hudbu složil John Williams ze dvou střídavých tónů.",
        "Vypráví o žraloku, který ohrožuje ostrovní letovisko.",
    )),
    ("Poznej knihu.", "Vojna a mír", ["Vojna a mír (kniha)"], (
        "Autorova žena ho podle legendy přepisovala načisto sedmkrát.",
        "Sám autor tvrdil, že to není román, a odmítal to zařadit do jakéhokoli žánru.",
        "Je to ruský epos o napoleonských válkách od Lva Nikolajeviče Tolstého.",
    )),
    ("Poznej hudební skupinu.", "Queen", [], (
        "Jejich kytarista si nástroj vyrobil s otcem z krbové římsy a strun z motocyklu.",
        "Jméno si vybral zpěvák, který se narodil na Zanzibaru jako Farrokh Bulsara.",
        "Zpívají Bohemian Rhapsody a We Will Rock You.",
    )),
    ("Poznej film.", "Obchod na korze", [], (
        "Získal roku 1966 prvního československého Oscara za cizojazyčný film.",
        "Natočili ho Ján Kadár a Elmar Klos podle povídky Ladislava Grosmana.",
        "Vypráví o árizátorovi, který má převzít krám staré hluché Židovky za slovenského štátu.",
    )),
    ("Poznej obraz.", "Mona Lisa", ["La Gioconda", "Mona Lisa (obraz)"], (
        "Roku 1911 ji ukradl italský zaměstnanec muzea a dva roky ji měl v kufru pod postelí.",
        "Je malovaná na topolové desce a měří jen zhruba 77 na 53 centimetrů.",
        "Visí v Louvru za neprůstřelným sklem a proslula svým úsměvem.",
    )),
    ("Poznej seriál.", "Nemocnice na kraji města", [], (
        "Scenárista Jaroslav Dietl psal díly tak rychle, že se natáčelo současně s psaním.",
        "Vysílal se od roku 1977 a odehrává se na ortopedickém oddělení v nejmenovaném okresním sídle.",
        "Hrál v něm Ladislav Chudík jako primář Sova a Miloš Kopecký jako doktor Štrosmajer.",
    )),
    ("Poznej stavbu.", "Tádž Mahal", ["Taj Mahal"], (
        "Jeho čtyři minarety jsou schválně nakloněné od středu, aby při zemětřesení nespadly na hrobku.",
        "Postavil ho v 17. století mughalský vládce Šáhdžahán a stavělo ho přes dvacet tisíc lidí.",
        "Je to bílý mramorový mauzoleum v indické Ágře, které dal panovník postavit pro svou zesnulou ženu.",
    )),
    ("Poznej hudební dílo.", "Má vlast", [], (
        "Autor ho dokončil ve chvíli, kdy už neslyšel ani vlastní tóny; jednotlivé části vznikaly pět let.",
        "Skládá se ze šesti symfonických básní a druhá z nich je nejhranější.",
        "Zahajuje se jím festival Pražské jaro vždy 12. května a napsal ho Bedřich Smetana.",
    )),
    ("Poznej film.", "Matrix", [], (
        "Zelený déšť znaků na obrazovkách tvoří zrcadlově obrácené japonské slabiky opsané z receptů na suši.",
        "Vyšel roku 1999 a proslavil filmový trik zvaný bullet time.",
        "Hlavní hrdina Neo si vybírá mezi červenou a modrou pilulkou.",
    )),
    ("Poznej knihu.", "Osudy dobrého vojáka Švejka", ["Švejk"], (
        "Autor ji nedokončil — zemřel v Lipnici nad Sázavou ve věku čtyřiceti let a poslední díl dopsal někdo jiný.",
        "Ilustroval ji Josef Lada, ačkoli hlavního hrdinu nikdy neviděl tak, jak si ho představoval autor.",
        "Je to nejpřekládanější česká kniha a jejím hrdinou je obchodník se psy z první světové války.",
    )),
    ("Poznej hudební nástroj.", "Varhany", [], (
        "Hráč ovládá kromě rukou i klaviaturu pod nohama a k obsluze rejstříků míval pomocníka.",
        "Vzduch do nich dřív pumpovali kalkanti, dnes to obstarává elektrický ventilátor.",
        "Stojí ve většině kostelů a Johann Sebastian Bach pro ně napsal Toccatu a fugu d moll.",
    )),
    ("Poznej film.", "Vesničko má středisková", [], (
        "Byl roku 1987 nominován na Oscara za cizojazyčný film, ale nezískal ho.",
        "Natočil ho Jiří Menzel podle scénáře Zdeňka Svěráka.",
        "Hlavními postavami jsou řidič Pávek a jeho nešikovný závozník Otík.",
    )),
    ("Poznej hudební styl.", "Jazz", [], (
        "Vznikl na přelomu 19. a 20. století v New Orleansu ze splynutí blues, ragtimu a dechovkových pochodů.",
        "Jeho podstatou je improvizace nad harmonickým schématem a swingový rytmus.",
        "Hrál ho Louis Armstrong a v Česku ho proslavil Jaroslav Ježek.",
    )),
    ("Poznej divadlo.", "Národní divadlo", ["Zlatá kaplička"], (
        "Vyhořelo roku 1881, jen pár týdnů po slavnostním otevření, a znovu se otevřelo za dva roky.",
        "Na jeho stavbu se sbíralo po celé zemi a nad jevištěm je nápis Národ sobě.",
        "Stojí v Praze na břehu Vltavy a jeho pozlacené střeše vděčí za lidovou přezdívku.",
    )),
    ("Poznej film.", "Pán prstenů", ["Pán prstenů: Společenstvo prstenu"], (
        "Všechny tři díly se natáčely naráz během patnácti měsíců a devět herců si nechalo vytetovat elfské znamení.",
        "Režíroval je Peter Jackson a natáčely se na Novém Zélandu.",
        "Vypráví o hobitovi, který nese do Mordoru šperk, jenž vládne všem ostatním.",
    )),
    ("Poznej spisovatele.", "Bohumil Hrabal", ["Hrabal"], (
        "Vystudoval práva, ale živil se jako dělník v kladenských hutích, balič papíru a kulisák.",
        "Psal takzvané pábitelské texty a jeho knihy stáhli za normalizace z knihoven.",
        "Napsal Ostře sledované vlaky a Postřižiny; chodil do hospody U Zlatého tygra.",
    )),
    ("Poznej píseň.", "Imagine", [], (
        "Text vychází z básniček ve sbírce Grapefruit, kterou napsala autorova manželka.",
        "Vyšla roku 1971 a autor v ní zpívá o světě bez zemí a bez majetku.",
        "Napsal ji John Lennon a hraje se na ni na bílém klavíru.",
    )),
    ("Poznej stavbu.", "Koloseum", ["Kolosseum", "Flaviovský amfiteátr"], (
        "Vešlo se do něj kolem padesáti tisíc lidí a plátěná plachta nad hledištěm se ovládala lany podle větru.",
        "Postavili ho Flaviovci v prvním století a pod arénou byl systém chodeb a výtahů pro zvířata.",
        "Stojí v Římě a konaly se v něm gladiátorské zápasy.",
    )),
    ("Poznej českého skladatele.", "Leoš Janáček", ["Janáček"], (
        "Zapisoval si do notesu nápěvky lidské řeči a tvrdil, že z nich pozná náladu mluvčího.",
        "Byl to moravský skladatel, kterému se prosadit podařilo až po šedesátce.",
        "Napsal opery Její pastorkyňa a Příhody lišky Bystroušky a cyklus Po zarostlém chodníčku.",
    )),
    ("Poznej film.", "Casablanca", [], (
        "Scénář se dopisoval během natáčení, takže herci dlouho nevěděli, jak film skončí.",
        "Vznikl roku 1942 a odehrává se v marockém městě pod vládou Vichy.",
        "Humphrey Bogart v něm provozuje bar a zazní tu prosba o zahrání jedné písně.",
    )),
]

BANK["historie"] += [
    ("Poznej událost.", "Bostonské pití čaje", ["Boston Tea Party"], (
        "Účastníci se přestrojili za Mohykány a do vody naházeli náklad v hodnotě, která by dnes byla přes milion dolarů.",
        "Šlo o protest proti daňové výsadě Východoindické společnosti, ne proti dani samotné.",
        "Odehrálo se roku 1773 v americkém přístavu a bývá označováno za předehru války za nezávislost.",
    )),
    ("Poznej panovnici.", "Marie Terezie", [], (
        "Porodila šestnáct dětí a jedna z dcer skončila na popravišti ve Francii.",
        "Byla to jediná žena na habsburském trůně a nastoupila díky pragmatické sankci svého otce.",
        "Zavedla povinnou školní docházku a číslování domů.",
    )),
    ("Poznej válku.", "Krymská válka", ["Krym"], (
        "Poprvé se v ní ve velkém uplatnila telegrafní zpráva z bojiště a fotografie z fronty.",
        "Proslula útokem lehké brigády a působením ošetřovatelky Florence Nightingalové.",
        "Vedly ji v padesátých letech 19. století Rusko proti Turecku, Británii a Francii o poloostrov v Černém moři.",
    )),
    ("Poznej událost.", "Velká francouzská revoluce", ["francouzská revoluce"], (
        "Zavedla nový kalendář, ve kterém měl týden deset dní a měsíce se jmenovaly podle počasí.",
        "Její hesla zněla volnost, rovnost, bratrství a přinesla i vládu teroru pod Robespierrem.",
        "Začala roku 1789 dobytím Bastilly a skončila popravou krále.",
    )),
    ("Poznej dynastii.", "Přemyslovci", [], (
        "Vymřeli po meči roku 1306 zavražděním posledního mužského člena v Olomouci.",
        "Byl to první český panovnický rod a jejich mýtickým zakladatelem byl oráč od Stadic.",
        "Patřili k nim svatý Václav, Otakar II. i Václav II.",
    )),
    ("Poznej období.", "Průmyslová revoluce", [], (
        "Zahájila ji v Anglii textilní výroba; létající člunek a spřádací stroj předběhly i parní pohon.",
        "Přinesla stěhování lidí do měst, dětskou práci v továrnách a vznik dělnické třídy.",
        "Její pohon obstaral parní stroj a symbolem se staly komíny a železnice.",
    )),
    ("Poznej stavbu.", "Petřínská rozhledna", ["Petřín", "rozhledna na Petříně"], (
        "Postavili ji roku 1891 za pouhé čtyři měsíce pro Jubilejní zemskou výstavu.",
        "Měří 63,5 metru, ale díky poloze na kopci sahá její vrchol do stejné výšky jako pařížský vzor.",
        "Je to zmenšená napodobenina Eiffelovy věže nad Prahou.",
    )),
    ("Poznej událost.", "Bitva u Waterloo", ["Waterloo"], (
        "Rozhodl ji večerní příchod pruských jednotek, na které vítěz čekal celý den.",
        "Odehrála se v červnu 1815 v dnešní Belgii a ukončila stodenní návrat jednoho vládce.",
        "Definitivně v ní padl Napoleon a její jméno se stalo synonymem konečné porážky.",
    )),
    ("Poznej říši.", "Byzantská říše", ["Byzanc"], (
        "Sama sebe nikdy nenazývala tímhle jménem — její obyvatelé si říkali Římané.",
        "Vládl jí Justinián, který nechal postavit chrám Hagia Sofia, a používala řecký oheň.",
        "Byla to východní část římského impéria s hlavním městem Konstantinopolí.",
    )),
    ("Poznej událost.", "Vestfálský mír", ["vestfálský mír"], (
        "Jednalo se o něm pět let ve dvou městech současně, protože katolíci a protestanti nechtěli sedět spolu.",
        "Uzavřel roku 1648 třicetiletou válku a bývá označován za zrod moderního mezistátního práva.",
        "Potvrdil zásadu, že o náboženství v zemi rozhoduje panovník, a připravil Habsburky o vliv v říši.",
    )),
    ("Poznej vojevůdce.", "Jan Žižka", ["Žižka"], (
        "Před husitskými válkami sloužil na dvoře krále Václava IV. a bojoval i u Grunwaldu.",
        "Nikdy neprohrál bitvu a vozovou hradbu proměnil v pojízdnou pevnost.",
        "Byl jednooký a jeho jezdecká socha na Vítkově je největší v Česku.",
    )),
    ("Poznej událost.", "Atentát na Heydricha", ["operace Anthropoid", "Anthropoid"], (
        "Rozhodujícím okamžikem bylo zaseknutí samopalu; použila se proto upravená protitanková mina.",
        "Následovalo vypálení Lidic a Ležáků a obležení kostela v Resslově ulici.",
        "Provedli ho roku 1942 v Praze parašutisté Kubiš a Gabčík na zastupujícího říšského protektora.",
    )),
    ("Poznej stavbu.", "Alhambra", [], (
        "Její jméno pochází z arabského výrazu pro červenou, podle barvy hlíny v cihlách.",
        "Postavili ji Nasrovci a po dobytí ji Španělé nesrovnali se zemí, jen do ní vestavěli renesanční palác.",
        "Stojí v Granadě a je vrcholem maurského umění v Evropě.",
    )),
    ("Poznej událost.", "Karibská krize", ["kubánská raketová krize"], (
        "Odvrátil ji mimo jiné sovětský důstojník na ponorce, který odmítl souhlasit s odpálením torpéda.",
        "Trvala třináct dní v říjnu 1962 a skončila stažením raket výměnou za stažení amerických z Turecka.",
        "Šlo o sovětské jaderné rakety rozmístěné na ostrově devadesát mil od Floridy.",
    )),
    ("Poznej dokument.", "Zlatá bula sicilská", [], (
        "Vydána byla v Basileji, ačkoli ji vydal panovník sídlící na Sicílii — odtud ten přívlastek.",
        "Potvrdila roku 1212 dědičnost královského titulu pro český rod a jeho postavení v říši.",
        "Získal ji Přemysl Otakar I. a je uložena v Národním archivu.",
    )),
    ("Poznej událost.", "Vynález kola", ["kolo"], (
        "Nejstarší doklady pocházejí z Mezopotámie a překvapivě se nejdřív používalo v hrnčířství, ne k dopravě.",
        "Předkolumbovská Amerika ho znala jen na dětských hračkách, protože chyběla tažná zvířata.",
        "Je to kruhový předmět otáčející se kolem osy a bez něj by nejezdil vůz ani auto.",
    )),
    ("Poznej říši.", "Starověký Řím", ["Řím", "římská říše"], (
        "Jeho vodovody vedly vodu samospádem a spád byl místy jen několik centimetrů na kilometr.",
        "Republiku vystřídalo císařství a jeho armádu tvořily legie po zhruba pěti tisících mužích.",
        "Jeho jazykem byla latina a legendárními zakladateli Romulus a Remus.",
    )),
    ("Poznej událost.", "Objevení Ameriky", ["objevení Ameriky Kolumbem"], (
        "Nový světadíl dostal jméno po jiném mořeplavci, jehož dopisy jako první tvrdily, že jde o novou pevninu.",
        "Vikingové tam byli o pět set let dřív a založili osadu na Newfoundlandu.",
        "Stalo se to roku 1492, kdy tři lodě dopluly na Bahamy.",
    )),
    ("Poznej válku.", "Punské války", ["punské války"], (
        "Jméno mají po latinském označení pro Féničany, ze kterých pocházeli obyvatelé poraženého města.",
        "Vedly se ve třech kolech mezi Římem a Kartágem o vládu nad západním Středomořím.",
        "Proslavil je Hannibal, který přešel Alpy se slony.",
    )),
    ("Poznej stavbu.", "Stonehenge", [], (
        "Menší modré kameny sem dopravili z velšských hor vzdálených přes dvě stě kilometrů.",
        "Stavělo se v několika fázích zhruba mezi lety 3000 a 1600 před naším letopočtem.",
        "Je to kruh z obrovských kamenů v jižní Anglii, orientovaný podle slunovratu.",
    )),
]

BANK["priroda"] += [
    ("Poznej zvíře.", "Žirafa", [], (
        "Má stejný počet krčních obratlů jako člověk — sedm —, jen jsou obrovské.",
        "Její srdce váží přes deset kilo, aby dokázalo hnát krev do hlavy.",
        "Je to nejvyšší suchozemské zvíře a okusuje listí z akácií v africké savaně.",
    )),
    ("Poznej rostlinu.", "Rafflésie", ["rafflesie", "raflézie"], (
        "Nemá kořeny, stonek ani listy — žije jako parazit uvnitř liány a navenek se ukáže jen květem.",
        "Roste v deštných pralesích Sumatry a Bornea a pupen jí zraje devět měsíců.",
        "Má největší jednotlivý květ na světě a páchne po zdechlině, aby přilákala mouchy.",
    )),
    ("Poznej zvíře.", "Netopýr", ["netopýři"], (
        "Jeho křídlo je vlastně ruka — blána je napjatá mezi neúměrně prodlouženými prsty.",
        "Je to jediný savec, který se dokáže aktivně vznést a létat, ne jen plachtit.",
        "Orientuje se echolokací a přes den visí hlavou dolů.",
    )),
    ("Poznej strom.", "Baobab", [], (
        "V kmeni zadrží až sto tisíc litrů vody a dřevo má tak měkké, že se dá strhat rukou.",
        "Roste v afrických savanách a některé duté kmeny sloužily jako vězení, obchod i autobusová zastávka.",
        "Vypadá, jako by rostl kořeny vzhůru, a objevuje se v Malém princi.",
    )),
    ("Poznej živočicha.", "Korál", ["koráli", "korálnatci"], (
        "Je to živočich, ale energii z velké části dostává od řas, které mu žijí v tkáních.",
        "Když se voda oteplí, řasy vypudí a zbělá — tomu se říká bělení.",
        "Z jeho vápenatých schránek vznikl Velký bariérový útes u Austrálie.",
    )),
    ("Poznej rostlinu.", "Rýže", [], (
        "Pole se zaplavují ne kvůli rostlině samotné, ale proto, že voda potlačí plevel.",
        "Je základní potravinou pro víc než polovinu lidstva a pěstuje se hlavně v Asii.",
        "Vaří se z ní příloha a sushi a sklízí se na terasovitých polích.",
    )),
    ("Poznej zvíře.", "Slon africký", ["slon"], (
        "Dorozumívá se i zvuky pod hranicí lidského sluchu, které se nesou na kilometry.",
        "Chobot má přes čtyřicet tisíc svalů a zvedne s ním kmen i zvedne jediné stéblo.",
        "Je to největší suchozemský savec a jeho kly jsou důvodem, proč ho pytláci hubí.",
    )),
    ("Poznej rostlinu.", "Leknín", ["lekníny"], (
        "Jeho listy mají na spodní straně žebroví, které je udrží na hladině i s několika kilogramy zátěže.",
        "Kořeny má v bahně na dně, květ na hladině a v noci se zavírá.",
        "Maloval je Claude Monet ve své zahradě v Giverny.",
    )),
    ("Poznej živočicha.", "Kudlanka nábožná", ["kudlanka"], (
        "Otočí hlavu skoro o 180 stupňů, což jinému hmyzu nejde, a má jediné ucho uprostřed hrudi.",
        "V Česku se v posledních desetiletích šíří na jižní Moravě, kde dřív nebyla.",
        "Přední nohy drží složené jako při modlitbě a samice někdy sežere samce.",
    )),
    ("Poznej houbu.", "Hřib smrkový", ["hřib", "hřib pravý", "praváček"], (
        "Netvoří ho jen klobouk a třeň — pod zemí je propletená síť vláken, která spolupracuje s kořeny stromu.",
        "Roste hlavně pod smrky a duby a jeho rourky jsou zprvu bílé, později nazelenalé.",
        "Je to nejvyhledávanější jedlá houba a suší se na omáčku.",
    )),
    ("Poznej zvíře.", "Los evropský", ["los"], (
        "V Česku se sám vrátil v šedesátých letech ze severu a v jižních Čechách žije malá populace.",
        "Jeho paroží může vážit přes dvacet kilo a shazuje ho každou zimu.",
        "Je největším žijícím jelenovitým a má nápadný převislý pysk.",
    )),
    ("Poznej rostlinu.", "Slunečnice", [], (
        "Za sluncem se otáčí jen dokud roste; rozkvetlý úbor už zůstane natočený na východ.",
        "Semínka v úboru jsou uspořádaná do dvou soustav spirál a jejich počty tvoří Fibonacciho čísla.",
        "Lisuje se z ní olej a namaloval ji van Gogh.",
    )),
    ("Poznej živočicha.", "Mravenec", ["mravenci"], (
        "Některé druhy pěstují houby a jiné chovají mšice jako dobytek kvůli sladké medovici.",
        "Celková hmotnost všech jedinců na Zemi se odhaduje na srovnatelnou s hmotností všech lidí.",
        "Žije v koloniích s královnou a v lese staví kupy z jehličí.",
    )),
    ("Poznej rostlinu.", "Brambor", ["brambory", "lilek brambor"], (
        "Do Evropy se dostal v 16. století a dlouho se pěstoval jen jako okrasná rostlina; jeho nať je jedovatá.",
        "Jeho nemoc způsobila v 19. století v Irsku hladomor, po kterém se země vylidnila o čtvrtinu.",
        "Jedlá je hlíza pod zemí a dělají se z ní knedlíky i hranolky.",
    )),
    ("Poznej zvíře.", "Vlk obecný", ["vlk"], (
        "Ve smečce se rozmnožuje zpravidla jediný pár a ostatní členové jsou jeho odrostlá mláďata.",
        "Do Česka se sám vrátil z Německa a Polska a dnes žije v Krkonoších i na Šumavě.",
        "Je předkem psa domácího a vyje na měsíc.",
    )),
    ("Poznej jev.", "Migrace ptáků", ["tah ptáků", "ptačí tah"], (
        "Řídí se při ní polohou hvězd, magnetickým polem i pachy a mladí jedinci to u některých druhů zvládají bez doprovodu.",
        "Rekordmanem je rybák dlouhoocasý, který každoročně letí od pólu k pólu.",
        "Vlaštovky kvůli ní na podzim odlétají do Afriky a na jaře se vracejí.",
    )),
    ("Poznej minerál.", "Křemen", ["křemen (minerál)"], (
        "Jeho krystal se pod tlakem elektricky nabíjí, čehož se využívá v hodinkách i v zapalovačích.",
        "Ve stupnici tvrdosti má číslo sedm a v čisté podobě je bezbarvý — pak se mu říká křišťál.",
        "Je to nejrozšířenější minerál zemské kůry a tvoří většinu písku.",
    )),
    ("Poznej zvíře.", "Klokan", ["klokani"], (
        "Skáče tak, že šlachy v nohou pracují jako pružiny — při vyšší rychlosti spotřebuje méně energie, ne víc.",
        "Samice dokáže zastavit vývoj zárodku, dokud předchozí mládě neopustí vak.",
        "Je to symbol Austrálie a mládě mu roste v kožním vaku na břiše.",
    )),
    ("Poznej rostlinu.", "Chmel", [], (
        "Pěstuje se jen samičí rostlina, protože oplodněné šištice by nápoji zkazily chuť.",
        "V Česku má jeho nejznámější odrůda jméno podle města na Lounsku a rostliny šplhají po drátěnkách do šesti metrů.",
        "Dává pivu hořkou chuť a vůni.",
    )),
    ("Poznej živočicha.", "Ježek", ["ježek západní", "ježci"], (
        "Když narazí na neznámý pach, olíže si ho a pěnu si rozetře po bodlinách — nikdo přesně neví proč.",
        "Zimu prospí v hnízdě z listí a tep mu klesne z několika set na pár desítek za minutu.",
        "Má na hřbetě bodliny a při nebezpečí se stočí do klubíčka.",
    )),
]

BANK["technika"] += [
    ("Poznej vynález.", "Telefon", [], (
        "Přihláška se podala v tentýž den jako konkurenční od Elishy Graye a soudy se o prvenství vedly desítky let.",
        "První slova, která se jím přenesla, byla výzva pomocníkovi ve vedlejší místnosti, aby přišel.",
        "Vynalezl ho Alexander Graham Bell a dnes ho má každý v kapse.",
    )),
    ("Poznej dopravní prostředek.", "Vrtulník", ["helikoptéra"], (
        "Bez vyrovnávacího prvku na ocasu by se trup roztočil na opačnou stranu než nosná plocha.",
        "První použitelný stroj postavil roku 1939 Igor Sikorskij a dokáže viset na místě.",
        "Přistane bez rozjezdu a používá se u záchranky i v horách.",
    )),
    ("Poznej materiál.", "Beton", [], (
        "Římané ho míchali se sopečným popelem a jejich směs tvrdne dodnes i pod mořskou hladinou.",
        "Sám o sobě dobře snáší tlak, ale ne tah, proto se do něj vkládá ocelová výztuž.",
        "Je z něj většina moderních staveb a míchá se z cementu, písku a vody.",
    )),
    ("Poznej vynález.", "Internet", [], (
        "Jeho předchůdce ARPANET propojil roku 1969 čtyři americké univerzity a první přenesená zpráva se přerušila po dvou písmenech.",
        "Stojí na protokolech TCP/IP a na myšlence, že data putují po částech různými cestami.",
        "Bez něj by nefungoval web ani e-mail.",
    )),
    ("Poznej stroj.", "Tiskárna", ["počítačová tiskárna"], (
        "Inkoustová technologie vznikla podle legendy poté, co si inženýr položil na injekční stříkačku horkou páječku.",
        "Laserová varianta pracuje s elektrostatickým nábojem na válci a práškovým barvivem.",
        "Připojí se k počítači a přenese text na papír.",
    )),
    ("Poznej vynález.", "Zip", ["zdrhovadlo"], (
        "První použitelnou podobu navrhl roku 1913 Švéd Gideon Sundbäck a nejdřív se používal na galoše.",
        "Dnešní jméno vymyslela obuvnická firma podle zvuku, který přitom vzniká.",
        "Zapíná se jím bunda a jezdec spojuje dvě řady zoubků.",
    )),
    ("Poznej stavbu.", "Golden Gate", ["Golden Gate Bridge", "most Golden Gate"], (
        "Jeho barva se jmenuje international orange a natírá se prakticky nepřetržitě.",
        "Otevřel se roku 1937 a při stavbě zachránila síť pod mostem devatenáct dělníků.",
        "Klene se nad vjezdem do zálivu u San Franciska.",
    )),
    ("Poznej dopravní prostředek.", "Concorde", ["Concord"], (
        "Trup se za letu horkem prodloužil zhruba o dvacet centimetrů, takže mezi panely zůstávala mezera.",
        "Létal nadzvukovou rychlostí a Londýn s New Yorkem zvládal za necelé tři a půl hodiny.",
        "Vyráběly ho společně Francie a Británie a provoz skončil roku 2003.",
    )),
    ("Poznej vynález.", "Baterie", ["elektrický článek", "galvanický článek"], (
        "První podobu tvořil sloupec střídavých kotoučů dvou kovů proložených papírem namočeným v solance.",
        "Postavil ji roku 1800 Alessandro Volta a nese po něm jméno jednotka napětí.",
        "Dnes je v každém mobilu a v autě startuje motor.",
    )),
    ("Poznej techniku.", "Ultrazvuk", ["sonografie"], (
        "Vychází z výzkumu hledání ponorek za první světové války a z jevu, kdy se krystal pod napětím rozkmitá.",
        "Pracuje s frekvencemi nad hranicí lidského sluchu a obraz vzniká z odrazů.",
        "Díky němu rodiče vidí miminko dřív, než se narodí.",
    )),
    ("Poznej vozidlo.", "Škoda 120", ["Škoda 105", "Škoda 105/120"], (
        "Motor měla vzadu a chladič také, takže se v zimě špatně topilo a vzadu bylo přetopeno.",
        "Vyráběla se v Mladé Boleslavi od roku 1976 a v Británii se jí posmívali v anekdotách.",
        "Byla to nejrozšířenější osobní auto v Československu před vozem Favorit.",
    )),
    ("Poznej vynález.", "Klimatizace", [], (
        "Vznikla roku 1902 ne kvůli lidem, ale kvůli tiskárně, které vlhkost rozmazávala barvy.",
        "Pracuje na stejném principu jako lednička — odebírá teplo odpařováním chladiva.",
        "V létě ochladí místnost a v autě ji dnes má skoro každý.",
    )),
    ("Poznej stavbu.", "Přehrada Orlík", ["Orlík"], (
        "Její vznik zaplavil část Zvíkova a zámek museli o několik desítek metrů vyzdvihnout.",
        "Dokončila se roku 1961 na Vltavě a je součástí kaskády.",
        "Je to největší česká přehradní nádrž podle objemu vody.",
    )),
    ("Poznej techniku.", "QR kód", ["QR"], (
        "Vznikl roku 1994 v Japonsku pro sledování dílů v automobilce Denso Wave, dceřince Toyoty.",
        "Tři čtverce v rozích slouží k tomu, aby si čtečka srovnala natočení.",
        "Naskenuje se telefonem a otevře odkaz nebo zaplatí složenku.",
    )),
    ("Poznej vynález.", "Airbag", [], (
        "Rozvine se rychlostí přes 300 km/h a nafoukne ho chemická reakce, ne stlačený plyn.",
        "První patenty jsou z padesátých let, ale povinný se stal až v devadesátých.",
        "Při nárazu chrání řidiče a vyskočí z volantu.",
    )),
    ("Poznej stroj.", "Kombajn", ["obilní kombajn"], (
        "Jméno pochází z anglického slova pro spojení — sdružuje tři dřív oddělené práce do jedné.",
        "Ty práce jsou žnutí, výmlat a čištění zrna.",
        "Jezdí po poli a sklízí obilí.",
    )),
    ("Poznej vynález.", "Padák", [], (
        "Jeho návrh nakreslil Leonardo da Vinci a roku 2000 podle něj někdo skutečně seskočil.",
        "První skutečný seskok z balonu provedl roku 1797 André-Jacques Garnerin nad Paříží.",
        "Zpomalí pád a vojáci na něm seskakují z letadel.",
    )),
    ("Poznej techniku.", "Wi-Fi", ["wifi"], (
        "Základ pro rozprostřené spektrum patentovala herečka Hedy Lamarrová se skladatelem Georgem Antheilem.",
        "Jméno nic neznamená — vymyslela ho marketingová agentura, aby znělo jako hi-fi.",
        "Připojí telefon k internetu bez kabelu, obvykle přes router.",
    )),
    ("Poznej vozidlo.", "Ponorka", [], (
        "K řízení hloubky slouží nádrže, které se střídavě plní vodou a vytlačují stlačeným vzduchem.",
        "První bojové nasazení proběhlo za americké občanské války a plavidlo se přitom samo potopilo.",
        "Pluje pod hladinou a periskopem se dívá nahoru.",
    )),
    ("Poznej stavbu.", "Maják", [], (
        "Jeden z nich patřil mezi sedm divů světa a stál u Alexandrie.",
        "Jeho světlo se zaostřuje soustavou prstencových čoček, kterou navrhl Augustin Fresnel.",
        "Stojí u pobřeží a v noci varuje lodě před skalami.",
    )),
]

BANK["sport"] += [
    ("Poznej sport.", "Volejbal", [], (
        "Vymyslel ho roku 1895 William Morgan jako mírnější alternativu k basketbalu pro starší pány.",
        "Družstvo má tři doteky a jeden hráč v jiném dresu smí hrát jen v zadní části hřiště.",
        "Hraje se přes vysokou síť a útočí se smečí.",
    )),
    ("Poznej sportovce.", "Roger Federer", ["Federer"], (
        "Jako junior pracoval jako sběrač míčků na turnaji v Basileji, který později osmkrát vyhrál.",
        "Byl to švýcarský tenista, který strávil na prvním místě žebříčku 237 týdnů v řadě.",
        "Vyhrál osm titulů ve Wimbledonu a jeho největšími soupeři byli Nadal a Djokovič.",
    )),
    ("Poznej sport.", "Golf", [], (
        "Míček má na povrchu důlky, protože poškrábaný míček létal dál než hladký.",
        "Skotský parlament ho v 15. století zakázal, protože odváděl muže od lukostřelby.",
        "Cílem je dostat míček do jamky na co nejméně ran a hraje se holemi.",
    )),
    ("Poznej sportovní akci.", "Olympijské hry", ["olympiáda"], (
        "Novodobé obnovil roku 1896 Pierre de Coubertin a první maraton vyhrál řecký vodař Spiridon Louis.",
        "Jejich symbolem je pět kruhů a mottem rychleji, výše, silněji.",
        "Konají se každé čtyři roky a vítěz dostává zlatou medaili.",
    )),
    ("Poznej sportovce.", "Michael Jordan", ["Jordan"], (
        "Na střední škole ho vyřadili ze školního týmu a musel hrát nižší soutěž.",
        "Hrál za Chicago Bulls a s číslem 23 získal šest titulů.",
        "Je považován za nejlepšího basketbalistu historie a nese jeho jméno řada bot.",
    )),
    ("Poznej sport.", "Veslování", [], (
        "Kormidelník bývá nejlehčí člen posádky a jeho hmotnost je pravidly zdola omezená, aby se nešidila.",
        "Závodní lodě se jmenují skif, dvojka nebo osma a jezdí se po sedačkách na kolejničkách.",
        "Nejslavnější závod je každoroční souboj Oxfordu a Cambridge na Temži.",
    )),
    ("Poznej klub.", "Sparta Praha", ["AC Sparta Praha", "Sparta"], (
        "Rudou barvu prý přijala poté, co si její funkcionář přivezl z Anglie dresy, které se mu líbily.",
        "Ve dvacátých letech vyhrála se svým městským rivalem Středoevropský pohár a říkalo se jí Železná.",
        "Hraje na Letné a jejím největším rivalem je pražská Slavia.",
    )),
    ("Poznej sport.", "Krasobruslení", [], (
        "Jméno má po povinných obrazcích, které se dřív vyjížděly do ledu a rozhodčí je chodili obkreslovat.",
        "Body se dnes dělí na technickou hodnotu a na složku za předvedení a hudbu.",
        "Skáče se v něm trojitý axel a v Česku ho proslavila Ája Vrzáňová.",
    )),
    ("Poznej sportovce.", "Pelé", ["Pele", "Edson Arantes do Nascimento"], (
        "Brazilská vláda ho prohlásila za národní poklad, aby ho evropské kluby nemohly koupit.",
        "Přezdívku dostal ve škole zkomolením jména brankáře, kterého obdivoval jeho otec.",
        "Získal tři tituly mistra světa ve fotbale a hrál za Santos.",
    )),
    ("Poznej sport.", "Cyklistika", ["silniční cyklistika"], (
        "Závodníci ve skupině ušetří v závěsu až třicet procent síly, proto se jezdí v pelotonu.",
        "Její tři velké etapové závody se jezdí ve Francii, Itálii a Španělsku.",
        "Jezdí se na kolech a nejslavnější závod je Tour de France.",
    )),
    ("Poznej sportovkyni.", "Barbora Špotáková", ["Špotáková"], (
        "Začínala jako sedmibojařka a k jedné disciplíně se upnula až po zranění.",
        "Získala olympijské zlato v Pekingu i v Londýně a světový rekord hodila roku 2008.",
        "Je to česká oštěpařka, která má na krku dvě olympijská zlata.",
    )),
    ("Poznej sport.", "Vzpírání", [], (
        "Soutěží se ve dvou disciplínách — v jedné jde činka nahoru jedním pohybem, ve druhé se cestou opře o ramena.",
        "Ty disciplíny se jmenují trh a nadhoz a závodí se v hmotnostních kategoriích.",
        "Zvedá se v něm těžká činka nad hlavu a v Československu ho proslavil Ota Zaremba.",
    )),
    ("Poznej trofej.", "Zlatý míč", ["Ballon d'Or"], (
        "Uděluje ho od roku 1956 francouzský časopis France Football a dlouho ho mohli získat jen Evropané.",
        "Prvním držitelem byl Angličan Stanley Matthews a nejvíc jich má Lionel Messi.",
        "Dostává ho nejlepší fotbalista roku a jednou ho získal i Čechoslovák.",
    )),
    ("Poznej sport.", "Lukostřelba", [], (
        "Závodní luk má stabilizátory a mířidla, takže s historickou zbraní má společný jen princip.",
        "Střílí se na terč s deseti kruhy ze vzdálenosti sedmdesáti metrů.",
        "Nejvíc olympijských medailí v ní posbírala Jižní Korea.",
    )),
    ("Poznej sportovce.", "Petr Čech", ["Čech"], (
        "Po zranění hlavy roku 2006 začal nosit ochrannou přilbu, kterou už nikdy neodložil.",
        "Chytal za Chelsea a Arsenal a je rekordmanem v počtu čistých kont Premier League.",
        "Je to český brankář a dnes hraje pro zábavu i hokej.",
    )),
    ("Poznej sport.", "Plavání", [], (
        "Nejrychlejší způsob není ten, který se učí jako první — kraul se v závodech objevil až kolem roku 1900.",
        "Závodí se ve čtyřech způsobech a v polohovém závodě se jdou všechny za sebou.",
        "Nejúspěšnějším olympionikem všech dob je v něm Michael Phelps.",
    )),
    ("Poznej klub.", "FC Barcelona", ["Barcelona", "Barca", "Barça"], (
        "Dlouho jako jediný velký klub neměl na dresu placenou reklamu a naopak platil UNICEF za to, že tam být smělo.",
        "Hraje na stadionu Camp Nou a jeho fanoušci jsou zároveň jeho majiteli.",
        "Vychoval Lionela Messiho a jeho úhlavním sokem je Real Madrid.",
    )),
    ("Poznej sport.", "Horolezectví", ["alpinismus"], (
        "Za jeho zrod se považuje výstup na Mont Blanc roku 1786, který podnítila vypsaná odměna.",
        "Rozlišuje se v něm sportovní lezení na skalách a výškové výstupy v horách.",
        "Nejtěžší metou je čtrnáct osmitisícovek a v Česku ho proslavil Radek Jaroš.",
    )),
    ("Poznej sportovkyni.", "Kateřina Neumannová", ["Neumannová"], (
        "Kromě zimního sportu závodila i na horském kole a startovala na letní olympiádě.",
        "Zlato získala až na páté olympiádě, v Turíně roku 2006 na třicetikilometrové trati.",
        "Je to česká běžkyně na lyžích a později šéfka organizace zimních závodů.",
    )),
    ("Poznej sport.", "Basketbal", [], (
        "Vymyslel ho roku 1891 James Naismith a místo koše se zpočátku používal skutečný košík na broskve.",
        "Hraje pět hráčů na každé straně a útok má na zakončení čtyřiadvacet sekund.",
        "Míč se hází do koše ve výšce 305 centimetrů a nejslavnější soutěž je NBA.",
    )),
]

BANK["jazyk"] += [
    ("Poznej jazyk.", "Čínština", ["mandarínština"], (
        "Její znaky nejsou obrázky, ale z většiny složeniny, kde jedna část napovídá význam a druhá výslovnost.",
        "Je to jazyk s nejvíce rodilými mluvčími na světě a v jedné jeho podobě rozlišuje čtyři tóny.",
        "Píše se znaky a v její zjednodušené podobě se učí v Číně.",
    )),
    ("Poznej slovo podle původu.", "Dolar", [], (
        "Kořen je v názvu údolí v Krušných horách, kde se v 16. století razila stříbrná mince.",
        "Ta mince se jmenovala tolar a přes nizozemštinu se dostala do angličtiny.",
        "Dnes je to měna Spojených států a jeho značka je přeškrtnuté S.",
    )),
    ("Poznej jev.", "Diakritika", ["diakritická znaménka"], (
        "Do češtiny ji podle tradice zavedl Jan Hus, aby nahradil spřežky jako cz nebo rz.",
        "Patří sem háček, čárka a kroužek nad písmenem.",
        "Bez ní by se z „kůň“ stalo „kun“ a z „šest“ „sest“.",
    )),
    ("Poznej slovo.", "Kalhoty", [], (
        "Do češtiny se dostalo z německého Kaltehose, tedy doslova studené nohavice.",
        "Ve staré češtině se pro tenhle kus oděvu užívalo slovo nohavice.",
        "Nosí se na dolní polovině těla a mají dvě nohavice.",
    )),
    ("Poznej termín.", "Eufemismus", [], (
        "Řecký původ slova znamená doslova „dobře mluvit“ a jeho opakem je dysfemismus.",
        "Používá ho úřední jazyk, když místo propouštění mluví o optimalizaci.",
        "Je to zjemnění — místo „zemřel“ se řekne „odešel“.",
    )),
    ("Poznej jazyk.", "Hebrejština", ["ivrit"], (
        "Přes tisíc let se jí nemluvilo v běžném životě a oživil ji na konci 19. století Eliezer Ben Jehuda.",
        "Píše se zprava doleva a v běžném textu se samohlásky nezapisují.",
        "Je to úřední jazyk Izraele a jazyk Starého zákona.",
    )),
    ("Poznej pravopisný jev.", "Shoda podmětu s přísudkem", ["shoda přísudku s podmětem", "shoda"], (
        "Když se v několikanásobném vyjádření děje sejde rod mužský životný s jinými, má přednost — a právě tohle se dnes zpochybňuje.",
        "Rozhoduje o tom, jestli se na konci minulého času píše tvrdé nebo měkké i.",
        "Kvůli ní se píše „ženy nesly“, ale „muži nesli“.",
    )),
    ("Poznej slovo podle původu.", "Šle", ["šle", "kšandy"], (
        "Slovo je přejaté z německého Gestell, tedy podpěra nebo kostra.",
        "Označuje dvojici popruhů přes ramena, na kterých se něco drží.",
        "Nosí se místo pásku, aby kalhoty nespadly, a k fraku patří bílé.",
    )),
    ("Poznej jazyk.", "Slovenština", ["slovensky"], (
        "Její dnešní podobu ustálil v 19. století Ľudovít Štúr; předtím se o kodifikaci pokusil Anton Bernolák a neujalo se to.",
        "Má samohlásku, kterou čeština nezná, a měkčí výslovnost než čeština.",
        "Je jí velmi blízko čeština a ve společném státě to byl druhý úřední jazyk.",
    )),
    ("Poznej jev.", "Metafora", [], (
        "Aristoteles ji považoval za nejtěžší dovednost básníka, protože se jí prý nedá naučit.",
        "Přenáší význam na základě podobnosti, na rozdíl od metonymie, která přenáší podle souvislosti.",
        "Když se řekne „moře slz“, je to ona.",
    )),
    ("Poznej termín.", "Neologismus", ["neologismy"], (
        "Slovníky ho zařadí až tehdy, když se drží v úzu několik let; jinak jde jen o okazionalismus.",
        "V češtině jich hodně vzniklo v době národního obrození zásluhou Josefa Jungmanna.",
        "Je to nově vzniklé slovo — třeba selfie nebo mikroplast.",
    )),
    ("Poznej abecedu.", "Morseova abeceda", ["morseovka", "Morse"], (
        "Délky značek nejsou náhodné — nejkratší dostala písmena, která jsou v angličtině nejčastější.",
        "Skládá se z teček a čárek a přenášela se telegrafem, světlem i klepáním.",
        "Nouzový signál SOS se v ní vysílá jako tři tečky, tři čárky, tři tečky.",
    )),
    ("Poznej jazyk.", "Arabština", [], (
        "Spisovná podoba se od mluvených nářečí liší tak, že si mluvčí ze dvou zemí nemusí rozumět.",
        "Píše se zprava doleva a její písmena mění tvar podle pozice ve slově.",
        "Je jazykem Koránu a mluví se jí od Maroka po Irák.",
    )),
    ("Poznej termín.", "Onomatopoie", ["zvukomalba", "onomatopoia"], (
        "V různých jazycích zní odlišně — kohout v češtině kikiriká, v angličtině cock-a-doodle-doo.",
        "Jazykovědci ji uvádějí jako výjimku z pravidla, že vztah mezi slovem a věcí je libovolný.",
        "Patří sem „bum“, „mňau“ nebo „šplouchat“.",
    )),
    ("Poznej slovo podle původu.", "Havárie", [], (
        "Přes francouzštinu a italštinu pochází z arabského slova pro poškozené zboží.",
        "Původně to byl obchodní pojem z námořního práva o škodě na nákladu.",
        "Dnes tak říkáme dopravní nehodě nebo poruše v elektrárně.",
    )),
    ("Poznej jev.", "Přechodník", ["přechodníky"], (
        "V češtině má tvary pro přítomnost i minulost a rozlišuje rod, což bývá důvod, proč se používá špatně.",
        "Ve starších textech je běžný, v dnešní mluvě působí knižně až komicky.",
        "Zní třeba „jda“, „vidouc“ nebo „přišedši“.",
    )),
    ("Poznej písmo.", "Klínové písmo", ["klínopis"], (
        "Rozluštit ho pomohl nápis vytesaný na skále v Behistúnu, který nesl týž text ve třech jazycích.",
        "Vzniklo v Mezopotámii a psalo se rákosovým rydlem do vlhké hliněné tabulky.",
        "Znaky vypadají jako otisky klínu a je v něm zapsán epos o Gilgamešovi.",
    )),
    ("Poznej termín.", "Synonymum", [], (
        "Dokonalá dvojice prakticky neexistuje — slova se skoro vždycky liší citovým zabarvením nebo užitím.",
        "Slovník, který je shromažďuje, se v angličtině jmenuje thesaurus.",
        "Jsou to slova s podobným významem, třeba „dům“ a „stavení“.",
    )),
    ("Poznej jazyk.", "Finština", ["finsky"], (
        "Nepatří k indoevropským jazykům a nejbližší větší příbuzný je estonština a vzdáleněji maďarština.",
        "Má patnáct pádů a nezná rod, takže nerozlišuje on a ona.",
        "Mluví se jí v zemi tisíce jezer a v její abecedě jsou dvojtečky nad písmeny.",
    )),
    ("Poznej slovo podle původu.", "Neděle", ["nedele"], (
        "Ve staré češtině stálo na začátku týdne a den následující se jmenoval prostě „po ní“.",
        "Vzniklo od zákazu práce a stejný původ má i ruské „voskresenije“, byť z jiného obrazu.",
        "Dnes je to podle normy sedmý den týdne a bývá dnem volna.",
    )),
]

BANK["spolecnost"] += [
    ("Poznej pojem.", "Recyklace", [], (
        "Hliník se dá vracet do oběhu prakticky donekonečna a ušetří přitom pětadevadesát procent energie oproti výrobě z rudy.",
        "V Česku se odpad třídí do barevných kontejnerů a zálohování PET lahví se teprve zavádí.",
        "Je to znovuvyužití odpadu a jejím symbolem jsou tři šipky do trojúhelníku.",
    )),
    ("Poznej instituci.", "Světová zdravotnická organizace", ["WHO"], (
        "Za svůj největší úspěch považuje vymýcení jedné nemoci, u níž se poslední přirozený případ objevil roku 1977.",
        "Sídlí v Ženevě a vznikla roku 1948 jako součást soustavy OSN.",
        "V roce 2020 vyhlásila pandemii covidu-19.",
    )),
    ("Poznej pojem.", "Hypotéka", [], (
        "Slovo pochází z řeckého výrazu pro podklad; ve starém Řecku se název pro zástavu vytesal na kámen na pozemku.",
        "Splácí se desítky let a věřitel má právo prodat zastavenou věc, když dlužník neplatí.",
        "Bere se na koupi bytu nebo domu a ručí se jím samotná nemovitost.",
    )),
    ("Poznej svátek.", "Vánoce", [], (
        "Datum se ustálilo ve 4. století a splynulo se slavností nepřemožitelného Slunce.",
        "V Česku se hlavní část odehrává 24. prosince, ve většině světa až následující den.",
        "Zdobí se stromeček a naděluje se pod ním.",
    )),
    ("Poznej pojem.", "Cenzura", [], (
        "Slovo pochází od římského úřadu, který původně vedl soupis obyvatel a dohlížel na mravy.",
        "Ve starém Rakousku existoval seznam zakázaných knih a v Československu ji formálně zrušili roku 1968.",
        "Je to zásah, který brání vyjít textu nebo filmu.",
    )),
    ("Poznej organizaci.", "Amnesty International", ["Amnesty"], (
        "Vznikla roku 1961 po novinovém článku o dvou portugalských studentech uvězněných za přípitek na svobodu.",
        "Jejím znakem je svíčka obtočená ostnatým drátem a roku 1977 dostala Nobelovu cenu míru.",
        "Zastává se vězňů svědomí po celém světě.",
    )),
    ("Poznej pojem.", "Nezaměstnanost", [], (
        "Statistika za nezaměstnaného považuje jen toho, kdo práci aktivně hledá a je schopen nastoupit.",
        "Rozlišuje se její frikční, strukturální a cyklická podoba.",
        "Měří se v procentech a v jejím důsledku se vyplácí podpora.",
    )),
    ("Poznej pojem.", "Právní stát", ["vláda práva"], (
        "Jeho jádrem je, že moc je vázána zákonem stejně jako občan a soudy jsou nezávislé.",
        "Německy se mu říká Rechtsstaat a v anglosaském světě rule of law.",
        "Znamená, že nikdo není nad zákonem — ani prezident, ani ministr.",
    )),
    ("Poznej tradici.", "Pouť", ["poutě"], (
        "Původně to bylo výročí posvěcení kostela a teprve později se z ní stala zábava s kolotoči.",
        "V Česku k ní patří perník, střelnice a řetízkový kolotoč.",
        "Přijede na náves jednou za rok a vozí se na ní na houpačkách.",
    )),
    ("Poznej pojem.", "Referendum", [], (
        "V Česku proběhlo celostátní zatím jediné, roku 2003, a rozhodovalo se v něm o vstupu do unie.",
        "Ve Švýcarsku se koná několikrát ročně a lidé v něm rozhodují i o zdanění.",
        "Je to hlasování všech občanů o jedné otázce.",
    )),
    ("Poznej instituci.", "Ústavní soud", [], (
        "Jeho patnáct členů jmenuje prezident se souhlasem Senátu na deset let a týž člověk to nesmí dělat dvakrát po sobě.",
        "Sídlí v Brně a obrátit se na něj může i jednotlivec, když vyčerpal všechny ostatní možnosti.",
        "Může zrušit zákon, který schválil parlament, pokud odporuje nejvyšší normě státu.",
    )),
    ("Poznej pojem.", "Občanská neposlušnost", [], (
        "Pojem zpopularizoval americký myslitel Henry David Thoreau esejí z roku 1849, když odmítl platit daň.",
        "Její podstatou je vědomé porušení zákona spojené s přijetím trestu, aby se ukázala jeho nespravedlnost.",
        "Použil ji Gándhí i Martin Luther King.",
    )),
    ("Poznej svátek.", "Den boje za svobodu a demokracii", ["17. listopad"], (
        "Připomíná dvě události s odstupem padesáti let, obě spojené se studenty.",
        "Roku 1939 po něm nacisté uzavřeli české vysoké školy a devět lidí popravili.",
        "Roku 1989 se v ten den rozběhla sametová revoluce.",
    )),
    ("Poznej pojem.", "Daň z přidané hodnoty", ["DPH"], (
        "Odvádí se v každém článku řetězce, ale jen z rozdílu mezi nákupem a prodejem — proto ten název.",
        "V Česku má základní a sníženou sazbu a platí ji nakonec spotřebitel.",
        "Je zahrnutá v ceně na účtence a její zkratka má tři písmena.",
    )),
    ("Poznej instituci.", "Senát", ["senát"], (
        "Třetina jeho členů se obměňuje každé dva roky, takže se nikdy nevolí celý najednou.",
        "Vznikl roku 1996 a sídlí ve Valdštejnském paláci v Praze.",
        "Je to horní komora českého parlamentu s jednaosmdesáti členy.",
    )),
    ("Poznej pojem.", "Charita", ["dobročinnost"], (
        "Slovo pochází z latinského caritas, tedy láska k bližnímu, a v katolické nauce patří mezi tři božské ctnosti.",
        "V Česku se s ní pojí Tříkrálová sbírka na začátku ledna.",
        "Je to pomoc potřebným, ať už penězi nebo prací zdarma.",
    )),
    ("Poznej tradici.", "Svatba", [], (
        "Prsten se nosí na čtvrtém prstu podle staré představy, že odtud vede žíla přímo k srdci.",
        "V Česku ji uzavírá starosta nebo oddávající a snoubenci si vyměňují prsteny.",
        "Nevěsta bývá v bílém a hází se za ni kytice.",
    )),
    ("Poznej pojem.", "Veřejnoprávní médium", ["veřejnoprávní média"], (
        "V Česku ho neplatí stát z rozpočtu, ale domácnosti přímým poplatkem, aby na něm vláda neměla páku.",
        "Dohlíží na ně rada volená sněmovnou a jeho vzorem bývá britská BBC.",
        "Patří sem Česká televize a Český rozhlas.",
    )),
    ("Poznej pojem.", "Očkování", ["vakcinace"], (
        "Slovo pochází z latinského vacca, tedy kráva — první látku získal Edward Jenner z neštovic dojiček.",
        "Funguje tak, že se tělu ukáže neškodná část choroboplodného zárodku a ono si vytvoří paměť.",
        "Díky němu vymizely pravé neštovice a dětem se dává v prvních letech života.",
    )),
    ("Poznej pojem.", "Kolektivní vyjednávání", ["odbory"], (
        "Právo na ně zaručuje Listina základních práv a svobod a jeho výsledkem je smlouva platná pro celý podnik.",
        "Vede ho zástupce zaměstnanců se zaměstnavatelem o mzdách a pracovních podmínkách.",
        "Krajní zbraní v něm bývá stávka.",
    )),
]

# ==========================================================================
# Třetí dávka
# ==========================================================================

BANK["osobnost"] += [
    ("Poznej známou osobnost.", "Ema Destinnová", ["Destinnová"], (
        "Za války jí Rakousko zabavilo pas a musela zůstat na svém jihočeském zámku ve Stráži nad Nežárkou.",
        "Umělecké jméno si vzala po své učitelce zpěvu Marii Loewe-Destinn.",
        "Byla to světoznámá sopranistka a její podobizna byla na dvoutisícové bankovce.",
    )),
    ("Poznej známou osobnost.", "Ernest Hemingway", ["Hemingway"], (
        "Přežil dvě letecké havárie během dvou dnů a noviny mezitím otiskly jeho nekrology.",
        "Byl to americký spisovatel, který pracoval jako novinář ve Španělsku i na Kubě.",
        "Napsal Stařec a moře a Komu zvoní hrana.",
    )),
    ("Poznej známou osobnost.", "Otto Wichterle", ["Wichterle"], (
        "Za války ho zavřelo gestapo a po roce 1968 ho vyhodili z ústavu, který sám vybudoval.",
        "Byl to český chemik, který vynalezl silon a stál u zrodu makromolekulární chemie u nás.",
        "Nejznámější vynález mu vznikl doma na dětské stavebnici Merkur — měkké kontaktní čočky.",
    )),
    ("Poznej známou osobnost.", "Steve Jobs", ["Jobs"], (
        "Chodil na kurz kaligrafie, který podle vlastních slov rozhodl o tom, jak budou vypadat počítačová písma.",
        "Z firmy, kterou spoluzaložil, ho roku 1985 vyhodili a po jedenácti letech se vrátil.",
        "Uvedl na trh iPod, iPhone a iPad a nosil černý rolák.",
    )),
    ("Poznej známou osobnost.", "Ludvík Svoboda", ["Svoboda"], (
        "Za první světové války bojoval v československých legiích v Rusku a po druhé velel armádnímu sboru.",
        "Byl to generál, kterého v padesátých letech odsunuli do JZD v Kroměříži jako účetního.",
        "V letech 1968 až 1975 byl československým prezidentem.",
    )),
    ("Poznej známou osobnost.", "Marie Antoinetta", ["Marie Antoinette"], (
        "Byla nejmladší dcerou rakouské císařovny a do Francie ji provdali ve čtrnácti letech.",
        "Nechala si v zahradě Versailles postavit selskou vesničku, kde si hrála na pastýřku.",
        "Skončila pod gilotinou a připisuje se jí věta o koláčích, kterou nikdy neřekla.",
    )),
    ("Poznej známou osobnost.", "Jan Neruda", ["Neruda"], (
        "Bydlel na Malé Straně v domě U dvou slunců a živil se hlavně novinařinou.",
        "Byl to český básník a fejetonista, po kterém si vzal jméno chilský nositel Nobelovy ceny.",
        "Napsal Povídky malostranské a báseň Romance o Karlu IV.",
    )),
    ("Poznej známou osobnost.", "Albert Einstein", ["Einstein"], (
        "Pracoval jako úředník patentového úřadu v Bernu, když vydal čtyři práce, které převrátily fyziku.",
        "Nabídli mu roku 1952 funkci izraelského prezidenta a on ji odmítl.",
        "Nobelovu cenu dostal za fotoelektrický jev a nejznámější je jeho vzorec o hmotě a energii.",
    )),
    ("Poznej známou osobnost.", "Matka Tereza", ["Tereza z Kalkaty"], (
        "Narodila se v dnešní Severní Makedonii v albánské rodině a do Indie odjela v osmnácti.",
        "Založila kongregaci Misionářek lásky a roku 1979 dostala Nobelovu cenu míru.",
        "Starala se o umírající v indickém velkoměstě na Ganze a papež ji roku 2016 prohlásil za svatou.",
    )),
    ("Poznej známou osobnost.", "Jaroslav Heyrovský", ["Heyrovský"], (
        "Za války musel z fakulty odejít, protože byly české vysoké školy zavřené, a bádal v soukromí.",
        "Byl to český fyzikální chemik, který svou metodu objevil roku 1922 při práci s rtuťovou kapkou.",
        "Za polarografii dostal roku 1959 jako první Čech Nobelovu cenu za chemii.",
    )),
    ("Poznej známou osobnost.", "Cleopatra", ["Kleopatra", "Kleopatra VII."], (
        "Byla řeckého původu a z celé své dynastie prý jako jediná uměla egyptsky.",
        "Vládla v Alexandrii a měla děti s Caesarem i s Marcem Antoniem.",
        "Podle tradice se zabila kousnutím hada a byla poslední egyptskou vládkyní.",
    )),
    ("Poznej známou osobnost.", "Josef Čapek", ["Čapek"], (
        "Zemřel roku 1945 v Bergen-Belsenu a jeho hrob se nikdy nenašel.",
        "Byl to malíř a spisovatel, který svému mladšímu bratrovi poradil slovo robot.",
        "Napsal a ilustroval Povídání o pejskovi a kočičce.",
    )),
    ("Poznej známou osobnost.", "Alexandr Veliký", ["Alexandr Makedonský", "Alexandr Veliký"], (
        "Jeho učitelem byl Aristoteles a svého koně Bukefala prý zkrotil jako chlapec.",
        "Do třiatřiceti let dobyl říši od Řecka po Indii a zakládal města nesoucí jeho jméno.",
        "Podle pověsti rozťal gordický uzel mečem, místo aby ho rozvazoval.",
    )),
    ("Poznej známou osobnost.", "Zdeněk Svěrák", ["Svěrák"], (
        "Původním povoláním byl učitel češtiny a ruštiny na základní škole v Měcholupech.",
        "Spoluzaložil divadlo, které uvádí hry o fiktivním českém géniovi.",
        "Napsal scénář ke Kolji, za který získal Oscara, a zpívá s Jaroslavem Uhlířem.",
    )),
    ("Poznej známou osobnost.", "Vladimír Remek", ["Remek"], (
        "Vystudoval leteckou akademii v Košicích a později byl poslancem Evropského parlamentu i velvyslancem v Moskvě.",
        "Letěl roku 1978 na palubě Sojuzu 28 a strávil ve vesmíru necelých osm dní.",
        "Byl prvním člověkem ve vesmíru, který nepocházel ze Sovětského svazu ani z USA.",
    )),
    ("Poznej známou osobnost.", "Coco Chanel", ["Chanel", "Gabrielle Chanel"], (
        "Vyrůstala v sirotčinci u jeptišek a přezdívku prý získala podle písničky, kterou zpívala v kabaretu.",
        "Osvobodila ženy od korzetu a prosadila kalhoty i jednoduché černé šaty.",
        "Nese její jméno parfém s číslem pět.",
    )),
    ("Poznej známou osobnost.", "Jiří Voskovec", ["Voskovec"], (
        "V Americe si zkrátil jméno na George a hrál v porotě filmu Dvanáct rozhněvaných mužů.",
        "Po roce 1948 zůstal v emigraci a jedenáct měsíců ho drželi na Ellis Islandu.",
        "Tvořil s Janem Werichem slavnou dvojici prvorepublikového Osvobozeného divadla.",
    )),
    ("Poznej známou osobnost.", "Tycho Brahe", ["Brahe"], (
        "V souboji přišel o kus nosu a nosil protézu ze slitiny kovů; rozbor jeho vousů vyloučil otravu.",
        "Byl to dánský astronom, který svá nejlepší měření pořídil ještě před vynálezem dalekohledu.",
        "Zemřel roku 1601 v Praze a jeho data použil Johannes Kepler.",
    )),
    ("Poznej známou osobnost.", "Emil Škoda", ["Škoda"], (
        "Roku 1869 koupil strojírnu v Plzni, kde do té doby působil jako vrchní inženýr.",
        "Jeho podnik vyráběl ocelové odlitky, cukrovary a později děla pro rakouskou armádu.",
        "Nese jeho jméno automobilka i plzeňský průmyslový podnik.",
    )),
    ("Poznej známou osobnost.", "Rosalind Franklinová", ["Rosalind Franklin", "Franklinová"], (
        "Zemřela roku 1958 ve věku sedmatřiceti let na rakovinu vaječníků, patrně od rentgenového záření.",
        "Její rentgenový snímek číslo 51 rozhodl o rozluštění struktury dědičné informace.",
        "Nobelovu cenu za to dostali Watson, Crick a Wilkins — ona ne, protože se uděluje jen žijícím.",
    )),
]

BANK["zemepis"] += [
    ("Poznej stát.", "Norsko", [], (
        "Jeho svrchovaný fond, plněný z ropných příjmů, vlastní zhruba procento a půl všech akcií na světě.",
        "Táhne se podél pobřeží s tisíci zálivy a k jeho území patří i Špicberky.",
        "Jeho hlavním městem je Oslo a proslulo fjordy a lososem.",
    )),
    ("Poznej město.", "Jeruzalém", [], (
        "Klíč od Chrámu Božího hrobu drží po staletí dvě muslimské rodiny, aby se křesťanské církve nehádaly.",
        "Je posvátným městem pro tři náboženství a jeho staré město dělí čtyři čtvrti.",
        "Stojí tu Zeď nářků a Skalní dóm se zlatou kupolí.",
    )),
    ("Poznej stát.", "Nizozemsko", ["Holandsko"], (
        "Čtvrtina jeho území leží pod hladinou moře a nejnižší bod je skoro sedm metrů pod ní.",
        "Po povodni roku 1953 postavilo obří systém hrází a vrat zvaný Deltaplán.",
        "Jeho symbolem jsou tulipány, větrné mlýny a kola.",
    )),
    ("Poznej pohoří.", "Alpy", [], (
        "Roku 1991 v jejich ledovci našli mumii muže, který tam zemřel před více než pěti tisíci lety.",
        "Rozkládají se přes osm států a nejvyšší vrchol Mont Blanc měří 4 808 metrů.",
        "Jezdí se v nich na lyžích a vede jimi průsmyk Brenner.",
    )),
    ("Poznej řeku.", "Mississippi", [], (
        "Její jméno pochází z jazyka Odžibvejů a znamená velká řeka.",
        "Ústí do Mexického zálivu rozsáhlou deltou a její tok stabilizuje soustava hrází.",
        "Plují po ní kolesové parníky a psal o ní Mark Twain.",
    )),
    ("Poznej stát.", "Irsko", [], (
        "Nežijí tu žádní hadi a legenda to připisuje svatému Patrikovi; ve skutečnosti se sem po době ledové nedostali.",
        "Jeho úředními jazyky jsou angličtina a irština a hlavním městem Dublin.",
        "Jeho symbolem je trojlístek a zelená barva.",
    )),
    ("Poznej jezero.", "Ženevské jezero", ["Lac Léman", "Léman"], (
        "Vede jeho středem státní hranice a jeho fontána stříká vodu do výšky 140 metrů.",
        "Leží mezi Švýcarskem a Francií a protéká jím Rhôna.",
        "Na jeho břehu sídlí OSN a Mezinárodní olympijský výbor.",
    )),
    ("Poznej stát.", "Peru", [], (
        "Nazca linie na jeho pobřežní poušti jsou vidět jen ze vzduchu a jejich smysl se dohaduje.",
        "Leží v něm část Amazonie i vysoké Andy a mluví se tu i kečuánsky.",
        "Stojí tu Machu Picchu a byla to říše Inků.",
    )),
    ("Poznej české pohoří.", "Šumava", [], (
        "Její jezera vznikla v ledovcových karech a největší z nich, Černé, je nejrozsáhlejší v Česku.",
        "Je to největší český národní park a spory se v ní vedou o to, jak nakládat s kůrovcem.",
        "Pramení tu Vltava a leží tu Boubín s pralesem.",
    )),
    ("Poznej ostrov.", "Kuba", [], (
        "Její dva hlavní vývozní artikly, cukr a doutníky, stály na plantážích s otrockou prací až do roku 1886.",
        "Leží devadesát mil od Floridy a od roku 1959 tu vládl jeden režim šest desetiletí.",
        "Jejím hlavním městem je Havana a proslula rumem a starými americkými auty.",
    )),
    ("Poznej stát.", "Rakousko", [], (
        "Jeho stálou neutralitu zakotvil zákon z roku 1955, kdy odsud odešly okupační armády.",
        "Devět spolkových zemí, hlavní město na Dunaji a hranice s osmi státy.",
        "Leží v něm Alpy, Vídeň a Salcburk, kde se narodil Mozart.",
    )),
    ("Poznej horu.", "Matterhorn", ["Cervino"], (
        "Při prvním výstupu roku 1865 se cestou dolů přetrhlo lano a čtyři z nich zahynuli.",
        "Stojí na hranici Švýcarska a Itálie nad městečkem Zermatt.",
        "Má nezaměnitelný jehlanovitý tvar a je na obalu čokolády Toblerone.",
    )),
    ("Poznej město.", "Vídeň", [], (
        "Její obyvatelé pijí vodu přivedenou samospádem z hor přes sto kilometrů dlouhými vodovody z 19. století.",
        "Leží na Dunaji a v žebříčcích kvality života se pravidelně umísťuje na prvních místech.",
        "Sídlil tu císařský dvůr, stojí tu Schönbrunn a hraje se tu novoroční koncert.",
    )),
    ("Poznej stát.", "Jihoafrická republika", ["JAR"], (
        "Má tři hlavní města — každé pro jinou moc ve státě — a jedenáct úředních jazyků.",
        "Leží na jižním cípu Afriky a její vlajka má šest barev.",
        "Skončil tu apartheid a prvním černošským prezidentem byl Nelson Mandela.",
    )),
    ("Poznej řeku.", "Labe", [], (
        "V Hřensku, kde opouští Česko, je nejnižší bod země — 115 metrů nad mořem.",
        "Pramení v Krkonoších a v Německu se jmenuje Elbe.",
        "Je to hlavní česká řeka a ústí do Severního moře u Hamburku.",
    )),
    ("Poznej město.", "Dubaj", ["Dubai"], (
        "Ropa dnes tvoří jen několik procent jeho hospodářství; zbytek jsou obchod, doprava a turistika.",
        "Leží ve Spojených arabských emirátech a jeho letiště patří k nejvytíženějším na světě.",
        "Stojí tu Burdž Chalífa, nejvyšší budova světa, a umělé ostrovy ve tvaru palmy.",
    )),
    ("Poznej stát.", "Řecko", [], (
        "Má přes šest tisíc ostrovů, ale trvale obydleno je jich jen kolem dvou set.",
        "Jeho vlajka má devět pruhů podle slabik hesla o svobodě nebo smrti.",
        "Odsud pochází demokracie a olympijské hry a hlavním městem jsou Atény.",
    )),
    ("Poznej pouštní oblast.", "Antarktida", [], (
        "Formálně je to poušť — na většině území spadne méně srážek než na Sahaře.",
        "Nemá stálé obyvatele a mezinárodní smlouva z roku 1959 tu zakazuje vojenskou činnost i těžbu.",
        "Je to nejjižnější světadíl a žijí tu tučňáci.",
    )),
    ("Poznej město.", "Krakov", ["Kraków"], (
        "Z věže mariánského kostela zaznívá každou hodinu signál, který se láme uprostřed na památku zabitého trubače.",
        "Bylo to dřívější hlavní město Polska a jeho univerzita je jedna z nejstarších v Evropě.",
        "Nedaleko leží Osvětim a solný důl ve Věličce.",
    )),
    ("Poznej stát.", "Vietnam", [], (
        "Je největším vývozcem kávy robusta na světě, ačkoli sám je zemí čaje.",
        "Táhne se v úzkém pásu podél pobřeží a jeho tvar bývá přirovnáván k rameni s nůší.",
        "V Česku tu žije početná komunita a hlavním městem je Hanoj.",
    )),
]

BANK["veda"] += [
    ("Poznej chemický prvek.", "Kyslík", ["O"], (
        "Objevili ho nezávisle na sobě dva badatelé a jeho jméno, znamenající „tvořící kyseliny“, vzniklo z omylu.",
        "Tvoří pětinu vzduchu a v zemské kůře je vůbec nejrozšířenějším prvkem.",
        "Bez něj se nedýchá a s vodíkem dává vodu.",
    )),
    ("Poznej vesmírné těleso.", "Mars", [], (
        "Jeho dva měsíce se jmenují Hrůza a Děs a ten větší se pomalu blíží k planetě, až se jednou rozpadne.",
        "Stojí na něm sopka Olympus Mons, nejvyšší v celé sluneční soustavě.",
        "Barví ho oxidy železa do červena a jezdí po něm americká vozítka.",
    )),
    ("Poznej jednotku.", "Kelvin", ["K"], (
        "Jako jediná ze základních jednotek SI se od roku 1968 píše bez slova stupeň.",
        "Její nula leží na úplném dně teplotní škály, kde ustává tepelný pohyb.",
        "Přepočítá se na Celsia odečtením 273,15.",
    )),
    ("Poznej vědce.", "Archimédés", ["Archimedes"], (
        "Podle vyprávění ho zabil římský voják při dobývání Syrakus, když počítal obrazce v písku.",
        "Sestrojil válec, kterým se dodnes čerpá voda, a údajně pomáhal bránit město stroji.",
        "Do vany a ven z ní; nese jeho jméno zákon o vztlaku a volání „heuréka“.",
    )),
    ("Poznej jev.", "Gravitace", ["tíže", "gravitační síla"], (
        "Je zdaleka nejslabší ze čtyř základních sil — magnet na ledničce ji přebije celou planetou.",
        "Ohýbá i světlo, což potvrdilo pozorování zatmění roku 1919.",
        "Kvůli ní padají jablka a Země obíhá kolem Slunce.",
    )),
    ("Poznej lidský orgán.", "Ledviny", ["ledvina"], (
        "Denně přefiltrují kolem 180 litrů tekutiny, ale skoro všechno vrátí zpět do těla.",
        "Vyrábějí hormon, který nutí kostní dřeň tvořit červené krvinky.",
        "Když selžou, chodí pacient na dialýzu; člověk vystačí i s jednou.",
    )),
    ("Poznej živočicha.", "Krokodýl", ["krokodýli"], (
        "Nedokáže žvýkat, proto potravu trhá otáčením kolem osy, kterému se říká smrtící váleček.",
        "Pohlaví mláďat určuje teplota, při které se vejce ve hnízdě zahřívá.",
        "Má nejsilnější skus ze všech zvířat a plave v Nilu i v Austrálii.",
    )),
    ("Poznej materiál.", "Guma", ["kaučuk"], (
        "Přírodní podobu se podařilo zbavit lepivosti roku 1839, když Charles Goodyear omylem upustil směs se sírou na kamna.",
        "Ten proces se jmenuje vulkanizace a získává se z mléčné šťávy tropického stromu.",
        "Jsou z ní pneumatiky a gumičky do vlasů.",
    )),
    ("Poznej jev.", "Statická elektřina", ["statická elektřina", "elektrostatika"], (
        "Její pořadí popisuje takzvaná triboelektrická řada, která říká, který materiál se nabije kladně a který záporně.",
        "Vzniká třením a je příčinou blesku ve velkém měřítku.",
        "Kvůli ní se vlasy postaví po přejetí nafouknutým balonkem.",
    )),
    ("Poznej vědce.", "Dmitrij Mendělejev", ["Mendělejev"], (
        "Byl nejmladší ze čtrnácti dětí a matka s ním kvůli studiu přejela půl Ruska.",
        "Ve své tabulce nechal prázdná místa a předpověděl vlastnosti prvků, které ještě nikdo neznal.",
        "Nese jeho jméno periodická soustava prvků i prvek s číslem 101.",
    )),
    ("Poznej lidskou soustavu.", "Nervová soustava", ["nervy"], (
        "Signál se v ní šíří po myelinizovaném vlákně rychlostí přes sto metrů za sekundu, ale jinde jen v jednotkách.",
        "Dělí se na centrální a obvodovou a její základní jednotkou je neuron.",
        "Patří do ní mozek a mícha.",
    )),
    ("Poznej chemický prvek.", "Křemík", ["Si"], (
        "Po kyslíku je druhým nejrozšířenějším prvkem zemské kůry, ale v čisté podobě se v přírodě nevyskytuje.",
        "Pro elektroniku se musí vyčistit tak, že na miliardu atomů připadá méně než jeden cizí.",
        "Jsou z něj čipy a je po něm pojmenováno kalifornské údolí.",
    )),
    ("Poznej jev.", "Skleníkový efekt", [], (
        "Bez něj by průměrná teplota Země byla kolem minus osmnácti stupňů a planeta by byla neobyvatelná.",
        "Popsal ho už v 19. století Svante Arrhenius a spočítal i vliv spalování uhlí.",
        "Zesiluje ho oxid uhličitý a metan a způsobuje oteplování.",
    )),
    ("Poznej vesmírný objekt.", "Černá díra", [], (
        "První snímek jedné z nich zveřejnili roku 2019 a vznikl propojením osmi radioteleskopů po celé planetě.",
        "Její hranicí je horizont událostí a v jejím okolí plyne čas pomaleji.",
        "Nic z ní neunikne, ani světlo, a vzniká zhroucením hmotné hvězdy.",
    )),
    ("Poznej léčivo.", "Inzulin", [], (
        "Objevitelé prodali patent univerzitě za symbolický jeden dolar, aby byl lék dostupný.",
        "Poprvé ho podali roku 1922 čtrnáctiletému chlapci a dřív se získával ze slinivek prasat.",
        "Píchají si ho diabetici a snižuje hladinu cukru v krvi.",
    )),
    ("Poznej chemickou sloučeninu.", "Oxid uhličitý", ["CO2"], (
        "V pevné podobě se nazývá suchý led a sublimuje při minus osmasedmdesáti stupních.",
        "Rostliny ho spotřebovávají při fotosyntéze a člověk ho vydechuje.",
        "Bublinkuje v limonádě a jeho vzorec je CO₂.",
    )),
    ("Poznej jev.", "Magnetické pole Země", ["magnetické pole Země"], (
        "Během posledních pěti milionů let se jeho póly převrátily zhruba dvacetkrát a záznam o tom nesou horniny na dně oceánů.",
        "Vzniká prouděním roztaveného železa v zemském jádru a chrání planetu před slunečním větrem.",
        "Podle něj se natáčí střelka kompasu.",
    )),
    ("Poznej vědce.", "Stephen Hawking", ["Hawking"], (
        "Diagnózu, která mu dávala dva roky života, dostal ve svých jednadvaceti a žil ještě půl století.",
        "Zabýval se kosmologií a předpověděl, že černé díry vyzařují a postupně se vypařují.",
        "Napsal Stručnou historii času a mluvil počítačovým hlasem z vozíku.",
    )),
    ("Poznej živočicha.", "Blecha", ["blechy"], (
        "Odraz jí nedávají svaly, ale bílkovina resilin, která funguje jako natažená pružina.",
        "Přenášela ve středověku mor, protože žila na krysách.",
        "Skáče do výšky mnohonásobku svého těla a saje krev.",
    )),
    ("Poznej lidskou tkáň.", "Kost", ["kosti", "kostní tkáň"], (
        "Novorozenec jich má kolem tří set, dospělý dvě stě šest — část jich během růstu sroste.",
        "Uvnitř je dřeň, která vyrábí krvinky, a její vnitřní stavba se přizpůsobuje zátěži.",
        "Zlomí se a pak se dává do sádry.",
    )),
]

BANK["kultura"] += [
    ("Poznej film.", "Ostře sledované vlaky", [], (
        "Získal roku 1968 druhého československého Oscara za cizojazyčný film.",
        "Režíroval ho Jiří Menzel podle Bohumila Hrabala a hlavní roli hrál Václav Neckář.",
        "Odehrává se na nádraží za protektorátu a hrdina Miloš Hrma řeší svou nezkušenost.",
    )),
    ("Poznej hudební skupinu.", "The Beatles", ["Beatles"], (
        "Nahrávací zkoušku u Decca Records neprošli — firma jim řekla, že kytarové skupiny jsou na ústupu.",
        "Pocházeli z Liverpoolu a jejich producentem byl George Martin.",
        "Zpívají Yesterday a Let It Be a jejich členy byli Lennon a McCartney.",
    )),
    ("Poznej knihu.", "1984", ["Devatenáct set osmdesát čtyři"], (
        "Autor ji dopsal na skotském ostrově Jura, kde umíral na tuberkulózu, a název vznikl prohozením číslic roku dopsání.",
        "Zavedla pojmy jako newspeak, ministerstvo pravdy a policie myšlení.",
        "Napsal ji George Orwell a Velký bratr v ní všechno vidí.",
    )),
    ("Poznej film.", "Titanic (film)", ["Titanic"], (
        "Jeho natáčení stálo víc než stavba skutečné lodi, i po přepočtu na dnešní ceny.",
        "Roku 1998 získal jedenáct Oscarů, což je dodnes rekord sdílený se dvěma jinými filmy.",
        "Kate Winsletová a Leonardo DiCaprio v něm stojí na přídi a hraje k tomu píseň Céline Dion.",
    )),
    ("Poznej obraz.", "Hvězdná noc", ["Hvězdná noc (obraz)"], (
        "Autor ho namaloval z okna pokoje v ústavu v Saint-Rémy, kde se dobrovolně léčil.",
        "Krajina na něm neodpovídá skutečnosti — cypřiš i vesnice jsou domalované z paměti.",
        "Je na něm vířící noční obloha nad vsí a namaloval ho Vincent van Gogh.",
    )),
    ("Poznej českou kapelu.", "Kabát", [], (
        "Vznikla v Teplicích a její jméno bylo původně vtip o tom, že si ho členové mohou obléknout.",
        "Reprezentovala Česko roku 2007 na Eurovizi a skončila poslední.",
        "Zpívá Pohoda a Malá dáma a jejím frontmanem je Josef Vojtek.",
    )),
    ("Poznej film.", "Hvězdné války", ["Star Wars"], (
        "Režisér se vzdal části honoráře výměnou za práva na merchandising, což se ukázalo jako geniální obchod.",
        "První díl vyšel roku 1977 a byl označen jako Epizoda IV.",
        "Vystupuje v nich Darth Vader a světelné meče.",
    )),
    ("Poznej hudební skladbu.", "Čtvero ročních dob", ["Čtvero ročních období"], (
        "Ke každému koncertu autor připojil sonet, který popisuje, co hudba znázorňuje.",
        "Napsal ji benátský kněz přezdívaný podle barvy vlasů Ryšavý páter.",
        "Skládá se ze čtyř houslových koncertů a napsal ji Antonio Vivaldi.",
    )),
    ("Poznej seriál.", "Simpsonovi", ["The Simpsons"], (
        "Postavy mají žlutou barvu, aby při přepínání kanálů zaujaly pohled diváka.",
        "Jsou nejdéle běžícím animovaným seriálem a jejich autorem je Matt Groening.",
        "Žijí ve Springfieldu a otec rodiny pracuje v jaderné elektrárně.",
    )),
    ("Poznej českou operu.", "Prodaná nevěsta", [], (
        "Autor ji čtyřikrát přepracoval — z původní hry s mluveným slovem se stala opera s recitativy.",
        "Napsal ji Bedřich Smetana a odehrává se na české vsi o pouti.",
        "Vystupuje v ní Kecal a komediant s medvědem, tančí se v ní polka a furiant.",
    )),
    ("Poznej film.", "Vykoupení z věznice Shawshank", ["Shawshank", "The Shawshank Redemption"], (
        "V kinech propadl a slávu získal až na videokazetách a v televizi.",
        "Vychází z novely Stephena Kinga a natáčelo se v opuštěné trestnici v Ohiu.",
        "Hrdina si dvacet let hloubí únikovou cestu a hraje ho Tim Robbins vedle Morgana Freemana.",
    )),
    ("Poznej hudebníka.", "Jaroslav Ježek", ["Ježek"], (
        "Od dětství byl téměř slepý a jeho pracovna v Praze měla schválně modré stěny, protože modrou barvu vnímal nejlépe.",
        "Psal hudbu pro Osvobozené divadlo a roku 1939 emigroval do New Yorku, kde brzy zemřel.",
        "Složil Bugatti Step a Tmavomodrý svět.",
    )),
    ("Poznej stavbu.", "Sagrada Família", ["Sagrada Familia"], (
        "Její stavitel je pod ní pohřben a dostavba se odhaduje na rok 2026, sto let po jeho smrti.",
        "Stavba začala roku 1882 a financuje se výhradně z darů a vstupného.",
        "Stojí v Barceloně a navrhl ji Antoni Gaudí.",
    )),
    ("Poznej film.", "Kolja", [], (
        "Roli malého chlapce hrál ruský herec, který česky neuměl ani slovo a repliky se učil zpaměti.",
        "Získal roku 1997 Oscara za cizojazyčný film a Zlatý glóbus.",
        "Režíroval ho Jan Svěrák podle scénáře svého otce a hlavní roli hraje violoncellista.",
    )),
    ("Poznej knihu.", "Harry Potter", ["Harry Potter a Kámen mudrců"], (
        "Rukopis odmítlo dvanáct nakladatelství a to třinácté ho vzalo na radu osmileté dcery ředitele.",
        "Vyšel poprvé roku 1997 a autorka ho z velké části psala v edinburských kavárnách.",
        "Vypráví o chlapci s jizvou na čele, který nastoupí do školy čar a kouzel v Bradavicích.",
    )),
    ("Poznej českou pohádku.", "Pyšná princezna", [], (
        "Vznikla roku 1952 a byla to nejnavštěvovanější česká pohádka v kinech vůbec.",
        "Hraje v ní Alena Vránová a Vladimír Ráž a král Miroslav se vydává na cesty v přestrojení.",
        "Hlavní hrdinka zpychne a zkrotí ji zpívající kytka.",
    )),
    ("Poznej hudební styl.", "Reggae", [], (
        "Vzniklo na Jamajce z předchozích stylů ska a rocksteady a rytmus klade důraz na slabé doby.",
        "Je spjaté s hnutím rastafariánů a v roce 2018 ho UNESCO zapsalo mezi nehmotné dědictví.",
        "Nejznámějším představitelem byl Bob Marley.",
    )),
    ("Poznej film.", "Rain Man", [], (
        "Herec, který ztvárnil hlavní postavu, strávil rok pozorováním muže, jehož výjimečná paměť předlohu inspirovala.",
        "Získal roku 1989 Oscara za nejlepší film i za mužský herecký výkon.",
        "Dustin Hoffman v něm hraje autistu s mimořádnou pamětí vedle Toma Cruise.",
    )),
    ("Poznej malíře.", "Pablo Picasso", ["Picasso"], (
        "Jeho plné křestní jméno má přes dvacet slov a nese jména příbuzných a svatých.",
        "Prošel modrým a růžovým obdobím a spoluzaložil kubismus.",
        "Namaloval Guernicu jako protest proti bombardování baskického městečka.",
    )),
    ("Poznej hudební nástroj.", "Housle", [], (
        "Nástroje z italské Cremony ze 17. a 18. století se dodnes prodávají za miliony a jejich lak se marně zkoumá.",
        "Mají čtyři struny laděné po kvintách a hraje se na ně smyčcem s žíněmi.",
        "Nejslavnější výrobce se jmenoval Stradivari.",
    )),
]

BANK["historie"] += [
    ("Poznej událost.", "Pražská defenestrace", ["defenestrace", "třetí pražská defenestrace"], (
        "Všichni tři vyhození pád z výšky kolem sedmnácti metrů přežili — katolíci to připisovali andělům, protestanti hnojišti.",
        "Odehrálo se roku 1618 v Praze a bylo bezprostřední záminkou třicetileté války.",
        "Šlo o vyhození dvou místodržících a písaře z okna České kanceláře na Hradě.",
    )),
    ("Poznej říši.", "Mongolská říše", ["Mongolové"], (
        "Zavedla poštovní síť zvanou jam se stanicemi po čtyřiceti kilometrech; posel urazil za den i tři sta.",
        "Ve své největší podobě to byla největší souvislá říše dějin, od Koreje po Uhry.",
        "Založil ji Čingischán a jeho vnuk Kublaj vládl Číně.",
    )),
    ("Poznej událost.", "Pearl Harbor", ["Pearl Harbour"], (
        "Americké letadlové lodě, hlavní cíl, byly toho rána náhodou na moři a útok je minul.",
        "Odehrálo se 7. prosince 1941 na Havaji a prezident to nazval dnem hanby.",
        "Japonský nálet na námořní základnu přivedl USA do druhé světové války.",
    )),
    ("Poznej panovníka.", "Jindřich VIII.", ["Jindřich Osmý"], (
        "Byl mladší syn a na trůn se dostal až po smrti staršího bratra, s jehož vdovou se pak oženil.",
        "Kvůli rozvodu se odtrhl od Říma a stal se hlavou vlastní církve.",
        "Měl šest manželek a dvě z nich nechal popravit.",
    )),
    ("Poznej událost.", "Bitva u Slavkova", ["Slavkov", "bitva tří císařů"], (
        "Odehrála se přesně v den prvního výročí korunovace vítěze a on ji pak nazýval svou nejkrásnější.",
        "Rozhodl ji útok na Pratecký kopec, který soupeři opustili, aby obešli křídlo.",
        "Roku 1805 v ní na Moravě zvítězil Napoleon nad Rakouskem a Ruskem.",
    )),
    ("Poznej období.", "Renesance", [], (
        "Rozšířila se z italských městských států, kde na ni měli peníze bankéřské rody jako Medicejští.",
        "Slovo znamená znovuzrození a myslel se jím návrat k antickému vzoru.",
        "Patří do ní Leonardo, Michelangelo a objev perspektivy v malbě.",
    )),
    ("Poznej událost.", "Bitva u Hastingsu", ["Hastings"], (
        "Zachytila ji vyšívaná tapiserie dlouhá skoro sedmdesát metrů, která je dnes v Bayeux.",
        "Odehrála se roku 1066 a anglický král v ní podle tradice padl zasažen šípem do oka.",
        "Zvítězil v ní Vilém Dobyvatel z Normandie a začala tím normanská vláda v Anglii.",
    )),
    ("Poznej dokument.", "Charta 77", ["Charta"], (
        "Vznikla mimo jiné jako reakce na proces s hudební skupinou The Plastic People of the Universe.",
        "Opírala se o mezinárodní pakty, které Československo samo podepsalo a vyhlásilo ve sbírce zákonů.",
        "Jejími prvními mluvčími byli Václav Havel, Jan Patočka a Jiří Hájek.",
    )),
    ("Poznej stavbu.", "Machu Picchu", [], (
        "Kameny jsou skládané nasucho tak přesně, že mezi ně nelze vsunout list papíru — což pomáhá při zemětřesení.",
        "Ukázal ho světu roku 1911 americký badatel Hiram Bingham, ačkoli místní o něm věděli.",
        "Je to horské město Inků v peruánských Andách.",
    )),
    ("Poznej událost.", "Vznik Československa", ["vznik ČSR", "28. říjen"], (
        "Rozhodující zprávou byla nóta ministra Andrássyho, kterou lidé v Praze pochopili jako kapitulaci.",
        "Ve stejný den vydal Národní výbor první zákon o zřízení samostatného státu.",
        "Stalo se to 28. října 1918 a prvním prezidentem se stal Masaryk.",
    )),
    ("Poznej civilizaci.", "Starověký Egypt", ["Egypt"], (
        "Písaři patřili k nejvyšší vrstvě, protože ovládat tři tisíce znaků uměl málokdo.",
        "Trvala přes tři tisíce let a rozdělovala se na Starou, Střední a Novou říši.",
        "Stavěli pyramidy a psali hieroglyfy; jejich vládcům se říká faraoni.",
    )),
    ("Poznej událost.", "Nástup Hitlera k moci", ["Hitler", "Adolf Hitler"], (
        "Roku 1923 se pokusil o převrat v mnichovské pivnici, skončil ve vězení a tam napsal svou knihu.",
        "Kancléřem se stal roku 1933 a po požáru Říšského sněmu si nechal odhlasovat zmocňovací zákon.",
        "Rozpoutal druhou světovou válku a spáchal roku 1945 sebevraždu v bunkru.",
    )),
    ("Poznej událost.", "Zrušení nevolnictví", ["nevolnictví"], (
        "Vydal ho roku 1781 syn Marie Terezie, který v témže roce vydal i toleranční patent.",
        "Neznamenalo to konec roboty — ta padla až o šedesát let později.",
        "Poddaní se od té chvíle mohli stěhovat, ženit a posílat děti na studia bez svolení vrchnosti.",
    )),
    ("Poznej stavbu.", "Pyramidy v Gíze", ["Cheopsova pyramida", "pyramidy"], (
        "Nejvyšší z nich byla přes tři tisíce sedm set let nejvyšší stavbou světa.",
        "Postavili je ve 3. tisíciletí před naším letopočtem jako hrobky panovníků.",
        "Stojí u nich Velká sfinga a jsou jediným dochovaným ze sedmi divů světa.",
    )),
    ("Poznej válku.", "Třicetiletá válka", [], (
        "Švédský král Gustav II. Adolf v ní padl v bitvě u Lützenu, kterou jeho vojsko přesto vyhrálo.",
        "Začala v Čechách stavovským povstáním a skončila roku 1648 vestfálským mírem.",
        "Za ni přišly české země podle odhadů o třetinu obyvatel a vypálil je Švéd.",
    )),
    ("Poznej událost.", "Rozdělení Československa", ["rozdělení ČSFR"], (
        "Rozhodli o něm politici bez referenda, ačkoli si ho většina lidí v obou částech přála.",
        "Proběhlo v noci na 1. ledna 1993 a označuje se jako sametový rozvod.",
        "Vznikly tím Česká republika a Slovensko.",
    )),
    ("Poznej období.", "Doba kamenná", [], (
        "Její poslední úsek přinesl zemědělství, což se označuje za největší proměnu způsobu života v dějinách.",
        "Dělí se na starší, střední a mladší a končí objevem zpracování kovů.",
        "Lidé v ní používali pěstní klín a malovali v jeskyních.",
    )),
    ("Poznej událost.", "Kolonizace Ameriky", ["kolonizace"], (
        "S Evropany přišly nemoci, na které původní obyvatelé neměli odolnost, a zemřela většina z nich.",
        "Španělé a Portugalci si území rozdělili smlouvou z Tordesillas roku 1494 čárou na mapě.",
        "Zničila říše Aztéků a Inků a Cortés s Pizarrem u toho byli.",
    )),
    ("Poznej dopravní stavbu.", "Transsibiřská magistrála", ["transsibiřská magistrála"], (
        "Cesta z jednoho konce na druhý trvá zhruba sedm dní a překročí osm časových pásem.",
        "Stavěla se v letech 1891 až 1916 a přes jedno jezero se zpočátku vozily vagony trajektem.",
        "Je to nejdelší železnice světa, z Moskvy do Vladivostoku.",
    )),
    ("Poznej událost.", "Vypálení Lidic", ["Lidice"], (
        "Obec vybrali na základě dopisu, který s atentátem neměl nic společného.",
        "Muže postříleli u zdi Horákova statku, ženy odvezli do Ravensbrücku a většinu dětí zavraždili.",
        "Stalo se to v červnu 1942 jako odveta za atentát na Heydricha.",
    )),
]

BANK["priroda"] += [
    ("Poznej živočicha.", "Delfín", ["delfíni"], (
        "Spí tak, že odpočívá vždy jen jedna polovina mozku — jinak by se utopil.",
        "Dorozumívá se hvizdy, které fungují jako jména, a používá echolokaci.",
        "Je to mořský savec, který skáče u lodí a vystupuje ve výcvikových nádržích u moře.",
    )),
    ("Poznej rostlinu.", "Kávovník", ["káva"], (
        "Podle legendy si jeho účinku všiml etiopský pastýř, jehož kozy po ochutnání plodů nespaly.",
        "Pěstuje se ve dvou hlavních druzích, arabica a robusta, a plodům se říká třešně.",
        "Ze semen se praží a mele nápoj, který se pije ráno.",
    )),
    ("Poznej živočicha.", "Žralok bílý", ["žralok"], (
        "Zuby mu dorůstají v několika řadách a za život jich vystřídá desetitisíce.",
        "Nemá plynový měchýř, proto se musí neustále pohybovat, aby se nepotopil.",
        "Proslavil ho film Čelisti a loví tuleně u pobřeží Jižní Afriky.",
    )),
    ("Poznej strom.", "Dub", ["dub letní"], (
        "Jeho dřevo obsahuje třísloviny, které z něj dělají nejlepší materiál na sudy pro víno a whisky.",
        "Roste stovky let a v Česku je z něj nejstarší památný strom.",
        "Jeho plodem je žalud a listy má laločnaté.",
    )),
    ("Poznej živočicha.", "Kukačka", ["kukačka obecná"], (
        "Vejce klade během několika vteřin a barvou i vzorem je přizpůsobí hostiteli.",
        "Mládě po vylíhnutí vyhází z hnízda ostatní vejce a nechá se krmit cizími rodiči.",
        "Ozývá se dvěma slabikami a její jméno nesou hodiny.",
    )),
    ("Poznej rostlinu.", "Pšenice", [], (
        "Dnešní odrůdy vznikly zkřížením několika druhů trav a mají šestinásobnou sadu chromozomů.",
        "Je to nejpěstovanější obilnina mírného pásu a její lepek dělá těsto pružným.",
        "Mele se z ní mouka na chleba.",
    )),
    ("Poznej živočicha.", "Mravkolev", ["mravkolev obecný"], (
        "Dospělec připomíná vážku a žije jen pár týdnů; dravá je pouze larva.",
        "Larva si v písku hloubí trychtýř a čeká vespod schovaná s otevřenými kusadly.",
        "Do jámy spadne mravenec a už se nevyhrabe.",
    )),
    ("Poznej jev.", "Bouřka", [], (
        "Vzdálenost blesku se odhadne tak, že se sekundy do zahřmění vydělí třemi — dá to kilometry.",
        "Vzniká ve vysokém oblaku, kterému se říká cumulonimbus, při silném stoupavém proudu.",
        "Blýská se a hřmí a lidé se schovávají před deštěm.",
    )),
    ("Poznej živočicha.", "Sob", ["sob polární"], (
        "Jako jediný savec vidí i v ultrafialovém světle, takže rozezná lišejník na sněhu.",
        "Paroží mají u něj i samice a jeho oči v zimě mění barvu.",
        "Táhne saně a v Laponsku ho chovají Sámové.",
    )),
    ("Poznej rostlinu.", "Konvalinka", ["konvalinka vonná"], (
        "Celá rostlina včetně vody ve váze je jedovatá a její látky působí na srdce.",
        "Ve Francii se prvního května dává jako dárek pro štěstí.",
        "Roste v lese, má bílé zvonečky a silně voní.",
    )),
    ("Poznej živočicha.", "Bobr", ["bobr evropský"], (
        "Řezáky mu neustále dorůstají a oranžová barva na nich je od železa, které je zpevňuje.",
        "Staví hráze, aby si zvýšil hladinu, a vchod do obydlí má vždy pod vodou.",
        "Kácí stromy zuby a plácá plochým ocasem.",
    )),
    ("Poznej rostlinu.", "Orchidej", ["orchideje", "vstavačovité"], (
        "Semínka nemají zásobu živin, takže bez spolupráce s houbou vůbec nevyklíčí.",
        "Je to nejpočetnější čeleď rostlin s víc než dvaceti tisíci druhy a v Česku patří k chráněným.",
        "Vanilka je její plod a její květy se prodávají v květináči do bytu.",
    )),
    ("Poznej živočicha.", "Rejsek", ["rejsek obecný"], (
        "Musí jíst každé dvě až tři hodiny, jinak zemře hlady; přes zimu mu i zmenšuje lebka.",
        "Není to hlodavec, ale hmyzožravec, a má jedovaté sliny.",
        "Je to jeden z nejmenších savců a má protaženou čenichovou trubičku.",
    )),
    ("Poznej rostlinu.", "Len", ["len setý"], (
        "Ze stonků se získává vlákno máčením, kterému se říká rosení, a ze semen olej.",
        "V Česku se z něj tkalo plátno a jeho pěstování patřilo k tradičním řemeslům Podkrkonoší.",
        "Má modré kvítky a dělá se z něj lněné plátno a lněný olej.",
    )),
    ("Poznej živočicha.", "Kachna divoká", ["kachna", "divoká kachna"], (
        "Peří jí neprosákne, protože si ho maže tukem z žlázy nad kořenem ocasu.",
        "Samec má zelenou hlavu, samice hnědou, a v létě přepeřuje do nenápadného šatu.",
        "Plave na rybníce a lidé jí házejí rohlík, ačkoli by neměli.",
    )),
    ("Poznej horninu.", "Žula", ["granit"], (
        "Vznikla pomalým tuhnutím magmatu hluboko pod povrchem, proto má velká zrna.",
        "Tvoří ji křemen, živec a slída a v Česku se láme hlavně na Českomoravské vrchovině.",
        "Dlaždí se z ní chodníky a dělají se z ní pomníky.",
    )),
    ("Poznej živočicha.", "Vážka", ["vážky"], (
        "Larva žije ve vodě i několik let a loví vystřelovací spodní čelistí zvanou maska.",
        "Dospělec má dva páry křídel, která ovládá nezávisle, takže umí letět i pozpátku.",
        "Poletuje nad rybníkem a má obrovské složené oči.",
    )),
    ("Poznej rostlinu.", "Vinná réva", ["réva", "réva vinná"], (
        "V 19. století zničila evropské vinice mšička révokaz a zachránilo je roubování na americké podnože.",
        "Pěstuje se na jižní Moravě a její odrůdy nesou jména jako Ryzlink nebo Veltlínské.",
        "Rostou na ní hrozny a dělá se z nich víno.",
    )),
    ("Poznej živočicha.", "Sýkora koňadra", ["sýkora"], (
        "V Británii se naučila propichovat víčka lahví s mlékem a dovednost se mezi ptáky rozšířila učením.",
        "Je to nejběžnější návštěvník krmítka a černý pruh na bříšku má samec širší než samice.",
        "Má žluté bříško, černou hlavu a bílé tváře.",
    )),
    ("Poznej jev.", "Sopečná erupce", ["sopka", "vulkanismus"], (
        "Její sílu měří index VEI a stupnice je logaritmická jako u zemětřesení.",
        "Nejvíc obětí nemívá lávový proud, ale žhavé mračno popela a plynů, které se řítí ze svahu.",
        "Vytéká při ní láva a vyvrhuje se popel.",
    )),
]

BANK["technika"] += [
    ("Poznej vynález.", "Kolo bicyklu", ["jízdní kolo", "bicykl", "kolo"], (
        "Jeho první podoba z roku 1817 neměla šlapky — jezdec se odrážel nohama od země a říkalo se jí drezína.",
        "Šlapky na předním kole přinesly vysoké modely s obřím kolem, které vystřídal řetězový převod.",
        "Má dvě kola, řídítka a pedály a jezdí se na něm po cyklostezce.",
    )),
    ("Poznej stavbu.", "Akvadukt", ["akvadukty"], (
        "Nejznámější zachovaný ve Španělsku stojí bez malty — kameny drží jen vlastní vahou.",
        "Římané jich postavili stovky a voda v nich tekla samospádem, obloukové mosty jsou jen viditelná část.",
        "Vede vodu přes údolí a nejslavnější je Pont du Gard ve Francii.",
    )),
    ("Poznej vynález.", "Termoska", ["Dewarova nádoba"], (
        "Vynalezl ji roku 1892 skotský fyzik při pokusech se zkapalňováním plynů a nenechal si ji patentovat.",
        "Funguje díky vakuu mezi dvěma stěnami a odrazivé vrstvě, která brání vyzařování tepla.",
        "Udrží čaj horký a limonádu studenou.",
    )),
    ("Poznej techniku.", "Radar", [], (
        "Britové jeho existenci za války tajili a nálezy připisovali tomu, že jejich piloti jedí hodně mrkve.",
        "Vysílá radiové vlny a měří čas jejich návratu; jméno je zkratka anglického popisu činnosti.",
        "Používá ho letecký provoz, meteorologové i policie u silnice.",
    )),
    ("Poznej stroj.", "Traktor", [], (
        "První úspěšné modely nahradily parní stroj spalovacím a zásadní byl vynález hydraulického závěsu Harryho Fergusona.",
        "Jeho zadní kola bývají výrazně větší než přední kvůli tahu a přenosu síly.",
        "Táhne pluh po poli a jezdí s ním zemědělci.",
    )),
    ("Poznej vynález.", "Konzerva", [], (
        "Metodu vymyslel Nicolas Appert roku 1809 na vypsanou odměnu francouzské vlády pro armádu.",
        "Otvírák na ni vznikl až o desítky let později; do té doby se otevírala dlátem a kladivem.",
        "Uchová jídlo léta a otevírá se plechovka.",
    )),
    ("Poznej dopravní stavbu.", "Eurotunel", ["tunel pod Lamanšským průlivem"], (
        "Ražba postupovala z obou stran a obě čela se setkala s odchylkou jen pár desítek centimetrů.",
        "Otevřel se roku 1994, měří pod mořem přes třicet kilometrů a auta jezdí na vlaku.",
        "Spojuje Anglii s Francií pod kanálem La Manche.",
    )),
    ("Poznej vynález.", "Šicí stroj", [], (
        "Rozhodujícím nápadem bylo dát ouško jehly ke špičce, ne k tupému konci.",
        "Isaac Singer z něj udělal masový výrobek a zavedl prodej na splátky.",
        "Šije látku a šlape se u něj nohou.",
    )),
    ("Poznej techniku.", "Solární panel", ["fotovoltaika", "solární panely"], (
        "Jev, na kterém stojí, vysvětlil Albert Einstein a dostal za to Nobelovu cenu.",
        "Účinnost běžných křemíkových desek se dnes pohybuje kolem dvaceti procent.",
        "Dává se na střechu a vyrábí elektřinu ze slunce.",
    )),
    ("Poznej stroj.", "Výtah", [], (
        "Rozšířil se teprve poté, co Elisha Otis roku 1854 veřejně předvedl pojistku a nechal si přeseknout lano.",
        "Bez něj by nemělo smysl stavět mrakodrapy, protože nahoru by nikdo nechodil.",
        "Vozí lidi mezi patry a má tlačítka s čísly.",
    )),
    ("Poznej vynález.", "Gramofon", ["fonograf"], (
        "První přístroj zaznamenával zvuk na staniolem potažený válec a jeho vynálezce ho zamýšlel hlavně na diktování dopisů.",
        "Deska nahradila válec, protože se dala lisovat ve velkém, a rychlost se ustálila na 33 otáčkách.",
        "Jehla jede v drážce a hraje z desky.",
    )),
    ("Poznej vozidlo.", "Trolejbus", [], (
        "Potřebuje dvě troleje, ne jednu jako tramvaj, protože proud se nemá kudy vrátit kolejnicemi.",
        "V Česku jezdí například v Plzni, Brně a v Českých Budějovicích a v Ústí nad Labem.",
        "Vypadá jako autobus, ale jede na elektřinu z drátů nad silnicí.",
    )),
    ("Poznej techniku.", "Optické vlákno", ["optická vlákna"], (
        "Světlo se v něm drží úplným odrazem na rozhraní, takže se za rohem neztratí.",
        "Jedno takové tenčí než vlas přenese data pro celé město a neruší ho elektromagnetické pole.",
        "Vede jím rychlý internet místo měděného kabelu.",
    )),
    ("Poznej vynález.", "Brýle", [], (
        "Objevily se v Itálii kolem roku 1290 a první podobu tvořily dvě lupy spojené nýtem, které se držely v ruce.",
        "Nožičky za uši přišly až o čtyři sta let později, v 18. století v Anglii.",
        "Nosí se na nose a opravují krátkozrakost.",
    )),
    ("Poznej stavbu.", "Rozhledna", [], (
        "V Česku jich stojí přes tři sta a řada z nich vznikla v 19. století zásluhou turistických spolků.",
        "Bývá na kopci a její jediný účel je dostat oko výš, než dosáhnou stromy.",
        "Vyleze se po schodech nahoru a je z ní vidět do kraje.",
    )),
    ("Poznej techniku.", "Termovize", ["termokamera", "infrakamera"], (
        "Pracuje ve vlnových délkách kolem deseti mikrometrů, kde vyzařují tělesa o pokojové teplotě.",
        "Používá ji hasič v zakouřeném domě i stavař, který hledá, kudy z budovy uniká teplo.",
        "Ukáže obraz v barvách podle teploty — teplé části svítí.",
    )),
    ("Poznej vynález.", "Rozhlas", ["rozhlasový přijímač"], (
        "Pravidelné vysílání začalo v Československu roku 1923 z plátěného stanu v Kbelích.",
        "Vlny přenášejí zvuk modulací amplitudy nebo frekvence a první československá stanice se jmenovala Radiojournal.",
        "Naladí se na frekvenci a hraje hudbu a zprávy.",
    )),
    ("Poznej materiál.", "Papír", [], (
        "Recept se z Číny dostal na Západ podle tradice přes zajaté řemeslníky po bitvě u Talasu roku 751.",
        "Vyrábí se z buničiny a jeho gramáž se udává v gramech na metr čtvereční.",
        "Píše se na něj a formát A4 měří 210 na 297 milimetrů.",
    )),
    ("Poznej techniku.", "Kryogenika", ["kryogenní technika"], (
        "Kapalné helium umožnilo objevit supravodivost, protože pod čtyřmi kelviny odpor rtuti zmizel.",
        "Zabývá se teplotami blízkými absolutní nule a kapalný dusík má minus 196 stupňů.",
        "Díky ní se vozí zemní plyn v tankerech ve zkapalněné podobě a mrazí se biologické vzorky.",
    )),
    ("Poznej vynález.", "Fén", ["vysoušeč vlasů"], (
        "Jméno má po teplém padavém větru, který fouká z hor do údolí.",
        "První modely z počátku 20. století vážily přes dvě kila a vyráběly se z těžkého kovu.",
        "Fouká horký vzduch a používá se po ranní sprše na hlavu.",
    )),
]

BANK["sport"] += [
    ("Poznej sport.", "Skoky na lyžích", ["skok na lyžích"], (
        "Bodují se dvě věci — délka a styl —, a k tomu se přepočítává vítr a délka nájezdu.",
        "Technika do V se prosadila až koncem osmdesátých let a rozhodčí ji zpočátku strhávali.",
        "Skáče se z můstku a v Česku ho proslavil Jiří Raška.",
    )),
    ("Poznej sportovce.", "Nikola Karabatič", ["Karabatič"], (
        "Jeho otec i bratr byli reprezentanti a on sám hrál za kluby ve třech zemích.",
        "Je to francouzský házenkář, trojnásobný olympijský vítěz.",
        "Patří k nejlepším hráčům házené všech dob a hrál za Barcelonu i PSG.",
    )),
    ("Poznej sport.", "Vodní slalom", [], (
        "Branky se počítají tak, že se za dotek přičítají dvě sekundy a za minutí padesát.",
        "Jezdí se proti proudu i po proudu a v Praze je pro něj kanál v Troji.",
        "Česko v něm má olympijská zlata a jezdí se v kajaku nebo kanoi.",
    )),
    ("Poznej klub.", "Manchester United", ["Manchester Utd"], (
        "Roku 1958 zahynula část jeho týmu při letecké havárii v Mnichově.",
        "Vedl ho šestadvacet let Alex Ferguson a hraje na Old Trafford.",
        "Je to jeden z nejbohatších fotbalových klubů světa a hrál za něj David Beckham.",
    )),
    ("Poznej sport.", "Triatlon", [], (
        "Vznikl v sedmdesátých letech na Havaji ze sázky, který sport je nejnáročnější — tak je spojili.",
        "Nejdelší podoba nese jméno podle toho ostrova a měří 226 kilometrů.",
        "Skládá se z plavání, jízdy na kole a běhu.",
    )),
    ("Poznej sportovce.", "Ondřej Synek", ["Synek"], (
        "Startoval na pěti olympiádách a ze čtyř si přivezl medaili, ale nikdy zlatou.",
        "Byl to český veslař, pětinásobný mistr světa na skifu.",
        "Trénoval na Labi u Nymburka a měřil přes dva metry.",
    )),
    ("Poznej sport.", "Stolní tenis", ["ping pong", "pingpong"], (
        "Vznikl v Anglii jako salonní zábava a jako síť sloužila řada knih přes stůl.",
        "Míček má průměr čtyřicet milimetrů a povinně se hraje do jedenácti bodů.",
        "Hraje se na zeleném stole s pálkou a Čína v něm dominuje.",
    )),
    ("Poznej sportovkyni.", "Šárka Kašpárková", ["Kašpárková"], (
        "Před přechodem k jedné disciplíně skákala do výšky a startovala i v dálce.",
        "Roku 1997 se v Athénách stala mistryní světa a v Atlantě získala bronz.",
        "Je to česká trojskokanka a drží dodnes český rekord.",
    )),
    ("Poznej sport.", "Box", ["boxování"], (
        "Pravidla, podle kterých se dnes hraje, sepsal roku 1867 John Chambers a nesou jméno markýze z Queensberry.",
        "Rukavice se zavedly právě tehdy a boj se rozdělil na kola po třech minutách.",
        "Vyhrává se knokautem nebo na body a hmotnostní kategorie jsou od muší po těžkou.",
    )),
    ("Poznej trofej.", "Davisův pohár", ["Davis Cup"], (
        "Věnoval ji roku 1900 americký student, který zaplatil stříbrnou mísu ze svého.",
        "Hraje se v ní na domácí a venkovní zápasy mezi státy a Česko ji vyhrálo v letech 1980 a 2012.",
        "Je to nejprestižnější tenisová soutěž družstev mužů.",
    )),
    ("Poznej sport.", "Sportovní gymnastika", ["gymnastika"], (
        "Bodování bez horní hranice zavedli až roku 2006; do té doby byla nejvyšší známka desítka.",
        "Muži soutěží na šesti nářadích, ženy na čtyřech, a prvky se pojmenovávají po objevitelích.",
        "Cvičí se na bradlech, kladině a v prostných.",
    )),
    ("Poznej sportovce.", "Dominik Hašek", [], (
        "Vystudoval pedagogickou fakultu a v mládí hrával za Pardubice, kam se ve čtyřiceti letech vracel.",
        "Získal šestkrát Vezinovu trofej pro nejlepšího brankáře NHL a dvakrát Hart Trophy.",
        "Chytal v Naganu a jeho lapačce se říkalo nejrychlejší ruka ligy.",
    )),
    ("Poznej sport.", "Kanoistika", ["rychlostní kanoistika"], (
        "Rozlišuje se sed s pádlem o dvou listech a klek s pádlem o jednom.",
        "Závodí se na klidné vodě na tratích 200, 500 a 1000 metrů.",
        "Česko v ní má olympijská zlata a jezdí se v kajaku a kánoi.",
    )),
    ("Poznej sportovní akci.", "Wimbledon", [], (
        "Jako jediný z velkých turnajů má dodnes přísný předpis, že hráči musí být oblečeni téměř celí v bílém.",
        "Hraje se od roku 1877 a na trávě, což mění odskok míče.",
        "Je to nejstarší tenisový turnaj a vítězi se podává jahodový dezert.",
    )),
    ("Poznej sport.", "Šachy", [], (
        "Počet možných partií je vyšší než počet atomů v pozorovatelném vesmíru.",
        "Vznikly v Indii jako čaturanga a přes Persii se dostaly do Evropy.",
        "Hraje se na 64 polích a cílem je dát mat králi.",
    )),
    ("Poznej sportovce.", "Lionel Messi", ["Messi"], (
        "Jako dítě mu v Argentině diagnostikovali nedostatek růstového hormonu a klub ve Španělsku mu zaplatil léčbu.",
        "Získal osm Zlatých míčů, víc než kdokoli jiný.",
        "Hrál za Barcelonu a s Argentinou vyhrál roku 2022 mistrovství světa.",
    )),
    ("Poznej sport.", "Hokej", ["lední hokej"], (
        "Puk se před zápasem mrazí, aby na ledě zbytečně neskákal.",
        "Hraje se třikrát dvacet minut čistého času a střídá se za běhu.",
        "Česko v něm má zlato z Nagana a nejslavnější soutěž je NHL.",
    )),
    ("Poznej sportovce.", "Jan Kodeš", ["Kodeš"], (
        "Po kariéře vedl český tenisový svaz a byl ředitelem pražského turnaje.",
        "Vyhrál dvakrát Roland Garros, v letech 1970 a 1971.",
        "Roku 1973 zvítězil ve Wimbledonu jako dosud jediný Čech ve dvouhře mužů.",
    )),
    ("Poznej sport.", "Atletika", [], (
        "Označuje se za královnu sportů a její disciplíny se dělí na běhy, skoky, vrhy a víceboje.",
        "Na dráze se běží proti směru hodinových ručiček a okruh měří 400 metrů.",
        "Patří sem sprint, maraton, skok do dálky i hod oštěpem.",
    )),
    ("Poznej klub.", "Slavia Praha", ["SK Slavia Praha", "Slavia"], (
        "Vznikla roku 1892 jako literární a řečnický spolek studentů, teprve pak z ní byl sportovní klub.",
        "Hraje v červenobílém a jejím znakem je pěticípá hvězda.",
        "Její stadion je v Edenu a rivalem je pražská Sparta.",
    )),
]

BANK["jazyk"] += [
    ("Poznej jazyk.", "Němčina", ["německy"], (
        "Podstatná jména se v ní píší s velkým písmenem, což jinde v Evropě prakticky neexistuje.",
        "Skládá slova do dlouhých celků a její sloveso se v podřadné větě posouvá až na konec.",
        "Mluví se jí v Rakousku, částečně ve Švýcarsku a hlavně v zemi, jejíž hlavní město je Berlín.",
    )),
    ("Poznej slovo podle původu.", "Bakterie", [], (
        "Pochází z řeckého slova pro hůlku, protože první pozorované měly tvar tyčinky.",
        "Poprvé je uviděl Antoni van Leeuwenhoek svým vlastnoručně broušeným mikroskopem.",
        "Jsou to jednobuněčné organismy a proti některým zabírá penicilin.",
    )),
    ("Poznej termín.", "Aliterace", [], (
        "Ve staré germánské poezii nahrazovala rým jako hlavní organizační princip verše.",
        "V češtině se jí říká náslovný rým a hojně ji používají reklamní slogany.",
        "Je to opakování stejné hlásky na začátku slov — třeba „plyne peníz po penízku“.",
    )),
    ("Poznej jazyk.", "Ruština", ["ruský jazyk"], (
        "V její abecedě jsou dvě písmena, která se sama nevyslovují a jen mění tvrdost té předchozí hlásky.",
        "Přízvuk v ní není pevný a mění se podle tvaru slova, což dělá cizincům největší potíže.",
        "Píše se azbukou a je úředním jazykem největšího státu světa.",
    )),
    ("Poznej slovo.", "Robota", [], (
        "V češtině ještě v 19. století označovalo povinnou práci poddaného na panském.",
        "Ve slovenštině dodnes znamená prostě práci a v ruštině je základem slovesa pracovat.",
        "Z jeho zkráceného tvaru vzniklo označení pro stroj, který pracuje místo člověka.",
    )),
    ("Poznej jev.", "Vokalizace", ["vokalizace předložky"], (
        "Řídí se výslovnostní snadností — vkládá se, když by jinak vznikl těžko vyslovitelný shluk.",
        "Proto se říká „ve válce“, ale „v lese“, a „ke stolu“, ale „k oknu“.",
        "Je to přidání samohlásky k jednohláskovému slůvku před podstatným jménem.",
    )),
    ("Poznej termín.", "Archaismus", ["archaismy"], (
        "Liší se od historismu tím, že označovaná věc existuje dál, jen se pro ni používá nové slovo.",
        "Ve školní četbě z 19. století jich je plno a čtenář jim rozumí jen z kontextu.",
        "Patří sem „šat“ místo oblečení nebo „kterak“ místo jak.",
    )),
    ("Poznej jazyk.", "Italština", ["italsky"], (
        "Ustálila se na základě toskánského nářečí, protože v něm psali Dante, Petrarca a Boccaccio.",
        "Skoro každé její slovo končí samohláskou, což jí dává zpěvný ráz.",
        "Je jazykem opery a hudebních pokynů jako allegro nebo forte.",
    )),
    ("Poznej slovo podle původu.", "Karanténa", [], (
        "Číslovka v základu slova říká, kolik dní musely lodě čekat před přístavem — bylo jich čtyřicet.",
        "Zavedly ji Benátky a Dubrovník ve 14. století proti moru.",
        "Dnes tak říkáme izolaci člověka, který mohl přijít do styku s nákazou.",
    )),
    ("Poznej jev.", "Sufix", ["sufixy"], (
        "Rozlišuje se od koncovky tím, že se při skloňování nemění a patří ke kmeni slova.",
        "Češtině umožňuje tvořit řady jako učit — učitel — učitelka — učitelství.",
        "Je to část připojená za kořen slova; česky se mu říká přípona.",
    )),
    ("Poznej písmo.", "Hieroglyfy", ["hieroglyfické písmo"], (
        "Rozluštil je roku 1822 Jean-François Champollion a klíčem mu byl kámen nalezený u města Rašíd.",
        "Kombinují znaky pro hlásky, slabiky i celé pojmy a jméno panovníka se psalo do oválu.",
        "Psali jimi ve starém Egyptě na papyrus i na stěny chrámů.",
    )),
    ("Poznej termín.", "Ironie", [], (
        "Sokratovská podoba spočívala v předstírané nevědomosti, kterou filozof vedl soupeře k rozporu.",
        "Její vyostřená forma s úmyslem ranit se jmenuje sarkasmus.",
        "Řekne se opak toho, co se myslí — třeba „to se ti povedlo“ nad rozbitým hrnkem.",
    )),
    ("Poznej jazyk.", "Polština", ["polsky"], (
        "Má hlásky zapisované spřežkami jako sz, cz nebo rz a přízvuk vždy na předposlední slabice.",
        "Je češtině blízká, ale plno slov znamená něco jiného — „szukać“ rozhodně neznamená hledat na veřejnosti.",
        "Mluví se jí v zemi, jejímž hlavním městem je Varšava.",
    )),
    ("Poznej slovo podle původu.", "Salám", [], (
        "Kořen slova je v latinském sal, tedy sůl, kterou se maso konzervovalo.",
        "Do češtiny se dostalo z italštiny a jeho výroba stojí na sušení a zrání.",
        "Krájí se na chleba a jeho uherská odrůda se u nás jmenuje po sousední zemi.",
    )),
    ("Poznej jev.", "Nářečí", ["dialekt"], (
        "V Česku se tradičně rozdělují do čtyř skupin a jejich hranice sledují staré správní celky.",
        "Na Moravě se drží víc než v Čechách a na Chodsku či Valašsku jsou dodnes slyšet.",
        "Je to místní obměna jazyka — Pražák řekne jinak než Ostravák.",
    )),
    ("Poznej termín.", "Akronym", [], (
        "Liší se od obyčejné zkratky tím, že se čte jako slovo, ne po písmenech.",
        "Některé už jako zkratky ani nevnímáme — třeba laser nebo radar.",
        "Patří sem NATO nebo UNESCO.",
    )),
    ("Poznej jazyk.", "Japonština", ["japonsky"], (
        "Používá tři písemné soustavy najednou a v jedné větě se běžně střídají všechny.",
        "Nemá množné číslo ani budoucí čas a míra zdvořilosti mění tvar slovesa.",
        "Mluví se jí v zemi vycházejícího slunce a její znaky přejala z Číny.",
    )),
    ("Poznej slovo podle původu.", "Šek", [], (
        "Podle jednoho výkladu souvisí s perským slovem pro krále, odtud i pojem ze šachu.",
        "Je to písemný příkaz bance, aby vyplatila uvedenou částku.",
        "Cestovní podoba se dřív brávala na dovolenou místo hotovosti.",
    )),
    ("Poznej jev.", "Kalk", ["kalky"], (
        "Slovo samo pochází z francouzského výrazu pro průsvitný papír na obkreslování.",
        "Vzniká doslovným přeložením cizí složeniny po částech, ne převzetím celku.",
        "Patří sem „mrakodrap“ z anglického skyscraper nebo „zeměpis“ z geografie.",
    )),
    ("Poznej termín.", "Ortoepie", ["ortoepie", "spisovná výslovnost"], (
        "Její pravidla řeší i to, kde se v souvislé řeči smí a nesmí spodobovat znělost.",
        "Je protějškem pravopisu, jenže pro mluvené slovo, a používají ji hlasatelé.",
        "Určuje, jak se má správně vyslovovat — třeba že „shoda“ zní na Moravě jinak než v Čechách.",
    )),
]

BANK["spolecnost"] += [
    ("Poznej pojem.", "Minimální mzda", [], (
        "V některých zemích neexistuje vůbec a její výši tam určuje jen dohoda odborů se zaměstnavateli.",
        "V Česku ji stanovuje vláda nařízením a od ní se odvozují i zaručené mzdy podle náročnosti práce.",
        "Je to nejnižší částka, kterou zaměstnavatel smí za měsíc práce vyplatit.",
    )),
    ("Poznej instituci.", "Veřejný ochránce práv", ["ombudsman"], (
        "Úřad má původ ve Švédsku, kde vznikl už roku 1809, a jeho švédské jméno se ujalo po celém světě.",
        "V Česku sídlí v Brně, volí ho sněmovna a nemůže rozhodovat, jen doporučovat.",
        "Občan se na něj obrací, když se s ním úřad chová špatně.",
    )),
    ("Poznej pojem.", "Sociální stát", ["welfare"], (
        "Jeho zárodkem bylo nemocenské a důchodové pojištění, které zavedl Bismarck, aby oslabil své odpůrce zleva.",
        "Skandinávský model stojí na vysokých daních a širokých veřejných službách.",
        "Znamená, že veřejná moc zajišťuje důchody, zdravotní péči a podporu v nezaměstnanosti.",
    )),
    ("Poznej svátek.", "Dušičky", ["Památka zesnulých", "Svátek zesnulých"], (
        "Zavedl je opat Odilo z Cluny v 11. století a položil je na den po svátku všech svatých.",
        "V Mexiku má jejich obdoba veselý ráz s barevnými lebkami a průvody.",
        "V Česku se při nich chodí na hřbitov se svíčkou a chryzantémami.",
    )),
    ("Poznej pojem.", "Korupce", [], (
        "Nevládní organizace Transparency International o ní vydává každoroční žebříček vnímání.",
        "Rozlišuje se malá, s níž se občan setká u přepážky, a velká, která ovlivňuje zákony.",
        "Je to úplatek za rozhodnutí, které mělo být nestranné.",
    )),
    ("Poznej organizaci.", "Greenpeace", [], (
        "Vznikla roku 1971 z výpravy lodi, která měla zabránit jaderné zkoušce na aljašském ostrově.",
        "Její loď Rainbow Warrior potopila roku 1985 francouzská tajná služba v Aucklandu.",
        "Zabývá se ochranou životního prostředí a proslula přímými akcemi.",
    )),
    ("Poznej pojem.", "Rozpočtový deficit", ["deficit", "schodek rozpočtu"], (
        "Pravidla Evropské unie ho doporučují držet pod třemi procenty hrubého domácího produktu.",
        "Kryje se vydáním dluhopisů a jeho součet za všechny roky tvoří státní dluh.",
        "Nastane, když stát utratí víc, než vybere.",
    )),
    ("Poznej pojem.", "Občanství", [], (
        "Získává se buď podle původu rodičů, nebo podle místa narození, a některé státy uznávají obojí.",
        "V Česku je od roku 2014 možné mít ho víc než jedno naráz.",
        "Opravňuje volit a mít pas dané země.",
    )),
    ("Poznej instituci.", "Univerzita Karlova", ["Karlova univerzita", "UK"], (
        "Její zakládací listinu vydal panovník roku 1348 a je to nejstarší vysoké učení ve střední Evropě.",
        "Roku 1882 se rozdělila na českou a německou část a znovu se spojila po druhé světové válce.",
        "Sídlí v Praze v Karolinu a má sedmnáct fakult.",
    )),
    ("Poznej pojem.", "Předsudek", [], (
        "Sociální psychologie ukázala, že se dá zmírnit prostým kontaktem — pokud jsou obě strany rovnocenné.",
        "Liší se od diskriminace tím, že jde o postoj, ne o jednání.",
        "Je to úsudek o člověku předem, jen podle skupiny, ke které patří.",
    )),
    ("Poznej svátek.", "Silvestr", ["Nový rok", "Silvestr a Nový rok"], (
        "Jméno má po papeži, který zemřel poslední den roku 335.",
        "V Česku se k němu tradičně podává čočka a pouští se ohňostroj.",
        "Slaví se na přelomu let a o půlnoci se připíjí.",
    )),
    ("Poznej pojem.", "Dělba moci", ["trojdělba moci"], (
        "Její dnešní podobu popsal Montesquieu ve spise O duchu zákonů roku 1748.",
        "Jde o to, aby žádná složka nemohla rozhodovat sama a navzájem se brzdily.",
        "Ty složky jsou zákonodárná, výkonná a soudní.",
    )),
    ("Poznej organizaci.", "Lékaři bez hranic", ["Médecins Sans Frontières"], (
        "Vznikli roku 1971 ve Francii po zkušenosti z války v Biafře, kde zdravotníci nesměli mluvit o tom, co viděli.",
        "Nobelovu cenu míru dostali roku 1999 a peníze použili na kampaň za dostupné léky.",
        "Vyjíždějí ošetřovat raněné do válek a katastrof, kam se nikdo jiný nedostane.",
    )),
    ("Poznej pojem.", "Urbanizace", [], (
        "Od roku 2007 poprvé v dějinách žije ve městech víc lidí než na venkově.",
        "Její důsledkem je i vznik takzvaných tepelných ostrovů, kde je o několik stupňů tepleji.",
        "Je to stěhování lidí z vesnic do měst.",
    )),
    ("Poznej instituci.", "Poslanecká sněmovna", ["sněmovna"], (
        "Aby se do ní strana dostala, musí získat aspoň pět procent hlasů; koalice mají práh vyšší.",
        "Má dvě stě členů volených na čtyři roky poměrným systémem ve čtrnácti krajích.",
        "Je to dolní komora českého parlamentu a schvaluje rozpočet.",
    )),
    ("Poznej pojem.", "Stárnutí populace", ["demografické stárnutí"], (
        "Vzniká ze dvou příčin naráz — lidé se dožívají víc a rodí se méně dětí.",
        "Ukazuje se na věkové pyramidě, která přestává být pyramidou a mění se v urnu.",
        "Kvůli němu se zvyšuje věk odchodu do důchodu.",
    )),
    ("Poznej pojem.", "Svoboda projevu", ["svoboda slova"], (
        "Podle českých soudů nekryje výroky, které podněcují k nenávisti vůči skupině obyvatel.",
        "Zaručuje ji Listina základních práv a k ní patří i právo informace přijímat a rozšiřovat.",
        "Znamená, že člověk smí říct svůj názor bez trestu.",
    )),
    ("Poznej tradici.", "Vinobraní", ["burčákové slavnosti"], (
        "Vrcholí, když cukernatost hroznů dosáhne potřebné hodnoty; termín se proto rok od roku posouvá.",
        "Slaví se na jižní Moravě a v Praze na Grébovce a nalévá se při něm zkvašený mošt.",
        "Je to podzimní veselice na oslavu sklizně hroznů.",
    )),
    ("Poznej pojem.", "Exekuce", [], (
        "V Česku byla dlouho výjimečná v tom, že si věřitel mohl vybrat úředníka, který ji povede, kdekoli v zemi.",
        "Provádí se srážkami ze mzdy, blokací účtu nebo prodejem majetku.",
        "Nastane, když dlužník nesplácí a soud nařídí vymáhání.",
    )),
    ("Poznej pojem.", "Dobrovolnictví", [], (
        "Odhaduje se, že jeho hodnota by v ekonomikách vyspělých zemí odpovídala několika procentům HDP.",
        "V Česku ho upravuje zákon a organizace může mít akreditaci ministerstva vnitra.",
        "Je to práce zdarma pro druhé — třeba hasič v obci nebo pomoc v útulku.",
    )),
]

# ==========================================================================
# Čtvrtá dávka
# ==========================================================================

BANK["osobnost"] += [
    ("Poznej známou osobnost.", "Josef Sudek", ["Sudek"], (
        "V první světové válce přišel o pravou ruku a fotoaparát pak obsluhoval jednou rukou, často s pomocí přátel.",
        "Měl ateliér na Újezdě a proslul cyklem snímků z okna svého dvorku.",
        "Říkalo se mu básník Prahy a fotografoval Svatovítskou katedrálu při obnově.",
    )),
    ("Poznej známou osobnost.", "Ada Lovelace", ["Lovelace"], (
        "Byla dcerou básníka lorda Byrona, kterého osobně nikdy nepoznala.",
        "K analytickému stroji Charlese Babbage napsala poznámky delší než původní text.",
        "Bývá označována za první programátorku a nese její jméno programovací jazyk Ada.",
    )),
    ("Poznej známou osobnost.", "Miloš Forman", ["Forman"], (
        "Oba jeho rodiče zahynuli v koncentračních táborech a vychovávali ho příbuzní.",
        "Po roce 1968 zůstal v Americe a stal se profesorem na Kolumbijské univerzitě.",
        "Získal dva Oscary za režii — za Přelet nad kukaččím hnízdem a za Amadea.",
    )),
    ("Poznej známou osobnost.", "Ivan Petrovič Pavlov", ["Pavlov"], (
        "Nobelovu cenu dostal roku 1904 za výzkum trávení, ne za to, čím dnes proslul.",
        "Byl to ruský fyziolog, který si vedl pečlivé záznamy o slinění pokusných zvířat.",
        "Nese jeho jméno podmíněný reflex a pokusy se psy a zvonkem.",
    )),
    ("Poznej známou osobnost.", "Elon Musk", ["Musk"], (
        "Narodil se v Jihoafrické republice a jako student prodal svou první firmu za dvě stě milionů dolarů.",
        "Vede podnik, který jako první přistál s raketovým stupněm zpátky na plošině.",
        "Vlastní automobilku vyrábějící elektromobily a koupil síť, kterou přejmenoval na X.",
    )),
    ("Poznej známou osobnost.", "Zdeněk Fibich", ["Fibich"], (
        "Napsal přes tři sta klavírních skladbiček, které si vedl jako hudební deník o své žačce.",
        "Byl to český skladatel druhé poloviny 19. století, vrstevník Dvořákův.",
        "Jeho Poem se hraje jako svatební skladba i v reklamách.",
    )),
    ("Poznej známou osobnost.", "Sokrates", ["Sókratés"], (
        "Sám nenapsal jediný řádek — všechno, co o něm víme, pochází od jeho žáků a od komediografa Aristofana.",
        "Aténský soud ho odsoudil k smrti za kažení mládeže a on odmítl útěk z vězení.",
        "Vypil číši bolehlavu a proslul větou, že ví, že nic neví.",
    )),
    ("Poznej známou osobnost.", "Eliška Krásnohorská", ["Krásnohorská"], (
        "Od mládí trpěla těžkou revmatickou chorobou, kvůli které nemohla hrát na klavír.",
        "Napsala libreta ke čtyřem Smetanovým operám, mimo jiné k Hubičce a Tajemství.",
        "Prosadila založení prvního dívčího gymnázia ve střední Evropě, které dostalo jméno Minerva.",
    )),
    ("Poznej známou osobnost.", "Kurt Gödel", ["Gödel"], (
        "Narodil se v Brně a ke konci života odmítal jíst jinak než z rukou své ženy ze strachu z otravy.",
        "Byl to logik a matematik, blízký přítel Alberta Einsteina v Princetonu.",
        "Dokázal, že v každé dostatečně bohaté matematické soustavě existují pravdivá tvrzení, která v ní nelze dokázat.",
    )),
    ("Poznej známou osobnost.", "Julius Fučík", ["Fučík"], (
        "Skladatel téhož jména napsal pochod Vjezd gladiátorů, který dodnes zní v cirkusech — jsou to ale dva různí lidé.",
        "Byl to komunistický novinář popravený roku 1943 v Berlíně.",
        "Napsal ve vězení Reportáž psanou na oprátce, která končí výzvou k bdělosti.",
    )),
    ("Poznej známou osobnost.", "Malala Yousafzai", ["Malála", "Malala"], (
        "Psala pod pseudonymem blog pro BBC o životě pod vládou Talibanu ve svých jedenácti letech.",
        "Roku 2012 ji cestou ze školy postřelili do hlavy a přežila.",
        "Roku 2014 se stala nejmladší nositelkou Nobelovy ceny míru v dějinách.",
    )),
    ("Poznej známou osobnost.", "Josef Ressel", ["Ressel"], (
        "Pracoval jako lesmistr v Terstu a technikou se zabýval ve volném čase.",
        "Roku 1829 zkusil svůj vynález na lodi Civetta, ale zásah úřadů pokus zastavil.",
        "Vynalezl lodní šroub a narodil se v Chrudimi.",
    )),
    ("Poznej známou osobnost.", "Vasilij Kandinskij", ["Kandinskij", "Kandinsky"], (
        "Do malířství se pustil až ve třiceti letech; předtím vystudoval práva a ekonomii.",
        "Tvrdil, že vidí barvy jako zvuky, a učil na Bauhausu.",
        "Bývá označován za autora prvního čistě abstraktního obrazu.",
    )),
    ("Poznej známou osobnost.", "Milan Kundera", ["Kundera"], (
        "Roku 1979 mu Československo odebralo občanství a vrátilo mu ho až po čtyřiceti letech.",
        "Od osmdesátých let psal francouzsky a bránil se překladům svých knih do češtiny.",
        "Napsal Nesnesitelnou lehkost bytí a Žert.",
    )),
    ("Poznej známou osobnost.", "Robert Koch", ["Koch"], (
        "Do svých postupů zavedl fotografování bakterií a pevné živné půdy, které umožnily oddělit jednotlivé kmeny.",
        "Byl to německý lékař, jehož čtyři pravidla dodnes určují, kdy lze mikroba označit za původce nemoci.",
        "Objevil původce tuberkulózy, kterému se dodnes říká jeho bacil.",
    )),
    ("Poznej známou osobnost.", "Františka Plamínková", ["Plamínková"], (
        "Pracovala jako učitelka a nesměla se vdát, protože tehdejší předpisy to učitelkám zakazovaly.",
        "Byla senátorkou a zakladatelkou Ženské národní rady.",
        "Prosadila do první československé ústavy rovnost mužů a žen; nacisté ji roku 1942 popravili.",
    )),
    ("Poznej známou osobnost.", "Johannes Kepler", ["Kepler"], (
        "Jeho matku obvinili z čarodějnictví a on ji šest let hájil u soudu, až ji osvobodili.",
        "Působil v Praze na dvoře Rudolfa II. a využil pozorování Tychona Brahe.",
        "Zformuloval tři zákony pohybu planet a zjistil, že obíhají po elipsách.",
    )),
    ("Poznej známou osobnost.", "Karel Zeman", ["Zeman"], (
        "Před filmem pracoval jako aranžér výkladních skříní ve Francii a v Maroku.",
        "Ve zlínských ateliérech spojoval hrané herce s kreslenými a loutkovými kulisami.",
        "Natočil Vynález zkázy a Cestu do pravěku podle Julese Verna.",
    )),
    ("Poznej známou osobnost.", "Elizabeth I.", ["Alžběta I.", "Alžběta První"], (
        "Její matku nechal otec popravit, když jí byly necelé tři roky, a ona sama byla prohlášena za nemanželskou.",
        "Vládla Anglii pětačtyřicet let a nikdy se neprovdala, za což jí říkali Panenská královna.",
        "Za ní porazila Anglie španělskou Armadu a psal Shakespeare.",
    )),
    ("Poznej známou osobnost.", "Bedřich Smetana", ["Smetana"], (
        "Osm let působil ve švédském Göteborgu jako učitel hudby a dirigent.",
        "Poslední léta byl zcela hluchý a zemřel roku 1884 v ústavu pro choromyslné.",
        "Napsal Prodanou nevěstu a cyklus Má vlast.",
    )),
]

BANK["zemepis"] += [
    ("Poznej stát.", "Finsko", [], (
        "Rodiče novorozenců tu od státu dostávají krabici s výbavou, ve které dítě může i spát.",
        "Má přes sto osmdesát tisíc jezer a v Laponsku svítí v létě slunce i o půlnoci.",
        "Jeho hlavním městem je Helsinky a vynašli tu saunu i mobily Nokia.",
    )),
    ("Poznej město.", "Barcelona", [], (
        "Její čtvrť Eixample má bloky se zkosenými rohy, aby se na křižovatkách lépe zatáčelo.",
        "Hostila roku 1992 olympijské hry, které město obrátily zády k vnitrozemí a čelem k moři.",
        "Stojí tu Sagrada Família a hraje tu slavný fotbalový klub.",
    )),
    ("Poznej stát.", "Argentina", [], (
        "Její jméno pochází z latinského slova pro stříbro, které tu ale ve velkém nikdy nenašli.",
        "Leží v ní část Patagonie i nejvyšší hora obou Amerik a tančí se tu tango.",
        "Jejím hlavním městem je Buenos Aires a hrál za ni Maradona.",
    )),
    ("Poznej řeku.", "Odra", [], (
        "Kanál ji spojuje s Labem a po staletí se plánovalo její propojení až k Dunaji.",
        "Pramení v Česku u Oderských vrchů a tvoří část hranice mezi Německem a Polskem.",
        "Roku 1997 se po jejím rozvodnění zaplavila velká část Moravy.",
    )),
    ("Poznej stát.", "Izrael", [], (
        "Jeho vodní hospodářství stojí na odsolování mořské vody a na kapkové závlaze, kterou tu vynalezli.",
        "Vznikl roku 1948 a jeho úředními jazyky jsou hebrejština a arabština.",
        "Leží v něm Jeruzalém a Mrtvé moře.",
    )),
    ("Poznej český kraj.", "Vysočina", [], (
        "Jako jediná z českých samosprávných oblastí nemá jméno podle města ani podle historické země.",
        "Leží na rozhraní Čech a Moravy a její správní sídlo je v Jihlavě.",
        "Stojí tu Telč a poutní kostel na Zelené hoře, oba na seznamu UNESCO.",
    )),
    ("Poznej horu.", "Fudži", ["Fudžisan", "Fuji"], (
        "Je to činná sopka, jejíž poslední výbuch roku 1707 zasypal popelem tehdejší Edo, sto kilometrů daleko.",
        "Stoupá na ni v létě přes dvě stě tisíc lidí ročně a bývá vidět z hlavního města.",
        "Je nejvyšší horou Japonska a má souměrný kužel se zasněženým vrcholem.",
    )),
    ("Poznej stát.", "Etiopie", [], (
        "Má vlastní kalendář, který se od našeho liší o sedm až osm let, a den u nich začíná svítáním.",
        "Jako jediná africká země nikdy nebyla trvale kolonizována a měla vlastního císaře.",
        "Odsud pochází káva a hlavním městem je Addis Abeba.",
    )),
    ("Poznej jezero.", "Viktoriino jezero", ["Jezero Viktoria", "Viktoria"], (
        "Pojmenoval ho roku 1858 John Hanning Speke po britské panovnici a spor o to, jestli je to pramen Nilu, trval roky.",
        "Hraničí s ním tři státy a leží na rovníku ve východní Africe.",
        "Je největším jezerem Afriky a odtéká z něj Bílý Nil.",
    )),
    ("Poznej stát.", "Španělsko", [], (
        "Jeho vysokorychlostní železnice je po Číně druhá nejdelší na světě.",
        "Dělí se na sedmnáct autonomních společenství a mluví se v něm i katalánsky, baskicky a galicijsky.",
        "Leží v něm Madrid a Barcelona a běhá se tu s býky v Pamploně.",
    )),
    ("Poznej město.", "Řím", [], (
        "Uvnitř jeho hranic leží jiný samostatný stát a jeho voda dodnes teče z antických akvaduktů.",
        "Podle pověsti ho založili dva bratři vychovaní vlčicí.",
        "Stojí tu Koloseum a Fontána di Trevi.",
    )),
    ("Poznej ostrov.", "Sicílie", [], (
        "Její poloha uprostřed Středomoří z ní udělala postupně řeckou, kartaginskou, arabskou i normanskou zemi.",
        "Je největším ostrovem Středozemního moře a od pevniny ji dělí Messinská úžina.",
        "Stojí na ní sopka Etna a pochází odsud mafie.",
    )),
    ("Poznej stát.", "Polsko", [], (
        "Přesunulo se po druhé světové válce jako celek zhruba o dvě stě kilometrů na západ.",
        "Má přes třicet osm milionů obyvatel a jeho pobřeží leží u Baltského moře.",
        "Hlavní město je Varšava a nejvyšší hory Tatry sdílí se Slovenskem.",
    )),
    ("Poznej vodní plochu.", "Aralské jezero", ["Aralské moře", "Aral"], (
        "Sovětský plán odvedl jeho přítoky na zavlažování bavlny a plocha se zmenšila o víc než devadesát procent.",
        "Leží mezi Kazachstánem a Uzbekistánem a v písku po něm zůstaly rezavějící lodě.",
        "Bývalo čtvrtým největším jezerem světa a dnes je z něj poušť.",
    )),
    ("Poznej stát.", "Brazílie", [], (
        "Jako jediná země Ameriky mluví portugalsky, protože smlouva z Tordesillas ji přidělila Portugalsku.",
        "Zabírá skoro polovinu Jižní Ameriky a protéká jí Amazonka.",
        "Konal se tu karneval v Riu a pětkrát vyhrála mistrovství světa ve fotbale.",
    )),
    ("Poznej pohoří.", "Himálaj", ["Himaláje"], (
        "Roste asi o centimetr ročně, protože indická deska stále naráží do asijské.",
        "Jméno znamená v sanskrtu sídlo sněhu a leží v něm všech čtrnáct osmitisícovek.",
        "Je to nejvyšší pohoří světa a leží v něm Mount Everest.",
    )),
    ("Poznej město.", "Amsterdam", [], (
        "Domy tu mají háky pod štítem, protože schody jsou tak úzké, že se nábytek stěhuje oknem.",
        "Stojí na dřevěných pilotech v bažině a vede jím přes sto kilometrů kanálů.",
        "Je hlavním městem Nizozemska a jezdí se tu hlavně na kole.",
    )),
    ("Poznej stát.", "Indie", [], (
        "Její ústava je nejdelší psanou ústavou světa a má přes sto tisíc slov.",
        "Uznává dvaadvacet úředních jazyků a od roku 2023 je nejlidnatější zemí světa.",
        "Stojí tu Tádž Mahal a hraje se tu kriket.",
    )),
    ("Poznej české město.", "Olomouc", [], (
        "Bývala hlavním městem Moravy, než o tu úlohu přišla po švédském obléhání v 17. století.",
        "Stojí tu druhá nejstarší univerzita v českých zemích a orloj přestavěný v duchu socialistického realismu.",
        "Je tu sloup Nejsvětější Trojice na seznamu UNESCO a vyrábějí se tu tvarůžky.",
    )),
    ("Poznej stát.", "Jižní Korea", ["Korejská republika"], (
        "Ještě v šedesátých letech patřila mezi nejchudší země světa, chudší než tehdejší Ghana.",
        "Její hospodářství stojí na velkých rodinných konglomerátech, kterým se říká čebol.",
        "Vyrábí se tu Samsung a Hyundai a hlavním městem je Soul.",
    )),
]

BANK["veda"] += [
    ("Poznej chemický prvek.", "Draslík", ["K"], (
        "Jeho značka pochází z latinského kalium, které vzniklo z arabského slova pro popel.",
        "Je tak reaktivní, že se skladuje pod petrolejem a s vodou reaguje výbušně.",
        "Je ho hodně v banánech a jeho nedostatek se projeví křečemi.",
    )),
    ("Poznej vesmírné těleso.", "Slunce", [], (
        "Světlo z jeho jádra putuje k povrchu desítky tisíc let, ale odtud k nám urazí cestu za osm minut.",
        "Tvoří 99,8 procenta hmotnosti celé soustavy a jeho povrch má kolem 5 500 stupňů.",
        "Vychází ráno na východě a Země kolem něj obíhá.",
    )),
    ("Poznej lidský orgán.", "Srdce", [], (
        "Má vlastní elektrický budič, takže bije i mimo tělo, dokud má výživu.",
        "Přečerpá za den kolem sedmi tisíc litrů krve a má čtyři oddíly.",
        "Bije v hrudi a jeho zástava se řeší defibrilátorem.",
    )),
    ("Poznej jev.", "Osmóza", [], (
        "Buňka se v čisté vodě nafoukne a v koncentrovaném roztoku svraští — kořen bývá právě tohle.",
        "Je to průchod rozpouštědla polopropustnou blánou k vyšší koncentraci.",
        "Kvůli ní se okurka v soli scvrkne a rozinka ve vodě nabobtná.",
    )),
    ("Poznej živočicha.", "Medúza", ["medúzy"], (
        "Jeden druh dokáže po dosažení dospělosti přejít zpátky do nedospělého stádia, takže teoreticky nestárne.",
        "Tvoří ji z devadesáti pěti procent voda a nemá mozek ani srdce.",
        "Plave v moři jako průsvitný zvon a její žahavá vlákna pálí.",
    )),
    ("Poznej vědce.", "Antoine Lavoisier", ["Lavoisier"], (
        "Živil se výběrem daní, což mu za revoluce vyneslo gilotinu; matematik Lagrange na to řekl, že takovou hlavu nevytvoří století.",
        "Dokázal vážením, že při hoření se hmota neztrácí, jen mění podobu.",
        "Bývá označován za zakladatele moderní chemie a pojmenoval kyslík.",
    )),
    ("Poznej jev.", "Setrvačnost", ["inercie"], (
        "Popsal ji první ze tří zákonů, které v 17. století sepsal Isaac Newton.",
        "Znamená, že těleso setrvá v klidu nebo v rovnoměrném pohybu, dokud na něj nepůsobí síla.",
        "Kvůli ní se v brzdícím autobuse cestující nakloní dopředu.",
    )),
    ("Poznej chemickou sloučeninu.", "Ethanol", ["etanol", "líh"], (
        "Vzniká činností kvasinek a při obsahu kolem patnácti procent je vlastní kvasinky zabije.",
        "Odbourává ho v játrech enzym alkoholdehydrogenáza rychlostí zhruba deset gramů za hodinu.",
        "Je to alkohol v pivu a ve víně a používá se i k dezinfekci.",
    )),
    ("Poznej lidský smysl.", "Čich", [], (
        "Jeho dráha jako jediná ze smyslů nevede přes mozkový thalamus a napojuje se přímo na paměťová centra.",
        "Proto vyvolá vzpomínku silněji než obraz nebo zvuk; literárně to popsal Marcel Proust.",
        "Ztrácí se při rýmě a byl typickým příznakem covidu.",
    )),
    ("Poznej vesmírný objekt.", "Mléčná dráha", ["Galaxie"], (
        "V jejím středu sedí černá díra o hmotnosti čtyř milionů Sluncí, kterou pojmenovali Sagittarius A*.",
        "Má spirální ramena a naše soustava leží zhruba ve dvou třetinách vzdálenosti od středu.",
        "Za tmavé noci je vidět jako světlý pás přes oblohu.",
    )),
    ("Poznej chemický prvek.", "Dusík", ["N"], (
        "Rostliny ho neumějí brát ze vzduchu samy; pomáhají jim bakterie v hlízkách na kořenech bobovitých.",
        "Tvoří skoro čtyři pětiny vzduchu a v kapalné podobě má minus 196 stupňů.",
        "Jeho sloučeniny jsou základ hnojiv a s vodíkem dává čpavek.",
    )),
    ("Poznej vědce.", "Barbara McClintocková", ["McClintocková", "Barbara McClintock"], (
        "Její objev byl přes třicet let přehlížen a Nobelovu cenu dostala až v jedenaosmdesáti letech.",
        "Pracovala celý život s kukuřicí a barevné skvrny na zrnech jí prozradily, co se v buňce děje.",
        "Zjistila, že geny se v chromozomech přesouvají — objevila takzvané skákající geny.",
    )),
    ("Poznej jev.", "Kapilarita", ["vzlínavost"], (
        "Stromy díky ní spolu s odpařováním z listů dopraví vodu i do stometrové výšky bez čerpadla.",
        "Vzniká z toho, že přitažlivost kapaliny ke stěně je větší než mezi jejími vlastními molekulami.",
        "Kvůli ní nasákne ubrousek a vlhne zdivo od základů.",
    )),
    ("Poznej lidský orgán.", "Kůže", [], (
        "Je největším orgánem těla a dospělý člověk jí má kolem dvou metrů čtverečních.",
        "Vzniká v ní vitamin D a její vrchní vrstva se úplně obmění zhruba za měsíc.",
        "Opálí se na slunci a při popálení puchýřuje.",
    )),
    ("Poznej chemickou sloučeninu.", "Methan", ["metan"], (
        "Za skleníkový efekt je krátkodobě zhruba osmdesátkrát účinnější než oxid uhličitý.",
        "Vzniká rozkladem bez přístupu vzduchu a v dolech se mu říká důlní plyn.",
        "Je hlavní složkou zemního plynu a má vzorec CH₄.",
    )),
    ("Poznej jev.", "Difuze", [], (
        "Popsal ji Robert Brown pozorováním pylových zrn a Einstein ji roku 1905 vysvětlil pohybem molekul.",
        "Jde o samovolné promíchávání látek bez míchání, jen tepelným pohybem částic.",
        "Kvůli ní se vůně parfému rozšíří po celé místnosti.",
    )),
    ("Poznej vědce.", "Jan Janský", ["Janský"], (
        "Původně byl psychiatr a ke krvi ho přivedla domněnka, že by mohla souviset s duševními nemocemi.",
        "Roku 1907 rozdělil krev do čtyř skupin a označil je římskými číslicemi.",
        "Nese jeho jméno plaketa udělovaná dárcům krve.",
    )),
    ("Poznej živočicha.", "Hlemýžď", ["hlemýžď zahradní", "šnek"], (
        "Je obojetník — každý jedinec má samčí i samičí orgány a při páření se oplodní navzájem.",
        "Ulita se mu stáčí skoro vždy doprava; jedinci se závitem doleva jsou vzácnost.",
        "Leze pomalu, nese si domeček na zádech a má tykadla s očima.",
    )),
    ("Poznej jednotku.", "Metr", ["m"], (
        "Původně to měla být desetimiliontina vzdálenosti od pólu k rovníku a měřila se kvůli tomu léta trvající výprava.",
        "Dnes je definován přes rychlost světla a vzorový hranol v Sèvres už neplatí.",
        "Je základní jednotkou délky a má sto centimetrů.",
    )),
    ("Poznej jev.", "Fotosyntéza", [], (
        "Probíhá ve dvou fázích a ta druhá, která poutá uhlík, nepotřebuje světlo přímo.",
        "Odehrává se v chloroplastech a barvivo, které při ní pracuje, se jmenuje chlorofyl.",
        "Rostliny při ní vyrábějí cukr a uvolňují kyslík.",
    )),
]

BANK["kultura"] += [
    ("Poznej film.", "Forrest Gump", [], (
        "Herec, který ho hraje, si nechal vyplatit část honoráře v podílu na tržbách a vydělal víc než na gáži.",
        "Získal roku 1995 šest Oscarů a jeho hrdina se objevuje v dobových záběrech vedle prezidentů.",
        "Padne v něm věta o životě jako o bonboniéře a hrdina běží přes celou Ameriku.",
    )),
    ("Poznej hudební skupinu.", "ABBA", [], (
        "Jméno vzniklo z počátečních písmen křestních jmen členů a museli si vyžádat souhlas rybářské firmy téhož jména.",
        "Roku 1974 vyhráli Eurovizi s písní Waterloo.",
        "Jsou to Švédové a jejich písně nesou muzikál Mamma Mia.",
    )),
    ("Poznej knihu.", "Pán much", ["Lord of the Flies"], (
        "Rukopis odmítlo víc než dvacet nakladatelství a jeden redaktor ho odbyl jako absurdní a nezajímavý.",
        "Napsal ji William Golding, který za své dílo dostal roku 1983 Nobelovu cenu.",
        "Vypráví o chlapcích ztroskotaných na ostrově, kde se rozpadne civilizovaný řád.",
    )),
    ("Poznej film.", "Amélie z Montmartru", ["Amélie"], (
        "Kavárna, ve které hrdinka pracuje, existuje a od premiéry se stala poutním místem turistů.",
        "Natočil ho roku 2001 Jean-Pierre Jeunet a hraje v něm Audrey Tautou.",
        "Hrdinka tajně zlepšuje životy druhých a hledá majitele krabičky z dětství.",
    )),
    ("Poznej obraz.", "Poslední večeře", [], (
        "Autor použil místo fresky experimentální techniku, kvůli které se dílo začalo rozpadat ještě za jeho života.",
        "Je na stěně refektáře kláštera v Miláně a za války do místnosti spadla bomba.",
        "Namaloval ji Leonardo da Vinci a zachycuje okamžik po oznámení zrady.",
    )),
    ("Poznej seriál.", "Chalupáři", [], (
        "Vysílal se roku 1975 a scenárista Jaroslav Dietl v něm zachytil dobovou vášeň pro chataření.",
        "Hrají v něm Josef Kemr, Jaroslava Obermaierová a Luděk Sobota.",
        "Postavy Evžen Huml a Bohouš Císař řeší chalupu v podhůří.",
    )),
    ("Poznej hudební nástroj.", "Klavír", ["piano"], (
        "Jeho italský název znamená doslova tichý-hlasitý, protože na rozdíl od cembala uměl obojí.",
        "Struny rozeznívají plstěná kladívka a rám unese napětí přes dvacet tun.",
        "Má osmaosmdesát kláves, bílých a černých, a stojí v každé hudebce.",
    )),
    ("Poznej film.", "Marečku, podejte mi pero", [], (
        "Vznikl roku 1976 a scénář napsal Ladislav Smoljak se Zdeňkem Svěrákem.",
        "Odehrává se ve večerní škole, kam mistři z továrny chodí dodělat si vzdělání.",
        "Padne v něm hláška o slupkách zbavených zrn ječmene a hraje tu Jiří Sovák.",
    )),
    ("Poznej stavbu.", "Opera v Sydney", ["Sydney Opera House"], (
        "Návrh vytáhl z koše porotce, který přijel pozdě; rozpočet se nakonec překročil čtrnáctkrát.",
        "Autorem je Dán Jørn Utzon, který stavbu ve sporech opustil a hotovou ji nikdy neviděl.",
        "Její bílé skořepiny stojí v přístavu australského největšího města.",
    )),
    ("Poznej českou kapelu.", "Lucie", [], (
        "Vznikla roku 1985 a jméno si dala podle písně, kterou tehdy zpívala jiná kapela.",
        "Jejími členy jsou David Koller a Robert Kodym.",
        "Zpívá Medvídka a Chci zas v tobě spát.",
    )),
    ("Poznej film.", "Pulp Fiction", ["Historky z podsvětí"], (
        "Vypráví se v nezvyklém pořadí, takže postava, která zemře uprostřed, je v závěru zase naživu.",
        "Natočil ho roku 1994 Quentin Tarantino a získal Zlatou palmu v Cannes.",
        "John Travolta a Samuel L. Jackson v něm hrají dvojici gangsterů a řeší se v něm hamburger.",
    )),
    ("Poznej hudební žánr.", "Opera", [], (
        "Vznikla kolem roku 1600 ve Florencii ze snahy obnovit antické divadlo, kde se prý zpívalo.",
        "Zpěvák v ní musí přezpívat orchestr bez zesílení, což určuje celou techniku hlasu.",
        "Nejznámější domy jsou La Scala a Metropolitní; v Praze Národní divadlo.",
    )),
    ("Poznej knihu.", "Robinson Crusoe", ["Robinson"], (
        "Předlohou byl skotský námořník Alexander Selkirk, který strávil čtyři roky sám na ostrově u Chile.",
        "Napsal ji roku 1719 Daniel Defoe a bývá označována za první anglický román.",
        "Hrdina ztroskotá, staví si přístřešek a potká domorodce, kterému dá jméno Pátek.",
    )),
    ("Poznej film.", "Tenkrát na Západě", ["Once Upon a Time in the West"], (
        "Hudba vznikla dřív než film a herci ji na place poslouchali, aby se do ní vešli.",
        "Režíroval ho Sergio Leone a hudbu složil Ennio Morricone.",
        "Charles Bronson v něm hraje na foukací harmoniku a Henry Fonda je poprvé záporák.",
    )),
    ("Poznej českou stavbu.", "Tančící dům", [], (
        "Původně se mu říkalo Ginger a Fred podle tanečního páru a stojí na místě domu zbořeného náletem roku 1945.",
        "Navrhli ho Vlado Milunić a Frank Gehry a otevřel se roku 1996.",
        "Stojí na pražském nábřeží a vypadá, jako by se prohýbal.",
    )),
    ("Poznej hudebníka.", "Louis Armstrong", ["Armstrong"], (
        "Vyrůstal v sirotčinci pro černošské chlapce, kde ho poprvé postavili k nástroji.",
        "Přezdívalo se mu Satchmo a proslul chraplavým hlasem i improvizací na trubku.",
        "Zpívá What a Wonderful World.",
    )),
    ("Poznej knihu.", "Bible", [], (
        "Je nejtištěnější knihou dějin a její první tištěné vydání pochází z Gutenbergovy dílny.",
        "Dělí se na Starý a Nový zákon a do češtiny ji v 16. století přeložili Bratři jako Kralickou.",
        "Začíná stvořením světa a obsahuje evangelia.",
    )),
    ("Poznej film.", "Přelet nad kukaččím hnízdem", ["Přelet nad kukaččím hnízdem", "One Flew Over the Cuckoo's Nest"], (
        "Natáčelo se ve skutečné psychiatrické léčebně v Oregonu a část komparzu tvořili pacienti.",
        "Získal roku 1976 všech pět hlavních Oscarů, což se povedlo jen třem filmům v dějinách.",
        "Režíroval ho Miloš Forman a hlavní roli hraje Jack Nicholson.",
    )),
    ("Poznej hudební dílo.", "Osudová symfonie", ["Beethovenova Pátá", "Symfonie č. 5"], (
        "Její úvodní rytmus se za války vysílal do okupované Evropy, protože v Morseově abecedě znamená písmeno V jako vítězství.",
        "Autor na ní pracoval čtyři roky a premiéra roku 1808 proběhla v nevytopeném sále na čtyřhodinovém koncertu.",
        "Začíná čtyřmi tóny, o kterých se říká, že tak klepe osud na dveře.",
    )),
    ("Poznej malíře.", "Claude Monet", ["Monet"], (
        "V zahradě v Giverny si nechal vykopat rybník a postavit japonský můstek, aby měl co malovat.",
        "Podle jeho obrazu Imprese, východ slunce dostal jméno celý umělecký směr.",
        "Maloval katedrálu v Rouenu v různých hodinách dne a lekníny.",
    )),
]

BANK["historie"] += [
    ("Poznej událost.", "Křižácké výpravy", ["křížové výpravy"], (
        "Jedna z nich vůbec nedošla do Svaté země a místo toho vyplenila křesťanskou Konstantinopol.",
        "Vyhlásil je roku 1095 papež Urban II. na koncilu v Clermontu.",
        "Jejich cílem bylo dobýt Jeruzalém a jejich účastníci nosili na plášti kříž.",
    )),
    ("Poznej panovníka.", "Ludvík XIV.", ["Ludvík Čtrnáctý"], (
        "Nastoupil ve čtyřech letech a vládl dvaasedmdesát let, což je v Evropě rekord.",
        "Nechal přestavět lovecký zámeček ve Versailles a přestěhoval tam celý dvůr, aby měl šlechtu pod dohledem.",
        "Říkalo se mu král Slunce a připisuje se mu věta „stát jsem já“.",
    )),
    ("Poznej událost.", "Bitva u Stalingradu", ["Stalingrad"], (
        "Bojovalo se dům od domu a jedna obytná budova, kterou bránila hrstka vojáků, vydržela déle než celá Francie.",
        "Trvala od srpna 1942 do února 1943 a skončila kapitulací 6. armády s polním maršálem Paulusem.",
        "Bývá označována za obrat druhé světové války na východní frontě.",
    )),
    ("Poznej dokument.", "Deklarace nezávislosti", ["Deklarace nezávislosti USA"], (
        "Nejnápadnější podpis patří Johnu Hancockovi a jeho jméno se v angličtině stalo synonymem pro podpis.",
        "Sepsal ji hlavně Thomas Jefferson a mluví o právu na život, svobodu a hledání štěstí.",
        "Přijali ji 4. července 1776 a připomíná ji americký státní svátek.",
    )),
    ("Poznej období.", "Velká Morava", ["Velkomoravská říše"], (
        "Ani po desítkách let výzkumu se badatelé neshodli, kde přesně leželo její hlavní sídlo Veligrad.",
        "Zanikla na začátku 10. století po vpádech Maďarů a vnitřních sporech.",
        "Pozval si sem kníže Rastislav Cyrila a Metoděje.",
    )),
    ("Poznej událost.", "Pád Říma", ["zánik Západořímské říše"], (
        "Za formální konec se bere rok 476, kdy germánský velitel Odoaker sesadil posledního císaře-chlapce.",
        "Předcházelo mu vyplenění města Vizigóty roku 410 a Vandaly roku 455.",
        "Ukončil starověk a začal jím středověk.",
    )),
    ("Poznej stavbu.", "Pražský hrad", ["Hrad"], (
        "Podle Guinnessovy knihy je to největší souvislý hradní komplex na světě.",
        "Založil ho v 9. století kníže Bořivoj a poslední velkou úpravu mu dal architekt Plečnik.",
        "Sídlí tu prezident a stojí v něm katedrála svatého Víta.",
    )),
    ("Poznej událost.", "Únor 1948", ["únorový převrat", "Vítězný únor"], (
        "Spustila ho demise dvanácti nekomunistických ministrů, kteří počítali s tím, že prezident vypíše volby.",
        "Prezident Beneš demisi po týdnu nátlaku a manifestací přijal.",
        "Znamenal nástup komunistů k moci v Československu na čtyřicet let.",
    )),
    ("Poznej civilizaci.", "Aztékové", ["Aztécká říše"], (
        "Jejich hlavní město stálo na ostrově v jezeře a plovoucí zahrady zvané chinampy uživily statisíce lidí.",
        "Vládl jim Moctezuma, když roku 1519 dorazili Španělé pod vedením Hernána Cortése.",
        "Přinášeli lidské oběti a na místě jejich města dnes stojí Ciudad de México.",
    )),
    ("Poznej vynález.", "Papírové peníze", ["bankovky"], (
        "V Číně je zavedli už v 11. století a Evropa se k nim dostala o šest set let později ve Švédsku.",
        "Jejich hodnota nestojí na materiálu, ale na důvěře, že je někdo přijme.",
        "Dnes se tisknou na bavlněný papír s vodoznakem a ochranným proužkem.",
    )),
    ("Poznej událost.", "Světová hospodářská krize", ["Velká hospodářská krize"], (
        "Spustila ji panika na newyorské burze v říjnu 1929, které se říká Černý čtvrtek a Černé úterý.",
        "V Německu z ní vytěžili nacisté a v USA na ni Roosevelt odpověděl Novým údělem.",
        "V Československu při ní nezaměstnanost přesáhla milion lidí a nejhůř dopadlo pohraničí.",
    )),
    ("Poznej panovnici.", "Viktorie", ["královna Viktorie"], (
        "Po smrti manžela Alberta nosila čtyřicet let černou a skoro se neukazovala na veřejnosti.",
        "Vládla třiašedesát let a devět jejích dětí se provdalo do evropských dvorů.",
        "Nese její jméno celá epocha a bývá symbolem britského impéria.",
    )),
    ("Poznej událost.", "Zavraždění Františka Ferdinanda", ["sarajevský atentát", "atentát v Sarajevu"], (
        "První pokus téhož dne selhal, bomba se odrazila a vybuchla u dalšího vozu; k druhému došlo náhodou, když řidič špatně zabočil.",
        "Odehrálo se 28. června 1914 a útočník patřil ke skupině Mladá Bosna.",
        "Rozpoutalo první světovou válku.",
    )),
    ("Poznej stavbu.", "Chrám svatého Víta", ["katedrála svatého Víta", "svatý Vít"], (
        "Stavěl se s přestávkami skoro šest set let a dostavěl se až roku 1929.",
        "První stavitel Matyáš z Arrasu zemřel brzy a dílo dokončoval Petr Parléř se svou hutí.",
        "Stojí na Pražském hradě a jsou v něm uloženy korunovační klenoty.",
    )),
    ("Poznej období.", "Osvícenství", [], (
        "Jeho symbolem byla Encyklopedie, na které se pod vedením Diderota podílelo přes sto padesát autorů.",
        "Kladlo rozum a zkušenost nad tradici a autoritu a vyústilo v reformy i revoluce.",
        "Patří do něj Voltaire, Rousseau a u nás reformy Josefa II.",
    )),
    ("Poznej událost.", "Bitva u Lipan", ["Lipany"], (
        "Rozhodl ji předstíraný ústup, po kterém se vozová hradba otevřela a jezdectvo vjelo dovnitř.",
        "Odehrála se roku 1434 mezi husitskými svazy a znamenala konec radikálního křídla.",
        "Padl v ní Prokop Holý a otevřela cestu ke smíru s císařem.",
    )),
    ("Poznej říši.", "Osmanská říše", ["Osmani", "Turecká říše"], (
        "Její elitní pěchotu tvořili chlapci odvedení z křesťanských rodin, vychovaní jako muslimové.",
        "Trvala přes šest set let a zanikla po první světové válce.",
        "Roku 1683 marně obléhala Vídeň a jejím vládcům se říkalo sultán.",
    )),
    ("Poznej dokument.", "Toleranční patent", [], (
        "Vydal ho roku 1781 týž panovník, který o pár týdnů dřív zrušil nevolnictví.",
        "Povolil vedle katolictví ještě luterány, kalvinisty a pravoslavné — ne však bez omezení.",
        "Nekatolické modlitebny podle něj nesměly mít věž ani vchod z ulice.",
    )),
    ("Poznej událost.", "Sarajevská olympiáda", ["olympiáda v Sarajevu"], (
        "Sportoviště, na kterých se závodilo, se za necelých deset let ocitla uprostřed obležení a bobová dráha sloužila jako palebné postavení.",
        "Konala se roku 1984 v Jugoslávii a maskotem byl vlček Vučko.",
        "Vyhrála na ní Katarina Wittová a Torvill s Deanovou dostali samé šestky za Bolero.",
    )),
    ("Poznej období.", "Baroko", [], (
        "Slovo původně označovalo nepravidelnou perlu a jako název slohu se zprvu užívalo posměšně.",
        "Bylo dobou protireformace a jeho stavby pracují s dramatickým světlem a pohybem.",
        "V Čechách jsou z něj Santiniho kostely a hudbu psali Bach a Vivaldi.",
    )),
]

BANK["priroda"] += [
    ("Poznej živočicha.", "Tygr", [], (
        "Vzor pruhů má na kůži, ne jen na srsti, a je u každého jedince jiný jako otisk prstu.",
        "Je největší kočkovitou šelmou a na rozdíl od většiny koček rád plave.",
        "Žije v Asii a jeho sibiřský poddruh snese padesátistupňové mrazy.",
    )),
    ("Poznej rostlinu.", "Tabák", ["tabák virginský"], (
        "Látka, kvůli které se pěstuje, je pro rostlinu přirozený insekticid proti hmyzu.",
        "Do Evropy ho přivezli Španělé a jméno mu dal francouzský vyslanec Jean Nicot.",
        "Suší se z něj listy a balí do cigaret.",
    )),
    ("Poznej živočicha.", "Kosatka dravá", ["kosatka"], (
        "Skupiny mluví odlišnými nářečími hvizdů a některé loví způsobem, který se předává jen v dané rodině.",
        "Je to největší zástupce delfínovitých a samice žijí i po skončení plodnosti, což je u zvířat vzácné.",
        "Má černobílé zbarvení a přezdívá se jí velryba zabiják.",
    )),
    ("Poznej strom.", "Bříza", ["bříza bělokorá"], (
        "Bílá kůra jí odráží zimní slunce a chrání kmen před popálením mrazem.",
        "Roste rychle na spáleništích a výsypkách a její míza se na jaře sbírá.",
        "Má bílý kmen s černými skvrnami a dělá se z ní koště.",
    )),
    ("Poznej živočicha.", "Mloka skvrnitého", ["mlok skvrnitý", "mlok"], (
        "Jako jediný náš obojživelník rodí živá mláďata, respektive larvy rovnou do potoka.",
        "Žlutočerné zbarvení je varovné a z kožních žláz vylučuje jedovatý sekret.",
        "Vylézá po dešti na lesních cestách v Beskydech i na Šumavě.",
    )),
    ("Poznej rostlinu.", "Kopretina", ["kopretina bílá"], (
        "To, co vypadá jako jeden květ, je ve skutečnosti celé květenství složené ze stovek drobných kvítků.",
        "Bílé okrajové jazykovité kvítky lákají hmyz, žlutý střed nese semena.",
        "Trhá se na louce a otrhává se při „má mě ráda, nemá mě ráda“.",
    )),
    ("Poznej živočicha.", "Zebra", [], (
        "Nejnovější výzkumy naznačují, že pruhy hlavně matou bodavý hmyz, ne šelmy.",
        "Nikdy se ji nepodařilo spolehlivě domestikovat a v zajetí bývá agresivnější než kůň.",
        "Žije v africké savaně a její vzor dal jméno přechodu pro chodce.",
    )),
    ("Poznej rostlinu.", "Kaktus", ["kaktusy"], (
        "Jeho trny jsou přeměněné listy a fotosyntézu za ně obstarává zelený stonek.",
        "Rostou skoro výhradně v Americe a v noci otevírají průduchy, aby ušetřily vodu.",
        "Mají píchající trny a rostou v poušti.",
    )),
    ("Poznej živočicha.", "Kondor", ["kondor andský", "kondor velký"], (
        "Nemá hlasivky, takže vydává jen sípavé zvuky, a hlavu má holou kvůli hygieně při krmení.",
        "Má největší rozpětí křídel ze všech dravých ptáků a plachtí bez jediného mávnutí i hodiny.",
        "Žije v Andách a je na státním znaku několika jihoamerických zemí.",
    )),
    ("Poznej houbu.", "Kvasinka", ["kvasinky", "pivní kvasinky"], (
        "Rozmnožuje se pučením a její genom byl roku 1996 prvním kompletně přečteným u složitější buňky.",
        "Přeměňuje cukr na alkohol a oxid uhličitý, čehož se využívá dvěma různými směry.",
        "Kvasí díky ní pivo a kyne díky ní chleba.",
    )),
    ("Poznej živočicha.", "Labuť velká", ["labuť"], (
        "Má krční obratlů kolem pětadvaceti, víc než kterýkoli jiný pták.",
        "V Británii patří všechny volně žijící kusy formálně panovníkovi a jednou ročně se sčítají.",
        "Je bílá s dlouhým krkem a plave na rybníce; Čajkovskij o ní napsal balet.",
    )),
    ("Poznej rostlinu.", "Kaštanovník", ["kaštanovník setý", "jedlý kaštan"], (
        "Se stromem, jehož plody sbírají české děti na podzim, není příbuzný — ten pochází z Balkánu.",
        "Roste ve Středomoří a jeho plody se pekly jako náhrada obilí v horských oblastech.",
        "Praží se z něj plody, které se prodávají v kornoutu na vánočních trzích.",
    )),
    ("Poznej živočicha.", "Škvor", ["škvor obecný"], (
        "Samice hlídá vajíčka a olizuje je proti plísni, což je u hmyzu neobvyklá péče o potomstvo.",
        "Klíšťky na konci zadečku slouží k obraně a k rozkládání křídel, která skoro nepoužívá.",
        "Vlezl podle pověr lidem do ucha, ačkoli to není pravda.",
    )),
    ("Poznej rostlinu.", "Bez černý", ["černý bez", "bez"], (
        "Jeho dřeň se dřív používala v mikroskopii k upínání tenkých řezů.",
        "Syrové plody i listy obsahují látku, která se rozkládá teprve varem.",
        "Kvete bílými talíři, dělá se z něj sirup a v lidovém léčitelství čaj na potní kúru.",
    )),
    ("Poznej živočicha.", "Pavouk křižák", ["křižák obecný", "křižák"], (
        "Síť staví každý večer znovu a starou sní, aby neztratil bílkovinu.",
        "Jeho vlákno je při stejné tloušťce pevnější než ocel a laboratoře se ho marně snaží napodobit.",
        "Má na hřbetě světlý kříž a sedí uprostřed kruhové sítě v zahradě.",
    )),
    ("Poznej jev.", "Fotoperiodismus", ["fotoperioda"], (
        "Rostliny neměří délku dne, ale nepřerušené tmy — stačí krátký záblesk v noci a kvetení se zastaví.",
        "Za měření odpovídá barvivo fytochrom, které mění tvar podle světla.",
        "Kvůli němu kvetou chryzantémy na podzim a jahody v létě.",
    )),
    ("Poznej živočicha.", "Sysel", ["sysel obecný"], (
        "V Česku patří k nejohroženějším savcům a přežívá hlavně na letištích a golfových hřištích, kde se seká tráva.",
        "Zimu prospí v noře a tělesná teplota mu klesne skoro k bodu mrazu.",
        "Postaví se na zadní jako sloupek a je předlohou úsloví o tvrdém spánku.",
    )),
    ("Poznej rostlinu.", "Jetel", ["jetel luční"], (
        "Na kořenech mu žijí bakterie, které poutají vzdušný dusík, takže půdu obohacuje místo aby ji vyčerpával.",
        "Seje se jako pícnina a jeho zaorávání bylo základem trojhonného hospodaření.",
        "Má trojlístek a nález čtyřlístku prý přináší štěstí.",
    )),
    ("Poznej živočicha.", "Perloočka", ["perloočky", "hrotnatka"], (
        "Má průhledné tělo, takže se jí pod mikroskopem pozoruje tep srdce zaživa.",
        "Rozmnožuje se většinu roku bez samců a teprve před zimou vytvoří odolná vajíčka.",
        "Je to drobný korýš v rybníce a suší se jako krmivo pro akvarijní ryby.",
    )),
    ("Poznej jev.", "Symbióza", [], (
        "Lišejník je její učebnicový příklad — je to houba a řasa dohromady, ne jeden organismus.",
        "Rozlišuje se od parazitismu tím, že prospěch má obě strany.",
        "Patří sem i bakterie ve střevech nebo mravenci pečující o mšice.",
    )),
]

BANK["technika"] += [
    ("Poznej vynález.", "Tranzistor", [], (
        "Jeho objevitelé dostali roku 1956 Nobelovu cenu a jeden z nich pak stál u zrodu Silicon Valley.",
        "Nahradil elektronku, protože nepotřeboval žhavení a vešel se do zlomku prostoru.",
        "Je jich miliarda v každém procesoru a bez něj by nebyl počítač.",
    )),
    ("Poznej stavbu.", "Vodní elektrárna", ["vodní dílo", "hydroelektrárna"], (
        "Přečerpávací varianta v noci vodu čerpá nahoru a ve špičce ji pouští dolů — funguje jako obří baterie.",
        "V Česku je největší Dlouhé stráně v Jeseníkách, ukrytá uvnitř hory.",
        "Vyrábí elektřinu z padající vody a její turbínu vynalezl Viktor Kaplan.",
    )),
    ("Poznej vynález.", "Sirka", ["sirky"], (
        "Bezpečná podoba přesunula fosfor ze špičky na škrtátko, takže se nedá zapálit o cokoli.",
        "V Sušici z nich byla za Rakouska největší továrna v monarchii.",
        "Škrtne se o krabičku a zapálí se jí svíčka.",
    )),
    ("Poznej techniku.", "Kryptografie", ["šifrování"], (
        "Dnešní veřejná varianta stojí na tom, že vynásobit dvě velká prvočísla je snadné, ale rozložit součin zpátky ne.",
        "Používali ji už Římané prostým posunem abecedy, kterému se říká Caesarova šifra.",
        "Díky ní nikdo nepřečte, co posíláš v aplikaci nebo platíš kartou.",
    )),
    ("Poznej vozidlo.", "Tramvaj", ["tramvaje"], (
        "Nejdřív ji tahali koně a teprve roku 1891 předvedl František Křižík v Praze její elektrickou podobu.",
        "Napájí se ze stejnosměrné troleje a proud se vrací kolejnicemi.",
        "Jezdí po kolejích v ulicích a v Brně se jí říká šalina.",
    )),
    ("Poznej vynález.", "Chladnička", ["lednice"], (
        "Dřív se v ní jako chladivo používal čpavek nebo oxid siřičitý, které byly nebezpečné při úniku.",
        "Freony, které je nahradily, se ukázaly jako škodlivé pro ozonovou vrstvu a Montrealský protokol je zakázal.",
        "Stojí v každé kuchyni a v mrazáku má minus osmnáct.",
    )),
    ("Poznej stroj.", "Turbína", [], (
        "Její název pochází z latinského slova pro vír a nejrozšířenější vodní typ navrhl Čech.",
        "Přeměňuje pohyb tekutiny na otáčení hřídele a v elektrárně žene generátor.",
        "Pohání ji pára, voda nebo vítr.",
    )),
    ("Poznej techniku.", "Digitální fotoaparát", ["digitál"], (
        "První prototyp postavil roku 1975 inženýr Kodaku, ale firma se bála, že si sama podřízne film.",
        "Snímek zachycuje čip CCD nebo CMOS a ukládá se na paměťovou kartu.",
        "Nahradil kinofilm a je dnes v každém telefonu.",
    )),
    ("Poznej dopravní prostředek.", "Lanovka", ["lanová dráha"], (
        "Nejstarší v Česku vede na Petřín a její vozy se vyvažují napouštěním a vypouštěním vody v nádrži.",
        "Pohyb obstarává tažné lano navíjené v horní stanici a dva vozy se vzájemně vyvažují.",
        "Vozí lyžaře na kopec a v horách se jí jezdí na výhledy.",
    )),
    ("Poznej vynález.", "Elektrokardiograf", ["EKG"], (
        "Willem Einthoven za jeho vývoj dostal roku 1924 Nobelovu cenu a jeho první přístroj vážil přes dvě stě kilo.",
        "Zaznamenává elektrické napětí, které vzniká při stahu svalu, a křivku popisují vlny označené písmeny.",
        "Nalepí se elektrody na hrudník a papír vyjede se záznamem tepu.",
    )),
    ("Poznej stavbu.", "Větrná elektrárna", ["větrník", "větrná turbína"], (
        "Listy má obvykle tři, protože sudý počet by při míjení stožáru způsoboval nerovnoměrné zatížení.",
        "Špička listu se pohybuje rychlostí přes 250 km/h, i když se celek otáčí pomalu.",
        "Stojí na kopci a vyrábí elektřinu z větru.",
    )),
    ("Poznej techniku.", "Autopilot", [], (
        "První použitelné zařízení předvedl roku 1914 Lawrence Sperry tak, že za letu vstal a odešel od řízení.",
        "Stojí na gyroskopech a dnes zvládne i přistání za nulové viditelnosti.",
        "Drží letadlo v kurzu, aniž by pilot držel knipl.",
    )),
    ("Poznej vynález.", "Mikroskop", [], (
        "Světelný typ nemůže rozlišit detaily menší než zhruba polovina vlnové délky světla — to je fyzikální strop.",
        "Elektronová varianta ho obešla použitím svazku elektronů místo světla.",
        "Dívá se jím na kapku vody a vidí prvoky.",
    )),
    ("Poznej materiál.", "Ocel", [], (
        "Od litiny se liší obsahem uhlíku — pod dvěma procenty je kujná, nad tím křehká.",
        "Nerezavějící podobu dělá chrom, který na povrchu vytvoří neviditelnou ochrannou vrstvičku.",
        "Vyrábí se z železné rudy ve vysoké peci a staví se z ní mosty.",
    )),
    ("Poznej techniku.", "Robotika", ["roboti"], (
        "Tři zákony, které se s oborem spojují, vymyslel spisovatel Isaac Asimov, ne inženýr.",
        "Průmyslové rameno se programuje tak, že ho člověk provede pohybem a stroj si ho zapamatuje.",
        "Slovo pro její stroje vzniklo v Čapkově hře R.U.R.",
    )),
    ("Poznej vynález.", "Sluchátka", [], (
        "První pár vyrobil roku 1910 Nathaniel Baldwin ve své kuchyni a americké námořnictvo mu nechtělo věřit.",
        "Aktivní potlačení hluku funguje tak, že se k okolnímu zvuku přehraje jeho převrácená podoba.",
        "Nasadí se na uši a poslouchá se v nich hudba.",
    )),
    ("Poznej stavbu.", "Mrakodrap", [], (
        "Bez dvou vynálezů by nevznikl: bezpečnostní brzdy ve výtahu a ocelové kostry, která nese váhu místo zdí.",
        "První stavby toho druhu vyrostly v Chicagu po požáru roku 1871.",
        "Nejvyšší dnes stojí v Dubaji a měří přes 800 metrů.",
    )),
    ("Poznej techniku.", "Kvantový počítač", [], (
        "Jeho základní jednotka může být v obou stavech naráz, což u obyčejného bitu nejde.",
        "Musí se chladit skoro k absolutní nule, protože sebemenší otřes výpočet zničí.",
        "Sliboval by rozlousknout dnešní šifrování a zatím jsou to laboratorní stroje.",
    )),
    ("Poznej vynález.", "Kompas", [], (
        "Číňané ho zprvu používali k orientaci staveb podle nauky feng-šuej, ne k plavbě.",
        "Jeho střelka neukazuje k zeměpisnému pólu, ale k magnetickému, který se stále posouvá.",
        "Vždycky ukáže na sever a bere se na túru s mapou.",
    )),
    ("Poznej stroj.", "Bagr", ["rypadlo"], (
        "Největší kolesová stroj svého druhu na světě váží přes třináct tisíc tun a jezdí v německých hnědouhelných dolech.",
        "Pásový podvozek rozloží váhu tak, aby stroj nezapadl do měkkého terénu.",
        "Hloubí základy a nakládá zeminu lžící na rameni.",
    )),
]

BANK["sport"] += [
    ("Poznej sport.", "Rychlobruslení", [], (
        "Sklápěcí brusle s odklápěcí patou přinesly v devadesátých letech skokové zlepšení všech rekordů.",
        "Závodí se ve dvojicích proti sobě a v půlce kola se dráhy povinně kříží.",
        "Jezdí se v aerodynamickém trikotu na oválu dlouhém 400 metrů.",
    )),
    ("Poznej sportovce.", "Roman Šebrle", ["Šebrle"], (
        "Jako první člověk na světě překonal ve své disciplíně hranici devíti tisíc bodů.",
        "V Athénách roku 2004 získal olympijské zlato a předtím i po tom sbíral tituly z halových šampionátů.",
        "Je to český desetibojař.",
    )),
    ("Poznej sport.", "Softbal", [], (
        "Vznikl jako halová obdoba jiné hry a jméno má po měkčím míči, který se ale dnes měkký nezdá.",
        "Nadhazuje se spodem a hřiště je menší, takže se hraje jen sedm směn.",
        "Je to příbuzný baseballu, u nás populární hlavně mezi ženami.",
    )),
    ("Poznej klub.", "Kometa Brno", ["Kometa", "HC Kometa Brno"], (
        "V padesátých letech vyhrála jedenáct titulů v řadě jako armádní klub pod jiným jménem.",
        "Po roce 2009 se vrátila do nejvyšší soutěže a hraje v modrobílém.",
        "Je to nejúspěšnější hokejový klub druhého největšího českého města.",
    )),
    ("Poznej sport.", "Fotbal", ["kopaná"], (
        "Pravidlo o postavení mimo hru je jediné, které se od roku 1863 měnilo prakticky nepřetržitě.",
        "Hraje jedenáct hráčů na každé straně a rozhodčí má od roku 1970 žluté a červené karty.",
        "Kope se do míče a nejslavnější klubovou soutěží je Liga mistrů.",
    )),
    ("Poznej sportovkyni.", "Martina Sáblíková", ["Sáblíková"], (
        "Trénuje pod vedením Petra Nováka a v létě jezdí závodně na kole.",
        "Získala tři olympijská zlata na dlouhých tratích a řadu titulů mistryně světa.",
        "Je to česká rychlobruslařka z Nového Města na Moravě.",
    )),
    ("Poznej sport.", "Squash", [], (
        "Vznikl ve vězení Fleet v Londýně, kde si vězni odráželi míček od zdi.",
        "Jméno má podle měkkého míčku, který se při nárazu zmáčkne, a před hrou se musí zahřát.",
        "Hraje se raketou proti stěně v uzavřené místnosti.",
    )),
    ("Poznej sportovce.", "Tomáš Berdych", ["Berdych"], (
        "Roku 2004 v Athénách porazil jako mladíček Rogera Federera, který byl tehdy světovou jedničkou.",
        "Ve Wimbledonu roku 2010 došel do finále, kde nestačil na Rafaela Nadala.",
        "Je to český tenista z Valašského Meziříčí, který v žebříčku vystoupal na čtvrté místo.",
    )),
    ("Poznej sportovní akci.", "Velká pardubická", [], (
        "Nejobtížnější překážkou je Taxisův příkop, který se po protestech několikrát zmírňoval.",
        "Jede se od roku 1874 vždy druhou říjnovou neděli.",
        "Je to nejtěžší kontinentální dostih a jezdec Josef Váňa ho vyhrál osmkrát.",
    )),
    ("Poznej sport.", "Florbal", [], (
        "Vznikl v sedmdesátých letech ve Švédsku z dětské hry s plastovými hokejkami.",
        "Míček má třiadvacet dírek a hraje se pět na pět plus brankář, který nemá hokejku.",
        "Je to halová obdoba hokeju s plastovou hokejkou a Česko v něm patří ke světové špičce.",
    )),
    ("Poznej sportovce.", "Karel Loprais", ["Loprais"], (
        "Přezdívalo se mu Král pouště a jeho synovec v závodě pokračoval.",
        "Vyhrál šestkrát Rallye Dakar v kategorii nákladních automobilů.",
        "Jezdil s vozem Tatra 815.",
    )),
    ("Poznej sport.", "Zápas", ["řecko-římský zápas", "wrestling"], (
        "Dělí se na dva styly a v jednom z nich se nesmí sahat pod pás ani používat nohy.",
        "Je to jeden z nejstarších olympijských sportů a bojuje se na kruhové žíněnce.",
        "Vítězí se položením soupeře na lopatky.",
    )),
    ("Poznej trofej.", "Zlatá hokejka", [], (
        "Uděluje se od roku 1969 a nejvíc jich má Jaromír Jágr — dvanáct.",
        "Hlasují o ní hráči nejvyšší soutěže i reprezentanti.",
        "Dostává ji vítěz ankety o nejlepšího českého hráče ledního sportu za sezonu.",
    )),
    ("Poznej sport.", "Krosový běh", ["přespolní běh", "kros"], (
        "Byl olympijským sportem jen třikrát; v Paříži roku 1924 skončil kvůli vedru tak, že do cíle doběhla necelá polovina.",
        "Běží se v terénu přes bláto, kopce a přírodní překážky.",
        "Na podzim se v něm konají závody v lesích a parcích.",
    )),
    ("Poznej sportovce.", "Petra Kvitová", ["Kvitová"], (
        "Roku 2016 jí útočník v jejím bytě pořezal ruku, kterou drží raketu, a k tenisu se vrátila po pěti měsících.",
        "Pochází z Fulneku a hraje levou rukou.",
        "Vyhrála dvakrát Wimbledon, v letech 2011 a 2014.",
    )),
    ("Poznej sport.", "Sportovní lezení", ["lezení"], (
        "Obtížnost cest se u nás značí francouzskou stupnicí a nejtěžší přelezené se pohybují kolem devítky.",
        "Na olympiádě se objevilo poprvé roku 2021 a spojovalo tři disciplíny do jednoho pořadí.",
        "Leze se po umělé stěně s chyty a jistí se lanem.",
    )),
    ("Poznej klub.", "Bayern Mnichov", ["Bayern"], (
        "Jeho zakladatelé odešli roku 1900 z jiného klubu kvůli sporu o vstup do německého fotbalového svazu.",
        "Vyhrál Ligu mistrů šestkrát a jeho stadion se jmenuje Allianz Arena.",
        "Je to nejúspěšnější německý fotbalový klub.",
    )),
    ("Poznej sport.", "Skeleton", [], (
        "Jméno prý dostal podle kostry, které se první ocelové sáně podobaly.",
        "Jezdí se hlavou napřed na břiše a rychlost přesahuje 130 km/h.",
        "Je to zimní olympijský sport na ledové dráze, příbuzný bobů.",
    )),
    ("Poznej sportovce.", "Jarmila Kratochvílová", ["Kratochvílová"], (
        "Její světový rekord z roku 1983 je nejdéle platným rekordem v atletice vůbec.",
        "Ten rekord má hodnotu 1:53,28 a byl vytvořen v Mnichově.",
        "Je to česká běžkyně na 800 metrů.",
    )),
    ("Poznej sport.", "Jachting", ["plachtění"], (
        "Loď dokáže plout i proti větru — křižováním v úhlu kolem pětačtyřiceti stupňů.",
        "Nejslavnějším pohárem je Americký, nejstarší mezinárodní trofej ve sportu vůbec.",
        "Závodí se na plachetnicích a v Česku se trénuje hlavně na Lipně.",
    )),
]

BANK["jazyk"] += [
    ("Poznej jazyk.", "Angličtina", ["anglicky"], (
        "Slovní zásoba jí z velké části přišla z francouzštiny po roce 1066, proto má na maso a na zvíře jiná slova.",
        "Nemá skloňování, ale zato dvanáct slovesných časů a pravopis, který se rozešel s výslovností.",
        "Je to nejrozšířenější druhý jazyk světa a mluví se jí v Británii i v USA.",
    )),
    ("Poznej slovo podle původu.", "Vlak", [], (
        "Jungmann ho vzkřísil ze staročeského výrazu pro to, co se vleče, a přiřkl mu nový význam.",
        "Ve slovenštině se tomu říká stejně, v ruštině a polštině úplně jinak.",
        "Táhne ho lokomotiva a jezdí po kolejích.",
    )),
    ("Poznej jev.", "Spodoba znělosti", ["asimilace znělosti", "spodoba"], (
        "Uvnitř skupiny souhlásek rozhoduje ta poslední a ostatní se jí přizpůsobí — proto se říká „lékď“ místo „lékd“.",
        "Kvůli ní se „svatba“ vyslovuje se z a „nehet“ na konci s t.",
        "Je to důvod, proč se v češtině často píše něco jiného, než se říká.",
    )),
    ("Poznej termín.", "Pleonasmus", ["pleonasmy"], (
        "Odborně se liší od tautologie tím, že opakuje význam uvnitř jednoho výrazu, ne ve dvou větách.",
        "V úřední češtině se jich najde spousta — třeba „v současné době nyní“.",
        "Patří sem „bílý bělouš“ nebo „vrátit se zpátky“.",
    )),
    ("Poznej jazyk.", "Maďarština", ["maďarsky"], (
        "Nepatří k indoevropským jazykům a jejími nejbližšími příbuznými jsou jazyky za Uralem.",
        "Má osmnáct pádů a přízvuk vždy na první slabice, stejně jako čeština.",
        "Mluví se jí v zemi s hlavním městem Budapešť.",
    )),
    ("Poznej slovo podle původu.", "Nikotin", [], (
        "Jméno nese po francouzském vyslanci u portugalského dvora, který rostlinu poslal královně.",
        "Chemicky je to alkaloid a rostlina si ho vyrábí jako obranu proti hmyzu.",
        "Je v cigaretách a je návykový.",
    )),
    ("Poznej jev.", "Zdvořilostní plurál", ["vykání"], (
        "Vzniklo v pozdním Římě, kde se císař oslovoval množným číslem, protože vládl s kolegou.",
        "V češtině se pojí s množným tvarem slovesa, ale jednotným tvarem příčestí — „vy jste přišel“.",
        "Je to způsob, jak se oslovuje někdo, komu se netyká.",
    )),
    ("Poznej termín.", "Etymologie", [], (
        "Řecký základ slova znamená hledání pravého významu, protože antika věřila, že slovo v sobě nese podstatu věci.",
        "V češtině má vlastní slovník, který sestavil Václav Machek.",
        "Zabývá se tím, odkud slova pocházejí.",
    )),
    ("Poznej jazyk.", "Švédština", ["švédsky"], (
        "Reforma z roku 1967 v ní zrušila zdvořilostní oslovování a od té doby si tam tykají skoro všichni.",
        "Má melodický přízvuk, takže dvě stejně psaná slova znamenají něco jiného podle intonace.",
        "Mluví se jí v zemi s hlavním městem Stockholm.",
    )),
    ("Poznej slovo podle původu.", "Balkon", ["balkón"], (
        "Přes italštinu a francouzštinu sahá ke germánskému slovu pro trám.",
        "Je to vysunutá plošina bez podpěry zdola, na rozdíl od lodžie zapuštěné do stavby.",
        "Vyjde se na něj z bytu a suší se na něm prádlo.",
    )),
    ("Poznej termín.", "Hyperbola", ["nadsázka"], (
        "Sdílí jméno s kuželosečkou, protože obojí pochází z řeckého výrazu pro přehození přes míru.",
        "Používá se v reklamě i v běžné řeči a nemá se brát doslova.",
        "Patří sem „už tisíckrát jsem ti to říkal“.",
    )),
    ("Poznej jazyk.", "Řečtina", ["řecky"], (
        "Její abeceda dala jméno samotnému slovu abeceda podle prvních dvou písmen.",
        "Existuje nepřetržitě přes tři tisíce let, což je v Evropě rekord.",
        "Píše se jí písmeny jako alfa, beta a omega.",
    )),
    ("Poznej jev.", "Frazém", ["frazeologismus"], (
        "Jeho jednotlivá slova se nedají zaměnit ani za synonyma — „chytat lelky“ nejde říct jinak.",
        "Zkoumá ho zvláštní obor jazykovědy a jeho ustálenost se pozná právě podle toho, co v něm nejde změnit.",
        "Patří sem „mít za lubem“ nebo „chodit kolem horké kaše“.",
    )),
    ("Poznej slovo podle původu.", "Hurikán", [], (
        "Do evropských jazyků ho přinesli Španělé z jazyka karibských Taínů, kde označovalo boha bouře.",
        "V Tichém oceánu se témuž jevu říká tajfun, v Indickém cyklón.",
        "Je to tropická bouře a jednotlivé případy dostávají křestní jména.",
    )),
    ("Poznej jazyk.", "Latinka", ["latinské písmo"], (
        "Písmena J, U a W se v ní ustálila až ve středověku; antika je neznala.",
        "Vychází z etruského a řeckého písma a používá ji dnes většina světa.",
        "Je to písmo, kterým je napsaná tato věta.",
    )),
    ("Poznej termín.", "Argot", ["hantýrka"], (
        "Původně to byla mluva zlodějů, která měla utajit obsah před nezasvěcenými.",
        "Od profesní mluvy se odlišuje právě tou snahou nebýt srozumitelný pro okolí.",
        "Patří sem výrazy jako „bouchačka“ nebo „chlupatej“ pro policistu.",
    )),
    ("Poznej jev.", "Krátící pravidlo", ["krácení", "rytmický zákon"], (
        "Ve slovenštině se dvě dlouhé slabiky za sebou nesnesou, takže se ta druhá zkrátí.",
        "Proto je „krásny“, ne „krásný“, a „biely“, ale „peknému“.",
        "Čeština nic takového nemá a právě tím se od slovenštiny liší nejnápadněji.",
    )),
    ("Poznej slovo podle původu.", "Šálek", [], (
        "Přišlo z německého Schale, které původně znamenalo misku nebo skořápku.",
        "Ve staré češtině se pro nádobu na pití užívalo slovo číše nebo koflík.",
        "Pije se z něj čaj a má ouško.",
    )),
    ("Poznej jazyk.", "Portugalština", ["portugalsky"], (
        "Má nosovky značené vlnovkou a v brazilské podobě se vyslovuje výrazně otevřeněji než v evropské.",
        "Je to nejrozšířenější jazyk na jižní polokouli.",
        "Mluví se jí v Brazílii a v zemi s hlavním městem Lisabon.",
    )),
    ("Poznej termín.", "Interpunkce", ["interpunkční znaménka"], (
        "Otazník i vykřičník vznikly ve středověku zkratkami latinských slov quaestio a io, psanými nad sebe.",
        "Čárku před spojkou „a“ čeština klade jen v některých případech, což bývá častá chyba.",
        "Patří sem tečka, čárka a středník.",
    )),
]

BANK["spolecnost"] += [
    ("Poznej pojem.", "Inkluzivní vzdělávání", ["inkluze"], (
        "V Česku ho zavedla novela školského zákona roku 2016 a přinesla pozici asistenta pedagoga.",
        "Opírá se o Úmluvu OSN o právech osob se zdravotním postižením.",
        "Znamená, že děti se speciálními potřebami chodí do běžné třídy.",
    )),
    ("Poznej instituci.", "Mezinárodní měnový fond", ["MMF", "IMF"], (
        "Vznikl roku 1944 na konferenci v Bretton Woods spolu se Světovou bankou.",
        "Půjčuje státům v potížích, ale podmiňuje to úspornými opatřeními, za což bývá kritizován.",
        "Sídlí ve Washingtonu a jeho zkratka má tři písmena.",
    )),
    ("Poznej pojem.", "Sekularizace", [], (
        "V Česku ji zásadně urychlily dvě vlny — josefínské reformy a pak komunistický režim.",
        "Neznamená nutně úbytek víry, ale ústup náboženství z veřejného rozhodování.",
        "Kvůli ní se u nás ke státní neutralitě řadí i to, že škola není konfesní.",
    )),
    ("Poznej tradici.", "Betlém", ["jesličky"], (
        "První živý postavil roku 1223 František z Assisi v italském Grecciu.",
        "V Třebechovicích pod Orebem je dřevěný, pohyblivý a je národní kulturní památkou.",
        "Staví se pod stromeček a jsou v něm Josef, Marie a jesle.",
    )),
    ("Poznej pojem.", "Whistleblowing", ["oznamovatel", "oznamování protiprávního jednání"], (
        "Evropská směrnice z roku 2019 nutí firmy nad padesát zaměstnanců zřídit vnitřní kanál pro hlášení.",
        "Chrání toho, kdo se ozve, před výpovědí nebo šikanou v práci.",
        "Je to upozornění na nepravost uvnitř vlastní organizace.",
    )),
    ("Poznej organizaci.", "Člověk v tísni", [], (
        "Vznikla roku 1992 při České televizi jako nadace na pomoc lidem ve válkách.",
        "Provozuje program Skutečná pomoc a vzdělávací projekt Jeden svět na školách.",
        "Pořádá filmový festival Jeden svět a pomáhá lidem v exekucích.",
    )),
    ("Poznej pojem.", "Kvorum", ["usnášeníschopnost"], (
        "Latinsky to znamená „z nichž“ a pochází ze středověké formulace jmenování soudců.",
        "Ve sněmovně jich stačí třetina, aby se vůbec smělo hlasovat.",
        "Je to nejmenší počet přítomných, aby bylo hlasování platné.",
    )),
    ("Poznej svátek.", "Mikuláš", ["svatý Mikuláš"], (
        "Historický biskup, ke kterému se váže, žil ve 4. století v Myře v dnešním Turecku.",
        "Z jeho jména vznikla přes nizozemštinu i postava Santa Clause.",
        "Chodí pátého prosince s andělem a čertem.",
    )),
    ("Poznej pojem.", "Progresivní zdanění", ["progresivní daň"], (
        "Opakem je rovná daň, kterou Česko zavedlo roku 2008 a po dvanácti letech se od ní zase odchýlilo.",
        "Zdůvodňuje se tím, že tisícikoruna znamená pro chudého víc než pro bohatého.",
        "Znamená, že kdo vydělá víc, platí vyšší procento.",
    )),
    ("Poznej instituci.", "Nejvyšší kontrolní úřad", ["NKÚ"], (
        "Jeho prezidenta jmenuje hlava státu na návrh sněmovny na devět let.",
        "Nemůže nikoho potrestat, jen zveřejnit zjištění a předat je orgánům činným v trestním řízení.",
        "Prověřuje, jak stát hospodaří s penězi daňových poplatníků.",
    )),
    ("Poznej pojem.", "Digitální propast", ["digital divide"], (
        "Netýká se jen připojení, ale i dovedností — mezi seniory a mladými je rozdíl větší než mezi regiony.",
        "Během covidu ji ukázalo distanční vyučování, kdy část dětí neměla počítač.",
        "Je to rozdíl mezi těmi, kdo mají přístup k technologiím, a těmi, kdo ne.",
    )),
    ("Poznej tradici.", "Máje", ["stavění máje", "máj"], (
        "Zvyk vychází z předkřesťanských oslav plodnosti a strom se musel hlídat, aby ho sousedi nepodřízli.",
        "Staví se na návsi a bývá u něj věneček a barevné stuhy.",
        "Postaví se poslední dubnovou noc a k tomu se pálí čarodějnice.",
    )),
    ("Poznej pojem.", "Prekarizace", ["prekérní práce"], (
        "Pojem zavedl sociolog Guy Standing pro vrstvu, kterou nazval prekariátem.",
        "Projevuje se řetězením smluv na dobu určitou a prací načerno na živnostenský list.",
        "Znamená nejistou práci bez jistoty příjmu a bez nároků.",
    )),
    ("Poznej instituci.", "Česká národní banka", ["ČNB"], (
        "Její hlavní úkol nestanovuje vláda, ale ústava, což jí dává nezávislost na politicích.",
        "Sedmičlenná rada v ní rozhoduje o úrokových sazbách a v letech 2013 až 2017 držela kurz koruny.",
        "Vydává mince i papírová platidla a hlídá inflaci.",
    )),
    ("Poznej pojem.", "Odpovědnost za škodu", ["náhrada škody"], (
        "Občanský zákoník od roku 2014 rozlišuje újmu majetkovou a nemajetkovou, tedy i tu na zdraví a na duši.",
        "Kdo ji způsobí, musí uvést věc do původního stavu, a když to nejde, zaplatit v penězích.",
        "Kvůli ní má člověk povinné ručení u auta.",
    )),
    ("Poznej pojem.", "Migrace", ["migrace obyvatel"], (
        "Rozlišuje se vnitřní a vnější a demografové ji měří saldem, tedy rozdílem příchozích a odchozích.",
        "Češi jich v moderních dějinách zažili několik velkých vln — po roce 1938, 1948 i 1968.",
        "Znamená stěhování lidí za prací nebo před válkou.",
    )),
    ("Poznej svátek.", "Svátek matek", ["Den matek"], (
        "V Československu ho prosadila Alice Masaryková a po roce 1948 ho nahradil Mezinárodní den žen.",
        "Slaví se druhou květnovou neděli a jeho symbolem je karafiát.",
        "Děti k němu kreslí přáníčka a nosí kytku mamince.",
    )),
    ("Poznej pojem.", "Veřejná zakázka", ["zadávání veřejných zakázek"], (
        "Zákon nutí u vyšších částek soutěžit i to, co by úřad koupil běžně v obchodě.",
        "Nejčastější výtkou bývá, že se dělí na menší části, aby se soutěži předešlo.",
        "Je to nákup, který za peníze daňových poplatníků dělá stát nebo obec.",
    )),
    ("Poznej organizaci.", "Světová obchodní organizace", ["WTO"], (
        "Nahradila roku 1995 dohodu GATT a její rozhodovací orgán je od roku 2019 ochromený.",
        "Rozhoduje spory mezi státy o cla a dotace a rozhodnutí přijímá konsensem.",
        "Sídlí v Ženevě a její zkratka má tři písmena.",
    )),
    ("Poznej pojem.", "Genocida", [], (
        "Slovo složil roku 1944 právník Raphael Lemkin z řeckého kmene pro rod a latinského pro vraždu.",
        "OSN ji vymezila úmluvou z roku 1948 a nepromlčuje se.",
        "Je to úmyslné vyhlazení národa nebo etnika.",
    )),
]
