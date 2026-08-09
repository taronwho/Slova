/**
 * Podklady pro Google Play.
 *
 * Snímky obrazovky do obchodu se nedělají fotoaparátem z telefonu — musí být
 * přesně velké, čisté a hlavně se dají udělat znovu, až se hra změní. Tenhle
 * skript je vyfotí přímo z běžící hry a k tomu složí hlavní grafiku, kterou
 * Play chce v přesných rozměrech 1024×500.
 *
 * Profil se před focením naplní, aby na snímcích nestálo všude nula: hráč
 * v obchodě se dívá na to, jak hra vypadá rozehraná, ne prázdná.
 *
 * Použití:
 *   npx vite preview --port 4173 &
 *   node tools/play-assets.mjs
 *
 * Výstup:  play/ — snímky 1080×1920 a hlavní grafika 1024×500
 */

import { chromium } from 'playwright'
import { mkdirSync } from 'node:fs'
import { dirname, join } from 'node:path'
import { fileURLToPath } from 'node:url'

import { dismissTutorial, openGame, waitReady } from './_ui.mjs'

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..')
const OUT = join(ROOT, 'play')
const URL = process.env.URL ?? 'http://localhost:4173/'

/**
 * Telefonní snímek pro Play: 1080×1920, tedy přesně 9:16.
 *
 * Skládá se z malého okna a hustého displeje, ne z velkého okna: kdyby se
 * fotilo v šířce 1080 CSS pixelů, hra by se přepnula do rozvržení pro monitor
 * a v obchodě by visely snímky s postranními sloupci, které na telefonu
 * nikdo neuvidí. Výška 720 je schválně nad hranicí 660, pod kterou se hra
 * stahuje do úsporného rozvržení pro malé displeje.
 */
const PHONE = { width: 405, height: 720 }
const DENSITY = 1920 / 720

mkdirSync(OUT, { recursive: true })

/**
 * Profil, se kterým se fotí.
 *
 * Věhlas přes tři čtvrtě milionu = hodnost kolem třicáté, tedy odznak, který
 * už něco vydržel. Sedmidenní řada a plný kalamář dělají totéž pro lištu.
 */
const PROFILE = {
  fame: 900_000,
  streak: 7,
  bestStreak: 12,
  ink: 240,
  guideSeen: true,
  tutorialSeen: {
    chain: true,
    hive: true,
    tower: true,
    gallows: true,
    detective: true,
    tetris: true,
    quotes: true,
    intruder: true,
  },
}

const ME = {
  nick: 'Kroužek',
  wins: 9,
  losses: 4,
  draws: 1,
  matches: [],
  blocked: [],
}

const browser = await chromium.launch({
  executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome',
})

async function open() {
  const page = await browser.newPage({
    viewport: PHONE,
    deviceScaleFactor: DENSITY,
    isMobile: true,
    hasTouch: true,
    locale: 'cs-CZ',
  })
  await page.addInitScript(
    ([profile, me]) => {
      localStorage.setItem('slova.profile.v1', JSON.stringify(profile))
      localStorage.setItem('slova.multi.v1', JSON.stringify(me))
    },
    [PROFILE, ME],
  )
  await page.goto(URL, { waitUntil: 'load' })
  await waitReady(page)
  return page
}

const shots = []
async function shoot(page, name) {
  const file = join(OUT, `${name}.png`)
  await page.waitForTimeout(400)
  await page.screenshot({ path: file })
  shots.push(name)
  console.log(`  ✓ ${name}.png`)
}

console.log('\nSNÍMKY OBRAZOVKY')

// 1. Menu — první, co člověk v obchodě uvidí. Musí být poznat, že her je osm.
{
  const page = await open()
  await shoot(page, '1-menu')
  await page.close()
}

// 2. Voština rozehraná — nejfotogeničtější deska, jakou hra má.
{
  const page = await open()
  await openGame(page, 'hive')
  for (const letter of ['.hex.center', '.hex:nth-of-type(2)', '.hex:nth-of-type(3)']) {
    await page.locator(letter).click().catch(() => undefined)
  }
  await shoot(page, '2-vostina')
  await page.close()
}

