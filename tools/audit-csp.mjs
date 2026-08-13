/**
 * Zásada zabezpečení obsahu — kontrola, že hru neuškrtila.
 *
 * `Content-Security-Policy` v hlavičce stránky říká prohlížeči, odkud smí
 * hra brát skripty, styly, obrázky a na koho smí volat. Je to obrana, která
 * nic nestojí, ale má jednu ošklivou vlastnost: **když je moc přísná, nic
 * se nerozbije nahlas**. Hra se tváří normálně, jen jí zmizí písmo, obrázek
 * nebo se tiše nespojí se serverem — a všimne si toho až hráč.
 *
 * Tenhle skript proto hru rozehraje a poslouchá, jestli prohlížeč něco
 * neodmítl. Porušení zásady chodí do konzole jako hláška „Refused to …",
 * a k tomu se dá odchytit i událost `securitypolicyviolation`, kterou
 * prohlížeč pošle na stránku. Bere se obojí, protože se nekryjí:
 * do konzole se některá odmítnutí píšou jen jednou za stránku.
 *
 * Co skript **neověří**: souboje. Firebase je za přihlášením a z testovacího
 * stroje na něj není vidět, takže adresy pro `connect-src` musí projít
 * očima — a hlavně první živý souboj na telefonu.
 *
 * Spuštění:  npm run audit:csp   (nad `dist` na http://localhost:4173)
 */

import { chromium } from 'playwright'

import { waitReady, dismissTutorial } from './_ui.mjs'

const ROOT = process.env.URL ?? 'http://localhost:4173/'
const CHROME = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome'

const problems = []
const check = (ok, msg) => {
  console.log(`  ${ok ? '✓' : '✗'} ${msg}`)
  if (!ok) problems.push(msg)
}

const browser = await chromium.launch({ executablePath: CHROME })
const page = await (
  await browser.newContext({ viewport: { width: 390, height: 844 }, locale: 'cs-CZ' })
).newPage()

/** Odmítnutí, která prohlížeč nahlásil. */
const refused = []
page.on('console', (message) => {
  const text = message.text()
  if (/Content Security Policy|Refused to/i.test(text)) refused.push(text)
})
page.on('pageerror', (error) => refused.push('chyba stránky: ' + error.message))

/** Druhý zdroj: událost, kterou prohlížeč posílá přímo na stránku. */
async function listen() {
  await page.addInitScript(() => {
    window.__cspHits = []
    document.addEventListener('securitypolicyviolation', (event) => {
      window.__cspHits.push(`${event.violatedDirective} ← ${event.blockedURI}`)
    })
  })
}

const hits = async () => (await page.evaluate(() => window.__cspHits ?? [])) ?? []

await listen()

console.log('ZÁSADA JE V HLAVIČCE STRÁNKY')
await page.goto(ROOT, { waitUntil: 'networkidle' })
const policy = await page.evaluate(
  () =>
    document
      .querySelector('meta[http-equiv="Content-Security-Policy" i]')
      ?.getAttribute('content') ?? '',
)
check(policy.length > 0, 'stránka zásadu vůbec má')
for (const rule of [
  "default-src 'self'",
  "script-src 'self'",
  "object-src 'none'",
  "base-uri 'self'",
]) {
  check(policy.replace(/\s+/g, ' ').includes(rule), `obsahuje ${rule}`)
}

console.log('\nHRA SE ROZEHRAJE, ANIŽ PROHLÍŽEČ NĚCO ODMÍTNE')
await waitReady(page)
check((await hits()).length === 0 && refused.length === 0, 'menu se načetlo čistě')

// Písmo je první, co přísná zásada obvykle uškrtí — a pozná se to jen tím,
// že se stránka vykreslí náhradním písmem systému.
const font = await page.evaluate(() => document.fonts.check('1em "Bricolage Grotesque Variable"'))
check(font, 'vlastní písmo se načetlo')

for (const mode of ['hive', 'chain', 'quotes']) {
  await page.locator(`.mode-tile[data-mode="${mode}"]`).click()
  await page.locator('.sheet').waitFor()
  await page.locator('.sheet-actions .btn', { hasText: /^(Hrát|Nová hra)$/ }).first().click()
  await page.waitForSelector('.board, .game', { timeout: 20000 })
  await dismissTutorial(page)
  await page.waitForTimeout(400)
  check((await hits()).length === 0, `${mode}: nic odmítnutého`)
  await page.goto(ROOT, { waitUntil: 'networkidle' })
  await waitReady(page)
}

console.log('\nHRANÍ SAMO O SOBĚ NIKAM NEVOLÁ')
// Zásady ochrany soukromí slibují, že se na server nic nedostane, dokud si
// hráč nezvolí přezdívku. Je to slib, který se dá porušit jedním nešikovným
// importem — Firebase se natahuje až uvnitř funkcí právě proto —, takže se
// hlídá strojově: při obyčejném hraní nesmí odejít požadavek jinam než
// na server, ze kterého hra běží.
const cizi = new Set()
const doma = new URL(ROOT).origin
page.on('request', (request) => {
  const origin = new URL(request.url()).origin
  if (origin !== doma && !request.url().startsWith('data:')) cizi.add(origin)
})
await page.goto(ROOT, { waitUntil: 'networkidle' })
await waitReady(page)
await page.locator('.mode-tile[data-mode="gallows"]').click()
await page.locator('.sheet').waitFor()
await page.locator('.sheet-actions .btn', { hasText: /^(Hrát|Nová hra)$/ }).first().click()
await page.waitForSelector('.board', { timeout: 20000 })
await dismissTutorial(page)
await page.locator('.letter-key:not([disabled])').first().click()
await page.waitForTimeout(600)
check(cizi.size === 0, `žádný cizí server (${[...cizi].join(', ') || 'nic'})`)

console.log('\nSTRÁNKA SE ZÁSADAMI SOUKROMÍ')
await page.goto(ROOT + 'soukromi.html', { waitUntil: 'networkidle' })
await page.waitForTimeout(300)
check((await hits()).length === 0, 'zásady soukromí se načetly čistě')

console.log('\nSERVICE WORKER SE ZAREGISTROVAL')
// `worker-src` je přesně ta direktiva, na kterou se zapomíná, a bez ní
// přestane hra fungovat offline — což je půlka důvodu, proč je to aplikace.
await page.goto(ROOT, { waitUntil: 'networkidle' })
const worker = await page.evaluate(async () => {
  const list = await navigator.serviceWorker.getRegistrations()
  return list.length > 0
})
check(worker, 'registrace prošla')

if (refused.length > 0) {
  console.log('\nODMÍTNUTO:')
  for (const line of new Set(refused)) console.log('  • ' + line)
  problems.push(`prohlížeč odmítl ${refused.length} požadavků`)
}
const seen = await hits()
if (seen.length > 0) {
  console.log('\nPORUŠENÍ ZÁSADY:')
  for (const line of new Set(seen)) console.log('  • ' + line)
}

console.log(problems.length ? `\nNÁLEZY: ${problems.length}` : '\nVŠE PROŠLO')
await browser.close()
process.exit(problems.length > 0 ? 1 : 0)
