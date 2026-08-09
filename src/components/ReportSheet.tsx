/**
 * Nahlášení a zablokování soupeře.
 *
 * Přezdívku si píše hráč sám a vidí ji ostatní; filtr při zabírání zachytí
 * to zjevné, ale zbytek musí jít nahlásit. Panel dělá dvě věci naráz, protože
 * kdo sem přišel, chce obojí: pošle hlášení obsluze a soupeře rovnou odklidí
 * z cesty — od té chvíle se neobjeví ani jako náhodný soupeř, ani mezi výzvami.
 *
 * Zablokování platí i tehdy, když se hlášení nepodaří odeslat. Je místní,
 * takže na síti nezávisí, a hráč nemá čekat na server kvůli něčemu, co se
 * ho dotklo.
 */

import { useState } from 'react'

import { REPORT_REASONS } from '../game/nickCheck'

interface Props {
  nick: string
  onClose: () => void
  /** Odešle hlášení a zablokuje. Volá se až po výběru důvodu. */
  onSend: (reason: string) => void
}

export function ReportSheet({ nick, onClose, onSend }: Props) {
  const [sent, setSent] = useState(false)

  return (
    <div className="sheet-scrim" onClick={onClose}>
      <div className="sheet" onClick={(event) => event.stopPropagation()}>
        {sent ? (
          <>
            <h3>Odesláno</h3>
            <p className="muted">
              Hlášení jsme předali obsluze a hráče <b>{nick}</b> jsme ti
              zablokovali — už na něj v soubojích nenarazíš. Odblokovat ho jde
              v nabídce Hra s přáteli.
            </p>
            <div className="sheet-actions">
              <button type="button" className="btn btn-primary" onClick={onClose}>
                Zavřít
              </button>
            </div>
          </>
        ) : (
          <>
            <h3>Nahlásit hráče {nick}</h3>
            <p className="muted">
              Vyber, co je na něm špatně. Hráče ti zároveň zablokujeme, takže
              se ti už nepřiplete do cesty.
            </p>
            <div className="report-reasons">
              {REPORT_REASONS.map((reason) => (
                <button
                  type="button"
                  className="btn report-reason"
                  key={reason}
                  onClick={() => {
                    onSend(reason)
                    setSent(true)
                  }}
                >
                  {reason}
                </button>
              ))}
            </div>
            <div className="sheet-actions">
              <button type="button" className="btn btn-ghost" onClick={onClose}>
                Zpět
              </button>
            </div>
          </>
        )}
      </div>
    </div>
  )
}
