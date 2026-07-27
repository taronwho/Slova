/**
 * Hlavička a cenovky panelu nápověd.
 *
 * Cena se hlásí dvěma způsoby podle toho, čím se zrovna platí: dokud má hráč
 * dost inkoustu, vidí u tlačítka kapku a číslo, jinak bodovou srážku. Je to
 * na jednom místě, protože tohle pravidlo platí ve všech šesti hrách stejně
 * a rozepsané šestkrát by se rozešlo.
 */

import { inkPrice } from '../game/economy'
import { InkMark } from './art/InkMark'

/** Popisek nad tlačítky: kolik nápověd padlo a co zbývá v kalamáři. */
export function HintHead({ used, ink }: { used: number; ink: number }) {
  return (
    <div className="label">
      Nápovědy · {used} použito
      {ink > 0 && (
        <span className="free-left">
          {' · '}
          <InkMark size={10} /> {ink}
        </span>
      )}
    </div>
  )
}

/** Cenovka jedné nápovědy. `points` je její cena ve skóre. */
export function HintPrice({ points, ink }: { points: number; ink: number }) {
  const price = inkPrice(points)
  if (ink >= price) {
    return (
      <small className="price-ink">
        <InkMark size={10} /> {price}
      </small>
    )
  }
  return <small>−{points}</small>
}
