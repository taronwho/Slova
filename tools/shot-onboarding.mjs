import { chromium } from 'playwright'
import { mkdirSync } from 'node:fs'
import { dismissTutorial, goHome, openGame, waitReady } from './_ui.mjs'

const MODE_ID = { 'Řetěz': 'chain', 'Voština': 'hive', 'Věž': 'tower' }
const OUT = new URL('../shots/onboarding/', import.meta.url).pathname
mkdirSync(OUT, { recursive: true })
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' })
const problems = []
const check = (ok, m) => { console.log(`  ${ok?'✓':'✗'} ${m}`); if(!ok) problems.push(m) }

// MOBIL: menu bez rolování + tutoriál
const c = await b.newContext({ viewport:{width:390,height:844}, isMobile:true, hasTouch:true, deviceScaleFactor:2, locale:'cs-CZ' })
const p = await c.newPage()
p.on('pageerror', e => { problems.push('chyba: '+e.message); console.log('  ✗ chyba: '+e.message) })
await p.goto('http://localhost:4173/', { waitUntil:'networkidle' })

const firstCard = await p.evaluate(() => {
  const tiles = [...document.querySelectorAll('.mode-tile')]
  const first = tiles[0]?.getBoundingClientRect()
  const last = tiles[tiles.length - 1]?.getBoundingClientRect()
  return { top: Math.round(first?.top ?? -1), playBottom: Math.round(last?.bottom ?? -1), vh: document.documentElement.clientHeight }
})
check(firstCard.top < 260, `první hra je hned nahoře (začíná na ${firstCard.top}px)`)
check(firstCard.playBottom <= firstCard.vh, `tlačítko Hrát je vidět bez rolování (${firstCard.playBottom}/${firstCard.vh}px)`)
await p.screenshot({ path: `${OUT}mobil-menu.png`, fullPage: false })

// tutoriál se otevře sám při prvním spuštění
await openGame(p, 'chain')
await p.waitForSelector('.tut-card', { timeout: 20000 })
check(true, 'návod se při prvním spuštění otevřel sám')
const steps = await p.locator('.tut-progress span').count()
check(steps >= 5, `návod má ${steps} kroků`)
await p.screenshot({ path: `${OUT}mobil-tutorial-1.png` })

// projít celý návod
for (let i = 0; i < steps - 1; i++) {
  await p.locator('.tut-actions .btn-primary').click()
  await p.waitForTimeout(220)
}
await p.screenshot({ path: `${OUT}mobil-tutorial-posledni.png` })
const finishText = await p.locator('.tut-actions .btn-primary').innerText()
check(/Začít hrát/.test(finishText), `poslední krok nabízí "${finishText}"`)
await p.locator('.tut-actions .btn-primary').click()
await p.waitForTimeout(400)
check(await p.locator('.ladder').isVisible(), 'po návodu se pokračuje do rozehrané hry')

// podruhé už se neotevře
await p.goto('http://localhost:4173/', { waitUntil:'networkidle' })
await openGame(p, 'chain')
await p.waitForSelector('.ladder', { timeout: 20000 })
check(!(await p.locator('.tut-card').isVisible()), 'podruhé se návod sám neotevře')

// tlačítko Pravidla ho vyvolá znovu
await p.locator('.topbar').getByText('Pravidla').click()
await p.waitForSelector('.tut-card')
check(true, 'tlačítko Pravidla návod znovu otevře')
await p.locator('.tut-head').getByText('Přeskočit').click()
await p.waitForTimeout(300)
check(!(await p.locator('.tut-card').isVisible()), 'Přeskočit návod zavře')

// ostatní režimy
for (const mode of ['Voština','Věž']) {
  await p.goto('http://localhost:4173/', { waitUntil:'networkidle' })
  await openGame(p, MODE_ID[mode])
  await p.waitForSelector('.tut-card', { timeout: 20000 })
  check(true, `${mode}: návod se otevřel`)
  await p.screenshot({ path: `${OUT}mobil-tutorial-${mode.toLowerCase()}.png` })
  await p.locator('.tut-head').getByText('Přeskočit').click()
  await p.waitForTimeout(300)
}

// rozbalovací pravidla na domovské obrazovce
await p.goto('http://localhost:4173/', { waitUntil:'networkidle' })
await p.locator('.rules-toggle').first().click()
await p.waitForTimeout(300)
check(await p.locator('.rules-body').first().isVisible(), 'pravidla na domovské obrazovce se rozbalí')
await p.screenshot({ path: `${OUT}mobil-pravidla.png`, fullPage:true })
await c.close()

// DESKTOP
const dc = await b.newContext({ viewport:{width:1280,height:900}, locale:'cs-CZ' })
const dp = await dc.newPage()
await dp.goto('http://localhost:4173/', { waitUntil:'networkidle' })
await dp.screenshot({ path: `${OUT}desktop-menu.png`, fullPage:true })
await openGame(dp, 'tower')
await dp.waitForSelector('.tut-card', { timeout: 20000 })
await dp.screenshot({ path: `${OUT}desktop-tutorial.png` })
await dc.close()

await b.close()
console.log(problems.length ? `\nPROBLÉMŮ: ${problems.length}` : '\nVŠE PROŠLO')
process.exit(problems.length ? 1 : 0)
