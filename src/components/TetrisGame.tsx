/** Obrazovka režimu SLABIKOVÝ TETRIS. */

import { useCallback, useEffect, useMemo, useRef, useState } from 'react'

import { inkPrice } from '../game/economy'
import { scoreTetris } from '../game/scoring'
import {
  canDrop,
  createTetrisState,
  dropSyllable,
  giveUp as giveUpState,
  isOver,
  isSwept,
  isWon,
  placed,
  scoringColumns,
  takeTetrisHint,
  TETRIS_HINT_COST,
  tray,
  upcoming,
  type TetrisPuzzle,
  type TetrisState,
} from '../game/tetris'
import type { RoundResult } from '../game/types'
import { Confirm } from './Confirm'
import { HintHead, HintPrice } from './HintPanel'
import { ResultOverlay } from './ResultOverlay'

interface Props {
  puzzle: TetrisPuzzle
  streak: number
  dayLabel: string
  onFinish: (result: RoundResult) => void
  onNext: () => void
  onHome: () => void
  /** Uložený stav rozehraného kola, když se hráč vrací zpátky do hry. */
  resume?: TetrisState | null
  /** Inkoust v profilu. Když na nápovědu stačí, zaplatí se jím místo bodů. */
  ink: number
  onSpendInk: (price: number) => void
  onProgress: (state: TetrisState, finished: boolean) => void
}

