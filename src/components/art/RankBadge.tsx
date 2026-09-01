/**
 * Odznak hodnosti — vlastní kresba, ne písmenko z fontu.
 *
 * Odznak má hráče potěšit, ne ho jen zařadit. Proto se s každou hodností
 * viditelně mění, a ne až s každou pátou:
 *
 *   1. **Tvar štítu a kov** se mění po pěti hodnostech, spolu. Devět pětic,
 *      devět siluet — kolo, buňka plástve, štít, osmiúhelník, zaoblený
 *      čtverec, hvězda, ozubené kolo, ovál, růžice — a k nim devět kovů od
 *      bronzu k plazmě. Pětice se tak od sebe pozná na první pohled, i když
 *      hráč kouká na dva odznaky vedle sebe v šedi.
 *   2. **Ozdoby uvnitř pětice** přibývají po jedné a nikdy neubývají, takže
 *      každý vyšší odznak je bohatší než ten pod ním:
 *        0. holý štít,
 *        1. + ražené perličky po obvodu,
 *        2. + vnitřní obruč,
 *        3. + podložka, druhý plát vykukující zpod štítu,
 *        4. + broušený kámen ve středu znamení a vavřínová snítka pod štítem.
 *      Ve vyšších pěticích jsou i ozdoby bohatší: perličky se mění v kosočtverce
 *      a obruč se zdvojí. Pátý odznak deváté pětice je tedy o dvě třídy jinde
 *      než první odznak té první — a přesně tak se to má číst.
 *   3. **Znamení uvnitř** je vždycky prstenec ze tří oblouků — totéž „O"
 *      jako ve značce a v úvodní animaci. Tři barvy, tři oblouky. To jediné
 *      zůstává napříč celým žebříčkem stejné, aby odznaky drželi pohromadě.
 *
 * Od šestačtyřicáté hodnosti výš soustava končí a nastupují **vrcholné
 * odznaky** z `crests.tsx`: každý má vlastní tvar, vlastní kov a vlastní
 * znamení podle svého jména. Na těch stupních se hraje roky a odznak
 * odlišený jen ozdobou by za tu cestu byl málo.
 *
 * Barvy kovů jsou napevno, ne z tokenů: odznak má vypadat jako ražený kus,
 * ne jako plocha uživatelského rozhraní, a musí být týž ve světlém i tmavém
 * tématu. Prstenec uvnitř naopak barvy režimů dědí, takže se ladí se zbytkem.
 */

import { CREST_FROM, CRESTS, polygon, rosette, star, type Metal } from './crests'

interface Props {
  /** Pořadí hodnosti 1–58. */
  rank: number
  /** Hrana v pixelech. */
  size?: number
  /** Nezískaná hodnost se kreslí v šedi. */
  locked?: boolean
  /**
   * Jen štít, bez toho, co visí pod ním.
   *
   * V liště je odznak vysoký dvaadvacet pixelů — vavřín v něm není vidět,
   * ale zabírá čtvrtinu výšky, takže štít vyjde nad optický střed a odznak
   * v čipu „plave". Bez něj sedí přesně a je o čtvrtinu větší. Pětice se
   * i tak pozná: perličky, obruč, podložka i kámen jsou na štítu samotném.
   */
  compact?: boolean
}

/** Devět kovů, po pěti hodnostech jeden. Pořadí je vzestup od bronzu k plazmě. */
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
]

const LOCKED: Metal = {
  light: '#b9b6c9',
  dark: '#6f6b84',
  rim: '#8d89a0',
  glow: '#d7d5e0',
}

/**
 * Devět obrysů štítu, jeden na každou pětici.
 *
 * Všechny se vejdou do pole 100×100 a žádný z nich se nikde nepřibližuje
 * středu blíž než na 37 — pod tou hranicí leží perličky i obruč, takže
 * ozdoby nikde nevykouknou ven ze štítu.
 */
