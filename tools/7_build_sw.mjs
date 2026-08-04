/**
 * Po buildu doplní do service workeru seznam souborů skořápky.
 *
 * Názvy sestavených souborů obsahují hash, takže je nejde napsat ručně —
 * čtou se z hotového buildu. Verze cache se odvozuje z obsahu, aby si
 * prohlížeč po nasazení nové verze nedržel tu starou.
 */

import { createHash } from 'node:crypto'
import { readFileSync, readdirSync, statSync, writeFileSync } from 'node:fs'
import { join, dirname, relative } from 'node:path'
import { fileURLToPath } from 'node:url'

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..')
const DIST = join(ROOT, 'dist')

function walk(dir) {
  const out = []
  for (const entry of readdirSync(dir)) {
    const full = join(dir, entry)
    if (statSync(full).isDirectory()) out.push(...walk(full))
    else out.push(full)
  }
  return out
}

const files = walk(DIST).map((f) => './' + relative(DIST, f).split('\\').join('/'))

// Skořápka = všechno kromě herních dat, samotného workeru a knihovny pro
// souboje. Data se ukládají až za běhu, jsou jich megabajty a hráč potřebuje
// jen část; Firebase se stahuje, teprve když hráč do soubojů vleze — kdo je
// nehraje, ať kvůli nim nečeká na první spuštění.
const shell = files.filter(
  (f) =>
    !f.startsWith('./data/') &&
    !f.endsWith('/sw.js') &&
    f !== './sw.js' &&
    !f.includes('/index.esm-') &&
    !f.endsWith('.map'),
)

const swPath = join(DIST, 'sw.js')
const source = readFileSync(swPath, 'utf-8')

const hash = createHash('sha256')
for (const file of shell.sort()) {
  hash.update(file)
  hash.update(readFileSync(join(DIST, file.slice(2))))
}
const version = `slova-${hash.digest('hex').slice(0, 8)}`

const injected = source
  .replace(
    "const VERSION = 'slova-v1'",
    `const VERSION = '${version}'`,
  )
  .replace(
    'const SHELL_URLS = self.__SLOVA_SHELL__ ?? []',
    `const SHELL_URLS = ${JSON.stringify(shell)}`,
  )
  .replace(
    "const SHELL_URLS = self.__SLOVA_SHELL__ ?? ['./', './index.html']",
    `const SHELL_URLS = ${JSON.stringify(['./', ...shell])}`,
  )

if (injected === source) {
  throw new Error('Do service workeru se nepodařilo doplnit seznam skořápky')
}

writeFileSync(swPath, injected)
console.log(
  `service worker: ${shell.length} souborů skořápky, verze ${version}`,
)
