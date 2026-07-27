/** Bodování — jednotné napříč režimy, s režimově specifickými pravidly. */

import { budgetFor, type ChainState } from './chain'
import {
  DETECTIVE_COST,
  isWon as detectiveWon,
  missCount,
  neededLetters as detectiveLetters,
  type DetectiveState,
} from './detective'
import {
  GALLOWS_LIVES,
  isWon,
  neededLetters,
  wrongCount,
  type GallowsState,
} from './gallows'
import { currentScore, type HiveState } from './hive'
import type { TowerState } from './tower'

export interface ScoreBreakdown {
  lines: { label: string; value: number }[]
  multiplier: number
  multiplierLabel: string | null
  total: number
  perfect: boolean
}

/** Sérií se násobí každé dokončené kolo, strop je +50 %. */
export function streakMultiplier(streak: number): number {
  return Math.min(1 + 0.05 * Math.max(streak - 1, 0), 1.5)
}

function speedBonus(elapsedMs: number, fullMs: number, zeroMs: number, max: number): number {
  if (elapsedMs <= fullMs) return max
  if (elapsedMs >= zeroMs) return 0
  const ratio = 1 - (elapsedMs - fullMs) / (zeroMs - fullMs)
  return Math.round((max * ratio) / 10) * 10
}

function finish(
  lines: { label: string; value: number }[],
  multiplier: number,
  multiplierLabel: string | null,
  perfect: boolean,
  floor: number,
): ScoreBreakdown {
  const subtotal = lines.reduce((sum, line) => sum + line.value, 0)
  const total = Math.max(Math.round(subtotal * multiplier), floor)
  return { lines, multiplier, multiplierLabel, total, perfect }
}

export const CHAIN_BASE = 1000

export function scoreChain(
  state: ChainState,
  streak: number,
  now = Date.now(),
): ScoreBreakdown {
  const moves = state.path.length - 1
  const over = Math.max(0, moves - state.puzzle.par)
  const elapsed = (state.finishedAt ?? now) - state.startedAt
  const budget = budgetFor(state.puzzle)

  const lines = [{ label: 'Základ', value: CHAIN_BASE }]
  if (over > 0) lines.push({ label: `Tahů navíc (${over})`, value: -100 * over })
  if (moves > budget) {
    lines.push({ label: 'Překročený rozpočet', value: -200 })
  }
  // Nápovědy zdarma z peněženky profilu nic nestojí, takže se z bonusu za
  // nevyužité nápovědy neodečítají a ani se nestrhávají body.
  const paidHints = Math.max(0, state.hintsUsed - (state.freeHints ?? 0))
  const unused = Math.max(0, 3 - paidHints)
  if (unused > 0) lines.push({ label: `Nevyužité nápovědy (${unused})`, value: 50 * unused })
  if (state.hintCost > 0) {
    lines.push({ label: `Nápovědy (${paidHints})`, value: -state.hintCost })
  }

  const bonus = speedBonus(elapsed, 60_000, 240_000, 300)
  if (bonus > 0) lines.push({ label: 'Rychlost', value: bonus })

  const perfect = over === 0 && state.hintsUsed === 0
  const streakMul = streakMultiplier(streak)
  const multiplier = (perfect ? 1.5 : 1) * streakMul

  const labels: string[] = []
  if (perfect) labels.push('PERFEKTNÍ ×1,5')
  if (streakMul > 1) labels.push(`Série ×${streakMul.toFixed(2).replace('.', ',')}`)

  return finish(lines, multiplier, labels.join('  ·  ') || null, perfect, 100)
}

/** Věž: každé postavené patro boduje podle své délky. */
export function scoreTower(
  state: TowerState,
  streak: number,
  now = Date.now(),
): ScoreBreakdown {
  const elapsed = (state.finishedAt ?? now) - state.startedAt
  const lines: { label: string; value: number }[] = []

  let levelPoints = 0
  for (let i = 1; i < state.built.length; i++) {
    levelPoints += (state.built[i]!.length) * 25
  }
  lines.push({ label: `Postavená patra (${state.built.length - 1})`, value: levelPoints })

  if (state.hintCost > 0) {
    const paid = Math.max(0, state.hintsUsed - (state.freeHints ?? 0))
    lines.push({ label: `Nápovědy (${paid})`, value: -state.hintCost })
  }

  const bonus = speedBonus(elapsed, 90_000, 360_000, 250)
  if (bonus > 0) lines.push({ label: 'Rychlost', value: bonus })

  const perfect = state.hintsUsed === 0
  const streakMul = streakMultiplier(streak)
  const multiplier = (perfect ? 1.4 : 1) * streakMul

  const labels: string[] = []
  if (perfect) labels.push('BEZ NÁPOVĚDY ×1,4')
  if (streakMul > 1) labels.push(`Série ×${streakMul.toFixed(2).replace('.', ',')}`)

  return finish(lines, multiplier, labels.join('  ·  ') || null, perfect, 50)
}

/** Voština: skóre vychází z bodů za slova, bonus za dotažení plástve. */
export function scoreHive(state: HiveState, streak: number): ScoreBreakdown {
  const points = currentScore(state)
  const found = state.found.length
  const foundPangrams = state.found.filter((w) =>
    state.puzzle.pangrams.includes(w),
  ).length

  const lines = [{ label: `Body za slova (${found})`, value: points * 8 }]
  if (foundPangrams > 0) {
    lines.push({ label: `Pangramy (${foundPangrams})`, value: 150 * foundPangrams })
  }
  // Nápovědy zdarma z peněženky profilu se do bodů nepromítají. Do
  // `hintsUsed` se ale počítají, takže kolo pořád není „bez nápovědy".
  const paidHints = Math.max(0, state.hintsUsed - (state.freeHints ?? 0))
  if (paidHints > 0) {
    lines.push({ label: `Nápovědy (${paidHints})`, value: -80 * paidHints })
  }
  const complete = found >= state.puzzle.solutions.length
  if (complete) lines.push({ label: 'Kompletní plástev', value: 500 })

  const perfect = complete && state.hintsUsed === 0
  const streakMul = streakMultiplier(streak)
  const multiplier = streakMul

  return finish(
    lines,
    multiplier,
    streakMul > 1 ? `Série ×${streakMul.toFixed(2).replace('.', ',')}` : null,
    perfect,
    0,
  )
}

