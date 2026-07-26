/**
 * Průchod hrou v reálném prohlížeči — ověří, že se všechny tři režimy
 * rozehrají, přijmou tah a dojdou k výsledku. Zároveň pořídí snímky.
 */

import { chromium } from 'playwright'
import { mkdirSync } from 'node:fs'
import { dismissTutorial, goHome, openGame, waitReady } from './_ui.mjs'

const APP_URL = process.env.URL ?? 'http://localhost:4173/'
const SHOTS = new URL('../shots/', import.meta.url).pathname
mkdirSync(SHOTS, { recursive: true })

const problems = []
const log = (...args) => console.log(...args)

function check(condition, message) {
  if (condition) log(`  ✓ ${message}`)
  else {
    log(`  ✗ ${message}`)
    problems.push(message)
  }
}

const browser = await chromium.launch({
  executablePath:
    process.env.CHROME_PATH ?? '/opt/pw-browsers/chromium-1194/chrome-linux/chrome',
})

async function newPage(size) {
  const context = await browser.newContext({ viewport: size, locale: 'cs-CZ' })
  const page = await context.newPage()
  page.on('pageerror', (error) => {
    problems.push(`chyba stránky: ${error.message}`)
    log(`  ✗ chyba stránky: ${error.message}`)
  })
  page.on('console', (message) => {
    if (message.type() === 'error') {
      problems.push(`console.error: ${message.text()}`)
      log(`  ✗ console.error: ${message.text()}`)
    }
  })
  await page.goto(APP_URL, { waitUntil: 'networkidle' })
  await page.locator('.splash').waitFor({ state: 'detached', timeout: 8000 }).catch(() => undefined)
  return page
}



const desktop = { width: 1280, height: 900 }
const mobile = { width: 390, height: 844 }

/* ---------- Domovská obrazovka ---------- */
log('\nDOMŮ')
{
  const page = await newPage(desktop)
  check(
    await page.locator('h1', { hasText: 'Vyber si hru' }).isVisible(),
    'výběr hry je hned na úvodu',
  )
  check((await page.locator('.mode-tile').count()) === 4, 'čtyři dlaždice režimů')
  await page.screenshot({ path: `${SHOTS}01-home-light.png`, fullPage: true })

  // Tmavé téma
  await page.locator('.topbar button[title^="Téma"]').click()
  await page.locator('.topbar button[title^="Téma"]').click()
  await page.waitForTimeout(300)
  check(
    (await page.locator('html').getAttribute('data-theme')) === 'dark',
    'přepnutí na tmavé téma',
  )
  await page.screenshot({ path: `${SHOTS}02-home-dark.png`, fullPage: true })
  await page.close()
}

/* ---------- Řetěz ---------- */
log('\nŘETĚZ')
{
  const page = await newPage(desktop)
  await openGame(page, 'chain')
  await page.waitForSelector('.ladder', { timeout: 20000 })
  await dismissTutorial(page)

  const par = await page
    .locator('.stat', { hasText: 'Nejkratší cesta' })
    .locator('.value')
    .innerText()
  check(Number(par) > 0, `nejkratší cesta je načtená (${par})`)

  const remaining = await page
    .locator('.stat', { hasText: 'Zbývá nejméně' })
    .locator('.value')
    .innerText()
  check(
    remaining === par,
    `strážce hlásí stejnou vzdálenost jako nejkratší cesta (${remaining})`,
  )

  await page.screenshot({ path: `${SHOTS}03-chain.png`, fullPage: true })

  // Neplatný tah musí být odmítnutý.
  const startWord = (await page.locator('.rung.is-start .tile').allInnerTexts()).join('')
  await page.locator('.rung').nth(1).locator('.tile').first().click()
  await page.keyboard.press('q')
  await page.keyboard.press('Enter')
  await page.waitForTimeout(400)
  check(
    await page.locator('.banner-error').isVisible(),
    'neplatné slovo je odmítnuto s hláškou',
  )

  // Nápověda „celé slovo" musí dát platný tah.
  await page.locator('button', { hasText: 'Celé slovo' }).click()
  await page.waitForTimeout(300)
  await page.keyboard.press('Enter')
  await page.waitForTimeout(500)
  const rungs = await page.locator('.ladder .rung').count()
  check(rungs >= 3, 'tah po nápovědě prošel a řetěz se prodloužil')

  const after = (await page.locator('.rung').nth(1).locator('.tile').allInnerTexts()).join('')
  check(after !== startWord, `řetěz postoupil (${startWord} → ${after})`)

  await page.screenshot({ path: `${SHOTS}04-chain-hraje.png`, fullPage: true })

  // Dohrát celé kolo nápovědami — ověří, že se objeví výsledek.
  for (let i = 0; i < 14; i++) {
    if (await page.locator('.result-card').isVisible()) break
    const button = page.locator('button', { hasText: 'Celé slovo' })
    if (!(await button.isVisible())) break
    await button.click()
    await page.waitForTimeout(150)
    await page.keyboard.press('Enter')
    await page.waitForTimeout(350)
  }
  check(await page.locator('.result-card').isVisible(), 'kolo lze dohrát do konce')
  const total = await page.locator('.breakdown-line.total .num').innerText()
  check(/\d/.test(total), `výsledek ukazuje skóre (${total})`)
  await page.screenshot({ path: `${SHOTS}05-chain-vysledek.png` })
  await page.close()
}

