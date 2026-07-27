/**
 * Kresby ocenění.
 *
 * Jedna soustava, ne třicet nesouvisejících obrázků. Všechny jsou v poli
 * 48×48, kreslené linkou tloušťky 2,6 se zakulacenými konci, a každá má
 * **právě jednu** plnou plochu v barvě své skupiny — oko tak na mřížce ocenění
 * hned vidí, kam co patří, aniž by četlo nadpisy.
 *
 * Tvarosloví je půjčené ze hry samotné: článek řetězu, šestiúhelník plástve,
 * patra věže, které se směrem nahoru rozšiřují (protože každé patro má o
 * písmeno víc). Emoji ani ikony odjinud tu nejsou — všechno je kreslené pro
 * Slova.
 *
 * Odstupňovaná ocenění (tři pangramy, sedm denních výzev) sdílejí kresbu a
 * liší se krokvemi pod ní — stejná řeč jako u odznaků hodností.
 */

interface Props {
  /** Klíč kresby, viz Award.art. */
  art: string
  /** Stupeň v rodině 1–5; kolik krokví se ukáže pod kresbou. */
  tier?: number | undefined
  size?: number | undefined
}

/** Šestiúhelník plástve, špičkou nahoru, kolem zadaného středu. */
function hex(cx: number, cy: number, r: number): string {
  const w = r * 0.866
  return `M${cx} ${cy - r} ${cx + w} ${cy - r / 2}v${r}L${cx} ${cy + r} ${cx - w} ${cy + r / 2}v-${r}Z`
}

/** Sedm buněk plástve — střed a šest kolem. */
const COMB: [number, number][] = [
  [24, 24],
  [24, 10.5],
  [35.7, 17.25],
  [35.7, 30.75],
  [24, 37.5],
  [12.3, 30.75],
  [12.3, 17.25],
]

