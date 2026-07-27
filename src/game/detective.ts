/**
 * Režim ETYMOLOGICKÝ DETEKTIV — hádání slova podle jeho původu.
 *
 * Hráč vidí jen počet písmen a text o tom, odkud slovo přišlo:
 *
 *     „Odvozeno (snad přes hornoněmčinu) z latinského castellum (bašta,
 *      pevnůstka, menší tvrz), zdrobněliny slova castrum."   →   KOSTEL
 *
 * Mechanika je příbuzná Šibenici: zkoušejí se písmena, diakritika se hádá po
 * základním písmeni. Jsou ale dva zásadní rozdíly, a oba jdou za tím, aby to
 * byla **detektivka, ne šibenice s textem navíc**:
 *
 * 1. **Nehraje se na životy, ale na body.** Chybné písmeno nezabíjí, jen
 *    stojí. Hráč tak může přemýšlet nahlas a zkoušet, místo aby po osmi
 *    chybách skončil — text mu má dávat vodítko, kterým se dá pracovat.
 * 2. **Slovo se dá tipnout celé.** Kdo na to přijde z etymologie po třech
 *    písmenech, nemusí doklikávat zbytek; tipnutí je za prémii a chybný tip
 *    stojí stejně jako pár písmen.
 *
 * Texty pocházejí z české sekce Wikislovníku (CC BY-SA) a generátor v
 * `tools/5d_build_detective.py` vyhazuje ty, které slovo prozradí — nejčastěji
 * rozbory složenin typu „ze spojení jest-li".
 */

import { fold } from '../lib/czech'
import type { Difficulty } from './types'

export interface DetectivePuzzle {
  id: string
  word: string
  /** Text o původu slova, tak jak ho podává Wikislovník. */
  clue: string
  difficulty: Difficulty
}

/** Klávesnice detektiva: základní písmena, diakritika se skládá sama. */
export const DETECTIVE_KEYS = 'abcdefghijklmnopqrstuvwxyz'.split('')

export const DETECTIVE_COST = {
  /** Písmeno, které ve slově není. */
  miss: 60,
  /** Chybný tip na celé slovo. */
  wrongGuess: 120,
  /** Nápověda: odhalí jedno písmeno. */
  letter: 150,
} as const

/** Nad tolik chybných písmen se kolo ukončí, ať se nedá vyklikat abecedou. */
export const DETECTIVE_MISS_LIMIT = 12

export interface DetectiveState {
  puzzle: DetectivePuzzle
  /** Zkoušená základní písmena v pořadí, jak padla. */
  tried: string[]
  /** Neúspěšné tipy na celé slovo — ukazují se, aby je hráč neopakoval. */
  guesses: string[]
  solved: boolean
  hintsUsed: number
  /** Kolik nápověd bylo z peněženky profilu. */
  freeHints: number
  hintCost: number
  startedAt: number
  finishedAt: number | null
}

export function createDetectiveState(
  puzzle: DetectivePuzzle,
  now = Date.now(),
): DetectiveState {
  return {
    puzzle,
    tried: [],
    guesses: [],
    solved: false,
    hintsUsed: 0,
    freeHints: 0,
    hintCost: 0,
    startedAt: now,
    finishedAt: null,
  }
}

/** Základní podoba slova — proti ní se porovnávají zkoušená písmena. */
export function plain(state: DetectiveState): string {
  return fold(state.puzzle.word)
}

export function neededLetters(puzzle: DetectivePuzzle): Set<string> {
  return new Set(fold(puzzle.word))
}

/** Písmena slova v pořadí; neodhalená jsou `null`. */
export function revealed(state: DetectiveState): (string | null)[] {
  const base = plain(state)
  if (state.solved) return [...state.puzzle.word]
  return [...state.puzzle.word].map((ch, i) =>
    state.tried.includes(base[i]!) ? ch : null,
  )
}

