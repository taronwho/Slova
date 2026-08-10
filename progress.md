# 80 nových střech do Vetřelce (střední + těžká)

Cíl: 80 nových **skrytých** rodin — pětice, kde na první pohled nemají slova
nic společného. Data se nepíšou ručně do souboru, ale generuje je skript
`tools/gen_families7.py`, který zapisuje `tools/intruder_families7.py`.

Co skript dělá navíc proti ručnímu psaní:

* **Mechanické rodiny** (pravidlo o písmenech) si slova **najde sám** ve
  slovníku hry a ověří pravidlo slovo po slovu — dovnitř i ven.
* **Slova vně** bere z nudné zásoby a automaticky z ní vyhazuje všechno, co
  leží uvnitř kterékoli rodiny — ani jedné z osmdesáti.
* **Zavádějící věty** vybírá z banky a ty, které jde ověřit strojem
  (palindrom, bez samohlásky, zdvojená písmena, schované zvíře…), ověří:
  věta nesmí platit ani pro jedno slovo v rodině, jinak by mohla vydělit
  vetřelce sama.
* Hlídá, že první otázka je napříč všemi rodinami **jedinečná** (je to klíč
  rodiny) a že sedí do věty „Čtyři z nich …".

## Stav

| dávka | rodin | stav |
|---|---|---|
| 1 — mechanické (písmena a tvar slova) | 18 | **hotovo** |
| 2 — slovo je zároveň něco jiného, I. | 20 | **hotovo** |
| 3 — slovo je zároveň něco jiného, II. | 12 | **hotovo** |
| 4 — slovo je v názvu (populární) | 14 | **hotovo** |
| 5 — slovo je v názvu (znalostní) | 16 | **hotovo** |

Hotovo: **80 / 80**

## Plán

### Dávka 1 — mechanické (skript si slova najde a ověří)

| # | id | úroveň | osa |
|---|---|---|---|
| 1 | mech-abecedni-poradi | střední | písmena jdou v abecedním pořadí |
| 2 | mech-stejne-kraje | střední | začínají i končí stejným písmenem |
| 3 | mech-skryte-cislo | střední | schované číslo (sto, tři, pět, osm…) |
| 4 | mech-skryte-telo | střední | schovaná část těla (oko, nos, ruka…) |
| 5 | mech-stejna-samohlaska | střední | ve všech slabikách táž samohláska |
| 6 | mech-samohlaska-kraje | střední | začínají i končí samohláskou |
| 7 | mech-tri-souhlasky | střední | tři souhlásky za sebou |
| 8 | mech-dvojhlaska | střední | mají v sobě ou, au nebo eu |
| 9 | mech-dvakrat-dvojice | střední | táž dvojice písmen dvakrát |
| 10 | mech-vzacne-pismeno | střední | písmeno f, g, x nebo w |
| 11 | mech-vic-samohlasek | střední | víc samohlásek než souhlásek |
| 12 | mech-ruzne-samohlasky | střední | každá samohláska jiná |
| 13 | mech-dve-slova | těžká | dají se rozdělit na dvě jiná slova |
| 14 | mech-prvni-pulka | těžká | písmena jen z první poloviny abecedy |
| 15 | mech-leva-ruka | těžká | dají se napsat jen levou rukou |
| 16 | mech-bez-opakovani | těžká | sedm písmen a žádné se neopakuje |
| 17 | mech-sousedni-pismena | těžká | dvě písmena, co jdou v abecedě po sobě |
| 18 | mech-rimske-cislo | těžká | jen písmena římských číslic |
| 19 | mech-skryty-stat | těžká | schované jméno státu |

### Dávka 2 — slovo je zároveň něco jiného, I.

metro, měny, řecká písmena, ostrovy, karetní hry, časopisy, hudební skupiny,
hokejové kluby, motorky, sýry, tance, sladkosti, mluvnické pojmy, divadelní
pojmy, části ucha a oka, počítačové pojmy, fotbalové pojmy, hory, větry,
pražská divadla

### Dávka 3 — slovo je zároveň něco jiného, II.

nakladatelství, knihtisk, stavba domu, hudební značky, skladatelé, pražské
parky, anglická slova, součásti kola, části boty, okno a dveře, části houslí

### Dávka 4 — slovo je v názvu (populární)

Harry Potter, Pán prstenů, Star Wars, Disney, Andersen, Grimm, Lindgrenová,
dětské písničky, české komedie, světové filmy, seriály, Gott, řecké báje,
Dumas

### Dávka 5 — slovo je v názvu (znalostní)

Foglar, Verne, Neruda, Jirásek, Němcová, Smetanovy opery, Dvořák a Janáček,
Hitchcock, Svěrák, muzikály, Kryl, Nohavica, Werich, Ota Pavel, Nezval
a Seifert, Sherlock Holmes

## Deník

