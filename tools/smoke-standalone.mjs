/** Ověří, že jednosouborová verze funguje bez jakéhokoli síťového požadavku. */
import { chromium } from 'playwright'

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
check(await page.locator('h1', { hasText: 'Slova' }).isVisible(), 'stránka se vykreslila')
check(await page.evaluate(() => getComputedStyle(document.querySelector('h1')).fontFamily.includes('Outfit')), 'zabudovaný font se použil')

for (const [mode, sel] of [['Řetěz', '.ladder'], ['Voština', '.hive'], ['Věž', '.tower']]) {
  await page.goto(FILE, { waitUntil: 'networkidle' })
  await page.locator('.mode-card', { hasText: mode }).getByText('Hrát').click()
  await page.waitForSelector(sel, { timeout: 15000 })
  check(true, `${mode} se rozehrál ze zabudovaných dat`)
}

// dohrát řetěz do konce
await page.goto(FILE, { waitUntil: 'networkidle' })
await page.locator('.mode-card', { hasText: 'Řetěz' }).getByText('Hrát').click()
await page.waitForSelector('.ladder')
for (let i = 0; i < 14 && !(await page.locator('.result-card').isVisible()); i++) {
  await page.locator('button', { hasText: 'Celé slovo' }).click()
  await page.waitForTimeout(120)
  await page.keyboard.press('Enter')
  await page.waitForTimeout(300)
}
check(await page.locator('.result-card').isVisible(), 'kolo lze dohrát do konce')

check(external.length === 0, `žádný externí požadavek (${external.length}${external.length ? ': ' + external.slice(0,3).join(', ') : ''})`)

await browser.close()
console.log(problems.length ? `\nPROBLÉMŮ: ${problems.length}` : '\nVŠE PROŠLO')
process.exit(problems.length ? 1 : 0)
