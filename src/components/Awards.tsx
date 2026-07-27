/**
 * Vitrína — hodnost, žebříček padesáti stupňů a mřížka všech ocenění.
 *
 * Zamčené ocenění se neschovává. Hráč má vidět, co ho čeká, i jak daleko
 * k tomu má — u met na počet se pod dlaždicí táhne proužek postupu. Schované
 * mety nemotivují, protože o nich nikdo neví.
 */

import { useState } from 'react'

import { AWARDS, AWARD_GROUPS, GROUP_LABEL, GROUP_NOTE, type Award } from '../game/awards'
import { RANKS, rankFor } from '../game/ranks'
import { useBackGuard } from '../lib/back'
import type { Profile } from '../lib/storage'
import { AwardArt } from './art/AwardArt'
import { InkMark } from './art/InkMark'
import { RankBadge } from './art/RankBadge'

interface Props {
  profile: Profile
  onBack: () => void
}

const DATE = new Intl.DateTimeFormat('cs-CZ', { day: 'numeric', month: 'numeric', year: 'numeric' })

function AwardTile({ award, profile }: { award: Award; profile: Profile }) {
  const at = profile.awards[award.id]
  const has = at !== undefined
  const share = has ? 1 : (award.progress?.(profile) ?? 0)

  return (
    <div className={`award ${has ? 'has' : ''}`} data-tone={award.tone}>
      <AwardArt art={award.art} tier={award.tier} />
      <span className="award-title">{award.title}</span>
      <span className="award-goal">{award.goal}</span>
      {has ? (
        <span className="award-date">{DATE.format(at)}</span>
      ) : share > 0 ? (
        <span className="award-track" aria-hidden="true">
          <span style={{ width: `${Math.round(share * 100)}%` }} />
        </span>
      ) : (
        <span className="award-date faint">zamčeno</span>
      )}
    </div>
  )
}

export function Awards({ profile, onBack }: Props) {
  const progress = rankFor(profile.fame)
  const [ladder, setLadder] = useState(false)
  const has = AWARDS.filter((award) => profile.awards[award.id] !== undefined).length

  useBackGuard(ladder, () => setLadder(false))

  return (
    <>
      <div className="section-head" style={{ marginTop: 0 }}>
        <h2>Vitrína</h2>
        <span className="rule" />
        <button type="button" className="btn btn-sm" onClick={onBack}>
          Zpět
        </button>
      </div>

      <div className="panel rank-card">
        <RankBadge rank={progress.rank.index} size={72} />
        <div className="rank-card-body">
          <span className="label">
            Hodnost {progress.rank.index} / {RANKS.length}
          </span>
          <span className="rank-name">{progress.rank.name}</span>
          <div className="fame-bar">
            <span
              style={{ width: `${progress.span ? (progress.into / progress.span) * 100 : 100}%` }}
            />
          </div>
          <span className="faint">
            {progress.next
              ? `Do hodnosti ${progress.next.name} zbývá ${(
                  progress.span - progress.into
                ).toLocaleString('cs-CZ')} věhlasu`
              : 'Nejvyšší hodnost — dál už se nešplhá'}
          </span>
        </div>
      </div>

      <div className="award-summary">
        <span className="chip chip-accent">
          Ocenění {has} / {AWARDS.length}
        </span>
        <span className="chip">{profile.fame.toLocaleString('cs-CZ')} věhlasu</span>
        <span className="chip chip-ink">
          <InkMark size={11} /> <span className="num">{profile.ink}</span>
        </span>
        <span className="chip">Nejlepší série {profile.bestStreak}</span>
        <button type="button" className="btn btn-sm" onClick={() => setLadder(true)}>
          Všech {RANKS.length} hodností
        </button>
      </div>

      {AWARD_GROUPS.map((group) => {
        const list = AWARDS.filter((award) => award.group === group)
        const done = list.filter((award) => profile.awards[award.id] !== undefined).length
        return (
          <section key={group}>
            <div className="section-head">
              <h2>{GROUP_LABEL[group]}</h2>
              <span className="rule" />
              <span className="faint num">
                {done}/{list.length}
              </span>
            </div>
            <p className="faint group-note">{GROUP_NOTE[group]}</p>
            <div className="award-grid">
              {list.map((award) => (
                <AwardTile key={award.id} award={award} profile={profile} />
              ))}
            </div>
          </section>
        )
      })}

      {ladder && (
        <div
          className="sheet-scrim"
          role="dialog"
          aria-modal="true"
          aria-label="Žebříček hodností"
          onClick={() => setLadder(false)}
        >
          <div className="sheet" onClick={(event) => event.stopPropagation()}>
            <div className="sheet-head">
              <h2>Hodnosti</h2>
              {/* Čísla v řádcích jsou věhlas; bez téhle hlavičky by u každého
                  z padesáti řádků muselo stát „věhlasu" znovu. */}
              <span className="label">věhlas</span>
              <button
                type="button"
                className="btn btn-sm btn-ghost"
                onClick={() => setLadder(false)}
              >
                Zavřít
              </button>
            </div>
            <div className="ladder-list">
              {RANKS.map((rank) => {
                const reached = profile.fame >= rank.at
                return (
                  <div className={`ladder-row ${reached ? 'has' : ''}`} key={rank.index}>
                    <RankBadge rank={rank.index} size={38} locked={!reached} />
                    <span className="ladder-name">
                      {rank.index}. {rank.name}
                    </span>
                    <span className="num faint ladder-at">
                      {rank.at.toLocaleString('cs-CZ')}
                    </span>
                  </div>
                )
              })}
            </div>
          </div>
        </div>
      )}
    </>
  )
}
