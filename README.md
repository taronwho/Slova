# Slova

Pět českých slovních her v jedné webové aplikaci. Běží čistě staticky, bez serveru,
a **každá vygenerovaná hádanka je ověřeně dohratelná**.

## Režimy

### Řetěz — slovní žebřík
Od startovního slova k cílovému, vždy změnou jednoho písmene, a každý mezikrok
musí být platné české slovo. Žádné slovo se nesmí zopakovat.

Hra po každém tahu spočítá skutečnou zbývající vzdálenost k cíli průchodem
grafu **bez už použitých slov** a ukáže ji jako „zbývá nejméně X tahů". Když
tah zavře cestu nebo vyčerpá rozpočet, strážce řešitelnosti to hlásí a nabídne
vrácení tahu. Hráč se tedy nikdy nedostane do neřešitelné pozice, aniž by o tom
věděl.

### Voština — plástev písmen
Sedm písmen, prostřední povinné. Skládají se slova od čtyř písmen výš, písmena
se smějí opakovat. V každé plástvi je aspoň jeden pangram využívající všech
sedm písmen. Postup vede přes hodnosti od Začátečníka po Královnu češtiny.

Diakritika se proti plástvi skládá (á=a, č=c, ř=r …), takže „cili" najde slovo
„cíli" — jinak by nešlo hrát ťukáním do šestiúhelníků na mobilu.

