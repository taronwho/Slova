/**
 * Obrazovka HRA S PŘÁTELI.
 *
 * Souboje mají vlastní obrazovku, protože se řídí jinými pravidly než zbytek
 * hry: nedávají věhlas, neberou inkoust a nepočítají se do denní várky.
 * Míchat je mezi dlaždice her by slibovalo něco, co souboj nedělá.
 *
 * Drží čtyři věci a nic víc: kdo jsem, koho vyzvat, co došlo a jak to
 * dopadlo. Vysvětlení obou formátů stojí až dole — kdo sem přijde podruhé,
 * čte jen horní polovinu.
 */

import { useState } from 'react'

import {
  DUEL_ABOUT,
  DUEL_KINDS,
  DUEL_MODE,
  DUEL_TITLE,
  verdictOf,
  VERDICT_TITLE,
  type DuelKind,
} from '../game/duel'
import { MODE_GLYPH } from '../game/types'
import {
  claimNick,
  loadMe,
  nickError,
  saveMe,
  SoubojChyba,
  type Challenge,
  type Me,
} from '../lib/multi'

/** Dohraný zápas, o kterém hráč ještě neví. */
export interface DuelReport {
  id: string
  kind: DuelKind
  rival: string
  mine: number
  theirs: number
}

interface Props {
  me: Me
  onMe: (me: Me) => void
  challenges: Challenge[]
  onAccept: (challenge: Challenge) => void
  reports: DuelReport[]
  onSeen: (id: string) => void
  onChallenge: () => void
  onReport: (uid: string, nick: string) => void
  onUnblock: (uid: string) => void
  onErase: () => void
  onBack: () => void
}

