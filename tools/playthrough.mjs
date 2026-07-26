/**
 * Deset odehraných kol od každého režimu — a kontrola, že se za celou dobu
 * neobjevilo slovo mimo povolené tvary.
 *
 * Slovník se ověřuje i testem nad daty (tests/data.test.ts), jenže ten čte
 * vygenerované soubory. Tenhle běh jde opačnou cestou: co doopravdy prošlo
 * přes obrazovku, ať už to hra sama vypsala (žebřík, patra, nápovědy, řešení
 * ve výsledku), nebo to přijala od hráče. Kdyby se někde do hry dostal jiný
 * seznam slov než ten ověřený, chytí se to tady.
 *
 * Kola se hrají nápovědami — hra si tím sama ukáže korektní řešení a projde
 * se celá cesta až do výsledku.
 */

import { chromium } from 'playwright'
import { readFileSync } from 'node:fs'

import { goHome, openGame, waitReady } from './_ui.mjs'

const APP_URL = process.env.URL ?? 'http://localhost:4173/'
const ROUNDS = Number(process.env.ROUNDS ?? 10)

const allowed = new Set(
  JSON.parse(readFileSync(new URL('../tests/fixtures/base-forms.json', import.meta.url))),
)

const problems = []
const seenWords = new Set()
const log = (...args) => console.log(...args)

function check(condition, message) {
  if (condition) log(`  ✓ ${message}`)
  else {
    log(`  ✗ ${message}`)
    problems.push(message)
  }
}

/** Každé slovo, které hra ukázala nebo přijala, musí být povolený tvar. */
function collect(words, where) {
  for (const raw of words) {
    const word = (raw ?? '').trim().toLowerCase()
    if (!/^[a-záčďéěíňóřšťúůýž]{3,}$/.test(word)) continue
    seenWords.add(word)
    if (!allowed.has(word)) problems.push(`${where}: nepovolený tvar „${word}"`)
  }
}

const browser = await chromium.launch({
  executablePath:
    process.env.CHROME_PATH ?? '/opt/pw-browsers/chromium-1194/chrome-linux/chrome',
})
const context = await browser.newContext({
  viewport: { width: 390, height: 844 },
  locale: 'cs-CZ',
})
const page = await context.newPage()
page.on('pageerror', (error) => problems.push(`chyba stránky: ${error.message}`))
page.on('console', (message) => {
  if (message.type() === 'error') problems.push(`console.error: ${message.text()}`)
})
await page.goto(APP_URL, { waitUntil: 'networkidle' })
  await page.locator('.splash').waitFor({ state: 'detached', timeout: 8000 }).catch(() => undefined)

async function start(mode) {
  await goHome(page)
  // Nová hra zahodí rozehrané kolo, takže se pokaždé začíná načisto.
  await openGame(page, mode)
}

/* ---------- ŘETĚZ ---------- */

async function playChain() {
  await start('chain')
  for (let guard = 0; guard < 40; guard++) {
    if (await page.locator('.result-card').isVisible().catch(() => false)) break
    const word = page.locator('.hints .btn', { hasText: 'Celé slovo' })
    if (!(await word.isEnabled().catch(() => false))) break
    await word.click()
    await page.waitForTimeout(120)
    // Nápověda slovo jen předepíše, zahrát ho musí hráč.
    await page.keyboard.press('Enter')
    await page.waitForTimeout(250)
    collect(await page.locator('.ladder .rung').allInnerTexts().then(clean), 'řetěz — žebřík')
  }
  const result = page.locator('.result-card')
  if (await result.isVisible().catch(() => false)) {
    collect(
      await result.locator('.solution-path > span').allInnerTexts().then(clean),
      'řetěz — řešení',
    )
  }
  return await result.isVisible().catch(() => false)
}

/* ---------- VOŠTINA ---------- */

async function playHive() {
  await start('hive')
  for (let i = 0; i < 8; i++) {
    await page.locator('.board-footer .btn', { hasText: 'Nápověda' }).click()
    await page.waitForTimeout(120)
  }
  collect(await page.locator('.found-word').allInnerTexts().then(clean), 'voština — nalezená')
  await page.locator('.board-footer .btn', { hasText: 'Ukončit plástev' }).click()
  // Ukončení se ptá na potvrzení, ať se netrefí omylem.
  await page.locator('.sheet.confirm .btn', { hasText: 'Ukončit' }).click()
  const result = page.locator('.result-card')
  await result.waitFor({ timeout: 5000 }).catch(() => undefined)
  return await result.isVisible().catch(() => false)
}

