/**
 * Přehled statistik a historie kol.
 *
 * Každá dlaždice je klikací. Buď má pojem ve slovníčku (věhlas, série, denní
 * výzva) a otevře jeho výklad, nebo si nese vlastní jednu větu, která se pod ní
 * rozbalí — číslo bez vysvětlení je k ničemu, když si hráč není jistý, co se do
 * něj počítá.
 */

import { useState } from 'react'

import { rankFor } from '../game/ranks'
import { MODE_LABEL, type ModeId } from '../game/types'
import type { Profile } from '../lib/storage'
import { Explain, useExplain } from './Explain'

interface Props {
  profile: Profile
  onBack: () => void
  onReset: () => void
}

// Všech šest her, ne pět. Slabiky ve výpisu chyběly, takže hráč o svých
// číslech z jedné celé hry nevěděl.
const MODES: ModeId[] = ['chain', 'hive', 'tower', 'gallows', 'detective', 'tetris']

/** Popisky detailů kola — v historii je čte hráč, ne vývojář. */
const DETAIL_LABEL: Record<string, string> = {
  moves: 'tahů',
  par: 'nejkratší cesta',
  found: 'nalezeno slov',
  total: 'z celku',
  rank: 'hodnost',
  floors: 'pater',
  top: 'nejvyšší patro',
  words: 'slov',
  chain: 'nejdelší řetěz',
  level: 'úroveň',
  solved: 'uhodnuto',
  wrong: 'chyb',
  lives: 'zbylo životů',
  guessed: 'tipnuto',
  extra: 'navíc',
  full: 'dostavěno',
  pangrams: 'pangramů',
  rankTop: 'nejvyšší hodnost',
}

const EXTRA_LABEL: Record<ModeId, string> = {
  chain: 'Průměr tahů navíc',
  hive: 'Průměr nalezených slov',
  tower: 'Průměr postavených pater',
  gallows: 'Průměr zbylých životů',
  detective: 'Průměr nevyužitých pokusů',
  tetris: 'Průměr složených slov',
  quotes: 'Průměr nevyužitých pokusů',
}

/** Co znamená „perfektní" — v každé hře něco jiného. */
const PERFECT_NOTE: Record<ModeId, string> = {
  chain: 'Kola dohraná na počet tahů nejkratší cesty a bez nápovědy.',
  hive: 'Kola, ve kterých jsi vysbíral celou plástev bez nápovědy.',
  tower: 'Věže dostavěné až nahoru bez nápovědy.',
  gallows: 'Slova uhodnutá bez jediné chyby a bez nápovědy.',
  detective: 'Případy rozluštěné bez chybného písmene a bez nápovědy.',
  tetris: 'Kola aspoň s tuctem slov a bez nápovědy.',
  quotes: 'Výroky doplněné bez chybného písmene a bez nápovědy.',
}

/**
 * Jedna dlaždice statistiky.
 *
 * `term` ji pověsí na slovníček, `note` na vlastní větu, která se rozbalí
 * pod číslem. Bez jednoho i druhého by se na dlaždici nedalo kliknout a to je
 * ve Slovech porušení pravidla, ne úspora práce.
 */
function Stat({
  label,
  value,
  tone,
  note,
  term,
}: {
  label: string
  value: string | number
  tone?: 'accent' | 'gold'
  note?: string
  term?: string
}) {
  const { show } = useExplain()
  const [open, setOpen] = useState(false)

  return (
    <button
      type="button"
      className={`stat ${open ? 'open' : ''}`}
      onClick={() => (term ? show(term) : setOpen((was) => !was))}
    >
      <div className="label">{label}</div>
      <div className={`value num ${tone ?? ''}`}>{value}</div>
      {open && note && <div className="stat-explain">{note}</div>}
    </button>
  )
}

