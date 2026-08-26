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
import { RivalChip } from './RivalChip'

interface Props {
  match: Match
  uid: string
  mine: number
  /** Skóre soupeře spočítané na místě — u Voštiny je známé rovnou. */
  fallback?: MatchScore
  verdict?: Verdict
  note?: string
  onHome: () => void
  onVerdict: (verdict: Verdict, mine: number) => void
  /**
   * Odveta se stejným soupeřem a stejným formátem.
   *
   * Bez ní se musela přezdívka pokaždé psát znovu, což u dvou lidí, kteří
   * si hrají celý večer, znamenalo psát ji pořád dokola. Vrací false, když
   * se soupeř mezitím ztratil (smazal si přezdívku).
   */
  onRematch?: () => Promise<boolean>
}

export function DuelEnd({
  match,
  uid,
  mine,
  fallback,
  note,
  onHome,
  onVerdict,
  onRematch,
}: Props) {
  const [rows, setRows] = useState<Record<string, MatchScore>>({})
  const [odveta, setOdveta] = useState<'ne' | 'bezi' | 'chyba'>('ne')
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
    onVerdict(verdict, mine)
  }, [mine, onVerdict, verdict])

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
              <RivalChip uid={rivalUid} nick={row?.nick ?? rivalNick} />
            </span>
          </div>

          {!row && (
            <p className="muted">
              {rivalNick} má tvoje kolo ve výzvách. Až ho dohraje, najdeš
              výsledek v menu u soubojů.
            </p>
          )}

          {odveta === 'chyba' && (
            <p className="duel-problem">
              Odvetu se nepodařilo poslat. Zkus to z Hry s přáteli.
            </p>
          )}

          <div className="result-actions">
            {onRematch && (
              <button
                type="button"
                className="btn btn-primary"
                disabled={odveta === 'bezi'}
                onClick={() => {
                  setOdveta('bezi')
                  void onRematch().then(
                    (ok) => setOdveta(ok ? 'ne' : 'chyba'),
                    () => setOdveta('chyba'),
                  )
                }}
              >
                {odveta === 'bezi' ? 'Posílám odvetu…' : 'Odveta'}
              </button>
            )}
            <button
              type="button"
              className={`btn ${onRematch ? '' : 'btn-primary'}`}
              onClick={onHome}
            >
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
