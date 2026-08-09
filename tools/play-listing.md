# Google Play — texty a odpovědi do dotazníků

Všechno, co Play Console chce vyplnit, na jednom místě. Kopíruj odsud, ať se
to nevymýšlí pokaždé znovu a ať odpovědi v dotaznících sedí s tím, co hra
opravdu dělá — nesoulad mezi formulářem a chováním aplikace je jeden
z nejčastějších důvodů zamítnutí.

Grafiku a snímky vyrobí `node tools/play-assets.mjs` do složky `play/`.
Zabalení do androidího balíku popisuje `tools/android/README.md`.

---

## Základní údaje

| Pole | Hodnota |
|---|---|
| Název aplikace (max 30) | `Slova — české slovní hry` |
| Typ | Hra |
| Kategorie | Slovní hry (Word) |
| Značka / tagy | slovní hra, čeština, hlavolam, denní výzva |
| Web | https://taronwho.github.io/Slova/ |
| Kontaktní e‑mail | taronwho@gmail.com |
| Zásady ochrany soukromí | https://taronwho.github.io/Slova/soukromi.html |
| Smazání účtu a dat | https://taronwho.github.io/Slova/soukromi.html#mazani |
| Obsahuje reklamy | **Ne** |
| Nákupy v aplikaci | **Ne** |
| Cílová věková skupina | **13+** (mimo program Rodina) |

---

## Stručný popis (max 80 znaků)

```
Osm slovních her v češtině. Denní výzvy, souboje s přáteli, i bez signálu.
```

---

## Úplný popis (max 4000 znaků)

```
Osm slovních her, které mají společné jedno: hrají se česky a doopravdy
s češtinou pracují. Žádné překlady, žádná slova, která by ve slovníku
nikdo nenašel.

CO SE HRAJE

Řetěz — přepiš jedno slovo na druhé, vždycky po jednom písmenu. Každý
mezikrok musí být skutečné slovo.

Voština — sedm písmen, prostřední musí být v každém slově. Kolik jich
z plástve dostaneš ven?

Věž — z jednoho slova postav další tak, že přidáš písmeno a přeházíš
pořadí. Patro po patře až nahoru.

Šibenice — klasika, na kterou se nezapomíná. Hádej písmena, dokud máš čas.

Detektiv — dostaneš spis: mluvnické údaje, rozmazaný význam, cenzurovaný
původ slova. Celý příběh se dozvíš, až slovo odhalíš.

Slabiky — padající kostky se slabikami. Skládej z nich slova dřív, než
se sloupce zaplní.

Citát — z výroku vidíš pár slov, zbytek doplň. Nápovědy jdou po řadě:
portrét, kdo to byl, jméno.

Vetřelec — pět slov, čtyři něco spojuje a páté ne. Souvislosti nejsou
slovníkové: někdy jde o hlásky, jindy o filmy nebo o to, co se schovává
uvnitř slov.

DENNÍ VÝZVA

Každý den osm hádanek — pro všechny hráče stejných — a k tomu Otázka dne
o češtině. Za dohranou várku padá inkoust, kterým se platí nápovědy.

HRA S PŘÁTELI

Vyzvi kamaráda podle přezdívky. Voština se hraje naráz a slova se v ní
kradou: patří tomu, kdo je odevzdá dřív, a soupeři pak zmizí pod rukama.
Vetřelec se hraje na tři kola a čekat na sebe nemusíte — rozhodne trefa
a čas.

VĚHLAS, HODNOSTI, OCENĚNÍ

Body ze všech her se sčítají do věhlasu a ten posouvá hodnost. Je jich
osmapadesát, od Nováčka po Nesmrtelného písaře, a každá má vlastní ražený
odznak. K tomu přes dvě stě ocenění za věci, na které se přijde jen hraním.

CO HRA NEDĚLÁ

Žádné reklamy. Žádné nákupy. Žádné měření návštěvnosti ani sledování.
Nechce polohu, kontakty ani fotky. Hraje se i bez signálu — celá hra
i s hádankami se stáhne do telefonu.
```

---

## Bezpečnost dat (Data safety)

Hra shromažďuje data **jen tehdy, když si hráč zvolí přezdívku a začne hrát
souboje**. Bez toho neopustí telefon nic.

