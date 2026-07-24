/** Virtuální česká klávesnice — na mobilu hlavní vstup, na desktopu doplněk. */

import { KEYBOARD_ROWS } from '../lib/czech'

interface Props {
  onLetter: (letter: string) => void
  onBackspace: () => void
  onEnter: () => void
  enterLabel?: string
  /** Písmena, která teď nemají smysl (mimo plástev, mimo zásobník dlaždic). */
  disabled?: ReadonlySet<string>
  enterDisabled?: boolean
}

export function Keyboard({
  onLetter,
  onBackspace,
  onEnter,
  enterLabel = 'Potvrdit',
  disabled,
  enterDisabled = false,
}: Props) {
  return (
    <div className="keyboard" role="group" aria-label="Klávesnice">
      {KEYBOARD_ROWS.map((row, index) => (
        <div className="kb-row" key={index}>
          {row.map((letter) => (
            <button
              type="button"
              key={letter}
              className="key"
              disabled={disabled?.has(letter) ?? false}
              onClick={() => onLetter(letter)}
            >
              {letter}
            </button>
          ))}
        </div>
      ))}
      {/* Akce mají vlastní řádek — jinak by se jejich popisky na úzkém
          telefonu ořezaly. */}
      <div className="kb-row">
        <button
          type="button"
          className="key wide"
          onClick={onBackspace}
          aria-label="Smazat písmeno"
        >
          ⌫
        </button>
        <button
          type="button"
          className="key wide accent"
          onClick={onEnter}
          disabled={enterDisabled}
        >
          {enterLabel}
        </button>
      </div>
    </div>
  )
}