### Šibenice — hádání po písmenech
Slovo je schované za prázdnými políčky, hráč zkouší písmena a osm chybných
znamená konec. Dvě věci jsou jinak než na papíře: **diakritika se hádá po
základním písmeni** („u" odhalí u, ú i ů), takže se hádá slovo a ne háčky a na
telefonu stačí šestadvacet kláves; a nápověda „vyškrtni pět" zhasne písmena,
která ve slově nejsou, za body, ne za život.

Slova se vybírají podle frekvence, ne náhodně — u ostatních režimů se dá dojít
oklikou, tady buď slovo znáš, nebo visíš.

### Etymologický detektiv — poznej slovo podle původu
Místo písmenkové nápovědy dostane hráč text o tom, odkud slovo přišlo:
„Z latinského *castellum* (bašta, pevnůstka), zdrobněliny slova *castrum*" →
KOSTEL. Zkoušejí se písmena jako v Šibenici, ale **chyba nezabíjí, jen stojí
body** — text má být vodítko, se kterým se dá pracovat, ne past. A kdo na slovo
přijde dřív, může ho tipnout celé; čím víc písmen je ještě skrytých, tím vyšší
prémie.

Hádanek je **1 437** — tolik hesel má v české sekci Wikislovníku etymologii
a zároveň jsou to ověřené základní tvary. Kvůli tomu sahá slovník až ke
čtrnáctipísmenným slovům, i když se Řetěz, Voština a Věž drží do devíti: právě
u dlouhých přejatých slov („aproximace", „konvergentní") mívá Wikislovník
etymologii nejčastěji.

Text je z Wikislovníku tak, jak ho tam někdo napsal — jen se z něj vyhodí to,
co v hádance nedává smysl. Odkazovací ocas („Srovnej např. stožár, stehno,
stěžeň") je ve slovníku užitečný, hráči ale podstrčí jmenný seznam, který
o hledaném slově neříká nic. A useknout indicii uprostřed souvětí je ještě
horší, takže se krátí jen po celých větách. Kde by text slovo prozradil, je
místo něj **okénko s otazníkem** — schválně ne výpustka, ta se v etymologiích
vyskytuje sama o sobě.

### Slabikový tetris — padají slabiky, ty z nich skládáš slova

Shora padá **dvojice slabik**. Hráč s ní posouvá doleva a doprava, otáčí ji
a může ji nechat spadnout naráz. Jakmile dvě nebo tři sousední slabiky dají
platné české slovo, slovo zmizí, co bylo nad ním spadne dolů a z toho může
vzniknout další slovo — řetěz. Deska se plní, tempo zrychluje a kolo končí,
až se nová dvojice nemá kam vejít. Dohrát se nedá; hraje se, dokud se hráč
sám nezablokuje.

Otáčení je to hlavní, co se hraje. Dvojice má čtyři polohy a v každé se čte
jinak — vodorovně zleva doprava, svisle **zdola nahoru** (tím směrem, kterým
sloupec roste, stejně jako se čte Věž). „ko" a „lo" tedy dá KOLO ve dvou
různých polohách a v dalších dvou nedá nic.

Rozdává se z **balíčku tří set padesáti slabik**, ne z připravené dávky —
dvě kola po sobě proto nevypadají stejně. Zhruba každá třetí dvojice je
rozdělené slovo, které jde složit hned, jen ho správně otočit; zbytek se musí
doplnit tím, co na desce leží. Co je platné slovo, hra **nehádá**: seznam
devíti tisíc slov, která z balíčku jdou složit, je předpočítaný a staví se
z ověřených základních tvarů.

### Věž — anagramová věž### Věž — anagramová věž
Od tří písmen nahoru. V každém patře přibude jedno písmeno a hráč ze **všech**
dostupných písmen složí nové slovo v libovolném pořadí.

Právě povinnost použít všechna písmena dává věži nejsilnější možnou garanci:
každé platné řešení patra má nutně stejný podpis, takže volba konkrétního slova
nemůže zablokovat cestu nahoru. Řetěz podpisů je ověřený už při generování.

## Data

| | zdroj | výsledek |
|---|---|---|
| Slovník | frekvenční seznam češtiny profiltrovaný přes hunspell `cs_CZ` | 378 417 ověřených slov |
| Základní tvary | slova se skloňovacím/časovacím vzorem + lemmatizace | 55 585 slov |
| 1. pád množného čísla | buňky deklinačních vzorů z `cs_CZ.aff` | + 10 264 slov |
| Řetěz | grafy pro délky 4, 5 a 6 | 7 824 hádanek |
| Voština | plástve odvozené od pangramů | 2 400 hádanek |
| Věž | ověřené řetězy přesmyček 3→6/7/8 | 1 962 hádanek |
| Šibenice | nejčastější základní tvary po délkách | 2 100 slov |
| Detektiv | etymologie z české sekce Wikislovníku | 1 437 hádanek |
| Slabiky | pravidlové dělení základních tvarů na slabiky | 38 917 slov; balíček 350 slabik a 9 037 slov |

### Jen 1. pád a infinitiv

Hra pracuje výhradně se základními tvary: podstatná jména v 1. pádu (jednotné
i množné číslo), slovesa v infinitivu, přídavná jména, číslovky, zájmena,
příslovce a spojky. Bez toho hráč ve Voštině sbíral varianty jednoho slova
(„hravá, hravé, hravě, hrává") místo aby hledal nová.

Slovník vzniká ve dvou krocích.

**1. Základní tvar** (`tools/2b_base_forms.py`). Příznaky v `cs_CZ.aff` jsou
skloňovací a časovací **vzory** a vzor jde pověsit jedině na základní tvar —
hunspell z něj celé paradigma teprve odvozuje. To je důkaz, ne odhad:

```
hrad/HR      vzor „hrad"          -> 1. pád j. č.,  projde
mířit/AN     časování             -> infinitiv,     projde
velký/Y      skloňování adjektiv  -> 1. pád m. r.,  projde
agente       bez vzoru            -> neprojde
ovsa         bez vzoru            -> neprojde
stůj/N       jen předpona ne-     -> neprojde
sťat/ON      jmenný tvar          -> neprojde
moha/XN      přechodník           -> neprojde
níže/E       jen předpona nej-    -> neprojde
```

Holá hesla bez vzoru jsou v `cs_CZ.dic` promíchaná. Jsou mezi nimi příslovce
(„dnes"), spojky („ale") i nesklonná jména („alibi") — jenže úplně stejně
vypadá 2. pád („ovsa"), 5. pád („bože"), rozkaz („stůj") i zkratka („geol"),
protože nepravidelná slova má slovník rozepsaná po tvarech. Rozlišit je
automaticky nejde, takže se **zahazují všechna** a ručně ověřený výběr se vrací
ze souboru `tools/base_extra.txt` (nepravidelná jména jako „pes", „stůl",
„člověk", základní příslovce, spojky, předložky, zájmena a číslovky).

Druhá podmínka je **lemma se rovná slovu**: hunspell má jako hesla i ohýbané
tvary („boha", „bohu", „bohů"), ty odchytí **LemmaGen3**. `simplemma` jsem
zkoušel taky, ale pro češtinu je nepoužitelná — lemmatizuje „dobrý" na
„dokonavý" a „dělat" na „udělat".

Předchozí verze filtru zkoušely ruční pravidla nad koncovkami, porovnávání
frekvencí a nakonec „je to heslo slovníku?". Všechny propouštěly: „tang" je
jen 2× vzácnější než „tango", zatímco legitimní „lít" je 498× vzácnější než
„líto"; a jako hesla jsou vedená i „bože", „ovsa" nebo „stůj". Teprve
požadavek na skloňovací vzor je ostrý.

Cenou je příznak `R`, kterým hunspell tvoří odvozená příslovce („dobře ←
dobrý") *i* 6. pád („roce ← rok", „autě ← auto"). Rozlišit je nejde, takže se
nepouští ani jedno.

**2. Množné číslo** (`tools/2c_plural.py`). Ve vzoru se dá buňka „1. pád
množného čísla" ukázat prstem — je to konkrétní příponové pravidlo:

```
SFX H   0   y   [^ey]      hrad  -> hrady
SFX Z   a   y   [^…]a      žena  -> ženy
SFX M   o   a   [^c]o      město -> města
SFX I   ch  ši  ch         hoch  -> hoši
```

Vybrané buňky jsou v `tools/_plural_rules.py` (vzory H, L, S, U, D, I, V, Z,
K, M) a `2c_plural.py --vzorek` u každé vypíše dvojice ke kontrole. Nepoužívá
se `Q` (2. pád mn. č. — „služba → služeb", „tango → tang"), `P` (mužský vzor
bez vlastního 1. pádu mn. č.), `R`, `Y` ani slovesné příznaky.

Pojistky: příznaky `I`, `V` a `D` visí i na číslovkách („deset → deseti")
a slovesech, takže platí jen se jmenným vzorem; každý vygenerovaný tvar musí
být v ověřeném lexikonu; a když v jednom vzoru zaberou na jedno slovo dvě
pravidla, generování se zastaví — právě takhle se chytlo „kmen → kmene" vedle
správného „kmen → kmeny".

Poslední pojistkou je lemmatizér, ale jen jako **námitka**, ne jako potvrzení.
LemmaGen3 zná jen část slovní zásoby: u „sekery" vrátí „sekery", protože to
slovo prostě nemá. Když se to bralo jako neshoda, mizelo přes pět set správných
množných čísel („jablka", „trička", „pavouci", „sloni", „třešně") a hráč pak
ve Voštině napsal *sekery* a hra tvrdila, že to slovo nezná. Teď se tvar
zahodí, jen když ho lemmatizér přiřadí k **jinému** heslu — to znamená, že
vzor sáhl vedle. Že filtr není přísný na úkor správných tvarů, hlídá test
„zná i množná čísla, která lemmatizér neumí".

Vedlejším produktem je mapa tvar → výchozí heslo, kterou používá Věž: patro
nad „trajekt" nesmí nabídnout „trajekty". Přidat koncovku není hádanka, jen
opsané slovo, takže množné číslo slova z patra pod sebou se z nabídky vyhazuje
(a když by patro zůstalo prázdné, celá věž se zahodí).

Omezení na základní tvary má cenu: propojenost grafu pro Řetěz klesla natolik,
že se musely snížit prahy frekvence. Základní tvary jsou ale samy o sobě
srozumitelnější, takže nižší práh nevadí — „kaktus" pozná každý, i když se
v korpusu objevuje méně než „kaktusům".

Hunspell zároveň spolehlivě odfiltruje vlastní jména: ta jsou ve slovníku
uložena jen s velkým počátečním písmenem, takže lookup malé varianty („praha",
„brno") selže. Navíc se uplatňuje blocklist vulgarismů a hanlivých výrazů.

Do prohlížeče se posílají jen malé balíčky podle potřeby; graf sousednosti pro
Řetěz si klient staví sám ze seznamu slov (wildcard kbelíky, O(n·délka)), takže
se žádná předpočítaná struktura přenášet nemusí.

## Jak je řešitelnost doložená

Testy v `tests/data.test.ts` projdou **každou** hádanku, která by se dostala ke
hráči, a ověří:

- **Řetěz** — start i cíl jsou ve slovníku, uložená délka nejkratší cesty
  (v kódu `par`) se rovná skutečné vzdálenosti spočítané BFS, a rekonstruovaná
  cesta se v každém kroku liší přesně o jedno písmeno bez opakování slov.
- **Voština** — každé řešení jde z plástve složit, obsahuje povinný střed, každá
  plástev má aspoň jeden pangram a dost slov na rozehrání.
- **Věž** — každé patro má aspoň jedno slovo, všechna sedí na podpis a každé
  patro vzniklo přidáním právě jednoho písmene k tomu pod ním.
- **Šibenice** — hádané slovo je v ověřeném seznamu základních tvarů, délka
  sedí na obtížnost a slovo má aspoň tři různá písmena (dvoupísmenné slovo se
  uhodne dvěma tahy a hádanka to není).
- **Slabiky** — každé slovo, které jde na desce složit, je v ověřeném seznamu
  základních tvarů, a každé slovo balíčku jde z rozdávaných slabik opravdu
  poskládat (kontroluje se to zpětně na hotových datech, ne jen v generátoru).
- **Detektiv** — hádané slovo je v ověřeném seznamu základních tvarů a **text
  o původu ho nikde neprozradí**; kontroluje se to na hotových datech, ne jen
  ve generátoru. Prozradit ho umí i pravopisná varianta („spósob" vedle
  „způsob"), takže se porovnávají i souhláskové kostry. Navíc se hlídá, že
  indicie je celá věta a že v ní nezůstal slovníkový odkaz.

A protože testy čtou vygenerované soubory, jde `npm run play:verify` opačnou
cestou: v Chromiu **odehraje deset kol od každého z šesti režimů** a každé slovo, které
se objevilo na obrazovce nebo ho hra přijala, porovná se seznamem povolených
tvarů. Zároveň ověří, že se rozehrané kolo dá dohrát po návratu do menu
i po zavření hry a že se na telefonu všechno vejde na jednu obrazovku.

```
npm test             # 61 testů: herní logika + validace všech dat
npm run smoke        # průchod všemi třemi režimy v Chromiu, včetně mobilu
npm run play:verify  # 30 odehraných kol + kontrola tvarů slov
npm run audit:mobile # kontrola rozvržení na pěti rozlišeních
npm run audit:pwa    # manifest, ikony, offline režim
```

## Spuštění

```bash
npm install
npm run dev       # vývojový server
npm run build     # typecheck + produkční build do dist/
npm run preview   # náhled produkčního buildu
```

Systémové tlačítko zpět (na Androidu gesto) zavírá vrstvy hry, ne celou
aplikaci: nejdřív potvrzení nebo seznam, pak návod, pak hru, a teprve na
úvodní obrazovce se chová normálně. Řeší to `src/lib/back.ts` — každá
otevřená vrstva si přidá jeden záznam do historie a při návratu se zavře
místo toho, aby se opustila stránka.

Nevratné kroky (vzdát kolo, ukončit plástev) se nejdřív zeptají — tlačítka
jsou hned vedle ovládání a dají se trefit omylem.

Aplikace nepotřebuje žádný backend — `dist/` se dá nasadit na jakýkoli statický
hosting. Postup hráče se ukládá do `localStorage`, a to ve dvou klíčích:
profil se statistikami a zvlášť **rozehraná kola**, jedno od každého režimu.
Zapisují se po každém tahu, takže se hra dá dohrát i po odchodu do menu nebo
zavření prohlížeče, a rozehraný Řetěz nezruší rozehranou Voštinu — dlaždice
v menu ukáže „Rozehráno · 4 tahy" a panel nabídne Pokračovat i Novou hru.
Stranou od profilu jsou schválně: zapisují se často a jejich poškození nesmí
vzít s sebou statistiky.

### Jednosouborová verze

```bash
npm run build:standalone   # -> dist/slova-standalone.html
npm run smoke:standalone   # ověří, že běží bez jediného síťového požadavku
```

Pro hostování, kde stránka nesmí nic dotahovat ze sítě. Vloží dovnitř CSS, JS,
fonty jako data URI i herní data. Dvě věci, na které si tam dát pozor:

- výstup skriptů se převádí na čisté ASCII (`\uXXXX`), protože bez správně
  deklarovaného kódování by se české řetězce rozsypaly a shodily celý skript,
- escapují se sekvence `</`, `<script` a `<!--`, které přepínají stav HTML
  parseru uvnitř `<script>` (React DOM má `"<script><\/script>"` v literálu).

Datové sady se pro tuhle verzi ořezávají, ať stránka zůstane rozumně velká —
Řetěz jde celý, u Voštiny a Věže je to výřez.

## Přegenerování dat

Hotová data jsou v repozitáři (`public/data/`), takže build funguje rovnou.
Přegenerovat je lze takto:

```bash
pip install spylls
npm run data:build
```

Skripty v `tools/` běží po krocích:

| skript | co dělá |
|---|---|
| `0_download.sh` | stáhne frekvenční seznam a hunspellový slovník |
| `1_validate_words.py` | ověří slova proti hunspellu (~4 min na 4 jádrech) |
| `2_curate.py` | rozdělí lexikon podle délky, uplatní blocklist |
| `2b_base_forms.py` | nechá jen hesla hunspellu, u kterých lemma sedí |
| `2c_plural.py` | dogeneruje 1. pád množného čísla z deklinačních vzorů |
| `3_build_chain.py` | postaví grafy, najde dvojice a ověří nejkratší cesty |
| `4_build_hive.py` | odvodí plástve od pangramů a spočítá kompletní řešení |
| `5_build_tower.py` | najde ověřené řetězy přesmyček |
| `5b_build_gallows.py` | vybere nejčastější slova po délkách pro Šibenici |
| `5c_fetch_etymology.py` | stáhne etymologie z Wikislovníku do cache |
| `5d_build_detective.py` | vybere z nich hádanky a zamaskuje prozrazující slova |
| `5e_syllables.py` | rozdělí základní tvary na slabiky, sporná dělení zahodí |
| `5f_build_tetris.py` | vybere slabiky k rozdávání a spočítá všechna jejich slova |
| `playthrough.mjs` | odehraje 10 kol od každého z šesti režimů a zkontroluje tvary slov |

## Struktura

```
src/game/        herní logika bez závislosti na UI (chain, hive, tower, scoring)
src/lib/         české utility, seedovaný RNG, perzistence
src/components/  React komponenty jednotlivých obrazovek
src/styles/      designové tokeny a stylopis
public/data/     vygenerované hádanky
tools/           generátory dat a prohlížečový test
tests/           testy logiky a validace dat
```

## Značka

Prostřední „O" ve slově SLOVA je terč a vedle názvu svítí tři tečky, jedna za
každou hru. Z toho vychází i **ikona aplikace**: kroužek složený ze tří
stejných oblouků v barvách Řetězu, Voštiny a Věže, uprostřed světlý bod.
Nese informaci (tři hry v jedné) a čte se i v 48 px. Generuje ji
`tools/6_build_icons.py` v obou variantách, běžné i maskable.

Totéž znamení se při spuštění krátce ukáže na celé obrazovce: oblouky se
nakreslí (animovaný `stroke-dashoffset`), název se poskládá po písmenech,
značka vteřinu vydrží a rozplyne se do menu. Hra se pod ní mezitím načítá,
takže úvod nikoho nezdržuje, a s `prefers-reduced-motion` zůstane jen
prolnutí.

## Vzhled

Identita stojí na elektrické fialové a triádě barev pro tři režimy: fialová
Řetěz, medová Voština, rumělková Věž. Ty tři se potkávají ve značce a na
domovské obrazovce; uvnitř hry pak barva režimu přebere roli akcentu a obarví
celé prostředí, takže hráč pozná, kde je, ještě než přečte nadpis. Neutrály
nejsou šedé — mají fialový nádech, aby se značkou ladily.

Typografie: Bricolage Grotesque pro nadpisy, dlaždice a čísla, Manrope pro
běžný text. Obě písma pokrývají českou diakritiku kompletně (ověřeno proti
seznamu znaků, latin + latin-ext dohromady).

Světlé i tmavé téma podle systému nebo ručně; animace respektují
`prefers-reduced-motion`.

Kontrast řeší dva tokeny. `--band-ink` je barva textu na barevném pruhu karty
a `--on-accent` barva textu na plné ploše akcentu — v tmavém tématu jsou barvy
režimů světlé, takže se text musí obrátit na tmavý. Medová je světlá v obou
tématech a má tmavý text vždy.

## Návody

Při prvním spuštění každého režimu se otevře návod: šest kroků s ukázkami
poskládanými ze skutečných herních prvků, zvýrazněnou hlavní zásadou a
možností přeskočit. Znovu ho lze vyvolat tlačítkem Pravidla v horní liště
nebo z domovské obrazovky, kde jsou pravidla i v rozbalovací textové podobě.

Texty žijí v `src/game/tutorials.ts` odděleně od komponent, aby je šlo použít
na obou místech.

## Hodnosti a ocenění

Postup drží dvě věci: **padesát hodností** (`src/game/ranks.ts`) a
**sto čtyřiašedesát ocenění** (`src/game/awards.ts`). Hodnost roste
s **věhlasem** — tak se jmenuje součet bodů ze všech šesti her —, ocenění jsou
jednotlivé mety.

Prahy hodností jsou nerovnoměrné schválně. První tři odsýpají, ať má nový hráč
co slavit hned první večer: druhá padne po jednom kole, třetí po druhém, čtvrtá
po pátém. Od té chvíle se rozestupy natahují o patnáct procent na každém
stupni, takže dvacátá hodnost je na dvě stě kol a padesátá na dobrých jedenáct
tisíc. Hlídá to test: od čtvrté hodnosti musí být každý další stupeň dražší než
ten předchozí a poslední přes deset milionů věhlasu.

### Žebříčky, ne seznam

Čtyřicet met se vyčerpá za pár večerů a pak už není za čím jít. Slova se ale
mají hrát roky, takže je většina met postavená jako **žebříček**: jedna rodina,
tři až pět stupňů, poslední tak daleko, že se na něj hraje sezónu. Rodin je
jednačtyřicet a nese je `ladder()` — dostane jedno číslo z profilu a seznam
prahů, zbytek (klíče, stupně, ukazatel postupu) dopočítá.

Ve vitríně se žebříček **nerozbaluje celý**. Ukazují se získané stupně a hned
následující, tedy ten, na který se zrovna hraje; sto šedesát dlaždic naráz
nikoho nemotivuje, jeden další stupeň ano. Kdo chce vidět celou cestu až
k Legendě, přepne se v hlavičce na „Všech 164".

Mety zůstávají schválně **za dovednost, ne za vysedění**. Nejpočetnější skupina
je „Mistrovské kousky" (47 met) a hned za ní „Mistrovství her" — šest žebříčků
po pěti stupních, od Učně po Legendu, a všechny počítají jen kola dohraná
**bez nápovědy**. „Odehraj sto kol" má jedinou skromnou rodinu ve Vytrvalosti;
takovou metu splní každý, kdo vydrží klikat. Hlídá to test „většina met stojí
na dovednosti nebo bodech": skupiny `clean`, `score`, `mastery` a `feat` musí
dohromady tvořit víc než polovinu.

Jediná skupina, kterou nejde dohnat jedním večerem, je „Návyk": dny v řadě, dny
celkem a denní várky. Den se počítá jednou, ať se odehraje kolo nebo dvacet.

**Klíče ocenění jsou navěky.** Podle nich se v uloženém profilu pozná, co hráč
má; přejmenovat klíč znamená udělit metu — a inkoust za ni — podruhé. Proto tu
zůstávají i klíče, které se s dnešním nadpisem míjejí (`xp-50k` pro věhlas,
`skore-1500` pro pět set bodů). Nadpis i práh se přepsat smí, klíč ne; hlídá to
test na duplicity.

**Čisté kolo je až to, které hráč dotáhl.** Viselec v Šibenici ani plástev
ukončená po třech slovech se nepočítají, i když v nich nebyla ani jedna
nápověda — jinak by se meta „Vlastní hlavou" dala splnit tím, že hráč kolo
prostě prohraje. Každý režim proto hlásí `success` (došel do cíle, vysbíral
plástev, dostavěl věž, uhodl slovo) zvlášť od toho, že kolo skončilo.

Podmínka ocenění se čte **jen z profilu**, nikdy z právě dohraného kola.
Ocenění se proto dají kdykoli přepočítat znovu (a při načtení profilu se to
dělá): kdyby kolo spadlo dřív, než se zapsalo, meta se dožene sama. Profil
kvůli tomu vedle statistik drží počítadla, která se ze statistik odvodit
nedají — čistá kola a jejich nejdelší řada, pangramy, dostavěné věže bez
nápovědy, nejrychlejší čistý řetěz.

Kresby jsou vlastní, ne emoji ani ikony odjinud:

- `src/components/art/RankBadge.tsx` — odznak hodnosti. Padesát stupňů má pět
  tvarů štítu (kolo, šestiúhelník, štít, hvězda, rozeta) a deset kovů: tvar se
  mění po deseti hodnostech, kov po pěti, takže každý tvar má chudší a bohatší
  podobu. Uvnitř je vždycky prstenec ze tří oblouků — totéž znamení jako v logu
  a v úvodní animaci — a krokve pod štítem říkají pořadí uvnitř pětice. Rozeta
  se počítá, nekreslí ručně: dvanáct stejných obloučků je přesně ta věc, u které
  se ruční `d` rozjede.
- `src/components/art/AwardArt.tsx` — dvaadvacet kreseb v poli 48×48, linka 2,6
  se zakulacenými konci a právě jedna plná plocha v barvě mety. Tvarosloví je
  ze hry: článek řetězu, buňka plástve, patra věže rozšiřující se nahoru
  (každé má o písmeno víc). Odstupňované mety sdílejí kresbu a liší se
  krokvemi, stejnou řečí jako hodnosti.

Domovská obrazovka zůstává, jaká byla — přibylo na ní tlačítko „Ocenění n/164"
a pruh denní výzvy. Všechno ostatní žije na vlastní obrazovce (`Awards.tsx`),
kde je i celý žebříček padesáti hodností. Zamčené mety se neschovávají a
u met na počet se pod dlaždicí táhne proužek postupu; schovaná meta
nemotivuje, protože o ní nikdo neví.

Co v kole padlo, oznámí `AwardPopup.tsx` až **nad** výsledkem — nejdřív skóre,
pak odměna za něj. Když padne víc věcí naráz, jdou po jedné.

### Inkoust

Ocenění a hodnosti nejsou jen odznaky: za každou padne **inkoust**
(`src/game/economy.ts`) — měna, za kterou se kupují nápovědy. Kalamář se veze
v profilu a je vidět v horní liště, protože podle něj se hráč rozhoduje, jestli
si nápovědu vzít.

Dřív se sypaly nápovědy zdarma přímo a bylo jedno, jestli si za ně hráč nechal
odhalit jedno písmeno, nebo rovnou celé slovo. Peněženka se plnila rychleji,
než se stíhala utrácet, a nápověda přestala být rozhodnutí. Teď má každá
nápověda cenu a platí pro ni jedno pravidlo přes všech šest her: **cena
v inkoustu je desetina bodové ceny téže nápovědy**. Malá vyjde na pět, odhalení
celého slova na dvacet — za totéž, co dřív koupilo čtyři celá slova, je dnes
jedno. Nová nápověda si tak cenu přinese sama a nedá se splést.

Příjem je držený nízko a **roste se stupněm žebříčku, ne s počtem met**: šest
za první stupeň, čtyřicet za pátý. Ocenění je sto čtyřiašedesát, ale drtivá
většina jich je nízko, takže za všechna dohromady padne kolem 2 500 inkoustu —
zhruba sto dvacet odhalených slov za celých pět let hraní. K tomu hodnost
(osm až dvaašedesát podle toho, jak je vysoká) a osm za **kompletní** denní
várku. Denní odměna padá až za všech šest výzev dne; šest režimů krát odměna
denně by kalamář zaplavilo rychleji než všechno ostatní dohromady.

Nápověda zaplacená inkoustem **nestojí body, ale pořád se počítá jako
nápověda**. Do `hintsUsed` se započítá stejně jako placená, jen do `freeHints`
navíc — a bodování odečítá jen rozdíl. Kolo s ní tedy není „kolo bez nápovědy"
a mety ze skupiny „Bez nápovědy" se za inkoust koupit nedají. Jinak by stačilo
nasbírat si ho a odemknout si jím právě ty mety, které mají dokazovat opak.

Starý profil se převede sám: `xp` se přejmenuje na `fame`, každá nasbíraná
nápověda zdarma se přepočte na dvanáct inkoustu.

### Denní výzva v menu

Denní výzva má vlastní pruh hned pod mřížkou her, jednu dlaždici na hru, s
označením dne a se skóre u toho, co je dneska hotové. Je to hlavní důvod, proč
se hráč vrací každý den, takže nesmí být schovaná v panelu režimu — odsud se do
ní vejde jedním ťuknutím.

## Mobil

Na telefonu se hra chová jako aplikace, ne jako dokument, a **vejde se na jednu
obrazovku**: nahoře proužek s ukazateli, uprostřed hrací plocha, pod ní
nápovědy a úplně dole ovládání s klávesnicí. Stránka jako celek se neroluje
vůbec; roluje se jedině hrací plocha, a to jen když se do své výšky nevejde.
Pro nápovědu ani pro klávesnici se tedy nikam jezdit nemusí.

Dlaždice se **dopočítávají z volného místa**, ne z pevné velikosti. Hrací
plocha je kontejner (`container-type: size`) a Řetěz i Věž si z jejích rozměrů
odvodí stranu dlaždice:

```css
--fit-h: calc((100cqh - 48px - var(--rows) * 11px) / (var(--rows) * 1.1));
--fit-w: calc((100cqw - (var(--cols) - 1) * 6px) / var(--cols));
--tile: clamp(40px, min(var(--fit-w), var(--fit-h)), 58px);
```

Počet řádků a sloupců dodá komponenta (`--rows` roste s délkou řetězu,
`--cols` je nejdelší patro věže), takže osmipísmenná věž se vejde celá
a v Řetězu je pod sebou vidět co nejvíc slov. Dolní mez 40 px je dotykový
cíl — pod ni se dlaždice nesmrskne ani na 320px displeji, tam radši žebřík
roluje. Plástev jde stejnou cestou: dostane zbylou výšku a šířku si dopočítá
z poměru stran, takže je vidět i s řádkem „piš slovo".

Postranní sloupce, které jsou na monitoru vlevo a vpravo od hrací plochy, se
na telefonu rozpadnou (`display: contents`) a jejich dvě části se zařadí nad
plochu a pod ni. Pravý sloupec je jen opis toho, co je na ploše vidět, takže
se skryje. Že to platí, hlídá `npm run play:verify` — měří, jestli spodní
hrana ovládání i nápověd zůstává nad okrajem displeje.

Česká klávesnice řeší to, že čeština má 42 písmen: základní rozložení má
nejvýš 10 kláves na řádek a písmena s diakritikou se vytáhnou **podržením**
základního písmene, stejně jako na nativní klávesnici. V rohu klávesy je náhled
varianty, aby o té možnosti hráč věděl. Ve čtyřech řadách po 11 klávesách by
na 320px displeji vyšly klávesy široké 25 px.

Rozvržení je ověřené na 320, 360, 390 a 412 px na výšku i na otočeném telefonu
(na šířku se klávesnice přesune vedle hrací plochy, ne pod ni):

```bash
npm run audit:mobile   # přetékání, dosažitelnost ovládání, velikost dotykových cílů
```

Audit hlídá dotykové cíle 44 px u běžných ovládacích prvků. Klávesy klávesnice
mají vlastní, nižší práh na šířku — nativní české klávesnice mají na 360dp
displeji klávesy kolem 34 dp a víc se jich do řady nevejde; kompenzuje se to
výškou a rozestupy.

## PWA a cesta do Google Play

Hra je plnohodnotná PWA, což je předpoklad pro zabalení do Google Play přes
**Trusted Web Activity** (např. nástrojem Bubblewrap):

- `public/manifest.webmanifest` — standalone režim, zámek na výšku, kategorie,
  zkratky na jednotlivé režimy,
- ikony 192 a 512 px včetně **maskable** variant (bez nich Android ořízne
  obsah ikony do svého tvaru) — generuje `npm run build:icons`,
- service worker s předuloženou skořápkou; datové balíčky se ukládají až při
  prvním použití, protože jich jsou megabajty a hráč potřebuje jen část.

```bash
npm run audit:pwa   # manifest, ikony, registrace workeru a skutečný běh offline
```

Pro TWA ještě bude potřeba nasadit hru na vlastní doménu přes HTTPS a přidat
`.well-known/assetlinks.json` s otiskem podpisového klíče — teprve to Androidu
řekne, že aplikace a doména patří k sobě, a schová adresní řádek.

## Původ dat

Slovníková data pocházejí z projektů
[hermitdave/FrequencyWords](https://github.com/hermitdave/FrequencyWords) a
[LibreOffice/dictionaries](https://github.com/LibreOffice/dictionaries)
a řídí se licencemi svých původních projektů.

Texty o původu slov v režimu **Detektiv** pocházejí z české sekce
[Wikislovníku](https://cs.wiktionary.org) a jsou pod licencí
[CC BY-SA](https://creativecommons.org/licenses/by-sa/4.0/deed.cs). Nejsou
psané mnou ani vygenerované — skript `tools/5c_fetch_etymology.py` je jen
stáhne přes API, očistí od wikitextu a uloží do cache; `5d_build_detective.py`
z nich pak vybírá a maskuje výskyty hledaného slova. Etymologie je obor, kde se
chyba nepozná, takže si hra netroufá tvrdit nic vlastního.

Sběr je šetrný: padesát hesel na jeden dotaz, pauza mezi dávkami, popisná
hlavička User-Agent a cache, díky které se stejné heslo nestahuje dvakrát.