export function Friends({
  me,
  onMe,
  challenges,
  onAccept,
  reports,
  onSeen,
  onChallenge,
  onReport,
  onUnblock,
  onErase,
  onBack,
}: Props) {
  const [draft, setDraft] = useState('')
  const [busy, setBusy] = useState(false)
  const [problem, setProblem] = useState<string | null>(null)

  async function claim() {
    const bad = nickError(draft)
    if (bad) {
      setProblem(bad)
      return
    }
    setBusy(true)
    setProblem(null)
    try {
      const free = await claimNick(draft)
      if (!free) {
        setProblem('Tuhle přezdívku už někdo má. Zkus jinou.')
        return
      }
      const next = { ...loadMe(), nick: draft.trim() }
      saveMe(next)
      onMe(next)
    } catch (chyba) {
      setProblem(
        chyba instanceof SoubojChyba
          ? chyba.message
          : 'Nepodařilo se spojit. Zkus to znovu, až budeš online.',
      )
    } finally {
      setBusy(false)
    }
  }

  const played = me.wins + me.losses + me.draws

  return (
    <div className="friends">
      <div className="friends-head">
        <span className="duel-mark big" aria-hidden="true">
          ⚔
        </span>
        <h1>Hra s přáteli</h1>
        <p className="muted">
          Vyzvi kamaráda podle přezdívky. Body ze soubojů se nepočítají do
          věhlasu ani do ocenění — jde v nich jen o to, kdo koho.
        </p>
      </div>

      {!me.nick ? (
        <div className="panel friends-claim">
          <h2>Zvol si přezdívku</h2>
          <p className="muted">
            Uvidí ji soupeři u výsledků a podle ní tě dokážou vyzvat. Každá může
            být ve hře jen jednou — kdo dřív přijde, ten ji má.
          </p>
          <input
            className="guess-input"
            value={draft}
            maxLength={16}
            placeholder="Přezdívka"
            onChange={(event) => {
              setDraft(event.target.value)
              setProblem(null)
            }}
            onKeyDown={(event) => {
              if (event.key === 'Enter') void claim()
            }}
          />
          {problem && <p className="duel-problem">{problem}</p>}
          <button
            type="button"
            className="btn btn-primary"
            disabled={busy || !draft}
            onClick={() => void claim()}
          >
            {busy ? 'Zapisuji…' : 'Zabrat přezdívku'}
          </button>
        </div>
      ) : (
        <>
          <div className="panel friends-me">
            <span className="friends-nick">{me.nick}</span>
            <span className="friends-tally">
              {played === 0 ? (
                <span className="faint">Zatím žádný souboj</span>
              ) : (
                <>
                  <b className="num">{me.wins}</b> výher ·{' '}
                  <b className="num">{me.losses}</b> proher ·{' '}
                  <b className="num">{me.draws}</b> remíz
                </>
              )}
            </span>
            <button type="button" className="btn btn-primary" onClick={onChallenge}>
              Vyzvat hráče
            </button>
          </div>

          {reports.length > 0 && (
            <div className="friends-list">
              <h2>Dohráno</h2>
              {reports.map((item) => {
                const verdict = verdictOf(item.mine, item.theirs)
                return (
                  <button
                    type="button"
                    className={`duel-strip report ${verdict}`}
                    key={item.id}
                    onClick={() => onSeen(item.id)}
                  >
                    <span className="duel-mark" aria-hidden="true">
                      {MODE_GLYPH[DUEL_MODE[item.kind]]}
                    </span>
                    <span className="duel-body">
                      <span className="duel-title">
                        {VERDICT_TITLE[verdict]} · {item.rival}
                      </span>
                      <span className="faint">
                        {item.mine.toLocaleString('cs-CZ')} :{' '}
                        {item.theirs.toLocaleString('cs-CZ')} · {DUEL_TITLE[item.kind]}
                      </span>
                    </span>
                  </button>
                )
              })}
            </div>
          )}

          <div className="friends-list">
            <h2>Došlé výzvy</h2>
            {challenges.length === 0 ? (
              <p className="faint">
                Zatím nic. Voština se hraje naráz, takže výzva na ni dorazí
                jen ve chvíli, kdy na tebe soupeř čeká — tady, v téhle nabídce.
              </p>
            ) : (
              challenges.map((item) => (
                /* Není to jeden `<button>`: nahlášení uvnitř spouštěče by bylo
                   tlačítko v tlačítku, což prohlížeč ani čtečka neunesou. */
                <div className="duel-strip challenge" key={item.id}>
                  <button
                    type="button"
                    className="duel-strip-go"
                    onClick={() => onAccept(item)}
                  >
                    <span className="duel-mark" aria-hidden="true">
                      {MODE_GLYPH[DUEL_MODE[item.kind]]}
                    </span>
                    <span className="duel-body">
                      <span className="duel-title">{item.nick} tě vyzval</span>
                      <span className="faint">{DUEL_TITLE[item.kind]}</span>
                    </span>
                  </button>
                  <button
                    type="button"
                    className="duel-strip-report"
                    aria-label={`Nahlásit hráče ${item.nick}`}
                    title="Nahlásit"
                    onClick={() => onReport(item.from, item.nick)}
                  >
                    !
                  </button>
                </div>
              ))
            )}
          </div>

          {(me.blocked ?? []).length > 0 && (
            <div className="friends-list">
              <h2>Zablokovaní</h2>
              <p className="faint">
                Tyhle hráče ti nepodstrčíme jako soupeře a jejich výzvy ti
                nedorazí. Odblokovat je můžeš kdykoli.
              </p>
              {(me.blocked ?? []).map((uid) => (
                <div className="duel-strip done" key={uid}>
                  <span className="duel-mark" aria-hidden="true">
                    ⊘
                  </span>
                  <span className="duel-body">
                    <span className="duel-title">Zablokovaný hráč</span>
                    <span className="faint">{uid.slice(0, 8)}…</span>
                  </span>
                  <button type="button" className="btn btn-sm" onClick={() => onUnblock(uid)}>
                    Odblokovat
                  </button>
                </div>
              ))}
            </div>
          )}
          {/* Kdo si u hry založil jméno, musí ho umět zase zrušit — a přímo
              odsud, ne mailem někam do prázdna. Maže se všechno, co o hráči
              ví server: přezdívka, záznam hráče i došlé výzvy. */}
          <div className="friends-list">
            <h2>Moje data</h2>
            <p className="faint">
              Hra o tobě ukládá přezdívku, výsledky odehraných kol a bilanci
              soubojů. Nic z toho není spojené se jménem, e‑mailem ani
              telefonním číslem — jen se skrytým id, které ti hra přidělila.
            </p>
            <div className="friends-erase">
              <button type="button" className="btn btn-sm" onClick={onErase}>
                Smazat přezdívku a data
              </button>
              <a
                className="btn btn-sm btn-ghost"
                href="./soukromi.html"
                target="_blank"
                rel="noreferrer"
              >
                Ochrana soukromí
              </a>
            </div>
          </div>
        </>
      )}

      <div className="friends-list">
        <h2>Co se dá hrát</h2>
        {DUEL_KINDS.map((kind) => (
          <div className="duel-pick" key={kind} data-mode={DUEL_MODE[kind]}>
            <span className="duel-pick-head">
              <span className="duel-mark" aria-hidden="true">
                {MODE_GLYPH[DUEL_MODE[kind]]}
              </span>
              <span className="duel-title">{DUEL_TITLE[kind]}</span>
            </span>
            <span className="faint">{DUEL_ABOUT[kind]}</span>
          </div>
        ))}
      </div>

      <div className="friends-actions">
        <button type="button" className="btn btn-ghost" onClick={onBack}>
          Zpět na hry
        </button>
      </div>
    </div>
  )
}
