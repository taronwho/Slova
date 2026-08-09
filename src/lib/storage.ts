/** Perzistence profilu, statistik a rozehraných kol v localStorage. */

import { AWARDS } from '../game/awards'
import { awardInk, DAILY_INK, LEGACY_HINT_INK, rankInk, START_INK } from '../game/economy'
import { rankFor } from '../game/ranks'
import { MODE_ORDER, type Difficulty, type ModeId, type RoundResult } from '../game/types'

const KEY = 'slova.profile.v1'

/** Všechny hry v pořadí, ve kterém se ukazují. Jediný seznam pro celý soubor. */
// Seznam režimů se bere z jednoho místa. Když se sem psal ručně, přibyly
// Citát s Vetřelcem a profil o nich nevěděl: rozehraná kola se po návratu
// ztrácela a inkoust za kompletní denní várku padal už po šesti výzvách
// z osmi.
const MODES: ModeId[] = MODE_ORDER
const ROUNDS_KEY = 'slova.rounds.v1'

export interface ModeStats {
  played: number
  bestScore: number
  totalScore: number
  /** Řetěz: součet tahů navíc. Věž: součet postavených pater. */
  extra: number
  perfect: number
  /**
   * Kolik kol v téhle hře hráč dotáhl bez jediné nápovědy.
   *
   * Na tomhle čísle stojí žebříčky mistrovství — jsou to jediné počty, které
   * se v hodnocení počítají, protože „odehraj sto kol" splní každý, kdo
   * vydrží klikat, kdežto „dohraj sto kol načisto" ne.
   */
  clean: number
}

/**
 * Čísla, na která běžné statistiky nestačí, ale ocenění je potřebují.
 *
 * Držet je průběžně je jediná možnost — historie kol se ořezává na padesát
 * záznamů, takže zpětně dopočítat, kolik pangramů hráč za celou dobu našel,
 * by nešlo.
 */
export interface Counters {
  /** Kolik kol hráč dohrál bez jediné nápovědy. */
  noHint: number
  /** Kolik takových kol má za sebou právě teď v řadě. */
  noHintStreak: number
  /** Nejdelší řada kol bez nápovědy. */
  bestNoHintStreak: number
  /** Věž: dostavěná až nahoru a bez jediné nápovědy. */
  towerFullNoHint: number
  /** Voština: kolik pangramů hráč celkem našel. */
  pangrams: number
  /** Voština: kolikrát vysbíral celou plástev. */
  hiveFull: number
  /** Voština: kolikrát došel na nejvyšší hodnost. */
  hiveQueen: number
  /** Voština: nejvíc slov v jednom kole. */
  hiveBestWords: number
  /** Řetěz: kolik kol dohrál na počet tahů nejkratší cesty. */
  chainPar: number
  /** Řetěz: nejrychleji dohrané kolo *bez nápovědy* v ms (0 = zatím žádné). */
  chainFastMs: number
  /** Věž: kolik věží dostavěl až nahoru. */
  towerFull: number
  /** Věž: nejdelší postavené patro. */
  towerBestFloor: number
  /** Věž: nejrychleji dostavěná věž v ms (0 = zatím žádná). */
  towerFastMs: number
  /** Šibenice: kolik slov uhodl. */
  gallowsSolved: number
  /** Šibenice: kolik slov uhodl bez jediné chyby (a bez nápovědy). */
  gallowsClean: number
  /** Detektiv: kolik případů rozluštil. */
  detectiveSolved: number
  /** Detektiv: kolikrát tipl slovo, když byla víc než půlka písmen skrytá. */
  detectiveGuessed: number
  /** Slabiky: kolik slov celkem složil. */
  tetrisWords: number
  /** Slabiky: nejdelší řetěz z jednoho tahu. */
  tetrisChain: number
  /** Kolik denních výzev dohrál. */
  dailies: number
  /** Kolikrát dohrál denní výzvy ve všech šesti hrách v jednom dni. */
  dailySets: number
  /** Nejlepší skóre v jednom kole napříč režimy. */
  bestScore: number
}

