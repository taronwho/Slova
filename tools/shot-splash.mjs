/** Snímky úvodní značky v průběhu animace. */
import { chromium } from 'playwright'
import { mkdirSync } from 'node:fs'
const SHOTS = new URL('../shots/', import.meta.url).pathname
mkdirSync(SHOTS, { recursive: true })
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' })
for (const theme of ['light', 'dark']) {
  const p = await (await b.newContext({ viewport: { width: 390, height: 780 }, locale: 'cs-CZ', deviceScaleFactor: 2, colorScheme: theme })).newPage()
  await p.goto(process.env.URL ?? 'http://localhost:4173/')
  for (const t of [350, 750]) {
    await p.waitForTimeout(t === 350 ? 350 : 400)
    await p.screenshot({ path: `${SHOTS}splash-${theme}-${t}.png` })
  }
  await p.close()
}
await b.close()
console.log('ok')
