/** Ověří, že jednosouborová verze funguje bez jakéhokoli síťového požadavku. */
import { chromium } from 'playwright'
import { readFileSync, writeFileSync, unlinkSync } from 'node:fs'

const FILE = process.env.SURL ?? 'http://localhost:4180/slova-standalone.html'
const problems = []
const check = (ok, msg) => { console.log(`  ${ok ? '✓' : '✗'} ${msg}`); if (!ok) problems.push(msg) }

const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' })
const page = await (await browser.newContext({ viewport: { width: 1280, height: 900 }, locale: 'cs-CZ' })).newPage()

const external = []
page.on('request', r => {
  const u = r.url()
  // Samotný dokument a favicon nejsou herní data.
  if (u === FILE || u.startsWith('data:') || u.endsWith('/favicon.ico')) return
  external.push(u)
})
page.on('pageerror', e => { problems.push('chyba: ' + e.message); console.log('  ✗ chyba: ' + e.message) })
page.on('console', m => { if (m.type() === 'error' && !/favicon/.test(m.location()?.url ?? '')) { problems.push('console: ' + m.text()); console.log('  ✗ console: ' + m.text()) } })

await page.goto(FILE, { waitUntil: 'networkidle' })
check(
  await page.locator('h1', { hasText: 'Vyber si hru' }).isVisible(),
  'stránka se vykreslila',
)

/** Po prvním spuštění režimu leží přes hru návod — test ho odbaví. */
async function dismissTutorial(target) {
  const card = target.locator('.tut-card')
  if (await card.isVisible().catch(() => false)) {
    await target.locator('.tut-head').getByText('Přeskočit').click()
    await target.waitForTimeout(250)
  }
}
check(
  await page.evaluate(() =>
    getComputedStyle(document.querySelector('h1')).fontFamily.includes('Bricolage'),
  ),
  'zabudovaný font se použil',
)

for (const [mode, sel] of [['Řetěz', '.ladder'], ['Voština', '.hive'], ['Věž', '.tower']]) {
  await page.goto(FILE, { waitUntil: 'networkidle' })
  await page.locator('.mode-card', { hasText: mode }).getByText('Hrát').click()
  await page.waitForSelector(sel, { timeout: 15000 })
  await dismissTutorial(page)
  check(true, `${mode} se rozehrál ze zabudovaných dat`)
}

// dohrát řetěz do konce
await page.goto(FILE, { waitUntil: 'networkidle' })
await page.locator('.mode-card', { hasText: 'Řetěz' }).getByText('Hrát').click()
await page.waitForSelector('.ladder')
await dismissTutorial(page)
for (let i = 0; i < 14 && !(await page.locator('.result-card').isVisible()); i++) {
  await page.locator('button', { hasText: 'Celé slovo' }).click()
  await page.waitForTimeout(120)
  await page.keyboard.press('Enter')
  await page.waitForTimeout(300)
}
check(await page.locator('.result-card').isVisible(), 'kolo lze dohrát do konce')

check(external.length === 0, `žádný externí požadavek (${external.length}${external.length ? ': ' + external.slice(0,3).join(', ') : ''})`)

// Na telefonu se stránka musí vykreslit v šířce displeje, ne v 980px.
// Bez `viewport` prohlížeč vykreslí desktopové rozvržení a jen ho zmenší.
const mobile = await (await browser.newContext({
  viewport: { width: 390, height: 844 },
  isMobile: true,
  hasTouch: true,
  deviceScaleFactor: 3,
  locale: 'cs-CZ',
})).newPage()
await mobile.goto(FILE, { waitUntil: 'networkidle' })
const vp = await mobile.evaluate(() => ({
  width: window.innerWidth,
  mobileLayout: matchMedia('(max-width: 899px)').matches,
}))
check(vp.width === 390, `stránka se vykreslí v šířce displeje (${vp.width}px)`)
check(vp.mobileLayout, 'uplatní se mobilní rozvržení')
await mobile.locator('.mode-card', { hasText: 'Řetěz' }).getByText('Hrát').click()
await mobile.waitForSelector('.ladder', { timeout: 15000 })
await dismissTutorial(mobile)
const kb = await mobile.evaluate(() => {
  const footer = document.querySelector('.board-footer')
  const r = footer?.getBoundingClientRect()
  return r ? Math.round(r.bottom) <= document.documentElement.clientHeight + 1 : false
})
check(kb, 'ovládání je na telefonu vidět bez rolování')

// Hostitel může stránku zabalit do vlastní hlavičky, ve které už nějaký
// `viewport` je. Ten by ten náš přebil, kdyby se spoléhalo jen na značku
// v obsahu — proto ho bootstrap skript přepisuje. Tady se to ověřuje.
const dir = new URL('../dist/', import.meta.url).pathname
const wrapped = `${dir}.wrapped-test.html`
writeFileSync(
  wrapped,
  '<!doctype html><html lang="cs"><head><meta charset="utf-8">' +
    '<meta name="viewport" content="width=1024">' +
    '<title>Hostitel</title></head><body>' +
    readFileSync(`${dir}slova-standalone.html`, 'utf-8') +
    '</body></html>',
)

const hosted = await (await browser.newContext({
  viewport: { width: 390, height: 844 },
  isMobile: true,
  hasTouch: true,
  deviceScaleFactor: 3,
})).newPage()
await hosted.goto(FILE.replace('slova-standalone.html', '.wrapped-test.html'), {
  waitUntil: 'networkidle',
})
const hostedWidth = await hosted.evaluate(() => window.innerWidth)
check(
  hostedWidth === 390,
  `obal hostitele s vlastním viewportem stránku nerozbije (${hostedWidth}px)`,
)
unlinkSync(wrapped)

await browser.close()
console.log(problems.length ? `\nPROBLÉMŮ: ${problems.length}` : '\nVŠE PROŠLO')
process.exit(problems.length ? 1 : 0)
