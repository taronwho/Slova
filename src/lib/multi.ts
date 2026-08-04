/**
 * Souboje — tenká vrstva nad Firebase.
 *
 * Multiplayer je jediná část hry, která potřebuje síť, takže se drží
 * stranou od všeho ostatního a řídí se třemi pravidly:
 *
 * 1. **Firebase se načte, až když je potřeba.** Import je uvnitř funkcí,
 *    ne nahoře v souboru. Hlavní balík hry tím nenaroste a hra zůstane
 *    použitelná offline; kdo se do soubojů nepodívá, nestáhne ani bajt.
 * 2. **Jednosouborová verze souboje nemá.** Ta se skládá do jediného
 *    HTML a nesmí sáhnout na síť — proto `MULTI_ON`.
 * 3. **Vlastní hra nikdy nečeká na server.** Všechny funkce tady se
 *    volají až po dohraném kole, nebo vedle hraní. Když selžou, hráč to
 *    pozná jen tím, že se souboj neukáže.
 *
 * Skóre ze soubojů **nejde do věhlasu ani do ocenění**. Dva domluvení
 * kamarádi by si jinak vyfarmili hodnosti za večer.
 */

import type { DuelKind } from '../game/duel'
import type { ModeId } from '../game/types'

/** Konfigurace projektu. Není to tajemství — ochranu dělají pravidla. */
const CONFIG = {
  apiKey: 'AIzaSyCP2B80opEgCy3E5BdQEIPj9tc2j2iMoBs',
  authDomain: 'slova-b0176.firebaseapp.com',
  databaseURL: 'https://slova-b0176-default-rtdb.europe-west1.firebasedatabase.app',
  projectId: 'slova-b0176',
  storageBucket: 'slova-b0176.firebasestorage.app',
  messagingSenderId: '591894657531',
  appId: '1:591894657531:web:8afd620ac9f8c848c6b35e',
}

/** V jednosouborové verzi se souboje vypnou — ta nesmí na síť vůbec. */
export const MULTI_ON = !__STANDALONE__

export interface Duel {
  /** Přezdívka soupeře. */
  nick: string
  score: number
  /** true = vyhrál jsi, false = prohrál, null = shoda. */
  won: boolean | null
}

export interface Tally {
  wins: number
  losses: number
  draws: number
}

/** Přezdívka pro zápis do databáze: bez diakritiky, malá písmena. */
export function nickKey(nick: string): string {
  return nick
    .normalize('NFD')
    .replace(/\p{M}/gu, '')
    .toLowerCase()
    .replace(/[^a-z0-9_-]/g, '')
}

export const NICK_MIN = 3
export const NICK_MAX = 16

/** Sedí přezdívka na pravidla? Vrací chybu k zobrazení, nebo null. */
export function nickError(nick: string): string | null {
  const key = nickKey(nick)
  if (key.length < NICK_MIN) return `Aspoň ${NICK_MIN} znaky.`
  if (key.length > NICK_MAX) return `Nejvýš ${NICK_MAX} znaků.`
  if (nick.trim() !== nick) return 'Bez mezer na začátku a na konci.'
  return null
}

/* ---------- spojení ---------- */

type Db = Awaited<ReturnType<typeof connect>>

let ready: Promise<Db> | null = null

/**
 * Přihlásí telefon a vrátí, co je potřeba k práci s databází.
 *
 * Přihlášení je anonymní — hráč nikam nezadává e‑mail ani heslo, jen
 * dostane skryté id, na které se navěsí přezdívka.
 */
async function connect() {
  const [{ initializeApp }, auth, db] = await Promise.all([
    import('firebase/app'),
    import('firebase/auth'),
    import('firebase/database'),
  ])
  const app = initializeApp(CONFIG)
  const session = auth.getAuth(app)
  const user = session.currentUser ?? (await auth.signInAnonymously(session)).user
  const base = db.getDatabase(app)
  // O kolik jsou hodiny telefonu vedle. Voština v souboji odpočítává oběma
  // stejné tři minuty, takže se nesmí spoléhat na místní čas.
  db.onValue(db.ref(base, '.info/serverTimeOffset'), (snap) => {
    offset = Number(snap.val() ?? 0)
  })
  return { db, base, uid: user.uid }
}

const open = (): Promise<Db> => (ready ??= connect())

/** Rozdíl mezi hodinami telefonu a serverem, v milisekundách. */
let offset = 0

/**
 * Trvalé sledování jedné větve.
 *
 * Vrací se rovnou, ještě než je spojení hotové — volající tak nemusí nic
 * čekat a odhlásit se dá kdykoli, i uprostřed přihlašování.
 */