/**
 * Otázka dne — jediná hra mimo šestici slovních, a proto i jediná, která má
 * v profilu vlastní přihrádku místo `stats[mode]`.
 *
 * Nemá obtížnost, nedá se hrát vícekrát denně a nesype body, takže by se do
 * statistik režimů vešla jen násilím. Její čísla jsou vlastní: kolikrát se
 * hráč trefil, na kolik indicií a kolik dní v řadě.
 */
export interface QuizRecord {
  /** Poslední den, ve kterém hráč otázku dohrál. Podle něj se zamyká další. */
  lastDay: string | null
  /** Kolik otázek hráč dohrál celkem, i těch neuhodnutých. */
  played: number
  /** Kolik jich uhodl. */
  solved: number
  /** Kolik uhodl na jedinou indicii — to je ta nejtěžší cesta. */
  expert: number
  /** Kolik dní po sobě se trefil. Neúspěch i vynechaný den řadu utne. */
  streak: number
  bestStreak: number
  /** Kolik inkoustu si z Otázky dne za celou dobu odnesl. */
  ink: number
}

export function emptyQuiz(): QuizRecord {
  return {
    lastDay: null,
    played: 0,
    solved: 0,
    expert: 0,
    streak: 0,
    bestStreak: 0,
    ink: 0,
  }
}

/**
 * Denní série jedné hry.
 *
 * Sedm různých čísel místo jednoho: hráč, který každý den řeší Voštinu a na
 * Šibenici nemá náladu, si zaslouží vidět, že Voštinu drží — a ne aby mu to
 * jedna vynechaná hra shodila celé. Proto má každá hra vlastní řadu a Otázka
 * dne tu svou už měla dřív, ve vlastní přihrádce.
 *
 * Počítá se **účast, ne výhra**. Denní výzva je návyk; Šibenice se dá prohrát
 * a Voština se dá ukončit kdykoli, takže podmínka na úspěch by z řady udělala
 * loterii. Stejně se chová i `dayStreak`, který počítá dny se hrou vůbec.
 */
export interface DailyStreak {
  /** Poslední den, kdy hráč tuhle denní výzvu dohrál. */
  lastDay: string | null
  streak: number
  best: number
}

export function emptyDailyStreak(): DailyStreak {
  return { lastDay: null, streak: 0, best: 0 }
}

export interface Profile {
  /** Verze uloženého profilu — podle ní se pozná, co je potřeba přepočítat. */
  version: number
  /**
   * Věhlas — součet bodů ze všech dohraných kol. Jediné číslo, které žene
   * hodnost nahoru. Dřív se jmenoval `xp`; migrace to přejmenuje.
   */
  fame: number
  /**
   * Série **čistých kol** — kol dohraných bez jediné nápovědy, jedno za
   * druhým. Dřív se počítalo každé kolo, takže série osmnácti mohla vzniknout
   * z osmnácti prohraných šibenic; to nedávalo smysl a hráč to nahlásil.
   * Sérií se násobí skóre, takže musí něco stát.
   */
  streak: number
  bestStreak: number
  /** Dny po sobě, kdy hráč aspoň jednou hrál. Jiná věc než série kol. */
  dayStreak: number
  bestDayStreak: number
  /** Kolik různých dní hráč hrál celkem. */
  daysPlayed: number
  lastPlayedDay: string | null
  /** ID hádanek, které už hráč dohrál — aby se neopakovaly. */
  seen: Record<ModeId, string[]>
  stats: Record<ModeId, ModeStats>
  counters: Counters
  /**
   * Inkoust — měna za nápovědy. Utratí se místo bodů, takže kolo se pořád
   * počítá jako „s nápovědou" a mety za hru bez nápovědy se za něj koupit
   * nedají; šetří jen skóre. Sype ho nová hodnost, každé ocenění a kompletní
   * denní várka. Kolik která nápověda stojí, říká `inkPrice` v economy.ts.
   */
  ink: number
  /** Nejvyšší hodnost, za kterou už inkoust padl — aby nepadl dvakrát. */
  inkRankPaid: number
  /** ID získaného ocenění -> kdy padlo (ms). */
  awards: Record<string, number>
  history: RoundResult[]
  difficulty: Record<ModeId, Difficulty>
  theme: 'light' | 'dark' | 'system'
  dailyDone: Record<string, number>
  /** Režimy, u kterých hráč viděl návod — při prvním spuštění se otevře sám. */
  tutorialSeen: Record<ModeId, boolean>
  /**
   * Viděl hráč průvodce celou hrou? Otevře se sám při úplně prvním spuštění;
   * potom už jen na vyžádání z domovské obrazovky.
   */
  guideSeen: boolean
  /** Otázka dne — vlastní přihrádka, protože se do statistik režimů nevejde. */
  quiz: QuizRecord
  /** Denní série, jedna za každou hru. */
  dailyStreak: Record<ModeId, DailyStreak>
}