const PLATES = [
  // kolo
  'M50 7a43 43 0 1 1 0 86 43 43 0 0 1 0-86Z',
  // šestiúhelník na výšku — buňka plástve
  polygon(50, 50, 45, 6),
  // štít
  'M50 7 87 20v35c0 21-16 31-37 37-21-6-37-16-37-37V20Z',
  // osmiúhelník
  polygon(50, 50, 45, 8),
  // zaoblený čtverec
  'M20 10h60a11 11 0 0 1 11 11v58a11 11 0 0 1-11 11H20A11 11 0 0 1 9 79V21A11 11 0 0 1 20 10Z',
  // osmicípá hvězda
  star(50, 50, 45, 8, 0.8),
  // ozubené kolo
  star(50, 50, 45, 12, 0.86),
  // ovál
  'M50 6c21 0 37 20 37 44s-16 44-37 44S13 74 13 50 29 6 50 6Z',
  // dvanáctilistá růžice
  rosette(50, 50, 44, 12),
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

/** Kolem kterého poloměru leží perličky a kde vnitřní obruč. */
const BEAD_R = 34.5
const HOOP_R = 30.5

/**
 * Ražené perličky po obvodu — první ozdoba uvnitř pětice.
 *
 * Ve vyšších pěticích jich je víc a mají broušený tvar místo kulatého;
 * je to drobnost, ale právě z drobností se pozná, že je odznak bohatší.
 */
function Beads({ tier, metal }: { tier: number; metal: Metal }) {
  const count = 8 + tier * 2
  const cut = tier >= 5
  return (
    <g fill={metal.light} stroke={metal.dark} strokeWidth="0.9" strokeLinejoin="round">
      {Array.from({ length: count }, (_, i) => {
        const angle = (i * Math.PI * 2) / count - Math.PI / 2
        const x = 50 + BEAD_R * Math.cos(angle)
        const y = 50 + BEAD_R * Math.sin(angle)
        if (!cut) return <circle key={i} cx={x.toFixed(2)} cy={y.toFixed(2)} r="2.3" />
        const s = 3
        return (
          <path
            key={i}
            d={`M${x.toFixed(2)} ${(y - s).toFixed(2)}L${(x + s).toFixed(2)} ${y.toFixed(2)}L${x.toFixed(2)} ${(y + s).toFixed(2)}L${(x - s).toFixed(2)} ${y.toFixed(2)}Z`}
          />
        )
      })}
    </g>
  )
}

export function RankBadge({ rank, size = 56, locked = false, compact = false }: Props) {
  const index = Math.max(1, Math.min(rank, CREST_FROM - 1 + CRESTS.length)) - 1
  // Vrcholné hodnosti mají každá svůj vlastní odznak; nižší se skládají
  // z kovu a tvaru štítu (obojí po pěti hodnostech) a z ozdob, kterých
  // uvnitř pětice s každým stupněm přibývá.
  const crest = index + 1 >= CREST_FROM ? CRESTS[index + 1 - CREST_FROM]! : null
  const tier = Math.floor(index / 5)
  const step = crest ? 0 : index % 5
  const metal: Metal = locked ? LOCKED : (crest?.metal ?? METALS[tier]!)
  const plate = crest ? crest.plate : PLATES[tier]!
  const id = `rank-${rank}${locked ? '-off' : ''}`

  const laurel = crest !== null || step >= 4

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

      {/* Podložka — druhý, tmavý plát, který kouká zpod štítu. Kreslí se
          první, protože leží vzadu; tvar má týž, jen o kousek větší. */}
      {step >= 3 && (
        <path
          d={plate}
          transform="translate(50 50) scale(1.09) translate(-50 -50)"
          fill={metal.dark}
        />
      )}

      <path d={plate} fill={`url(#${id}-plate)`} stroke={metal.dark} strokeWidth="2.5" />
      <path d={plate} fill={`url(#${id}-shine)`} />

      {/* Vnitřní obruč. Ve vyšších pěticích dvojitá. */}
      {step >= 2 && (
        <>
          <circle
            cx="50"
            cy="50"
            r={HOOP_R}
            fill="none"
            stroke={metal.dark}
            strokeWidth="1.8"
            opacity="0.65"
          />
          {tier >= 4 && (
            <circle
              cx="50"
              cy="50"
              r={HOOP_R + 2.6}
              fill="none"
              stroke={metal.dark}
              strokeWidth="1"
              opacity="0.5"
            />
          )}
        </>
      )}

      {step >= 1 && <Beads tier={tier} metal={metal} />}

      {/* Zapuštěné pole, ve kterém sedí znamení. */}
      <circle cx="50" cy="50" r={crest ? 30 : 27} fill={metal.dark} opacity="0.28" />
      <circle
        cx="50"
        cy="50"
        r={crest ? 30 : 27}
        fill="none"
        stroke={metal.dark}
        strokeWidth="2"
      />

      <g opacity={locked ? 0.55 : 1}>
        {crest ? (
          crest.emblem(metal)
        ) : (
          <>
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
            {/* Střed znamení. U poslední hodnosti v pětici je z něj broušený
                kámen — jediná ozdoba, která je vidět i v liště. */}
            {step >= 4 ? (
              <g fill={metal.light} stroke={metal.dark} strokeWidth="1.4" strokeLinejoin="round">
                <path d="M50 41 59 50 50 59 41 50Z" />
                <path d="M50 41 54.5 50 50 59 45.5 50Z" opacity="0.55" />
              </g>
            ) : (
              <circle cx="50" cy="50" r="7" fill={metal.light} />
            )}
          </>
        )}
      </g>

      {/* Vavřínová snítka pod štítem. Nese ji poslední hodnost každé pětice
          a všechny vrcholné odznaky — je to znamení „došel jsi až sem". */}
      {laurel && !compact && (
        <g fill="none" stroke={metal.rim} strokeWidth="3.5" strokeLinecap="round">
          <path d="M50 112c-9 0-15-4-18-11 8-2 14 1 18 6" />
          <path d="M50 112c9 0 15-4 18-11-8-2-14 1-18 6" />
          <path d="M50 101v13" />
        </g>
      )}
    </svg>
  )
}
