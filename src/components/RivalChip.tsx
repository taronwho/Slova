/**
 * Soupeř v souboji — přezdívka, odznak hodnosti a její číslo.
 *
 * V souboji je jméno soupeře jediné, co o něm hráč ví, a to je málo: proti
 * komu vlastně hraju, je zkušený, nebo taky začíná? Odznak s číslem to řekne
 * na první pohled a ťuknutí otevře zbytek — jméno hodnosti, soubojovou
 * hodnost a bilanci vzájemných klání.
 *
 * Karta se načítá **až na ťuknutí**, ne dopředu. Uprostřed souboje se nemá
 * chodit na server pro nic, co hráč nechtěl; a kdo si soupeře prohlížet
 * nebude, nezaplatí za to ani jedním požadavkem.
 */

import { useState } from 'react'

import { duelPoints, duelRankFor, duelsPlayed, duelWinRate } from '../game/duelRank'
import { RANKS } from '../game/ranks'
import { nactiHrace, SoubojChyba, type KartaHrace } from '../lib/multi'
import { RankBadge } from './art/RankBadge'

interface Props {
  uid: string
  nick: string
  /** Hodnost, kterou hra zná ze zápasu. Karta ji po načtení upřesní. */
  band?: number
}

export function RivalChip({ uid, nick, band = 0 }: Props) {
  const [otevreno, setOtevreno] = useState(false)
  const [karta, setKarta] = useState<KartaHrace | null>(null)
  const [chyba, setChyba] = useState<string | null>(null)
  const [nacita, setNacita] = useState(false)

  const hodnost = karta?.band || band

  async function otevri() {
    setOtevreno(true)
    if (karta || nacita) return
    setNacita(true)
    setChyba(null)
    try {
      const nalezeno = await nactiHrace(uid)
      if (!nalezeno) setChyba('O tomhle hráči zatím server nic neví.')
      else setKarta(nalezeno)
    } catch (potiz) {
      setChyba(
        potiz instanceof SoubojChyba
          ? potiz.message
          : 'Kartu se nepodařilo načíst. Zkus to za chvíli.',
      )
    } finally {
      setNacita(false)
    }
  }

  return (
    <>
      <button
        type="button"
        className="rival-chip"
        onClick={() => void otevri()}
        aria-label={`${nick}${hodnost > 0 ? `, hodnost ${hodnost}` : ''} — ukázat kartu hráče`}
      >
        {hodnost > 0 && <RankBadge rank={hodnost} size={18} compact />}
        <span className="rival-nick">{nick}</span>
        {hodnost > 0 && <span className="rival-band num">{hodnost}</span>}
      </button>

      {otevreno && (
        <div className="sheet-scrim" onClick={() => setOtevreno(false)}>
          <div
            className="sheet rival-sheet"
            onClick={(event) => event.stopPropagation()}
            role="dialog"
            aria-modal="true"
            aria-label={`Karta hráče ${nick}`}
          >
            <KartaObsah karta={karta} nick={nick} band={hodnost} nacita={nacita} chyba={chyba} />
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
}: {
  karta: KartaHrace | null
  nick: string
  band: number
  nacita: boolean
  chyba: string | null
}) {
  const jmenoHodnosti = band > 0 ? RANKS[band - 1]?.name : undefined
  const bilance = karta ?? { wins: 0, losses: 0, draws: 0 }
  const souboju = duelsPlayed(bilance)
  const soubojova = duelRankFor(duelPoints(bilance))
  const uspesnost = duelWinRate(bilance)

  return (
    <>
      <div className="rival-head">
        {band > 0 && <RankBadge rank={band} size={44} />}
        <div>
          <h3>{karta?.nick ?? nick}</h3>
          <p className="faint">
            {jmenoHodnosti ? `${jmenoHodnosti} · ${band}. hodnost` : 'Hodnost zatím neposlal'}
          </p>
        </div>
      </div>

      {nacita && <p className="muted">Načítám kartu…</p>}
      {chyba && <p className="duel-problem">{chyba}</p>}

      {karta && (
        <>
          <div className="rival-rank">
            <span className="label">V soubojích</span>
            <b>{soubojova.rank.name}</b>
            <span className="faint">
              {soubojova.next
                ? `${soubojova.rank.index}. z ${12} · do další ${soubojova.span - soubojova.into} b.`
                : `${soubojova.rank.index}. z ${12} · nejvyšší`}
            </span>
          </div>

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
              ? 'Tohle je jeho první souboj.'
              : `Odehráno ${souboju} soubojů${uspesnost === null ? '' : ` · úspěšnost ${uspesnost} %`}.`}
          </p>
        </>
      )}
    </>
  )
}
