/**
 * Ocenění — trvalé mety napříč hrou.
 *
 * Slova mají vydržet roky, ne týden. Čtyřicet met se vyčerpá za pár večerů a
 * pak už není za čím jít, takže mety jsou postavené jako **žebříčky**: jedna
 * rodina, pět stupňů, poslední tak daleko, že se na něj hraje sezónu. Kdo hru
 * otevře poprvé, má první stupeň na dosah; kdo ji hraje pátým rokem, má pořád
 * rozdělaný ten pátý.
 *
 * Těžiště zůstává na **dovednosti, ne na vysedění**. Žebříčky mistrovství
 * počítají jen kola dohraná bez nápovědy — „odehraj sto kol" splní každý, kdo
 * vydrží klikat, „dohraj sto kol načisto" ne. Počty odehraných kol mají
 * vlastní, mnohem skromnější rodinu ve Vytrvalosti, protože i vytrvalost je
 * něco, ale není to totéž co umět.
 *
 * Rodiny se ve vitríně **nerozbalují celé**: vidíš získané stupně a hned
 * následující. Sto šedesát dlaždic naráz nikoho nemotivuje, jeden další stupeň
 * ano.
 *
 * Každá podmínka se čte **jen z profilu**, nikdy z právě dohraného kola.
 * Díky tomu se dají ocenění kdykoli přepočítat znovu (a při načtení profilu
 * se to taky dělá): kdyby některé kolo spadlo dřív, než se zapsalo, meta se
 * dožene sama, místo aby zůstala navždy zamčená. Profil proto vedle statistik
 * drží i pár počítadel, která se z běžných statistik odvodit nedají — čistá
 * kola, pangramy, dostavěné věže bez nápovědy, uhodnutá slova v Šibenici.
 *
 * Identifikátory jsou navěky. Podle nich se v uloženém profilu pozná, co už
 * hráč má; přejmenovat id znamená udělit ocenění (a inkoust za ně) podruhé.
 * Proto tu jsou i klíče, které se s dnešním názvem míjejí — `xp-50k` pro
 * věhlas, `skore-1500` pro pět set bodů. Nadpis se přepsat smí, klíč ne.
 */

import type { Profile } from '../lib/storage'
import type { ModeId } from './types'

const MODES: ModeId[] = ['chain', 'hive', 'tower', 'gallows', 'detective', 'tetris']

export type AwardGroup =
  | 'start'
  | 'clean'
  | 'score'
  | 'feat'
  | 'grit'
  | 'mastery'
  | 'habit'

/** Barva kresby. Meta patřící k jednomu režimu si bere jeho barvu. */
export type AwardTone =
  | 'brand'
  | 'chain'
  | 'hive'
  | 'tower'
  | 'gallows'
  | 'detective'
  | 'tetris'
  | 'ok'
  | 'gold'
  | 'warn'

export interface Award {
  id: string
  group: AwardGroup
  tone: AwardTone
  title: string
  /** Co je potřeba udělat — píše se do dlaždice i k zamčenému ocenění. */
  goal: string
  /** Kresba v AwardArt.tsx. */
  art: string
  /** Stupeň v rámci rodiny (1–5) — pod kresbou se ukáže tolik krokví. */
  tier?: number | undefined
  /**
   * Klíč rodiny. Vitrína podle něj sbalí žebříček na získané stupně a jeden
   * další. Samostatná meta rodinu nemá.
   */
  family?: string | undefined
  done: (profile: Profile) => boolean
  /** Kolik z cíle je hotovo (0–1). Zamčená dlaždice tím ukáže postup. */
  progress?: (profile: Profile) => number
}

export const GROUP_LABEL: Record<AwardGroup, string> = {
  start: 'První kroky',
  clean: 'Bez nápovědy',
  mastery: 'Mistrovství her',
  score: 'Body',
  feat: 'Mistrovské kousky',
  habit: 'Návyk',
  grit: 'Vytrvalost',
}

export const GROUP_NOTE: Record<AwardGroup, string> = {
  start: 'Než se rozkoukáš. Každá hra má svoje první.',
  clean: 'Kolo bez jediné nápovědy. Tady se pozná, kdo hraje sám za sebe.',
  mastery: 'Každá hra má vlastní žebříček od Učně po Legendu. Poslední stupeň je na roky.',
  score: 'Za body — v jednom kole i za celou dobu.',
  feat: 'Kousky, které se jen tak nepovedou.',
  habit: 'Za to, že se vracíš den po dni. Jediné mety, které nejdou dohnat jedním večerem.',
  grit: 'Za dlouhé série a nasbírané kilometry.',
}

