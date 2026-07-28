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

describe('šibenice — data', () => {
  const puzzles = readJson<{ id: string; word: string; difficulty: string }[]>(
    'gallows',
    'puzzles.json',
  )

  it('má slova pro všechny tři obtížnosti', () => {
    for (const difficulty of ['easy', 'normal', 'hard']) {
      expect(puzzles.filter((p) => p.difficulty === difficulty).length).toBeGreaterThan(300)
    }
  })

  it('id jsou jedinečná a slova se neopakují', () => {
    expect(new Set(puzzles.map((p) => p.id)).size).toBe(puzzles.length)
    expect(new Set(puzzles.map((p) => p.word)).size).toBe(puzzles.length)
  })

  it('délky sedí na obtížnost a slovo má dost různých písmen', () => {
    const bands: Record<string, [number, number]> = {
      easy: [4, 5],
      normal: [6, 7],
      hard: [8, 9],
    }
    const problems: string[] = []
    for (const puzzle of puzzles) {
      const [min, max] = bands[puzzle.difficulty]!
      if (puzzle.word.length < min || puzzle.word.length > max) problems.push(puzzle.word)
      // Slovo ze dvou různých písmen se uhodne dvěma tahy — to není hádanka.
      if (new Set(fold(puzzle.word)).size < 3) problems.push(puzzle.word)
    }
    expect(problems.slice(0, 10)).toEqual([])
  })
})

