/** Obrazovka režimu ŠIBENICE. */

import { useCallback, useEffect, useMemo, useRef, useState } from 'react'

import {
  createGallowsState,
  GALLOWS_ERROR_TEXT,
  GALLOWS_HINT_COST,
  GALLOWS_LIVES,
  guessLetter,
  isLost,
  isOver,
  isWon,
  neededLetters,
  plain,
  revealed,
  takeGallowsHint,
  wrongCount,
  type GallowsHintKind,
  type GallowsPuzzle,
  type GallowsState,
} from '../game/gallows'
import { inkPrice } from '../game/economy'
import { HintHead, HintPrice } from './HintPanel'
import { StatTile } from './Explain'
import { scoreGallows } from '../game/scoring'
import type { RoundResult } from '../game/types'
import { Confirm } from './Confirm'
import { Gallows } from './art/Gallows'
import { ResultOverlay } from './ResultOverlay'

interface Props {
  puzzle: GallowsPuzzle
  streak: number
  dayLabel: string
  onFinish: (result: RoundResult) => void
  onNext: () => void
  onHome: () => void
  onGiveUp: () => void
  /** Uložený stav rozehraného kola, když se hráč vrací zpátky do hry. */
  resume?: GallowsState | null
  /** Inkoust v profilu. Když na nápovědu stačí, zaplatí se jím místo bodů. */
  ink: number
  onSpendInk: (price: number) => void
  onProgress: (state: GallowsState, finished: boolean) => void
}

/** Rozložení kláves — tři řady jako na skutečné klávesnici. */
const ROWS = ['qwertzuiop', 'asdfghjkl', 'yxcvbnm'].map((row) => row.split(''))

