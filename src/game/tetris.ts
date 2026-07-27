/**
 * SLABIKOVÝ TETRIS — logika.
 *
 * Padá dvojice slabik. Hráč s ní posouvá doleva a doprava, **otáčí ji** a
 * může ji nechat spadnout naráz. Když dvě nebo tři sousední slabiky dají
 * platné české slovo, slovo zmizí, co bylo nad ním spadne dolů a z toho může
 * vzniknout další slovo — řetěz. Deska se plní, tempo zrychluje, kolo končí,
 * až se nová dvojice nemá kam vejít.
 *
 * Otáčení je to hlavní, co se hraje. Dvojice `a`+`b` má čtyři polohy a v nich
 * se čte obojím pořadím:
 *
 *     0  a b        vodorovně, zleva doprava   -> „ab"
 *     1  b/a        svisle, zdola nahoru       -> „ab"
 *     2  b a        vodorovně                  -> „ba"
 *     3  a/b        svisle                     -> „ba"
 *
 * Padá tedy „ko"+„lo" a je jen na hráči, jestli z toho udělá KOLO hned, nebo
 * si každou půlku uloží k něčemu, co na desce leží.
 *
 * Co je platné slovo, hra **nehádá**: `deck.words` je předpočítaný seznam
 * všech slov, která z rozdávaných slabik jdou složit, a staví se z ověřených
 * základních tvarů (`tools/5f_build_tetris.py`).
 *
 * Deska se drží jako **husté pole zdola**: `grid[sloupec][patro]`, patro 0 je
 * dole. Gravitace pak není samostatný krok — smazáním prvku z pole se všechno
 * nad ním samo posune dolů.
 */

import { mulberry32 } from '../lib/rng'
import type { Difficulty } from './types'

export interface TetrisDeck {
  /** Slabika a její váha při rozdávání. */
  syllables: [string, number][]
  /** Dvojslabičná slova rozdělená na dvě slabiky. */
  pairs: [string, string][]
  /** Všechna slova, která z balíčku jdou složit. */
  words: string[]
}

export interface TetrisSetup {
  difficulty: Difficulty
  cols: number
  rows: number
  /** Jak dlouho trvá pád o jedno patro na začátku (ms). */
  startMs: number
  /** Kolik slov se musí složit, než tempo přidá. */
  perLevel: number
  /** Zrnko pro rozdávání — denní výzva má u všech hráčů stejné. */
  seed: number
}

/** Dvojice, která právě padá. */
export interface Piece {
  a: string
  b: string
  /** Sloupec, ve kterém je `a`. */
  col: number
  /** Patro, ve kterém je `a` (0 = dole). */
  row: number
  /** 0 = b vpravo, 1 = b nahoře, 2 = b vlevo, 3 = b dole. */
  turn: number
}

export interface TetrisState {
  deck: TetrisDeck
  setup: TetrisSetup
  /** grid[sloupec] = slabiky zdola nahoru. */
  grid: string[][]
  piece: Piece | null
  /** Co přijde po ní. */
  queue: [string, string][]
  /** Kolik dvojic už bylo rozdáno — z toho se odvozuje stav generátoru. */
  dealt: number
  cleared: string[]
  bestChain: number
  hintsUsed: number
  /** Kolik nápověd bylo zaplaceno inkoustem — ty se do bodů nepočítají. */
  freeHints: number
  hintCost: number
  paused: boolean
  over: boolean
  startedAt: number
  finishedAt: number | null
}

/** Nejvíc slabik vedle sebe, které se ještě čtou jako jedno slovo. */
export const TETRIS_MAX_RUN = 3

/** Kolik dvojic dopředu hráč vidí. */
export const TETRIS_PREVIEW = 2

/**
 * Bodová cena nápověd.
 *
 * Skóre Slabik jde na desetinu ostatních her (viz `scoreTetris`), takže
 * s ním musí jít i ceny nápověd — jinak by jedna nápověda spolkla celé kolo.
 */
export const TETRIS_HINT_COST = {
  /** Ukáže polohu, ve které padající dvojice něco složí. */
  spot: 4,
  /** Vymění padající dvojici za tu následující. */
  swap: 2,
} as const

/**
 * Cena nápověd v inkoustu.
 *
 * Jinde se odvozuje z bodové ceny (`inkPrice`), tady ne: čtyři body by daly
 * jedinou kapku a nápověda by přestala být rozhodnutí. Inkoust se platí za
 * **velikost pomoci**, a ta je ve Slabikách stejná jako kdekoli jinde, ať se
 * bodová stupnice režimu jmenuje jakkoli.
 */