/**
 * Kolik dní v řadě řada **doopravdy** drží.
 *
 * Uložené číslo se nuluje až při dalším odehrání, takže samo o sobě může
 * tvrdit dvanáct dní i tři týdny poté, co hráč naposledy hrál. Na obrazovku
 * proto jde tahle hodnota: řada platí, jen když se hrálo dnes nebo včera —
 * dnešek se ještě dá dohnat, cokoli staršího je už přetržené.
 */
export function liveStreak(row: DailyStreak, today: string): number {
  if (!row.lastDay) return 0
  if (row.lastDay === today || row.lastDay === shiftDay(today, -1)) return row.streak
  return 0
}

function emptyStats(): ModeStats {
  return { played: 0, bestScore: 0, totalScore: 0, extra: 0, perfect: 0, clean: 0 }
}

export function emptyCounters(): Counters {
  return {
    noHint: 0,
    noHintStreak: 0,
    bestNoHintStreak: 0,
    towerFullNoHint: 0,
    pangrams: 0,
    hiveFull: 0,
    hiveQueen: 0,
    hiveBestWords: 0,
    chainPar: 0,
    chainFastMs: 0,
    towerFull: 0,
    towerBestFloor: 0,
    towerFastMs: 0,
    gallowsSolved: 0,
    gallowsClean: 0,
    detectiveSolved: 0,
    detectiveGuessed: 0,
    tetrisWords: 0,
    tetrisChain: 0,
    dailies: 0,
    dailySets: 0,
    bestScore: 0,
  }
}

/** Aktuální verze profilu. Zvýšit, kdykoli je potřeba data přepočítat. */
const PROFILE_VERSION = 3

export function emptyProfile(): Profile {
  return {
    version: PROFILE_VERSION,
    fame: 0,
    streak: 0,
    bestStreak: 0,
    dayStreak: 0,
    bestDayStreak: 0,
    daysPlayed: 0,
    lastPlayedDay: null,
    seen: {
      chain: [], hive: [], tower: [], gallows: [], detective: [], tetris: [], quotes: [], intruder: [],
    },
    stats: {
      chain: emptyStats(),
      hive: emptyStats(),
      tower: emptyStats(),
      gallows: emptyStats(),
      detective: emptyStats(),
      tetris: emptyStats(),
      quotes: emptyStats(),
      intruder: emptyStats(),
    },
    counters: emptyCounters(),
    ink: START_INK,
    inkRankPaid: 1,
    awards: {},
    history: [],
    difficulty: {
      chain: 'normal',
      hive: 'normal',
      tower: 'normal',
      gallows: 'normal',
      detective: 'normal',
      tetris: 'normal',
      quotes: 'normal',
      intruder: 'normal',
    },
    theme: 'system',
    dailyDone: {},
    tutorialSeen: {
      chain: false,
      hive: false,
      tower: false,
      gallows: false,
      detective: false,
      tetris: false,
      quotes: false,
      intruder: false,
    },
    guideSeen: false,
    quiz: emptyQuiz(),
    dailyStreak: Object.fromEntries(
      MODES.map((mode) => [mode, emptyDailyStreak()]),
    ) as Record<ModeId, DailyStreak>,
  }
}

/**
 * Starý profil ještě nezná věhlas ani inkoust — měl `xp`, `hints`
 * a `hintRankPaid`.
 */
interface LegacyProfile {
  xp?: number
  hints?: number
  hintRankPaid?: number
}

