/** Obrazovka režimu CITÁT. */

import { useCallback, useEffect, useMemo, useRef, useState } from 'react'

import { inkPrice } from '../game/economy'
import {
  artUrl,
  countLetter,
  createQuoteState,
  hintLadder,
  isSolved,
  missCount,
  QUOTE_COST,
  QUOTE_MISS_LIMIT,
  revealWord,
  tokens,
  tryLetter as playLetter,
  type Quote,
  type QuoteHint,
  type QuoteState,
} from '../game/quotes'
import { scoreQuote } from '../game/scoring'
import type { RoundResult } from '../game/types'
import { Confirm } from './Confirm'
import { StatTile } from './Explain'
import { HintHead, HintPrice } from './HintPanel'
import { ResultOverlay } from './ResultOverlay'

interface Props {
  quote: Quote
  /** Seed pro výběr slov odkrytých na začátku — u denní výzvy je pevný. */
  seed: number
  streak: number
  dayLabel: string
  onFinish: (result: RoundResult) => void
  onNext: () => void
  onHome: () => void
  onGiveUp: () => void
  resume?: QuoteState | null
  ink: number
  onSpendInk: (price: number) => void
  onProgress: (state: QuoteState, finished: boolean) => void
}

const ROWS = ['qwertzuiop', 'asdfghjkl', 'yxcvbnm'].map((row) => row.split(''))

const HINT_LABEL: Record<QuoteHint, string> = {
  art: 'Ukaž podobiznu',
  note: 'Kdo to byl',
  who: 'Jméno autora',
  word: 'Odhal slovo',
}

