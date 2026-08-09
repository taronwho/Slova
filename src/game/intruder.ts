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

export interface IntruderPuzzle {
  id: string
  words: string[]
  /** Slovo, které do pětice nepatří. */
  odd: string
  /** Tři věty do druhého kroku, už zamíchané. */
  choices: string[]
  /** Ta z nich, která čtveřici od vetřelce opravdu odděluje. */
  answer: string
  /** Věta do vyhodnocení — co pětici spojovalo a co s vetřelcem. */
  recap: string
  difficulty: Difficulty
  /**
   * Rodina, ze které pětice pochází — zhruba „střecha", pod kterou slova patří.
   *
   * Je to jediné, podle čeho jde poznat, že dvě pětice jsou si podobné, i když
   * nemají společné ani jedno slovo. Hra podle toho rodiny střídá.
   */
  family: string
}

/**
 * Kolik posledních kol se hlídá, aby se rodina neopakovala.
 *
 * Hráč hlásil, že z deseti kol byly pětkrát karty a třikrát zvěrokruh. Půlku
 * toho měla na svědomí sada, ve které měly některé rodiny osminásobný podíl;
 * to je spravené u zdroje. Druhá půlka je náhoda sama: i z rovnoměrné sady
 * padne totéž dvakrát za sebou překvapivě často. Šest kol zpátky je dost
 * na to, aby se to nestávalo, a málo na to, aby došly rodiny k výběru.
 */
export const FAMILY_GAP = 6

/**
 * Pětice, která navazuje na to, co hráč nedávno hrál.
 *
 * Vybírá se z těch, které ještě nehrál **a** nejsou z rodiny posledních šesti
 * kol. Když by tím nezbylo nic, podmínky se pouštějí po jedné — nejdřív
 * rodina, potom i to, že hádanku už viděl. Prázdný výběr vrátit nesmí,
 * hra by neměla co spustit.
 */
export function pickIntruder(
  pool: IntruderPuzzle[],
  seen: string[],
  random: () => number,
): IntruderPuzzle {
  const byId = new Map(pool.map((puzzle) => [puzzle.id, puzzle]))
  const recent = new Set<string>()
  for (const id of seen.slice(-FAMILY_GAP)) {
    const found = byId.get(id)
    if (found) recent.add(found.family)
  }
  const played = new Set(seen)
  const fresh = pool.filter((one) => !played.has(one.id) && !recent.has(one.family))
  const unplayed = pool.filter((one) => !played.has(one.id))
  const use = fresh.length > 0 ? fresh : unplayed.length > 0 ? unplayed : pool
  return use[Math.floor(random() * use.length)]!
}

/**
 * Pětice na denní výzvu.
 *
 * Musí být pro všechny stejná a pro daný den pevná, takže se nedá vybírat
 * podle toho, co kdo hrál. Rodina se proto určí číslem dne: den po dni se
 * projde celý seznam rodin a teprve pak se začne nanovo. Dva dny po sobě
 * tak nikdy nepřijde totéž a hráč projde všechny rodiny dřív, než uvidí
 * jednu podruhé.
 */
export function dailyIntruder(
  pool: IntruderPuzzle[],
  day: number,
  random: () => number,
): IntruderPuzzle {
  const families = [...new Set(pool.map((one) => one.family))].sort()
  if (families.length === 0) return pool[Math.floor(random() * pool.length)]!
  const family = families[((day % families.length) + families.length) % families.length]!
  const group = pool.filter((one) => one.family === family)
  return group[Math.floor(random() * group.length)]!
}

export const INTRUDER_HINT_COST = 40

export interface IntruderState {
  puzzle: IntruderPuzzle
  /** Slovo, na které hráč ukázal. */
  picked: string | null
  /** Souvislost, kterou pojmenoval. */
  reason: string | null
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
  state.reason === state.puzzle.answer

/**
 * Ukázání na slovo kolo rovnou ukončí.
 *
 * Druhý krok — vybrat ze tří vět tu správnou — z Vetřelce vypadl schválně.
 * U skrytých souvislostí byl největší nápovědou ve hře: hráč nemusel na nic
 * přijít, stačilo mu přečíst nabídku a ověřit ji. Souvislost se teď dozví
 * až ve vyhodnocení, kde už prozrazovat nemá co.
 */
export function pick(state: IntruderState, word: string): IntruderState {
  if (state.picked || state.finishedAt) return state
  return { ...state, picked: word, finishedAt: Date.now() }
}

export function name(state: IntruderState, choice: string): IntruderState {
  if (!state.picked || state.reason || state.finishedAt) return state
  return { ...state, reason: choice, finishedAt: Date.now() }
}

/** Nápověda vyloučí jedno slovo, které vetřelec není. */
export function takeHint(state: IntruderState): IntruderState | null {
  const safe = state.puzzle.words.filter(
    (word) => word !== state.puzzle.odd && !state.ruled.includes(word),
  )
  if (state.picked || safe.length === 0) return null
  return { ...state, ruled: [...state.ruled, safe[0]!] }
}