/**
 * Body šly na třetinu a prahy hodností s nimi. Nasbíraný věhlas i rekordy se
 * proto přepočítají stejným dílem — hráč tím nepřijde o hodnost ani o
 * ocenění, jen se čísla srovnají s novým měřítkem.
 */
const SCORE_RESCALE = 3

/** O kolik se zlevnily Slabiky ve verzi 3. Musí sedět s `scoreTetris`. */
const TETRIS_RESCALE = 10

/**
 * Slabiky šly na desetinu — a s nimi i to, co za ně hráč nasbíral.
 *
 * Kolo v Slabikách nemá konec, hraje se, dokud se deska nezablokuje, takže
 * vytrvalý hráč z nich vytěžil násobky toho, co jde získat kdekoli jinde.
 * Kdyby se přepočítalo jen budoucí bodování, zůstal by v profilu navždy hrb
 * z doby, kdy hra platila víc.
 *
 * Odečíst se dá **přesně**: profil vede součet bodů za každou hru zvlášť,
 * takže se z věhlasu ubere devět desetin toho, co Slabiky nasypaly, a totéž
 * se udělá s jejich rekordem i součtem. Ostatní hry se nedotknou.
 */
function rescaleTetris(profile: Profile): Profile {
  const tetris = profile.stats.tetris
  const overpaid = tetris.totalScore - Math.round(tetris.totalScore / TETRIS_RESCALE)
  return {
    ...profile,
    version: 3,
    fame: Math.max(0, profile.fame - overpaid),
    stats: {
      ...profile.stats,
      tetris: {
        ...tetris,
        bestScore: Math.round(tetris.bestScore / TETRIS_RESCALE),
        totalScore: Math.round(tetris.totalScore / TETRIS_RESCALE),
      },
    },
    counters: {
      ...profile.counters,
      // Nejlepší kolo napříč režimy se z historie spolehlivě dopočítat nedá,
      // ale když ho drželo právě kolo Slabik, sedne mu nová stupnice taky.
      bestScore:
        profile.counters.bestScore === tetris.bestScore
          ? Math.round(tetris.bestScore / TETRIS_RESCALE)
          : profile.counters.bestScore,
    },
    history: profile.history.map((round) =>
      round.mode === 'tetris'
        ? { ...round, score: Math.round(round.score / TETRIS_RESCALE) }
        : round,
    ),
  }
}

function rescale(profile: Profile): Profile {
  const stats = { ...profile.stats }
  for (const mode of MODES) {
    const one = stats[mode]
    stats[mode] = {
      ...one,
      bestScore: Math.round(one.bestScore / SCORE_RESCALE),
      totalScore: Math.round(one.totalScore / SCORE_RESCALE),
    }
  }
  return {
    ...profile,
    version: 2,
    fame: Math.round(profile.fame / SCORE_RESCALE),
    stats,
    counters: {
      ...profile.counters,
      bestScore: Math.round(profile.counters.bestScore / SCORE_RESCALE),
    },
    history: profile.history.map((round) => ({
      ...round,
      score: Math.round(round.score / SCORE_RESCALE),
    })),
  }
}

function mergeStats(
  base: Record<ModeId, ModeStats>,
  saved: Partial<Record<ModeId, ModeStats>> | undefined,
): Record<ModeId, ModeStats> {
  const stats = { ...base }
  for (const mode of MODES) stats[mode] = { ...base[mode], ...(saved?.[mode] ?? {}) }
  return stats
}

/**
 * Doplní chybějící klíče, aby starší uložený profil nikdy nespadl, a prožene
 * ho přepočty, které ještě neviděl. Exportuje se kvůli testům — jinak by se
 * dalo ověřit jen přes localStorage.
 */
