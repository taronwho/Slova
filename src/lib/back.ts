/**
 * Systémové tlačítko zpět.
 *
 * Na Androidu je „zpět" gesto, které hráč používá pořád. V nainstalované hře
 * ale nemá kam jít — historie je prázdná — a tak se celá aplikace zavře.
 * Tohle tomu dá smysl: každá otevřená vrstva (hra, návod, panel, potvrzení)
 * si přidá jeden záznam do historie, a když se hráč vrátí, zavře se místo
 * aplikace jen ta vrstva. Až když není co zavřít, chová se zpět normálně.
 *
 * Vrstvy se skládají na sebe, takže zpět nad otevřeným návodem uvnitř hry
 * zavře nejdřív návod a teprve pak hru.
 */

import { useEffect, useRef } from 'react'

interface Layer {
  id: number
  close: () => void
}

const layers: Layer[] = []
let nextId = 1
let listening = false
/**
 * Návrat, který si aplikace vyvolala sama při úklidu, a obsluha ho tedy má
 * pustit bez zavírání. Je to jedno místo, ne počítadlo: kdyby se úklidy
 * sešly, spolkne se jeden návrat navíc — což je pořád lepší, než aby
 * počítadlo narostlo a hltalo hráčovo mačkání zpět donekonečna.
 */
let skipLayerId: number | null = null

function onPopState() {
  if (skipLayerId !== null) {
    skipLayerId = null
    return
  }
  layers.pop()?.close()
}

/**
 * Dokud je `active`, přebírá systémové zpět zavření téhle vrstvy.
 *
 * `close` se čte přes ref, takže se obsluha nepřepisuje při každém renderu
 * a vrstva se do historie přidá právě jednou.
 */
export function useBackGuard(active: boolean, close: () => void): void {
  const closeRef = useRef(close)
  closeRef.current = close

  useEffect(() => {
    if (!active || typeof window === 'undefined') return

    const layer: Layer = { id: nextId++, close: () => closeRef.current() }
    layers.push(layer)
    if (!listening) {
      window.addEventListener('popstate', onPopState)
      listening = true
    }
    window.history.pushState({ slovaLayer: layer.id }, '')

    return () => {
      const at = layers.indexOf(layer)
      if (at >= 0) layers.splice(at, 1)
      // Vrstva se zavřela z aplikace, ne tlačítkem zpět — pak po ní zůstal
      // v historii záznam navíc a ten je potřeba uklidit. Návrat, který tím
      // vznikne, si obsluha musí nechat projít bez zavírání další vrstvy.
      const state = window.history.state as { slovaLayer?: number } | null
      if (state?.slovaLayer === layer.id) {
        skipLayerId = layer.id
        window.history.back()
      }
    }
  }, [active])
}