function subscribe(path: string, onChange: (value: unknown) => void): () => void {
  let stop: (() => void) | null = null
  let dead = false
  void open()
    .then(({ db, base }) => {
      if (dead) return
      stop = db.onValue(db.ref(base, path), (snap) => onChange(snap.val()))
    })
    .catch(() => undefined)
  return () => {
    dead = true
    stop?.()
  }
}

/* ---------- přezdívka ---------- */

/**
 * Zabere přezdívku. Vrací true, když se to povedlo.
 *
 * Zabírá se zápisem do `nicks/{klíč}`, který pravidla pustí jen tehdy,
 * když tam ještě nic není. Když dva lidé pošlou totéž jméno v tutéž
 * vteřinu, uspěje právě jeden — bez transakce a bez čekání.
 */
export async function claimNick(nick: string): Promise<boolean> {
  const { db, base, uid } = await open()
  const key = nickKey(nick)
  try {
    await db.set(db.ref(base, `nicks/${key}`), uid)
  } catch {
    return false
  }
  await db.update(db.ref(base, `players/${uid}`), {
    nick: nick.trim(),
    key,
    seenAt: db.serverTimestamp(),
  })
  return true
}

/** Je tahle přezdívka volná? Pro průběžnou kontrolu při psaní. */
export async function nickFree(nick: string): Promise<boolean> {
  const { db, base } = await open()
  const found = await db.get(db.ref(base, `nicks/${nickKey(nick)}`))
  return !found.exists()
}

/* ---------- kolo ---------- */

/**
 * Zapíše výsledek a vrátí soupeře, se kterým se hráč utkal.
 *
 * Soupeř se hledá mezi těmi, kdo hráli **tutéž hádanku** — nemusí být
 * online, stačí, že tu byl někdy dřív. Tím odpadá čekání ve frontě
 * i celá otázka latence: neporovnávají se tahy, ale hotové výsledky.
 *
 * Vybírá se z podobného pásma hodnosti, aby nováček nedostával výprask
 * od někoho s milionem věhlasu. Když v pásmu nikdo není, bere se kdokoli.
 */
export async function playRound(
  mode: ModeId,
  puzzle: string,
  score: number,
  band: number,
): Promise<Duel | null> {
  const { db, base, uid } = await open()
  const path = `results/${mode}/${puzzle}`

  const all = await db.get(db.ref(base, path))
  const rows: { uid: string; nick: string; score: number; band: number }[] = []
  all.forEach((row) => {
    const value = row.val() as { nick: string; score: number; band: number }
    if (row.key && row.key !== uid) rows.push({ uid: row.key, ...value })
  })

  // Vlastní výsledek se zapisuje až po přečtení, aby se hráč nepotkal sám
  // se sebou, a jen jednou — pravidla přepis neumožní, takže druhý pokus
  // o tutéž hádanku tiše selže a to je správně.
  db.set(db.ref(base, `${path}/${uid}`), {
    nick: (await db.get(db.ref(base, `players/${uid}/nick`))).val() ?? '?',
    score,
    band,
    at: db.serverTimestamp(),
  }).catch(() => undefined)

  if (rows.length === 0) return null
  const near = rows.filter((row) => Math.abs(row.band - band) <= 5)
  const pool = near.length > 0 ? near : rows
  const rival = pool[Math.floor(Math.random() * pool.length)]!
  return {
    nick: rival.nick,
    score: rival.score,
    won: score === rival.score ? null : score > rival.score,
  }
}

/** Připíše výsledek souboje do vlastní tabulky. */
export async function recordDuel(duel: Duel, before: Tally): Promise<Tally> {
  const next: Tally = {
    wins: before.wins + (duel.won === true ? 1 : 0),
    losses: before.losses + (duel.won === false ? 1 : 0),
    draws: before.draws + (duel.won === null ? 1 : 0),
  }
  try {
    const { db, base, uid } = await open()
    await db.update(db.ref(base, `players/${uid}`), { ...next, seenAt: db.serverTimestamp() })
  } catch {
    // Tabulka je jen ozdoba; když se nezapíše, hra běží dál.
  }
  return next
}

/* ---------- co si hra pamatuje sama ---------- */

const KEY = 'slova.multi.v1'

export interface Me extends Tally {
  nick: string
  /**
   * Zápasy, které čekají na dohrání soupeřem.
   *
   * U Vetřelce si vyzývatel odehraje svoje tři kola hned a soupeř třeba až
   * druhý den. Aby se výsledek neztratil, drží si vyzývatel id zápasu
   * u sebe a při návratu do menu se na něj podívá.
   */
  matches: string[]
}

const EMPTY: Me = { nick: '', wins: 0, losses: 0, draws: 0, matches: [] }

/** Přidá zápas mezi rozehrané a rovnou uloží. */
export function rememberMatch(me: Me, id: string): Me {
  const next: Me = {
    ...me,
    matches: [id, ...(me.matches ?? []).filter((one) => one !== id)].slice(0, 12),
  }
  saveMe(next)
  return next
}

