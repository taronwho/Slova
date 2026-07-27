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
import { AWARDS, AWARD_GROUPS, visibleAwards } from '../src/game/awards'
import {
  buyClues,
  createQuizState,
  guess as quizGuess,
  matches as quizMatches,
  QUIZ_CONSOLATIONS,
  QUIZ_REWARD,
  QUIZ_TOPICS,
  QUIZ_TRIES,
  quizCycle,
  quizFor,
  quizReward,
  revealClue,
  type QuizDeck,
  type QuizQuestion,
} from '../src/game/quiz'
import {
  scoreChain,
  scoreDetective,
  scoreGallows,
  scoreTetris,
  streakMultiplier,
} from '../src/game/scoring'
import {
  cells,
  createTetrisState,
  dropMs,
  hardDrop,
  level as tetrisLevel,
  partnerCell,
  placed as tetrisPlaced,
  rotate,
  step,
  takeTetrisHint,
  tetrisSetup,
  TETRIS_HINT_COST,
  togglePause,
  type Piece,
  type TetrisDeck,
  type TetrisState,
} from '../src/game/tetris'
import type { RoundResult } from '../src/game/types'
import { awardInk, DAILY_INK, inkPrice, rankInk } from '../src/game/economy'
import {
  emptyCounters,
  emptyProfile,
  grantAwards,
  migrate as migrateProfile,
  recordQuiz,
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
    expect(score.total).toBe(713)
  })

  it('tahy nad par ubírají body', () => {
    const state = {
      ...createChainState(puzzle, 0),
      path: ['kosa', 'kosy', 'kasa', 'masa', 'mísa'],
      finishedAt: 30_000,
    }
    const score = scoreChain(state, 1, 30_000)
    expect(score.perfect).toBe(false)
    expect(score.total).toBe(440)
  })

  it('skóre nikdy nespadne pod minimum', () => {
    const state = {
      ...createChainState(puzzle, 0),
      path: ['kosa', ...Array.from({ length: 20 }, (_, i) => `x${i}`), 'mísa'],
      hintsUsed: 3,
      hintCost: 600,
      finishedAt: 600_000,
    }
    expect(scoreChain(state, 1, 600_000).total).toBe(35)
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
  // hraje sám, nebo že nasbírá body. Mistrovství sem patří taky: počítá jen
  // kola dohraná bez nápovědy, ne odehraná.
  it('většina met stojí na dovednosti nebo bodech, ne na počtu kol', () => {
    const skill = AWARDS.filter(
      (a) =>
        a.group === 'clean' ||
        a.group === 'score' ||
        a.group === 'mastery' ||
        a.group === 'feat',
    )
    expect(skill.length).toBeGreaterThan(AWARDS.length / 2)
  })

  // Hra má vydržet roky. Kdyby se dala vyčerpat za měsíc, přestala by mít
  // po měsíci smysl — proto je met hodně a nejvyšší stupně jsou daleko.
  it('met je dost na roky hraní a žebříčky mají pět stupňů', () => {
    expect(AWARDS.length).toBeGreaterThan(140)
    const families = new Set(AWARDS.map((a) => a.family).filter(Boolean))
    expect(families.size).toBeGreaterThan(25)
    expect(AWARDS.some((a) => a.tier === 5)).toBe(true)
  })

  // Klíč je navěky: podle něj se v uloženém profilu pozná, co hráč má.
  // Duplikát by znamenal metu, která se udělí dvakrát — i s inkoustem.
  it('žádné dvě mety nesdílejí klíč', () => {
    const ids = AWARDS.map((a) => a.id)
    expect(new Set(ids).size).toBe(ids.length)
  })

  // Uvnitř rodiny musí prahy růst. Kdyby ne, vyšší stupeň by padl dřív než
  // nižší a žebříček by ztratil smysl.
  it('žebříčky jdou stupeň po stupni nahoru', () => {
    const probe = (award: (typeof AWARDS)[number], profile: Profile) =>
      award.done(profile)
    const families = new Map<string, (typeof AWARDS)[number][]>()
    for (const award of AWARDS) {
      if (!award.family) continue
      const list = families.get(award.family) ?? []
      list.push(award)
      families.set(award.family, list)
    }
    for (const [, list] of families) {
      list.forEach((award, i) => expect(award.tier).toBe(i + 1))
      // Co splní vyšší stupeň, splní i všechny nižší.
      const top = list[list.length - 1]!
      const full: Profile = {
        ...emptyProfile(),
        fame: 9_999_999,
        bestStreak: 9_999,
        bestDayStreak: 9_999,
        daysPlayed: 9_999,
      }
      if (probe(top, full)) {
        for (const award of list) expect(probe(award, full)).toBe(true)
      }
    }
  })

  // Sto šedesát dlaždic naráz nikoho nemotivuje; jeden další stupeň ano.
  it('vitrína ukáže z rodiny získané stupně a jeden další', () => {
    const family = AWARDS.filter((a) => a.family === 'mistr-chain')
    expect(family.length).toBe(5)

    const fresh = visibleAwards(family, emptyProfile())
    expect(fresh.map((a) => a.id)).toEqual([family[0]!.id])

    const two: Profile = {
      ...emptyProfile(),
      awards: { [family[0]!.id]: 1, [family[1]!.id]: 2 },
    }
    expect(visibleAwards(family, two).map((a) => a.id)).toEqual([
      family[0]!.id,
      family[1]!.id,
      family[2]!.id,
    ])

    // Samostatná meta se neschovává nikdy.
    const solo = AWARDS.filter((a) => a.id === 'petiboj')
    expect(visibleAwards(solo, emptyProfile())).toEqual(solo)
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
  const deck: TetrisDeck = {
    syllables: [
      ['ko', 3],
      ['lo', 3],
      ['vo', 2],
      ['da', 2],
    ],
    pairs: [['ko', 'lo']],
    words: ['kolo', 'voda', 'kova', 'lokovat'],
  }
  const setup = tetrisSetup('normal', 1)
  const fresh = () => createTetrisState(deck, setup, 0)

  /** Postaví desku ze sloupců zdola nahoru — v testu se to čte líp než tahy. */
  function withGrid(grid: string[][], piece: Partial<Piece> = {}): TetrisState {
    const base = fresh()
    return {
      ...base,
      grid: Array.from({ length: setup.cols }, (_, i) => grid[i] ?? []),
      piece: { a: 'ko', b: 'lo', col: 0, row: setup.rows - 1, turn: 0, ...piece },
    }
  }

  it('dvojice padá po patrech, dokud nedosedne', () => {
    let state = fresh()
    const startRow = state.piece!.row
    state = step(state).state
    expect(state.piece!.row).toBe(startRow - 1)
  })

  // Tohle je jádro hry: jedna dvojice se dá přečíst čtyřmi způsoby.
  it('otočení mění pořadí i směr čtení', () => {
    const state = withGrid([], { turn: 0 })
    expect(cells(state.piece!).map((c) => c.text)).toEqual(['ko', 'lo'])
    // 0 = vodorovně vedle sebe, 1 = svisle nad sebou.
    expect(partnerCell(state.piece!)).toEqual({ col: 1, row: state.piece!.row })
    const turned = rotate(state).piece!
    expect(partnerCell(turned)).toEqual({ col: 0, row: state.piece!.row + 1 })
  })

  it('vodorovná dvojice složí slovo zleva doprava', () => {
    const state = withGrid([], { col: 0, turn: 0 })
    const result = hardDrop(state)
    expect(result.words).toEqual(['kolo'])
    expect(tetrisPlaced(result.state)).toBe(0)
  })

  it('svislá dvojice se čte zdola nahoru', () => {
    // turn 1 = „b" nad „a", tedy zdola „ko" a nad ním „lo".
    const state = withGrid([], { col: 0, turn: 1 })
    expect(hardDrop(state).words).toEqual(['kolo'])
    // Opačná poloha dá „loko", což slovo není.
    const flipped = withGrid([], { col: 0, turn: 3 })
    expect(hardDrop(flipped).words).toEqual([])
  })

  it('slovo se skládá i s tím, co na desce leží', () => {
    // Ve sloupci 1 leží „da"; dvojice „vo"+? doplní VODA vodorovně.
    const state = withGrid([[], ['da']], { a: 'vo', b: 'ko', col: 0, turn: 0 })
    const result = hardDrop(state)
    expect(result.words).toEqual(['voda'])
  })

  // Runtime nemá jak vymyslet slovo mimo slovník balíčku.
  it('uzná jen slovo ze slovníku balíčku', () => {
    const strict: TetrisDeck = { ...deck, words: ['voda'] }
    const state = { ...withGrid([], { col: 0, turn: 0 }), deck: strict }
    const result = hardDrop(state)
    expect(result.words).toEqual([])
    expect(tetrisPlaced(result.state)).toBe(2)
  })

  it('tempo se s úrovní zrychluje', () => {
    const slow = fresh()
    const fast = { ...slow, cleared: Array.from({ length: 24 }, () => 'kolo') }
    expect(tetrisLevel(fast)).toBeGreaterThan(tetrisLevel(slow))
    expect(dropMs(fast)).toBeLessThan(dropMs(slow))
  })

  it('kolo skončí, až se nová dvojice nemá kam vejít', () => {
    const full = Array.from({ length: setup.cols }, () =>
      Array.from({ length: setup.rows }, () => 'xx'),
    )
    const state = withGrid(full, { col: 0, turn: 0 })
    const result = hardDrop(state)
    expect(result.state.over).toBe(true)
  })

  it('nápověda najde polohu, ve které se něco složí', () => {
    const state = withGrid([], { a: 'ko', b: 'lo' })
    const hint = takeTetrisHint(state, 'spot', false)!
    expect(hint.spot!.words).toContain('kolo')
    expect(hint.state.hintCost).toBe(TETRIS_HINT_COST.spot)
  })

  it('nápověda zaplacená inkoustem nestojí body, ale pořád je to nápověda', () => {
    const hint = takeTetrisHint(fresh(), 'swap', true)!
    expect(hint.state.hintCost).toBe(0)
    expect(hint.state.hintsUsed).toBe(1)
    expect(hint.state.freeHints).toBe(1)
  })

  it('pauza zastaví pád', () => {
    const paused = togglePause(fresh())
    expect(step(paused).state.piece!.row).toBe(paused.piece!.row)
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
    expect(inkPrice(HINT_COST.distance)).toBe(5)
    expect(inkPrice(HINT_COST.word)).toBe(20)
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
    expect(PROFILE_RANKS[3]!.at).toBeLessThanOrEqual(2_500)
    // Od té chvíle každý další stupeň stojí víc než ten předchozí.
    for (let i = 4; i < PROFILE_RANKS.length; i += 1) {
      expect(gap(i)).toBeGreaterThan(gap(i - 1))
    }
    // Nejvyšší hodnost je běh na roky, ne na měsíc.
    expect(PROFILE_RANKS[PROFILE_RANKS.length - 1]!.at).toBeGreaterThan(3_000_000)
  })

  // Kolo Slabik nemá konec — padá se, dokud se deska nezablokuje — takže
  // vytrvalý hráč z nich vytěžil násobky toho, co jde získat jinde. Bodování
  // šlo na desetinu a s ním i to, co za ně hráč nasbíral.
  it('Slabiky dávají desetinu toho co dřív a profil se přepočítá zpětně', () => {
    const state = {
      cleared: Array.from({ length: 9 }, () => 'slabi'),
      bestChain: 1,
      hintCost: 0,
      hintsUsed: 0,
      freeHints: 0,
      setup: { perLevel: 100 },
    } as unknown as TetrisState
    const before = scoreTetris(state, 0).total
    // Devět slov po pěti písmenech: 35*9 + 13*45 = 900 na staré stupnici.
    expect(before).toBe(90)

    // Uložený profil: ze 4 000 věhlasu jich 3 000 přinesly Slabiky.
    const stored = {
      version: 2,
      fame: 4000,
      stats: {
        tetris: { played: 5, bestScore: 900, totalScore: 3000, extra: 0, perfect: 0, clean: 0 },
      },
      counters: { ...emptyCounters(), bestScore: 900 },
      history: [
        { mode: 'tetris', score: 900, difficulty: 'normal', puzzleId: 't', perfect: false, success: true, elapsedMs: 0, hintsUsed: 0, detail: {} },
        { mode: 'chain', score: 400, difficulty: 'normal', puzzleId: 'c', perfect: false, success: true, elapsedMs: 0, hintsUsed: 0, detail: {} },
      ],
    }
    const after = migrateProfile(stored)
    // Devět desetin toho, co Slabiky nasypaly, se z věhlasu ubere.
    expect(after.fame).toBe(1300)
    expect(after.stats.tetris.totalScore).toBe(300)
    expect(after.stats.tetris.bestScore).toBe(90)
    expect(after.counters.bestScore).toBe(90)
    expect(after.history[0]!.score).toBe(90)
    // Ostatní hry se nedotkne.
    expect(after.history[1]!.score).toBe(400)
    expect(after.stats.chain.totalScore).toBe(0)

    // Podruhé už se nic neděje.
    expect(migrateProfile(after).fame).toBe(1300)
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
    // Rozdíl je aspoň DAILY_INK. Kompletní várka navíc rovnou odemkne první
    // stupeň mety „Celá várka", takže se k němu připočte ještě inkoust za ni —
    // proto se porovnává „aspoň", ne „přesně".
    expect(
      recordRound(almost, round(), day, true).ink -
        recordRound(almost, round(), day, false).ink,
    ).toBeGreaterThanOrEqual(DAILY_INK)
  })

  // Denní várka se počítá jen jednou za den a jen když je opravdu celá.
  it('celá denní várka se započítá právě jednou', () => {
    const day = '2026-01-01'
    const start = emptyProfile()
    expect(recordRound(start, round(), day, true).counters.dailySets).toBe(0)

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
    expect(recordRound(almost, round(), day, true).counters.dailySets).toBe(1)
    expect(recordRound(almost, round(), day, false).counters.dailySets).toBe(0)
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
    expect(won.total).toBeGreaterThan(300)

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


describe('otázka dne', () => {
  function question(topic: (typeof QUIZ_TOPICS)[number], n: number): QuizQuestion {
    return {
      id: `${topic}-${n}`,
      topic,
      ask: 'Poznej něco.',
      clues: ['těžká', 'střední', 'návodná'],
      answer: `odpověď ${n}`,
    }
  }

  const deck = Object.fromEntries(
    QUIZ_TOPICS.map((topic) => [topic, [0, 1, 2].map((n) => question(topic, n))]),
  ) as QuizDeck

  // Přesně to, co hráč nechce: pětkrát sport za týden. Obory se proto
  // střídají kolečkem a žádná náhoda v tom není.
  it('obory se střídají kolečkem, jeden den jeden obor', () => {
    const week = Array.from({ length: QUIZ_TOPICS.length }, (_, day) =>
      quizFor(deck, day)!.topic,
    )
    expect(new Set(week).size).toBe(QUIZ_TOPICS.length)
  })

  it('otázka se nezopakuje dřív, než projdou všechny', () => {
    const cycle = quizCycle(deck)
    expect(cycle).toBe(3 * QUIZ_TOPICS.length)
    const ids = Array.from({ length: cycle }, (_, day) => quizFor(deck, day)!.id)
    expect(new Set(ids).size).toBe(cycle)
    // Po celém kole se první otázka vrátí — a to je v pořádku.
    expect(quizFor(deck, cycle)!.id).toBe(ids[0])
  })

  it('týž den dá všem hráčům tutéž otázku', () => {
    expect(quizFor(deck, 412)!.id).toBe(quizFor(deck, 412)!.id)
    expect(quizFor(deck, 412)!.id).not.toBe(quizFor(deck, 413)!.id)
  })

  // Sázka se dělá naslepo, proto je za jednu indicii trojnásobek. Kdyby to
  // bylo naopak nebo nastejno, nikdo by si nevzal míň než tři.
  it('míň indicií znamená větší odměnu', () => {
    expect(QUIZ_REWARD[1]).toBeGreaterThan(QUIZ_REWARD[2])
    expect(QUIZ_REWARD[2]).toBeGreaterThan(QUIZ_REWARD[3])
    expect(QUIZ_REWARD[1]).toBe(3 * QUIZ_REWARD[3])
  })

  it('koupí se jen tolik indicií, kolik si hráč vybral', () => {
    let state = buyClues(createQuizState(question('veda', 1)), 2)
    expect(state.bought).toBe(2)
    expect(state.shown).toBe(1)
    state = revealClue(state)
    expect(state.shown).toBe(2)
    // Třetí si nekoupil, tak ji nedostane.
    expect(revealClue(state).shown).toBe(2)
  })

  it('rozhodnutí o počtu indicií se nedá vzít zpět', () => {
    const state = buyClues(buyClues(createQuizState(question('veda', 1)), 1), 3)
    expect(state.bought).toBe(1)
  })

  it('odpověď se porovnává bez diakritiky, velikosti písmen i mezer', () => {
    const q: QuizQuestion = {
      id: 'x',
      topic: 'osobnost',
      ask: 'Kdo?',
      clues: ['a', 'b', 'c'],
      answer: 'Édith Piaf',
      alt: ['Piaf'],
    }
    expect(quizMatches(q, 'edith piaf')).toBe(true)
    expect(quizMatches(q, 'Edith-Piaf')).toBe(true)
    expect(quizMatches(q, '  PIAF ')).toBe(true)
    expect(quizMatches(q, 'Piaff')).toBe(false)
  })

  it('po třech chybách kolo končí a odměna je nulová', () => {
    let state = buyClues(createQuizState(question('sport', 1)), 1)
    for (let i = 0; i < QUIZ_TRIES; i += 1) {
      state = quizGuess(state, `vedle ${i}`).state
    }
    expect(state.finishedAt).not.toBeNull()
    expect(state.solved).toBe(false)
    expect(quizReward(state)).toBe(0)
  })

  it('trefa na jednu indicii platí nejvíc', () => {
    const q = question('sport', 1)
    const one = quizGuess(buyClues(createQuizState(q), 1), q.answer).state
    const three = quizGuess(buyClues(createQuizState(q), 3), q.answer).state
    expect(quizReward(one)).toBe(QUIZ_REWARD[1])
    expect(quizReward(three)).toBe(QUIZ_REWARD[3])
  })

  // Po čtvrté prohře by jedna věta zněla jako automat.
  it('povzbuzení má patnáct obměn a střídá se po dnech', () => {
    expect(QUIZ_CONSOLATIONS.length).toBe(15)
    expect(new Set(QUIZ_CONSOLATIONS).size).toBe(15)
  })

  it('zápis do profilu zamkne dnešek a vede řadu úspěšných dnů', () => {
    const start = emptyProfile()
    const first = recordQuiz(start, '2026-03-01', { solved: true, clues: 1, ink: 30 })
    expect(first.quiz.lastDay).toBe('2026-03-01')
    expect(first.quiz.solved).toBe(1)
    expect(first.quiz.expert).toBe(1)
    expect(first.quiz.streak).toBe(1)
    // Kromě odměny padne ještě inkoust za mety, které tím kolem padly.
    expect(first.ink).toBeGreaterThanOrEqual(start.ink + 30)

    const second = recordQuiz(first, '2026-03-02', { solved: true, clues: 3, ink: 10 })
    expect(second.quiz.streak).toBe(2)
    expect(second.quiz.expert).toBe(1)

    // Vynechaný den řadu utne stejně jako špatná odpověď.
    const gap = recordQuiz(second, '2026-03-05', { solved: true, clues: 2, ink: 20 })
    expect(gap.quiz.streak).toBe(1)
    const missed = recordQuiz(gap, '2026-03-06', { solved: false, clues: 1, ink: 0 })
    expect(missed.quiz.streak).toBe(0)
    expect(missed.quiz.played).toBe(4)
    expect(missed.quiz.bestStreak).toBe(2)
  })

  // Otázka dne není o češtině, takže nesmí hýbat věhlasem ani sérií kol.
  it('nedává body ani nehýbe sérií čistých kol', () => {
    const start: Profile = { ...emptyProfile(), fame: 1234, streak: 7 }
    const after = recordQuiz(start, '2026-03-01', { solved: true, clues: 1, ink: 30 })
    expect(after.fame).toBe(1234)
    expect(after.streak).toBe(7)
  })
})
