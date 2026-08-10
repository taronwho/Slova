/**
 * Odchod z rozehraného kola a návrat do něj.
 *
 * Hráč nahlásil, že se u Citátu po odchodu do menu vrací na začátek. Příčina
 * byla v překladu uloženého stavu zpátky na hádanku: psal se jako řada
 * `else if` s koncovým `else`, do kterého Citát i Vetřelec spadly, protože
 * přibyly později. Chyba se ale nedá uhlídat čtením — musí ji hlídat kolo
 * odehrané v prohlížeči, protože se skládá z ukládání, obnovy, menu
 * i hodin naráz.
 *
 * Prochází se čtyři věci:
 *
 * 1. **Každá hra** se po tahu uloží, po návratu pokračuje se stejným stavem
 *    a hodiny navazují.
 * 2. **Denní výzva a volná hra téže hry** leží každá zvlášť a nepřepisují se.
 * 3. **Otázka dne** si pamatuje sázku na indicie i pokusy.
 * 4. **Čas běží i mimo hru** a včerejší denní kolo se dneska nenabízí.
 *
 * Spuštění:  npm run audit:resume   (nad `npm run preview` nebo dist)
 */

import { chromium } from 'playwright'

import { waitReady } from './_ui.mjs'

const URL = process.env.URL ?? 'http://localhost:4173/'
const CHROME = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome'

const problems = []
const check = (ok, msg) => {
  console.log(`  ${ok ? '✓' : '✗'} ${msg}`)
  if (!ok) problems.push(msg)
}

const NAME = {
  chain: 'Řetěz',
  hive: 'Voština',
  tower: 'Věž',
  gallows: 'Šibenice',
  detective: 'Detektiv',
  tetris: 'Slabiky',
  quotes: 'Citát',
  intruder: 'Vetřelec',
}

/** Přihrádka, ve které kolo leží — musí sedět s `roundSlot` ve hře. */
const slot = (mode, daily) => (daily ? `${mode}:denni` : mode)

const browser = await chromium.launch({ executablePath: CHROME })
const page = await (
  await browser.newContext({ viewport: { width: 390, height: 844 }, locale: 'cs-CZ' })
).newPage()
page.on('pageerror', (e) => {
  problems.push('chyba: ' + e.message)
  console.log('  ✗ chyba: ' + e.message)
})

const rounds = () =>
  page.evaluate(() => JSON.parse(localStorage.getItem('slova.rounds.v1') ?? '{}'))
const quizRound = () =>
  page.evaluate(() => JSON.parse(localStorage.getItem('slova.quizround.v1') ?? 'null'))
const clock = () => page.locator('.chip-time .num').innerText()

async function home() {
  await page.goto(URL, { waitUntil: 'networkidle' })
  await waitReady(page)
}

/** Návod se při prvním spuštění režimu otevře sám; tady jen překáží. */
async function skipTutorial() {
  const card = page.locator('.tut-card')
  if (await card.isVisible().catch(() => false)) {
    await page.locator('.tut-head').getByText('Přeskočit').click()
  }
}

async function openDaily(mode) {
  await page.locator('.daily-row .daily-item').filter({ hasText: NAME[mode] }).first().click()
  await page.waitForSelector('.board, .game', { timeout: 20000 })
  await skipTutorial()
}

/**
 * Jeden tah v každé hře. Nemusí být chytrý, jen musí změnit stav.
 *
 * Ve Vetřelci se nehraje nic: ukázat na slovo je tam **konec kola**, ne tah,
 * takže rozehraný stav je ten hned po otevření — a i ten se musí uložit,
 * protože s ním jde čas, od kterého kolo běží.
 */
const MOVE = {
  quotes: () => page.locator('.letter-key:not([disabled])').first().click(),
  gallows: () => page.locator('.letter-key:not([disabled])').first().click(),
  detective: () => page.locator('.letter-key:not([disabled])').first().click(),
  tower: () => page.locator('.letter-key:not([disabled])').first().click(),
  chain: () => page.locator('.letter-key:not([disabled])').first().click(),
  tetris: () => page.locator('.tetris-cell, .slot, .tetris-slot').first().click(),
  hive: () => page.locator('.hive-cell, .cell').nth(1).click(),
  intruder: async () => {},
}

for (const mode of Object.keys(NAME)) {
  console.log(`\n${NAME[mode].toUpperCase()}`)
  await home()
  await openDaily(mode)
  await MOVE[mode]().catch(() => undefined)
  await page.waitForTimeout(400)

  const before = (await rounds())[slot(mode, true)]
  check(!!before, 'rozehrané kolo se uložilo')
  if (!before) continue
  check(before.daily === true, 'uložené kolo ví, že je denní')

  await home()
  const tile = page.locator('.daily-row .daily-item').filter({ hasText: NAME[mode] }).first()
  check(!(await tile.isDisabled()), 'dlaždice denní výzvy jde znovu otevřít')
  check(
    (await tile.innerText()).toLowerCase().includes('rozehráno') ||
      /\d/.test(await tile.innerText()),
    'dlaždice ukazuje, že se v kole pokračuje',
  )
  await openDaily(mode)
  await page.waitForTimeout(400)

  const after = (await rounds())[slot(mode, true)]
  check(!!after, 'po návratu je kolo pořád rozehrané')
  check(
    JSON.stringify(after?.state) === JSON.stringify(before.state),
    'stav je stejný jako před odchodem',
  )
  check((await clock()) !== '0:00', `hodiny navazují (${await clock()})`)
}

