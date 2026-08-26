/**
 * Souboj ve Voštině — jedna plástev, tři minuty, dva lidé naráz.
 *
 * Proti běžnému kolu se liší v jediné podstatné věci: slova jsou společná.
 * Kdo je odevzdá dřív, tomu patří — druhému za ně nepadne nic a v seznamu
 * mu zšedne. Proto tady nejsou nápovědy ani inkoust; napovídat v souboji
 * o čas by nedávalo smysl.
 */

import { useCallback, useEffect, useMemo, useRef, useState } from 'react'

import {
  claimKey,
  HIVE_DUEL_MS,
  HIVE_DUEL_WARN_MS,
  verdictOf,
  type Verdict,
} from '../game/duel'
import {
  createHiveState,
  HIVE_ERROR_TEXT,
  letterSet,
  submitWord,
  wordScore,
  type HivePuzzle,
  type HiveState,
} from '../game/hive'
import { fold } from '../lib/czech'
import {
  cancelMatch,
  claimWord,
  finishMatch,
  pingMatch,
  serverNow,
  watchMatch,
  watchWords,
  type Match,
} from '../lib/multi'
import { DuelEnd } from './DuelEnd'
import { RivalChip } from './RivalChip'

interface Props {
  match: Match
  puzzle: HivePuzzle
  /** Moje skryté id — podle něj se v mapě pozná, co je čí. */
  uid: string
  nick: string
  onHome: () => void
  onVerdict: (verdict: Verdict, mine: number) => void
  /** Odveta se stejným soupeřem, aby se přezdívka nemusela psát znovu. */
  onRematch?: () => Promise<boolean>
}

const RING = [
  { left: '33.5%', top: '0%' },
  { left: '67%', top: '16.9%' },
  { left: '67%', top: '50.7%' },
  { left: '33.5%', top: '67.6%' },
  { left: '0%', top: '50.7%' },
  { left: '0%', top: '16.9%' },
]

const CENTER = { left: '33.5%', top: '33.8%' }