export const TETRIS_INK_COST = {
  spot: 11,
  swap: 6,
} as const

export type TetrisHintKind = keyof typeof TETRIS_HINT_COST

export const TETRIS_LEVELS: Record<Difficulty, Omit<TetrisSetup, 'seed' | 'difficulty'>> = {
  easy: { cols: 6, rows: 11, startMs: 1500, perLevel: 8 },
  normal: { cols: 6, rows: 12, startMs: 1100, perLevel: 8 },
  hard: { cols: 7, rows: 13, startMs: 800, perLevel: 6 },
}

/** Pod tuhle hranici tempo neklesne — jinak by se nedalo číst. */
const MIN_MS = 380

export function tetrisSetup(difficulty: Difficulty, seed: number): TetrisSetup {
  return { difficulty, seed, ...TETRIS_LEVELS[difficulty] }
}

/**
 * Rozdá dvojici.
 *
 * Zhruba každá třetí je **rozdělené slovo** — jde složit hned, ale jen když ji
 * hráč otočí do správné polohy. Zbytek se losuje po slabikách podle váhy, aby
 * deska nebyla samé „po" a „ná".
 */
function deal(deck: TetrisDeck, seed: number, index: number): [string, string] {
  const random = mulberry32((seed + index * 0x9e3779b1) >>> 0)
  if (deck.pairs.length > 0 && random() < 0.34) {
    const pair = deck.pairs[Math.floor(random() * deck.pairs.length)]!
    // Pořadí se prohodí, ať se nedá spoléhat, že „první je vždycky první".
    return random() < 0.5 ? [pair[0], pair[1]] : [pair[1], pair[0]]
  }
  return [pick(deck, random()), pick(deck, random())]
}

/** Vybere slabiku podle váhy. */
function pick(deck: TetrisDeck, roll: number): string {
  const total = deck.syllables.reduce((sum, [, weight]) => sum + weight, 0)
  let at = roll * total
  for (const [syllable, weight] of deck.syllables) {
    at -= weight
    if (at <= 0) return syllable
  }
  return deck.syllables[0]![0]
}

function spawn(state: TetrisState, pair: [string, string]): Piece {
  return {
    a: pair[0],
    b: pair[1],
    col: Math.floor((state.setup.cols - 1) / 2),
    row: state.setup.rows - 1,
    turn: 0,
  }
}

export function createTetrisState(
  deck: TetrisDeck,
  setup: TetrisSetup,
  now = Date.now(),
): TetrisState {
  const base: TetrisState = {
    deck,
    setup,
    grid: Array.from({ length: setup.cols }, () => []),
    piece: null,
    queue: [],
    dealt: 0,
    cleared: [],
    bestChain: 0,
    hintsUsed: 0,
    freeHints: 0,
    hintCost: 0,
    paused: false,
    over: false,
    startedAt: now,
    finishedAt: null,
  }
  const queue: [string, string][] = []
  for (let i = 0; i <= TETRIS_PREVIEW; i += 1) queue.push(deal(deck, setup.seed, i))
  const [first, ...rest] = queue
  base.dealt = TETRIS_PREVIEW + 1
  base.queue = rest
  base.piece = spawn(base, first!)
  return base
}

/** Kde leží druhá polovina dvojice. */
export function partnerCell(piece: Piece): { col: number; row: number } {
  if (piece.turn === 0) return { col: piece.col + 1, row: piece.row }
  if (piece.turn === 1) return { col: piece.col, row: piece.row + 1 }
  if (piece.turn === 2) return { col: piece.col - 1, row: piece.row }
  return { col: piece.col, row: piece.row - 1 }
}

/** Obě políčka dvojice — první je vždycky `a`. */
export function cells(piece: Piece): { col: number; row: number; text: string }[] {
  const other = partnerCell(piece)
  return [
    { col: piece.col, row: piece.row, text: piece.a },
    { col: other.col, row: other.row, text: piece.b },
  ]
}

function free(state: TetrisState, col: number, row: number): boolean {
  if (col < 0 || col >= state.setup.cols) return false
  if (row < 0) return false
  // Nad deskou je volno — dvojice se tam smí rodit i otáčet.
  if (row >= state.setup.rows) return true
  return state.grid[col]!.length <= row
}

function fits(state: TetrisState, piece: Piece): boolean {
  return cells(piece).every((cell) => free(state, cell.col, cell.row))
}

/** Level roste se složenými slovy; s ním roste tempo. */
export function level(state: TetrisState): number {
  return Math.floor(state.cleared.length / state.setup.perLevel) + 1
}

