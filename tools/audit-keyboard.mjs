/**
 * Podržení klávesy a vytažené písmeno s háčkem.
 *
 * Hráč hlásil, že v Řetězu po podržení klávesy sice vyskočí písmeno
 * s diakritikou, ale klepnutí na ně provede **tlačítko pod ním** — vrátí
 * tah nebo nabídne vzdání kola. Nabídka se totiž otevírá nad klávesnicí
 * a přesně tam, kde v Řetězu leží ovládací tlačítka.
 *
 * Chyba je v pořadí událostí na dotykovém displeji, ne v CSS:
 *
 *   1. prst se zvedne         → `pointerup` na vytažené variantě,
 *   2. napíše se písmeno a nabídka se **odstraní z DOMu**,
 *   3. prohlížeč pošle dodatečné `click` (kvůli starým stránkám psaným
 *      na myš) a znovu se ptá, co je na těch souřadnicích — nabídka už
 *      tam není, takže klepnutí spadne na tlačítko pod ní.
 *
 * Písmeno se přitom napsalo správně; hned nato ho ale *Vrátit tah* smazal,
 * takže to vypadalo, že se klepnutí vůbec nepovedlo.
 *
 * Skript to hraje jako člověk: dotykem, s podržením a zvlášť mířeným
 * klepnutím. Bez skutečného dotyku se chyba neprojeví — myš dodatečné
 * `click` neposílá.
 *
 * Spuštění:  npm run audit:keyboard   (nad `dist` na http://localhost:4173)
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
const context = await browser.newContext({
  viewport: { width: 390, height: 844 },
  locale: 'cs-CZ',
  hasTouch: true,
  isMobile: true,
})
const page = await context.newPage()
page.on('pageerror', (error) => problems.push('chyba stránky: ' + error.message))

/** Rozehraje Řetěz na volné hře. */
async function openChain() {
  await page.goto(ROOT, { waitUntil: 'networkidle' })
  await waitReady(page)
  await page.locator('.mode-tile[data-mode="chain"]').tap()
  await page.locator('.sheet').waitFor()
  await page.locator('.sheet-actions .btn', { hasText: /^(Hrát|Nová hra)$/ }).first().tap()
  await page.waitForSelector('.board', { timeout: 20000 })
  await dismissTutorial(page)
}

/** Podrží klávesu, dokud nevyskočí nabídka variant. */
async function hold(letter) {
  const key = page.locator(`.key-slot:has(> .key:text-is("${letter}")) > .key`).first()
  const box = await key.boundingBox()
  await page.touchscreen.tap(-10, -10).catch(() => undefined)
  const client = await page.context().newCDPSession(page)
  const x = box.x + box.width / 2
  const y = box.y + box.height / 2
  await client.send('Input.dispatchTouchEvent', {
    type: 'touchStart',
    touchPoints: [{ x, y }],
  })
  await page.waitForTimeout(450)
  await client.send('Input.dispatchTouchEvent', { type: 'touchEnd', touchPoints: [] })
  return { client, x, y }
}

await openChain()

console.log('PODRŽENÍ VYTÁHNE PÍSMENO S HÁČKEM')
await hold('e')
const nabidka = page.locator('.key-variants')
check(await nabidka.isVisible(), 'nabídka variant se otevřela')
const varianty = await nabidka.locator('.key.variant').allInnerTexts()
check(varianty.join('').toLowerCase() === 'ěé', `nabízí ě a é (${varianty.join(' ')})`)

console.log('\nKLEPNUTÍ NA VYTAŽENÉ PÍSMENO NAPÍŠE PRÁVĚ TO PÍSMENO')
// Nabídka leží nad klávesnicí, tedy přes tlačítka Řetězu. Přesně tam
// klepnutí padalo do tlačítka místo do písmene.
const pod = await page.evaluate(() => {
  const one = document.querySelector('.key-variants .key.variant')
  const box = one.getBoundingClientRect()
  const x = box.left + box.width / 2
  const y = box.top + box.height / 2
  const stack = document.elementsFromPoint(x, y)
  return {
    prvni: stack[0]?.className ?? '',
    tlacitko: stack.find((el) => el.matches('.board-footer .btn'))?.textContent ?? null,
  }
})
check(pod.prvni.includes('variant'), `nejvýš leží varianta, ne něco jiného (${pod.prvni})`)
if (pod.tlacitko) console.log(`    (pod ní leží tlačítko „${pod.tlacitko}")`)

const pred = await page.locator('.rung:has(button.tile)').first().innerText().catch(() => '')
await page.locator('.key-variants .key.variant', { hasText: 'ě' }).tap()
await page.waitForTimeout(400)

const napsano = await page.evaluate(() => {
  const draft = document.querySelector('.rung:has(button.tile)')
  return draft ? draft.innerText.replace(/\s+/g, '') : ''
})
check(napsano.toLowerCase().includes('ě'), `písmeno se napsalo (${napsano || 'nic'})`)
check(!(await page.locator('.confirm-card, .sheet-confirm').isVisible().catch(() => false)),
  'neotevřelo se okno „Vzdát kolo"')
check(!(await nabidka.isVisible().catch(() => false)), 'nabídka se po výběru zavřela')

console.log('\nPODRŽENÍ A SJETÍ PRSTEM NA VARIANTU')
// Tak se to dělá na systémové klávesnici: prst se nezvedne, jen sjede.
await page.goto(ROOT, { waitUntil: 'networkidle' })
await openChain()
{
  const key = page.locator('.key-slot:has(> .key:text-is("a")) > .key').first()
  const box = await key.boundingBox()
  const client = await page.context().newCDPSession(page)
  const x = box.x + box.width / 2
  const y = box.y + box.height / 2
  await client.send('Input.dispatchTouchEvent', { type: 'touchStart', touchPoints: [{ x, y }] })
  await page.waitForTimeout(450)
  const cil = await page.locator('.key-variants .key.variant').first().boundingBox()
  await client.send('Input.dispatchTouchEvent', {
    type: 'touchMove',
    touchPoints: [{ x: cil.x + cil.width / 2, y: cil.y + cil.height / 2 }],
  })
  await page.waitForTimeout(120)
  await client.send('Input.dispatchTouchEvent', { type: 'touchEnd', touchPoints: [] })
  await page.waitForTimeout(400)
  const draft = await page.evaluate(() => {
    const one = document.querySelector('.rung:has(button.tile)')
    return one ? one.innerText.replace(/\s+/g, '') : ''
  })
  check(draft.toLowerCase().includes('á'), `sjetí prstem napsalo á (${draft || 'nic'})`)
}

console.log(problems.length ? `\nNÁLEZY: ${problems.length}` : '\nVŠE PROŠLO')
await browser.close()
process.exit(problems.length > 0 ? 1 : 0)