// 3. Řetěz — druhá hra, úplně jiný tvar desky.
{
  const page = await open()
  await openGame(page, 'chain')
  await shoot(page, '3-retez')
  await page.close()
}

// 4. Vetřelec — hra, která nejlíp vysvětlí sama sebe jedním obrázkem.
{
  const page = await open()
  await openGame(page, 'intruder')
  await shoot(page, '4-vetrelec')
  await page.close()
}

// 5. Detektiv — ukazuje, že hra umí i něco jiného než skládání písmen.
{
  const page = await open()
  await openGame(page, 'detective')
  await dismissTutorial(page)
  await shoot(page, '5-detektiv')
  await page.close()
}

// 6. Žebříček hodností — osmapadesát odznaků je věc, kvůli které se hraje dál.
{
  const page = await open()
  await page.locator('.profile-chip').click()
  await page.waitForTimeout(400)
  await page.locator('.rank-card').click()
  await page.waitForTimeout(500)
  await page.locator('.ladder-row').nth(28).scrollIntoViewIfNeeded()
  await shoot(page, '6-hodnosti')
  await page.close()
}

// 7. Hra s přáteli — souboje jsou to, co hru odlišuje od hromady jiných.
{
  const page = await open()
  await page.getByRole('button', { name: /Hra s přáteli/ }).first().click()
  await page.waitForTimeout(500)
  await shoot(page, '7-souboje')
  await page.close()
}

/**
 * Hlavní grafika, 1024×500.
 *
 * Skládá se tady, ne v grafickém programu, aby se dala udělat znovu, až se
 * hra přebarví — barvy režimů jsou tytéž proměnné, jaké má hra.
 */
console.log('\nHLAVNÍ GRAFIKA')
{
  const page = await browser.newPage({ viewport: { width: 1024, height: 500 } })
  await page.setContent(`
    <style>
      @import url('${URL}assets/');
      * { margin: 0; box-sizing: border-box; }
      body {
        width: 1024px; height: 500px; display: grid; place-items: center;
        background: radial-gradient(120% 140% at 20% 0%, #2a2154 0%, #121028 60%);
        font-family: system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
        color: #f2f1fa; overflow: hidden;
      }
      .wrap { text-align: center; position: relative; z-index: 2; }
      .brand {
        font-size: 118px; font-weight: 800; letter-spacing: -0.04em; line-height: 1;
      }
      .brand .o {
        display: inline-grid; place-items: center; width: 0.78em; height: 0.78em;
        border-radius: 50%; background: #5b3df5; vertical-align: -0.06em;
      }
      .brand .o i {
        width: 0.3em; height: 0.3em; border-radius: 50%; background: #fff;
      }
      .tag { margin-top: 18px; font-size: 30px; color: #c8c4e6; letter-spacing: 0.01em; }
      .dots { margin-top: 26px; display: flex; gap: 14px; justify-content: center; }
      .dots i { width: 18px; height: 18px; border-radius: 50%; }
      .glow {
        position: absolute; border-radius: 50%; filter: blur(70px); opacity: 0.5;
      }
    </style>
    <div class="glow" style="width:340px;height:340px;background:#5b3df5;left:-90px;top:-120px"></div>
    <div class="glow" style="width:300px;height:300px;background:#e0a91d;right:-80px;bottom:-120px"></div>
    <div class="wrap">
      <div class="brand">Sl<span class="o"><i></i></span>va</div>
      <div class="tag">Osm českých slovních her. I bez signálu.</div>
      <div class="dots">
        <i style="background:#5b3df5"></i><i style="background:#e0a91d"></i>
        <i style="background:#e0433a"></i><i style="background:#0f8a8a"></i>
        <i style="background:#8a6a3a"></i><i style="background:#3fa96a"></i>
        <i style="background:#b0446a"></i><i style="background:#2a8f95"></i>
      </div>
    </div>
  `)
  await page.waitForTimeout(300)
  await page.screenshot({ path: join(OUT, 'feature-1024x500.png') })
  console.log('  ✓ feature-1024x500.png')
  await page.close()
}

await browser.close()
console.log(`\nHOTOVO — ${shots.length} snímků a hlavní grafika v play/\n`)