function Glyph({ art }: { art: string }) {
  switch (art) {
    // --- První kroky ----------------------------------------------------
    // Články jsou šikmé a posunuté po diagonále — dva souosé ovály vedle sebe
    // splynou v jednu tobolku a řetěz z nich není poznat.
    case 'link':
      return (
        <>
          <rect
            x="3"
            y="12"
            width="24"
            height="15"
            rx="7.5"
            className="ln"
            transform="rotate(-22 15 19.5)"
          />
          <rect
            x="21"
            y="21"
            width="24"
            height="15"
            rx="7.5"
            className="tn"
            transform="rotate(-22 33 28.5)"
          />
        </>
      )
    case 'cell':
      return (
        <>
          <path d={hex(24, 24, 16)} className="ln" />
          <circle cx="24" cy="24" r="5" className="tf" />
        </>
      )
    // Patra se směrem nahoru rozšiřují, protože každé má o písmeno víc.
    // Jeden obrys se dvěma přepážkami drží tvar věže i v malém — tři
    // samostatné obdélníky se při téhle velikosti slily do lampičky.
    case 'blocks':
      return (
        <>
          <path d="M6 9h36l-6 33H12Z" className="ln" />
          <path d="M9.7 20h28.6M11.8 31h24.4" className="ln" />
          <path d="M6 9h36l-1.8 10H7.8Z" className="tf" />
        </>
      )
    case 'triad':
      return (
        <>
          <circle cx="17" cy="19" r="10" fill="var(--mode-chain)" opacity="0.85" stroke="none" />
          <circle cx="31" cy="19" r="10" fill="var(--mode-hive)" opacity="0.85" stroke="none" />
          <circle cx="24" cy="31" r="10" fill="var(--mode-tower)" opacity="0.85" stroke="none" />
        </>
      )

    // --- Řetěz ----------------------------------------------------------
    case 'arrow':
      return (
        <>
          <circle cx="7" cy="24" r="4" className="ln" />
          <path d="M13 24h24" className="ln" />
          <path d="M31 17.5 38.5 24 31 30.5" className="ln" />
          <circle cx="41" cy="24" r="4" className="tf" />
        </>
      )
    case 'chain3':
      return (
        <>
          <rect
            x="0"
            y="13"
            width="21"
            height="13"
            rx="6.5"
            className="ln"
            transform="rotate(-22 10.5 19.5)"
          />
          <rect
            x="13.5"
            y="17.5"
            width="21"
            height="13"
            rx="6.5"
            className="ln"
            transform="rotate(-22 24 24)"
          />
          <rect
            x="27"
            y="22"
            width="21"
            height="13"
            rx="6.5"
            className="tn"
            transform="rotate(-22 37.5 28.5)"
          />
        </>
      )
    case 'bolt':
      return (
        <>
          <path d="M27 4 12 26h9l-3 18 18-24h-9l5-16Z" className="tf" />
        </>
      )

    // --- Šibenice -------------------------------------------------------
    // Rameno šibenice s oprátkou. Kresba je stejná jako ve hře, jen zmenšená,
    // takže je meta poznat dřív, než se přečte nadpis.
    case 'noose':
      return (
        <>
          <path d="M8 44h16M12 44V8h20" className="ln" />
          <path d="M12 15 19 8" className="ln" />
          <path d="M32 8v9" className="ln" />
          <path d="M32 17a7 7 0 1 1 0 14 7 7 0 0 1 0-14Z" className="tn" />
        </>
      )

    // --- Detektiv -------------------------------------------------------
    // Lupa nad řádkem textu — ten text je v téhle hře to hlavní.
    case 'glass':
      return (
        <>
          <path d="M6 34h12M6 40h20" className="ln" />
          <circle cx="27" cy="18" r="12" className="tn" />
          <path d="M36 27 43 34" className="ln" />
          <path d="M27 11a7 7 0 0 0-7 7" className="ln" />
        </>
      )

    // --- Voština --------------------------------------------------------
    case 'star-cell':
      return (
        <>
          <path d={hex(24, 24, 17)} className="ln" />
          <path
            d="M24 13.5 27 21l7.5.5-5.8 4.9 1.9 7.3L24 29.6l-6.6 4.1 1.9-7.3-5.8-4.9L21 21Z"
            className="tf"
          />
        </>
      )
    case 'comb':
      return (
        <>
          {COMB.map(([cx, cy], i) => (
            <path key={i} d={hex(cx, cy, 7.5)} className={i === 0 ? 'tf' : 'tn'} />
          ))}
        </>
      )
    case 'crown':
      return (
        <>
          <path d="M8 30 5 13l9 6 10-12 10 12 9-6-3 17Z" className="tf" />
          <path d="M9 36h30" className="ln" />
        </>
      )
    case 'list':
      return (
        <>
          <path d={hex(9, 14, 4.5)} className="tf" />
          <path d={hex(9, 24, 4.5)} className="tf" />
          <path d={hex(9, 34, 4.5)} className="tf" />
          <path d="M19 14h24M19 24h24M19 34h16" className="ln" />
        </>
      )

    // --- Věž ------------------------------------------------------------
    case 'flag':
      return (
        <>
          <path d="M8 42 24 23l16 19" className="ln" />
          <path d="M24 42V7" className="ln" />
          <path d="M24 8h14l-4 5.5 4 5.5H24Z" className="tf" />
        </>
      )
    // Osm dlaždic v řadě, poslední obarvená — čte se to jako patro o osmi
    // písmenech, kdežto plotna s přepážkami vypadala jako radiátor.
    case 'wide':
      return (
        <>
          {Array.from({ length: 8 }, (_, i) => (
            <rect
              key={i}
              x={1.9 + i * 5.8}
              y="18"
              width="4.6"
              height="12"
              rx="1.5"
              className={i === 7 ? 'tf' : 'tn'}
            />
          ))}
        </>
      )
    case 'nohint':
      return (
        <>
          <path d="M24 6a12 12 0 0 1 7 21.7V33H17v-5.3A12 12 0 0 1 24 6Z" className="ln" />
          <path d="M19 38h10" className="ln" />
          <path d="M7 7l34 34" className="tn" />
        </>
      )
    // --- Vytrvalost -----------------------------------------------------
    case 'flame':
      return (
        <>
          <path
            d="M24 4c7 8 13 12 13 21a13 13 0 0 1-26 0c0-5 3-8 5-11 1 3 3 5 5 5 2-4-1-9 3-15Z"
            className="tf"
          />
          <path d="M24 39a6 6 0 0 1-4-10c1 3 3 4 5 3 1 3 3 3 3 5a4 4 0 0 1-4 2Z" fill="var(--surface)" stroke="none" />
        </>
      )
    case 'day':
      return (
        <>
          <rect x="6" y="10" width="36" height="32" rx="5" className="ln" />
          <path d="M6 20h36" className="ln" />
          <path d="M15 6v8M33 6v8" className="ln" />
          <path d="M17 31.5 22 36.5 32 26" className="tn" />
        </>
      )

    // --- Mistrovství ----------------------------------------------------
    case 'gem':
      return (
        <>
          <path d="M14 8h20l10 12-20 22L4 20Z" className="tf" />
          <path d="M4 20h40M14 8l-4 12 14 22 14-22-4-12" className="ln" />
        </>
      )
    case 'peak':
      return (
        <>
          <rect x="5" y="30" width="9" height="13" rx="2" className="ln" />
          <rect x="19" y="22" width="9" height="21" rx="2" className="ln" />
          <rect x="33" y="12" width="9" height="31" rx="2" className="tn" />
          <path d="M37.5 3l1.9 4 4.4.6-3.2 3 .8 4.3-3.9-2.1-3.9 2.1.8-4.3-3.2-3 4.4-.6Z" className="tf" />
        </>
      )
    case 'deck':
      return (
        <>
          <rect x="6" y="14" width="26" height="30" rx="4" className="ln" transform="rotate(-9 19 29)" />
          <rect x="13" y="10" width="26" height="30" rx="4" className="tn" />
          <path d="M20 20h12M20 27h12M20 34h7" className="ln" />
        </>
      )
    case 'medal':
      return (
        <>
          <path d="M16 4 24 20 32 4" className="ln" />
          <circle cx="24" cy="31" r="13" className="tn" />
          <path d="M24 23.5l2.6 5.4 5.9.8-4.3 4.1 1 5.9-5.2-2.8-5.2 2.8 1-5.9-4.3-4.1 5.9-.8Z" className="tf" />
        </>
      )
    default:
      return <circle cx="24" cy="24" r="15" className="ln" />
  }
}

export function AwardArt({ art, tier, size = 44 }: Props) {
  const rows = tier ?? 0
  // Krokve se kreslí od y=50 po čtyřech, špička o čtyři níž. Plátno proto
  // musí růst s jejich počtem — u tří vyjde přesně 64 jako dřív, u pěti 76.
  const height = rows > 0 ? 46 + rows * 6 : 48

  return (
    <svg
      className="award-art"
      width={size}
      height={Math.round((size * height) / 48)}
      viewBox={`0 0 48 ${height}`}
      role="img"
      aria-hidden="true"
    >
      <Glyph art={art} />
      {/* Krokve = kolikátý stupeň v rodině. Stejné znamení jako u hodností. */}
      {Array.from({ length: rows }, (_, i) => (
        <path key={i} d={`M18 ${50 + i * 4} 24 ${54 + i * 4} 30 ${50 + i * 4}`} className="pip" />
      ))}
    </svg>
  )
}
