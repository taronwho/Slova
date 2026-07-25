import { chromium } from 'playwright'
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' })
const p = await (await b.newContext({ viewport:{width:390,height:844}, isMobile:true, hasTouch:true, deviceScaleFactor:2, locale:'cs-CZ' })).newPage()
await p.goto('http://localhost:4173/', { waitUntil:'networkidle' })
await p.locator('.mode-card', { hasText:'Řetěz' }).getByText('Hrát').click()
await p.waitForSelector('.tut-card')
await p.locator('.tut-actions .btn-primary').click()   // krok 2 = tvary slov
await p.waitForTimeout(400)
console.log('nadpis:', await p.locator('.tut-body h2').innerText())
await p.screenshot({ path: 'shots/tutorial-tvary.png' })
await b.close()