| Otázka | Odpověď |
|---|---|
| Shromažďuje aplikace data? | **Ano** |
| Šifruje se přenos? | **Ano** (HTTPS) |
| Může uživatel požádat o smazání dat? | **Ano**, přímo v aplikaci i e‑mailem |
| Sdílí se data s třetími stranami? | **Ne** (Google Firebase je zpracovatel, ne příjemce) |
| Jsou data povinná? | **Ne** — bez přezdívky se dá hrát všechno kromě soubojů |

Typy dat k zaškrtnutí:

| Typ | Sbírá se | Sdílí se | Povinné | Účel |
|---|---|---|---|---|
| ID uživatele (anonymní id z Firebase) | Ano | Ne | Ne | Funkce aplikace |
| Jiný obsah vytvořený uživatelem (přezdívka) | Ano | Ne | Ne | Funkce aplikace |
| Herní aktivita (skóre, výsledky kol) | Ano | Ne | Ne | Funkce aplikace |

**Nezaškrtávat:** poloha, kontakty, zprávy, fotky, zdraví, finance, prohlížení
webu, reklamní ID. Nic z toho hra nemá.

---

## Hodnocení obsahu (IARC dotazník)

| Otázka | Odpověď |
|---|---|
| Násilí | Ne |
| Sexuální obsah | Ne |
| Vulgarita | Ne |
| Drogy, alkohol, tabák | Ne |
| Hazard nebo simulace hazardu | Ne |
| Strašidelný obsah | Ne |
| Nákupy v aplikaci | Ne |
| Sdílení polohy | Ne |
| Sdílení osobních údajů mezi uživateli | **Ano** — hráči vidí přezdívky ostatních |
| Uživatelé spolu mohou komunikovat | **Ano, omezeně** — jen přezdívkou, žádný chat |
| Obsah vytvářený uživateli | **Ano** — přezdívky |
| Je obsah moderován? | **Ano** — filtr při zadání, nahlášení a blokování v aplikaci |

Očekávané hodnocení: **PEGI 3 / Everyone**, případně o stupeň výš kvůli
interakci mezi uživateli.

---

## Uživatelský obsah — čím se to obhájí

Play se u aplikací s obsahem od uživatelů ptá, jak se řeší závadné jméno.
Hra má tohle:

1. **Filtr při zabírání přezdívky** (`src/game/nickCheck.ts`) — vulgarismy,
   nadávky, nenávistné výrazy a jména vydávající se za obsluhu, včetně obměn
   s číslicemi a zdvojenými písmeny. Závadné jméno se nezabere, takže ho
   nikdo neuvidí.
2. **Nahlášení** — u výsledku kola, u konce souboje i u došlé výzvy. Hlášení
   jde do databáze, kam se dá jen zapisovat; čte je obsluha.
3. **Blokování** — děje se spolu s nahlášením. Zablokovaný hráč se neobjeví
   ani jako náhodný soupeř, ani mezi výzvami. Odblokovat jde v nabídce
   Hra s přáteli.
4. **Žádný chat.** Hráči si nemohou poslat text — jediné, co po sobě vidí,
   je přezdívka a skóre.

---

## Snímky obrazovky

`node tools/play-assets.mjs` vyrobí do `play/`:

| Soubor | Co je na něm |
|---|---|
| `1-menu.png` | Nabídka her, denní výzva, Hra s přáteli |
| `2-vostina.png` | Rozehraná Voština |
| `3-retez.png` | Rozehraný Řetěz |
| `4-vetrelec.png` | Vetřelec — pětice slov |
| `5-detektiv.png` | Detektiv — spis o slově |
| `6-hodnosti.png` | Žebříček hodností s odznaky |
| `7-souboje.png` | Hra s přáteli |
| `feature-1024x500.png` | Hlavní grafika |

Ikona do obchodu (512×512) je `public/icons/icon-512.png`.

Play chce aspoň dva telefonní snímky; sedm je lepší, protože v obchodě se
listuje a osm her se na dvou obrázcích ukázat nedá.

---

## Než odešleš ke schválení — kontrolní seznam

- [ ] Ověřená totožnost v Play Console
- [ ] Uzavřený test: 12 testerů, 14 dní souvisle
- [ ] `assetlinks.json` na kořeni domény, ověření prochází
- [ ] V telefonu se po spuštění **neukazuje adresní řádek**
- [ ] Odkaz na zásady ochrany soukromí funguje z obchodu i z aplikace
- [ ] Mazání dat vyzkoušené na skutečném zařízení
- [ ] Nahlášení a blokování vyzkoušené mezi dvěma telefony
- [ ] Hra funguje v letadlovém režimu (offline)
- [ ] Systémové tlačítko zpět nezavírá hru uprostřed kola
