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
import {
  createGallowsState,
  GALLOWS_LIVES,
  guessLetter,
  isLost,
  isOver,
  isWon,
  revealed,
  takeGallowsHint,
  wrongCount,
  type GallowsPuzzle,
} from '../src/game/gallows'
import {
  createDetectiveState,
  guessLetter as detectiveLetter,
  guessWord,
  isOver as detectiveOver,
  isWon as detectiveWon,
  missCount as detectiveMisses,
  revealed as detectiveRevealed,
  type DetectivePuzzle,
} from '../src/game/detective'
import { fold, letterMask, normalizeInput, signature } from '../src/lib/czech'
import { mulberry32, shuffled } from '../src/lib/rng'
// Hodnost v plástvi (rankFor z game/hive) a hodnost profilu jsou dvě různé
// věci se stejným jménem — v testu se proto rozlišují předponou.
import { RANKS as PROFILE_RANKS, rankFor as profileRankFor } from '../src/game/ranks'
import { AWARDS, AWARD_GROUPS } from '../src/game/awards'
import { scoreChain, scoreDetective, scoreGallows, streakMultiplier } from '../src/game/scoring'
import {
  canDrop,
  createTetrisState,
  dropSyllable,
  isOver as tetrisOver,
  placed as tetrisPlaced,
  scoringColumns,
  tray,
  takeTetrisHint,
  TETRIS_HINT_COST,
  type TetrisPuzzle,
} from '../src/game/tetris'
import type { RoundResult } from '../src/game/types'
import { awardInk, DAILY_INK, inkPrice, rankInk } from '../src/game/economy'
import {
  emptyProfile,
  grantAwards,
  recordRound,
  spendInk,
  type Profile,
} from '../src/lib/storage'

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

})

