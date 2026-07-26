/**
 * Oznámení o postupu — nová hodnost a čerstvá ocenění.
 *
 * Ukazuje se až **nad** výsledkem kola, protože je to odměna za to kolo:
 * hráč si nejdřív přečte skóre a teprve pak dostane, co mu za něj přibylo.
 * Když padne víc věcí naráz, projdou se jedna po druhé — dvě ocenění vedle
 * sebe by si navzájem ukradla okamžik.
 */

import { useState } from 'react'

import { AWARD_HINTS, awardById } from '../game/awards'
import { RANK_HINTS, RANKS } from '../game/ranks'
import { useBackGuard } from '../lib/back'
import { AwardArt } from './art/AwardArt'
import { RankBadge } from './art/RankBadge'

export interface Gained {
  /** Nová hodnost (1–20), pokud hráč povýšil. */
  rank: number | null
  /** ID ocenění, která padla v tomhle kole. */
  awards: string[]
}

interface Props {
  gained: Gained
  onClose: () => void
}

export function AwardPopup({ gained, onClose }: Props) {
  const items = [
    ...(gained.rank ? [{ kind: 'rank' as const, id: String(gained.rank) }] : []),
    ...gained.awards.map((id) => ({ kind: 'award' as const, id })),
  ]
  const [at, setAt] = useState(0)
  useBackGuard(true, onClose)

  const item = items[at]
  if (!item) return null

  const last = at === items.length - 1
  const next = () => (last ? onClose() : setAt((n) => n + 1))

  const rank = item.kind === 'rank' ? RANKS[Number(item.id) - 1]! : null
  const award = item.kind === 'award' ? awardById(item.id) : undefined
  const reward = rank ? RANK_HINTS : award ? AWARD_HINTS(award) : 0

  return (
    <div className="gained" role="dialog" aria-modal="true" aria-label="Nové ocenění">
      <div className="gained-card" key={item.id}>
        <span className="gained-kicker">{rank ? 'Nová hodnost' : 'Nové ocenění'}</span>

        <div className="gained-art">
          {rank ? (
            <RankBadge rank={rank.index} size={112} />
          ) : (
            <AwardArt art={award?.art ?? ''} tier={award?.tier} size={96} />
          )}
        </div>

        <h2>{rank ? rank.name : (award?.title ?? '')}</h2>
        <p className="muted">
          {rank ? `${rank.index}. hodnost z ${RANKS.length}` : (award?.goal ?? '')}
        </p>

        {/* Odměna je půlka radosti — bez ní by oznámení bylo jen pochvala. */}
        <span className="gained-reward">
          +{reward} {reward === 1 ? 'nápověda' : reward <= 4 ? 'nápovědy' : 'nápověd'} zdarma
        </span>

        {items.length > 1 && (
          <span className="faint num gained-count">
            {at + 1} / {items.length}
          </span>
        )}

        <div className="result-actions">
          <button type="button" className="btn btn-primary" onClick={next}>
            {last ? 'Pokračovat' : 'Další'}
          </button>
        </div>
      </div>
    </div>
  )
}
