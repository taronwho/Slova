/**
 * Virtuální česká klávesnice.
 *
 * Čeština má 42 písmen, což by ve čtyřech řadách znamenalo 11 kláves na řádek
 * a na 320px displeji klávesy široké 25px. Řeší se to stejně jako na nativních
 * klávesnicích: základní rozložení má nejvýš 10 kláves a písmena s diakritikou
 * se vytáhnou podržením základního písmene. V rohu klávesy je náhled varianty,
 * aby to bylo poznat na první pohled.
 */

import { useCallback, useEffect, useRef, useState } from 'react'

const ROWS = ['qwertzuiop', 'asdfghjkl', 'yxcvbnm'].map((row) => row.split(''))

/** Varianty dostupné po podržení klávesy. */
const VARIANTS: Record<string, string[]> = {
  a: ['á'],
  c: ['č'],
  d: ['ď'],
  e: ['ě', 'é'],
  i: ['í'],
  n: ['ň'],
  o: ['ó'],
  r: ['ř'],
  s: ['š'],
  t: ['ť'],
  u: ['ů', 'ú'],
  y: ['ý'],
  z: ['ž'],
}

const LONG_PRESS_MS = 280

interface Props {
  onLetter: (letter: string) => void
  onBackspace: () => void
  onEnter: () => void
  enterLabel?: string
  /** Písmena, která teď nemají smysl. */
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
  const [openKey, setOpenKey] = useState<string | null>(null)
  const timer = useRef<number | null>(null)
  const fired = useRef(false)

  const clearTimer = useCallback(() => {
    if (timer.current !== null) {
      window.clearTimeout(timer.current)
      timer.current = null
    }
  }, [])

  useEffect(() => clearTimer, [clearTimer])

  // Klepnutí mimo vyskakovací nabídku ji zavře.
  useEffect(() => {
    if (!openKey) return
    const close = (event: Event) => {
      const target = event.target as HTMLElement | null
      if (!target?.closest('.key-variants')) setOpenKey(null)
    }
    window.addEventListener('pointerdown', close, true)
    return () => window.removeEventListener('pointerdown', close, true)
  }, [openKey])

  function pressStart(letter: string) {
    fired.current = false
    if (!VARIANTS[letter]) return
    clearTimer()
    timer.current = window.setTimeout(() => {
      fired.current = true
      setOpenKey(letter)
      if (navigator.vibrate) navigator.vibrate(12)
    }, LONG_PRESS_MS)
  }

  function pressEnd(letter: string, event: React.PointerEvent) {
    clearTimer()
    // Po vytažení variant se základní písmeno nezapisuje.
    if (fired.current) {
      fired.current = false
      // Prst mohl mezitím sjet na vytaženou variantu, jako na systémové
      // klávesnici. Na dotykovém displeji přitom `pointerup` dostane pořád
      // základní klávesa — prohlížeč jí ukazatel na začátku stisku
      // implicitně přidělí a do konce gesta ho nepustí. Co je pod prstem
      // doopravdy, se proto musí zjistit ze souřadnic.
      const under = document.elementFromPoint(event.clientX, event.clientY)
      const picked = under?.closest<HTMLElement>('.key.variant')?.dataset.letter
      if (picked) {
        onLetter(picked)
        setOpenKey(null)
      }
      return
    }
    if (openKey) return
    onLetter(letter)
  }

  return (
    <div className="keyboard" role="group" aria-label="Klávesnice">
      {ROWS.map((row, index) => (
        <div className="kb-row" key={index}>
          {row.map((letter) => {
            const variants = VARIANTS[letter]
            return (
              <div className="key-slot" key={letter}>
                <button
                  type="button"
                  className="key"
                  disabled={disabled?.has(letter) ?? false}
                  onPointerDown={() => pressStart(letter)}
                  onPointerUp={(event) => pressEnd(letter, event)}
                  onPointerLeave={clearTimer}
                  onPointerCancel={clearTimer}
                  onContextMenu={(event) => event.preventDefault()}
                  aria-label={
                    variants ? `${letter}, podržením ${variants.join(' nebo ')}` : letter
                  }
                >
                  {letter}
                  {variants && <span className="key-hint">{variants[0]}</span>}
                </button>

                {openKey === letter && variants && (
                  <div className="key-variants">
                    {variants.map((variant) => (
                      <button
                        type="button"
                        key={variant}
                        className="key variant"
                        data-letter={variant}
                        /*
                         * Zapisuje se na `click`, ne na `pointerup`.
                         *
                         * Nabídka se otevírá **nad** klávesnicí a v Řetězu
                         * tím pádem přesně přes tlačítka Vrátit tah a Vzdát
                         * kolo. Když se písmeno zapsalo už na `pointerup`,
                         * zmizela nabídka z DOMu dřív, než prohlížeč stihl
                         * poslat dodatečné `click` — to, které posílá po
                         * každém doteku kvůli stránkám psaným na myš. Ptal
                         * se pak znovu, co na těch souřadnicích leží, našel
                         * tlačítko pod nabídkou a stiskl je. Písmeno se
                         * přitom napsalo správně, jenže hned nato ho *Vrátit
                         * tah* smazal, takže to vypadalo, že klepnutí
                         * netrefilo.
                         *
                         * Na `click` nabídka v DOMu ještě stojí, klepnutí
                         * dostane ona a žádné další už nepřijde. Navrch to
                         * spraví ovládání z klávesnice, kde `pointerup`
                         * nikdy nepřijde.
                         */
                        onClick={() => {
                          onLetter(variant)
                          setOpenKey(null)
                        }}
                      >
                        {variant}
                      </button>
                    ))}
                  </div>
                )}
              </div>
            )
          })}
        </div>
      ))}

      <div className="kb-row kb-actions">
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
