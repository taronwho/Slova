/** Obrazovka režimu SLABIKOVÝ TETRIS. */

import { useCallback, useEffect, useMemo, useRef, useState } from 'react'

import { inkPrice } from '../game/economy'
import { scoreTetris } from '../game/scoring'
import {
  cells,
  createTetrisState,
  landing,
  dropMs,
  endRound,
  fill,
  hardDrop,
  isWon,
  level,
  move,
  placed,
  rotate,
  step,
  takeTetrisHint,
  TETRIS_HINT_COST,
  togglePause,
  type Spot,
  type TetrisDeck,
  type TetrisSetup,
  type TetrisState,
} from '../game/tetris'
import type { RoundResult } from '../game/types'
import { Confirm } from './Confirm'
import { StatTile } from './Explain'
import { HintHead, HintPrice } from './HintPanel'
import { ResultOverlay } from './ResultOverlay'

interface Props {
  deck: TetrisDeck
  setup: TetrisSetup
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
  deck,
  setup,
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
  const [state, setState] = useState<TetrisState>(
    () => resume ?? createTetrisState(deck, setup),
  )
  const [flash, setFlash] = useState<{ text: string; tone: string; key: number } | null>(null)
  const [spot, setSpot] = useState<Spot | null>(null)
  const [done, setDone] = useState(false)
  const [confirmEnd, setConfirmEnd] = useState(false)
  /** Otočil už hráč aspoň jednou? Do té doby se tlačítko hlásí samo. */
  const [turned, setTurned] = useState(false)
  const reported = useRef(false)

  const over = state.over
  const left = placed(state)

