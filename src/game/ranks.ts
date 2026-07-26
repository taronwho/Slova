/**
 * Hodnosti profilu.
 *
 * Dvacet stupňů od Nováčka po Vládce slov. Hodnost je jediné číslo, které
 * roste přes všechny tři režimy dohromady — hráč tak vidí, že se mu počítá
 * všechno, ať si zrovna zahrál cokoli.
 *
 * Prahy jsou naschvál nerovnoměrné: prvních pět hodností odsýpá (ať má nový
 * hráč co slavit hned první večer), od desítky se rozestupy natahují a
 * poslední čtyři jsou běh na dlouhou trať. Průměrné dobré kolo dá kolem
 * 1 200 bodů, takže poslední hodnost je zhruba pět set kol.
 *
 * Čtyři pětice hodností mají čtyři různé odznaky (bronz, stříbro, zlato,
 * plazma) a uvnitř pětice se liší počtem stupňů — kresba je v RankBadge.tsx.
 */

export interface Rank {
  /** Pořadí 1–20, používá se i jako klíč do kresby odznaku. */
  index: number
  name: string
  /** Kolik XP je potřeba nasbírat. */
  at: number
  /** 0 bronz, 1 stříbro, 2 zlato, 3 plazma. */
  tier: number
  /** Kolikátá hodnost uvnitř svého kovu (0–4) — počet stupňů pod odznakem. */
  step: number
}

const NAMES = [
  'Nováček',
  'Slabikář',
  'Písmenkář',
  'Luštitel',
  'Písař',
  'Skladač slov',
  'Slovař',
  'Hláskomistr',
  'Vypravěč',
  'Písmák',
  'Skladatel',
  'Rétor',
  'Jazykozpytec',
  'Slovotepec',
  'Mistr slova',
  'Velmistr',
  'Strážce slovníku',
  'Kronikář',
  'Legenda češtiny',
  'Vládce slov',
]

const THRESHOLDS = [
  0, 1_500, 4_000, 8_000, 14_000, 22_000, 33_000, 47_000, 65_000, 88_000,
  115_000, 148_000, 188_000, 235_000, 292_000, 360_000, 440_000, 535_000,
  650_000, 800_000,
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