export function migrate(raw: unknown): Profile {
  const base = emptyProfile()
  if (!raw || typeof raw !== 'object') return base
  const saved = raw as Partial<Profile>
  const old = raw as LegacyProfile
  const merged: Profile = {
    ...base,
    ...saved,
    version: saved.version ?? 0,
    // Přejmenování veličin. Nasbírané body zůstávají tak jak byly, jen se
    // teď jmenují věhlas; nápovědy zdarma se přepočtou na inkoust kurzem,
    // který odpovídá střední nápovědě — nikdo tím nepřijde zkrátka.
    fame: saved.fame ?? old.xp ?? 0,
    ink: saved.ink ?? (old.hints ?? 0) * LEGACY_HINT_INK,
    inkRankPaid: saved.inkRankPaid ?? old.hintRankPaid ?? 1,
    seen: { ...base.seen, ...(saved.seen ?? {}) },
    // Statistiky se slučují **po jednotlivých hrách**, ne jen po klíčích
    // režimu: mělké sloučení by uložený objekt vzalo celý a nově přidané
    // políčko (naposled `clean`) by zůstalo `undefined`, což by v podmínkách
    // ocenění tiše vyhodnotilo NaN.
    stats: mergeStats(base.stats, saved.stats),
    counters: { ...base.counters, ...(saved.counters ?? {}) },
    awards: { ...(saved.awards ?? {}) },
    difficulty: { ...base.difficulty, ...(saved.difficulty ?? {}) },
    dailyDone: { ...base.dailyDone, ...(saved.dailyDone ?? {}) },
    tutorialSeen: { ...base.tutorialSeen, ...(saved.tutorialSeen ?? {}) },
    quiz: { ...base.quiz, ...(saved.quiz ?? {}) },
    // Po jedné hře, ne mělce: nová hra v žebříčku by jinak zůstala
    // `undefined` a série by se na ní počítala z ničeho.
    dailyStreak: Object.fromEntries(
      MODES.map((mode) => [
        mode,
        { ...emptyDailyStreak(), ...(saved.dailyStreak?.[mode] ?? {}) },
      ]),
    ) as Record<ModeId, DailyStreak>,
    history: saved.history ?? [],
  }
  // Přepočty se řetězí: starý profil projde všemi, novější jen těmi, které
  // ještě neviděl.
  let out = merged
  if (out.version < 2) out = rescale(out)
  if (out.version < 3) out = rescaleTetris(out)
  return out
}

/**
 * Dopočítá ocenění a hodnosti, na které profil má, a připíše za ně nápovědy.
 *
 * Volá se po každém kole i hned po načtení profilu. Podmínky se čtou jen ze
 * statistik, takže druhé spuštění nic nezmění — a hráč, který si zahrál dřív,
 * než ocenění existovala, dostane zpětně všechno, na co dosáhl.
 *
 * Nápovědy se připisují právě jednou: u ocenění proto, že se připisují jen
 * spolu s nově přidaným klíčem, u hodností přes `hintRankPaid`.
 */
export function grantAwards(profile: Profile, now = Date.now()): Profile {
  let awards = profile.awards
  let ink = profile.ink

  for (const award of AWARDS) {
    if (awards[award.id] !== undefined) continue
    if (!award.done(profile)) continue
    if (awards === profile.awards) awards = { ...awards }
    awards[award.id] = now
    ink += awardInk(award)
  }

  // Za každou hodnost, kterou hráč překročil od minule. Odměna roste
  // s hodností, takže se sčítá po jedné, ne násobením.
  const rank = rankFor(profile.fame).rank.index
  const paid = Math.max(profile.inkRankPaid, 1)
  for (let index = paid + 1; index <= rank; index += 1) ink += rankInk(index)

  if (awards === profile.awards && ink === profile.ink && rank <= paid) return profile
  return { ...profile, awards, ink, inkRankPaid: Math.max(paid, rank) }
}

export function loadProfile(): Profile {
  try {
    const raw = localStorage.getItem(KEY)
    return grantAwards(raw ? migrate(JSON.parse(raw)) : emptyProfile())
  } catch {
    return emptyProfile()
  }
}

export function saveProfile(profile: Profile): void {
  try {
    localStorage.setItem(KEY, JSON.stringify(profile))
  } catch {
    // Soukromý režim prohlížeče — hra běží dál, jen se neuloží.
  }
}

