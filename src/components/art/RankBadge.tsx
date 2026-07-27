/**
 * Odznak hodnosti — vlastní kresba, ne písmenko z fontu.
 *
 * Odznak se skládá ze tří vrstev, které dohromady řeknou hodnost na první
 * pohled, i když si hráč nepřečte jméno:
 *
 *   1. **Tvar štítu** — kolo, šestiúhelník, štít, hvězda, vavřín. Mění se po
 *      deseti hodnostech. Šestiúhelník je zároveň buňka Voštiny, takže i tady
 *      zůstává hra ve svém tvarosloví.
 *   2. **Kov** se mění po pěti hodnostech, takže každý tvar má dvě podoby:
 *      chudší a bohatší. Padesát hodností tak vystačí s pěti tvary a deseti
 *      kovy, místo aby se rozpadlo do padesáti nesouvisejících obrázků.
 *   3. **Znamení uvnitř** je vždycky prstenec ze tří oblouků — totéž „O"
 *      jako ve značce a v úvodní animaci. Tři barvy, tři hry.
 *   4. **Krokve pod štítem** říkají, kolikátá hodnost uvnitř pětice to je.
 *
 * Barvy kovů jsou napevno, ne z tokenů: odznak má vypadat jako ražený kus,
 * ne jako plocha uživatelského rozhraní, a musí být týž ve světlém i tmavém
 * tématu. Prstenec uvnitř naopak barvy režimů dědí, takže se ladí se zbytkem.
 */

interface Props {
  /** Pořadí hodnosti 1–50. */
  rank: number
  /** Hrana v pixelech. */
  size?: number
  /** Nezískaná hodnost se kreslí v šedi. */
  locked?: boolean
  /**
   * Jen štít, bez krokví pod ním.
   *
   * V liště je odznak vysoký dvaadvacet pixelů — krokve v něm nejsou vidět,
   * ale zabírají čtvrtinu výšky, takže štít vyjde nad optický střed a odznak
   * v čipu „plave". Bez nich sedí přesně a je o čtvrtinu větší.
   */
  compact?: boolean
}

interface Metal {
  light: string
  dark: string
  rim: string
  glow: string
}

/** Deset kovů, po pěti hodnostech jeden. Pořadí je vzestup od bronzu k démantu. */
const METALS: Metal[] = [
  { light: '#e3a86a', dark: '#9a5a22', rim: '#c07c38', glow: '#ffd9ab' }, // bronz
  { light: '#f0b98c', dark: '#a8471b', rim: '#d1743a', glow: '#ffe2c4' }, // měď
  { light: '#e9edf5', dark: '#8d97ad', rim: '#aab4c8', glow: '#ffffff' }, // stříbro
  { light: '#d8e4f0', dark: '#6b7f96', rim: '#94a8be', glow: '#f4faff' }, // ocel
  { light: '#ffd86b', dark: '#c08a06', rim: '#e0a91d', glow: '#fff1bd' }, // zlato
  { light: '#ffc94a', dark: '#b06a00', rim: '#e08f0c', glow: '#ffe9a8' }, // jantar
  { light: '#e6f0f4', dark: '#7d95a0', rim: '#a6bcc6', glow: '#ffffff' }, // platina
  { light: '#b9a6ff', dark: '#5b3df5', rim: '#7c60ff', glow: '#e4dbff' }, // ametyst
  { light: '#8ff0e6', dark: '#0d7f86', rim: '#2aa9ae', glow: '#d6fffa' }, // plazma
  { light: '#ffffff', dark: '#7f93c9', rim: '#b3c4ea', glow: '#ffffff' }, // démant
]

const LOCKED: Metal = {
  light: '#b9b6c9',
  dark: '#6f6b84',
  rim: '#8d89a0',
  glow: '#d7d5e0',
}

/**
 * Rozeta — kruh z vypouklých oblouků, jako ražená růžice na medaili.
 *
 * Počítá se, ne píše ručně: dvanáct obloučků se stejným poloměrem je přesně
 * ta věc, u které se ruční `d` rozjede a tvar se scvrkne do beztvarého fleku.
 */
function rosette(cx: number, cy: number, r: number, lobes: number): string {
  const step = (Math.PI * 2) / lobes
  const arc = r * 0.3
  let d = ''
  for (let i = 0; i < lobes; i++) {
    const a0 = i * step - Math.PI / 2
    const a1 = a0 + step
    const x1 = (cx + r * Math.cos(a1)).toFixed(2)
    const y1 = (cy + r * Math.sin(a1)).toFixed(2)
    if (i === 0) d += `M${(cx + r * Math.cos(a0)).toFixed(2)} ${(cy + r * Math.sin(a0)).toFixed(2)}`
    d += `A${arc.toFixed(2)} ${arc.toFixed(2)} 0 0 1 ${x1} ${y1}`
  }
  return `${d}Z`
}

