/** Domovská obrazovka — mřížka her nahoře, pod ní profil a pravidla. */

import { useState } from 'react'

import { AWARDS } from '../game/awards'
import { QUIZ_REWARD } from '../game/quiz'
import { rankFor } from '../game/ranks'
import { MODE_SUMMARY, TUTORIALS } from '../game/tutorials'
import {
  DIFFICULTY_LABEL,
  howToPlay,
  MODE_LABEL,
  MODE_TAGLINE,
  type Difficulty,
  type ModeId,
} from '../game/types'
import { useBackGuard } from '../lib/back'
import { InkMark } from './art/InkMark'
import { Explain } from './Explain'
import type { Profile, SavedRound, SavedRounds } from '../lib/storage'

interface Props {
  profile: Profile
  dayKey: string
  /** Označení dne, třeba „#412" — ukazuje se u denní výzvy. */
  dayLabel: string
  onPlay: (mode: ModeId, daily: boolean) => void
  onDifficulty: (mode: ModeId, difficulty: Difficulty) => void
  onStats: () => void
  onAwards: () => void
  onRules: (mode: ModeId) => void
  /** Průvodce celou hrou — společná pravidla, body, inkoust, hodnosti. */
  onGuide: () => void
  /** Otázka dne — jednou denně, mimo šestici slovních her. */
  onQuiz: () => void
  /** Přehled všech otázek. Předává se jen v kontrolním buildu. */
  onQuizList?: () => void
  /** Kola přerušená odchodem do menu nebo zavřením hry, po jednom od režimu. */
  saved: SavedRounds
  onResume: (mode: ModeId) => void
}

const MODES: { id: ModeId; glyph: string; color: string }[] = [
  { id: 'chain', glyph: '→', color: 'var(--mode-chain)' },
  { id: 'hive', glyph: '⬡', color: 'var(--mode-hive)' },
  { id: 'tower', glyph: '↑', color: 'var(--mode-tower)' },
  { id: 'gallows', glyph: '?', color: 'var(--mode-gallows)' },
  { id: 'detective', glyph: '§', color: 'var(--mode-detective)' },
  { id: 'tetris', glyph: '▚', color: 'var(--mode-tetris)' },
]

const DIFFICULTIES: Difficulty[] = ['easy', 'normal', 'hard']

const DIFFICULTY_NOTE: Record<ModeId, Record<Difficulty, string>> = {
  chain: {
    easy: '4 písmena, kratší cesty',
    normal: '5 písmen',
    hard: '6 písmen, delší cesty',
  },
  hive: {
    easy: 'menší plástev, do 35 slov',
    normal: 'do 60 slov',
    hard: 'bohatá plástev, až 90 slov',
  },
  tower: {
    easy: 'věž do 6 pater',
    normal: 'věž do 7 pater',
    hard: 'věž až na 8 písmen',
  },
  gallows: {
    easy: '4–5 písmen, nejběžnější slova',
    normal: '6–7 písmen',
    hard: '8–9 písmen',
  },
  detective: {
    easy: 'krátká, běžná slova',
    normal: '6–7 písmen',
    hard: 'dlouhá slova a spletitější původ',
  },
  tetris: {
    easy: '6 sloupců, klidné tempo',
    normal: '6 sloupců, svižnější',
    hard: '7 sloupců, rychlý pád',
  },
}

/** Česká čísla: 1 tah, 2–4 tahy, 5 a víc tahů. */
function plural(count: number, one: string, few: string, many: string): string {
  const form = count === 1 ? one : count >= 2 && count <= 4 ? few : many
  return `${count} ${form}`
}

