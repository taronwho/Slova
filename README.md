# Slova

Tři české slovní hry v jedné webové aplikaci. Běží čistě staticky, bez serveru,
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

### Věž — anagramová věž
Od tří písmen nahoru. V každém patře přibude jedno písmeno a hráč ze **všech**
dostupných písmen složí nové slovo v libovolném pořadí.

Právě povinnost použít všechna písmena dává věži nejsilnější možnou garanci:
každé platné řešení patra má nutně stejný podpis, takže volba konkrétního slova
nemůže zablokovat cestu nahoru. Řetěz podpisů je ověřený už při generování.

## Data

| | zdroj | výsledek |
|---|---|---|
| Slovník | frekvenční seznam češtiny profiltrovaný přes hunspell `cs_CZ` | 248 181 ověřených slov |
| Základní tvary | hesla hunspellu + lemmatizace (LemmaGen3) | 40 519 slov |
| 1. pád množného čísla | buňky deklinačních vzorů z `cs_CZ.aff` | + 7 693 slov |
| Řetěz | grafy pro délky 4, 5 a 6 | 7 841 hádanek |
| Voština | plástve odvozené od pangramů | 2 400 hádanek |
| Věž | ověřené řetězy přesmyček 3→6/7/8 | 2 245 hádanek |

### Jen 1. pád a infinitiv

Hra pracuje výhradně se základními tvary: podstatná jména v 1. pádu (jednotné
i množné číslo), slovesa v infinitivu, přídavná jména, číslovky, zájmena,
příslovce a spojky. Bez toho hráč ve Voštině sbíral varianty jednoho slova
(„hravá, hravé, hravě, hrává") místo aby hledal nová.

Slovník vzniká ve dvou krocích.

**1. Základní tvar** (`tools/2b_base_forms.py`). Slovo projde, jen když splní
obě podmínky:

1. **Hunspell ho přečte bez jediné přípony a předpony** — je to tedy přímo
   heslo slovníku, ne odvozený tvar. Analýza není odhad: hunspell u každého
   slova řekne, z jakého hesla a jakým příznakem ho odvodil (`agente ← agent`
   příponou P, `nemíříš ← mířit` příponou A a předponou N, `tang ← tango`
   příponou Q).
2. **Lemma se rovná slovu.** Heslo samo nestačí, český hunspell má jako hesla
   i ohýbané tvary („boha", „bohu", „bohů"). Odchytí je **LemmaGen3**.
   `simplemma` jsem zkoušel taky, ale pro češtinu je nepoužitelná —
   lemmatizuje „dobrý" na „dokonavý" a „dělat" na „udělat".

Dřívější verze stála na ručních pravidlech nad koncovkami a porovnávání
frekvencí. Vždycky něco proklouzlo: „tang" je jen 2× vzácnější než „tango",
zatímco zcela legitimní „lít" je 498× vzácnější než „líto". Pozitivní kritérium
(je to heslo?) je proti tomu ostré.

Cenou je příznak `R`, kterým hunspell tvoří odvozená příslovce („dobře ←
dobrý") *i* 6. pád („roce ← rok", „autě ← auto"). Rozlišit je nejde, takže se
nepouští ani jedno — hra tím přichází o „dobře" a „rychle", ale nepustí do sebe
pádový tvar.

**2. Množné číslo** (`tools/2c_plural.py`). Příznaky v `cs_CZ.aff` fungují jako
deklinační vzory: jeden příznak = jedno paradigma a v něm sada přípon
s podmínkami. Buňka „1. pád množného čísla" se tedy dá určit přesně, ne
odhadem — je to konkrétní příponové pravidlo:

```
SFX H   0   y   [^ey]      hrad  -> hrady
SFX Z   a   y   [^…]a      žena  -> ženy
SFX M   o   a   [^c]o      město -> města
SFX I   ch  ši  ch         hoch  -> hoši
```

Vybrané buňky jsou vypsané v `tools/_plural_rules.py` (vzory H, L, S, U, D, I,
V, Z, K, M) a skript `2c_plural.py --vzorek` u každé z nich ukáže vzorek
vygenerovaných dvojic ke kontrole. Nepoužívá se `Q` (2. pád mn. č. — „služba →
služeb", „tango → tang"), `P` (mužský vzor bez vlastního 1. pádu mn. č.), `R`,
`Y` ani slovesné příznaky.

Dvě pojistky navíc: příznaky `I`, `V` a `D` hunspell věší i na číslovky
(„deset → deseti") a slovesa, takže se berou jen ve společnosti některého
jmenného vzoru; a každý vygenerovaný tvar musí být v ověřeném lexikonu
a lemmatizér ho musí vrátit zpátky na výchozí heslo.

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

```
npm test          # 57 testů: herní logika + validace všech dat
npm run smoke     # průchod všemi třemi režimy v Chromiu, včetně mobilu
```

## Spuštění

```bash
npm install
npm run dev       # vývojový server
npm run build     # typecheck + produkční build do dist/
npm run preview   # náhled produkčního buildu
```

Aplikace nepotřebuje žádný backend — `dist/` se dá nasadit na jakýkoli statický
hosting. Postup hráče se ukládá do `localStorage`.

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

## Mobil

Na telefonu se hra chová jako aplikace, ne jako dokument: hlavička drží nahoře,
hrací plocha roluje uvnitř a ovládání s klávesnicí je přišpendlené dole, takže
nikdy neskončí pod okrajem displeje. Po každém tahu se plocha sama doroluje
k rozepsanému slovu.

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
