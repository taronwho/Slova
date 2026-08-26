/**
 * Aktualizace: hra se musí přepnout na novou verzi sama.
 *
 * Hráč tři a půl hodiny hrál verzi, kterou už nahradily dvě novější — a nic
 * mu to neřeklo. Nainstalovaná aplikace se totiž na telefonu nezavírá, jen
 * odloží na pozadí a zas vytáhne, a stránka se přitom **nenačítá znovu**.
 * Kontrola verze při načtení se tak nemusí spustit celé dny.
 *
 * Tenhle audit to hraje přesně tak: otevře starou verzi, pak se pod ní
 * vymění soubory za novou (jako by mezitím proběhlo nasazení), hra se
 * odloží na pozadí a zase vytáhne. Musí sama naskočit na novou.
 *
 * Spuštění:  npm run audit:update
 */

import { chromium } from 'playwright'
import { cpSync, mkdirSync, readFileSync, rmSync, writeFileSync } from 'node:fs'
import { createServer } from 'node:http'
import { extname, join, normalize } from 'node:path'

const CHROME = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome'
const ROOT = new URL('../', import.meta.url).pathname
const DIST = join(ROOT, 'dist')
const HRISTE = join(ROOT, 'dist-update')

const problems = []
const check = (ok, msg) => {
  console.log(`  ${ok ? '✓' : '✗'} ${msg}`)
  if (!ok) problems.push(msg)
}

/** Malý server nad `dist-update`, ať se dá obsah pod běžící hrou vyměnit. */
const TYPY = {
  '.html': 'text/html; charset=utf-8',
  '.js': 'text/javascript',
  '.css': 'text/css',
  '.json': 'application/json',
  '.webmanifest': 'application/manifest+json',
  '.png': 'image/png',
  '.svg': 'image/svg+xml',
}
const server = createServer((req, res) => {
  const cesta = decodeURIComponent((req.url ?? '/').split('?')[0])
  const soubor = join(HRISTE, normalize(cesta).replace(/^(\.\.[/\\])+/, ''))
  const cil = cesta.endsWith('/') ? join(soubor, 'index.html') : soubor
  try {
    const data = readFileSync(cil)
    res.writeHead(200, {
      'Content-Type': TYPY[extname(cil)] ?? 'application/octet-stream',
      // Jako na GitHub Pages: HTML se nesmí držet, otisknuté soubory ano.
      'Cache-Control': extname(cil) === '.html' ? 'no-cache' : 'max-age=600',
    })
    res.end(data)
  } catch {
    res.writeHead(404)
    res.end('nenalezeno')
  }
})
await new Promise((hotovo) => server.listen(4175, hotovo))
const APP = 'http://localhost:4175/'

/** Postaví „starou" verzi: tatáž hra, jen s jiným otiskem v názvu souboru. */
function pripravStarou() {
  rmSync(HRISTE, { recursive: true, force: true })
  mkdirSync(HRISTE, { recursive: true })
  cpSync(DIST, HRISTE, { recursive: true })
  const html = readFileSync(join(HRISTE, 'index.html'), 'utf8')
  const jmeno = html.match(/assets\/index-[A-Za-z0-9_-]+\.js/)?.[0]
  if (!jmeno) throw new Error('v index.html není hlavní skript')
  const stare = jmeno.replace(/index-/, 'index-stara')
  cpSync(join(HRISTE, jmeno), join(HRISTE, stare))
  writeFileSync(
    join(HRISTE, 'index.html'),
    html.split(jmeno).join(stare).replace('verze ', 'verze STARÁ '),
  )
  return { nove: jmeno, stare }
}

const { nove, stare } = pripravStarou()
console.log(`stará: ${stare}\nnová:  ${nove}\n`)

const browser = await chromium.launch({ executablePath: CHROME })
const context = await browser.newContext({
  viewport: { width: 412, height: 915 },
  deviceScaleFactor: 2,
  isMobile: true,
  hasTouch: true,
  locale: 'cs-CZ',
})
const page = await context.newPage()

console.log('HRÁČ OTEVŘE STAROU VERZI')
await page.goto(APP, { waitUntil: 'networkidle' })
await page.waitForTimeout(2500)
const bezi = () => page.evaluate(() => [...document.scripts].map((s) => s.src).join(' '))
check((await bezi()).includes('index-stara'), 'běží stará verze')

console.log('\nMEZITÍM SE NASADÍ NOVÁ')
// Vymění se jen index.html; otisknuté soubory zůstávají oba, jako po
// skutečném nasazení.
const html = readFileSync(join(DIST, 'index.html'), 'utf8')
writeFileSync(join(HRISTE, 'index.html'), html)

// Mezi kontrolami má hra odstup, aby nechodila na server při každém
// přepnutí mezi aplikacemi. Test si ho musí odsedět, jinak by měřil ten
// odstup, ne aktualizaci.
console.log('\n(čekám, až uplyne odstup mezi kontrolami)')
await page.waitForTimeout(32000)

console.log('\nHRA SE ODLOŽÍ NA POZADÍ A ZASE VYTÁHNE')
/*
 * Tohle dělá telefon, když se hra přepne do jiné aplikace a zpátky.
 * Stránka se **nenačítá znovu** — jen se změní `visibilityState`.
 */
await page.evaluate(() => {
  Object.defineProperty(document, 'visibilityState', { value: 'hidden', configurable: true })
  document.dispatchEvent(new Event('visibilitychange'))
})
await page.waitForTimeout(500)
await page.evaluate(() => {
  Object.defineProperty(document, 'visibilityState', { value: 'visible', configurable: true })
  document.dispatchEvent(new Event('visibilitychange'))
})

// Hra se má sama přenačíst na novou verzi.
const naskocila = await page
  .waitForFunction(
    () => [...document.scripts].some((s) => s.src.includes('/index-') && !s.src.includes('index-stara')),
    undefined,
    { timeout: 30000 },
  )
  .then(() => true)
  .catch(() => false)
check(naskocila, `hra sama naskočila na novou verzi${naskocila ? '' : ` (pořád ${stare})`}`)

if (naskocila) {
  await page.waitForTimeout(1500)
  const zdrava = await page.locator('.mode-tile').first().isVisible().catch(() => false)
  check(zdrava, 'a po přenačtení se normálně otevře')
}

server.close()
rmSync(HRISTE, { recursive: true, force: true })
console.log(problems.length ? `\nNÁLEZY: ${problems.length}` : '\nVŠE PROŠLO')
await browser.close()
process.exit(problems.length > 0 ? 1 : 0)
