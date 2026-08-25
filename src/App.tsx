/** Kořen aplikace — téma, profil, výběr hádanek a přepínání obrazovek. */

import { useCallback, useEffect, useMemo, useRef, useState } from 'react'

import {
  loadChain,
  loadHive,
  loadDetective,
  loadIntruder,
  loadQuotes,
  loadTetris,
  loadGallows,
  loadHiveIndex,
  loadQuiz,
  loadTower,
  loadTowerIndex,
  pickUnseen,
  type ChainBundle,
} from './app/data'
import {
  DuelContext,
  NextUpContext,
  ReportContext,
  RoundModeContext,
  type NextUpItem,
} from './app/nextUp'
import { restore, stillDaily } from './app/resume'
import { AwardPopup, type Gained } from './components/AwardPopup'
import { Awards } from './components/Awards'
import { InkMark } from './components/art/InkMark'
import { RankBadge } from './components/art/RankBadge'
import { ChainGame } from './components/ChainGame'
import { DetectiveGame } from './components/DetectiveGame'
import { Confirm } from './components/Confirm'
import { Explain, ExplainProvider } from './components/Explain'
import { GallowsGame } from './components/GallowsGame'
import { Guide } from './components/Guide'
import { HiveGame } from './components/HiveGame'
import { Home } from './components/Home'
import { QuizGame } from './components/QuizGame'
import { IntruderGame } from './components/IntruderGame'
import { DuelHive } from './components/DuelHive'
import { DuelIntruder } from './components/DuelIntruder'
import { DuelSetup } from './components/DuelSetup'
import { Friends, type DuelReport } from './components/Friends'
import { ReportSheet } from './components/ReportSheet'
import { FriendsEntry } from './components/FriendsEntry'
import { QuotesGame } from './components/QuotesGame'
import { QuizReview } from './components/QuizReview'
import { Splash } from './components/Splash'
import { Stats } from './components/Stats'
import { Tutorial } from './components/Tutorial'
import { TetrisGame } from './components/TetrisGame'
import { TowerGame } from './components/TowerGame'
import type { ChainPuzzle, ChainState } from './game/chain'
import type { DetectivePuzzle, DetectiveState } from './game/detective'
import type { ExplainTarget } from './game/glossary'
import type { GallowsPuzzle, GallowsState } from './game/gallows'
import type { HivePuzzle, HiveState } from './game/hive'
import { quizFor, type QuizDeck, type QuizQuestion, type QuizState } from './game/quiz'
import {
  dailyIntruder,
  pickIntruder,
  type IntruderPuzzle,
  type IntruderState,
} from './game/intruder'
import type { Challenge, Match } from './lib/multi'
import {
  blockPlayer,
  createMatch,
  dropChallenge,
  eraseMe,
  reportPlayer,
  forgetMatch,
  loadMatch,
  loadMe,
  matchDone,
  MULTI_ON,
  myUid,
  playRound,
  recordDuel,
  rememberMatch,
  saveMe,
  saveTally,
  serverNow,
  startMatch,
  tallyWith,
  watchChallenges,
  type Duel,
  type Me,
} from './lib/multi'
import {
  DUEL_MODE,
  DUEL_TITLE,
  INTRUDER_ROUNDS,
  type DuelKind,
  type Verdict,
} from './game/duel'
import { upozorni } from './lib/upozorneni'
import type { Quote, QuoteState } from './game/quotes'
import { RANKS, rankFor } from './game/ranks'
import { tetrisSetup, type TetrisDeck, type TetrisSetup, type TetrisState } from './game/tetris'
import type { TowerPuzzle, TowerState } from './game/tower'
import {
  MODE_GLYPH,
  MODE_LABEL,
  MODE_ORDER,
  type Difficulty,
  type ModeId,
  type RoundResult,
} from './game/types'
import { useBackGuard } from './lib/back'
import { dayNumber, hashSeed, mulberry32, todayKey } from './lib/rng'
import {
  breakStreak,
  emptyProfile,
  liveStreak,
  loadProfile,
  loadQuizRound,
  loadRounds,
  recordQuiz,
  recordRound,
  roundSlot,
  saveProfile,
  saveQuizRound,
  saveRounds,
  spendInk,
  type Profile,
  type SavedQuiz,
  type SavedRound,
  type SavedRounds,
} from './lib/storage'

type View =
  | { kind: 'home' }
  | { kind: 'stats' }
  | { kind: 'awards' }
  | { kind: 'game'; mode: ModeId; daily: boolean; nonce: number }
  // Souboj dvou jmenovitých hráčů. Nemá obtížnost ani denní várku a body
  // z něj nejdou do věhlasu, takže s `game` nemá společného skoro nic.
  | { kind: 'duel' }
  // Nabídka soubojů. Stojí mimo hry — nedává věhlas, nebere inkoust
  // a nepočítá se do denní várky.
  | { kind: 'friends' }
  // Otázka dne stojí mimo šestici — nemá obtížnost ani rozehrané kolo,
  // takže se do `game` nevejde.
  | { kind: 'quiz' }
  // Přehled všech otázek. Jen v kontrolním buildu, viz QuizReview.
  | { kind: 'quizlist' }

interface Loaded {
  chain?: { bundle: ChainBundle; puzzle: ChainPuzzle }
  hive?: HivePuzzle
  tower?: TowerPuzzle
  gallows?: GallowsPuzzle
  detective?: DetectivePuzzle
  quotes?: { quote: Quote; seed: number }
  intruder?: IntruderPuzzle
  tetris?: { deck: TetrisDeck; setup: TetrisSetup }
  quiz?: QuizQuestion
  quizDeck?: QuizDeck
}

