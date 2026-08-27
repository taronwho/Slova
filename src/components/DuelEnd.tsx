/**
 * Konec souboje.
 *
 * U Voštiny je hotovo hned — oba skončili v tutéž vteřinu a výsledek je
 * jen sečtená společná mapa. U Vetřelce může soupeř hrát až za den, takže
 * karta umí i stav „odehráno, čeká se". Jakmile výsledek dorazí, přepíše
 * se sama; kdo mezitím odejde do menu, najde ho tam v proužku soubojů.
 *
 * Obsah karty je **totéž porovnání**, které se dá kdykoli otevřít
 * z odehraných soubojů. Kdo hraje druhý, uvidí obě strany rovnou; kdo
 * první, uvidí svoji a u soupeře čekání. Dvě různé obrazovky pro tutéž věc
 * by znamenaly, že si hráč po dohrání a po návratu musí zvykat dvakrát.
 */

import { useContext, useEffect, useRef, useState } from 'react'

import { ReportContext } from '../app/nextUp'
import { verdictOf, type Verdict } from '../game/duel'
import { watchDone, type KartaHrace, type Match, type MatchScore } from '../lib/multi'
import { Confetti } from './Confetti'
import { DuelReport } from './DuelReport'

interface Props {
  match: Match
  uid: string
  /** Moje přezdívka — v porovnání stojí proti soupeřově. */
  nick: string
  mine: number
  /** Můj rozpis kol, zakódovaný. */
  detail?: string
  /** Moje soubojová hodnost pro erb. */
  rank?: number
  /** Moje karta z telefonu — aby se dalo ťuknout i na vlastní profil. */
  mojeKarta?: KartaHrace
  /** Skóre soupeře spočítané na místě — u Voštiny je známé rovnou. */
  fallback?: MatchScore
  verdict?: Verdict
  onHome: () => void
  /** Poslední parametr je můj rozpis — jde do archivu vedle soupeřova. */
  onVerdict: (
    verdict: Verdict,
    mine: number,
    souper: MatchScore,
    mujRozpis?: string,
  ) => void
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
  nick,
  mine,
  detail,
  rank = 0,
  mojeKarta,
  fallback,
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
    onVerdict(verdict, mine, row ?? { nick: rivalNick, score: 0 }, detail)
  }, [detail, mine, onVerdict, rivalNick, row, verdict])

  return (
    <>
      {verdict === 'win' && <Confetti />}
      <div className="result" role="dialog" aria-modal="true" aria-label="Výsledek souboje">
        <div className="result-card result-duel">
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

          <DuelReport
            id={match.id}
            kind={match.kind}
            verdict={verdict}
            me={{ nick, score: mine, detail, rank }}
            rivalNick={row?.nick ?? rivalNick}
            rivalUid={rivalUid}
            mojeKarta={mojeKarta}
            rival={
              row
                ? { nick: row.nick, score: row.score, detail: row.detail, uid: rivalUid }
                : null
            }
          />

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
                {/*
                  * Dokud soupeř nedohrál, není co oplácet — „Odveta" by na
                  * téhle obrazovce byla holá nepravda. Až když je výsledek
                  * známý, dává to slovo smysl.
                  */}
                {odveta === 'bezi'
                  ? 'Posílám…'
                  : verdict
                    ? 'Odveta'
                    : 'Vyzvat znovu'}
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
