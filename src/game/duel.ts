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
  loss: 'Prohrál jsi',
  draw: 'Remíza',
}

/**
 * Hláška pod výsledkem.
 *
 * Jedna věta na všechny výhry omrzí po třetím souboji. Je jich proto po
 * dvaceti od každého a vybírá se podle **id zápasu**, ne náhodou: kdyby se
 * losovalo při každém vykreslení, měnila by se hláška pod rukama pokaždé,
 * když se obrazovka překreslí. Takhle má každý souboj tu svou napořád —
 * i když se na něj hráč podívá zpětně v přehledu.
 *
 * Psané jsou tak, aby nikoho nesrážely: prohra je prohra, ale hraje se
 * s kamarádem, ne o čest rodu.
 */
export const VERDICT_LINES: Record<Verdict, string[]> = {
  win: [
    'Slova poslouchala tebe.',
    'Tohle bylo čisté vítězství.',
    'Soupeř se na tebe může jít podívat do slovníku pod heslem „rychlost".',
    'Vedl jsi od začátku do konce.',
    'Zasloužená výhra — a bylo to znát.',
    'Trefa za trefou. Tohle se hned tak nevidí.',
    'Soupeř hrál dobře. Ty líp.',
    'Někdo si dneska musí dát odvetu.',
    'Body mluví za tebe.',
    'Přesně tak se to má hrát.',
    'Vyhrál jsi to hlavou, ne štěstím.',
    'Slovníkové vítězství.',
    'Tohle si zaslouží zůstat v přehledu.',
    'Soupeř tě bude chtít zpátky. Buď připravený.',
    'Rychle, přesně a bez zaváhání.',
    'Máš to. A bylo to o víc než o kousek.',
    'Kdo umí, umí.',
    'Dneska ti to myslelo.',
    'Vítězství jako z učebnice.',
    'Tohle byl tvůj souboj od první otázky.',
  ],
  loss: [
    'Dneska to bylo o kousek.',
    'Soupeř byl rychlejší. Příště ty.',
    'Body nesedly, hlava ano.',
    'Bylo to blízko — a to se počítá.',
    'Prohra s dobrým soupeřem není ostuda.',
    'Tentokrát vedle. Odveta je od toho, aby se tohle spravilo.',
    'Slova si tentokrát vybrala jeho.',
    'Chybělo málo. Vážně málo.',
    'Soupeř měl svůj den.',
    'Zkus to znovu, hned to bude vypadat jinak.',
    'Prohrát se dá i dobře odehraným soubojem.',
    'Tohle si vem jako rozcvičku.',
    'Byl rychlejší, ne chytřejší. To se dohání.',
    'Příští pětice bude tvoje.',
    'Nedopadlo to. Ale hrálo se pěkně.',
    'Soupeř má náskok. Zatím.',
    'Skóre říká svoje, ale nic nekončí.',
    'Někdy je rychlejší ten druhý. Dneska byl.',
    'Za tohle se hanbit nemusíš.',
    'Odveta čeká hned pod tímhle.',
  ],
  draw: [
    'Ani o bod. To se jen tak nepovede.',
    'Shoda až do posledního bodu.',
    'Rovnocenní soupeři — přesně o tomhle to je.',
    'Nikdo nevyhrál, nikdo neprohrál. A bylo to napínavé.',
    'Stejně rychlí, stejně přesní.',
    'Tohle volá po odvetě.',
    'Remíza, která se počítá za dobrou hru oběma.',
    'Bod k bodu. Zajímavé.',
    'Dva stejně dobří hráči, jeden výsledek.',
    'Nerozhodně — a nikdo si nemá co vyčítat.',
    'Přesná shoda. Skoro to vypadá domluveně.',
    'Ani jeden neustoupil.',
    'Tenhle souboj rozhodnutí nepřinesl. Ten další možná.',
    'Vyrovnané od začátku do konce.',
    'Remíza je nejtěžší výsledek. Máte ji.',
    'Stejné skóre, stejná zásluha.',
    'Nic mezi vámi není. Zatím.',
    'Souboj skončil tam, kde začal.',
    'Dva vítězové, žádný poražený.',
    'Tohle si žádá třetí kolo.',
  ],
}

/** Hláška pro tenhle konkrétní souboj — pořád tatáž, i po návratu. */
export function verdictLine(verdict: Verdict, id: string): string {
  const rada = VERDICT_LINES[verdict]
  let soucet = 0
  for (let i = 0; i < id.length; i += 1) soucet = (soucet * 31 + id.charCodeAt(i)) % 100_000
  return rada[soucet % rada.length]!
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
