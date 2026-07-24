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
| Slovník | frekvenční seznam češtiny profiltrovaný přes hunspell `cs_CZ` | 248 811 ověřených slov |
| Řetěz | grafy pro délky 4, 5 a 6 | 8 879 hádanek |
| Voština | plástve odvozené od pangramů | 2 400 hádanek |
| Věž | ověřené řetězy přesmyček 3→6/7/8 | 2 700 hádanek |

Hunspell zároveň spolehlivě odfiltruje vlastní jména: ta jsou ve slovníku
uložena jen s velkým počátečním písmenem, takže lookup malé varianty („praha",
„brno") selže. Navíc se uplatňuje blocklist vulgarismů a hanlivých výrazů.

Do prohlížeče se posílají jen malé balíčky podle potřeby; graf sousednosti pro
Řetěz si klient staví sám ze seznamu slov (wildcard kbelíky, O(n·délka)), takže
se žádná předpočítaná struktura přenášet nemusí.

## Jak je řešitelnost doložená

Testy v `tests/data.test.ts` projdou **každou** hádanku, která by se dostala ke
hráči, a ověří:

- **Řetěz** — start i cíl jsou ve slovníku, uložený par se rovná skutečné
  nejkratší vzdálenosti spočítané BFS, a rekonstruovaná cesta se v každém kroku
  liší přesně o jedno písmeno bez opakování slov.
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

Světlé i tmavé téma (podle systému nebo ručně), typografie Outfit + Inter,
responzivní od 320 px výš, animace respektují `prefers-reduced-motion`.
Na mobilu je k dispozici česká virtuální klávesnice QWERTZ s řádkem diakritiky.

## Původ dat

Slovníková data pocházejí z projektů
[hermitdave/FrequencyWords](https://github.com/hermitdave/FrequencyWords) a
[LibreOffice/dictionaries](https://github.com/LibreOffice/dictionaries)
a řídí se licencemi svých původních projektů.
