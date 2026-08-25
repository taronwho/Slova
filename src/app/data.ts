/** Načítání herních dat — vše staticky, po balíčcích, s cache v paměti. */

import { buildChainGraph, type ChainGraph, type ChainPuzzle } from '../game/chain'
import type { HivePuzzle } from '../game/hive'
import type { DetectivePuzzle } from '../game/detective'
import type { GallowsPuzzle } from '../game/gallows'
import type { QuizDeck } from '../game/quiz'
import type { IntruderPuzzle } from '../game/intruder'
import type { Quote } from '../game/quotes'
import type { TetrisDeck } from '../game/tetris'
import type { TowerPuzzle } from '../game/tower'
import type { Difficulty } from '../game/types'

const BASE = import.meta.env.BASE_URL

const cache = new Map<string, Promise<unknown>>()

/**
 * Jednosouborový build (a stránky s přísnou CSP) nesmí nic dotahovat ze sítě,
 * proto se do něj data vloží rovnou. Když jsou k dispozici, čtou se odsud.
 */
declare global {
  interface Window {
    __SLOVA_DATA__?: Record<string, unknown>
  }
}

/**
 * Stažení jednoho balíčku dat — s lhůtou.
 *
 * `fetch` sám od sebe nikdy neskončí: když spojení uvázne v půli (telefon
 * přepíná mezi wi-fi a daty, síť odpoví jen zpola), slib se nesplní ani
 * nezamítne a obrazovka, která na data čeká, zůstane viset. Přesně tak
 * uvázla výzva na souboj ve fázi „Chystám hádanky…". Půl minuty je dost
 * i na dvoumegový balíček přes pomalé připojení.
 */
const NACITANI_MS = 30_000

async function nacti<T>(path: string): Promise<T> {
  const stopka = new AbortController()
  const budik = setTimeout(() => stopka.abort(), NACITANI_MS)
  try {
    const response = await fetch(`${BASE}data/${path}`, { signal: stopka.signal })
    if (!response.ok) throw new Error(`Nepodařilo se načíst ${path}`)
    return (await response.json()) as T
  } catch (chyba) {
    if (stopka.signal.aborted) throw new Error(`Data se nestihla načíst (${path}).`)
    throw chyba
  } finally {
    clearTimeout(budik)
  }
}

function fetchJson<T>(path: string): Promise<T> {
  const key = path
  const hit = cache.get(key)
  if (hit) return hit as Promise<T>

  const embedded = typeof window !== 'undefined' ? window.__SLOVA_DATA__?.[path] : undefined
  const request =
    embedded !== undefined
      ? Promise.resolve(embedded as T)
      : nacti<T>(path)
          /*
           * Neúspěch se nesmí zapamatovat.
           *
           * V paměti leží slib, ne hotová data — a zamítnutý slib se vracel
           * pořád dokola. Jedno klopýtnutí sítě tak umlčelo celý balíček až
           * do restartu hry: hráč se vrátil na signál, ťukl znovu a dostal
           * tutéž chybu, protože se o nic nepokusilo.
           */
          .catch((chyba: unknown) => {
            cache.delete(key)
            throw chyba
          })

  cache.set(key, request)
  return request
}

/* ---------- Řetěz ---------- */

export const CHAIN_LENGTH: Record<Difficulty, 4 | 5 | 6> = {
  easy: 4,
  normal: 5,
  hard: 6,
}

export interface ChainBundle {
  length: number
  graph: ChainGraph
  puzzles: ChainPuzzle[]
}

const chainBundles = new Map<number, Promise<ChainBundle>>()

export function loadChain(difficulty: Difficulty): Promise<ChainBundle> {
  const length = CHAIN_LENGTH[difficulty]
  const hit = chainBundles.get(length)
  if (hit) return hit

  const bundle = Promise.all([
    fetchJson<string[]>(`chain/words-${length}.json`),
    fetchJson<[string, string, number][]>(`chain/puzzles-${length}.json`),
  ]).then(([words, rows]) => ({
    length,
    graph: buildChainGraph(words),
    puzzles: rows.map(([start, target, par], i) => ({
      id: `c${length}-${i}`,
      start,
      target,
      par,
      difficulty,
    })),
  }))

  chainBundles.set(length, bundle)
  return bundle
}

