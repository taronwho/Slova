/**
 * Ověření vygenerovaných dat — tohle je vlastní důkaz garantované řešitelnosti.
 * Prochází se *každá* hádanka, která by se dostala ke hráči.
 */

import { createHash } from 'node:crypto'
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
      // A musí jít vyhádat po písmenech: mezera ani spojovník na klávesnici
      // nejsou, takže by se takové slovo nedalo nikdy dokončit.
      if (!/^[a-z]+$/.test(fold(puzzle.word))) problems.push(puzzle.word)
    }
    expect(problems.slice(0, 10)).toEqual([])
  })
})

describe('detektiv — data', () => {
  interface Case {
    id: string
    word: string
    clue: string
    grammar?: string
    origin?: string
    story?: string
    difficulty: string
  }
  const puzzles = readJson<Case[]>('detective', 'puzzles.json')

  /** Všechno, co hráč čte během hry. Nic z toho nesmí odpověď prozradit. */
  const shownWhilePlaying = (puzzle: Case): string[] =>
    [puzzle.clue, puzzle.grammar, puzzle.origin].filter((text): text is string => !!text)

  // Sada vyrostla řádově, když indicie přestala stát na etymologii a začala
  // stát na významu: etymologii má sotva každé dvacáté heslo, význam skoro
  // každé. Hranice je nízko schválně — hlídá se, že se sada nerozsype, ne
  // kolik přesně jich zrovna je.
  it('má dost případů a jedinečná id i slova', () => {
    expect(puzzles.length).toBeGreaterThan(2000)
    expect(new Set(puzzles.map((p) => p.id)).size).toBe(puzzles.length)
    expect(new Set(puzzles.map((p) => p.word)).size).toBe(puzzles.length)
  })

  // Nejdůležitější kontrola celého režimu: nic, co hráč během hry vidí,
  // nesmí obsahovat hledané slovo. Generátor takové výskyty maskuje, tohle
  // to hlídá na hotových datech.
  it('nic z toho, co hráč čte, neprozradí hledané slovo', () => {
    const problems: string[] = []
    for (const puzzle of puzzles) {
      for (const text of shownWhilePlaying(puzzle)) {
        if (fold(text.toLowerCase()).includes(fold(puzzle.word))) {
          problems.push(`${puzzle.word}: ${text}`)
        }
      }
    }
    expect(problems.slice(0, 5)).toEqual([])
  })

  /**
   * Po zakrytí musí v indicii zůstat něco, z čeho se dá vyjít.
   *
   * „Mající chuť [?]" u *slaného* nebo „Odborník v oboru [?]" u *psychiatra*
   * projde délkou i počtem slov, jenže všechno podstatné leží právě v té
   * díře. U nezakryté definice se nic takového stát nemůže, ta se neměří.
   */
  it('po zakrytí zbude ve významu aspoň nějaká informace', () => {
    const filler = new Set(
      `majici majicich takovy takova takove ktery ktera ktere kterym jenz
       schopny schopna schopne nachazejici nachazi urceny urcena urcene slouzici
       ktereho jehoz nekdo neco nejaky nejaka nejake jeho jeji jejich prip apod
       zpusob zpusobem vlastnost vlastnosti cinnost delat udelat mit byt stav
       obvykle zejmena zvlaste vetsinou take tedy`.split(/\s+/),
    )
    const hollow = puzzles.filter((puzzle) => {
      if (!puzzle.clue.includes('[?]')) return false
      const words = puzzle.clue
        .replaceAll('[?]', ' ')
        .split(/[^\p{L}]+/u)
        .map((word) => fold(word.toLowerCase()))
        .filter((word) => word.length >= 4 && !filler.has(word))
      return words.length < 3
    })
    expect(hollow.map((p) => `${p.word}: ${p.clue}`).slice(0, 6)).toEqual([])
  })

  /**
   * Totéž pro původ, jen jiným metrem.
   *
   * „Odvozeno od substantiva [?] pomocí předpony [?]-." má přes čtyřicet
   * znaků, takže délková podmínka projde — jenže to sedí na stovky slov
   * a hráč z toho nemá co vytěžit.
   */
  it('po zakrytí zbude v původu aspoň nějaká informace', () => {
    const filler = new Set(
      `odvozeno odvozene odvozeneho odvozena odvozeny odvozenim utvoreno utvorena
       utvoreny vzniklo vznikla vznikl vznik pochazi prejato prevzato prejaty prejate
       pres pomoci predpony predpona pripony pripona pripon koncovky substantiva
       substantivum substantivem adjektiva adjektivum adjektivem slovesa sloveso
       slovem slova slovo tvaru tvar tvary korene koren zakladu zaklad zakladem
       jazyka jazyky jazyk vyznamu vyznam vyznamem tehoz stejneho stejnym dolozeno
       poprve patrne pravdepodobne zrejme nejspis snad dale take tedy dnes puvodne
       puvodni puvodniho novejsi starsi tvarem varianta prechylenim podstatneho
       jmena pricesti pritomne minule trpne slovotvornemu slovotvorneho ktery ktera
       ktere kterym jehoz jejiz coz jako toto tento tato temer velmi`.split(/\s+/),
    )
    const hollow = puzzles.filter((puzzle) => {
      if (!puzzle.origin) return false
      const words = puzzle.origin
        .replaceAll('[?]', ' ')
        .split(/[^\p{L}]+/u)
        .map((word) => fold(word.toLowerCase()))
        .filter((word) => word.length >= 4 && !filler.has(word))
      return words.length < 3
    })
    expect(hollow.map((p) => `${p.word}: ${p.origin}`).slice(0, 6)).toEqual([])
  })

  /**
   * V indicii nesmí být nic, co zní jako hledané slovo.
   *
   * Tohle je hlavní kontrola celého režimu a schválně je napsaná jinak než
   * pravidlo v generátoru: kdyby se obojí měřilo stejným metrem, chyba
   * v metru by prošla oběma. Tady se porovnávají souhláskové kostry
   * (souterrain → STRN, suterén → STRN) a nejdelší společný úsek písmen.
   */
  it('v ničem, co hráč čte, není slovo znějící jako odpověď', () => {
    const sound: Record<string, string> = {
      b: 'P', p: 'P', d: 'T', t: 'T', v: 'F', w: 'F', f: 'F',
      g: 'K', h: 'K', k: 'K', c: 'K', q: 'K', x: 'K',
      s: 'S', z: 'S', m: 'M', n: 'N', r: 'R', l: 'L', j: '', y: '',
    }
    const phon = (raw: string): string => {
      let word = fold(raw.toLowerCase()).replace(/[^a-z]/g, '').replace(/(.)\1+/g, '$1')
      for (const [pair, one] of [['qu', 'kv'], ['ch', 'k'], ['th', 't'], ['ph', 'f'], ['ck', 'k']]) {
        word = word.split(pair!).join(one!)
      }
      return [...word].map((ch) => sound[ch] ?? '').join('').replace(/(.)\1+/g, '$1')
    }
    const shared = (a: string, b: string): number => {
      let best = 0
      for (let i = 0; i < a.length; i++) {
        for (let j = 0; j < b.length; j++) {
          let run = 0
          while (i + run < a.length && j + run < b.length && a[i + run] === b[j + run]) run++
          if (run > best) best = run
        }
      }
      return best
    }

    const leaky: string[] = []
    for (const puzzle of puzzles) {
      const target = fold(puzzle.word.toLowerCase())
      const ear = phon(puzzle.word)
      for (const text of shownWhilePlaying(puzzle)) {
        for (const raw of text.split(/[^\p{L}]+/u)) {
          if (raw.length < 3) continue
          const token = fold(raw.toLowerCase())
          const mine = phon(raw)
          const sounds = ear.length >= 2 && mine.length >= 2 && mine === ear
          const looks = target.length >= 5 && shared(token, target) >= Math.max(4, target.length - 2)
          if (sounds || looks) leaky.push(`${puzzle.word}: „${raw}"`)
        }
      }
    }
    expect(leaky.slice(0, 8)).toEqual([])
  })

  /**
   * Indicie nesmí obsahovat cizojazyčný protějšek hledaného slova.
   *
   * „Převzato z anglického hurricane, jež je odvozeno ze španělského huracán"
   * u slova hurikán se nehádá, jen opisuje. Stejně tak „Z německého Ballast"
   * u balastu. Maskování dřív hlídalo jen společný začátek, a ten se u
   * přejímek často liší uvnitř slova.
   */
  it('nikde není skoro stejné slovo v jiném jazyce', () => {
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
      for (const text of shownWhilePlaying(puzzle)) {
        for (const raw of text.split(/[^\p{L}]+/u)) {
          const token = fold(raw.toLowerCase())
          if (token.length < 5) continue
          if (ratio(token, target) >= 0.8) leaky.push(`${puzzle.word}: „${raw}"`)
        }
      }
    }
    expect(leaky.slice(0, 8)).toEqual([])
  })

  /**
   * Text o původu nesmí skončit uprostřed myšlenky.
   *
   * Text se zkracuje po větách a dělič vět bral tečku za řadovou číslovkou
   * jako konec věty — indicie pak končila „…se na začátku 17." a hráč čekal
   * zbytek, který nikdy nepřišel.
   */
  it('text o původu končí dokončenou větou', () => {
    const truncated = puzzles.filter((puzzle) => {
      const origin = (puzzle.origin ?? '').trim()
      if (!origin) return false
      return (
        !/[.!?]$/.test(origin) ||
        // řadová číslovka bez toho, co počítá („v 18.")
        /\s\d{1,2}\.$/.test(origin) ||
        // Zkratka, po které musí věta pokračovat. Musí před ní stát mezera:
        // `\b` je v JS bez příznaku `u` jen o ASCII, takže „hêr." vypadá
        // jako zkratka „r." a test hlásil planý poplach.
        /(?:^|\s)(?:např|resp|srov|lat|řec|něm|angl|tzv|stol|r)\.$/i.test(origin) ||
        origin.split('(').length !== origin.split(')').length
      )
    })
    expect(truncated.map((p) => `${p.word}: …${p.origin!.slice(-40)}`)).toEqual([])
  })

  it('text je čitelně dlouhý a bez zbytků wikitextu', () => {
    const problems: string[] = []
    for (const puzzle of puzzles) {
      if (puzzle.clue.length < 16 || puzzle.clue.length > 180) {
        problems.push(`${puzzle.word}: ${puzzle.clue.length} znaků`)
      }
      for (const text of [...shownWhilePlaying(puzzle), puzzle.story ?? '']) {
        if (/\[\[|\{\{|<ref|''/.test(text)) problems.push(`${puzzle.word}: wikitext`)
      }
    }
    expect(problems.slice(0, 5)).toEqual([])
  })

  // Hráč si stěžoval, že indicii nerozumí: text vypočítával příbuzná slova
  // („Srovnej např. stožár, stehno"), což je ve slovníku na místě, ale
  // v hádance to jenom mate.
  it('indicie neodkazuje jinam do slovníku', () => {
    const problems: string[] = []
    for (const puzzle of puzzles) {
      for (const text of shownWhilePlaying(puzzle)) {
        // Hranice slova se musí psát přes `\p{L}`: `\b` je v JS bez příznaku
        // `u` jen o ASCII, takže „vizí" vypadá jako odkaz „viz".
        if (/(^|[^\p{L}])(srovnej|srov\.|porovnej|viz)([^\p{L}]|$)/iu.test(text)) {
          problems.push(`${puzzle.word}: odkaz`)
        }
      }
    }
    expect(problems.slice(0, 5)).toEqual([])
  })

  /**
   * Celá etymologie se ukazuje až ve vyhodnocení, kde prozrazovat nemá co.
   *
   * Během hry hráč vidí `origin` se zakrytými místy; `story` je tentýž text
   * nezakrytý a smí do něj patřit i hledané slovo. Kdyby se ta dvě pole
   * někdy prohodila, celý režim by se rozsypal — proto se hlídá, že jdou
   * ruku v ruce a že zakrytá verze je opravdu ta kratší.
   */
  it('nezakrytý původ patří k zakrytému a nikam jinam', () => {
    const problems: string[] = []
    for (const puzzle of puzzles) {
      if (!!puzzle.origin !== !!puzzle.story) {
        problems.push(`${puzzle.word}: původ jen napůl`)
        continue
      }
      if (!puzzle.origin) continue
      if (puzzle.story!.includes('[?]')) problems.push(`${puzzle.word}: zakryté i ve vyhodnocení`)
      if (puzzle.story!.length < puzzle.origin.replaceAll('[?]', '').length) {
        problems.push(`${puzzle.word}: nezakrytá verze je kratší`)
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

  // Otázka dne a Detektiv nesmí hrát na totéž slovo. Hráč by v jednom režimu
  // dostal odpověď z druhého — a ještě týž den.
  it('hádané slovo jde vyhádat po písmenech', () => {
    // Detektiv i Šibenice porovnávají zkoušené písmeno proti složenému tvaru
    // slova. Mezera ani spojovník na klávesnici nejsou, takže by se slovo,
    // které je obsahuje, nedalo nikdy dokončit — kolo by uvázlo.
    const problems = puzzles
      .filter((one) => !/^[a-z]+$/.test(fold(one.word)))
      .map((one) => one.word)
    expect(problems.slice(0, 10)).toEqual([])
  })

  it('nehádá se slovo, na které se ptá Otázka dne', () => {
    const deck = readJson<Record<string, { answer: string; alt?: string[] }[]>>(
      'quiz',
      'deck.json',
    )
    const asked = new Set<string>()
    for (const questions of Object.values(deck)) {
      for (const question of questions) {
        for (const text of [question.answer, ...(question.alt ?? [])]) {
          for (const token of text.split(/[^\p{L}]+/u)) {
            if (token) asked.add(fold(token.toLowerCase()))
          }
        }
      }
    }
    const clash = puzzles.filter((p) => asked.has(fold(p.word.toLowerCase())))
    expect(clash.map((p) => p.word).slice(0, 5)).toEqual([])
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

  it('voština nabízí jen povolené tvary — i mezi vzácnými slovy', () => {
    const problems: string[] = []
    for (const file of readdirSync(join(DATA, 'hive')).filter((f) => f.startsWith('pack-'))) {
      for (const hive of readJson<{ solutions: string[]; extra?: string[] }[]>('hive', file)) {
        // `extra` se uznává stejně jako cíl, takže musí projít stejnou
        // kontrolou — jinak by se do hry zadními vrátky dostal ohnutý tvar.
        for (const word of [...hive.solutions, ...(hive.extra ?? [])]) {
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

describe('vetřelec — vyváženost sady', () => {
  it('žádná rodina nezabírá víc než desetinu své obtížnosti', () => {
    const puzzles = JSON.parse(
      readFileSync('public/data/intruder/puzzles.json', 'utf-8'),
    ) as { difficulty: string; family: string }[]

    for (const level of ['easy', 'normal', 'hard']) {
      const pool = puzzles.filter((one) => one.difficulty === level)
      const counts = new Map<string, number>()
      for (const one of pool) counts.set(one.family, (counts.get(one.family) ?? 0) + 1)
      const worst = Math.max(...counts.values())
      // Dřív měl zvěrokruh pětinu střední obtížnosti a hráč potkával tutéž
      // souvislost pořád dokola. Desetina je strop s rezervou.
      expect(worst / pool.length).toBeLessThan(0.1)
      // Střední a těžkou nesou jen skryté rodiny, a těch je z podstaty míň
      // než rodin se střechou — vymyslet pětici bez viditelné střechy dá
      // práci. Deset je spodní mez, pod kterou by se sada začala opakovat
      // i přes rozestup, který drží hra sama.
      expect(counts.size).toBeGreaterThanOrEqual(10)
    }
  })

  it('vetřelec netrčí už tím, že je jediný psaný velkým písmenem', () => {
    const puzzles = JSON.parse(
      readFileSync('public/data/intruder/puzzles.json', 'utf-8'),
    ) as { words: string[]; odd: string; difficulty: string; family: string }[]

    // Hráči hlásili dvě hádanky v těžké úrovni, které se daly vyřešit bez
    // přemýšlení: *Jan, Václav, Anežka, Kliment* — a mezi nimi **kolík**.
    // Čtyři vlastní jména a jedno obyčejné slovo; vetřelec je vidět dřív,
    // než si člověk stihne přečíst, na co se ptá.
    //
    // Vlastní jméno se pozná strojově podle velkého písmene, takže tohle
    // je jediná část problému, kterou jde uhlídat testem: buď jsou velká
    // všechna, nebo žádné. Zbytek — aby vetřelec nebyl jediné cizí slovo
    // mezi domácími nebo jediná domácí potřeba mezi řemeslnými termíny —
    // řeší stavitel tím, že vetřelce bere ze sousední rodiny téhož druhu.
    const bad = puzzles.filter((one) => {
      const four = one.words.filter((w) => w !== one.odd)
      const velke = (w: string) => w[0] !== w[0]?.toLowerCase()
      return velke(one.odd) !== four.some(velke)
    })
    expect(bad.slice(0, 3)).toEqual([])
  })

  it('každá pětice ví, z jaké je rodiny', () => {
    const puzzles = JSON.parse(
      readFileSync('public/data/intruder/puzzles.json', 'utf-8'),
    ) as { family?: string }[]
    expect(puzzles.every((one) => typeof one.family === 'string' && one.family.length > 0)).toBe(true)
  })

  it('detektiv nehádá přídavné jméno popisem osoby', () => {
    const puzzles = JSON.parse(
      readFileSync('public/data/detective/puzzles.json', 'utf-8'),
    ) as { word: string; clue: string; grammar?: string }[]
    // „vztahovačný — Člověk, který má sklon…" pošle hráče hledat podstatné
    // jméno. Slovník takhle definuje nositele vlastnosti; hádanka to unést
    // nemůže.
    const osoba = /^(?:Člověk|Osoba|Ten,\s*kdo|Ta,\s*kdo|Kdo)\b/i
    const problems = puzzles
      .filter((one) => (one.grammar ?? '').includes('přídavné') && osoba.test(one.clue))
      .map((one) => `${one.word}: ${one.clue.slice(0, 40)}`)
    expect(problems.slice(0, 5)).toEqual([])
  })

  it('plástev uzná každé slovo ze slovníku, které do ní patří', () => {
    const slovnik = JSON.parse(
      readFileSync('tests/fixtures/base-forms.json', 'utf-8'),
    ) as string[]
    const index = JSON.parse(
      readFileSync('public/data/hive/index.json', 'utf-8'),
    ) as { hives: { id: string; pack: number; center: string; outer: string[] }[] }

    // Hráč nahlásil, že Voština nezná *lysiny*. Slovo přitom pravidlům
    // vyhovuje — má aspoň čtyři písmena, obsahuje prostřední a nesahá po
    // ničem, co v plástvi není. Odmítnout takové slovo je chyba, i když je
    // vzácné; proto se vedle cíle veze `extra`.
    const problems: string[] = []
    for (const entry of index.hives.slice(0, 40)) {
      const pack = JSON.parse(
        readFileSync(`public/data/hive/pack-${String(entry.pack).padStart(3, '0')}.json`, 'utf-8'),
      ) as { id: string; solutions: string[]; extra?: string[] }[]
      const hive = pack.find((one) => one.id === entry.id)!
      const uzna = new Set([...hive.solutions, ...(hive.extra ?? [])].map(fold))
      const pismena = new Set([entry.center, ...entry.outer])
      for (const word of slovnik) {
        if (word.length < 4) continue
        const f = fold(word)
        if (!f.includes(entry.center)) continue
        if ([...f].some((ch) => !pismena.has(ch))) continue
        if (!uzna.has(f)) problems.push(`${entry.id}: ${word}`)
      }
    }
    expect(problems.slice(0, 5)).toEqual([])
  })

  it('v pětici nestojí dvě slova z jednoho kořene', () => {
    const puzzles = JSON.parse(
      readFileSync('public/data/intruder/puzzles.json', 'utf-8'),
    ) as { words: string[] }[]
    // „malina" a „malinovka" vedle sebe vypadají jako přehlédnutí, i když
    // do rodiny patří obě.
    const problems = puzzles
      .filter((one) => new Set(one.words.map((w) => fold(w).slice(0, 5))).size < 5)
      .slice(0, 5)
      .map((one) => one.words.join(' '))
    expect(problems).toEqual([])
  })

  it('pětice nenabízí druhou stejně dobrou odpověď', () => {
    const puzzles = JSON.parse(
      readFileSync('public/data/intruder/puzzles.json', 'utf-8'),
    ) as { words: string[]; odd: string; recap: string }[]
    const { skatulky } = JSON.parse(
      readFileSync('tests/fixtures/word-tags.json', 'utf-8'),
    ) as { skatulky: Record<string, string[]> }

    // Hlášená pětice: labuť, plachty, srnec, orel, had — „čtyři z nich jsou
    // souhvězdí", jenže zbylá čtyři slova jsou zvířata a ukazují na
    // plachty. Vadí právě tenhle případ: škatulku sdílí čtyři slova a jedno
    // z nich je vetřelec. Když ji sdílí všech pět nebo právě ta čtveřice
    // zevnitř, nikoho to nevyděluje nebo to vydělí téhož vetřelce.
    const problems: string[] = []
    for (const [tag, list] of Object.entries(skatulky)) {
      const set = new Set(list)
      for (const one of puzzles) {
        const n = one.words.filter((w) => set.has(w)).length
        if (n === 4 && set.has(one.odd)) problems.push(`${tag}: ${one.words.join(' ')}`)
      }
    }
    expect(problems.slice(0, 5)).toEqual([])
  })

  it('id pětice se odvozuje z jejího obsahu, ne z pořadí', () => {
    const puzzles = JSON.parse(
      readFileSync('public/data/intruder/puzzles.json', 'utf-8'),
    ) as { id: string; words: string[]; odd: string; answer: string; family: string }[]

    // Tohle rozbíjelo souboje: id se dřív rozdávala podle pořadí v hotové
    // sadě (`i-0000`, `i-0001`, …) po zamíchání, takže je každé přestavění
    // dat celá přeházelo. Zápas si přitom drží jen id — a když měl každý
    // telefon jinou verzi dat, přeložil si tatáž id na **jiné pětice** a
    // hráči v jednom souboji odpovídali každý na něco jiného.
    const rozbite: string[] = []
    for (const one of puzzles) {
      // Jazykové pětice se staví z Wikislovníku a mají vlastní klíč.
      if (one.family?.startsWith('jaz:')) continue
      const zaklad = `${[...one.words].sort().join('|')}>${one.odd}>${one.answer}`
      const cekany = `i-${createHash('sha1').update(zaklad, 'utf8').digest('hex').slice(0, 10)}`
      if (one.id !== cekany) rozbite.push(`${one.id} != ${cekany} (${one.words.join(' ')})`)
    }
    expect(rozbite.slice(0, 5)).toEqual([])

    // A žádná dvě id nesmí ukazovat na dvě různé pětice.
    expect(new Set(puzzles.map((one) => one.id)).size).toBe(puzzles.length)
  })

  it('pětice nejde vyřešit hruběji, než na co se ptá', () => {
    const puzzles = JSON.parse(
      readFileSync('public/data/intruder/puzzles.json', 'utf-8'),
    ) as { words: string[]; odd: string; answer: string }[]
    const { skatulky, osy_skatulek } = JSON.parse(
      readFileSync('tests/fixtures/word-tags.json', 'utf-8'),
    ) as { skatulky: Record<string, string[]>; osy_skatulek: string[] }

    // Hlášená pětice: lavička, opice, tygr, drak, krysa — „čtyři z nich jsou
    // znamení čínského zvěrokruhu". O zvěrokruhu se hráč nemusel dozvědět
    // nic: stačilo vidět, že kromě lavičky jsou to zvířata. Vetřelec musí
    // ležet ve stejném soudku jako čtveřice, jinak je osa na ozdobu.
    //
    // Výjimka jsou rodiny, které se na tu škatulku ptají samy („čtyři z nich
    // jsou psi" — nad zvířetem už nic hrubšího není).
    const osy = new Set(osy_skatulek)
    const problems: string[] = []
    for (const [tag, list] of Object.entries(skatulky)) {
      const set = new Set(list)
      const patri = (w: string) => set.has(w) || w.split(' ').some((p) => set.has(p))
      for (const one of puzzles) {
        if (osy.has(one.answer)) continue
        const four = one.words.filter((w) => w !== one.odd)
        if (four.length === 4 && four.every(patri) && !patri(one.odd)) {
          problems.push(`${tag}: ${one.words.join(' ')} (${one.answer})`)
        }
      }
    }
    expect(problems.slice(0, 5)).toEqual([])
  })

  it('v pětici se totéž neschovává dvakrát', () => {
    const puzzles = JSON.parse(
      readFileSync('public/data/intruder/puzzles.json', 'utf-8'),
    ) as { words: string[]; family: string }[]
    const { skryte } = JSON.parse(
      readFileSync('tests/fixtures/word-tags.json', 'utf-8'),
    ) as { skryte: Record<string, Record<string, string>> }

    // „malinovka" i „maximalista" nesou Mali. Osa sedí, ale hráči to
    // připadá jako přehlédnutí — čtveřice má schovávat čtyři různé věci.
    const problems: string[] = []
    for (const one of puzzles) {
      const map = skryte[one.family]
      if (!map) continue
      const found = one.words.map((w) => map[w]).filter(Boolean)
      if (new Set(found).size < found.length) problems.push(one.words.join(' '))
    }
    expect(problems.slice(0, 5)).toEqual([])
  })

  it('věta do vyhodnocení sedí do rámce „Čtyři z nich …"', () => {
    const puzzles = JSON.parse(
      readFileSync('public/data/intruder/puzzles.json', 'utf-8'),
    ) as { recap: string }[]
    // Rámec rozbíjí jednotné číslo („Čtyři z nich je to polévka"), příklonka
    // na špatném místě („čtou se stejně" místo „se čtou stejně") a zástupka
    // za slovo, které už stojí v podmětu („sedá se na ně").
    const spatne = [' je to ', ' bývá to ', ' to ', ' na ně ', ' jim ']
    const problems = new Set<string>()
    for (const one of puzzles) {
      const at = one.recap.indexOf('Čtyři z nich ')
      if (at < 0) continue
      const veta = one.recap.slice(at + 'Čtyři z nich'.length).split(' — ')[0]!
      for (const kus of spatne) if (veta.includes(kus)) problems.add(veta.trim())
    }
    expect([...problems].slice(0, 5)).toEqual([])
  })
})
