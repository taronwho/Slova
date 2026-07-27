/**
 * Bodování — jednotné napříč režimy, s režimově specifickými pravidly.
 *
 * Čísla jsou proti první verzi na **třetinu**. Kolo dávalo přes tisíc bodů,
 * což znělo velkoryse, ale nic to neznamenalo: když je štědré všechno, není
 * štědré nic. Teď dá dobré kolo kolem čtyř set a je poznat rozdíl mezi
 * odbytým a povedeným. Prahy hodností jsou přepočítané stejným dílem, takže
 * postup profilu zůstal, kde byl.
 */

import { budgetFor, type ChainState } from './chain'
import {
  DETECTIVE_COST,
  isWon as detectiveWon,
  missCount,
  neededLetters as detectiveLetters,
  type DetectiveState,
} from './detective'
import { HIVE_HINT_COST } from './hive'
import { level as tetrisLevel, type TetrisState } from './tetris'
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

export const CHAIN_BASE = 330

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
  if (over > 0) lines.push({ label: `Tahů navíc (${over})`, value: -35 * over })
  if (moves > budget) {
    lines.push({ label: 'Překročený rozpočet', value: -70 })
  }
  // Nápovědy zaplacené inkoustem nic nestojí, takže se z bonusu za
  // nevyužité nápovědy neodečítají a ani se nestrhávají body.
  const paidHints = Math.max(0, state.hintsUsed - (state.freeHints ?? 0))
  const unused = Math.max(0, 3 - paidHints)
  if (unused > 0) lines.push({ label: `Nevyužité nápovědy (${unused})`, value: 15 * unused })
  if (state.hintCost > 0) {
    lines.push({ label: `Nápovědy (${paidHints})`, value: -state.hintCost })
  }

  const bonus = speedBonus(elapsed, 60_000, 240_000, 100)
  if (bonus > 0) lines.push({ label: 'Rychlost', value: bonus })

  const perfect = over === 0 && state.hintsUsed === 0
  const streakMul = streakMultiplier(streak)
  const multiplier = (perfect ? 1.5 : 1) * streakMul

  const labels: string[] = []
  if (perfect) labels.push('PERFEKTNÍ ×1,5')
  if (streakMul > 1) labels.push(`Série ×${streakMul.toFixed(2).replace('.', ',')}`)

  return finish(lines, multiplier, labels.join('  ·  ') || null, perfect, 35)
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
    levelPoints += (state.built[i]!.length) * 8
  }
  lines.push({ label: `Postavená patra (${state.built.length - 1})`, value: levelPoints })

  if (state.hintCost > 0) {
    const paid = Math.max(0, state.hintsUsed - (state.freeHints ?? 0))
    lines.push({ label: `Nápovědy (${paid})`, value: -state.hintCost })
  }

  const bonus = speedBonus(elapsed, 90_000, 360_000, 80)
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

  const lines = [{ label: `Body za slova (${found})`, value: points * 3 }]
  if (foundPangrams > 0) {
    lines.push({ label: `Pangramy (${foundPangrams})`, value: 50 * foundPangrams })
  }
  // Nápovědy zaplacené inkoustem se do bodů nepromítají. Do
  // `hintsUsed` se ale počítají, takže kolo pořád není „bez nápovědy".
  const paidHints = Math.max(0, state.hintsUsed - (state.freeHints ?? 0))
  if (paidHints > 0) {
    lines.push({ label: `Nápovědy (${paidHints})`, value: -HIVE_HINT_COST * paidHints })
  }
  const complete = found >= state.puzzle.solutions.length
  if (complete) lines.push({ label: 'Kompletní plástev', value: 170 })

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
    lines.push({ label: 'Uhodnuté slovo', value: 300 })
    if (lives > 0) lines.push({ label: `Zbylé životy (${lives})`, value: 20 * lives })
  } else {
    // Za rozluštěnou část slova se něco počítá i po prohře.
    const guessed = [...neededLetters(state.puzzle)].filter((letter) =>
      state.tried.includes(letter),
    ).length
    lines.push({ label: `Odhalená písmena (${guessed})`, value: 15 * guessed })
    lines.push({ label: 'Slovo neuhodnuto', value: -35 })
  }
  if (wrong > 0) lines.push({ label: `Chybná písmena (${wrong})`, value: -25 * wrong })

  if (state.hintCost > 0) {
    const paid = Math.max(0, state.hintsUsed - (state.freeHints ?? 0))
    lines.push({ label: `Nápovědy (${paid})`, value: -state.hintCost })
  }

  const bonus = won ? speedBonus(elapsed, 45_000, 180_000, 70) : 0
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
    lines.push({ label: 'Rozluštěné slovo', value: 270 })
    if (state.solved) {
      // Kolik písmen zbývalo odhalit, když hráč slovo tipl — čím dřív, tím víc.
      const open = [...detectiveLetters(state.puzzle)].filter(
        (letter) => !state.tried.includes(letter),
      ).length
      lines.push({ label: `Tip na slovo (${open} písmen skrytých)`, value: 35 * open })
    }
  } else {
    const found = [...detectiveLetters(state.puzzle)].filter((letter) =>
      state.tried.includes(letter),
    ).length
    lines.push({ label: `Odhalená písmena (${found})`, value: 15 * found })
    lines.push({ label: 'Slovo nerozluštěno', value: -35 })
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

  const bonus = won ? speedBonus(elapsed, 60_000, 240_000, 70) : 0
  if (bonus > 0) lines.push({ label: 'Rychlost', value: bonus })

  const perfect = won && misses === 0 && state.hintsUsed === 0 && state.guesses.length === 0
  const streakMul = streakMultiplier(streak)
  const multiplier = (perfect ? 1.5 : 1) * streakMul

  const labels: string[] = []
  if (perfect) labels.push('BEZ ŠKOBRTNUTÍ ×1,5')
  if (streakMul > 1) labels.push(`Série ×${streakMul.toFixed(2).replace('.', ',')}`)

  return finish(lines, multiplier, labels.join('  ·  ') || null, perfect, 0)
}

