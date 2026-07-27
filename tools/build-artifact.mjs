/**
 * Sestaví hru do jediného HTML souboru — pro hostování, kde stránka nesmí
 * nic dotahovat ze sítě (přísná CSP, žádné sourozenecké soubory).
 *
 * Vše se vloží dovnitř: CSS, JS, fonty jako data URI a herní data do
 * window.__SLOVA_DATA__. Datové sady se ořezávají, aby stránka zůstala
 * v rozumné velikosti; plná verze je ve statickém buildu v dist/.
 */

import { execSync } from 'node:child_process'
import { readFileSync, readdirSync, writeFileSync, existsSync } from 'node:fs'
import { join, dirname } from 'node:path'
import { fileURLToPath } from 'node:url'

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..')
const DIST = join(ROOT, 'dist')
const DATA = join(ROOT, 'public', 'data')
// Kontrolní build se ukládá vedle ostrého, ať se dají držet oba naráz.
const OUT = join(
  ROOT,
  'dist',
  process.env.QUIZ_ALL === '1' ? 'slova-kontrolni.html' : 'slova-standalone.html',
)

// Kolik balíčků se do jednosouborové verze vejde. Řetěz jde celý, u ostatních
// je to výřez — pořád stovky hádanek na režim.
const HIVE_PACKS = 14
const TOWER_PACKS = 16

console.log('Build…')
execSync('npx vite build', { cwd: ROOT, stdio: 'inherit' })

const html = readFileSync(join(DIST, 'index.html'), 'utf-8')

/* ---------- CSS + fonty ---------- */

const cssName = readdirSync(join(DIST, 'assets')).find((f) => f.endsWith('.css'))
let css = readFileSync(join(DIST, 'assets', cssName), 'utf-8')

