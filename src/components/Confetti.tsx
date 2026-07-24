/** Oslavné konfety — čisté CSS, respektují prefers-reduced-motion. */

import { useMemo } from 'react'

const COLORS = [
  'var(--accent)',
  'var(--gold)',
  'var(--warn)',
  'color-mix(in oklab, var(--accent) 55%, var(--gold))',
]

export function Confetti({ count = 70 }: { count?: number }) {
  const reduced =
    typeof window !== 'undefined' &&
    window.matchMedia?.('(prefers-reduced-motion: reduce)').matches

  const pieces = useMemo(
    () =>
      Array.from({ length: count }, (_, i) => ({
        left: Math.random() * 100,
        delay: Math.random() * 0.6,
        duration: 2.2 + Math.random() * 1.6,
        color: COLORS[i % COLORS.length]!,
        rotate: Math.random() * 180,
      })),
    [count],
  )

  if (reduced) return null

  return (
    <div className="confetti" aria-hidden="true">
      {pieces.map((piece, i) => (
        <i
          key={i}
          style={{
            left: `${piece.left}%`,
            background: piece.color,
            animationDelay: `${piece.delay}s`,
            animationDuration: `${piece.duration}s`,
            transform: `rotate(${piece.rotate}deg)`,
          }}
        />
      ))}
    </div>
  )
}
