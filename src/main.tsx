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
 * Když se ani po dvou pokusech nepodaří starou verzi setřást, hra to řekne
 * nahlas: na úvodní obrazovce se rozsvítí řádek s tlačítkem Aktualizovat.
 * Tiché vzdání bylo horší než chyba — hráč pak roky hraje starou verzi
 * a nemá jak se to dozvědět.
 */
const TRIES = 'slova.refreshTries'
/** Ke které verzi se ty pokusy vztahují. */
const TRIES_FOR = 'slova.refreshTarget'

async function ensureLatestBuild() {
  try {
    // Dotaz s časovým razítkem — jinak by ho odchytil service worker
    // z cache a porovnávalo by se staré se starým.
    const response = await fetch(
      `${import.meta.env.BASE_URL}index.html?v=${Date.now()}`,
      { cache: 'no-store' },
    )
    if (!response.ok) return
    const live = (await response.text()).match(/assets\/index-[A-Za-z0-9_-]+\.js/)
    if (!live) return
    if (import.meta.url.includes(live[0])) {
      // Sedí to. Počitadlo pokusů se smaže, aby se příští aktualizace
      // neposuzovala podle toho, jak dopadla ta minulá.
      sessionStorage.removeItem(TRIES)
      return
    }

    /*
     * Počitadlo pokusů patří k jedné konkrétní verzi.
     *
     * Dřív se počítalo napříč vším: kdo se dvakrát marně pokusil doskočit
     * na jednu verzi, měl aktualizace do konce sezení zamčené — a protože
     * se nainstalovaná aplikace nezavírá, klidně i na dny. Nová verze
     * dostane vlastní pokusy.
     */
    if (sessionStorage.getItem(TRIES_FOR) !== live[0]) {
      sessionStorage.setItem(TRIES_FOR, live[0])
      sessionStorage.removeItem(TRIES)
    }

    const tries = Number(sessionStorage.getItem(TRIES) ?? '0')
    if (tries >= 2) {
      // Dvakrát jsme zkusili všechno a pořád jede stará verze. Dál to samo
      // nepůjde — nejspíš drží mezipaměť někde po cestě, ne v telefonu.
      document.documentElement.dataset.stale = 'true'
      window.dispatchEvent(new Event('slova:stale'))
      return
    }

    sessionStorage.setItem(TRIES, String(tries + 1))
    const registrations = await navigator.serviceWorker.getRegistrations()
    await Promise.all(registrations.map((registration) => registration.unregister()))
    if ('caches' in window) {
      const keys = await caches.keys()
      await Promise.all(keys.map((key) => caches.delete(key)))
    }
    // Ne `reload()`: ten by index.html vytáhl z běžné mezipaměti prohlížeče
    // a přenačetl by se týž starý soubor. Adresa s jednorázovým parametrem
    // žádnou uloženou kopii nemá.
    const fresh = new URL(location.href)
    fresh.searchParams.set('v', String(Date.now()))
    location.replace(fresh.toString())
  } catch {
    // Bez sítě se nedá nic ověřit — hra běží dál z toho, co má.
  }
}

/*
 * Kontrola se opakuje, ne jen při načtení.
 *
 * Nainstalovaná aplikace se na telefonu nezavírá — jen se odloží na pozadí
 * a pak zas vytáhne, a stránka se přitom **nenačítá znovu**. Kontrola při
 * načtení se tedy nemusí spustit celé dny a hráč hraje starou verzi, aniž
 * by udělal cokoli špatně. Přesně tak zůstal hráč tři a půl hodiny na
 * verzi, kterou už dávno nahradily dvě novější.
 *
 * Proto se kontroluje i pokaždé, když se hra vrátí na obrazovku. Aby to
 * nechodilo na server při každém přepnutí, drží se mezi kontrolami odstup.
 */
const ODSTUP_MS = 30 * 1000
let posledniKontrola = 0
let kontrolaBezi = false

async function zkontrolujVerzi() {
  if (kontrolaBezi) return
  const ted = Date.now()
  if (ted - posledniKontrola < ODSTUP_MS) return
  posledniKontrola = ted
  kontrolaBezi = true
  try {
    await ensureLatestBuild()
  } finally {
    kontrolaBezi = false
  }
}

if (import.meta.env.PROD && 'serviceWorker' in navigator && !window.__SLOVA_DATA__) {
  void zkontrolujVerzi()

  document.addEventListener('visibilitychange', () => {
    if (document.visibilityState === 'visible') void zkontrolujVerzi()
  })

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
