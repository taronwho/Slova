/**
 * Service worker — hra musí fungovat i bez signálu.
 *
 * Skořápka aplikace (HTML, JS, CSS, fonty, ikony) se předukládá při instalaci.
 * Datové balíčky hádanek se ukládají až při prvním použití, protože jich jsou
 * megabajty a hráč jich stejně potřebuje jen část.
 */

const VERSION = 'slova-06346802'
const SHELL = `${VERSION}-shell`
const DATA = `${VERSION}-data`

// Doplní se při buildu; tady jsou jen jistoty, které existují vždy.
const SHELL_URLS = ["./","./.nojekyll","./assets/bricolage-grotesque-latin-ext-wght-normal-CcLUaPy7.woff2","./assets/bricolage-grotesque-latin-wght-normal-DLoelf7F.woff2","./assets/bricolage-grotesque-vietnamese-wght-normal-BUzh504Q.woff2","./assets/index-BBQFJeOS.js","./assets/index-BO_08ukz.css","./assets/manrope-cyrillic-wght-normal-Dvxsihut.woff2","./assets/manrope-greek-wght-normal-DL7QRZyv.woff2","./assets/manrope-latin-ext-wght-normal-Ch3YOpNY.woff2","./assets/manrope-latin-wght-normal-DHIcAJRg.woff2","./assets/manrope-vietnamese-wght-normal-usUDDRr7.woff2","./icons/apple-touch-icon.png","./icons/icon-192.png","./icons/icon-512.png","./icons/icon-maskable-192.png","./icons/icon-maskable-512.png","./index.html","./manifest.webmanifest","./slova-standalone.html"]

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches
      .open(SHELL)
      .then((cache) => cache.addAll(SHELL_URLS))
      // Jeden nedostupný soubor nesmí shodit celou instalaci.
      .catch(() => undefined)
      .then(() => self.skipWaiting()),
  )
})

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches
      .keys()
      .then((keys) =>
        Promise.all(
          keys
            .filter((key) => !key.startsWith(VERSION))
            .map((key) => caches.delete(key)),
        ),
      )
      .then(() => self.clients.claim()),
  )
})

self.addEventListener('fetch', (event) => {
  const request = event.request
  if (request.method !== 'GET') return

  const url = new URL(request.url)
  if (url.origin !== self.location.origin) return

  // Navigace: nejdřív síť (kvůli aktualizacím), při výpadku uložená skořápka.
  if (request.mode === 'navigate') {
    // Jako skořápku se ukládá **jen samotná hra**. Na stejné adrese můžou
    // ležet i jiné stránky (třeba kontrolní build otázek) a kdyby se uložily
    // pod index.html, dostal by hráč offline místo hry něco úplně jiného.
    const isApp =
      url.pathname.endsWith('/') || url.pathname.endsWith('/index.html')
    event.respondWith(
      fetch(request)
        .then((response) => {
          if (isApp) {
            const copy = response.clone()
            caches.open(SHELL).then((cache) => cache.put('./index.html', copy))
          }
          return response
        })
        .catch(() =>
          caches
            .match('./index.html')
            .then((cached) => cached ?? caches.match('./')),
        ),
    )
    return
  }

  // Manifest a index.html se z cache neberou nikdy. Skript a styly mají
  // v názvu otisk obsahu, takže nová verze = nová adresa a cache je pustí
  // sama; manifest a index.html ale svoji adresu nemění, a kdyby se braly
  // z cache, držel by telefon starou hru i starou ikonu donekonečna.
  const alwaysFresh =
    url.pathname.endsWith('.webmanifest') || url.pathname.endsWith('index.html')
  if (alwaysFresh) {
    event.respondWith(
      fetch(request)
        .then((response) => {
          if (response.ok && response.type === 'basic') {
            const copy = response.clone()
            caches.open(SHELL).then((cache) => cache.put(request, copy))
          }
          return response
        })
        .catch(() => caches.match(request)),
    )
    return
  }

  // Datové balíčky: z cache, jinak stáhnout a uložit.
  const isData = url.pathname.includes('/data/')
  const cacheName = isData ? DATA : SHELL

  event.respondWith(
    caches.match(request).then((cached) => {
      if (cached) return cached
      return fetch(request).then((response) => {
        if (response.ok && response.type === 'basic') {
          const copy = response.clone()
          caches.open(cacheName).then((cache) => cache.put(request, copy))
        }
        return response
      })
    }),
  )
})
