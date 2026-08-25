/**
 * Audit rozvržení — tlačítka, čipy a symboly na všech obrazovkách.
 *
 * `audit:mobile` hlídá, jestli se obrazovka vejde: přetečení stránky, malé
 * dotykové cíle, ovládání pod okrajem. Tenhle audit se ptá na něco jiného —
 * jestli každý jednotlivý prvek sedí ve svém místě:
 *
 *   1. **obsah přetéká ze svého tlačítka.** Tlačítko v pružném řádku se
 *      smrskne pod svůj obsah a nápis z něj vyleze ven. Nikde se nic
 *      neuřízne, stránka se nerozšíří, jen se nápis kreslí přes souseda —
 *      přesně tak vypadala lišta v Citátu, kde „← Menu" leželo pod čipem
 *      s plamínkem. Ani jedna z dosavadních kontrol na tohle nesáhne.
 *   2. **sourozenci se překrývají.** Dva prvky v jednom řádku na sobě.
 *   3. **prvek leží mimo obrazovku.** Vlevo od nuly nebo za pravým okrajem.
 *   4. **malý dotykový cíl.** Pod 40 px (klávesy mají vlastní práh).
 *   5. **stránka přetéká do strany.**
 *
 * Prochází se každá obrazovka, do které se dá bez sítě dostat: menu, všech
 * devět her v běžném i denním kole, Otázka dne, statistiky, vitrína, žebříček
 * hodností, průvodce, návod, panel nápověd a potvrzení vzdání kola. Na pěti
 * šířkách telefonu — od 320 px po 430 px.
 *
 * Spuštění:  npm run audit:layout   (nad `dist` na http://localhost:4173)
 */

import { chromium } from 'playwright'

import { dismissTutorial, waitReady } from './_ui.mjs'

const APP = process.env.URL ?? 'http://localhost:4173/'
const CHROME = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome'

const SIZES = [
  { name: '320', width: 320, height: 568 },
  { name: '360', width: 360, height: 640 },
  { name: '390', width: 390, height: 844 },
  { name: '412', width: 412, height: 915 },
  { name: '430', width: 430, height: 932 },
  { name: '740 naležato', width: 740, height: 360 },
  // Ustupování v liště má stupně na 899 a 640 px; obojí se musí projít, aby
  // se nestalo, že se něco vejde na telefon i na monitor, ale mezi tím ne.
  { name: '820 tablet', width: 820, height: 1180 },
  { name: '1280 monitor', width: 1280, height: 800, desktop: true },
]

const MODES = [
  ['chain', 'Řetěz'],
  ['hive', 'Voština'],
  ['tower', 'Věž'],
  ['gallows', 'Šibenice'],
  ['detective', 'Detektiv'],
  ['tetris', 'Slabiky'],
  ['quotes', 'Citát'],
  ['intruder', 'Vetřelec'],
]

const findings = []
const note = (where, text) => {
  findings.push(`${where}: ${text}`)
  console.log(`  ! ${where} — ${text}`)
}

/**
 * Změří jednu obrazovku. Běží uvnitř stránky, vrací seznam nálezů.
 */
