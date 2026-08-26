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

console.log('\nHODNOST SOUPEŘE JE VIDĚT UŽ PŘI HŘE')
/*
 * V souboji je jméno soupeře jediné, co o něm hráč ví, a to je málo.
 * Odznak s číslem hodnosti musí být u přezdívky vidět **sám od sebe** —
 * dřív se načítal až na ťuknutí, takže při hře tam nebyl vůbec.
 */
{
  const cip = jedna.page.locator('.duel-game .rival-chip').first()
  const jeCip = await cip.waitFor({ timeout: 20000 }).then(() => true).catch(() => false)
  check(jeCip, 'u přezdívky soupeře je čip s hodností')
  if (jeCip) {
    const odznak = await cip.locator('.rank-badge').count()
    const cislo = (await cip.locator('.rival-band').innerText().catch(() => '')).trim()
    check(odznak > 0, 'odznak hodnosti je vidět bez ťuknutí')
    check(/^\d+$/.test(cislo), `a vedle něj číslo hodnosti (${cislo || 'chybí'})`)

    // Ťuknutím se otevře karta se jménem hodnosti a bilancí.
    await cip.click()
    const karta = await jedna.page
      .locator('.rival-sheet')
      .waitFor({ timeout: 20000 })
      .then(() => true)
      .catch(() => false)
    check(karta, 'ťuknutím se otevře karta hráče')
    if (karta) {
      const text = await jedna.page.locator('.rival-sheet').innerText()
      check(/hodnost/i.test(text), 'karta říká jméno hodnosti')
      check(/V soubojích/i.test(text), 'a soubojovou hodnost')
      check(/Výhry/i.test(text), 'a bilanci soubojů')
      await jedna.page.locator('.rival-sheet .btn', { hasText: 'Zavřít' }).click()
    }
  }
}

console.log('\nODEHRANÝ SOUBOJ ČEKÁ NA SOUPEŘE A JE TO VIDĚT')
/*
 * U Vetřelce si každý zahraje, kdy chce. Mezi „odehráno" a „známe výsledek"
 * tak může být klidně den — a bez výpisu to vypadalo, že se zápas ztratil.
 */
{
  const page = jedna.page
  // Tři kola: trefit nemusíme, jde o to dohrát je až do konce.
  for (let kolo = 0; kolo < 3; kolo += 1) {
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
  // Soupeř si odehraje svoje tři kola.
  for (let kolo = 0; kolo < 3; kolo += 1) {
    await druha.page.locator('.intruder-word').first().click()
    await druha.page.locator('.duel-round-end .btn').click()
    await druha.page.waitForTimeout(400)
  }
  await druha.page.locator('.result-card').waitFor({ timeout: 20000 }).catch(() => undefined)
  const vysledek = await druha.page.locator('.result-card').innerText().catch(() => '')
  check(/\d+\s*:\s*\d+/.test(vysledek.replace(/\s+/g, ' ')), 'soupeř vidí výsledek proti sobě')

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
  }
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