export function Stats({ profile, onBack, onReset }: Props) {
  const progress = rankFor(profile.fame)
  const played = MODES.reduce((sum, mode) => sum + profile.stats[mode].played, 0)

  return (
    <>
      <div className="section-head" style={{ marginTop: 0 }}>
        <h2>Statistiky</h2>
        <span className="rule" />
        <button type="button" className="btn btn-sm" onClick={onBack}>
          Zpět
        </button>
      </div>

      <div className="panel" style={{ marginBottom: 'var(--sp-5)' }}>
        <Explain term="hodnost" className="rank-line">
          <span className="rank">
            {progress.rank.name} · hodnost {progress.rank.index}
          </span>
          <span className="num muted">
            {profile.fame.toLocaleString('cs-CZ')} věhlasu
          </span>
        </Explain>
        <div className="fame-bar">
          <span
            style={{ width: `${progress.span ? (progress.into / progress.span) * 100 : 100}%` }}
          />
        </div>
        <p className="faint" style={{ fontSize: '0.8rem', marginTop: 'var(--sp-2)' }}>
          {progress.next
            ? `Do hodnosti ${progress.next.name} zbývá ${(
                progress.span - progress.into
              ).toLocaleString('cs-CZ')} věhlasu`
            : 'Nejvyšší hodnost — dál už se nešplhá'}
        </p>
      </div>

      <div className="stats-grid" style={{ marginBottom: 'var(--sp-5)' }}>
        <Stat label="Odehráno kol" value={played} term="odehrano" />
        <Stat
          label="Kol bez nápovědy"
          value={profile.counters.noHint}
          tone="accent"
          term="serie"
        />
        <Stat
          label="Nejdelší čistá řada"
          value={profile.bestStreak}
          tone="accent"
          term="serie"
        />
        <Stat label="Dní v řadě" value={profile.dayStreak} term="dny" />
        <Stat label="Nejvíc dní v řadě" value={profile.bestDayStreak} term="dny" />
        <Stat label="Dnů celkem" value={profile.daysPlayed} term="dny" />
        <Stat
          label="Pangramů"
          value={profile.counters.pangrams}
          tone="gold"
          term="pangram"
        />
        <Stat
          label="Celých pláství"
          value={profile.counters.hiveFull}
          note="Kolikrát jsi ve Voštině našel úplně všechna slova, do posledního."
        />
        <Stat
          label="Nejkratších cest"
          value={profile.counters.chainPar}
          note="Kolikrát jsi Řetěz dohrál na tolik tahů, kolik jich má nejkratší možná cesta."
        />
        <Stat
          label="Dostavěných věží"
          value={profile.counters.towerFull}
          note="Kolikrát jsi Věž postavil až do posledního patra."
        />
        <Stat
          label="Slov ze slabik"
          value={profile.counters.tetrisWords}
          note="Kolik slov jsi celkem složil z padajících slabik."
        />
        <Stat label="Denních výzev" value={profile.counters.dailies} term="denni" />
        <Stat label="Celých denních várek" value={profile.counters.dailySets} term="denni" />
        <Stat
          label="Nejlepší kolo"
          value={profile.counters.bestScore.toLocaleString('cs-CZ')}
          tone="gold"
          term="body"
        />
      </div>

      {MODES.map((mode) => {
        const stats = profile.stats[mode]
        const average = stats.played > 0 ? stats.totalScore / stats.played : 0
        const extra = stats.played > 0 ? stats.extra / stats.played : 0
        return (
          <section key={mode} style={{ marginBottom: 'var(--sp-5)' }}>
            <div className="section-head" style={{ marginTop: 'var(--sp-4)' }}>
              <h2>{MODE_LABEL[mode]}</h2>
              <span className="rule" />
            </div>
            <div className="stats-grid">
              <Stat
                label="Odehráno"
                value={stats.played}
                note={`Kolik kol hry ${MODE_LABEL[mode]} máš za sebou, včetně nepovedených.`}
              />
              <Stat
                label="Bez nápovědy"
                value={stats.clean}
                tone="accent"
                note="Kola dotažená do konce bez jediné nápovědy. Na tomhle čísle stojí žebříček mistrovství téhle hry."
              />
              <Stat
                label="Nejlepší skóre"
                value={stats.bestScore.toLocaleString('cs-CZ')}
                tone="accent"
                term="body"
              />
              <Stat
                label="Průměr"
                value={Math.round(average).toLocaleString('cs-CZ')}
                note="Průměrné skóre za kolo v téhle hře."
              />
              <Stat
                label="Perfektních"
                value={stats.perfect}
                tone="gold"
                note={PERFECT_NOTE[mode]}
              />
              <Stat
                label={EXTRA_LABEL[mode]}
                value={stats.played > 0 ? extra.toFixed(1).replace('.', ',') : '—'}
                note="Průměr za jedno odehrané kolo."
              />
            </div>
          </section>
        )
      })}

      <div className="section-head">
        <h2>Posledních {Math.min(profile.history.length, 15)} kol</h2>
        <span className="rule" />
      </div>
      <div className="card" style={{ padding: 'var(--sp-4) var(--sp-5)' }}>
        {profile.history.length === 0 && (
          <p className="faint">Zatím žádné dohrané kolo.</p>
        )}
        {profile.history.slice(0, 15).map((round, i) => (
          <div className="history-row" key={i}>
            <span className="chip">{MODE_LABEL[round.mode]}</span>
            <span className="muted" style={{ flex: 1, fontSize: '0.85rem' }}>
              {Object.entries(round.detail)
                .filter(([key]) => key !== 'extra')
                .map(([key, value]) => `${DETAIL_LABEL[key] ?? key} ${value}`)
                .join(' · ')}
            </span>
            {round.perfect && <span className="chip chip-gold">perfektní</span>}
            <span className="num" style={{ fontWeight: 600 }}>
              {round.score.toLocaleString('cs-CZ')}
            </span>
          </div>
        ))}
      </div>

      <div style={{ marginTop: 'var(--sp-6)', textAlign: 'center' }}>
        <button type="button" className="btn btn-sm btn-ghost" onClick={onReset}>
          Vymazat postup
        </button>
      </div>
    </>
  )
}
