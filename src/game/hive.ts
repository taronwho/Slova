/**
 * Režim VOŠTINA — sedm písmen v plástvi, prostřední je povinné.
 *
 * Diakritika se při porovnávání s pláství skládá (á=a, č=c, ř=r …), takže
 * hráč píše normální češtinu, ale plástev nese jen sedm základních písmen.
 * Kompletní seznam řešení je předpočítaný při buildu, takže hra vždy ví,
 * kolik slov existuje, a ukazatel postupu nikdy neklame.
 */

import { fold } from '../lib/czech'
import type { Difficulty } from './types'

export interface HivePuzzle {
  id: string
  /** Prostřední, povinné písmeno. */
  center: string
  /** Šest okrajových písmen. */
  outer: string[]
  /** Všechna uznávaná slova (s diakritikou), předpočítaná. */
  solutions: string[]
  /** Slova používající všech sedm písmen. */
  pangrams: string[]
  difficulty: Difficulty
}

export interface HiveState {
  puzzle: HivePuzzle
  found: string[]
  /** Aktuální pořadí okrajových písmen — mění tlačítko Zamíchat. */
  ring: string[]
  hintsUsed: number
  /** Kolik z nich bylo zdarma — ty se do bodů nepočítají. */
  freeHints: number
  startedAt: number
}

export type HiveError =
  | 'too-short'
  | 'missing-center'
  | 'foreign-letter'
  | 'unknown-word'
  | 'already-found'

export const HIVE_ERROR_TEXT: Record<HiveError, string> = {
  'too-short': 'Slovo musí mít aspoň 4 písmena',
  'missing-center': 'Chybí prostřední písmeno',
  'foreign-letter': 'Použil jsi písmeno, které v plástvi není',
  'unknown-word': 'To slovo neznám',
  'already-found': 'Tohle slovo už máš',
}

export const MIN_WORD_LENGTH = 4

/** Body za slovo: čtyřpísmenné 1 bod, delší 1 bod za písmeno, pangram +7. */
export function wordScore(puzzle: HivePuzzle, word: string): number {
  const base = word.length === MIN_WORD_LENGTH ? 1 : word.length
  return base + (puzzle.pangrams.includes(word) ? 7 : 0)
}

export function maxScore(puzzle: HivePuzzle): number {
  return puzzle.solutions.reduce((sum, word) => sum + wordScore(puzzle, word), 0)
}

export function currentScore(state: HiveState): number {
  return state.found.reduce((sum, word) => sum + wordScore(state.puzzle, word), 0)
}

/** Hodnosti podle podílu dosaženého skóre. */
export const RANKS: { at: number; name: string }[] = [
  { at: 0, name: 'Začátečník' },
  { at: 0.02, name: 'Nováček' },
  { at: 0.05, name: 'Šikula' },
  { at: 0.08, name: 'Dobrý' },
  { at: 0.15, name: 'Slušný' },
  { at: 0.25, name: 'Skvělý' },
  { at: 0.4, name: 'Vynikající' },
  { at: 0.55, name: 'Génius' },
  { at: 1, name: 'Královna češtiny' },
]

export function rankFor(score: number, max: number): { name: string; index: number } {
  const ratio = max > 0 ? score / max : 0
  let index = 0
  for (let i = 0; i < RANKS.length; i++) {
    if (ratio >= RANKS[i]!.at) index = i
  }
  return { name: RANKS[index]!.name, index }
}

export function letterSet(puzzle: HivePuzzle): Set<string> {
  return new Set([puzzle.center, ...puzzle.outer])
}

export function createHiveState(puzzle: HivePuzzle, now = Date.now()): HiveState {
  return {
    puzzle,
    found: [],
    ring: [...puzzle.outer],
    hintsUsed: 0,
    freeHints: 0,
    startedAt: now,
  }
}

export type HiveOutcome =
  | { ok: false; error: HiveError }
  | { ok: true; state: HiveState; word: string; points: number; pangram: boolean }

/**
 * Řešení seskupená podle tvaru bez diakritiky.
 *
 * Plástev nese jen základní písmena, takže hráč, který slovo naťuká do
 * šestiúhelníků (na mobilu jediná cesta), nemá jak háčky a čárky zadat.
 * Porovnává se proto složený tvar a uznají se všechny zápisy, které na něj
 * sedí — „cili" tedy najde „cíli".
 */
function foldedGroups(puzzle: HivePuzzle): Map<string, string[]> {
  const groups = new Map<string, string[]>()
  for (const solution of puzzle.solutions) {
    const key = fold(solution)
    const group = groups.get(key)
    if (group) group.push(solution)
    else groups.set(key, [solution])
  }
  return groups
}

export function submitWord(
  state: HiveState,
  raw: string,
  now = Date.now(),
): HiveOutcome {
  void now
  const word = raw.trim().toLowerCase()
  const folded = fold(word)
  const letters = letterSet(state.puzzle)

  if (word.length < MIN_WORD_LENGTH) return { ok: false, error: 'too-short' }
  // Cizí písmeno se hlásí dřív než chybějící střed — je to konkrétnější
  // a pro hráče srozumitelnější důvod odmítnutí.
  for (const ch of folded) {
    if (!letters.has(ch)) return { ok: false, error: 'foreign-letter' }
  }
  if (!folded.includes(state.puzzle.center)) return { ok: false, error: 'missing-center' }

  const matches = foldedGroups(state.puzzle).get(folded)
  if (!matches) return { ok: false, error: 'unknown-word' }

  const fresh = matches.filter((solution) => !state.found.includes(solution))
  if (fresh.length === 0) return { ok: false, error: 'already-found' }

  // Přesný zápis s diakritikou se uzná přednostně, jinak se berou všechny
  // varianty skupiny — hráč je od sebe stejně nemá jak odlišit.
  const credited = matches.includes(word) && fresh.includes(word) ? [word] : fresh
  const points = credited.reduce((sum, item) => sum + wordScore(state.puzzle, item), 0)

  return {
    ok: true,
    state: { ...state, found: [...state.found, ...credited] },
    word: credited[0]!,
    points,
    pangram: credited.some((item) => state.puzzle.pangrams.includes(item)),
  }
}

/** Bodová cena nápovědy „další slovo". Odsud si ji bere i skóre. */
export const HIVE_HINT_COST = 80

/** Nápověda: odhalí nejkratší dosud nenalezené slovo. */
export function takeHiveHint(
  state: HiveState,
  /** Zaplacená inkoustem — do bodů se pak nepromítne. */
  free = false,
): { state: HiveState; word: string } | null {
  const remaining = state.puzzle.solutions
    .filter((word) => !state.found.includes(word))
    .sort((a, b) => a.length - b.length)
  const word = remaining[0]
  if (!word) return null
  return {
    state: {
      ...state,
      found: [...state.found, word],
      hintsUsed: state.hintsUsed + 1,
      freeHints: (state.freeHints ?? 0) + (free ? 1 : 0),
    },
    word,
  }
}

/** Přehled „kolik slov které délky ještě zbývá" — mřížka nápovědy. */
export function remainingByLength(state: HiveState): Map<number, number> {
  const counts = new Map<number, number>()
  for (const word of state.puzzle.solutions) {
    if (state.found.includes(word)) continue
    counts.set(word.length, (counts.get(word.length) ?? 0) + 1)
  }
  return new Map([...counts.entries()].sort((a, b) => a[0] - b[0]))
}
