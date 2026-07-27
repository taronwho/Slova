/**
 * Návod, který se otevře při prvním spuštění režimu — a kdykoli později
 * tlačítkem Pravidla. Kroky mají malé ukázky ze skutečných herních prvků,
 * aby hráč poznal, na co se v samotné hře dívá.
 */

import { useState, type ReactNode } from 'react'

import { TUTORIALS, type TutorialVisual } from '../game/tutorials'
import { MODE_LABEL, type ModeId } from '../game/types'
import { Gallows } from './art/Gallows'

interface Props {
  mode: ModeId
  onClose: () => void
  /** Popisek posledního tlačítka — liší se podle toho, odkud se návod otevřel. */
  finishLabel?: string
}

/** Zvýrazní **tučné** úseky, aby text nesl důraz bez HTML v datech. */
function withEmphasis(text: string): ReactNode[] {
  return text.split(/(\*\*[^*]+\*\*)/g).map((part, i) =>
    part.startsWith('**') && part.endsWith('**') ? (
      <strong key={i}>{part.slice(2, -2)}</strong>
    ) : (
      <span key={i}>{part}</span>
    ),
  )
}

function Tiles({ word, variant }: { word: string; variant?: string }) {
  return (
    <div className={`rung ${variant ?? ''}`}>
      {[...word].map((letter, i) => (
        <div className="tile" key={i}>
          {letter}
        </div>
      ))}
    </div>
  )
}

