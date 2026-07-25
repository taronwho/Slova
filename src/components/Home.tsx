/** Domovská obrazovka — výběr hry nahoře, pod ním profil a pravidla. */

import { useState } from 'react'

import { levelFor } from '../game/scoring'
import { MODE_SUMMARY, TUTORIALS } from '../game/tutorials'
import {
  DIFFICULTY_LABEL,
  MODE_LABEL,
  MODE_TAGLINE,
  type Difficulty,
  type ModeId,
} from '../game/types'
import type { Profile } from '../lib/storage'

interface Props {
  profile: Profile
  dayKey: string
  onPlay: (mode: ModeId, daily: boolean) => void
  onDifficulty: (mode: ModeId, difficulty: Difficulty) => void
  onStats: () => void
  onRules: (mode: ModeId) => void
}

const MODES: { id: ModeId; glyph: string; color: string }[] = [
  { id: 'chain', glyph: '→', color: 'var(--accent)' },
  { id: 'hive', glyph: '⬡', color: 'var(--gold)' },
  { id: 'tower', glyph: '↑', color: 'var(--warn)' },
]

const DIFFICULTIES: Difficulty[] = ['easy', 'normal', 'hard']

const DIFFICULTY_NOTE: Record<ModeId, Record<Difficulty, string>> = {
  chain: {
    easy: '4 písmena, kratší cesty',
    normal: '5 písmen',
    hard: '6 písmen, delší cesty',
  },
  hive: {
    easy: 'menší plástev, do 35 slov',
    normal: 'do 60 slov',
    hard: 'bohatá plástev, až 90 slov',
  },
  tower: {
    easy: 'věž do 6 pater',
    normal: 'věž do 7 pater',
    hard: 'věž až na 8 písmen',
  },
}

export function Home({
  profile,
  dayKey,
  onPlay,
  onDifficulty,
  onStats,
  onRules,
}: Props) {
  const level = levelFor(profile.xp)
  const [openRules, setOpenRules] = useState<ModeId | null>(null)
  const played =
    profile.stats.chain.played + profile.stats.hive.played + profile.stats.tower.played

  return (
    <>
      {/* Výběr hry je první věc na stránce — nikam se kvůli němu neroluje. */}
      <div className="home-head">
        <h1>Vyber si hru</h1>
        <p className="muted">Tři české slovní hry. Každá hádanka jde vždycky dohrát.</p>
      </div>

      <div className="mode-grid">
        {MODES.map((mode) => {
          const dailyDone = profile.dailyDone[`${dayKey}:${mode.id}`] !== undefined
          const isNew = !profile.tutorialSeen[mode.id]
          return (
            <article
              className="mode-card"
              key={mode.id}
              style={{ ['--mode-color' as string]: mode.color }}
            >
              <div className="mode-card-top">
                <span className="mode-glyph">{mode.glyph}</span>
                {isNew && <span className="chip chip-accent">Nové</span>}
              </div>

              <div>
                <h2>{MODE_LABEL[mode.id]}</h2>
                <p className="muted" style={{ fontSize: '0.94rem' }}>
                  {MODE_TAGLINE[mode.id]}
                </p>
              </div>

              <ul className="mode-rules">
                {MODE_SUMMARY[mode.id].map((rule) => (
                  <li key={rule}>{rule}</li>
                ))}
              </ul>

              <div>
                <div className="label" style={{ marginBottom: 'var(--sp-2)' }}>
                  Obtížnost
                </div>
                <div className="seg">
                  {DIFFICULTIES.map((difficulty) => (
                    <button
                      type="button"
                      key={difficulty}
                      aria-pressed={profile.difficulty[mode.id] === difficulty}
                      onClick={() => onDifficulty(mode.id, difficulty)}
                    >
                      {DIFFICULTY_LABEL[difficulty]}
                    </button>
                  ))}
                </div>
                <p className="faint" style={{ fontSize: '0.8rem', marginTop: 'var(--sp-2)' }}>
                  {DIFFICULTY_NOTE[mode.id][profile.difficulty[mode.id]]}
                </p>
              </div>

              <div className="mode-meta">
                <button
                  type="button"
                  className="btn btn-primary"
                  onClick={() => onPlay(mode.id, false)}
                >
                  Hrát
                </button>
                <button type="button" className="btn" onClick={() => onPlay(mode.id, true)}>
                  {dailyDone ? 'Denní ✓' : 'Denní výzva'}
                </button>
                <button
                  type="button"
                  className="btn btn-ghost"
                  onClick={() => onRules(mode.id)}
                >
                  Návod
                </button>
              </div>
            </article>
          )
        })}
      </div>

      {/* Profil až pod výběrem hry — je to doplněk, ne to hlavní. */}
      <div className="panel home-profile">
        <div className="rank-line">
          <span className="rank">
            {level.title} · úroveň {level.level}
          </span>
          <span className="num muted">{profile.xp.toLocaleString('cs-CZ')} XP</span>
        </div>
        <div className="xp-bar">
          <span style={{ width: `${(level.into / level.span) * 100}%` }} />
        </div>
        <div className="home-profile-chips">
          <span className="chip chip-accent">Série {profile.streak}</span>
          <span className="chip">Nejlepší série {profile.bestStreak}</span>
          <span className="chip">Odehráno {played}</span>
          <button type="button" className="btn btn-sm btn-ghost" onClick={onStats}>
            Statistiky
          </button>
        </div>
      </div>

      <div className="section-head">
        <h2>Pravidla podrobně</h2>
        <span className="rule" />
      </div>
      <p className="muted" style={{ marginBottom: 'var(--sp-4)', fontSize: '0.94rem' }}>
        Rozklikni hru a projdi si všechno, co v ní platí. Totéž ti hra ukáže
        i sama, když ji spustíš poprvé.
      </p>

      <div className="rules-list">
        {MODES.map((mode) => {
          const open = openRules === mode.id
          return (
            <div className="rules-item" key={mode.id}>
              <button
                type="button"
                className="rules-toggle"
                aria-expanded={open}
                onClick={() => setOpenRules(open ? null : mode.id)}
              >
                <span className="mode-glyph" style={{ color: mode.color, fontSize: '1.2rem' }}>
                  {mode.glyph}
                </span>
                <span className="rules-title">Jak se hraje {MODE_LABEL[mode.id]}</span>
                <span className={`rules-caret ${open ? 'open' : ''}`} aria-hidden="true">
                  ⌄
                </span>
              </button>

              {open && (
                <div className="rules-body">
                  {TUTORIALS[mode.id].map((step) => (
                    <section key={step.title}>
                      <h3>{step.title}</h3>
                      {step.body.map((paragraph, i) => (
                        <p key={i}>{paragraph.replace(/\*\*/g, '')}</p>
                      ))}
                      {step.key && <p className="rules-key">{step.key.replace(/\*\*/g, '')}</p>}
                    </section>
                  ))}
                  <button
                    type="button"
                    className="btn btn-sm"
                    onClick={() => onRules(mode.id)}
                  >
                    Projít návod s ukázkami
                  </button>
                </div>
              )}
            </div>
          )
        })}
      </div>
    </>
  )
}
