import { describe, expect, it } from 'vitest'

import {
  buildChainGraph,
  bfsDistances,
  createChainState,
  hammingDistance,
  HINT_COST,
  playMove,
  remainingDistance,
  shortestPath,
  takeHint,
  undoMove,
  type ChainPuzzle,
} from '../src/game/chain'
import {
  createHiveState,
  currentScore,
  rankFor,
  submitWord,
  wordScore,
  type HivePuzzle,
} from '../src/game/hive'
import {
  createTowerState,
  currentLevel,
  isFinished,
  submitLevel,
  takeTowerHint,
  type TowerPuzzle,
} from '../src/game/tower'
import { fold, letterMask, normalizeInput, signature } from '../src/lib/czech'
import { mulberry32, shuffled } from '../src/lib/rng'
import { levelFor, scoreChain, streakMultiplier } from '../src/game/scoring'

describe('české utility', () => {
  it('skládá diakritiku', () => {
    expect(fold('příliš žluťoučký')).toBe('prilis zlutoucky')
    expect(fold('ěščřžýáíé')).toBe('escrzyaie')
  })

  it('počítá masku různých písmen ze složeného tvaru', () => {
    expect(letterMask('kůň')).toBe(letterMask('kun'))
    expect(letterMask('aaa')).toBe(1)
  })

  it('podpis je setříděná písmena včetně diakritiky', () => {
    expect(signature('pila')).toBe(signature('lipa'))
    expect(signature('kočí')).toBe('koíč')
    // Diakritika se v podpisu zachovává — „pila" a „píla" nejsou přesmyčky.
    expect(signature('pila')).not.toBe(signature('píla'))
  })

  it('očistí vstup hráče', () => {
    expect(normalizeInput('  Ko Sa! ')).toBe('kosa')
    expect(normalizeInput('a-b-c')).toBe('abc')
  })
})

describe('řetěz — graf', () => {
  const words = ['kosa', 'koza', 'kosí', 'kasa', 'masa', 'mísa', 'míra', 'kůra']
  const graph = buildChainGraph(words)

  it('spojí slova lišící se jedním písmenem', () => {
    const neighbours = graph.adj[graph.index.get('kosa')!]!.map((i) => words[i])
    expect(neighbours.sort()).toEqual(['kasa', 'kosí', 'koza'])
  })

  it('nespojí slovo samo se sebou ani slova na vzdálenost 2', () => {
    const neighbours = graph.adj[graph.index.get('kosa')!]!.map((i) => words[i])
    expect(neighbours).not.toContain('kosa')
    expect(neighbours).not.toContain('masa')
  })

  it('BFS měří vzdálenosti a označí nedosažitelné', () => {
    const dist = bfsDistances(graph, graph.index.get('kosa')!)
    expect(dist[graph.index.get('kasa')!]).toBe(1)
    expect(dist[graph.index.get('masa')!]).toBe(2)
    expect(dist[graph.index.get('kůra')!]).toBe(-1)
  })

  it('najde nejkratší cestu a umí se vyhnout zakázaným slovům', () => {
    const from = graph.index.get('kosa')!
    const to = graph.index.get('mísa')!
    const path = shortestPath(graph, from, to)!.map((i) => words[i])
    expect(path).toEqual(['kosa', 'kasa', 'masa', 'mísa'])

    const blocked = new Set([graph.index.get('masa')!])
    expect(shortestPath(graph, from, to, blocked)).toBeNull()
  })

  it('hammingova vzdálenost', () => {
    expect(hammingDistance('kosa', 'koza')).toBe(1)
    expect(hammingDistance('kosa', 'míra')).toBe(3)
  })
})

