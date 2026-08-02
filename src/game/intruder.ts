/**
 * Režim VETŘELEC — čtyři slova něco spojuje, páté ne.
 *
 * Hráč nehádá slovo, **třídí** je: ukáže na vetřelce a pak řekne proč.
 * Souvislost je vždycky jedna ze tří — jazyk původu, počet slabik, slovní
 * druh —, a aby byl vetřelec právě jeden, shoduje se pětice na obou
 * zbylých znacích. Generátor v `tools/9_build_intruder.py` jinou pětici
 * nepustí ven.
 *
 * Druhý krok je schválně placený zvlášť: trefit slovo se dá i náhodou,
 * pojmenovat souvislost už ne.
 */

import type { Difficulty } from './types'

export type IntruderKind = 'lang' | 'syl' | 'pos'

export const KIND_LABEL: Record<IntruderKind, string> = {
  lang: 'jazyk původu',
  syl: 'počet slabik',
  pos: 'slovní druh',
}

export const KIND_ORDER: IntruderKind[] = ['lang', 'syl', 'pos']

export interface IntruderPuzzle {
  id: string
  words: string[]
  /** Slovo, které do pětice nepatří. */
  odd: string
  kind: IntruderKind
  /** Hodnota, na které se shoduje čtveřice — „latina", 3, „sloveso". */
  shared: string | number
  /** Táž hodnota u vetřelce. */
  oddValue: string | number
  difficulty: Difficulty
}

export const INTRUDER_HINT_COST = 40

export interface IntruderState {
  puzzle: IntruderPuzzle
  /** Slovo, na které hráč ukázal. */
  picked: string | null
  /** Souvislost, kterou pojmenoval. */
  reason: IntruderKind | null
  /** Slova vyloučená nápovědou. */
  ruled: string[]
  hintsUsed: number
  freeHints: number
  hintCost: number
  startedAt: number
  finishedAt: number | null
}

export function createIntruderState(
  puzzle: IntruderPuzzle,
  now = Date.now(),
): IntruderState {
  return {
    puzzle,
    picked: null,
    reason: null,
    ruled: [],
    hintsUsed: 0,
    freeHints: 0,
    hintCost: 0,
    startedAt: now,
    finishedAt: null,
  }
}

export const foundOdd = (state: IntruderState): boolean =>
  state.picked === state.puzzle.odd

export const namedReason = (state: IntruderState): boolean =>
  state.reason === state.puzzle.kind

export function pick(state: IntruderState, word: string): IntruderState {
  if (state.picked || state.finishedAt) return state
  return { ...state, picked: word }
}

export function name(state: IntruderState, kind: IntruderKind): IntruderState {
  if (!state.picked || state.reason || state.finishedAt) return state
  return { ...state, reason: kind, finishedAt: Date.now() }
}

/** Nápověda vyloučí jedno slovo, které vetřelec není. */
export function takeHint(state: IntruderState): IntruderState | null {
  const safe = state.puzzle.words.filter(
    (word) => word !== state.puzzle.odd && !state.ruled.includes(word),
  )
  if (state.picked || safe.length === 0) return null
  return { ...state, ruled: [...state.ruled, safe[0]!] }
}
