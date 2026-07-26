/** Přehled statistik a historie kol. */

import { rankFor } from '../game/ranks'
import { MODE_LABEL, type ModeId } from '../game/types'
import type { Profile } from '../lib/storage'

interface Props {
  profile: Profile
  onBack: () => void
  onReset: () => void
}

const MODES: ModeId[] = ['chain', 'hive', 'tower']

/** Popisky detailů kola — v historii je čte hráč, ne vývojář. */
const DETAIL_LABEL: Record<string, string> = {
  moves: 'tahů',
  par: 'nejkratší cesta',
  found: 'nalezeno slov',
  total: 'z celku',
  rank: 'hodnost',
  floors: 'pater',
  top: 'nejvyšší patro',
}

const EXTRA_LABEL: Record<ModeId, string> = {
  chain: 'Průměr tahů navíc',
  hive: 'Průměr nalezených slov',
  tower: 'Průměr postavených pater',
}

export function Stats({ profile, onBack, onReset }: Props) {
  const progress = rankFor(profile.xp)

  return (
    <>
      <div className="section-head" style={{ marginTop: 0 }}>
        <h2>Statistiky</h2>
        <span className="rule" />
        <button type="button" className="btn btn-sm" onClick={onBack}>
          Zpět
        </button>
      </div>

      <div className="panel" style={{ marginBottom: 'var(--sp-5)' }}>
        <div className="rank-line">
          <span className="rank">
            {progress.rank.name} · hodnost {progress.rank.index}
          </span>
          <span className="num muted">{profile.xp.toLocaleString('cs-CZ')} XP</span>
        </div>
        <div className="xp-bar">
          <span
            style={{ width: `${progress.span ? (progress.into / progress.span) * 100 : 100}%` }}
          />
        </div>
        <p className="faint" style={{ fontSize: '0.8rem', marginTop: 'var(--sp-2)' }}>
          {progress.next
            ? `Do hodnosti ${progress.next.name} zbývá ${(
                progress.span - progress.into
              ).toLocaleString('cs-CZ')} XP`
            : 'Nejvyšší hodnost — dál už se nešplhá'}
        </p>
      </div>

      <div className="stats-grid" style={{ marginBottom: 'var(--sp-5)' }}>
        <div className="stat">
          <div className="label">Kol bez nápovědy</div>
          <div className="value num accent">{profile.counters.noHint}</div>
        </div>
        <div className="stat">
          <div className="label">Nejdelší čistá řada</div>
          <div className="value num accent">{profile.counters.bestNoHintStreak}</div>
        </div>
        <div className="stat">
          <div className="label">Pangramů</div>
          <div className="value num gold">{profile.counters.pangrams}</div>
        </div>
        <div className="stat">
          <div className="label">Celých pláství</div>
          <div className="value num">{profile.counters.hiveFull}</div>
        </div>
        <div className="stat">
          <div className="label">Nejkratších cest</div>
          <div className="value num">{profile.counters.chainPar}</div>
        </div>
        <div className="stat">
          <div className="label">Dostavěných věží</div>
          <div className="value num">{profile.counters.towerFull}</div>
        </div>
        <div className="stat">
          <div className="label">Denních výzev</div>
          <div className="value num">{profile.counters.dailies}</div>
        </div>
      </div>

      {MODES.map((mode) => {
        const stats = profile.stats[mode]
        const average = stats.played > 0 ? stats.totalScore / stats.played : 0
        const extra = stats.played > 0 ? stats.extra / stats.played : 0
        return (
          <section key={mode} style={{ marginBottom: 'var(--sp-5)' }}>
            <div className="section-head" style={{ marginTop: 'var(--sp-4)' }}>
              <h2>{MODE_LABEL[mode]}</h2>
              <span className="rule" />
            </div>
            <div className="stats-grid">
              <div className="stat">
                <div className="label">Odehráno</div>
                <div className="value num">{stats.played}</div>
              </div>
              <div className="stat">
                <div className="label">Nejlepší skóre</div>
                <div className="value num accent">{stats.bestScore.toLocaleString('cs-CZ')}</div>
              </div>
              <div className="stat">
                <div className="label">Průměr</div>
                <div className="value num">{Math.round(average).toLocaleString('cs-CZ')}</div>
              </div>
              <div className="stat">
                <div className="label">Perfektních</div>
                <div className="value num gold">{stats.perfect}</div>
              </div>
              <div className="stat">
                <div className="label">{EXTRA_LABEL[mode]}</div>
                <div className="value num">
                  {stats.played > 0 ? extra.toFixed(1).replace('.', ',') : '—'}
                </div>
              </div>
            </div>
          </section>
        )
      })}

      <div className="section-head">
        <h2>Posledních {Math.min(profile.history.length, 15)} kol</h2>
        <span className="rule" />
      </div>
      <div className="card" style={{ padding: 'var(--sp-4) var(--sp-5)' }}>
        {profile.history.length === 0 && (
          <p className="faint">Zatím žádné dohrané kolo.</p>
        )}
        {profile.history.slice(0, 15).map((round, i) => (
          <div className="history-row" key={i}>
            <span className="chip">{MODE_LABEL[round.mode]}</span>
            <span className="muted" style={{ flex: 1, fontSize: '0.85rem' }}>
              {Object.entries(round.detail)
                .filter(([key]) => key !== 'extra')
                .map(([key, value]) => `${DETAIL_LABEL[key] ?? key} ${value}`)
                .join(' · ')}
            </span>
            {round.perfect && <span className="chip chip-gold">perfektní</span>}
            <span className="num" style={{ fontWeight: 600 }}>
              {round.score.toLocaleString('cs-CZ')}
            </span>
          </div>
        ))}
      </div>

      <div style={{ marginTop: 'var(--sp-6)', textAlign: 'center' }}>
        <button type="button" className="btn btn-sm btn-ghost" onClick={onReset}>
          Vymazat postup
        </button>
      </div>
    </>
  )
}