describe('hodnosti', () => {
  it('má padesát stupňů, které jdou vzestupně', () => {
    expect(PROFILE_RANKS).toHaveLength(50)
    for (let i = 1; i < PROFILE_RANKS.length; i++) {
      expect(PROFILE_RANKS[i]!.at).toBeGreaterThan(PROFILE_RANKS[i - 1]!.at)
    }
  })

  it('zařadí hráče podle XP', () => {
    expect(profileRankFor(0).rank.index).toBe(1)
    expect(profileRankFor(PROFILE_RANKS[1]!.at).rank.index).toBe(2)
    expect(profileRankFor(PROFILE_RANKS[1]!.at - 1).rank.index).toBe(1)
    expect(profileRankFor(99_000_000).rank.index).toBe(50)
  })

  it('jména hodností se neopakují', () => {
    expect(new Set(PROFILE_RANKS.map((r) => r.name)).size).toBe(PROFILE_RANKS.length)
  })

  it('na vrcholu žebříčku už nikam neukazuje', () => {
    const top = profileRankFor(99_000_000)
    expect(top.next).toBeNull()
    expect(top.span).toBe(0)
  })

  it('zbytek do další hodnosti sedí na práh', () => {
    const progress = profileRankFor(PROFILE_RANKS[3]!.at + 100)
    expect(progress.rank.index).toBe(4)
    expect(progress.into).toBe(100)
    expect(progress.span).toBe(PROFILE_RANKS[4]!.at - PROFILE_RANKS[3]!.at)
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

describe('ocenění', () => {
  const round = (over: Partial<RoundResult> = {}): RoundResult => ({
    mode: 'chain',
    difficulty: 'normal',
    puzzleId: 'p1',
    score: 1000,
    perfect: false,
    success: true,
    elapsedMs: 120_000,
    hintsUsed: 0,
    detail: {},
    ...over,
  })

  it('klíče ocenění jsou jedinečné', () => {
    expect(AWARDS.length).toBeGreaterThanOrEqual(30)
    expect(new Set(AWARDS.map((a) => a.id)).size).toBe(AWARDS.length)
  })

  // Každá hra musí mít v každé skupině, kde to dává smysl, aspoň jednu metu —
  // jinak by nový režim vypadal jako přílepek.
  it('každá hra má první krok i metu bez nápovědy', () => {
    for (const mode of ['chain', 'hive', 'tower', 'gallows']) {
      expect(AWARDS.some((a) => a.group === 'start' && a.tone === mode)).toBe(true)
      expect(AWARDS.some((a) => a.group === 'clean' && a.tone === mode)).toBe(true)
    }
  })

  it('každé ocenění patří do některé skupiny a má kresbu', () => {
    for (const award of AWARDS) {
      expect(AWARD_GROUPS).toContain(award.group)
      expect(award.art).not.toBe('')
      expect(award.goal.length).toBeGreaterThan(5)
    }
  })

  // Za sezení u hry se nemá dávat skoro nic — mety mají být za to, že hráč
  // hraje sám, nebo že nasbírá body.
  it('většina met stojí na dovednosti nebo bodech, ne na počtu kol', () => {
    const skill = AWARDS.filter((a) => a.group === 'clean' || a.group === 'score')
    expect(skill.length).toBeGreaterThan(AWARDS.length / 2)
  })

  it('čerstvý profil nemá zadarmo ani jedno', () => {
    expect(Object.keys(grantAwards(emptyProfile()).awards)).toEqual([])
  })

  it('první dohrané kolo odemkne, co na něj padne', () => {
    const after = recordRound(emptyProfile(), round(), '2026-01-01')
    expect(after.awards['prvni-retez']).toBeDefined()
    expect(after.awards['cisto-1']).toBeDefined()
    // Cizí režim se nechytí — kolo Řetězu není kolo Věže.
    expect(after.awards['prvni-vez']).toBeUndefined()
  })

  it('kolo s nápovědou se do čistých nepočítá a řadu zlomí', () => {
    let profile = recordRound(emptyProfile(), round(), '2026-01-01')
    profile = recordRound(profile, round({ puzzleId: 'p2' }), '2026-01-02')
    expect(profile.counters.noHintStreak).toBe(2)
    profile = recordRound(profile, round({ puzzleId: 'p3', hintsUsed: 1 }), '2026-01-03')
    expect(profile.counters.noHint).toBe(2)
    expect(profile.counters.noHintStreak).toBe(0)
    expect(profile.counters.bestNoHintStreak).toBe(2)
  })

  it('pět čistých v řadě odemkne metu, roztroušená ne', () => {
    let profile = emptyProfile()
    for (let i = 0; i < 4; i++) {
      profile = recordRound(profile, round({ puzzleId: `a${i}` }), '2026-01-01')
      profile = recordRound(profile, round({ puzzleId: `b${i}`, hintsUsed: 2 }), '2026-01-01')
    }
    expect(profile.counters.noHint).toBe(4)
    expect(profile.awards['cisto-v-rade']).toBeUndefined()
    for (let i = 0; i < 5; i++) {
      profile = recordRound(profile, round({ puzzleId: `c${i}` }), '2026-01-02')
    }
    expect(profile.awards['cisto-v-rade']).toBeDefined()
  })

  it('rychlík se počítá jen bez nápovědy', () => {
    const fast = (hintsUsed: number, puzzleId: string) =>
      round({ hintsUsed, puzzleId, elapsedMs: 30_000 })
    let profile = recordRound(emptyProfile(), fast(3, 'p1'), '2026-01-01')
    expect(profile.counters.chainFastMs).toBe(0)
    expect(profile.awards['retez-rychlik']).toBeUndefined()
    profile = recordRound(profile, fast(0, 'p2'), '2026-01-02')
    expect(profile.counters.chainFastMs).toBe(30_000)
    expect(profile.awards['retez-rychlik']).toBeDefined()
  })

  it('pangramy se sčítají přes kola', () => {
    const hive = (pangrams: number, puzzleId: string) =>
      round({ mode: 'hive', puzzleId, detail: { found: 10, total: 30, pangrams, rankTop: 0 } })
    let profile = recordRound(emptyProfile(), hive(1, 'h1'), '2026-01-01')
    profile = recordRound(profile, hive(2, 'h2'), '2026-01-02')
    expect(profile.counters.pangrams).toBe(3)
    expect(profile.awards['pangram-1']).toBeDefined()
    expect(profile.awards['pangram-10']).toBeUndefined()
  })

  it('věž bez lešení musí být dostavěná i bez nápovědy', () => {
    const tower = (full: number, hintsUsed: number, puzzleId: string) =>
      round({ mode: 'tower', hintsUsed, puzzleId, detail: { floors: 2, top: 5, full } })
    let profile = recordRound(emptyProfile(), tower(1, 2, 't1'), '2026-01-01')
    expect(profile.counters.towerFullNoHint).toBe(0)
    profile = recordRound(profile, tower(0, 0, 't2'), '2026-01-02')
    expect(profile.counters.towerFullNoHint).toBe(0)
    profile = recordRound(profile, tower(1, 0, 't3'), '2026-01-03')
    expect(profile.counters.towerFullNoHint).toBe(1)
    expect(profile.awards['vez-cista']).toBeDefined()
  })

  it('denní výzva se počítá, jen když se o ni hraje', () => {
    let profile = recordRound(emptyProfile(), round(), '2026-01-01', false)
    expect(profile.counters.dailies).toBe(0)
    profile = recordRound(profile, round({ puzzleId: 'p2' }), '2026-01-02', true)
    expect(profile.counters.dailies).toBe(1)
  })

  it('získané ocenění se podruhé nepřepíše ani neztratí', () => {
    const first = recordRound(emptyProfile(), round(), '2026-01-01')
    const when = first.awards['prvni-retez']!
    const again = grantAwards(recordRound(first, round({ puzzleId: 'p2' }), '2026-01-02'), when + 999)
    expect(again.awards['prvni-retez']).toBe(when)
  })

  it('ukazatel postupu roste od nuly k jedné', () => {
    const award = AWARDS.find((a) => a.id === 'cisto-50')!
    const empty = emptyProfile()
    expect(award.progress!(empty)).toBe(0)
    const half = { ...empty, counters: { ...empty.counters, noHint: 25 } }
    expect(award.progress!(half)).toBeCloseTo(0.5)
    const over = { ...empty, counters: { ...empty.counters, noHint: 500 } }
    expect(award.progress!(over)).toBe(1)
  })
})

describe('slabikový tetris', () => {
  const puzzle: TetrisPuzzle = {
    id: 't-test',
    difficulty: 'normal',
    cols: 4,
    rows: 4,
    queue: ['ko', 'lo', 'vo', 'da'],
    words: ['kolo', 'voda', 'kova'],
    seed: ['kolo', 'voda'],
  }

  it('dvě slabiky vedle sebe složí slovo a zmizí', () => {
    let state = createTetrisState(puzzle)
    state = dropSyllable(state, 0)!.state
    const hit = dropSyllable(state, 1)!
    expect(hit.words).toEqual(['kolo'])
    expect(tetrisPlaced(hit.state)).toBe(0)
  })

  it('svisle se čte zdola nahoru — tím směrem sloupec roste', () => {
    let state = createTetrisState(puzzle)
    state = dropSyllable(state, 0)!.state
    // „lo" do vzdáleného sloupce, aby nevzniklo vodorovné „kolo".
    state = dropSyllable(state, 2)!.state
    // Teď „vo" nad „ko": zdola nahoru je to „kovo", což slovo není.
    const miss = dropSyllable(state, 0)!
    expect(miss.words).toEqual([])
  })

  // Zásobník je to, co dělá hru hrou: bez volby by slabika, která se zrovna
  // nehodí, zůstala ležet navždycky.
  it('hráč si vybírá ze tří slabik v zásobníku', () => {
    const state = createTetrisState(puzzle)
    expect(tray(state)).toEqual(['ko', 'lo', 'vo'])
    // Druhá slabika ze zásobníku; první zůstává ve frontě.
    const after = dropSyllable(state, 0, 1)!.state
    expect(tray(after)).toEqual(['ko', 'vo', 'da'])
    expect(after.queue.length).toBe(3)
  })

  it('do zásobníku se sahá jen na první tři slabiky', () => {
    const state = createTetrisState(puzzle)
    expect(dropSyllable(state, 0, 3)).toBeNull()
  })

  it('slabika, která nic nesloží, prostě zůstane ležet', () => {
    const state = createTetrisState(puzzle)
    const result = dropSyllable(state, 0)!
    expect(result.words).toEqual([])
    expect(tetrisPlaced(result.state)).toBe(1)
  })

  // Zásadní pojistka: co hra uzná, musí být v předpočítaném seznamu dávky.
  // Runtime nemá jak vymyslet slovo, které by ve slovníku nebylo.
  it('uzná jen slovo ze seznamu dávky', () => {
    const strict: TetrisPuzzle = { ...puzzle, words: ['voda'] }
    let state = createTetrisState(strict)
    state = dropSyllable(state, 0)!.state
    const result = dropSyllable(state, 1)!
    expect(result.words).toEqual([])
    expect(tetrisPlaced(result.state)).toBe(2)
  })

  it('plný sloupec už nepřijme', () => {
    const narrow: TetrisPuzzle = {
      ...puzzle,
      cols: 1,
      rows: 2,
      queue: ['ko', 'ko', 'ko'],
      words: [],
    }
    let state = createTetrisState(narrow)
    state = dropSyllable(state, 0)!.state
    state = dropSyllable(state, 0)!.state
    expect(canDrop(state, 0)).toBe(false)
    expect(dropSyllable(state, 0)).toBeNull()
    expect(tetrisOver(state)).toBe(true)
  })

  it('nápověda ukáže sloupec, kde se něco složí', () => {
    let state = createTetrisState(puzzle)
    state = dropSyllable(state, 0)!.state
    // Po „ko" ve sloupci 0 složí „lo" slovo hned dvakrát: vedle (vodorovně)
    // i na něj (svisle zdola nahoru).
    expect(scoringColumns(state)).toEqual([0, 1])
    const hint = takeTetrisHint(state, 'column', false)!
    expect(scoringColumns(state)).toContain(hint.column)
    expect(hint.state.hintCost).toBe(TETRIS_HINT_COST.column)
  })

  it('nápověda zaplacená inkoustem nestojí body, ale pořád je to nápověda', () => {
    const state = createTetrisState(puzzle)
    const hint = takeTetrisHint(state, 'swap', true)!
    expect(hint.state.hintCost).toBe(0)
    expect(hint.state.hintsUsed).toBe(1)
    expect(hint.state.freeHints).toBe(1)
  })
})

describe('nápovědy zdarma', () => {
  const puzzle: ChainPuzzle = {
    id: 'test',
    start: 'kosa',
    target: 'mísa',
    par: 3,
    difficulty: 'normal',
  }
  const graph = buildChainGraph(['kosa', 'koza', 'kasa', 'masa', 'mísa'])

  const round = (over: Partial<RoundResult> = {}): RoundResult => ({
    mode: 'chain',
    difficulty: 'normal',
    puzzleId: 'p1',
    score: 1000,
    perfect: false,
    success: true,
    elapsedMs: 120_000,
    hintsUsed: 0,
    detail: {},
    ...over,
  })

  it('nová hra začíná s trochou inkoustu na uvítanou', () => {
    expect(emptyProfile().ink).toBeGreaterThan(0)
  })

  // Kvůli tomuhle vznikla měna: dřív stálo odhalení celého slova stejně jako
  // napovězení vzdálenosti, takže se peněženka utrácela nejdražší nápovědou
  // a nic to nestálo.
  it('velká nápověda stojí výrazně víc než malá', () => {
    expect(inkPrice(HINT_COST.word)).toBeGreaterThanOrEqual(inkPrice(HINT_COST.distance) * 3)
    expect(inkPrice(50)).toBe(5)
    expect(inkPrice(200)).toBe(20)
  })

  it('nápověda za inkoust nestojí body, ale pořád se počítá jako nápověda', () => {
    const state = takeHint(graph, createChainState(puzzle), 'word', true)!.state
    expect(state.hintCost).toBe(0)
    expect(state.hintsUsed).toBe(1)
    expect(state.freeHints).toBe(1)
  })

  it('placená nápověda peněženku neošidí', () => {
    const state = takeHint(graph, createChainState(puzzle), 'word', false)!.state
    expect(state.hintCost).toBe(HINT_COST.word)
    expect(state.freeHints).toBe(0)
  })

  // Za inkoust se nesmí dát koupit meta „bez nápovědy" — jinak by stačilo si
  // ho nasbírat a mety si jím odemknout.
  it('kolo s nápovědou za inkoust není kolo bez nápovědy', () => {
    const after = recordRound(emptyProfile(), round({ hintsUsed: 1 }), '2026-01-01')
    expect(after.counters.noHint).toBe(0)
    expect(after.awards['cisto-1']).toBeUndefined()
  })

  it('bodování počítá jen zaplacené nápovědy', () => {
    let state = createChainState(puzzle)
    state = takeHint(graph, state, 'word', true)!.state
    const free = scoreChain(state, 1, state.startedAt + 10_000)
    expect(free.lines.some((line) => line.label.startsWith('Nápovědy'))).toBe(false)
    expect(free.lines.find((line) => line.label.startsWith('Nevyužité'))?.label).toContain('3')
  })

  it('utrácení nikdy nespadne pod nulu', () => {
    const empty = { ...emptyProfile(), ink: 0 }
    expect(spendInk(empty, 20).ink).toBe(0)
    expect(spendInk({ ...empty, ink: 25 }, 20).ink).toBe(5)
    // Na co hráč nemá, to se neutratí ani zčásti.
    expect(spendInk({ ...empty, ink: 5 }, 20).ink).toBe(5)
  })

  it('nová hodnost i ocenění sypou inkoust, ale každé jen jednou', () => {
    const start = emptyProfile()
    const after = recordRound(start, round({ score: 20_000 }), '2026-01-01')
    expect(after.ink).toBeGreaterThan(start.ink)
    // Druhý průchod týchž podmínek už nic nepřipíše.
    expect(grantAwards(after).ink).toBe(after.ink)
  })

  // Skok přes několik hodností naráz musí zaplatit každou z nich, ne jen tu
  // poslední — a každou její vlastní sazbou.
  it('skok přes víc hodností zaplatí každou zvlášť', () => {
    const start = emptyProfile()
    const after = recordRound(start, round({ score: PROFILE_RANKS[3]!.at }), '2026-01-01')
    const ranks = rankInk(2) + rankInk(3) + rankInk(4)
    const awards = AWARDS.filter((award) => after.awards[award.id] !== undefined)
      .reduce((sum, award) => sum + awardInk(award), 0)
    expect(after.ink).toBe(start.ink + ranks + awards)
  })

  // Kvůli tomuhle se hodnosti přepracovaly: hráč hlásil, že mu naskakují
  // jedna za druhou. První tři smí odsýpat, dál se musí výrazně natahovat.
  it('hodnosti po třetí výrazně zpomalí', () => {
    const gap = (i: number) => PROFILE_RANKS[i]!.at - PROFILE_RANKS[i - 1]!.at
    // Prvních pár kol dá hned tři hodnosti.
    expect(PROFILE_RANKS[3]!.at).toBeLessThanOrEqual(6_000)
    // Od té chvíle každý další stupeň stojí víc než ten předchozí.
    for (let i = 4; i < PROFILE_RANKS.length; i += 1) {
      expect(gap(i)).toBeGreaterThan(gap(i - 1))
    }
    // Nejvyšší hodnost je běh na roky, ne na měsíc.
    expect(PROFILE_RANKS[PROFILE_RANKS.length - 1]!.at).toBeGreaterThan(10_000_000)
  })

  // Šest režimů krát odměna denně by peněženku zaplavilo rychleji než všechno
  // ostatní; padne proto až za kompletní denní várku.
  it('inkoust padne až za všechny denní výzvy dne', () => {
    const day = '2026-01-01'
    // Porovnává se proti témuž kolu mimo denní výzvu — jinak by do rozdílu
    // spadl i inkoust za ocenění, která tím kolem shodou okolností padla.
    const start = emptyProfile()
    expect(recordRound(start, round(), day, true).ink).toBe(
      recordRound(start, round(), day, false).ink,
    )

    const almost: Profile = {
      ...start,
      dailyDone: {
        [`${day}:hive`]: 1,
        [`${day}:tower`]: 1,
        [`${day}:gallows`]: 1,
        [`${day}:detective`]: 1,
        [`${day}:tetris`]: 1,
      },
    }
    expect(
      recordRound(almost, round(), day, true).ink -
        recordRound(almost, round(), day, false).ink,
    ).toBe(DAILY_INK)
  })

  // Přesně to, co hráč nahlásil: dostal metu „bez nápovědy" za kolo, které
  // prohrál. Neúspěšné kolo se za čisté počítat nesmí.
  it('prohrané kolo se za čisté nepočítá, i když v něm nebyla nápověda', () => {
    const lost = recordRound(emptyProfile(), round({ mode: 'gallows', success: false }), '2026-01-01')
    expect(lost.counters.noHint).toBe(0)
    expect(lost.counters.noHintStreak).toBe(0)
    expect(lost.awards['cisto-1']).toBeUndefined()

    const won = recordRound(emptyProfile(), round({ mode: 'gallows', success: true }), '2026-01-01')
    expect(won.counters.noHint).toBe(1)
    expect(won.awards['cisto-1']).toBeDefined()
  })

  it('nedotažená plástev taky není čisté kolo', () => {
    const quit = recordRound(
      emptyProfile(),
      round({ mode: 'hive', success: false, detail: { found: 3, total: 40 } }),
      '2026-01-01',
    )
    expect(quit.counters.noHint).toBe(0)
  })
})

describe('šibenice', () => {
  const puzzle: GallowsPuzzle = { id: 'g-1', word: 'kůň', difficulty: 'normal' }
  // „protože" má dvakrát o — nápověda „odhal písmeno" má sáhnout právě po něm.
  const long: GallowsPuzzle = { id: 'g-2', word: 'protože', difficulty: 'hard' }

  it('písmeno bez diakritiky odhalí i tvar s háčkem a kroužkem', () => {
    let state = createGallowsState(puzzle)
    for (const letter of ['k', 'u', 'n']) {
      const result = guessLetter(state, letter)
      expect(result.ok).toBe(true)
      if (!result.ok) return
      expect(result.hit).toBe(true)
      state = result.state
    }
    expect(revealed(state)).toEqual(['k', 'ů', 'ň'])
    expect(isWon(state)).toBe(true)
  })

  it('chybné písmeno ubere život, správné ne', () => {
    const miss = guessLetter(createGallowsState(long), 'x')
    expect(miss.ok).toBe(true)
    if (!miss.ok) return
    expect(miss.hit).toBe(false)
    expect(wrongCount(miss.state)).toBe(1)

    const hit = guessLetter(miss.state, 'o')
    expect(hit.ok).toBe(true)
    if (!hit.ok) return
    expect(hit.hit).toBe(true)
    expect(wrongCount(hit.state)).toBe(1)
  })

  it('osm chyb kolo ukončí a slovo se prohraje', () => {
    let state = createGallowsState(puzzle)
    for (const letter of 'bcfgjmr') {
      const result = guessLetter(state, letter)
      expect(result.ok).toBe(true)
      if (result.ok) state = result.state
    }
    expect(isLost(state)).toBe(false)
    const last = guessLetter(state, 'x')
    expect(last.ok).toBe(true)
    if (!last.ok) return
    expect(wrongCount(last.state)).toBe(GALLOWS_LIVES)
    expect(isLost(last.state)).toBe(true)
    expect(isOver(last.state)).toBe(true)
    // Po konci už se nehádá dál.
    expect(guessLetter(last.state, 'z')).toMatchObject({ ok: false, error: 'over' })
  })

  it('stejné písmeno podruhé neprojde', () => {
    const first = guessLetter(createGallowsState(puzzle), 'k')
    expect(first.ok).toBe(true)
    if (!first.ok) return
    expect(guessLetter(first.state, 'k')).toMatchObject({ ok: false, error: 'used' })
  })

  it('„vyškrtni" odstraní jen písmena, která ve slově nejsou', () => {
    const result = takeGallowsHint(createGallowsState(long), 'strike')
    expect(result).not.toBeNull()
    if (!result) return
    const base = fold(long.word)
    for (const letter of result.letters) expect(base).not.toContain(letter)
    // Vyškrtnutí nestojí život — je to nákup, ne tah.
    expect(wrongCount(result.state)).toBe(0)
    expect(result.state.hintsUsed).toBe(1)
  })

  it('„odhal písmeno" ukáže to nejčastější a nestojí život', () => {
    const result = takeGallowsHint(createGallowsState(long), 'letter')
    expect(result).not.toBeNull()
    if (!result) return
    expect(result.letters).toEqual(['o'])
    expect(wrongCount(result.state)).toBe(0)
  })

  it('nápověda zdarma nestojí body, ale počítá se jako nápověda', () => {
    const free = takeGallowsHint(createGallowsState(long), 'letter', true)!
    expect(free.state.hintCost).toBe(0)
    expect(free.state.hintsUsed).toBe(1)
    expect(free.state.freeHints).toBe(1)
  })

  it('bodování odmění zbylé životy a prohru netrestá nulou', () => {
    let state = createGallowsState(puzzle)
    for (const letter of ['k', 'u', 'n']) {
      const result = guessLetter(state, letter)
      if (result.ok) state = result.state
    }
    const won = scoreGallows(state, 1, state.startedAt + 20_000)
    expect(won.perfect).toBe(true)
    expect(won.total).toBeGreaterThan(900)

    let dead = createGallowsState(puzzle)
    for (const letter of 'bcfgjmrx') {
      const result = guessLetter(dead, letter)
      if (result.ok) dead = result.state
    }
    const lost = scoreGallows(dead, 1, dead.startedAt + 20_000)
    expect(lost.perfect).toBe(false)
    expect(lost.total).toBeGreaterThanOrEqual(0)
    expect(lost.total).toBeLessThan(won.total)
  })
})

describe('detektiv', () => {
  const puzzle: DetectivePuzzle = {
    id: 'd-1',
    word: 'kostel',
    clue: 'Z latinského castellum, zdrobněliny slova castrum.',
    difficulty: 'normal',
  }

  it('chybné písmeno kolo neukončí, jen se počítá', () => {
    const miss = detectiveLetter(createDetectiveState(puzzle), 'x')
    expect(miss.ok).toBe(true)
    if (!miss.ok) return
    expect(miss.hit).toBe(false)
    expect(detectiveMisses(miss.state)).toBe(1)
    expect(detectiveOver(miss.state)).toBe(false)
  })

  it('slovo se dá tipnout celé, i bez diakritiky', () => {
    const kun: DetectivePuzzle = { ...puzzle, word: 'kůň' }
    const hit = guessWord(createDetectiveState(kun), 'kun')
    expect(hit.ok && hit.correct).toBe(true)
    if (!hit.ok) return
    expect(detectiveWon(hit.state)).toBe(true)
    expect(detectiveRevealed(hit.state)).toEqual(['k', 'ů', 'ň'])
  })

  it('chybný tip se zapamatuje a podruhé neprojde', () => {
    const first = guessWord(createDetectiveState(puzzle), 'hrad')
    expect(first.ok).toBe(true)
    if (!first.ok) return
    expect(first.correct).toBe(false)
    expect(first.state.guesses).toEqual(['hrad'])
    expect(guessWord(first.state, 'hrad')).toMatchObject({ ok: false, error: 'repeat' })
  })

  it('dvanáct písmen vedle případ uzavře jako nevyřešený', () => {
    let state = createDetectiveState(puzzle)
    for (const letter of 'abdfghijmpqru') {
      const result = detectiveLetter(state, letter)
      if (result.ok) state = result.state
    }
    expect(detectiveMisses(state)).toBeGreaterThanOrEqual(12)
    expect(detectiveOver(state)).toBe(true)
    expect(detectiveWon(state)).toBe(false)
  })

  it('odhalení všech písmen je taky výhra', () => {
    let state = createDetectiveState(puzzle)
    for (const letter of ['k', 'o', 's', 't', 'e', 'l']) {
      const result = detectiveLetter(state, letter)
      if (result.ok) state = result.state
    }
    expect(detectiveWon(state)).toBe(true)
    expect(detectiveOver(state)).toBe(true)
  })

  it('tip zavčas dá víc bodů než doklikání po písmenech', () => {
    const early = guessWord(createDetectiveState(puzzle), 'kostel')
    expect(early.ok).toBe(true)
    if (!early.ok) return

    let slow = createDetectiveState(puzzle)
    for (const letter of ['k', 'o', 's', 't', 'e', 'l']) {
      const result = detectiveLetter(slow, letter)
      if (result.ok) slow = result.state
    }
    const fast = scoreDetective(early.state, 1, early.state.startedAt + 10_000)
    const plodding = scoreDetective(slow, 1, slow.startedAt + 10_000)
    expect(fast.total).toBeGreaterThan(plodding.total)
    expect(fast.perfect).toBe(true)
  })
})