/* ---------- VĚŽ ---------- */

async function playTower() {
  await start('tower')
  for (let guard = 0; guard < 20; guard++) {
    if (await page.locator('.result-card').isVisible().catch(() => false)) break
    const word = page.locator('.hints .btn', { hasText: 'Celé slovo' })
    if (!(await word.isEnabled().catch(() => false))) break
    await word.click()
    await page.waitForTimeout(150)
    const build = page.locator('.board-footer .btn', { hasText: 'Postavit patro' })
    if (await build.isEnabled().catch(() => false)) await build.click()
    await page.waitForTimeout(250)
    collect(await page.locator('.floor.done').allInnerTexts().then(clean), 'věž — patra')
  }
  const result = page.locator('.result-card')
  return await result.isVisible().catch(() => false)
}

function clean(texts) {
  return texts.map((t) => t.replace(/[\s\n▸·0-9]/g, ''))
}

const MODES = [
  ['ŘETĚZ', playChain],
  ['VOŠTINA', playHive],
  ['VĚŽ', playTower],
]

for (const [name, play] of MODES) {
  log(`\n${name} — ${ROUNDS} kol`)
  let finished = 0
  for (let round = 1; round <= ROUNDS; round++) {
    const done = await play()
    if (done) finished++
    else problems.push(`${name}: kolo ${round} nedošlo k výsledku`)
  }
  check(finished === ROUNDS, `dohráno ${finished}/${ROUNDS} kol`)
}

/* ---------- Pokračování v rozehraném kole ---------- */

log('\nROZEHRANÉ KOLO')
{
  // Řetěz i Věž se rozehrají a nechají rozdělané naráz — každý režim má
  // vlastní uložené kolo.
  await start('chain')
  await page.locator('.hints .btn', { hasText: 'Celé slovo' }).click()
  await page.keyboard.press('Enter')
  await page.waitForTimeout(300)
  const chainRungs = await page.locator('.ladder .rung').count()

  await goHome(page)
  await start('tower')
  await page.locator('.hints .btn', { hasText: 'Celé slovo' }).click()
  await page.waitForTimeout(150)
  await page.locator('.board-footer .btn', { hasText: 'Postavit patro' }).click()
  await page.waitForTimeout(300)
  const towerFloors = await page.locator('.floor.done').count()

  await goHome(page)
  const live = await page.locator('.mode-tile .mode-flag.live').allInnerTexts()
  check(live.length === 2, `obě rozehrané hry se nabízejí zvlášť (${JSON.stringify(live)})`)

  await page.reload({ waitUntil: 'networkidle' })
  await waitReady(page)
  check(
    (await page.locator('.mode-tile .mode-flag.live').count()) === 2,
    'nabídka přežije zavření a otevření hry',
  )

  await openGame(page, 'chain', { resume: true })
  check(
    (await page.locator('.ladder .rung').count()) === chainRungs,
    `Řetěz pokračuje tam, kde skončil (${chainRungs} článků)`,
  )

  await goHome(page)
  await openGame(page, 'tower', { resume: true })
  check(
    (await page.locator('.floor.done').count()) === towerFloors,
    `Věž pokračuje tam, kde skončila (${towerFloors} pater)`,
  )
}

/* ---------- Ovládání ---------- */

