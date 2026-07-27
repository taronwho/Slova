/**
 * Vysvětlivky — vrstva, díky které jde ve Slovech kliknout úplně na všechno.
 *
 * Pravidlo je jednoduché: **žádný popisek není slepý**. Když na obrazovce
 * stojí číslo nebo název, ťuknutí na něj buď otevře odstavec vysvětlení
 * (`<Explain term="…">`), nebo vede tam, kam patří — do vitríny, do statistik,
 * do pravidel hry. Nikdy se nestane nic.
 *
 * Provider drží jediný panel pro celou aplikaci. Kdyby si každý čip vozil
 * vlastní, byl by ve stromu třicetkrát a systémové zpět by se v nich zamotalo;
 * takhle je vrstva jedna a `useBackGuard` na ni stačí jedno.
 */

import {
  createContext,
  useCallback,
  useContext,
  useMemo,
  useState,
  type ReactNode,
} from 'react'

import { TERMS, type ExplainTarget, type Term } from '../game/glossary'
import { useBackGuard } from '../lib/back'

interface ExplainApi {
  /** Otevře výklad pojmu ze slovníčku. Neznámý klíč nic neudělá. */
  show: (id: string) => void
  /**
   * Otevře výklad, který nemá smysl vozit ve slovníčku.
   *
   * Údaje uvnitř kola („Zbývá nejméně", „Životy") patří jedné hře a jedné
   * obrazovce; do společného slovníčku by je nikdo nehledal. Panel je ale
   * stejný, takže se hráč neučí dvoje ovládání — a hlavně se ve hře nic
   * nerozbalí a deska se nehne.
   */
  note: (title: string, body: string) => void
  /** Odejde na obrazovku, o které výklad mluví. */
  go: (target: ExplainTarget) => void
}

const Context = createContext<ExplainApi | null>(null)

export function useExplain(): ExplainApi {
  const api = useContext(Context)
  // Bez provideru se komponenta pořád vykreslí — jen se nic nestane. Hra
  // nemá spadnout kvůli vysvětlivce.
  return api ?? { show: () => {}, note: () => {}, go: () => {} }
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

export function ExplainProvider({
  onGo,
  children,
}: {
  onGo: (target: ExplainTarget) => void
  children: ReactNode
}) {
  /** Buď klíč do slovníčku, nebo rovnou hotový výklad z místa volání. */
  const [open, setOpen] = useState<string | Term | null>(null)

  const api = useMemo<ExplainApi>(
    () => ({
      show: (id: string) => setOpen(id),
      note: (title: string, body: string) => setOpen({ title, body: [body] }),
      go: (target: ExplainTarget) => {
        // Odkaz na jiné heslo hráče nikam neodvede — jen se v panelu vymění
        // text. Uprostřed rozehraného kola je to jediný cíl, který se dá
        // nabídnout, aniž by se opustila hra.
        if (target.startsWith('term:')) {
          setOpen(target.slice('term:'.length))
          return
        }
        setOpen(null)
        onGo(target)
      },
    }),
    [onGo],
  )

  const close = useCallback(() => setOpen(null), [])
  useBackGuard(open !== null, close)

  const entry = typeof open === 'string' ? TERMS[open] : (open ?? undefined)

  return (
    <Context.Provider value={api}>
      {children}
      {entry && (
        <div
          className="sheet-scrim"
          role="dialog"
          aria-modal="true"
          aria-label={entry.title}
          onClick={close}
        >
          <div className="sheet sheet-term" onClick={(event) => event.stopPropagation()}>
            <div className="sheet-head">
              <h2>{entry.title}</h2>
              <span className="rule" />
              <button type="button" className="btn btn-sm btn-ghost" onClick={close}>
                Zavřít
              </button>
            </div>
            <div className="term-body">
              {entry.body.map((paragraph, i) => (
                <p key={i}>{withEmphasis(paragraph)}</p>
              ))}
            </div>
            {entry.links && (
              <div className="sheet-actions">
                {entry.links.map((link) => (
                  <button
                    type="button"
                    key={link.to}
                    className="btn btn-sm"
                    onClick={() => api.go(link.to)}
                  >
                    {link.label}
                  </button>
                ))}
              </div>
            )}
          </div>
        </div>
      )}
    </Context.Provider>
  )
}

interface ExplainProps {
  /** Klíč do slovníčku v glossary.ts. */
  term: string
  /** Třída obalu — čip vypadá jako čip, řádek jako řádek. */
  className?: string
  /** Přípona k popisku pro čtečky, když z obsahu není jasné, o co jde. */
  label?: string
  title?: string
  style?: React.CSSProperties
  children: ReactNode
}

/**
 * Klikací obal nad čímkoli, co má vysvětlivku.
 *
 * Je to `<button>`, ne `<span>` s posluchačem: čtečka i klávesnice se k němu
 * pak dostanou samy a nemusí se nic dolepovat rolí a tabindexem.
 */
export function Explain({ term, className, label, title, style, children }: ExplainProps) {
  const { show } = useExplain()
  const entry = TERMS[term]
  return (
    <button
      type="button"
      className={`explain ${className ?? ''}`}
      style={style}
      title={title ?? `${entry?.title ?? term} — co to je`}
      aria-label={label}
      onClick={() => show(term)}
    >
      {children}
    </button>
  )
}

/**
 * Údaj na desce hry — „Tahy 3", „Životy 6", „Zbývá nejméně 4".
 *
 * Vypadá jako každá jiná dlaždice statistiky, jen se dá ťuknout a řekne, co
 * měří. Uprostřed kola se nesmí nic rozbalovat pod prstem, takže se výklad
 * otevře v panelu nad hrou a deska zůstane, kde je.
 *
 * `term` bere výklad ze slovníčku, `note` z místa volání. Bez jednoho i druhého
 * je z dlaždice zase jen mrtvé číslo.
 */
export function StatTile({
  label,
  value,
  tone,
  note,
  term,
  title,
  className,
  children,
}: {
  label: ReactNode
  value: ReactNode
  tone?: 'accent' | 'gold' | 'warn' | undefined
  note?: string
  term?: string
  /** Nadpis panelu, když se popisek skládá z prvků a nedá se z něj přečíst. */
  title?: string
  className?: string
  /** Drobnost pod číslem — třeba rozpočet tahů v Řetězu. */
  children?: ReactNode
}) {
  const api = useExplain()
  const heading = title ?? (typeof label === 'string' ? label : '')
  return (
    <button
      type="button"
      className={`stat stat-tap ${className ?? ''}`}
      title={note ?? heading}
      onClick={() => {
        if (term) api.show(term)
        else if (note) api.note(heading, note)
      }}
    >
      <div className="label">{label}</div>
      <div className={`value num ${tone ?? ''}`}>{value}</div>
      {children}
    </button>
  )
}
