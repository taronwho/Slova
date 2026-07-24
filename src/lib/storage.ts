/** Perzistence profilu, statistik a rozehraných kol v localStorage. */

import type { Difficulty, ModeId, RoundResult } from '../game/types'

const KEY = 'slova.profile.v1'

export interface ModeStats {
  played: number
  bestScore: number
  totalScore: number
  /** Řetěz: součet tahů nad par. Věž: součet postavených pater. */
  extra: number
  perfect: number
}

export interface Profile {
  xp: number
  streak: number
  bestStreak: number
  lastPlayedDay: string | null
  /** ID hádanek, které už hráč dohrál — aby se neopakovaly. */
  seen: Record<ModeId, string[]>
  stats: Record<ModeId, ModeStats>
  history: RoundResult[]
  difficulty: Record<ModeId, Difficulty>
  theme: 'light' | 'dark' | 'system'
  dailyDone: Record<string, number>
}

function emptyStats(): ModeStats {
  return { played: 0, bestScore: 0, totalScore: 0, extra: 0, perfect: 0 }
}

export function emptyProfile(): Profile {
  return {
    xp: 0,
    streak: 0,
    bestStreak: 0,
    lastPlayedDay: null,
    seen: { chain: [], hive: [], tower: [] },
    stats: { chain: emptyStats(), hive: emptyStats(), tower: emptyStats() },
    history: [],
    difficulty: { chain: 'normal', hive: 'normal', tower: 'normal' },
    theme: 'system',
    dailyDone: {},
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
    difficulty: { ...base.difficulty, ...(saved.difficulty ?? {}) },
    dailyDone: { ...base.dailyDone, ...(saved.dailyDone ?? {}) },
    history: saved.history ?? [],
  }
}

export function loadProfile(): Profile {
  try {
    const raw = localStorage.getItem(KEY)
    return raw ? migrate(JSON.parse(raw)) : emptyProfile()
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

/** Seznam dohraných hádanek držíme omezený, ať localStorage neroste bez konce. */
const SEEN_LIMIT = 4000

export function recordRound(profile: Profile, result: RoundResult, day: string): Profile {
  const stats = { ...profile.stats[result.mode] }
  stats.played += 1
  stats.totalScore += result.score
  stats.bestScore = Math.max(stats.bestScore, result.score)
  if (result.perfect) stats.perfect += 1
  if (typeof result.detail.extra === 'number') stats.extra += result.detail.extra

  const seen = [...profile.seen[result.mode], result.puzzleId].slice(-SEEN_LIMIT)
  const streak = profile.streak + 1

  return {
    ...profile,
    xp: profile.xp + result.score,
    streak,
    bestStreak: Math.max(profile.bestStreak, streak),
    lastPlayedDay: day,
    seen: { ...profile.seen, [result.mode]: seen },
    stats: { ...profile.stats, [result.mode]: stats },
    history: [result, ...profile.history].slice(0, 50),
  }
}

/** Vzdání kola sérii ukončí, ale statistiky nechá být. */
export function breakStreak(profile: Profile): Profile {
  return { ...profile, streak: 0 }
}
