/**
 * Porovnání souboje — kdo, co, kdy a za kolik.
 *
 * Souboj končil jedním číslem proti druhému a tím to haslo. Jenže „412 : 430"
 * neřekne nic o tom, kde se to zlomilo: jestli soupeř věděl víc, nebo jen
 * jednou nezaváhal. Tahle obrazovka to rozepíše po kolech a postaví obě
 * strany vedle sebe.
 *
 * Ukazuje se na třech místech a všude stejná:
 *
 * - hned po dohrání tomu, kdo hrál **druhý** — má obě strany,
 * - hned po dohrání tomu, kdo hrál **první** — má zatím jen svoji a místo
 *   soupeřovy sloupec čekání,
 * - kdykoli později z přehledu odehraných soubojů.
 *
 * Rozpis je nepovinný (viz `game/duelDetail`): když ho soupeř neposlal,
 * zůstane porovnání u součtů a nic se nerozbije.
 */

import { useMemo } from 'react'

import {
  DUEL_MODE,
  DUEL_TITLE,
  INTRUDER_DUEL_MAX,
  VERDICT_TITLE,
  verdictLine,
  type DuelKind,
  type Verdict,
} from '../game/duel'
import { decodeSteps, stepTime, type DuelStep } from '../game/duelDetail'
import { MODE_GLYPH } from '../game/types'
import type { KartaHrace } from '../lib/multi'
import { DuelCrest } from './art/DuelCrest'
import { RivalChip } from './RivalChip'

export interface DuelStrana {
  nick: string
  score: number
  /** Zakódovaný rozpis. Chybí, když ho hráč neposlal. */
  detail?: string | undefined
  /** Soubojová hodnost pro erb. 0 = neznámá, erb se nekreslí. */
  rank?: number
  /** Skryté id — podle něj se karta hráče načte ze serveru. */
  uid?: string | undefined
}

interface Props {
  /** Id zápasu. Vybírá se podle něj hláška, ať je pořád tatáž. */
  id: string
  kind: DuelKind
  me: DuelStrana
  /** Soupeř, nebo null, dokud nedohrál. */
  rival: DuelStrana | null
  /** Přezdívka soupeře. Zná se ze zápasu i dřív, než dohraje. */
  rivalNick: string
  /** Verdikt. Null znamená „ještě se čeká". */
  verdict: Verdict | null
  /**
   * Skryté id soupeře. Zná se ze zápasu i dřív, než dohraje — díky tomu se
   * dá jeho karta otevřít i ze strany, kde se zatím čeká.
   */
  rivalUid?: string | undefined
  /**
   * Moje karta, hotová z telefonu.
   *
   * Na vlastní profil se má dát ťuknout stejně jako na soupeřův. Data jsou
   * po ruce, takže se kvůli tomu nikam nechodí.
   */
  mojeKarta?: KartaHrace | undefined
}

/** Čas od začátku plástve: 1:07. */
function hiveTime(ms: number): string {
  if (ms <= 0) return '—'
  const s = Math.round(ms / 1000)
  return `${Math.floor(s / 60)}:${String(s % 60).padStart(2, '0')}`
}

export function DuelReport({
  id,
  kind,
  me,
  rival,
  rivalNick,
  verdict,
  rivalUid,
  mojeKarta,
}: Props) {
  const mine = useMemo(() => decodeSteps(me.detail), [me.detail])
  const theirs = useMemo(() => decodeSteps(rival?.detail), [rival?.detail])

  const rozdil = rival ? Math.abs(me.score - rival.score) : 0
  /** Id soupeře — ze zápasu i z archivu; podle něj se otevírá jeho karta. */
  const kdo = rival?.uid ?? rivalUid

  return (
    <div className={`rozbor ${verdict ?? 'ceka'}`}>
      <div className="rozbor-head">
        <span className="rozbor-mode" style={{ ['--tint' as string]: `var(--mode-${DUEL_MODE[kind]})` }}>
          <span aria-hidden="true">{MODE_GLYPH[DUEL_MODE[kind]]}</span>
          {DUEL_TITLE[kind]}
        </span>
        <h2>{verdict ? VERDICT_TITLE[verdict] : 'Odehráno'}</h2>
        <p className="rozbor-line">
          {verdict
            ? verdictLine(verdict, id)
            : `${rivalNick} má tvoje kolo ve výzvách. Až si ho zahraje, výsledek se tu doplní sám.`}
        </p>
      </div>

      <div className="rozbor-vs">
        <div className={`rozbor-side ${verdict === 'win' ? 'top' : ''}`}>
          {mojeKarta ? (
            <RivalChip nick={me.nick || 'Ty'} variant="panel" karta={mojeKarta} role="ty" />
          ) : (
            <>
              {me.rank ? <DuelCrest rank={me.rank} size={46} /> : null}
              <span className="rozbor-nick">{me.nick || 'Ty'}</span>
            </>
          )}
          <b className="rozbor-score num">{me.score.toLocaleString('cs-CZ')}</b>
        </div>

        <span className="rozbor-mezi" aria-hidden="true">
          {verdict ? (rozdil === 0 ? 'shoda' : `o ${rozdil} b.`) : '⏳'}
        </span>

        <div className={`rozbor-side ${verdict === 'loss' ? 'top' : ''} ${rival ? '' : 'ceka'}`}>
          {/*
            * Erb je součástí tlačítka karty, takže se na soupeřův profil dá
            * ťuknout i ve chvíli, kdy ještě nedohrál — o hráči se ví dost
            * i bez výsledku a čekání není důvod ho schovávat. Bez id (starší
            * záznam v archivu) zbude jen jméno.
            */}
          {kdo ? (
            <RivalChip uid={kdo} nick={rival?.nick ?? rivalNick} variant="panel" />
          ) : (
            <>
              {rival?.rank ? (
                <DuelCrest rank={rival.rank} size={46} />
              ) : (
                <DuelCrest rank={2} size={46} locked />
              )}
              <span className="rozbor-nick">{rival?.nick ?? rivalNick}</span>
            </>
          )}
          {rival ? (
            <b className="rozbor-score num">{rival.score.toLocaleString('cs-CZ')}</b>
          ) : (
            <b className="rozbor-score faint">čeká se</b>
          )}
        </div>
      </div>

      {kind === 'intruder' ? (
        <Kola mine={mine} theirs={theirs} ceka={!rival} />
      ) : (
        <Plastev mine={mine} theirs={theirs} ceka={!rival} mujNick={me.nick} jehoNick={rivalNick} />
      )}
    </div>
  )
}