  const shown = useRef(setup.seed)
  useEffect(() => {
    if (shown.current === setup.seed) return
    shown.current = setup.seed
    setState(createTetrisState(deck, setup))
    setFlash(null)
    setSpot(null)
    setDone(false)
    setTurned(false)
    reported.current = false
  }, [deck, setup])

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
      difficulty: setup.difficulty,
      puzzleId: `t-${setup.seed}`,
      score: breakdown.total,
      perfect: breakdown.perfect,
      success: isWon(state),
      elapsedMs: (state.finishedAt ?? Date.now()) - state.startedAt,
      hintsUsed: state.hintsUsed,
      detail: {
        words: state.cleared.length,
        chain: state.bestChain,
        level: level(state),
        leftover: left,
        extra: state.cleared.length,
      },
    })
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [over])

  const showFlash = useCallback((text: string, tone: string) => {
    setFlash({ text, tone, key: Date.now() })
  }, [])

  // První, co hráč v kole uvidí. Otáčení je nejméně samozřejmá věc na celé
  // hře, takže se o něm řekne rovnou, ne až v návodu.
  useEffect(() => {
    if (turned || over) return undefined
    const timer = window.setTimeout(
      () => showFlash('Dvojici můžeš otáčet tlačítkem ⟳', 'accent'),
      600,
    )
    return () => window.clearTimeout(timer)
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  /** Společný konec tahu: hlášení o složených slovech, zhasnutí nápovědy. */
  const settle = useCallback(
    (words: string[]) => {
      if (words.length === 0) return
      setSpot(null)
      if (navigator.vibrate) navigator.vibrate(words.length > 1 ? 40 : 18)
      showFlash(
        words.length === 1
          ? words[0]!.toUpperCase()
          : `Řetěz ×${words.length} · ${words.join(' · ').toUpperCase()}`,
        words.length > 1 ? 'gold' : 'ok',
      )
    },
    [showFlash],
  )

  // Hodiny hry. Interval se přepočítá, kdykoli se změní tempo — tedy po
  // každé nové úrovni.
  const speed = dropMs(state)
  useEffect(() => {
    if (over || state.paused || done) return undefined
    const timer = window.setInterval(() => {
      setState((prev) => {
        const result = step(prev)
        if (result.words.length > 0) settle(result.words)
        return result.state
      })
    }, speed)
    return () => window.clearInterval(timer)
  }, [speed, over, state.paused, done, settle])

  const drop = useCallback(() => {
    setState((prev) => {
      const result = hardDrop(prev)
      if (result.words.length > 0) settle(result.words)
      return result.state
    })
  }, [settle])

  const soft = useCallback(() => {
    setState((prev) => {
      const result = step(prev)
      if (result.words.length > 0) settle(result.words)
      return result.state
    })
  }, [settle])

  useEffect(() => {
    function onKey(event: KeyboardEvent) {
      if (event.metaKey || event.ctrlKey || event.altKey) return
      const key = event.key
      if (key === 'ArrowLeft') setState((prev) => move(prev, -1))
      else if (key === 'ArrowRight') setState((prev) => move(prev, 1))
      else if (key === 'ArrowUp' || key === 'x' || key === 'X') {
        setTurned(true)
        setState((prev) => rotate(prev))
      } else if (key === 'z' || key === 'Z') {
        setTurned(true)
        setState((prev) => rotate(prev, -1))
      }
      else if (key === 'ArrowDown') soft()
      else if (key === ' ' || key === 'Enter') drop()
      else if (key === 'p' || key === 'P') setState(togglePause)
      else return
      event.preventDefault()
    }
    window.addEventListener('keydown', onKey)
    return () => window.removeEventListener('keydown', onKey)
  }, [drop, soft])

  function hint(kind: 'spot' | 'swap') {
    const price = inkPrice(TETRIS_HINT_COST[kind])
    const free = ink >= price
    const result = takeTetrisHint(state, kind, free)
    if (!result) {
      showFlash(
        kind === 'spot'
          ? 'Touhle dvojicí se teď nic složit nedá.'
          : 'Vyměnit teď nejde.',
        'warn',
      )
      return
    }
    if (free) onSpendInk(price)
    setState(result.state)
    if (result.spot) {
      setSpot(result.spot)
      showFlash(`${result.spot.words[0]!.toUpperCase()} — sloupec ${result.spot.col + 1}`, 'accent')
    } else {
      setSpot(null)
      showFlash('Vyměněno za další dvojici', 'accent')
    }
  }

  const shareText = useMemo(
    () =>
      [
        `SLOVA — Slabiky ${dayLabel}`,
        `${state.cleared.length} slov · řetěz ${state.bestChain} · úroveň ${level(state)}`,
        `★ ${breakdown.total}`,
      ].join('\n'),
    [breakdown.total, dayLabel, state],
  )

  // Kde dvojice dosedne, kdyby teď spadla. Bez stínu se u rychlejšího tempa
  // netrefí ani sloupec.
  const ghost = useMemo(() => (state.piece && !over ? landing(state) : []), [state, over])

  const falling = useMemo(() => (state.piece && !over ? cells(state.piece) : []), [state, over])
  const fullness = fill(state)

  return (
    <div className="game with-rail">
      <aside className="rail rail-left">
        <div className="hud">
          <div className="stat-row">
            <StatTile
              label="Slov"
              value={state.cleared.length}
              tone="accent"
              note="Kolik slov už jsi z padajících slabik složil. Za tucet slov v jednom kole bez nápovědy je meta."
            />
            <StatTile
              label="Řetěz"
              value={state.bestChain}
              tone="gold"
              note="Nejdelší řetěz z jednoho dopadu. Když se po odebrání slova slabiky sesypou a složí další, počítá se to jako řetěz — a je za něj prémie."
            />
            <StatTile
              label="Úroveň"
              value={level(state)}
              note="Roste s počtem složených slov a s ní i rychlost padání. Za každou dosaženou úroveň jsou body navíc."
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
              onClick={() => hint('spot')}
            >
              <span>Poradit</span>
              <HintPrice points={TETRIS_HINT_COST.spot} ink={ink} />
            </button>
            <button
              type="button"
              className="btn btn-sm"
              disabled={over}
              onClick={() => hint('swap')}
            >
              <span>Vyměnit</span>
              <HintPrice points={TETRIS_HINT_COST.swap} ink={ink} />
            </button>
          </div>
        </div>
      </aside>

      <div className="board">
        <div className="well-head">
          <span className="well-next-label">dál</span>
          <span className="well-next">
            {state.queue.map((pair, i) => (
              <span className="syl-pair" key={i}>
                <span className="syl-chip">{pair[0]}</span>
                <span className="syl-chip">{pair[1]}</span>
              </span>
            ))}
          </span>
          <span className="well-fill" aria-label="Zaplnění desky">
            <i style={{ width: `${Math.round(fullness * 100)}%` }} />
          </span>
          <button
            type="button"
            className="btn btn-sm btn-ghost"
            onClick={() => setState(togglePause)}
            disabled={over}
          >
            {state.paused ? 'Pokračovat' : 'Pauza'}
          </button>
        </div>

        {/* Hlášení o složeném slově má vlastní řádek s pevnou výškou. Padá po
            každém dopadu, takže kdyby se objevovalo a mizelo, deska by pod
            ním poskakovala. */}
        <div className="well-msg">
          {flash && (
            <span className={`banner banner-${flash.tone}`} key={flash.key}>
              {flash.text}
            </span>
          )}
        </div>

        <div className="well-stage">
          <div
            className={`well ${state.paused ? 'paused' : ''}`}
            style={{
              ['--cols' as string]: state.setup.cols,
              ['--rows' as string]: state.setup.rows,
            }}
          >
            {Array.from({ length: state.setup.rows }, (_, i) => {
              const row = state.setup.rows - 1 - i
              return Array.from({ length: state.setup.cols }, (_, col) => {
                const settled = state.grid[col]![row]
                const live = falling.find((cell) => cell.col === col && cell.row === row)
                const shadow = ghost.find((cell) => cell.col === col && cell.row === row)
                const marked =
                  spot && spot.col === col && !settled && !live
                    ? 'spot'
                    : ''
                // Šipka na první půlce ukazuje, kterým směrem se dvojice čte.
                // Bez ní se pravidlo „svisle zdola nahoru" musí pamatovat;
                // takhle je vidět přímo na desce.
                const lead = Boolean(live) && live === falling[0]
                return (
                  <span
                    className={`cell ${settled ? 'filled' : ''} ${live ? 'live' : ''} ${
                      !settled && !live && shadow ? 'ghost' : ''
                    } ${marked}`}
                    key={`${col}-${row}`}
                  >
                    {live?.text ?? settled ?? ''}
                    {lead && state.piece && (
                      <i className="lead" data-turn={state.piece.turn} aria-hidden="true" />
                    )}
                  </span>
                )
              })
            })}
            {state.paused && !over && <div className="well-pause">Pauza</div>}
          </div>
        </div>
      </div>

      <div className="board-footer">
        <div className="pad">
          <button
            type="button"
            className="btn pad-key"
            aria-label="Doleva"
            disabled={over || state.paused}
            onClick={() => setState((prev) => move(prev, -1))}
          >
            <span className="pad-icon" aria-hidden="true">
              ◀
            </span>
            <small>vlevo</small>
          </button>
          {/* Otáčení je ten tah, o který v téhle hře jde, a čtyři stejné
              ikonky vedle sebe ho neprozradí — proto popisek a dokud ho hráč
              nepoužije, i pulz. Zhasne po prvním otočení, ne po čase. */}
          <button
            type="button"
            className={`btn pad-key pad-turn ${turned ? '' : 'nudge'}`}
            aria-label="Otočit dvojici"
            disabled={over || state.paused}
            onClick={() => {
              setTurned(true)
              setState((prev) => rotate(prev))
            }}
          >
            <span className="pad-icon" aria-hidden="true">
              ⟳
            </span>
            <small>otočit</small>
          </button>
          <button
            type="button"
            className="btn pad-key"
            aria-label="Doprava"
            disabled={over || state.paused}
            onClick={() => setState((prev) => move(prev, 1))}
          >
            <span className="pad-icon" aria-hidden="true">
              ▶
            </span>
            <small>vpravo</small>
          </button>
          <button
            type="button"
            className="btn btn-primary pad-key pad-drop"
            aria-label="Položit"
            disabled={over || state.paused}
            onClick={drop}
          >
            <span className="pad-icon" aria-hidden="true">
              ⤓
            </span>
            <small>položit</small>
          </button>
        </div>
        <div style={{ display: 'flex', justifyContent: 'center' }}>
          <button
            type="button"
            className="btn btn-sm btn-ghost"
            onClick={() => setConfirmEnd(true)}
            disabled={over}
          >
            Ukončit kolo
          </button>
        </div>
      </div>

      <aside className="rail rail-right">
        <div className="card" style={{ padding: 'var(--sp-4)' }}>
          <div className="label">Složená slova</div>
          <div className="found-list" style={{ marginTop: 'var(--sp-2)' }}>
            {state.cleared
              .slice()
              .reverse()
              .map((word, i) => (
                <span className="found-word" key={`${word}-${i}`}>
                  {word}
                </span>
              ))}
            {state.cleared.length === 0 && <span className="faint">Zatím nic.</span>}
          </div>
        </div>
        <p className="faint" style={{ fontSize: '0.82rem', lineHeight: 1.55 }}>
          Dvojice se dá otočit do čtyř poloh a v každé se čte jinak: vodorovně
          zleva doprava, svisle zdola nahoru. „ko" a „lo" tedy dá KOLO i „lo"
          a „ko" — jen je otočit správně.
        </p>
      </aside>

      {confirmEnd && (
        <Confirm
          title="Ukončit kolo?"
          body={`Kolo se spočítá tak, jak je — máš ${state.cleared.length} slov.`}
          confirmLabel="Ukončit"
          onConfirm={() => {
            setConfirmEnd(false)
            setState(endRound(state))
          }}
          onCancel={() => setConfirmEnd(false)}
        />
      )}

      {done && (
        <ResultOverlay
          title={state.cleared.length > 0 ? 'Deska přetekla' : 'Konec kola'}
          subtitle={`${state.cleared.length} slov · úroveň ${level(state)}`}
          breakdown={breakdown}
          shareText={shareText}
          celebrate={state.cleared.length >= 12}
          onNext={onNext}
          onHome={onHome}
        />
      )}
    </div>
  )
}
