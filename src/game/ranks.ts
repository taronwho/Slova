/**
 * Hodnosti profilu.
 *
 * Padesát stupňů od Nováčka po Vládce slov. Hodnost roste s **věhlasem** —
 * jediným číslem, do kterého se sčítají body ze všech pěti her. Hráč tak
 * vidí, že se mu počítá všechno, ať si zrovna zahrál cokoli.
 *
 * Prahy jsou naschvál nerovnoměrné. První tři hodnosti odsýpají, ať má nový
 * hráč co slavit hned první večer: druhá padne po jednom kole, třetí po
 * druhém, čtvrtá po pátém. Od té chvíle se rozestupy natahují o patnáct
 * procent na každém stupni, takže dvacátá hodnost je na dvě stě kol a
 * padesátá na dobrých jedenáct tisíc — na tu se hraje roky, ne měsíce.
 *
 * Odznak (RankBadge.tsx) se mění po pěti hodnostech: deset kovů a k nim pět
 * tvarů štítu, každý pro dva sousední kovy. Uvnitř pětice se hodnosti liší
 * počtem krokví. Za každou novou hodnost padne inkoust — kolik, říká
 * `rankInk` v economy.ts.
 */

export interface Rank {
  /** Pořadí 1–50, používá se i jako klíč do kresby odznaku. */
  index: number
  name: string
  /** Kolik věhlasu je potřeba nasbírat. */
  at: number
  /** 0–9; určuje kov odznaku a po dvou i tvar štítu. */
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
]

const THRESHOLDS = [
  0, 1_200, 3_000, 6_000, 9_500, 13_500, 18_000, 23_250, 29_250, 36_250,
  44_250, 53_500, 64_500, 76_500, 90_500, 106_500, 124_500, 145_500, 169_500, 197_500,
  229_500, 266_500, 309_500, 358_500, 414_500, 479_500, 554_500, 640_500, 739_500, 854_500,
  984_500, 1_134_500, 1_309_500, 1_509_500, 1_739_500, 2_004_500, 2_304_500, 2_649_500,
  3_049_500, 3_509_500,
  4_039_500, 4_649_500, 5_349_500, 6_154_500, 7_079_500, 8_154_500, 9_379_500, 10_779_500,
  12_404_500, 14_254_500,
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