/**
 * Rozehrané kolo.
 *
 * Drží se **zvlášť pro každý režim**, aby si hráč mohl nechat rozehraný
 * Řetěz i Voštinu naráz. Ukládá se stranou od profilu: zapisuje se po
 * každém tahu, takže se nesmí stát, aby jeho poškození vzalo s sebou
 * i statistiky. Stav hry je prostý objekt (cesta řetězu, nalezená slova,
 * postavená patra), takže stačí JSON — rekonstruovat se z něj dá celé kolo
 * včetně hádanky.
 */
export interface SavedRound {
  mode: ModeId
  daily: boolean
  difficulty: Difficulty
  puzzleId: string
  /** ChainState | HiveState | TowerState — typ hlídá režim. */
  state: unknown
  savedAt: number
}

export type SavedRounds = Partial<Record<ModeId, SavedRound>>

export function loadRounds(): SavedRounds {
  try {
    const raw = localStorage.getItem(ROUNDS_KEY)
    if (!raw) return {}
    const saved = JSON.parse(raw) as SavedRounds
    if (!saved || typeof saved !== 'object') return {}
    const rounds: SavedRounds = {}
    for (const mode of MODES) {
      const round = saved[mode]
      if (round && round.mode === mode && round.state) rounds[mode] = round
    }
    return rounds
  } catch {
    return {}
  }
}

export function saveRounds(rounds: SavedRounds): void {
  try {
    localStorage.setItem(ROUNDS_KEY, JSON.stringify(rounds))
  } catch {
    // Soukromý režim nebo plná kvóta — hra běží dál, jen se nedá pokračovat.
  }
}

/** Seznam dohraných hádanek držíme omezený, ať localStorage neroste bez konce. */
const SEEN_LIMIT = 4000

/** Zaplatí nápovědu inkoustem, pokud na ni hráč má. */
export function spendInk(profile: Profile, price: number): Profile {
  if (price <= 0 || profile.ink < price) return profile
  return { ...profile, ink: profile.ink - price }
}

/** Číslo z detailu kola; chybějící údaj se počítá jako nula. */
function num(result: RoundResult, key: string): number {
  const value = result.detail[key]
  return typeof value === 'number' ? value : 0
}

/** Menší z dvojice, ale nula znamená „zatím nic" a prohrává vždy. */
function fastest(current: number, candidate: number): number {
  if (candidate <= 0) return current
  return current === 0 ? candidate : Math.min(current, candidate)
}

function updateCounters(
  profile: Profile,
  result: RoundResult,
  day: string,
  daily: boolean,
): Counters {
  const c = { ...profile.counters }
  // Čisté kolo je až to, které hráč **dotáhl** bez nápovědy. Viselec ani
  // plástev ukončená po třech slovech se nepočítají — jinak by se meta „Vlastní
  // hlavou" dala splnit tím, že hráč kolo prostě prohraje.
  const clean = result.hintsUsed === 0 && result.success
  c.bestScore = Math.max(c.bestScore, result.score)
  if (daily) c.dailies += 1
  if (allDailiesDone(profile, result, day, daily)) c.dailySets += 1

  // Řada čistých kol se láme na prvním kole s nápovědou — jinak by „pět
  // načisto v řadě" šlo posbírat po jednom mezi nápovědovými koly.
  if (clean) {
    c.noHint += 1
    c.noHintStreak += 1
    c.bestNoHintStreak = Math.max(c.bestNoHintStreak, c.noHintStreak)
  } else {
    c.noHintStreak = 0
  }

  if (result.mode === 'chain') {
    // Nejkratší cesta se počítá jen bez nápovědy. „Celé slovo" hráče po
    // optimální cestě přímo vede, takže by tahle rodina neměřila, jestli ji
    // hráč našel, ale jestli si ji nechal ukázat.
    if (clean && num(result, 'moves') <= num(result, 'par')) c.chainPar += 1
    // Rychlost se počítá jen bez nápovědy — s „Celé slovo" je pod minutou
    // každý řetěz a meta by nic neznamenala.
    if (clean) c.chainFastMs = fastest(c.chainFastMs, result.elapsedMs)
  } else if (result.mode === 'hive') {
    c.pangrams += num(result, 'pangrams')
    c.hiveBestWords = Math.max(c.hiveBestWords, num(result, 'found'))
    if (num(result, 'found') >= num(result, 'total') && num(result, 'total') > 0) c.hiveFull += 1
    if (num(result, 'rankTop') === 1) c.hiveQueen += 1
  } else if (result.mode === 'detective') {
    if (num(result, 'solved') === 1) {
      c.detectiveSolved += 1
      // „Z první ruky" je za odvahu tipnout brzy, ne za doklikání abecedy.
      if (num(result, 'guessed') === 1 && num(result, 'extra') > 0) {
        c.detectiveGuessed += 1
      }
    }
  } else if (result.mode === 'tetris') {
    c.tetrisWords += num(result, 'words')
    c.tetrisChain = Math.max(c.tetrisChain, num(result, 'chain'))
  } else if (result.mode === 'gallows') {
    if (num(result, 'solved') === 1) {
      c.gallowsSolved += 1
      if (num(result, 'wrong') === 0 && clean) c.gallowsClean += 1
    }
  } else {
    c.towerBestFloor = Math.max(c.towerBestFloor, num(result, 'top'))
    if (num(result, 'full') === 1) {
      c.towerFull += 1
      if (clean) c.towerFullNoHint += 1
      // Rychlost dává smysl měřit jen u dostavěné věže — vzdané kolo po
      // dvou patrech by jinak bylo „nejrychlejší" vždycky — a jen bez
      // nápovědy. S „Celé slovo" postaví věž do dvou minut kdokoli, takže
      // meta bez téhle podmínky neměřila rychlost, ale trpělivost klikání.
      // Řetěz to tak měl od začátku; Věž se opomněla.
      if (clean) c.towerFastMs = fastest(c.towerFastMs, result.elapsedMs)
    }
  }
  return c
}

