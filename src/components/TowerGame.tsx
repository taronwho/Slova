/** Obrazovka režimu VĚŽ. */

import { useCallback, useEffect, useMemo, useRef, useState } from 'react'

import { scoreTower } from '../game/scoring'
import {
  currentLevel,
  currentLevelIndex,
  isFinished,
  shuffleTiles,
  submitLevel,
  takeTowerHint,
  TOWER_ERROR_TEXT,
  TOWER_HINT_COST,
  type TowerPuzzle,
  type TowerState,
} from '../game/tower'
import { createTowerState } from '../game/tower'
import type { RoundResult } from '../game/types'
import { CZECH_LETTERS } from '../lib/czech'
import { ResultOverlay } from './ResultOverlay'

interface Props {
  puzzle: TowerPuzzle
  streak: number
  dayLabel: string
  onFinish: (result: RoundResult) => void
  onNext: () => void
  onHome: () => void
  onGiveUp: () => void
}

export function TowerGame({
  puzzle,
  streak,
  dayLabel,
  onFinish,
  onNext,
  onHome,
  onGiveUp,
}: Props) {
  const [state, setState] = useState<TowerState>(() => createTowerState(puzzle))
  const [draft, setDraft] = useState('')
  const [flash, setFlash] = useState<{ text: string; tone: string; key: number } | null>(
    null,
  )
  const [shakeKey, setShakeKey] = useState(0)
  const [done, setDone] = useState(false)
  const reported = useRef(false)

  const level = currentLevel(state)
  const levelIndex = currentLevelIndex(state)
  const finished = isFinished(state)

  useEffect(() => {
    setState(createTowerState(puzzle))
    setDraft('')
    setFlash(null)
    setDone(false)
    reported.current = false
  }, [puzzle])

  const breakdown = useMemo(() => scoreTower(state, streak), [state, streak])

  useEffect(() => {
    if (!finished || reported.current) return
    reported.current = true
    setDone(true)
    onFinish({
      mode: 'tower',
      difficulty: puzzle.difficulty,
      puzzleId: puzzle.id,
      score: breakdown.total,
      perfect: breakdown.perfect,
      elapsedMs: (state.finishedAt ?? Date.now()) - state.startedAt,
      hintsUsed: state.hintsUsed,
      detail: {
        floors: state.built.length - 1,
        top: state.built[state.built.length - 1]!.length,
        extra: state.built.length - 1,
      },
    })
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [finished])

  const showFlash = useCallback((text: string, tone: string) => {
    setFlash({ text, tone, key: Date.now() })
  }, [])

  /** Zbývající dlaždice po odečtení už napsaných písmen. */
  const usedCounts = useMemo(() => {
    const counts = new Map<string, number>()
    for (const ch of draft) counts.set(ch, (counts.get(ch) ?? 0) + 1)
    return counts
  }, [draft])

  const tileStates = useMemo(() => {
    const left = new Map(usedCounts)
    return state.tiles.map((letter) => {
      const remaining = left.get(letter) ?? 0
      if (remaining > 0) {
        left.set(letter, remaining - 1)
        return { letter, used: true }
      }
      return { letter, used: false }
    })
  }, [state.tiles, usedCounts])

  const submit = useCallback(() => {
    if (!level) return
    const result = submitLevel(state, draft)
    if (!result.ok) {
      showFlash(TOWER_ERROR_TEXT[result.error], 'error')
      setShakeKey((n) => n + 1)
      if (navigator.vibrate) navigator.vibrate(40)
      return
    }
    setState(result.state)
    setDraft('')
    if (!result.finished) {
      const next = result.state.puzzle.levels[result.state.built.length]
      showFlash(
        `${result.word.toUpperCase()} stojí. Nové písmeno: ${next?.added?.toUpperCase() ?? ''}`,
        'accent',
      )
    }
  }, [draft, level, showFlash, state])

  const typeLetter = useCallback(
    (letter: string) => {
      if (!level) return
      // Písmeno lze použít jen tolikrát, kolikrát je v zásobníku.
      const available = [...level.sig].filter((ch) => ch === letter).length
      const used = [...draft].filter((ch) => ch === letter).length
      if (used >= available) return
      setDraft((prev) => prev + letter)
    },
    [draft, level],
  )

  useEffect(() => {
    function onKey(event: KeyboardEvent) {
      if (event.metaKey || event.ctrlKey || event.altKey) return
      if (event.key === 'Enter') {
        event.preventDefault()
        submit()
      } else if (event.key === 'Backspace') {
        event.preventDefault()
        setDraft((prev) => prev.slice(0, -1))
      } else if (event.key === ' ') {
        event.preventDefault()
        setState((prev) => shuffleTiles(prev))
      } else if (event.key.length === 1) {
        const letter = event.key.toLowerCase()
        if (CZECH_LETTERS.includes(letter)) {
          event.preventDefault()
          typeLetter(letter)
        }
      }
    }
    window.addEventListener('keydown', onKey)
    return () => window.removeEventListener('keydown', onKey)
  }, [submit, typeLetter])

  function hint(kind: 'letter' | 'word') {
    const result = takeTowerHint(state, kind)
    if (!result) return
    setState(result.state)
    setDraft(result.text)
    showFlash(
      kind === 'word' ? `Řešení: ${result.text.toUpperCase()}` : 'Odhalen začátek slova.',
      'warn',
    )
  }

  const shareText = useMemo(() => {
    const height = state.built[state.built.length - 1]!.length
    return [
      `SLOVA — Věž ${dayLabel}`,
      state.built.map((w) => w.toUpperCase()).join(' → '),
      `${height} pater · ★ ${breakdown.total}`,
    ].join('\n')
  }, [breakdown.total, dayLabel, state.built])

  const totalLevels = puzzle.levels.length

  return (
    <div className="game with-rail">
      <aside className="rail rail-left">
        <div className="stat-row">
          <div className="stat">
            <div className="label">Patro</div>
            <div className="value num accent">
              {Math.min(levelIndex + 1, totalLevels)}/{totalLevels}
            </div>
          </div>
          <div className="stat">
            <div className="label">Písmen</div>
            <div className="value num gold">{level ? level.sig.length : '—'}</div>
          </div>
        </div>

        {level?.added && (
          <div className="card" style={{ padding: 'var(--sp-4)', textAlign: 'center' }}>
            <div className="label" style={{ marginBottom: 'var(--sp-2)' }}>
              Nové písmeno
            </div>
            <span className="new-letter" key={levelIndex}>
              {level.added}
            </span>
          </div>
        )}

        <div className="card" style={{ padding: 'var(--sp-4)' }}>
          <div className="label" style={{ marginBottom: 'var(--sp-3)' }}>
            Nápovědy · {state.hintsUsed} použito
          </div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--sp-2)' }}>
            <button
              type="button"
              className="btn btn-sm"
              disabled={finished}
              onClick={() => hint('letter')}
            >
              Odhalit písmeno −{TOWER_HINT_COST.letter}
            </button>
            <button
              type="button"
              className="btn btn-sm"
              disabled={finished}
              onClick={() => hint('word')}
            >
              Celé slovo −{TOWER_HINT_COST.word}
            </button>
          </div>
        </div>
      </aside>

      <div className="board">
        {flash && (
          <div className={`banner banner-${flash.tone}`} key={flash.key}>
            <span>{flash.text}</span>
          </div>
        )}

        <div className="tower">
          {puzzle.levels.map((floor, index) => {
            const word = state.built[index]
            if (word) {
              return (
                <div
                  className={`floor ${index === 0 ? 'base' : 'done'}`}
                  key={index}
                  style={{ animationDelay: `${index * 40}ms` }}
                >
                  {[...word].map((letter, i) => (
                    <div className="tile" key={i}>
                      {letter}
                    </div>
                  ))}
                </div>
              )
            }
            if (index === levelIndex) {
              return (
                <div
                  className={`floor active ${shakeKey ? 'animate-shake' : ''}`}
                  key={`${index}-${shakeKey}`}
                >
                  {Array.from({ length: floor.sig.length }, (_, i) => (
                    <div
                      className={`tile ${draft[i] ? 'changed' : 'empty'}`}
                      key={i}
                    >
                      {draft[i] ?? ''}
                    </div>
                  ))}
                </div>
              )
            }
            return (
              <div className="floor future" key={index}>
                {Array.from({ length: floor.sig.length }, (_, i) => (
                  <div className="tile empty" key={i} />
                ))}
              </div>
            )
          })}
        </div>

        {level && (
          <div className="board-footer">
            <div className="tiles-tray">
              {tileStates.map((tile, i) => (
                <button
                  type="button"
                  key={`${tile.letter}-${i}`}
                  className={`tray-tile ${tile.used ? 'used' : ''} ${
                    tile.letter === level.added ? 'is-new' : ''
                  }`}
                  onClick={() => typeLetter(tile.letter)}
                >
                  {tile.letter}
                </button>
              ))}
            </div>

            <div style={{ display: 'flex', gap: 'var(--sp-2)', flexWrap: 'wrap', justifyContent: 'center' }}>
              <button
                type="button"
                className="btn"
                onClick={() => setDraft((prev) => prev.slice(0, -1))}
                disabled={!draft}
              >
                Smazat
              </button>
              <button
                type="button"
                className="btn"
                onClick={() => setState((prev) => shuffleTiles(prev))}
              >
                Zamíchat
              </button>
              <button
                type="button"
                className="btn btn-primary"
                onClick={submit}
                disabled={draft.length !== level.sig.length}
              >
                Postavit patro
              </button>
              <button type="button" className="btn btn-sm btn-ghost" onClick={onGiveUp}>
                Vzdát věž
              </button>
            </div>
          </div>
        )}
      </div>

      <aside className="rail rail-right">
        <div className="card" style={{ padding: 'var(--sp-4)' }}>
          <div className="label" style={{ marginBottom: 'var(--sp-3)' }}>
            Postavená patra
          </div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 6, fontSize: '0.9rem' }}>
            {state.built.map((word, i) => (
              <div key={i} className="floor-label">
                <span className="num faint">{word.length}</span>
                <span style={{ textTransform: 'uppercase', letterSpacing: '0.06em', color: 'var(--text)' }}>
                  {word}
                </span>
              </div>
            ))}
          </div>
        </div>
        <p className="faint" style={{ fontSize: '0.82rem', lineHeight: 1.55 }}>
          Každé patro použije všechna písmena toho pod ním plus jedno nové —
          v libovolném pořadí. Protože se musí použít všechna, žádná volba
          nemůže věž zablokovat.
        </p>
      </aside>

      {done && (
        <ResultOverlay
          title={breakdown.perfect ? 'Věž bez nápovědy!' : 'Věž stojí'}
          subtitle={state.built.map((w) => w.toUpperCase()).join(' → ')}
          breakdown={breakdown}
          shareText={shareText}
          onNext={onNext}
          onHome={onHome}
        />
      )}
    </div>
  )
}