/** Vyřízený zápas ze seznamu zmizí. */
export function forgetMatch(me: Me, id: string): Me {
  const next: Me = { ...me, matches: (me.matches ?? []).filter((one) => one !== id) }
  saveMe(next)
  return next
}

/** Připíše výsledek souboje do bilance a uloží ji i na server. */
export function tallyWith(me: Me, won: boolean | null): Me {
  return {
    ...me,
    wins: me.wins + (won === true ? 1 : 0),
    losses: me.losses + (won === false ? 1 : 0),
    draws: me.draws + (won === null ? 1 : 0),
  }
}

/** Přezdívka a tabulka výher. Drží se zvlášť od profilu, protože se
 *  souboje nepočítají do věhlasu ani do ocenění. */
export function loadMe(): Me {
  try {
    const raw = localStorage.getItem(KEY)
    if (!raw) return EMPTY
    return { ...EMPTY, ...(JSON.parse(raw) as Partial<Me>) }
  } catch {
    return EMPTY
  }
}

export function saveMe(me: Me): void {
  try {
    localStorage.setItem(KEY, JSON.stringify(me))
  } catch {
    // Soukromé okno bez úložiště — souboje prostě nebudou.
  }
}

/* ---------- souboje na konkrétní hru ---------- */

/**
 * Zápas dvou jmenovitých hráčů.
 *
 * `live` je jediný stav, který zápas má: 0 znamená „vyzývatel čeká",
 * kladné číslo je čas startu (a u Voštiny se od něj odpočítávají tři
 * minuty), −1 znamená odvoláno. Nic dalšího se nikam nepíše, takže
 * zápas nemá jak uváznout v půli.
 */
export interface Match {
  id: string
  kind: DuelKind
  /** Id hádanek — jedna u Voštiny, tři u Vetřelce. */
  puzzles: string[]
  host: string
  hostNick: string
  guest: string
  guestNick: string
  live: number
  /** Poslední ozvání vyzývatele, dokud čeká u Voštiny. */
  ping: number
}

/** Výsledek jednoho hráče v zápase. */
export interface MatchScore {
  nick: string
  score: number
}

export interface Challenge {
  id: string
  /** Kdo vyzval. */
  nick: string
  kind: DuelKind
  match: string
  at: number
}

function toMatch(id: string, value: Record<string, unknown> | null): Match | null {
  if (!value) return null
  return {
    id,
    kind: value.kind as DuelKind,
    puzzles: String(value.puzzles ?? '').split('|').filter(Boolean),
    host: String(value.host ?? ''),
    hostNick: String(value.hostNick ?? '?'),
    guest: String(value.guest ?? ''),
    guestNick: String(value.guestNick ?? '?'),
    live: Number(value.live ?? 0),
    ping: Number(value.ping ?? 0),
  }
}

/** Moje skryté id. Podle něj se v zápase pozná, co je čí. */
export async function myUid(): Promise<string> {
  return (await open()).uid
}

/**
 * Čas serveru.
 *
 * Voština se hraje na tři minuty a oba telefony musí odpočítávat totéž.
 * Hodiny v telefonech se běžně liší o vteřiny; Firebase sám hlásí, o kolik
 * je ten který přístroj vedle, a tenhle rozdíl se přičte.
 */
export function serverNow(): number {
  return Date.now() + offset
}

/** Najde hráče podle přezdívky. Vrací jeho id, nebo null. */
export async function findPlayer(nick: string): Promise<string | null> {
  const { db, base } = await open()
  const found = await db.get(db.ref(base, `nicks/${nickKey(nick)}`))
  return found.exists() ? (found.val() as string) : null
}

/**
 * Založí zápas a pošle výzvu. Vrací null, když hráč s takovou přezdívkou není.
 *
 * Hádanky vybírá vyzývatel a zápas si je nese s sebou, takže soupeř hraje
 * přesně to samé — jinak by se výsledky neměly podle čeho porovnat.
 */
export async function createMatch(
  kind: DuelKind,
  puzzles: string[],
  rivalNick: string,
): Promise<Match | null> {
  const { db, base, uid } = await open()
  const target = await findPlayer(rivalNick)
  if (!target || target === uid) return null
  const mine = String((await db.get(db.ref(base, `players/${uid}/nick`))).val() ?? '?')
  const guest = String((await db.get(db.ref(base, `players/${target}/nick`))).val() ?? rivalNick)

  const row = db.push(db.ref(base, 'duels'))
  const id = row.key!
  await db.set(row, {
    kind,
    puzzles: puzzles.join('|'),
    host: uid,
    hostNick: mine,
    guest: target,
    guestNick: guest,
    live: 0,
    ping: db.serverTimestamp(),
    at: db.serverTimestamp(),
  })
  await db.set(db.push(db.ref(base, `challenges/${target}`)), {
    from: uid,
    nick: mine,
    kind,
    match: id,
    at: db.serverTimestamp(),
  })
  return {
    id,
    kind,
    puzzles,
    host: uid,
    hostNick: mine,
    guest: target,
    guestNick: guest,
    live: 0,
    ping: serverNow(),
  }
}