export function QuotesGame({
  quote,
  seed,
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
  const [state, setState] = useState<QuoteState>(
    () => resume ?? createQuoteState(quote, seed),
  )
  const [flash, setFlash] = useState<{ text: string; tone: string; key: number } | null>(null)
  const [confirmGiveUp, setConfirmGiveUp] = useState(false)
  const [artFailed, setArtFailed] = useState(false)
  const [done, setDone] = useState(false)
  const reported = useRef(false)

  const over = state.finishedAt !== null
  const won = isSolved(state)
  const misses = missCount(state)
  const parts = useMemo(() => tokens(quote.text), [quote.text])

  const shown = useRef(quote.id)
  useEffect(() => {
    if (shown.current === quote.id) return
    shown.current = quote.id
    setState(createQuoteState(quote, seed))
    setFlash(null)
    setArtFailed(false)
    setDone(false)
    reported.current = false
  }, [quote, seed])

  useEffect(() => {
    onProgress(state, over || done)
  }, [state, over, done, onProgress])

  const breakdown = useMemo(() => scoreQuote(state, streak), [state, streak])

  useEffect(() => {
    if (!over || reported.current) return
    reported.current = true
    setDone(true)
    onFinish({
      mode: 'quotes',
      difficulty: quote.difficulty,
      puzzleId: quote.id,
      score: breakdown.total,
      perfect: breakdown.perfect,
      success: won,
      elapsedMs: (state.finishedAt ?? Date.now()) - state.startedAt,
      hintsUsed: state.hints.length,
      detail: { misses, solved: won ? 1 : 0, extra: Math.max(0, QUOTE_MISS_LIMIT - misses) },
    })
  }, [over, breakdown, onFinish, quote, state, won, misses])

  const showFlash = (text: string, tone: string) =>
    setFlash({ text, tone, key: Date.now() })

  const press = useCallback(
    (letter: string) => {
      if (over) return
      setState((current) => {
        if (current.tried.includes(letter)) return current
        const hits = countLetter(current, letter)
        showFlash(
          hits > 0 ? `${letter.toUpperCase()} — ${hits}×` : `${letter.toUpperCase()} tam není`,
          hits > 0 ? 'accent' : 'warn',
        )
        return playLetter(current, letter)
      })
    },
    [over],
  )

  useEffect(() => {
    const onKey = (event: KeyboardEvent) => {
      if (event.metaKey || event.ctrlKey || event.altKey) return
      if (event.key.length !== 1) return
      const letter = event.key.toLowerCase()
      if (!/[a-záčďéěíňóřšťúůýž]/.test(letter)) return
      event.preventDefault()
      press(letter)
    }
    window.addEventListener('keydown', onKey)
    return () => window.removeEventListener('keydown', onKey)
  }, [press])

  /** Nápovědy jdou po stupních; „odhal slovo" zbude, až dojdou ostatní. */
  const ladder = useMemo(() => hintLadder(quote), [quote])
  const nextStep: QuoteHint =
    ladder.find((step) => !state.hints.includes(step)) ?? 'word'

  function hint() {
    if (over) return
    const price = inkPrice(QUOTE_COST[nextStep])
    const free = ink >= price
    if (free) onSpendInk(price)
    setState((current) => {
      const paid = { ...current, hints: [...current.hints, nextStep] }
      paid.freeHints = current.freeHints + (free ? 1 : 0)
      paid.hintCost = current.hintCost + (free ? 0 : QUOTE_COST[nextStep])
      return nextStep === 'word' ? revealWord(paid) : paid
    })
    showFlash(HINT_LABEL[nextStep], 'accent')
  }

  const seenArt = state.hints.includes('art') && !!quote.art && !artFailed
  const seenNote = state.hints.includes('note') || state.hints.includes('who') || over
  const seenWho = state.hints.includes('who') || over

  const shareText = useMemo(
    () =>
      [
        `SLOVA — Citát ${dayLabel}`,
        won ? `„${quote.text}" — ${quote.who}` : 'nedoplněno',
        `${misses} vedle · ★ ${breakdown.total}`,
      ].join('\n'),
    [breakdown.total, dayLabel, misses, quote, won],
  )

  const words = parts.filter((token) => token.word).length
  const openWords = parts.filter(
    (token, index) =>
      token.word &&
      [...token.text].every(
        (letter) =>
          state.given.includes(index) ||
          state.tried.includes(letter.toLowerCase().normalize('NFD').replace(/\p{M}/gu, '')),
      ),
  ).length

  return (
    <div className="game with-rail">
      <aside className="rail rail-left">
        <div className="hud">
          <div className="stat-row">
            <StatTile
              label="Slov"
              value={`${openWords}/${words}`}
              tone="accent"
              note={'Kolik slov výroku je celých venku. Diakritika se nehádá — „u" odhalí i „ů".'}
            />
            <StatTile
              label="Vedle"
              value={misses}
              tone="warn"
              note={`Kolik písmen jsi zkusil mimo. Chyba kolo neukončí, jen ubere body — po ${QUOTE_MISS_LIMIT} chybách ale kolo skončí.`}
            />
          </div>
        </div>

        <div className="hints card">
          <HintHead used={state.hints.length} ink={ink} />
          <div className="hint-buttons">
            <button type="button" className="btn btn-sm" disabled={over} onClick={hint}>
              <span>{HINT_LABEL[nextStep]}</span>
              <HintPrice points={QUOTE_COST[nextStep]} ink={ink} />
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

        {/* Podobizna se stahuje z Commons, takže nemusí dorazit — bez sítě
            ani jednou. Když se nenačte, tiše zmizí a hráči zbude zařazení
            autora; inkoust za ni ale propadá, proto se nabízí až jako první
            a nejlevnější stupeň. */}
        {seenArt && (
          <figure className="quote-art">
            <img
              src={artUrl(quote.art!)}
              alt=""
              loading="lazy"
              onError={() => {
                // Bez sítě (nebo když soubor na Commons zmizel) hráč zaplatil
                // za nic. Místo podobizny proto dostane další stupeň zadarmo.
                setArtFailed(true)
                setState((current) => {
                  const swap: QuoteHint = quote.note && !current.hints.includes('note')
                    ? 'note'
                    : 'who'
                  return current.hints.includes(swap)
                    ? current
                    : { ...current, hints: [...current.hints, swap] }
                })
                showFlash('Podobizna nedorazila — další nápovědu máš zdarma.', 'warn')
              }}
            />
            <figcaption>
              Podobizna:{' '}
              <a
                href={`https://commons.wikimedia.org/wiki/File:${encodeURIComponent(quote.art!)}`}
                target="_blank"
                rel="noreferrer"
              >
                Wikimedia Commons
              </a>
            </figcaption>
          </figure>
        )}

        <blockquote className="quote-text">
          {parts.map((token, index) =>
            token.word ? (
              <span className="quote-word" key={index}>
                {[...token.text].map((letter, i) => {
                  const open =
                    state.given.includes(index) ||
                    state.tried.includes(
                      letter.toLowerCase().normalize('NFD').replace(/\p{M}/gu, ''),
                    )
                  return (
                    <span className={`quote-slot ${open ? 'open' : ''}`} key={i}>
                      {open || over ? letter : '\u00A0'}
                    </span>
                  )
                })}
              </span>
            ) : (
              <span
                className={`quote-gap ${token.text.trim() === '' ? 'space' : 'punct'}`}
                key={index}
              >
                {token.text.trim() === '' ? '' : token.text}
              </span>
            ),
          )}
        </blockquote>

        <p className="quote-who">
          {seenWho ? quote.who : seenNote && quote.note ? quote.note : '— ?'}
        </p>
      </div>

      <div className="board-footer">
        <div className="letter-keys">
          {ROWS.map((row, r) => (
            <div className="letter-row" key={r}>
              {row.map((key) => {
                const tried = state.tried.includes(key)
                const hit = tried && countLetter({ ...state, tried: [] }, key) > 0
                return (
                  <button
                    type="button"
                    key={key}
                    className={`letter-key ${hit ? 'hit' : tried ? 'miss' : ''}`}
                    disabled={tried || over}
                    onClick={() => press(key)}
                  >
                    {key}
                  </button>
                )
              })}
            </div>
          ))}
        </div>

        <div className="board-actions">
          <button
            type="button"
            className="btn btn-sm btn-ghost"
            onClick={() => setConfirmGiveUp(true)}
            disabled={over}
          >
            Vzdát kolo
          </button>
        </div>
      </div>

      <aside className="rail rail-right">
        <p className="faint" style={{ fontSize: '0.82rem', lineHeight: 1.55 }}>
          Výroky pocházejí z Wikicitátů. Část slov dostaneš zadarmo, zbytek
          se odkrývá po písmenech. Chyba kolo neukončí, jen stojí body — a
          nápovědy jdou od nejmlhavější k nejkonkrétnější.
        </p>
      </aside>

      {confirmGiveUp && (
        <Confirm
          title="Vzdát kolo?"
          body="Výrok zůstane nedoplněný a série se přeruší. Vrátit to nepůjde."
          confirmLabel="Vzdát kolo"
          onConfirm={onGiveUp}
          onCancel={() => setConfirmGiveUp(false)}
        />
      )}

      {done && (
        <ResultOverlay
          title={won ? 'Výrok doplněn!' : 'Výrok zůstal němý'}
          subtitle={quote.who}
          breakdown={breakdown}
          shareText={shareText}
          celebrate={won}
          onNext={onNext}
          onHome={onHome}
        >
          <p className="clue-recap">„{quote.text}"</p>
        </ResultOverlay>
      )}
    </div>
  )
}
