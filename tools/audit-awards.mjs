/**
 * Revize met: dohraje kolo **s nápovědou** a podívá se, co se z toho v profilu
 * stalo.
 *
 * Unit testy hlídají `recordRound`, tenhle běh hlídá cestu před ním — jestli
 * se nápověda vůbec dostane do stavu kola a odtud do hlášení o kole. Kdyby ji
 * některá hra zapomněla započítat, vyšlo by kolo jako čisté a hráč by dostal
 * metu, na kterou nemá. Na to si stěžoval hráč, takže se to musí ověřit ve
 * skutečné hře, ne jen v modelu.
 *
 * Kola se dohrávají stejně jako v `playthrough.mjs`, jen se po každém sáhne
 * do profilu a porovná se, co přibylo.
 */

import { chromium } from 'playwright'

import { dismissGained, goHome, openGame, waitReady } from './_ui.mjs'

const APP_URL = process.env.URL ?? 'http://localhost:4173/'
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
const context = await browser.newContext({ viewport: { width: 390, height: 844 }, locale: 'cs-CZ' })
const page = await context.newPage()
page.on('pageerror', (error) => problems.push(`chyba stránky: ${error.message}`))

const profile = () =>
  page.evaluate(() => JSON.parse(localStorage.getItem('slova.profile.v1') ?? '{}'))

await page.goto(APP_URL, { waitUntil: 'networkidle' })
await waitReady(page)

// Inkoust na nápovědy, ať jich jde vzít, kolik je potřeba.
await page.evaluate(() => {
  const key = 'slova.profile.v1'
  const raw = JSON.parse(localStorage.getItem(key))
  raw.ink = 99999
  localStorage.setItem(key, JSON.stringify(raw))
})
await page.reload({ waitUntil: 'networkidle' })
await waitReady(page)

const result = () => page.locator('.result-card')

/** Kolik nápověd má rozehrané kolo na kontě. */
const hintsInRound = (mode) =>
  page.evaluate(
    (m) => JSON.parse(localStorage.getItem('slova.rounds.v1') ?? '{}')[m]?.state?.hintsUsed ?? 0,
    mode,
  )

async function playChain() {
  for (let guard = 0; guard < 40; guard++) {
    if (await result().isVisible().catch(() => false)) break
    const word = page.locator('.hints .btn', { hasText: 'Celé slovo' })
    if (!(await word.isEnabled().catch(() => false))) break
    await word.click()
    await page.waitForTimeout(120)
    await page.keyboard.press('Enter')
    await page.waitForTimeout(220)
  }
}

async function playHive() {
  for (let i = 0; i < 8; i++) {
    await page.locator('.board-footer .btn', { hasText: 'Nápověda' }).click()
    await page.waitForTimeout(120)
  }
  await page.locator('.board-footer .btn', { hasText: 'Ukončit plástev' }).click()
  await page.locator('.sheet.confirm .btn', { hasText: 'Ukončit' }).click()
  await result().waitFor({ timeout: 5000 }).catch(() => undefined)
}

async function playTower() {
  for (let guard = 0; guard < 20; guard++) {
    if (await result().isVisible().catch(() => false)) break
    const word = page.locator('.hints .btn', { hasText: 'Celé slovo' })
    if (!(await word.isEnabled().catch(() => false))) break
    await word.click()
    await page.waitForTimeout(150)
    const build = page.locator('.board-footer .btn', { hasText: 'Postavit patro' })
    if (await build.isEnabled().catch(() => false)) await build.click()
    await page.waitForTimeout(220)
  }
}

async function playGallows() {
  // Nejdřív nápověda, pak se doklikají písmena — kolo tak skončí uhodnutím
  // a zároveň má nápovědu na kontě.
  const hint = page.locator('.hints .btn').first()
  if (await hint.isEnabled().catch(() => false)) {
    await hint.click()
    await page.waitForTimeout(200)
  }
  for (const letter of 'aeiounrstlkvpmdczybhjfg') {
    if (await result().isVisible().catch(() => false)) break
    const key = page.locator('.letter-key', { hasText: new RegExp(`^${letter}$`) })
    if (!(await key.isEnabled().catch(() => false))) continue
    await key.click()
    await page.waitForTimeout(80)
  }
  await result().waitFor({ timeout: 5000 }).catch(() => undefined)
}

async function playDetective() {
  for (let guard = 0; guard < 14; guard++) {
    if (await result().isVisible().catch(() => false)) break
    const hint = page.locator('.hints .btn', { hasText: 'Odhal písmeno' })
    if (!(await hint.isEnabled().catch(() => false))) break
    await hint.click()
    await page.waitForTimeout(120)
  }
  await result().waitFor({ timeout: 5000 }).catch(() => undefined)
}

