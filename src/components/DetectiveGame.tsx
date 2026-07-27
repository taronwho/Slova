/** Obrazovka režimu ETYMOLOGICKÝ DETEKTIV. */

import { useCallback, useEffect, useMemo, useRef, useState } from 'react'

import {
  createDetectiveState,
  DETECTIVE_COST,
  DETECTIVE_ERROR_TEXT,
  DETECTIVE_MISS_LIMIT,
  guessLetter,
  guessWord,
  isOver,
  isWon,
  missCount,
  neededLetters,
  plain,
  revealed,
  takeDetectiveHint,
  type DetectivePuzzle,
  type DetectiveState,
} from '../game/detective'
import { scoreDetective } from '../game/scoring'
import type { RoundResult } from '../game/types'
import { Confirm } from './Confirm'
import { ResultOverlay } from './ResultOverlay'

interface Props {
  puzzle: DetectivePuzzle
  streak: number
  dayLabel: string
  onFinish: (result: RoundResult) => void
  onNext: () => void
  onHome: () => void
  onGiveUp: () => void
  /** Uložený stav rozehraného kola, když se hráč vrací zpátky do hry. */
  resume?: DetectiveState | null
  /** Nápovědy zdarma z profilu. Když nějaká je, nápověda nestojí body. */
  freeHints: number
  onSpendHint: () => void
  onProgress: (state: DetectiveState, finished: boolean) => void
}

const ROWS = ['qwertzuiop', 'asdfghjkl', 'yxcvbnm'].map((row) => row.split(''))

