/**
 * Obrazovka OTÁZKY DNE.
 *
 * Dvě fáze a mezi nimi jedno rozhodnutí, na kterém stojí celá hra. Nejdřív
 * hráč vidí **jen nadpis** a sází, kolik indicií bude potřebovat; teprve pak
 * se odkrývá. Sázka se dělá naslepo, a proto je za jednu indicii trojnásobná
 * odměna — jinak by si každý vzal všechny tři a nebylo by co řešit.
 *
 * Odkryté indicie zůstávají na obrazovce a nová se přidává pod ně, takže hráč
 * vidí, jak se kruh svírá. Zamčenou třetí je vidět jako zavřený řádek, ne jako
 * prázdno — kdo si ji nekoupil, má vědět, co si nekoupil.
 */

import { useCallback, useEffect, useRef, useState } from 'react'

import {
  buyClues,
  consolationFor,
  createQuizState,
  giveUpQuiz,
  guess as guessAnswer,
  isOver,
  QUIZ_REWARD,
  QUIZ_TRIES,
  quizReward,
  revealClue,
  TOPIC_LABEL,
  triesLeft,
  type QuizQuestion,
  type QuizState,
} from '../game/quiz'
import { useBackGuard } from '../lib/back'
import { InkMark } from './art/InkMark'
import { Confirm } from './Confirm'
import { Explain } from './Explain'

interface Props {
  question: QuizQuestion
  /** Označení dne — vybírá i větu na rozloučenou, ať se neopakuje. */
  day: number
  dayLabel: string
  onFinish: (outcome: { solved: boolean; clues: number; ink: number }) => void
  onHome: () => void
}

/** Kolik teček nese indicie — stejná řeč jako na kartách: víc teček, víc bodů. */
function Pips({ count }: { count: number }) {
  return (
    <span className="quiz-pips" aria-hidden="true">
      {Array.from({ length: count }, (_, i) => (
        <i key={i} />
      ))}
    </span>
  )
}

