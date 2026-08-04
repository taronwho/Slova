/**
 * Souboje dvou hráčů — pravidla, která se obejdou bez sítě.
 *
 * Souboj není denní výzva odehraná dvakrát. Jsou to dva formáty psané
 * schválně pro dva lidi:
 *
 * - **Voština na krádež.** Jedna plástev, tři minuty, oba naráz. Slovo
 *   patří tomu, kdo ho odevzdá dřív; druhému zmizí pod rukama. Kdo tedy
 *   dumá nad devítipísmenným, riskuje, že mezitím přijde o tři krátká.
 * - **Vetřelec na tři kola.** Tytéž tři pětice, ale každý si je zahraje,
 *   kdy chce. Nic se nemusí potkat v čase, protože o výsledku rozhoduje
 *   trefa a čas — a ten se dá porovnat i o den později.
 *
 * Body ze soubojů se **nepočítají do věhlasu ani do ocenění**; proto tu
 * stojí vlastní, jednoduché bodování a ne to z běžných kol.
 */

import { fold } from '../lib/czech'
import type { ModeId } from './types'

export type DuelKind = 'hive' | 'intruder'

export const DUEL_KINDS: DuelKind[] = ['hive', 'intruder']

/** Kterou hru souboj používá — kvůli barvě a znaku režimu. */
export const DUEL_MODE: Record<DuelKind, ModeId> = {
  hive: 'hive',
  intruder: 'intruder',
}

export const DUEL_TITLE: Record<DuelKind, string> = {
  hive: 'Voština — krádež slov',
  intruder: 'Vetřelec — tři kola',
}

export const DUEL_ABOUT: Record<DuelKind, string> = {
  hive: 'Tři minuty na jedné plástvi. Hrajete zároveň a každé slovo patří tomu, kdo ho odevzdá dřív — soupeři pak už nezbývá.',
  intruder: 'Tři stejné pětice. Každý si je zahraje, kdy chce; rozhoduje trefa a čas, takže na sebe nemusíte čekat.',
}

/** Voština v souboji trvá tři minuty. */
export const HIVE_DUEL_MS = 180_000

/** Kolik vteřin před koncem se hodiny zbarví do červena. */
export const HIVE_DUEL_WARN_MS = 30_000

/** Vetřelec se hraje na tři pětice. */
export const INTRUDER_ROUNDS = 3

/**
 * Body za jedno kolo Vetřelce.
 *
 * Vedle se rozhoduje jen mezi dvěma lidmi, takže bodování musí být čitelné
 * na první pohled: trefa se počítá, vedle je nula, a mezi dvěma trefami
 * rozhoduje čas. Čtyři body za vteřinu, dolní hranice čtyřicet — kdo přemýšlí
 * minutu a trefí se, pořád má víc než ten, kdo střelil vedle hned.
 */
export function duelRoundScore(correct: boolean, ms: number): number {
  if (!correct) return 0
  return Math.max(40, 200 - Math.round(Math.max(ms, 0) / 250))
}

/** Nejvyšší možný výsledek souboje ve Vetřelci — do popisku „z kolika". */
export const INTRUDER_DUEL_MAX = INTRUDER_ROUNDS * 200

export type Verdict = 'win' | 'loss' | 'draw'

export function verdictOf(mine: number, theirs: number): Verdict {
  if (mine > theirs) return 'win'
  if (mine < theirs) return 'loss'
  return 'draw'
}

export const VERDICT_TITLE: Record<Verdict, string> = {
  win: 'Vyhrál jsi!',
  loss: 'Tentokrát ne',
  draw: 'Remíza',
}

/**
 * Klíč slova ve sdílené mapě ukořistěných slov.
 *
 * Bere se složený tvar bez diakritiky — jednak ho databáze v klíči snese,
 * jednak plástev stejně uznává všechny zápisy, které na sebe sednou
 * („cili" i „cíli"). Ukořistit se tedy dá celá skupina naráz, což je
 * správně: hráč mezi nimi nemá jak rozlišit.
 */
export function claimKey(word: string): string {
  return fold(word)
}
