/**
 * Ověří, že je z hry plnohodnotná PWA — tedy že ji jde zabalit do Google Play
 * přes Trusted Web Activity: manifest, ikony včetně maskable, service worker
 * a hlavně skutečný běh po odpojení sítě.
 */

import { chromium } from 'playwright'
import { dismissTutorial, goHome, openGame, waitReady } from './_ui.mjs'

const MODE_ID = { 'Řetěz': 'chain', 'Voština': 'hive', 'Věž': 'tower' }

const APP_URL = process.env.URL ?? 'http://localhost:4173/'
const problems = []
const check = (ok, message) => {
  console.log(`  ${ok ? '✓' : '✗'} ${message}`)
  if (!ok) problems.push(message)
}

const browser = await chromium.launch({
  executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome',
})
const context = await browser.newContext({
  viewport: { width: 390, height: 844 },
  isMobile: true,
  hasTouch: true,
  locale: 'cs-CZ',
})
const page = await context.newPage()
await page.goto(APP_URL, { waitUntil: 'networkidle' })
  await page.locator('.splash').waitFor({ state: 'detached', timeout: 8000 }).catch(() => undefined)

/* ---------- Manifest ---------- */

const manifestHref = await page.getAttribute('link[rel=manifest]', 'href')
check(Boolean(manifestHref), 'stránka odkazuje na manifest')

const manifest = await page.evaluate(async (href) => {
  const response = await fetch(href)
  return response.ok ? response.json() : null
}, manifestHref)

check(manifest !== null, 'manifest se načte')
if (manifest) {
  check(Boolean(manifest.name && manifest.short_name), 'manifest má název')
  check(manifest.display === 'standalone', `display je standalone (${manifest.display})`)
  check(Boolean(manifest.start_url), 'manifest má start_url')
  check(/^#[0-9a-f]{6}$/i.test(manifest.theme_color ?? ''), 'manifest má theme_color')
  check(
    /^#[0-9a-f]{6}$/i.test(manifest.background_color ?? ''),
    'manifest má background_color',
  )

  const sizes = (manifest.icons ?? []).map((i) => i.sizes)
  check(sizes.includes('192x192'), 'ikona 192×192 (minimum pro instalaci)')
  check(sizes.includes('512x512'), 'ikona 512×512 (nutná pro Play Store)')
  check(
    (manifest.icons ?? []).some((i) => (i.purpose ?? '').includes('maskable')),
    'maskable ikona (jinak Android ořízne obsah)',
  )

  const iconResults = await page.evaluate(async (icons) => {
    const out = []
    for (const icon of icons) {
      const response = await fetch(icon.src)
      out.push({ src: icon.src, ok: response.ok })
    }
    return out
  }, manifest.icons ?? [])
  const missing = iconResults.filter((r) => !r.ok)
  check(missing.length === 0, `všechny ikony existují${missing.length ? `: chybí ${missing.map((m) => m.src).join(', ')}` : ''}`)
}

/* ---------- Service worker ---------- */

await page.waitForTimeout(1500)
const swState = await page.evaluate(async () => {
  const registration = await navigator.serviceWorker.getRegistration()
  if (!registration) return null
  await navigator.serviceWorker.ready
  return { scope: registration.scope, active: Boolean(registration.active) }
})
check(swState !== null && swState.active, 'service worker je zaregistrovaný a aktivní')

/* ---------- Offline ---------- */

// Projít režimy, aby se datové balíčky dostaly do cache.
for (const mode of ['Řetěz', 'Voština', 'Věž']) {
  await page.goto(APP_URL, { waitUntil: 'networkidle' })
  await page.locator('.splash').waitFor({ state: 'detached', timeout: 8000 }).catch(() => undefined)
  await openGame(page, MODE_ID[mode])
  await page.waitForSelector('.board', { timeout: 20000 })
  const tut = page.locator('.tut-card')
  if (await tut.isVisible().catch(() => false)) {
    await page.locator('.tut-head').getByText('Přeskočit').click()
  }
  await page.waitForTimeout(500)
}

await context.setOffline(true)
await page.goto(APP_URL, { waitUntil: 'domcontentloaded' })
await page.waitForTimeout(800)

const offlineOk = await page
  .locator('h1', { hasText: 'Vyber si hru' })
  .isVisible()
  .catch(() => false)
check(offlineOk, 'aplikace se načte i offline')

if (offlineOk) {
  await openGame(page, 'chain')
  const played = await page
    .waitForSelector('.ladder', { timeout: 15000 })
    .then(() => true)
    .catch(() => false)
  check(played, 'hádanku lze rozehrát i offline')
}

await context.setOffline(false)
await browser.close()

console.log(problems.length === 0 ? '\nVŠE PROŠLO' : `\nPROBLÉMŮ: ${problems.length}`)
process.exit(problems.length === 0 ? 0 : 1)
