/**
 * Přehled všech otázek — jen v kontrolním buildu.
 *
 * Otázky se v ostré hře odemykají po jedné denně a hádat se přes dvě stovky,
 * jen aby se daly přečíst, je nesmysl. Tahle obrazovka je vysype všechny
 * naráz i s odpověďmi, seřazené po oborech a v tom pořadí, ve kterém je
 * dostanou hráči — takže je vidět i to, jestli se sousedním dnům netrefila
 * dvě podobná zadání.
 *
 * Do ostré hry se nedostane: `App.tsx` ji vykresluje jen pod `__QUIZ_ALL__`,
 * takže ji vite z ostrého buildu vyhodí i s daty.
 */

import { useMemo, useState } from 'react'

import {
  QUIZ_TOPICS,
  quizFor,
  TOPIC_LABEL,
  type QuizDeck,
  type QuizQuestion,
  type QuizTopic,
} from '../game/quiz'

interface Props {
  deck: QuizDeck
  /** Číslo dnešního dne — podle něj se pozná, na kterou otázku právě došlo. */
  today: number
  onBack: () => void
}

/** Otázka i s dnem, na který v pořadí připadne. */
interface Dated {
  question: QuizQuestion
  day: number
}

function Pips({ count }: { count: number }) {
  return (
    <span className="quiz-pips" aria-hidden="true">
      {Array.from({ length: count }, (_, i) => (
        <i key={i} />
      ))}
    </span>
  )
}

export function QuizReview({ deck, today, onBack }: Props) {
  const [topic, setTopic] = useState<QuizTopic | 'vse'>('vse')
  /** Odkryté odpovědi. Kdo si chce otázku nejdřív zkusit, nechá je zavřené. */
  const [open, setOpen] = useState<Set<string>>(new Set())
  const [showAnswers, setShowAnswers] = useState(true)

  /**
   * Otázky v pořadí, ve kterém na ně dojde řada.
   *
   * Nebere se pořadí z dat, ale to, co doopravdy uvidí hráč — obory se
   * střídají kolečkem a uvnitř oboru je pořadí zamíchané, takže seznam
   * z dat by ukazoval něco jiného než hra.
   */
  const timeline = useMemo<Dated[]>(() => {
    const total = QUIZ_TOPICS.reduce((sum, key) => sum + (deck[key]?.length ?? 0), 0)
    const seen = new Set<string>()
    const out: Dated[] = []
    for (let day = 0; out.length < total && day < total * 4; day += 1) {
      const question = quizFor(deck, day)
      if (!question || seen.has(question.id)) continue
      seen.add(question.id)
      out.push({ question, day })
    }
    return out
  }, [deck])

  const shown = timeline.filter((row) => topic === 'vse' || row.question.topic === topic)

  function toggle(id: string) {
    setOpen((was) => {
      const next = new Set(was)
      if (next.has(id)) next.delete(id)
      else next.add(id)
      return next
    })
  }

  return (
    <>
      <div className="section-head" style={{ marginTop: 0 }}>
        <h2>Všechny otázky</h2>
        <span className="rule" />
        <button type="button" className="btn btn-sm" onClick={onBack}>
          Zpět
        </button>
      </div>

      <p className="muted" style={{ marginBottom: 'var(--sp-3)' }}>
        {timeline.length} otázek v pořadí, ve kterém na ně dojde řada. Číslo
        u otázky je den, na který připadne — dnešek je #{today}.
      </p>

      <div className="review-bar">
        <div className="seg seg-wide">
          <button
            type="button"
            aria-pressed={showAnswers}
            onClick={() => setShowAnswers(true)}
          >
            S odpověďmi
          </button>
          <button
            type="button"
            aria-pressed={!showAnswers}
            onClick={() => setShowAnswers(false)}
          >
            Zakryté
          </button>
        </div>
      </div>

      <div className="review-topics">
        <button
          type="button"
          className={`chip ${topic === 'vse' ? 'chip-accent' : ''}`}
          onClick={() => setTopic('vse')}
        >
          Vše ({timeline.length})
        </button>
        {QUIZ_TOPICS.map((key) => (
          <button
            type="button"
            key={key}
            className={`chip ${topic === key ? 'chip-accent' : ''}`}
            onClick={() => setTopic(key)}
          >
            {TOPIC_LABEL[key]} ({deck[key]?.length ?? 0})
          </button>
        ))}
      </div>

      <div className="review-list">
        {shown.map(({ question, day }) => {
          const revealed = showAnswers || open.has(question.id)
          return (
            <article className="review-item panel" key={question.id}>
              <div className="review-head">
                <span className="chip">{TOPIC_LABEL[question.topic]}</span>
                <span className="faint num">
                  #{day} · {question.id}
                </span>
                {day === today && <span className="chip chip-gold">dnes</span>}
              </div>
              <h3>{question.ask}</h3>
              <ol className="quiz-clues">
                {question.clues.map((clue, i) => (
                  <li key={i} className="open">
                    <Pips count={3 - i} />
                    <span>{clue}</span>
                  </li>
                ))}
              </ol>
              <button
                type="button"
                className={`review-answer ${revealed ? 'open' : ''}`}
                onClick={() => toggle(question.id)}
              >
                {revealed ? question.answer : 'Ukázat odpověď'}
              </button>
              {revealed && question.alt && question.alt.length > 0 && (
                <p className="faint">
                  Uzná se také: {question.alt.join(', ')}
                </p>
              )}
            </article>
          )
        })}
      </div>
    </>
  )
}
