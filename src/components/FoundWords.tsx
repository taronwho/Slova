/**
 * Seznam už nalezených slov ve Voštině.
 *
 * Na monitoru je vidět v pravém sloupci pořád, na telefonu se tam nevejde —
 * otevře se tedy přes tlačítko. Bez něj hráč po chvíli neví, co už našel,
 * a zkouší dokola totéž.
 */

import { useBackGuard } from '../lib/back'

interface Props {
  words: string[]
  pangrams: string[]
  total: number
  score: (word: string) => number
  /** Kolik slov které délky ještě zbývá — délka -> počet. */
  remaining: Map<number, number>
  onClose: () => void
}

export function FoundWords({ words, pangrams, total, score, remaining, onClose }: Props) {
  useBackGuard(true, onClose)

  // Nejdelší nahoře — tam je nejvíc bodů a hráč si je pamatuje nejhůř.
  const byLength = new Map<number, string[]>()
  for (const word of [...words].sort((a, b) => a.localeCompare(b, 'cs'))) {
    const list = byLength.get(word.length) ?? []
    list.push(word)
    byLength.set(word.length, list)
  }
  const lengths = [...byLength.keys()].sort((a, b) => b - a)

  return (
    <div
      className="sheet-scrim"
      role="dialog"
      aria-modal="true"
      aria-label="Nalezená slova"
      onClick={onClose}
    >
      <div className="sheet" onClick={(event) => event.stopPropagation()}>
        <div className="sheet-head">
          <h2>
            Nalezená slova <span className="num muted">{words.length}/{total}</span>
          </h2>
          <button type="button" className="btn btn-sm btn-ghost" onClick={onClose}>
            Zavřít
          </button>
        </div>

        {/* Přehled zbývajících délek. Na telefonu je jen tady: v panelu
            pod pláství zabíral dva řádky čipů a plástev se pak nevešla na
            obrazovku. Sem patří i významem — je to referenční údaj, ne
            ovládání. */}
        {remaining.size > 0 && (
          <div className="remaining-strip">
            <div className="label">Kolik slov ještě zbývá</div>
            <div className="remaining-chips">
              {[...remaining.entries()].map(([length, count]) => (
                <span className="chip" key={length}>
                  {length} písmen · {count}
                </span>
              ))}
            </div>
          </div>
        )}

        <div className="found-groups">
          {lengths.map((length) => (
            <section key={length}>
              <div className="label">{length} písmen · {byLength.get(length)!.length}</div>
              <div className="found-list">
                {byLength.get(length)!.map((word) => (
                  <span
                    key={word}
                    className={`found-word ${pangrams.includes(word) ? 'pangram' : ''}`}
                    title={`+${score(word)}`}
                  >
                    {word}
                  </span>
                ))}
              </div>
            </section>
          ))}
          {words.length === 0 && (
            <p className="faint">Zatím nic — začni čtyřpísmenným slovem.</p>
          )}
        </div>
      </div>
    </div>
  )
}
