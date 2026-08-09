/** Závěrečná karta kola — rozpis skóre, sdílení, další kolo. */

import { useContext, useEffect, useState, type ReactNode } from 'react'

import { DuelContext, ReportContext, RoundModeContext, useNextUp } from '../app/nextUp'
import type { ScoreBreakdown } from '../game/scoring'
import { Confetti } from './Confetti'
import { Explain } from './Explain'

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

/** Česká čísla: poslední výzva, 2–4 výzvy, 5 a víc výzev. */
function count(left: number): string {
  if (left === 1) return 'poslední výzva'
  return `${left} ${left <= 4 ? 'výzvy' : 'výzev'}`
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
  const nextUp = useNextUp()
  const mode = useContext(RoundModeContext)
  const duel = useContext(DuelContext)
  const report = useContext(ReportContext)
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
          {/* Karta se podepíše. Snímek výsledku putuje ven ze hry — do
              zpráv, na sítě —, a bez značky je to jen tabulka čísel. */}
          <div className="result-sign">
            <span className="brand result-brand" aria-label="Slova">
              Sl<span className="mark">o</span>va
              <span className="brand-triad" aria-hidden="true">
                <i style={{ background: 'var(--mode-chain)' }} />
                <i style={{ background: 'var(--mode-hive)' }} />
                <i style={{ background: 'var(--mode-tower)' }} />
              </span>
            </span>
            {mode && (
              <span className="result-mode">
                <span className="result-mode-glyph" aria-hidden="true">
                  {mode.glyph}
                </span>
                {mode.label}
              </span>
            )}
          </div>

          <h2>{title}</h2>
          {subtitle && <p className="muted" style={{ marginTop: 'var(--sp-2)' }}>{subtitle}</p>}

          {/* I skóre je klikací: rozpis pod ním říká, za co body padly, ale
              ne to, kam se počítají a proč jsou čísla, jaká jsou. */}
          <Explain term="body" className="score-big num">
            {score.toLocaleString('cs-CZ')}
          </Explain>
          {breakdown.multiplierLabel && (
            <Explain term="serie" className="chip chip-gold">
              {breakdown.multiplierLabel}
            </Explain>
          )}

          {/* Souboj: tvoje skóre proti někomu, kdo hrál tutéž hádanku. */}
          {duel && (
            <div className={`duel-card ${duel.won === true ? 'won' : duel.won === false ? 'lost' : ''}`}>
              <span className="duel-verdict">
                {duel.won === null ? 'Remíza' : duel.won ? 'Vyhrál jsi!' : 'Tentokrát ne'}
              </span>
              <span className="duel-line">
                <b className="num">{breakdown.total.toLocaleString('cs-CZ')}</b>
                <span className="faint">:</span>
                <b className="num">{duel.score.toLocaleString('cs-CZ')}</b>
                <span className="faint">{duel.nick}</span>
              </span>
              {/* Přezdívku soupeře si psal on sám. Musí jít nahlásit odsud,
                  tedy z místa, kde ji hráč vidí — jinam se pro to vracet
                  nebude. */}
              {report && (
                <button
                  type="button"
                  className="report-link"
                  onClick={() => report(duel.uid, duel.nick)}
                >
                  Nahlásit přezdívku
                </button>
              )}
            </div>
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

          {/* Zbytek dnešní várky. Kdo hraje denní výzvy, nemusí se kvůli
              další vracet do menu — a hlavně vidí, kolik jich ještě zbývá. */}
          {nextUp.length > 0 && (
            <div className="next-up">
              <p className="next-up-head">
                {nextUp[0]!.id === 'quiz'
                  ? 'Denní výzvy máš hotové. Zbývá Otázka dne:'
                  : `Zbývá dnes ${count(nextUp.length)}:`}
              </p>
              <div className="next-up-list">
                {nextUp.map((item) => (
                  <button
                    type="button"
                    className="next-up-item"
                    key={item.id}
                    onClick={item.start}
                    data-mode={item.id}
                  >
                    <span className="next-up-glyph" aria-hidden="true">
                      {item.glyph}
                    </span>
                    {item.label}
                  </button>
                ))}
              </div>
            </div>
          )}

          <div className="result-actions">
            {nextUp.length > 0 ? (
              <button type="button" className="btn btn-primary" onClick={nextUp[0]!.start}>
                {nextUp[0]!.id === 'quiz' ? 'Otázka dne' : `Hrát ${nextUp[0]!.label}`}
              </button>
            ) : (
              <button type="button" className="btn btn-primary" onClick={onNext}>
                Další kolo
              </button>
            )}
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
