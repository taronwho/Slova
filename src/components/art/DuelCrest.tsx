/**
 * Erby soubojových hodností.
 *
 * Dvanáct stupňů, dvanáct **úplně jiných** erbů — ne jedna kresba
 * přebarvená dvanáctkrát. Hodnost v soubojích roste pomalu (poslední stupeň
 * je na dvě stě vyhraných klání), takže každý posun musí být vidět na první
 * pohled a musí být na co se těšit.
 *
 * Odznaky profilu (RankBadge) staví na jednom štítu a mění kov a krokve;
 * tady je to schválně naopak. Souboj je o dvou lidech proti sobě, ne o cestě
 * jednoho hráče, a tomu odpovídá i jazyk kreseb: zbraně, ostří, hvězdy,
 * plameny. Každý stupeň má vlastní tvar podkladu, vlastní dvojici barev
 * a vlastní znak uvnitř.
 *
 * Kreslí se v soustavě 0–64 a škáluje se `size`. Barvy jsou natvrdo, ne
 * z proměnných motivu: erb má vypadat stejně ve světlém i tmavém, jako
 * skutečný odznak, který si člověk přišpendlí na batoh.
 */

interface Props {
  /** Pořadí hodnosti 1–12. */
  rank: number
  size?: number
  /** Šedivý erb pro hodnost, na kterou hráč ještě nedosáhl. */
  locked?: boolean
  title?: string
}

interface Erb {
  /** Podklad — cesta v soustavě 0–64. */
  tvar: string
  /** Světlá a tmavá barva podkladu; přechod mezi nimi dělá kov. */
  a: string
  b: string
  /** Barva kresby uvnitř. */
  znak: string
  /** Kresba uvnitř erbu. */
  uvnitr: (znak: string) => React.ReactNode
}

/* Tvary podkladu. Každý stupeň má jiný, aby se erby daly rozeznat
   i podle obrysu — třeba v malém čipu u přezdívky soupeře. */
const KRUH = 'M32 4a28 28 0 1 1 0 56 28 28 0 0 1 0-56z'
const STIT = 'M32 3l24 8v22c0 14-10 24-24 31C18 57 8 47 8 33V11z'
const KOSOCTVEREC = 'M32 2l30 30-30 30L2 32z'
const PETIUHELNIK = 'M32 3l29 21-11 34H14L3 24z'
const SESTIUHELNIK = 'M32 2l26 15v30L32 62 6 47V17z'
const VLNA = 'M32 3c16 0 27 7 27 18 0 8-4 12-4 18s5 9 5 15c0 5-11 9-28 9S4 59 4 54c0-6 5-9 5-15s-4-10-4-18C5 10 16 3 32 3z'
const HVEZDA =
  'M32 2l8 19 21 2-16 14 5 21-18-11-18 11 5-21L3 23l21-2z'
const KRIZ = 'M23 3h18v20h20v18H41v20H23V41H3V23h20z'
const KAPKA = 'M32 2c14 14 22 24 22 34a22 22 0 1 1-44 0C10 26 18 16 32 2z'
const VEJIR = 'M32 4c17 0 30 12 30 28 0 12-9 21-14 24-4 3-9 6-16 6s-12-3-16-6C11 53 2 44 2 32 2 16 15 4 32 4z'
const KORUNA = 'M6 22l10 10 8-20 8 20 8-20 8 20 10-10-4 36H10z'
const SLUNCE =
  'M32 1l6 8 9-5 2 10 10 2-5 9 8 6-8 6 5 9-10 2-2 10-9-5-6 8-6-8-9 5-2-10-10-2 5-9-8-6 8-6-5-9 10-2 2-10 9 5z'

const c = (d: string, barva: string, sirka = 0) => (
  <path d={d} fill={sirka ? 'none' : barva} stroke={sirka ? barva : 'none'} strokeWidth={sirka}
    strokeLinecap="round" strokeLinejoin="round" />
)

/*
 * Dvanáct erbů.
 *
 * Pořadí barev jde od chladných a kovových přes teplé až k zářivým: první
 * stupně jsou cín a měď, prostředek ocel a bronz, vrchol zlato a plamen.
 * Uvnitř se motiv posouvá od jednoduchého (kolík, ostří) ke složitému
 * (zkřížené meče, koruna, slunce) — čím výš, tím víc je na erbu co číst.
 */