export function DetectiveGame({
  puzzle,
  streak,
  dayLabel,
  onFinish,
  onNext,
  onHome,
  onGiveUp,
  resume,
  freeHints,
  onSpendHint,
  onProgress,
}: Props) {
  const [state, setState] = useState<DetectiveState>(
    () => resume ?? createDetectiveState(puzzle),
  )
  const [draft, setDraft] = useState('')
  const [typing, setTyping] = useState(false)
  const [flash, setFlash] = useState<{ text: string; tone: string; key: number } | null>(null)
  const [shakeKey, setShakeKey] = useState(0)
  const [done, setDone] = useState(false)
  const [confirmGiveUp, setConfirmGiveUp] = useState(false)
  const reported = useRef(false)

  const misses = missCount(state)
  const won = isWon(state)
  const over = isOver(state)
  const letters = useMemo(() => revealed(state), [state])

  const shown = useRef(puzzle.id)
  useEffect(() => {
    if (shown.current === puzzle.id) return
    shown.current = puzzle.id
    setState(createDetectiveState(puzzle))
    setDraft('')
    setTyping(false)
    setFlash(null)
    setDone(false)
    reported.current = false
  }, [puzzle])

  useEffect(() => {
    onProgress(state, over || done)
  }, [state, over, done, onProgress])

  const breakdown = useMemo(() => scoreDetective(state, streak), [state, streak])

  useEffect(() => {
    if (!over || reported.current) return
    reported.current = true
    setDone(true)
    onFinish({
      mode: 'detective',
      difficulty: puzzle.difficulty,
      puzzleId: puzzle.id,
      score: breakdown.total,
      perfect: breakdown.perfect,
      success: won,
      elapsedMs: (state.finishedAt ?? Date.now()) - state.startedAt,
      hintsUsed: state.hintsUsed,
      detail: {
        word: puzzle.word,
        misses,
        solved: won ? 1 : 0,
        // Uhodnout slovo tipem je jiný výkon než vyklikat ho po písmenech.
        guessed: state.solved ? 1 : 0,
        extra: Math.max(0, DETECTIVE_MISS_LIMIT - misses),
      },
    })
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [over])

  const showFlash = useCallback((text: string, tone: string) => {
    setFlash({ text, tone, key: Date.now() })
  }, [])

  const tryLetter = useCallback(
    (letter: string) => {
      const result = guessLetter(state, letter)
      if (!result.ok) {
        if (result.error !== 'over') showFlash(DETECTIVE_ERROR_TEXT[result.error], 'error')
        return
      }
      setState(result.state)
      if (result.hit) {
        const times = plain(result.state).split(result.letter).length - 1
        showFlash(
          `${result.letter.toUpperCase()} — ${times === 1 ? 'sedí' : `sedí ${times}×`}`,
          'ok',
        )
      } else {
        setShakeKey((n) => n + 1)
        if (navigator.vibrate) navigator.vibrate(30)
        showFlash(`${result.letter.toUpperCase()} ve slově není · −${DETECTIVE_COST.miss}`, 'warn')
      }
    },
    [showFlash, state],
  )

  const submitWord = useCallback(() => {
    const result = guessWord(state, draft)
    if (!result.ok) {
      if (result.error === 'repeat') showFlash('Tohle už jsi zkusil', 'error')
      return
    }
    setDraft('')
    setState(result.state)
    if (result.correct) {
      showFlash('Máš ho!', 'ok')
    } else {
      setShakeKey((n) => n + 1)
      if (navigator.vibrate) navigator.vibrate(40)
      showFlash(`To není ono · −${DETECTIVE_COST.wrongGuess}`, 'error')
    }
  }, [draft, showFlash, state])

  useEffect(() => {
    function onKey(event: KeyboardEvent) {
      if (event.metaKey || event.ctrlKey || event.altKey) return
      // Když hráč píše celý tip, klávesnice patří textovému poli.
      if (typing) return
      if (event.key.length !== 1) return
      const letter = event.key.toLowerCase()
      if (!/[a-záčďéěíňóřšťúůýž]/.test(letter)) return
      event.preventDefault()
      tryLetter(letter)
    }
    window.addEventListener('keydown', onKey)
    return () => window.removeEventListener('keydown', onKey)
  }, [tryLetter, typing])

  function hint() {
    const free = freeHints > 0
    const result = takeDetectiveHint(state, free)
    if (!result) {
      showFlash('Tady už nápověda nepomůže.', 'warn')
      return
    }
    if (free) onSpendHint()
    setState(result.state)
    showFlash(`Odhaleno písmeno ${result.letter.toUpperCase()}`, 'accent')
  }

  const shareText = useMemo(
    () =>
      [
        `SLOVA — Detektiv ${dayLabel}`,
        won ? puzzle.word.toUpperCase() : `${puzzle.word.length} písmen — nerozluštěno`,
        `${misses} vedle · ★ ${breakdown.total}`,
      ].join('\n'),
    [breakdown.total, dayLabel, misses, puzzle.word, won],
  )

  const needed = useMemo(() => neededLetters(puzzle), [puzzle])
  const foundLetters = state.tried.filter((letter) => needed.has(letter)).length

  return (
    <div className="game with-rail">
      <aside className="rail rail-left">
        <div className="hud">
          <div className="stat-row">
            <div className="stat">
              <div className="label">Písmen</div>
              <div className="value num accent">{puzzle.word.length}</div>
            </div>
            <div className="stat">
              <div className="label">Odhaleno</div>
              <div className="value num gold">
                {foundLetters}/{needed.size}
              </div>
            </div>
            <div className="stat">
              <div className="label">Vedle</div>
              <div className="value num warn">{misses}</div>
            </div>
          </div>
        </div>

        <div className="hints card">
          <div className="label">
            Nápovědy · {state.hintsUsed} použito
            {freeHints > 0 && <span className="free-left"> · {freeHints} zdarma</span>}
          </div>
          <div className="hint-buttons">
            <button type="button" className="btn btn-sm" disabled={over} onClick={hint}>
              <span>Odhal písmeno</span>
              <small>{freeHints > 0 ? 'zdarma' : `−${DETECTIVE_COST.letter}`}</small>
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

        {/* Text o původu slova je tady to hlavní, ne dekorace — dostává
            největší plochu a čtenářskou sazbu. */}
        <blockquote className="clue-card">
          <span className="clue-mark" aria-hidden="true">
            ❝
          </span>
          <p>{puzzle.clue}</p>
        </blockquote>

        <div className={`word-slots ${shakeKey ? 'animate-shake' : ''}`} key={shakeKey}
          style={{ ['--slots' as string]: puzzle.word.length }}>
          {letters.map((letter, i) => (
            <span
              className={`slot ${letter ? 'filled' : ''} ${over && !won ? 'missed' : ''}`}
              key={i}
            >
              {letter ?? (over && !won ? puzzle.word[i] : '')}
            </span>
          ))}
        </div>

        {state.guesses.length > 0 && (
          <div className="wrong-guesses">
            {state.guesses.map((guess) => (
              <span className="chip" key={guess}>
                {guess}
              </span>
            ))}
          </div>
        )}
      </div>

      <div className="board-footer">
        {typing ? (
          <div className="guess-row">
            <input
              className="guess-input"
              value={draft}
              autoFocus
              placeholder="Napiš celé slovo"
              onChange={(event) => setDraft(event.target.value)}
              onKeyDown={(event) => {
                if (event.key === 'Enter') submitWord()
                if (event.key === 'Escape') setTyping(false)
              }}
            />
            <button type="button" className="btn btn-primary" onClick={submitWord} disabled={!draft}>
              Tipnout
            </button>
            <button type="button" className="btn btn-ghost" onClick={() => setTyping(false)}>
              Zpět k písmenům
            </button>
          </div>
        ) : (
          <div className="letter-keys">
            {ROWS.map((row, r) => (
              <div className="letter-row" key={r}>
                {row.map((key) => {
                  const tried = state.tried.includes(key)
                  const hit = tried && plain(state).includes(key)
                  return (
                    <button
                      type="button"
                      key={key}
                      className={`letter-key ${hit ? 'hit' : tried ? 'miss' : ''}`}
                      disabled={tried || over}
                      onClick={() => tryLetter(key)}
                    >
                      {key}
                    </button>
                  )
                })}
              </div>
            ))}
          </div>
        )}

        <div
          style={{
            display: 'flex',
            gap: 'var(--sp-2)',
            flexWrap: 'wrap',
            justifyContent: 'center',
          }}
        >
          {!typing && (
            <button
              type="button"
              className="btn btn-primary btn-sm"
              onClick={() => setTyping(true)}
              disabled={over}
            >
              Znám ho — tipnout slovo
            </button>
          )}
          <button
            type="button"
            className="btn btn-sm btn-ghost"
            onClick={() => setConfirmGiveUp(true)}
            disabled={over}
          >
            Vzdát případ
          </button>
        </div>
      </div>

      <aside className="rail rail-right">
        <p className="faint" style={{ fontSize: '0.82rem', lineHeight: 1.55 }}>
          Text o původu slova pochází z Wikislovníku. Chybné písmeno tu nikoho
          nevěší — jen stojí body, takže se dá v klidu přemýšlet. Kdo na slovo
          přijde dřív, může ho tipnout celé a dostane prémii.
        </p>
      </aside>

      {confirmGiveUp && (
        <Confirm
          title="Vzdát případ?"
          body="Kolo skončí nerozluštěné a série se přeruší. Vrátit to nepůjde."
          confirmLabel="Vzdát případ"
          onConfirm={onGiveUp}
          onCancel={() => setConfirmGiveUp(false)}
        />
      )}

      {done && (
        <ResultOverlay
          title={won ? (state.solved ? 'Rozluštěno tipem!' : 'Rozluštěno!') : 'Případ neuzavřen'}
          subtitle={puzzle.word.toUpperCase()}
          breakdown={breakdown}
          shareText={shareText}
          celebrate={won}
          onNext={onNext}
          onHome={onHome}
        />
      )}
    </div>
  )
}