describe('řetěz — pravidla tahu', () => {
  const words = ['kosa', 'koza', 'kasa', 'masa', 'mísa', 'mísy', 'kosy']
  const graph = buildChainGraph(words)
  const puzzle: ChainPuzzle = {
    id: 'test',
    start: 'kosa',
    target: 'mísa',
    par: 3,
    difficulty: 'normal',
  }

  it('odmítne špatnou délku, nulovou i dvojnásobnou změnu', () => {
    const state = createChainState(puzzle)
    expect(playMove(graph, state, 'kos')).toMatchObject({ ok: false, error: 'length' })
    expect(playMove(graph, state, 'kosa')).toMatchObject({ ok: false, error: 'no-change' })
    expect(playMove(graph, state, 'mísa')).toMatchObject({
      ok: false,
      error: 'not-one-letter',
    })
  })

  it('odmítne slovo mimo slovník', () => {
    const state = createChainState(puzzle)
    expect(playMove(graph, state, 'kola')).toMatchObject({
      ok: false,
      error: 'unknown-word',
    })
  })

  it('odmítne slovo, které už v řetězu je', () => {
    const first = playMove(graph, createChainState(puzzle), 'kasa')
    expect(first.ok).toBe(true)
    if (!first.ok) return
    const back = playMove(graph, first.state, 'kosa')
    expect(back).toMatchObject({ ok: false, error: 'already-used' })
  })

  it('přijme platný tah a spočítá zbývající vzdálenost', () => {
    const move = playMove(graph, createChainState(puzzle), 'kasa')
    expect(move.ok).toBe(true)
    if (!move.ok) return
    expect(move.remaining).toBe(2)
    expect(move.warning).toBeNull()
    expect(move.solved).toBe(false)
  })

  it('pozná vyřešení', () => {
    let state = createChainState(puzzle)
    for (const word of ['kasa', 'masa', 'mísa']) {
      const move = playMove(graph, state, word)
      expect(move.ok).toBe(true)
      if (!move.ok) return
      state = move.state
    }
    expect(state.finishedAt).not.toBeNull()
    expect(state.path).toEqual(['kosa', 'kasa', 'masa', 'mísa'])
  })

  it('strážce ohlásí slepou uličku vzniklou zákazem opakování', () => {
    // kosy -> kosa -> kasa -> masa -> mísa; přes kosy se hráč nikam nedostane
    const deadPuzzle: ChainPuzzle = { ...puzzle, start: 'koza', par: 4 }
    const move = playMove(graph, createChainState(deadPuzzle), 'kosa')
    expect(move.ok).toBe(true)
    if (!move.ok) return
    const trap = playMove(graph, move.state, 'kosy')
    expect(trap.ok).toBe(true)
    if (!trap.ok) return
    expect(trap.warning).toBe('dead-end')
    expect(trap.remaining).toBe(-1)
  })

  it('undo vrátí poslední tah a nikdy neodebere start', () => {
    const move = playMove(graph, createChainState(puzzle), 'kasa')
    expect(move.ok).toBe(true)
    if (!move.ok) return
    const back = undoMove(move.state)
    expect(back.path).toEqual(['kosa'])
    expect(undoMove(back).path).toEqual(['kosa'])
  })

  it('remainingDistance respektuje už použitá slova', () => {
    const state = createChainState(puzzle)
    expect(remainingDistance(graph, state)).toBe(3)
  })

  it('nápovědy vycházejí z platné optimální cesty', () => {
    const state = createChainState(puzzle)
    expect(takeHint(graph, state, 'distance')).toMatchObject({ distance: 3 })
    expect(takeHint(graph, state, 'position')).toMatchObject({ position: 1 })
    expect(takeHint(graph, state, 'word')).toMatchObject({ word: 'kasa' })
  })

  it('každý druh nápovědy stojí svoji cenu', () => {
    let state = createChainState(puzzle)
    state = takeHint(graph, state, 'distance')!.state
    expect(state.hintCost).toBe(HINT_COST.distance)
    state = takeHint(graph, state, 'word')!.state
    expect(state.hintCost).toBe(HINT_COST.distance + HINT_COST.word)
    expect(state.hintsUsed).toBe(2)
  })
})

