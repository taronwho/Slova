/**
 * Ocenění — třicet trvalých met napříč hrou.
 *
 * Těžiště je na **dovednosti, ne na vysedění**: většina met stojí na tom, že
 * hráč kolo dohrál bez nápovědy, nebo že v něm nasbíral hodně bodů. „Odehraj
 * padesát kol" je meta, kterou splní každý, kdo vydrží klikat, a proto tu
 * takové skoro nejsou — jediné počty, které se počítají, jsou počty *čistých*
 * kol.
 *
 * Každá podmínka se čte **jen z profilu**, nikdy z právě dohraného kola.
 * Díky tomu se dají ocenění kdykoli přepočítat znovu (a při načtení profilu
 * se to taky dělá): kdyby některé kolo spadlo dřív, než se zapsalo, meta se
 * dožene sama, místo aby zůstala navždy zamčená. Profil proto vedle statistik
 * drží i pár počítadel, která se z běžných statistik odvodit nedají — čistá
 * kola, pangramy, dostavěné věže bez nápovědy.
 */

import type { Profile } from '../lib/storage'

export type AwardGroup = 'start' | 'clean' | 'score' | 'feat' | 'grit'

/** Barva kresby. Meta patřící k jednomu režimu si bere jeho barvu. */
export type AwardTone = 'brand' | 'chain' | 'hive' | 'tower' | 'ok' | 'gold' | 'warn'

export interface Award {
  id: string
  group: AwardGroup
  tone: AwardTone
  title: string
  /** Co je potřeba udělat — píše se do dlaždice i k zamčenému ocenění. */
  goal: string
  /** Kresba v AwardArt.tsx. */
  art: string
  /** Stupeň v rámci rodiny (1–3) — pod kresbou se ukáže tolik krokví. */
  tier?: number | undefined
  done: (profile: Profile) => boolean
  /** Kolik z cíle je hotovo (0–1). Zamčená dlaždice tím ukáže postup. */
  progress?: (profile: Profile) => number
}

export const GROUP_LABEL: Record<AwardGroup, string> = {
  start: 'První kroky',
  clean: 'Bez nápovědy',
  score: 'Body',
  feat: 'Mistrovské kousky',
  grit: 'Vytrvalost',
}

export const GROUP_NOTE: Record<AwardGroup, string> = {
  start: 'Než se rozkoukáš.',
  clean: 'Kolo bez jediné nápovědy. Tady se pozná, kdo hraje sám za sebe.',
  score: 'Za body — v jednom kole i za celou dobu.',
  feat: 'Kousky, které se jen tak nepovedou.',
  grit: 'Za to, že se vracíš.',
}

/** Podíl splnění, oříznutý na 0–1. */
function ratio(have: number, need: number): number {
  return Math.max(0, Math.min(have / need, 1))
}

/** Meta na počet: stejná podmínka i ukazatel postupu z jednoho čísla. */
function count(
  id: string,
  group: AwardGroup,
  tone: AwardTone,
  title: string,
  goal: string,
  art: string,
  need: number,
  value: (profile: Profile) => number,
  tier?: number | undefined,
): Award {
  return {
    id,
    group,
    tone,
    title,
    goal,
    art,
    tier,
    done: (profile) => value(profile) >= need,
    progress: (profile) => ratio(value(profile), need),
  }
}

