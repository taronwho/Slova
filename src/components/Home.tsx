/** Domovská obrazovka — mřížka her nahoře, pod ní profil a pravidla. */

import { useEffect, useState, type ReactNode } from 'react'

import { AWARDS } from '../game/awards'
import { QUIZ_REWARD } from '../game/quiz'
import { rankFor } from '../game/ranks'
import { MODE_SUMMARY, TUTORIALS } from '../game/tutorials'
import {
  DIFFICULTY_LABEL,
  howToPlay,
  MODE_GLYPH,
  MODE_LABEL,
  MODE_ORDER,
  MODE_TAGLINE,
  type Difficulty,
  type ModeId,
} from '../game/types'
import { stillDaily } from '../app/resume'
import { RankBadge } from './art/RankBadge'
import { useBackGuard } from '../lib/back'
import { todayKey } from '../lib/rng'
import { InkMark } from './art/InkMark'
import { Explain } from './Explain'
import {
  liveStreak,
  roundSlot,
  type Profile,
  type SavedRound,
  type SavedRounds,
} from '../lib/storage'

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
  /** Proužek soubojů. Nese ho App, protože potřebuje síť. */
  duels?: ReactNode
}

const MODES: { id: ModeId; glyph: string; color: string }[] = MODE_ORDER.map((id) => ({
  id,
  glyph: MODE_GLYPH[id],
  color: `var(--mode-${id})`,
}))

const DIFFICULTIES: Difficulty[] = ['easy', 'normal', 'hard']

/**
 * Rozehraná **dnešní** denní výzva, nebo nic.
 *
 * Po půlnoci se včerejší kolo dohrává jako volná hra (viz `stillDaily`), takže
 * se u dnešní dlaždice nesmí hlásit jako rozehraná výzva — hráč by čekal, že
 * v něm ťuknutím naváže, a ono začne dnešní hádanka od začátku.
 */