export function QuizGame({ question, day, dayLabel, onFinish, onHome }: Props) {
  const [state, setState] = useState<QuizState>(() => createQuizState(question))
  const [draft, setDraft] = useState('')
  const [flash, setFlash] = useState<{ text: string; key: number } | null>(null)
  const [confirmGiveUp, setConfirmGiveUp] = useState(false)
  const input = useRef<HTMLInputElement | null>(null)
  const reported = useRef(false)

  const over = isOver(state)
  const left = triesLeft(state)

  // Kolo se hlásí právě jednou, hned jak skončí.
  useEffect(() => {
    if (!over || reported.current) return
    reported.current = true
    onFinish({
      solved: state.solved,
      clues: state.bought ?? 3,
      ink: quizReward(state),
    })
  }, [over, state, onFinish])

  useBackGuard(confirmGiveUp, () => setConfirmGiveUp(false))

  const showFlash = useCallback((text: string) => {
    setFlash({ text, key: Date.now() })
  }, [])

  const submit = useCallback(() => {
    if (over || state.bought === null) return
    const clean = draft.trim()
    if (clean === '') return
    const outcome = guessAnswer(state, clean)
    setState(outcome.state)
    setDraft('')
    if (!outcome.correct && !outcome.lost) {
      showFlash(
        outcome.state.tried.length === QUIZ_TRIES - 1
          ? 'Vedle. Zbývá poslední pokus.'
          : 'Vedle. Zkus to znovu.',
      )
    }
  }, [draft, over, showFlash, state])

  function pick(count: number) {
    setState((previous) => buyClues(previous, count))
    // Pole se zaostří až po překreslení, jinak se na telefonu klávesnice
    // otevře dřív, než je kam psát.
    setTimeout(() => input.current?.focus(), 60)
  }

  const reward = state.bought === null ? 0 : QUIZ_REWARD[state.bought]!

  return (
    <div className="game quiz">
      <div className="quiz-card panel">
        <div className="quiz-head">
          <span className="chip chip-gold">Otázka dne {dayLabel}</span>
          <span className="chip">{TOPIC_LABEL[question.topic]}</span>
        </div>

        <h1 className="quiz-ask">{question.ask}</h1>

        {state.bought === null ? (
          <div className="quiz-bet">
            <p className="muted">
              Kolik indicií si vezmeš? Čím méně, tím větší odměna — a rozhodnout
              se musíš teď, než uvidíš první z nich.
            </p>
            <div className="quiz-bet-row">
              {[1, 2, 3].map((count) => (
                <button
                  type="button"
                  key={count}
                  className="quiz-bet-tile"
                  onClick={() => pick(count)}
                >
                  <Pips count={4 - count} />
                  <span className="quiz-bet-count">
                    {count === 1 ? '1 indicie' : count === 2 ? '2 indicie' : '3 indicie'}
                  </span>
                  <span className="quiz-bet-reward num">
                    <InkMark size={13} /> {QUIZ_REWARD[count]}
                  </span>
                  <small className="faint">
                    {count === 1
                      ? 'jen ta nejtěžší'
                      : count === 2
                        ? 'i ta prostřední'
                        : 'včetně návodné'}
                  </small>
                </button>
              ))}
            </div>
            <Explain term="otazka" className="faint quiz-note">
              Jak Otázka dne funguje
            </Explain>
          </div>
        ) : (
          <>
            <ol className="quiz-clues">
              {question.clues.slice(0, state.bought).map((clue, i) => {
                const open = i < state.shown
                return (
                  <li key={i} className={open ? 'open' : ''}>
                    <Pips count={3 - i} />
                    <span>{open ? clue : 'Zatím zavřená indicie'}</span>
                  </li>
                )
              })}
            </ol>

            {!over && state.shown < state.bought && (
              <button
                type="button"
                className="btn btn-sm"
                onClick={() => setState(revealClue)}
              >
                Odkrýt další indicii
              </button>
            )}

            {!over && (
              <div className="quiz-answer">
                <div className="guess-row">
                  <input
                    ref={input}
                    className="guess-input"
                    value={draft}
                    onChange={(event) => setDraft(event.target.value)}
                    onKeyDown={(event) => {
                      if (event.key === 'Enter') {
                        event.preventDefault()
                        submit()
                      }
                    }}
                    placeholder="Tvoje odpověď"
                    aria-label="Odpověď"
                    autoComplete="off"
                    autoCapitalize="off"
                    spellCheck={false}
                  />
                  <button type="button" className="btn btn-primary" onClick={submit}>
                    Odpovědět
                  </button>
                </div>
                <div className="quiz-meta">
                  <span className="faint">
                    {left === 1 ? 'Poslední pokus' : `Zbývají ${left} pokusy`}
                  </span>
                  <span className="chip chip-ink">
                    <InkMark size={11} /> <span className="num">{reward}</span>
                  </span>
                </div>
                {state.tried.length > 0 && (
                  <div className="quiz-tried">
                    {state.tried.map((word, i) => (
                      <span className="chip" key={i}>
                        {word}
                      </span>
                    ))}
                  </div>
                )}
                {flash && (
                  <div className="banner banner-warn" key={flash.key}>
                    {flash.text}
                  </div>
                )}
              </div>
            )}
          </>
        )}

        {over && (
          <div className={`quiz-result ${state.solved ? 'won' : 'lost'}`}>
            <h2>{state.solved ? 'Trefa!' : 'Správně bylo'}</h2>
            <p className="quiz-answer-text">{question.answer}</p>
            {state.solved ? (
              <p className="quiz-prize">
                <InkMark size={16} /> <span className="num">+{quizReward(state)}</span> inkoustu
                {state.bought === 1 && ' — a to na jedinou indicii'}
              </p>
            ) : (
              <p className="muted">{consolationFor(day)}</p>
            )}
            {/* Indicie, které si hráč nekoupil, se ukážou až teď. Je to
                půlka radosti: „aha, tohle jsem měl vědět." */}
            {question.clues.length > (state.bought ?? 3) && (
              <ol className="quiz-clues rest">
                {question.clues.slice(state.bought ?? 3).map((clue, i) => (
                  <li key={i} className="open">
                    <Pips count={3 - (state.bought ?? 3) - i} />
                    <span>{clue}</span>
                  </li>
                ))}
              </ol>
            )}
            <p className="faint">Další otázka na tebe čeká zítra.</p>
            <button type="button" className="btn btn-primary" onClick={onHome}>
              Zpět do menu
            </button>
          </div>
        )}

        {!over && state.bought !== null && (
          <button
            type="button"
            className="btn btn-sm btn-ghost quiz-give-up"
            onClick={() => setConfirmGiveUp(true)}
          >
            Vzdát to
          </button>
        )}
      </div>

      {confirmGiveUp && (
        <Confirm
          title="Vzdát otázku?"
          body="Uvidíš správnou odpověď, ale žádný inkoust nepadne — a další otázka je až zítra."
          confirmLabel="Vzdát"
          onCancel={() => setConfirmGiveUp(false)}
          onConfirm={() => {
            setConfirmGiveUp(false)
            setState(giveUpQuiz)
          }}
        />
      )}
    </div>
  )
}
