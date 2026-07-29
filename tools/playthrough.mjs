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

import { dismissTutorial, goHome, openGame, waitReady } from './_ui.mjs'

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

/* ---------- ŠIBENICE ---------- */

async function playGallows() {
  await start('gallows')
  // Postupně se zkusí celá abeceda — kolo tím vždycky dojde k výsledku,
  // ať už uhodnutím, nebo osmi chybami.
  for (const letter of 'aeiounrstlkvpmdczybhjfg') {
    if (await page.locator('.result-card').isVisible().catch(() => false)) break
    const key = page.locator('.letter-key', { hasText: new RegExp(`^${letter}$`) })
    if (!(await key.isEnabled().catch(() => false))) continue
    await key.click()
    await page.waitForTimeout(90)
  }
  const result = page.locator('.result-card')
  await result.waitFor({ timeout: 5000 }).catch(() => undefined)
  if (await result.isVisible().catch(() => false)) {
    collect(await result.locator('.result-card p.muted').allInnerTexts().then(clean), 'šibenice — slovo')
  }
  return await result.isVisible().catch(() => false)
}

/* ---------- DETEKTIV ---------- */

async function playDetective() {
  await start('detective')
  // Vyklikat abecedu se nedá — po dvanácti chybách kolo končí. Pro průchod
  // stačí nápověda, která odhalí písmeno; kolo tak dojde k výsledku vždycky.
  for (let guard = 0; guard < 14; guard++) {
    if (await page.locator('.result-card').isVisible().catch(() => false)) break
    const hint = page.locator('.hints .btn', { hasText: 'Odhal písmeno' })
    if (!(await hint.isEnabled().catch(() => false))) break
    await hint.click()
    await page.waitForTimeout(120)
  }
  const result = page.locator('.result-card')
  await result.waitFor({ timeout: 5000 }).catch(() => undefined)
  return await result.isVisible().catch(() => false)
}

/**
 * Slabikový tetris.
 *
 * Hraje se hloupě, ale úplně: otoč, posuň, polož — a tak pořád dokola,
 * dokud deska nepřeteče. Kolo se nedá „dohrát", končí až zablokováním,
 * takže se tím zároveň ověří, že konec vůbec nastane.
 */
async function playTetris() {
  await start('tetris')
  const result = page.locator('.result-card')
  for (let guard = 0; guard < 400; guard++) {
    if (await result.isVisible().catch(() => false)) break
    // Občas otočit a posunout, ať se testuje i to, ne jen volný pád.
    if (guard % 3 === 0) await page.locator('.pad-turn').click().catch(() => undefined)
    if (guard % 2 === 0) {
      const dir = guard % 4 === 0 ? 'Doleva' : 'Doprava'
      await page.locator(`.pad-key[aria-label="${dir}"]`).click().catch(() => undefined)
    }
    await page.locator('.pad-drop').click().catch(() => undefined)
    await page.waitForTimeout(30)
    collect(await page.locator('.rail-right .found-word').allTextContents(), 'slabiky')
  }
  await result.waitFor({ timeout: 5000 }).catch(() => undefined)
  return await result.isVisible().catch(() => false)
}

function clean(texts) {
  return texts.map((t) => t.replace(/[\s\n▸·0-9]/g, ''))
}