function scan() {
  const out = { overflowX: 0, spill: [], overlap: [], offscreen: [], small: [] }
  const doc = document.documentElement
  out.overflowX = doc.scrollWidth - doc.clientWidth

  const seen = (el) => {
    const r = el.getBoundingClientRect()
    if (r.width < 1 || r.height < 1) return null
    const style = getComputedStyle(el)
    if (style.visibility === 'hidden' || style.opacity === '0') return null
    return r
  }
  const name = (el) => {
    const cls = `${el.className}`.split(' ').filter(Boolean)[0] || el.tagName.toLowerCase()
    const text = (el.innerText || el.textContent || '').replace(/\s+/g, ' ').trim().slice(0, 16)
    return text ? `${cls} „${text}"` : cls
  }

  /* 1. Obsah, který nesedí ve svém tlačítku.
     Měří se podle dětí, ne podle scrollWidth: prvek se `justify-content:
     center` přetéká na obě strany a scrollWidth zná jen tu pravou. */
  const boxes = document.querySelectorAll(
    '.btn, .chip, .profile-chip, .mode-tile, .seg button, .tab, .key, .daily-item, .stat, .award',
  )
  for (const el of boxes) {
    const r = seen(el)
    if (!r) continue
    for (const child of el.children) {
      const c = seen(child)
      if (!c) continue
      if (getComputedStyle(child).position === 'absolute') continue
      const over = Math.round(Math.max(r.left - c.left, c.right - r.right))
      if (over > 1) out.spill.push(`${name(el)} přetéká o ${over}px`)
    }
    // Prvek bez dětí (holý nápis) se pozná přes scrollWidth.
    if (el.children.length === 0 && el.scrollWidth - el.clientWidth > 1) {
      out.spill.push(`${name(el)} přetéká o ${el.scrollWidth - el.clientWidth}px`)
    }
  }

  /* 2. Sourozenci na sobě. Překryv se počítá jen mezi prvky se stejným
     rodičem — nabídka nad klávesnicí nebo panel přes desku leží přes okolí
     schválně. */
  const rows = new Set()
  for (const el of document.querySelectorAll('.btn, .chip, .profile-chip, button, .mode-tile')) {
    if (el.parentElement) rows.add(el.parentElement)
  }
  for (const row of rows) {
    const kids = [...row.children].map((el) => ({ el, r: seen(el) })).filter((k) => k.r)
    for (let i = 0; i < kids.length; i++) {
      for (let j = i + 1; j < kids.length; j++) {
        const a = kids[i].r
        const b = kids[j].r
        const w = Math.min(a.right, b.right) - Math.max(a.left, b.left)
        const h = Math.min(a.bottom, b.bottom) - Math.max(a.top, b.top)
        if (w <= 1 || h <= 1) continue
        // Prvek vytažený z toku (nabídka variant, odznak v rohu) leží nad
        // sousedem záměrně.
        const pos = (el) => getComputedStyle(el).position
        if (pos(kids[i].el) !== 'static' || pos(kids[j].el) !== 'static') continue
        out.overlap.push(`${name(kids[i].el)} × ${name(kids[j].el)}`)
      }
    }
  }

  /* 3. Mimo obrazovku. */
  const watched = document.querySelectorAll(
    '.topbar > *, .btn, .chip, .profile-chip, .mode-tile, .key, .hex, .tray-tile, ' +
      '.well-col, .daily-item, .award, .rank-card, .stat, .tile',
  )
  for (const el of watched) {
    const r = seen(el)
    if (!r) continue
    if (r.right > window.innerWidth + 1 || r.left < -1) out.offscreen.push(name(el))
  }

  /* 4. Malé dotykové cíle.
     Počítá se plocha, do které se dá trefit, ne jen ta, která je vidět:
     vysvětlivky přilepené k textu mají neviditelný pseudoprvek navíc, aby
     se do nich dalo ťuknout palcem, aniž by roztáhly svůj řádek. */
  const landscape = window.innerWidth > window.innerHeight
  for (const el of document.querySelectorAll('button, .hex, .tray-tile, .well-col, [role="button"]')) {
    const r = seen(el)
    if (!r) continue
    if (el.disabled) continue
    let width = r.width
    let height = r.height
    for (const which of ['::before', '::after']) {
      const pseudo = getComputedStyle(el, which)
      if (!pseudo.content || pseudo.content === 'none' || pseudo.position !== 'absolute') continue
      width = Math.max(width, parseFloat(pseudo.width) || 0)
      height = Math.max(height, parseFloat(pseudo.height) || 0)
    }
    // Klávesy jsou úzké a vysoké — deset písmen v řadě jinak na 320px
    // displeji nevyjde ani nativní klávesnici. Plochu dohánějí výškou.
    const key =
      el.classList.contains('key') ||
      el.classList.contains('letter-key') ||
      el.classList.contains('well-col')
    const minW = key ? 28 : 40
    const minH = key ? (landscape ? 36 : 44) : 40
    // Zaokrouhluje se stejně, jako se to pak vypíše — jinak by audit hlásil
    // „40×40 je málo" kvůli dvěma desetinám pixelu.
    if (Math.round(width) < minW || Math.round(height) < minH) {
      out.small.push(`${name(el)} ${Math.round(width)}×${Math.round(height)}`)
    }
  }

  for (const list of [out.spill, out.overlap, out.offscreen, out.small]) {
    const unique = [...new Set(list)]
    list.length = 0
    list.push(...unique)
  }
  return out
}

/** Mez na dotykový cíl platí pro prst, ne pro myš. */
let touch = true

async function check(page, where) {
  await page.waitForTimeout(250)
  const found = await page.evaluate(scan)
  if (!touch) found.small.length = 0
  if (found.overflowX > 0) note(where, `stránka přetéká do strany o ${found.overflowX}px`)
  if (found.spill.length) note(where, `nápis leze z tlačítka: ${found.spill.slice(0, 4).join(', ')}`)
  if (found.overlap.length) note(where, `prvky na sobě: ${found.overlap.slice(0, 3).join(', ')}`)
  if (found.offscreen.length) note(where, `mimo obrazovku: ${found.offscreen.slice(0, 4).join(', ')}`)
  if (found.small.length) note(where, `malý cíl: ${found.small.slice(0, 4).join(', ')}`)
}

/**
 * Profil s tím nejširším, co se v liště může sejít: denní řada (čip
 * s plamínkem), dvouciferná série a zásoba inkoustu. S prázdným profilem by
 * se měřila lišta, kterou hráč po pár kolech nikdy neuvidí.
 */