describe('voština', () => {
  const puzzle: HivePuzzle = {
    id: 'test',
    center: 'r',
    outer: ['a', 'k', 't', 'o', 's', 'v'],
    solutions: ['kára', 'trakař', 'traktor', 'strava', 'krátká'],
    pangrams: ['trakař'],
    difficulty: 'normal',
  }

  it('boduje délku a přidá bonus za pangram', () => {
    expect(wordScore(puzzle, 'kára')).toBe(1)
    expect(wordScore(puzzle, 'strava')).toBe(6)
    expect(wordScore(puzzle, 'trakař')).toBe(6 + 7)
  })

  it('odmítne krátké slovo, chybějící střed a cizí písmeno', () => {
    const state = createHiveState(puzzle)
    expect(submitWord(state, 'kar')).toMatchObject({ error: 'too-short' })
    expect(submitWord(state, 'kosa')).toMatchObject({ error: 'missing-center' })
    expect(submitWord(state, 'brko')).toMatchObject({ error: 'foreign-letter' })
  })

  it('skládá diakritiku proti plástvi', () => {
    const state = createHiveState(puzzle)
    const result = submitWord(state, 'krátká')
    expect(result.ok).toBe(true)
  })

  it('uzná i zápis bez diakritiky — plástev háčky nenabízí', () => {
    const state = createHiveState(puzzle)
    const result = submitWord(state, 'kratka')
    expect(result.ok).toBe(true)
    if (!result.ok) return
    // Do nalezených se uloží správný český zápis, ne to, co hráč naťukal.
    expect(result.state.found).toEqual(['krátká'])
    expect(submitWord(result.state, 'krátká')).toMatchObject({
      error: 'already-found',
    })
  })

  it('pangram se pozná i bez diakritiky', () => {
    const state = createHiveState(puzzle)
    const result = submitWord(state, 'trakar')
    expect(result.ok).toBe(true)
    if (!result.ok) return
    expect(result.pangram).toBe(true)
    expect(result.points).toBe(13)
  })

  it('odmítne slovo mimo seznam řešení a duplicitu', () => {
    const state = createHiveState(puzzle)
    expect(submitWord(state, 'kraktos')).toMatchObject({ error: 'unknown-word' })
    const first = submitWord(state, 'kára')
    expect(first.ok).toBe(true)
    if (!first.ok) return
    expect(submitWord(first.state, 'kára')).toMatchObject({ error: 'already-found' })
  })

  it('sčítá skóre a posouvá hodnost', () => {
    let state = createHiveState(puzzle)
    for (const word of ['kára', 'strava', 'trakař']) {
      const result = submitWord(state, word)
      expect(result.ok).toBe(true)
      if (!result.ok) return
      state = result.state
    }
    expect(currentScore(state)).toBe(1 + 6 + 13)
    expect(rankFor(0, 100).name).toBe('Začátečník')
    expect(rankFor(100, 100).name).toBe('Královna češtiny')
  })
})

