/**
 * Karta hráče — erb soubojové hodnosti a přezdívka.
 *
 * Stojí u soupeře v liště souboje i na obou stranách porovnání, tedy i nad
 * vlastním jménem: „na profil se dá kliknout" má platit pro oba, ne jen pro
 * toho druhého. U sebe sama se na server nechodí — data jsou v telefonu
 * přesnější i rychlejší, takže se předají hotová (`karta`).
 *
 * V souboji je jméno soupeře jediné, co o něm hráč ví, a to je málo: proti
 * komu vlastně hraju, je zkušený, nebo taky začíná? Erb to řekne na první
 * pohled a ťuknutí otevře zbytek.
 *
 * Ukazuje se **soubojová** hodnost, ne ta z profilu. Souboj je o hraní proti
 * lidem a jediné, co v něm o soupeři něco vypovídá, je, kolik klání má za
 * sebou; věhlas z denních kol se do toho míchat nemá. Hodnost profilu proto
 * čeká uvnitř karty, kam se dostane ten, koho zajímá.
 *
 * Karta se načte **jednou při otevření souboje**. Původně se čekalo až na
 * ťuknutí, aby se uprostřed hry nechodilo na server zbytečně — jenže pak
 * u přezdívky nebyl erb vidět vůbec, dokud hráč sám neťukl, a to je přesně
 * to, co má o soupeři říct na první pohled. Je to jedno čtení na celý souboj
 * a bere se z něj i obsah karty, takže ťuknutí už na server nesahá.
 */

import { useEffect, useState } from 'react'

import { DUEL_RANKS, duelPoints, duelRankFor, duelsPlayed, duelWinRate } from '../game/duelRank'
import { RANKS } from '../game/ranks'
import { nactiHrace, SoubojChyba, type KartaHrace } from '../lib/multi'
import { DuelCrest } from './art/DuelCrest'
import { RankBadge } from './art/RankBadge'

interface Props {
  /** Skryté id hráče. Chybí, jen když je karta předaná hotová. */
  uid?: string
  nick: string
  /** Hodnost profilu, kterou hra zná ze zápasu. Karta ji po načtení upřesní. */
  band?: number
  /**
   * `chip` je proužek k přezdívce v liště souboje, `panel` je sloupec
   * v porovnání — tam je na erb místo a stojí za to ho ukázat velký.
   */
  variant?: 'chip' | 'panel'
  /** Hotová karta. Když je, na server se nesahá — typicky u sebe sama. */
  karta?: KartaHrace
  /** Popisek nad přezdívkou v panelu, třeba „ty" u vlastní strany. */
  role?: string
}