let fontBytes = 0
css = css.replace(/url\(([^)]*?\.woff2)\)/g, (whole, url) => {
  const file = url.replace(/^["']|["']$/g, '').replace(/^.*\//, '')
  const path = join(DIST, 'assets', file)
  if (!existsSync(path)) return whole
  const buffer = readFileSync(path)
  fontBytes += buffer.length
  return `url(data:font/woff2;base64,${buffer.toString('base64')})`
})

/* ---------- Herní data ---------- */

const readJson = (...parts) => JSON.parse(readFileSync(join(DATA, ...parts), 'utf-8'))
const embedded = {}

for (const length of [4, 5, 6]) {
  embedded[`chain/words-${length}.json`] = readJson('chain', `words-${length}.json`)
  embedded[`chain/puzzles-${length}.json`] = readJson('chain', `puzzles-${length}.json`)
}

// Index se ořízne na skutečně vložené balíčky, ať hra nikdy nesáhne po tom,
// co v souboru není.
const hiveIndex = readJson('hive', 'index.json')
hiveIndex.hives = hiveIndex.hives.filter((h) => h.pack < HIVE_PACKS)
embedded['hive/index.json'] = hiveIndex
for (let i = 0; i < HIVE_PACKS; i++) {
  const name = `pack-${String(i).padStart(3, '0')}.json`
  embedded[`hive/${name}`] = readJson('hive', name)
}

const towerIndex = readJson('tower', 'index.json')
towerIndex.towers = towerIndex.towers.filter((t) => t.pack < TOWER_PACKS)
embedded['tower/index.json'] = towerIndex
for (let i = 0; i < TOWER_PACKS; i++) {
  const name = `pack-${String(i).padStart(3, '0')}.json`
  embedded[`tower/${name}`] = readJson('tower', name)
}

// Šibenice má všechna slova v jednom malém souboru, takže se vejde celá.
embedded['gallows/puzzles.json'] = readJson('gallows', 'puzzles.json')
embedded['detective/puzzles.json'] = readJson('detective', 'puzzles.json')
embedded['tetris/deck.json'] = readJson('tetris', 'deck.json')
embedded['quiz/deck.json'] = readJson('quiz', 'deck.json')

/* ---------- JS ---------- */

const jsName = readdirSync(join(DIST, 'assets')).find((f) => f.endsWith('.js'))
const js = readFileSync(join(DIST, 'assets', jsName), 'utf-8')

/* ---------- Sestavení ---------- */

/**
 * Sekvence, na které reaguje HTML parser uvnitř <script>. Kromě `</script>`
 * přepne parser do jiného stavu i samotné `<script` (React DOM ho má
 * v řetězcovém literálu) a `<!--`. Zápis přes \x3C dá stejný znak, takže
 * význam kódu i dat zůstává nedotčený.
 */
function escapeForInlineScript(source) {
  return source
    .replace(/<\/(?=[a-zA-Z])/g, '\\x3C/')
    .replace(/<script/gi, '\\x3Cscript')
    .replace(/<!--/g, '\\x3C!--')
}

/**
 * Převede všechny neascii znaky na \uXXXX. České texty a slovní data by se
 * jinak rozsypaly všude, kde stránka nedostane deklarované kódování UTF-8 —
 * a poškozený řetězcový literál shodí celý skript. Takhle je výstup čistě
 * ASCII a na kódování nezávislý.
 */
function toAscii(source) {
  return source.replace(/[\u0080-\uFFFF]/g, (ch) =>
    '\\u' + ch.charCodeAt(0).toString(16).padStart(4, '0'),
  )
}

const dataLiteral = toAscii(escapeForInlineScript(JSON.stringify(embedded)))

const title = (html.match(/<title>([^<]*)<\/title>/) ?? [, 'Slova'])[1]

/**
 * Bez `viewport` vykreslí mobilní prohlížeč stránku v 980px a jen ji zmenší —
 * hráč pak na telefonu vidí zmenšené desktopové rozvržení.
 *
 * Značka se přidává staticky i skriptem: hostitel může stránku zabalit do
 * vlastní hlavičky, kde už nějaký `viewport` je (a přebil by ten náš), nebo
 * naopak žádný nemá. Skript sjednotí obě situace.
 */
const VIEWPORT = 'width=device-width, initial-scale=1, viewport-fit=cover'

const viewportBootstrap = `<script>
(function () {
  var want = ${JSON.stringify(VIEWPORT)}
  var head = document.head || document.documentElement
  var meta = document.querySelector('meta[name="viewport"]')
  if (!meta) {
    meta = document.createElement('meta')
    meta.setAttribute('name', 'viewport')
    head.appendChild(meta)
  }
  if (meta.getAttribute('content') !== want) meta.setAttribute('content', want)
})()
</script>`

const page = `<meta charset="utf-8">
<meta name="viewport" content="${VIEWPORT}">
<title>${title}</title>
${viewportBootstrap}
<style>
${css}
</style>
<div id="root"></div>
<script>window.__SLOVA_DATA__ = ${dataLiteral};</script>
<script type="module">
${toAscii(escapeForInlineScript(js))}
</script>
`

if (/[^\x00-\x7F]/.test(page.slice(page.indexOf('<div id="root">')))) {
  throw new Error('Ve skriptové části zůstaly neascii znaky')
}

if (/<\/style/i.test(css)) throw new Error('CSS obsahuje </style — je potřeba escapovat')

writeFileSync(OUT, page)

const kb = (n) => `${Math.round(n / 1024)} kB`
console.log(`\nCSS      ${kb(css.length)} (z toho fonty ${kb(fontBytes * 1.37)} base64)`)
console.log(`JS       ${kb(js.length)}`)
console.log(`Data     ${kb(dataLiteral.length)}`)
console.log(
  `  řetěz ${[4, 5, 6].reduce((n, l) => n + embedded[`chain/puzzles-${l}.json`].length, 0)} hádanek` +
    `, voština ${hiveIndex.hives.length}, věž ${towerIndex.towers.length}` +
    `, šibenice ${embedded['gallows/puzzles.json'].length}` +
    `, detektiv ${embedded['detective/puzzles.json'].length}` +
    `, slabiky ${embedded['tetris/deck.json'].words.length} slov` +
    `, otázka dne ${Object.values(embedded['quiz/deck.json']).flat().length}`,
)
console.log(`\nCelkem   ${kb(page.length)}  ->  ${OUT}`)