/** Pět obrysů štítu, každý pro dva sousední kovy. Vejdou se do pole 100×100. */
const PLATES = [
  // kolo
  'M50 6a44 44 0 1 1 0 88 44 44 0 0 1 0-88Z',
  // šestiúhelník na výšku
  'M50 5 88 27v46L50 95 12 73V27Z',
  // štít
  'M50 5 89 19v37c0 22-17 33-39 39-22-6-39-17-39-39V19Z',
  // osmicípá hvězda
  'M50 4 62 18l18-4 3 18 17 8-11 15 11 15-17 8-3 18-18-4-12 14-12-14-18 4-3-18-17-8 11-15L1 42l17-8 3-18 18 4Z',
  // rozeta — dvanáctilistá růžice
  rosette(50, 50, 45, 12),
]

/** Obvod kružnice r=21 a délka jednoho ze tří oblouků (108°). */
const R = 21
const CIRCUMFERENCE = 2 * Math.PI * R
const ARC = (CIRCUMFERENCE * 108) / 360

const ARCS = [
  { color: 'var(--mode-chain)', angle: -90 },
  { color: 'var(--mode-hive)', angle: 30 },
  { color: 'var(--mode-tower)', angle: 150 },
]

export function RankBadge({ rank, size = 56, locked = false, compact = false }: Props) {
  const index = Math.max(1, Math.min(rank, 50)) - 1
  // Kov se mění po pěti hodnostech, tvar štítu po deseti.
  const tier = Math.floor(index / 5)
  const shape = Math.floor(tier / 2)
  const step = index % 5
  const metal = locked ? LOCKED : METALS[tier]!
  const id = `rank-${rank}${locked ? '-off' : ''}`

  return (
    <svg
      className={`rank-badge ${locked ? 'locked' : ''}`}
      width={size}
      height={compact ? size : Math.round(size * 1.24)}
      viewBox={compact ? '0 0 100 100' : '0 0 100 124'}
      role="img"
      aria-label={`Odznak hodnosti ${rank}`}
    >
      <defs>
        <linearGradient id={`${id}-plate`} x1="0" y1="0" x2="0" y2="1">
          <stop offset="0" stopColor={metal.light} />
          <stop offset="0.52" stopColor={metal.rim} />
          <stop offset="1" stopColor={metal.dark} />
        </linearGradient>
        {/* Odlesk na horní půlce — bez něj vypadá štít jako plochá nálepka. */}
        <linearGradient id={`${id}-shine`} x1="0" y1="0" x2="0.4" y2="1">
          <stop offset="0" stopColor={metal.glow} stopOpacity="0.85" />
          <stop offset="0.55" stopColor={metal.glow} stopOpacity="0" />
        </linearGradient>
      </defs>

      <path d={PLATES[shape]} fill={`url(#${id}-plate)`} stroke={metal.dark} strokeWidth="2.5" />
      <path d={PLATES[shape]} fill={`url(#${id}-shine)`} />

      {/* Zapuštěné pole, ve kterém sedí znamení. */}
      <circle cx="50" cy="50" r="27" fill={metal.dark} opacity="0.28" />
      <circle cx="50" cy="50" r="27" fill="none" stroke={metal.dark} strokeWidth="2" />

      <g opacity={locked ? 0.45 : 1}>
        {ARCS.map((arc) => (
          <circle
            key={arc.angle}
            cx="50"
            cy="50"
            r={R}
            fill="none"
            stroke={locked ? '#4a4760' : arc.color}
            strokeWidth="8"
            strokeLinecap="butt"
            strokeDasharray={`${ARC} ${CIRCUMFERENCE - ARC}`}
            transform={`rotate(${arc.angle} 50 50)`}
          />
        ))}
        <circle cx="50" cy="50" r="7" fill={metal.light} />
      </g>

      {/* Krokve = pořadí uvnitř kovu. Nula u první hodnosti každého kovu.
          Drží se těsně pod štítem, aby patřily k němu a neplavaly zvlášť. */}
      {Array.from({ length: compact ? 0 : step }, (_, i) => (
        <path
          key={i}
          d={`M38 ${98 + i * 5.5} 50 ${103 + i * 5.5} 62 ${98 + i * 5.5}`}
          fill="none"
          stroke={metal.rim}
          strokeWidth="4.5"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
      ))}
    </svg>
  )
}
