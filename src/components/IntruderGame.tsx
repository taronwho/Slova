/** Obrazovka režimu VETŘELEC. */

import { useEffect, useMemo, useRef, useState } from 'react'

import { inkPrice } from '../game/economy'
import {
  createIntruderState,
  foundOdd,
  INTRUDER_HINT_COST,
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
      detail: { solved: right ? 1 : 0, extra: state.ruled.length },
    })
  }, [over, breakdown, onFinish, puzzle, state, right])

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
        `★ ${breakdown.total}`,
      ].join('\n'),
    [breakdown.total, dayLabel, puzzle.odd, right],
  )

  return (
    <div className="game with-rail">
      <aside className="rail rail-left">
        <div className="hud">
          <div className="stat-row">
            <StatTile
              label="Slov"
              value={puzzle.words.length}
              tone="accent"
              note="Čtyři z nich něco spojuje, páté ne. Co to bylo, se dozvíš po dohrání — přijít na to je celá hra."
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
          Které slovo do pětice nepatří?
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
          title={right ? 'Vetřelec odhalen!' : 'Vetřelec unikl'}
          breakdown={breakdown}
          shareText={shareText}
          celebrate={right}
          onNext={onNext}
          onHome={onHome}
        >
          {/* Celá pětice znovu, tentokrát s odpovědí. Samotné jméno vetřelce
              pod nadpisem bylo málo: hráč chce vidět, které čtyři k sobě
              patřily, ne jen to páté. Barva to řekne dřív než text. */}
          <div className="verdict-words">
            {puzzle.words.map((word) => (
              <span
                key={word}
                className={`verdict-word ${word === puzzle.odd ? 'odd' : 'fits'}`}
              >
                <span className="verdict-mark" aria-hidden="true">
                  {word === puzzle.odd ? '≠' : '✓'}
                </span>
                {word}
              </span>
            ))}
          </div>
          {/* Dvojtečka místo věty se spojkou: „jazyk původu: angličtina"
              je správně česky u všech sedmi souvislostí, kdežto „vetřelec
              má angličtina" nedávalo smysl u žádné. */}
          <p className="clue-recap">{puzzle.recap}</p>
        </ResultOverlay>
      )}
    </div>
  )
}
