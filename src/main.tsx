import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'

import '@fontsource-variable/manrope'
import '@fontsource-variable/bricolage-grotesque'
import './styles/tokens.css'
import './styles/base.css'
import './styles/app.css'

import App from './App'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <App />
  </StrictMode>,
)

/**
 * Service worker se registruje jen u běžného buildu. Jednosouborová verze
 * má data uvnitř stránky a žádný sw.js vedle sebe nemá, takže by registrace
 * skončila chybou 404.
 */
/**
 * Kontrola, že běží aktuální verze.
 *
 * Skript i styly mají v názvu otisk obsahu, takže se dá zjistit, jestli
 * stránka běží z toho, co je na serveru: stáhne se `index.html` mimo
 * jakoukoli cache a porovná se jméno souboru se skriptem, ze kterého jede
 * tenhle kód. Když nesedí, telefon drží starou verzi — service worker se
 * odregistruje, cache se smaže a stránka se jednou načte znovu.
 *
 * Bez tohohle by zaseknutá cache mohla starou hru držet i po vymazání dat
 * a jediná cesta ven by byla odinstalovat aplikaci.
 */
async function ensureLatestBuild() {
  if (sessionStorage.getItem('slova.refreshed') === '1') return
  try {
    // Dotaz s časovým razítkem — jinak by ho odchytil service worker
    // z cache a porovnávalo by se staré se starým.
    const response = await fetch(
      `${import.meta.env.BASE_URL}index.html?v=${Date.now()}`,
      { cache: 'no-store' },
    )
    if (!response.ok) return
    const live = (await response.text()).match(/assets\/index-[A-Za-z0-9_-]+\.js/)
    if (!live || import.meta.url.includes(live[0])) return

    sessionStorage.setItem('slova.refreshed', '1')
    const registrations = await navigator.serviceWorker.getRegistrations()
    await Promise.all(registrations.map((registration) => registration.unregister()))
    if ('caches' in window) {
      const keys = await caches.keys()
      await Promise.all(keys.map((key) => caches.delete(key)))
    }
    window.location.reload()
  } catch {
    // Bez sítě se nedá nic ověřit — hra běží dál z toho, co má.
  }
}

if (import.meta.env.PROD && 'serviceWorker' in navigator && !window.__SLOVA_DATA__) {
  void ensureLatestBuild()

  // Nová verze hry přináší i nový slovník. Když se service worker vymění,
  // stránka se hned načte znovu, aby hráč nedohrával kolo ze starých dat.
  // Rozehrané kolo tím nepřijde — drží se v localStorage.
  let hadController = Boolean(navigator.serviceWorker.controller)
  navigator.serviceWorker.addEventListener('controllerchange', () => {
    if (!hadController) {
      hadController = true
      return // první instalace, tady se přenačítat nemá co
    }
    window.location.reload()
  })

  window.addEventListener('load', () => {
    navigator.serviceWorker
      .register(`${import.meta.env.BASE_URL}sw.js`, {
        scope: import.meta.env.BASE_URL,
      })
      .then((registration) => registration.update())
      .catch(() => {
        // Hra funguje i bez offline režimu — není důvod obtěžovat hráče.
      })
  })
}
