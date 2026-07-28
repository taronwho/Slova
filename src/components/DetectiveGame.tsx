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
import { inkPrice } from '../game/economy'
import { Confirm } from './Confirm'
import { HintHead, HintPrice } from './HintPanel'
import { StatTile } from './Explain'
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
  /** Inkoust v profilu. Když na nápovědu stačí, zaplatí se jím místo bodů. */
  ink: number
  onSpendInk: (price: number) => void
  onProgress: (state: DetectiveState, finished: boolean) => void
}

const ROWS = ['qwertzuiop', 'asdfghjkl', 'yxcvbnm'].map((row) => row.split(''))

/** Značka zakrytého slova ve stopě — v datech je to obyčejné „[?]". */
const GAP = '[?]'

/** Vysází text stopy a z každé díry udělá viditelné okénko. */
function clueParts(clue: string) {
  return clue.split(GAP).flatMap((piece, i) =>
    i === 0
      ? [<span key={`t${i}`}>{piece}</span>]
      : [
          <mark className="clue-gap" key={`g${i}`} aria-label="zakryté slovo">
            ?
          </mark>,
          <span key={`t${i}`}>{piece}</span>,
        ],
  )
}

/** Totéž po dohrání — do děr se doplní odpověď, ať je vidět, že sedí. */
function filled(clue: string, word: string) {
  return clue.split(GAP).flatMap((piece, i) =>
    i === 0
      ? [<span key={`t${i}`}>{piece}</span>]
      : [<b key={`w${i}`}>{word}</b>, <span key={`t${i}`}>{piece}</span>],
  )
}

export function DetectiveGame({
  puzzle,
  streak,
  dayLabel,
  onFinish,
  onNext,
  onHome,
  onGiveUp,
  resume,
  ink,
  onSpendInk,
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
    const price = inkPrice(DETECTIVE_COST.letter)
    const free = ink >= price
    const result = takeDetectiveHint(state, free)
    if (!result) {
      showFlash('Tady už nápověda nepomůže.', 'warn')
      return
    }
    if (free) onSpendInk(price)
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
            <StatTile
              label="Písmen"
              value={puzzle.word.length}
              tone="accent"
              note={'Jak dlouhé je hledané slovo. Diakritika se nehádá — „u" odhalí i „ů".'}
            />
            <StatTile
              label="Odhaleno"
              value={`${foundLetters}/${needed.size}`}
              tone="gold"
              note="Kolik různých písmen slova už je venku. Jakmile tušíš, o co jde, můžeš slovo rovnou tipnout celé — a čím dřív, tím víc bodů."
            />
            <StatTile
              label="Vedle"
              value={misses}
              tone="warn"
              note="Kolik písmen jsi zkusil mimo. V Detektivovi chyba kolo neukončí, jen ubere body — takže se dá hádat dál."
            />
          </div>
        </div>

        <div className="hints card">
          <HintHead used={state.hintsUsed} ink={ink} />
          <div className="hint-buttons">
            <button type="button" className="btn btn-sm" disabled={over} onClick={hint}>
              <span>Odhal písmeno</span>
              <HintPrice points={DETECTIVE_COST.letter} ink={ink} />
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

        {/* Spis o slově je tady to hlavní, ne dekorace — dostává
            největší plochu a čtenářskou sazbu. */}
        {/* Spis o slově: mluvnická hlavička, význam, a když ho heslo má,
            i zakrytý původ. Význam je to hlavní a má proto plnou sazbu;
            zbytek jsou poznámky na okraji složky. */}
        <blockquote className="clue-card">
          <span className="clue-mark" aria-hidden="true">
            ❝
          </span>
          {puzzle.grammar && <p className="clue-grammar">{puzzle.grammar}</p>}
          <p>{clueParts(puzzle.clue)}</p>
          {puzzle.origin && (
            <p className="clue-origin">
              <span className="clue-label">původ</span>
              {clueParts(puzzle.origin)}
            </p>
          )}
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
          Spis o slově pochází z Wikislovníku. Chybné písmeno tu nikoho
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
        >
          {/* Spis ještě jednou, ale se slovem doplněným do mezer. Uhodnout
              slovo je půlka věci; druhá je vidět, že to sedí — a kdo neuhodl,
              se z toho aspoň něco dozví. Drobným písmem, ať to nepřebije
              samotnou odpověď. */}
          <p className="clue-recap">{filled(puzzle.clue, puzzle.word)}</p>
          {/* A tady teprve celá etymologie, nezakrytá. Během hry by odpověď
              prozradila jediným slovem; po dohrání je to to nejzajímavější,
              co se hráč o slově dozví. */}
          {puzzle.story && (
            <p className="clue-recap clue-story">
              <span className="clue-label">původ</span>
              {puzzle.story}
            </p>
          )}
        </ResultOverlay>
      )}
    </div>
  )
}
