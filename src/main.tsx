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
if (import.meta.env.PROD && 'serviceWorker' in navigator && !window.__SLOVA_DATA__) {
  window.addEventListener('load', () => {
    navigator.serviceWorker
      .register(`${import.meta.env.BASE_URL}sw.js`, {
        scope: import.meta.env.BASE_URL,
      })
      .catch(() => {
        // Hra funguje i bez offline režimu — není důvod obtěžovat hráče.
      })
  })
}
