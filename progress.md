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
| 14 | mech-prvni-pulka | těžká | písmena jen z první poloviny abecedy |
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

* 80 rodin vygenerováno a zapojeno do sady. Střední má nově **57 rodin**,
  těžká **51**; nejčastější rodina zabírá 2 % své obtížnosti (dřív 8,3 %).
* Rozpočet střední a těžké se zvedl (1400 a 1300 pětic), aby na rodinu
  vyšlo pětadvacet hádanek a ne čtrnáct. Sada má 3793 pětic.
* Ve stavěči sady přibyla brzda na dvě slova z jednoho kořene v jedné pětici
  (*malina* a *malinovka*) a v testech dvě nová tvrzení: kořeny a rámec věty
  do vyhodnocení.

## Opravy po prvním hraní

Hráč nahlásil tři věci a všechny tři měly stejný charakter: hádanka byla
formálně správná, ale nehrála se dobře. Každou opravu drží od téhle chvíle
skript, ne pozornost.

**1. Pětice se dvěma řešeními.** *labuť, plachty, srnec, orel, had* — osa
„čtyři z nich jsou souhvězdí" ukazuje na *srnce*, jenže zbylá čtyři slova
jsou zvířata a ukazují na *plachty*. Kdy to nastane, se dá spočítat: vadí
právě ten případ, kdy škatulku sdílí čtyři slova a **jedno z nich je
vetřelec**. Když ji sdílí všech pět, nikoho nevyděluje; když ji sdílí ta
čtveřice zevnitř, vydělí téhož vetřelce jako osa. Škatulky (zvíře, rostlina)
jsou v `tools/word_tags.py` a rodiny, které je mají přímo ve střeše
(„savci", „ptáci", „stromy"), si je **doplní samy** — ručně psaný seznam
nemůže být úplný a hned to bylo vidět: chyběl v něm *upír*.

**2. Totéž schované dvakrát.** *peruť, román, malinovka, maximalista* —
*malinovka* i *maximalista* nesou Mali. Generátor si u každého slova
zapamatuje, co v něm vlastně vězí, a stavěč sady nepustí do jedné pětice dvě
slova s touž násadou. Doplněno i starším rodinám (*rakev* a *raketa* nesou
obě raka, *sobota* a *osoba* soba).

**3. Pravidlo, které si hráč nemůže ověřit.** „Čtyři z nich se dají napsat
jen levou rukou na české klávesnici" — na telefonu klávesnici nikdo před
sebou nemá a rozdělení QWERTZ na půlky není vidět. Rodina šla pryč a
nahradila ji **Tisíc a jedna noc** (*lampa, koberec, sezam, jeskyně,
loupežník, duch*), kde stačí příběh znát.

Do testů přibyla dvě tvrzení nad hotovou sadou: žádná pětice se dvěma
řešeními a žádná pětice, kde se totéž schovává dvakrát.

Cestou se ukázalo ještě jedno: rodina „čtyři z nich umí aktivně létat" měla
uvnitř *netopýra*, *netopýra velkého* a *netopýra rezavého*, takže se čtyři
různá slova z ní nedala vybrat a rodina nevydala **ani jednu** pětici. Teď
má čtyři různé druhy (netopýr, kaloň, vrápenec, upír).

# Osmá várka — 50 rodin, pět nových druhů osy

Padesát dalších rodin téhož ražení by sadu nafouklo, ale hru by nezměnilo:
hráč by pořád hledal jednu ze tří věcí (pravidlo o písmenech, druhý význam,
název) a čtvrté kolo by se hrálo jako první. Tahle várka proto přidává
**nové druhy souvislosti**, ne jen další slova.

Generátor: `tools/gen_families8.py` → `tools/intruder_families8.py`.
Kontroly si bere ze sedmé várky, takže se nedublují.

| skupina | rodin | příklad |
|---|---|---|
| fyzikální vlastnost | 12 | *korek, dřevo, led, olej, **kámen*** — čtyři plavou |
| praktické použití | 8 | vejdou se do kapsy, teče z nich voda, potřebují dva lidi |
| mluvnice | 7 | jen v množném čísle, nesklonná, po odtržení předpony zbude slovo |
| ustálená spojení | 4 | zlatý déšť, zlatá horečka, zlaté ručičky, zlatý řez |
| text, který zná každý | 3 | česká hymna, přísloví, pranostiky |
| nové obory druhého významu | 6 | části kostela, včelařství, šití, rybaření, rybníky |
| další vlastnosti věcí | 10 | rozbijí se pádem, mají pružinu, věší se na hřebík |

Dvě věci se u nových typů dělají jinak:

* **Slova vně se nedají brát z nudné zásoby.** U rodiny „čtyři z nich
  plavou" musí být vetřelec věc, která se **jistě potopí** — kdyby tam stál
  deštník, hráč netuší, jak to s ním je, a hádanka se rozpadne na dohady.
  Skoro každá rodina má proto vlastní seznam vetřelců.
* **Past se staví schválně.** Mezi vetřelce u „vydávají vlastní světlo"
  patří *měsíc*, u „neskloňují se" *kino* a *metro*. Vypadají, že do
  čtveřice patří, a hra se láme přesně na nich.

## Stav po osmé várce

* Sada má **4383 pětic** a 158 rodin: lehká 84, střední **85**, těžká **73**.
* Nejčastější rodina zabírá 1,4 % své obtížnosti (před šestou várkou 8,3 %).
* Rozpočet střední a těžké zvednut na 1700 a 1600 pětic, aby na rodinu
  vyšlo dvacet hádanek a ne deset.
* `npm test` (201), `smoke`, `smoke:standalone`, `audit:mobile`,
  `audit:pwa`, `play:verify` — vše prošlo.

# Devátá várka — 100 rodin, a pokaždé jiná povaha osy

Generátor: `tools/gen_families9.py` → `tools/intruder_families9.py`.
Kontroly si bere ze sedmé várky, takže se nedublují.

| skupina | rodin | příklad |
|---|---|---|
| vlastnosti věcí a přírody | 15 | *voda, olej, rtuť, líh, **vosk*** — čtyři jsou tekuté |
| praktické použití | 2 | zamknout na klíč, autolékárnička |
| zeměpis | 4 | leží na Moravě, krajská města, Rakousko-Uhersko, UNESCO |
| mluvnice a pravopis | 4 | nepravidelné množné číslo, přesmyčky, dva druhy rýmu |
| ustálená spojení | 6 | bílá vrána, suchý humor, hluboký talíř, Tichý oceán |
| obory s vlastní řečí | 46 | film, právo, tělocvik, pivovar, jeskyně, tkalcovství, kosti |
| další prameny názvů | 14 | Malý princ, Alenka, Narnie, Poe, Wells, pražské pověsti |
| ještě vlastnosti věcí | 9 | mají rub a líc, patří na kompost, musí se naostřit |

## Co se při kontrole ukázalo

Sto rodin se nedá odbýt čtením; každou jsem si nechal vypsat i se slovy
vně a prošel je. Nálezy:

* **Torzo jména není slovo.** Kalendářní rodiny („čtyři z nich připadají
  každý rok na jiné datum") by do pětice postavily *Velký* nebo *Bílá* —
  půlku názvu *Velký pátek*. Rodiny padly a nahradily je vlastnosti.
  Ze stejného důvodu vypadly *Karlovy*, *Ústí* a *Kutná* z měst.
* **Vetřelec nesmí platit taky.** *Lampa* je přesmyčka slova *palma*, takže
  v rodině o přesmyčkách nemohla stát vně. *Sud vína amontilladského* je
  povídka od Poea, *Mojžíš* pluje v koši, *Alenka* proleze do zahrady
  a v Narnii stojí hned za skříní **lampa** — všechna tahle nudná slova
  musela z vetřelců pryč.
* **Nudné slovo bývá odborný pojem.** *Lopatka* je kost, *matice* je
  matematický pojem, *hřeben* je část hory, *police* je knihovnický pojem,
  *pekáč* a *trouba* patří do pekárny. Na to je seznam `avoid`.
* **Vata se vzorkuje.** Sto vetřelců na rodinu se nedá při kontrole
  přečíst — a číst se musí, protože zrovna tyhle chyby stroj nepozná.
  Bere se patnáct.

## Stav po deváté várce

* Sada má **4730 pětic** a 342 rodin: lehká 84, střední **145**, těžká
  **113**. Nejčastější rodina zabírá 0,7 % střední a 0,9 % těžké.
* Rozpočet střední a těžké zvednut na 2000 a 1800 pětic.
* Strojová kontrola nad hotovou sadou: žádná pětice se dvěma řešeními,
  žádná se dvěma slovy z jednoho kořene, žádná s toutéž schovanou věcí
  dvakrát, žádná rozbitá věta do vyhodnocení.
* `npm test` (201), `smoke`, `smoke:standalone`, `audit:pwa`,
  `play:verify` — vše prošlo; šest kol odehráno v prohlížeči.

# Návrat do rozehraného kola

Hráč nahlásil, že se u Citátu po odchodu do menu vrací na začátek, a chtěl
projít celou hru. Prošel jsem ji a našly se čtyři věci.

**1. Citát a Vetřelec se neobnovovaly vůbec.** Překlad uloženého stavu zpátky
na hádanku byl řada `else if` s koncovým `else`, který všechno ostatní
považoval za Věž. Obě hry přibyly později, spadly do něj a hráč začínal
znovu. Teď je to čistá funkce (`src/app/resume.ts`) a test prochází režim po
režimu — nová hra se do ní musí zapsat, jinak neprojde.

**2. Denní dlaždice začínala vždycky znovu.** Kdo si v půlce výzvy odskočil
a dlaždici ťukl podruhé, přišel o postup i o čas. Rozehraná dnešní výzva se
teď otevře tam, kde skončila, a na dlaždici je vidět, kolik má hráč za sebou.
Volná hra z panelu si dál začíná od začátku — „Pokračovat" tam má vlastní
tlačítko a hráč si vybírá.

**3. Denní výzva přepisovala volnou hru téže hry.** Kolo se ukládalo jen
podle režimu, takže rozehraný volný Řetěz zmizel ve chvíli, kdy hráč ťukl na
dnešní výzvu Řetězu. Nově má každá hra dvě přihrádky (`hive`, `hive:denni`)
a kola se nepřepisují. Kola uložená starší verzí se při načtení přesypou do
té správné.

**4. Otázka dne se neukládala vůbec.** Sázka na počet indicií je nevratná
a otázka je jedna denně — návrat na začátek by hráče připravil o celý den.
Ukládá se teď stejně jako hry, jen stranou: otázka není režim, nemá obtížnost
ani hádanku ze sady.

**A hodiny.** Čas kolu běžel i mimo hru (skóre se počítá z času uloženého ve
stavu), ale lišta po návratu ukazovala nulu — hráč tedy nevěděl, že o bonus
za rychlost přišel. Teď navazuje: měří se od chvíle, kdy kolo **začalo**.
Sekundy se navíc dopočítávají z času, ne přičítáním, protože prohlížeč na
pozadí intervaly zpomaluje a sčítaný počet se rozejde.

Denní kolo rozehrané včera a otevřené dnes se za dnešní výzvu nepočítá:
hádanka je včerejší a v přehledu ani v souboji by neseděla. Dlaždice proto
začne dnešní výzvu načisto.

## Čím je to hlídané

* `npm test` — obnova všech osmi režimů, přihrádky, přesyp starých kol.
* `npm run audit:resume` (nové) — v prohlížeči: odchod a návrat u každé hry,
  volná hra vedle denní výzvy, Otázka dne, běžící čas, včerejší výzva.

---

# Sto položek do každé z devíti her

Zadání znělo přidat do každé hry sto otázek, rodin, citátů — podle toho, co
která hra vlastně rozdává. To je devět různých úloh, protože každá hra bere
data odjinud.

| hra | bylo | je | odkud |
|---|---|---|---|
| Řetěz | 7824 | 7927 | vyšší strop v `3_build_chain.py` |
| Voština | 2400 | 2502 | `TARGET_HIVES` |
| Věž | 1962 | 2068 | `TOWERS_PER_DIFFICULTY` |
| Šibenice | 2100 | 2200 | `BANDS` |
| Detektiv | 3000 | 3100 | `CAP` |
| Slabiky | 9037 slov | 9213 slov | `DEAL_POOL` 350 → 358 |
| Citát | 2672 | 2835 | čerstvý dump + širší meze délky |
| Vetřelec | 335 rodin | 435 rodin | `tools/gen_families10.py` |
| Otázka dne | 1250 | 1350 | `tools/quiz_bank.py` |

## Hry ze slovníku

Šest her si data staví ze staženého korpusu. U nich nejde „dopsat sto
kousků" — jde jen povolit, aby jich stavitel vzal víc. To má háček: čísla
nejsou libovolná, protože se dělí mezi obtížnosti nebo mezi hodnoty par.
Kdyby se strop nastavil na kulaté číslo, posledních pár hádanek by se do
sady nedostalo, protože kvóta je celočíselný podíl.

Šestipísmenná úroveň Řetězu svůj strop nevyčerpává a nevyčerpá ho ani teď:
koncových kandidátů je jen sto třicet osm a všechny jejich dvojice v rozsahu
par se do hry berou tak jako tak. Stovku proto nesou čtyřky a pětky. Podobně
u Věže: strop platí na každou obtížnost zvlášť, ale vyčerpat se dá jen ta
nejlehčí — u střední a těžké dojdou dřív podpisy s úplným řetězem.

U Slabik se nepřidávaly hádanky, ale slova, ze kterých hra pozná, co je
platný tvar. Osm slabik navíc v rozdávacím poolu přineslo skoro dvě stě slov
a na hustotu desky to znát není: přibyly na konci pořadí podle četnosti,
takže mají nejmenší váhu a padají nejvzácněji.

U Citátu nestačilo stáhnout čerstvý dump — od posledního přibyly dva výroky.
Povolilo se proto jedno slovo a osm znaků navíc (5–15 slov, 30–118 znaků),
protože právě kolem téhle hranice jich leží nejvíc. Nejdelší citát zabere na
displeji 320 × 568 sedm řádků a 210 px; věta se sází přetékajícím řádkem,
takže se nic neuřízne.

Detektiv se staví **až po** Otázce dne: slova, na která se ptá kvíz, se
detektivkám zapovídají, aby hráč neluštil ráno v kvízu totéž co odpoledne
v detektivce. Sto nových otázek proto zvedlo počet zahozených hesel.

## Otázka dne

Deset otázek do každého z deseti oborů — jinak to nešlo. Obory se hráči
podávají kolečkem a délka toho nejmenšího určuje, za kolik dní se otázka
zopakuje; kdyby se jeden obor rozešel, zkrátil by cyklus celé hry. Teď je
všech deset po sto pětatřiceti, tedy 1350 dní bez opakování.

Build hlásil jediný nález: druhá indicie u turbodmychadla prozrazovala
odpověď slovem *turbínou* — kontrola porovnává přes kmen, takže si všimla
i toho, že *turbo* je uznávaná odpověď. A jedno upozornění navíc: indicie
u Marathónu ukazovala zájmenem na odpověď, která je spojením dvou jmen.
Obojí přepsáno.

## Vetřelec

Sto nových rodin, opět skript (`tools/gen_families10.py`), ne ruční seznam.
Osy jsou schválně z různých soudků:

* **tělo u věcí** — ucho hrnce, zuby pily, jazyk boty, oko sítě; slovo zná
  každý, ale že je to jedna a tatáž věc, dojde až po chvíli,
* **ustálená spojení** — těžký, horký, slepý, mrtvý, šedý, tvrdý,
* **řemesla** — kovárna, hasiči, truhlárna, hornictví, mlékárna, filatelie,
  účetnictví, pojišťovna, elektro, lukostřelba, šerm,
* **části věcí** — květ, zub, houba, kytara, kamna, most, kniha, střecha,
  schodiště, košile, vodovod, zámek, koňský vůz,
* **písmena** — slabikotvorné r, koncovka -tel, háčky, kroužek, useknuté
  první písmeno,
* **příroda podle chování** — co táhne na zimu, co spí zimní spánek, co
  svléká kůži, co kvete před olistěním, co žije na cizí úkor,
* **prameny názvů** — May, Havel, Kundera, Zeman, Chaplin, Dickens, Mucha,
  Menzel, Štorch,
* **vlastnosti a děje** — co saje vodu, co ji odpuzuje, co hasí oheň, co
  uletí ve větru, co svítí jen odraženým světlem.

### Co při psaní spadlo

**Slova vně musí být ze stejného soudku jako slova uvnitř.** U tažných ptáků
stojí vně ptáci stálí, u jedovatých rostlin rostliny neškodné, u zapalovaných
světel světla elektrická. Bez toho by osa sklouzla na „čtyři jsou ptáci"
a hádanka by měla dvě řešení.

**Jasan kvete taky před olistěním.** Byl mezi vetřelci u rodiny o dřevinách,
které kvetou dřív, než jim narostou listy — jako odpověď by byl stejně dobrý
jako slova uvnitř. Totéž javor mléč. Oba pryč; vně zůstaly lípa, dub, buk.

**Luk není část kytary.** Patří ke smyčcovým nástrojům.

**Příklonka.** Otázka se sází do rámce „Čtyři z nich …", takže sloveso je ve
větě až třetí a zvratné *se* se musí přesunout před ně: „Čtyři z nich **se**
sbírají v lese", ne „sbírají se v lese". Sdílená kontrola to nechytí, protože
hlídá jen podobu otázky samotné, a ta zní správně obojím způsobem. Přibyla
proto vlastní kontrola — s výjimkou pro „tvoří **se slovem** ostrý ustálené
spojení", kde *se* není příklonka, ale předložka.

**Dvakrát podmět.** „Čtyři z nich vyroste **z nich** rostlina." Rámec podmět
už říká, takže druhý odkaz je navíc. Hlídá se to teď taky.

### Co hlídá stroj

Rodiny s pravidlem o písmenech ověřuje skript na obě strany naráz: každé
slovo uvnitř pravidlu vyhovět **musí** a žádné slovo vně mu vyhovět **nesmí**.
Jedno pravidlo je zdroj pravdy pro obojí, takže se nedají omylem rozejít.
U rodiny „po useknutí prvního písmene dají jiné slovo" se navíc sahá do
slovníku hry — `sval` se tak neudržel, protože *val* v základních tvarech
není.

Ke stávajícím kontrolám (jedinečná otázka, rámec věty, žádná pětice se dvěma
řešeními, žádné dvě slova se stejným kmenem, žádná schovaná věc dvakrát)
přibylo ještě hlášení, když slovo stojí uvnitř i vně téže rodiny.

## Čím je to hlídané

* `npm test` — 209 testů, z toho datové na všech devět sad.
* `npm run smoke`, `smoke:standalone`, `play:verify` — 199 zkontrolovaných
  slov v odehraných kolech.
* `npm run audit:pwa`, `audit:mobile`, `audit:resume` — bez nálezů.

---

# Pět set otázek a dvě stě rodin navíc

Otázka dne vyrostla z 1350 na **1850**, Vetřelec z 435 rodin na **635**.

## Otázka dne

Padesát otázek do každého z deseti oborů, v pěti várkách po stovce. Rovnoměrně
to být muselo: obory se hráči podávají kolečkem a nejmenší z nich určuje, za
kolik dní se otázka zopakuje. Teď je všech deset po sto pětaosmdesáti, tedy
**1850 dní bez opakování** — přes pět let denního hraní.

Kontrola na únik odpovědi hlásila v každé várce deset až dvacet nálezů a
všechny byly opravdové. Nejčastěji šlo o tři věci:

* **Alternativní tvar odpovědi**, na který autor při psaní indicií nemyslel.
  U vokativu je uznávaná odpověď „pátý pád" — a druhá indicie začínala slovy
  „Pátý pád, tvar, kterým…". U turbodmychadla prozradilo odpověď slovo
  *turbínou*, protože *turbo* je taky uznávané.
* **Obecné slovo, které se u téhle odpovědi obecné být přestalo.** U rodin
  jazyků („slovanské jazyky", „germánské jazyky") se nedalo napsat „skupina
  indoevropských **jazyků**". Do seznamu druhových slov proto přibylo
  `jazyky` a `jazyku`: nadpis otázky to slovo stejně říká nahlas.
* **Kmen kratší, než se zdá.** Kontrola porovnává přes hrubý kmen, takže
  *Nigérie* se schová i v *Nigeru*, *svatého* v *svátku* a *teplo*
  v *teploměru*. Tyhle nálezy vypadají jako plané, ale nejsou: hráč vidí
  totéž, co stroj.

## Vetřelec

Dvě stě rodin ve dvou skriptech (`gen_families11.py`, `gen_families12.py`).
Osy jsou opět rozdělené do skupin, které si nejsou podobné:

* **části věcí** — strom, sud, pluh, mlýn, varhany, buben, meč, brnění,
  sedlo, deštník, zvon, postel, mikroskop, tunel, silnice, pila, nůžky,
  kladivo, stan, batoh, kotel, skříň, komín, studna, řeka, rybník, město,
  divadlo, klavír, trubka, brýle, motor, raketa, lyže, klobouk,
* **řemesla** — padesát oborů od sklárny a koželužny po numismatiku,
  kriminalistiku a paleontologii; slova jsou všední, druhý význam odborný,
* **ustálená spojení** — dvacet dalších přívlastků (zelený, modrý, sladký,
  měkký, lehký, krátký, vysoký, silný, prázdný, divoký, hořký, čerstvý,
  plný, holý, planý, hluchý, křivý, rovný, mokrý, drahý),
* **písmena** — koncovky -ost, -ník a -dlo, předpona pře-, ypsilon, ě,
  krajní písmena vedle sebe v abecedě, stejný počet samohlásek a souhlásek,
  useknuté poslední písmeno, slovo pozpátku, složené slovo ze dvou slov,
* **prameny názvů** — Vančura, Lada, Kästner, Twain, London, Kipling,
  Poláček, Chytilová, Kubrick, Hemingway, Kafka, Škvorecký, Kachyňa,
  Troška, Tučný, balety, operety, symfonické básně, trampské písně,
* **vlastnosti a děje** — co praská v ohni, co se táhne v teple, co pění,
  co dorůstá, co unese člověka, co chladí bez proudu, co se dá roztavit,
  recyklovat, zamrazit, vyžehlit, rozsvítit,
* **znalostní osy** — pražské vrchy, slovenská města, evropské metropole,
  čeští panovníci a světci, apoštolové, severští bohové, řecké bohyně,
  měsíce planet, odrůdy jablek, brambor a vína, uzly, moře, kávy, čaje,
  těstoviny, pečivo, prvky, africké a americké státy, olympijská města.

### Rozpočet pětic

Nová sada by byla menší než ta stará, a to je past, kterou nikdo nečeká:
rozpočet se dělí **rovným dílem mezi rodiny** dané úrovně, takže s každou
další rodinou ubude pěticím na rodinu — a při celočíselném dělení spadne
rovnou o celý stupeň. Dvě stě nových rodin srazilo podíl z deseti pětic na
šest a celá sada se scvrkla z 4893 na 4498. Čísla se proto zvedla tak, aby
na každou skrytou rodinu vyšlo osm pětic: **5614 pětic** z 635 rodin.

### Co spadlo při psaní

* **Slovo uvnitř i vně téže rodiny.** U drahého kovu stálo dvakrát *kov*.
* **Písmena, která se nepočítala.** *Propast* nekončí na -ost, *dech* nemá
  krajní písmena vedle sebe v abecedě. Obojí zastavil build.
* **Vetřelec, který pravidlu vyhovuje.** *Ručník* po useknutí posledního
  písmene dá *ručni*… ne, dá slovo, které ve slovníku hry je — a tím by
  hádanka měla dvě řešení. Stejně tak *motyka* má stejně samohlásek jako
  souhlásek a *propiska* nemá jedinou čárku ani háček.
* **Příklonka.** „sklízejí se až na podzim" musí být „se sklízejí až na
  podzim", jinak rekapitulace zní „Čtyři z nich sklízejí se…".

## Čím je to hlídané

* `npm test` — 209 testů.
* `npm run smoke`, `smoke:standalone`, `play:verify` (206 slov).
* `npm run audit:pwa`, `audit:mobile` (bez nálezů), `audit:resume`.

---

# Bezpečnostní kontrola před vydáním na Google Play

Prošel jsem celou aplikaci — klienta, pravidla databáze, závislosti,
zásady soukromí — a rozdělil nálezy na to, co jsem opravil, a na to, co se
musí udělat v konzolích (Firebase, Play), protože do repozitáře nepatří.

## Co bylo špatně a je opravené

**1. Smazání účtu neprošlo do konce. (vysoká)**
`eraseMe()` maže přezdívku, záznam hráče a došlé výzvy. Pravidlo pro
`nicks/{přezdívka}` ale povolovalo jen **zabrání**:
`!data.exists() && newData.val() === auth.uid`. Při mazání `data` existuje
a `newData` je prázdné, takže obě podmínky selhaly a Firebase zápis odmítla.
Výsledek: hráč dostal chybu, jeho záznam zmizel, ale **přezdívka zůstala
navěky zabraná mrtvým účtem** a nikdo jiný si ji nemohl vzít. Smazání účtu
přímo v aplikaci přitom Google Play vyžaduje. Pravidlo teď povoluje i
smazání vlastního záznamu.

**2. Přezdívku šlo podvrhnout. (střední)**
Filtr závadných jmen (`foulNick`) běží v telefonu — a to je v pořádku,
dokud server hlídá, že se ven dostane jen jméno, které filtrem prošlo.
U `results` se to hlídalo, u **výzev a soubojů ne**: `challenges/*/nick`,
`duels/hostNick`, `duels/guestNick` i `duels/*/done/*/nick` braly libovolný
řetězec. Upravený klient tak mohl druhému hráči zobrazit cokoli, včetně
toho, co filtr zakazuje. Všechna čtyři místa se teď ověřují proti
`players/{id}/nick`, tedy proti jménu, které filtrem prošlo při zabrání.

**3. Seznam všech hráčů se dal stáhnout. (střední)**
`players` mělo `.read` na úrovni celé větve, takže jeden anonymní účet mohl
jedním požadavkem vytáhnout všechny přezdívky a id. Hra to nikdy
nepotřebovala — čte vždy konkrétního hráče. `.read` sedí teď o patro níž,
na `players/{id}`.

**4. Chyběly meze u volných polí. (nízká)**
`duels.guest` mohl být libovolný řetězec (i neexistující hráč),
`duels/*/words/{slovo}` klíč libovolné délky. Obojí je teď omezené;
`guest` musí být existující hráč a nesmí to být vyzývatel sám.

**5. Jednosouborová verze sahala na Wikimedia. (střední — soukromí)**
Verze pro jeden soubor má slíbeno, že neodešle ani bajt, a smoke test to
kontroluje. Jenže nekontroloval nápovědu **podobizna** v Citátu, která
stahuje obrázek z Wikimedia Commons. Kdo si otevřel „kontrolní" soubor
a koupil si tuhle nápovědu, prozradil svoji IP adresu třetí straně.
Nápověda se v téhle verzi už vůbec nenabízí a navíc to vynucuje zásada
zabezpečení obsahu (`img-src data:`), takže se to nemůže vrátit omylem.

**6. Obrázek posílal Wikimedii adresu stránky. (nízká)**
`<img>` s podobiznou teď má `referrerPolicy="no-referrer"`.

**7. Zranitelnost v závislostech. (nízká)**
`nanoid < 3.3.17` (high, GHSA-2v37-7h3g-55p8) — jen vývojová závislost přes
Vite, do aplikace se nedostala. `npm audit fix`; obojí hlásí nula nálezů.

## Co přibylo navíc

**Zásada zabezpečení obsahu (CSP).** Hra sama žádný cizí kód nespouští, ale
v obalu pro Play běží jako webová stránka a dává smysl to říct nahlas.
Seznam adres není vymyšlený — je to úplný výčet toho, na co hra opravdu
sahá: Firebase (přihlášení a databáze) a Wikimedia Commons. Skripty smí
jen ze stejného původu, žádné v textu stránky.

Jednosouborová verze má vlastní, mnohem přísnější: `default-src 'none'`
a zpátky jen text skriptu, text stylů a `data:`. Slib „neodejde ani bajt"
je tím poprvé vynucený prohlížečem, ne jen dodržovaný.

**`npm run audit:csp`.** Přísná zásada má ošklivou vlastnost: když je moc
těsná, nic se nerozbije nahlas — jen zmizí písmo nebo se hra tiše nespojí
se serverem. Nový audit hru rozehraje a poslouchá, jestli prohlížeč něco
neodmítl (konzole i událost `securitypolicyviolation`), a ověří, že se
načetlo vlastní písmo a zaregistroval service worker.

**Kontrola slibu ze zásad soukromí.** Tentýž audit hlídá, že při obyčejném
hraní neodejde požadavek na žádný cizí server. Je to slib, který se dá
porušit jedním nešikovným importem — Firebase se proto natahuje až uvnitř
funkcí — a od teď to hlídá stroj.

**Zásady soukromí** dostaly odstavec o podobiznách z Wikimedia Commons.
Chyběl a bez něj by výčet toho, kam data odcházejí, nebyl úplný.

## Co pravidla neuhlídají a musí se nastavit v konzoli

* **Firebase App Check** s Play Integrity. Anonymní přihlášení je zdarma
  a bez omezení, takže si kdokoli může vyrobit libovolný počet identit
  a psát do databáze mimo aplikaci. Pravidla drží **tvar** dat, ne
  **množství**. App Check přijme jen požadavky z pravé aplikace.
* **Rozpočtové upozornění** na projektu, aby se zahlcení poznalo dřív
  než z faktury.
* **Omezení API klíče** v Google Cloud → Credentials: klíč v balíčku je
  veřejný z principu, ale dá se omezit na Firebase API a na otisk podpisu
  aplikace.
* **Čtení nahlášení.** `reports` umí jen zapsat, číst je jde jen v konzoli.
  Google Play u obsahu od uživatelů chce, aby hlášení někdo skutečně
  vyřizoval — tady stačí jednou za čas nahlédnout.

## Co Play bude chtět ve formulářích

* **Data safety:** ID uživatele (skryté id Firebase), obsah od uživatele
  (přezdívka — sdílená s ostatními hráči), aktivita v aplikaci (skóre).
  Šifrováno při přenosu ✔, smazání dat na žádost ✔ přímo v aplikaci
  i odkazem `soukromi.html#mazani`.
* **Hodnocení obsahu:** hra obsahuje obsah od uživatelů (přezdívky), ale
  žádný volný chat — důvody nahlášení jsou z pevného seznamu.
* **Oprávnění:** obal potřebuje jen `INTERNET`. Hra nežádá o polohu,
  kontakty, fotky, mikrofon ani kameru.

## Co zůstává vědomě tak, jak to je

Hra funguje offline, takže **všechna data hádanek včetně odpovědí jsou
v telefonu**. Kdo umí otevřít vývojářské nástroje, uvidí odpovědi Otázky
dne i řešení hádanek. To není chyba, kterou by šlo opravit — je to cena za
to, že se hraje bez signálu. Souboje z toho nic nekazí: skóre se porovnává
mezi lidmi, kteří hráli tutéž hádanku, a pravidla nedovolí zapsat výsledek
dvakrát ani ho po prohře přepsat.

---

# Vetřelec: vetřelec nesmí trčet už tím, jak vypadá

Hráč nahlásil dvě hádanky z **těžké** úrovně, které se daly vyřešit bez
přemýšlení:

* *rhenium, wolfram, lanthan, gallium* — a mezi nimi **šroub**,
* *Jan, Václav, Anežka, Kliment* — a mezi nimi **kolík**.

Osa v obou případech sedí a věta na konci je pravdivá. Přesto je hádanka
špatná: čtyři latinské názvy prvků a jedna domácí potřeba, čtyři vlastní
jména a jedno obyčejné slovo. **Vetřelec je vidět dřív, než si člověk
stihne přečíst, na co se ptá** — a znalost, na kterou se hádanka chtěla
ptát, k ničemu není.

## Odkud se to vzalo

Rodina má dva seznamy: slova uvnitř (patří k ose) a slova vně (nepatří).
Slova vně se u většiny rodin brala z **nudné zásoby** — sta všedních
domácích potřeb, které schválně nemají nic společného s ničím. U rodin,
kde jsou slova uvnitř taky všední (*mají ucho, i když neslyší*), je to
správně. U rodin, kde je uvnitř hantýrka nebo vlastní jména, je to špatně:
zásoba je z jiného soudku a je to vidět.

Prošel jsem tím měřítkem celou sadu. Z 635 rodin jich takhle rozpojených
bylo **56** — a nebyly to jen ty nové: patřily mezi ně i pivovar, mapa,
tkaní, myslivost nebo lodě z dřívějších várek.

## Tři opravy

**1. Vlastní jména mají vetřelce z vlastních jmen.** Dvaadvacet rodin
(světci, panovníci, apoštolové, hlavní města, africké státy, státy USA,
řeky, měsíce planet, odrůdy jablek a brambor, lázně, přehrady, CHKO,
pražské čtvrti a vrchy…) dostalo seznam psaný ručně tak, aby vetřelec byl
**téhož druhu**: u českých světců jsou vně česká jména, která svatořečená
nejsou; u měst letních olympiád velkoměsta, kde olympiáda nebyla; u měsíců
planet hvězdy. Hádanka se tím konečně ptá na to, na co se ptát chtěla.

**2. Řemesla, obory a prameny názvů si berou vetřelce od sousedů.** U sto
šedesáti rodin to teď dělá skript sám: vetřelec pro kovárnu je hasičská
*proudnice* nebo geologický *zlom*, pro ornitologii mineralogický *vryp*,
pro psychologii kriminalistická *daktyloskopie*. Věta „čtyři z nich jsou
zároveň kovářské pojmy — proudnice ne" platí doslova a hráč musí vědět,
co ke kterému oboru patří.

Slovo, které leží ve **dvou** rodinách skupiny naráz, se za vetřelce
nebere. *Měch* je díl varhan i kovářské náčiní, *obruč* patří k sudu i
k bubnu; u takového slova by hráč měl pravdu, i kdyby ukázal jinam.

Starší ručně psané rodiny na to nemusely čekat, až je někdo přepíše:
skupinu jde poznat z otázky, takže si sousedy dohledá stavitel při buildu.
Sahá jen na rodiny, které měly celou zásobu z nudné vaty — kde je seznam
psaný ručně, byl k tomu důvod a ten se nepřebíjí.

**3. Rodina, která se spravit nedala, zmizela.** *„Jsou to zároveň názvy
jazyků"* — cokoli, co jazyk není, trčí na první pohled, a cokoli, co jazyk
je, dělá z hádanky dvě řešení. Taková osa se nedá zachránit seznamem.

Při té příležitosti šly ven i dvě drobnosti: *„zelený slad"* se
v sladovnickém seznamu rozpadl na holé přídavné jméno a čajová rodina
míchala obyčejná přídavná jména (*zelený, černý*) s exotickými názvy
(*rooibos, matcha*) — obojí byl tentýž problém v malém.

## Čím je to hlídané

Stavitel pětici zahodí, když je vetřelec **jediné slovo psané velkým
písmenem** — nebo naopak jediné psané malým mezi vlastními jmény. Je to
ta část problému, kterou stroj pozná bezpečně, a hlídá ji i test nad
hotovými daty (`tests/data.test.ts`). Zbytek — cizí slovo mezi domácími,
domácí potřeba mezi řemeslnými termíny — drží tím, že vetřelec pochází
ze sousední rodiny téhož druhu.

Sada má po opravě 5606 pětic z 634 rodin a žádná rodina nepřišla o všechny
hádanky.

---

# Řetěz: klepnutí na vytažené písmeno padalo do tlačítka pod ním

Hráč hlásil, že v Řetězu po podržení klávesy sice vyskočí písmeno
s diakritikou, ale klepnutí na ně provede **tlačítko pod nabídkou** —
vrátí tah nebo nabídne vzdání kola.

## Co se dělo

Nabídka variant se otevírá **nad** klávesou, a v Řetězu tím pádem přesně
přes řádek s tlačítky *Zrušit úpravu*, *Vrátit tah* a *Vzdát kolo*.
Písmeno se zapisovalo na `pointerup`:

1. prst se zvedne → `pointerup` na vytažené variantě,
2. písmeno se napíše a nabídka **zmizí z DOMu**,
3. prohlížeč pošle po každém doteku ještě dodatečné `click` — to, kterým
   se od dob myši udržují při životě stránky, co o doteku nevědí. Znovu se
   zeptá, co na těch souřadnicích leží, nabídku už tam nenajde a stiskne
   tlačítko pod ní.

Písmeno se tedy napsalo správně. Jenže hned nato ho *Vrátit tah* (nebo
*Zrušit úpravu*) smazal, takže to vypadalo, že klepnutí vůbec netrefilo.

## Oprava

**Písmeno se zapisuje na `click`, ne na `pointerup`.** Nabídka v té chvíli
v DOMu ještě stojí, klepnutí dostane ona a žádné další už nepřijde. Navrch
to spraví ovládání z klávesnice, kde `pointerup` nikdy nepřijde.

**A druhé gesto, které nefungovalo vůbec.** Na systémové klávesnici se
písmeno s háčkem bere tak, že prst po podržení **sjede** na variantu
a teprve tam se zvedne. Tady to nedělalo nic, a byly to dvě věci naráz:

* prohlížeč si ten pohyb bral jako rolování stránky, posílal
  `pointercancel` a gesto skončilo nikde. Klávesy proto mají
  `touch-action: none` — dotek, který začal na klávese, patří klávesnici;
* i kdyby se to nestalo, `pointerup` dostane pořád **základní** klávesa,
  protože jí prohlížeč ukazatel na začátku stisku implicitně přidělí a do
  konce gesta ho nepustí. Co je pod prstem doopravdy, se proto zjišťuje ze
  souřadnic (`elementFromPoint`).

## Čím je to hlídané

`npm run audit:keyboard` (nový) hraje Řetěz **dotykem**: podrží klávesu,
klepne na vytažené písmeno a zvlášť zkusí i sjetí prstem. Kontroluje, že
se napsalo právě to písmeno, že se neotevřelo okno vzdání kola a že
nabídka nad klávesnicí opravdu leží nejvýš.

Myší se chyba nedá reprodukovat — ta dodatečné `click` neposílá. Právě
proto ji neodhalil ani jeden z dosavadních testů, které klikají myší.

# Rozvržení: lišta ve hře se rozsypala a nikdo to neměřil

Hráč poslal snímek z Citátu: nahoře vlevo „← Menu" napsané **přes** zlatý
čip s plamínkem, vpravo čip série uříznutý okrajem. Nebyla to jedna
překlepnutá hodnota — bylo to celé rodině chyb, která šla napříč všemi
devíti hrami a všemi šířkami telefonu.

## Co se dělo

**Tlačítko se smrsklo pod svůj nápis.** Prvek v pružném řádku se ve
výchozím nastavení nechá stlačit, jenže písmena uvnitř se nezmenší —
vylezou z tlačítka ven a kreslí se přes souseda. Tlačítko „← Menu" mělo být
62 px široké, dostalo 34 a zbytek nápisu si sedl na čip vedle. Nic se
neuřízlo, stránka se nerozšířila, jen dvě věci ležely na sobě, takže se
o tom žádná dosavadní kontrola nedozvěděla.

**Lišta se přestala vejít.** Ve hře veze osm věcí: zpět, denní řadu,
pravidla, hodnost, kalamář, hodiny, sérii a téma. Osm se nevejde na žádný
telefon. Ustupování bylo napsané pro dobu, kdy jich bylo míň, takže na
390 px visel přepínač témat za okrajem i v běžném kole a v denním k němu
přibyl čip série.

**Otázka dne o tom vůbec nevěděla.** Pravidla lišty se držela třídy
`playing`, kterou si bere jen deska hry a souboj. Kvíz má lištu stejně
nabitou (hodiny, kalamář, série), ale žádné ustupování se ho netýkalo —
přetékal až o 87 px.

**A hlavně: měřilo se jen šest her z devíti.** `audit:mobile` má seznam
režimů a Citát ani Vetřelec na něm nikdy nebyly. Chyba přitom byla úplně
všude — jen se koukalo jinam, než kam hráč.

## Co je opravené

* **Nic v liště se nesmí smrsknout pod svůj obsah** (`flex-shrink: 0`
  a `nowrap` na všech jejích dětech). Když se něco nevejde, lišta se
  poctivě přeplní — a to audit uvidí. Tiché překrytí ne.
* **Dopsané ustupování** do 899 px (značka, název režimu, slovo „Menu",
  přepínač témat), 560 px (profil) a 400 px (čip série, slovo ve značce).
  Kalamář a hodiny neustoupí nikdy — jsou to jediné dva údaje, které se
  během kola mění.
* **Značka ustoupí jen tam, kde ji vystřídá šipka zpět** (`:has(.btn-back)`).
  V souboji šipka není, takže tam značka zůstává a je pořád kudy ven.
* **Otázka dne dostala šipku zpět** a třídu `round`, která nese pravidla
  lišty pro každé běžící kolo. Bez šipky by se z ní na telefonu nedalo
  odejít — dosud to zastávala značka, která teď v kole ustupuje.
* **Dotykové cíle na 40 px.** V liště to bylo zadarmo (je vysoká 44 px), jen
  se to nikdy nenastavilo: čipy měly 32 px a profil 26. Klávesy Šibenice
  a Citátu mají místo toho podlahu 44 px na výšku — na šířku jich deset
  v řadě jinak nevyjde ani nativní klávesnici.
* **Vysvětlivky přilepené k textu** (popisek nad nápovědami, čísla
  v ukazateli hry) se zvětšit nedají — velikost jim určuje písmo, ke
  kterému patří. Dostaly neviditelnou plochu navíc; ťuká se do 40 px,
  vidět je pořád jen text. Otazník u Otázky dne ji dostat nemohl (hned
  vedle leží tlačítko, které kolo spouští), tak povyrostl doopravdy.
* Ze značky zmizelo `overflow: hidden`, které slovo mlčky uřízlo v půlce.

## Čím je to hlídané

`npm run audit:layout` (nový). Neptá se, jestli se obrazovka vejde — na to
je `audit:mobile` — ale jestli každý prvek sedí ve svém místě:

1. **nápis přetéká ze svého tlačítka** (měří se podle dětí, ne přes
   `scrollWidth`: vystředěný obsah přetéká na obě strany a `scrollWidth`
   zná jen tu pravou),
2. **sourozenci na sobě**,
3. **prvek za okrajem obrazovky**,
4. **malý dotykový cíl** — a počítá se plocha, do které se dá trefit, včetně
   neviditelné, takže se malý cíl nedá schovat pseudoprvkem naoko,
5. **stránka přetéká do strany**.

Prochází všech devět her v běžném i denním kole, Otázku dne, menu, panel
obtížnosti, panel nápověd, potvrzení vzdání kola, návod, vitrínu, žebříček
hodností, statistiky a průvodce — na osmi velikostech od 320 px po monitor.
Na monitoru se mez na dotykový cíl neuplatňuje; platí pro prst, ne pro myš.

`audit:mobile` má nově na seznamu i Citát a Vetřelce.

## Dodatek: značka se z menu neměla ztratit

Hráč hned nahlásil, že v menu zmizel nápis „Slova" a zbyl jen kroužek
s tečkami. Byla to moje chyba v předchozím kroku: ustupování jsem napsal
tak, že se pod 400 px schoval nápis — jenže značku má hráč v menu vidět
celou, včetně teček. To místo se dá vzít jinde.

Vyšlo přitom najevo, proč se to vůbec zdálo v pořádku: pravidlo, které
mělo tečky triády pod 420 px schovat, bylo napsané jako `.brand-triad`
a v souboru nad výchozím `.brand-triad { display: inline-flex }`. Stejná
specificita, později vyhrává to druhé — takže **nikdy neplatilo**. Tečky
byly vidět vždycky a šetření místem, se kterým se počítalo, se nikdy
nekonalo.

Značka je teď celá na každé šířce. Místo se bere z mezer a pod 340 px
(iPhone SE první řady) se přepínač témat vrací ke svým přirozeným 34 px
na šířku; na výšku má pořád 44. Je to jediná úleva z meze 40 px v celém
auditu a `audit:layout` ji zná pojmenovanou, ne mlčky.

Lišta v menu se s celou značkou vejde i se čtyřciferným kalamářem —
měřeno se zásobou 1312 inkoustu, na 320 až 430 px.

# Souboje nefungovaly vůbec — a mlčely o tom

Hráč poslal snímek, kde „Vyzvat hráče" zůstalo na **Posílám…** a už se
nehnulo. Nebyla to pomalá síť. Byly to čtyři chyby, které na sebe navazují,
a tři z nich jsem tam zavlekl při bezpečnostní kontrole a při psaní té
vrstvy.

## 1. Zásada obsahu zabila spojení s databází

Firebase se k databázi dostává websocketem. Když neprojde — mobilní síť,
firemní proxy, jedno klopýtnutí —, přepne na **záložní přenos**, a ten
funguje tak, že si do stránky vloží `<script src="…/.lp?…">`.

Zásada obsahu (CSP), kterou jsem přidal při kontrole pro Google Play, měla
`script-src 'self'`. Prohlížeč tedy ten skript odmítl:

```
Refused to load the script 'https://…firebasedatabase.app/.lp?start=t'
because it violates the following Content Security Policy directive:
"script-src 'self'".
```

Klient se nespojil vůbec. Websocket přitom zásada pouštěla — proto to
vypadalo, že je všechno v pořádku, a proto se toho nevšimla ani kontrola CSP.

Opravené tím, že `script-src` pouští **jednu jedinou** cizí adresu: naši
databázi, vypsanou celou, ne přes hvězdičku.

## 2. Nic ze sítě nemělo lhůtu

Tohle je důvod, proč se hráč nedozvěděl **nic**. Firebase žádnou lhůtu nemá:
dokud se klient nespojí, zápis leží ve frontě a slib se **nikdy nesplní ani
nezamítne**. Tlačítko proto svítilo „Posílám…" donekonečna — ne chybou,
ale čekáním na něco, co nikdy nepřijde.

Každé volání má teď dvanáctivteřinovou lhůtu a vlastní jméno kroku, takže
hláška řekne, kde to uvázlo: „Server neodpovídá (odeslání výzvy)."

## 3. Neúspěšné spojení se pamatovalo napořád

`ready ??= connect()` — když první pokus selhal, zůstal v proměnné
**zamítnutý slib** a vracel se pořád dokola. Jedno klopýtnutí sítě tím
umlčelo souboje až do restartu aplikace a rada „zkus to znovu, až budeš
online" se nedala poslechnout. Nepovedený pokus se teď zapomíná — a aby šel
zopakovat, hledá se existující instance Firebase místo slepého
`initializeApp`, který by podruhé spadl.

Stejná chyba byla i v načítání herních dat (`fetchJson`): v paměti leží
slib, ne hotová data, takže se pamatovalo i selhání a celý balíček byl do
restartu němý. Opravené obojí.

## 4. Přezdívka se dala zamknout sama sobě

Zabírá se dvěma zápisy — jméno a k němu záznam hráče. Komu prošel první
a druhý ne, ten měl na serveru jméno zabrané svým vlastním id, ale bez
záznamu hráče: nedalo se s ním nic dělat a každý další pokus hlásil „tuhle
přezdívku už někdo má". Teď se nejdřív zjistí, kdo jméno drží, a když jsem
to já sám, jen se dopíše, co chybí.

Navrch: zápas se nezaloží bez zapsané přezdívky (pravidla databáze u něj
ověřují, že jméno vyzývatele sedí se serverem) a řekne se to rovnou, místo
obecného „nepodařilo se spojit". A kdo napíše svoje vlastní jméno, dozví se,
že sám sebe vyzvat nemůže — dřív dostal „takového hráče neznám".

## Čím je to hlídané

`npm run audit:duel` (nový). Odehrát celý souboj z tohohle stroje nejde,
databáze je za bránou — ale právě to je ta situace, která byla rozbitá,
takže se ověřuje ona:

1. **Zásada pustí, co Firebase potřebuje** — websocket i záložní přenos.
   Rozlišuje se, jestli spojení odmítla zásada (chyba), nebo síť (tady
   v pořádku). Se starou zásadou audit spadne, ověřeno.
2. **Nedostupný server se ozve** — do dvaceti vteřin je na obrazovce hláška
   a tlačítko jde zmáčknout znovu. Nikde nesmí zůstat „Posílám…".

Co ověřit odsud nejde a musí se vyzkoušet na telefonu: že výzva doopravdy
dojde druhému hráči. Pravidla databáze jsem proti tomu, co hra posílá,
prošel řádek po řádku (včetně délky seznamu hádanek — id mají šest znaků,
limit je 120).

## Dodatek: kde přesně to visí, se dalo jen hádat

Hráč po opravě hlásil, že je to pořád stejné. Nasazený balík opravu měl —
ověřeno, hláška o lhůtě je v `assets/index-*.js`. Zbývaly dvě možnosti a obě
jsou teď zavřené:

**Načítání hádanek nemělo lhůtu.** Odeslání výzvy má dvě fáze: nejdřív se
stáhnou hádanky (stejná adresa jako hra), teprve pak se zakládá zápas
v databázi. Lhůtu dostala jen ta druhá. `fetch` přitom sám od sebe nikdy
neskončí — když spojení uvázne v půli (telefon přepíná mezi wi-fi a daty),
slib se nesplní ani nezamítne. Výzva tedy mohla viset dál, jen o krok dřív,
a vypadalo to úplně stejně. Načítání dat má teď třicetivteřinovou lhůtu
s `AbortController`.

**Z tlačítka nešlo poznat, která fáze stojí.** Obě říkaly „Posílám…". Teď
říkají „Chystám hádanky…" a „Posílám výzvu…", takže se ze snímku pozná, jestli
je problém v síti k herním datům, nebo v databázi soubojů.

`audit:duel` nově projde i samotné odeslání výzvy, ne jen zabrání přezdívky.

### K pravidlům, která hráč poslal

Ta na serveru jsou v pořádku a výzvu pustí — jsou dokonce volnější než ta
v repozitáři (`tools/firebase/database.rules.json`). Dvě věci by se z něj
ale doplnit měly:

* `nicks/$nick` na serveru nemá větev pro **smazání**, takže „smazat účet"
  po sobě přezdívku neuklidí. Obchody to vyžadují a repozitář to má.
* jména (`hostNick`, `guestNick`, `nick` u výzev) se na serveru neověřují
  proti záznamu hráče, takže si je kdokoli může poslat jaká chce.

## Dodatek 2: přihlášení projde, databáze mlčí

Hráč poslal snímek s hláškou **„Server neodpovídá (hledání hráče)"**. To je
přesně ta informace, která dosud chyběla, a zužuje to hledání na jediné
místo:

* **přihlášení proběhlo** (jinak by v závorce stálo „přihlášení"),
* **hádanky se stáhly** (jinak by tlačítko stálo na „Chystám hádanky…"),
* **databáze neodpověděla** — klient se k ní vůbec nespojil.

Adresa databáze je přitom v pořádku: `slova-b0176-default-rtdb.europe-west1.
firebasedatabase.app` má A i AAAA záznam. Zásada obsahu už pouští websocket
i záložní přenos (ověřeno auditem). Zbývá tedy něco na straně telefonu nebo
sítě, a to se odsud změřit nedá — databáze je z tohohle stroje za bránou.

**Přibyla proto zkouška spojení** přímo v Hře s přáteli. Rozebere to na tři
vrstvy, protože každá se dá rozbít zvlášť a každá selhává jinak:

1. **Přihlášení** — jde přes `identitytoolkit.googleapis.com`.
2. **Databáze běžným požadavkem** — `https://…/.json`. Pravidla ho odmítnou
   a to je v pořádku; podstatné je, že vůbec dorazí odpověď, tedy že je
   adresa dosažitelná.
3. **Databáze websocketem** — tudy mluví hra doopravdy. Když projde bod 2
   a neprojde bod 3, síť nepouští websockety a chyba není ve hře.

Výsledek se vypíše po řádcích a dá se vyfotit. `audit:duel` hlídá, že
zkouška doběhne a vypíše všechny tři kroky i tehdy, když neprojde ani jeden.

# Souboj se otevřel, ale deska měla nulovou výšku

Spojení už drží a výzva se založí. Jenže u Vetřelce se otevřela obrazovka
souboje, ukázala hlavičku („proti Zelda · 1. kolo ze 3 · nejvíc 600")
a **pod ní nic**. Vypadalo to, že se hra nespustila.

## Co se dělo

Deska hry má `container-type: size`. To znamená „počítej svoji velikost,
jako bys byla prázdná" — a je to schválně: díky tomu se dá obsah desky
škálovat podle jejích rozměrů, aniž by si to samo se sebou skákalo do řeči.

Podmínkou ale je, že výšku desce musí dát někdo shora. U běžných her ji dává
pravidlo `.shell.playing .game.with-rail { height: 100% }`. Souboj má vlastní
rozvržení (`duel-game`) a na tohle pravidlo nedosáhl — takže ve sloupci bez
určené výšky se deska smrskla na **nula pixelů**. Pětice slov se přitom
vysázela celá (288 px), jen ji nebylo kam vykreslit.

Změřeno, ne odhadnuto: `.board` 380×0, `.intruder-words` 380×288.

## Oprava

`.shell.playing .duel-game { height: 100% }` — souboj dostane plnou výšku
stejně jako ostatní hry. Deska pak měří 753 px místo nuly.

Platí pro oba formáty, Voština i Vetřelec sdílejí `duel-game`.

## Upozornění na výzvu

Hráč k tomu chtěl, aby o výzvě vždycky věděl. Přibylo tedy:

* **Výzvy se poslouchají pořád**, ne jen v menu. Dřív se posluchač uvnitř
  hry vypínal, aby neubíral spojení — jenže pak se o výzvě hráč dozvěděl,
  až když se vrátil do menu.
* **Systémové upozornění**, když nějaká dorazí. Ohlašuje se jen to, co
  přibylo (seznam chodí celý pokaždé), a první načtení po spuštění se
  neohlašuje — upozorňovat na to, co má hráč před očima, je otravné.
* **Povolení se ptá z ťuknutí** v Hře s přáteli, ne samo od sebe při
  spuštění. Bez gesta žádost prohlížeče rovnou zamítnou a druhá šance není.

Co to **neumí a je to u toho napsané**: upozornění chodí, dokud hra běží —
i schovaná na pozadí —, ale ne když je úplně zavřená. K tomu je potřeba
Firebase Cloud Messaging a k němu server, který zprávu odešle; odesílací
klíč je tajný a do telefonu se dát nesmí, jinak by mohl kdokoli posílat
upozornění všem hráčům. Znamenalo by to Cloud Function a k ní placený tarif.

## Čím je to hlídané

`audit:duel` má nový oddíl **„Souboj má na desku místo"**. Souboj se odsud
rozehrát nedá (potřebuje soupeře v databázi), ale rozvržení ano: do běžícího
kola se vloží deska souboje a změří se, že má výšku a že se do ní vejde celá
pětice. Bez opravy audit spadne na `0px` — ověřeno.

## Dodatek 3: čekalo se na dotaz, ne na spojení

Hráč hlásil totéž znovu — jenže mezitím jednou prošlo a souboj se založil.
Střídavý výsledek je jiná chyba než blokáda a ukazuje na jinou příčinu:
lhůta byla utažená na něco, co jí nepatřilo.

**Přihlášení a spojení s databází jsou dvě různá čekání.** Přihlášení je
jeden obyčejný požadavek — vteřinu, dvě. Databáze si ale drží **otevřené
spojení** a než ho navlékne, musí otevřít websocket (a když ho síť nepustí,
přepnout na pomalejší záložní přenos), vyměnit si přihlašovací lístek
a teprve pak umí odpovídat. Na telefonu to poprvé trvá klidně dvacet vteřin.

Dotaz se přitom posílal do ještě nespojeného klienta a měřila se mu tatáž
krátká lhůta jako všemu ostatnímu — dvanáct vteřin. Jednou se to stihlo
a hra běžela, podruhé ne a hlásilo se „server neodpovídá", i když byl server
v pořádku a stačilo mu dát chvíli.

**Teď se napřed počká na spojení a teprve pak se posílá dotaz.** Čeká se na
`.info/connected`, na což je pětadvacet vteřin, a dotazy pak běží proti živému
spojení, takže jim patnáct vteřin bohatě stačí. Když se spojení nenaváže,
řekne se to rovnou: „Nepodařilo se spojit s databází."

Zároveň o tom čekání obrazovka **říká**, místo aby mlčela — odeslání výzvy
má teď tři fáze: „Chystám hádanky…", „Spojuji se serverem…", „Posílám
výzvu…".

Zkouška spojení má čtvrtý řádek: **spojení hry s databází**, i s časem, jak
dlouho trvalo. To je ze všech kroků ten nejdůležitější — hra se neptá
websocketem přímo, ptá se přes Firebase, a ten si spojení navléká sám.

# Odveta, hodnost soupeře a soubojové mety

Souboje běží, takže přišly tři věci, o které si hráč řekl.

## Odveta

Po dohraném souboji se v závěrečné kartě nabídne **Odveta**. Založí nový
zápas s tímtéž soupeřem a ve stejném formátu, jen s novými hádankami —
staré by soupeř už znal. Dřív se musela přezdívka pokaždé vypsat znovu, což
u dvou lidí, kteří si hrají celý večer, znamenalo psát ji pořád dokola.

Obrazovka souboje se přitom musí rozehrát načisto, ne jen dostat nová data —
proto má `key={match.id}`. Bez toho by v ní zůstal starý stav a odveta by
začala u výsledku předchozího kola.

## Hodnost soupeře

U přezdívky soupeře je odznak hodnosti a její číslo; ťuknutím se otevře
karta hráče se jménem hodnosti, soubojovou hodností a bilancí.

Vlastní hodnost si každý posílá na server sám (`players/{uid}/band`) — jen
číslo, jméno si druhá strana dohledá ze stejného seznamu. Píše se, jen když
se změnila; hodnost roste pomalu a zápis při každém spuštění by byl jen šum.

**Karta se načítá až na ťuknutí.** Uprostřed souboje se nemá chodit na server
pro nic, co si hráč nevyžádal, a kdo si soupeře prohlížet nebude, nezaplatí
za to ani jedním požadavkem.

Pravidla databáze se kvůli tomu měnit nemusely: `band` i `wins/losses/draws`
jsou pole, která `players/$uid` už povoluje, a čtení je otevřené každému
přihlášenému.

## Hodnosti a mety za souboje

Dvanáct soubojových hodností od **Vyzyvatele** po **Nepřemožitelného**.
Počítají se ze tří čísel, která databáze o hráči už vede: za výhru tři body,
za remízu jeden, za prohru nula. Prohra tedy hodnost **nesráží** — kdo hraje
a prohrává, stojí; kdo nehraje, taky stojí. Hodnost říká „tohle jsem
odehrál", ne „o tolik jsem lepší".

Poslední stupeň je na zhruba dvě stě vyhraných soubojů, tedy na dlouhou
známost, ne na jeden večer. K odehranému souboji je pokaždé potřeba druhý
člověk — to je jediná obrana proti nahánění a stačí, protože žebříček nikam
neposílá a s nikým se neporovnává.

K tomu **čtrnáct nových met** ve vlastní skupině *Souboje s přáteli*: dva
žebříčky po pěti (odehrané souboje, výhry), tři za série výher a jedna za
vyhranou odvetu. Body ze soubojů dál nejdou do věhlasu ani do hodnosti
profilu; mety dávají jen inkoust a je jich pevný počet, takže se ani jimi
nedá nic nahnat donekonečna.

Podmínky se čtou z `profile.duels`, což je **kopie** bilance ze
`slova.multi.v1`. Je to schválně: ocenění se smí koukat jedině do profilu,
jinak by se nedala kdykoli přepočítat znovu a meta, která nestihla spadnout,
by zůstala navždy zamčená.

## Čím je to hlídané

Šest nových testů nad počítáním soubojové hodnosti: body za výhru a remízu,
že prohra hodnost nesráží, že žebříček začíná na nule a končí, že postup
uvnitř hodnosti sedí na prahy a že prahy jdou zdola nahoru bez opakování.

## Dodatek 4: spojení se občas nenavázalo a samo se nevzpamatovalo

Hráč hlásil „Nepodařilo se spojit s databází" — tedy novou hlášku, ne starý
zásek. Spojení se prostě nenavázalo ani za pětadvacet vteřin, a to střídavě:
jednou večer prošlo, podruhé ne. Poprvé to bylo na mobilních datech, teď na
wi-fi.

**Firebase si přenos vybírá sám a pamatuje si, co mu naposled nevyšlo.** Když
jednou neprojde websocket, drží se pak celé sezení pomalejšího záložního
přenosu — a když uvázne i ten, sám od sebe už nic nezkusí. Jediné, co
pomáhalo, bylo zavřít celou aplikaci.

Čekání na spojení je proto rozdělené na dva pokusy: deset vteřin, pak
`goOffline` + `goOnline` (což Firebase donutí začít načisto) a dalších
patnáct. Celkem tedy stejná trpělivost jako dřív, jen se uprostřed spojením
zatřepe.

Při té příležitosti se opravila i drobnost v čekání: posluchač se odhlašoval
uvnitř své vlastní obsluhy, kde ale proměnná s odhlašovací funkcí ještě
nebyla naplněná — když spojení stálo hned, posluchač po sobě neuklidil.

**A rozbor je nově rovnou u chyby.** Když výzva neprojde, je pod hláškou
tlačítko *Kde to vázne?*, které vypíše všechny čtyři kroky. Dosud se totéž
dalo najít jen jinde v nabídce, což je uprostřed nezdaru to poslední, co
hráč chce hledat.

`audit:duel` k tomu hlídá, že je rozbor u chyby po ruce, že vypíše všechny
kroky a že se panel s ním dá dorolovat — s rozborem povyroste a ovládání se
nesmí stát nedosažitelným.

## Dodatek 5: všechno zelené, a přesto to nešlo

Hráč poslal snímek, kde zkouška hlásí **čtyřikrát zeleně** — přihlášení
prošlo, databáze odpověděla (401 „Permission denied", což je správně,
pravidla čtení kořene nepustí), spojení hry se navázalo **za 10,1 s**
a websocket se otevřel. A výzva přesto skončila na „Server neodpovídá
(hledání hráče)". Dvě věci se z toho daly vyčíst.

### Klient se sám od sebe nespojí

Deset celých jedna vteřiny je podezřele přesně o desetinu víc, než byla
tehdejší lhůta prvního čekání. Spojení se tedy navázalo **až v ten okamžik,
kdy ho po marném čekání probudilo `goOffline`+`goOnline`** — ne někdy během
něj.

Důvod: Firebase navazuje spojení, teprve když o data někdo stojí. Čekání na
`.info/connected` o data nestojí — ta větev se obsluhuje v telefonu, ne na
serveru —, takže samotné čekání klienta nerozhýbe a vyprší naprázdno. Teď se
proto napřed řekne `goOnline` a **pak** se čeká.

### Ztracený dotaz se už nezopakuje

To druhé je jádro věci. Firebase doručuje čtení dvěma způsoby a liší se
právě v tom, co udělají, když spojení spadne:

* **Jednorázový dotaz (`get`)** se pošle a čeká na odpověď. Když se spojení
  mezitím přetrhne — a hned po navázání je to nejpravděpodobnější —, dotaz
  se **znovu neposílá**. Odpověď nikdy nepřijde a slib visí až do lhůty.
* **Posluchač (`onValue`)** je součástí stavu, který si klient po obnoveném
  spojení sám navěsí znovu. Výpadek tedy přežije a data doručí, jakmile je
  zas kudy.

Všech jedenáct čtení v `multi.ts` proto jde přes posluchače, kterého si po
první hodnotě zase odhlásíme. Zápisy se řešit nemusely — ty si Firebase
po obnoveném spojení posílá znovu sám.

To přesně sedí na hráčův snímek: spojení stálo (a zkouška ho proto našla
v pořádku), jen odpověď na dotaz se ztratila při jednom přeťatém spojení.

# Souboje: konečně proti skutečné databázi

Hráč poslal snímek se čtyřmi zelenými řádky zkoušky — a výzva přesto
neprošla. V tu chvíli došly hypotézy, které jde ověřit ze snímku, a bylo
potřeba přestat hádat.

## Emulátor: databáze, se kterou se dá mluvit

Databáze projektu je z vývojového stroje za bránou (proxy vrací 403 už na
`CONNECT`), takže se souboje nikdy nedaly odehrát a všechny dosavadní opravy
stály na čtení kódu a na hláškách z telefonu. Nově se pouští **emulátor
Firebase se skutečnými pravidly** z `tools/firebase/database.rules.json`:

* `bash tools/emu.sh start` — databáze na 9000, přihlášení na 9099.
  Emulátoru se musí sebrat proxy, jinak by přes ni posílal i dotazy na
  `127.0.0.1` a brána je odmítne.
* `SLOVA_EMU=1` postaví hru, která mluví s emulátorem. V běžném buildu je
  `__EMU__` natvrdo `false`, takže se ta část kódu do balíčku vůbec
  nedostane — ověřeno, v produkčním souboru není o emulátoru zmínka.
* `npm run audit:duel:e2e` složí obojí dohromady a odehraje celou cestu ve
  **dvou prohlížečích naráz**: oba si zaberou přezdívku, jeden vyzve
  druhého, výzva doopravdy dorazí, soupeř ji přijme a souboj se rozehraje.

Hned první běh ukázal, že hra i pravidla jsou v pořádku a spolu mluví. Chyba
tedy nebyla v tom, co se posílá, ale kdy a kudy.

## Nalezená chyba: přenos, ze kterého není cesty zpátky

Test si vynutil to, co má hráč v kapse — výpadek sítě — a chyba se ukázala
okamžitě. Firebase si přenos vybírá sám a **pamatuje si, co mu naposled
nevyšlo**. Stačí jediné klopýtnutí (telefon na vteřinu ztratí signál),
websocket se zapíše jako nefunkční a klient pak celé sezení jede přes
pomalejší záložní přenos. K websocketu se **sám nevrátí**, ani když už
dávno funguje. A když uvázne i ten záložní, nespojí se vůbec — jediné, co
pomůže, je zavřít celou aplikaci.

Přesně tak to hráč popisoval: jednou večer výzva projde, podruhé ne.

Opravené `forceWebSockets()`: přenos je vždycky jeden a týž, žádný skrytý
stav, a po výpadku se prostě zkusí znovu. Cenou je, že v síti, která
websockety vůbec nepouští, souboje nepojedou — z měření u hráče je ale
vidět, že websocket se otevírá bez potíží, a mlčky se zaseknout je horší
než se ozvat.

## Co audit hlídá

Kromě celé cesty dvou hráčů i dvě věci, které se z jednoho prohlížeče
ověřit nedají:

* **neznámá přezdívka se pozná hned** (do vteřiny), ne až po vypršení
  lhůty — jinak by překlep vypadal jako výpadek serveru,
* **po výpadku sítě se spojení obnoví bez restartu aplikace** — přesně to,
  co bylo rozbité.