function Visual({ visual }: { visual: TutorialVisual }) {
  switch (visual.kind) {
    case 'chain-goal':
      return (
        <div className="tut-visual tut-ladder">
          <Tiles word="kosa" variant="is-start" />
          <div className="ladder-gap">
            <div className="dots">
              <i />
              <i />
              <i />
            </div>
            <span>tvůj řetěz</span>
          </div>
          <Tiles word="míra" variant="is-goal" />
        </div>
      )

    case 'chain-move':
      return (
        <div className="tut-visual tut-ladder">
          <Tiles word="kosa" />
          <div className="connector lit" />
          <div className="rung">
            {[...'koza'].map((letter, i) => (
              <div className={`tile ${i === 2 ? 'changed' : ''}`} key={i}>
                {letter}
              </div>
            ))}
          </div>
          <p className="tut-caption">Změnilo se jediné písmeno — a vzniklo nové slovo.</p>
        </div>
      )

    case 'chain-guard':
      return (
        <div className="tut-visual">
          <div className="stat" style={{ maxWidth: 200, margin: '0 auto' }}>
            <div className="label">Zbývá nejméně</div>
            <div className="value num accent">3</div>
          </div>
          <div className="banner banner-warn" style={{ marginTop: 'var(--sp-3)' }}>
            <span>Slepá ulička — odtud už se k cíli nedostaneš.</span>
            <span className="banner-actions">
              <span className="btn btn-sm">Vrátit tah</span>
            </span>
          </div>
        </div>
      )

    case 'chain-score':
      return (
        <div className="tut-visual">
          <div className="breakdown" style={{ margin: 0 }}>
            <div className="breakdown-line">
              <span className="muted">Základ</span>
              <span className="num pos">+1 000</span>
            </div>
            <div className="breakdown-line">
              <span className="muted">Tahů navíc (1)</span>
              <span className="num neg">−100</span>
            </div>
            <div className="breakdown-line">
              <span className="muted">Rychlost</span>
              <span className="num pos">+300</span>
            </div>
          </div>
        </div>
      )

    case 'hive':
      return (
        <div className="tut-visual">
          <div className="hive tut-hive">
            <button type="button" className="hex center" style={{ left: '33.5%', top: '33.8%' }}>
              r
            </button>
            {[
              { l: 'a', left: '33.5%', top: '0%' },
              { l: 'k', left: '67%', top: '16.9%' },
              { l: 't', left: '67%', top: '50.7%' },
              { l: 'o', left: '33.5%', top: '67.6%' },
              { l: 's', left: '0%', top: '50.7%' },
              { l: 'v', left: '0%', top: '16.9%' },
            ].map((hex) => (
              <button type="button" className="hex" key={hex.l} style={{ left: hex.left, top: hex.top }}>
                {hex.l}
              </button>
            ))}
          </div>
        </div>
      )

    case 'hive-word':
      return (
        <div className="tut-visual">
          <div className="hive-input" style={{ justifyContent: 'center' }}>
            {[...'kára'].map((ch, i) => (
              <span className={`ch ${ch === 'r' ? 'center' : ''}`} key={i}>
                {ch}
              </span>
            ))}
          </div>
          <p className="tut-caption">
            Zvýrazněné písmeno uprostřed musí být v každém slově.
          </p>
        </div>
      )

    case 'hive-pangram':
      return (
        <div className="tut-visual">
          <div style={{ display: 'flex', gap: 'var(--sp-2)', justifyContent: 'center', flexWrap: 'wrap' }}>
            <span className="found-word">kára</span>
            <span className="found-word">tvar</span>
            <span className="found-word pangram">trakař</span>
          </div>
          <p className="tut-caption">Pangram použije všech sedm písmen — a nese 7 bodů navíc.</p>
        </div>
      )

    case 'hive-ranks':
      return (
        <div className="tut-visual">
          <div className="rank-line">
            <span className="rank">Skvělý</span>
            <span className="num muted">62 / 180</span>
          </div>
          <div className="progress-track">
            <div className="progress-fill" style={{ width: '34%' }} />
          </div>
        </div>
      )

    case 'tower':
      return (
        <div className="tut-visual">
          <div className="tower tut-tower">
            <div className="floor base">
              {[...'les'].map((l, i) => (
                <div className="tile" key={i}>
                  {l}
                </div>
              ))}
            </div>
            <div className="floor done">
              {[...'sele'].map((l, i) => (
                <div className="tile" key={i}>
                  {l}
                </div>
              ))}
            </div>
            <div className="floor active">
              {Array.from({ length: 5 }, (_, i) => (
                <div className="tile empty" key={i} />
              ))}
            </div>
          </div>
        </div>
      )

    case 'tower-letter':
      return (
        <div className="tut-visual">
          <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--sp-3)', justifyContent: 'center', flexWrap: 'wrap' }}>
            <div className="floor done">
              {[...'sele'].map((l, i) => (
                <div className="tile" key={i}>
                  {l}
                </div>
              ))}
            </div>
            <span className="muted" style={{ fontSize: '1.4rem' }}>+</span>
            <span className="new-letter">n</span>
            <span className="muted" style={{ fontSize: '1.4rem' }}>=</span>
            <div className="floor done">
              {[...'selen'].map((l, i) => (
                <div className="tile" key={i}>
                  {l}
                </div>
              ))}
            </div>
          </div>
        </div>
      )

    case 'word-forms':
      return (
        <div className="tut-visual">
          <div className="forms-table">
            <div className="forms-col ok">
              <span className="label">Platí</span>
              <span>pes</span>
              <span>psi</span>
              <span>psát</span>
              <span>velký</span>
            </div>
            <div className="forms-col no">
              <span className="label">Neplatí</span>
              <span>psa</span>
              <span>psy</span>
              <span>píšeš</span>
              <span>většímu</span>
            </div>
          </div>
        </div>
      )

    case 'tower-safe':
      return (
        <div className="tut-visual">
          <div style={{ display: 'flex', gap: 'var(--sp-3)', justifyContent: 'center', flexWrap: 'wrap' }}>
            <div className="floor done">
              {[...'pila'].map((l, i) => (
                <div className="tile" key={i}>
                  {l}
                </div>
              ))}
            </div>
            <div className="floor done">
              {[...'lipa'].map((l, i) => (
                <div className="tile" key={i}>
                  {l}
                </div>
              ))}
            </div>
          </div>
          <p className="tut-caption">
            Obě řešení mají stejná písmena, takže obě vedou dál. Nemůžeš vybrat špatně.
          </p>
        </div>
      )

    case 'gallows':
      return (
        <div className="tut-visual">
          <Gallows parts={3} />
          <div className="word-slots" style={{ ['--slots' as string]: 5 }}>
            {['k', null, 'n', null, null].map((letter, i) => (
              <span className={`slot ${letter ? 'filled' : ''}`} key={i}>
                {letter ?? ''}
              </span>
            ))}
          </div>
          <p className="tut-caption">Tři chybná písmena, tři díly. Zbývá pět životů.</p>
        </div>
      )

    // Ukázka na skutečném hesle: text o původu, v něm okénko po zakrytém
    // slově a pod ním prázdná políčka. Přesně to, co hráč uvidí v kole.
    case 'detective':
      return (
        <div className="tut-visual">
          <blockquote className="clue-card" style={{ width: '100%' }}>
            <p style={{ fontSize: '0.9rem' }}>
              Z latinského <mark className="clue-gap">?</mark> — „hlídač lože“, složeného
              z „postel“ a kořene slovesa „mít, držet“.
            </p>
          </blockquote>
          <div className="word-slots" style={{ ['--slots' as string]: 6 }}>
            {['e', null, null, null, null, null].map((letter, i) => (
              <span className={`slot ${letter ? 'filled' : ''}`} key={i}>
                {letter ?? ''}
              </span>
            ))}
          </div>
          <p className="tut-caption">Okénko s otazníkem je slovo, které hádáš.</p>
        </div>
      )

    // Padající dvojice a čtyři polohy, ve kterých se dá přečíst.
    case 'tetris':
      return (
        <div className="tut-visual">
          <div
            className="well"
            style={{ ['--cols' as string]: 4, ['--rows' as string]: 3, width: 180 }}
          >
            {[
              ['', '', '', ''],
              ['ko', 'lo', '', ''],
              ['', '', '', ''],
            ].map((row, r) =>
              row.map((text, c) => (
                <span className={`cell ${text ? 'live' : ''}`} key={`${r}-${c}`}>
                  {text}
                </span>
              )),
            )}
          </div>
          <p className="tut-caption">KO + LO vedle sebe = KOLO. Obojí zmizí.</p>
        </div>
      )

    // Otáčení: táž dvojice, čtyři polohy, dvojí pořadí.
    case 'tetris-chain':
      return (
        <div className="tut-visual">
          <div
            style={{ display: 'flex', gap: 'var(--sp-4)', alignItems: 'center', justifyContent: 'center' }}
          >
            <div style={{ textAlign: 'center' }}>
              <div className="well" style={{ ['--cols' as string]: 2, width: 88 }}>
                <span className="cell live">ko</span>
                <span className="cell live">lo</span>
              </div>
              <span className="faint" style={{ fontSize: '0.72rem' }}>
                KOLO
              </span>
            </div>
            <span className="tut-arrow" aria-hidden="true">
              ⟳
            </span>
            <div style={{ textAlign: 'center' }}>
              <div className="well" style={{ ['--cols' as string]: 1, width: 44 }}>
                <span className="cell live">lo</span>
                <span className="cell live">ko</span>
              </div>
              <span className="faint" style={{ fontSize: '0.72rem' }}>
                taky KOLO
              </span>
            </div>
          </div>
          <p className="tut-caption">Svisle se čte zdola nahoru — proto je „lo" nahoře.</p>
        </div>
      )

    case 'gallows-fold':
      return (
        <div className="tut-visual">
          <div style={{ display: 'flex', gap: 'var(--sp-3)', alignItems: 'center' }}>
            <span className="letter-key hit" style={{ maxWidth: 46, flex: '0 0 46px' }}>
              u
            </span>
            <span className="tut-arrow" aria-hidden="true">
              →
            </span>
            <div className="word-slots" style={{ ['--slots' as string]: 3 }}>
              {['k', 'ů', 'ň'].map((letter, i) => (
                <span className={`slot ${i === 1 ? 'filled' : ''}`} key={i}>
                  {i === 1 ? letter : ''}
                </span>
              ))}
            </div>
          </div>
          <p className="tut-caption">Písmeno „u" odhalí „u", „ú" i „ů".</p>
        </div>
      )
  }
}

