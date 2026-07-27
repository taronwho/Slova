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
        "Má na svém území víc jezer než zbytek světa dohromady a nejsevernější osada leží 800 kilometrů od pólu.",
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
        "Měří přes 4 000 kilometrů na délku, ale v průměru jen 180 na šířku.",
        "Leží na západním pobřeží Jižní Ameriky a patří mu Velikonoční ostrov.",
        "Roku 2010 tu z hloubky přes 600 metrů vytáhli po dvou měsících 33 zavalených horníků.",
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
        "Sedadla se sem vešla podle mistrovské kapacity jako do největšího stánku v zemi a je jich devadesát tisíc.",
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
