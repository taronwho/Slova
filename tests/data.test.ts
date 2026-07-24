/**
 * Ověření vygenerovaných dat — tohle je vlastní důkaz garantované řešitelnosti.
 * Prochází se *každá* hádanka, která by se dostala ke hráči.
 */

import { readFileSync, readdirSync } from 'node:fs'
import { join } from 'node:path'
import { describe, expect, it } from 'vitest'

import { bfsDistances, buildChainGraph, shortestPath } from '../src/game/chain'
import { fold } from '../src/lib/czech'
import { MIN_WORD_LENGTH } from '../src/game/hive'
import { signature } from '../src/lib/czech'

const DATA = join(__dirname, '..', 'public', 'data')

function readJson<T>(...parts: string[]): T {
  return JSON.parse(readFileSync(join(DATA, ...parts), 'utf-8')) as T
}

describe('řetěz — data', () => {
  const index = readJson<Record<string, { words: number; puzzles: number }>>(
    'chain',
    'index.json',
  )
  const lengths = Object.keys(index).map(Number)

  it('má hádanky pro všechny tři délky', () => {
    expect(lengths.sort()).toEqual([4, 5, 6])
  })

  for (const length of [4, 5, 6]) {
    describe(`délka ${length}`, () => {
      const words = readJson<string[]>('chain', `words-${length}.json`)
      const puzzles = readJson<[string, string, number][]>(
        'chain',
        `puzzles-${length}.json`,
      )
      const graph = buildChainGraph(words)

      it('všechna slova mají správnou délku a jsou unikátní', () => {
        expect(new Set(words).size).toBe(words.length)
        expect(words.every((w) => w.length === length)).toBe(true)
      })

      it('každá hádanka je řešitelná a par sedí na skutečnou nejkratší cestu', () => {
        expect(puzzles.length).toBeGreaterThan(300)

        const distanceCache = new Map<string, Int32Array>()
        const problems: string[] = []

        for (const [start, target, par] of puzzles) {
          const from = graph.index.get(start)
          const to = graph.index.get(target)
          if (from === undefined || to === undefined) {
            problems.push(`${start}->${target}: slovo není ve slovníku`)
            continue
          }
          if (start === target) {
            problems.push(`${start}: start se rovná cíli`)
            continue
          }

          let dist = distanceCache.get(start)
          if (!dist) {
            dist = bfsDistances(graph, from)
            distanceCache.set(start, dist)
          }

          const real = dist[to]!
          if (real === -1) problems.push(`${start}->${target}: nedosažitelné`)
          else if (real !== par) {
            problems.push(`${start}->${target}: par ${par}, skutečnost ${real}`)
          }
        }

        expect(problems.slice(0, 10)).toEqual([])
      })

      it('vzorek hádanek má rekonstruovatelnou cestu platnou po jednom písmenu', () => {
        const sample = puzzles.filter((_, i) => i % 37 === 0)
        for (const [start, target, par] of sample) {
          const path = shortestPath(
            graph,
            graph.index.get(start)!,
            graph.index.get(target)!,
          )
          expect(path, `${start}->${target}`).not.toBeNull()
          expect(path!.length - 1, `${start}->${target}`).toBe(par)

          const asWords = path!.map((i) => words[i]!)
          for (let i = 1; i < asWords.length; i++) {
            const a = asWords[i - 1]!
            const b = asWords[i]!
            let diff = 0
            for (let k = 0; k < a.length; k++) if (a[k] !== b[k]) diff++
            expect(diff, `${a} -> ${b}`).toBe(1)
          }
          expect(new Set(asWords).size).toBe(asWords.length)
        }
      })
    })
  }
})