describe('detektiv — data', () => {
  interface Case {
    id: string
    word: string
    clue: string
    difficulty: string
  }
  const puzzles = readJson<Case[]>('detective', 'puzzles.json')

  it('má dost případů a jedinečná id i slova', () => {
    expect(puzzles.length).toBeGreaterThan(1200)
    expect(new Set(puzzles.map((p) => p.id)).size).toBe(puzzles.length)
    expect(new Set(puzzles.map((p) => p.word)).size).toBe(puzzles.length)
  })

  // Nejdůležitější kontrola celého režimu: text o původu nesmí obsahovat
  // hledané slovo. Generátor takové výskyty maskuje, tohle to hlídá na
  // hotových datech.
  it('text o původu nikde neprozradí hledané slovo', () => {
    const problems: string[] = []
    for (const puzzle of puzzles) {
      if (fold(puzzle.clue.toLowerCase()).includes(fold(puzzle.word))) {
        problems.push(`${puzzle.word}: ${puzzle.clue}`)
      }
    }
    expect(problems.slice(0, 5)).toEqual([])
  })

  /**
   * Indicie nesmí obsahovat cizojazyčný protějšek hledaného slova.
   *
   * „Převzato z anglického hurricane, jež je odvozeno ze španělského huracán"
   * u slova hurikán se nehádá, jen opisuje. Stejně tak „Z německého Ballast"
   * u balastu. Maskování dřív hlídalo jen společný začátek, a ten se u
   * přejímek často liší uvnitř slova.
   */
  it('indicie neobsahuje skoro stejné slovo v jiném jazyce', () => {
    const ratio = (a: string, b: string): number => {
      // Podíl shodných znaků v pořadí — hrubá míra podobnosti dvou slov.
      const rows = Array.from({ length: a.length + 1 }, () =>
        new Array<number>(b.length + 1).fill(0),
      )
      for (let i = 1; i <= a.length; i++) {
        for (let j = 1; j <= b.length; j++) {
          rows[i]![j] =
            a[i - 1] === b[j - 1]
              ? rows[i - 1]![j - 1]! + 1
              : Math.max(rows[i - 1]![j]!, rows[i]![j - 1]!)
        }
      }
      return (2 * rows[a.length]![b.length]!) / (a.length + b.length)
    }

    const leaky: string[] = []
    for (const puzzle of puzzles) {
      const target = fold(puzzle.word.toLowerCase())
      if (target.length < 5) continue
      for (const raw of puzzle.clue.split(/[^\p{L}]+/u)) {
        const token = fold(raw.toLowerCase())
        if (token.length < 5) continue
        if (ratio(token, target) >= 0.8) leaky.push(`${puzzle.word}: „${raw}"`)
      }
    }
    expect(leaky.slice(0, 8)).toEqual([])
  })

  /**
   * Indicie nesmí skončit uprostřed myšlenky.
   *
   * Text se zkracuje po větách a dělič vět bral tečku za řadovou číslovkou
   * jako konec věty — indicie pak končila „…se na začátku 17." a hráč čekal
   * zbytek, který nikdy nepřišel.
   */
  it('text o původu končí dokončenou větou', () => {
    const truncated = puzzles.filter((puzzle) => {
      const clue = puzzle.clue.trim()
      return (
        !/[.!?]$/.test(clue) ||
        // řadová číslovka bez toho, co počítá („v 18.")
        /\s\d{1,2}\.$/.test(clue) ||
        // Zkratka, po které musí věta pokračovat. Musí před ní stát mezera:
        // `\b` je v JS bez příznaku `u` jen o ASCII, takže „hêr." vypadá
        // jako zkratka „r." a test hlásil planý poplach.
        /(?:^|\s)(?:např|resp|srov|lat|řec|něm|angl|tzv|stol|r)\.$/i.test(clue) ||
        clue.split('(').length !== clue.split(')').length
      )
    })
    expect(truncated.map((p) => `${p.word}: …${p.clue.slice(-40)}`)).toEqual([])
  })

  it('text je čitelně dlouhý a bez zbytků wikitextu', () => {
    const problems: string[] = []
    for (const puzzle of puzzles) {
      if (puzzle.clue.length < 40 || puzzle.clue.length > 320) problems.push(puzzle.word)
      if (/\[\[|\{\{|<ref|''/.test(puzzle.clue)) problems.push(`${puzzle.word}: wikitext`)
    }
    expect(problems.slice(0, 5)).toEqual([])
  })

  // Hráč si stěžoval, že indicii nerozumí: text končil uprostřed souvětí
  // („…, způsobem metafory a odvození pak i kardinální") a předtím vypočítával
  // příbuzná slova („Srovnej např. stožár, stehno"), což je ve slovníku na
  // místě, ale v hádance to jenom mate.
  it('indicie je celá věta bez slovníkových odkazů', () => {
    const problems: string[] = []
    for (const puzzle of puzzles) {
      if (!/[.!?]$/.test(puzzle.clue.trim())) problems.push(`${puzzle.word}: bez tečky`)
      if (/\b(srovnej|srov\.|porovnej|viz)\b/i.test(puzzle.clue)) {
        problems.push(`${puzzle.word}: odkaz`)
      }
    }
    expect(problems.slice(0, 5)).toEqual([])
  })

  // Zakryté místo je „[?]", ne výpustka — ta se v etymologických textech
  // vyskytuje sama o sobě a hráč by nepoznal, kde je díra k hádání.
  it('zakryté místo se pozná od běžné výpustky', () => {
    const gaps = puzzles.filter((p) => p.clue.includes('[?]'))
    expect(gaps.length).toBeGreaterThan(100)
    expect(puzzles.filter((p) => p.clue.includes('…'))).toEqual([])
  })
})

describe('slabikový tetris — data', () => {
  interface Deck {
    syllables: [string, number][]
    pairs: [string, string][]
    words: string[]
  }
  const deck = readJson<Deck>('tetris', 'deck.json')
  const pool = new Set(deck.syllables.map(([syllable]) => syllable))

  it('balíček je dost bohatý, aby se dvě kola neopakovala', () => {
    expect(deck.syllables.length).toBeGreaterThan(200)
    expect(deck.words.length).toBeGreaterThan(5000)
    expect(deck.pairs.length).toBeGreaterThan(500)
  })

  it('slabiky jsou krátké a mají váhu', () => {
    const problems: string[] = []
    for (const [syllable, weight] of deck.syllables) {
      if (syllable.length > 4) problems.push(`${syllable}: dlouhá`)
      if (weight <= 0) problems.push(`${syllable}: nulová váha`)
    }
    expect(problems.slice(0, 5)).toEqual([])
  })

  // Jádro celé hry: co hra uzná, musí jít z rozdávaných slabik opravdu
  // poskládat — jinak by na desce viselo slovo, které se nedá dosáhnout.
  it('každé slovo balíčku jde složit z 2–3 rozdávaných slabik', () => {
    const problems: string[] = []
    for (const word of deck.words) {
      if (!buildable(word, pool, 3)) problems.push(word)
    }
    expect(problems.slice(0, 5)).toEqual([])
  })

  it('rozdělené dvojice dávají slovo a obě půlky se rozdávají', () => {
    const words = new Set(deck.words)
    const problems: string[] = []
    for (const [a, b] of deck.pairs) {
      if (!words.has(a + b)) problems.push(`${a}+${b}`)
      if (!pool.has(a) || !pool.has(b)) problems.push(`${a}+${b}: mimo balíček`)
    }
    expect(problems.slice(0, 5)).toEqual([])
  })
})

/** Jde slovo poskládat z nejvýš `limit` slabik z poolu? */
function buildable(word: string, pool: Set<string>, limit: number): boolean {
  const walk = (rest: string, depth: number): boolean => {
    if (rest === '') return depth >= 2
    if (depth >= limit) return false
    for (let size = 1; size <= 4; size += 1) {
      const head = rest.slice(0, size)
      if (pool.has(head) && walk(rest.slice(size), depth + 1)) return true
    }
    return false
  }
  return walk(word, 0)
}

describe('slovník — jen základní tvary', () => {
  // Seznam povolených slov vzniká v tools/2b_base_forms.py: hunspell musí
  // slovo přečíst bez jediné přípony a předpony (je to tedy přímo heslo
  // slovníku) a lemma se musí rovnat slovu. Test hlídá, že se do hry
  // nedostane nic mimo něj — právě takhle se tam dřív dostalo „nemíříš",
  // „agente" nebo „tang".
  const allowed = new Set(readJson<string[]>('..', '..', 'tests', 'fixtures', 'base-forms.json'))

  it('fixtura povolených tvarů je načtená', () => {
    expect(allowed.size).toBeGreaterThan(20_000)
  })

  // Druhá strana téhož: filtr nesmí být tak přísný, aby vyhazoval správné
  // tvary. Lemmatizér zná jen část slovní zásoby, a když se jeho neznalost
  // brala jako námitka, chybělo pět set správných množných čísel — hráč pak
  // ve Voštině napsal „sekery" a hra tvrdila, že to slovo nezná.
  it('zná i množná čísla, která lemmatizér neumí', () => {
    const missing = [
      'sekery', 'jablka', 'trička', 'pavouci', 'sloni', 'kopce',
      'třešně', 'směsi', 'žebra', 'videa', 'latě', 'mniši',
    ].filter((word) => !allowed.has(word))
    expect(missing).toEqual([])
  })

  it('šibenice hádá jen povolené tvary', () => {
    const problems: string[] = []
    for (const puzzle of readJson<{ word: string }[]>('gallows', 'puzzles.json')) {
      if (!allowed.has(puzzle.word)) problems.push(puzzle.word)
    }
    expect(problems.slice(0, 10)).toEqual([])
  })

  it('slabikový tetris uznává jen povolené tvary', () => {
    const deck = readJson<{ words: string[] }>('tetris', 'deck.json')
    const problems = deck.words.filter((word) => !allowed.has(word))
    expect(problems.slice(0, 10)).toEqual([])
  })

  it('detektiv hádá jen povolené tvary', () => {
    const problems: string[] = []
    for (const puzzle of readJson<{ word: string }[]>('detective', 'puzzles.json')) {
      if (!allowed.has(puzzle.word)) problems.push(puzzle.word)
    }
    expect(problems.slice(0, 10)).toEqual([])
  })

  it('řetěz používá jen povolené tvary', () => {
    const problems: string[] = []
    for (const length of [4, 5, 6]) {
      for (const word of readJson<string[]>('chain', `words-${length}.json`)) {
        if (!allowed.has(word)) problems.push(word)
      }
    }
    expect(problems.slice(0, 10)).toEqual([])
  })

  it('voština nabízí jen povolené tvary', () => {
    const problems: string[] = []
    for (const file of readdirSync(join(DATA, 'hive')).filter((f) => f.startsWith('pack-'))) {
      for (const hive of readJson<{ solutions: string[] }[]>('hive', file)) {
        for (const word of hive.solutions) {
          if (!allowed.has(word)) problems.push(word)
        }
      }
    }
    expect(problems.slice(0, 10)).toEqual([])
  })

  it('věž staví jen z povolených tvarů', () => {
    const problems: string[] = []
    for (const file of readdirSync(join(DATA, 'tower')).filter((f) => f.startsWith('pack-'))) {
      for (const tower of readJson<{ levels: { words: string[] }[] }[]>('tower', file)) {
        for (const level of tower.levels) {
          for (const word of level.words) {
            if (!allowed.has(word)) problems.push(word)
          }
        }
      }
    }
    expect(problems.slice(0, 10)).toEqual([])
  })
})
