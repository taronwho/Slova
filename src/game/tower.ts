/**
 * Režim VĚŽ — anagramová věž.
 *
 * V každém patře dostane hráč jedno nové písmeno a musí ze **všech** písmen
 * složit nové slovo. Právě z toho plyne garance dohratelnosti: když se musí
 * použít všechna písmena, má každé platné řešení stejný podpis, takže volba
 * konkrétního slova nemůže zavřít cestu do dalšího patra. Řetěz podpisů je
 * ověřený už při generování.
 */

import { signature } from '../lib/czech'
import type { Difficulty } from './types'

export interface TowerLevel {
  /** Setříděná písmena patra. */
  sig: string
  /** Písmeno přidané oproti patru pod ním; u základny null. */
  added: string | null
  /** Všechna uznávaná slova s tímto podpisem, od nejběžnějšího. */
  words: string[]
}

export interface TowerPuzzle {
  id: string
  difficulty: Difficulty
  levels: TowerLevel[]
}

export interface TowerState {
  puzzle: TowerPuzzle
  /** Slova postavená v jednotlivých patrech; [0] je základ, dodaný hrou. */
  built: string[]
  /** Pořadí dlaždic aktuálního patra — mění tlačítko Zamíchat. */
  tiles: string[]
  hintsUsed: number
  /** Kolik z nich bylo zdarma — ty se do bodů nepočítají. */
  freeHints: number
  /** Body skutečně utracené za nápovědy — každý druh stojí jinak. */
  hintCost: number
  /** Patra, u kterých hráč použil nápovědu na celé slovo. */
  revealedLevels: number[]
  startedAt: number
  finishedAt: number | null
}

export type TowerError = 'wrong-letters' | 'unknown-word' | 'empty'

export const TOWER_ERROR_TEXT: Record<TowerError, string> = {
  'wrong-letters': 'Musíš použít všechna písmena, každé právě jednou',
  'unknown-word': 'To slovo neznám',
  empty: 'Napiš slovo',
}

export const BASE_LEVEL = 3

/** Index patra, které se právě řeší; rovná se počtu hotových pater. */
export function currentLevelIndex(state: TowerState): number {
  return state.built.length
}

export function isFinished(state: TowerState): boolean {
  return state.built.length >= state.puzzle.levels.length
}

export function currentLevel(state: TowerState): TowerLevel | null {
  return state.puzzle.levels[currentLevelIndex(state)] ?? null
}

export function createTowerState(puzzle: TowerPuzzle, now = Date.now()): TowerState {
  const base = puzzle.levels[0]!.words[0]!
  const next = puzzle.levels[1]
  return {
    puzzle,
    built: [base],
    tiles: next ? shuffleLetters(next.sig) : [],
    hintsUsed: 0,
    hintCost: 0,
    freeHints: 0,
    revealedLevels: [],
    startedAt: now,
    finishedAt: null,
  }
}

function shuffleLetters(sig: string): string[] {
  const letters = [...sig]
  for (let i = letters.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1))
    ;[letters[i], letters[j]] = [letters[j]!, letters[i]!]
  }
  return letters
}

export function shuffleTiles(state: TowerState): TowerState {
  const level = currentLevel(state)
  if (!level) return state
  return { ...state, tiles: shuffleLetters(level.sig) }
}

export type TowerOutcome =
  | { ok: false; error: TowerError }
  | { ok: true; state: TowerState; word: string; finished: boolean }

export function submitLevel(
  state: TowerState,
  raw: string,
  now = Date.now(),
): TowerOutcome {
  const word = raw.trim().toLowerCase()
  const level = currentLevel(state)
  if (!level) return { ok: false, error: 'empty' }
  if (!word) return { ok: false, error: 'empty' }
  if (signature(word) !== level.sig) return { ok: false, error: 'wrong-letters' }
  if (!level.words.includes(word)) return { ok: false, error: 'unknown-word' }

  const built = [...state.built, word]
  const finished = built.length >= state.puzzle.levels.length
  const nextLevel = state.puzzle.levels[built.length]

  return {
    ok: true,
    word,
    finished,
    state: {
      ...state,
      built,
      tiles: nextLevel ? shuffleLetters(nextLevel.sig) : [],
      finishedAt: finished ? now : null,
    },
  }
}

export type TowerHintKind = 'letter' | 'word'

export const TOWER_HINT_COST: Record<TowerHintKind, number> = {
  letter: 60,
  word: 200,
}

export interface TowerHintResult {
  kind: TowerHintKind
  state: TowerState
  /** Odhalený prefix u nápovědy „letter", celé slovo u „word". */
  text: string
}

/**
 * Nápověda odhaluje písmena kanonického řešení. Opakované použití prodlužuje
 * odhalený prefix, takže nápověda vždycky posune hráče dál.
 */
export function takeTowerHint(
  state: TowerState,
  kind: TowerHintKind,
  /** Zaplacená inkoustem — do bodů se pak nepromítne. */
  free = false,
): TowerHintResult | null {
  const level = currentLevel(state)
  if (!level) return null
  const answer = level.words[0]!
  const index = currentLevelIndex(state)

  if (kind === 'word') {
    return {
      kind,
      text: answer,
      state: {
        ...state,
        hintsUsed: state.hintsUsed + 1,
        hintCost: state.hintCost + (free ? 0 : TOWER_HINT_COST.word),
        freeHints: (state.freeHints ?? 0) + (free ? 1 : 0),
        revealedLevels: [...state.revealedLevels, index],
      },
    }
  }

  const already = state.revealedLevels.filter((i) => i === index).length
  const reveal = Math.min(already + 1, answer.length - 1)
  return {
    kind,
    text: answer.slice(0, reveal),
    state: {
      ...state,
      hintsUsed: state.hintsUsed + 1,
      hintCost: state.hintCost + (free ? 0 : TOWER_HINT_COST.letter),
      freeHints: (state.freeHints ?? 0) + (free ? 1 : 0),
      revealedLevels: [...state.revealedLevels, index],
    },
  }
}