log('\nOVLÁDÁNÍ')
{
  // Vlastní okno: historie prohlížeče je prázdná stejně jako po skutečném
  // spuštění hry, takže systémové zpět měříme na tom, co zažije hráč.
  const fresh = await browser.newContext({ viewport: { width: 390, height: 844 }, locale: 'cs-CZ' })
  const page = await fresh.newPage()
  await page.goto(APP_URL, { waitUntil: 'networkidle' })
  await waitReady(page)
  await openGame(page, 'chain')
  const ladder = await page.evaluate(() => {
    const board = document.querySelector('.board').getBoundingClientRect()
    const rows = [...document.querySelectorAll('.ladder .rung')].map((r) => r.getBoundingClientRect())
    return {
      count: rows.length,
      fits: rows.every((r) => r.top >= board.top - 1 && r.bottom <= board.bottom + 1),
    }
  })
  check(ladder.count >= 3, `řetěz ukáže start, rozepsané slovo i cíl (${ladder.count} řady)`)
  check(ladder.fits, 'všechny řady žebříku se vejdou do hrací plochy')

  await page.locator('.board-footer .btn', { hasText: 'Vzdát kolo' }).click()
  check(await page.locator('.sheet.confirm').isVisible(), 'vzdání se nejdřív zeptá')
  await page.locator('.sheet.confirm .btn', { hasText: 'Zrušit' }).click()
  check(await page.locator('.ladder').isVisible(), 'zrušené vzdání nechá kolo běžet')

  // Systémové zpět (na Androidu gesto) nesmí zavřít celou hru. Chvíli počkat:
  // zavřené potvrzení po sobě uklízí vlastní záznam v historii.
  await page.waitForTimeout(500)
  await page.goBack()
  await page.waitForTimeout(400)
  check(
    await page.locator('h1:has-text("Vyber si hru")').isVisible(),
    'zpět ze hry vede do menu, ne ven z aplikace',
  )
  await page.locator('.mode-tile[data-mode="hive"]').click()
  await page.locator('.sheet').waitFor()
  await page.goBack()
  await page.waitForTimeout(300)
  check(!(await page.locator('.sheet').isVisible()), 'zpět zavře panel režimu')

  await openGame(page, 'hive')
  await page.locator('.board-footer .btn', { hasText: 'Nápověda' }).click()
  await page.waitForTimeout(250)
  await page.locator('.found-toggle').click()
  check(
    await page.locator('.found-groups .found-word').first().isVisible(),
    'voština ukáže seznam nalezených slov',
  )
  await page.goBack()
  await page.waitForTimeout(300)
  check(!(await page.locator('.found-groups').isVisible()), 'zpět seznam zavře')

  await goHome(page)
  await openGame(page, 'tower')
  await page.locator('.hints .btn', { hasText: 'Celé slovo' }).click()
  await page.waitForTimeout(200)
  await page.locator('.board-footer .btn', { hasText: 'Postavit patro' }).click()
  await page.waitForTimeout(400)
  const green = await page.evaluate(() => {
    const color = getComputedStyle(document.querySelector('.floor.done .tile')).color
    const [r, g, b] = color.match(/\d+/g).map(Number)
    return { color, green: g > r && g > b }
  })
  check(green.green, `postavené patro věže je zelené, ne červené (${green.color})`)
  await fresh.close()
}

/* ---------- Vejde se hra na jednu obrazovku ---------- */

log('\nJEDNA OBRAZOVKA')
for (const mode of ['chain', 'hive', 'tower']) {
  await start(mode)
  const box = await page.evaluate(() => {
    const main = document.querySelector('.main')
    const footer = document.querySelector('.board-footer')
    const hints = document.querySelector('.hints')
    return {
      pageScroll: document.documentElement.scrollHeight - window.innerHeight,
      mainScroll: main.scrollHeight - main.clientHeight,
      footerBottom: footer?.getBoundingClientRect().bottom ?? 0,
      hintsBottom: hints?.getBoundingClientRect().bottom ?? 0,
      viewport: window.innerHeight,
    }
  })
  check(box.pageScroll <= 1, `${mode}: stránka se neroluje (${box.pageScroll}px)`)
  check(box.mainScroll <= 1, `${mode}: obsah hry se neroluje jako celek`)
  check(
    box.footerBottom > 0 && box.footerBottom <= box.viewport + 1,
    `${mode}: ovládání je vidět bez rolování`,
  )
  check(
    box.hintsBottom > 0 && box.hintsBottom <= box.viewport + 1,
    `${mode}: nápovědy jsou vidět bez rolování`,
  )
}

log(`\nzkontrolovaných slov: ${seenWords.size}`)
await browser.close()

if (problems.length > 0) {
  log(`\nNÁLEZY (${problems.length}):`)
  for (const problem of [...new Set(problems)].slice(0, 40)) log(`  • ${problem}`)
  process.exit(1)
}
log('\nVŠE PROŠLO')
