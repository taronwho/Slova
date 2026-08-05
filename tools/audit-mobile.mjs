/**
 * Mobilní audit — projde reálné velikosti telefonů a hlásí, co se nevejde
 * na obrazovku, co přetéká do strany a které dotykové cíle jsou moc malé.
 */

import { chromium, devices } from 'playwright'
import { mkdirSync } from 'node:fs'
import { dismissTutorial, goHome, openGame, waitReady } from './_ui.mjs'

const MODE_ID = {
  'Řetěz': 'chain',
  'Voština': 'hive',
  'Věž': 'tower',
  'Šibenice': 'gallows',
  'Detektiv': 'detective',
  'Slabiky': 'tetris',
}

const APP_URL = process.env.URL ?? 'http://localhost:4173/'
const SHOTS = new URL('../shots/mobile/', import.meta.url).pathname
mkdirSync(SHOTS, { recursive: true })

// Nejmenší běžně používané šířky až po velké telefony.
const SIZES = [
  { name: '320-se', width: 320, height: 568 },
  { name: '360-android', width: 360, height: 640 },
  { name: '390-ip14', width: 390, height: 844 },
  { name: '412-pixel', width: 412, height: 915 },
  { name: '740-landscape', width: 740, height: 360 },
]

const MODES = [
  ['Řetěz', '.ladder'],
  ['Voština', '.hive'],
  ['Věž', '.tower'],
  ['Šibenice', '.gallows-art'],
  ['Detektiv', '.clue-card'],
  ['Slabiky', '.well'],
]

// Běžné ovládací prvky: 44px podle doporučení pro dotyk.
// Klávesy virtuální klávesnice mají vlastní, nižší práh na šířku — nativní
// české klávesnice mají na 360dp displeji klávesy kolem 34dp a víc se jich
// do řady prostě nevejde. Kompenzuje se to výškou a rozestupy.
const MIN_TOUCH = 40
const MIN_KEY_WIDTH = 28
const MIN_KEY_HEIGHT = 44

const findings = []
const note = (where, text) => {
  findings.push(`${where}: ${text}`)
  console.log(`  ! ${where}: ${text}`)
}

const browser = await chromium.launch({
  executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome',
})

/**
 * Co z toho, co má být vidět, leží mimo obrazovku.
 *
 * Vodorovné přetečení stránky tohle nechytí: prvek uříznutý předkem
 * s `overflow: hidden` — třeba čip hodnosti vytlačený z horní lišty —
 * dokument nerozšíří, jen tiše zmizí. Přesně to hráč nahlásil.
 */
function offscreen() {
  const bad = []
  const watched = document.querySelectorAll(
    '.topbar > *, .mode-tile, .daily-item, .award, .ladder-row, .rank-card, .stat, .hints .btn',
  )
  for (const el of watched) {
    const r = el.getBoundingClientRect()
    if (r.width === 0 || r.height === 0) continue
    if (r.right > window.innerWidth + 1 || r.left < -1) {
      const what = `${el.className}`.split(' ')[0] || el.tagName.toLowerCase()
      bad.push(`${what} "${(el.textContent || '').trim().slice(0, 14)}"`)
    }
  }
  return [...new Set(bad)].slice(0, 6)
}