describe('voština — data', () => {
  interface Hive {
    id: string
    center: string
    outer: string[]
    solutions: string[]
    pangrams: string[]
    difficulty: string
  }

  const index = readJson<{ packSize: number; hives: { id: string; pack: number }[] }>(
    'hive',
    'index.json',
  )
  const packFiles = readdirSync(join(DATA, 'hive')).filter((f) => f.startsWith('pack-'))
  const hives: Hive[] = packFiles.flatMap((file) => readJson<Hive[]>('hive', file))

  it('index odpovídá balíčkům', () => {
    expect(hives.length).toBe(index.hives.length)
    expect(new Set(hives.map((h) => h.id)).size).toBe(hives.length)
  })

  it('každá plástev má sedm různých písmen', () => {
    for (const hive of hives) {
      const letters = [hive.center, ...hive.outer]
      expect(new Set(letters).size, hive.id).toBe(7)
      expect(hive.outer.length, hive.id).toBe(6)
    }
  })

  it('každé řešení jde z plástve složit a obsahuje střed', () => {
    const problems: string[] = []
    for (const hive of hives) {
      const letters = new Set([hive.center, ...hive.outer])
      for (const word of hive.solutions) {
        if (word.length < MIN_WORD_LENGTH) {
          problems.push(`${hive.id}: ${word} je příliš krátké`)
          continue
        }
        const folded = fold(word)
        if (!folded.includes(hive.center)) {
          problems.push(`${hive.id}: ${word} nemá střed ${hive.center}`)
          continue
        }
        for (const ch of folded) {
          if (!letters.has(ch)) {
            problems.push(`${hive.id}: ${word} používá cizí písmeno ${ch}`)
            break
          }
        }
      }
    }
    expect(problems.slice(0, 10)).toEqual([])
  })

  it('každá plástev má aspoň jeden pangram a ten je mezi řešeními', () => {
    for (const hive of hives) {
      expect(hive.pangrams.length, hive.id).toBeGreaterThan(0)
      for (const pangram of hive.pangrams) {
        expect(hive.solutions, hive.id).toContain(pangram)
        expect(new Set(fold(pangram)).size, `${hive.id}: ${pangram}`).toBe(7)
      }
    }
  })

  it('řešení jsou unikátní a plástev je dost bohatá na rozehrání', () => {
    for (const hive of hives) {
      expect(new Set(hive.solutions).size, hive.id).toBe(hive.solutions.length)
      expect(hive.solutions.length, hive.id).toBeGreaterThanOrEqual(22)
    }
  })
})

describe('věž — data', () => {
  interface Level {
    sig: string
    added: string | null
    words: string[]
  }
  interface Tower {
    id: string
    difficulty: string
    levels: Level[]
  }

  const index = readJson<{ towers: { id: string; pack: number; top: number }[] }>(
    'tower',
    'index.json',
  )
  const packFiles = readdirSync(join(DATA, 'tower')).filter((f) => f.startsWith('pack-'))
  const towers: Tower[] = packFiles.flatMap((file) => readJson<Tower[]>('tower', file))

  it('index odpovídá balíčkům', () => {
    expect(towers.length).toBe(index.towers.length)
    expect(new Set(towers.map((t) => t.id)).size).toBe(towers.length)
  })

  it('každé patro má aspoň jedno slovo a všechna sedí na podpis', () => {
    const problems: string[] = []
    for (const tower of towers) {
      for (const level of tower.levels) {
        if (level.words.length === 0) {
          problems.push(`${tower.id}: prázdné patro ${level.sig}`)
          continue
        }
        for (const word of level.words) {
          if (signature(word) !== level.sig) {
            problems.push(`${tower.id}: ${word} neodpovídá podpisu ${level.sig}`)
          }
        }
      }
    }
    expect(problems.slice(0, 10)).toEqual([])
  })

  it('každé patro přidává právě jedno písmeno k tomu pod ním', () => {
    const problems: string[] = []
    for (const tower of towers) {
      expect(tower.levels[0]!.added, tower.id).toBeNull()
      expect(tower.levels[0]!.sig.length, tower.id).toBe(3)

      for (let i = 1; i < tower.levels.length; i++) {
        const prev = tower.levels[i - 1]!
        const level = tower.levels[i]!
        if (level.sig.length !== prev.sig.length + 1) {
          problems.push(`${tower.id}: patro ${i} nemá o písmeno víc`)
          continue
        }
        // Podpis nižšího patra musí být multimnožinovou podmnožinou vyššího.
        const rest = [...level.sig]
        let ok = true
        for (const ch of prev.sig) {
          const at = rest.indexOf(ch)
          if (at === -1) {
            ok = false
            break
          }
          rest.splice(at, 1)
        }
        if (!ok || rest.length !== 1) {
          problems.push(`${tower.id}: patro ${i} nevzniklo přidáním jednoho písmene`)
          continue
        }
        if (rest[0] !== level.added) {
          problems.push(
            `${tower.id}: patro ${i} hlásí +${level.added}, ve skutečnosti +${rest[0]}`,
          )
        }
      }
    }
    expect(problems.slice(0, 10)).toEqual([])
  })

  it('věže mají obtížností danou výšku', () => {
    const heights: Record<string, number> = { easy: 6, normal: 7, hard: 8 }
    for (const tower of towers) {
      const top = tower.levels[tower.levels.length - 1]!.sig.length
      expect(top, tower.id).toBe(heights[tower.difficulty])
    }
  })
})
