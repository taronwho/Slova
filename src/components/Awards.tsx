/**
 * Vitrína — hodnost, žebříček padesáti stupňů a mřížka všech ocenění.
 *
 * Zamčené ocenění se neschovává: hráč má vidět, co ho čeká, i jak daleko
 * k tomu má — u met na počet se pod dlaždicí táhne proužek postupu. Schované
 * mety nemotivují, protože o nich nikdo neví.
 *
 * Ocenění je ale přes sto šedesát, a to už je opačný extrém: v takové zdi se
 * ztratí právě to jedno, na které hráč zrovna dosáhne. Žebříčky se proto
 * ukazují **sbalené na získané stupně a jeden další**; kdo chce vidět celou
 * cestu až k Legendě, přepne se na „Vše".
 *
 * Na dlaždici se dá ťuknout a vypíše se, co přesně je potřeba a jak daleko
 * k tomu je — u zamčené mety je to jediná odpověď na otázku „proč tuhle ještě
 * nemám".
 */

import { useState } from 'react'

import {
  AWARDS,
  AWARD_GROUPS,
  GROUP_LABEL,
  GROUP_NOTE,
  visibleAwards,
  type Award,
} from '../game/awards'
import { awardInk } from '../game/economy'
import { RANKS, rankFor } from '../game/ranks'
import { useBackGuard } from '../lib/back'
import type { Profile } from '../lib/storage'
import { AwardArt } from './art/AwardArt'
import { InkMark } from './art/InkMark'
import { RankBadge } from './art/RankBadge'
import { Explain } from './Explain'

interface Props {
  profile: Profile
  onBack: () => void
}

const DATE = new Intl.DateTimeFormat('cs-CZ', { day: 'numeric', month: 'numeric', year: 'numeric' })

function AwardTile({
  award,
  profile,
  onOpen,
}: {
  award: Award
  profile: Profile
  onOpen: (award: Award) => void
}) {
  const at = profile.awards[award.id]
  const has = at !== undefined
  const share = has ? 1 : (award.progress?.(profile) ?? 0)

  return (
    <button
      type="button"
      className={`award ${has ? 'has' : ''}`}
      data-tone={award.tone}
      onClick={() => onOpen(award)}
    >
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
    </button>
  )
}

export function Awards({ profile, onBack }: Props) {
  const progress = rankFor(profile.fame)
  const [ladder, setLadder] = useState(false)
  /** Rozbalené žebříčky — jinak se ukazuje jen nejbližší nezískaný stupeň. */
  const [all, setAll] = useState(false)
  /** Otevřená dlaždice s podrobnostmi. */
  const [detail, setDetail] = useState<Award | null>(null)
  const has = AWARDS.filter((award) => profile.awards[award.id] !== undefined).length

  useBackGuard(ladder, () => setLadder(false))
  useBackGuard(detail !== null, () => setDetail(null))

  const share = detail ? (detail.progress?.(profile) ?? 0) : 0
  const detailAt = detail ? profile.awards[detail.id] : undefined

  return (
    <>
      <div className="section-head" style={{ marginTop: 0 }}>
        <h2>Vitrína</h2>
        <span className="rule" />
        <button type="button" className="btn btn-sm" onClick={onBack}>
          Zpět
        </button>
      </div>

      <button type="button" className="panel rank-card" onClick={() => setLadder(true)}>
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
      </button>

      <div className="award-summary">
        <Explain term="oceneni" className="chip chip-accent">
          Ocenění {has} / {AWARDS.length}
        </Explain>
        <Explain term="vehlas" className="chip">
          {profile.fame.toLocaleString('cs-CZ')} věhlasu
        </Explain>
        <Explain term="inkoust" className="chip chip-ink">
          <InkMark size={11} /> <span className="num">{profile.ink}</span>
        </Explain>
        <Explain term="serie" className="chip">
          Nejlepší série {profile.bestStreak}
        </Explain>
        <Explain term="dny" className="chip">
          Nejvíc dní v řadě {profile.bestDayStreak}
        </Explain>
        <button type="button" className="btn btn-sm" onClick={() => setLadder(true)}>
          Všech {RANKS.length} hodností
        </button>
      </div>

      {/* Sbalené žebříčky jsou výchozí stav. Kdo si chce projít celou cestu
          až k Legendě, přepne — ale nikoho k tomu netlačíme. */}
      <div className="seg seg-wide award-filter">
        <button type="button" aria-pressed={!all} onClick={() => setAll(false)}>
          Na co dosáhneš
        </button>
        <button type="button" aria-pressed={all} onClick={() => setAll(true)}>
          Všech {AWARDS.length}
        </button>
      </div>

      {AWARD_GROUPS.map((group) => {
        const list = AWARDS.filter((award) => award.group === group)
        const done = list.filter((award) => profile.awards[award.id] !== undefined).length
        const shown = all ? list : visibleAwards(list, profile)
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
              {shown.map((award) => (
                <AwardTile
                  key={award.id}
                  award={award}
                  profile={profile}
                  onOpen={setDetail}
                />
              ))}
            </div>
          </section>
        )
      })}

      {detail && (
        <div
          className="sheet-scrim"
          role="dialog"
          aria-modal="true"
          aria-label={detail.title}
          onClick={() => setDetail(null)}
        >
          <div
            className="sheet sheet-term"
            data-tone={detail.tone}
            onClick={(event) => event.stopPropagation()}
          >
            <div className="sheet-head">
              <AwardArt art={detail.art} tier={detail.tier} size={38} />
              <h2>{detail.title}</h2>
              <span className="rule" />
              <button
                type="button"
                className="btn btn-sm btn-ghost"
                onClick={() => setDetail(null)}
              >
                Zavřít
              </button>
            </div>
            <div className="term-body">
              <p>{detail.goal}.</p>
              {detailAt !== undefined ? (
                <p className="faint">Získáno {DATE.format(detailAt)}.</p>
              ) : (
                <>
                  <div className="award-track big" aria-hidden="true">
                    <span style={{ width: `${Math.round(share * 100)}%` }} />
                  </div>
                  <p className="faint">
                    Hotovo {Math.round(share * 100)} %.
                    {detail.tier ? ` ${detail.tier}. stupeň žebříčku.` : ''}
                  </p>
                </>
              )}
              <p className="faint">
                Za tuhle metu padne {awardInk(detail)} inkoustu.
              </p>
            </div>
            <div className="sheet-actions">
              <button
                type="button"
                className="btn btn-sm"
                onClick={() => setDetail(null)}
              >
                Zpátky do vitríny
              </button>
            </div>
          </div>
        </div>
      )}

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
