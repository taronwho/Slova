/**
 * Proužek soubojů na domovské obrazovce.
 *
 * Bez přezdívky zve dovnitř. S přezdívkou drží tři věci: bilanci, tlačítko
 * na výzvu a to, co přišlo — došlé výzvy a dohrané zápasy, u kterých soupeř
 * mezitím odehrál svoje. Vejde se to sem právě proto, že souboj sám má
 * vlastní obrazovku a tady o něm stačí jedna řádka.
 */

import { useState } from 'react'

import { DUEL_MODE, DUEL_TITLE, verdictOf, VERDICT_TITLE, type DuelKind } from '../game/duel'
import { MODE_GLYPH } from '../game/types'
import { claimNick, loadMe, nickError, saveMe, type Challenge, type Me } from '../lib/multi'

/** Dohraný zápas, o kterém hráč ještě neví. */
export interface DuelReport {
  id: string
  kind: DuelKind
  rival: string
  mine: number
  theirs: number
}

interface Props {
  me: Me
  onMe: (me: Me) => void
  challenges?: Challenge[]
  onAccept?: (challenge: Challenge) => void
  reports?: DuelReport[]
  onSeen?: (id: string) => void
  onChallenge?: () => void
}

export function DuelStrip({
  me,
  onMe,
  challenges = [],
  onAccept,
  reports = [],
  onSeen,
  onChallenge,
}: Props) {
  const [open, setOpen] = useState(false)
  const [draft, setDraft] = useState('')
  const [busy, setBusy] = useState(false)
  const [problem, setProblem] = useState<string | null>(null)

  async function submit() {
    const bad = nickError(draft)
    if (bad) {
      setProblem(bad)
      return
    }
    setBusy(true)
    setProblem(null)
    try {
      const free = await claimNick(draft)
      if (!free) {
        setProblem('Tuhle přezdívku už někdo má. Zkus jinou.')
        return
      }
      const next = { ...loadMe(), nick: draft.trim() }
      saveMe(next)
      onMe(next)
      setOpen(false)
    } catch {
      setProblem('Nepodařilo se spojit. Zkus to znovu, až budeš online.')
    } finally {
      setBusy(false)
    }
  }

  if (!me.nick) {
    return (
      <>
        <button type="button" className="duel-strip" onClick={() => setOpen(true)}>
          <span className="duel-mark" aria-hidden="true">
            ⚔
          </span>
          <span className="duel-body">
            <span className="duel-title">Souboje</span>
            <span className="faint">Zvol přezdívku a vyzvi někoho na souboj</span>
          </span>
        </button>

        {open && (
          <div className="sheet-scrim" onClick={() => setOpen(false)}>
            <div className="sheet" onClick={(event) => event.stopPropagation()}>
              <h3>Jak ti mají ostatní říkat?</h3>
              <p className="muted">
                Přezdívku uvidí soupeři u výsledků a podle ní tě dokážou vyzvat.
                Každá může být ve hře jen jednou — kdo dřív přijde, ten ji má.
              </p>
              <input
                className="guess-input"
                value={draft}
                autoFocus
                maxLength={16}
                placeholder="Přezdívka"
                onChange={(event) => setDraft(event.target.value)}
                onKeyDown={(event) => {
                  if (event.key === 'Enter') void submit()
                }}
              />
              {problem && <p className="duel-problem">{problem}</p>}
              <div className="sheet-actions">
                <button
                  type="button"
                  className="btn btn-primary"
                  disabled={busy || !draft}
                  onClick={() => void submit()}
                >
                  {busy ? 'Zapisuji…' : 'Zabrat'}
                </button>
                <button type="button" className="btn btn-ghost" onClick={() => setOpen(false)}>
                  Teď ne
                </button>
              </div>
            </div>
          </div>
        )}
      </>
    )
  }

  const played = me.wins + me.losses + me.draws
  return (
    <>
      {/* Dohrané zápasy. Vyzývatel se o výsledku dozví právě tady — svoje
          kolo měl odehrané dávno, soupeř ho dohnal až teď. */}
      {reports.map((item) => {
        const verdict = verdictOf(item.mine, item.theirs)
        return (
          <button
            type="button"
            className={`duel-strip report ${verdict}`}
            key={item.id}
            onClick={() => onSeen?.(item.id)}
          >
            <span className="duel-mark" aria-hidden="true">
              {MODE_GLYPH[DUEL_MODE[item.kind]]}
            </span>
            <span className="duel-body">
              <span className="duel-title">
                {VERDICT_TITLE[verdict]} · {item.rival}
              </span>
              <span className="faint">
                {item.mine.toLocaleString('cs-CZ')} : {item.theirs.toLocaleString('cs-CZ')} ·{' '}
                {DUEL_TITLE[item.kind]}
              </span>
            </span>
          </button>
        )
      })}

      {/* Došlé výzvy. Ťuknutí spustí souboj — u Voštiny rovnou, protože na
          druhé straně někdo čeká. */}
      {challenges.map((item) => (
        <button
          type="button"
          className="duel-strip challenge"
          key={item.id}
          onClick={() => onAccept?.(item)}
        >
          <span className="duel-mark" aria-hidden="true">
            {MODE_GLYPH[DUEL_MODE[item.kind]]}
          </span>
          <span className="duel-body">
            <span className="duel-title">{item.nick} tě vyzval</span>
            <span className="faint">{DUEL_TITLE[item.kind]}</span>
          </span>
        </button>
      ))}

      <div className="duel-strip done">
        <span className="duel-mark" aria-hidden="true">
          ⚔
        </span>
        <span className="duel-body">
          <span className="duel-title">{me.nick}</span>
          <span className="faint">
            {played === 0
              ? 'Vyzvi někoho podle přezdívky a změř si s ním síly'
              : `${me.wins} výher · ${me.losses} proher · ${me.draws} remíz`}
          </span>
        </span>
        <button type="button" className="btn btn-sm" onClick={() => onChallenge?.()}>
          Vyzvat
        </button>
      </div>
    </>
  )
}
