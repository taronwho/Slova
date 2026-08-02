/** Obrazovka režimu VETŘELEC. */

import { useEffect, useMemo, useRef, useState } from 'react'

import { inkPrice } from '../game/economy'
import {
  createIntruderState,
  foundOdd,
  INTRUDER_HINT_COST,
  KIND_LABEL,
  KIND_ORDER,
  name as nameReason,
  namedReason,
  pick as pickWord,
  takeHint,
  type IntruderPuzzle,
  type IntruderState,
} from '../game/intruder'
import { scoreIntruder } from '../game/scoring'
import type { RoundResult } from '../game/types'
import { StatTile } from './Explain'
import { HintHead, HintPrice } from './HintPanel'
import { ResultOverlay } from './ResultOverlay'

interface Props {
  puzzle: IntruderPuzzle
  streak: number
  dayLabel: string
  onFinish: (result: RoundResult) => void
  onNext: () => void
  onHome: () => void
  resume?: IntruderState | null
  ink: number
  onSpendInk: (price: number) => void
  onProgress: (state: IntruderState, finished: boolean) => void
}

export function IntruderGame({
  puzzle,
  streak,
  dayLabel,
  onFinish,
  onNext,
  onHome,
  resume,
  ink,
  onSpendInk,
  onProgress,
}: Props) {
  const [state, setState] = useState<IntruderState>(
    () => resume ?? createIntruderState(puzzle),
  )
  const [done, setDone] = useState(false)
  const reported = useRef(false)
  const over = state.finishedAt !== null
  const right = foundOdd(state)
  const named = namedReason(state)

  const shown = useRef(puzzle.id)
  useEffect(() => {
    if (shown.current === puzzle.id) return
    shown.current = puzzle.id
    setState(createIntruderState(puzzle))
    setDone(false)
    reported.current = false
  }, [puzzle])

  useEffect(() => {
    onProgress(state, over || done)
  }, [state, over, done, onProgress])

  const breakdown = useMemo(() => scoreIntruder(state, streak), [state, streak])

  useEffect(() => {
    if (!over || reported.current) return
    reported.current = true
    setDone(true)
    onFinish({
      mode: 'intruder',
      difficulty: puzzle.difficulty,
      puzzleId: puzzle.id,
      score: breakdown.total,
      perfect: breakdown.perfect,
      success: right,
      elapsedMs: (state.finishedAt ?? Date.now()) - state.startedAt,
      hintsUsed: state.hintsUsed,
      detail: { solved: right ? 1 : 0, extra: named ? 1 : 0 },
    })
  }, [over, breakdown, onFinish, puzzle, state, right, named])

  function hint() {
    const price = inkPrice(INTRUDER_HINT_COST)
    const free = ink >= price
    const next = takeHint(state)
    if (!next) return
    if (free) onSpendInk(price)
    setState({
      ...next,
      hintsUsed: state.hintsUsed + 1,
      freeHints: state.freeHints + (free ? 1 : 0),
      hintCost: state.hintCost + (free ? 0 : INTRUDER_HINT_COST),
    })
  }

  const shareText = useMemo(
    () =>
      [
        `SLOVA — Vetřelec ${dayLabel}`,
        right ? `${puzzle.odd.toUpperCase()} ✓` : `${puzzle.odd.toUpperCase()} unikl`,
        `${named ? 'i důvod' : 'bez důvodu'} · ★ ${breakdown.total}`,
      ].join('\n'),
    [breakdown.total, dayLabel, named, puzzle.odd, right],
  )

  return (
    <div className="game with-rail">
      <aside className="rail rail-left">
        <div className="hud">
          <div className="stat-row">
            <StatTile
              label="Krok"
              value={state.picked ? '2 ze 2' : '1 ze 2'}
              tone="accent"
              note="Nejdřív ukaž na slovo, které do pětice nepatří. Pak řekni, co ta ostatní čtyři spojuje — za důvod je skoro tolik bodů co za samotného vetřelce."
            />
            <StatTile
              label="Vyloučeno"
              value={state.ruled.length}
              tone="gold"
              note="Kolik slov ti nápověda odklidila z cesty. Vyloučit jde jen slovo, které vetřelec není."
            />
          </div>
        </div>

        <div className="hints card">
          <HintHead used={state.hintsUsed} ink={ink} />
          <div className="hint-buttons">
            <button
              type="button"
              className="btn btn-sm"
              disabled={over || state.picked !== null}
              onClick={hint}
            >
              <span>Vyluč jedno slovo</span>
              <HintPrice points={INTRUDER_HINT_COST} ink={ink} />
            </button>
          </div>
        </div>
      </aside>

      <div className="board">
        <p className="intruder-ask">
          {state.picked
            ? 'A co spojuje ta ostatní čtyři?'
            : 'Které slovo do pětice nepatří?'}
        </p>

        <div className="intruder-words">
          {puzzle.words.map((word) => {
            const ruled = state.ruled.includes(word)
            const mine = state.picked === word
            const truth = over && word === puzzle.odd
            return (
              <button
                type="button"
                key={word}
                className={`intruder-word ${ruled ? 'ruled' : ''} ${mine ? 'mine' : ''} ${
                  truth ? 'truth' : ''
                } ${over && mine && !right ? 'wrong' : ''}`}
                disabled={ruled || state.picked !== null}
                onClick={() => setState((current) => pickWord(current, word))}
              >
                {word}
              </button>
            )
          })}
        </div>

        {state.picked && (
          <div className="intruder-reasons">
            {KIND_ORDER.map((kind) => (
              <button
                type="button"
                key={kind}
                className={`btn ${state.reason === kind ? 'btn-primary' : ''}`}
                disabled={state.reason !== null}
                onClick={() => setState((current) => nameReason(current, kind))}
              >
                {KIND_LABEL[kind]}
              </button>
            ))}
          </div>
        )}
      </div>

      <aside className="rail rail-right">
        <p className="faint" style={{ fontSize: '0.82rem', lineHeight: 1.55 }}>
          Čtyři slova něco spojuje, páté ne. Vetřelec je vždycky právě jeden —
          na zbylých dvou znacích se pětice shoduje, takže ukázat jinam
          a mít pravdu nejde.
        </p>
      </aside>

      {done && (
        <ResultOverlay
          title={right ? (named ? 'Trefa i důvod!' : 'Vetřelec odhalen') : 'Vetřelec unikl'}
          subtitle={puzzle.odd.toUpperCase()}
          breakdown={breakdown}
          shareText={shareText}
          celebrate={right}
          onNext={onNext}
          onHome={onHome}
        >
          <p className="clue-recap">
            Čtyři slova spojuje <b>{KIND_LABEL[puzzle.kind]}</b> — {puzzle.shared}.
            {' '}Vetřelec má {puzzle.oddValue}.
          </p>
        </ResultOverlay>
      )}
    </div>
  )
}
