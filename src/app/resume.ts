/**
 * Návrat do rozehraného kola.
 *
 * Kolo se ukládá po každém tahu (viz `keepProgress` v App), takže odchod do
 * menu ani zavření prohlížeče o postup nepřipraví. Zpátky se z uloženého
 * stavu musí vytáhnout hádanka — hra ji potřebuje dřív, než se stav nasadí.
 *
 * Tenhle překlad stál dřív v App jako řada `else if` a končil větví `else`,
 * která **všechno ostatní považovala za Věž**. Citát a Vetřelec přibyly
 * později, spadly do ní a hráč se místo rozehraného kola vracel na začátek.
 * Proto je to tady zvlášť, jako čistá funkce se seznamem, který test projde
 * režim po režimu.
 */

import type { ChainState } from '../game/chain'
import type { DetectiveState } from '../game/detective'
import type { GallowsState } from '../game/gallows'
import type { HiveState } from '../game/hive'
import type { IntruderState } from '../game/intruder'
import type { QuoteState } from '../game/quotes'
import type { TetrisState } from '../game/tetris'
import type { TowerState } from '../game/tower'
import type { ModeId } from '../game/types'
import type { SavedRound } from '../lib/storage'

/**
 * Hádanka vytažená z uloženého stavu.
 *
 * Řetěz potřebuje ještě graf, který se dohledá podle obtížnosti — ten se
 * načítá zvlášť, tady je jen hádanka. Ostatní režimy si vystačí s tím, co
 * v uloženém stavu leží.
 */
export type Restored =
  | { mode: 'chain'; puzzle: ChainState['puzzle'] }
  | { mode: 'hive'; puzzle: HiveState['puzzle'] }
  | { mode: 'tower'; puzzle: TowerState['puzzle'] }
  | { mode: 'gallows'; puzzle: GallowsState['puzzle'] }
  | { mode: 'detective'; puzzle: DetectiveState['puzzle'] }
  | { mode: 'intruder'; puzzle: IntruderState['puzzle'] }
  | { mode: 'quotes'; quote: QuoteState['quote'] }
  | { mode: 'tetris'; deck: TetrisState['deck']; setup: TetrisState['setup'] }

/**
 * Vytáhne z uloženého kola hádanku. Vrátí `null`, když stav nesedí na
 * režim — uložené kolo z jiné verze hry se pak zahodí a hráč začne znovu,
 * což je pořád lepší než prázdná obrazovka.
 */
export function restore(round: SavedRound): Restored | null {
  const state = round.state as Record<string, unknown> | null
  if (!state || typeof state !== 'object') return null

  switch (round.mode) {
    case 'chain':
    case 'hive':
    case 'tower':
    case 'gallows':
    case 'detective':
    case 'intruder': {
      const puzzle = state.puzzle
      if (!puzzle || typeof puzzle !== 'object') return null
      // Typ hádanky hlídá režim: `state.puzzle` je vždycky ta, se kterou se
      // kolo rozehrálo, a jinou v uloženém stavu být nemůže.
      return { mode: round.mode, puzzle } as Restored
    }
    case 'quotes': {
      const quote = state.quote
      if (!quote || typeof quote !== 'object') return null
      return { mode: 'quotes', quote } as Restored
    }
    case 'tetris': {
      const { deck, setup } = state
      if (!deck || !setup || typeof setup !== 'object') return null
      return { mode: 'tetris', deck, setup } as Restored
    }
    default:
      return null
  }
}

/**
 * Počítá se obnovené kolo pořád jako dnešní denní výzva?
 *
 * Denní kolo rozehrané včera a dohrané dnes by se zapsalo jako **dnešní**
 * výzva, jenže hádanka je včerejší — hráč by měl v přehledu skóre za něco,
 * co dnes nikdo jiný nehrál, a v souboji o denní výzvu by soupeře nenašel.
 * Po půlnoci se proto kolo dohrává jako volná hra: postup zůstává, jen
 * přestane platit za denní.
 */
export function stillDaily(round: SavedRound, today: string, dayOf: (at: number) => string): boolean {
  return round.daily && dayOf(round.savedAt) === today
}

/** Režimy, pro které `restore` umí vrátit hádanku. Test podle toho hlídá úplnost. */
export const RESTORABLE: ModeId[] = [
  'chain',
  'hive',
  'tower',
  'gallows',
  'detective',
  'intruder',
  'quotes',
  'tetris',
]
