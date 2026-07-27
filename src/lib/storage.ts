/** Perzistence profilu, statistik a rozehraných kol v localStorage. */

import { AWARD_HINTS, AWARDS } from '../game/awards'
import { RANK_HINTS, rankFor } from '../game/ranks'
import type { Difficulty, ModeId, RoundResult } from '../game/types'

const KEY = 'slova.profile.v1'
const ROUNDS_KEY = 'slova.rounds.v1'

export interface ModeStats {
  played: number
  bestScore: number
  totalScore: number
  /** Řetěz: součet tahů navíc. Věž: součet postavených pater. */
  extra: number
  perfect: number
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
  /** Kolik denních výzev dohrál. */
  dailies: number
  /** Nejlepší skóre v jednom kole napříč režimy. */
  bestScore: number
}

export interface Profile {
  xp: number
  streak: number
  bestStreak: number
  lastPlayedDay: string | null
  /** ID hádanek, které už hráč dohrál — aby se neopakovaly. */
  seen: Record<ModeId, string[]>
  stats: Record<ModeId, ModeStats>
  counters: Counters
  /**
   * Nápovědy zdarma. Utratí se místo bodů — kolo se tím pořád počítá jako
   * „s nápovědou", takže se jimi nedají získat mety za hru bez nápovědy, ale
   * skóre neutrpí. Sype je nová hodnost, každé ocenění a denní výzva.
   */
  hints: number
  /** Nejvyšší hodnost, za kterou už nápovědy padly — aby nepadly dvakrát. */
  hintRankPaid: number
  /** ID získaného ocenění -> kdy padlo (ms). */
  awards: Record<string, number>
  history: RoundResult[]
  difficulty: Record<ModeId, Difficulty>
  theme: 'light' | 'dark' | 'system'
  dailyDone: Record<string, number>
  /** Režimy, u kterých hráč viděl návod — při prvním spuštění se otevře sám. */
  tutorialSeen: Record<ModeId, boolean>
}

function emptyStats(): ModeStats {
  return { played: 0, bestScore: 0, totalScore: 0, extra: 0, perfect: 0 }
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
    dailies: 0,
    bestScore: 0,
  }
}

export function emptyProfile(): Profile {
  return {
    xp: 0,
    streak: 0,
    bestStreak: 0,
    lastPlayedDay: null,
    seen: { chain: [], hive: [], tower: [], gallows: [], detective: [] },
    stats: {
      chain: emptyStats(),
      hive: emptyStats(),
      tower: emptyStats(),
      gallows: emptyStats(),
      detective: emptyStats(),
    },
    counters: emptyCounters(),
    // Tři na uvítanou, ať si hráč nápovědu zkusí, než začne řešit, co ho stojí.
    hints: 3,
    hintRankPaid: 1,
    awards: {},
    history: [],
    difficulty: {
      chain: 'normal',
      hive: 'normal',
      tower: 'normal',
      gallows: 'normal',
      detective: 'normal',
    },
    theme: 'system',
    dailyDone: {},
    tutorialSeen: {
      chain: false,
      hive: false,
      tower: false,
      gallows: false,
      detective: false,
    },
  }
}