export const AWARD_GROUPS: AwardGroup[] = [
  'start',
  'clean',
  'mastery',
  'score',
  'feat',
  'habit',
  'grit',
]

/** Podíl splnění, oříznutý na 0–1. */
function ratio(have: number, need: number): number {
  return Math.max(0, Math.min(have / need, 1))
}

/** Číslo tak, jak se píše česky — s pevnou mezerou po tisících. */
function fmt(n: number): string {
  return n.toLocaleString('cs-CZ')
}

/** Číslo se správným tvarem podstatného jména: 1 kolo, 3 kola, 8 kol. */
function plural(n: number, one: string, few: string, many: string): string {
  return `${fmt(n)} ${n === 1 ? one : n < 5 ? few : many}`
}

const rounds = (n: number) => plural(n, 'kolo', 'kola', 'kol')
const words = (n: number) => plural(n, 'slovo', 'slova', 'slov')
const days = (n: number) => plural(n, 'den', 'dny', 'dní')

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
  family?: string | undefined,
): Award {
  return {
    id,
    group,
    tone,
    title,
    goal,
    art,
    tier,
    family,
    done: (profile) => value(profile) >= need,
    progress: (profile) => ratio(value(profile), need),
  }
}

/** Jeden stupeň žebříčku. `id` se uvádí tam, kde meta existovala už dřív. */
interface Step {
  id?: string
  need: number
  title: string
  goal: string
}

/**
 * Žebříček — několik stupňů téže mety nad jedním číslem z profilu.
 *
 * Stupně se číslují od jedné a číslo se propíše do krokví pod kresbou, takže
 * hráč na dlaždici pozná, jak vysoko v rodině je, aniž by ji hledal v seznamu.
 */
function ladder(
  family: string,
  group: AwardGroup,
  tone: AwardTone,
  art: string,
  value: (profile: Profile) => number,
  steps: Step[],
): Award[] {
  return steps.map((step, i) =>
    count(
      step.id ?? `${family}-${step.need}`,
      group,
      tone,
      step.title,
      step.goal,
      art,
      step.need,
      value,
      i + 1,
      family,
    ),
  )
}

/** Co je potřeba vědět o hře, aby se z ní daly vyrobit její žebříčky. */
interface ModeInfo {
  id: ModeId
  /** První pád — do nadpisu. */
  name: string
  /** Druhý pád — „Mistr Řetězu". */
  of: string
  tone: AwardTone
  art: string
  /** Meta na nejlepší skóre v jednom kole: tři stupně. */
  score: [number, number, number]
}

const MODE_INFO: ModeInfo[] = [
  { id: 'chain', name: 'Řetěz', of: 'Řetězu', tone: 'chain', art: 'link', score: [830, 1200, 1700] },
  { id: 'hive', name: 'Voština', of: 'Voštiny', tone: 'hive', art: 'cell', score: [1330, 1900, 2600] },
  { id: 'tower', name: 'Věž', of: 'Věže', tone: 'tower', art: 'blocks', score: [660, 950, 1300] },
  { id: 'gallows', name: 'Šibenice', of: 'Šibenice', tone: 'gallows', art: 'noose', score: [380, 520, 700] },
  { id: 'detective', name: 'Detektiv', of: 'Detektiva', tone: 'detective', art: 'glass', score: [380, 520, 700] },
  // Slabiky mají bodovou stupnici na desetině ostatních her, viz scoreTetris.
  { id: 'tetris', name: 'Slabiky', of: 'Slabik', tone: 'tetris', art: 'deck', score: [45, 80, 140] },
]

/** Stupně mistrovství. Cechovní řeč — pasuje ke hře o slovech a řemesle. */
const MASTER_TITLES = ['Učeň', 'Tovaryš', 'Mistr', 'Velmistr', 'Legenda']
const MASTER_NEEDS = [3, 10, 30, 100, 300]

