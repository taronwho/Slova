/** Načítání herních dat — vše staticky, po balíčcích, s cache v paměti. */

import { buildChainGraph, type ChainGraph, type ChainPuzzle } from '../game/chain'
import type { HivePuzzle } from '../game/hive'
import type { TowerPuzzle } from '../game/tower'
import type { Difficulty } from '../game/types'

const BASE = import.meta.env.BASE_URL

const cache = new Map<string, Promise<unknown>>()

function fetchJson<T>(path: string): Promise<T> {
  const key = path
  const hit = cache.get(key)
  if (hit) return hit as Promise<T>
  const request = fetch(`${BASE}data/${path}`).then((response) => {
    if (!response.ok) throw new Error(`Nepodařilo se načíst ${path}`)
    return response.json() as Promise<T>
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