const ERBY: Erb[] = [
  {
    // 1 — Vyzyvatel: praporek zaražený do země. Kdo přijde, vyzývá.
    tvar: KRUH, a: '#b9c4d6', b: '#7c8aa3', znak: '#31394a',
    uvnitr: (z) => (
      <>
        {c('M24 14v36', z, 5)}
        {c('M27 16h17l-5 7 5 7H27z', z)}
        {c('M18 50h14', z, 5)}
      </>
    ),
  },
  {
    // 2 — Sok: dvě ostří proti sobě.
    tvar: STIT, a: '#cbb79a', b: '#96795a', znak: '#3a2c1c',
    uvnitr: (z) => (
      <>
        {c('M22 18v18l-4 6 4 6', z, 4)}
        {c('M42 18v18l4 6-4 6', z, 4)}
      </>
    ),
  },
  {
    // 3 — Šermíř slov: zkřížené kordy.
    tvar: KOSOCTVEREC, a: '#a8d5c2', b: '#4f8f78', znak: '#12352a',
    uvnitr: (z) => (
      <>
        {c('M18 18L46 46', z, 4)}
        {c('M46 18L18 46', z, 4)}
        {c('M32 30a4 4 0 1 1 0 8 4 4 0 0 1 0-8z', z)}
      </>
    ),
  },
  {
    // 4 — Ostrý soupeř: hrot mířící vzhůru.
    tvar: PETIUHELNIK, a: '#a9c6ec', b: '#4a72ad', znak: '#122745',
    uvnitr: (z) => (
      <>
        {c('M32 14l10 20-10 6-10-6z', z)}
        {c('M32 40v10', z, 4)}
      </>
    ),
  },
  {
    // 5 — Rváč: sevřená pěst i s palcem.
    tvar: SESTIUHELNIK, a: '#e6b7a6', b: '#b05f43', znak: '#3d1a10',
    uvnitr: (z) => (
      <>
        {c('M21 30h21a4 4 0 0 1 4 4v7a9 9 0 0 1-9 9H27a6 6 0 0 1-6-6z', z)}
        {c('M26 30v-6a3 3 0 0 1 6 0v6M34 30v-8a3 3 0 0 1 6 0v8', z, 3)}
        {c('M21 36h-3a3 3 0 0 0 0 6h3', z, 3)}
      </>
    ),
  },
  {
    // 6 — Přeborník: vavřín kolem terče. Podklad je sám hvězda, další
    // hvězda uvnitř by se v ní ztratila.
    tvar: HVEZDA, a: '#e3d3a2', b: '#a98b3f', znak: '#3d2f0c',
    uvnitr: (z) => (
      <>
        {c('M32 24a8 8 0 1 1 0 16 8 8 0 0 1 0-16z', z, 4)}
        {c('M20 30c0 9 5 14 12 16', z, 3)}
        {c('M44 30c0 9-5 14-12 16', z, 3)}
      </>
    ),
  },
  {
    // 7 — Vítěz klání: pohár.
    tvar: VLNA, a: '#b8e0f0', b: '#3f8fb5', znak: '#0d3346',
    uvnitr: (z) => (
      <>
        {c('M22 16h20v10a10 10 0 0 1-20 0z', z)}
        {c('M22 20h-6a6 6 0 0 0 6 6M42 20h6a6 6 0 0 1-6 6', z, 3)}
        {c('M32 36v8', z, 4)}
        {c('M24 48h16', z, 4)}
      </>
    ),
  },
  {
    // 8 — Postrach soupeřů: blesk přes štít.
    tvar: KRIZ, a: '#cdbde8', b: '#6d54a8', znak: '#241540',
    uvnitr: (z) => c('M36 12L20 36h10l-4 18 18-26H34z', z),
  },
  {
    // 9 — Mistr soubojů: tři hvězdy nad ostřím.
    tvar: KAPKA, a: '#a9e3c6', b: '#2f8f66', znak: '#0b3324',
    uvnitr: (z) => (
      <>
        {c('M20 22l2 5 5 1-4 3 1 5-4-3-4 3 1-5-4-3 5-1z', z)}
        {c('M32 16l2 5 5 1-4 3 1 5-4-3-4 3 1-5-4-3 5-1z', z)}
        {c('M44 22l2 5 5 1-4 3 1 5-4-3-4 3 1-5-4-3 5-1z', z)}
        {c('M22 44h20l-10 10z', z)}
      </>
    ),
  },
  {
    // 10 — Velmistr: zkřížené meče pod korunkou.
    tvar: VEJIR, a: '#f0cf9a', b: '#c0872b', znak: '#3f2708',
    uvnitr: (z) => (
      <>
        {c('M18 46L44 20', z, 4)}
        {c('M46 46L20 20', z, 4)}
        {c('M18 16l5 6 9-8 9 8 5-6-3 12H21z', z)}
      </>
    ),
  },
  {
    // 11 — Legenda klání: plamen, který nezhasl. Tři kameny v koruně
    // vypadaly z dálky jako obličej, a to erb dělat nemá.
    tvar: KORUNA, a: '#f2c8d8', b: '#b8446f', znak: '#3d0f22',
    uvnitr: (z) => (
      <>
        {c('M32 22c7 8 11 13 11 18a11 11 0 0 1-22 0c0-5 4-10 11-18z', z, 4)}
        {c('M32 36c3 4 4 6 4 8a4 4 0 0 1-8 0c0-2 1-4 4-8z', z)}
      </>
    ),
  },
  {
    // 12 — Nepřemožitelný: slunce s okem uprostřed.
    tvar: SLUNCE, a: '#ffe08a', b: '#e0761b', znak: '#4a1f02',
    uvnitr: (z) => (
      <>
        {c('M14 32c6-8 12-12 18-12s12 4 18 12c-6 8-12 12-18 12s-12-4-18-12z', z, 4)}
        {c('M32 26a6 6 0 1 1 0 12 6 6 0 0 1 0-12z', z)}
      </>
    ),
  },
]

const SEDA: Pick<Erb, 'a' | 'b' | 'znak'> = { a: '#d5d7de', b: '#9aa0ad', znak: '#6c7280' }

export function DuelCrest({ rank, size = 48, locked = false, title }: Props) {
  const index = Math.max(1, Math.min(rank, ERBY.length)) - 1
  const erb = ERBY[index]!
  const barvy = locked ? SEDA : erb
  const id = `duel-crest-${index + 1}${locked ? '-off' : ''}`

  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 64 64"
      role={title ? 'img' : 'presentation'}
      aria-label={title}
      aria-hidden={title ? undefined : true}
      className="duel-crest"
    >
      <defs>
        <linearGradient id={id} x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stopColor={barvy.a} />
          <stop offset="100%" stopColor={barvy.b} />
        </linearGradient>
      </defs>
      <path d={erb.tvar} fill={`url(#${id})`} stroke={barvy.b} strokeWidth="2" strokeLinejoin="round" />
      <g opacity={locked ? 0.55 : 1}>{erb.uvnitr(barvy.znak)}</g>
    </svg>
  )
}
