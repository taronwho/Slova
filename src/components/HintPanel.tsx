/**
 * Hlavička a cenovky panelu nápověd.
 *
 * Cena se hlásí dvěma způsoby podle toho, čím se zrovna platí: dokud má hráč
 * dost inkoustu, vidí u tlačítka kapku a číslo, jinak bodovou srážku. Je to
 * na jednom místě, protože tohle pravidlo platí ve všech hrách stejně
 * a rozepsané v každé hře zvlášť by se dřív nebo později rozešlo.
 */

import { inkPrice } from '../game/economy'
import { InkMark } from './art/InkMark'
import { Explain } from './Explain'

/**
 * Popisek nad tlačítky: kolik nápověd padlo a co zbývá v kalamáři.
 *
 * Je klikací. Hráč se právě rozhoduje, jestli nápovědu vzít, a tohle je jediné
 * místo v celé hře, kde tu otázku řeší — takže je to i jediné místo, kde se
 * vyplatí mít výklad ekonomiky na dosah ruky.
 */
export function HintHead({ used, ink }: { used: number; ink: number }) {
  return (
    <Explain
      term="napoveda"
      className="label hint-head"
      label={`Nápovědy: ${used} použito, ${ink} inkoustu. Jak fungují`}
    >
      Nápovědy · {used} použito
      {ink > 0 && (
        <span className="free-left">
          {' · '}
          <InkMark size={10} /> {ink}
        </span>
      )}
    </Explain>
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
