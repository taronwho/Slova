/**
 * Souboj ve Vetřelci — tři stejné pětice, každý kdy chce.
 *
 * Živě se tu nemá co dít: soupeři nejde nic sebrat a nic mu neuteče.
 * Proto se nečeká, hraje se rovnou a porovnají se až hotové výsledky —
 * trefa a k ní čas, který si každý sám naměří.
 */

import { useEffect, useRef, useState } from 'react'

import { duelRoundScore, INTRUDER_DUEL_MAX, type Verdict } from '../game/duel'
import { encodeSteps, type DuelStep } from '../game/duelDetail'
import type { IntruderPuzzle } from '../game/intruder'
import { finishMatch, type Match, type MatchScore } from '../lib/multi'
import { DuelEnd } from './DuelEnd'
import { RivalChip } from './RivalChip'

interface Props {
  match: Match
  puzzles: IntruderPuzzle[]
  uid: string
  nick: string
  /** Moje soubojová hodnost — erb v porovnání na konci. */
  rank?: number
  onHome: () => void
  onVerdict: (
    verdict: Verdict,
    mine: number,
    souper: MatchScore,
    mujRozpis?: string,
  ) => void
  /** Odveta se stejným soupeřem, aby se přezdívka nemusela psát znovu. */
  onRematch?: () => Promise<boolean>
}

export function DuelIntruder({
  match,
  puzzles,
  uid,
  nick,
  rank = 0,
  onHome,
  onVerdict,
  onRematch,
}: Props) {
  const [round, setRound] = useState(0)
  const [picked, setPicked] = useState<string | null>(null)
  const [total, setTotal] = useState(0)
  const [gain, setGain] = useState(0)
  const [over, setOver] = useState(false)
  const started = useRef(Date.now())

  const puzzle = puzzles[round]!
  const right = picked === puzzle.odd

  /*
   * Rozpis kol pro porovnání se soupeřem.
   *
   * Drží se v ref, ne ve stavu: nic se z něj během hry nekreslí a překreslovat
   * plochu kvůli zápisu do archivu by bylo zbytečné.
   */
  const kroky = useRef<DuelStep[]>([])
  const [rozpis, setRozpis] = useState('')

  useEffect(() => {
    started.current = Date.now()
  }, [round])

  const sent = useRef(false)
  useEffect(() => {
    if (!over || sent.current) return
    sent.current = true
    const text = encodeSteps(kroky.current)
    setRozpis(text)
    void finishMatch(match.id, nick, total, text)
  }, [match.id, nick, over, total])

  function pick(word: string) {
    if (picked) return
    const ms = Date.now() - started.current
    const points = duelRoundScore(word === puzzle.odd, ms)
    kroky.current.push({ word, ms, points, odd: puzzle.odd })
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
  const rivalUid = match.host === uid ? match.guest : match.host

  return (
    <div className="game duel-game">
      <div className="duel-bar">
        <span className="duel-side me">
          <span className="duel-name">
            proti <RivalChip uid={rivalUid} nick={rival} />
          </span>
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
          nick={nick}
          mine={total}
          detail={rozpis}
          rank={rank}
          onHome={onHome}
          onVerdict={onVerdict}
          {...(onRematch ? { onRematch } : {})}
        />
      )}
    </div>
  )
}