/**
 * Vetřelec — tři stejná kola pro oba, takže se dají postavit přímo proti
 * sobě. To je celý smysl téhle obrazovky: vidět kolo, kde se to rozhodlo.
 */
function Kola({ mine, theirs, ceka }: { mine: DuelStep[]; theirs: DuelStep[]; ceka: boolean }) {
  const kol = Math.max(mine.length, theirs.length)
  if (kol === 0) {
    return (
      <p className="rozbor-prazdno">
        Rozpis kol tenhle souboj nemá — hrálo se ve verzi, která ho ještě
        neposílala. Zůstalo z něj skóre.
      </p>
    )
  }

  return (
    <ol className="rozbor-kola">
      {Array.from({ length: kol }, (_, i) => {
        const a = mine[i]
        const b = theirs[i]
        const spravne = a?.odd ?? b?.odd
        return (
          <li className="rozbor-kolo" key={i}>
            <span className="rozbor-cislo">
              {i + 1}. kolo <span className="faint">z {kol}</span>
            </span>
            <div className="rozbor-dvojice">
              <Bunka step={a} ceka={false} />
              <Bunka step={b} ceka={ceka} />
            </div>
            {/* Když se netrefil ani jeden, musí být vidět, co tam mělo být —
                jinak se oba budou ptát a nikdo neodpoví. */}
            {spravne && !(a?.points ?? 0) && (b === undefined || !b.points) && (
              <span className="rozbor-pravda">
                Nepatřilo tam: <b>{spravne}</b>
              </span>
            )}
          </li>
        )
      })}
      <li className="rozbor-strop faint">Nejvíc se dalo získat {INTRUDER_DUEL_MAX} bodů.</li>
    </ol>
  )
}

function Bunka({ step, ceka }: { step: DuelStep | undefined; ceka: boolean }) {
  if (!step) {
    return (
      <span className="rozbor-bunka prazdna">
        <span className="rozbor-slovo faint">{ceka ? 'čeká se' : '—'}</span>
      </span>
    )
  }
  const trefa = step.points > 0
  return (
    <span className={`rozbor-bunka ${trefa ? 'ok' : 'bad'}`}>
      <span className="rozbor-slovo">{step.word || '—'}</span>
      <span className="rozbor-cas faint">{stepTime(step.ms)}</span>
      <b className="rozbor-body num">{trefa ? `+${step.points}` : '0'}</b>
    </span>
  )
}

/**
 * Voština — společná plástev, ale úlovek každého jiný. Kola tu nejsou,
 * takže se staví vedle sebe dva seznamy: co komu zbylo a v které minutě
 * to stihl.
 */
function Plastev({
  mine,
  theirs,
  ceka,
  mujNick,
  jehoNick,
}: {
  mine: DuelStep[]
  theirs: DuelStep[]
  ceka: boolean
  mujNick: string
  jehoNick: string
}) {
  if (mine.length === 0 && theirs.length === 0) {
    return (
      <p className="rozbor-prazdno">
        Rozpis slov tenhle souboj nemá — hrálo se ve verzi, která ho ještě
        neposílala. Zůstalo z něj skóre.
      </p>
    )
  }

  return (
    <div className="rozbor-plastev">
      <Sloupec nadpis={mujNick || 'Ty'} steps={mine} ceka={false} />
      <Sloupec nadpis={jehoNick} steps={theirs} ceka={ceka} />
    </div>
  )
}

function Sloupec({
  nadpis,
  steps,
  ceka,
}: {
  nadpis: string
  steps: DuelStep[]
  ceka: boolean
}) {
  return (
    <div className="rozbor-sloupec">
      <h3>
        {nadpis} <span className="faint num">{steps.length}</span>
      </h3>
      {ceka ? (
        <p className="faint">Čeká se na odehrání.</p>
      ) : steps.length === 0 ? (
        <p className="faint">Ani slovo.</p>
      ) : (
        <ul>
          {steps.map((step, i) => (
            <li key={`${step.word}-${i}`}>
              <span className="rozbor-slovo">{step.word}</span>
              <span className="rozbor-cas faint">{hiveTime(step.ms)}</span>
              <b className="rozbor-body num">+{step.points}</b>
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}

/**
 * Porovnání v okně — z přehledu odehraných soubojů.
 *
 * Na obrazovce konce hry se rozbor ukazuje rovnou, tady se otevírá nad
 * seznamem; jinak je to tentýž obsah.
 */
export function DuelReportSheet({ onClose, ...props }: Props & { onClose: () => void }) {
  return (
    <div className="sheet-scrim" onClick={onClose}>
      <div
        className="sheet rozbor-sheet"
        onClick={(event) => event.stopPropagation()}
        role="dialog"
        aria-modal="true"
        aria-label="Porovnání souboje"
      >
        <DuelReport {...props} />
        <div className="sheet-actions">
          <button type="button" className="btn btn-ghost" onClick={onClose}>
            Zavřít
          </button>
        </div>
      </div>
    </div>
  )
}