describe('věž', () => {
  const puzzle: TowerPuzzle = {
    id: 'test',
    difficulty: 'hard',
    levels: [
      { sig: signature('pal'), added: null, words: ['pal'] },
      { sig: signature('pila'), added: 'i', words: ['pila', 'lipa'] },
      { sig: signature('pařil'), added: 'ř', words: ['pařil'] },
    ],
  }

  it('začíná se základním slovem a dlaždicemi dalšího patra', () => {
    const state = createTowerState(puzzle)
    expect(state.built).toEqual(['pal'])
    expect([...state.tiles].sort().join('')).toBe(signature('pila'))
    expect(currentLevel(state)!.added).toBe('i')
  })

  it('odmítne slovo z jiných písmen', () => {
    const state = createTowerState(puzzle)
    expect(submitLevel(state, 'pal')).toMatchObject({ error: 'wrong-letters' })
    expect(submitLevel(state, 'plia')).toMatchObject({ error: 'unknown-word' })
    expect(submitLevel(state, '')).toMatchObject({ error: 'empty' })
  })

  it('přijme kteroukoli přesmyčku daného patra', () => {
    const state = createTowerState(puzzle)
    const a = submitLevel(state, 'pila')
    const b = submitLevel(state, 'lipa')
    expect(a.ok).toBe(true)
    expect(b.ok).toBe(true)
    // Obě volby vedou na stejný podpis, takže věž pokračuje identicky.
    if (!a.ok || !b.ok) return
    expect(currentLevel(a.state)!.sig).toBe(currentLevel(b.state)!.sig)
  })

  it('dostaví věž a pozná konec', () => {
    let state = createTowerState(puzzle)
    for (const word of ['lipa', 'pařil']) {
      const result = submitLevel(state, word)
      expect(result.ok).toBe(true)
      if (!result.ok) return
      state = result.state
    }
    expect(isFinished(state)).toBe(true)
    expect(state.finishedAt).not.toBeNull()
    expect(currentLevel(state)).toBeNull()
  })

  it('nápověda odhaluje postupně delší prefix', () => {
    const state = createTowerState(puzzle)
    const first = takeTowerHint(state, 'letter')!
    expect(first.text).toBe('p')
    const second = takeTowerHint(first.state, 'letter')!
    expect(second.text).toBe('pi')
    expect(takeTowerHint(state, 'word')!.text).toBe('pila')
  })
})

describe('bodování', () => {
  const puzzle: ChainPuzzle = {
    id: 'x',
    start: 'kosa',
    target: 'mísa',
    par: 3,
    difficulty: 'normal',
  }

  it('perfektní kolo dostane násobitel', () => {
    const state = {
      ...createChainState(puzzle, 0),
      path: ['kosa', 'kasa', 'masa', 'mísa'],
      finishedAt: 30_000,
    }
    const score = scoreChain(state, 1, 30_000)
    expect(score.perfect).toBe(true)
    expect(score.multiplier).toBeCloseTo(1.5)
    // 1000 základ + 150 nevyužité nápovědy + 300 rychlost = 1450, ×1,5
    expect(score.total).toBe(2175)
  })

  it('tahy nad par ubírají body', () => {
    const state = {
      ...createChainState(puzzle, 0),
      path: ['kosa', 'kosy', 'kasa', 'masa', 'mísa'],
      finishedAt: 30_000,
    }
    const score = scoreChain(state, 1, 30_000)
    expect(score.perfect).toBe(false)
    expect(score.total).toBe(1350)
  })

  it('skóre nikdy nespadne pod minimum', () => {
    const state = {
      ...createChainState(puzzle, 0),
      path: ['kosa', ...Array.from({ length: 20 }, (_, i) => `x${i}`), 'mísa'],
      hintsUsed: 3,
      hintCost: 600,
      finishedAt: 600_000,
    }
    expect(scoreChain(state, 1, 600_000).total).toBe(100)
  })

  it('série má strop', () => {
    expect(streakMultiplier(1)).toBe(1)
    expect(streakMultiplier(5)).toBeCloseTo(1.2)
    expect(streakMultiplier(100)).toBe(1.5)
  })

  it('úrovně rostou plynule', () => {
    expect(levelFor(0).level).toBe(1)
    expect(levelFor(0).title).toBe('Učeň')
    expect(levelFor(2000).level).toBe(2)
    expect(levelFor(1_000_000).level).toBeGreaterThan(10)
  })
})

describe('rng', () => {
  it('je deterministický podle semínka', () => {
    const a = mulberry32(42)
    const b = mulberry32(42)
    expect([a(), a(), a()]).toEqual([b(), b(), b()])
  })

  it('míchání nemění vstup a zachová prvky', () => {
    const input = [1, 2, 3, 4, 5]
    const out = shuffled(mulberry32(7), input)
    expect(input).toEqual([1, 2, 3, 4, 5])
    expect([...out].sort()).toEqual(input)
  })
})
