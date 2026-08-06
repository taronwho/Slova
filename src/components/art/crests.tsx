/**
 * Vrcholné odznaky — třináct hodností, které se už neopakují.
 *
 * Spodních pětačtyřicet hodností stojí na soustavě: pět tvarů štítu, deset
 * kovů, krokve pod štítem. Je to úsporné a čitelné, protože těch hodností je
 * hodně a hráč jimi projde poměrně rychle.
 *
 * Od šestačtyřicáté hodnosti výš ta soustava přestává dávat smysl. Na Knížete
 * slova se hraje roky a další stupeň za ním je jednou za život — takový odznak
 * nesmí být „stejný jako minule, jen o krokev navíc". Každý z posledních
 * třinácti proto dostal vlastní tvar štítu, vlastní kov a hlavně vlastní
 * znamení, které se váže k tomu, jak se hodnost jmenuje: král má korunu,
 * strážce klíč, kronikář brk. Poznají se od sebe i v šedi, tedy i ve chvíli,
 * kdy si je hráč prohlíží v žebříčku a ještě žádný z nich nemá.
 *
 * Tvary štítů se počítají, nekreslí ručně: dvanáctiúhelník se stejnými
 * stranami nebo šestnáctilistá růžice jsou přesně ty věci, u kterých se ruční
 * `d` rozjede a tvar se scvrkne do beztvarého fleku.
 */

import type { ReactNode } from 'react'

export interface Metal {
  light: string
  dark: string
  rim: string
  glow: string
}

export interface Crest {
  /** Obrys štítu ve čtverci 100×100. */
  plate: string
  metal: Metal
  /** Znamení uvnitř. Patří do kruhu o poloměru 28 se středem 50,50. */
  emblem: (metal: Metal) => ReactNode
}

/* ---------- geometrie ---------- */

const point = (cx: number, cy: number, r: number, angle: number): string =>
  `${(cx + r * Math.cos(angle)).toFixed(2)} ${(cy + r * Math.sin(angle)).toFixed(2)}`

/** Pravidelný mnohoúhelník, prvním vrcholem nahoru. */
export function polygon(cx: number, cy: number, r: number, sides: number): string {
  const step = (Math.PI * 2) / sides
  let d = ''
  for (let i = 0; i < sides; i++) {
    d += `${i === 0 ? 'M' : 'L'}${point(cx, cy, r, i * step - Math.PI / 2)}`
  }
  return `${d}Z`
}

/** Hvězda: `points` cípů, vnitřní poloměr je `inner` násobek vnějšího. */
export function star(cx: number, cy: number, r: number, points: number, inner: number): string {
  const step = Math.PI / points
  let d = ''
  for (let i = 0; i < points * 2; i++) {
    const radius = i % 2 === 0 ? r : r * inner
    d += `${i === 0 ? 'M' : 'L'}${point(cx, cy, radius, i * step - Math.PI / 2)}`
  }
  return `${d}Z`
}

/** Růžice — kruh z vypouklých obloučků, jako ražená rozeta na medaili. */
export function rosette(cx: number, cy: number, r: number, lobes: number): string {
  const step = (Math.PI * 2) / lobes
  const arc = r * 0.3
  let d = ''
  for (let i = 0; i < lobes; i++) {
    const a0 = i * step - Math.PI / 2
    if (i === 0) d += `M${point(cx, cy, r, a0)}`
    d += `A${arc.toFixed(2)} ${arc.toFixed(2)} 0 0 1 ${point(cx, cy, r, a0 + step)}`
  }
  return `${d}Z`
}

/** Paprsky kolem znamení — čárky od vnitřního po vnější poloměr. */
function rays(count: number, from: number, to: number): string {
  let d = ''
  for (let i = 0; i < count; i++) {
    const a = (i * Math.PI * 2) / count - Math.PI / 2
    d += `M${point(50, 50, from, a)}L${point(50, 50, to, a)}`
  }
  return d
}

/* ---------- kovy ---------- */

const SAPPHIRE: Metal = { light: '#9dc4ff', dark: '#1d3f8f', rim: '#3f6ecb', glow: '#dbe9ff' }
const RUBY: Metal = { light: '#ff9fa8', dark: '#8e1026', rim: '#c62f45', glow: '#ffdadd' }
const EMERALD: Metal = { light: '#8ff0b8', dark: '#0c6b40', rim: '#22996a', glow: '#d6ffe8' }
const OPAL: Metal = { light: '#ffe4fb', dark: '#8e3f92', rim: '#c268c6', glow: '#fff2fd' }
const OBSIDIAN: Metal = { light: '#9b93bd', dark: '#241d3d', rim: '#4a3f74', glow: '#cfc7ee' }
const MALACHITE: Metal = { light: '#7fd6c6', dark: '#0a5b58', rim: '#1f8f85', glow: '#ccfff6' }
const ROSE_GOLD: Metal = { light: '#ffc9b0', dark: '#b45b3a', rim: '#df8a63', glow: '#ffe6da' }
const TURQUOISE: Metal = { light: '#8fe6ff', dark: '#0b6d95', rim: '#28a2c9', glow: '#d6f7ff' }
const INK: Metal = { light: '#a9b6ff', dark: '#1b1f66', rim: '#3d47a8', glow: '#dde2ff' }
const PATINA: Metal = { light: '#bfe8cf', dark: '#3f7a63', rim: '#69a58a', glow: '#e8fff2' }
const PEARL: Metal = { light: '#f2f7ff', dark: '#4f6187', rim: '#8fa2c2', glow: '#ffffff' }
const SOLAR: Metal = { light: '#ffe08a', dark: '#c25b00', rim: '#f09209', glow: '#fff3c9' }
const PRISM: Metal = { light: '#ffffff', dark: '#6f5bd6', rim: '#a892ff', glow: '#ffffff' }