export function GallowsGame({
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
  const [state, setState] = useState<GallowsState>(() => resume ?? createGallowsState(puzzle))
  const [flash, setFlash] = useState<{ text: string; tone: string; key: number } | null>(null)
  const [shakeKey, setShakeKey] = useState(0)
  const [done, setDone] = useState(false)
  const [confirmGiveUp, setConfirmGiveUp] = useState(false)
  const reported = useRef(false)

  const wrong = wrongCount(state)
  const won = isWon(state)
  const lost = isLost(state)
  const over = isOver(state)
  const letters = useMemo(() => revealed(state), [state])

  // Nové kolo — všechno zpět na začátek. Na prvním renderu se přeskočí,
  // jinak by přepsalo stav načtený z rozehraného kola.
  const shown = useRef(puzzle.id)
  useEffect(() => {
    if (shown.current === puzzle.id) return
    shown.current = puzzle.id
    setState(createGallowsState(puzzle))
    setFlash(null)
    setDone(false)
    reported.current = false
  }, [puzzle])

  useEffect(() => {
    onProgress(state, over || done)
  }, [state, over, done, onProgress])

  const breakdown = useMemo(() => scoreGallows(state, streak), [state, streak])

  useEffect(() => {
    if (!over || reported.current) return
    reported.current = true
    setDone(true)
    onFinish({
      mode: 'gallows',
      difficulty: puzzle.difficulty,
      puzzleId: puzzle.id,
      score: breakdown.total,
      perfect: breakdown.perfect,
      success: won,
      elapsedMs: (state.finishedAt ?? Date.now()) - state.startedAt,
      hintsUsed: state.hintsUsed,
      detail: {
        word: puzzle.word,
        wrong,
        // Pro ocenění: uhodnuté slovo je něco jiného než viselec.
        solved: won ? 1 : 0,
        lives: Math.max(0, GALLOWS_LIVES - wrong),
        extra: Math.max(0, GALLOWS_LIVES - wrong),
      },
    })
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [over])

  const showFlash = useCallback((text: string, tone: string) => {
    setFlash({ text, tone, key: Date.now() })
  }, [])

  const guess = useCallback(
    (letter: string) => {
      const result = guessLetter(state, letter)
      if (!result.ok) {
        if (result.error !== 'over') showFlash(GALLOWS_ERROR_TEXT[result.error], 'error')
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
        if (navigator.vibrate) navigator.vibrate(40)
        showFlash(`${result.letter.toUpperCase()} ve slově není`, 'error')
      }
    },
    [showFlash, state],
  )

  useEffect(() => {
    function onKey(event: KeyboardEvent) {
      if (event.metaKey || event.ctrlKey || event.altKey) return
      if (event.key.length !== 1) return
      const letter = event.key.toLowerCase()
      if (!/[a-záčďéěíňóřšťúůýž]/.test(letter)) return
      event.preventDefault()
      guess(letter)
    }
    window.addEventListener('keydown', onKey)
    return () => window.removeEventListener('keydown', onKey)
  }, [guess])

  function hint(kind: GallowsHintKind) {
    // Nápověda zaplacená inkoustem nestojí body; utratí se, až když padne.
    const price = inkPrice(GALLOWS_HINT_COST[kind])
    const free = ink >= price
    const result = takeGallowsHint(state, kind, free)
    if (!result) {
      showFlash('Tady už nápověda nepomůže.', 'warn')
      return
    }
    if (free) onSpendInk(price)
    setState(result.state)
    showFlash(
      kind === 'letter'
        ? `Odhaleno písmeno ${result.letters[0]!.toUpperCase()}`
        : `Vyškrtnuto ${result.letters.length} písmen, která ve slově nejsou`,
      'accent',
    )
  }

  const shareText = useMemo(
    () =>
      [
        `SLOVA — Šibenice ${dayLabel}`,
        won ? puzzle.word.toUpperCase() : `${puzzle.word.length} písmen — neuhodnuto`,
        `${wrong} chyb · ★ ${breakdown.total}`,
      ].join('\n'),
    [breakdown.total, dayLabel, puzzle.word, won, wrong],
  )

  const needed = useMemo(() => neededLetters(puzzle), [puzzle])
  const foundLetters = state.tried.filter((letter) => needed.has(letter)).length

  return (
    <div className="game with-rail">
      <aside className="rail rail-left">
        <div className="hud">
          <div className="stat-row">
            <StatTile
              label="Životy"
              value={`${Math.max(0, GALLOWS_LIVES - wrong)}/${GALLOWS_LIVES}`}
              tone="accent"
              note={`Kolik chyb ještě uneseš. Za každé písmeno mimo přibude kus šibenice; po ${GALLOWS_LIVES} chybách kolo končí. Zbylé životy se na konci připočtou k bodům.`}
            />
            <StatTile
              label="Písmen"
              value={puzzle.word.length}
              note={'Jak dlouhé je hledané slovo. Háčky a čárky se nehádají — „u" odhalí i „ů".'}
            />
            <StatTile
              label="Odhaleno"
              value={`${foundLetters}/${needed.size}`}
              tone="gold"
              note="Kolik různých písmen slova už je venku. Až budou všechna, kolo je vyhrané."
            />
          </div>
        </div>

        <div className="hints card">
          <HintHead used={state.hintsUsed} ink={ink} />
          <div className="hint-buttons">
            <button
              type="button"
              className="btn btn-sm"
              disabled={over}
              onClick={() => hint('letter')}
            >
              <span>Odhal písmeno</span>
              <HintPrice points={GALLOWS_HINT_COST.letter} ink={ink} />
            </button>
            <button
              type="button"
              className="btn btn-sm"
              disabled={over}
              onClick={() => hint('strike')}
            >
              <span>Vyškrtni pět</span>
              <HintPrice points={GALLOWS_HINT_COST.strike} ink={ink} />
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

        <div className={`gallows-wrap ${shakeKey ? 'animate-shake' : ''}`} key={shakeKey}>
          <Gallows parts={wrong} lost={lost} />
        </div>

        {/* Slovo se vejde na šířku i o devíti písmenech — počet se pošle do
            CSS a šířka políčka se z něj dopočítá. */}
        <div className="word-slots" style={{ ['--slots' as string]: puzzle.word.length }}>
          {letters.map((letter, i) => (
            <span
              className={`slot ${letter ? 'filled' : ''} ${lost && !letter ? 'missed' : ''}`}
              key={i}
            >
              {letter ?? (lost ? puzzle.word[i] : '')}
            </span>
          ))}
        </div>
      </div>

      <div className="board-footer">
        {/* Vlastní klávesnice, ne ta sdílená: tady se hádají jen základní
            písmena (diakritika se skládá sama) a každá klávesa nese stav —
            sedí, nesedí, vyškrtnuto. */}
        <div className="letter-keys">
          {ROWS.map((row, r) => (
            <div className="letter-row" key={r}>
              {row.map((key) => {
                const tried = state.tried.includes(key)
                const struck = state.struck.includes(key)
                const hit = tried && plain(state).includes(key)
                return (
                  <button
                    type="button"
                    key={key}
                    className={`letter-key ${hit ? 'hit' : tried ? 'miss' : ''} ${
                      struck ? 'struck' : ''
                    }`}
                    disabled={tried || struck || over}
                    onClick={() => guess(key)}
                  >
                    {key}
                  </button>
                )
              })}
            </div>
          ))}
        </div>

        <div
          style={{
            display: 'flex',
            gap: 'var(--sp-2)',
            flexWrap: 'wrap',
            justifyContent: 'center',
          }}
        >
          <button
            type="button"
            className="btn btn-sm btn-ghost"
            onClick={() => setConfirmGiveUp(true)}
            disabled={over}
          >
            Vzdát slovo
          </button>
        </div>
      </div>

      <aside className="rail rail-right">
        <p className="faint" style={{ fontSize: '0.82rem', lineHeight: 1.55 }}>
          Háčky a čárky se hádat nemusí — písmeno „u" odhalí „u", „ú" i „ů".
          Hádá se slovo, ne diakritika.
        </p>
      </aside>

      {confirmGiveUp && (
        <Confirm
          title="Vzdát slovo?"
          body="Kolo skončí neuhodnuté a série se přeruší. Vrátit to nepůjde."
          confirmLabel="Vzdát slovo"
          onConfirm={onGiveUp}
          onCancel={() => setConfirmGiveUp(false)}
        />
      )}

      {done && (
        <ResultOverlay
          title={won ? (breakdown.perfect ? 'Bez jediné chyby!' : 'Uhodnuto!') : 'Viselec'}
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
