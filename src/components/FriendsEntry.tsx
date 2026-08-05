/**
 * Vstup do soubojů na úvodní obrazovce.
 *
 * Stojí úplně nahoře, nad výběrem hry, protože souboj se hraje ve dvou —
 * a živá Voština se nedá odbýt „až se k tomu dostanu". Když něco došlo,
 * nese odznak s počtem; ten je jediný důvod, proč se sem hráč podívá,
 * aniž by měl v plánu někoho vyzvat.
 */

interface Props {
  /** Vlastní přezdívka, nebo prázdno, když ještě žádnou nemá. */
  nick: string
  /** Kolik věcí čeká na vyřízení — došlé výzvy a dohrané zápasy. */
  waiting: number
  onOpen: () => void
}

export function FriendsEntry({ nick, waiting, onOpen }: Props) {
  return (
    <button
      type="button"
      className={`friends-entry ${waiting > 0 ? 'live' : ''}`}
      onClick={onOpen}
      aria-label={
        waiting > 0 ? `Hra s přáteli — ${waiting} novinek` : 'Hra s přáteli'
      }
    >
      <span className="friends-entry-mark" aria-hidden="true">
        ⚔
      </span>
      <span className="friends-entry-body">
        <span className="friends-entry-title">Hra s přáteli</span>
        <span className="faint">
          {waiting > 0
            ? 'Někdo na tebe čeká'
            : nick
              ? `Hraješ jako ${nick}`
              : 'Vyzvi kamaráda na souboj'}
        </span>
      </span>
      {waiting > 0 && <span className="friends-entry-badge num">{waiting}</span>}
      <span className="friends-entry-go" aria-hidden="true">
        →
      </span>
    </button>
  )
}
