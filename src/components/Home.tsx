/** Domovská obrazovka — výběr režimu, obtížnosti a denní výzvy. */

import { levelFor } from '../game/scoring'
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
}

const MODES: { id: ModeId; glyph: string; color: string; how: string }[] = [
  {
    id: 'chain',
    glyph: '→',
    color: 'var(--accent)',
    how: 'Měň vždy jedno písmeno tak, aby vzniklo nové české slovo, a dojdi od startu k cíli. Hra ti pořád ukazuje, kolik tahů nejméně zbývá — do neřešitelné pozice tě nepustí.',
  },
  {
    id: 'hive',
    glyph: '⬡',
    color: 'var(--gold)',
    how: 'Sedm písmen, prostřední povinné. Skládej co nejvíc slov od čtyř písmen výš a najdi pangram, který použije všech sedm.',
  },
  {
    id: 'tower',
    glyph: '↑',
    color: 'var(--warn)',
    how: 'Od tří písmen nahoru. V každém patře přibude jedno písmeno a ty z nich všech složíš nové slovo — v jakémkoli pořadí.',
  },
]

const DIFFICULTIES: Difficulty[] = ['easy', 'normal', 'hard']

export function Home({ profile, dayKey, onPlay, onDifficulty, onStats }: Props) {
  const level = levelFor(profile.xp)

  return (
    <>
      <header className="hero">
        <h1>Slova</h1>
        <p>Tři české slovní hry. Každá hádanka je ověřeně dohratelná.</p>
      </header>

      <div className="panel" style={{ marginBottom: 'var(--sp-6)' }}>
        <div className="rank-line">
          <span className="rank">
            {level.title} · úroveň {level.level}
          </span>
          <span className="num muted">
            {profile.xp.toLocaleString('cs-CZ')} XP
          </span>
        </div>
        <div className="xp-bar">
          <span style={{ width: `${(level.into / level.span) * 100}%` }} />
        </div>
        <div
          style={{
            display: 'flex',
            gap: 'var(--sp-2)',
            marginTop: 'var(--sp-4)',
            flexWrap: 'wrap',
          }}
        >
          <span className="chip chip-accent">Série {profile.streak}</span>
          <span className="chip">Nejlepší série {profile.bestStreak}</span>
          <span className="chip">
            Odehráno{' '}
            {profile.stats.chain.played +
              profile.stats.hive.played +
              profile.stats.tower.played}
          </span>
          <button type="button" className="btn btn-sm btn-ghost" onClick={onStats}>
            Statistiky
          </button>
        </div>
      </div>

      <div className="mode-grid">
        {MODES.map((mode) => {
          const dailyKey = `${dayKey}:${mode.id}`
          const dailyDone = profile.dailyDone[dailyKey] !== undefined
          return (
            <article
              className="mode-card"
              key={mode.id}
              style={{ ['--mode-color' as string]: mode.color }}
            >
              <span className="mode-glyph">{mode.glyph}</span>
              <div>
                <h2>{MODE_LABEL[mode.id]}</h2>
                <p className="muted" style={{ fontSize: '0.92rem' }}>
                  {MODE_TAGLINE[mode.id]}
                </p>
              </div>
              <p className="faint" style={{ fontSize: '0.84rem', lineHeight: 1.55 }}>
                {mode.how}
              </p>

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
              </div>

              <div className="mode-meta">
                <button
                  type="button"
                  className="btn btn-primary"
                  onClick={() => onPlay(mode.id, false)}
                >
                  Hrát
                </button>
                <button
                  type="button"
                  className="btn"
                  onClick={() => onPlay(mode.id, true)}
                >
                  {dailyDone ? 'Denní ✓' : 'Denní výzva'}
                </button>
              </div>
            </article>
          )
        })}
      </div>

      <div className="section-head">
        <h2>Jak to funguje</h2>
        <span className="rule" />
      </div>
      <div className="mode-grid">
        <div className="card" style={{ padding: 'var(--sp-5)' }}>
          <h3 style={{ fontSize: '1rem', marginBottom: 'var(--sp-2)' }}>
            Ověřená řešitelnost
          </h3>
          <p className="muted" style={{ fontSize: '0.9rem', lineHeight: 1.6 }}>
            Každá hádanka prošla při sestavení důkazem: u Řetězu se nejkratší
            cesta hledá průchodem grafu, u Voštiny se ukládá kompletní seznam
            řešení, u Věže je ověřený celý řetěz přesmyček.
          </p>
        </div>
        <div className="card" style={{ padding: 'var(--sp-5)' }}>
          <h3 style={{ fontSize: '1rem', marginBottom: 'var(--sp-2)' }}>
            Skoro 249 tisíc slov
          </h3>
          <p className="muted" style={{ fontSize: '0.9rem', lineHeight: 1.6 }}>
            Slovník vznikl z frekvenčního seznamu češtiny profiltrovaného přes
            hunspell, takže neobsahuje vlastní jména ani překlepy. Hádanek je
            přes čtrnáct tisíc.
          </p>
        </div>
        <div className="card" style={{ padding: 'var(--sp-5)' }}>
          <h3 style={{ fontSize: '1rem', marginBottom: 'var(--sp-2)' }}>
            Hraje se i offline
          </h3>
          <p className="muted" style={{ fontSize: '0.9rem', lineHeight: 1.6 }}>
            Žádný server. Data se stahují po malých balíčcích a postup se ukládá
            přímo v prohlížeči.
          </p>
        </div>
      </div>
    </>
  )
}
