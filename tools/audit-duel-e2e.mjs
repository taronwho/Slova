/**
 * Souboj dvou hráčů odehraný celý, proti skutečné databázi.
 *
 * Databáze projektu je z vývojového stroje za bránou, takže se souboje
 * nedaly vyzkoušet a chyby se musely hádat z hlášek na snímcích. Tenhle
 * audit si pustí **emulátor Firebase se skutečnými pravidly** (`tools/emu.sh`)
 * a odehraje proti němu celou cestu ve dvou prohlížečích naráz:
 *
 *   1. oba si zaberou přezdívku,
 *   2. jeden vyzve druhého,
 *   3. výzva doopravdy dorazí,
 *   4. soupeř ji přijme a souboj se rozehraje.
 *
 * Je to jediné místo, kde se dá ověřit, že spolu hra a pravidla databáze
 * doopravdy mluví — všechno ostatní se dá jen odhadnout.
 *
 * Spuštění:  npm run audit:duel:e2e
 * (Sestavení pro emulátor a jeho start si skript udělá sám.)
 */

import { chromium } from 'playwright'

import { waitReady } from './_ui.mjs'

const APP = process.env.EMU_URL ?? 'http://localhost:4174/'
const CHROME = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome'

const problems = []
const check = (ok, msg) => {
  console.log(`  ${ok ? '✓' : '✗'} ${msg}`)
  if (!ok) problems.push(msg)
}

/*
 * Přezdívky pro tenhle běh.
 *
 * Emulátor si data drží, dokud běží, a zabraná přezdívka patří napořád
 * tomu, kdo ji zabral. Kdyby se jména opakovala, druhý běh by narazil sám
 * na sebe a hlásil „tuhle přezdívku už někdo má" — což by byla pravda,
 * jen ne ta, kterou chceme měřit.
 */
const beh = Date.now().toString(36).slice(-5)
const VYZYVATEL = `vyzyva${beh}`
const SOUPER = `souper${beh}`

/** Co vyzývatel viděl v jednotlivých kolech — soupeř to musí mít stejné. */
const vyzyvatelovaKola = []

const browser = await chromium.launch({ executablePath: CHROME })

/** Jeden hráč = vlastní prohlížeč, vlastní úložiště, vlastní přihlášení. */
async function hrac(prezdivka) {
  const context = await browser.newContext({
    viewport: { width: 412, height: 915 },
    deviceScaleFactor: 2,
    isMobile: true,
    hasTouch: true,
    locale: 'cs-CZ',
  })
  const page = await context.newPage()
  page.on('pageerror', (chyba) => problems.push(`${prezdivka}: ${chyba.message.slice(0, 120)}`))
  page.on('console', (m) => {
    if (m.type() === 'error') console.log(`    [${prezdivka}] ${m.text().slice(0, 220)}`)
  })
  await page.addInitScript(() => {
    const all = (v) => ({
      chain: v, hive: v, tower: v, gallows: v,
      detective: v, tetris: v, quotes: v, intruder: v,
    })
    localStorage.setItem(
      'slova.profile.v1',
      JSON.stringify({ version: 3, guideSeen: true, tutorialSeen: all(true), fame: 1200 }),
    )
  })
  await page.goto(APP, { waitUntil: 'networkidle' })
  await waitReady(page)
  await page.locator('.friends-entry, .btn', { hasText: /přáteli/i }).first().click()
  await page.locator('.friends').waitFor({ timeout: 15000 })
  return { context, page, prezdivka }
}

/** Zabere přezdívku a počká, až se to povede. */
async function zaberPrezdivku({ page, prezdivka }) {
  await page.locator('.friends-claim input').first().fill(prezdivka)
  await page.locator('.friends-claim .btn').first().click()
  await page.locator('.friends-me').waitFor({ timeout: 40000 }).catch(() => undefined)
  const hotovo = await page.locator('.friends-nick').innerText().catch(() => '')
  const potiz = await page.locator('.duel-problem').first().innerText().catch(() => '')
  check(
    hotovo.trim() === prezdivka,
    `${prezdivka}: přezdívka zabraná (${hotovo || 'nezabraná'}${potiz ? `, hláška: „${potiz}"` : ''})`,
  )
}

