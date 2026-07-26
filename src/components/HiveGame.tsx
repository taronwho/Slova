/** Obrazovka režimu VOŠTINA. */

import { useCallback, useEffect, useMemo, useRef, useState } from 'react'

import {
  createHiveState,
  currentScore,
  HIVE_ERROR_TEXT,
  letterSet,
  maxScore,
  rankFor,
  RANKS,
  remainingByLength,
  submitWord,
  takeHiveHint,
  wordScore,
  type HivePuzzle,
  type HiveState,
} from '../game/hive'
import { scoreHive } from '../game/scoring'
import type { RoundResult } from '../game/types'
import { CZECH_LETTERS, fold } from '../lib/czech'
import { Confirm } from './Confirm'
import { FoundWords } from './FoundWords'
import { ResultOverlay } from './ResultOverlay'

interface Props {
  puzzle: HivePuzzle
  streak: number
  dayLabel: string
  onFinish: (result: RoundResult) => void
  onNext: () => void
  onHome: () => void
  /** Uložený stav rozehraného kola, když se hráč vrací zpátky do hry. */
  resume?: HiveState | null
  onProgress: (state: HiveState, finished: boolean) => void
}

/** Souřadnice šesti okrajových buněk plástve v procentech rámu plástve. */
const RING = [
  { left: '33.5%', top: '0%' },
  { left: '67%', top: '16.9%' },
  { left: '67%', top: '50.7%' },
  { left: '33.5%', top: '67.6%' },
  { left: '0%', top: '50.7%' },
  { left: '0%', top: '16.9%' },
]

const CENTER = { left: '33.5%', top: '33.8%' }