export default function App() {
  const [profile, setProfile] = useState<Profile>(() => loadProfile())
  /**
   * Souboje. Drží se stranou od profilu, protože se nepočítají do věhlasu
   * ani do ocenění — dvojice kamarádů by si jinak hodnosti vyfarmila.
   */
  const [me, setMe] = useState<Me>(() => loadMe())
  const [duel, setDuel] = useState<Duel | null>(null)
  const [challenges, setChallenges] = useState<Challenge[]>([])
  /** Rozehraný zápas a hádanky, které si nese. */
  const [match, setMatch] = useState<Match | null>(null)
  const [matchHive, setMatchHive] = useState<HivePuzzle | null>(null)
  const [matchIntruder, setMatchIntruder] = useState<IntruderPuzzle[] | null>(null)
  /** Vlastní skryté id. Potřebuje ho jen souboj, tak se zjistí až s ním. */
  const [uid, setUid] = useState('')
  const [setup, setSetup] = useState(false)
  const [reports, setReports] = useState<DuelReport[]>([])
  /** Koho hráč právě nahlašuje. Panel drží App, ať se dá otevřít odkudkoli. */
  const [reporting, setReporting] = useState<{ uid: string; nick: string } | null>(null)
  /** Otevřené potvrzení mazání dat. */
  const [erasing, setErasing] = useState(false)
  const [view, setView] = useState<View>({ kind: 'home' })
  const [loaded, setLoaded] = useState<Loaded>({})
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  /** Otevřený návod. `pending` = otevřel se sám před první hrou režimu. */
  const [tutorial, setTutorial] = useState<{ mode: ModeId; pending: boolean } | null>(
    null,
  )
  /**
   * Průvodce celou hrou. Při úplně prvním spuštění se otevře sám — je to
   * jediné místo, kde se hráč dozví, co je věhlas a odkud se bere inkoust.
   */
  const [guide, setGuide] = useState(false)
  /** Rozehraná kola, jedno od každého režimu — nabídnou se na úvodní obrazovce. */
  const [saved, setSaved] = useState<SavedRounds>(() => loadRounds())
  /** Stav, se kterým se má hra nastartovat, když hráč klikne na Pokračovat. */
  const [resume, setResume] = useState<unknown>(null)
  /** Úvodní značka. Hra se pod ní mezitím načítá, takže nikoho nezdržuje. */
  const [splash, setSplash] = useState(true)
  /** Co hráči za poslední kolo přibylo — ukáže se nad výsledkem. */
  const [gained, setGained] = useState<Gained | null>(null)
  /**
   * O kolik dní dopředu se v Otázce dne kouká. V ostré hře vždycky nula —
   * otázka je jedna denně. V kontrolním buildu se tím listuje bankou, aby
   * šlo dvě stě otázek přečíst dřív než za dvě stě dní.
   */
  const [quizOffset, setQuizOffset] = useState(0)
  /** Rozehraná Otázka dne. Drží se stranou od kol — otázka není režim. */
  const [quizRound, setQuizRound] = useState<SavedQuiz | null>(() => loadQuizRound())
  /**
   * Kdy začalo kolo, které je na obrazovce.
   *
   * Nastavuje ho ten, kdo kolo otevřel: nové kolo teď, obnovené tím časem,
   * který má uložený ve svém stavu. Podle toho běží lišta a hráč vidí
   * tentýž čas, ze kterého se počítá bonus za rychlost.
   */
  const [roundStart, setRoundStart] = useState(() => Date.now())

  const rank = rankFor(profile.fame)
  const dayKey = todayKey()
  /**
   * Denní série hry, která je právě rozehraná.
   *
   * Bere se z profilu, ne z výsledku kola: dokud hráč dnešní výzvu nedohraje,
   * ukazuje se řada, kterou má za sebou, a teprve po dohrání povyroste.
   */
  const dailyStreak =
    view.kind === 'game' && view.daily
      ? liveStreak(profile.dailyStreak[view.mode], dayKey)
      : 0
  /**
   * Číslo dne do sdíleného textu.
   *
   * Na obrazovce nemá co dělat — hráči nic neříká a v hlavičce zabíralo
   * místo, kvůli kterému padal kalamář za okraj. Ve sdíleném výsledku smysl
   * má: podle něj se pozná, že dva lidé řešili tutéž hádanku.
   */
  const dayTag = `#${dayNumber()}`

  useEffect(() => {
    saveProfile(profile)
  }, [profile])

  // Téma
  useEffect(() => {
    const root = document.documentElement
    if (profile.theme === 'system') root.removeAttribute('data-theme')
    else root.setAttribute('data-theme', profile.theme)
  }, [profile.theme])

  const updateProfile = useCallback((patch: (previous: Profile) => Profile) => {
    setProfile(patch)
  }, [])

  /**
   * Co hráči přibylo, se pozná až na hotovém profilu.
   *
   * Ocenění uděluje `recordRound` uvnitř aktualizace stavu a ta musí zůstat
   * čistá — oznámení se proto odvodí až tady, porovnáním s poslední viděnou
   * podobou. První průchod jen zapamatuje, co profil má, aby po zapnutí hry
   * nevyskočilo všechno, co hráč nasbíral dřív.
   */
  const seenAwards = useRef<Set<string> | null>(null)
  const seenRank = useRef(0)
  useEffect(() => {
    const rank = rankFor(profile.fame).rank.index
    const ids = Object.keys(profile.awards)
    if (seenAwards.current === null) {
      seenAwards.current = new Set(ids)
      seenRank.current = rank
      return
    }
    const fresh = ids.filter((id) => !seenAwards.current!.has(id))
    const promoted = rank > seenRank.current
    seenAwards.current = new Set(ids)
    seenRank.current = rank
    if (fresh.length > 0 || promoted) {
      setGained({ rank: promoted ? rank : null, awards: fresh })
    }
  }, [profile.awards, profile.fame])

  /** Načte hádanku pro daný režim. Denní výzva je deterministická podle data. */
  const startRound = useCallback(
    async (mode: ModeId, daily: boolean) => {
      setLoading(true)
      setError(null)
      setResume(null)
      setRoundStart(Date.now())
      const difficulty = profile.difficulty[mode]
      const random = daily
        ? mulberry32(hashSeed(`${dayKey}:${mode}`))
        : mulberry32((Math.random() * 2 ** 32) >>> 0)

      try {
        if (mode === 'chain') {
          const bundle = await loadChain(difficulty)
          const puzzle = daily
            ? bundle.puzzles[Math.floor(random() * bundle.puzzles.length)]!
            : pickUnseen(bundle.puzzles, (p) => p.id, profile.seen.chain, random)
          setLoaded({ chain: { bundle, puzzle } })
        } else if (mode === 'hive') {
          const index = await loadHiveIndex()
          const pool = index.hives.filter((h) => h.difficulty === difficulty)
          const entries = pool.length > 0 ? pool : index.hives
          const entry = daily
            ? entries[Math.floor(random() * entries.length)]!
            : pickUnseen(entries, (e) => e.id, profile.seen.hive, random)
          setLoaded({ hive: await loadHive(entry) })
        } else if (mode === 'detective') {
          const words = await loadDetective()
          const pool = words.filter((w) => w.difficulty === difficulty)
          const entries = pool.length > 0 ? pool : words
          const entry = daily
            ? entries[Math.floor(random() * entries.length)]!
            : pickUnseen(entries, (e) => e.id, profile.seen.detective, random)
          setLoaded({ detective: entry })
        } else if (mode === 'intruder') {
          const all = await loadIntruder()
          const pool = all.filter((p) => p.difficulty === difficulty)
          const entries = pool.length > 0 ? pool : all
          // Vetřelec se nevybírá jako ostatní hry. Kdyby se bralo jen „co
          // hráč ještě neviděl", chodily by pětice ze stejné rodiny za sebou
          // — pořád jiná slova, pořád tentýž nápad. Střídání rodin má proto
          // vlastní pravidla, viz `pickIntruder` a `dailyIntruder`.
          const entry = daily
            ? dailyIntruder(entries, dayNumber(), random)
            : pickIntruder(entries, profile.seen.intruder, random)
          setLoaded({ intruder: entry })
        } else if (mode === 'quotes') {
          const all = await loadQuotes()
          const pool = all.filter((q) => q.difficulty === difficulty)
          const entries = pool.length > 0 ? pool : all
          // Bez připojení nemá smysl nabízet výrok, jehož jediná obrazová
          // nápověda by se stejně nestáhla — u volné hry se proto dá
          // přednost těm bez podobizny. Denní výzva musí padnout všem
          // stejná, takže tam se nevybírá.
          const offline = typeof navigator !== 'undefined' && navigator.onLine === false
          const usable = offline && !daily ? entries.filter((q) => !q.art) : entries
          const from = usable.length > 0 ? usable : entries
          const entry = daily
            ? from[Math.floor(random() * from.length)]!
            : pickUnseen(from, (e) => e.id, profile.seen.quotes, random)
          setLoaded({
            quotes: {
              quote: entry,
              seed: daily ? hashSeed(`${dayKey}:quotes`) : (Math.random() * 2 ** 32) >>> 0,
            },
          })
        } else if (mode === 'tetris') {
          // Tenhle režim nemá připravené hádanky — rozdává se náhodně, takže
          // stačí zrnko. Denní výzva ho má odvozené ze dne, takže všem padá
          // stejná řada dvojic.
          const deck = await loadTetris()
          const seed = daily
            ? hashSeed(`${dayKey}:tetris`)
            : (Math.random() * 2 ** 32) >>> 0
          setLoaded({ tetris: { deck, setup: tetrisSetup(difficulty, seed) } })
        } else if (mode === 'gallows') {
          const words = await loadGallows()
          const pool = words.filter((w) => w.difficulty === difficulty)
          const entries = pool.length > 0 ? pool : words
          const entry = daily
            ? entries[Math.floor(random() * entries.length)]!
            : pickUnseen(entries, (e) => e.id, profile.seen.gallows, random)
          setLoaded({ gallows: entry })
        } else {
          const index = await loadTowerIndex()
          const pool = index.towers.filter((t) => t.difficulty === difficulty)
          const entries = pool.length > 0 ? pool : index.towers
          const entry = daily
            ? entries[Math.floor(random() * entries.length)]!
            : pickUnseen(entries, (e) => e.id, profile.seen.tower, random)
          setLoaded({ tower: await loadTower(entry) })
        }
        setView((previous) => ({
          kind: 'game',
          mode,
          daily,
          nonce: previous.kind === 'game' ? previous.nonce + 1 : 1,
        }))
        setSaved((previous) => {
          // Zahodí se jen kolo téhož druhu. Rozehraná denní výzva a volná
          // hra téže hry leží každá jinde, takže se nepřepisují.
          const { [roundSlot(mode, daily)]: _dropped, ...rest } = previous
          saveRounds(rest)
          return rest
        })
        // Při prvním spuštění režimu se návod otevře sám nad rozehranou hrou.
        if (!profile.tutorialSeen[mode]) setTutorial({ mode, pending: true })
      } catch (cause) {
        setError(cause instanceof Error ? cause.message : 'Data se nepodařilo načíst')
      } finally {
        setLoading(false)
      }
    },
    [dayKey, profile.difficulty, profile.seen, profile.tutorialSeen],
  )

  /** Obnoví kolo přerušené odchodem do menu nebo zavřením hry. */
  const resumeRound = useCallback(
    async (round: SavedRound) => {
      setLoading(true)
      setError(null)
      try {
        const back = restore(round)
        if (!back) throw new Error('Uložené kolo už nejde otevřít')
        if (back.mode === 'chain') {
          // Jediný režim, který k hádance potřebuje ještě graf slov.
          setLoaded({ chain: { bundle: await loadChain(round.difficulty), puzzle: back.puzzle } })
        } else if (back.mode === 'tetris') {
          setLoaded({ tetris: { deck: back.deck, setup: back.setup } })
        } else if (back.mode === 'quotes') {
          // Odkrytá slova si stav nese s sebou, takže se seed k ničemu
          // nepotřebuje — hádanka se z něj losuje jen na začátku kola.
          setLoaded({ quotes: { quote: back.quote, seed: 0 } })
        } else {
          setLoaded({ [back.mode]: back.puzzle })
        }
        setResume(round.state)
        const started = (round.state as { startedAt?: number }).startedAt
        setRoundStart(typeof started === 'number' ? started : Date.now())
        setView((previous) => ({
          kind: 'game',
          mode: round.mode,
          daily: stillDaily(round, dayKey, (at) => todayKey(new Date(at))),
          nonce: previous.kind === 'game' ? previous.nonce + 1 : 1,
        }))
      } catch (cause) {
        setError(cause instanceof Error ? cause.message : 'Kolo se nepodařilo obnovit')
        setSaved((previous) => {
          const { [roundSlot(round.mode, round.daily)]: _dropped, ...rest } = previous
          saveRounds(rest)
          return rest
        })
      } finally {
        setLoading(false)
      }
    },
    [dayKey],
  )

  /**
   * Spuštění z menu.
   *
   * Denní výzva se ťuká z dlaždice a ta dřív začínala **vždycky znovu** —
   * kdo si v půlce odskočil a dlaždici zmáčkl podruhé, přišel o postup
   * i o čas. Rozehraná dnešní výzva se proto otevře tam, kde skončila;
   * volná hra z panelu si dál začíná od začátku, protože „Pokračovat" má
   * v panelu vlastní tlačítko a hráč si vybírá.
   */
  const play = useCallback(
    (mode: ModeId, daily: boolean) => {
      const round = saved[roundSlot(mode, true)]
      if (daily && round && stillDaily(round, dayKey, (at) => todayKey(new Date(at)))) {
        void resumeRound(round)
        return
      }
      void startRound(mode, daily)
    },
    [dayKey, resumeRound, saved, startRound],
  )

  /**
   * Průběžné ukládání. Volá se po každém tahu, takže se kolo dá dohrát i po
   * návratu do menu nebo po zavření prohlížeče. Dohrané kolo se maže —
   * nabízet „pokračovat" u něčeho hotového nedává smysl.
   */
  const keepProgress = useCallback(
    (mode: ModeId, puzzleId: string, difficulty: Difficulty, state: unknown, over: boolean) => {
      const daily = view.kind === 'game' ? view.daily : false
      const slot = roundSlot(mode, daily)
      setSaved((previous) => {
        let next: SavedRounds
        if (over) {
          const { [slot]: _dropped, ...rest } = previous
          next = rest
        } else {
          const round: SavedRound = {
            mode,
            daily,
            difficulty,
            puzzleId,
            state,
            savedAt: Date.now(),
          }
          next = { ...previous, [slot]: round }
        }
        saveRounds(next)
        return next
      })
    },
    [view],
  )

  /**
   * Souboj o denní výzvu.
   *
   * Odesílá se až po dohraném kole, takže na server nikdy nečeká hra, jen
   * karta výsledku. Soupeř nemusí být online — hledá se mezi těmi, kdo
   * hráli tutéž hádanku, třeba včera.
   */
  const duelRound = useCallback(
    (result: RoundResult, band: number) => {
      if (!MULTI_ON || !me.nick) return
      void playRound(result.mode, result.puzzleId, result.score, band, me.blocked ?? [])
        .then(async (found) => {
          if (!found) return
          setDuel(found)
          const next = { ...me, ...(await recordDuel(found, me)) }
          saveMe(next)
          setMe(next)
        })
        .catch(() => undefined)
    },
    [me],
  )

  /* ---------- souboje na jmenovitého soupeře ---------- */

  /**
   * Hádanky pro souboj.
   *
   * Vybírá je vyzývatel a zápas si je nese s sebou; soupeř pak hraje přesně
   * to samé. Obtížnost se bere z vyzývatelova nastavení — hraje ji stejně
   * oba, takže nikoho nezvýhodní.
   */
  const duelPuzzles = useCallback(
    async (kind: DuelKind) => {
      if (kind === 'hive') {
        const index = await loadHiveIndex()
        const pool = index.hives.filter((h) => h.difficulty === profile.difficulty.hive)
        const entries = pool.length > 0 ? pool : index.hives
        const entry = entries[Math.floor(Math.random() * entries.length)]!
        return { ids: [entry.id], hive: await loadHive(entry), intruder: null }
      }
      const all = await loadIntruder()
      const pool = all.filter((p) => p.difficulty === profile.difficulty.intruder)
      const entries = pool.length >= INTRUDER_ROUNDS ? pool : all
      // Tři kola souboje po sobě, takže se rodiny musí střídat i tady —
      // tři pětice ze zvěrokruhu za sebou by byl jeden nápad třikrát.
      const chosen: IntruderPuzzle[] = []
      const used: string[] = []
      for (let round = 0; round < INTRUDER_ROUNDS; round += 1) {
        const one = pickIntruder(entries, used, Math.random)
        used.push(one.id)
        chosen.push(one)
      }
      return { ids: chosen.map((one) => one.id), hive: null, intruder: chosen }
    },
    [profile.difficulty.hive, profile.difficulty.intruder],
  )

  /** Tytéž hádanky na straně soupeře — hledají se podle id ze zápasu. */
  const duelPuzzlesOf = useCallback(async (found: Match) => {
    if (found.kind === 'hive') {
      const index = await loadHiveIndex()
      const entry = index.hives.find((h) => h.id === found.puzzles[0])
      if (!entry) throw new Error('Plástev ze souboje se nenašla')
      return { hive: await loadHive(entry), intruder: null }
    }
    const all = await loadIntruder()
    const chosen = found.puzzles
      .map((id) => all.find((one) => one.id === id))
      .filter((one): one is IntruderPuzzle => Boolean(one))
    if (chosen.length === 0) throw new Error('Pětice ze souboje se nenašly')
    return { hive: null, intruder: chosen }
  }, [])

  /** Odešle výzvu a rovnou se do souboje pustí. */
  const sendDuel = useCallback(
    async (kind: DuelKind, nick: string, krok: (co: string) => void): Promise<boolean> => {
      // Dvě fáze, dvě různá čekání: hádanky se stahují ze stejné adresy jako
      // hra, zápas se zakládá v databázi. Když se to zasekne, musí být na
      // první pohled poznat, která z nich stojí.
      krok('Chystám hádanky…')
      const picked = await duelPuzzles(kind)
      krok('Posílám výzvu…')
      const created = await createMatch(kind, picked.ids, nick)
      if (!created) return false
      setUid(await myUid())
      setMatchHive(picked.hive)
      setMatchIntruder(picked.intruder)
      setMatch(created)
      setMe((previous) => rememberMatch(previous, created.id))
      setSetup(false)
      setView({ kind: 'duel' })
      return true
    },
    [duelPuzzles],
  )

  /** Přijme došlou výzvu. */
  const acceptDuel = useCallback(
    async (item: Challenge) => {
      setLoading(true)
      setError(null)
      void dropChallenge(item.id)
      setChallenges((list) => list.filter((one) => one.id !== item.id))
      try {
        const found = await loadMatch(item.match)
        if (!found) throw new Error('Souboj už neexistuje')
        // Voština se hraje naráz, takže má smysl jen dokud vyzývatel čeká.
        // Že u ní sedí, hlásí každých pět vteřin.
        if (found.kind === 'hive' && (found.live !== 0 || serverNow() - found.ping > 15_000)) {
          throw new Error(`${found.hostNick} už u výzvy nesedí. Vyzvi ho zpátky.`)
        }
        const picked = await duelPuzzlesOf(found)
        await startMatch(found.id)
        setUid(await myUid())
        setMatchHive(picked.hive)
        setMatchIntruder(picked.intruder)
        setMatch({ ...found, live: serverNow() })
        setView({ kind: 'duel' })
      } catch (cause) {
        setError(cause instanceof Error ? cause.message : 'Souboj se nepodařilo otevřít')
      } finally {
        setLoading(false)
      }
    },
    [duelPuzzlesOf],
  )

  /**
   * Nahlášení a zablokování.
   *
   * Obojí se děje naráz: kdo si dal práci s nahlášením, nechce toho člověka
   * vidět dál. Zablokování je místní a platí i tehdy, když se hlášení
   * nepodaří odeslat — na síti tedy nezávisí.
   */
  const reportAndBlock = useCallback((uid: string, nick: string, reason: string) => {
    void reportPlayer(uid, nick, reason)
    setMe((previous) => blockPlayer(previous, uid))
    setChallenges((list) => list.filter((one) => one.from !== uid))
    setDuel((current) => (current?.uid === uid ? null : current))
  }, [])

  /** Souboj je rozhodnutý — připíše se do bilance a zmizí z rozehraných. */
  const closeDuel = useCallback((id: string, verdict: Verdict) => {
    setMe((previous) => {
      const next = tallyWith(forgetMatch(previous, id), verdict === 'draw' ? null : verdict === 'win')
      saveMe(next)
      void saveTally(next)
      return next
    })
  }, [])

  const finishRound = useCallback(
    (result: RoundResult) => {
      const isDailyRound = view.kind === 'game' && view.daily
      setSaved((previous) => {
        const { [roundSlot(result.mode, isDailyRound)]: _dropped, ...rest } = previous
        saveRounds(rest)
        return rest
      })
      setDuel(null)
      if (view.kind === 'game' && view.daily) {
        duelRound(result, rankFor(profile.fame).rank.index)
      }
      updateProfile((previous) => {
        const isDaily = view.kind === 'game' && view.daily
        // Zapsat výsledek smí jen první dnešní pokus. Druhý by přepsal skóre
        // a hlavně by znovu odemkl várku i s odměnou.
        const first = isDaily && previous.dailyDone[`${dayKey}:${result.mode}`] === undefined
        const next = recordRound(previous, result, dayKey, isDaily)
        if (!first) return next
        return {
          ...next,
          dailyDone: { ...next.dailyDone, [`${dayKey}:${result.mode}`]: result.score },
        }
      })
    },
    [dayKey, duelRound, profile.fame, updateProfile, view],
  )

  const giveUp = useCallback(() => {
    setSaved((previous) => {
      if (view.kind !== 'game') return previous
      const { [roundSlot(view.mode, view.daily)]: _dropped, ...rest } = previous
      saveRounds(rest)
      return rest
    })
    updateProfile(breakStreak)
    setView({ kind: 'home' })
  }, [updateProfile, view])

  const spendInkOn = useCallback(
    (price: number) => updateProfile((profile) => spendInk(profile, price)),
    [updateProfile],
  )

  const goHome = useCallback(() => setView({ kind: 'home' }), [])

  /*
   * Došlé výzvy se poslouchají, dokud je otevřené menu.
   *
   * Voština v souboji se hraje naráz, takže výzva musí dorazit hned — kdyby
   * se jen jednou přečetla při vstupu do menu, vyzývatel by čekal u něčeho,
   * o čem soupeř neví. Uvnitř hry se posloucháni ukončí; tam by jen ubíralo
   * spojení, které hra sama nepotřebuje.
   */
  const outside = view.kind === 'home' || view.kind === 'friends'
  useEffect(() => {
    if (!MULTI_ON || !me.nick) return
    return watchChallenges(setChallenges, me.blocked ?? [])
  }, [me.nick, me.blocked])

  /*
   * Upozornění na došlou výzvu.
   *
   * Ohlásí se každá výzva, kterou hráč ještě neviděl — i když je zrovna
   * v jiné hře nebo má hru schovanou na pozadí. Ohlašuje se jen to, co
   * přibylo: seznam chodí celý pokaždé, takže bez pamatování už ohlášených
   * by se při každé změně ozvalo všechno znovu.
   *
   * Když je aplikace úplně zavřená, upozornění nepřijde — na to je potřeba
   * server, který zprávu odešle. Víc je v `lib/upozorneni.ts`.
   */
  const ohlasene = useRef<Set<string>>(new Set())
  const ohlaseniPripraveno = useRef(false)
  useEffect(() => {
    if (!MULTI_ON) return
    const nove = challenges.filter((one) => !ohlasene.current.has(one.id))
    for (const one of challenges) ohlasene.current.add(one.id)
    if (nove.length === 0) return
    // První načtení po spuštění se neohlašuje: hráč se na výzvy dívá právě
    // teď a upozornění na to, co má před očima, je otravné.
    if (!ohlaseniPripraveno.current) {
      ohlaseniPripraveno.current = true
      return
    }
    const prvni = nove[0]!
    upozorni(
      nove.length === 1 ? `${prvni.nick} tě vyzývá` : `${nove.length} nových výzev`,
      nove.length === 1
        ? `${DUEL_TITLE[prvni.kind]} — ťukni a pusť se do toho.`
        : 'Někdo na tebe čeká v Hře s přáteli.',
    ).catch(() => undefined)
  }, [challenges])

  /*
   * Dohrané zápasy, o kterých hráč ještě neví.
   *
   * U Vetřelce si vyzývatel odehraje svoje tři kola hned a soupeř třeba až
   * druhý den; výsledek se proto vyzvedává tady, při návratu do menu.
   */
  useEffect(() => {
    const waiting = me.matches ?? []
    if (!MULTI_ON || !me.nick || !outside || waiting.length === 0) return
    let dead = false
    void (async () => {
      const mine = await myUid()
      const out: DuelReport[] = []
      for (const id of waiting) {
        const found = await loadMatch(id)
        if (!found) continue
        const done = await matchDone(id)
        const own = done[mine]
        const theirs = done[found.host === mine ? found.guest : found.host]
        if (own && theirs) {
          out.push({ id, kind: found.kind, rival: theirs.nick, mine: own.score, theirs: theirs.score })
        }
      }
      if (!dead) setReports(out)
    })().catch(() => undefined)
    return () => {
      dead = true
    }
  }, [me.matches, me.nick, outside])

  /**
   * Hodiny kola v liště.
   *
   * Bonus za rychlost se dřív počítal ze skrytého času — hráč viděl až
   * v rozpisu, že o něj přišel. Ťuknutím se otevře, jak se počítá.
   *
   * Měří se od chvíle, kdy kolo **začalo**, ne od chvíle, kdy je hráč
   * otevřel. Když se vrátí k rozehranému kolu, navazují hodiny tam, kde
   * skutečně jsou: čas běží i mimo hru a skóre se z něj počítá, takže
   * vynulovaná lišta by hráči lhala. Odsud se taky bere `startedAt`
   * z uloženého stavu — jiné místo, kde by ho lišta vzala, není.
   *
   * Sekundy se dopočítávají z času, ne přičítáním: prohlížeč na pozadí
   * intervaly zpomaluje, takže sčítaný počet by se za chvíli rozešel
   * s hodinami.
   */
  const [, setTick] = useState(0)
  const roundKey = view.kind === 'game' ? `${view.mode}-${view.nonce}` : view.kind
  useEffect(() => {
    setTick((count) => count + 1)
  }, [roundKey])
  useEffect(() => {
    if (view.kind !== 'game' && view.kind !== 'quiz') return
    const id = setInterval(() => setTick((count) => count + 1), 1000)
    return () => clearInterval(id)
  }, [view.kind])
  const seconds = Math.max(0, Math.floor((Date.now() - roundStart) / 1000))
  const clock = `${Math.floor(seconds / 60)}:${String(seconds % 60).padStart(2, '0')}`

  /**
   * Otázka dne. Balík otázek je největší datový soubor ve hře a v ostatních
   * režimech není k ničemu, takže se stahuje až tady.
   */
  const startQuiz = useCallback(async (offset = 0) => {
    setLoading(true)
    setError(null)
    try {
      const deck = await loadQuiz()
      const question = quizFor(deck, dayNumber() + offset)
      if (!question) throw new Error('Otázka na dnešek chybí')
      setLoaded({ quiz: question, quizDeck: deck })
      setQuizOffset(offset)
      // Rozehraná otázka si nese svůj začátek s sebou, ať lišta po návratu
      // navazuje a neukazuje nulu u kola, které běží třeba hodinu.
      const saved = loadQuizRound()
      const started =
        saved && saved.day === dayNumber() + offset
          ? (saved.state as { startedAt?: number }).startedAt
          : undefined
      setRoundStart(typeof started === 'number' ? started : Date.now())
      setView({ kind: 'quiz' })
    } catch (cause) {
      setError(cause instanceof Error ? cause.message : 'Otázku se nepodařilo načíst')
    } finally {
      setLoading(false)
    }
  }, [])

  /**
   * Co hráče čeká po dohraném kole denní výzvy.
   *
   * Denní várka je šest kol a Otázka dne sedmá. Dřív se po každém z nich
   * muselo do menu a hledat, co ještě zbývá; teď to závěrečná karta ví sama.
   * Pořadí je dané: nejdřív zbylé výzvy, pak Otázka dne. Když je hotové
   * všechno, nabídka je prázdná a karta ukáže obyčejné „Další kolo".
   *
   * Platí to jen pro kola denní várky — kdo si jde zahrát na volno, chce
   * další kolo téže hry, ne přeskočit jinam.
   */
  const nextUp = useMemo<NextUpItem[]>(() => {
    if (view.kind !== 'game' || !view.daily) return []
    const left: NextUpItem[] = MODE_ORDER.filter(
      (mode) => profile.dailyDone[`${dayKey}:${mode}`] === undefined,
    ).map((mode) => ({
      id: mode,
      glyph: MODE_GLYPH[mode],
      label: MODE_LABEL[mode],
      start: () => play(mode, true),
    }))
    if (left.length > 0) return left
    if (!__QUIZ_ALL__ && profile.quiz.lastDay === dayKey) return []
    return [{ id: 'quiz', glyph: '?', label: 'Otázka dne', start: () => void startQuiz() }]
  }, [dayKey, play, profile.dailyDone, profile.quiz.lastDay, startQuiz, view])

  /** Přehled všech otázek — jen v kontrolním buildu. */
  const openQuizList = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const deck = await loadQuiz()
      setLoaded((previous) => ({ ...previous, quizDeck: deck }))
      setView({ kind: 'quizlist' })
    } catch (cause) {
      setError(cause instanceof Error ? cause.message : 'Otázky se nepodařilo načíst')
    } finally {
      setLoading(false)
    }
  }, [])

  const finishQuiz = useCallback(
    (outcome: { solved: boolean; clues: number; ink: number }) => {
      updateProfile((previous) => recordQuiz(previous, dayKey, outcome))
    },
    [dayKey, updateProfile],
  )

  /**
   * Průběžné ukládání Otázky dne.
   *
   * Zodpovězená otázka se maže: nabízet návrat do něčeho hotového nedává
   * smysl a druhý pokus by stejně nešel.
   */
  const keepQuiz = useCallback(
    (state: QuizState, over: boolean) => {
      const next: SavedQuiz | null = over
        ? null
        : { day: dayNumber() + quizOffset, state, savedAt: Date.now() }
      setQuizRound(next)
      saveQuizRound(next)
    },
    [quizOffset],
  )

  const closeGuide = useCallback(() => {
    setGuide(false)
    updateProfile((previous) =>
      previous.guideSeen ? previous : { ...previous, guideSeen: true },
    )
  }, [updateProfile])

  // Průvodce se sám otevře jen jednou za život profilu, a až po úvodní značce,
  // ať se hráči neotevře pod ještě neodkrytým plátnem.
  useEffect(() => {
    if (!splash && !profile.guideSeen) setGuide(true)
  }, [splash, profile.guideSeen])

  /**
   * Kam vede odkaz z vysvětlivky. Jediné místo, které zná navigaci celé hry.
   * Cíle `term:` sem nedojdou — ty si panel vysvětlivek vyřídí sám.
   */
  const goTo = useCallback((target: ExplainTarget) => {
    if (target === 'awards') setView({ kind: 'awards' })
    else if (target === 'stats') setView({ kind: 'stats' })
    else if (target === 'guide') setGuide(true)
    else if (target.startsWith('rules:')) {
      setTutorial({ mode: target.slice('rules:'.length) as ModeId, pending: false })
    }
  }, [])

  const closeTutorial = useCallback(() => {
    setTutorial((open) => {
      if (open) {
        updateProfile((previous) => ({
          ...previous,
          tutorialSeen: { ...previous.tutorialSeen, [open.mode]: true },
        }))
      }
      return null
    })
  }, [updateProfile])

  // Systémové zpět zavírá vrstvy odshora dolů: nejdřív návod, pak hru.
  // Až na domovské obrazovce se chová normálně a hru opustí.
  useBackGuard(view.kind !== 'home', goHome)
  useBackGuard(tutorial !== null, closeTutorial)
  useBackGuard(setup, () => setSetup(false))

  const themeButton = useMemo(() => {
    const order: Profile['theme'][] = ['system', 'light', 'dark']
    const icons: Record<Profile['theme'], string> = {
      system: '◐',
      light: '☀',
      dark: '☾',
    }
    const labels: Record<Profile['theme'], string> = {
      system: 'Podle systému',
      light: 'Světlé',
      dark: 'Tmavé',
    }
    const next = order[(order.indexOf(profile.theme) + 1) % order.length]!
    return (
      <button
        type="button"
        className="btn btn-sm btn-ghost btn-theme"
        title={`Téma: ${labels[profile.theme]}`}
        aria-label={`Téma: ${labels[profile.theme]}. Přepnout na ${labels[next]}`}
        onClick={() => updateProfile((previous) => ({ ...previous, theme: next }))}
      >
        {icons[profile.theme]}
      </button>
    )
  }, [profile.theme, updateProfile])

  return (
    <ExplainProvider onGo={goTo}>
    <NextUpContext.Provider value={nextUp}>
    <DuelContext.Provider value={duel}>
    <ReportContext.Provider
      value={MULTI_ON ? (uid, nick) => setReporting({ uid, nick }) : null}
    >
    <RoundModeContext.Provider
      value={
        view.kind === 'game'
          ? { glyph: MODE_GLYPH[view.mode], label: MODE_LABEL[view.mode] }
          : view.kind === 'quiz'
            ? { glyph: '?', label: 'Otázka dne' }
            : null
      }
    >
    <div
      /*
       * `playing` je celoobrazovkové rozvržení hry (deska, patička, žádné
       * rolování stránky) — to má jen deska hry a souboj.
       *
       * `round` je slabší tvrzení: běží kolo. Platí i pro Otázku dne, která
       * si celoobrazovkové rozvržení nebere, ale lištu má stejně nabitou —
       * hodiny, kalamář, série — a stejně jako ve hře se z ní musí uvolnit
       * místo. Bez toho z ní na každém telefonu vypadl přepínač témat.
       */
      className={[
        'shell',
        view.kind === 'game' || view.kind === 'duel' ? 'playing' : '',
        view.kind === 'game' || view.kind === 'duel' || view.kind === 'quiz' ? 'round' : '',
      ]
        .filter(Boolean)
        .join(' ')}
      data-mode={
        view.kind === 'game'
          ? view.mode
          : view.kind === 'duel' && match
            ? DUEL_MODE[match.kind]
            : undefined
      }
      // Čip „Denní" se na telefonu z lišty schová, aby se vešel kalamář.
      // Že běží denní kolo, se tím pádem nedá poznat z obrazovky — a testy
      // to vědět potřebují, takže to nese sama deska.
      data-daily={view.kind === 'game' && view.daily ? 'true' : undefined}
    >
      <header className="topbar">
        <button
          type="button"
          className="brand"
          onClick={goHome}
          style={{ color: 'inherit' }}
        >
          {/* Na nejužších telefonech zbude ze značky jen kroužkované „O" —
              lišta tam veze hodnost, kalamář a sérii a na celé slovo místo
              není. Tlačítko „domů" tím nemizí, jen se scvrkne na svůj znak. */}
          <span className="brand-word">Sl</span>
          <span className="mark">o</span>
          <span className="brand-word">va</span>
          <span className="brand-triad" aria-hidden="true">
            <i style={{ background: 'var(--mode-chain)' }} />
            <i style={{ background: 'var(--mode-hive)' }} />
            <i style={{ background: 'var(--mode-tower)' }} />
          </span>
        </button>
        {/* Zpět do menu. Rozehrané kolo se tím neztrácí — na úvodní
            obrazovce se nabídne k pokračování. Otázka dne má šipku taky:
            jinak by z ní na telefonu nevedla cesta ven, protože značka
            (která ji dosud zastávala) v běžícím kole z lišty ustupuje. */}
        {(view.kind === 'game' || view.kind === 'quiz') && (
          <button
            type="button"
            className="btn btn-sm btn-ghost btn-back"
            onClick={goHome}
            aria-label="Zpět do menu"
          >
            <span aria-hidden="true">←</span>
            {/* Na telefonu zůstane jen šipka. Slovo by se do lišty vešlo
                jen tak, že by se smrsklo tlačítko pod svůj nápis — a ten
                by pak ležel přes čip vedle. Šipka sama je srozumitelná
                a čtečka pořád čte „Zpět do menu". */}
            <span className="btn-back-label">Menu</span>
          </button>
        )}
        {view.kind === 'game' && (
          <>
            <button
              type="button"
              className="chip chip-mode"
              onClick={() => setTutorial({ mode: view.mode, pending: false })}
            >
              {MODE_LABEL[view.mode]}
            </button>
            {/* Denní výzva a k ní řada dnů, které hráč v téhle hře drží.
                Číslo je ta část, která na telefonu zůstává — slovo „Denní"
                se schová, plamínek s číslem ne. Je to jediné místo uvnitř
                hry, kde se řada dá vidět, a je to zároveň to jediné, co
                může hráč dnešním kolem ztratit. */}
            {view.daily && (
              <Explain
                term="denni"
                className="chip chip-gold chip-daily"
                label={
                  dailyStreak > 0
                    ? `Denní výzva. ${dailyStreak}. den v řadě`
                    : 'Denní výzva. Co to je'
                }
              >
                <span className="chip-label">Denní</span>
                {dailyStreak > 0 && (
                  <span className="daily-flame num">
                    <span aria-hidden="true">🔥</span>
                    {dailyStreak}
                  </span>
                )}
              </Explain>
            )}
            <button
              type="button"
              className="btn btn-sm btn-ghost"
              onClick={() => setTutorial({ mode: view.mode, pending: false })}
              aria-label="Pravidla"
            >
              <span className="wide-only">Pravidla</span>
              <span className="narrow-only" aria-hidden="true">
                ?
              </span>
            </button>
          </>
        )}
        <span className="topbar-spacer" />
        {/* Profil v liště: odznak a pořadí hodnosti jsou vidět na každé
            obrazovce, i uprostřed hry. Jméno hodnosti se vejde jen na širší
            displej, číslo drží vždycky — je to ta věc, která roste. */}
        <button
          type="button"
          className="profile-chip"
          onClick={() => setView({ kind: 'awards' })}
          title={`${rank.rank.name} — ${rank.rank.index}. hodnost z ${RANKS.length}`}
          aria-label={`Profil: ${rank.rank.name}, hodnost ${rank.rank.index}`}
        >
          <RankBadge rank={rank.rank.index} size={20} compact />
          <span className="profile-rank num">{rank.rank.index}</span>
          <span className="profile-rank profile-rank-name">{rank.rank.name}</span>
        </button>
        {/* Kalamář. Hráč se podle něj rozhoduje, jestli si nápovědu vzít,
            takže musí být vidět i uprostřed hry — a musí jít ťuknout, protože
            odjinud se nedozví, co inkoust je a kde se bere. */}
        {profile.ink > 0 && (
          <Explain
            term="inkoust"
            className="chip chip-ink"
            title={`${profile.ink} inkoustu na nápovědy`}
            label={`Inkoust: ${profile.ink}. Co to je`}
          >
            <InkMark size={11} />
            <span className="num">{profile.ink}</span>
          </Explain>
        )}
        {(view.kind === 'game' || view.kind === 'quiz') && (
          <Explain
            term="rychlost"
            className="chip chip-time"
            label={`Kolo běží ${clock}. Jak se počítají body za rychlost`}
          >
            <span className="num">{clock}</span>
          </Explain>
        )}
        <Explain
          term="serie"
          className="chip chip-accent chip-streak"
          label={`Série ${profile.streak} kol bez nápovědy. Co to je`}
        >
          <span className="chip-label">Série</span>
          <span className="num">{profile.streak}</span>
        </Explain>
        {themeButton}
      </header>

      <main className="main">
        {error && (
          <div className="banner banner-error" style={{ marginBottom: 'var(--sp-4)' }}>
            <span>{error}</span>
            <span className="banner-actions">
              <button type="button" className="btn btn-sm" onClick={goHome}>
                Domů
              </button>
            </span>
          </div>
        )}

        {loading && (
          <div className="loading">
            <span className="spinner" />
            <span>Načítám hádanku…</span>
          </div>
        )}

        {!loading && view.kind === 'home' && (
          <Home
            profile={profile}
            dayKey={dayKey}
            dayLabel={''}
            onPlay={play}
            onDifficulty={(mode, difficulty: Difficulty) =>
              updateProfile((previous) => ({
                ...previous,
                difficulty: { ...previous.difficulty, [mode]: difficulty },
              }))
            }
            onStats={() => setView({ kind: 'stats' })}
            onAwards={() => setView({ kind: 'awards' })}
            onRules={(mode) => setTutorial({ mode, pending: false })}
            onGuide={() => setGuide(true)}
            onQuiz={() => void startQuiz()}
            {...(__QUIZ_ALL__ ? { onQuizList: () => void openQuizList() } : {})}
            duels={
              MULTI_ON ? (
                <FriendsEntry
                  nick={me.nick}
                  waiting={challenges.length + reports.length}
                  onOpen={() => setView({ kind: 'friends' })}
                />
              ) : null
            }
            saved={saved}
            onResume={(mode) => {
              const round = saved[roundSlot(mode, false)]
              if (round) void resumeRound(round)
            }}
          />
        )}

        {!loading && view.kind === 'friends' && MULTI_ON && (
          <Friends
            me={me}
            onMe={setMe}
            challenges={challenges}
            onAccept={(item) => void acceptDuel(item)}
            reports={reports}
            onChallenge={() => setSetup(true)}
            onSeen={(id) => {
              const report = reports.find((one) => one.id === id)
              setReports((list) => list.filter((one) => one.id !== id))
              if (report) {
                closeDuel(
                  id,
                  report.mine === report.theirs
                    ? 'draw'
                    : report.mine > report.theirs
                      ? 'win'
                      : 'loss',
                )
              }
            }}
            onReport={(uid, nick) => setReporting({ uid, nick })}
            onUnblock={(uid) =>
              setMe((previous) => {
                const next = {
                  ...previous,
                  blocked: (previous.blocked ?? []).filter((one) => one !== uid),
                }
                saveMe(next)
                return next
              })
            }
            onErase={() => setErasing(true)}
            onBack={goHome}
          />
        )}

        {/* Souboj. Vlastní obrazovka bez inkoustu, nápověd a věhlasu —
            proti sobě stojí dva lidé a nic jiného se do toho neplete. */}
        {!loading && view.kind === 'duel' && match && matchHive && (
          <DuelHive
            match={match}
            puzzle={matchHive}
            uid={uid}
            nick={me.nick}
            onHome={goHome}
            onVerdict={(verdict) => closeDuel(match.id, verdict)}
          />
        )}

        {!loading && view.kind === 'duel' && match && matchIntruder && (
          <DuelIntruder
            match={match}
            puzzles={matchIntruder}
            uid={uid}
            nick={me.nick}
            onHome={goHome}
            onVerdict={(verdict) => closeDuel(match.id, verdict)}
          />
        )}

        {!loading && view.kind === 'stats' && (
          <Stats
            profile={profile}
            onBack={goHome}
            onReset={() => setProfile(emptyProfile())}
          />
        )}

        {!loading && view.kind === 'awards' && <Awards profile={profile} onBack={goHome} />}

        {!loading && view.kind === 'quizlist' && loaded.quizDeck && (
          <QuizReview deck={loaded.quizDeck} today={dayNumber()} onBack={goHome} />
        )}

        {!loading && view.kind === 'quiz' && loaded.quiz && (
          <QuizGame
            key={loaded.quiz.id}
            question={loaded.quiz}
            day={dayNumber() + quizOffset}
            dayLabel={__QUIZ_ALL__ ? `#${dayNumber() + quizOffset}` : ''}
            onFinish={finishQuiz}
            onHome={goHome}
            resume={
              quizRound && quizRound.day === dayNumber() + quizOffset
                ? (quizRound.state as QuizState)
                : null
            }
            onProgress={keepQuiz}
            {...(__QUIZ_ALL__
              ? { onNext: () => void startQuiz(quizOffset + 1) }
              : {})}
          />
        )}

        {!loading && view.kind === 'game' && view.mode === 'chain' && loaded.chain && (
          <ChainGame
            key={`${loaded.chain.puzzle.id}-${view.nonce}`}
            graph={loaded.chain.bundle.graph}
            puzzle={loaded.chain.puzzle}
            streak={profile.streak}
            dayLabel={view.daily ? dayTag : ''}
            onFinish={finishRound}
            onNext={() => startRound('chain', false)}
            onHome={goHome}
            onGiveUp={giveUp}
            resume={resume as ChainState | null}
            ink={profile.ink}
            onSpendInk={spendInkOn}
            onProgress={(state, finished) =>
              keepProgress('chain', state.puzzle.id, state.puzzle.difficulty, state, finished)
            }
          />
        )}

        {!loading && view.kind === 'game' && view.mode === 'hive' && loaded.hive && (
          <HiveGame
            key={`${loaded.hive.id}-${view.nonce}`}
            puzzle={loaded.hive}
            streak={profile.streak}
            dayLabel={view.daily ? dayTag : ''}
            onFinish={finishRound}
            onNext={() => startRound('hive', false)}
            onHome={goHome}
            resume={resume as HiveState | null}
            ink={profile.ink}
            onSpendInk={spendInkOn}
            onProgress={(state, finished) =>
              keepProgress('hive', state.puzzle.id, state.puzzle.difficulty, state, finished)
            }
          />
        )}

        {!loading && view.kind === 'game' && view.mode === 'tower' && loaded.tower && (
          <TowerGame
            key={`${loaded.tower.id}-${view.nonce}`}
            puzzle={loaded.tower}
            streak={profile.streak}
            dayLabel={view.daily ? dayTag : ''}
            onFinish={finishRound}
            onNext={() => startRound('tower', false)}
            onHome={goHome}
            onGiveUp={giveUp}
            resume={resume as TowerState | null}
            ink={profile.ink}
            onSpendInk={spendInkOn}
            onProgress={(state, finished) =>
              keepProgress('tower', state.puzzle.id, state.puzzle.difficulty, state, finished)
            }
          />
        )}

        {/* Nad výsledkem kola: nejdřív skóre, pak co za něj přibylo. */}
        {gained && !splash && <AwardPopup gained={gained} onClose={() => setGained(null)} />}

        {!loading && view.kind === 'game' && view.mode === 'gallows' && loaded.gallows && (
          <GallowsGame
            key={`${loaded.gallows.id}-${view.nonce}`}
            puzzle={loaded.gallows}
            streak={profile.streak}
            dayLabel={view.daily ? dayTag : ''}
            onFinish={finishRound}
            onNext={() => startRound('gallows', false)}
            onHome={goHome}
            onGiveUp={giveUp}
            resume={resume as GallowsState | null}
            ink={profile.ink}
            onSpendInk={spendInkOn}
            onProgress={(state, finished) =>
              keepProgress('gallows', state.puzzle.id, state.puzzle.difficulty, state, finished)
            }
          />
        )}

        {!loading && view.kind === 'game' && view.mode === 'tetris' && loaded.tetris && (
          <TetrisGame
            key={`${loaded.tetris.setup.seed}-${view.nonce}`}
            deck={loaded.tetris.deck}
            setup={loaded.tetris.setup}
            streak={profile.streak}
            dayLabel={view.daily ? dayTag : ''}
            onFinish={finishRound}
            onNext={() => startRound('tetris', false)}
            onHome={goHome}
            resume={resume as TetrisState | null}
            ink={profile.ink}
            onSpendInk={spendInkOn}
            onProgress={(state, finished) =>
              keepProgress(
                'tetris',
                `t-${state.setup.seed}`,
                state.setup.difficulty,
                state,
                finished,
              )
            }
          />
        )}

        {!loading && view.kind === 'game' && view.mode === 'intruder' && loaded.intruder && (
          <IntruderGame
            key={`${loaded.intruder.id}-${view.nonce}`}
            puzzle={loaded.intruder}
            streak={profile.streak}
            dayLabel={view.daily ? dayTag : ''}
            onFinish={finishRound}
            onNext={() => startRound('intruder', false)}
            onHome={goHome}
            resume={resume as IntruderState | null}
            ink={profile.ink}
            onSpendInk={spendInkOn}
            onProgress={(state, finished) =>
              keepProgress('intruder', state.puzzle.id, state.puzzle.difficulty, state, finished)
            }
          />
        )}

        {!loading && view.kind === 'game' && view.mode === 'quotes' && loaded.quotes && (
          <QuotesGame
            key={`${loaded.quotes.quote.id}-${view.nonce}`}
            quote={loaded.quotes.quote}
            seed={loaded.quotes.seed}
            streak={profile.streak}
            dayLabel={view.daily ? dayTag : ''}
            onFinish={finishRound}
            onNext={() => startRound('quotes', false)}
            onHome={goHome}
            onGiveUp={giveUp}
            resume={resume as QuoteState | null}
            ink={profile.ink}
            onSpendInk={spendInkOn}
            onProgress={(state, finished) =>
              keepProgress('quotes', state.quote.id, state.quote.difficulty, state, finished)
            }
          />
        )}

        {!loading && view.kind === 'game' && view.mode === 'detective' && loaded.detective && (
          <DetectiveGame
            key={`${loaded.detective.id}-${view.nonce}`}
            puzzle={loaded.detective}
            streak={profile.streak}
            dayLabel={view.daily ? dayTag : ''}
            onFinish={finishRound}
            onNext={() => startRound('detective', false)}
            onHome={goHome}
            onGiveUp={giveUp}
            resume={resume as DetectiveState | null}
            ink={profile.ink}
            onSpendInk={spendInkOn}
            onProgress={(state, finished) =>
              keepProgress('detective', state.puzzle.id, state.puzzle.difficulty, state, finished)
            }
          />
        )}

        {setup && <DuelSetup onClose={() => setSetup(false)} onSend={sendDuel} />}

        {erasing && (
          <Confirm
            title="Smazat přezdívku a data?"
            body="Ze serveru zmizí tvoje přezdívka, bilance soubojů i došlé výzvy a přezdívku si bude moci zabrat někdo jiný. Postup ve hrách, hodnost a ocenění ti zůstanou — ty leží jen v telefonu. Vrátit to nejde."
            confirmLabel="Smazat"
            onConfirm={() => {
              setErasing(false)
              setChallenges([])
              setReports([])
              void eraseMe()
                .catch(() =>
                  setError(
                    'Data se ze serveru nepodařilo smazat. Zkus to znovu, až budeš online.',
                  ),
                )
                .finally(() => setMe(loadMe()))
            }}
            onCancel={() => setErasing(false)}
          />
        )}

        {reporting && (
          <ReportSheet
            nick={reporting.nick}
            onClose={() => setReporting(null)}
            onSend={(reason) => reportAndBlock(reporting.uid, reporting.nick, reason)}
          />
        )}

        {splash && <Splash onDone={() => setSplash(false)} />}

        {tutorial && (
          <Tutorial
            mode={tutorial.mode}
            onClose={closeTutorial}
            finishLabel={tutorial.pending ? 'Začít hrát' : 'Zavřít'}
          />
        )}

        {/* Průvodce je pod návodem režimu: když se otevřou oba, hráč řeší
            nejdřív hru, kterou zrovna spustil. */}
        {guide && !tutorial && !splash && (
          <Guide
            onClose={closeGuide}
            onRules={(mode) => {
              closeGuide()
              setTutorial({ mode, pending: false })
            }}
            finishLabel={profile.guideSeen ? 'Zavřít' : 'Jdu na to'}
          />
        )}
      </main>
    </div>
    </RoundModeContext.Provider>
    </ReportContext.Provider>
    </DuelContext.Provider>
    </NextUpContext.Provider>
    </ExplainProvider>
  )
}