/* ---------- znamení ---------- */

/**
 * Společné nastavení pro kresbu znamení.
 *
 * Znamení se kreslí světlým kovem s tmavým obrysem — bez obrysu splyne
 * s propadlým polem, ve kterém sedí, a je z něj jen skvrna.
 */
const paint = (metal: Metal) => ({
  fill: metal.light,
  stroke: metal.dark,
  strokeWidth: 2.4,
  strokeLinejoin: 'round' as const,
  strokeLinecap: 'round' as const,
})

/** Jen obrys, bez výplně — pro tahy, které mají zůstat čárou. */
const line = (metal: Metal, width = 3.4) => ({
  fill: 'none',
  stroke: metal.light,
  strokeWidth: width,
  strokeLinecap: 'round' as const,
  strokeLinejoin: 'round' as const,
})

export const CRESTS: Crest[] = [
  // 46. Kníže slova — knížecí čapka: obruč a tři perly, o stupeň skromnější
  // než koruna krále hned za ní.
  {
    plate: 'M50 4 87 17v27c0 27-21 42-37 51C35 86 13 71 13 44V17Z',
    metal: SAPPHIRE,
    emblem: (metal) => (
      <g {...paint(metal)}>
        <path d="M33 61h34v8H33z" />
        <path d="M35 59 32 43c5 4 10 4 13 0l5-7 5 7c3 4 8 4 13 0l-3 16z" />
        <circle cx="32" cy="40" r="4" />
        <circle cx="50" cy="31" r="4.5" />
        <circle cx="68" cy="40" r="4" />
      </g>
    ),
  },

  // 47. Král slabik — koruna se špicemi a kamenem na vrcholu.
  {
    plate: 'M50 3 97 50 50 97 3 50Z',
    metal: RUBY,
    emblem: (metal) => (
      <g {...paint(metal)}>
        <path d="M32 62h36v8H32z" />
        <path d="M34 60 30 37l12 9 8-13 8 13 12-9-4 23z" />
        <circle cx="50" cy="28" r="4" />
      </g>
    ),
  },

  // 48. Císař češtiny — císařská koruna: k obruči přibyl oblouk, jablko a kříž.
  {
    plate: polygon(50, 50, 47, 12),
    metal: EMERALD,
    emblem: (metal) => (
      <g {...paint(metal)}>
        <path d="M33 63h34v7H33z" />
        <path d="M35 61 32 45l9 6 9-10 9 10 9-6-3 16z" />
        <path d="M36 48c5-13 23-13 28 0" {...line(metal, 3)} />
        <circle cx="50" cy="33" r="4" />
        <path d="M50 26v5M47.5 28.5h5" {...line(metal, 2.6)} />
      </g>
    ),
  },

  // 49. Génius jazyka — jiskra. Nápad, ne úřad: tvar, který jako jediný
  // v této řadě nemá obruč ani žezlo.
  {
    plate: star(50, 50, 47, 6, 0.62),
    metal: OPAL,
    emblem: (metal) => (
      <g {...paint(metal)}>
        <path d="M50 24c2 13 7 18 20 20-13 2-18 7-20 20-2-13-7-18-20-20 13-2 18-7 20-20Z" />
        <path d="M69 28c1 4 2 5 6 6-4 1-5 2-6 6-1-4-2-5-6-6 4-1 5-2 6-6Z" />
        <path d="M31 62c1 3 2 4 5 5-3 1-4 2-5 5-1-3-2-4-5-5 3-1 4-2 5-5Z" />
      </g>
    ),
  },

  // 50. Vládce slov — říšské jablko s křížem. Vláda, ne korunovace.
  {
    plate: star(50, 50, 47, 16, 0.86),
    metal: OBSIDIAN,
    emblem: (metal) => (
      <g {...paint(metal)}>
        <circle cx="50" cy="56" r="17" />
        <path d="M33 56h34" {...line(metal, 3)} />
        <path d="M50 39c7 5 7 29 0 34" {...line(metal, 3)} />
        <path d="M50 39V26M44 31h12" {...line(metal, 3.4)} />
      </g>
    ),
  },

  // 51. Strážce jazyka — klíč. Strážce něco odemyká a zamyká, ne vládne.
  {
    plate: 'M50 6h30l14 14v30c0 24-18 36-44 44C24 86 6 74 6 50V20L20 6Z',
    metal: MALACHITE,
    emblem: (metal) => (
      <g>
        <circle cx="50" cy="35" r="10" {...line(metal, 5)} />
        <path d="M50 45v29M50 60h10M50 68h8" {...line(metal, 5)} />
      </g>
    ),
  },

  // 52. Kníže slovníku — kniha s knížecí čapkou. Vrací se motiv Knížete slova,
  // ale už nad otevřenou knihou.
  {
    plate: polygon(50, 50, 47, 8),
    metal: ROSE_GOLD,
    emblem: (metal) => (
      <g {...paint(metal)}>
        <path d="M40 39l3-10 7 6 7-6 3 10z" />
        <path d="M27 47c8-4 15-4 23 2 8-6 15-6 23-2v23c-8-4-15-4-23 2-8-6-15-6-23-2z" />
        <path d="M50 49v23" {...line(metal, 2.2)} />
      </g>
    ),
  },

  // 53. Věčný luštitel — přesýpací hodiny. Věčnost je tady čas, ne moc.
  {
    plate: star(50, 50, 47, 12, 0.84),
    metal: TURQUOISE,
    emblem: (metal) => (
      <g {...paint(metal)}>
        <path d="M37 30c0 10 13 16 13 20s-13 10-13 20h26c0-10-13-16-13-20s13-10 13-20z" />
        <path d="M33 27h34M33 73h34" {...line(metal, 4.4)} />
      </g>
    ),
  },

  // 54. Slovní kronikář — brk. Kronikář zapisuje, proto pero a kapka inkoustu.
  {
    plate: polygon(50, 50, 47, 5),
    metal: INK,
    emblem: (metal) => (
      <g {...paint(metal)}>
        <path d="M72 26c-21 2-35 15-39 36 12-1 20-6 25-13 6-8 12-14 14-23Z" />
        <path d="M33 74 47 58" {...line(metal, 4)} />
        <circle cx="30" cy="40" r="4.5" />
      </g>
    ),
  },

  // 55. Patriarcha češtiny — vavřínový věnec. Nejstarší odznak zásluh, jaký
  // kdo vymyslel, a jediné místo v žebříčku, kde se hodí.
  {
    plate: 'M50 5c25 0 40 18 40 45S75 95 50 95 10 77 10 50 25 5 50 5Z',
    metal: PATINA,
    emblem: (metal) => (
      <g {...paint(metal)}>
        {[-1, 1].map((side) => (
          <g key={side}>
            <path
              d={`M50 74c${side * -16} -4 ${side * -22} -14 ${side * -20} -30`}
              {...line(metal, 3)}
            />
            {[0, 1, 2, 3].map((i) => (
              <ellipse
                key={i}
                cx={50 + side * (10 + i * 2.5)}
                cy={68 - i * 11}
                rx="4"
                ry="6.5"
                transform={`rotate(${side * (40 - i * 22)} ${50 + side * (10 + i * 2.5)} ${68 - i * 11})`}
              />
            ))}
          </g>
        ))}
        <circle cx="50" cy="34" r="5" />
      </g>
    ),
  },

  // 56. Živoucí slovník — kniha, ze které jde světlo. Ne majetek, ale zdroj.
  {
    plate: rosette(50, 50, 46, 8),
    metal: PEARL,
    emblem: (metal) => (
      <g {...paint(metal)}>
        <path d="M27 48c8-4 15-4 23 2 8-6 15-6 23-2v24c-8-4-15-4-23 2-8-6-15-6-23-2z" />
        <path d="M50 50v24" {...line(metal, 2.2)} />
        <path d="M50 38V26M36 42 30 32M64 42l6-10" {...line(metal, 3.2)} />
      </g>
    ),
  },

  // 57. Legenda Slov — hvězda s ocasem. O legendě se vypráví, i když už tu není.
  {
    plate: star(50, 50, 47, 12, 0.55),
    metal: SOLAR,
    emblem: (metal) => (
      <g {...paint(metal)}>
        <path d={star(56, 42, 19, 5, 0.42)} />
        <path d="M40 56 27 70M47 62l-9 10M33 54l-8 8" {...line(metal, 3.4)} />
      </g>
    ),
  },

  // 58. Nesmrtelný písař — slunce a v něm nekonečno. Poslední hodnost
  // v žebříčku, deset milionů věhlasu: dál už se jít nedá, a přesně to
  // znamení říká.
  {
    plate: rosette(50, 50, 46, 16),
    metal: PRISM,
    emblem: (metal) => (
      <g>
        <path d={rays(16, 20, 28)} {...line(metal, 2.6)} />
        <circle cx="43" cy="50" r="8.5" {...line(metal, 3.6)} />
        <circle cx="57" cy="50" r="8.5" {...line(metal, 3.6)} />
      </g>
    ),
  },
]

/** Od které hodnosti se kreslí vrcholné odznaky. */
export const CREST_FROM = 46