/**
 * Šibenice: základ minus chyby, plus prémie za nevyužité životy.
 *
 * Prohrané kolo dostane jen zbytek za uhodnutá písmena — nula by hráče
 * odradila od dohrání, ale plný základ by zase nic neznamenal.
 */
export function scoreGallows(
  state: GallowsState,
  streak: number,
  now = Date.now(),
): ScoreBreakdown {
  const elapsed = (state.finishedAt ?? now) - state.startedAt
  const wrong = wrongCount(state)
  const won = isWon(state)
  const lives = Math.max(0, GALLOWS_LIVES - wrong)

  const lines: { label: string; value: number }[] = []
  if (won) {
    lines.push({ label: 'Uhodnuté slovo', value: 900 })
    if (lives > 0) lines.push({ label: `Zbylé životy (${lives})`, value: 60 * lives })
  } else {
    // Za rozluštěnou část slova se něco počítá i po prohře.
    const guessed = [...neededLetters(state.puzzle)].filter((letter) =>
      state.tried.includes(letter),
    ).length
    lines.push({ label: `Odhalená písmena (${guessed})`, value: 40 * guessed })
    lines.push({ label: 'Slovo neuhodnuto', value: -100 })
  }
  if (wrong > 0) lines.push({ label: `Chybná písmena (${wrong})`, value: -70 * wrong })

  if (state.hintCost > 0) {
    const paid = Math.max(0, state.hintsUsed - (state.freeHints ?? 0))
    lines.push({ label: `Nápovědy (${paid})`, value: -state.hintCost })
  }

  const bonus = won ? speedBonus(elapsed, 45_000, 180_000, 200) : 0
  if (bonus > 0) lines.push({ label: 'Rychlost', value: bonus })

  const perfect = won && wrong === 0 && state.hintsUsed === 0
  const streakMul = streakMultiplier(streak)
  const multiplier = (perfect ? 1.5 : 1) * streakMul

  const labels: string[] = []
  if (perfect) labels.push('BEZ CHYBY ×1,5')
  if (streakMul > 1) labels.push(`Série ×${streakMul.toFixed(2).replace('.', ',')}`)

  return finish(lines, multiplier, labels.join('  ·  ') || null, perfect, 0)
}

/**
 * Detektiv: základ za rozluštění, prémie za tip na celé slovo.
 *
 * Chybné písmeno tu nekončí kolo, jen stojí — proto je odečet jediné, co
 * hráče brzdí, a proto je tip na celé slovo tak štědrý: je to sázka, kterou
 * dělá jen ten, kdo z textu opravdu něco vyčetl.
 */
export function scoreDetective(
  state: DetectiveState,
  streak: number,
  now = Date.now(),
): ScoreBreakdown {
  const elapsed = (state.finishedAt ?? now) - state.startedAt
  const misses = missCount(state)
  const won = detectiveWon(state)

  const lines: { label: string; value: number }[] = []
  if (won) {
    lines.push({ label: 'Rozluštěné slovo', value: 800 })
    if (state.solved) {
      // Kolik písmen zbývalo odhalit, když hráč slovo tipl — čím dřív, tím víc.
      const open = [...detectiveLetters(state.puzzle)].filter(
        (letter) => !state.tried.includes(letter),
      ).length
      lines.push({ label: `Tip na slovo (${open} písmen skrytých)`, value: 100 * open })
    }
  } else {
    const found = [...detectiveLetters(state.puzzle)].filter((letter) =>
      state.tried.includes(letter),
    ).length
    lines.push({ label: `Odhalená písmena (${found})`, value: 40 * found })
    lines.push({ label: 'Slovo nerozluštěno', value: -100 })
  }

  if (misses > 0) {
    lines.push({ label: `Písmena vedle (${misses})`, value: -DETECTIVE_COST.miss * misses })
  }
  if (state.guesses.length > 0) {
    lines.push({
      label: `Chybné tipy (${state.guesses.length})`,
      value: -DETECTIVE_COST.wrongGuess * state.guesses.length,
    })
  }
  if (state.hintCost > 0) {
    const paid = Math.max(0, state.hintsUsed - (state.freeHints ?? 0))
    lines.push({ label: `Nápovědy (${paid})`, value: -state.hintCost })
  }

  const bonus = won ? speedBonus(elapsed, 60_000, 240_000, 200) : 0
  if (bonus > 0) lines.push({ label: 'Rychlost', value: bonus })

  const perfect = won && misses === 0 && state.hintsUsed === 0 && state.guesses.length === 0
  const streakMul = streakMultiplier(streak)
  const multiplier = (perfect ? 1.5 : 1) * streakMul

  const labels: string[] = []
  if (perfect) labels.push('BEZ ŠKOBRTNUTÍ ×1,5')
  if (streakMul > 1) labels.push(`Série ×${streakMul.toFixed(2).replace('.', ',')}`)

  return finish(lines, multiplier, labels.join('  ·  ') || null, perfect, 0)
}

/* Postup profilu (hodnosti 1–50) je v game/ranks.ts — je to samostatná věc
   od bodování kola a mluví do něj i vitrína ocenění. */
