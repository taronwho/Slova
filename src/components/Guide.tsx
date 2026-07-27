/**
 * Průvodce celou hrou — „Jak se hrají Slova".
 *
 * Návody jednotlivých her vysvětlí, jak se hraje Řetěz nebo Voština. Tenhle
 * vysvětlí, co je věhlas, proč se láme série a odkud se bere inkoust — tedy
 * všechno, co je společné a co se hráč jinak nedozvěděl nikde.
 *
 * Otevře se sám při úplně prvním spuštění a od té chvíle je pod tlačítkem na
 * domovské obrazovce. Není to krokovaný tutoriál, ale souvislý text: kdo se
 * v něm potřebuje jen něco doohlédnout, nemá proklikávat devět obrazovek.
 */

import { GUIDE } from '../game/tutorials'
import { MODE_LABEL, MODE_TAGLINE, type ModeId } from '../game/types'
import { useBackGuard } from '../lib/back'
import { useExplain } from './Explain'

interface Props {
  onClose: () => void
  onRules: (mode: ModeId) => void
  /** Popisek posledního tlačítka — po prvním spuštění zní jinak než jindy. */
  finishLabel?: string
}

const MODES: ModeId[] = ['chain', 'hive', 'tower', 'gallows', 'detective', 'tetris']

/** Zvýrazní **tučné** úseky, aby text nesl důraz bez HTML v datech. */
function withEmphasis(text: string) {
  return text.split(/(\*\*[^*]+\*\*)/g).map((part, i) =>
    part.startsWith('**') && part.endsWith('**') ? (
      <strong key={i}>{part.slice(2, -2)}</strong>
    ) : (
      <span key={i}>{part}</span>
    ),
  )
}

export function Guide({ onClose, onRules, finishLabel = 'Zavřít' }: Props) {
  const { show } = useExplain()
  useBackGuard(true, onClose)

  return (
    <div
      className="sheet-scrim"
      role="dialog"
      aria-modal="true"
      aria-label="Jak se hrají Slova"
      onClick={onClose}
    >
      <div className="sheet sheet-guide" onClick={(event) => event.stopPropagation()}>
        <div className="sheet-head">
          <h2>Jak se hrají Slova</h2>
          <span className="rule" />
          <button type="button" className="btn btn-sm btn-ghost" onClick={onClose}>
            Zavřít
          </button>
        </div>

        <div className="guide-body">
          {GUIDE.map((section) => (
            <section key={section.title}>
              <h3>{section.title}</h3>
              {section.body.map((paragraph, i) => (
                <p key={i}>{withEmphasis(paragraph)}</p>
              ))}
              {section.term && (
                <button
                  type="button"
                  className="btn btn-sm btn-ghost guide-more"
                  onClick={() => show(section.term!)}
                >
                  Více
                </button>
              )}
            </section>
          ))}

          <section>
            <h3>Které hry to jsou</h3>
            <p>Ťukni na hru a otevře se její podrobný návod s ukázkami.</p>
            <div className="guide-modes">
              {MODES.map((mode) => (
                <button
                  type="button"
                  key={mode}
                  className="guide-mode"
                  data-mode={mode}
                  onClick={() => onRules(mode)}
                >
                  <span className="guide-mode-name">{MODE_LABEL[mode]}</span>
                  <span className="faint">{MODE_TAGLINE[mode]}</span>
                </button>
              ))}
            </div>
          </section>
        </div>

        <div className="sheet-actions">
          <button type="button" className="btn btn-primary" onClick={onClose}>
            {finishLabel}
          </button>
        </div>
      </div>
    </div>
  )
}