/** Má hráč po tomhle kole hotové denní výzvy ve všech režimech? */
function allDailiesDone(
  profile: Profile,
  result: RoundResult,
  day: string,
  daily: boolean,
): boolean {
  if (!daily) return false
  return MODES.every(
    (mode) => mode === result.mode || profile.dailyDone[`${day}:${mode}`] !== undefined,
  )
}

export function recordRound(
  profile: Profile,
  result: RoundResult,
  day: string,
  wanted = false,
): Profile {
  // Denní výzva se počítá jednou za den a hru. Bez téhle podmínky šlo pustit
  // hotovou výzvu znovu a znovu a pokaždé inkasovat inkoust za dokončenou
  // várku — hráč na to přišel. Nestačí zašedit dlaždici: kdo zná adresu,
  // spustí kolo i tak, takže se to hlídá tady, ne v obrazovce.
  //
  // Kolo se pořád zapíše jako běžné — body, věhlas i statistiky platí.
  // Nepočítá se jen podruhé jako *denní*.
  const daily = wanted && profile.dailyDone[`${day}:${result.mode}`] === undefined
  // Série je řada **čistých** kol: dotažených a bez jediné nápovědy. Dřív se
  // počítalo každé odehrané kolo, takže série osmnácti mohla vzniknout
  // z osmnácti prohraných šibenic. Násobí se jí skóre, takže musí něco stát.
  const clean = result.hintsUsed === 0 && result.success

  const stats = { ...profile.stats[result.mode] }
  stats.played += 1
  stats.totalScore += result.score
  stats.bestScore = Math.max(stats.bestScore, result.score)
  if (result.perfect) stats.perfect += 1
  if (clean) stats.clean += 1
  if (typeof result.detail.extra === 'number') stats.extra += result.detail.extra

  const seen = [...profile.seen[result.mode], result.puzzleId].slice(-SEEN_LIMIT)

  const streak = clean ? profile.streak + 1 : 0

  // Denní série je jiná věc: dny po sobě, kdy hráč aspoň jednou hrál. Není
  // za výkon, je za návyk — a proto se nepřeruší tím, že se kolo nepovedlo.
  const days = dayStreakAfter(profile, day)

  return grantAwards({
    ...profile,
    // Denní várka je jediná věc, za kterou padá inkoust jen za účast — je to
    // důvod se vrátit zítra. Padne až za všech šest her.
    ink: profile.ink + (allDailiesDone(profile, result, day, daily) ? DAILY_INK : 0),
    fame: profile.fame + result.score,
    streak,
    bestStreak: Math.max(profile.bestStreak, streak),
    dayStreak: days.streak,
    bestDayStreak: Math.max(profile.bestDayStreak, days.streak),
    daysPlayed: profile.daysPlayed + (days.fresh ? 1 : 0),
    lastPlayedDay: day,
    seen: { ...profile.seen, [result.mode]: seen },
    stats: { ...profile.stats, [result.mode]: stats },
    counters: updateCounters(profile, result, day, daily),
    history: [result, ...profile.history].slice(0, 50),
    dailyStreak: daily
      ? {
          ...profile.dailyStreak,
          [result.mode]: bumpDaily(profile.dailyStreak[result.mode], day),
        }
      : profile.dailyStreak,
  })
}

