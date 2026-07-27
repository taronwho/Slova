#!/usr/bin/env python3
"""
Banka otázek pro Otázku dne.

Formát jednoho záznamu:

    ("nadpis", "odpověď", ["alt", …], ("indicie 1", "indicie 2", "indicie 3"))

**Indicie jsou odstupňované a na pořadí záleží.** Je to jediné pravidlo, na
kterém celá hra stojí:

1. **Malá.** Pro člověka, který se v oboru pohybuje. Většině lidí neřekne nic,
   ale kdo to ví, uhodne z ní. Konkrétní datum, číslo, vedlejší souvislost.
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
        "Narodil se roku 1890 v Malých Svatoňovicích v podkrkonoší a vystudoval filozofii.",
        "Byl to český spisovatel a novinář, který zemřel na zápal plic těsně před Vánocemi 1938.",
        "Do světových jazyků se přes jeho hru R.U.R. dostalo slovo robot, které mu poradil jeho bratr.",
    )),
    ("Poznej známou osobnost.", "Nikola Tesla", ["Tesla"], (
        "Narodil se roku 1856 v chorvatském Smiljanu do rodiny pravoslavného kněze.",
        "Byl to srbsko-americký vynálezce, který prosazoval střídavý proud proti Edisonovu stejnosměrnému.",
        "Nese jeho jméno jednotka magnetické indukce i americká automobilka elektromobilů.",
    )),
    ("Poznej známou osobnost.", "Marie Curie", ["Marie Curie-Sklodowská", "Marie Skłodowska-Curie", "Curie"], (
        "Narodila se roku 1867 ve Varšavě a do Paříže odešla studovat proto, že doma ženy na univerzitu nesměly.",
        "Byla to fyzička a chemička, první žena, která přednášela na pařížské Sorbonně.",
        "Jako jediná získala Nobelovu cenu ve dvou různých vědních oborech; objevila polonium a radium.",
    )),
    ("Poznej známou osobnost.", "Antonín Dvořák", ["Dvořák"], (
        "Narodil se roku 1841 v Nelahozevsi jako syn řezníka a hostinského.",
        "Byl to český skladatel, který tři roky vedl konzervatoř v New Yorku.",
        "Jeho Symfonie č. 9 se jmenuje Z Nového světa.",
    )),
    ("Poznej známou osobnost.", "Alan Turing", ["Turing"], (
        "V roce 1952 byl odsouzen za tehdejší britský trestný čin a o dva roky později zemřel na otravu kyanidem.",
        "Byl to britský matematik, který za války v Bletchley Parku pomáhal luštit německou šifru Enigma.",
        "Nese jeho jméno test, kterým se zkouší, zda se stroj dokáže vydávat za člověka.",
    )),
    ("Poznej známou osobnost.", "Emil Zátopek", ["Zátopek"], (
        "Narodil se roku 1922 v Kopřivnici a k běhu se dostal až jako dělník v Baťově Zlíně.",
        "Byl to československý atlet, jehož ženou byla olympijská vítězka v hodu oštěpem.",
        "Na olympiádě v Helsinkách 1952 vyhrál pětku, desítku i maraton, který běžel poprvé v životě.",
    )),
    ("Poznej známou osobnost.", "Frida Kahlo", ["Kahlo"], (
        "Při nehodě autobusu v osmnácti letech utrpěla těžká zranění, kvůli kterým se celý život léčila.",
        "Byla to mexická malířka, manželka mnohem staršího muralisty Diega Rivery.",
        "Proslula autoportréty se srostlým obočím; roku 2002 ji ve filmu zahrála Salma Hayek.",
    )),
    ("Poznej známou osobnost.", "Ludwig van Beethoven", ["Beethoven"], (
        "Narodil se roku 1770 v Bonnu a jeho děd pocházel z vlámského rodu, odkud má předložku ve jméně.",
        "Byl to německý skladatel, který postupně ohluchl, ale komponoval dál.",
        "Jeho Devátá symfonie končí Ódou na radost, dnešní hymnou Evropské unie.",
    )),
    ("Poznej známou osobnost.", "Édith Piaf", ["Piaf"], (
        "Její životní láska, boxer Marcel Cerdan, zahynul roku 1949 při letecké nehodě.",
        "Byla to francouzská zpěvačka, která zemřela ve stejný den jako její krajan Jean Cocteau.",
        "Proslavila se pod pseudonymem, který v překladu do češtiny znamená „vrabčák“, a písní Non, je ne regrette rien.",
    )),
    ("Poznej známou osobnost.", "Jan Amos Komenský", ["Komenský", "Comenius"], (
        "Po bitvě na Bílé hoře odešel do exilu a zbytek života strávil v Lešně a v Amsterodamu.",
        "Byl to poslední biskup Jednoty bratrské a nazývá se učitelem národů.",
        "Napsal Labyrint světa a ráj srdce a obrázkovou učebnici Orbis pictus.",
    )),
    ("Poznej známou osobnost.", "Leonardo da Vinci", ["Leonardo", "da Vinci"], (
        "Poslední léta strávil ve Francii na zámku Clos Lucé, kam ho pozval král František I.",
        "Byl to italský renesanční malíř a vynálezce, který psal poznámky zrcadlově obráceně.",
        "Namaloval Poslední večeři a Monu Lisu.",
    )),
    ("Poznej známou osobnost.", "Winston Churchill", ["Churchill"], (
        "V roce 1953 dostal Nobelovu cenu — ale za literaturu, ne za mír.",
        "Byl to britský premiér, který se v roce 1945 sešel se Stalinem a Rooseveltem na Jaltě.",
        "Proslul projevem o krvi, dřině, slzách a potu a symbolem vítězství ze dvou prstů.",
    )),
    ("Poznej známou osobnost.", "Vincent van Gogh", ["van Gogh"], (
        "Za života prodal podle většiny badatelů jediný obraz a živil ho jeho bratr Theo.",
        "Byl to nizozemský malíř, který si v Arles po hádce s Gauguinem uřízl kus ucha.",
        "Namaloval Slunečnice a Hvězdnou noc.",
    )),
    ("Poznej známou osobnost.", "Božena Němcová", ["Němcová"], (
        "Zemřela roku 1862 v bídě, ve dvaačtyřiceti letech, a její původ je dodnes předmětem dohadů.",
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
        "Zemřel roku 1791 ve Vídni ve věku pětatřiceti let a byl pohřben do společného hrobu.",
        "Byl to rakouský skladatel, který jako dítě koncertoval po evropských dvorech.",
        "V Praze měla premiéru jeho opera Don Giovanni a jeho život zfilmoval Miloš Forman ve snímku s osmi Oscary.",
    )),
    ("Poznej známou osobnost.", "Jan Železný", ["Železný"], (
        "Narodil se roku 1966 v Mladé Boleslavi a jeho otec i matka byli také oštěpaři.",
        "Je to český atlet, trojnásobný olympijský vítěz z let 1992, 1996 a 2000.",
        "Drží dosud světový rekord v hodu oštěpem — 98,48 metru z roku 1996.",
    )),
    ("Poznej známou osobnost.", "Nelson Mandela", ["Mandela"], (
        "Strávil osmnáct z celkových sedmadvaceti let vězení na ostrově Robben Island.",
        "Byl to jihoafrický politik, který dostal roku 1993 Nobelovu cenu míru.",
        "Stal se prvním černošským prezidentem Jihoafrické republiky po pádu apartheidu.",
    )),
    ("Poznej známou osobnost.", "Galileo Galilei", ["Galileo", "Galilei"], (
        "Poslední léta strávil v domácím vězení ve vile v Arcetri u Florencie a oslepl.",
        "Byl to italský astronom, kterého inkvizice donutila odvolat učení o pohybu Země.",
        "Dalekohledem objevil čtyři největší měsíce Jupiteru, které se po něm dodnes jmenují.",
    )),
    ("Poznej známou osobnost.", "Agatha Christie", ["Christie"], (
        "V prosinci 1926 na jedenáct dní beze stopy zmizela a nikdy to nevysvětlila.",
        "Byla to britská spisovatelka detektivek, nejprodávanější autorka všech dob.",
        "Vymyslela belgického detektiva Hercula Poirota a slečnu Marplovou.",
    )),
    ("Poznej známou osobnost.", "Tomáš Garrigue Masaryk", ["Masaryk", "T. G. Masaryk", "TGM"], (
        "Prostřední jméno přijal po své americké manželce Charlotte.",
        "Byl to filozof a politik, který se v Rukopisném sporu postavil na stranu odpůrců pravosti.",
        "Stal se prvním československým prezidentem a říkalo se mu tatíček.",
    )),
    ("Poznej známou osobnost.", "Charlie Chaplin", ["Chaplin"], (
        "V roce 1952 mu USA v době mccarthismu odmítly obnovit povolení k návratu a usadil se ve Švýcarsku.",
        "Byl to britský komik němého filmu, spoluzakladatel studia United Artists.",
        "Proslavil se postavou tuláka v buřince s hůlčičkou a knírkem.",
    )),
    ("Poznej známou osobnost.", "Jan Hus", ["Hus"], (
        "Poslední měsíce před koncilem strávil na Kozím hrádku a na hradě Krakovci.",
        "Byl to český kazatel, který kázal v pražské Betlémské kapli.",
        "Roku 1415 byl v Kostnici upálen; výročí jeho smrti je český státní svátek.",
    )),
    ("Poznej známou osobnost.", "Věra Čáslavská", ["Čáslavská"], (
        "V Mexiku roku 1968 při hymně sklonila hlavu a odvrátila ji na protest proti okupaci Československa.",
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
        "Pramení v Schwarzwaldu a ústí do moře rozsáhlou deltou, která je na seznamu UNESCO.",
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
        "Jeho parlament Alþingi bývá označován za nejstarší dosud fungující na světě.",
        "Leží na rozhraní dvou litosférických desek, takže se každý rok o pár centimetrů rozšiřuje.",
        "Jeho hlavním městem je Reykjavík a v roce 2010 tu sopka Eyjafjallajökull zastavila leteckou dopravu v Evropě.",
    )),
    ("Poznej horu.", "Mount Everest", ["Everest", "Sagarmatha", "Čomolungma"], (
        "Jeho výška se od prvního měření roku 1856 několikrát opravovala, naposledy roku 2020 na dnešní hodnotu.",
        "Leží na hranici Nepálu a Číny a jeho evropské jméno nese britského geodeta.",
        "Je nejvyšší horou světa, měří 8 849 metrů.",
    )),
    ("Poznej moře.", "Mrtvé moře", [], (
        "Jeho hladina leží víc než 400 metrů pod úrovní světového oceánu — je to nejníže položená souš na Zemi.",
        "Leží mezi Izraelem a Jordánskem a ústí do něj řeka Jordán.",
        "Kvůli extrémní slanosti v něm člověk plave, i když se o to nesnaží, a nežijí v něm ryby.",
    )),
    ("Poznej české město.", "Kutná Hora", [], (
        "Ve 14. století se tu razil pražský groš a město bylo po Praze druhé nejbohatší v zemi.",
        "Leží ve Středočeském kraji a její historické jádro je od roku 1995 na seznamu UNESCO.",
        "Stojí tu chrám svaté Barbory a nedaleká kostnice v Sedlci vyzdobená lidskými kostmi.",
    )),
    ("Poznej stát.", "Kanada", [], (
        "Má nejdelší pobřeží ze všech států světa a její jméno pochází z irokézského slova pro vesnici.",
        "Je to druhý největší stát světa a má dva úřední jazyky.",
        "Na její vlajce je javorový list a jejím hlavním městem je Ottawa.",
    )),
    ("Poznej poušť.", "Sahara", [], (
        "Její jméno je v arabštině prostě „pouště“ — množné číslo od slova pro poušť.",
        "Rozkládá se přes deset afrických států a na jihu ji lemuje pás Sahel.",
        "Je největší horkou pouští světa, zhruba tak velká jako Spojené státy.",
    )),
    ("Poznej hlavní město.", "Brasília", ["Brasilia"], (
        "Postavilo se od nuly na prázdné náhorní plošině a otevřelo se roku 1960.",
        "Jeho hlavní architekt Oscar Niemeyer je z téže země, jejíž největší město je São Paulo.",
        "Půdorys má připomínat letadlo nebo motýla a je celé na seznamu UNESCO.",
    )),
    ("Poznej jezero.", "Bajkal", ["Bajkalské jezero"], (
        "Je staré zhruba 25 milionů let a žije v něm jediný sladkovodní tuleň na světě.",
        "Leží na jihu Sibiře a napájí ho víc než tři sta řek, ale odtéká z něj jediná — Angara.",
        "Je nejhlubší jezero světa a je v něm asi pětina veškeré sladké povrchové vody planety.",
    )),
    ("Poznej stát.", "Nepál", [], (
        "Jako jediný stát na světě nemá obdélníkovou vlajku — tvoří ji dva nad sebou položené trojúhelníky.",
        "Leží mezi Indií a Čínou a jeho hlavním městem je Káthmándú.",
        "Leží na jeho území osm z deseti nejvyšších hor světa.",
    )),
    ("Poznej průplav.", "Panamský průplav", ["Panama"], (
        "Práce na něm nejdřív začali Francouzi pod vedením stavitele Suezského průplavu a zkrachovali.",
        "Otevřel se roku 1914 a spojuje dva oceány přes nejužší místo pevniny.",
        "Lodě v něm zdvihá soustava zdymadel a jmenuje se po středoamerickém státě, kterým vede.",
    )),
    ("Poznej vodopád.", "Niagarské vodopády", ["Niagara"], (
        "Tvoří je tři samostatné vodopády a mezi dvěma z nich leží Kozí ostrov.",
        "Leží na hranici USA a Kanady mezi jezery Erie a Ontario.",
        "Nejznámější z nich se pro svůj tvar jmenuje Podkova a k jeho úpatí vozí turisty loď Panna mlhy.",
    )),
    ("Poznej stát.", "Švýcarsko", [], (
        "Jeho mezinárodní zkratka CH pochází z latinského Confoederatio Helvetica.",
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
        "Místo hrubého domácího produktu sleduje ukazatel zvaný hrubé národní štěstí.",
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
        "Stojí na více než stovce ostrůvků a domy se opírají o dřevěné piloty zaražené do bahna.",
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
        "Alchymisté ji získávali pálením zelené skalice a říkali jí olej vitriolový.",
        "Je to bezbarvá olejovitá kapalina, která silně pohlcuje vodu a přitom se zahřívá.",
        "Její vzorec je H₂SO₄ a je náplní olověných autobaterií.",
    )),
    ("Poznej chemický prvek.", "Rtuť", ["Hg"], (
        "Jeho značka pochází z latinského hydrargyrum, tedy „vodní stříbro“.",
        "Je to jediný kov, který je za pokojové teploty kapalný.",
        "Býval v teploměrech a nese jméno stejné jako planeta nejblíž Slunci.",
    )),
    ("Poznej chemický prvek.", "Helium", ["He"], (
        "Objevili ho ve spektru sluneční koróny dřív, než ho našli na Zemi — proto to jméno.",
        "Je to druhý nejlehčí prvek a jediný, který nejde zmrazit za normálního tlaku.",
        "Plní se jím balonky a po nadechnutí zvýší hlas.",
    )),
    ("Poznej jednotku.", "Newton", ["N"], (
        "V základních jednotkách SI se vyjádří jako kilogram krát metr děleno sekundou na druhou.",
        "Měří se jí veličina, kterou popisují tři pohybové zákony.",
        "Jmenuje se po anglickém fyzikovi a měří sílu.",
    )),
    ("Poznej vědecký objev.", "DNA", ["deoxyribonukleová kyselina"], (
        "Klíčový rentgenový snímek číslo 51 pořídila roku 1952 Rosalind Franklinová.",
        "Její strukturu popsali roku 1953 James Watson a Francis Crick.",
        "Má tvar dvoušroubovice a nese genetickou informaci.",
    )),
    ("Poznej planetu.", "Venuše", [], (
        "Otáčí se kolem osy opačným směrem než většina planet a jeden její den trvá déle než rok.",
        "Je Zemi nejbližší planetou a hustá atmosféra oxidu uhličitého na ní drží přes 460 °C.",
        "Ze Země je nejjasnějším objektem po Slunci a Měsíci; říká se jí Jitřenka nebo Večernice.",
    )),
    ("Poznej meteorologický jev.", "Tornádo", [], (
        "Jeho sílu klasifikuje Fujitova stupnice, dnes v takzvané rozšířené podobě.",
        "Místem jeho zvýšeného výskytu je středozápad Spojených států.",
        "Má ho jako součást uměleckého pseudonymu zpěvačka ve filmu Limonádový Joe.",
    )),
    ("Poznej teplotní stupnici.", "Fahrenheitova stupnice", ["Fahrenheit"], (
        "Bod varu vody na ní leží na 212 stupních a mrazu na 32.",
        "Pojmenována je podle německého fyzika, který zdokonalil rtuťový teploměr.",
        "Dodnes se používá ve Spojených státech a v pár závislých územích.",
    )),
    ("Poznej vědeckou teorii.", "Teorie relativity", ["relativita", "speciální teorie relativity"], (
        "Její obecnou verzi potvrdilo roku 1919 pozorování zatmění Slunce, které vedl Arthur Eddington.",
        "Vychází z ní, že čas plyne pomaleji, čím rychleji se pozorovatel pohybuje.",
        "Autorem je Albert Einstein a nejznámější vzorec z ní je E = mc².",
    )),
    ("Poznej lidský orgán.", "Játra", [], (
        "Jsou jediným lidským orgánem, který dokáže dorůst i ze čtvrtiny své hmoty.",
        "Váží zhruba půldruhého kilogramu a produkují žluč.",
        "Poškozuje je alkohol a jejich onemocnění se jmenuje cirhóza.",
    )),
    ("Poznej vesmírné těleso.", "Halleyova kometa", ["Halley"], (
        "Její návraty zpětně dopočítal astronom, který ji pak sám nikdy nespatřil — zemřel před dalším návratem.",
        "Vrací se zhruba jednou za 76 let, naposledy roku 1986.",
        "Zachycuje ji tapiserie z Bayeux jako znamení před bitvou u Hastingsu roku 1066.",
    )),
    ("Poznej chemický prvek.", "Uhlík", ["C"], (
        "Podle jeho izotopu s hmotnostním číslem 14 se datují archeologické nálezy.",
        "Tvoří základ všech organických sloučenin a v přírodě se vyskytuje ve dvou velmi odlišných podobách.",
        "Jednou z nich je grafit v tužce, druhou diamant.",
    )),
    ("Poznej vědce.", "Gregor Johann Mendel", ["Mendel"], (
        "Většinu pokusů dělal na zahradě augustiniánského kláštera v Brně.",
        "Byl to opat, který svá zjištění zveřejnil roku 1866 a za života nezískal uznání.",
        "Zakladatel genetiky; jeho pravidla se učí jako zákony dědičnosti a pracoval s hrachem.",
    )),
    ("Poznej jev.", "Polární záře", ["aurora"], (
        "Vzniká, když nabité částice slunečního větru narazí na atomy v horních vrstvách atmosféry.",
        "Zelenou barvu jí dává kyslík, načervenalou a fialovou dusík.",
        "Nejlépe je vidět v pásu kolem magnetického pólu — třeba na Islandu nebo v severním Norsku.",
    )),
    ("Poznej léčivo.", "Penicilin", [], (
        "Objevil se roku 1928 náhodou na kontaminované Petriho misce, kterou nechal někdo ležet přes dovolenou.",
        "Za jeho objev a výrobu dostali roku 1945 tři vědci Nobelovu cenu.",
        "Byl to první antibiotikum a jeho objevitelem je Alexander Fleming.",
    )),
    ("Poznej chemickou sloučeninu.", "Amoniak", ["NH3", "čpavek"], (
        "Vyrábí se Haberovým–Boschovým postupem přímo z prvků za vysokého tlaku.",
        "Jeho vodný roztok je zásaditý a slouží jako základ pro dusíkatá hnojiva.",
        "Má vzorec NH₃ a je cítit štiplavě, jako čisticí prostředky nebo zvířecí močůvka.",
    )),
    ("Poznej hvězdu.", "Sirius", ["Sírius"], (
        "Je to ve skutečnosti dvojhvězda; její slabší složkou je bílý trpaslík zvaný Štěně.",
        "Leží v souhvězdí Velkého psa, asi 8,6 světelného roku od nás.",
        "Je to nejjasnější hvězda noční oblohy.",
    )),
    ("Poznej stupnici.", "Richterova stupnice", ["Richter"], (
        "Je logaritmická — každý stupeň znamená zhruba dvaatřicetkrát víc uvolněné energie.",
        "Zavedl ji roku 1935 americký seismolog a dnes ji odborníci nahradili momentovým měřítkem.",
        "Měří se jí síla zemětřesení.",
    )),
    ("Poznej živočicha.", "Ptakopysk", ["ptakopysk podivný"], (
        "Samci mají na zadních nohou ostruhu s jedem a živočich loví se zavřenýma očima podle elektrických signálů.",
        "Žije ve východní Austrálii a na Tasmánii a je to savec, který klade vejce.",
        "Má zobák jako kachna, ocas jako bobr a plovací blány.",
    )),
    ("Poznej chemický prvek.", "Zlato", ["Au"], (
        "Jeho značka pochází z latinského aurum a čistota se udává v karátech.",
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
        "Byla vyvinuta v roce 1972 jako cvičení pro nového zaměstnance.",
        "Byla to první hra vyvinutá společností Atari.",
        "Figurují v ní dvě plošinky, které se snaží odrážet míč pohybující se mezi nimi.",
    )),
    ("Poznej hudební skupinu.", "Pink Floyd", [], (
        "Jméno vzniklo spojením křestních jmen dvou amerických bluesmanů z desek, které měl doma zakládající člen.",
        "Jejich prvního frontmana museli nahradit poté, co se psychicky zhroutil.",
        "Album The Dark Side of the Moon má na obalu hranol rozkládající světlo.",
    )),
    ("Poznej obraz.", "Křik", ["Výkřik", "The Scream"], (
        "Autor si k němu do deníku poznamenal, že šel po cestě, když nebe zrudlo a přírodou prošel nekonečný jekot.",
        "Namaloval ho Nor Edvard Munch a existuje ve čtyřech verzích.",
        "Je na něm postava, která si drží hlavu a otevírá ústa na můstku pod krvavým nebem.",
    )),
    ("Poznej film.", "Vetřelec", ["Alien"], (
        "Návrh titulního tvora vychází z obrazu Necronom IV švýcarského výtvarníka H. R. Gigera.",
        "Režíroval ho Ridley Scott a hlavní hrdinku Ripleyovou hraje Sigourney Weaverová.",
        "Slogan zněl „ve vesmíru vás nikdo neslyší křičet“ a nejslavnější scéna se odehraje u jídelního stolu.",
    )),
    ("Poznej českou pohádku.", "Tři oříšky pro Popelku", ["Tři oříšky pro Popelku (film)"], (
        "Natáčelo se roku 1973 na zámku Moritzburg a na Švihově; v Německu ji vysílají každé Vánoce.",
        "Hlavní roli hraje Libuše Šafránková, prince Pavel Trávníček.",
        "Hrdinka dostane od holoubků kouzelné dárky, na plese ztratí střevíček a umí střílet z kuše.",
    )),
    ("Poznej muzikál.", "Kočky", ["Cats"], (
        "Libreto vychází ze sbírky básniček T. S. Eliota o praktických kocourech.",
        "Napsal ho Andrew Lloyd Webber a nejznámější píseň se jmenuje Memory.",
        "Herci v něm celý večer vystupují v kostýmech koček.",
    )),
    ("Poznej spisovatele.", "Franz Kafka", ["Kafka"], (
        "Pracoval jako úředník Dělnické úrazové pojišťovny a psal po nocích.",
        "Byl to pražský německy píšící autor, který svému příteli odkázal spálit rukopisy — a ten to neudělal.",
        "Napsal Proces, Zámek a Proměnu, v níž se hrdina probudí jako hmyz.",
    )),
    ("Poznej stavbu.", "Eiffelova věž", ["Eiffelovka"], (
        "Postavila se jako dočasná dominanta světové výstavy roku 1889 a měla se po dvaceti letech zbourat.",
        "Zachránilo ji, že se hodila jako anténa pro radiotelegrafii.",
        "Měří přes tři sta metrů a stojí v Paříži.",
    )),
    ("Poznej film.", "Kmotr", ["The Godfather"], (
        "Studio nechtělo obsadit hlavního herce ani režiséra; oba si prosadili až po dlouhých sporech.",
        "Natočil ho roku 1972 Francis Ford Coppola podle románu Maria Puza.",
        "Marlon Brando v něm hraje dona Vita Corleoneho a padne tu věta o nabídce, která se nedá odmítnout.",
    )),
    ("Poznej hudební album.", "Abbey Road", [], (
        "Nahrávalo se v létě 1969 a bylo poslední, na kterém všichni čtyři členové pracovali společně.",
        "Druhou stranu tvoří skoro souvislá směs kratších skladeb.",
        "Na obalu přechází čtveřice po přechodu pro chodce před londýnským studiem.",
    )),
    ("Poznej českého malíře.", "Alfons Mucha", ["Mucha"], (
        "Prorazil v Paříži plakátem pro Sarah Bernhardtovou, který nakreslil přes noc na Štědrý den.",
        "Je nejznámějším představitelem secese a v Paříži navrhoval plakáty, šperky i výstavní pavilon Bosny.",
        "Dvacet let maloval cyklus dvaceti velkoformátových pláten Slovanská epopej.",
    )),
    ("Poznej divadelní hru.", "Hamlet", [], (
        "Předloha vychází ze severské látky o princi Amlethovi zapsané dánským kronikářem Saxem Grammatikem.",
        "Napsal ji Shakespeare a odehrává se na hradě Elsinor.",
        "Zaznívá v ní věta „Být, či nebýt“ a hlavní hrdina drží lebku šaška Yoricka.",
    )),
    ("Poznej seriál.", "Přátelé", ["Friends"], (
        "Šest hlavních herců si na konci vyjednávalo plat společně, takže brali všichni stejně.",
        "Vysílal se v letech 1994 až 2004 a odehrává se hlavně v newyorské kavárně Central Perk.",
        "Znělku Iʼll Be There for You zpívají The Rembrandts.",
    )),
    ("Poznej sochu.", "David", ["Davidova socha"], (
        "Vytesal ji z jediného bloku carrarského mramoru, který před ním dva jiní sochaři vzdali.",
        "Vznikla v letech 1501 až 1504 ve Florencii a dnes stojí v Galerii dell'Accademia.",
        "Autorem je Michelangelo a socha zobrazuje biblického mladíka s prakem.",
    )),
    ("Poznej film.", "Pelíšky", [], (
        "Odehrává se v letech 1967 a 1968 a scénář vychází z povídek Petra Šabacha.",
        "Režíroval ho Jan Hřebejk; hrají Miroslav Donutil a Jiří Kodet jako sousedi z protilehlých bytů.",
        "Zůstala z něj hláška o lžičkách, které se ve východoněmeckém plastu rozpustí v čaji.",
    )),
    ("Poznej knihu.", "Malý princ", ["Le Petit Prince"], (
        "Autor byl pilot, který se roku 1944 ztratil při průzkumném letu nad Středozemním mořem.",
        "Vypravěč potká hrdinu po havárii na Sahaře; hrdina pochází z planetky B 612.",
        "Napsal ji Antoine de Saint-Exupéry a je v ní liška, která učí, že správně vidíme jen srdcem.",
    )),
    ("Poznej hudební nástroj.", "Theremin", ["theremin"], (
        "Vznikl roku 1920 v sovětském Rusku při pokusech s měřením hustoty plynů.",
        "Ovládá se dvěma anténami, které snímají polohu rukou.",
        "Je to jediný nástroj, na který se hraje, aniž by se ho člověk dotkl.",
    )),
    ("Poznej českou kapelu.", "Olympic", [], (
        "Vznikla roku 1962 a původně doprovázela zpěváky v divadle Semafor.",
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
        "Trvala zhruba dvě hodiny a odehrála se 8. listopadu 1620.",
        "Po ní následovala poprava sedmadvaceti českých pánů na Staroměstském náměstí.",
        "Znamenala porážku českých stavů a začátek doby, které se říká temno.",
    )),
    ("Poznej událost.", "Sametová revoluce", ["sametová revoluce v Československu"], (
        "Rozběhla se po zásahu proti studentskému průvodu na Národní třídě 17. listopadu 1989.",
        "Vzniklo při ní Občanské fórum a lidé na náměstích cinkali klíči.",
        "Skončila pádem komunistického režimu a prezidentem se stal Václav Havel.",
    )),
    ("Poznej stavbu.", "Berlínská zeď", ["berlínská zeď"], (
        "Postavila se během jediné noci ze 12. na 13. srpna 1961.",
        "Nejznámější přechod mezi jejími stranami se jmenoval Checkpoint Charlie.",
        "Padla 9. listopadu 1989 a rozdělovala hlavní město Německa.",
    )),
    ("Poznej panovníka.", "Karel IV.", ["Karel Čtvrtý"], (
        "Vlastním jménem se jmenoval Václav a jméno si změnil při biřmování ve Francii.",
        "Byl to český král a římský císař, který vydal roku 1356 Zlatou bulu.",
        "Založil pražskou univerzitu, Nové Město pražské a hrad Karlštejn.",
    )),
    ("Poznej lodní katastrofu.", "Titanic", [], (
        "Loď měla dvacet záchranných člunů, tedy méně, než bylo lidí na palubě, ale víc, než tehdy vyžadoval předpis.",
        "Potopila se v noci na 15. dubna 1912 na cestě ze Southamptonu do New Yorku.",
        "O katastrofě natočil roku 1997 James Cameron film s Leonardem DiCapriem.",
    )),
    ("Poznej událost.", "Pád Cařihradu", ["dobytí Konstantinopole", "pád Konstantinopole"], (
        "Rozhodly o něm mimo jiné obří děla odlitá uherským puškařem Urbanem.",
        "Stalo se to 29. května 1453 a znamenalo konec Byzantské říše.",
        "Město poté přejmenovali a dnes se jmenuje Istanbul.",
    )),
    ("Poznej období.", "Zlatá horečka", ["kalifornská zlatá horečka"], (
        "Začala v lednu 1848 nálezem v pile Johna Suttera u řeky American River.",
        "Za rok se do oblasti sjelo přes tři sta tisíc lidí, kterým se říkalo devětačtyřicátníci.",
        "Odehrála se v Kalifornii a připomíná ji přezdívka fotbalového týmu San Francisco 49ers.",
    )),
    ("Poznej vládce.", "Napoleon Bonaparte", ["Napoleon"], (
        "Zemřel roku 1821 na ostrově Svaté Heleny a příčina jeho smrti je dodnes sporná.",
        "Byl to francouzský císař, který roku 1805 zvítězil u Slavkova na Moravě.",
        "Jeho tažení skončilo porážkou u Waterloo a nechal sestavit občanský zákoník, který nese jeho jméno.",
    )),
    ("Poznej událost.", "Mnichovská dohoda", ["Mnichov"], (
        "Podepsali ji v noci na 30. září 1938 zástupci čtyř velmocí bez účasti dotčeného státu.",
        "Britský premiér Neville Chamberlain po ní mluvil o míru pro naši dobu.",
        "Československo po ní přišlo o pohraničí a v Česku se jí říká zrada.",
    )),
    ("Poznej vynález.", "Knihtisk", [], (
        "Rozhodující nebyl lis, ale odlévání jednotlivých písmen ze slitiny olova, cínu a antimonu.",
        "Zavedl ho kolem roku 1450 v Mohuči Johannes Gutenberg.",
        "První velkou tištěnou knihou byla dvaačtyřicetiřádková bible.",
    )),
    ("Poznej událost.", "Přistání na Měsíci", ["Apollo 11", "první přistání na Měsíci"], (
        "Palubní počítač během sestupu opakovaně hlásil chybu 1202, protože byl přetížený.",
        "Stalo se to 20. července 1969 a modul se jmenoval Eagle.",
        "Neil Armstrong u toho pronesl větu o malém kroku pro člověka.",
    )),
    ("Poznej civilizaci.", "Mayové", ["mayská civilizace"], (
        "Jako jediní v předkolumbovské Americe měli plně rozvinuté písmo a znali pojem nuly.",
        "Žili na území dnešního Mexika, Guatemaly a Belize; jejich města jsou Tikal nebo Chichén Itzá.",
        "Roku 2012 se hodně mluvilo o konci jejich kalendáře jako o konci světa.",
    )),
    ("Poznej dokument.", "Magna charta", ["Magna Charta Libertatum", "Velká listina svobod"], (
        "Panovník ji podepsal roku 1215 na louce Runnymede pod nátlakem vzbouřených baronů.",
        "Papež ji o pár měsíců později prohlásil za neplatnou, ale znovu se potvrzovala po celé století.",
        "Je to anglická listina, kterou dodnes citují jako první krok k omezení moci panovníka.",
    )),
    ("Poznej válku.", "Stoletá válka", [], (
        "Trvala ve skutečnosti 116 let, s dlouhými přestávkami, a rozhodly ji nakonec děla.",
        "Vedly ji Anglie a Francie o nástupnictví na francouzský trůn.",
        "Objevila se v ní Jana z Arku a Angličané v ní zvítězili u Kresčaku a Azincourtu.",
    )),
    ("Poznej osobnost.", "Kryštof Kolumbus", ["Kolumbus", "Columbus"], (
        "Přepočítal si obvod Země zhruba o čtvrtinu menší, než ve skutečnosti je — jinak by se na cestu nevydal.",
        "Vyplul roku 1492 se třemi loděmi, z nichž největší se jmenovala Santa María.",
        "Do smrti věřil, že doplul do Indie; podle toho se dodnes říká původním obyvatelům Ameriky.",
    )),
    ("Poznej období.", "Pražské jaro", [], (
        "Program se opíral o takzvaný akční program KSČ z dubna 1968.",
        "V čele stál Alexander Dubček a mluvilo se o socialismu s lidskou tváří.",
        "Skončilo v noci na 21. srpna 1968 vpádem vojsk Varšavské smlouvy.",
    )),
    ("Poznej mořeplavce.", "Fernão de Magalhães", ["Magalhães", "Magellan"], (
        "Sám cestu nedokončil — zahynul roku 1521 při šarvátce na filipínském ostrově Mactan.",
        "Byl to Portugalec ve španělských službách; z pěti lodí se vrátila jediná, Victoria.",
        "Jeho výprava jako první obeplula svět a nese jeho jméno průliv u jižního cípu Ameriky.",
    )),
    ("Poznej stavbu.", "Velká čínská zeď", ["čínská zeď"], (
        "Není to jedna souvislá stavba, ale soustava opevnění z různých staletí; dnešní podoba je hlavně z doby dynastie Ming.",
        "Měří i s odbočkami přes 21 000 kilometrů.",
        "Rozšířená pověra tvrdí, že je vidět z vesmíru pouhým okem — není.",
    )),
]

# --------------------------------------------------------------------------
# Příroda
# --------------------------------------------------------------------------
BANK["priroda"] = [
    ("Poznej zvíře.", "Chameleon", ["chameleoni"], (
        "Každé oko mu funguje samostatně, takže vidí naráz dvěma směry.",
        "Barvu nemění hlavně kvůli maskování, ale kvůli náladě a teplotě.",
        "Loví dlouhým vystřelovacím jazykem a většina druhů žije na Madagaskaru.",
    )),
    ("Poznej strom.", "Sekvojovec obrovský", ["sekvojovec", "sekvoje"], (
        "Šišky mu otevírá teprve žár lesního požáru, takže bez ohně se špatně množí.",
        "Roste jen na západních svazích pohoří Sierra Nevada v Kalifornii.",
        "Největší žijící exemplář se jmenuje General Sherman a je to objemově největší strom světa.",
    )),
    ("Poznej ptáka.", "Kolibřík", ["kolibříci"], (
        "Srdce mu při letu bije až 1 200krát za minutu a v noci upadá do strnulosti, aby ušetřil energii.",
        "Žije jen v Americe a je jediným ptákem, který umí letět pozadu.",
        "Je to nejmenší pták světa a křídly kmitá tak rychle, že vydávají bzučivý zvuk.",
    )),
    ("Poznej rostlinu.", "Mucholapka podivná", ["mucholapka", "Dionaea muscipula"], (
        "Past sklapne teprve tehdy, když se hmyz během pár vteřin dotkne spouštěcího chloupku dvakrát.",
        "Roste v přírodě jen na malém území v Severní a Jižní Karolíně.",
        "Je to nejznámější masožravá rostlina a její list vypadá jako zubatá čelist.",
    )),
    ("Poznej živočicha.", "Medvídek koala", ["koala"], (
        "Otisky prstů má tak podobné lidským, že se pod mikroskopem těžko rozlišují.",
        "Prospí až dvacet hodin denně, protože jeho potrava má málo energie a je jedovatá pro většinu zvířat.",
        "Živí se listy blahovičníku a žije v Austrálii.",
    )),
    ("Poznej houbu.", "Muchomůrka zelená", ["muchomůrka"], (
        "Její jed amanitin nezničí ani var a příznaky otravy se objeví až po mnoha hodinách.",
        "Má bílé lupeny, prsten a na bázi třeně pochvu — nedá se splést s pravou žampionem, kdo se dívá.",
        "Je to nejjedovatější houba u nás a má na svědomí většinu smrtelných otrav houbami.",
    )),
    ("Poznej rybu.", "Žralok velrybí", ["žralok obrovský"], (
        "Vzor teček na jeho kůži je u každého jedince jiný a badatelé podle něj jednotlivé kusy rozeznávají.",
        "Živí se planktonem, který cedí z vody, a člověku nebezpečný není.",
        "Je to největší ryba světa; dorůstá přes dvanáct metrů.",
    )),
    ("Poznej hmyz.", "Včela medonosná", ["včela"], (
        "Polohu zdroje potravy si dělnice sdělují tancem ve tvaru osmičky.",
        "Královna klade až dva tisíce vajíček denně a žije několik let, dělnice v létě jen pár týdnů.",
        "Vyrábí med a stavějí šestiúhelníkové plástve.",
    )),
    ("Poznej savce.", "Vorvaň obrovský", ["vorvaň"], (
        "Má největší mozek ze všech živočichů, kteří kdy na Zemi žili.",
        "Potápí se za potravou přes kilometr hluboko a hledá ji echolokací.",
        "Je hlavní postavou románu Moby Dick a získávala se z něj ambra.",
    )),
    ("Poznej rostlinu.", "Bambus", [], (
        "Některé druhy vyrostou o víc než 90 centimetrů za jediný den.",
        "Je to ve skutečnosti tráva, ne strom, a některé druhy kvetou jednou za desítky let — všechny naráz.",
        "Živí se jím panda velká a v Asii se z něj staví lešení.",
    )),
    ("Poznej živočicha.", "Krtek obecný", ["krtek"], (
        "Jeho slina obsahuje látku, která ochromí žížalu, takže si ji může ukládat živou do zásoby.",
        "Denně sní potravu o hmotnosti blízké své vlastní a bez jídla vydrží jen pár hodin.",
        "Hrabe pod zemí chodby a vyhazuje hromádky; Zdeněk Miler o něm nakreslil večerníček.",
    )),
    ("Poznej strom.", "Ginkgo biloba", ["jinan dvoulaločný", "ginkgo", "jinan"], (
        "V Hirošimě přežilo několik jeho jedinců výbuch atomové bomby a rostou dodnes.",
        "Je to jediný žijící zástupce celé rostlinné třídy; říká se mu živoucí fosilie.",
        "Má listy ve tvaru vějíře s výřezem uprostřed a jeho výtažek se prodává na paměť.",
    )),
    ("Poznej zvíře.", "Mravenečník velký", ["mravenečník"], (
        "Nemá jediný zub a jazyk mu vyjede přes šedesát centimetrů, až sto padesátkrát za minutu.",
        "Žije ve Střední a Jižní Americe a chodí po hřbetech předních tlap, aby si nezničil drápy.",
        "Sní denně desetitisíce mravenců a termitů, které vybírá z rozhrabaných hnízd.",
    )),
    ("Poznej přírodní úkaz.", "Zatmění Slunce", ["úplné zatmění Slunce"], (
        "Je možné jen proto, že Měsíc je zhruba 400krát menší než hvězda za ním a zároveň 400krát blíž.",
        "Na jednom a témž místě na Zemi se v celé své podobě opakuje průměrně jednou za zhruba 375 let.",
        "Během něj se objeví koróna a na pár minut se zešeří jako v noci.",
    )),
    ("Poznej zvíře.", "Tučňák císařský", ["tučňák"], (
        "Samci celou antarktickou zimu drží jediné vejce na nohou pod kožním záhybem a nic nejedí.",
        "Je největším ze všech svých příbuzných a měří přes metr.",
        "Jeho hnízdění zachytil oceněný francouzský dokument z roku 2005; žije jen v Antarktidě.",
    )),
    ("Poznej rostlinu.", "Kopřiva dvoudomá", ["kopřiva"], (
        "Její žahavé chlupy jsou duté křemičité jehličky, které se ulomí a vstříknou obsah do kůže.",
        "Používá se v kuchyni na polévku a její vlákna se dřív spřádala na látku.",
        "Kdo se jí dotkne, dostane pupínky a pálí to; roste u plotů a na hnojišti.",
    )),
    ("Poznej živočicha.", "Chobotnice", ["chobotnice pobřežní", "chobotnice obecná"], (
        "Má tři srdce a modrou krev, protože kyslík v ní přenáší měď místo železa.",
        "Dvě třetiny jejích neuronů jsou v ramenech, ne v mozku, takže rameno „myslí“ samo.",
        "Má osm ramen s přísavkami a při útěku vypouští oblak inkoustu.",
    )),
    ("Poznej horninu.", "Vápenec", [], (
        "Tvoří ho hlavně minerál kalcit a po kápnutí kyseliny chlorovodíkové šumí.",
        "Rozpouští se v dešťové vodě, takže se v něm tvoří jeskyně a krasové útvary.",
        "Je z něj Český kras s Koněpruskými jeskyněmi a pálí se z něj vápno.",
    )),
    ("Poznej zvíře.", "Lenochod", ["lenochodi"], (
        "V jeho srsti roste zelená řasa a žijí v ní zavíječi, kteří jinde nežijí.",
        "Trávení jednoho listu mu trvá i měsíc a na záchod leze dolů zhruba jednou týdně.",
        "Visí hlavou dolů ze stromů ve Střední a Jižní Americe a pohybuje se velmi pomalu.",
    )),
    ("Poznej ptáka.", "Sova pálená", ["sova"], (
        "Uši má posazené nesymetricky, takže dokáže kořist zaměřit i ve tmě jen podle sluchu.",
        "Náběžná hrana jejích per je roztřepená, takže letí prakticky neslyšně.",
        "Má bílý srdcovitý obličej a hnízdí ve věžích a stodolách.",
    )),
]

# --------------------------------------------------------------------------
# Technika
# --------------------------------------------------------------------------
BANK["technika"] = [
    ("Který slavný konstruktér zbraní?", "John Browning", ["Browning"], (
        "Vynalezl automatickou pistoli se zásobníkem v rukojeti, ve svém oboru je držitelem 128 patentů.",
        "Zjevně nejznámější pistoli pojmenoval z jedno dílny je model Colt 1911 Government.",
        "Výrobek jeho konstrukce použil nechvalně proslulý Gavrilo Princip při útoku na Františka Ferdinanda d'Este.",
    )),
    ("Poznej vynález.", "Rentgen", ["rentgenové záření", "paprsky X"], (
        "Objevitel ho v roce 1895 nazval prostě neznámým — proto ta písmena v mezinárodním názvu.",
        "První snímek zachycoval ruku manželky objevitele s prstenem.",
        "Za jeho objev udělili roku 1901 vůbec první Nobelovu cenu za fyziku.",
    )),
    ("Poznej dopravní prostředek.", "Zeppelin", ["vzducholoď"], (
        "Nosnou konstrukci mu tvoří pevná kostra z duralu, což ho odlišuje od balonů.",
        "Hélium mu Spojené státy odmítly prodat, takže se plnil vodíkem.",
        "Éru jeho slávy ukončila roku 1937 katastrofa lodi Hindenburg v Lakehurstu.",
    )),
    ("Poznej vynález.", "Suchý zip", ["velcro"], (
        "Vynálezce dostal nápad, když si po procházce prohlížel pod mikroskopem, čím se mu na kalhoty chytily plody lopuchu.",
        "Švýcar George de Mestral si ho nechal patentovat roku 1955.",
        "Tvoří ho dva pásky — jeden s háčky, druhý se smyčkami — a při odtržení to zapraská.",
    )),
    ("Poznej auto.", "Volkswagen Brouk", ["Brouk", "VW Brouk", "Volkswagen Beetle"], (
        "Návrh vznikl ve třicátých letech pod vedením Ferdinanda Porscheho jako „vůz pro lid“.",
        "Motor má vzadu, chlazený vzduchem, a vyráběl se přes šedesát let prakticky beze změny tvaru.",
        "Ve filmu Herbie má číslo 53 a jeho lidová přezdívka odkazuje k hmyzu.",
    )),
    ("Poznej vynález.", "Mikrovlnná trouba", ["mikrovlnka"], (
        "Vynálezci Percymu Spencerovi se při pokusech s radarovým magnetronem roztekla v kapse čokoládová tyčinka.",
        "Ohřívá tak, že rozkmitá molekuly vody v potravině.",
        "První model z roku 1947 vážil přes 300 kilo a stál jako auto; dnes je skoro v každé kuchyni.",
    )),
    ("Poznej stroj.", "Parní stroj", [], (
        "Rozhodujícím zlepšením Jamese Watta byl oddělený kondenzátor, díky němuž se válec nemusel pořád ochlazovat.",
        "Jeho výkon se dodnes připomíná jednotkou, kterou Watt zavedl, aby ho porovnal s tažnými zvířaty.",
        "Poháněl první lokomotivy a rozjel průmyslovou revoluci.",
    )),
    ("Poznej techniku.", "GPS", ["Global Positioning System"], (
        "Aby soustava fungovala, musí se v družicových hodinách započítávat oba Einsteinovy relativistické efekty.",
        "Původně to byl vojenský systém americké armády, pro civilisty dlouho úmyslně zhoršený.",
        "Určuje polohu a jeho evropskou obdobou je Galileo.",
    )),
    ("Poznej vynález.", "Dynamit", [], (
        "Podstatou je nasáknout nitroglycerin do křemeliny, čímž se stane bezpečně přenosným.",
        "Jeho vynálezce z výnosů založil nadaci, která uděluje nejznámější světové ceny.",
        "Patentoval ho roku 1867 Alfred Nobel.",
    )),
    ("Poznej dopravní stavbu.", "Metro", ["podzemní dráha"], (
        "První linka na světě se otevřela v Londýně roku 1863 a jezdily po ní parní lokomotivy.",
        "V Praze začalo jezdit roku 1974 a má tři linky označené písmeny.",
        "Je to podzemní kolejová doprava ve velkých městech.",
    )),
    ("Poznej techniku.", "3D tisk", ["aditivní výroba"], (
        "Odborně se tomu říká aditivní výroba, protože materiál přibývá, místo aby se odebíral.",
        "Nejrozšířenější domácí metoda taví plastovou strunu a klade ji po vrstvách.",
        "Česká firma Průša patří k jeho světovým výrobcům.",
    )),
    ("Poznej vynález.", "Kardiostimulátor", ["pacemaker"], (
        "První plně implantovatelný přístroj dostal roku 1958 pacient Arne Larsson — a přežil svého lékaře i vynálezce.",
        "Napájí ho baterie, která vydrží zhruba deset let, pak se mění celý přístroj.",
        "Zavádí se pod kůži na hrudi a udržuje pravidelný tep srdce.",
    )),
    ("Poznej vynález.", "Fotoaparát", ["kamera obscura", "fotografie"], (
        "Nejstarší dochovaný snímek pořídil Nicéphore Niépce kolem roku 1826 a expozice trvala hodiny.",
        "Princip vychází z temné komory, kterou popisovali už středověcí učenci.",
        "Dnes ho má každý v telefonu a dřív se do něj zakládal film.",
    )),
    ("Poznej českou značku.", "Tatra", [], (
        "Její nákladní vozy mají centrální nosnou rouru a nezávisle zavěšená výkyvná polonáprava.",
        "Sídlí v Kopřivnici a vyráběla i luxusní vozy s aerodynamickou zádí.",
        "Jejími vozy jezdí Rallye Dakar a model 815 zná v Česku každý ze stavby.",
    )),
    ("Poznej vynález.", "Kontaktní čočka", ["kontaktní čočky"], (
        "Měkké čočky z hydrogelu vynalezl v Československu Otto Wichterle a první odlil na dětské stavebnici.",
        "Materiál se jmenuje HEMA a patent skončil v cizích rukou.",
        "Nosí se místo brýlí přímo na oku.",
    )),
    ("Poznej techniku.", "Šifra Enigma", ["Enigma"], (
        "Základ luštění položili polští matematici v čele s Marianem Rejewskim ještě před válkou.",
        "Klíčovou slabinou bylo, že písmeno se nikdy nezašifrovalo samo na sebe.",
        "Používal ji za druhé světové války Wehrmacht a luštil ji Alan Turing v Bletchley Parku.",
    )),
    ("Poznej stavbu.", "Suezský průplav", ["Suez"], (
        "Nemá jediné zdymadlo, protože obě moře na jeho koncích jsou skoro ve stejné výšce.",
        "Otevřel se roku 1869 podle projektu Ferdinanda de Lesseps.",
        "Roku 2021 ho na šest dní zablokovala loď Ever Given.",
    )),
    ("Poznej vynález.", "Žárovka", [], (
        "Rozhodující nebylo vlákno samo, ale dostatečně kvalitní vývěva, která z baňky odčerpala vzduch.",
        "Thomas Edison ji nevynalezl jako první, ale jako první ji udělal prakticky použitelnou.",
        "Dnes ji nahradily úspornější LED diody.",
    )),
    ("Poznej techniku.", "Bluetooth", [], (
        "Jméno nese po dánském králi z 10. století, který sjednotil znesvářené kmeny.",
        "Jeho značka je runová ligatura iniciál toho krále.",
        "Bezdrátově spojuje sluchátka, reproduktory a telefony na krátkou vzdálenost.",
    )),
    ("Poznej stroj.", "Jaderný reaktor", ["atomový reaktor"], (
        "První řízenou řetězovou reakci spustil Enrico Fermi roku 1942 pod tribunou chicagského stadionu.",
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
        "Přídomek v názvu mu roku 1920 udělil král Alfons XIII.",
        "Hraje na stadionu Santiago Bernabéu a jeho největší rival je z hlavního města Katalánska.",
        "Je to nejúspěšnější klub v historii Ligy mistrů a hrál za něj Cristiano Ronaldo.",
    )),
    ("Poznej sport.", "Curling", [], (
        "Kameny se vyrábějí ze žuly z jediného skotského ostrůvku Ailsa Craig.",
        "Hráči před kamenem zametají led, aby upravili jeho dráhu a rychlost.",
        "Je to zimní olympijský sport a v Česku ho zpopularizovaly hlavně smíšené páry.",
    )),
    ("Poznej sportovce.", "Jaromír Jágr", ["Jágr"], (
        "Číslo 68 nosí na památku roku, kdy do Československa vpadla vojska.",
        "Je odchovancem Kladna, jehož klub později koupil.",
        "Je nejproduktivnějším Evropanem v historii NHL a získal Stanley Cup s Pittsburghem.",
    )),
    ("Poznej sportovní akci.", "Tour de France", [], (
        "Vznikla roku 1903 jako reklama na noviny L'Auto, které se tiskly na žlutém papíře.",
        "Proto má vedoucí závodník žlutý dres; puntíkovaný patří nejlepšímu vrchaři.",
        "Je to nejslavnější cyklistický závod a končí na pařížské Champs-Élysées.",
    )),
    ("Poznej sport.", "Baseball", [], (
        "Nadhazovač smí za zápas hodit prakticky neomezeně, ale hra nemá časový limit — může trvat, jak dlouho chce.",
        "Hřiště má tvar výseče se čtyřmi metami a zápas má devět směn.",
        "Nejslavnější soutěž se hraje v USA a Japonsku a její vyvrcholení nese název Světová série.",
    )),
    ("Poznej sportovkyni.", "Martina Navrátilová", ["Navrátilová"], (
        "V roce 1975 po US Open požádala o azyl ve Spojených státech a přišla o československé občanství.",
        "Získala devět wimbledonských titulů ve dvouhře, nejvíc v historii.",
        "Je to česko-americká tenistka, jejíž největší soupeřkou byla Chris Evertová.",
    )),
    ("Poznej fotbalistu.", "Josef Masopust", ["Masopust"], (
        "Roku 1962 se stal jediným Čechoslovákem, který získal Zlatý míč pro nejlepšího fotbalistu Evropy.",
        "Hrál za Duklu Praha a vstřelil první gól ve finále mistrovství světa v Chile.",
        "Byl vyhlášen českým fotbalistou století a nese jeho jméno i typický útočný manévr se dvěma přihrávkami.",
    )),
    ("Poznej sport.", "Biatlon", [], (
        "Za každou nezasaženou terčovou položku se běží trestné kolo 150 metrů nebo se přičítá minuta.",
        "Střílí se vleže i vstoje na terče vzdálené padesát metrů.",
        "Spojuje běh na lyžích a střelbu z malorážky; v Česku ho proslavila Gabriela Soukalová.",
    )),
    ("Poznej stadion.", "Wembley", ["Wembley Stadium"], (
        "Nad novou stavbou z roku 2007 se klene oblouk vysoký 133 metrů, který nese většinu váhy střechy.",
        "Starou podobu poznal každý podle dvou bílých věží.",
        "Je to národní fotbalový stadion Anglie v Londýně.",
    )),
    ("Poznej sportovce.", "Usain Bolt", ["Bolt"], (
        "Trpí skoliózou a jeho krok měří přes dva a půl metru, takže na stovku potřebuje o pár kroků méně než soupeři.",
        "Pochází z Jamajky a jeho oslavné gesto připomíná lučištníka.",
        "Drží světové rekordy na 100 i 200 metrů z Berlína 2009.",
    )),
    ("Poznej sport.", "Šerm", [], (
        "Soutěží se ve třech zbraních, které se liší platnou zásahovou plochou i pravidlem přednosti.",
        "Ty zbraně se jmenují fleret, kord a šavle.",
        "Je jedním z pěti sportů, které byly na programu všech novodobých olympiád.",
    )),
    ("Poznej sportovní trofej.", "Stanley Cup", ["Stanleyův pohár"], (
        "Jména vítězů se do ní ryjí a nejstarší prstence se po čase odebírají do síně slávy.",
        "Darovaný roku 1892 generálním guvernérem Kanady a je to nejstarší trofej severoamerického profesionálního sportu.",
        "Získává ji vítěz play off NHL.",
    )),
    ("Poznej olympijský sport.", "Moderní pětiboj", ["pětiboj"], (
        "Sestavil ho zakladatel novodobých olympijských her Pierre de Coubertin podle představy o schopnostech kurýra za nepřátelskou linií.",
        "Jednou z pěti částí bývala jízda na neznámém koni, kterou po sporech v Tokiu 2020 nahradila překážková dráha.",
        "Zbylé části jsou šerm, plavání, běh a střelba — a Češi v něm mají olympijské zlato Davida Svobody.",
    )),
    ("Poznej sportovce.", "Muhammad Ali", ["Ali", "Cassius Clay"], (
        "Roku 1967 odmítl narukovat do Vietnamu a na tři a půl roku přišel o licenci.",
        "Zápas v Kinshase roku 1974 proti Georgi Foremanovi vešel do dějin jako Rachot v džungli.",
        "Byl to boxer, který o sobě říkal, že se vznáší jako motýl a bodá jako včela.",
    )),
    ("Poznej sport.", "Ragby", ["rugby"], (
        "Míč se smí přihrávat jen dozadu, dopředu se s ním běží nebo kope.",
        "Podle legendy vzniklo, když žák anglické školy popadl při fotbale míč do rukou a rozběhl se.",
        "Nejslavnější soutěž je Světový pohár a hraje se s oválným míčem.",
    )),
    ("Poznej fotbalový turnaj.", "Mistrovství světa ve fotbale", ["MS ve fotbale", "světový pohár"], (
        "První ročník se hrál roku 1930 v Uruguayi a evropské týmy tam pluly lodí.",
        "Trofej ve své první podobě jednou ukradli a našel ji pes jménem Pickles.",
        "Koná se každé čtyři roky a nejvíc titulů má Brazílie.",
    )),
    ("Poznej sportovkyni.", "Ester Ledecká", ["Ledecká"], (
        "V Pchjongčchangu jela na vypůjčených lyžích od Mikaely Shiffrinové.",
        "Je vnučkou hokejisty Jana Klapáče a dcerou známého českého zpěváka a kytaristy.",
        "Na jedné olympiádě vyhrála super-G na lyžích i paralelní obří slalom na snowboardu.",
    )),
    ("Poznej sport.", "Judo", [], (
        "Zakladatel Džigoró Kanó ho vytvořil roku 1882 z jiu-jitsu a název znamená „jemná cesta“.",
        "Vítězství se dá získat naráz technikou zvanou ippon.",
        "Závodí se v kimonu a v Česku ho proslavil olympijský vítěz Lukáš Krpálek.",
    )),
    ("Poznej hokejový turnaj.", "Nagano 1998", ["olympiáda v Naganu", "Nagano"], (
        "Poprvé se sem směli přihlásit hráči ze zámořské profesionální soutěže, která kvůli tomu přerušila sezonu.",
        "Ve finále padl jediný gól, ve čtvrtfinále rozhodly nájezdy proti Kanadě.",
        "Češi na něm vyhráli hokejové zlato a brankářem byl Dominik Hašek.",
    )),
]

# --------------------------------------------------------------------------
# Jazyk
# --------------------------------------------------------------------------
BANK["jazyk"] = [
    ("Doplňte společný přívlastek.", "turecký", ["turecké", "turecká"], (
        "Prohlubeň klínové kosti lebky, ve které je uložena hypofýza.",
        "Klavírní sonáta A dur Wolfganga Amadea Mozarta se tak jmenuje podle svého třetího věty.",
        "Určitá káva se připravuje z jemně mleté kávy zalité vroucí vodou přímo v šálku.",
    )),
    ("Poznej příjmení.", "Wright", [], (
        "Měl ho klávesista skupiny Pink Floyd, který si křestní jméno Richard zkracoval na Rick.",
        "Nosil ho i slavný americký architekt Frank Lloyd.",
        "Proslavili ho také bratři Wilbur a Orville, průkopníci letectví.",
    )),
    ("Poznej jazyk.", "Baskičtina", ["baskicky", "baskický jazyk"], (
        "Je to takzvaný izolovaný jazyk — nepodařilo se prokázat příbuznost s žádným jiným na světě.",
        "Mluví se jím na pomezí Španělska a Francie kolem Biskajského zálivu.",
        "Sami mu mluvčí říkají euskara a hovoří jím zhruba tři čtvrtě milionu lidí.",
    )),
    ("Poznej slovo podle původu.", "Robot", [], (
        "Základem je staročeské slovo pro nucenou práci na panském.",
        "Do světových jazyků ho dostala divadelní hra z roku 1920.",
        "Autorovi ho poradil jeho bratr Josef a dnes tak říkáme strojům, které pracují místo lidí.",
    )),
    ("Poznej písmo.", "Hlaholice", [], (
        "Sestavil ji v 9. století Konstantin pro překlad bohoslužebných knih do slovanského jazyka.",
        "Její tvary se odvozují od řecké minuskule a znaky mají i číselnou hodnotu.",
        "Používali ji na Velké Moravě Cyril a Metoděj; později ji vytlačila cyrilice.",
    )),
    ("Poznej jazykový jev.", "Palindrom", [], (
        "Nejdelší běžně uváděné české slovo tohoto typu je „nepochopen“.",
        "Latinský příklad zní „sator arepo tenet opera rotas“ a dá se číst i po sloupcích.",
        "Je to slovo nebo věta, která zní stejně zepředu i zezadu — třeba „kobyla má malý bok“.",
    )),
    ("Poznej pravopisný jev.", "Vyjmenovaná slova", ["vyjmenovaná slova po B"], (
        "Existují jen v češtině a slovenštině a jinde ve slovanských jazycích obdobu nemají.",
        "Souvisejí s tím, že se v dávné výslovnosti lišila dvě písmena, která dnes zní stejně.",
        "Školáci se je učí zpaměti v řadách jako „být, bydlit, obyvatel, byt, příbytek…“.",
    )),
    ("Poznej slovo.", "Ostrov", [], (
        "Ve staré češtině znamenalo doslova „obtékané“ — od téhož základu jako proud a struha.",
        "Ve Středočeském kraji i v Karlovarském kraji je město s tímhle jménem.",
        "Je to souš ze všech stran obklopená vodou.",
    )),
    ("Poznej jazyk.", "Esperanto", [], (
        "Autor ho vydal roku 1887 pod pseudonymem, který v tom jazyce znamená „doufající“.",
        "Podstatná jména v něm končí na -o, přídavná na -a a nemá výjimky.",
        "Je to nejrozšířenější umělý jazyk a vytvořil ho Ludvík Lazar Zamenhof.",
    )),
    ("Poznej rčení.", "Mít máslo na hlavě", ["máslo na hlavě"], (
        "Podle jednoho výkladu pochází z časů, kdy hospodyně nosily zboží na trh na temeni a v horku jim teklo.",
        "Znamená to nést vlastní vinu, kterou by si člověk měl uvědomit dřív, než ukáže prstem na někoho jiného.",
        "Říká se to o někom, kdo obviňuje ostatní z něčeho, co má na svědomí sám.",
    )),
    ("Poznej termín.", "Pangram", [], (
        "Nejznámější anglický příklad se používá jako ukázka písma a mluví o lišce a psu.",
        "Český příklad zní „příliš žluťoučký kůň úpěl ďábelské ódy“.",
        "Je to věta, ve které se objeví všechna písmena abecedy.",
    )),
    ("Poznej abecedu.", "Braillovo písmo", ["Braille", "braillovo písmo"], (
        "Vychází z vojenského systému nočního psaní, který vymyslel Charles Barbier pro čtení potmě.",
        "Autor ho vytvořil ve svých patnácti letech, sám nevidomý po úrazu z dětství.",
        "Je to písmo pro nevidomé, sestavené ze šesti vyvýšených bodů.",
    )),
    ("Poznej slovo podle původu.", "Pistole", [], (
        "Nejrozšířenější výklad ho odvozuje z názvu českého města Písek, kde se v husitské době vyráběly.",
        "Do němčiny se dostalo skoro beze změny a odtud se rozšířilo do celého světa.",
        "Je to krátká ruční palná zbraň.",
    )),
    ("Poznej jazyk.", "Latina", [], (
        "Jako úřední jazyk ji dodnes používá jediný stát na světě — Vatikán.",
        "Vznikla v kraji Latium a rozšířila ji říše, jejímž hlavním městem byl Řím.",
        "Vycházejí z ní románské jazyky a používá se v biologickém a lékařském názvosloví.",
    )),
    ("Poznej termín.", "Anagram", ["přesmyčka"], (
        "Slavným příkladem je „Marie Curie“ přeskládané jinými autory na různé věty.",
        "V češtině se mu říká přesmyčka a je základem hry Věž.",
        "Vznikne přeházením písmen jednoho slova tak, že vyjde slovo jiné.",
    )),
    ("Poznej slovo.", "Tunel", [], (
        "Pochází ze starofrancouzského slova pro soudek nebo trubku.",
        "V češtině devadesátých let se z něj stalo sloveso pro vyvádění peněz z firmy.",
        "Původně a hlavně je to podzemní chodba pro dopravu.",
    )),
    ("Poznej jazyk.", "Islandština", ["islandsky"], (
        "Změnila se od dob ság tak málo, že dnešní mluvčí přečte středověké texty bez překladu.",
        "Nová slova se v ní zásadně netvoří přejímáním, ale skládáním domácích kořenů.",
        "Mluví se jí na severoatlantském ostrově s hlavním městem Reykjavík.",
    )),
    ("Poznej jev.", "Homonymum", [], (
        "Odborně se rozlišuje ještě na homofona, která stejně znějí, a homografa, která se stejně píší.",
        "Klasický český příklad je slovo „kolej“ nebo „raketa“.",
        "Jsou to slova, která znějí stejně, ale znamenají něco úplně jiného.",
    )),
    ("Poznej jazyk.", "Sanskrt", [], (
        "Jeho gramatiku popsal Pánini už kolem 4. století př. n. l. tak přesně, že ji dodnes uvádějí jako vzor.",
        "Objev jeho podobnosti s řečtinou a latinou v 18. století založil srovnávací jazykovědu.",
        "Je to posvátný jazyk hinduismu, ve kterém je napsána Bhagavadgíta.",
    )),
    ("Poznej termín.", "Idiom", ["frazém", "ustálené spojení"], (
        "Jeho význam se nedá odvodit ze součtu významů jednotlivých slov.",
        "Bývá to nejtěžší část jazyka pro cizince a strojový překlad ho často zkazí.",
        "Patří sem třeba „házet flintu do žita“ nebo „mít hlavu v oblacích“.",
    )),
]

# --------------------------------------------------------------------------
# Společnost
# --------------------------------------------------------------------------
BANK["spolecnost"] = [
    ("Poznej organizaci.", "Červený kříž", ["Mezinárodní červený kříž"], (
        "Vznikl po bitvě u Solferina roku 1859, kterou popsal Henri Dunant v knize Vzpomínka na Solferino.",
        "Jeho znak je obrácená vlajka Švýcarska a v muslimských zemích se používá jiný symbol.",
        "Stará se o raněné ve válce a jeho sídlo je v Ženevě.",
    )),
    ("Poznej dokument.", "Všeobecná deklarace lidských práv", ["deklarace lidských práv"], (
        "Přijalo ji Valné shromáždění OSN 10. prosince 1948 v Paříži; osm států se zdrželo.",
        "Na jejím vzniku měla velký podíl Eleanor Rooseveltová.",
        "Je to nejpřekládanější dokument světa a začíná větou, že všichni lidé se rodí svobodní a rovní.",
    )),
    ("Poznej cenu.", "Nobelova cena", [], (
        "Uděluje se od roku 1901 a peníze na ni plynou z nadace založené z výnosů dynamitu.",
        "Tu za mír uděluje jako jedinou norský výbor, ostatní švédské instituce.",
        "Předává se každý rok 10. prosince, v den úmrtí zakladatele.",
    )),
    ("Poznej svátek.", "Velikonoce", [], (
        "Datum se řídí prvním jarním úplňkem, proto se každý rok posouvá.",
        "Křesťané při nich slaví zmrtvýchvstání a předchází jim čtyřicetidenní půst.",
        "V Česku k nim patří pomlázka, kraslice a Velký pátek.",
    )),
    ("Poznej instituci.", "Evropský parlament", [], (
        "Zasedá střídavě ve dvou městech, což kritici označují za drahý cirkus.",
        "Ta města jsou Brusel a Štrasburk, sekretariát sídlí v Lucemburku.",
        "Jeho poslance volí občané členských států unie přímo, jednou za pět let.",
    )),
    ("Poznej zvyk.", "Podávání ruky", ["potřesení rukou", "handshake"], (
        "Jeden z výkladů říká, že gesto původně ukazovalo, že v ruce není zbraň.",
        "V Japonsku ho z velké části nahrazuje úklona, v arabském světě má vlastní pravidla.",
        "Je to nejběžnější evropský pozdrav při setkání i uzavření dohody.",
    )),
    ("Poznej pojem.", "Demokracie", [], (
        "Slovo skládá řecké démos a kratos, tedy „lid“ a „vláda“.",
        "Její přímou podobu praktikovaly Athény v 5. století př. n. l., ale bez žen a otroků.",
        "Dnes se jí říká vláda lidu a jejím základem jsou svobodné volby.",
    )),
    ("Poznej měnu.", "Euro", [], (
        "V bezhotovostní podobě začalo platit už roku 1999, mince a bankovky až o tři roky později.",
        "Na bankovkách jsou schválně smyšlené stavby, aby nezvýhodnily žádnou zemi.",
        "Platí jím většina států Evropské unie a jeho symbol vychází z řeckého písmene epsilon.",
    )),
    ("Poznej instituci.", "UNESCO", [], (
        "Zkratka rozepsaná znamená Organizace OSN pro výchovu, vědu a kulturu.",
        "Sídlí v Paříži a vzniklo roku 1945 s myšlenkou, že mír se buduje v myslích lidí.",
        "Vede seznam světového dědictví, na kterém je z Česka Praha, Český Krumlov nebo Kutná Hora.",
    )),
    ("Poznej pojem.", "Inflace", [], (
        "Měří se indexem spotřebitelských cen ze spotřebního koše zboží a služeb.",
        "Její extrémní podoba postihla Německo roku 1923, kdy se ceny zdvojnásobovaly každé dva dny.",
        "Je to růst cenové hladiny — za stejné peníze si člověk koupí míň než dřív.",
    )),
    ("Poznej svátek.", "Svátek práce", ["1. máj", "První máj"], (
        "Datum připomíná stávku a následné střety v Chicagu roku 1886.",
        "V Česku je zároveň dnem, kdy se líbá pod rozkvetlou třešní.",
        "Připadá na začátek května a v Česku je to státní svátek.",
    )),
    ("Poznej pojem.", "Gramotnost", [], (
        "Odborně se dnes rozlišuje ještě funkční podoba, tedy schopnost textu porozumět a použít ho.",
        "Světový den se jí věnuje 8. září a UNESCO ji sleduje jako klíčový ukazatel rozvoje.",
        "Základem je umět číst a psát.",
    )),
    ("Poznej organizaci.", "NATO", ["Severoatlantická aliance"], (
        "Její zakládací smlouva se podepsala roku 1949 ve Washingtonu.",
        "Slavný článek 5 říká, že útok na jednoho je útokem na všechny; poprvé se uplatnil po 11. září 2001.",
        "Česko do ní vstoupilo roku 1999 a jejím sídlem je Brusel.",
    )),
    ("Poznej pojem.", "Volební právo žen", ["ženské volební právo"], (
        "Jako první ho na celostátní úrovni zavedl roku 1893 Nový Zéland.",
        "V Československu platilo od ústavy roku 1920, ve Švýcarsku na federální úrovni až od roku 1971.",
        "Znamená, že ženy smějí volit stejně jako muži.",
    )),
    ("Poznej pojem.", "Sčítání lidu", ["cenzus"], (
        "Nejstarší doložené probíhalo v Egyptě a v Bibli se o něm mluví v souvislosti s Betlémem.",
        "V Česku ho provádí Český statistický úřad a koná se jednou za deset let.",
        "Zjišťuje, kolik lidí kde žije a jak.",
    )),
    ("Poznej tradici.", "Masopust", ["karneval"], (
        "Trvá od Tří králů do Popeleční středy a končí půlnočním pochováním basy.",
        "V Hlinecku je zapsán na seznamu nehmotného dědictví UNESCO.",
        "Je to období zabijaček, průvodů v maskách a veselí před postem.",
    )),
    ("Poznej pojem.", "Sociální síť", ["sociální sítě"], (
        "Původně to byl pojem ze sociologie pro vztahy mezi lidmi, dávno před internetem.",
        "První velkou internetovou podobu měla SixDegrees.com z roku 1997, pojmenovaná podle teorie šesti kroků.",
        "Dnes si pod tím každý představí Facebook nebo Instagram.",
    )),
    ("Poznej dokument.", "Ústava České republiky", ["česká ústava", "Ústava ČR"], (
        "Byla přijata 16. prosince 1992, tedy ještě před vznikem státu, který upravuje.",
        "Skládá se z preambule a osmi hlav a mluví o svobodných a odpovědných občanech.",
        "Platí od 1. ledna 1993 a stojí na jejím vrcholu Ústavní soud v Brně.",
    )),
    ("Poznej instituci.", "Vatikán", ["Vatikánský městský stát", "Svatý stolec"], (
        "S rozlohou 0,44 km² je nejmenším uznaným státem světa a vznikl Lateránskými dohodami roku 1929.",
        "Střeží ho Švýcarská garda a jeho jediným úředním jazykem je latina.",
        "Sídlí tu papež a stojí zde Sixtinská kaple.",
    )),
    ("Poznej pojem.", "Menšina", ["národnostní menšina"], (
        "Právně ji definují mezinárodní úmluvy podle jazyka, kultury nebo původu, ne podle počtu samotného.",
        "V Česku má zákonem uznaných čtrnáct takových skupin a zastupuje je vládní rada.",
        "Je to skupina, která se v zemi odlišuje od většiny a má právo na svá práva.",
    )),
]
