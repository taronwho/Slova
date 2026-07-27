/**
 * SLABIKOVÝ TETRIS — logika.
 *
 * Slabiky padají do sloupců a hráč z nich skládá slova. Vodorovně se čte
 * **zleva doprava**, svisle **zdola nahoru** — tedy směrem, kterým sloupec
 * roste, stejně jako se čte Věž. Jakmile dvě nebo tři sousední slabiky dají
 * platné slovo, zmizí a co bylo nad nimi, spadne dolů; z toho můžou vzniknout
 * další slova a řetěz pokračuje.
 *
 * Co je platné slovo, hra **nehádá**. Ke každé dávce je předpočítaný seznam
 * všech slov, která z jejích slabik jdou složit (`tools/5f_build_tetris.py`),
 * a ten se staví z ověřených základních tvarů. Runtime tedy jen hledá
 * v množině — nemůže uznat tvar, který by ve slovníku nebyl.
 *
 * Deska se drží jako **husté pole zdola**: `grid[sloupec][patro]`, patro 0 je
 * dole. Gravitace pak není samostatný krok — smazáním prvku z pole se všechno
 * nad ním samo posune dolů.
 */

import type { Difficulty } from './types'

export interface TetrisPuzzle {
  id: string
  difficulty: Difficulty
  cols: number
  rows: number
  /** Slabiky v pořadí, v jakém přijdou. */
  queue: string[]
  /** Všechna slova, která z dávky jdou složit. */
  words: string[]
  /** Slova, ze kterých dávka vznikla — ukážou se až po kole. */
  seed: string[]
}

export interface TetrisState {
  puzzle: TetrisPuzzle
  /** grid[sloupec] = slabiky zdola nahoru. */
  grid: string[][]
  /**
   * Slabiky, které ještě čekají. První tři jsou v zásobníku a hráč si mezi
   * nimi vybírá — bez té volby je hra loterie: jedna slabika, která se zrovna
   * nehodí, zůstane na desce ležet navždycky.
   */
  queue: string[]
  /** Složená slova v pořadí, jak padla. */
  cleared: string[]
  /** Nejdelší řetěz slov z jednoho tahu. */
  bestChain: number
  hintsUsed: number
  /** Kolik nápověd bylo zaplaceno inkoustem — ty se do bodů nepočítají. */
  freeHints: number
  hintCost: number
  startedAt: number
  finishedAt: number | null
  /** Hráč kolo ukončil sám. */
  gaveUp: boolean
}

/** Nejvíc slabik vedle sebe, které se ještě čtou jako jedno slovo. */
export const TETRIS_MAX_RUN = 3

/** Kolik slabik má hráč v zásobníku na výběr. */
export const TETRIS_TRAY = 3

export const TETRIS_HINT_COST = {
  /** Ukáže tah, který právě teď něco složí. */
  column: 100,
  /** Pošle slabiku ze zásobníku na konec fronty. */
  swap: 60,
} as const

export type TetrisHintKind = keyof typeof TETRIS_HINT_COST

export function createTetrisState(puzzle: TetrisPuzzle, now = Date.now()): TetrisState {
  return {
    puzzle,
    grid: Array.from({ length: puzzle.cols }, () => []),
    queue: [...puzzle.queue],
    cleared: [],
    bestChain: 0,
    hintsUsed: 0,
    freeHints: 0,
    hintCost: 0,
    startedAt: now,
    finishedAt: null,
    gaveUp: false,
  }
}

/** Slabiky v zásobníku — z těch si hráč vybírá. */
export function tray(state: TetrisState): string[] {
  return state.queue.slice(0, TETRIS_TRAY)
}

/** Co čeká za zásobníkem. Jen náznak, ať se dá plánovat dopředu. */
export function upcoming(state: TetrisState, count = 3): string[] {
  return state.queue.slice(TETRIS_TRAY, TETRIS_TRAY + count)
}

export function placed(state: TetrisState): number {
  return state.grid.reduce((sum, column) => sum + column.length, 0)
}

/** Do sloupce se vejde další slabika? */
export function canDrop(state: TetrisState, col: number): boolean {
  const column = state.grid[col]
  return column !== undefined && column.length < state.puzzle.rows
}

export function isFull(state: TetrisState): boolean {
  return state.grid.every((column) => column.length >= state.puzzle.rows)
}

/** Fronta došla — hráč umístil všechno, co dostal. */
export function isDone(state: TetrisState): boolean {
  return state.queue.length === 0
}

export function isOver(state: TetrisState): boolean {
  return state.gaveUp || isDone(state) || isFull(state)
}

/**
 * Dotáhl hráč kolo?
 *
 * Ne „vyčistil desku", ale „rozmístil celou dávku". Zbytek na desce stojí
 * body, ale kolo je dohrané — stejně jako plástev, ze které hráč nevysbírá
 * všechno.
 */
export function isWon(state: TetrisState): boolean {
  return isDone(state) && !state.gaveUp
}

/** Deska je po kole prázdná — celá dávka se rozpustila ve slovech. */
export function isSwept(state: TetrisState): boolean {
  return isDone(state) && placed(state) === 0
}

interface Match {
  word: string
  /** Buňky ke smazání jako [sloupec, patro]. */
  cells: [number, number][]
}

