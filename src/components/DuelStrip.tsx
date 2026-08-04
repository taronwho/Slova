/**
 * Proužek soubojů na domovské obrazovce.
 *
 * Bez přezdívky zve dovnitř, s přezdívkou ukazuje bilanci. Nic víc se sem
 * nevejde a nic víc tu ani nemá být — souboje se hrají uvnitř běžných kol,
 * ne na vlastní obrazovce.
 */

import { useState } from 'react'

import {
  claimNick,
  loadMe,
  nickError,
  saveMe,
  type Me,
} from '../lib/multi'

interface Props {
  me: Me
  onMe: (me: Me) => void
}

export function DuelStrip({ me, onMe }: Props) {
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
            <span className="faint">Zvol přezdívku a měř se s ostatními</span>
          </span>
        </button>

        {open && (
          <div className="sheet-scrim" onClick={() => setOpen(false)}>
            <div className="sheet" onClick={(event) => event.stopPropagation()}>
              <h3>Jak ti mají ostatní říkat?</h3>
              <p className="muted">
                Přezdívku uvidí soupeři u výsledků. Každá může být ve hře jen
                jednou — kdo dřív přijde, ten ji má.
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
    <div className="duel-strip done">
      <span className="duel-mark" aria-hidden="true">
        ⚔
      </span>
      <span className="duel-body">
        <span className="duel-title">{me.nick}</span>
        <span className="faint">
          {played === 0
            ? 'Zahraj denní výzvu a najde se ti soupeř'
            : `${me.wins} výher · ${me.losses} proher · ${me.draws} remíz`}
        </span>
      </span>
    </div>
  )
}