export function missCount(state: DetectiveState): number {
  const base = plain(state)
  return state.tried.filter((letter) => !base.includes(letter)).length
}

/** Odhalil hráč slovo po písmenech? */
export function isComplete(state: DetectiveState): boolean {
  for (const letter of neededLetters(state.puzzle)) {
    if (!state.tried.includes(letter)) return false
  }
  return true
}

export function isOver(state: DetectiveState): boolean {
  return state.solved || isComplete(state) || missCount(state) >= DETECTIVE_MISS_LIMIT
}

/** Uhodl hráč slovo? Vyčerpané pokusy se za úspěch nepočítají. */
export function isWon(state: DetectiveState): boolean {
  return state.solved || isComplete(state)
}

export type LetterResult =
  | { ok: false; error: 'used' | 'over' | 'unknown-letter' }
  | { ok: true; state: DetectiveState; hit: boolean; letter: string }

export const DETECTIVE_ERROR_TEXT: Record<'used' | 'over' | 'unknown-letter', string> = {
  used: 'Tohle písmeno už jsi zkusil',
  over: 'Kolo je u konce',
  'unknown-letter': 'To písmeno na klávesnici není',
}

export function guessLetter(state: DetectiveState, raw: string): LetterResult {
  if (isOver(state)) return { ok: false, error: 'over' }
  const letter = fold(raw.toLowerCase())
  if (!DETECTIVE_KEYS.includes(letter)) return { ok: false, error: 'unknown-letter' }
  if (state.tried.includes(letter)) return { ok: false, error: 'used' }

  const next: DetectiveState = { ...state, tried: [...state.tried, letter] }
  if (isOver(next)) next.finishedAt = Date.now()
  return { ok: true, state: next, hit: plain(state).includes(letter), letter }
}

export type WordResult =
  | { ok: false; error: 'empty' | 'over' | 'repeat' }
  | { ok: true; state: DetectiveState; correct: boolean }

/**
 * Tip na celé slovo.
 *
 * Porovnává se bez diakritiky, stejně jako u písmen — hráč, který na slovo
 * přišel, nemá padnout na tom, jestli je tam „ů" nebo „ú".
 */
export function guessWord(state: DetectiveState, raw: string): WordResult {
  if (isOver(state)) return { ok: false, error: 'over' }
  const guess = fold(raw.trim().toLowerCase())
  if (!guess) return { ok: false, error: 'empty' }
  if (state.guesses.some((old) => fold(old) === guess)) return { ok: false, error: 'repeat' }

  if (guess === plain(state)) {
    return {
      ok: true,
      correct: true,
      state: { ...state, solved: true, finishedAt: Date.now() },
    }
  }
  const next: DetectiveState = { ...state, guesses: [...state.guesses, raw.trim()] }
  return { ok: true, correct: false, state: next }
}

export interface DetectiveHintResult {
  state: DetectiveState
  letter: string
}

export function takeDetectiveHint(
  state: DetectiveState,
  /** Zaplacená z peněženky profilu — do bodů se pak nepromítne. */
  free = false,
): DetectiveHintResult | null {
  if (isOver(state)) return null
  const base = plain(state)
  const missing = [...neededLetters(state.puzzle)].filter(
    (letter) => !state.tried.includes(letter),
  )
  if (missing.length === 0) return null
  // Nejčastější z chybějících písmen — nápověda má posunout, ne dát písmeno
  // stojící na jediném místě.
  missing.sort(
    (a, b) => base.split(b).length - base.split(a).length || a.localeCompare(b, 'cs'),
  )
  const letter = missing[0]!
  const next: DetectiveState = {
    ...state,
    tried: [...state.tried, letter],
    hintsUsed: state.hintsUsed + 1,
    freeHints: (state.freeHints ?? 0) + (free ? 1 : 0),
    hintCost: state.hintCost + (free ? 0 : DETECTIVE_COST.letter),
  }
  if (isOver(next)) next.finishedAt = Date.now()
  return { state: next, letter }
}
