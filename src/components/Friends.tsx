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
import { duelPoints, duelRankFor, DUEL_RANKS } from '../game/duelRank'
import { MODE_GLYPH } from '../game/types'
import { DuelCrest } from './art/DuelCrest'
import { DuelReportSheet } from './DuelReport'
import {
  pozadatOPovoleni,
  stavPovoleni,
  type Povoleni,
} from '../lib/upozorneni'
import {
  claimNick,
  loadMe,
  nickError,
  saveMe,
  SoubojChyba,
  zkouskaSpojeni,
  type Challenge,
  type DuelLog,
  type Me,
  type Nalez,
} from '../lib/multi'

/**
 * Souboj, který hráč odehrál a čeká, až si ho zahraje soupeř.
 *
 * U Vetřelce si každý zahraje, kdy chce, takže mezi „odehráno" a „známe
 * výsledek" může být klidně den. Bez tohohle výpisu to vypadalo, že se
 * souboj někam ztratil — hráč odehrál tři kola a pak už o zápase neslyšel.
 */
export interface DuelWaiting {
  id: string
  kind: DuelKind
  rival: string
  mine: number
}

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
  waiting: DuelWaiting[]
  onSeen: (id: string) => void
  /** Moje soubojová hodnost — erb v panelu i v porovnání. */
  duelRank: number
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
  waiting,
  onSeen,
  duelRank,
  onChallenge,
  onReport,
  onUnblock,
  onErase,
  onBack,
}: Props) {
  const [draft, setDraft] = useState('')
  const [busy, setBusy] = useState(false)
  const [problem, setProblem] = useState<string | null>(null)
  const [zkouska, setZkouska] = useState<Nalez[] | 'bezi' | null>(null)
  const [povoleni, setPovoleni] = useState<Povoleni>(() => stavPovoleni())
  /*
   * Otevřené porovnání.
   *
   * Bere se z archivu v telefonu, ne ze serveru: k odehranému souboji se
   * hráč vrací i po týdnech, kdy už zápas na serveru nemusí být.
   */
  const [rozbor, setRozbor] = useState<DuelLog | null>(null)

  async function zkusit() {
    setZkouska('bezi')
    setZkouska(await zkouskaSpojeni())
  }

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
  const soubojova = duelRankFor(duelPoints(me))

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
          {/*
            * Vlastní soubojová hodnost.
            *
            * Souboje se nepočítají do věhlasu — a bez vlastního žebříčku by
            * z nich nezůstalo nic než čísla výher. Tenhle roste pomalu (za
            * výhru tři body, za remízu jeden) a je to záznam o hraní proti
            * lidem, ne měřítko, kdo je lepší: k odehranému souboji je
            * pokaždé potřeba druhý člověk.
            */}
          <div className="panel friends-rank">
            <DuelCrest
              rank={soubojova.rank.index}
              size={56}
              title={`Erb hodnosti ${soubojova.rank.name}`}
            />
            <span className="label">Hodnost v soubojích</span>
            <b className="friends-rank-name">{soubojova.rank.name}</b>
            <span className="faint">
              {soubojova.rank.index}. z {DUEL_RANKS.length}
              {soubojova.next
                ? ` · do hodnosti ${soubojova.next.name} zbývá ${
                    soubojova.span - soubojova.into
                  } b.`
                : ' · nejvyšší'}
            </span>
            {soubojova.next && (
              <span
                className="friends-rank-bar"
                role="progressbar"
                aria-valuemin={0}
                aria-valuemax={soubojova.span}
                aria-valuenow={soubojova.into}
              >
                <i style={{ width: `${Math.round((soubojova.into / soubojova.span) * 100)}%` }} />
              </span>
            )}
          </div>

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

          {waiting.length > 0 && (
            <div className="friends-list">
              <h2>Čeká se na soupeře</h2>
              <p className="faint">
                Odehráno máš, teď je řada na druhém. Až si to zahraje,
                objeví se tu výsledek — u Vetřelce to může být klidně
                zítra, každý si ho zahraje, kdy chce.
              </p>
              {waiting.map((item) => (
                /* Není to tlačítko: čekat se dá jen tak, ťuknutí by nemělo
                   co udělat a tlačítko, které nic nedělá, je horší než text. */
                <div className="duel-strip pending" key={item.id}>
                  <span className="duel-mark" aria-hidden="true">
                    {MODE_GLYPH[DUEL_MODE[item.kind]]}
                  </span>
                  <span className="duel-body">
                    <span className="duel-title">Čeká se na {item.rival}</span>
                    <span className="faint">
                      {DUEL_TITLE[item.kind]} · tvoje skóre{' '}
                      {item.mine.toLocaleString('cs-CZ')}
                    </span>
                  </span>
                  <span className="duel-wait-mark" aria-hidden="true">
                    ⏳
                  </span>
                </div>
              ))}
            </div>
          )}

          {reports.length > 0 && (
            <div className="friends-list">
              <h2>Čerstvé výsledky</h2>
              {/*
                * Do bilance jsou tyhle souboje připsané už od chvíle, kdy
                * soupeř dohrál — tohle je jen upozornění, že se něco stalo,
                * dokud si toho hráč nevšimne. Ťuknutím se otevře porovnání
                * a proužek odsud zmizí; v odehraných zůstane napořád.
                */}
              <p className="faint">
                Soupeř dohrál, zatímco jsi byl pryč. Ťukni a podívej se, jak to
                dopadlo.
              </p>
              {reports.map((item) => {
                const verdict = verdictOf(item.mine, item.theirs)
                return (
                  <button
                    type="button"
                    className={`duel-strip report ${verdict}`}
                    key={item.id}
                    onClick={() => {
                      const zapis = (me.log ?? []).find((one) => one.id === item.id)
                      if (zapis) setRozbor(zapis)
                      onSeen(item.id)
                    }}
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

          {(me.log ?? []).length > 0 && (
            <div className="friends-list">
              <h2>Odehrané souboje</h2>
              <p className="faint">
                Posledních {Math.min((me.log ?? []).length, 50)} klání i s tím,
                jak dopadla. Ťukni na souboj a rozbalí se porovnání — kdo co
                odevzdal, za jak dlouho a kolik za to dostal.
              </p>
              {(me.log ?? []).map((item) => {
                const verdict = verdictOf(item.mine, item.theirs)
                return (
                  <button
                    type="button"
                    className={`duel-strip past ${verdict}`}
                    key={item.id}
                    onClick={() => setRozbor(item)}
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
                        {item.theirs.toLocaleString('cs-CZ')} · {DUEL_TITLE[item.kind]} ·{' '}
                        {new Date(item.at).toLocaleDateString('cs-CZ', {
                          day: 'numeric',
                          month: 'numeric',
                        })}
                      </span>
                    </span>
                    <span className="duel-strip-more" aria-hidden="true">
                      ›
                    </span>
                  </button>
                )
              })}
            </div>
          )}

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
            {/*
              * Upozornění na došlou výzvu.
              *
              * Ptá se až tady, z ťuknutí — bez gesta prohlížeče žádost rovnou
              * zamítnou a druhá šance pak není. A rovnou se říká, kam
              * upozornění dosáhnou: dokud hra běží (i schovaná), ne když je
              * zavřená. Slibovat víc by bylo horší než neslíbit nic.
              */}
            {povoleni !== 'nejde' && (
              <div className="friends-notify">
                {povoleni === 'nezeptáno' && (
                  <button
                    type="button"
                    className="btn btn-sm"
                    onClick={() => void pozadatOPovoleni().then(setPovoleni)}
                  >
                    Upozorňovat na došlé výzvy
                  </button>
                )}
                <p className="faint">
                  {povoleni === 'ano'
                    ? 'Upozornění na výzvy jsou zapnutá. Přijdou, dokud hra běží — i když ji máš schovanou. Když ji úplně zavřeš, dozvíš se o výzvě až po otevření.'
                    : povoleni === 'ne'
                      ? 'Upozornění máš pro tuhle hru zakázaná. Zapnout se dají v nastavení telefonu u aplikace.'
                      : 'Dají se zapnout upozornění, když tě někdo vyzve. Chodí, dokud hra běží — i když ji máš schovanou na pozadí.'}
                </p>
              </div>
            )}

            {/*
              * Zkouška spojení.
              *
              * Souboje jsou jediná část hry, která potřebuje server, a když
              * mlčí, nedá se z jedné hlášky poznat proč: jestli je chyba
              * v přihlášení, v adrese databáze, nebo v tom, že síť nepustí
              * websockety. Tohle to rozebere na tři kroky a napíše, který
              * z nich neprošel — dá se to vyfotit a poslat.
              */}
            <div className="friends-check">
              <button
                type="button"
                className="btn btn-sm btn-ghost"
                onClick={() => void zkusit()}
                disabled={zkouska === 'bezi'}
              >
                {zkouska === 'bezi' ? 'Zkouším…' : 'Zkusit spojení se serverem'}
              </button>
              {Array.isArray(zkouska) && (
                <ul className="check-list">
                  {zkouska.map((nalez) => (
                    <li key={nalez.krok} className={nalez.ok ? 'ok' : 'bad'}>
                      <span aria-hidden="true">{nalez.ok ? '✓' : '✗'}</span> {nalez.krok}:{' '}
                      <span className="faint">{nalez.detail}</span>
                    </li>
                  ))}
                </ul>
              )}
            </div>

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

      {rozbor && (
        <DuelReportSheet
          id={rozbor.id}
          kind={rozbor.kind}
          verdict={verdictOf(rozbor.mine, rozbor.theirs)}
          me={{ nick: me.nick, score: rozbor.mine, detail: rozbor.mineDetail, rank: duelRank }}
          rivalNick={rozbor.rival}
          rival={{
            nick: rozbor.rival,
            score: rozbor.theirs,
            detail: rozbor.theirsDetail,
            ...(rozbor.rivalUid ? { uid: rozbor.rivalUid } : {}),
          }}
          onClose={() => setRozbor(null)}
        />
      )}
    </div>
  )
}