/** Žebříček mistrovství jedné hry: kola dohraná bez nápovědy. */
function masteryLadder(mode: ModeInfo): Award[] {
  return ladder(
    `mistr-${mode.id}`,
    'mastery',
    mode.tone,
    mode.art,
    (p) => p.stats[mode.id].clean,
    MASTER_NEEDS.map((need, i) => ({
      need,
      title: `${MASTER_TITLES[i]} ${mode.of}`,
      goal: `Dohraj ${rounds(need)} hry ${mode.name} bez nápovědy`,
    })),
  )
}

/** Žebříček nejlepšího skóre v jedné hře. */
function scoreLadder(mode: ModeInfo): Award[] {
  // První stupeň nese původní klíč, aby o něj nikdo nepřišel ani nedostal
  // inkoust dvakrát. Zbylé dva jsou nové.
  const first: Record<string, string | undefined> = {
    chain: 'retez-skore',
    hive: 'plastev-skore',
    tower: 'vez-skore',
  }
  return ladder(
    `skore-${mode.id}`,
    'score',
    mode.tone,
    'medal',
    (p) => p.stats[mode.id].bestScore,
    mode.score.map((need, i) => ({
      ...(i === 0 && first[mode.id] ? { id: first[mode.id]! } : {}),
      need,
      title: `${mode.name} na ${fmt(need)}`,
      goal: `Dohraj ${mode.name} za ${fmt(need)} bodů v jednom kole`,
    })),
  )
}

/** Stupeň žebříčku na čas: menší je lepší a nula znamená „zatím nic". */
interface FastStep {
  id?: string
  ms: number
  title: string
  goal: string
}

/**
 * Žebříček na čas.
 *
 * Zvlášť od `ladder`, protože se tu porovnává obráceně — a hlavně proto, že
 * nula v profilu neznamená „nekonečně rychle", ale „ještě se nepovedlo".
 * Postup se ukazuje jako podíl cíle k dosaženému času, takže se proužek plní,
 * jak se hráč zrychluje.
 */
function fastLadder(
  family: string,
  tone: AwardTone,
  art: string,
  value: (profile: Profile) => number,
  steps: FastStep[],
): Award[] {
  return steps.map((step, i) => ({
    id: step.id ?? `${family}-${Math.round(step.ms / 1000)}`,
    group: 'feat' as AwardGroup,
    tone,
    title: step.title,
    goal: step.goal,
    art,
    tier: i + 1,
    family,
    done: (profile: Profile) => {
      const ms = value(profile)
      return ms > 0 && ms <= step.ms
    },
    progress: (profile: Profile) => {
      const ms = value(profile)
      return ms > 0 ? ratio(step.ms, ms) : 0
    },
  }))
}

/** Kolik kol hráč odehrál dohromady, napříč všemi hrami. */
function totalPlayed(p: Profile): number {
  return MODES.reduce((sum, mode) => sum + p.stats[mode].played, 0)
}

