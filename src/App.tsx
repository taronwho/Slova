/** Kořen aplikace — téma, profil, výběr hádanek a přepínání obrazovek. */

import { useCallback, useEffect, useMemo, useRef, useState } from 'react'

import {
  loadChain,
  loadHive,
  loadDetective,
  loadTetris,
  loadGallows,
  loadHiveIndex,
  loadTower,
  loadTowerIndex,
  pickUnseen,
  type ChainBundle,
} from './app/data'
import { AwardPopup, type Gained } from './components/AwardPopup'
import { Awards } from './components/Awards'
import { InkMark } from './components/art/InkMark'
import { RankBadge } from './components/art/RankBadge'
import { ChainGame } from './components/ChainGame'
import { DetectiveGame } from './components/DetectiveGame'
import { GallowsGame } from './components/GallowsGame'
import { HiveGame } from './components/HiveGame'
import { Home } from './components/Home'
import { Splash } from './components/Splash'
import { Stats } from './components/Stats'
import { Tutorial } from './components/Tutorial'
import { TetrisGame } from './components/TetrisGame'
import { TowerGame } from './components/TowerGame'
import type { ChainPuzzle, ChainState } from './game/chain'
import type { DetectivePuzzle, DetectiveState } from './game/detective'
import type { GallowsPuzzle, GallowsState } from './game/gallows'
import type { HivePuzzle, HiveState } from './game/hive'
import { RANKS, rankFor } from './game/ranks'
import type { TetrisPuzzle, TetrisState } from './game/tetris'
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
  spendInk,
  type Profile,
  type SavedRound,
  type SavedRounds,
} from './lib/storage'

type View =
  | { kind: 'home' }
  | { kind: 'stats' }
  | { kind: 'awards' }
  | { kind: 'game'; mode: ModeId; daily: boolean; nonce: number }

interface Loaded {
  chain?: { bundle: ChainBundle; puzzle: ChainPuzzle }
  hive?: HivePuzzle
  tower?: TowerPuzzle
  gallows?: GallowsPuzzle
  detective?: DetectivePuzzle
  tetris?: TetrisPuzzle
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
  /** Co hráči za poslední kolo přibylo — ukáže se nad výsledkem. */
  const [gained, setGained] = useState<Gained | null>(null)

  const rank = rankFor(profile.fame)
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