/** Kolik toho v přerušeném kole zbývá — ať hráč ví, do čeho se vrací. */
function progressNote(saved: SavedRound): string {
  const state = saved.state as {
    path?: string[]
    found?: string[]
    built?: string[]
    tried?: string[]
    cleared?: string[]
    puzzle?: { solutions?: string[]; levels?: unknown[] }
  }
  switch (saved.mode) {
    case 'chain':
      return plural((state.path?.length ?? 1) - 1, 'tah', 'tahy', 'tahů')
    case 'hive':
      return `${state.found?.length ?? 0} z ${state.puzzle?.solutions?.length ?? 0} slov`
    case 'gallows':
    case 'detective':
      return plural(state.tried?.length ?? 0, 'písmeno', 'písmena', 'písmen')
    case 'tetris':
      return plural(state.cleared?.length ?? 0, 'slovo', 'slova', 'slov')
    default: {
      const built = (state.built?.length ?? 1) - 1
      return `${built} z ${(state.puzzle?.levels?.length ?? 1) - 1} pater`
    }
  }
}

export function Home({
  profile,
  dayKey,
  dayLabel,
  onPlay,
  onDifficulty,
  onStats,
  onAwards,
  onRules,
  onGuide,
  onQuiz,
  onQuizList,
  saved,
  onResume,
}: Props) {
  const progress = rankFor(profile.fame)
  const awards = AWARDS.filter((award) => profile.awards[award.id] !== undefined).length
  const dailyLeft = MODES.filter(
    (mode) => profile.dailyDone[`${dayKey}:${mode.id}`] === undefined,
  ).length
  const [openRules, setOpenRules] = useState<ModeId | null>(null)
  /** Otevřená dlaždice — volba obtížnosti a spuštění se dějí až v ní. */
  const [picked, setPicked] = useState<ModeId | null>(null)
  // Všech šest her, ne jen ty tři původní — jinak by „Odehráno" hlásilo míň,
  // než kolik má hráč doopravdy za sebou.
  const played = MODES.reduce((sum, mode) => sum + profile.stats[mode.id].played, 0)

  // Otázka dne se hraje jednou za den; podle zápisu v profilu se pozná,
  // že je dnešek hotový.
  // Kontrolní build zámek nemá — jinak by po první otázce nešlo pokračovat.
  const quizDone = !__QUIZ_ALL__ && profile.quiz.lastDay === dayKey

  const pickedMode = picked ? MODES.find((m) => m.id === picked)! : null
  const pickedSaved = picked ? saved[picked] : undefined

  // Systémové zpět zavře panel, ne celou hru.
  useBackGuard(picked !== null, () => setPicked(null))

  /**
   * Proužek Otázky dne.
   *
   * Stojí buď úplně nahoře, nebo úplně dole — podle toho, jestli je dnešek
   * zodpovězený. Nezodpovězený tiše pulzuje nad nadpisem, protože je to jediná
   * věc na obrazovce, která zítra propadne; jakmile hráč odpoví, sesune se pod
   * hry a přestane se hýbat.
   *
   * Popisek, co Otázka dne obnáší, v proužku nestojí — vejde se do otazníčku
   * vpravo, který otevře výklad. Proužek tak zůstane úzký i na malém telefonu.
   *
   * Není to jeden `<button>`, ale `<div>` se dvěma: otazník uvnitř spouštěče
   * by byl tlačítko v tlačítku, což prohlížeč ani čtečka neunesou.
   */
  const quizStrip = (
    <div className={`quiz-strip ${quizDone ? 'done' : 'live'}`}>
      <button
        type="button"
        className="quiz-strip-go"
        onClick={onQuiz}
        disabled={quizDone}
        aria-label={
          quizDone ? 'Otázka dne — dnešek hotový' : `Hrát Otázku dne ${dayLabel}`
        }
      >
        <span className="quiz-strip-mark" aria-hidden="true">
          ?
        </span>
        <span className="quiz-strip-body">
          <span className="quiz-strip-title">Otázka dne</span>
          <span className="faint">
            {quizDone
              ? `Uhodnuto ${profile.quiz.solved} z ${profile.quiz.played} · další zítra`
              : dayLabel}
          </span>
        </span>
        {!quizDone && (
          <span className="chip chip-ink">
            <InkMark size={12} /> <span className="num">{QUIZ_REWARD[1]}</span>
          </span>
        )}
      </button>
      <Explain term="otazka" className="quiz-strip-help" label="Jak Otázka dne funguje">
        ?
      </Explain>
    </div>
  )

  /**
   * Připomínka nedohraných denních výzev.
   *
   * Zmizí ve chvíli, kdy je hráč má všechny — proto nese počet, ne jen text:
   * „4 z 6" je pobídka, „Nedohrál jsi všechny" samo o sobě jen výtka. Ťuknutí
   * sjede k várce, odkud se výzvy spouštějí.
   *
   * Pulzuje stejným rytmem jako Otázka dne, aby se ty dvě věci nahoře
   * nepřekřikovaly — jsou to dvě upomínky, ne dvě soutěže o pozornost.
   */
  const dailyAlert = dailyLeft > 0 && (
    <button
      type="button"
      className="daily-alert live"
      onClick={() => {
        document.querySelector('.daily-strip')?.scrollIntoView({
          behavior: 'smooth',
          block: 'center',
        })
      }}
    >
      <span className="daily-alert-mark" aria-hidden="true">
        !
      </span>
      <span className="daily-alert-text">Nedohrál jsi všechny denní výzvy</span>
      <span className="daily-alert-count num">
        {MODES.length - dailyLeft}/{MODES.length}
      </span>
    </button>
  )

  return (
    <>
      {/* Nahoře stojí to, co dneškem propadne: nezodpovězená Otázka dne
          a nedohrané denní výzvy. Obojí zmizí, jakmile je hotovo — a mřížka
          her se musí vejít na displej i s oběma, viz `.home-top` ve stylech. */}
      <div className="home-top">
        {!quizDone && quizStrip}
        {dailyAlert}
      </div>

      {/* Mřížka her je první věc na stránce a vejde se celá na displej.
          Až přibudou další režimy, jen se do ní přidají další dlaždice. */}
      <h1 className="home-head">Vyber si hru</h1>

      <div className="mode-grid">
        {MODES.map((mode) => {
          const dailyDone = profile.dailyDone[`${dayKey}:${mode.id}`] !== undefined
          const round = saved[mode.id]
          return (
            <button
              type="button"
              className="mode-tile"
              key={mode.id}
              data-mode={mode.id}
              style={{ ['--mode-color' as string]: mode.color }}
              onClick={() => setPicked(mode.id)}
            >
              <span className="mode-glyph" aria-hidden="true">
                {mode.glyph}
              </span>
              <span className="mode-name">{MODE_LABEL[mode.id]}</span>
              <span className="mode-tag">{MODE_TAGLINE[mode.id]}</span>
              {round ? (
                <span className="mode-flag live">Rozehráno · {progressNote(round)}</span>
              ) : !profile.tutorialSeen[mode.id] ? (
                <span className="mode-flag">Nové</span>
              ) : dailyDone ? (
                <span className="mode-flag">Denní ✓</span>
              ) : null}
            </button>
          )
        })}
      </div>

      {/* Denní výzva hned pod mřížkou. Je to hlavní důvod, proč se hráč
          vrací každý den, takže nesmí být schovaná v panelu režimu — odsud
          se do ní vejde jedním ťuknutím a je vidět, co ještě dneska zbývá. */}
      <div className="panel daily-strip">
        <div className="daily-head">
          <Explain term="denni" className="label">
            Denní výzva {dayLabel}
          </Explain>
          <span className="faint">
            {dailyLeft === 0
              ? 'Hotovo — celou várku dneska máš'
              : `Zbývá ${plural(dailyLeft, 'výzva', 'výzvy', 'výzev')}`}
          </span>
        </div>
        <div className="daily-row">
          {MODES.map((mode) => {
            const score = profile.dailyDone[`${dayKey}:${mode.id}`]
            const done = score !== undefined
            return (
              <button
                type="button"
                key={mode.id}
                className={`daily-item ${done ? 'done' : ''}`}
                style={{ ['--mode-color' as string]: mode.color }}
                // Hotová výzva se už nespustí. Šlo ji hrát pořád dokola a
                // pokaždé inkasovat inkoust za dokončenou várku; zamčené je
                // to i v `recordRound`, tohle je jen ta viditelná půlka.
                disabled={done}
                title={done ? 'Dnešní výzvu už máš hotovou' : undefined}
                onClick={() => onPlay(mode.id, true)}
              >
                <span className="mode-glyph" aria-hidden="true">
                  {mode.glyph}
                </span>
                <span className="daily-name">{MODE_LABEL[mode.id]}</span>
                <span className="daily-note num">
                  {done ? `✓ ${score.toLocaleString('cs-CZ')}` : 'Hrát'}
                </span>
              </button>
            )
          })}
        </div>
      </div>

      {/* Zodpovězená otázka se odsune sem dolů — je z ní jen tichý řádek se
          skóre, který nikomu nepřekáží. Zítra se zase objeví nahoře. */}
      {quizDone && quizStrip}

      {/* Kontrolní build: seznam všech otázek, ať se nemusí prohádat. */}
      {onQuizList && (
        <button
          type="button"
          className="btn btn-sm review-open"
          onClick={onQuizList}
          style={{ width: '100%', marginBottom: 'var(--sp-4)' }}
        >
          Projít všechny otázky
        </button>
      )}

      {pickedMode && (
        <div
          className="sheet-scrim"
          role="dialog"
          aria-modal="true"
          aria-label={MODE_LABEL[pickedMode.id]}
          onClick={() => setPicked(null)}
        >
          <div
            className="sheet"
            data-mode={pickedMode.id}
            style={{ ['--mode-color' as string]: pickedMode.color }}
            onClick={(event) => event.stopPropagation()}
          >
            <div className="sheet-head">
              <span className="mode-glyph" aria-hidden="true">
                {pickedMode.glyph}
              </span>
              <h2>{MODE_LABEL[pickedMode.id]}</h2>
              <button
                type="button"
                className="btn btn-sm btn-ghost"
                onClick={() => setPicked(null)}
              >
                Zavřít
              </button>
            </div>

            <ul className="mode-rules">
              {MODE_SUMMARY[pickedMode.id].map((rule) => (
                <li key={rule}>{rule}</li>
              ))}
            </ul>

            <div>
              <div className="label" style={{ marginBottom: 'var(--sp-2)' }}>
                Obtížnost
              </div>
              <div className="seg">
                {DIFFICULTIES.map((difficulty) => (
                  <button
                    type="button"
                    key={difficulty}
                    aria-pressed={profile.difficulty[pickedMode.id] === difficulty}
                    onClick={() => onDifficulty(pickedMode.id, difficulty)}
                  >
                    {DIFFICULTY_LABEL[difficulty]}
                  </button>
                ))}
              </div>
              <p className="faint" style={{ fontSize: '0.8rem', marginTop: 'var(--sp-2)' }}>
                {DIFFICULTY_NOTE[pickedMode.id][profile.difficulty[pickedMode.id]]}
              </p>
            </div>

            <div className="sheet-actions">
              {pickedSaved && (
                <button
                  type="button"
                  className="btn btn-primary"
                  onClick={() => onResume(pickedMode.id)}
                >
                  Pokračovat · {progressNote(pickedSaved)}
                </button>
              )}
              <button
                type="button"
                className={`btn ${pickedSaved ? '' : 'btn-primary'}`}
                onClick={() => onPlay(pickedMode.id, false)}
              >
                {pickedSaved ? 'Nová hra' : 'Hrát'}
              </button>
              <button
                type="button"
                className="btn"
                disabled={profile.dailyDone[`${dayKey}:${pickedMode.id}`] !== undefined}
                onClick={() => onPlay(pickedMode.id, true)}
              >
                {profile.dailyDone[`${dayKey}:${pickedMode.id}`] !== undefined
                  ? 'Denní ✓'
                  : 'Denní výzva'}
              </button>
              <button
                type="button"
                className="btn btn-ghost"
                onClick={() => onRules(pickedMode.id)}
              >
                Návod
              </button>
            </div>

            {pickedSaved && (
              <p className="faint" style={{ fontSize: '0.8rem' }}>
                Nová hra rozehrané kolo zahodí.
              </p>
            )}
          </div>
        </div>
      )}

      {/* Profil až pod výběrem hry — je to doplněk, ne to hlavní. Na každý
          údaj se dá ťuknout: hodnost a věhlas vedou do vitríny, čipy si
          otevřou vlastní vysvětlivku. Nikde nemá zůstat mrtvý popisek. */}
      <div className="panel home-profile">
        <button type="button" className="rank-line" onClick={onAwards}>
          <span className="rank">
            {progress.rank.name} · hodnost {progress.rank.index}
          </span>
          <span className="num muted">
            {profile.fame.toLocaleString('cs-CZ')} věhlasu
          </span>
        </button>
        <div className="fame-bar">
          <span
            style={{ width: `${progress.span ? (progress.into / progress.span) * 100 : 100}%` }}
          />
        </div>
        <div className="home-profile-chips">
          <Explain term="serie" className="chip chip-accent">
            Série {profile.streak}
          </Explain>
          <Explain term="serie" className="chip">
            Nejlepší série {profile.bestStreak}
          </Explain>
          <Explain term="dny" className="chip">
            Dny v řadě {profile.dayStreak}
          </Explain>
          <Explain term="odehrano" className="chip">
            Odehráno {played}
          </Explain>
          <Explain term="inkoust" className="chip chip-ink" title="Inkoust na nápovědy">
            <InkMark size={11} /> <span className="num">{profile.ink}</span>
          </Explain>
          <button type="button" className="btn btn-sm btn-ghost" onClick={onAwards}>
            Ocenění {awards}/{AWARDS.length}
          </button>
          <button type="button" className="btn btn-sm btn-ghost" onClick={onStats}>
            Statistiky
          </button>
        </div>
        {/* Verze buildu — podle ní se pozná, jestli telefon drží starou cache. */}
        <p className="faint build-mark">verze {__BUILD__}</p>
      </div>

      <div className="section-head">
        <h2>Pravidla podrobně</h2>
        <span className="rule" />
      </div>
      <p className="muted" style={{ marginBottom: 'var(--sp-3)', fontSize: '0.94rem' }}>
        Rozklikni hru a projdi si všechno, co v ní platí. Totéž ti hra ukáže
        i sama, když ji spustíš poprvé.
      </p>
      {/* Průvodce celou hrou stojí nad návody jednotlivých her: nejdřív ať se
          hráč dozví, co je věhlas a odkud se bere inkoust, teprve pak pravidla
          Voštiny. */}
      <button
        type="button"
        className="btn btn-primary guide-open"
        onClick={onGuide}
        style={{ marginBottom: 'var(--sp-4)' }}
      >
        Jak se hrají Slova — body, hodnosti, inkoust
      </button>

      <div className="rules-list">
        {MODES.map((mode) => {
          const open = openRules === mode.id
          return (
            <div className="rules-item" key={mode.id}>
              <button
                type="button"
                className="rules-toggle"
                aria-expanded={open}
                onClick={() => setOpenRules(open ? null : mode.id)}
              >
                <span className="mode-glyph" style={{ color: mode.color, fontSize: '1.2rem' }}>
                  {mode.glyph}
                </span>
                <span className="rules-title">{howToPlay(mode.id)}</span>
                <span className={`rules-caret ${open ? 'open' : ''}`} aria-hidden="true">
                  ⌄
                </span>
              </button>

              {open && (
                <div className="rules-body">
                  {TUTORIALS[mode.id].map((step) => (
                    <section key={step.title}>
                      <h3>{step.title}</h3>
                      {step.body.map((paragraph, i) => (
                        <p key={i}>{paragraph.replace(/\*\*/g, '')}</p>
                      ))}
                      {step.key && <p className="rules-key">{step.key.replace(/\*\*/g, '')}</p>}
                    </section>
                  ))}
                  <button
                    type="button"
                    className="btn btn-sm"
                    onClick={() => onRules(mode.id)}
                  >
                    Projít návod s ukázkami
                  </button>
                </div>
              )}
            </div>
          )
        })}
      </div>
    </>
  )
}