async function playTetris() {
  // „Poradit" umí odmítnout, když se z padající dvojice nedá nic složit —
  // pak se zkusí „Vyměnit", které jde skoro vždycky. Kdyby se nechytla ani
  // jedna, kolo by bylo poctivě čisté a test by měřil něco jiného.
  for (let attempt = 0; attempt < 12; attempt++) {
    const before = await hintsInRound('tetris')
    const label = attempt % 2 === 0 ? 'Poradit' : 'Vyměnit'
    await page.locator('.hints .btn', { hasText: label }).click().catch(() => undefined)
    await page.waitForTimeout(200)
    if ((await hintsInRound('tetris')) > before) break
    await page.locator('.pad-drop').click().catch(() => undefined)
    await page.waitForTimeout(120)
  }
  for (let guard = 0; guard < 400; guard++) {
    if (await result().isVisible().catch(() => false)) break
    if (guard % 3 === 0) await page.locator('.pad-turn').click().catch(() => undefined)
    if (guard % 2 === 0) {
      const dir = guard % 4 === 0 ? 'Doleva' : 'Doprava'
      await page.locator(`.pad-key[aria-label="${dir}"]`).click().catch(() => undefined)
    }
    await page.locator('.pad-drop').click().catch(() => undefined)
    await page.waitForTimeout(25)
  }
  await result().waitFor({ timeout: 5000 }).catch(() => undefined)
}

const PLAY = {
  chain: playChain,
  hive: playHive,
  tower: playTower,
  gallows: playGallows,
  detective: playDetective,
  tetris: playTetris,
}

for (const [mode, play] of Object.entries(PLAY)) {
  log(`\n${mode.toUpperCase()} — kolo s nápovědou`)
  const before = await profile()

  await goHome(page)
  await openGame(page, mode)
  await play()

  const finished = await result().isVisible().catch(() => false)
  check(finished, 'kolo došlo k výsledku')

  await goHome(page)
  await dismissGained(page)

  const after = await profile()
  const mine = after.stats?.[mode] ?? {}
  const yours = before.stats?.[mode] ?? {}
  const played = (mine.played ?? 0) - (yours.played ?? 0)
  check(played === 1, `kolo se zapsalo právě jednou (${played})`)

  // Nápovědy placené inkoustem se ze skóre nestrhávají, takže je ve výsledku
  // nevidět. Do hlášení o kole ale patřit musí — historie ho drží celý.
  const last = (after.history ?? [])[0] // historie je od nejnovějšího
  check(
    last?.mode === mode && (last?.hintsUsed ?? 0) > 0,
    `hlášení o kole ví o nápovědě (hintsUsed = ${last?.hintsUsed ?? '—'})`,
  )

  // Kolo s nápovědou nesmí přidat nic z čistých počítadel.
  check(
    (mine.clean ?? 0) === (yours.clean ?? 0),
    `čistá kola se nezvýšila (${yours.clean ?? 0} → ${mine.clean ?? 0})`,
  )
  check(
    (mine.perfect ?? 0) === (yours.perfect ?? 0),
    `perfektní kola se nezvýšila (${yours.perfect ?? 0} → ${mine.perfect ?? 0})`,
  )
  check(
    (after.counters?.noHint ?? 0) === (before.counters?.noHint ?? 0),
    `čítač kol bez nápovědy se nezvýšil (${before.counters?.noHint ?? 0} → ${after.counters?.noHint ?? 0})`,
  )
  check(
    (after.streak ?? 0) === 0,
    `série se přerušila (${after.streak ?? 0})`,
  )
}

// Po samých nápovědových kolech nesmí být udělená žádná meta za dovednost.
//
// Rychlostní a „nejkratší cesta" rodiny se sem počítají taky: nápověda za
// hráče odvede přesně tu práci, kterou mají měřit. Věž na tom kdysi
// pohořela — kolo postavené jen z nápověd rozdalo obě rychlostní mety.
const final = await profile()
const ids = Object.keys(final.awards ?? {})
const suspicious = ids.filter((id) =>
  /^cisto|cist|mistr-|-cisty|-cista|napoprve|rychla|rychlik|retez-par/.test(id),
)
check(
  suspicious.length === 0,
  `žádná meta za dovednost nepadla (${suspicious.join(', ') || 'žádná'})`,
)
check(
  (final.counters?.towerFastMs ?? 0) === 0,
  `čas věže se z nápovědového kola nezapsal (${final.counters?.towerFastMs ?? 0})`,
)
check(
  (final.counters?.chainPar ?? 0) === 0,
  `nejkratší cesta se z nápovědového kola nezapsala (${final.counters?.chainPar ?? 0})`,
)
log(`\nudělené mety: ${ids.join(', ') || 'žádné'}`)

log('')
if (problems.length > 0) {
  log(`NÁLEZY (${problems.length}):`)
  for (const problem of problems) log(`  • ${problem}`)
} else {
  log('BEZ NÁLEZŮ')
}

await browser.close()
process.exit(problems.length > 0 ? 1 : 0)