/* ---------- Voština ---------- */
log('\nVOŠTINA')
{
  const page = await newPage(desktop)
  await openGame(page, 'hive')
  await page.waitForSelector('.hive', { timeout: 20000 })
  await dismissTutorial(page)
  check((await page.locator('.hex').count()) === 7, 'plástev má sedm buněk')
  await page.screenshot({ path: `${SHOTS}06-hive.png`, fullPage: true })

  // Nápověda odhalí platné slovo a musí přibýt mezi nalezená.
  await page.locator('button', { hasText: 'Nápověda' }).click()
  await page.waitForTimeout(400)
  check(
    (await page.locator('.found-word').count()) === 1,
    'nápověda přidala slovo mezi nalezená',
  )

  // Odhalené slovo napsané bez diakritiky musí plástev poznat — na mobilu
  // se píše ťukáním do šestiúhelníků, které háčky nenabízejí.
  const revealed = await page.locator('.found-word').first().innerText()
  const plain = revealed
    .normalize('NFD')
    .replace(/[̀-ͯ]/g, '')
    .replace(/ě/g, 'e')
  await page.keyboard.type(plain)
  await page.keyboard.press('Enter')
  await page.waitForTimeout(300)
  const message = await page.locator('.banner').first().innerText()
  check(
    !/neznám/i.test(message),
    `tvar bez diakritiky je rozpoznán (${revealed} → ${plain}: „${message}")`,
  )

  // Slovo mimo plástev musí spadnout na chybu.
  await page.keyboard.type('xxxx')
  await page.keyboard.press('Enter')
  await page.waitForTimeout(300)
  check(await page.locator('.banner-error').isVisible(), 'cizí písmeno je odmítnuto')

  await page.locator('button', { hasText: 'Zamíchat' }).click()
  await page.waitForTimeout(200)
  check((await page.locator('.hex').count()) === 7, 'zamíchání nerozbije plástev')
  await page.screenshot({ path: `${SHOTS}07-hive-hraje.png`, fullPage: true })
  await page.close()
}

/* ---------- Věž ---------- */
log('\nVĚŽ')
{
  const page = await newPage(desktop)
  await openGame(page, 'tower')
  await page.waitForSelector('.tower', { timeout: 20000 })
  await dismissTutorial(page)
  check((await page.locator('.tray-tile').count()) >= 4, 'zásobník dlaždic je připravený')
  await page.screenshot({ path: `${SHOTS}08-tower.png`, fullPage: true })

  // Postavit celou věž pomocí nápovědy na celé slovo.
  for (let i = 0; i < 8; i++) {
    if (await page.locator('.result-card').isVisible()) break
    const button = page.locator('button', { hasText: 'Celé slovo' })
    if (!(await button.isVisible())) break
    await button.click()
    await page.waitForTimeout(200)
    await page.locator('button', { hasText: 'Postavit patro' }).click()
    await page.waitForTimeout(350)
  }
  check(await page.locator('.result-card').isVisible(), 'věž lze dostavět do konce')
  await page.screenshot({ path: `${SHOTS}09-tower-vysledek.png` })
  await page.close()
}

/* ---------- Mobil ---------- */
log('\nMOBIL')
{
  const page = await newPage(mobile)
  const overflow = await page.evaluate(
    () => document.documentElement.scrollWidth - document.documentElement.clientWidth,
  )
  check(overflow <= 0, `domů se nepřetéká vodorovně (${overflow}px)`)
  await page.screenshot({ path: `${SHOTS}10-mobil-home.png`, fullPage: true })

  await openGame(page, 'chain')
  await page.waitForSelector('.ladder', { timeout: 20000 })
  await dismissTutorial(page)
  const overflowGame = await page.evaluate(
    () => document.documentElement.scrollWidth - document.documentElement.clientWidth,
  )
  check(overflowGame <= 0, `hra se nepřetéká vodorovně (${overflowGame}px)`)
  check(await page.locator('.keyboard').isVisible(), 'virtuální klávesnice je vidět')
  await page.screenshot({ path: `${SHOTS}11-mobil-chain.png`, fullPage: true })

  await page.goto(APP_URL, { waitUntil: 'networkidle' })
  await page.locator('.splash').waitFor({ state: 'detached', timeout: 8000 }).catch(() => undefined)
  await openGame(page, 'hive')
  await dismissTutorial(page)
  await page.waitForSelector('.hive', { timeout: 20000 })
  await page.screenshot({ path: `${SHOTS}12-mobil-hive.png`, fullPage: true })

  await page.goto(APP_URL, { waitUntil: 'networkidle' })
  await page.locator('.splash').waitFor({ state: 'detached', timeout: 8000 }).catch(() => undefined)
  await openGame(page, 'tower')
  await dismissTutorial(page)
  await page.waitForSelector('.tower', { timeout: 20000 })
  await page.screenshot({ path: `${SHOTS}13-mobil-tower.png`, fullPage: true })
  await page.close()
}

await browser.close()

log(`\n${problems.length === 0 ? 'VŠE PROŠLO' : `PROBLÉMŮ: ${problems.length}`}`)
for (const problem of problems) log(` - ${problem}`)
process.exit(problems.length === 0 ? 0 : 1)
