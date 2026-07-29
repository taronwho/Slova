/**
 * Náhledy vitríny.
 *
 * Odznaky a kresby ocenění se nedají ohlídat testem — jestli jsou hezké a
 * jestli se nepřekrývají, se pozná jenom pohledem. Skript nasype do profilu
 * hotový postup a udělá snímky ve světlém i tmavém tématu.
 */

import { chromium } from 'playwright'
import { mkdirSync } from 'node:fs'

import { waitReady } from './_ui.mjs'

const URL = process.env.URL ?? 'http://localhost:4173/'
const OUT = 'tools/out/shots'

/** Profil rozehraný natolik, aby byla vidět většina odemčených ocenění. */
const PROFILE = {
  xp: 260_000,
  streak: 9,
  bestStreak: 12,
  lastPlayedDay: null,
  seen: { chain: [], hive: [], tower: [] },
  stats: {
    chain: { played: 42, bestScore: 2600, totalScore: 60_000, extra: 12, perfect: 9 },
    hive: { played: 31, bestScore: 3400, totalScore: 52_000, extra: 900, perfect: 3 },
    tower: { played: 24, bestScore: 2100, totalScore: 38_000, extra: 120, perfect: 6 },
  },
  counters: {
    noHint: 26,
    noHintStreak: 4,
    bestNoHintStreak: 7,
    towerFullNoHint: 5,
    pangrams: 14,
    hiveFull: 3,
    hiveQueen: 2,
    hiveBestWords: 47,
    chainPar: 18,
    chainFastMs: 52_000,
    towerFull: 11,
    towerBestFloor: 8,
    towerFastMs: 74_000,
    dailies: 9,
    bestScore: 3400,
  },
  awards: {},
  hints: 6,
  hintRankPaid: 1,
  history: [],
  difficulty: { chain: 'normal', hive: 'normal', tower: 'normal' },
  theme: 'system',
  dailyDone: {},
  tutorialSeen: { chain: true, hive: true, tower: true },
}

async function shoot(page, name) {
  await page.screenshot({ path: `${OUT}/${name}.png`, fullPage: true })
  console.log(`  ${OUT}/${name}.png`)
}

const browser = await chromium.launch({
  executablePath:
    process.env.CHROME_PATH ?? '/opt/pw-browsers/chromium-1194/chrome-linux/chrome',
})
mkdirSync(OUT, { recursive: true })

for (const theme of ['light', 'dark']) {
  const context = await browser.newContext({
    viewport: { width: 390, height: 844 },
    deviceScaleFactor: 2,
    colorScheme: theme,
  })
  const page = await context.newPage()
  await page.addInitScript(
    (profile) => localStorage.setItem('slova.profile.v1', JSON.stringify(profile)),
    PROFILE,
  )
  await page.goto(URL, { waitUntil: 'networkidle' })
  await waitReady(page)

  await shoot(page, `home-${theme}`)

  await page.locator('.home-profile-actions .btn', { hasText: 'Vitrína' }).click()
  await page.waitForSelector('.award-grid')
  await page.waitForTimeout(400)
  await shoot(page, `awards-${theme}`)

  await page.locator('.award-summary .btn').click()
  await page.waitForSelector('.ladder-list')
  await page.waitForTimeout(400)
  await shoot(page, `ladder-${theme}`)

  await context.close()
}

await browser.close()
