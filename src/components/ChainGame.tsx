/** Obrazovka režimu ŘETĚZ. */

import { useCallback, useEffect, useMemo, useRef, useState } from 'react'

import {
  budgetFor,
  createChainState,
  hammingDistance,
  HINT_COST,
  MOVE_ERROR_TEXT,
  playMove,
  remainingDistance,
  shortestPath,
  takeHint,
  undoMove,
  type ChainGraph,
  type ChainPuzzle,
  type ChainState,
  type HintKind,
} from '../game/chain'
import { scoreChain } from '../game/scoring'
import type { RoundResult } from '../game/types'
import { CZECH_LETTERS } from '../lib/czech'
import { Confirm } from './Confirm'
import { inkPrice } from '../game/economy'
import { HintHead, HintPrice } from './HintPanel'
import { Keyboard } from './Keyboard'
import { ResultOverlay } from './ResultOverlay'

interface Props {
  graph: ChainGraph
  puzzle: ChainPuzzle
  streak: number
  dayLabel: string
  onFinish: (result: RoundResult) => void
  onNext: () => void
  onHome: () => void
  onGiveUp: () => void
  /** Uložený stav rozehraného kola, když se hráč vrací zpátky do hry. */
  resume?: ChainState | null
  /** Inkoust v profilu. Když na nápovědu stačí, zaplatí se jím místo bodů. */
  ink: number
  onSpendInk: (price: number) => void
  onProgress: (state: ChainState, finished: boolean) => void
}

interface Flash {
  text: string
  tone: 'error' | 'warn' | 'accent'
  key: number
}

