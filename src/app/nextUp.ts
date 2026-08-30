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

/**
 * Která hra právě skončila. Závěrečná karta se jím podepíše — značkou hry
 * a drobným řádkem s režimem —, aby se sdílený snímek dal zařadit.
 * Nese se stejnou cestou jako nabídka a ze stejného důvodu.
 */
export const RoundModeContext = createContext<{ glyph: string; label: string } | null>(null)

/**
 * Srovnání právě dohraného denního kola se sledovanými hráči.
 *
 * Je jich tolik, kolik si jich hráč vybral — proto seznam, ne jedno jméno.
 * Prázdný znamená „nikdo ze sledovaných tuhle hádanku (zatím) nehrál".
 */
export const DuelContext = createContext<
  { uid: string; nick: string; score: number; won: boolean | null }[]
>([])

/**
 * Nahlášení soupeře.
 *
 * Přezdívku píše hráč sám a vidí ji ostatní, takže musí jít odkudkoli, kde
 * se cizí jméno objeví, poslat hlášení a soupeře zablokovat. Panel drží App;
 * sem se nese jen to, koho se to týká — stejnou cestou jako zbytek, protože
 * karta výsledku sedí uvnitř osmi her a protahovat tudy další prop by
 * znamenalo osm stejných úprav v osmi souborech.
 */
export const ReportContext = createContext<((uid: string, nick: string) => void) | null>(
  null,
)

export const useNextUp = (): NextUpItem[] => useContext(NextUpContext)
