/**
 * Konec souboje.
 *
 * U Voštiny je hotovo hned — oba skončili v tutéž vteřinu a výsledek je
 * jen sečtená společná mapa. U Vetřelce může soupeř hrát až za den, takže
 * karta umí i stav „odehráno, čeká se". Jakmile výsledek dorazí, přepíše
 * se sama; kdo mezitím odejde do menu, najde ho tam v proužku soubojů.
 */

import { useContext, useEffect, useRef, useState } from 'react'

import { ReportContext } from '../app/nextUp'
import { VERDICT_TITLE, verdictOf, type Verdict } from '../game/duel'
import { watchDone, type Match, type MatchScore } from '../lib/multi'
import { Confetti } from './Confetti'

interface Props {
  match: Match
  uid: string
  mine: number
  /** Skóre soupeře spočítané na místě — u Voštiny je známé rovnou. */
  fallback?: MatchScore
  verdict?: Verdict
  note?: string
  onHome: () => void
  onVerdict: (verdict: Verdict) => void
}

export function DuelEnd({ match, uid, mine, fallback, note, onHome, onVerdict }: Props) {
  const [rows, setRows] = useState<Record<string, MatchScore>>({})
  const report = useContext(ReportContext)
  const rivalUid = match.host === uid ? match.guest : match.host
  const rivalNick = match.host === uid ? match.guestNick : match.hostNick

  useEffect(() => watchDone(match.id, setRows), [match.id])

  const row = rows[rivalUid] ?? fallback ?? null
  const verdict = row ? verdictOf(mine, row.score) : null

  // Bilance se připíše jednou, až je o čem. Čekání se do ní nepočítá.
  const counted = useRef(false)
  useEffect(() => {
    if (!verdict || counted.current) return
    counted.current = true
    onVerdict(verdict)
  }, [onVerdict, verdict])

  return (
    <>
      {verdict === 'win' && <Confetti />}
      <div className="result" role="dialog" aria-modal="true" aria-label="Výsledek souboje">
        <div className="result-card">
          <div className="result-sign">
            <span className="brand result-brand" aria-label="Slova">
              Sl<span className="mark">o</span>va
              <span className="brand-triad" aria-hidden="true">
                <i style={{ background: 'var(--mode-chain)' }} />
                <i style={{ background: 'var(--mode-hive)' }} />
                <i style={{ background: 'var(--mode-tower)' }} />
              </span>
            </span>
            <span className="result-mode">
              <span className="result-mode-glyph" aria-hidden="true">
                ⚔
              </span>
              Souboj
            </span>
          </div>

          <h2>{verdict ? VERDICT_TITLE[verdict] : 'Odehráno'}</h2>
          {note && <p className="muted">{note}</p>}

          <div className={`duel-card ${verdict === 'win' ? 'won' : verdict === 'loss' ? 'lost' : ''}`}>
            <span className="duel-line">
              <b className="num">{mine.toLocaleString('cs-CZ')}</b>
              <span className="faint">:</span>
              <b className="num">{row ? row.score.toLocaleString('cs-CZ') : '—'}</b>
              <span className="faint">{row?.nick ?? rivalNick}</span>
            </span>
          </div>

          {!row && (
            <p className="muted">
              {rivalNick} má tvoje kolo ve výzvách. Až ho dohraje, najdeš
              výsledek v menu u soubojů.
            </p>
          )}

          <div className="result-actions">
            <button type="button" className="btn btn-primary" onClick={onHome}>
              Zpět do menu
            </button>
          </div>

          {report && (
            <button
              type="button"
              className="report-link"
              onClick={() => report(rivalUid, row?.nick ?? rivalNick)}
            >
              Nahlásit přezdívku
            </button>
          )}
        </div>
      </div>
    </>
  )
}
