/**
 * Režim ŠIBENICE — hádání slova po písmenech.
 *
 * Pravidla jsou klasická: slovo je schované, hráč zkouší písmena a za každé,
 * které ve slově není, přibude jeden díl šibenice. Osm dílů a je konec.
 *
 * Dvě věci jsou udělané jinak, než jak se šibenice hraje na papíře:
 *
 * 1. **Diakritika se hádá po základním písmeni.** „u" odhalí „u", „ú" i „ů".
 *    Jinak by hra byla hádání háčků místo hádání slova a na telefonu by se
 *    musela vytáhnout klávesnice se čtyřiceti dvěma klávesami. Voština to
 *    dělá stejně, takže je to i uvnitř hry jedno pravidlo, ne výjimka.
 * 2. **Nápověda „vyškrtni" nestojí život.** Odstraní z klávesnice pět písmen,
 *    která ve slově nejsou; hráč je tím pádem nezkusí a nezaplatí za ně dílem
 *    šibenice. Platí se za ni body, ne krkem.
 *
 * Řešitelnost je tu triviální a přesto ji stojí za to říct nahlas: hádané
 * slovo je jedno jediné a bere se z ověřeného seznamu základních tvarů, takže
 * každá hádanka má právě jedno správné řešení a to řešení je platné slovo.
 */

import { fold } from '../lib/czech'
import type { Difficulty } from './types'

export interface GallowsPuzzle {
  id: string
  word: string
  difficulty: Difficulty
}

/** Kolik chybných písmen hráč vydrží — tolik má šibenice dílů. */
export const GALLOWS_LIVES = 8

/** Klávesnice Šibenice: jen základní písmena, diakritika se řeší skládáním. */
export const GALLOWS_KEYS = 'abcdefghijklmnopqrstuvwxyz'.split('')

export const GALLOWS_HINT_COST = {
  /** Odhalí jedno dosud neuhodnuté písmeno. */
  letter: 50,
  /** Vyškrtne z klávesnice pět písmen, která ve slově nejsou. */
  strike: 35,
} as const

export type GallowsHintKind = keyof typeof GALLOWS_HINT_COST

/** Kolik písmen vyškrtne jedna nápověda. */
export const STRIKE_COUNT = 5

export interface GallowsState {
  puzzle: GallowsPuzzle
  /** Zkoušená základní písmena, v pořadí, jak padla. */
  tried: string[]
  /** Písmena zhasnutá nápovědou — na klávesnici nejdou, ale život nestála. */
  struck: string[]
  hintsUsed: number
  /** Kolik nápověd bylo zaplaceno inkoustem — ty se do bodů nepočítají. */
  freeHints: number
  hintCost: number
  startedAt: number
  finishedAt: number | null
}

export function createGallowsState(puzzle: GallowsPuzzle, now = Date.now()): GallowsState {
  return {
    puzzle,
    tried: [],
    struck: [],
    hintsUsed: 0,
    freeHints: 0,
    hintCost: 0,
    startedAt: now,
    finishedAt: null,
  }
}

/** Základní podoba slova — proti ní se porovnávají zkoušená písmena. */
export function plain(state: GallowsState): string {
  return fold(state.puzzle.word)
}

/** Různá základní písmena, která je potřeba uhodnout. */
export function neededLetters(puzzle: GallowsPuzzle): Set<string> {
  return new Set(fold(puzzle.word))
}

/** Písmena slova v pořadí; neuhodnutá jsou `null`. */
export function revealed(state: GallowsState): (string | null)[] {
  const base = plain(state)
  return [...state.puzzle.word].map((ch, i) =>
    state.tried.includes(base[i]!) ? ch : null,
  )
}

/** Kolik dílů šibenice už stojí. */
export function wrongCount(state: GallowsState): number {
  const base = plain(state)
  return state.tried.filter((letter) => !base.includes(letter)).length
}

export function isWon(state: GallowsState): boolean {
  for (const letter of neededLetters(state.puzzle)) {
    if (!state.tried.includes(letter)) return false
  }
  return true
}

export function isLost(state: GallowsState): boolean {
  return wrongCount(state) >= GALLOWS_LIVES
}

export function isOver(state: GallowsState): boolean {
  return isWon(state) || isLost(state)
}

export type GuessResult =
  | { ok: false; error: 'used' | 'over' | 'unknown-letter' }
  | { ok: true; state: GallowsState; hit: boolean; letter: string; won: boolean; lost: boolean }

export const GALLOWS_ERROR_TEXT: Record<'used' | 'over' | 'unknown-letter', string> = {
  used: 'Tohle písmeno už jsi zkusil',
  over: 'Kolo je u konce',
  'unknown-letter': 'To písmeno na klávesnici není',
}

export function guessLetter(state: GallowsState, raw: string): GuessResult {
  if (isOver(state)) return { ok: false, error: 'over' }
  const letter = fold(raw.toLowerCase())
  if (!GALLOWS_KEYS.includes(letter)) return { ok: false, error: 'unknown-letter' }
  if (state.tried.includes(letter) || state.struck.includes(letter)) {
    return { ok: false, error: 'used' }
  }

  const next: GallowsState = { ...state, tried: [...state.tried, letter] }
  const won = isWon(next)
  const lost = isLost(next)
  if (won || lost) next.finishedAt = Date.now()

  return {
    ok: true,
    state: next,
    hit: plain(state).includes(letter),
    letter,
    won,
    lost,
  }
}

export interface GallowsHintResult {
  kind: GallowsHintKind
  state: GallowsState
  /** U „letter" odhalené písmeno, u „strike" vyškrtnutá písmena. */
  letters: string[]
}

export function takeGallowsHint(
  state: GallowsState,
  kind: GallowsHintKind,
  /** Zaplacená inkoustem — do bodů se pak nepromítne. */
  free = false,
): GallowsHintResult | null {
  if (isOver(state)) return null
  const cost = free ? 0 : GALLOWS_HINT_COST[kind]

  if (kind === 'letter') {
    const missing = [...neededLetters(state.puzzle)].filter(
      (letter) => !state.tried.includes(letter),
    )
    // Odhalí se nejčastější z chybějících písmen — nápověda má pomoct,
    // ne dát hráči písmeno, které stejně stojí jen na jednom místě.
    const base = plain(state)
    missing.sort(
      (a, b) => base.split(b).length - base.split(a).length || a.localeCompare(b, 'cs'),
    )
    const letter = missing[0]
    if (!letter) return null
    const next: GallowsState = {
      ...state,
      tried: [...state.tried, letter],
      hintsUsed: state.hintsUsed + 1,
      freeHints: (state.freeHints ?? 0) + (free ? 1 : 0),
      hintCost: state.hintCost + cost,
    }
    if (isWon(next)) next.finishedAt = Date.now()
    return { kind, state: next, letters: [letter] }
  }

  const needed = neededLetters(state.puzzle)
  const dead = GALLOWS_KEYS.filter(
    (letter) =>
      !needed.has(letter) && !state.tried.includes(letter) && !state.struck.includes(letter),
  )
  if (dead.length === 0) return null
  const letters = dead.slice(0, STRIKE_COUNT)
  return {
    kind,
    letters,
    state: {
      ...state,
      struck: [...state.struck, ...letters],
      hintsUsed: state.hintsUsed + 1,
      freeHints: (state.freeHints ?? 0) + (free ? 1 : 0),
      hintCost: state.hintCost + cost,
    },
  }
}