export function Tutorial({ mode, onClose, finishLabel = 'Začít hrát' }: Props) {
  const steps = TUTORIALS[mode]
  const [index, setIndex] = useState(0)
  const step = steps[index]!
  const last = index === steps.length - 1

  return (
    <div className="result" role="dialog" aria-modal="true" aria-label={`Návod — ${MODE_LABEL[mode]}`}>
      <div className="tut-card">
        <div className="tut-head">
          <span className="label">
            {MODE_LABEL[mode]} · návod {index + 1}/{steps.length}
          </span>
          <button type="button" className="btn btn-sm btn-ghost" onClick={onClose}>
            Přeskočit
          </button>
        </div>

        <div className="tut-progress" aria-hidden="true">
          {steps.map((_, i) => (
            <span key={i} className={i <= index ? 'on' : ''} />
          ))}
        </div>

        <div className="tut-body" key={index}>
          <h2>{step.title}</h2>
          {step.visual && <Visual visual={step.visual} />}
          {step.body.map((paragraph, i) => (
            <p key={i}>{withEmphasis(paragraph)}</p>
          ))}
          {step.key && <p className="tut-key">{withEmphasis(step.key)}</p>}
        </div>

        <div className="tut-actions">
          <button
            type="button"
            className="btn"
            onClick={() => setIndex((n) => n - 1)}
            disabled={index === 0}
          >
            Zpět
          </button>
          <button
            type="button"
            className="btn btn-primary"
            onClick={() => (last ? onClose() : setIndex((n) => n + 1))}
          >
            {last ? finishLabel : 'Další'}
          </button>
        </div>
      </div>
    </div>
  )
}
