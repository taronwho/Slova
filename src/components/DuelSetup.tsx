/**
 * Výzva konkrétnímu hráči na konkrétní souboj.
 *
 * Dvě věci a nic víc: co se bude hrát a s kým. Formáty jsou dva a liší se
 * i tím, jestli na sebe musíte počkat — proto to u nich stojí rovnou,
 * ne až v pravidlech.
 */

import { useState } from 'react'

import { DUEL_ABOUT, DUEL_KINDS, DUEL_MODE, DUEL_TITLE, type DuelKind } from '../game/duel'
import { MODE_GLYPH } from '../game/types'

interface Props {
  onClose: () => void
  /** Vrací false, když hráč s takovou přezdívkou není. */
  onSend: (kind: DuelKind, nick: string) => Promise<boolean>
}

export function DuelSetup({ onClose, onSend }: Props) {
  const [kind, setKind] = useState<DuelKind>('hive')
  const [nick, setNick] = useState('')
  const [busy, setBusy] = useState(false)
  const [problem, setProblem] = useState<string | null>(null)

  async function send() {
    setBusy(true)
    setProblem(null)
    try {
      const ok = await onSend(kind, nick.trim())
      if (!ok) setProblem('Takového hráče neznám. Zkontroluj přezdívku.')
    } catch {
      setProblem('Nepodařilo se spojit. Zkus to znovu, až budeš online.')
    } finally {
      setBusy(false)
    }
  }

  return (
    <div className="sheet-scrim" onClick={onClose}>
      <div className="sheet" onClick={(event) => event.stopPropagation()}>
        <h3>Vyzvat hráče</h3>

        <div className="duel-picks">
          {DUEL_KINDS.map((one) => (
            <button
              type="button"
              key={one}
              className={`duel-pick ${kind === one ? 'on' : ''}`}
              data-mode={DUEL_MODE[one]}
              onClick={() => setKind(one)}
            >
              <span className="duel-pick-head">
                <span className="duel-mark" aria-hidden="true">
                  {MODE_GLYPH[DUEL_MODE[one]]}
                </span>
                <span className="duel-title">{DUEL_TITLE[one]}</span>
              </span>
              <span className="faint">{DUEL_ABOUT[one]}</span>
            </button>
          ))}
        </div>

        <input
          className="guess-input"
          value={nick}
          maxLength={16}
          placeholder="Přezdívka soupeře"
          onChange={(event) => {
            setNick(event.target.value)
            setProblem(null)
          }}
          onKeyDown={(event) => {
            if (event.key === 'Enter' && nick.trim()) void send()
          }}
        />
        {problem && <p className="duel-problem">{problem}</p>}

        <div className="sheet-actions">
          <button
            type="button"
            className="btn btn-primary"
            disabled={busy || !nick.trim()}
            onClick={() => void send()}
          >
            {busy ? 'Posílám…' : 'Vyzvat'}
          </button>
          <button type="button" className="btn btn-ghost" onClick={onClose}>
            Zpět
          </button>
        </div>
      </div>
    </div>
  )
}