/** Najde nejdelší slovo, které na desce právě leží. */
function findMatch(grid: string[][], words: Set<string>): Match | null {
  const cols = grid.length
  const rows = Math.max(0, ...grid.map((column) => column.length))

  // Delší slovo má přednost: „žra-lok" se nemá rozpadnout na kratší kousek,
  // který náhodou taky existuje.
  for (let len = TETRIS_MAX_RUN; len >= 2; len -= 1) {
    // Vodorovně, zleva doprava.
    for (let row = 0; row < rows; row += 1) {
      for (let col = 0; col + len <= cols; col += 1) {
        const cells: [number, number][] = []
        let text = ''
        let ok = true
        for (let i = 0; i < len; i += 1) {
          const syllable = grid[col + i]?.[row]
          if (syllable === undefined) {
            ok = false
            break
          }
          text += syllable
          cells.push([col + i, row])
        }
        if (ok && words.has(text)) return { word: text, cells }
      }
    }
    // Svisle, zdola nahoru — tím směrem sloupec roste.
    for (let col = 0; col < cols; col += 1) {
      const column = grid[col]!
      for (let row = 0; row + len <= column.length; row += 1) {
        let text = ''
        const cells: [number, number][] = []
        for (let i = 0; i < len; i += 1) {
          text += column[row + i]!
          cells.push([col, row + i])
        }
        if (words.has(text)) return { word: text, cells }
      }
    }
  }
  return null
}

/** Smaže buňky. Husté pole se tím samo srovná — to je gravitace. */
function removeCells(grid: string[][], cells: [number, number][]): string[][] {
  const drop = new Map<number, Set<number>>()
  for (const [col, row] of cells) {
    if (!drop.has(col)) drop.set(col, new Set())
    drop.get(col)!.add(row)
  }
  return grid.map((column, col) => {
    const rows = drop.get(col)
    if (!rows) return column
    return column.filter((_, row) => !rows.has(row))
  })
}

export interface DropResult {
  state: TetrisState
  /** Slova, která tah složil — v pořadí řetězu. */
  words: string[]
}

/**
 * Položí vybranou slabiku ze zásobníku do sloupce a vyhodnotí, co z toho
 * spadlo. `slot` je pozice v zásobníku (0–2).
 */
export function dropSyllable(state: TetrisState, col: number, slot = 0): DropResult | null {
  const syllable = state.queue[slot]
  if (syllable === undefined || slot >= TETRIS_TRAY) return null
  if (isOver(state) || !canDrop(state, col)) return null

  let grid = state.grid.map((column, i) => (i === col ? [...column, syllable] : column))
  const words = new Set(state.puzzle.words)
  const made: string[] = []
  for (;;) {
    const match = findMatch(grid, words)
    if (!match) break
    made.push(match.word)
    grid = removeCells(grid, match.cells)
  }

  const next: TetrisState = {
    ...state,
    grid,
    queue: state.queue.filter((_, i) => i !== slot),
    cleared: [...state.cleared, ...made],
    bestChain: Math.max(state.bestChain, made.length),
  }
  // Kolo končí, až když je fronta pryč nebo se nikam nedá položit.
  if (isOver(next)) next.finishedAt = Date.now()
  return { state: next, words: made }
}

/** Sloupce, kde by slabika ze zásobníku něco složila. */
export function scoringColumns(state: TetrisState, slot = 0): number[] {
  const out: number[] = []
  for (let col = 0; col < state.puzzle.cols; col += 1) {
    if (!canDrop(state, col)) continue
    const result = dropSyllable(state, col, slot)
    if (result && result.words.length > 0) out.push(col)
  }
  return out
}

/** Tah, který právě teď něco složí: [zásobník, sloupec]. */
export function scoringMove(state: TetrisState): [number, number] | null {
  for (let slot = 0; slot < Math.min(TETRIS_TRAY, state.queue.length); slot += 1) {
    const columns = scoringColumns(state, slot)
    if (columns.length > 0) return [slot, columns[0]!]
  }
  return null
}

export interface TetrisHintResult {
  kind: TetrisHintKind
  state: TetrisState
  /** U nápovědy „tah" doporučený sloupec a slabika ze zásobníku. */
  column?: number
  slot?: number
  /** U nápovědy „odložit" slabika, která šla dozadu. */
  syllable?: string
}

export function takeTetrisHint(
  state: TetrisState,
  kind: TetrisHintKind,
  /** Zaplacená inkoustem — do bodů se pak nepromítne. */
  free = false,
): TetrisHintResult | null {
  if (isOver(state)) return null
  const paid = {
    hintsUsed: state.hintsUsed + 1,
    freeHints: state.freeHints + (free ? 1 : 0),
    hintCost: state.hintCost + (free ? 0 : TETRIS_HINT_COST[kind]),
  }

  if (kind === 'column') {
    const move = scoringMove(state)
    if (!move) return null
    return { kind, state: { ...state, ...paid }, slot: move[0], column: move[1] }
  }

  // Odložit: první slabika ze zásobníku jde na konec fronty. Zbaví hráče
  // kamene, který se zrovna nehodí, ale nezmizí — jen počká.
  if (state.queue.length <= TETRIS_TRAY) return null
  const [first, ...rest] = state.queue
  const queue = [...rest, first!]
  return { kind, state: { ...state, ...paid, queue }, syllable: first! }
}

export function giveUp(state: TetrisState): TetrisState {
  return { ...state, gaveUp: true, finishedAt: Date.now() }
}
