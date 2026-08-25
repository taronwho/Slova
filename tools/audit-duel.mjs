/**
 * Souboje: nedostupný server se musí ozvat, ne mlčet.
 *
 * Hráč nahlásil, že „Vyzvat hráče" zůstane navždycky na „Posílám…" — a bylo
 * to přesně tak. Firebase totiž žádnou lhůtu nemá: dokud se klient nespojí,
 * zápis leží ve frontě a slib se **nikdy nesplní ani nezamítne**. Obrazovka
 * pak čeká na něco, co nikdy nepřijde.
 *
 * Spojení rozbila zásada obsahu (CSP) přidaná při bezpečnostní kontrole:
 * když Firebase neprojde websocketem, přepne na záložní přenos, který si do
 * stránky vloží `<script src="…/.lp?…">` — a `script-src 'self'` ho odmítl.
 * Klient se tím nespojil vůbec a nikde se to nedozvědělo.
 *
 * Tenhle audit kontroluje obojí:
 *
 *   1. **CSP pustí, co Firebase potřebuje** — websocket i záložní přenos.
 *      Měří se doopravdy: stránka si o obojí řekne a hlídá se, jestli to
 *      odmítne zásada (to je chyba), nebo síť (to je tady v pořádku,
 *      databáze je z tohohle stroje nedostupná).
 *   2. **Když je server nedostupný, obrazovka to řekne** — do dvaceti vteřin
 *      se objeví hláška a tlačítko jde zmáčknout znovu. Nikde nesmí zůstat
 *      „Posílám…" ani „Zapisuji…".
 *
 * Odehrát celý souboj odsud nejde, databáze je za bránou; tohle je ta část,
 * kterou ověřit lze — a je to právě ta, která byla rozbitá.
 *
 * Spuštění:  npm run audit:duel   (nad `dist` na http://localhost:4173)
 */

import { chromium } from 'playwright'

import { waitReady } from './_ui.mjs'

const APP = process.env.URL ?? 'http://localhost:4173/'
const CHROME = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome'
/** Adresa databáze — musí sedět s `CONFIG.databaseURL` v src/lib/multi.ts. */
const RTDB = 'slova-b0176-default-rtdb.europe-west1.firebasedatabase.app'

const problems = []
const check = (ok, msg) => {
  console.log(`  ${ok ? '✓' : '✗'} ${msg}`)
  if (!ok) problems.push(msg)
}

const browser = await chromium.launch({ executablePath: CHROME })
const context = await browser.newContext({
  viewport: { width: 412, height: 915 },
  deviceScaleFactor: 2,
  isMobile: true,
  hasTouch: true,
  locale: 'cs-CZ',
})
const page = await context.newPage()

// Odmítnutí zásadou se pozná podle důvodu selhání požadavku.
const odmitnutoCsp = new Set()
page.on('requestfailed', (request) => {
  if (request.failure()?.errorText === 'csp') odmitnutoCsp.add(request.url())
})

await page.goto(APP, { waitUntil: 'networkidle' })
await waitReady(page)

console.log('ZÁSADA OBSAHU PUSTÍ FIREBASE')
const spojeni = await page.evaluate(
  async (host) => {
    const out = {}
    // Hlavní přenos: websocket.
    out.ws = await new Promise((hotovo) => {
      let ws
      try {
        ws = new WebSocket(`wss://${host}/.ws?v=5`)
      } catch (chyba) {
        hotovo(`výjimka: ${String(chyba).slice(0, 80)}`)
        return
      }
      const budik = setTimeout(() => hotovo('bez odpovědi'), 8000)
      ws.onopen = () => {
        clearTimeout(budik)
        hotovo('otevřeno')
        ws.close()
      }
      ws.onerror = () => {
        clearTimeout(budik)
        hotovo('neotevřelo se')
      }
    })
    // Záložní přenos: vložený skript z adresy databáze.
    out.lp = await new Promise((hotovo) => {
      const skript = document.createElement('script')
      skript.src = `https://${host}/.lp?start=t`
      skript.onload = () => hotovo('načteno')
      skript.onerror = () => hotovo('nenačteno')
      document.head.appendChild(skript)
      setTimeout(() => hotovo('bez odpovědi'), 8000)
    })
    return out
  },
  RTDB,
)

const cspWs = [...odmitnutoCsp].some((url) => url.startsWith('wss:'))
const cspLp = [...odmitnutoCsp].some((url) => url.includes('/.lp'))
check(!cspWs, `websocket zásada nezakazuje (${spojeni.ws})`)
check(!cspLp, `záložní přenos zásada nezakazuje (${spojeni.lp})`)
if (spojeni.ws !== 'otevřeno') {
  console.log('    (databáze je z tohohle stroje nedostupná — měří se zásada, ne dosah)')
}

console.log('\nNEDOSTUPNÝ SERVER SE OZVE, MÍSTO ABY MLČEL')
const vstup = page.locator('.friends-entry, .btn', { hasText: /přáteli/i }).first()
check(await vstup.isVisible().catch(() => false), 'vstup do soubojů je v menu vidět')
await vstup.click()
await page.locator('.friends').waitFor({ timeout: 10000 })

const pole = page.locator('.friends-claim input').first()
if (await pole.isVisible().catch(() => false)) {
  await pole.fill('zkouskaserveru')
  const tlacitko = page.locator('.friends-claim .btn').first()
  await tlacitko.click()
  // Lhůta v `multi.ts` je 12 s; s rezervou na přihlašování se čeká 25.
  await page.waitForFunction(
    () => {
      const btn = document.querySelector('.friends-claim .btn')
      return btn ? !/…/.test(btn.textContent ?? '') : true
    },
    undefined,
    { timeout: 25000 },
  ).catch(() => undefined)

  const napis = (await tlacitko.innerText().catch(() => '')).trim()
  check(!napis.includes('…'), `tlačítko se odemklo (${napis || 'zmizelo'})`)
  const hlaska = await page.locator('.duel-problem').first().innerText().catch(() => '')
  check(hlaska.length > 0, `hráč se dozvěděl, co se stalo („${hlaska}")`)
} else {
  check(false, 'zabrání přezdívky se nedá vyzkoušet — pole není vidět')
}

console.log(problems.length ? `\nNÁLEZY: ${problems.length}` : '\nVŠE PROŠLO')
await browser.close()
process.exit(problems.length > 0 ? 1 : 0)
