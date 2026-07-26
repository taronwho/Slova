/** Kořen aplikace — téma, profil, výběr hádanek a přepínání obrazovek. */

import { useCallback, useEffect, useMemo, useState } from 'react'

import {
  loadChain,
  loadHive,
  loadHiveIndex,
  loadTower,
  loadTowerIndex,
  pickUnseen,
  type ChainBundle,
} from './app/data'
import { ChainGame } from './components/ChainGame'
import { HiveGame } from './components/HiveGame'
import { Home } from './components/Home'
import { Splash } from './components/Splash'
import { Stats } from './components/Stats'
import { Tutorial } from './components/Tutorial'
import { TowerGame } from './components/TowerGame'
import type { ChainPuzzle, ChainState } from './game/chain'
import type { HivePuzzle, HiveState } from './game/hive'
import type { TowerPuzzle, TowerState } from './game/tower'
import { MODE_LABEL, type Difficulty, type ModeId, type RoundResult } from './game/types'
import { useBackGuard } from './lib/back'
import { dayNumber, hashSeed, mulberry32, todayKey } from './lib/rng'
import {
  breakStreak,
  emptyProfile,
  loadProfile,
  loadRounds,
  recordRound,
  saveProfile,
  saveRounds,
  type Profile,
  type SavedRound,
  type SavedRounds,
} from './lib/storage'

type View =
  | { kind: 'home' }
  | { kind: 'stats' }
  | { kind: 'game'; mode: ModeId; daily: boolean; nonce: number }

interface Loaded {
  chain?: { bundle: ChainBundle; puzzle: ChainPuzzle }
  hive?: HivePuzzle
  tower?: TowerPuzzle
}