/* ---------- Voština ---------- */

interface HiveIndexEntry {
  id: string
  pack: number
  center: string
  outer: string[]
  n: number
  difficulty: Difficulty
}

export function loadHiveIndex(): Promise<{ hives: HiveIndexEntry[] }> {
  return fetchJson('hive/index.json')
}

export async function loadHive(entry: HiveIndexEntry): Promise<HivePuzzle> {
  const pack = await fetchJson<HivePuzzle[]>(
    `hive/pack-${String(entry.pack).padStart(3, '0')}.json`,
  )
  const hive = pack.find((item) => item.id === entry.id)
  if (!hive) throw new Error(`Plástev ${entry.id} chybí v balíčku`)
  return hive
}

/* ---------- Věž ---------- */

interface TowerIndexEntry {
  id: string
  pack: number
  difficulty: Difficulty
  top: number
}

export function loadTowerIndex(): Promise<{ towers: TowerIndexEntry[] }> {
  return fetchJson('tower/index.json')
}

export async function loadTower(entry: TowerIndexEntry): Promise<TowerPuzzle> {
  const pack = await fetchJson<TowerPuzzle[]>(
    `tower/pack-${String(entry.pack).padStart(3, '0')}.json`,
  )
  const tower = pack.find((item) => item.id === entry.id)
  if (!tower) throw new Error(`Věž ${entry.id} chybí v balíčku`)
  return tower
}

/* ---------- Šibenice ---------- */

/* Slova jsou krátká a je jich jen pár tisíc, takže se vejdou do jednoho
   souboru — dělit je na balíčky by bylo zbytečné. */
export function loadGallows(): Promise<GallowsPuzzle[]> {
  return fetchJson<GallowsPuzzle[]>('gallows/puzzles.json')
}

/* ---------- Detektiv ---------- */

/* Hádanek je pár set a nesou navíc jen krátký text, takže jeden soubor stačí. */
export function loadDetective(): Promise<DetectivePuzzle[]> {
  return fetchJson<DetectivePuzzle[]>('detective/puzzles.json')
}

/* ---------- Vetřelec ---------- */

/* Pětic je pár set a nesou jen slova a klíč — jeden soubor stačí. */
export function loadIntruder(): Promise<IntruderPuzzle[]> {
  return fetchJson<IntruderPuzzle[]>('intruder/puzzles.json')
}

/* ---------- Citát ---------- */

/* Přes dva tisíce výroků v jednom souboru — pořád méně než balíček Otázky
   dne a stahuje se až při prvním spuštění režimu. */
export function loadQuotes(): Promise<Quote[]> {
  return fetchJson<Quote[]>('quotes/deck.json')
}

/* ---------- Slabikový tetris ---------- */

/* Jeden balíček pro celou hru: slabiky k rozdávání a seznam všech slov,
   která z nich jdou složit. Hádanky tenhle režim nemá — padá náhodně. */
export function loadTetris(): Promise<TetrisDeck> {
  return fetchJson<TetrisDeck>('tetris/deck.json')
}

/* ---------- Otázka dne ---------- */

/**
 * Balík otázek se načítá **až když na něj dojde**, tedy jednou denně.
 * Je to největší datový soubor ve hře a v ostatních režimech není k ničemu.
 */
export function loadQuiz(): Promise<QuizDeck> {
  return fetchJson<QuizDeck>('quiz/deck.json')
}

/* ---------- Výběr hádanky ---------- */

/**
 * Vybere hádanku, kterou hráč ještě nehrál. Když dojdou, cyklus se restartuje
 * — nikdy se nestane, že by nebylo co hrát.
 */
export function pickUnseen<T>(
  items: readonly T[],
  idOf: (item: T) => string,
  seen: readonly string[],
  random: () => number,
): T {
  const seenSet = new Set(seen)
  const fresh = items.filter((item) => !seenSet.has(idOf(item)))
  const pool = fresh.length > 0 ? fresh : items
  return pool[Math.floor(random() * pool.length)]!
}
