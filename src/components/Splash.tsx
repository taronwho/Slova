/**
 * Úvodní obrazovka se značkou.
 *
 * Kroužek ze tří oblouků je totéž znamení jako ikona aplikace a jako
 * prostřední „O" ve slově SLOVA — tři barvy, tři hry. Oblouky se nakreslí,
 * název se poskládá po písmenech, značka chvíli zůstane stát a pak se
 * rozplyne do menu.
 *
 * Hra pod tím se mezitím normálně načítá, takže úvod nikoho nezdržuje.
 */

import { useEffect, useState } from 'react'

/** Obvod kružnice o poloměru 38 a délka jednoho ze tří oblouků (112°). */
const CIRCUMFERENCE = 2 * Math.PI * 38
const ARC = (CIRCUMFERENCE * 112) / 360

const ARCS = [
  { color: 'var(--mode-chain)', angle: -86 },
  { color: 'var(--mode-hive)', angle: 34 },
  { color: 'var(--mode-tower)', angle: 154 },
]

interface Props {
  onDone: () => void
}

export function Splash({ onDone }: Props) {
  const [leaving, setLeaving] = useState(false)

  useEffect(() => {
    const calm = window.matchMedia?.('(prefers-reduced-motion: reduce)').matches ?? false
    const hold = calm ? 1200 : 2000
    const fade = calm ? 250 : 400
    const out = window.setTimeout(() => setLeaving(true), hold)
    const gone = window.setTimeout(onDone, hold + fade)
    return () => {
      window.clearTimeout(out)
      window.clearTimeout(gone)
    }
  }, [onDone])

  return (
    <div className={`splash ${leaving ? 'leaving' : ''}`} role="presentation">
      <div className="splash-inner">
        <svg className="splash-mark" viewBox="0 0 100 100" aria-hidden="true">
          {ARCS.map((arc, i) => (
            <circle
              key={arc.angle}
              cx="50"
              cy="50"
              r="38"
              fill="none"
              stroke={arc.color}
              strokeWidth="15"
              strokeDasharray={`${ARC} ${CIRCUMFERENCE - ARC}`}
              transform={`rotate(${arc.angle} 50 50)`}
              style={{
                strokeDashoffset: ARC,
                animationDelay: `${i * 90}ms`,
              }}
            />
          ))}
          <circle className="splash-core" cx="50" cy="50" r="13" fill="#fff" />
        </svg>

        <div className="splash-word" aria-label="Slova">
          {[...'SLOVA'].map((letter, i) => (
            <span key={i} style={{ animationDelay: `${300 + i * 55}ms` }}>
              {letter}
            </span>
          ))}
        </div>
      </div>
    </div>
  )
}
