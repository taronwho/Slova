/**
 * Výzva konkrétnímu hráči na konkrétní souboj.
 *
 * Dvě věci a nic víc: co se bude hrát a s kým. Formáty jsou dva a liší se
 * i tím, jestli na sebe musíte počkat — proto to u nich stojí rovnou,
 * ne až v pravidlech.
 */

import { useState } from 'react'

import { DUEL_ABOUT, DUEL_KINDS, DUEL_MODE, DUEL_TITLE, type DuelKind } from '../game/duel'
import { SoubojChyba, zkouskaSpojeni, type Nalez } from '../lib/multi'
import { MODE_GLYPH } from '../game/types'

interface Props {
  onClose: () => void
  /**
   * Vrací false, když hráč s takovou přezdívkou není.
   *
   * `krok` je popisek toho, co se zrovna děje. Odeslání výzvy má dvě fáze
   * a každá čeká na něco jiného — hádanky na síť, zápas na databázi —
   * a když se to zaseklo, byl na tlačítku pořád jen jeden nápis, takže
   * z něj nešlo poznat, která z nich stojí.
   */
  onSend: (kind: DuelKind, nick: string, krok: (co: string) => void) => Promise<boolean>
}

export function DuelSetup({ onClose, onSend }: Props) {
  const [kind, setKind] = useState<DuelKind>('hive')
  const [nick, setNick] = useState('')
  const [busy, setBusy] = useState(false)
  const [krok, setKrok] = useState('Posílám…')
  const [problem, setProblem] = useState<string | null>(null)
  const [rozbor, setRozbor] = useState<Nalez[] | 'bezi' | null>(null)

  async function send() {
    setBusy(true)
    setKrok('Posílám…')
    setProblem(null)
    setRozbor(null)
    try {
      const ok = await onSend(kind, nick.trim(), setKrok)
      if (!ok) setProblem('Takového hráče neznám. Zkontroluj přezdívku.')
    } catch (chyba) {
      // Do konzole i celá chyba: hláška na obrazovce je pro hráče, tohle je
      // pro případ, kdy se to hlásí a je potřeba vědět víc.
      console.error('Souboj se nepodařilo odeslat:', chyba)
      // Co má hráč vědět přesně (server mlčí, chybí přezdívka), to se ukáže
      // doslova; zbytek dostane obecnou větu.
      setProblem(
        chyba instanceof SoubojChyba
          ? chyba.message
          : 'Nepodařilo se spojit. Zkus to znovu, až budeš online.',
      )
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
          aria-label="Přezdívka soupeře"
          onChange={(event) => {
            setNick(event.target.value)
            setProblem(null)
          }}
          onKeyDown={(event) => {
            if (event.key === 'Enter' && nick.trim()) void send()
          }}
        />
        {problem && <p className="duel-problem">{problem}</p>}

        {/*
          * Rozbor rovnou u chyby.
          *
          * Když výzva neprojde, je jediná otázka „kde to vázne" — a odpověď
          * na ni je jinde v nabídce, což je uprostřed nezdaru to poslední,
          * co chce hráč hledat. Tady je na jedno ťuknutí a dá se vyfotit.
          */}
        {problem && (
          <div className="duel-rozbor">
            <button
              type="button"
              className="btn btn-sm btn-ghost"
              disabled={rozbor === 'bezi'}
              onClick={() => {
                setRozbor('bezi')
                void zkouskaSpojeni().then(setRozbor, () => setRozbor(null))
              }}
            >
              {rozbor === 'bezi' ? 'Zjišťuji…' : 'Kde to vázne?'}
            </button>
            {Array.isArray(rozbor) && (
              <ul className="check-list">
                {rozbor.map((nalez) => (
                  <li key={nalez.krok} className={nalez.ok ? 'ok' : 'bad'}>
                    <span aria-hidden="true">{nalez.ok ? '✓' : '✗'}</span> {nalez.krok}:{' '}
                    <span className="faint">{nalez.detail}</span>
                  </li>
                ))}
              </ul>
            )}
          </div>
        )}

        <div className="sheet-actions">
          <button
            type="button"
            className="btn btn-primary"
            disabled={busy || !nick.trim()}
            onClick={() => void send()}
          >
            {busy ? krok : 'Vyzvat'}
          </button>
          <button type="button" className="btn btn-ghost" onClick={onClose}>
            Zpět
          </button>
        </div>
      </div>
    </div>
  )
}
