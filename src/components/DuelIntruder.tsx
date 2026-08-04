/**
 * Souboj ve Vetřelci — tři stejné pětice, každý kdy chce.
 *
 * Živě se tu nemá co dít: soupeři nejde nic sebrat a nic mu neuteče.
 * Proto se nečeká, hraje se rovnou a porovnají se až hotové výsledky —
 * trefa a k ní čas, který si každý sám naměří.
 */

import { useEffect, useRef, useState } from 'react'

import { duelRoundScore, INTRUDER_DUEL_MAX, type Verdict } from '../game/duel'
import type { IntruderPuzzle } from '../game/intruder'
import { finishMatch, type Match } from '../lib/multi'
import { DuelEnd } from './DuelEnd'

interface Props {
  match: Match
  puzzles: IntruderPuzzle[]
  uid: string
  nick: string
  onHome: () => void
  onVerdict: (verdict: Verdict) => void
}

export function DuelIntruder({ match, puzzles, uid, nick, onHome, onVerdict }: Props) {
  const [round, setRound] = useState(0)
  const [picked, setPicked] = useState<string | null>(null)
  const [total, setTotal] = useState(0)
  const [gain, setGain] = useState(0)
  const [over, setOver] = useState(false)
  const started = useRef(Date.now())

  const puzzle = puzzles[round]!
  const right = picked === puzzle.odd

  useEffect(() => {
    started.current = Date.now()
  }, [round])

  const sent = useRef(false)
  useEffect(() => {
    if (!over || sent.current) return
    sent.current = true
    void finishMatch(match.id, nick, total)
  }, [match.id, nick, over, total])

  function pick(word: string) {
    if (picked) return
    const points = duelRoundScore(word === puzzle.odd, Date.now() - started.current)
    setPicked(word)
    setGain(points)
    setTotal((sum) => sum + points)
  }

  function next() {
    if (round + 1 >= puzzles.length) {
      setOver(true)
      return
    }
    setRound((index) => index + 1)
    setPicked(null)
    setGain(0)
  }

  const rival = match.host === uid ? match.guestNick : match.hostNick

  return (
    <div className="game duel-game">
      <div className="duel-bar">
        <span className="duel-side me">
          <span className="duel-name">proti {rival}</span>
          <span className="num">{total}</span>
        </span>
        <span className="duel-clock">
          {round + 1}. kolo ze {puzzles.length}
        </span>
        <span className="duel-side">
          <span className="duel-name">nejvíc</span>
          <span className="num">{INTRUDER_DUEL_MAX}</span>
        </span>
      </div>

      <div className="board">
        <p className="intruder-ask">Které slovo do pětice nepatří?</p>

        <div className="intruder-words">
          {puzzle.words.map((word) => (
            <button
              type="button"
              key={word}
              className={`intruder-word ${picked === word ? 'mine' : ''} ${
                picked && word === puzzle.odd ? 'truth' : ''
              } ${picked === word && !right ? 'wrong' : ''}`}
              disabled={picked !== null}
              onClick={() => pick(word)}
            >
              {word}
            </button>
          ))}
        </div>

        {picked && (
          <div className="duel-round-end">
            <p className={`duel-verdict ${right ? 'ok' : 'bad'}`}>
              {right ? `Trefa · +${gain}` : 'Vedle · 0'}
            </p>
            <p className="clue-recap">{puzzle.recap}</p>
            <button type="button" className="btn btn-primary" onClick={next}>
              {round + 1 >= puzzles.length ? 'Vyhodnotit souboj' : 'Další kolo'}
            </button>
          </div>
        )}
      </div>

      {over && (
        <DuelEnd
          match={match}
          uid={uid}
          mine={total}
          note={`${total} bodů ze tří kol`}
          onHome={onHome}
          onVerdict={onVerdict}
        />
      )}
    </div>
  )
}