export function HiveGame({
  puzzle,
  streak,
  dayLabel,
  onFinish,
  onNext,
  onHome,
  resume,
  onProgress,
}: Props) {
  const [state, setState] = useState<HiveState>(() => resume ?? createHiveState(puzzle))
  const [draft, setDraft] = useState('')
  const [flash, setFlash] = useState<{ text: string; tone: string; key: number } | null>(
    null,
  )
  const [shakeKey, setShakeKey] = useState(0)
  const [done, setDone] = useState(false)
  const [showFound, setShowFound] = useState(false)
  const [confirmEnd, setConfirmEnd] = useState(false)
  const reported = useRef(false)

  const letters = useMemo(() => letterSet(puzzle), [puzzle])
  const max = useMemo(() => maxScore(puzzle), [puzzle])
  const points = currentScore(state)
  const rank = rankFor(points, max)
  const complete = state.found.length >= puzzle.solutions.length

  // Nové kolo — všechno zpět na začátek. Na prvním renderu se přeskočí,
  // jinak by přepsalo stav načtený z rozehraného kola.
  const shown = useRef(puzzle.id)
  useEffect(() => {
    if (shown.current === puzzle.id) return
    shown.current = puzzle.id
    setState(createHiveState(puzzle))
    setDraft('')
    setFlash(null)
    setDone(false)
    reported.current = false
  }, [puzzle])

  // Po každé změně stavu se kolo uloží, aby šlo pokračovat i po zavření hry.
  // Dohrané ani předčasně ukončené kolo se neukládá — nabízet „pokračovat"
  // u něčeho, co je za sebou, nedává smysl.
  useEffect(() => {
    onProgress(state, complete || done)
  }, [state, done, onProgress])

  const breakdown = useMemo(() => scoreHive(state, streak), [state, streak])

  const finishRound = useCallback(() => {
    if (reported.current) return
    reported.current = true
    setDone(true)
    onFinish({
      mode: 'hive',
      difficulty: puzzle.difficulty,
      puzzleId: puzzle.id,
      score: breakdown.total,
      perfect: breakdown.perfect,
      elapsedMs: Date.now() - state.startedAt,
      hintsUsed: state.hintsUsed,
      detail: {
        found: state.found.length,
        total: puzzle.solutions.length,
        rank: rank.name,
        extra: state.found.length,
      },
    })
  }, [breakdown, onFinish, puzzle, rank.name, state])

  useEffect(() => {
    if (complete && !reported.current) finishRound()
  }, [complete, finishRound])

  const showFlash = useCallback((text: string, tone: string) => {
    setFlash({ text, tone, key: Date.now() })
  }, [])

  const submit = useCallback(() => {
    if (!draft) return
    const result = submitWord(state, draft)
    if (!result.ok) {
      showFlash(HIVE_ERROR_TEXT[result.error], 'error')
      setShakeKey((n) => n + 1)
      if (navigator.vibrate) navigator.vibrate(40)
      setDraft('')
      return
    }
    setState(result.state)
    setDraft('')
    if (result.pangram) {
      showFlash(`PANGRAM! ${result.word.toUpperCase()} · +${result.points}`, 'accent')
      if (navigator.vibrate) navigator.vibrate([30, 40, 60])
    } else {
      showFlash(`${result.word.toUpperCase()} · +${result.points}`, 'accent')
    }
  }, [draft, showFlash, state])

  const typeLetter = useCallback(
    (letter: string) => {
      setDraft((prev) => (prev.length < 16 ? prev + letter : prev))
    },
    [],
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
        setState((prev) => ({ ...prev, ring: shuffle(prev.ring) }))
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

  function hint() {
    const result = takeHiveHint(state)
    if (!result) {
      showFlash('Všechna slova už máš.', 'accent')
      return
    }
    setState(result.state)
    showFlash(`Nápověda: ${result.word.toUpperCase()}`, 'warn')
  }

  const remaining = useMemo(() => remainingByLength(state), [state])
  const nextRank = RANKS[rank.index + 1]

  const shareText = useMemo(
    () =>
      [
        `SLOVA — Voština ${dayLabel}`,
        `${puzzle.center.toUpperCase()} · ${puzzle.outer.join('').toUpperCase()}`,
        `${state.found.length}/${puzzle.solutions.length} slov · ${rank.name} · ★ ${breakdown.total}`,
      ].join('\n'),
    [breakdown.total, dayLabel, puzzle, rank.name, state.found.length],
  )

  return (
    <div className="game with-rail">
      <aside className="rail rail-left">
        <div className="hud">
        <div className="panel">
          <div className="rank-line">
            <span className="rank">{rank.name}</span>
            <span className="num muted">
              {points} / {max}
            </span>
          </div>
          <div className="progress-track">
            <div
              className="progress-fill"
              style={{ width: `${max ? Math.min((points / max) * 100, 100) : 0}%` }}
            />
          </div>
          {nextRank && (
            <p className="faint" style={{ fontSize: '0.78rem', marginTop: 'var(--sp-2)' }}>
              Do hodnosti {nextRank.name} zbývá {Math.max(1, Math.ceil(nextRank.at * max) - points)} bodů
            </p>
          )}
        </div>

        <div className="stat-row">
          <div className="stat">
            <div className="label">Slov</div>
            <div className="value num accent">{state.found.length}</div>
          </div>
          <div className="stat">
            <div className="label">Z celku</div>
            <div className="value num">{puzzle.solutions.length}</div>
          </div>
          {/* Návod se dá přeskočit a pak je „Pangramy" jen záhadné číslo.
              Ťuknutím se vysvětlí tam, kde na něj hráč kouká. */}
          <button
            type="button"
            className="stat stat-tap"
            onClick={() =>
              showFlash('Pangram = slovo ze všech sedmi písmen · +7 bodů', 'info')
            }
          >
            <div className="label">Pangramy</div>
            <div className="value num gold">
              {state.found.filter((w) => puzzle.pangrams.includes(w)).length}/
              {puzzle.pangrams.length}
            </div>
          </button>
        </div>

        </div>

        <div className="hints card">
          {/* Nalezená slova jsou na monitoru v pravém sloupci; na telefonu
              se tam nevejdou, tak se otevřou přes tlačítko. */}
          <button
            type="button"
            className="btn btn-sm found-toggle"
            onClick={() => setShowFound(true)}
            disabled={state.found.length === 0}
          >
            <span>Nalezená slova</span>
            <small>{state.found.length}</small>
          </button>
          <div className="label">Kolik slov ještě zbývá</div>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: 'var(--sp-2)' }}>
            {[...remaining.entries()].map(([length, count]) => (
              <span className="chip" key={length}>
                {length} písmen · {count}
              </span>
            ))}
            {remaining.size === 0 && <span className="faint">Máš všechna slova!</span>}
          </div>
        </div>
      </aside>

      <div className="board">
        {flash && (
          <div className={`banner banner-${flash.tone}`} key={flash.key}>
            <span>{flash.text}</span>
          </div>
        )}

        <div className="hive-wrap">
          <div className={`hive-input ${shakeKey ? 'animate-shake' : ''}`} key={shakeKey}>
            {draft.length === 0 && <span className="faint">Piš slovo…</span>}
            {[...draft].map((ch, i) => {
              const folded = fold(ch)
              const isCenter = folded === puzzle.center
              const known = letters.has(folded)
              return (
                <span
                  key={i}
                  className={`ch ${isCenter ? 'center' : ''} ${known ? '' : 'bad'}`}
                >
                  {ch}
                </span>
              )
            })}
            <span className="cursor" />
          </div>

          <div className="hive">
            <button
              type="button"
              className="hex center"
              style={CENTER}
              onClick={() => typeLetter(puzzle.center)}
            >
              {puzzle.center}
            </button>
            {state.ring.map((letter, i) => (
              <button
                type="button"
                key={letter}
                className="hex"
                style={RING[i]}
                onClick={() => typeLetter(letter)}
              >
                {letter}
              </button>
            ))}
          </div>

        </div>
      </div>

        <div className="board-footer">
          <div style={{ display: 'flex', gap: 'var(--sp-2)', flexWrap: 'wrap', justifyContent: 'center' }}>
            <button
              type="button"
              className="btn"
              onClick={() => setDraft((prev) => prev.slice(0, -1))}
            >
              Smazat
            </button>
            <button
              type="button"
              className="btn"
              onClick={() => setState((prev) => ({ ...prev, ring: shuffle(prev.ring) }))}
            >
              Zamíchat
            </button>
            <button type="button" className="btn btn-primary" onClick={submit}>
              Potvrdit
            </button>
          </div>

          <div style={{ display: 'flex', gap: 'var(--sp-2)', flexWrap: 'wrap', justifyContent: 'center' }}>
            <button type="button" className="btn btn-sm" onClick={hint}>
              Nápověda −80
            </button>
            <button
              type="button"
              className="btn btn-sm btn-ghost"
              onClick={() => setConfirmEnd(true)}
            >
              Ukončit plástev
            </button>
          </div>
        </div>

      <aside className="rail rail-right">
        <div className="card" style={{ padding: 'var(--sp-4)' }}>
          <div className="label" style={{ marginBottom: 'var(--sp-3)' }}>
            Nalezená slova
          </div>
          <div className="found-list">
            {[...state.found]
              .sort((a, b) => b.length - a.length || a.localeCompare(b, 'cs'))
              .map((word) => (
                <span
                  key={word}
                  className={`found-word ${puzzle.pangrams.includes(word) ? 'pangram' : ''}`}
                  title={`+${wordScore(puzzle, word)}`}
                >
                  {word}
                </span>
              ))}
            {state.found.length === 0 && (
              <span className="faint">Zatím nic — začni čtyřpísmenným slovem.</span>
            )}
          </div>
        </div>
        <p className="faint" style={{ fontSize: '0.82rem', lineHeight: 1.55 }}>
          Slova musí mít aspoň 4 písmena a vždy obsahovat prostřední písmeno.
          Písmena se smí opakovat. Diakritiku piš normálně — plástev ji skládá.
        </p>
      </aside>

      {showFound && (
        <FoundWords
          words={state.found}
          pangrams={puzzle.pangrams}
          total={puzzle.solutions.length}
          score={(word) => wordScore(puzzle, word)}
          onClose={() => setShowFound(false)}
        />
      )}

      {confirmEnd && (
        <Confirm
          title="Ukončit plástev?"
          body={`Kolo se spočítá tak, jak je — máš ${state.found.length} z ${puzzle.solutions.length} slov. Zbytek už nedohledáš.`}
          confirmLabel="Ukončit"
          onConfirm={() => {
            setConfirmEnd(false)
            finishRound()
          }}
          onCancel={() => setConfirmEnd(false)}
        />
      )}

      {done && (
        <ResultOverlay
          title={complete ? 'Plástev kompletní!' : 'Plástev uzavřena'}
          subtitle={`${state.found.length} z ${puzzle.solutions.length} slov · ${rank.name}`}
          breakdown={breakdown}
          shareText={shareText}
          celebrate={complete}
          onNext={onNext}
          onHome={onHome}
        />
      )}
    </div>
  )
}

function shuffle(items: string[]): string[] {
  const out = [...items]
  for (let i = out.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1))
    ;[out[i], out[j]] = [out[j]!, out[i]!]
  }
  return out
}