/**
 * Slabiky mají skóre na **desetině** ostatních her.
 *
 * Ostatní režimy mají kolo ohraničené — řetěz dojde do cíle, věž se dostaví,
 * slovo se uhodne. Slabiky ne: padá se, dokud si hráč desku nezablokuje,
 * takže vytrvalý hráč nasbírá násobky toho, co jde získat kdekoli jinde.
 * Věhlas ze Slabik pak přerostl všechno ostatní. Poměry uvnitř hry zůstávají
 * beze změny, jen se celá stupnice dělí deseti.
 */
const TETRIS_SCALE = 10

/** Bodová řádka Slabik na správné stupnici. */
function tetrisPoints(raw: number): number {
  return Math.round(raw / TETRIS_SCALE)
}

/**
 * Slabikový tetris.
 *
 * Body nesou slova, ne položené kostky — dvojice sama o sobě nedává nic.
 * Řetěz (několik slov z jednoho dopadu) je to, na co se hraje: prémie roste
 * s druhou mocninou, takže čtyřslovný řetěz je čtyřikrát cennější než dva
 * dvouslovné. Přidává se i za tempo: kdo vydrží do vyšších úrovní, dostane
 * za každé slovo víc.
 */
export function scoreTetris(state: TetrisState, streak: number): ScoreBreakdown {
  const letters = state.cleared.reduce((sum, word) => sum + word.length, 0)
  const reached = tetrisLevel(state)

  const lines: { label: string; value: number }[] = []
  if (state.cleared.length > 0) {
    lines.push({
      label: `Složená slova (${state.cleared.length})`,
      value: tetrisPoints(35 * state.cleared.length + 13 * letters),
    })
  }
  if (state.bestChain >= 2) {
    lines.push({
      label: `Nejdelší řetěz (${state.bestChain})`,
      value: tetrisPoints(50 * (state.bestChain - 1) * state.bestChain),
    })
  }
  if (reached > 1) {
    lines.push({ label: `Úroveň ${reached}`, value: tetrisPoints(40 * (reached - 1)) })
  }
  if (state.hintCost > 0) {
    const paid = Math.max(0, state.hintsUsed - (state.freeHints ?? 0))
    lines.push({ label: `Nápovědy (${paid})`, value: -state.hintCost })
  }

  // „Perfektní" kolo je tady slušný výkon bez nápovědy — dohrát se to nedá,
  // hraje se, dokud deska nepřeteče.
  const perfect = state.hintsUsed === 0 && state.cleared.length >= 12
  const streakMul = streakMultiplier(streak)
  const multiplier = (perfect ? 1.5 : 1) * streakMul

  const labels: string[] = []
  if (perfect) labels.push('BEZ NÁPOVĚDY ×1,5')
  if (streakMul > 1) labels.push(`Série ×${streakMul.toFixed(2).replace('.', ',')}`)

  return finish(lines, multiplier, labels.join('  ·  ') || null, perfect, 0)
}

/* Postup profilu (hodnosti 1–50) je v game/ranks.ts — je to samostatná věc
   od bodování kola a mluví do něj i vitrína ocenění. */
