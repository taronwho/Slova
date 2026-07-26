/**
 * Hodnosti profilu.
 *
 * Padesát stupňů od Nováčka po Vládce slov. Hodnost je jediné číslo, které
 * roste přes všechny tři režimy dohromady — hráč tak vidí, že se mu počítá
 * všechno, ať si zrovna zahrál cokoli.
 *
 * Prahy jsou naschvál nerovnoměrné: prvních pár hodností odsýpá (ať má nový
 * hráč co slavit hned první večer) a rozestupy se pak plynule natahují, každý
 * o zhruba dvanáct procent. Průměrné dobré kolo dá kolem 1 200 bodů, takže
 * druhá hodnost padne po prvním kole a poslední je běh na hodně dlouhou trať.
 *
 * Odznak (RankBadge.tsx) se mění po pěti hodnostech: deset kovů a k nim pět
 * tvarů štítu, každý pro dva sousední kovy. Uvnitř pětice se hodnosti liší
 * počtem krokví. Za každou novou hodnost dostane hráč nápovědy zdarma —
 * kolik, říká RANK_HINTS.
 */

export interface Rank {
  /** Pořadí 1–50, používá se i jako klíč do kresby odznaku. */
  index: number
  name: string
  /** Kolik XP je potřeba nasbírat. */
  at: number
  /** 0–9; určuje kov odznaku a po dvou i tvar štítu. */
  tier: number
  /** Kolikátá hodnost uvnitř své pětice (0–4) — počet krokví pod odznakem. */
  step: number
}

/** Kolik nápověd zdarma padne za každou nově dosaženou hodnost. */
export const RANK_HINTS = 2

const NAMES = [
  'Nováček',
  'Slabikář',
  'Písmenkář',
  'Čtenář',
  'Opisovač',
  'Luštitel',
  'Písař',
  'Skladač slov',
  'Hláskomistr',
  'Slovař',
  'Sběratel slov',
  'Vypravěč',
  'Písmák',
  'Zapisovatel',
  'Skladatel',
  'Veršotepec',
  'Rétor',
  'Slovotepec',
  'Jazykozpytec',
  'Mistr slova',
  'Tvůrce vět',
  'Znalec kořenů',
  'Etymolog',
  'Lexikograf',
  'Velmistr',
  'Slovní alchymista',
  'Strážce pravopisu',
  'Kronikář',
  'Vykladač',
  'Arcimistr',
  'Bard',
  'Klenotník slov',
  'Slovní architekt',
  'Hlasatel',
  'Slovní mág',
  'Pán přesmyček',
  'Vládce plástve',
  'Kovář vět',
  'Strážce slovníku',
  'Legenda češtiny',
  'Mudrc',
  'Titán slovníku',
  'Věštec slov',
  'Nesmrtelný písmák',
  'Patriarcha jazyka',
  'Kníže slova',
  'Král slabik',
  'Císař češtiny',
  'Génius jazyka',
  'Vládce slov',
]

const THRESHOLDS = [
  0, 1_300, 2_800, 4_500, 6_300, 8_400, 10_500, 13_500, 16_000, 19_500,
  23_000, 27_000, 31_500, 36_500, 42_000, 48_000, 55_000, 62_500, 71_000, 80_500,
  91_000, 103_000, 116_000, 131_000, 147_000, 165_000, 186_000, 208_000, 234_000, 262_000,
  293_000, 328_000, 367_000, 411_000, 459_000, 514_000, 574_000, 641_000, 716_000, 800_000,
  894_000, 998_000, 1_115_000, 1_245_000, 1_385_000, 1_550_000, 1_730_000, 1_930_000,
  2_150_000, 2_400_000,
]

export const RANKS: Rank[] = NAMES.map((name, i) => ({
  index: i + 1,
  name,
  at: THRESHOLDS[i]!,
  tier: Math.floor(i / 5),
  step: i % 5,
}))

export interface RankProgress {
  rank: Rank
  next: Rank | null
  /** Kolik XP hráč nasbíral nad práh současné hodnosti. */
  into: number
  /** Kolik XP je mezi současnou a další hodností. 0 na konci žebříčku. */
  span: number
}

export function rankFor(xp: number): RankProgress {
  let at = 0
  while (at + 1 < RANKS.length && xp >= RANKS[at + 1]!.at) at += 1
  const rank = RANKS[at]!
  const next = RANKS[at + 1] ?? null
  return {
    rank,
    next,
    into: xp - rank.at,
    span: next ? next.at - rank.at : 0,
  }
}