console.log('\nVOLNÁ HRA VEDLE DENNÍ VÝZVY')
await home()
await page.locator('.mode-tile[data-mode="gallows"]').click()
await page.locator('.sheet-actions .btn', { hasText: /^(Hrát|Nová hra)$/ }).first().click()
await page.waitForSelector('.board', { timeout: 20000 })
await skipTutorial()
await page.locator('.letter-key:not([disabled])').first().click()
await page.waitForTimeout(400)
const free = (await rounds())[slot('gallows', false)]
check(!!free, 'volné kolo se uložilo do vlastní přihrádky')

await home()
await openDaily('gallows')
await page.locator('.letter-key:not([disabled])').first().click()
await page.waitForTimeout(400)
const both = await rounds()
check(!!both[slot('gallows', true)], 'denní kolo se uložilo vedle něj')
check(
  JSON.stringify(both[slot('gallows', false)]?.state) === JSON.stringify(free?.state),
  'volné kolo zůstalo netknuté',
)

await home()
await page.locator('.mode-tile[data-mode="gallows"]').click()
const again = page.locator('.sheet-actions .btn', { hasText: /^Pokračovat/ })
check(await again.isVisible(), 'panel režimu nabízí návrat do volné hry')
await again.click()
await page.waitForSelector('.board', { timeout: 20000 })
await page.waitForTimeout(400)
check(
  JSON.stringify((await rounds())[slot('gallows', false)]?.state) === JSON.stringify(free?.state),
  'volná hra pokračuje tam, kde skončila',
)

console.log('\nOTÁZKA DNE')
await home()
await page.locator('.daily-quiz').click()
await page.waitForSelector('.quiz-card', { timeout: 20000 })
// Sázka na počet indicií je nevratná — přesně to, co se nesmí ztratit.
await page.locator('.quiz-card button').filter({ hasText: /^[123]/ }).first().click()
await page.waitForTimeout(400)
const quizBefore = await quizRound()
check(!!quizBefore, 'rozehraná otázka se uložila')
check(quizBefore?.state?.bought != null, 'uložila se i sázka na indicie')

await home()
const quizTile = page.locator('.daily-quiz')
check(!(await quizTile.isDisabled()), 'dlaždice Otázky dne jde znovu otevřít')
await quizTile.click()
await page.waitForSelector('.quiz-card', { timeout: 20000 })
await page.waitForTimeout(400)
check(
  JSON.stringify((await quizRound())?.state) === JSON.stringify(quizBefore?.state),
  'stav otázky je stejný jako před odchodem',
)

console.log('\nČAS BĚŽÍ I MIMO HRU')
// Posun začátku kola nahrazuje čekání: hra o něm neví a musí se zachovat
// stejně, jako by hráč byl půl hodiny pryč.
await page.evaluate(() => {
  const all = JSON.parse(localStorage.getItem('slova.rounds.v1'))
  all['gallows:denni'].state.startedAt -= 25 * 60 * 1000
  localStorage.setItem('slova.rounds.v1', JSON.stringify(all))
})
await home()
await openDaily('gallows')
const late = await clock()
check(Number(late.split(':')[0]) >= 25, `lišta počítá čas od začátku kola (${late})`)

console.log('\nVČEREJŠÍ DENNÍ VÝZVA')
// Datum se posouvá z menu, ne z otevřené hry: rozehraná hra si stav ukládá
// po každém překreslení a posun by hned přepsala zpátky na dnešek.
await home()
await page.evaluate(() => {
  const all = JSON.parse(localStorage.getItem('slova.rounds.v1'))
  all['gallows:denni'].savedAt -= 24 * 60 * 60 * 1000
  localStorage.setItem('slova.rounds.v1', JSON.stringify(all))
})
await home()
await openDaily('gallows')
await page.waitForTimeout(300)
const fresh = (await rounds())[slot('gallows', true)]
check(!!fresh, 'dnešní výzva se rozehrála')
check(
  JSON.stringify(fresh?.state?.tried ?? []) === '[]',
  'je čistá, ne dohrávka včerejška',
)
check((await clock()).startsWith('0:'), `a hodiny začínají od nuly (${await clock()})`)

console.log(problems.length ? `\nNÁLEZY: ${problems.length}` : '\nVŠE PROŠLO')
await browser.close()
process.exit(problems.length > 0 ? 1 : 0)
