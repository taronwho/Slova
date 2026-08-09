# Zabalení hry pro Google Play

Slova jsou webová hra a do obchodu jdou jako **Trusted Web Activity** (TWA) —
tenká androidí slupka, která uvnitř spustí prohlížeč bez adresního řádku
a načte hru z webu. Balík má pár set kilobajtů a **každé nasazení na Pages je
zároveň aktualizací aplikace**, bez schvalování a bez čekání.

Aby slupka schovala adresní řádek, musí web dokázat, že k té aplikaci patří.
Dělá se to souborem `assetlinks.json` na **kořeni domény** — a právě v tom je
u GitHub Pages háček, viz krok 3.

Tenhle adresář drží konfiguraci; samotný androidí projekt se generuje a do
repozitáře nepatří (je to pár set megabajtů závislostí).

---

## Co je potřeba mít

* **JDK 17** a **Android SDK** (stačí `cmdline-tools`; Bubblewrap si zbytek
  doinstaluje sám a nabídne to při prvním spuštění)
* **Node 18+**
* Účet v Play Console s ověřenou totožností

---

## 1. Bubblewrap

```bash
npm install -g @bubblewrap/cli
```

## 2. Vygenerování projektu

V prázdném adresáři **mimo tenhle repozitář** (třeba `~/slova-android`):

```bash
cp /cesta/k/Slova/tools/android/twa-manifest.json .
bubblewrap init --manifest ./twa-manifest.json
```

Bubblewrap se zeptá na podpisový klíč. Nech si vytvořit nový a **zálohuj ho**
i s heslem: bez něj se aplikace už nikdy nedá aktualizovat a nezachrání to
ani Google.

```bash
bubblewrap build
```

Vypadne `app-release-bundle.aab` (do obchodu) a `app-release-signed.apk`
(na vyzkoušení v telefonu přes `adb install`).

## 3. Ověření domény — `assetlinks.json`

Vypiš otisk podpisového klíče:

```bash
bubblewrap fingerprint list
```

Vezmi hodnotu **SHA-256** a vlož ji místo `SEM_PATŘÍ_OTISK` do souboru
`root-site/.well-known/assetlinks.json` vedle tohohle návodu.

Ten soubor pak musí být dostupný na adrese:

```
https://taronwho.github.io/.well-known/assetlinks.json
```

Pozor na to, že je to **kořen domény**, ne adresář hry. Hra leží
v `taronwho.github.io/Slova/`, ale ověřuje se `taronwho.github.io`. Musíš tedy
založit repozitář pojmenovaný přesně **`taronwho.github.io`** — jméno musí
sedět na písmeno, jinak z něj GitHub neudělá kořen domény.

Obsah toho repozitáře je připravený ve složce **`root-site/`**. Zkopíruj ji
celou včetně skrytých souborů:

```bash
# v prázdném naklonovaném repozitáři taronwho.github.io
cp -r /cesta/k/Slova/tools/android/root-site/. .
git add -A && git commit -m "Ověření aplikace Slova" && git push
```

Pak v jeho nastavení zapni **Settings → Pages → Deploy from a branch → main**.

> **Past, na kterou se naráží nejčastěji:** GitHub Pages prohání obsah přes
> Jekyll a ten **zahazuje všechno, co začíná tečkou** — tedy i celou složku
> `.well-known/`. Soubor by se nahrál, ale na webu by nebyl a ověření by
> mlčky selhalo. Proto je ve složce prázdný soubor `.nojekyll`; bez něj to
> nefunguje. Ověř si po nasazení, že adresa výš opravdu vrací ten JSON,
> a ne stránku s chybou 404.

Prázdná adresa `taronwho.github.io` by vypadala jako zapomenutý projekt,
takže je ve složce i drobný rozcestník `index.html` s odkazem do hry.

> **Lepší cesta: vlastní doména.** Ověřuješ tím celou svoji github.io doménu,
> o kterou se dělí všechny tvoje projekty. S vlastní doménou (třeba
> `slova.cz`, nasměrovanou na Pages přes CNAME) patří ověření jen téhle hře,
> adresa vypadá jako hra a ne jako repozitář, a v obchodě to působí jinak.
> Když se pro ni rozhodneš, změň v `twa-manifest.json` `host`, `startUrl`,
> `fullScopeUrl` a všechny adresy ikon — a `assetlinks.json` dej na kořen té
> nové domény.

Ověření se dá zkontrolovat Googlím nástrojem:

```
https://digitalassetlinks.googleapis.com/v1/statements:list?source.web.site=https://taronwho.github.io&relation=delegate_permission/common.handle_all_urls
```

Když v telefonu vidíš nahoře adresní řádek, ověření neprošlo — nejčastěji
proto, že se plete otisk klíče, kterým je aplikace **doopravdy** podepsaná.
Pokud používáš Play App Signing (a to bys měl), podepisuje výsledek Google
vlastním klíčem a do `assetlinks.json` patří **jeho** otisk: najdeš ho
v Play Console v části *Nastavení → Integrita aplikace → Podpisový certifikát*.

## 4. Vydání

1. V Play Console založ aplikaci, nahraj `.aab`.
2. Vyplň dotazníky — texty a odpovědi jsou v `tools/play-listing.md`.
3. Grafiku a snímky vygeneruje `node tools/play-assets.mjs` do složky `play/`.
4. Pusť uzavřený test, sežeň dvanáct testerů a nech je tam čtrnáct dní.
5. Teprve pak jde požádat o produkci.

## 5. Aktualizace hry

Obsah se aktualizuje sám nasazením na Pages — nový balík kvůli tomu není
potřeba. Nový `.aab` dělej jen tehdy, když se mění něco v samotné slupce
(ikona, jméno, cílová úroveň API). Nezapomeň zvednout `appVersionCode`.

Cílovou úroveň API zvedá Google každý srpen; když ti Play Console začne hlásit,
že je balík zastaralý, stačí přegenerovat s novějším Bubblewrapem.
