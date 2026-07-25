/**
 * Service worker — hra musí fungovat i bez signálu.
 *
 * Skořápka aplikace (HTML, JS, CSS, fonty, ikony) se předukládá při instalaci.
 * Datové balíčky hádanek se ukládají až při prvním použití, protože jich jsou
 * megabajty a hráč jich stejně potřebuje jen část.
 */

const VERSION = 'slova-v1'
const SHELL = `${VERSION}-shell`
const DATA = `${VERSION}-data`

// Doplní se při buildu; tady jsou jen jistoty, které existují vždy.
const SHELL_URLS = self.__SLOVA_SHELL__ ?? ['./', './index.html']

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
    event.respondWith(
      fetch(request)
        .then((response) => {
          const copy = response.clone()
          caches.open(SHELL).then((cache) => cache.put('./index.html', copy))
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