/** Přečte zápas. */
export async function loadMatch(id: string): Promise<Match | null> {
  const { db, base } = await open()
  const found = await db.get(db.ref(base, `duels/${id}`))
  return toMatch(id, found.val() as Record<string, unknown> | null)
}

/** Sleduje zápas. Vrací funkci, kterou se sledování ukončí. */
export function watchMatch(id: string, onChange: (match: Match | null) => void): () => void {
  return subscribe(`duels/${id}`, (value) =>
    onChange(toMatch(id, value as Record<string, unknown> | null)),
  )
}

/** Vyzývatel dá vědět, že u Voštiny pořád čeká. */
export async function pingMatch(id: string): Promise<void> {
  const { db, base } = await open()
  await db.set(db.ref(base, `duels/${id}/ping`), db.serverTimestamp()).catch(() => undefined)
}

/** Soupeř výzvu přijal — zápas se rozjede. */
export async function startMatch(id: string): Promise<void> {
  const { db, base } = await open()
  await db.set(db.ref(base, `duels/${id}/live`), db.serverTimestamp())
}

/** Vyzývatel čekání vzdal. */
export async function cancelMatch(id: string): Promise<void> {
  const { db, base } = await open()
  await db.set(db.ref(base, `duels/${id}/live`), -1).catch(() => undefined)
}

/**
 * Ukořistí slovo. Vrací false, když ho soupeř stihl dřív.
 *
 * Pravidla pustí zápis jen tam, kde ještě nic není, takže když dva lidé
 * odevzdají totéž slovo v tutéž vteřinu, uspěje právě jeden a druhému se
 * zápis odmítne. Žádná transakce ani čekání ve frontě k tomu není potřeba.
 */
export async function claimWord(id: string, key: string): Promise<boolean> {
  const { db, base, uid } = await open()
  try {
    await db.set(db.ref(base, `duels/${id}/words/${key}`), uid)
    return true
  } catch {
    return false
  }
}

/** Sleduje, komu co v plástvi patří. */
export function watchWords(
  id: string,
  onChange: (owners: Record<string, string>) => void,
): () => void {
  return subscribe(`duels/${id}/words`, (value) =>
    onChange((value as Record<string, string> | null) ?? {}),
  )
}

/** Zapíše vlastní výsledek zápasu. */
export async function finishMatch(id: string, nick: string, score: number): Promise<void> {
  const { db, base, uid } = await open()
  await db
    .set(db.ref(base, `duels/${id}/done/${uid}`), { nick, score, at: db.serverTimestamp() })
    .catch(() => undefined)
}

/** Přečte výsledky zápasu — pro proužek v menu, kde se nesleduje nic trvale. */
export async function matchDone(id: string): Promise<Record<string, MatchScore>> {
  const { db, base } = await open()
  const found = await db.get(db.ref(base, `duels/${id}/done`))
  return (found.val() as Record<string, MatchScore> | null) ?? {}
}

/** Uloží bilanci soubojů i na server, ať ji vidí ostatní. */
export async function saveTally(tally: Tally): Promise<void> {
  try {
    const { db, base, uid } = await open()
    await db.update(db.ref(base, `players/${uid}`), { ...tally, seenAt: db.serverTimestamp() })
  } catch {
    // Bilance je jen ozdoba; když se nezapíše, hra běží dál.
  }
}

/** Sleduje výsledky obou stran. */
export function watchDone(
  id: string,
  onChange: (rows: Record<string, MatchScore>) => void,
): () => void {
  return subscribe(`duels/${id}/done`, (value) =>
    onChange((value as Record<string, MatchScore> | null) ?? {}),
  )
}

/** Došlé výzvy. Poslouchá se, dokud je otevřené menu — výzva tak dorazí hned. */
export function watchChallenges(onChange: (list: Challenge[]) => void): () => void {
  let stop: (() => void) | null = null
  let dead = false
  void open().then(({ uid }) => {
    if (dead) return
    stop = subscribe(`challenges/${uid}`, (value) => {
      const rows = (value as Record<string, Omit<Challenge, 'id'>> | null) ?? {}
      onChange(Object.entries(rows).map(([id, row]) => ({ id, ...row })).reverse())
    })
  })
  return () => {
    dead = true
    stop?.()
  }
}

/** Smaže vyřízenou výzvu. */
export async function dropChallenge(id: string): Promise<void> {
  const { db, base, uid } = await open()
  await db.remove(db.ref(base, `challenges/${uid}/${id}`)).catch(() => undefined)
}