/** Jak dlouho teď trvá pád o jedno patro. */
export function dropMs(state: TetrisState): number {
  const step = level(state) - 1
  return Math.max(MIN_MS, Math.round(state.setup.startMs * Math.pow(0.9, step)))
}

export function move(state: TetrisState, dx: number): TetrisState {
  if (!state.piece || state.over || state.paused) return state
  const next = { ...state.piece, col: state.piece.col + dx }
  return fits(state, next) ? { ...state, piece: next } : state
}

/**
 * Otočí dvojici o čtvrt otáčky.
 *
 * Když se otočená poloha nevejde (dvojice stojí u kraje), zkusí se ještě
 * posun o jedno políčko dovnitř — klasický „kop od stěny", bez kterého se
 * u kraje otáčet nedá.
 */
export function rotate(state: TetrisState, by = 1): TetrisState {
  if (!state.piece || state.over || state.paused) return state
  const turn = (state.piece.turn + by + 4) % 4
  for (const dx of [0, 1, -1]) {
    const next = { ...state.piece, turn, col: state.piece.col + dx }
    if (fits(state, next)) return { ...state, piece: next }
  }
  return state
}

interface Match {
  word: string
  cells: [number, number][]
}

function findMatch(grid: string[][], words: Set<string>): Match | null {
  const cols = grid.length
  const rows = Math.max(0, ...grid.map((column) => column.length))

  // Delší slovo má přednost: ze „žra-lok" se nemá stát „lok".
  for (let len = TETRIS_MAX_RUN; len >= 2; len -= 1) {
    for (let row = 0; row < rows; row += 1) {
      for (let col = 0; col + len <= cols; col += 1) {
        const list: [number, number][] = []
        let text = ''
        let ok = true
        for (let i = 0; i < len; i += 1) {
          const syllable = grid[col + i]?.[row]
          if (syllable === undefined) {
            ok = false
            break
          }
          text += syllable
          list.push([col + i, row])
        }
        if (ok && words.has(text)) return { word: text, cells: list }
      }
    }
    for (let col = 0; col < cols; col += 1) {
      const column = grid[col]!
      for (let row = 0; row + len <= column.length; row += 1) {
        let text = ''
        const list: [number, number][] = []
        for (let i = 0; i < len; i += 1) {
          text += column[row + i]!
          list.push([col, row + i])
        }
        if (words.has(text)) return { word: text, cells: list }
      }
    }
  }
  return null
}

/** Smaže políčka. Husté pole se tím samo srovná — to je gravitace. */
function removeCells(grid: string[][], list: [number, number][]): string[][] {
  const drop = new Map<number, Set<number>>()
  for (const [col, row] of list) {
    if (!drop.has(col)) drop.set(col, new Set())
    drop.get(col)!.add(row)
  }
  return grid.map((column, col) => {
    const rows = drop.get(col)
    if (!rows) return column
    return column.filter((_, row) => !rows.has(row))
  })
}

/** Položí dvojici do mřížky. Obě půlky padnou do svého sloupce zvlášť. */
function place(grid: string[][], piece: Piece): string[][] {
  const next = grid.map((column) => [...column])
  // Odspodu, aby si dvě půlky v jednom sloupci nepřehodily pořadí.
  for (const cell of cells(piece).sort((x, y) => x.row - y.row)) {
    next[cell.col]!.push(cell.text)
  }
  return next
}

export interface StepResult {
  state: TetrisState
  /** Dvojice právě dosedla. */
  locked: boolean
  /** Slova, která z toho spadla — v pořadí řetězu. */
  words: string[]
}

/** Posun o jedno patro dolů. Když už to nejde, dvojice dosedne. */
export function step(state: TetrisState): StepResult {
  if (!state.piece || state.over || state.paused) {
    return { state, locked: false, words: [] }
  }
  const down = { ...state.piece, row: state.piece.row - 1 }
  if (fits(state, down)) {
    return { state: { ...state, piece: down }, locked: false, words: [] }
  }
  return lock(state)
}

/** Kam by dvojice dosedla, kdyby teď spadla — stín pod padající dvojicí. */
export function landing(state: TetrisState): { col: number; row: number; text: string }[] {
  if (!state.piece) return []
  let piece = state.piece
  for (;;) {
    const down = { ...piece, row: piece.row - 1 }
    if (!fits(state, down)) break
    piece = down
  }
  return cells(piece)
}

/** Nechá dvojici spadnout až dolů. */
export function hardDrop(state: TetrisState): StepResult {
  if (!state.piece || state.over || state.paused) {
    return { state, locked: false, words: [] }
  }
  let piece = state.piece
  for (;;) {
    const down = { ...piece, row: piece.row - 1 }
    if (!fits(state, down)) break
    piece = down
  }
  return lock({ ...state, piece })
}