function seedProfile(page) {
  return page.addInitScript((day) => {
    const streak = { lastDay: day, streak: 12, best: 30 }
    const all = (value) => ({
      chain: value, hive: value, tower: value, gallows: value,
      detective: value, tetris: value, quotes: value, intruder: value,
    })
    localStorage.setItem(
      'slova.profile.v1',
      JSON.stringify({
        version: 3,
        guideSeen: true,
        tutorialSeen: all(true),
        dailyStreak: all(streak),
        ink: 128,
        streak: 18,
        xp: 4200,
      }),
    )
  }, new Date().toISOString().slice(0, 10))
}

async function home(page) {
  await page.goto(APP, { waitUntil: 'networkidle' })
  await waitReady(page)
}

async function openGame(page, mode, daily) {
  await home(page)
  await page.locator(`.mode-tile[data-mode="${mode}"]`).click()
  await page.locator('.sheet').waitFor()
  const label = daily ? /^Denní/ : /^(Hrát|Nová hra)$/
  await page.locator('.sheet-actions .btn', { hasText: label }).first().click()
  await page.waitForSelector('.board', { timeout: 20000 })
  await dismissTutorial(page)
}

const browser = await chromium.launch({ executablePath: CHROME })

for (const size of SIZES) {
  console.log(`\n=== ${size.width}×${size.height} ===`)
  touch = !size.desktop
  const context = await browser.newContext({
    viewport: { width: size.width, height: size.height },
    deviceScaleFactor: 2,
    isMobile: !size.desktop,
    hasTouch: !size.desktop,
    locale: 'cs-CZ',
  })
  const page = await context.newPage()
  page.on('pageerror', (error) => note(size.name, `chyba stránky: ${error.message}`))
  await seedProfile(page)

  await home(page)
  await check(page, `${size.name}/menu`)

  // Panel s obtížností a přehled řad — otevírá se z menu přes dlaždici.
  await page.locator('.mode-tile[data-mode="chain"]').click()
  await page.locator('.sheet').waitFor()
  await check(page, `${size.name}/panel hry`)
  await page.keyboard.press('Escape').catch(() => undefined)

  for (const [mode, label] of MODES) {
    for (const daily of [false, true]) {
      await openGame(page, mode, daily)
      await check(page, `${size.name}/${label}${daily ? ' denní' : ''}`)
    }
  }

  // Uvnitř hry: panel nápověd a potvrzení vzdání kola.
  await openGame(page, 'chain', false)
  const hint = page.locator('.board-footer .btn, .hints .btn').first()
  if (await hint.isVisible().catch(() => false)) {
    await hint.click().catch(() => undefined)
    await check(page, `${size.name}/Řetěz po ťuknutí do patičky`)
  }
  const give = page.locator('.btn', { hasText: 'Vzdát kolo' }).first()
  if (await give.isVisible().catch(() => false)) {
    await give.click()
    await check(page, `${size.name}/vzdát kolo`)
    const cancel = page.locator('.sheet .btn', { hasText: /Zrušit|Zpět/ }).first()
    if (await cancel.isVisible().catch(() => false)) await cancel.click()
  }

  // Návod k pravidlům přímo ze hry.
  const rules = page.locator('.topbar .btn-ghost').first()
  if (await rules.isVisible().catch(() => false)) {
    await rules.click().catch(() => undefined)
    if (await page.locator('.tut-card').isVisible().catch(() => false)) {
      await check(page, `${size.name}/návod`)
      await page.locator('.tut-head').getByText('Přeskočit').click()
    }
  }

  // Otázka dne.
  await home(page)
  const quiz = page.locator('.daily-item.daily-quiz, .btn', { hasText: 'Otázka dne' }).first()
  if (await quiz.isVisible().catch(() => false)) {
    await quiz.click()
    await page.waitForSelector('.quiz, .quiz-card', { timeout: 20000 }).catch(() => undefined)
    await check(page, `${size.name}/Otázka dne`)
  }

  // Vitrína, žebříček hodností, statistiky, průvodce.
  await home(page)
  await page.locator('.profile-chip').click()
  await check(page, `${size.name}/vitrína`)
  const ladder = page.locator('.btn', { hasText: 'hodností' }).first()
  if (await ladder.isVisible().catch(() => false)) {
    await ladder.click()
    await check(page, `${size.name}/žebříček`)
  }

  await home(page)
  const stats = page.locator('.btn', { hasText: /Statistik|Výsledky/ }).first()
  if (await stats.isVisible().catch(() => false)) {
    await stats.click()
    await check(page, `${size.name}/statistiky`)
  }

  await home(page)
  const guide = page.locator('.btn', { hasText: /Jak se hraj|Průvodce/ }).first()
  if (await guide.isVisible().catch(() => false)) {
    await guide.click()
    await check(page, `${size.name}/průvodce`)
  }

  await context.close()
}

await browser.close()
console.log(`\n${findings.length === 0 ? 'BEZ NÁLEZŮ' : `NÁLEZŮ: ${findings.length}`}`)
process.exit(findings.length > 0 ? 1 : 0)
