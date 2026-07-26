/** Snímky mobilního rozvržení — menu a všechny tři hry po rozehrání. */
import { chromium } from 'playwright'
import { mkdirSync } from 'node:fs'

const URL_ = process.env.URL ?? 'http://localhost:4173/'
const SHOTS = new URL('../shots/', import.meta.url).pathname
mkdirSync(SHOTS, { recursive: true })

const browser = await chromium.launch({
  executablePath:
    process.env.CHROME_PATH ?? '/opt/pw-browsers/chromium-1194/chrome-linux/chrome',
})
const page = await (
  await browser.newContext({
    viewport: { width: 390, height: 780 },
    locale: 'cs-CZ',
    deviceScaleFactor: 2,
  })
).newPage()
await page.goto(URL_, { waitUntil: 'networkidle' })
  await page.locator('.splash').waitFor({ state: 'detached', timeout: 8000 }).catch(() => undefined)
await page.waitForTimeout(1600) // úvodní logo

async function home() {
  const back = page.locator('.result-actions .btn', { hasText: 'Domů' })
  if (await back.isVisible().catch(() => false)) await back.click()
  const menu = page.locator('.btn-back')
  if (await menu.isVisible().catch(() => false)) await menu.click()
  await page.waitForSelector('h1:has-text("Vyber si hru")')
  await page.locator('.sheet-scrim').click({ position: { x: 5, y: 5 } }).catch(() => undefined)
}

await page.screenshot({ path: `${SHOTS}mob-home.png` })

for (const [mode, hints] of [
  ['chain', 6],
  ['hive', 0],
  ['tower', 3],
]) {
  await home()
  await page.locator(`.mode-tile[data-mode="${mode}"]`).click()
  await page.locator('.sheet-actions .btn', { hasText: /^(Hrát|Nová hra)$/ }).click()
  await page.waitForSelector('.board')
  const tut = page.locator('.tut-card')
  if (await tut.isVisible().catch(() => false)) {
    await page.locator('.tut-head').getByText('Přeskočit').click()
    await page.waitForTimeout(300)
  }
  for (let i = 0; i < hints; i++) {
    if (await page.locator('.result-card').isVisible().catch(() => false)) break
    await page.locator('.hints .btn', { hasText: 'Celé slovo' }).click()
    await page.waitForTimeout(150)
    if (mode === 'chain') await page.keyboard.press('Enter')
    else await page.locator('.board-footer .btn', { hasText: 'Postavit patro' }).click()
    await page.waitForTimeout(300)
    // Snímek po každém tahu; dohrané kolo přebije výsledek, ten nechceme.
    if (!(await page.locator('.result-card').isVisible().catch(() => false))) {
      await page.screenshot({ path: `${SHOTS}mob-${mode}.png` })
    }
  }
  await page.waitForTimeout(400)
  if (!(await page.locator('.result-card').isVisible().catch(() => false))) {
    await page.screenshot({ path: `${SHOTS}mob-${mode}.png` })
  }
}

await browser.close()
console.log('snímky v shots/')