export function TetrisGame({
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
  const [state, setState] = useState<TetrisState>(() => resume ?? createTetrisState(puzzle))
  const [flash, setFlash] = useState<{ text: string; tone: string; key: number } | null>(null)
  const [tip, setTip] = useState<number | null>(null)
  /** Kterou slabiku ze zásobníku hráč zrovna pokládá. */
  const [slot, setSlot] = useState(0)
  const [done, setDone] = useState(false)
  const [confirmEnd, setConfirmEnd] = useState(false)
  const reported = useRef(false)

  const over = isOver(state)
  const won = isWon(state)
  const hand = useMemo(() => tray(state), [state])
  const pick = Math.min(slot, Math.max(0, hand.length - 1))
  const next = useMemo(() => upcoming(state), [state])
  const left = placed(state)

  const shown = useRef(puzzle.id)
  useEffect(() => {
    if (shown.current === puzzle.id) return
    shown.current = puzzle.id
    setState(createTetrisState(puzzle))
    setFlash(null)
    setTip(null)
    setSlot(0)
    setDone(false)
    reported.current = false
  }, [puzzle])

  useEffect(() => {
    onProgress(state, over || done)
  }, [state, over, done, onProgress])

  const breakdown = useMemo(() => scoreTetris(state, streak), [state, streak])

  useEffect(() => {
    if (!over || reported.current) return
    reported.current = true
    setDone(true)
    onFinish({
      mode: 'tetris',
      difficulty: puzzle.difficulty,
      puzzleId: puzzle.id,
      score: breakdown.total,
      perfect: breakdown.perfect,
      success: won,
      elapsedMs: (state.finishedAt ?? Date.now()) - state.startedAt,
      hintsUsed: state.hintsUsed,
      detail: {
        words: state.cleared.length,
        chain: state.bestChain,
        leftover: left,
        swept: isSwept(state) ? 1 : 0,
        extra: state.cleared.length,
      },
    })
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [over])

  const showFlash = useCallback((text: string, tone: string) => {
    setFlash({ text, tone, key: Date.now() })
  }, [])

  const drop = useCallback(
    (col: number) => {
      const result = dropSyllable(state, col, pick)
      if (!result) return
      setTip(null)
      setSlot(0)
      setState(result.state)
      if (result.words.length > 0) {
        if (navigator.vibrate) navigator.vibrate(20)
        showFlash(
          result.words.length === 1
            ? `${result.words[0]!.toUpperCase()}`
            : `Řetěz ×${result.words.length} · ${result.words.join(' · ').toUpperCase()}`,
          result.words.length > 1 ? 'gold' : 'ok',
        )
      }
    },
    [pick, showFlash, state],
  )

  useEffect(() => {
    function onKey(event: KeyboardEvent) {
      if (event.metaKey || event.ctrlKey || event.altKey) return
      const index = Number(event.key)
      if (!Number.isInteger(index) || index < 1 || index > puzzle.cols) return
      event.preventDefault()
      drop(index - 1)
    }
    window.addEventListener('keydown', onKey)
    return () => window.removeEventListener('keydown', onKey)
  }, [drop, puzzle.cols])

  function hint(kind: 'column' | 'swap') {
    const price = inkPrice(TETRIS_HINT_COST[kind])
    const free = ink >= price
    const result = takeTetrisHint(state, kind, free)
    if (!result) {
      showFlash(
        kind === 'column'
          ? 'Ze zásobníku se teď nic složit nedá. Zkus něco odložit.'
          : 'Fronta došla, není co odkládat.',
        'warn',
      )
      return
    }
    if (free) onSpendInk(price)
    setState(result.state)
    if (result.kind === 'column' && result.column !== undefined) {
      setSlot(result.slot ?? 0)
      setTip(result.column)
      showFlash(
        `${(hand[result.slot ?? 0] ?? '').toUpperCase()} do sloupce ${result.column + 1}`,
        'accent',
      )
    } else if (result.syllable) {
      setTip(null)
      setSlot(0)
      showFlash(`${result.syllable.toUpperCase()} jde na konec fronty`, 'accent')
    }
  }

  const shareText = useMemo(
    () =>
      [
        `SLOVA — Slabiky ${dayLabel}`,
        `${state.cleared.length} slov · řetěz ${state.bestChain}`,
        `★ ${breakdown.total}`,
      ].join('\n'),
    [breakdown.total, dayLabel, state.bestChain, state.cleared.length],
  )

  // Kam by slabika spadla — bez toho hráč netrefí sloupec napoprvé.
  const landing = useMemo(
    () => state.grid.map((column) => (column.length < puzzle.rows ? column.length : -1)),
    [state.grid, puzzle.rows],
  )
  const helpful = useMemo(
    () => new Set(over ? [] : scoringColumns(state, pick)),
    [state, over, pick],
  )

  return (
    <div className="game with-rail">
      <aside className="rail rail-left">
        <div className="hud">
          <div className="stat-row">
            <div className="stat">
              <div className="label">Slov</div>
              <div className="value num accent">{state.cleared.length}</div>
            </div>
            <div className="stat">
              <div className="label">Ve frontě</div>
              <div className="value num">{state.queue.length}</div>
            </div>
            <div className="stat">
              <div className="label">Řetěz</div>
              <div className="value num gold">{state.bestChain}</div>
            </div>
          </div>
        </div>

        <div className="hints card">
          <HintHead used={state.hintsUsed} ink={ink} />
          <div className="hint-buttons">
            <button
              type="button"
              className="btn btn-sm"
              disabled={over}
              onClick={() => hint('column')}
            >
              <span>Poradit tah</span>
              <HintPrice points={TETRIS_HINT_COST.column} ink={ink} />
            </button>
            <button
              type="button"
              className="btn btn-sm"
              disabled={over}
              onClick={() => hint('swap')}
            >
              <span>Odložit</span>
              <HintPrice points={TETRIS_HINT_COST.swap} ink={ink} />
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

        {/* Zásobník: ze tří slabik si hráč vybírá, kterou položí. Bez téhle
            volby je hra loterie — slabika, která se zrovna nehodí, zůstane
            na desce ležet navždycky. */}
        <div className="syl-queue">
          {hand.map((item, i) => (
            <button
              type="button"
              className={`syl-now ${i === pick ? 'picked' : ''}`}
              key={`${item}-${i}`}
              disabled={over}
              aria-pressed={i === pick}
              onClick={() => setSlot(i)}
            >
              {item}
            </button>
          ))}
          {hand.length === 0 && <span className="faint">konec dávky</span>}
          {next.length > 0 && (
            <>
              <span className="syl-next-label">dál</span>
              <span className="syl-next">
                {next.map((item, i) => (
                  <span className="syl-chip" key={`${item}-${i}`}>
                    {item}
                  </span>
                ))}
              </span>
            </>
          )}
        </div>

        <div
          className="well"
          style={{
            ['--cols' as string]: puzzle.cols,
            ['--rows' as string]: puzzle.rows,
          }}
        >
          {state.grid.map((column, col) => (
            <button
              type="button"
              className={`well-col ${tip === col ? 'tip' : ''} ${
                helpful.has(col) ? 'helpful' : ''
              }`}
              key={col}
              disabled={over || !canDrop(state, col)}
              aria-label={`Sloupec ${col + 1}`}
              onClick={() => drop(col)}
            >
              {/* Shora dolů, aby políčka seděla tak, jak je hráč vidí. */}
              {Array.from({ length: puzzle.rows }, (_, i) => {
                const row = puzzle.rows - 1 - i
                const item = column[row]
                return (
                  <span
                    className={`cell ${item ? 'filled' : ''} ${
                      !item && row === landing[col] ? 'landing' : ''
                    }`}
                    key={row}
                  >
                    {item ?? ''}
                  </span>
                )
              })}
            </button>
          ))}
        </div>
      </div>

      <div className="board-footer">
        <div className="found-strip">
          {state.cleared.length === 0 ? (
            <span className="faint">Zatím žádné slovo — dvě slabiky vedle sebe stačí.</span>
          ) : (
            state.cleared
              .slice(-6)
              .map((word, i) => (
                <span className="chip" key={`${word}-${i}`}>
                  {word}
                </span>
              ))
          )}
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
            onClick={() => setConfirmEnd(true)}
            disabled={over}
          >
            Ukončit dávku
          </button>
        </div>
      </div>

      <aside className="rail rail-right">
        <div className="card" style={{ padding: 'var(--sp-4)' }}>
          <div className="label">Složená slova</div>
          <div className="found-list" style={{ marginTop: 'var(--sp-2)' }}>
            {state.cleared.map((word, i) => (
              <span className="found-word" key={`${word}-${i}`}>
                {word}
              </span>
            ))}
            {state.cleared.length === 0 && <span className="faint">Zatím nic.</span>}
          </div>
        </div>
        <p className="faint" style={{ fontSize: '0.82rem', lineHeight: 1.55 }}>
          Vodorovně se čte zleva doprava, svisle zdola nahoru. Slabiky v dávce
          nejsou náhodné — vznikly rozsypáním celých slov, takže žádná z nich
          není zbytečná.
        </p>
      </aside>

      {confirmEnd && (
        <Confirm
          title="Ukončit dávku?"
          body={`Kolo se spočítá tak, jak je — máš ${state.cleared.length} slov. Zbytek dávky propadne.`}
          confirmLabel="Ukončit"
          onConfirm={() => {
            setConfirmEnd(false)
            setState(giveUpState(state))
          }}
          onCancel={() => setConfirmEnd(false)}
        />
      )}

      {done && (
        <ResultOverlay
          title={isSwept(state) ? 'Deska čistá!' : won ? 'Dávka rozmístěna' : 'Konec dávky'}
          subtitle={`${state.cleared.length} slov · nejdelší řetěz ${state.bestChain}`}
          breakdown={breakdown}
          shareText={shareText}
          celebrate={isSwept(state)}
          onNext={onNext}
          onHome={onHome}
        />
      )}
    </div>
  )
}
