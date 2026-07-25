/**
 * Mobilní audit — projde reálné velikosti telefonů a hlásí, co se nevejde
 * na obrazovku, co přetéká do strany a které dotykové cíle jsou moc malé.
 */

import { chromium, devices } from 'playwright'
import { mkdirSync } from 'node:fs'

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

  const homeOverflow = await page.evaluate(
    () => document.documentElement.scrollWidth - document.documentElement.clientWidth,
  )
  if (homeOverflow > 0) note(`${size.name}/domů`, `přetéká vodorovně o ${homeOverflow}px`)
  // Pozor: screenshot s fullPage dočasně mění viewport a Chromium při tom
  // ztratí emulaci dotyku, takže `pointer: coarse` přestane platit. Snímek
  // domovské obrazovky proto až na konci, po všech měřeních.

  for (const [mode, selector] of MODES) {
    await page.goto(APP_URL, { waitUntil: 'networkidle' })
    await page.locator('.mode-card', { hasText: mode }).getByText('Hrát').click()
    await page.waitForSelector(selector, { timeout: 20000 })
    await page.waitForTimeout(400)

    const metrics = await page.evaluate(() => {
      const doc = document.documentElement
      const board = document.querySelector('.board')
      const rect = board?.getBoundingClientRect()
      const small = []
      for (const el of document.querySelectorAll(
        '.board button, .keyboard button, .hex, .tray-tile',
      )) {
        const r = el.getBoundingClientRect()
        if (r.width === 0 || r.height === 0) continue
        const isKey = Boolean(el.closest('.keyboard'))
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

    await page.screenshot({
      path: `${SHOTS}${size.name}-${mode.toLowerCase()}.png`,
      fullPage: false,
    })
  }

  await page.goto(APP_URL, { waitUntil: 'networkidle' })
  await page.screenshot({ path: `${SHOTS}${size.name}-home.png`, fullPage: true })
  await context.close()
}

await browser.close()

console.log(`\n${findings.length === 0 ? 'BEZ NÁLEZŮ' : `NÁLEZŮ: ${findings.length}`}`)