**Dávka 1 — 18 mechanických rodin.** Původní plán měl 19, jedna se počítala
dvakrát; chybějící rodina se dobere v dalších dávkách, celek zůstává 80.

Co se cestou ukázalo a co s tím skript dělá:

* **Schované slovo se musí hledat i s háčky.** Napřed skript srovnával slova
  bez diakritiky, a tak mu jako „slovo se schovanou trojkou" prošlo
  *povětří* („tří", ne „tři") a *sestra* („sest", ne „šest"). Hráč by po
  vyhodnocení hledal, kde tam jaká trojka je. Teď se hledá v slově tak, jak
  se píše.
* **Slovo, které tím hledaným samo je, se nepočítá** — *dlaň* mezi slovy se
  schovanou částí těla nic neschovává, jen prozrazuje osu.
* **Vetřelec nesmí trčet délkou.** Rodiny s pravidlem o písmenech mají slova
  krátká (*los, kos, most*) a skript k nim napřed sázel *prostěradlo*. Slova
  vně se teď vybírají v délce, kterou má čtveřice.
* Ruční brzda `ban` na slova, která pravidlem projdou, ale osu prozradí:
  *pětky, osmnáctka, sedmikráska* mezi slovy se schovaným číslem.

**Dávka 2 — 20 rodin „slovo je zároveň něco jiného".** Metro, měny, řecká
písmena, ostrovy, karetní hry, časopisy, kapely, hokejové kluby, motorky,
sýry, tance, sladkosti, mluvnice, divadlo, části ucha a oka, počítačové
pojmy, fotbal (střední); hory, větry, pražská divadla (těžká).

Pravidlo pro slova uvnitř: **každé musí být samo o sobě všední**. Kdyby mezi
stanicemi metra stálo Kobylisy nebo mezi ostrovy Sumatra, pozná hráč osu
podle jediného slova. Proto anděl, muzeum, můstek — a malta, java, kuba.

* Do vaty se dostávala slova, která do rodiny patřila: *branka* mezi
  fotbalovými pojmy. Na to je ruční seznam `avoid` — stroj to nepozná.
* Vata se zároveň pročistila. Byla v ní slova jako *tesařina* nebo *mopík*,
  a vzácné slovo mezi čtyřmi běžnými trčí i bez znalosti osy: hráč vetřelce
  pozná podle toho, že o něm nikdy neslyšel.

**Dávka 3 — 12 rodin.** Nakladatelství, knihtisk, stavba domu, značky
v notách, skladatelé, pražské parky, česká slova, která jsou zároveň
anglická, součásti kola, části boty, okno a dveře, části houslí. Plus
devatenáctá mechanická rodina místo té, která se v plánu počítala dvakrát:
**slova s jedinou samohláskou** (*srdce, prsten, vlak, stůl*).

* Zkoušel jsem rodinu „slova, ve kterých se schovává jméno českého města",
  ale padla: *Aš* se schovává skoro všude (*naše, kaše, flaška*) a zbytek
  měst se ve slovech nevyskytuje. Skript to ukázal na počtu nalezených slov,
  ne až hráč.
* Padla i rodina „slova, která se dají rozdělit na dvě jiná slova": čeština
  není němčina, ve slovníku hry se takové slovo našlo **jedno** (televize).

**Dávky 4 a 5 — 30 rodin „slovo stojí v názvu".** Harry Potter, Pán prstenů,
Star Wars, disneyovky, Andersen, Grimmové, Lindgrenová, dětské písničky,
české komedie, světové filmy, seriály, Gott, antická rčení, Dumas (střední);
Foglar, Verne, Neruda, Jirásek, Němcová, Smetanovy opery, Dvořák a Janáček,
Hitchcock, Svěrák, muzikály, Kryl, Nohavica, Werich, Ota Pavel, Nezval
a Seifert, Sherlock Holmes (těžká).

Tenhle druh rodiny je ze všech nejvydatnější: v názvu knihy může stát
cokoli, od *celeru* po *koloběžku*, takže pětice vypadá jako náhodná hromada
i tomu, kdo všechny ty knihy četl. Souvislost se hledá po paměti, ne podle
významu — a přesně to má Vetřelec dávat.

## Hotovo

* 80 rodin vygenerováno a zapojeno do sady. Střední má nově **56 rodin**,
  těžká **52**; nejčastější rodina zabírá 1,8 % své obtížnosti (dřív 8,3 %).
* Rozpočet střední a těžké se zvedl (1400 a 1300 pětic), aby na rodinu
  vyšlo pětadvacet hádanek a ne čtrnáct. Sada má 3840 pětic.
* Ve stavěči sady přibyla brzda na dvě slova z jednoho kořene v jedné pětici
  (*malina* a *malinovka*) a v testech dvě nová tvrzení: kořeny a rámec věty
  do vyhodnocení.