export const AWARDS: Award[] = [
  // --- První kroky ------------------------------------------------------
  count('prvni-retez', 'start', 'chain', 'První řetěz', 'Dohraj kolo Řetězu', 'link', 1,
    (p) => p.stats.chain.played),
  count('prvni-plastev', 'start', 'hive', 'První plástev', 'Dohraj kolo Voštiny', 'cell', 1,
    (p) => p.stats.hive.played),
  count('prvni-vez', 'start', 'tower', 'První věž', 'Dohraj kolo Věže', 'blocks', 1,
    (p) => p.stats.tower.played),
  count('prvni-sibenice', 'start', 'gallows', 'První slovo', 'Uhodni slovo v Šibenici',
    'noose', 1, (p) => p.counters.gallowsSolved),
  count('prvni-pripad', 'start', 'detective', 'První případ',
    'Rozlušti slovo podle jeho původu', 'glass', 1, (p) => p.counters.detectiveSolved),
  count('prvni-davka', 'start', 'tetris', 'První slabiky', 'Slož slovo z padajících slabik',
    'blocks', 1, (p) => p.counters.tetrisWords),
  {
    id: 'petiboj',
    group: 'start',
    tone: 'brand',
    title: 'Všestranný',
    goal: 'Dohraj kolo v každé hře',
    art: 'triad',
    done: (p) => MODES.every((mode) => p.stats[mode].played > 0),
    progress: (p) => ratio(MODES.filter((mode) => p.stats[mode].played > 0).length, MODES.length),
  },

  // --- Bez nápovědy -----------------------------------------------------
  ...ladder('cisto', 'clean', 'ok', 'nohint', (p) => p.counters.noHint, [
    { id: 'cisto-1', need: 1, title: 'Vlastní hlavou', goal: 'Dohraj kolo bez jediné nápovědy' },
    { id: 'cisto-10', need: 10, title: 'Deset načisto', goal: 'Dohraj 10 kol bez jediné nápovědy' },
    { id: 'cisto-50', need: 50, title: 'Padesát načisto', goal: 'Dohraj 50 kol bez jediné nápovědy' },
    { need: 200, title: 'Dvě stě načisto', goal: 'Dohraj 200 kol bez jediné nápovědy' },
    { need: 750, title: 'Sedm set padesát načisto', goal: 'Dohraj 750 kol bez jediné nápovědy' },
  ]),
  ...ladder('retez-cisty', 'clean', 'chain', 'arrow', (p) => p.stats.chain.perfect, [
    { id: 'retez-cisty', need: 1, title: 'Čistý řetěz', goal: 'Dojdi na nejkratší cestu bez nápovědy' },
    { id: 'retez-cisty-10', need: 10, title: 'Deset čistých řetězů', goal: 'Dojdi na nejkratší cestu bez nápovědy desetkrát' },
    { need: 50, title: 'Padesát čistých řetězů', goal: 'Dojdi na nejkratší cestu bez nápovědy padesátkrát' },
  ]),
  ...ladder('plastev-cista', 'clean', 'hive', 'list', (p) => p.stats.hive.perfect, [
    { id: 'plastev-cista', need: 1, title: 'Plástev bez nápovědy', goal: 'Vysbírej celou plástev bez jediné nápovědy' },
    { need: 10, title: 'Deset pláství bez nápovědy', goal: 'Vysbírej celou plástev bez nápovědy desetkrát' },
    { need: 50, title: 'Padesát pláství bez nápovědy', goal: 'Vysbírej celou plástev bez nápovědy padesátkrát' },
  ]),
  ...ladder('vez-cista', 'clean', 'tower', 'flag', (p) => p.counters.towerFullNoHint, [
    { id: 'vez-cista', need: 1, title: 'Věž bez lešení', goal: 'Dostav věž až nahoru bez jediné nápovědy' },
    { id: 'vez-cista-10', need: 10, title: 'Deset věží bez lešení', goal: 'Dostav deset věží bez jediné nápovědy' },
    { need: 50, title: 'Padesát věží bez lešení', goal: 'Dostav padesát věží bez jediné nápovědy' },
  ]),
  ...ladder('sibenice-cista', 'clean', 'gallows', 'noose', (p) => p.counters.gallowsClean, [
    { id: 'sibenice-cista', need: 1, title: 'Napoprvé', goal: 'Uhodni slovo bez jediné chyby a bez nápovědy' },
    { id: 'sibenice-cista-10', need: 10, title: 'Deset napoprvé', goal: 'Uhodni deset slov bez jediné chyby a bez nápovědy' },
    { need: 50, title: 'Padesát napoprvé', goal: 'Uhodni padesát slov bez jediné chyby a bez nápovědy' },
  ]),
  ...ladder('detektiv-cisty', 'clean', 'detective', 'glass', (p) => p.stats.detective.perfect, [
    { id: 'detektiv-cisty', need: 1, title: 'Bez škobrtnutí', goal: 'Rozlušti případ bez chybného písmene a bez nápovědy' },
    { id: 'detektiv-cisty-10', need: 10, title: 'Deset bez škobrtnutí', goal: 'Rozlušti deset případů bez chyby a bez nápovědy' },
    { need: 50, title: 'Padesát bez škobrtnutí', goal: 'Rozlušti padesát případů bez chyby a bez nápovědy' },
  ]),
  ...ladder('slabiky-ciste', 'clean', 'tetris', 'deck', (p) => p.stats.tetris.perfect, [
    { id: 'slabiky-ciste', need: 1, title: 'Tucet ze slabik', goal: 'Slož v jednom kole tucet slov bez nápovědy' },
    { id: 'slabiky-ciste-10', need: 10, title: 'Deset tuctů', goal: 'Zvládni to desetkrát' },
    { need: 50, title: 'Padesát tuctů', goal: 'Zvládni to padesátkrát' },
  ]),

  // --- Mistrovství her --------------------------------------------------
  ...MODE_INFO.flatMap(masteryLadder),

  // --- Body -------------------------------------------------------------
  ...ladder('skore', 'score', 'gold', 'peak', (p) => p.counters.bestScore, [
    { id: 'skore-1500', need: 500, title: 'Pět set', goal: 'Nasbírej v jednom kole 500 bodů' },
    { id: 'skore-3000', need: 1000, title: 'Tisíc', goal: 'Nasbírej v jednom kole 1 000 bodů' },
    { id: 'skore-5000', need: 1700, title: 'Sedmnáct set', goal: 'Nasbírej v jednom kole 1 700 bodů' },
    { need: 2600, title: 'Šestadvacet set', goal: 'Nasbírej v jednom kole 2 600 bodů' },
    { need: 4000, title: 'Čtyři tisíce', goal: 'Nasbírej v jednom kole 4 000 bodů' },
  ]),
  ...ladder('vehlas', 'score', 'gold', 'deck', (p) => p.fame, [
    { id: 'xp-50k', need: 17_000, title: 'Sedmnáct tisíc', goal: 'Nasbírej 17 000 věhlasu' },
    { id: 'xp-250k', need: 80_000, title: 'Osmdesát tisíc', goal: 'Nasbírej 80 000 věhlasu' },
    { need: 300_000, title: 'Tři sta tisíc', goal: 'Nasbírej 300 000 věhlasu' },
    { need: 1_000_000, title: 'Milion', goal: 'Nasbírej milion věhlasu' },
    { need: 3_000_000, title: 'Tři miliony', goal: 'Nasbírej tři miliony věhlasu' },
  ]),
  ...MODE_INFO.flatMap(scoreLadder),

  // --- Mistrovské kousky ------------------------------------------------
  // Voština
  ...ladder('pangram', 'feat', 'hive', 'star-cell', (p) => p.counters.pangrams, [
    { id: 'pangram-1', need: 1, title: 'Pangram', goal: 'Najdi slovo ze všech sedmi písmen' },
    { id: 'pangram-10', need: 10, title: 'Pangramista', goal: 'Najdi deset pangramů' },
    { need: 50, title: 'Pangramový lovec', goal: 'Najdi padesát pangramů' },
    { need: 200, title: 'Pangramová legenda', goal: 'Najdi dvě stě pangramů' },
  ]),
  ...ladder('plastev-cela', 'feat', 'hive', 'comb', (p) => p.counters.hiveFull, [
    { id: 'plastev-cela', need: 1, title: 'Kompletní plástev', goal: 'Najdi v plástvi všechna slova' },
    { need: 10, title: 'Deset kompletních pláství', goal: 'Vysbírej plástev do posledního slova desetkrát' },
    { need: 50, title: 'Padesát kompletních pláství', goal: 'Vysbírej plástev do posledního slova padesátkrát' },
  ]),
  ...ladder('kralovna', 'feat', 'hive', 'crown', (p) => p.counters.hiveQueen, [
    { id: 'kralovna', need: 1, title: 'Královna češtiny', goal: 'Dosáhni v plástvi nejvyšší hodnosti' },
    { need: 10, title: 'Královna podesáté', goal: 'Dosáhni v plástvi nejvyšší hodnosti desetkrát' },
    { need: 50, title: 'Rod královen', goal: 'Dosáhni v plástvi nejvyšší hodnosti padesátkrát' },
  ]),
  ...ladder('plastev-slov', 'feat', 'hive', 'list', (p) => p.counters.hiveBestWords, [
    { need: 20, title: 'Dvacet z plástve', goal: `Najdi v jedné plástvi ${words(20)}` },
    { need: 35, title: 'Pětatřicet z plástve', goal: `Najdi v jedné plástvi ${words(35)}` },
    { need: 50, title: 'Padesát z plástve', goal: `Najdi v jedné plástvi ${words(50)}` },
  ]),

  // Řetěz
  ...ladder('retez-par', 'feat', 'chain', 'arrow', (p) => p.counters.chainPar, [
    { need: 10, title: 'Deset nejkratších cest', goal: 'Dohraj Řetěz na počet tahů nejkratší cesty desetkrát' },
    { need: 50, title: 'Padesát nejkratších cest', goal: 'Dohraj Řetěz na nejkratší cestu padesátkrát' },
    { need: 200, title: 'Dvě stě nejkratších cest', goal: 'Dohraj Řetěz na nejkratší cestu dvěstěkrát' },
    { need: 600, title: 'Šest set nejkratších cest', goal: 'Dohraj Řetěz na nejkratší cestu šestsetkrát' },
  ]),
  // Rychlost se měří jen u kol bez nápovědy — s „Celé slovo" je pod minutou
  // každý řetěz a meta by nic neznamenala.
  ...fastLadder('retez-rychlik', 'chain', 'bolt', (p) => p.counters.chainFastMs, [
    { id: 'retez-rychlik', ms: 60_000, title: 'Bleskový převod', goal: 'Dohraj Řetěz bez nápovědy do jedné minuty' },
    { ms: 45_000, title: 'Blesk podruhé', goal: 'Dohraj Řetěz bez nápovědy do 45 sekund' },
    { ms: 30_000, title: 'Rychlejší než myšlenka', goal: 'Dohraj Řetěz bez nápovědy do 30 sekund' },
  ]),

  // Věž
  ...ladder('vez-patro', 'feat', 'tower', 'wide', (p) => p.counters.towerBestFloor, [
    { id: 'vez-osm', need: 8, title: 'Osmé patro', goal: 'Postav patro z osmi písmen' },
    { need: 9, title: 'Deváté patro', goal: 'Postav patro z devíti písmen' },
    { need: 10, title: 'Desáté patro', goal: 'Postav patro z deseti písmen' },
  ]),
  ...ladder('vez-cela', 'feat', 'tower', 'flag', (p) => p.counters.towerFull, [
    { need: 5, title: 'Pět hotových věží', goal: 'Dostav věž až nahoru pětkrát' },
    { need: 25, title: 'Pětadvacet hotových věží', goal: 'Dostav věž až nahoru pětadvacetkrát' },
    { need: 100, title: 'Sto hotových věží', goal: 'Dostav věž až nahoru stokrát' },
    { need: 400, title: 'Čtyři sta hotových věží', goal: 'Dostav věž až nahoru čtyřistakrát' },
  ]),
  ...fastLadder('vez-rychla', 'tower', 'bolt', (p) => p.counters.towerFastMs, [
    { ms: 180_000, title: 'Svižná stavba', goal: 'Dostav věž do tří minut' },
    { ms: 120_000, title: 'Stavba na dvě minuty', goal: 'Dostav věž do dvou minut' },
  ]),

  // Šibenice
  ...ladder('sibenice', 'feat', 'gallows', 'noose', (p) => p.counters.gallowsSolved, [
    { need: 10, title: 'Deset z oprátky', goal: `Uhodni v Šibenici ${words(10)}` },
    { need: 50, title: 'Padesát z oprátky', goal: `Uhodni v Šibenici ${words(50)}` },
    { need: 200, title: 'Dvě stě z oprátky', goal: `Uhodni v Šibenici ${words(200)}` },
    { need: 800, title: 'Osm set z oprátky', goal: `Uhodni v Šibenici ${words(800)}` },
  ]),

  // Detektiv
  ...ladder('detektiv', 'feat', 'detective', 'glass', (p) => p.counters.detectiveSolved, [
    { need: 10, title: 'Deset případů', goal: 'Rozlušti deset slov podle jejich původu' },
    { need: 50, title: 'Padesát případů', goal: 'Rozlušti padesát slov podle jejich původu' },
    { need: 200, title: 'Dvě stě případů', goal: 'Rozlušti dvě stě slov podle jejich původu' },
    { need: 800, title: 'Osm set případů', goal: 'Rozlušti osm set slov podle jejich původu' },
  ]),
  ...ladder('detektiv-tip', 'feat', 'detective', 'bolt', (p) => p.counters.detectiveGuessed, [
    { id: 'detektiv-tip', need: 1, title: 'Z první ruky', goal: 'Tipni slovo, když je ještě víc než půlka písmen skrytá' },
    { need: 10, title: 'Deset z první ruky', goal: 'Tipni slovo z málo písmen desetkrát' },
    { need: 50, title: 'Padesát z první ruky', goal: 'Tipni slovo z málo písmen padesátkrát' },
  ]),

  // Slabiky
  ...ladder('slabiky-slov', 'feat', 'tetris', 'list', (p) => p.counters.tetrisWords, [
    { id: 'slabiky-100', need: 100, title: 'Sto slov ze slabik', goal: 'Slož ze slabik sto slov celkem' },
    { need: 500, title: 'Pět set slov ze slabik', goal: 'Slož ze slabik pět set slov celkem' },
    { need: 2000, title: 'Dva tisíce slov ze slabik', goal: 'Slož ze slabik dva tisíce slov celkem' },
    { need: 8000, title: 'Osm tisíc slov ze slabik', goal: 'Slož ze slabik osm tisíc slov celkem' },
  ]),
  ...ladder('slabiky-retez', 'feat', 'tetris', 'chain3', (p) => p.counters.tetrisChain, [
    { id: 'slabiky-retez', need: 3, title: 'Domino', goal: 'Slož jedním dopadem řetěz tří slov' },
    { need: 4, title: 'Čtyřnásobné domino', goal: 'Slož jedním dopadem řetěz čtyř slov' },
    { need: 5, title: 'Pětinásobné domino', goal: 'Slož jedním dopadem řetěz pěti slov' },
  ]),

  // --- Návyk ------------------------------------------------------------
  // Jediná rodina, kterou nejde dohnat jedním večerem: den se počítá jednou,
  // ať se ho odehraje kolo nebo dvacet.
  ...ladder('den-v-rade', 'habit', 'warn', 'flame', (p) => p.bestDayStreak, [
    { need: 3, title: 'Tři dny v řadě', goal: 'Hraj tři dny po sobě' },
    { need: 7, title: 'Týden v řadě', goal: 'Hraj sedm dní po sobě' },
    { need: 30, title: 'Měsíc v řadě', goal: 'Hraj třicet dní po sobě' },
    { need: 100, title: 'Sto dní v řadě', goal: 'Hraj sto dní po sobě' },
    { need: 365, title: 'Rok v řadě', goal: 'Hraj tři sta pětašedesát dní po sobě' },
  ]),
  ...ladder('dnu', 'habit', 'brand', 'day', (p) => p.daysPlayed, [
    { need: 10, title: 'Deset dnů se Slovy', goal: `Zahraj si celkem ${days(10)}` },
    { need: 50, title: 'Padesát dnů se Slovy', goal: `Zahraj si celkem ${days(50)}` },
    { need: 150, title: 'Sto padesát dnů se Slovy', goal: `Zahraj si celkem ${days(150)}` },
    { need: 365, title: 'Rok se Slovy', goal: `Zahraj si celkem ${days(365)}` },
    { need: 1000, title: 'Tisíc dnů se Slovy', goal: `Zahraj si celkem ${days(1000)}` },
  ]),
  ...ladder('denni', 'habit', 'warn', 'day', (p) => p.counters.dailies, [
    { id: 'denni-7', need: 7, title: 'Týden výzev', goal: 'Dohraj sedm denních výzev' },
    { need: 30, title: 'Třicet výzev', goal: 'Dohraj třicet denních výzev' },
    { need: 100, title: 'Sto výzev', goal: 'Dohraj sto denních výzev' },
    { need: 365, title: 'Rok výzev', goal: 'Dohraj tři sta pětašedesát denních výzev' },
    { need: 1000, title: 'Tisíc výzev', goal: 'Dohraj tisíc denních výzev' },
  ]),
  // Otázka dne se dá zahrát jen jednou denně, takže i její mety běží v čase
  // a ne v počtu odehraných kol — dohnat se nedají.
  ...ladder('otazka', 'habit', 'gold', 'glass', (p) => p.quiz.solved, [
    { need: 1, title: 'První trefa', goal: 'Uhodni Otázku dne' },
    { need: 10, title: 'Deset otázek', goal: 'Uhodni deset Otázek dne' },
    { need: 50, title: 'Padesát otázek', goal: 'Uhodni padesát Otázek dne' },
    { need: 200, title: 'Dvě stě otázek', goal: 'Uhodni dvě stě Otázek dne' },
    { need: 700, title: 'Sedm set otázek', goal: 'Uhodni sedm set Otázek dne' },
  ]),
  ...ladder('otazka-serie', 'habit', 'warn', 'flame', (p) => p.quiz.bestStreak, [
    { need: 5, title: 'Pět otázek v řadě', goal: 'Uhodni Otázku dne pět dní po sobě' },
    { need: 20, title: 'Dvacet otázek v řadě', goal: 'Uhodni Otázku dne dvacet dní po sobě' },
    { need: 60, title: 'Šedesát otázek v řadě', goal: 'Uhodni Otázku dne šedesát dní po sobě' },
  ]),
  ...ladder('otazka-znalec', 'feat', 'gold', 'peak', (p) => p.quiz.expert, [
    { need: 1, title: 'Na jedinou indicii', goal: 'Uhodni Otázku dne jen z první, nejtěžší indicie' },
    { need: 10, title: 'Desetkrát na jedinou', goal: 'Uhodni deset Otázek dne z jediné indicie' },
    { need: 50, title: 'Padesátkrát na jedinou', goal: 'Uhodni padesát Otázek dne z jediné indicie' },
  ]),
  ...ladder('varka', 'habit', 'gold', 'triad', (p) => p.counters.dailySets, [
    { need: 1, title: 'Celá várka', goal: 'Dohraj v jeden den denní výzvu v každé hře' },
    { need: 10, title: 'Deset várek', goal: 'Zvládni celou denní várku desetkrát' },
    { need: 50, title: 'Padesát várek', goal: 'Zvládni celou denní várku padesátkrát' },
    { need: 200, title: 'Dvě stě várek', goal: 'Zvládni celou denní várku dvěstěkrát' },
  ]),

  // --- Vytrvalost -------------------------------------------------------
  // Série je řada kol dohraných bez jediné nápovědy. Dřív se počítalo každé
  // odehrané kolo, takže série osmnácti mohla vzniknout z osmnácti prohraných
  // šibenic — to nedávalo smysl a hráč to nahlásil.
  ...ladder('serie', 'grit', 'ok', 'gem', (p) => p.bestStreak, [
    { id: 'cisto-v-rade', need: 5, title: 'Pět načisto v řadě', goal: 'Dohraj pět kol za sebou bez jediné nápovědy' },
    { id: 'serie-7', need: 10, title: 'Ve formě', goal: 'Dohraj deset kol za sebou bez jediné nápovědy' },
    { need: 20, title: 'V ráži', goal: 'Dohraj dvacet kol za sebou bez jediné nápovědy' },
    { id: 'serie-30', need: 40, title: 'Bez zaváhání', goal: 'Dohraj čtyřicet kol za sebou bez jediné nápovědy' },
    { need: 80, title: 'Neomylný', goal: 'Dohraj osmdesát kol za sebou bez jediné nápovědy' },
  ]),
  ...ladder('kol', 'grit', 'brand', 'deck', totalPlayed, [
    { need: 50, title: 'Padesát kol', goal: `Odehraj celkem ${rounds(50)}` },
    { need: 250, title: 'Dvě stě padesát kol', goal: `Odehraj celkem ${rounds(250)}` },
    { need: 1000, title: 'Tisíc kol', goal: `Odehraj celkem ${rounds(1000)}` },
    { need: 3000, title: 'Tři tisíce kol', goal: `Odehraj celkem ${rounds(3000)}` },
    { need: 10_000, title: 'Deset tisíc kol', goal: `Odehraj celkem ${rounds(10_000)}` },
  ]),
]

export function awardById(id: string): Award | undefined {
  return AWARDS.find((award) => award.id === id)
}

/**
 * Co z rodiny ukázat ve vitríně: získané stupně a první nezískaný.
 *
 * Kdyby se vysypalo všech sto šedesát dlaždic naráz, hráč by mezi nimi ztratil
 * ten jeden, na který zrovna dosáhne. Samostatné mety projdou beze změny.
 */
export function visibleAwards(list: Award[], profile: Profile): Award[] {
  const shown: Award[] = []
  const openFamily = new Set<string>()
  for (const award of list) {
    if (!award.family) {
      shown.push(award)
      continue
    }
    const has = profile.awards[award.id] !== undefined
    if (has) {
      shown.push(award)
      continue
    }
    // První nezískaný stupeň rodiny je ten, na který se hraje. Další už ne.
    if (openFamily.has(award.family)) continue
    openFamily.add(award.family)
    shown.push(award)
  }
  return shown
}
