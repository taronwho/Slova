/**
 * Potvrzení nevratného kroku.
 *
 * Vzdát kolo je jedno klepnutí od ztráty rozehrané hry a tlačítko je hned
 * vedle ovládání, takže se dá trefit omylem. Tenhle dialog se zeptá dřív,
 * než se něco stane; systémové zpět ho zavře jako každou jinou vrstvu.
 */

import { useBackGuard } from '../lib/back'

interface Props {
  title: string
  body: string
  confirmLabel: string
  onConfirm: () => void
  onCancel: () => void
}

export function Confirm({ title, body, confirmLabel, onConfirm, onCancel }: Props) {
  useBackGuard(true, onCancel)

  return (
    <div
      className="sheet-scrim"
      role="dialog"
      aria-modal="true"
      aria-label={title}
      onClick={onCancel}
    >
      <div className="sheet confirm" onClick={(event) => event.stopPropagation()}>
        <h2>{title}</h2>
        <p className="muted">{body}</p>
        <div className="sheet-actions">
          {/* Zrušit je první a výrazné — je to ta bezpečná volba. */}
          <button type="button" className="btn btn-primary" onClick={onCancel}>
            Zrušit
          </button>
          <button type="button" className="btn btn-danger" onClick={onConfirm}>
            {confirmLabel}
          </button>
        </div>
      </div>
    </div>
  )
}