  /**
   * Co hráči přibylo, se pozná až na hotovém profilu.
   *
   * Ocenění uděluje `recordRound` uvnitř aktualizace stavu a ta musí zůstat
   * čistá — oznámení se proto odvodí až tady, porovnáním s poslední viděnou
   * podobou. První průchod jen zapamatuje, co profil má, aby po zapnutí hry
   * nevyskočilo všechno, co hráč nasbíral dřív.
   */
  const seenAwards = useRef<Set<string> | null>(null)
  const seenRank = useRef(0)
  useEffect(() => {
    const rank = rankFor(profile.fame).rank.index
    const ids = Object.keys(profile.awards)
    if (seenAwards.current === null) {
      seenAwards.current = new Set(ids)
      seenRank.current = rank
      return
    }
    const fresh = ids.filter((id) => !seenAwards.current!.has(id))
    const promoted = rank > seenRank.current
    seenAwards.current = new Set(ids)
    seenRank.current = rank
    if (fresh.length > 0 || promoted) {
      setGained({ rank: promoted ? rank : null, awards: fresh })
    }
  }, [profile.awards, profile.fame])

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
        } else if (mode === 'detective') {
          const words = await loadDetective()
          const pool = words.filter((w) => w.difficulty === difficulty)
          const entries = pool.length > 0 ? pool : words
          const entry = daily
            ? entries[Math.floor(random() * entries.length)]!
            : pickUnseen(entries, (e) => e.id, profile.seen.detective, random)
          setLoaded({ detective: entry })
        } else if (mode === 'tetris') {
          const packs = await loadTetris()
          const pool = packs.filter((p) => p.difficulty === difficulty)
          const entries = pool.length > 0 ? pool : packs
          const entry = daily
            ? entries[Math.floor(random() * entries.length)]!
            : pickUnseen(entries, (e) => e.id, profile.seen.tetris, random)
          setLoaded({ tetris: entry })
        } else if (mode === 'gallows') {
          const words = await loadGallows()
          const pool = words.filter((w) => w.difficulty === difficulty)
          const entries = pool.length > 0 ? pool : words
          const entry = daily
            ? entries[Math.floor(random() * entries.length)]!
            : pickUnseen(entries, (e) => e.id, profile.seen.gallows, random)
          setLoaded({ gallows: entry })
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
        } else if (round.mode === 'detective') {
          setLoaded({ detective: (round.state as DetectiveState).puzzle })
        } else if (round.mode === 'tetris') {
          setLoaded({ tetris: (round.state as TetrisState).puzzle })
        } else if (round.mode === 'gallows') {
          setLoaded({ gallows: (round.state as GallowsState).puzzle })
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
        const isDaily = view.kind === 'game' && view.daily
        const next = recordRound(previous, result, dayKey, isDaily)
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

  const spendInkOn = useCallback(
    (price: number) => updateProfile((profile) => spendInk(profile, price)),
    [updateProfile],
  )

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
            <span className="chip chip-mode">{MODE_LABEL[view.mode]}</span>
            {view.daily && <span className="chip chip-gold">Denní {dayLabel}</span>}
            <button
              type="button"
              className="btn btn-sm btn-ghost"
              onClick={() => setTutorial({ mode: view.mode, pending: false })}
              aria-label="Pravidla"
            >
              <span className="wide-only">Pravidla</span>
              <span className="narrow-only" aria-hidden="true">
                ?
              </span>
            </button>
          </>
        )}
        <span className="topbar-spacer" />
        {/* Profil v liště: odznak a pořadí hodnosti jsou vidět na každé
            obrazovce, i uprostřed hry. Jméno hodnosti se vejde jen na širší
            displej, číslo drží vždycky — je to ta věc, která roste. */}
        <button
          type="button"
          className="profile-chip"
          onClick={() => setView({ kind: 'awards' })}
          title={`${rank.rank.name} — ${rank.rank.index}. hodnost z ${RANKS.length}`}
          aria-label={`Profil: ${rank.rank.name}, hodnost ${rank.rank.index}`}
        >
          <RankBadge rank={rank.rank.index} size={20} compact />
          <span className="profile-rank num">{rank.rank.index}</span>
          <span className="profile-rank profile-rank-name">{rank.rank.name}</span>
        </button>
        {/* Kalamář. Hráč se podle něj rozhoduje, jestli si nápovědu vzít,
            takže musí být vidět i uprostřed hry. */}
        {profile.ink > 0 && (
          <span className="chip chip-ink" title={`${profile.ink} inkoustu na nápovědy`}>
            <InkMark size={11} />
            <span className="num">{profile.ink}</span>
          </span>
        )}
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
            dayLabel={dayLabel}
            onPlay={startRound}
            onDifficulty={(mode, difficulty: Difficulty) =>
              updateProfile((previous) => ({
                ...previous,
                difficulty: { ...previous.difficulty, [mode]: difficulty },
              }))
            }
            onStats={() => setView({ kind: 'stats' })}
            onAwards={() => setView({ kind: 'awards' })}
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

        {!loading && view.kind === 'awards' && <Awards profile={profile} onBack={goHome} />}

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
            ink={profile.ink}
            onSpendInk={spendInkOn}
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
            ink={profile.ink}
            onSpendInk={spendInkOn}
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
            ink={profile.ink}
            onSpendInk={spendInkOn}
            onProgress={(state, finished) =>
              keepProgress('tower', state.puzzle.id, state.puzzle.difficulty, state, finished)
            }
          />
        )}

        {/* Nad výsledkem kola: nejdřív skóre, pak co za něj přibylo. */}
        {gained && !splash && <AwardPopup gained={gained} onClose={() => setGained(null)} />}

        {!loading && view.kind === 'game' && view.mode === 'gallows' && loaded.gallows && (
          <GallowsGame
            key={`${loaded.gallows.id}-${view.nonce}`}
            puzzle={loaded.gallows}
            streak={profile.streak}
            dayLabel={view.daily ? dayLabel : ''}
            onFinish={finishRound}
            onNext={() => startRound('gallows', false)}
            onHome={goHome}
            onGiveUp={giveUp}
            resume={resume as GallowsState | null}
            ink={profile.ink}
            onSpendInk={spendInkOn}
            onProgress={(state, finished) =>
              keepProgress('gallows', state.puzzle.id, state.puzzle.difficulty, state, finished)
            }
          />
        )}

        {!loading && view.kind === 'game' && view.mode === 'tetris' && loaded.tetris && (
          <TetrisGame
            key={`${loaded.tetris.id}-${view.nonce}`}
            puzzle={loaded.tetris}
            streak={profile.streak}
            dayLabel={view.daily ? dayLabel : ''}
            onFinish={finishRound}
            onNext={() => startRound('tetris', false)}
            onHome={goHome}
            resume={resume as TetrisState | null}
            ink={profile.ink}
            onSpendInk={spendInkOn}
            onProgress={(state, finished) =>
              keepProgress('tetris', state.puzzle.id, state.puzzle.difficulty, state, finished)
            }
          />
        )}

        {!loading && view.kind === 'game' && view.mode === 'detective' && loaded.detective && (
          <DetectiveGame
            key={`${loaded.detective.id}-${view.nonce}`}
            puzzle={loaded.detective}
            streak={profile.streak}
            dayLabel={view.daily ? dayLabel : ''}
            onFinish={finishRound}
            onNext={() => startRound('detective', false)}
            onHome={goHome}
            onGiveUp={giveUp}
            resume={resume as DetectiveState | null}
            ink={profile.ink}
            onSpendInk={spendInkOn}
            onProgress={(state, finished) =>
              keepProgress('detective', state.puzzle.id, state.puzzle.difficulty, state, finished)
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
