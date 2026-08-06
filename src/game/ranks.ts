/**
 * Hodnosti profilu.
 *
 * Osmapadesát stupňů od Nováčka po Nesmrtelného písaře. Hodnost roste
 * s **věhlasem** —
 * jediným číslem, do kterého se sčítají body ze všech her. Hráč tak
 * vidí, že se mu počítá všechno, ať si zrovna zahrál cokoli.
 *
 * Prahy jsou naschvál nerovnoměrné. První tři hodnosti odsýpají, ať má nový
 * hráč co slavit hned první večer: druhá padne po jednom kole, třetí po
 * druhém, čtvrtá po pátém. Od té chvíle se rozestupy natahují o patnáct
 * procent na každém stupni, takže dvacátá hodnost je na dvě stě kol
 * a poslední na deset milionů věhlasu — na tu se hraje roky, ne měsíce.
 *
 * Odznak (RankBadge.tsx) se do pětačtyřicáté hodnosti mění po pěti stupních:
 * devět kovů a k nim pět tvarů štítu, každý pro dva sousední kovy; uvnitř
 * pětice se hodnosti liší počtem krokví. Posledních třináct hodností má
 * vlastní kresbu (crests.tsx) — na těch stupních se hraje roky a odznak
 * odlišený jen krokví by za tu cestu byl málo. Za každou novou hodnost padne
 * inkoust — kolik, říká `rankInk` v economy.ts.
 */

export interface Rank {
  /** Pořadí 1–58, používá se i jako klíč do kresby odznaku. */
  index: number
  name: string
  /** Kolik věhlasu je potřeba nasbírat. */
  at: number
  /** Určuje kov odznaku a po dvou i tvar štítu. Od 46. hodnosti se nepoužije. */
  tier: number
  /** Kolikátá hodnost uvnitř své pětice (0–4) — počet krokví pod odznakem. */
  step: number
}

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
  'Strážce jazyka',
  'Kníže slovníku',
  'Věčný luštitel',
  'Slovní kronikář',
  'Patriarcha češtiny',
  'Živoucí slovník',
  'Legenda Slov',
  'Nesmrtelný písař',
]

const THRESHOLDS = [
  0, 400, 1_000, 2_000, 3_200, 4_500, 6_000, 7_800, 9_800, 12_000,
  15_000, 18_100, 21_600, 25_600, 30_100, 35_600, 41_600, 48_600, 56_600, 66_100,
  76_600, 89_100, 102_600, 120_100, 138_100, 160_600, 185_600, 213_100, 248_100, 285_600,
  328_100, 378_100, 438_100, 503_100, 580_600, 668_100, 768_100, 883_100, 1_020_600, 1_170_600,
  1_350_600, 1_550_600, 1_780_600, 2_050_600, 2_360_600, 2_720_600, 3_130_600, 3_590_600, 4_130_600, 4_750_600,
  // Padesátá osmá hodnost stojí přesně deset milionů věhlasu. Rozestupy se
  // dál natahují, takže poslední stupně jsou na roky hraní.
  5_380_600, 6_018_000, 6_662_800, 7_315_000,
  7_974_600, 8_641_600, 9_316_000, 10_000_000,
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
  /** Kolik věhlasu hráč nasbíral nad práh současné hodnosti. */
  into: number
  /** Kolik věhlasu je mezi současnou a další hodností. 0 na konci žebříčku. */
  span: number
}

export function rankFor(fame: number): RankProgress {
  let at = 0
  while (at + 1 < RANKS.length && fame >= RANKS[at + 1]!.at) at += 1
  const rank = RANKS[at]!
  const next = RANKS[at + 1] ?? null
  return {
    rank,
    next,
    into: fame - rank.at,
    span: next ? next.at - rank.at : 0,
  }
}
