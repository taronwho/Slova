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

## Pořadí, na kterém záleží

Ověření domény **nejde dokončit dřív, než je balíček nahraný v Play Console**.
Do `assetlinks.json` totiž patří otisk klíče, kterým je aplikace **doopravdy**
podepsaná — a při zapnutém Play App Signing (což je doporučený stav)
podepisuje výsledek Google vlastním klíčem, jehož otisk se dozvíš až
z konzole. Kroky proto jdou takhle:

1. postavit balíček
2. nahrát `.aab` do Play Console a přijmout Play App Signing
3. **teprve pak** opsat otisk z konzole do `assetlinks.json` a nasadit ho
4. v telefonu ověřit, že nahoře není adresní řádek

Kdo dá `assetlinks.json` na web dřív s otiskem vlastního klíče, dostane tiše
nefunkční ověření a bude ho hledat v úplně jiných místech.

---

## 1. Postavení balíčku

### Snadná cesta: GitHub Actions

V repozitáři je workflow **`.github/workflows/android.yml`**, který balíček
postaví sám — běžci GitHubu mají JDK i Android SDK předinstalované, takže se
na vlastní počítač nemusí instalovat vůbec nic.

Jednorázově je potřeba uložit podpisový klíč do
*Settings → Secrets and variables → Actions*:

| Tajemství | Co to je |
|---|---|
| `ANDROID_KEYSTORE_BASE64` | soubor `android.keystore` zakódovaný base64 |
| `ANDROID_KEYSTORE_PASSWORD` | heslo k němu |

Klíč se do repozitáře **nikdy nekommituje**. Kdo ho ještě nemá, vyrobí si ho:

```bash
keytool -genkeypair -v -keystore android.keystore -alias slova \
  -keyalg RSA -keysize 4096 -validity 10000
base64 -w0 android.keystore    # tohle jde do ANDROID_KEYSTORE_BASE64
```

Pak stačí *Actions → Androidí balíček → Run workflow*, zadat číslo verze
a po pár minutách si stáhnout `app-release-bundle.aab` (do obchodu)
a `app-release-signed.apk` (na vyzkoušení přes `adb install`).

Bez těch tajemství se build nezastaví — vyrobí si klíč na jedno použití
a výsledek pojmenuje `ZKUSEBNI-nepouzivat`. Slouží k tomu, aby šlo ověřit,
že se všechno sestaví; do obchodu takový balíček nepatří, protože příští
běh by ho podepsal jinak a aplikace by nešla aktualizovat.

### Ruční cesta

Když je potřeba stavět lokálně, je nutné mít **JDK 17**, **Android SDK**
(stačí `cmdline-tools`) a **Node 18+**:

```bash
npm install -g @bubblewrap/cli
mkdir ~/slova-android && cd ~/slova-android
cp /cesta/k/Slova/tools/android/twa-manifest.json .
bubblewrap init --manifest ./twa-manifest.json
bubblewrap build
```

## 2. Podpisový klíč — co s ním

Klíč je pečeť aplikace. **Zálohuj ho i s heslem**: bez něj by aplikace
nešla aktualizovat.

Jediná úleva je **Play App Signing**: Google si podepsaný balíček podepíše
ještě jednou vlastním klíčem, který drží on. Ten tvůj je pak jen *nahrávací*
klíč, a kdyby se ztratil, Google umí vystavit nový. Proto ho přijmi hned při
prvním nahrání.

## 3. Ověření domény — `assetlinks.json`

Otisk vezmi z Play Console: *Nastavení → Integrita aplikace → Podpisový
certifikát*, hodnotu **SHA-256**. (Bez Play App Signing by to byl výstup
`bubblewrap fingerprint list`, respektive `keytool -list -v`.)

Vlož ho místo `SEM_PATŘÍ_OTISK` do souboru
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
proto, že se plete otisk klíče, kterým je aplikace doopravdy podepsaná.

## 4. Vydání

1. V Play Console založ aplikaci, nahraj `.aab`.
2. Vyplň dotazníky — texty a odpovědi jsou v `tools/play-listing.md`.
3. Grafiku a snímky vygeneruje `node tools/play-assets.mjs` do složky `play/`.
4. Pusť uzavřený test, sežeň dvanáct testerů a nech je tam čtrnáct dní.
5. Teprve pak jde požádat o produkci.

## 5. Aktualizace hry

Obsah se aktualizuje sám nasazením na Pages — nový balík kvůli tomu není
potřeba. Nový `.aab` dělej jen tehdy, když se mění něco v samotné slupce
(ikona, jméno, cílová úroveň API). Nezapomeň zvednout `appVersionCode`;
ve workflow se zadává při spuštění, takže se kvůli němu nemusí nic
kommitovat.

Cílovou úroveň API zvedá Google každý srpen; když ti Play Console začne hlásit,
že je balík zastaralý, stačí přegenerovat s novějším Bubblewrapem.