function lock(state: TetrisState): StepResult {
  const piece = state.piece!
  let grid = place(state.grid, piece)
  const words = new Set(state.deck.words)
  const made: string[] = []
  for (;;) {
    const match = findMatch(grid, words)
    if (!match) break
    made.push(match.word)
    grid = removeCells(grid, match.cells)
  }

  // Co přeteče nad okraj desky, se zahodí — jinak by sloupec rostl donekonečna.
  grid = grid.map((column) => column.slice(0, state.setup.rows))

  const [nextPair, ...rest] = state.queue
  const queue = [...rest, deal(state.deck, state.setup.seed, state.dealt)]
  const base: TetrisState = {
    ...state,
    grid,
    queue,
    dealt: state.dealt + 1,
    piece: null,
    cleared: [...state.cleared, ...made],
    bestChain: Math.max(state.bestChain, made.length),
  }
  const fresh = spawn(base, nextPair!)
  if (!fits(base, fresh)) {
    return {
      state: { ...base, over: true, finishedAt: Date.now() },
      locked: true,
      words: made,
    }
  }
  return { state: { ...base, piece: fresh }, locked: true, words: made }
}

export function togglePause(state: TetrisState): TetrisState {
  if (state.over) return state
  return { ...state, paused: !state.paused }
}

export function endRound(state: TetrisState): TetrisState {
  if (state.over) return state
  return { ...state, over: true, finishedAt: Date.now() }
}

export function placed(state: TetrisState): number {
  return state.grid.reduce((sum, column) => sum + column.length, 0)
}

/** Jak plná je deska (0–1). Podle toho se barví ukazatel. */
export function fill(state: TetrisState): number {
  return placed(state) / (state.setup.cols * state.setup.rows)
}

export function isOver(state: TetrisState): boolean {
  return state.over
}

/**
 * Kolo se počítá za dohrané, když v něm hráč něco složil.
 *
 * Tenhle režim se nedá „vyhrát" — hraje se, dokud deska nepřeteče. Metou tedy
 * není dojít do cíle, ale vůbec něco poskládat; prázdný odchod se nepočítá,
 * aby se čisté kolo nedalo získat okamžitým ukončením.
 */
export function isWon(state: TetrisState): boolean {
  return state.cleared.length > 0
}

export interface Spot {
  turn: number
  col: number
  words: string[]
}

/** Polohy, ve kterých by padající dvojice po dopadu něco složila. */
export function scoringSpots(state: TetrisState): Spot[] {
  if (!state.piece || state.over) return []
  const out: Spot[] = []
  for (let turn = 0; turn < 4; turn += 1) {
    for (let col = 0; col < state.setup.cols; col += 1) {
      const trial: TetrisState = {
        ...state,
        paused: false,
        piece: { ...state.piece, turn, col, row: state.setup.rows },
      }
      if (!fits(trial, trial.piece!)) continue
      const result = hardDrop(trial)
      if (result.words.length > 0) out.push({ turn, col, words: result.words })
    }
  }
  return out
}

export interface TetrisHintResult {
  kind: TetrisHintKind
  state: TetrisState
  spot?: Spot
}

export function takeTetrisHint(
  state: TetrisState,
  kind: TetrisHintKind,
  /** Zaplacená inkoustem — do bodů se pak nepromítne. */
  free_ = false,
): TetrisHintResult | null {
  if (state.over || !state.piece) return null
  const paid = {
    hintsUsed: state.hintsUsed + 1,
    freeHints: state.freeHints + (free_ ? 1 : 0),
    hintCost: state.hintCost + (free_ ? 0 : TETRIS_HINT_COST[kind]),
  }

  if (kind === 'spot') {
    const spots = scoringSpots(state)
    if (spots.length === 0) return null
    // Nejvýnosnější poloha, ne první nalezená.
    const best = spots.reduce((top, spot) => (spot.words.length > top.words.length ? spot : top))
    return { kind, state: { ...state, ...paid }, spot: best }
  }

  // Výměna za následující dvojici. Padající se zařadí zpátky do fronty.
  const [next, ...rest] = state.queue
  if (!next) return null
  const piece = { ...state.piece, a: next[0], b: next[1] }
  if (!fits(state, piece)) return null
  return {
    kind,
    state: {
      ...state,
      ...paid,
      piece,
      queue: [...rest, [state.piece.a, state.piece.b]],
    },
  }
}