console.log('DVA HRÁČI SI ZABEROU PŘEZDÍVKU')
const jedna = await hrac(VYZYVATEL)
const druha = await hrac(SOUPER)
await zaberPrezdivku(jedna)
await zaberPrezdivku(druha)

console.log('\nVÝZVA DOJDE A DÁ SE PŘIJMOUT')
await jedna.page.locator('.friends .btn', { hasText: /^Vyzvat/ }).first().click()
await jedna.page.locator('.sheet').waitFor({ timeout: 10000 })
// Vetřelec: hraje se na tři kola a nečeká se, až bude soupeř u telefonu.
await jedna.page.locator('button.duel-pick', { hasText: 'Vetřelec' }).click()
await jedna.page.locator('.sheet input').fill(SOUPER)
await jedna.page.locator('.sheet .btn-primary').click()

// Vyzývateli se má souboj rovnou rozehrát.
const deska = await jedna.page
  .locator('.duel-game .intruder-words')
  .waitFor({ timeout: 60000 })
  .then(() => true)
  .catch(() => false)
const potiz = await jedna.page.locator('.duel-problem').first().innerText().catch(() => '')
check(deska, `vyzývateli se souboj rozehrál${potiz ? ` (hláška: „${potiz}")` : ''}`)
if (deska) {
  const slov = await jedna.page.locator('.intruder-word').count()
  check(slov === 5, `na desce je pětice slov (${slov})`)
}

// Soupeři má výzva dorazit sama, bez obnovení stránky.
const vyzva = druha.page.locator('.duel-strip.challenge').first()
const dosla = await vyzva
  .waitFor({ timeout: 60000 })
  .then(() => true)
  .catch(() => false)
if (dosla) {
  const komu = await vyzva.innerText().catch(() => '')
  check(komu.toLowerCase().includes(VYZYVATEL), `výzva je od správného hráče (${komu.split('\n')[0]})`)
}
check(dosla, 'soupeři dorazila výzva do Hry s přáteli')

if (dosla) {
  const prijmout = vyzva.locator('.duel-strip-go')
  if (await prijmout.isVisible().catch(() => false)) {
    await prijmout.click()
    const rozehrano = await druha.page
      .locator('.duel-game .intruder-words')
      .waitFor({ timeout: 60000 })
      .then(() => true)
      .catch(() => false)
    check(rozehrano, 'soupeř výzvu přijal a souboj se mu rozehrál')
  } else {
    check(false, 'u došlé výzvy chybí tlačítko k přijetí')
  }
}

console.log('\nERB SOUPEŘE JE VIDĚT UŽ PŘI HŘE')
/*
 * V souboji je jméno soupeře jediné, co o něm hráč ví, a to je málo.
 * U přezdívky proto stojí **erb soubojové hodnosti** a musí být vidět sám
 * od sebe — dřív se načítal až na ťuknutí, takže při hře tam nebyl vůbec.
 *
 * Hodnost z profilu se ukazuje jen v otevřené kartě: věhlas se sbírá
 * v denních kolech, kde soupeř žádný není, a do souboje proto nemluví.
 */
{
  const cip = jedna.page.locator('.duel-game .rival-chip').first()
  const jeCip = await cip.waitFor({ timeout: 20000 }).then(() => true).catch(() => false)
  check(jeCip, 'u přezdívky soupeře je čip')
  if (jeCip) {
    const erb = await cip
      .locator('.duel-crest')
      .waitFor({ timeout: 20000 })
      .then(() => true)
      .catch(() => false)
    check(erb, 'erb soubojové hodnosti je vidět bez ťuknutí')
    check(
      (await cip.locator('.rank-badge').count()) === 0,
      'a hodnost z profilu se do souboje neplete',
    )

    // Ťuknutím se otevře karta se jménem hodnosti a bilancí.
    await cip.click()
    const karta = await jedna.page
      .locator('.rival-sheet')
      .waitFor({ timeout: 20000 })
      .then(() => true)
      .catch(() => false)
    check(karta, 'ťuknutím se otevře karta hráče')
    if (karta) {
      const list = jedna.page.locator('.rival-sheet')
      const text = await list.innerText()
      check((await list.locator('.duel-crest').count()) > 0, 'karta vede erbem soubojové hodnosti')
      check(/Výhry/i.test(text), 'a bilancí soubojů')
      check(/Mimo souboje/i.test(text), 'a teprve dole hodností z profilu')
      check(
        (await list.locator('.rival-offline .rank-badge').count()) > 0,
        'i s jejím odznakem',
      )
      await jedna.page.locator('.rival-sheet .btn', { hasText: 'Zavřít' }).click()
    }
  }
}

console.log('\nOBA HRÁČI MAJÍ TUTÉŽ SADU OTÁZEK')
/*
 * Tohle je ta nejzákladnější podmínka souboje a hráč nahlásil, že neplatila:
 * v jednom zápase odpovídal každý na něco jiného. Příčina byla v datech —
 * pětice se do zápasu zapisovaly pořadovým číslem (`i-0000`), jenže ta se
 * při každém přestavění sady přeházela. Dva telefony s různou verzí hry si
 * pod týmž číslem našly jinou pětici. Id jsou teď odvozená z obsahu.
 */
{
  const slova = async (page) =>
    (await page.locator('.intruder-word').allInnerTexts()).map((t) => t.trim())
  const moje = await slova(jedna.page)
  const jeho = await slova(druha.page)
  check(moje.length === 5 && jeho.length === 5, `oba mají pětici (${moje.length} : ${jeho.length})`)
  check(
    moje.join(' ') === jeho.join(' '),
    `a je to tatáž pětice · vyzývatel: ${moje.join(' ')} · soupeř: ${jeho.join(' ')}`,
  )
}

console.log('\nODEHRANÝ SOUBOJ ČEKÁ NA SOUPEŘE A JE TO VIDĚT')
/*
 * U Vetřelce si každý zahraje, kdy chce. Mezi „odehráno" a „známe výsledek"
 * tak může být klidně den — a bez výpisu to vypadalo, že se zápas ztratil.
 */
{
  const page = jedna.page
  // Tři kola: trefit nemusíme, jde o to dohrát je až do konce. Po cestě se
  // schová, co v kterém kole stálo — soupeř to pak musí mít stejné.
  vyzyvatelovaKola.length = 0
  for (let kolo = 0; kolo < 3; kolo += 1) {
    vyzyvatelovaKola.push((await page.locator('.intruder-word').allInnerTexts()).join(' '))
    await page.locator('.intruder-word').first().click()
    await page.locator('.duel-round-end .btn').click()
    await page.waitForTimeout(400)
  }
  await page.locator('.result-card').waitFor({ timeout: 20000 }).catch(() => undefined)

  /*
   * Na kartě „Odehráno" (soupeř ještě nehrál) stálo tlačítko **Odveta**,
   * což je holá nepravda: oplácet se dá až prohra, kterou zatím nikdo
   * neutrpěl.
   */
  const napis = (await page.locator('.result-actions .btn-primary').first().innerText().catch(() => '')).trim()
  check(
    napis === 'Vyzvat znovu',
    `dokud soupeř nedohrál, stojí na tlačítku „Vyzvat znovu" (${napis || 'nic'})`,
  )

  /*
   * Porovnání kol i tomu, kdo dohrál první.
   *
   * Vidí svoje tři kola i s časy a body; na straně soupeře je zatím
   * čekání. Dřív mu zůstalo jen „odehráno" a jedno číslo.
   */
  const rozbor = page.locator('.result-card .rozbor')
  const jeRozbor = await rozbor.waitFor({ timeout: 20000 }).then(() => true).catch(() => false)
  check(jeRozbor, 'první hráč vidí rozpis svých kol')
  if (jeRozbor) {
    const mych = await rozbor.locator('.rozbor-dvojice > .rozbor-bunka:not(.prazdna)').count()
    const cekacich = await rozbor.locator('.rozbor-bunka.prazdna').count()
    check(mych === 3, `jsou v něm tři odehraná kola (${mych})`)
    check(cekacich === 3, `a u soupeře se zatím čeká (${cekacich})`)
    const text = (await rozbor.innerText()).replace(/\s+/g, ' ')
    check(/\d+[,.]?\d*\s*s/.test(text), 'u kol je čas')
    check(/[+]\d+|(^|\s)0(\s|$)/.test(text), 'a body za kolo')
    check(
      (await rozbor.locator('.rozbor-side .duel-crest').count()) === 2,
      'a nad tím stojí dva erby proti sobě',
    )
  }

  await page.locator('.result-actions .btn', { hasText: 'Zpět do menu' }).click()
  await page.locator('.friends-entry, .btn', { hasText: /přáteli/i }).first().click()
  await page.locator('.friends').waitFor({ timeout: 15000 })

  const cekani = page.locator('.duel-strip.pending').first()
  const jeVidet = await cekani.waitFor({ timeout: 40000 }).then(() => true).catch(() => false)
  check(jeVidet, 'v Hře s přáteli je vidět, na koho se čeká')
  if (jeVidet) {
    const text = (await cekani.innerText()).replace(/\s+/g, ' ')
    check(text.includes(SOUPER), `a je u toho jméno soupeře (${text})`)
  }
}

console.log('\nSOUPEŘ DOHRAJE A OBA VIDÍ VYHODNOCENÍ')
{
  // Soupeř si odehraje svoje tři kola — a musí u toho vidět tytéž pětice.
  const souperovaKola = []
  for (let kolo = 0; kolo < 3; kolo += 1) {
    souperovaKola.push((await druha.page.locator('.intruder-word').allInnerTexts()).join(' '))
    await druha.page.locator('.intruder-word').first().click()
    await druha.page.locator('.duel-round-end .btn').click()
    await druha.page.waitForTimeout(400)
  }
  check(
    souperovaKola.join(' | ') === vyzyvatelovaKola.join(' | '),
    `všechna tři kola sedí oběma\n      vyzývatel: ${vyzyvatelovaKola.join(' | ')}\n      soupeř:    ${souperovaKola.join(' | ')}`,
  )
  await druha.page.locator('.result-card').waitFor({ timeout: 20000 }).catch(() => undefined)

  /*
   * Kdo hraje druhý, má obě strany rovnou: svoje kolo proti soupeřovu,
   * s časy a body u obou.
   */
  const rozbor = druha.page.locator('.result-card .rozbor')
  const jeRozbor = await rozbor.waitFor({ timeout: 20000 }).then(() => true).catch(() => false)
  check(jeRozbor, 'druhý hráč vidí celé porovnání')
  if (jeRozbor) {
    const bunek = await rozbor.locator('.rozbor-bunka:not(.prazdna)').count()
    check(bunek === 6, `obě strany mají svoje tři kola (${bunek} z 6)`)
    check(
      (await rozbor.locator('.rozbor-bunka.prazdna').count()) === 0,
      'a nikde se už nečeká',
    )
    const nadpis = (await rozbor.locator('h2').innerText()).trim()
    check(
      ['Vyhrál jsi!', 'Prohrál jsi', 'Remíza'].includes(nadpis),
      `nahoře stojí výsledek (${nadpis})`,
    )
    const hlaska = (await rozbor.locator('.rozbor-line').innerText()).trim()
    check(hlaska.length > 0, `a pod ním hláška („${hlaska}")`)
  }

  const tlacitkoSoupere = (await druha.page.locator('.result-actions .btn-primary').first().innerText().catch(() => '')).trim()
  check(tlacitkoSoupere === 'Odveta', `a u dohraného souboje je „Odveta" (${tlacitkoSoupere || 'nic'})`)

  await druha.page.locator('.result-actions .btn', { hasText: 'Zpět do menu' }).click()
  await druha.page.locator('.friends-entry, .btn', { hasText: /přáteli/i }).first().click()
  await druha.page.locator('.friends').waitFor({ timeout: 15000 })
  const archiv = druha.page.locator('.duel-strip.past').first()
  const jeArchiv = await archiv.waitFor({ timeout: 20000 }).then(() => true).catch(() => false)
  check(jeArchiv, 'odehraný souboj zůstal v přehledu')
  if (jeArchiv) {
    const radek = (await archiv.innerText()).replace(/\s+/g, ' ')
    check(radek.includes(VYZYVATEL), `a je v něm soupeř i skóre (${radek})`)

    // Ťuknutím se otevře totéž porovnání, i po týdnech.
    await archiv.click()
    const okno = druha.page.locator('.rozbor-sheet')
    const jeOkno = await okno.waitFor({ timeout: 10000 }).then(() => true).catch(() => false)
    check(jeOkno, 'a dá se z něj otevřít porovnání')
    if (jeOkno) {
      const bunek = await okno.locator('.rozbor-bunka:not(.prazdna)').count()
      check(bunek === 6, `v archivu zůstala kola obou stran (${bunek} z 6)`)
      await okno.locator('.btn', { hasText: 'Zavřít' }).click()
    }
  }
}

console.log('\nVÝSLEDEK SE PŘIPÍŠE SÁM, BEZ ŤUKNUTÍ NA OZNÁMENÍ')
/*
 * Tohle hlásil hráč: souboj byl rozhodnutý, ale do bilance se nezapsal,
 * dokud si neťukl na oznámení o dohraném souboji. Připisovat výsledek až
 * za odměnu za ťuknutí je nesmysl — rozhodnuto je rozhodnuto.
 *
 * Zkouší se to na prvním hráči: ten odešel do menu dřív, než soupeř
 * dohrál, takže se výsledek dozví až při návratu k aplikaci.
 */
{
  const page = jedna.page
  await page.locator('.result-actions .btn', { hasText: 'Zpět do menu' }).first().click().catch(() => undefined)
  await page.goto(APP, { waitUntil: 'networkidle' })
  await waitReady(page)
  await page.locator('.friends-entry, .btn', { hasText: /přáteli/i }).first().click()
  await page.locator('.friends').waitFor({ timeout: 15000 })

  // Bilance se má srovnat sama, ještě než na cokoli sáhneme.
  const zapsano = await page
    .waitForFunction(
      () => {
        const text = document.querySelector('.friends-tally')?.textContent ?? ''
        return !/Zatím žádný souboj/.test(text) && /\d/.test(text)
      },
      undefined,
      { timeout: 40000 },
    )
    .then(() => true)
    .catch(() => false)
  const bilance = (await page.locator('.friends-tally').innerText().catch(() => '')).replace(/\s+/g, ' ')
  check(zapsano, `výsledek je v bilanci bez ťuknutí (${bilance || 'prázdná'})`)

  const archiv = page.locator('.duel-strip.past').first()
  const jeArchiv = await archiv.waitFor({ timeout: 20000 }).then(() => true).catch(() => false)
  check(jeArchiv, 'a souboj sám od sebe spadl do odehraných')

  // Ťuknutí na oznámení „Dohráno" otevře porovnání, ne teprve zápis.
  const zprava = page.locator('.duel-strip.report').first()
  if (await zprava.isVisible().catch(() => false)) {
    await zprava.click()
    const okno = await page.locator('.rozbor-sheet').waitFor({ timeout: 10000 }).then(() => true).catch(() => false)
    check(okno, 'ťuknutím na oznámení se otevře porovnání')
    if (okno) await page.locator('.rozbor-sheet .btn', { hasText: 'Zavřít' }).click()
  }

  // A dvakrát se tentýž souboj do bilance zapsat nesmí.
  const pocet = await page.locator('.duel-strip.past').count()
  check(pocet === 1, `souboj je v archivu jen jednou (${pocet})`)
  const cisla = (bilance.match(/\d+/g) ?? []).map(Number)
  check(
    cisla.reduce((a, b) => a + b, 0) === 1,
    `a v bilanci je započítaný jen jednou (${bilance})`,
  )
}

console.log('\nNEZNÁMÁ PŘEZDÍVKA SE POZNÁ HNED, NE AŽ PO LHŮTĚ')
/*
 * Přezdívka, kterou nikdo nezabral. Hra ji má poznat rovnou — čte se
 * větev, která v databázi není, a to není chyba, to je odpověď „nic tu
 * není". Kdyby se místo toho čekalo do vypršení lhůty, vypadalo by
 * překlepnuté jméno jako výpadek serveru.
 */
{
  const strankaJedna = jedna.page
  await strankaJedna.locator('.result-actions .btn', { hasText: 'Zpět do menu' }).first().click().catch(() => undefined)
  await strankaJedna.goto(APP, { waitUntil: 'networkidle' })
  await waitReady(strankaJedna)
  await strankaJedna.locator('.friends-entry, .btn', { hasText: /přáteli/i }).first().click()
  await strankaJedna.locator('.friends').waitFor({ timeout: 15000 })
  await strankaJedna.locator('.friends .btn', { hasText: /^Vyzvat/ }).first().click()
  await strankaJedna.locator('.sheet').waitFor({ timeout: 10000 })
  await strankaJedna.locator('.sheet input').fill('nikdotakovyneni')

  const start = Date.now()
  await strankaJedna.locator('.sheet .btn-primary').click()
  await strankaJedna
    .waitForFunction(
      () => Boolean(document.querySelector('.duel-problem')?.textContent?.trim()),
      undefined,
      { timeout: 40000 },
    )
    .catch(() => undefined)
  const trvalo = Math.round((Date.now() - start) / 1000)
  const hlaska = await strankaJedna.locator('.duel-problem').first().innerText().catch(() => '')
  check(/neznám/i.test(hlaska), `neznámá přezdívka se pozná (${trvalo} s, „${hlaska}")`)
  check(trvalo < 10, `a pozná se hned, ne až po lhůtě (${trvalo} s)`)
}

console.log('\nPO VÝPADKU SÍTĚ SE TO MUSÍ VZPAMATOVAT')
/*
 * Tohle hlásil hráč: jednou večer výzva projde, podruhé ne, a pomůže až
 * zavření celé aplikace. Přesně tak se chová klient, který si po výpadku
 * sítě nesáhne pro nové spojení. Zkouší se proto obojí: že se hra při
 * odpojení ozve (a nezůstane viset) a hlavně že po návratu sítě zase
 * funguje, bez restartu.
 */
{
  const page = jedna.page
  const vyzvi = async () => {
    await page.locator('.friends .btn', { hasText: /^Vyzvat/ }).first().click()
    await page.locator('.sheet').waitFor({ timeout: 10000 })
    await page.locator('.sheet input').fill(SOUPER)
    await page.locator('.sheet .btn-primary').click()
  }
  const dojdiDoMenu = async () => {
    await page.goto(APP, { waitUntil: 'networkidle' }).catch(() => undefined)
    await waitReady(page)
    await page.locator('.friends-entry, .btn', { hasText: /přáteli/i }).first().click()
    await page.locator('.friends').waitFor({ timeout: 20000 })
  }

  await dojdiDoMenu()
  await jedna.context.setOffline(true)
  await vyzvi()
  const ozvalo = await page
    .waitForFunction(
      () => Boolean(document.querySelector('.duel-problem')?.textContent?.trim()),
      undefined,
      { timeout: 70000 },
    )
    .then(() => true)
    .catch(() => false)
  const hlaska = await page.locator('.duel-problem').first().innerText().catch(() => '')
  check(ozvalo, `bez sítě se hra ozve místo mlčení („${hlaska}")`)

  // A teď to hlavní: síť je zpátky a hra musí zase mluvit se serverem —
  // bez zavření aplikace. Měří se to tím, co má hráč po ruce sám: rozborem
  // pod chybou, který se ptá stejnou cestou jako hra.
  await jedna.context.setOffline(false)
  await page.waitForTimeout(3000)
  await page.locator('.duel-rozbor .btn').first().click()
  await page.locator('.duel-rozbor .check-list').waitFor({ timeout: 120000 }).catch(() => undefined)
  const radky = await page.locator('.duel-rozbor .check-list li').allInnerTexts().catch(() => [])
  for (const radek of radky) console.log(`    ${radek.replace(/\s+/g, ' ')}`)
  const spojeni = radky.find((r) => r.includes('Spojení hry')) ?? ''
  check(
    spojeni.includes('navázáno'),
    `po návratu sítě se spojení obnoví bez restartu (${spojeni.replace(/\s+/g, ' ') || 'nezměřeno'})`,
  )
}

console.log(problems.length ? `\nNÁLEZY: ${problems.length}` : '\nVŠE PROŠLO')
for (const one of problems) console.log(`  • ${one}`)
await browser.close()
process.exit(problems.length > 0 ? 1 : 0)
