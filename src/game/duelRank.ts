/**
 * Hodnosti v soubojích.
 *
 * Vlastní žebříček, oddělený od věhlasu. Důvod je ten samý, proč se body ze
 * soubojů nepočítají do hodnosti profilu: dva domluvení kamarádi by si za
 * večer nahnali cokoli. Soubojová hodnost je proto **záznam o hraní proti
 * lidem**, ne měřítko, kdo je lepší — roste pomalu, nikdo o ni nepřijde
 * a nikam se neposílá.
 *
 * Počítá se ze tří čísel, která už databáze o hráči vede (výhry, remízy,
 * prohry), takže o ní nemusí server vědět nic navíc. Za výhru tři body, za
 * remízu jeden, za prohru nula — prohra tedy nesráží, jen neposouvá. Kdo
 * hraje a prohrává, stojí; kdo nehraje vůbec, taky stojí. Tak to má být:
 * hodnost říká „tohle jsem odehrál", ne „tolik jsem lepší".
 */

/** Bilance soubojů, jak ji vede databáze i telefon. */
export interface DuelTally {
  wins: number
  losses: number
  draws: number
}

export interface DuelRank {
  /** Pořadí 1–12. */
  index: number
  name: string
  /** Kolik soubojových bodů je potřeba. */
  at: number
}

const NAMES = [
  'Vyzyvatel',
  'Sok',
  'Šermíř slov',
  'Ostrý soupeř',
  'Rváč',
  'Přeborník',
  'Vítěz klání',
  'Postrach soupeřů',
  'Mistr soubojů',
  'Velmistr soubojů',
  'Legenda klání',
  'Nepřemožitelný',
]

/*
 * Prahy.
 *
 * První tři jsou skoro hned — kdo odehraje první souboj, má co slavit. Pak
 * se rozestupy natahují, ale ne tak surově jako u věhlasu: soubojů se
 * neodehraje tisíc, na ně je potřeba někdo druhý. Poslední stupeň vyjde na
 * zhruba dvě stě vyhraných soubojů, tedy na dlouhou známost, ne na jeden
 * večer.
 */
const THRESHOLDS = [0, 3, 9, 20, 40, 75, 130, 210, 330, 500, 750, 1100]

export const DUEL_RANKS: DuelRank[] = NAMES.map((name, i) => ({
  index: i + 1,
  name,
  at: THRESHOLDS[i]!,
}))

/** Body ze soubojů: tři za výhru, jeden za remízu, nic za prohru. */
export function duelPoints(tally: DuelTally): number {
  return Math.max(0, tally.wins) * 3 + Math.max(0, tally.draws)
}

export interface DuelRankProgress {
  rank: DuelRank
  next: DuelRank | null
  /** Kolik bodů hráč má nad prahem své hodnosti. */
  into: number
  /** Kolik bodů je mezi touhle a další hodností. 0 na konci žebříčku. */
  span: number
}

export function duelRankFor(points: number): DuelRankProgress {
  let at = 0
  while (at + 1 < DUEL_RANKS.length && points >= DUEL_RANKS[at + 1]!.at) at += 1
  const rank = DUEL_RANKS[at]!
  const next = DUEL_RANKS[at + 1] ?? null
  return {
    rank,
    next,
    into: points - rank.at,
    span: next ? next.at - rank.at : 0,
  }
}

/** Kolik soubojů má hráč za sebou. */
export function duelsPlayed(tally: DuelTally): number {
  return Math.max(0, tally.wins) + Math.max(0, tally.losses) + Math.max(0, tally.draws)
}

/**
 * Úspěšnost v procentech, nebo null, když ještě není z čeho počítat.
 *
 * Remíza se počítá za půl výhry — jinak by hráč, který třikrát remizoval,
 * vypadal stejně jako ten, kdo třikrát prohrál.
 */
export function duelWinRate(tally: DuelTally): number | null {
  const total = duelsPlayed(tally)
  if (total === 0) return null
  return Math.round(((tally.wins + tally.draws / 2) / total) * 100)
}