export function ChainGame({
  graph,
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
  const [state, setState] = useState<ChainState>(() => resume ?? createChainState(puzzle))
  const [draft, setDraft] = useState<string[]>(() => [...puzzle.start])
  const [cursor, setCursor] = useState(0)
  const [flash, setFlash] = useState<Flash | null>(null)
  const [shakeKey, setShakeKey] = useState(0)
  const [hintPosition, setHintPosition] = useState<number | null>(null)
  const [pendingUndo, setPendingUndo] = useState(false)
  const [done, setDone] = useState(false)
  const [confirmGiveUp, setConfirmGiveUp] = useState(false)
  const reported = useRef(false)

  const draftRef = useRef<HTMLDivElement | null>(null)
  const current = state.path[state.path.length - 1]!
  const solved = state.finishedAt !== null
  const moves = state.path.length - 1
  const budget = budgetFor(puzzle)

  const remaining = useMemo(
    () => (solved ? 0 : remainingDistance(graph, state)),
    [graph, state, solved],
  )

  // Nové kolo — všechno zpět na začátek. Na prvním renderu se přeskočí,
  // jinak by přepsalo stav načtený z rozehraného kola.
  const shown = useRef(puzzle.id)
  useEffect(() => {
    if (shown.current === puzzle.id) return
    shown.current = puzzle.id
    setState(createChainState(puzzle))
    setDraft([...puzzle.start])
    setCursor(0)
    setFlash(null)
    setHintPosition(null)
    setPendingUndo(false)
    setDone(false)
    reported.current = false
  }, [puzzle])

  // Po každé změně stavu se kolo uloží, aby šlo pokračovat i po zavření hry.
  // Dohrané ani předčasně ukončené kolo se neukládá — nabízet „pokračovat"
  // u něčeho, co je za sebou, nedává smysl.
  useEffect(() => {
    onProgress(state, state.finishedAt !== null || done)
  }, [state, done, onProgress])

  useEffect(() => {
    if (!solved || reported.current) return
    reported.current = true
    setDone(true)
  }, [solved])

  // Po každém tahu doroluj k rozepsanému slovu — na telefonu žebřík povyroste
  // a hráč by jinak koukal na starou část řetězu.
  useEffect(() => {
    if (solved) return
    draftRef.current?.scrollIntoView({
      behavior: window.matchMedia?.('(prefers-reduced-motion: reduce)').matches
        ? 'auto'
        : 'smooth',
      block: 'center',
    })
  }, [state.path.length, solved])

  const breakdown = useMemo(
    () => (solved ? scoreChain(state, streak) : null),
    [solved, state, streak],
  )

  useEffect(() => {
    if (!done || !breakdown) return
    onFinish({
      mode: 'chain',
      difficulty: puzzle.difficulty,
      puzzleId: puzzle.id,
      score: breakdown.total,
      perfect: breakdown.perfect,
      // Řetěz se hlásí jen po dosažení cíle — vzdané kolo se nezapisuje.
      success: true,
      elapsedMs: (state.finishedAt ?? Date.now()) - state.startedAt,
      hintsUsed: state.hintsUsed,
      detail: { moves, par: puzzle.par, extra: moves - puzzle.par },
    })
    // Kolo se hlásí právě jednou; závislost na `done` to hlídá.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [done])

  const showFlash = useCallback((text: string, tone: Flash['tone']) => {
    setFlash({ text, tone, key: Date.now() })
  }, [])

  const resetDraft = useCallback(
    (word: string) => {
      setDraft([...word])
      setCursor(0)
      setHintPosition(null)
    },
    [],
  )

  const submit = useCallback(() => {
    if (solved) return
    const word = draft.join('')
    const outcome = playMove(graph, state, word)

    if (!outcome.ok) {
      showFlash(MOVE_ERROR_TEXT[outcome.error], 'error')
      setShakeKey((n) => n + 1)
      if (navigator.vibrate) navigator.vibrate(40)
      return
    }

    setState(outcome.state)
    resetDraft(outcome.state.path[outcome.state.path.length - 1]!)

    if (outcome.solved) {
      setFlash(null)
      setPendingUndo(false)
      return
    }
    if (outcome.warning === 'dead-end') {
      showFlash('Slepá ulička — odtud už se k cíli nedostaneš.', 'warn')
      setPendingUndo(true)
    } else if (outcome.warning === 'over-budget') {
      showFlash('Pozor, tímhle tahem se nevejdeš do rozpočtu.', 'warn')
      setPendingUndo(true)
    } else {
      setFlash(null)
      setPendingUndo(false)
    }
  }, [draft, graph, resetDraft, showFlash, solved, state])

  const undo = useCallback(() => {
    const back = undoMove(state)
    setState(back)
    resetDraft(back.path[back.path.length - 1]!)
    setFlash(null)
    setPendingUndo(false)
  }, [resetDraft, state])

  const typeLetter = useCallback(
    (letter: string) => {
      if (solved) return
      setDraft((prev) => {
        const next = [...prev]
        next[cursor] = letter
        return next
      })
      setCursor((prev) => Math.min(prev + 1, current.length - 1))
      setHintPosition(null)
    },
    [cursor, current.length, solved],
  )

  const backspace = useCallback(() => {
    if (solved) return
    const at = cursor
    setDraft((prev) => {
      const next = [...prev]
      next[at] = current[at]!
      return next
    })
    setCursor((prev) => Math.max(prev - 1, 0))
  }, [cursor, current, solved])

  // Fyzická klávesnice
  useEffect(() => {
    function onKey(event: KeyboardEvent) {
      if (event.metaKey || event.ctrlKey || event.altKey) return
      if (event.key === 'Enter') {
        event.preventDefault()
        submit()
      } else if (event.key === 'Backspace') {
        event.preventDefault()
        backspace()
      } else if (event.key === 'ArrowLeft') {
        setCursor((prev) => Math.max(prev - 1, 0))
      } else if (event.key === 'ArrowRight') {
        setCursor((prev) => Math.min(prev + 1, current.length - 1))
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
  }, [backspace, current.length, submit, typeLetter])

  function useHint(kind: HintKind) {
    // Nápověda zaplacená inkoustem nestojí body. Utratí se až tady, když se
    // opravdu povedla — za nápovědu, která nemá co poradit, se neplatí.
    const price = inkPrice(HINT_COST[kind])
    const free = ink >= price
    const result = takeHint(graph, state, kind, free)
    if (!result) {
      showFlash('Odsud už nápověda nepomůže — vrať tah zpět.', 'warn')
      return
    }
    if (free) onSpendInk(price)
    setState(result.state)
    if (kind === 'distance') {
      showFlash(`K cíli zbývá nejméně ${result.distance} tahů.`, 'accent')
    } else if (kind === 'position') {
      setHintPosition(result.position ?? null)
      setCursor(result.position ?? 0)
      showFlash('Zvýrazněné písmeno se mění.', 'accent')
    } else if (result.word) {
      setDraft([...result.word])
      showFlash(`Další slovo je ${result.word.toUpperCase()}.`, 'accent')
    }
  }

  const solutionPath = useMemo(() => {
    if (!solved) return []
    const from = graph.index.get(puzzle.start)
    const to = graph.index.get(puzzle.target)
    if (from === undefined || to === undefined) return []
    return (shortestPath(graph, from, to) ?? []).map((i) => graph.words[i]!)
  }, [graph, puzzle, solved])

  const draftDiff = hammingDistance(current, draft.join(''))
  const nearGoal = remaining >= 0 && remaining <= 2

  const shareText = useMemo(() => {
    const marks = Array.from({ length: moves }, (_, i) =>
      i < puzzle.par ? '🟩' : '🟨',
    ).join('')
    return [
      `SLOVA — Řetěz ${dayLabel}`,
      `${puzzle.start.toUpperCase()} ▸ ${puzzle.target.toUpperCase()}   nejkratší cesta ${puzzle.par}, dohráno na ${moves}`,
      `${marks}  ★ ${breakdown?.total ?? 0}`,
    ].join('\n')
  }, [breakdown, dayLabel, moves, puzzle])

  return (
    <div className="game with-rail">
      <aside className="rail rail-left">
        <div className="hud">
          <div className="stat-row">
            <div className="stat">
              <div className="label">Tahy</div>
              <div className={`value num ${moves > budget ? 'warn' : ''}`}>{moves}</div>
            </div>
            <div className="stat">
              {/* Na tři sloupce se celý popisek na řádek nevejde a zalomil by
                  se, což ukrojí z hrací plochy. Na úzkém displeji stačí
                  zkrácený. */}
              <div className="label">
                <span className="wide-only">Nejkratší cesta</span>
                <span className="narrow-only">Nejkratší</span>
              </div>
              <div className="value num gold">{puzzle.par}</div>
            </div>
            <div className="stat">
              <div className="label">Zbývá nejméně</div>
              <div className={`value num ${remaining === -1 ? 'warn' : 'accent'}`}>
                {solved ? 0 : remaining === -1 ? '—' : remaining}
              </div>
              <div className="stat-note faint">rozpočet {budget} tahů</div>
            </div>
          </div>
        </div>

        <div className="hints card">
          <HintHead used={state.hintsUsed} ink={ink} />
          <div className="hint-buttons">
            <button
              type="button"
              className="btn btn-sm"
              disabled={solved}
              onClick={() => useHint('distance')}
            >
              <span>Vzdálenost</span>
              <HintPrice points={HINT_COST.distance} ink={ink} />
            </button>
            <button
              type="button"
              className="btn btn-sm"
              disabled={solved}
              onClick={() => useHint('position')}
            >
              <span>Písmeno</span>
              <HintPrice points={HINT_COST.position} ink={ink} />
            </button>
            <button
              type="button"
              className="btn btn-sm"
              disabled={solved}
              onClick={() => useHint('word')}
            >
              <span>Celé slovo</span>
              <HintPrice points={HINT_COST.word} ink={ink} />
            </button>
          </div>
        </div>
      </aside>

      <div className="board">
        {flash && (
          <div className={`banner banner-${flash.tone}`} key={flash.key}>
            <span>{flash.text}</span>
            {pendingUndo && (
              <span className="banner-actions">
                <button type="button" className="btn btn-sm" onClick={undo}>
                  Vrátit tah
                </button>
              </span>
            )}
          </div>
        )}

        {/* Rozměr dlaždice se dopočítá z toho, kolik řad se doopravdy kreslí:
            celý dosavadní řetěz, rozepsané slovo a cílové slovo. Čím delší
            řetěz, tím menší dlaždice, aby bylo pod sebou vidět co nejvíc. */}
        <div
          className="ladder"
          style={{
            ['--rows' as string]: state.path.length + (solved ? 0 : 2),
            ['--cols' as string]: puzzle.start.length,
          }}
        >
          {state.path.map((word, index) => {
            const previous = index > 0 ? state.path[index - 1]! : null
            return (
              <div className="rung-wrap" key={`${word}-${index}`}>
                {index > 0 && <div className="connector lit" />}
                <div className={`rung ${index === 0 ? 'is-start' : ''}`}>
                  {[...word].map((letter, i) => (
                    <div
                      key={i}
                      className={`tile ${previous && previous[i] !== letter ? 'changed' : ''}`}
                    >
                      {letter}
                    </div>
                  ))}
                </div>
              </div>
            )
          })}

          {!solved && (
            <>
              <div className="connector" />
              <div
                className={`rung ${shakeKey ? 'animate-shake' : ''}`}
                key={shakeKey}
                ref={draftRef}
              >
                {draft.map((letter, i) => (
                  <button
                    type="button"
                    key={i}
                    className={`tile ${i === cursor ? 'editing' : ''} ${
                      hintPosition === i ? 'changed' : ''
                    } ${letter !== current[i] ? 'caret' : ''}`}
                    onClick={() => setCursor(i)}
                    aria-label={`Pozice ${i + 1}, písmeno ${letter}`}
                  >
                    {letter}
                  </button>
                ))}
              </div>

              <div className="ladder-gap">
                <div className="dots">
                  <i />
                  <i />
                  <i />
                </div>
                <span>
                  {remaining === -1
                    ? 'slepá ulička'
                    : `zbývá nejméně ${remaining} ${remaining === 1 ? 'tah' : remaining < 5 ? 'tahy' : 'tahů'}`}
                </span>
              </div>
            </>
          )}

          <div className={`rung is-goal goal-card ${nearGoal ? 'near' : ''}`}>
            {[...puzzle.target].map((letter, i) => (
              <div key={i} className="tile">
                {letter}
              </div>
            ))}
          </div>
        </div>

      </div>

      {!solved && (
        <div className="board-footer">
          <div style={{ display: 'flex', gap: 'var(--sp-2)', flexWrap: 'wrap', justifyContent: 'center' }}>
            <button
              type="button"
              className="btn btn-sm"
              onClick={() => resetDraft(current)}
              disabled={draftDiff === 0}
            >
              Zrušit úpravu
            </button>
            <button
              type="button"
              className="btn btn-sm"
              onClick={undo}
              disabled={state.path.length <= 1}
            >
              Vrátit tah
            </button>
            <button
              type="button"
              className="btn btn-sm btn-ghost"
              onClick={() => setConfirmGiveUp(true)}
            >
              Vzdát kolo
            </button>
          </div>

          <Keyboard
            onLetter={typeLetter}
            onBackspace={backspace}
            onEnter={submit}
            enterDisabled={draftDiff !== 1}
            enterLabel="Zahrát"
          />
        </div>
      )}

      <aside className="rail rail-right">
        <div className="card" style={{ padding: 'var(--sp-4)' }}>
          <div className="label" style={{ marginBottom: 'var(--sp-2)' }}>
            Řetěz
          </div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 4, fontSize: '0.9rem' }}>
            {state.path.map((word, i) => (
              <div key={i} style={{ display: 'flex', justifyContent: 'space-between' }}>
                <span style={{ textTransform: 'uppercase', letterSpacing: '0.06em' }}>
                  {word}
                </span>
                <span className="faint num">{i}</span>
              </div>
            ))}
          </div>
        </div>
        <p className="faint" style={{ fontSize: '0.82rem', lineHeight: 1.55 }}>
          Měň vždy jedno písmeno. Každý mezikrok musí být české slovo a žádné se
          nesmí zopakovat. Ukazatel „zbývá nejméně" počítá skutečnou vzdálenost
          k cíli s ohledem na už použitá slova.
        </p>
      </aside>

      {confirmGiveUp && (
        <Confirm
          title="Vzdát kolo?"
          body="Rozehraný řetěz se zahodí a série se přeruší. Vrátit to nepůjde."
          confirmLabel="Vzdát kolo"
          onConfirm={onGiveUp}
          onCancel={() => setConfirmGiveUp(false)}
        />
      )}

      {done && breakdown && (
        <ResultOverlay
          title={breakdown.perfect ? 'Perfektní!' : 'Dohráno'}
          subtitle={`${puzzle.start.toUpperCase()} ▸ ${puzzle.target.toUpperCase()} · nejkratší cesta ${puzzle.par}, tvých tahů ${moves}`}
          breakdown={breakdown}
          shareText={shareText}
          onNext={onNext}
          onHome={onHome}
        >
          {solutionPath.length > 0 && (
            <div className="solution-path">
              {solutionPath.map((word, i) => (
                <span key={i}>
                  {i > 0 && <span className="sep"> · </span>}
                  {word}
                </span>
              ))}
            </div>
          )}
        </ResultOverlay>
      )}
    </div>
  )
}