export default function App() {
  const [profile, setProfile] = useState<Profile>(() => loadProfile())
  const [view, setView] = useState<View>({ kind: 'home' })
  const [loaded, setLoaded] = useState<Loaded>({})
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  /** Otevřený návod. `pending` = otevřel se sám před první hrou režimu. */
  const [tutorial, setTutorial] = useState<{ mode: ModeId; pending: boolean } | null>(
    null,
  )
  /** Rozehraná kola, jedno od každého režimu — nabídnou se na úvodní obrazovce. */
  const [saved, setSaved] = useState<SavedRounds>(() => loadRounds())
  /** Stav, se kterým se má hra nastartovat, když hráč klikne na Pokračovat. */
  const [resume, setResume] = useState<unknown>(null)
  /** Úvodní značka. Hra se pod ní mezitím načítá, takže nikoho nezdržuje. */
  const [splash, setSplash] = useState(true)

  const dayKey = todayKey()
  const dayLabel = `#${dayNumber()}`

  useEffect(() => {
    saveProfile(profile)
  }, [profile])

  // Téma
  useEffect(() => {
    const root = document.documentElement
    if (profile.theme === 'system') root.removeAttribute('data-theme')
    else root.setAttribute('data-theme', profile.theme)
  }, [profile.theme])

  const updateProfile = useCallback((patch: (previous: Profile) => Profile) => {
    setProfile(patch)
  }, [])

  /** Načte hádanku pro daný režim. Denní výzva je deterministická podle data. */
  const startRound = useCallback(
    async (mode: ModeId, daily: boolean) => {
      setLoading(true)
      setError(null)
      setResume(null)
      const difficulty = profile.difficulty[mode]
      const random = daily
        ? mulberry32(hashSeed(`${dayKey}:${mode}`))
        : mulberry32((Math.random() * 2 ** 32) >>> 0)

      try {
        if (mode === 'chain') {
          const bundle = await loadChain(difficulty)
          const puzzle = daily
            ? bundle.puzzles[Math.floor(random() * bundle.puzzles.length)]!
            : pickUnseen(bundle.puzzles, (p) => p.id, profile.seen.chain, random)
          setLoaded({ chain: { bundle, puzzle } })
        } else if (mode === 'hive') {
          const index = await loadHiveIndex()
          const pool = index.hives.filter((h) => h.difficulty === difficulty)
          const entries = pool.length > 0 ? pool : index.hives
          const entry = daily
            ? entries[Math.floor(random() * entries.length)]!
            : pickUnseen(entries, (e) => e.id, profile.seen.hive, random)
          setLoaded({ hive: await loadHive(entry) })
        } else {
          const index = await loadTowerIndex()
          const pool = index.towers.filter((t) => t.difficulty === difficulty)
          const entries = pool.length > 0 ? pool : index.towers
          const entry = daily
            ? entries[Math.floor(random() * entries.length)]!
            : pickUnseen(entries, (e) => e.id, profile.seen.tower, random)
          setLoaded({ tower: await loadTower(entry) })
        }
        setView((previous) => ({
          kind: 'game',
          mode,
          daily,
          nonce: previous.kind === 'game' ? previous.nonce + 1 : 1,
        }))
        setSaved((previous) => {
          const { [mode]: _dropped, ...rest } = previous
          saveRounds(rest)
          return rest
        })
        // Při prvním spuštění režimu se návod otevře sám nad rozehranou hrou.
        if (!profile.tutorialSeen[mode]) setTutorial({ mode, pending: true })
      } catch (cause) {
        setError(cause instanceof Error ? cause.message : 'Data se nepodařilo načíst')
      } finally {
        setLoading(false)
      }
    },
    [dayKey, profile.difficulty, profile.seen, profile.tutorialSeen],
  )

  /** Obnoví kolo přerušené odchodem do menu nebo zavřením hry. */
  const resumeRound = useCallback(
    async (round: SavedRound) => {
      setLoading(true)
      setError(null)
      try {
        if (round.mode === 'chain') {
          const state = round.state as ChainState
          const bundle = await loadChain(round.difficulty)
          setLoaded({ chain: { bundle, puzzle: state.puzzle } })
        } else if (round.mode === 'hive') {
          setLoaded({ hive: (round.state as HiveState).puzzle })
        } else {
          setLoaded({ tower: (round.state as TowerState).puzzle })
        }
        setResume(round.state)
        setView((previous) => ({
          kind: 'game',
          mode: round.mode,
          daily: round.daily,
          nonce: previous.kind === 'game' ? previous.nonce + 1 : 1,
        }))
      } catch (cause) {
        setError(cause instanceof Error ? cause.message : 'Kolo se nepodařilo obnovit')
        setSaved((previous) => {
          const { [round.mode]: _dropped, ...rest } = previous
          saveRounds(rest)
          return rest
        })
      } finally {
        setLoading(false)
      }
    },
    [],
  )

  /**
   * Průběžné ukládání. Volá se po každém tahu, takže se kolo dá dohrát i po
   * návratu do menu nebo po zavření prohlížeče. Dohrané kolo se maže —
   * nabízet „pokračovat" u něčeho hotového nedává smysl.
   */
  const keepProgress = useCallback(
    (mode: ModeId, puzzleId: string, difficulty: Difficulty, state: unknown, over: boolean) => {
      const daily = view.kind === 'game' ? view.daily : false
      setSaved((previous) => {
        let next: SavedRounds
        if (over) {
          const { [mode]: _dropped, ...rest } = previous
          next = rest
        } else {
          const round: SavedRound = {
            mode,
            daily,
            difficulty,
            puzzleId,
            state,
            savedAt: Date.now(),
          }
          next = { ...previous, [mode]: round }
        }
        saveRounds(next)
        return next
      })
    },
    [view],
  )

  const finishRound = useCallback(
    (result: RoundResult) => {
      setSaved((previous) => {
        const { [result.mode]: _dropped, ...rest } = previous
        saveRounds(rest)
        return rest
      })
      updateProfile((previous) => {
        const next = recordRound(previous, result, dayKey)
        const isDaily = view.kind === 'game' && view.daily
        if (!isDaily) return next
        return {
          ...next,
          dailyDone: { ...next.dailyDone, [`${dayKey}:${result.mode}`]: result.score },
        }
      })
    },
    [dayKey, updateProfile, view],
  )

  const giveUp = useCallback(() => {
    setSaved((previous) => {
      const mode = view.kind === 'game' ? view.mode : null
      if (!mode) return previous
      const { [mode]: _dropped, ...rest } = previous
      saveRounds(rest)
      return rest
    })
    updateProfile(breakStreak)
    setView({ kind: 'home' })
  }, [updateProfile, view])

  const goHome = useCallback(() => setView({ kind: 'home' }), [])

  const closeTutorial = useCallback(() => {
    setTutorial((open) => {
      if (open) {
        updateProfile((previous) => ({
          ...previous,
          tutorialSeen: { ...previous.tutorialSeen, [open.mode]: true },
        }))
      }
      return null
    })
  }, [updateProfile])

  // Systémové zpět zavírá vrstvy odshora dolů: nejdřív návod, pak hru.
  // Až na domovské obrazovce se chová normálně a hru opustí.
  useBackGuard(view.kind !== 'home', goHome)
  useBackGuard(tutorial !== null, closeTutorial)

  const themeButton = useMemo(() => {
    const order: Profile['theme'][] = ['system', 'light', 'dark']
    const icons: Record<Profile['theme'], string> = {
      system: '◐',
      light: '☀',
      dark: '☾',
    }
    const labels: Record<Profile['theme'], string> = {
      system: 'Podle systému',
      light: 'Světlé',
      dark: 'Tmavé',
    }
    const next = order[(order.indexOf(profile.theme) + 1) % order.length]!
    return (
      <button
        type="button"
        className="btn btn-sm btn-ghost"
        title={`Téma: ${labels[profile.theme]}`}
        aria-label={`Téma: ${labels[profile.theme]}. Přepnout na ${labels[next]}`}
        onClick={() => updateProfile((previous) => ({ ...previous, theme: next }))}
      >
        {icons[profile.theme]}
      </button>
    )
  }, [profile.theme, updateProfile])

  return (
    <div
      className={`shell ${view.kind === 'game' ? 'playing' : ''}`}
      data-mode={view.kind === 'game' ? view.mode : undefined}
    >
      <header className="topbar">
        <button
          type="button"
          className="brand"
          onClick={goHome}
          style={{ color: 'inherit' }}
        >
          Sl<span className="mark">o</span>va
          <span className="brand-triad" aria-hidden="true">
            <i style={{ background: 'var(--mode-chain)' }} />
            <i style={{ background: 'var(--mode-hive)' }} />
            <i style={{ background: 'var(--mode-tower)' }} />
          </span>
        </button>
        {view.kind === 'game' && (
          <>
            {/* Zpět do menu. Rozehrané kolo se tím neztrácí — na úvodní
                obrazovce se nabídne k pokračování. */}
            <button
              type="button"
              className="btn btn-sm btn-ghost btn-back"
              onClick={goHome}
              aria-label="Zpět do menu"
            >
              <span aria-hidden="true">←</span> Menu
            </button>
            <span className="chip">{MODE_LABEL[view.mode]}</span>
            {view.daily && <span className="chip chip-gold">Denní {dayLabel}</span>}
            <button
              type="button"
              className="btn btn-sm btn-ghost"
              onClick={() => setTutorial({ mode: view.mode, pending: false })}
            >
              Pravidla
            </button>
          </>
        )}
        <span className="topbar-spacer" />
        <span className="chip chip-accent chip-streak">
          <span className="chip-label">Série</span>
          <span className="num">{profile.streak}</span>
        </span>
        {themeButton}
      </header>

      <main className="main">
        {error && (
          <div className="banner banner-error" style={{ marginBottom: 'var(--sp-4)' }}>
            <span>{error}</span>
            <span className="banner-actions">
              <button type="button" className="btn btn-sm" onClick={goHome}>
                Domů
              </button>
            </span>
          </div>
        )}

        {loading && (
          <div className="loading">
            <span className="spinner" />
            <span>Načítám hádanku…</span>
          </div>
        )}

        {!loading && view.kind === 'home' && (
          <Home
            profile={profile}
            dayKey={dayKey}
            onPlay={startRound}
            onDifficulty={(mode, difficulty: Difficulty) =>
              updateProfile((previous) => ({
                ...previous,
                difficulty: { ...previous.difficulty, [mode]: difficulty },
              }))
            }
            onStats={() => setView({ kind: 'stats' })}
            onRules={(mode) => setTutorial({ mode, pending: false })}
            saved={saved}
            onResume={(mode) => {
              const round = saved[mode]
              if (round) void resumeRound(round)
            }}
          />
        )}

        {!loading && view.kind === 'stats' && (
          <Stats
            profile={profile}
            onBack={goHome}
            onReset={() => setProfile(emptyProfile())}
          />
        )}

        {!loading && view.kind === 'game' && view.mode === 'chain' && loaded.chain && (
          <ChainGame
            key={`${loaded.chain.puzzle.id}-${view.nonce}`}
            graph={loaded.chain.bundle.graph}
            puzzle={loaded.chain.puzzle}
            streak={profile.streak}
            dayLabel={view.daily ? dayLabel : ''}
            onFinish={finishRound}
            onNext={() => startRound('chain', false)}
            onHome={goHome}
            onGiveUp={giveUp}
            resume={resume as ChainState | null}
            onProgress={(state, finished) =>
              keepProgress('chain', state.puzzle.id, state.puzzle.difficulty, state, finished)
            }
          />
        )}

        {!loading && view.kind === 'game' && view.mode === 'hive' && loaded.hive && (
          <HiveGame
            key={`${loaded.hive.id}-${view.nonce}`}
            puzzle={loaded.hive}
            streak={profile.streak}
            dayLabel={view.daily ? dayLabel : ''}
            onFinish={finishRound}
            onNext={() => startRound('hive', false)}
            onHome={goHome}
            resume={resume as HiveState | null}
            onProgress={(state, finished) =>
              keepProgress('hive', state.puzzle.id, state.puzzle.difficulty, state, finished)
            }
          />
        )}

        {!loading && view.kind === 'game' && view.mode === 'tower' && loaded.tower && (
          <TowerGame
            key={`${loaded.tower.id}-${view.nonce}`}
            puzzle={loaded.tower}
            streak={profile.streak}
            dayLabel={view.daily ? dayLabel : ''}
            onFinish={finishRound}
            onNext={() => startRound('tower', false)}
            onHome={goHome}
            onGiveUp={giveUp}
            resume={resume as TowerState | null}
            onProgress={(state, finished) =>
              keepProgress('tower', state.puzzle.id, state.puzzle.difficulty, state, finished)
            }
          />
        )}

        {splash && <Splash onDone={() => setSplash(false)} />}

        {tutorial && (
          <Tutorial
            mode={tutorial.mode}
            onClose={closeTutorial}
            finishLabel={tutorial.pending ? 'Začít hrát' : 'Zavřít'}
          />
        )}
      </main>
    </div>
  )
}