export function RivalChip({
  uid,
  nick,
  band = 0,
  variant = 'chip',
  karta: hotova,
  role,
}: Props) {
  const [otevreno, setOtevreno] = useState(false)
  const [nactena, setNactena] = useState<KartaHrace | null>(null)
  const [chyba, setChyba] = useState<string | null>(null)
  const [nacita, setNacita] = useState(false)

  const karta = hotova ?? nactena
  const hodnost = karta?.band || band
  const soubojova = karta ? duelRankFor(duelPoints(karta)) : null

  useEffect(() => {
    if (hotova || !uid) return undefined
    let zahozeno = false
    setNacita(true)
    setChyba(null)
    nactiHrace(uid)
      .then((nalezeno) => {
        if (zahozeno) return
        if (!nalezeno) setChyba('O tomhle hráči zatím server nic neví.')
        else setNactena(nalezeno)
      })
      .catch((potiz: unknown) => {
        if (zahozeno) return
        setChyba(
          potiz instanceof SoubojChyba
            ? potiz.message
            : 'Kartu se nepodařilo načíst. Zkus to za chvíli.',
        )
      })
      .finally(() => {
        if (!zahozeno) setNacita(false)
      })
    return () => {
      zahozeno = true
    }
  }, [hotova, uid])

  const popis = hotova
    ? `${nick}${soubojova ? `, ${soubojova.rank.name}` : ''} — ukázat tvoji kartu`
    : `${nick}${soubojova ? `, ${soubojova.rank.name}` : ''} — ukázat kartu hráče`

  return (
    <>
      <button
        type="button"
        className={variant === 'panel' ? 'rival-panel' : 'rival-chip'}
        onClick={() => setOtevreno(true)}
        aria-label={popis}
      >
        {/* Dokud karta nedorazí, drží místo zašedlý erb. Bez něj se sloupec
            po načtení posune a v porovnání se rozjedou obě strany. */}
        <DuelCrest
          rank={soubojova?.rank.index ?? 2}
          size={variant === 'panel' ? 46 : 20}
          locked={!soubojova}
        />
        <span className="rival-nick">{karta?.nick ?? nick}</span>
        {variant === 'panel' && (
          <span className="rival-rank-name faint">
            {role ? `${role} · ` : ''}
            {soubojova ? soubojova.rank.name : '…'}
          </span>
        )}
      </button>

      {otevreno && (
        <div className="sheet-scrim" onClick={() => setOtevreno(false)}>
          <div
            className="sheet rival-sheet"
            onClick={(event) => event.stopPropagation()}
            role="dialog"
            aria-modal="true"
            aria-label={hotova ? 'Tvoje karta' : `Karta hráče ${nick}`}
          >
            <KartaObsah
              karta={karta}
              nick={nick}
              band={hodnost}
              nacita={nacita}
              chyba={chyba}
              ja={Boolean(hotova)}
            />
            <div className="sheet-actions">
              <button type="button" className="btn btn-ghost" onClick={() => setOtevreno(false)}>
                Zavřít
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  )
}

function KartaObsah({
  karta,
  nick,
  band,
  nacita,
  chyba,
  ja,
}: {
  karta: KartaHrace | null
  nick: string
  band: number
  nacita: boolean
  chyba: string | null
  /** Vlastní karta. Mění se jí jen mluvnická osoba — o tobě, ne o něm. */
  ja: boolean
}) {
  const jmenoHodnosti = band > 0 ? RANKS[band - 1]?.name : undefined
  const bilance = karta ?? { wins: 0, losses: 0, draws: 0 }
  const souboju = duelsPlayed(bilance)
  const soubojova = duelRankFor(duelPoints(bilance))
  const uspesnost = duelWinRate(bilance)

  return (
    <>
      {/* Hlavička patří soubojové hodnosti — kvůli ní se karta otevírá. */}
      <div className="rival-head">
        <DuelCrest rank={soubojova.rank.index} size={64} title={soubojova.rank.name} />
        <div>
          <h3>{karta?.nick ?? nick}</h3>
          <p className="faint">
            {soubojova.rank.name} · {soubojova.rank.index}. z {DUEL_RANKS.length}
          </p>
        </div>
      </div>

      {nacita && <p className="muted">Načítám kartu…</p>}
      {chyba && <p className="duel-problem">{chyba}</p>}

      {karta && (
        <>
          <div className="rival-tally">
            <span className="stat">
              <span className="label">Výhry</span>
              <span className="value num">{bilance.wins}</span>
            </span>
            <span className="stat">
              <span className="label">Remízy</span>
              <span className="value num">{bilance.draws}</span>
            </span>
            <span className="stat">
              <span className="label">Prohry</span>
              <span className="value num">{bilance.losses}</span>
            </span>
          </div>

          <p className="faint">
            {souboju === 0
              ? ja
                ? 'Tohle je tvůj první souboj.'
                : 'Tohle je jeho první souboj.'
              : `Odehráno ${souboju} soubojů${uspesnost === null ? '' : ` · úspěšnost ${uspesnost} %`}.`}
            {soubojova.next
              ? ` Do hodnosti ${soubojova.next.name} ${ja ? 'ti' : 'mu'} zbývá ${
                  soubojova.span - soubojova.into
                } b.`
              : ' Výš už se dostat nedá.'}
          </p>

          {/*
            * Hodnost z profilu až tady dole, a jen tady.
            *
            * Věhlas se sbírá v denních kolech, kde soupeř žádný není —
            * do souboje proto nemluví. Kdo ale chce vědět, kolik toho ten
            * druhý nahrál mimo klání, najde to po rozkliknutí karty.
            */}
          {band > 0 && (
            <div className="rival-offline">
              <RankBadge rank={band} size={34} />
              <span>
                <span className="label">Mimo souboje</span>
                <b>{jmenoHodnosti}</b>
                <span className="faint"> · {band}. hodnost</span>
              </span>
            </div>
          )}
        </>
      )}
    </>
  )
}
