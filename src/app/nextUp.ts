/**
 * Co hráče čeká po dohraném kole.
 *
 * Denní výzvy jsou šest kol a Otázka dne sedmá; kdo je chce dohrát všechny,
 * musel se po každém kole vracet do menu a hledat, co ještě zbývá. Závěrečná
 * karta to teď ví sama — a nabídne zbytek rovnou.
 *
 * Nabídka se nese přes kontext, ne přes propy. Karta výsledku sedí uvnitř
 * všech šesti her a protahovat jí tudy další prop by znamenalo šest stejných
 * úprav v šesti souborech; nabídka přitom s pravidly té které hry nemá nic
 * společného.
 */

import { createContext, useContext } from 'react'

export interface NextUpItem {
  /** Klíč do seznamu — id režimu, nebo „quiz" pro Otázku dne. */
  id: string
  /** Znak režimu; u Otázky dne otazník. */
  glyph: string
  label: string
  start: () => void
}

export const NextUpContext = createContext<NextUpItem[]>([])

export const useNextUp = (): NextUpItem[] => useContext(NextUpContext)