const MODES = [
  ['ŘETĚZ', playChain],
  ['VOŠTINA', playHive],
  ['VĚŽ', playTower],
  ['ŠIBENICE', playGallows],
  ['DETEKTIV', playDetective],
  ['SLABIKY', playTetris],
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

  // Ukazatelů na desce je víc a všechny jsou klikací; pangramy se hledají
  // podle popisku. Výklad se otevře v panelu nad hrou, ne v pruhu pod ní —
  // uprostřed kola se deska nesmí hnout pod prstem.
  await page.locator('.stat-tap', { hasText: 'Pangramy' }).click()
  await page.waitForTimeout(300)
  check(
    (await page.locator('.sheet-term').innerText()).includes('všech sedm'),
    'ťuknutí na pangramy vysvětlí, co to je',
  )
  await page.locator('.sheet-term .sheet-head .btn').click()
  await page.waitForTimeout(250)

  await goHome(page)
  await openGame(page, 'tower')

  // Hlavička nápověd je jediné místo, kde se hráč rozhoduje, jestli pomoc
  // vzít — takže tam musí být po ruce i to, co ho to stojí.
  await page.locator('.hint-head').click()
  await page.waitForTimeout(300)
  const hintText = await page.locator('.sheet-term').innerText()
  check(
    hintText.includes('inkoust') && hintText.includes('body'),
    'hlavička nápověd vysvětlí, čím se platí',
  )
  await page.locator('.sheet-term .sheet-head .btn').click()
  await page.waitForTimeout(250)

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
for (const mode of ['chain', 'hive', 'tower', 'gallows', 'detective', 'tetris']) {
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

/* ---------- Vitrína ---------- */

log('\nVITRÍNA')
{
  await goHome(page)
  const chip = page.locator('.home-profile-actions .btn', { hasText: 'Vitrína' })
  // Počet visí v dlaždici statistik, klik do vitríny na tlačítku pod ní.
  const label = await page.locator('.stat-cell', { hasText: 'ocenění' }).innerText()
  // Po třiceti odehraných kolech musí být něco odemčené — kdyby se ocenění
  // neudělovala, stálo by tu 0/30.
  const gotSome = Number(label.match(/\d+/)?.[0] ?? 0) > 0
  check(gotSome, `odehraná kola odemkla ocenění (${label.replace(/\s+/g, ' ')})`)

  await chip.click()
  await page.waitForSelector('.award-grid')
  const tiles = await page.locator('.award').count()
  check(tiles >= 30, `vitrína ukáže všech ${tiles} ocenění`)
  check(
    (await page.locator('.award.has').count()) > 0,
    'získaná ocenění jsou odlišená od zamčených',
  )
  // Kresba musí být vlastní grafika, ne znak z fontu.
  check(
    (await page.locator('.award svg.award-art').count()) === tiles,
    'každé ocenění má vlastní kresbu',
  )

  await page.locator('.award-summary .btn').click()
  await page.waitForSelector('.ladder-list')
  check(
    (await page.locator('.ladder-row').count()) === 50,
    'žebříček má padesát hodností',
  )
  check(
    (await page.locator('.ladder-row.has').count()) > 0,
    'dosažené hodnosti jsou odlišené',
  )
  await page.goBack()
  await page.waitForTimeout(300)
  check(!(await page.locator('.ladder-list').isVisible()), 'zpět žebříček zavře')
  await goHome(page)
}

/* ---------- Denní výzva a inkoust ---------- */

log('\nDENNÍ VÝZVA A INKOUST')
{
  await goHome(page)
  check(
    (await page.locator('.daily-strip .daily-item').count()) === 6,
    'denní výzva je vidět rovnou v menu, jedna dlaždice na hru',
  )
  const strip = await page.locator('.daily-strip').boundingBox()
  const grid = await page.locator('.mode-grid').boundingBox()
  check(strip.y > grid.y, 'denní výzva je pod mřížkou her, ne místo ní')

  check(
    await page.locator('.profile-chip').isVisible(),
    'hodnost je vidět v liště na úvodní obrazovce',
  )

  // Denní výzva se spouští jedním ťuknutím, bez oklik přes panel režimu.
  await page.locator('.daily-item', { hasText: 'Řetěz' }).click()
  await page.waitForSelector('.board', { timeout: 20000 })
  await dismissTutorial(page)
  // Zlatý čip v liště se na telefonu schovává, aby zbylo místo na kalamář,
  // takže se denní kolo pozná z desky, ne z hlavičky.
  check(
    await page.locator('.shell[data-daily="true"]').isVisible(),
    'spustí se rovnou denní kolo',
  )
  check(await page.locator('.profile-chip').isVisible(), 'hodnost je vidět i ve hře')
  await goHome(page)

  // Kalamář se pro tuhle kontrolu nastaví do známého stavu. Po padesáti
  // odehraných kolech je většinou prázdný a test by pak měřil náhodu.
  // Pětadvacet stačí na jedno „Celé slovo" (20) a už ne na druhé.
  const wallet = await browser.newContext({
    viewport: { width: 390, height: 844 },
    locale: 'cs-CZ',
  })
  const shop = await wallet.newPage()
  await shop.addInitScript(() => {
    const raw = localStorage.getItem('slova.profile.v1')
    const profile = raw ? JSON.parse(raw) : {}
    profile.ink = 25
    localStorage.setItem('slova.profile.v1', JSON.stringify(profile))
  })
  await shop.goto(APP_URL, { waitUntil: 'networkidle' })
  await waitReady(shop)
  await openGame(shop, 'chain')

  const before = Number((await shop.locator('.chip-ink .num').innerText()).trim())
  check(before === 25, `kalamář nese inkoust (${before})`)

  // Cena musí odpovídat velikosti nápovědy — kvůli tomu měna vznikla.
  const small = await shop.locator('.hints .btn', { hasText: 'Vzdálenost' }).innerText()
  const big = await shop.locator('.hints .btn', { hasText: 'Celé slovo' }).innerText()
  const price = (text) => Number(text.replace(/[^0-9]/g, ''))
  check(price(big) >= price(small) * 3, `velká nápověda stojí víc než malá (${price(small)} vs ${price(big)})`)
  check(
    (await shop.locator('.hints .btn', { hasText: 'Celé slovo' }).locator('.price-ink').count()) === 1,
    'nápověda se platí inkoustem, dokud je z čeho brát',
  )

  await shop.locator('.hints .btn', { hasText: 'Celé slovo' }).click()
  await shop.waitForTimeout(300)
  const after = Number((await shop.locator('.chip-ink .num').innerText()).trim())
  check(after === before - price(big), `nápověda ubrala z kalamáře (${before} → ${after})`)

  // Na druhé „Celé slovo" už zbytek nestačí, takže se zase platí body.
  const paid = await shop.locator('.hints .btn', { hasText: 'Celé slovo' }).innerText()
  check(paid.includes('\u2212'), 'na co inkoust nestačí, se zase platí body')
  // Menší nápověda ale z toho zbytku pořád jde.
  check(
    (await shop.locator('.hints .btn', { hasText: 'Vzdálenost' }).locator('.price-ink').count()) === 1,
    'na malou nápovědu zbytek inkoustu pořád stačí',
  )
  await wallet.close()
}

log(`\nzkontrolovaných slov: ${seenWords.size}`)
await browser.close()

if (problems.length > 0) {
  log(`\nNÁLEZY (${problems.length}):`)
  for (const problem of [...new Set(problems)].slice(0, 40)) log(`  • ${problem}`)
  process.exit(1)
}
log('\nVŠE PROŠLO')