export function DuelHive({ match, puzzle, uid, nick, onHome, onVerdict, onRematch }: Props) {
  const [live, setLive] = useState(match.live)
  const [owners, setOwners] = useState<Record<string, string>>({})
  const [state, setState] = useState<HiveState>(() => createHiveState(puzzle))
  const [draft, setDraft] = useState('')
  const [flash, setFlash] = useState<{ text: string; tone: string; key: number } | null>(null)
  const [left, setLeft] = useState(HIVE_DUEL_MS)
  const [over, setOver] = useState(false)
  const rival = match.host === uid ? match.guestNick : match.hostNick
  const rivalUid = match.host === uid ? match.guest : match.host
  const host = match.host === uid

  const letters = useMemo(() => letterSet(puzzle), [puzzle])

  /** Skupiny řešení podle složeného tvaru — z nich se počítají body za klíč. */
  const groups = useMemo(() => {
    const out = new Map<string, string[]>()
    for (const word of puzzle.solutions) {
      const key = fold(word)
      const group = out.get(key)
      if (group) group.push(word)
      else out.set(key, [word])
    }
    return out
  }, [puzzle.solutions])

  const keyScore = useCallback(
    (key: string) =>
      (groups.get(key) ?? []).reduce((sum, word) => sum + wordScore(puzzle, word), 0),
    [groups, puzzle],
  )

  useEffect(() => watchMatch(match.id, (next) => next && setLive(next.live)), [match.id])
  useEffect(() => watchWords(match.id, setOwners), [match.id])

  // Dokud vyzývatel čeká, dává o sobě vědět. Soupeř podle toho pozná, že
  // výzva je živá a nemá cenu přijímat něco, u čeho už nikdo nesedí.
  useEffect(() => {
    if (!host || live !== 0) return
    void pingMatch(match.id)
    const id = setInterval(() => void pingMatch(match.id), 5000)
    return () => clearInterval(id)
  }, [host, live, match.id])

  // Odpočet. Počítá se z času serveru, ne z hodin telefonu — jinak by
  // každému běžely tři minuty jinak dlouho.
  useEffect(() => {
    if (live <= 0 || over) return
    const ends = live + HIVE_DUEL_MS
    const tick = () => setLeft(Math.max(0, ends - serverNow()))
    tick()
    const id = setInterval(tick, 250)
    return () => clearInterval(id)
  }, [live, over])

  const points = useMemo(
    () =>
      Object.entries(owners)
        .filter(([, who]) => who === uid)
        .reduce((sum, [key]) => sum + keyScore(key), 0),
    [keyScore, owners, uid],
  )
  const rivalPoints = useMemo(
    () =>
      Object.entries(owners)
        .filter(([, who]) => who !== uid)
        .reduce((sum, [key]) => sum + keyScore(key), 0),
    [keyScore, owners, uid],
  )

  // Konec kola. Výsledek se zapíše jen jednou; obě strany dopočítají totéž
  // ze společné mapy, takže se nemají jak rozejít.
  const sent = useRef(false)
  useEffect(() => {
    if (left > 0 || live <= 0 || sent.current) return
    sent.current = true
    setOver(true)
    void finishMatch(match.id, nick, points)
  }, [left, live, match.id, nick, points])

  const showFlash = useCallback((text: string, tone: string) => {
    setFlash({ text, tone, key: Date.now() })
  }, [])

  const submit = useCallback(async () => {
    if (!draft || over || live <= 0) return
    const result = submitWord(state, draft)
    if (!result.ok) {
      showFlash(HIVE_ERROR_TEXT[result.error], 'error')
      setDraft('')
      if (navigator.vibrate) navigator.vibrate(40)
      return
    }
    const key = claimKey(result.word)
    setDraft('')
    if (owners[key]) {
      showFlash(`${result.word.toUpperCase()} — tohle už sebral ${rival}`, 'warn')
      return
    }
    const mine = await claimWord(match.id, key)
    if (!mine) {
      showFlash(`${result.word.toUpperCase()} — o vteřinu dřív byl ${rival}`, 'warn')
      return
    }
    setState(result.state)
    if (result.pangram) {
      showFlash(`PANGRAM! ${result.word.toUpperCase()} · +${result.points}`, 'accent')
      if (navigator.vibrate) navigator.vibrate([30, 40, 60])
    } else {
      showFlash(`${result.word.toUpperCase()} · +${result.points}`, 'accent')
    }
  }, [draft, live, match.id, over, owners, rival, showFlash, state])

  const type = (letter: string) =>
    setDraft((previous) => (previous.length < 16 ? previous + letter : previous))

  if (live === 0) {
    return (
      <div className="game duel-wait">
        <div className="card duel-wait-card">
          <span className="duel-mark big" aria-hidden="true">
            ⚔
          </span>
          <h2>Čekám na soupeře</h2>
          <p className="muted">
            {rival} má výzvu v menu. Voština se rozjede, jakmile ji přijme —
            hraje se tři minuty a oba naráz, takže na sebe musíte počkat.
          </p>
          <span className="spinner" />
          <div className="sheet-actions">
            <button
              type="button"
              className="btn btn-ghost"
              onClick={() => {
                void cancelMatch(match.id)
                onHome()
              }}
            >
              Zrušit výzvu
            </button>
          </div>
        </div>
      </div>
    )
  }

  if (live < 0) {
    return (
      <div className="game duel-wait">
        <div className="card duel-wait-card">
          <h2>Výzva byla odvolána</h2>
          <p className="muted">{rival} už u ní neseděl.</p>
          <div className="sheet-actions">
            <button type="button" className="btn btn-primary" onClick={onHome}>
              Zpět do menu
            </button>
          </div>
        </div>
      </div>
    )
  }

  const seconds = Math.ceil(left / 1000)
  const clock = `${Math.floor(seconds / 60)}:${String(seconds % 60).padStart(2, '0')}`
  const mineWords = [...state.found].sort(
    (a, b) => b.length - a.length || a.localeCompare(b, 'cs'),
  )
  const stolen = Object.entries(owners).filter(([, who]) => who !== uid).length

  return (
    <div className="game duel-game">
      <div className="duel-bar">
        <span className="duel-side me">
          <span className="duel-name">{nick}</span>
          <span className="num">{points}</span>
        </span>
        <span className={`duel-clock num ${left <= HIVE_DUEL_WARN_MS ? 'urgent' : ''}`}>
          {clock}
        </span>
        <span className="duel-side">
          <span className="duel-name">
            <RivalChip uid={rivalUid} nick={rival} />
          </span>
          <span className="num">{rivalPoints}</span>
        </span>
      </div>

      <div className="board">
        <div className="quote-strip">
          {flash && (
            <div className={`banner banner-${flash.tone}`} key={flash.key}>
              <span>{flash.text}</span>
            </div>
          )}
        </div>

        <div className="hive-wrap">
          <div className="hive-input">
            {draft.length === 0 && <span className="faint">Piš slovo…</span>}
            {[...draft].map((ch, i) => {
              const folded = fold(ch)
              return (
                <span
                  key={i}
                  className={`ch ${folded === puzzle.center ? 'center' : ''} ${
                    letters.has(folded) ? '' : 'bad'
                  }`}
                >
                  {ch}
                </span>
              )
            })}
            <span className="cursor" />
          </div>

          <div className="hive">
            <button
              type="button"
              className="hex center"
              style={CENTER}
              onClick={() => type(puzzle.center)}
            >
              {puzzle.center}
            </button>
            {state.ring.map((letter, i) => (
              <button
                type="button"
                key={letter}
                className="hex"
                style={RING[i]}
                onClick={() => type(letter)}
              >
                {letter}
              </button>
            ))}
          </div>
        </div>
      </div>

      <div className="board-footer">
        <div className="duel-keys">
          <button
            type="button"
            className="btn"
            onClick={() => setDraft((previous) => previous.slice(0, -1))}
          >
            Smazat
          </button>
          <button
            type="button"
            className="btn"
            onClick={() => setState((previous) => ({ ...previous, ring: shuffle(previous.ring) }))}
          >
            Zamíchat
          </button>
          <button type="button" className="btn btn-primary" onClick={() => void submit()}>
            Potvrdit
          </button>
        </div>
        <p className="faint duel-found">
          {mineWords.length === 0
            ? 'Zatím nic — začni čtyřpísmenným slovem.'
            : mineWords.join(' · ')}
          {stolen > 0 && <em> · soupeři patří {stolen}</em>}
        </p>
      </div>

      {over && (
        <DuelEnd
          match={match}
          uid={uid}
          mine={points}
          fallback={{ nick: rival, score: rivalPoints }}
          verdict={verdictOf(points, rivalPoints)}
          note={`${mineWords.length} slov · ${points} bodů z plástve`}
          onHome={onHome}
          onVerdict={onVerdict}
          {...(onRematch ? { onRematch } : {})}
        />
      )}
    </div>
  )
}

function shuffle(items: string[]): string[] {
  const out = [...items]
  for (let i = out.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1))
    ;[out[i], out[j]] = [out[j]!, out[i]!]
  }
  return out
}
