/** Závěrečná karta kola — rozpis skóre, sdílení, další kolo. */

import { useEffect, useState, type ReactNode } from 'react'

import type { ScoreBreakdown } from '../game/scoring'
import { Confetti } from './Confetti'

interface Props {
  title: string
  subtitle?: string
  breakdown: ScoreBreakdown
  shareText: string
  celebrate?: boolean
  children?: ReactNode
  onNext: () => void
  onHome: () => void
}

/** Odpočítá skóre nahoru — drobnost, která výsledku dá váhu. */
function useCountUp(target: number, duration = 900): number {
  const [value, setValue] = useState(0)

  useEffect(() => {
    const reduced = window.matchMedia?.('(prefers-reduced-motion: reduce)').matches
    if (reduced) {
      setValue(target)
      return
    }
    let frame = 0
    const start = performance.now()
    const tick = (now: number) => {
      const progress = Math.min((now - start) / duration, 1)
      // easeOutCubic
      const eased = 1 - Math.pow(1 - progress, 3)
      setValue(Math.round(target * eased))
      if (progress < 1) frame = requestAnimationFrame(tick)
    }
    frame = requestAnimationFrame(tick)
    return () => cancelAnimationFrame(frame)
  }, [target, duration])

  return value
}

export function ResultOverlay({
  title,
  subtitle,
  breakdown,
  shareText,
  celebrate = true,
  children,
  onNext,
  onHome,
}: Props) {
  const score = useCountUp(breakdown.total)
  const [copied, setCopied] = useState(false)

  async function share() {
    try {
      if (navigator.share) {
        await navigator.share({ text: shareText })
        return
      }
      await navigator.clipboard.writeText(shareText)
      setCopied(true)
      setTimeout(() => setCopied(false), 2200)
    } catch {
      // Uživatel sdílení zrušil — není co řešit.
    }
  }

  return (
    <>
      {celebrate && <Confetti />}
      <div className="result" role="dialog" aria-modal="true" aria-label="Výsledek kola">
        <div className="result-card">
          <h2>{title}</h2>
          {subtitle && <p className="muted" style={{ marginTop: 'var(--sp-2)' }}>{subtitle}</p>}

          <div className="score-big num">{score.toLocaleString('cs-CZ')}</div>
          {breakdown.multiplierLabel && (
            <span className="chip chip-gold">{breakdown.multiplierLabel}</span>
          )}

          {children}

          <div className="breakdown">
            {breakdown.lines.map((line, i) => (
              <div
                className="breakdown-line"
                key={line.label}
                style={{ animationDelay: `${120 + i * 70}ms` }}
              >
                <span className="muted">{line.label}</span>
                <span className={`num ${line.value < 0 ? 'neg' : 'pos'}`}>
                  {line.value > 0 ? '+' : ''}
                  {line.value.toLocaleString('cs-CZ')}
                </span>
              </div>
            ))}
            <div className="breakdown-line total">
              <span>Celkem</span>
              <span className="num">{breakdown.total.toLocaleString('cs-CZ')}</span>
            </div>
          </div>

          <div className="result-actions">
            <button type="button" className="btn btn-primary" onClick={onNext}>
              Další kolo
            </button>
            <button type="button" className="btn" onClick={share}>
              {copied ? 'Zkopírováno' : 'Sdílet'}
            </button>
            <button type="button" className="btn btn-ghost" onClick={onHome}>
              Domů
            </button>
          </div>
        </div>
      </div>
    </>
  )
}
