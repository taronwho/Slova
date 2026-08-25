/**
 * Snímek horní lišty ve hře — jak vypadá po dopsaném ustupování.
 *
 * Spuštění:  node tools/shot-topbar.mjs   (nad `dist` na http://localhost:4173)
 * Ukládá do `shots/topbar/`.
 */

import { chromium } from 'playwright'
import { mkdirSync } from 'node:fs'

import { dismissTutorial, waitReady } from './_ui.mjs'

const APP = process.env.URL ?? 'http://localhost:4173/'
const CHROME = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome'
const SHOTS = new URL('../shots/topbar/', import.meta.url).pathname
mkdirSync(SHOTS, { recursive: true })

const browser = await chromium.launch({ executablePath: CHROME })

for (const [width, height] of [[320, 568], [390, 844], [412, 915]]) {
  const context = await browser.newContext({
    viewport: { width, height },
    deviceScaleFactor: 2,
    isMobile: true,
    hasTouch: true,
    locale: 'cs-CZ',
  })
  const page = await context.newPage()
  await page.addInitScript((day) => {
    const streak = { lastDay: day, streak: 12, best: 30 }
    const all = (value) => ({
      chain: value, hive: value, tower: value, gallows: value,
      detective: value, tetris: value, quotes: value, intruder: value,
    })
    localStorage.setItem(
      'slova.profile.v1',
      JSON.stringify({
        version: 3, guideSeen: true, tutorialSeen: all(true),
        dailyStreak: all(streak), ink: 128, streak: 18, xp: 4200,
      }),
    )
  }, new Date().toISOString().slice(0, 10))

  await page.goto(APP, { waitUntil: 'networkidle' })
  await waitReady(page)
  await page.locator('.mode-tile[data-mode="quotes"]').click()
  await page.locator('.sheet').waitFor()
  await page.locator('.sheet-actions .btn', { hasText: /^Denní/ }).first().click()
  await page.waitForSelector('.board', { timeout: 20000 })
  await dismissTutorial(page)
  await page.waitForTimeout(500)

  const bar = await page.locator('.topbar').boundingBox()
  await page.screenshot({
    path: `${SHOTS}citat-${width}.png`,
    clip: { x: 0, y: 0, width, height: Math.ceil(bar.height) + 4 },
  })
  console.log(`citat-${width}.png`)
  await context.close()
}

await browser.close()