/**
 * Zapíše dohranou Otázku dne.
 *
 * Nemíchá se do `recordRound`: nedává body, nemá obtížnost, nepatří do
 * historie kol a nesmí hnout sérií čistých kol ani věhlasem. Jediné, co
 * z ní teče do zbytku hry, je inkoust — a ten je tu nejštědřejší v celé hře,
 * protože se dá vzít právě jednou denně.
 *
 * `day` zamyká další otázku do zítřka. Zapisuje se i neúspěch, jinak by po
 * neuhodnuté otázce šlo obnovit stránku a zkusit to znovu.
 */
export function recordQuiz(
  profile: Profile,
  day: string,
  outcome: { solved: boolean; clues: number; ink: number },
): Profile {
  const quiz = profile.quiz
  // Řada dní se počítá jen za trefu a jen za den, který navazuje na ten
  // minulý. Vynechaný den ji utne stejně jako špatná odpověď — je to řada
  // správných odpovědí, ne řada návštěv.
  const follows = quiz.lastDay !== null && quiz.lastDay === shiftDay(day, -1)
  const streak = outcome.solved ? (follows ? quiz.streak + 1 : 1) : 0

  return grantAwards({
    ...profile,
    ink: profile.ink + outcome.ink,
    quiz: {
      lastDay: day,
      played: quiz.played + 1,
      solved: quiz.solved + (outcome.solved ? 1 : 0),
      expert: quiz.expert + (outcome.solved && outcome.clues === 1 ? 1 : 0),
      streak,
      bestStreak: Math.max(quiz.bestStreak, streak),
      ink: quiz.ink + outcome.ink,
    },
  })
}

/** Vzdání kola sérii ukončí, ale statistiky nechá být. */
export function breakStreak(profile: Profile): Profile {
  return { ...profile, streak: 0 }
}

/**
 * Denní série jedné hry po dohrané denní výzvě.
 *
 * Navazuje se jen na včerejšek; mezera řadu utne a začíná se od jedničky.
 * Druhé kolo v tentýž den řadu neposune — je to řada dnů, ne kol —, a proto
 * se nejdřív porovnává `lastDay`.
 */
function bumpDaily(row: DailyStreak, day: string): DailyStreak {
  if (row.lastDay === day) return row
  const streak = row.lastDay === shiftDay(day, -1) ? row.streak + 1 : 1
  return { lastDay: day, streak, best: Math.max(row.best, streak) }
}

/**
 * Denní série po odehrání ve dni `day`.
 *
 * Navazuje se jen na **včerejšek**; mezera řadu utne. Dva zápasy v jeden den
 * sérii neposunou, protože je to řada dnů, ne kol.
 */
function dayStreakAfter(profile: Profile, day: string): { streak: number; fresh: boolean } {
  if (profile.lastPlayedDay === day) {
    return { streak: Math.max(profile.dayStreak, 1), fresh: false }
  }
  const yesterday = shiftDay(day, -1)
  const follows = profile.lastPlayedDay === yesterday
  return { streak: follows ? profile.dayStreak + 1 : 1, fresh: true }
}

/** Datum ve tvaru YYYY-MM-DD posunuté o `by` dní. */
function shiftDay(day: string, by: number): string {
  const stamp = Date.parse(`${day}T12:00:00Z`)
  if (Number.isNaN(stamp)) return day
  return new Date(stamp + by * 86_400_000).toISOString().slice(0, 10)
}