export const AWARDS: Award[] = [
  // --- První kroky ------------------------------------------------------
  count('prvni-retez', 'start', 'chain', 'První řetěz', 'Dohraj kolo Řetězu', 'link', 1,
    (p) => p.stats.chain.played),
  count('prvni-plastev', 'start', 'hive', 'První plástev', 'Dohraj kolo Voštiny', 'cell', 1,
    (p) => p.stats.hive.played),
  count('prvni-vez', 'start', 'tower', 'První věž', 'Dohraj kolo Věže', 'blocks', 1,
    (p) => p.stats.tower.played),
  {
    id: 'trojboj',
    group: 'start',
    tone: 'brand',
    title: 'Trojboj',
    goal: 'Dohraj kolo ve všech třech hrách',
    art: 'triad',
    done: (p) => p.stats.chain.played > 0 && p.stats.hive.played > 0 && p.stats.tower.played > 0,
    progress: (p) =>
      ratio(
        [p.stats.chain.played, p.stats.hive.played, p.stats.tower.played].filter((n) => n > 0)
          .length,
        3,
      ),
  },

  // --- Bez nápovědy -----------------------------------------------------
  count('cisto-1', 'clean', 'ok', 'Vlastní hlavou', 'Dohraj kolo bez jediné nápovědy',
    'nohint', 1, (p) => p.counters.noHint, 1),
  count('cisto-10', 'clean', 'ok', 'Deset načisto', 'Dohraj 10 kol bez jediné nápovědy',
    'nohint', 10, (p) => p.counters.noHint, 2),
  count('cisto-50', 'clean', 'ok', 'Padesát načisto', 'Dohraj 50 kol bez jediné nápovědy',
    'nohint', 50, (p) => p.counters.noHint, 3),
  count('cisto-v-rade', 'clean', 'ok', 'Pět načisto v řadě',
    'Dohraj pět kol za sebou bez jediné nápovědy', 'gem', 5,
    (p) => p.counters.bestNoHintStreak),
  count('retez-cisty', 'clean', 'chain', 'Čistý řetěz',
    'Dojdi na nejkratší cestu bez nápovědy', 'arrow', 1, (p) => p.stats.chain.perfect, 1),
  count('retez-cisty-10', 'clean', 'chain', 'Deset čistých řetězů',
    'Dojdi na nejkratší cestu bez nápovědy desetkrát', 'chain3', 10,
    (p) => p.stats.chain.perfect, 3),
  count('plastev-cista', 'clean', 'hive', 'Plástev bez nápovědy',
    'Vysbírej celou plástev bez jediné nápovědy', 'list', 1, (p) => p.stats.hive.perfect),
  count('vez-cista', 'clean', 'tower', 'Věž bez lešení',
    'Dostav věž až nahoru bez jediné nápovědy', 'flag', 1,
    (p) => p.counters.towerFullNoHint, 1),
  count('vez-cista-10', 'clean', 'tower', 'Deset věží bez lešení',
    'Dostav deset věží bez jediné nápovědy', 'flag', 10,
    (p) => p.counters.towerFullNoHint, 3),

  // --- Body -------------------------------------------------------------
  count('skore-1500', 'score', 'gold', 'Patnáct set', 'Nasbírej v jednom kole 1 500 bodů',
    'peak', 1500, (p) => p.counters.bestScore, 1),
  count('skore-3000', 'score', 'gold', 'Tři tisíce', 'Nasbírej v jednom kole 3 000 bodů',
    'peak', 3000, (p) => p.counters.bestScore, 2),
  count('skore-5000', 'score', 'gold', 'Pět tisíc', 'Nasbírej v jednom kole 5 000 bodů',
    'peak', 5000, (p) => p.counters.bestScore, 3),
  count('retez-skore', 'score', 'chain', 'Mistrovský řetěz', 'Dohraj Řetěz za 2 500 bodů',
    'medal', 2500, (p) => p.stats.chain.bestScore),
  count('plastev-skore', 'score', 'hive', 'Bohatá plástev', 'Dohraj Voštinu za 4 000 bodů',
    'medal', 4000, (p) => p.stats.hive.bestScore),
  count('vez-skore', 'score', 'tower', 'Vysoké skóre věže', 'Dohraj Věž za 2 000 bodů',
    'medal', 2000, (p) => p.stats.tower.bestScore),
  count('xp-50k', 'score', 'gold', 'Padesát tisíc', 'Nasbírej 50 000 XP', 'deck', 50_000,
    (p) => p.xp, 1),
  count('xp-250k', 'score', 'gold', 'Čtvrt milionu', 'Nasbírej 250 000 XP', 'deck', 250_000,
    (p) => p.xp, 3),

  // --- Mistrovské kousky ------------------------------------------------
  count('pangram-1', 'feat', 'hive', 'Pangram', 'Najdi slovo ze všech sedmi písmen',
    'star-cell', 1, (p) => p.counters.pangrams, 1),
  count('pangram-10', 'feat', 'hive', 'Pangramista', 'Najdi deset pangramů', 'star-cell', 10,
    (p) => p.counters.pangrams, 3),
  count('plastev-cela', 'feat', 'hive', 'Kompletní plástev', 'Najdi v plástvi všechna slova',
    'comb', 1, (p) => p.counters.hiveFull),
  count('kralovna', 'feat', 'hive', 'Královna češtiny', 'Dosáhni v plástvi nejvyšší hodnosti',
    'crown', 1, (p) => p.counters.hiveQueen),
  count('vez-osm', 'feat', 'tower', 'Osmé patro', 'Postav patro z osmi písmen', 'wide', 8,
    (p) => p.counters.towerBestFloor),
  {
    id: 'retez-rychlik',
    group: 'feat',
    tone: 'chain',
    title: 'Bleskový převod',
    goal: 'Dohraj Řetěz bez nápovědy do jedné minuty',
    art: 'bolt',
    done: (p) => p.counters.chainFastMs > 0 && p.counters.chainFastMs <= 60_000,
  },

  // --- Vytrvalost -------------------------------------------------------
  count('serie-7', 'grit', 'warn', 'Ve formě', 'Dohraj sedm kol za sebou bez vzdání', 'flame', 7,
    (p) => p.bestStreak, 1),
  count('serie-30', 'grit', 'warn', 'Bez zaváhání', 'Dohraj třicet kol za sebou bez vzdání',
    'flame', 30, (p) => p.bestStreak, 3),
  count('denni-7', 'grit', 'warn', 'Týden výzev', 'Dohraj sedm denních výzev', 'day', 7,
    (p) => p.counters.dailies),
]

export const AWARD_GROUPS: AwardGroup[] = ['start', 'clean', 'score', 'feat', 'grit']

export function awardById(id: string): Award | undefined {
  return AWARDS.find((award) => award.id === id)
}
