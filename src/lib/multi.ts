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
  return { db, base: db.getDatabase(app), uid: user.uid }
}

const open = (): Promise<Db> => (ready ??= connect())

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
}

const EMPTY: Me = { nick: '', wins: 0, losses: 0, draws: 0 }

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