for (const size of SIZES) {
  console.log(`\n=== ${size.name} (${size.width}×${size.height}) ===`)
  const context = await browser.newContext({
    viewport: { width: size.width, height: size.height },
    deviceScaleFactor: 2,
    isMobile: true,
    hasTouch: true,
    locale: 'cs-CZ',
    ...devices['Pixel 5'].userAgent ? { userAgent: devices['Pixel 5'].userAgent } : {},
  })
  const page = await context.newPage()
  await page.goto(APP_URL, { waitUntil: 'networkidle' })
  await page.locator('.splash').waitFor({ state: 'detached', timeout: 8000 }).catch(() => undefined)

  const homeOverflow = await page.evaluate(
    () => document.documentElement.scrollWidth - document.documentElement.clientWidth,
  )
  if (homeOverflow > 0) note(`${size.name}/domů`, `přetéká vodorovně o ${homeOverflow}px`)

  /*
   * Mřížka her musí být po otevření vidět, ne se teprve hledat rolováním.
   * Měří se to na šesté dlaždici, tedy na třech řadách ze čtyř: pravidlo
   * vzniklo, když byly hry právě tři řady, a s přibývajícími hrami by
   * doslovné „všechny dlaždice nad okrajem" znamenalo, že každá další hra
   * musí zdola ukrojit z něčeho nahoře. Tři řady jsou dost na to, aby bylo
   * poznat, že se vybírá z mřížky, a aby zbytek byl na dosah palce.
   *
   * Měří se v nejhorším případě, tedy s prázdným profilem, kdy nahoře svítí
   * všechny upomínky naráz.
   */
  const grid = await page.evaluate(() => {
    const tiles = [...document.querySelectorAll('.mode-tile')]
    const sixth = tiles[5]?.getBoundingClientRect()
    return {
      tiles: tiles.length,
      bottom: sixth ? Math.round(sixth.bottom) : 0,
      view: window.innerHeight,
      alerts: document.querySelectorAll('.home-top > *').length,
    }
  })
  if (size.height >= size.width && grid.bottom > grid.view) {
    note(
      `${size.name}/domů`,
      `šestá dlaždice je pod okrajem o ${grid.bottom - grid.view}px ` +
        `(upomínek nahoře: ${grid.alerts})`,
    )
  }
  // Pozor: screenshot s fullPage dočasně mění viewport a Chromium při tom
  // ztratí emulaci dotyku, takže `pointer: coarse` přestane platit. Snímek
  // domovské obrazovky proto až na konci, po všech měřeních.

  // Denní kolo veze v liště čip navíc. Právě on kdysi vytlačil kalamář,
  // sérii i přepínač témat mimo obrazovku na každém telefonu — a audit to
  // neodhalil, protože otevíral jen běžná kola. Proto se lišta měří v obou
  // podobách, než se pustíme do zbytku hry.
  for (const [mode] of MODES) {
    for (const daily of [false, true]) {
      await page.goto(APP_URL, { waitUntil: 'networkidle' })
      await page.locator('.splash').waitFor({ state: 'detached', timeout: 8000 }).catch(() => undefined)
      await openGame(page, MODE_ID[mode], { daily })
      await page.waitForTimeout(300)
      const clipped = await page.evaluate(offscreen)
      if (clipped.length > 0) {
        note(
          `${size.name}/${mode}${daily ? '/denní' : ''}`,
          `mimo obrazovku: ${clipped.join(', ')}`,
        )
      }
    }
  }

  for (const [mode, selector] of MODES) {
    await page.goto(APP_URL, { waitUntil: 'networkidle' })
  await page.locator('.splash').waitFor({ state: 'detached', timeout: 8000 }).catch(() => undefined)
    await openGame(page, MODE_ID[mode])
    await page.waitForSelector(selector, { timeout: 20000 })
    // Návod při prvním spuštění by ležel přes hru a měření by bylo nesmyslné.
    const tut = page.locator('.tut-card')
    if (await tut.isVisible().catch(() => false)) {
      await page.locator('.tut-head').getByText('Přeskočit').click()
    }
    await page.waitForTimeout(400)

    const metrics = await page.evaluate(() => {
      const doc = document.documentElement
      const board = document.querySelector('.board')
      const rect = board?.getBoundingClientRect()
      const small = []
      for (const el of document.querySelectorAll(
        '.board button, .keyboard button, .hex, .tray-tile, .well-col',
      )) {
        const r = el.getBoundingClientRect()
        if (r.width === 0 || r.height === 0) continue
        // Klávesa i sloupec desky jsou úzké a vysoké — plochu mají velkou,
        // jen jinak tvarovanou než běžné tlačítko. Měří se proto jako klávesy.
        const isKey = Boolean(el.closest('.keyboard')) || el.classList.contains('well-col')
        // Na šířku je svislého místa málo a nižší klávesy jsou i na nativních
        // klávesnicích běžné; na výšku se drží plná velikost.
        const landscape = window.innerWidth > window.innerHeight
        const minW = isKey ? 28 : 40
        const minH = isKey ? (landscape ? 36 : 44) : 40
        if (r.width < minW || r.height < minH) {
          const where = el.closest('.keyboard')
            ? 'klávesnice'
            : el.closest('.board-footer')
              ? 'patička'
              : el.closest('.rail')
                ? 'panel'
                : 'plocha'
          small.push(
            `${where}/"${(el.textContent || '').trim().slice(0, 14)}" ` +
              `${Math.round(r.width)}×${Math.round(r.height)}`,
          )
        }
      }
      const footer = document.querySelector('.board-footer')
      const footerRect = footer?.getBoundingClientRect()
      return {
        overflowX: doc.scrollWidth - doc.clientWidth,
        boardBottom: rect ? Math.round(rect.bottom) : 0,
        footerBottom: footerRect ? Math.round(footerRect.bottom) : 0,
        footerTop: footerRect ? Math.round(footerRect.top) : 0,
        hasFooter: Boolean(footer),
        viewportHeight: doc.clientHeight,
        pageHeight: doc.scrollHeight,
        small: [...new Set(small)],
      }
    })

    const label = `${size.name}/${mode}`
    if (metrics.overflowX > 0) note(label, `přetéká vodorovně o ${metrics.overflowX}px`)
    // Se sticky patičkou nevadí, že hrací plocha přesahuje — vadí, když
    // ovládání není vidět bez rolování.
    if (!metrics.hasFooter) {
      note(label, 'chybí přišpendlená patička s ovládáním')
    } else if (metrics.footerBottom > metrics.viewportHeight + 1) {
      note(
        label,
        `ovládání je pod okrajem o ${metrics.footerBottom - metrics.viewportHeight}px`,
      )
    } else if (metrics.footerTop < 0) {
      note(label, 'ovládání je nad horním okrajem')
    }
    if (metrics.small.length > 0) {
      note(
        label,
        `malé dotykové cíle (běžné <${MIN_TOUCH}px, klávesy <${MIN_KEY_WIDTH}×${MIN_KEY_HEIGHT}px): ` +
          metrics.small.slice(0, 4).join(', '),
      )
    }

    const clipped = await page.evaluate(offscreen)
    if (clipped.length > 0) note(label, `mimo obrazovku: ${clipped.join(', ')}`)

    await page.screenshot({
      path: `${SHOTS}${size.name}-${mode.toLowerCase()}.png`,
      fullPage: false,
    })
  }

  await page.goto(APP_URL, { waitUntil: 'networkidle' })
  await page.locator('.splash').waitFor({ state: 'detached', timeout: 8000 }).catch(() => undefined)

  // Vitrína a žebříček hodností. Odznaky, dlaždice ocenění a padesát řádků
  // žebříčku jsou nejhustší obsah v celé hře, takže se na úzkém displeji
  // rozbijí jako první.
  for (const [name, open] of [
    ['vitrína', async () => page.locator('.profile-chip').click()],
    ['žebříček', async () => page.locator('.btn', { hasText: 'hodností' }).first().click()],
  ]) {
    await open()
    await page.waitForTimeout(400)
    const clipped = await page.evaluate(offscreen)
    if (clipped.length > 0) note(`${size.name}/${name}`, `mimo obrazovku: ${clipped.join(', ')}`)
    const wide = await page.evaluate(
      () => document.documentElement.scrollWidth - document.documentElement.clientWidth,
    )
    if (wide > 0) note(`${size.name}/${name}`, `přetéká vodorovně o ${wide}px`)
  }

  await page.goto(APP_URL, { waitUntil: 'networkidle' })
  await page.locator('.splash').waitFor({ state: 'detached', timeout: 8000 }).catch(() => undefined)
  const homeClipped = await page.evaluate(offscreen)
  if (homeClipped.length > 0) note(`${size.name}/domů`, `mimo obrazovku: ${homeClipped.join(', ')}`)

  await page.screenshot({ path: `${SHOTS}${size.name}-home.png`, fullPage: true })
  await context.close()
}

await browser.close()

console.log(`\n${findings.length === 0 ? 'BEZ NÁLEZŮ' : `NÁLEZŮ: ${findings.length}`}`)