/** Doplní chybějící klíče, aby starší uložený profil nikdy nespadl. */
function migrate(raw: unknown): Profile {
  const base = emptyProfile()
  if (!raw || typeof raw !== 'object') return base
  const saved = raw as Partial<Profile>
  return {
    ...base,
    ...saved,
    seen: { ...base.seen, ...(saved.seen ?? {}) },
    stats: { ...base.stats, ...(saved.stats ?? {}) },
    counters: { ...base.counters, ...(saved.counters ?? {}) },
    awards: { ...(saved.awards ?? {}) },
    difficulty: { ...base.difficulty, ...(saved.difficulty ?? {}) },
    dailyDone: { ...base.dailyDone, ...(saved.dailyDone ?? {}) },
    tutorialSeen: { ...base.tutorialSeen, ...(saved.tutorialSeen ?? {}) },
    history: saved.history ?? [],
  }
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
  let hints = profile.hints

  for (const award of AWARDS) {
    if (awards[award.id] !== undefined) continue
    if (!award.done(profile)) continue
    if (awards === profile.awards) awards = { ...awards }
    awards[award.id] = now
    hints += AWARD_HINTS(award)
  }

  const rank = rankFor(profile.xp).rank.index
  const paid = Math.max(profile.hintRankPaid, 1)
  if (rank > paid) hints += (rank - paid) * RANK_HINTS

  if (awards === profile.awards && hints === profile.hints && rank <= paid) return profile
  return { ...profile, awards, hints, hintRankPaid: Math.max(paid, rank) }
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
    for (const mode of ['chain', 'hive', 'tower', 'gallows', 'detective'] as ModeId[]) {
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

/**
 * Kolik nápověd zdarma padne za **kompletní** denní várku.
 *
 * Ne za každou výzvu zvlášť: čtyři režimy krát jedna nápověda denně by
 * peněženku zaplavily rychleji než všechno ostatní dohromady. Takhle je to
 * jedna denně a zároveň důvod dohrát i tu čtvrtou.
 */
export const DAILY_HINTS = 1

/** Utratí nápovědu zdarma, pokud nějakou má. */
export function spendHint(profile: Profile): Profile {
  if (profile.hints <= 0) return profile
  return { ...profile, hints: profile.hints - 1 }
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

function updateCounters(profile: Profile, result: RoundResult, daily: boolean): Counters {
  const c = { ...profile.counters }
  // Čisté kolo je až to, které hráč **dotáhl** bez nápovědy. Viselec ani
  // plástev ukončená po třech slovech se nepočítají — jinak by se meta „Vlastní
  // hlavou" dala splnit tím, že hráč kolo prostě prohraje.
  const clean = result.hintsUsed === 0 && result.success
  c.bestScore = Math.max(c.bestScore, result.score)
  if (daily) c.dailies += 1

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
    if (num(result, 'moves') <= num(result, 'par')) c.chainPar += 1
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
      // dvou patrech by jinak bylo „nejrychlejší" vždycky.
      c.towerFastMs = fastest(c.towerFastMs, result.elapsedMs)
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
  const modes: ModeId[] = ['chain', 'hive', 'tower', 'gallows', 'detective']
  return modes.every(
    (mode) => mode === result.mode || profile.dailyDone[`${day}:${mode}`] !== undefined,
  )
}

export function recordRound(
  profile: Profile,
  result: RoundResult,
  day: string,
  daily = false,
): Profile {
  const stats = { ...profile.stats[result.mode] }
  stats.played += 1
  stats.totalScore += result.score
  stats.bestScore = Math.max(stats.bestScore, result.score)
  if (result.perfect) stats.perfect += 1
  if (typeof result.detail.extra === 'number') stats.extra += result.detail.extra

  const seen = [...profile.seen[result.mode], result.puzzleId].slice(-SEEN_LIMIT)
  const streak = profile.streak + 1

  return grantAwards({
    ...profile,
    // Denní výzva je jediná věc, za kterou padá nápověda jen za účast —
    // je to důvod se vrátit zítra. Padne až za všechny čtyři.
    hints: profile.hints + (allDailiesDone(profile, result, day, daily) ? DAILY_HINTS : 0),
    xp: profile.xp + result.score,
    streak,
    bestStreak: Math.max(profile.bestStreak, streak),
    lastPlayedDay: day,
    seen: { ...profile.seen, [result.mode]: seen },
    stats: { ...profile.stats, [result.mode]: stats },
    counters: updateCounters(profile, result, daily),
    history: [result, ...profile.history].slice(0, 50),
  })
}

/** Vzdání kola sérii ukončí, ale statistiky nechá být. */
export function breakStreak(profile: Profile): Profile {
  return { ...profile, streak: 0 }
}