function dnesniRozehrane(
  saved: SavedRounds,
  mode: ModeId,
  dayKey: string,
): SavedRound | undefined {
  const round = saved[roundSlot(mode, true)]
  if (!round) return undefined
  return stillDaily(round, dayKey, (at) => todayKey(new Date(at))) ? round : undefined
}

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
    easy: 'slova, která zná každý',
    normal: 'méně častá slova',
    hard: 'vzácná slova',
  },
  tetris: {
    easy: '6 sloupců, klidné tempo',
    normal: '6 sloupců, svižnější',
    hard: '7 sloupců, rychlý pád',
  },
  quotes: {
    easy: 'krátké výroky',
    normal: 'delší výroky',
    hard: 'dlouhá souvětí',
  },
  intruder: {
    easy: 'rozdíl je vidět hned',
    normal: 'rozdíl chce zamyšlení',
    hard: 'rozdíl je skrytý',
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
  duels,
}: Props) {
  const progress = rankFor(profile.fame)
  const awards = AWARDS.filter((award) => profile.awards[award.id] !== undefined).length
  const dailyLeft = MODES.filter(
    (mode) => profile.dailyDone[`${dayKey}:${mode.id}`] === undefined,
  ).length
  const [openRules, setOpenRules] = useState<ModeId | null>(null)
  /** Otevřená dlaždice — volba obtížnosti a spuštění se dějí až v ní. */
  const [picked, setPicked] = useState<ModeId | null>(null)
  /** Otevřený přehled denních sérií. */
  const [streaks, setStreaks] = useState(false)
  /**
   * Drží telefon starou verzi hry, kterou se nedaří setřást?
   *
   * Hlásí to `ensureLatestBuild` v `main.tsx` — ten se o výměnu pokusí sám
   * a ozve se, teprve když to dvakrát nevyjde. Pak už to musí vzít do ruky
   * hráč, a musí se to k němu dostat: bez tohohle řádku by hrál starou verzi
   * dál a neměl jak na to přijít.
   */
  const [stale, setStale] = useState(
    () => document.documentElement.dataset.stale === 'true',
  )
  useEffect(() => {
    const notice = () => setStale(true)
    window.addEventListener('slova:stale', notice)
    return () => window.removeEventListener('slova:stale', notice)
  }, [])
  // Všechny hry, ne jen ty tři původní — jinak by „Odehráno" hlásilo míň,
  // než kolik má hráč doopravdy za sebou.
  const played = MODES.reduce((sum, mode) => sum + profile.stats[mode.id].played, 0)

  // Otázka dne se hraje jednou za den; podle zápisu v profilu se pozná,
  // že je dnešek hotový.
  // Kontrolní build zámek nemá — jinak by po první otázce nešlo pokračovat.
  const quizDone = !__QUIZ_ALL__ && profile.quiz.lastDay === dayKey

  /**
   * Řada Otázky dne, ale jen dokud platí.
   *
   * Uložené číslo se nuluje až další odpovědí, takže po týdnu ticha by pořád
   * tvrdilo šest dnů v řadě. Stejné síto jako u her — jen tady sedí data
   * ve vlastní přihrádce, protože Otázka dne je měla dřív než ony.
   */
  const quizStreak = liveStreak(
    {
      lastDay: profile.quiz.lastDay,
      streak: profile.quiz.streak,
      best: profile.quiz.bestStreak,
    },
    dayKey,
  )

  const pickedMode = picked ? MODES.find((m) => m.id === picked)! : null
  // Panel režimu je o volné hře, takže tlačítko Pokračovat nabízí volné
  // kolo. Rozehraná denní výzva má vlastní cestu zpátky — svou dlaždici.
  const pickedSaved = picked ? saved[roundSlot(picked, false)] : undefined

  // Systémové zpět zavře panel, ne celou hru.
  useBackGuard(picked !== null, () => setPicked(null))
  useBackGuard(streaks, () => setStreaks(false))

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
        {/* Souboje stojí nad vším ostatním: živá Voština se hraje naráz, takže
            výzva má cenu jen ve chvíli, kdy dorazí — ne až si jí někdo všimne
            pod výběrem hry. */}
        {duels}
        {!quizDone && quizStrip}
        {dailyAlert}
      </div>

      {/* Mřížka her je první věc na stránce a vejde se celá na displej.
          Až přibudou další režimy, jen se do ní přidají další dlaždice. */}
      <h1 className="home-head">Vyber si hru</h1>

      <div className="mode-grid">
        {MODES.map((mode) => {
          const dailyDone = profile.dailyDone[`${dayKey}:${mode.id}`] !== undefined
          const round = saved[roundSlot(mode.id, false)] ?? dnesniRozehrane(saved, mode.id, dayKey)
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
          {/* Řady se vejdou k dlaždicím jen jako číslo. Kdo chce vědět víc —
              nejdelší řadu, jak na tom je Otázka dne —, otevře si přehled. */}
          <button
            type="button"
            className="btn btn-sm streaks-open"
            onClick={() => setStreaks(true)}
          >
            <span aria-hidden="true">🔥</span> Denní série
          </button>
        </div>
        <div className="daily-row">
          {MODES.map((mode) => {
            const score = profile.dailyDone[`${dayKey}:${mode.id}`]
            const done = score !== undefined
            // Rozehraná dnešní výzva: dlaždice v ní pokračuje, tak ať je to
            // na ní vidět. Bez toho vypadá stejně jako nezačatá a hráč neví,
            // jestli ťuknutím naváže, nebo začne od začátku.
            const started = dnesniRozehrane(saved, mode.id, dayKey)
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
                  {done
                    ? `✓ ${score.toLocaleString('cs-CZ')}`
                    : started
                      ? progressNote(started)
                      : 'Hrát'}
                </span>
                {/* Řada dnů u téhle hry. Ukazuje se, jen když nějaká je —
                    nula u sedmi dlaždic by z mřížky udělala tabulku nul. */}
                {liveStreak(profile.dailyStreak[mode.id], dayKey) > 0 && (
                  <span className="daily-flame num">
                    <span aria-hidden="true">🔥</span>
                    {liveStreak(profile.dailyStreak[mode.id], dayKey)}
                  </span>
                )}
              </button>
            )
          })}

          {/* Devátá dlaždice: Otázka dne. Osm her nechávalo v mřížce po třech
              sloupcích prázdné místo a otázka se přitom hraje ze stejného
              důvodu jako ony — jednou denně, zítra je jiná. Do várky, za
              kterou padá inkoust, se ale nepočítá, proto je zlatá a ne
              v barvě hry. */}
          <button
            type="button"
            className={`daily-item daily-quiz ${quizDone ? 'done' : ''}`}
            style={{ ['--mode-color' as string]: 'var(--gold)' }}
            disabled={quizDone}
            title={quizDone ? 'Dnešní otázku už máš zodpovězenou' : undefined}
            onClick={onQuiz}
          >
            <span className="mode-glyph" aria-hidden="true">
              ?
            </span>
            <span className="daily-name">Otázka dne</span>
            <span className="daily-note num">{quizDone ? '✓ hotovo' : 'Hrát'}</span>
            {quizStreak > 0 && (
              <span className="daily-flame num">
                <span aria-hidden="true">🔥</span>
                {quizStreak}
              </span>
            )}
          </button>
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

      {/* Přehled všech řad naráz. Osm her a Otázka dne, u každé kolik dnů
          drží a kolik nejvíc kdy držela. Vejde se sem i to, co u dlaždice
          nemá kam — proto je to panel a ne další čísílko v mřížce. */}
      {streaks && (
        <div className="sheet-scrim" onClick={() => setStreaks(false)}>
          <div className="sheet" onClick={(event) => event.stopPropagation()}>
            <div className="sheet-head">
              <h2>Denní série</h2>
              <button
                type="button"
                className="btn btn-sm btn-ghost"
                onClick={() => setStreaks(false)}
              >
                Zavřít
              </button>
            </div>
            <p className="muted" style={{ fontSize: '0.86rem' }}>
              Kolik dní po sobě jsi tu kterou denní výzvu dohrál. Počítá se
              účast, ne výhra — vynechaný den řadu utne, prohrané kolo ne.
              U Otázky dne je to naopak řada správných odpovědí.
            </p>
            <div className="streak-list">
              {MODES.map((mode) => {
                const row = profile.dailyStreak[mode.id]
                const live = liveStreak(row, dayKey)
                return (
                  <div className={`streak-row ${live > 0 ? 'live' : ''}`} key={mode.id}>
                    <span
                      className="streak-glyph"
                      aria-hidden="true"
                      style={{ ['--mode-color' as string]: mode.color }}
                    >
                      {mode.glyph}
                    </span>
                    <span className="streak-name">{MODE_LABEL[mode.id]}</span>
                    <span className="streak-now num">
                      {live > 0 ? `🔥 ${live}` : '—'}
                    </span>
                    <span className="streak-best num faint">nejvíc {row.best}</span>
                  </div>
                )
              })}
              <div className={`streak-row ${quizStreak > 0 ? 'live' : ''}`}>
                <span className="streak-glyph" aria-hidden="true">
                  ?
                </span>
                <span className="streak-name">Otázka dne</span>
                <span className="streak-now num">
                  {quizStreak > 0 ? `🔥 ${quizStreak}` : '—'}
                </span>
                <span className="streak-best num faint">
                  nejvíc {profile.quiz.bestStreak}
                </span>
              </div>
            </div>
          </div>
        </div>
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
          {/* Odznak hodnosti, ne jen její jméno. Kov a tvar štítu řeknou, jak
              daleko hráč je, dřív než se stihne přečíst číslo. */}
          <RankBadge rank={progress.rank.index} size={46} compact />
          <span className="rank-line-name">
            <span className="rank">{progress.rank.name}</span>
            <span className="rank-step">hodnost {progress.rank.index}</span>
          </span>
          <span className="rank-line-fame">
            <span className="num">{profile.fame.toLocaleString('cs-CZ')}</span>
            <span className="rank-step">věhlasu</span>
          </span>
        </button>
        <div className="fame-bar">
          <span
            style={{ width: `${progress.span ? (progress.into / progress.span) * 100 : 100}%` }}
          />
        </div>
        <p className="fame-note">
          {progress.next
            ? `Do hodnosti ${progress.next.index} — ${progress.next.name} — zbývá ${(
                progress.span - progress.into
              ).toLocaleString('cs-CZ')} věhlasu.`
            : 'Nejvyšší hodnost. Dál už se stoupat nedá.'}
        </p>
        {/* Mřížka místo rozsypaných čipů: čísla stojí pod sebou ve sloupcích,
            takže se dají porovnat očima, ne čtením. */}
        <div className="stat-grid">
          <Explain term="serie" className="stat-cell live">
            <b className="num">{profile.streak}</b>
            <span>Série</span>
          </Explain>
          <Explain term="serie" className="stat-cell">
            <b className="num">{profile.bestStreak}</b>
            <span>Nejlepší série</span>
          </Explain>
          <Explain term="dny" className="stat-cell">
            <b className="num">{profile.dayStreak}</b>
            <span>Dny v řadě</span>
          </Explain>
          <Explain term="odehrano" className="stat-cell">
            <b className="num">{played}</b>
            <span>Odehráno</span>
          </Explain>
          <Explain term="inkoust" className="stat-cell ink" title="Inkoust na nápovědy">
            <b className="num">
              {/* Kapka je značka, ne text — visí vedle čísla, aby zůstalo
                  přesně nad popiskem jako v ostatních buňkách. */}
              <span className="stat-figure">
                <span className="stat-aside left" aria-hidden="true">
                  <InkMark size={13} />
                </span>
                {profile.ink}
              </span>
            </b>
            <span>Inkoust</span>
          </Explain>
          <button type="button" className="stat-cell" onClick={onAwards}>
            <b className="num">{awards}</b>
            <span>ze {AWARDS.length} ocenění</span>
          </button>
        </div>
        <div className="home-profile-actions">
          <button type="button" className="btn btn-sm btn-ghost" onClick={onAwards}>
            Vitrína ocenění
          </button>
          <button type="button" className="btn btn-sm btn-ghost" onClick={onStats}>
            Statistiky
          </button>
        </div>
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

      {/* Úplně dole, tiše. Hra se sama drží v telefonu i bez sítě, takže po
          nasazení opravy může ještě chvíli běžet stará verze — tohle ji
          zahodí a stáhne novou. Když se nic nezměnilo, jen se to načte znovu.
          Tiše ale jen do chvíle, než se ukáže, že hra opravdu drží starou
          verzi a sama se jí nezbaví; pak se řádek rozsvítí. */}
      <div className={`refresh-row ${stale ? 'stale' : ''}`}>
        <button
          type="button"
          className={`btn btn-sm ${stale ? 'btn-primary' : 'btn-ghost'} refresh-btn`}
          onClick={refresh}
        >
          Aktualizovat
        </button>
        {stale && <span className="refresh-note">Je k dispozici novější verze</span>}
        <span className="faint">verze {__BUILD__}</span>
        {/* Zásady ochrany soukromí musí být po ruce i tomu, kdo souboje
            nikdy neotevře — obchody s aplikacemi to vyžadují a je to
            správně i bez nich. */}
        <a className="faint refresh-privacy" href="./soukromi.html" target="_blank" rel="noreferrer">
          Soukromí
        </a>
      </div>
    </>
  )
}

/**
 * Zahodí uloženou verzi hry a načte ji znovu ze sítě.
 *
 * Slova fungují i bez připojení, takže si telefon drží celou hru u sebe —
 * a po nasazení opravy ji podle toho, jak se prohlížeč zrovna rozhodne, může
 * ještě den nabízet ze staré zásoby. Odhlášení obsluhy a smazání zásob je
 * jediná jistota, že se hráč dívá na to, co je právě nasazené.
 *
 * Profil se tím nemaže — ten leží jinde a aktualizace se ho netýká.
 */
async function refresh(): Promise<void> {
  try {
    // Ruční pokus začíná nanovo — počitadlo automatických pokusů se smaže,
    // ať se hra po přenačtení ještě jednou pokusí sama.
    sessionStorage.removeItem('slova.refreshTries')
    if ('serviceWorker' in navigator) {
      const workers = await navigator.serviceWorker.getRegistrations()
      await Promise.all(workers.map((worker) => worker.unregister()))
    }
    if ('caches' in window) {
      const names = await caches.keys()
      await Promise.all(names.map((name) => caches.delete(name)))
    }
  } catch {
    // I když se úklid nepovede, načtení znovu stojí za pokus.
  }
  // Prosté `location.reload()` nestačí. Servisní pracovník a jeho mezipaměť
  // jsou pryč, jenže index.html leží ještě v běžné mezipaměti prohlížeče
  // (GitHub Pages ho posílá s desetiminutovou platností) a načtení znovu si
  // ho odtud zase vezme — hráč pak vidí starou verzi i po kliknutí.
  // Adresa s jednorázovým parametrem žádnou uloženou kopii nemá, takže se
  // musí sáhnout na síť. Zbytek souborů má v názvu otisk obsahu, ten se
  // dotáhne sám.
  const fresh = new URL(location.href)
  fresh.searchParams.set('v', String(Date.now()))
  location.replace(fresh.toString())
}
