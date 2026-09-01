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
import { foulNick } from '../game/nickCheck'
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
  /** Skryté id soupeře — potřebné k nahlášení a zablokování. */
  uid: string
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
  // Závadná jména se zastaví tady, tedy dřív, než je kdokoli uvidí.
  return foulNick(nick)
}

/* ---------- spojení ---------- */

type Db = Awaited<ReturnType<typeof connect>>

let ready: Promise<Db> | null = null

/**
 * Jak dlouho se čeká na server, než se to vzdá.
 *
 * Firebase žádnou lhůtu nemá: dokud se klient nespojí, zápis se drží ve
 * frontě a slib se **nikdy nesplní ani nezamítne**. Na obrazovce to vypadá
 * jako tlačítko, které navždycky svítí „Posílám…" — přesně tak vypadala
 * rozbitá výzva. Chyba se musí ozvat, i když druhá strana mlčí.
 */
const CEKANI_MS = 15_000

/**
 * Jak dlouho se čeká, než se databáze doopravdy spojí.
 *
 * Tohle je jiné čekání než to nahoře a musí být štědřejší. Přihlášení je
 * jeden obyčejný požadavek, kdežto databáze si drží **otevřené spojení**
 * a než ho navlékne, musí projít několik kroků: otevřít websocket (a když
 * ho síť nepustí, přepnout na záložní přenos, který je pomalejší),
 * vyměnit si přihlašovací lístek a teprve pak umí odpovídat. Na telefonu
 * to poprvé trvá klidně dvacet vteřin.
 *
 * Dřív se na to nečekalo vůbec: dotaz se poslal do ještě nespojeného
 * klienta a měřila se mu tatáž krátká lhůta jako všemu ostatnímu. Jednou
 * to stihl a hra běžela, podruhé ne a hlásilo se „server neodpovídá",
 * i když byl server v pořádku a stačilo mu dát chvíli. Proto se teď
 * napřed počká na spojení a **teprve pak** se posílá dotaz.
 */
const SPOJENI_PRVNI_MS = 8_000
const SPOJENI_DRUHY_MS = 15_000

/**
 * Chyba, kterou smí hráč přečíst.
 *
 * Zbytek — hlášky z Firebase jako `PERMISSION_DENIED` — se na obrazovku
 * nepouští; jsou v angličtině a hráči neřeknou nic. Obrazovky proto
 * ukazují text jen z téhle třídy a na všechno ostatní mají svoji větu.
 */
export class SoubojChyba extends Error {}

function docekat<T>(prace: Promise<T>, co: string): Promise<T> {
  let budik: ReturnType<typeof setTimeout> | undefined
  const lhuta = new Promise<never>((_, zamitnout) => {
    budik = setTimeout(
      () => zamitnout(new SoubojChyba(`Server neodpovídá (${co}). Zkus to za chvíli.`)),
      CEKANI_MS,
    )
  })
  return Promise.race([prace, lhuta]).finally(() => clearTimeout(budik))
}

/**
 * Přihlásí telefon a vrátí, co je potřeba k práci s databází.
 *
 * Přihlášení je anonymní — hráč nikam nezadává e‑mail ani heslo, jen
 * dostane skryté id, na které se navěsí přezdívka.
 */
async function connect() {
  const [core, auth, db] = await Promise.all([
    import('firebase/app'),
    import('firebase/auth'),
    import('firebase/database'),
  ])
  // Druhý pokus o spojení nesmí ztroskotat na tom, že aplikace už jednou
  // vznikla — `initializeApp` by podruhé vyhodil chybu a hráč by po jednom
  // výpadku sítě už souboje nerozchodil.
  const app = core.getApps().length > 0 ? core.getApp() : core.initializeApp(CONFIG)
  const session = auth.getAuth(app)
  // Sestavení pro emulátor (`SLOVA_EMU=1`). V běžném buildu je `__EMU__`
  // natvrdo `false`, takže tenhle blok z balíčku vypadne celý.
  if (__EMU__) {
    auth.connectAuthEmulator(session, 'http://127.0.0.1:9099', { disableWarnings: true })
  }
  const user = session.currentUser ?? (await auth.signInAnonymously(session)).user
  const base = db.getDatabase(app)
  if (__EMU__) db.connectDatabaseEmulator(base, '127.0.0.1', 9000)
  /*
   * Jen websocket, žádný záložní přenos.
   *
   * Firebase si přenos vybírá sám a **pamatuje si, co mu naposled nevyšlo**.
   * Stačí jediné klopýtnutí sítě — třeba když telefon na vteřinu ztratí
   * signál — a websocket se zapíše jako nefunkční; klient pak celé sezení
   * jede přes pomalejší záložní přenos a k websocketu se sám nevrátí, ani
   * když už dávno funguje. Když uvázne i ten záložní, nespojí se vůbec
   * a jediné, co pomůže, je zavřít celou aplikaci. Přesně tak to hráč
   * popisoval: jednou večer výzva projde, podruhé ne.
   *
   * `forceWebSockets` ten skrytý stav ruší — přenos je vždycky jeden a týž
   * a po výpadku se prostě zkusí znovu. Cenou je, že v síti, která
   * websockety vůbec nepouští, souboje nepojedou; z měření u hráče je ale
   * vidět, že websocket se otevírá bez potíží, a mlčky se zaseknout je
   * horší než se ozvat.
   */
  db.forceWebSockets()
  // O kolik jsou hodiny telefonu vedle. Voština v souboji odpočítává oběma
  // stejné tři minuty, takže se nesmí spoléhat na místní čas.
  db.onValue(db.ref(base, '.info/serverTimeOffset'), (snap) => {
    offset = Number(snap.val() ?? 0)
  })
  return { db, base, uid: user.uid }
}

/**
 * Spojení, které se dá zkusit znovu.
 *
 * Dřív tu stálo `ready ??= connect()`. Když se první pokus nepovedl —
 * telefon byl na vteřinu bez signálu, přihlášení se nedovolalo —, zůstal
 * v proměnné **zamítnutý slib** a vracel se pořád dokola. Souboje tím byly
 * mrtvé až do úplného restartu aplikace a rada „zkus to znovu, až budeš
 * online" se nedala poslechnout. Nepovedený pokus se proto zapomíná.
 */
function open(): Promise<Db> {
  ready ??= docekat(connect(), 'přihlášení').catch((chyba: unknown) => {
    ready = null
    throw chyba
  })
  return ready
}

/**
 * Spojení, přes které se dá **hned** ptát.
 *
 * `open()` vrací hotové přihlášení, ne hotové spojení s databází — to se
 * navléká na pozadí a chvíli to trvá. Kdo se chce ptát, počká si tady.
 * Kdo jen navěšuje posluchač (`subscribe`), čekat nemusí: posluchač si
 * počká sám a zavolá se, až data přijdou.
 */
function pockejNaSpojeni(db: Db['db'], base: Db['base'], kolik: number): Promise<boolean> {
  return new Promise<boolean>((hotovo) => {
    let odpojit: (() => void) | null = null
    let sesnuto = false
    const konec = (uspech: boolean) => {
      if (sesnuto) return
      sesnuto = true
      clearTimeout(budik)
      odpojit?.()
      hotovo(uspech)
    }
    const budik = setTimeout(() => konec(false), kolik)
    odpojit = db.onValue(db.ref(base, '.info/connected'), (snap) => {
      if (snap.val() === true) konec(true)
    })
    // Kdyby spojení stálo hned, `onValue` se ozve ještě uvnitř téhle řádky —
    // a `odpojit` by v tu chvíli bylo prázdné. Posluchač se proto odhlašuje
    // až tady, když se to stihlo.
    if (sesnuto) odpojit()
  })
}

async function pripraveno(): Promise<Db> {
  const spojeni = await open()
  const { db, base } = spojeni
  /*
   * Napřed se řekne „buď online", teprve pak se čeká.
   *
   * Klient se totiž sám od sebe nespojí — spojení navazuje, až když o data
   * někdo stojí. Čekání na `.info/connected` o data nestojí (ta větev se
   * obsluhuje v telefonu), takže samotné čekání ho nerozhýbe a vyprší
   * naprázdno. Poznalo se to z měření u hráče: spojení se navázalo za
   * 10,1 s, tedy přesně desetinu vteřiny po tom, co ho po marném čekání
   * probudilo `goOnline`. `goOnline` je přitom laciné a dá se volat kdykoli.
   */
  db.goOnline(base)
  if (await pockejNaSpojeni(db, base, SPOJENI_PRVNI_MS)) return spojeni

  /*
   * Nespojilo se. Než se to vzdá, spojení se zatřepe.
   *
   * Firebase si přenos vybírá sám a pamatuje si, co mu naposled nevyšlo —
   * když se jednou nepovede websocket, drží se pak celé sezení pomalejšího
   * záložního přenosu, a když uvázne i ten, sám od sebe už nic nezkusí.
   * `goOffline` + `goOnline` ho donutí začít načisto; hráč pak nemusí zavírat
   * celou aplikaci, což bylo jediné, co dosud pomáhalo.
   */
  db.goOffline(base)
  db.goOnline(base)
  if (await pockejNaSpojeni(db, base, SPOJENI_DRUHY_MS)) return spojeni

  throw new SoubojChyba(
    'Nepodařilo se spojit s databází. Zkontroluj připojení a zkus to znovu.',
  )
}

/**
 * Přečtení jedné větve — posluchačem, ne jednorázovým dotazem.
 *
 * Vypadá to jako oklika a je to jádro celé opravy. Firebase totiž obojí
 * doručuje jinak:
 *
 * * **Jednorázový dotaz (`get`)** se pošle po spojení a čeká na odpověď.
 *   Když spojení mezitím spadne — a ono padá, hned po navázání to je nejvíc
 *   pravděpodobné —, dotaz se **znovu neposílá**. Odpověď už nikdy nepřijde
 *   a slib visí. Přesně takhle padala výzva ve chvíli, kdy hráč u sebe viděl
 *   všechny čtyři kroky zelené: spojení stálo, jen odpověď na dotaz se
 *   ztratila při jednom přeťatém spojení.
 * * **Posluchač (`onValue`)** je součástí stavu, který si klient po
 *   obnoveném spojení sám navěsí znovu. Přežije tedy výpadek a data
 *   doručí, jakmile je zas kudy.
 *
 * Čte se proto posluchačem, kterého si po první hodnotě zase odhlásíme.
 * Chybu (třeba zamítnutá práva) hlásí druhá obsluha, takže se nezamění
 * s tichem.
 */
function precti(
  { db, base }: Pick<Db, 'db' | 'base'>,
  path: string,
  co: string,
): Promise<unknown> {
  return new Promise<unknown>((hotovo, zamitnout) => {
    let odpojit: (() => void) | null = null
    let sesnuto = false
    const konec = (udelej: () => void) => {
      if (sesnuto) return
      sesnuto = true
      clearTimeout(budik)
      odpojit?.()
      udelej()
    }
    const budik = setTimeout(
      () => konec(() => zamitnout(new SoubojChyba(`Server neodpovídá (${co}). Zkus to za chvíli.`))),
      CEKANI_MS,
    )
    odpojit = db.onValue(
      db.ref(base, path),
      (snap) => konec(() => hotovo(snap.val())),
      (chyba: unknown) => konec(() => zamitnout(chyba)),
    )
    // Data z paměti dorazí ještě uvnitř řádky výš — `odpojit` je pak prázdné
    // a posluchač by po sobě neuklidil.
    if (sesnuto) odpojit()
  })
}

/**
 * Navázat spojení předem, aby o tom šlo dát vědět.
 *
 * Čekání na spojení je ta nejdelší část celého odesílání a bez tohohle by
 * se odehrálo mlčky pod nápisem „Posílám výzvu…". Obrazovka si ho tímhle
 * vyžádá zvlášť a může u něj napsat, co se děje.
 */
export async function pripravSpojeni(): Promise<void> {
  await pripraveno()
}

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
  const { db, base, uid } = await pripraveno()
  const key = nickKey(nick)
  /*
   * Nejdřív se zjistí, kdo přezdívku drží.
   *
   * Zabírá se dvěma zápisy — jméno a k němu záznam hráče — a dřív se
   * rovnou psalo. Komu prošel první a druhý ne (spadlo spojení mezi nimi),
   * ten si svoje vlastní jméno zamkl: na serveru bylo zabrané jeho id, ale
   * bez záznamu hráče, takže se s ním nedalo nic dělat a každý další pokus
   * hlásil „tuhle přezdívku už někdo má". Vlastní jméno se proto pozná
   * a dopíše se jen to, co chybí.
   */
  const drzitel = await precti({ db, base }, `nicks/${key}`, 'přezdívka')
  if (drzitel != null && drzitel !== uid) return false
  if (drzitel == null) {
    try {
      await docekat(db.set(db.ref(base, `nicks/${key}`), uid), 'přezdívka')
    } catch (chyba) {
      // Někdo byl o vteřinu rychlejší — pravidla druhý zápis nepustí.
      // Do konzole i celá chyba: bez ní se „přezdívku už někdo má" nedalo
      // odlišit od skutečného zámku a hledalo se to hodně dlouho.
      console.error('Zabrání přezdívky selhalo:', chyba)
      return false
    }
  }
  await docekat(
    db.update(db.ref(base, `players/${uid}`), {
      nick: nick.trim(),
      key,
      seenAt: db.serverTimestamp(),
    }),
    'záznam hráče',
  )
  return true
}

/** Je tahle přezdívka volná? Pro průběžnou kontrolu při psaní. */
export async function nickFree(nick: string): Promise<boolean> {
  const { db, base } = await pripraveno()
  return (await precti({ db, base }, `nicks/${nickKey(nick)}`, 'přezdívka')) == null
}

/* ---------- karta hráče ---------- */

export interface KartaHrace {
  uid: string
  nick: string
  /** Hodnost profilu (1–58), nebo 0, když ji hráč ještě neposlal. */
  band: number
  wins: number
  losses: number
  draws: number
}

/**
 * Vlastní hodnost profilu na server, aby ji soupeř viděl.
 *
 * Posílá se samotné číslo, nic víc — jméno hodnosti si druhá strana dohledá
 * sama ze stejného seznamu. Píše se, jen když se změnila; hodnost roste
 * pomalu a zbytečný zápis při každém spuštění by byl jen šum.
 */
let poslednaHodnost = 0

export async function ulozHodnost(band: number): Promise<void> {
  if (!Number.isFinite(band) || band <= 0 || band === poslednaHodnost) return
  poslednaHodnost = band
  try {
    const { db, base, uid } = await pripraveno()
    await docekat(
      db.update(db.ref(base, `players/${uid}`), { band, seenAt: db.serverTimestamp() }),
      'hodnost',
    )
  } catch {
    // Hodnost je údaj pro ostatní, ne pro hru. Když se nezapíše, nic se
    // neděje — příště to zkusí znovu.
    poslednaHodnost = 0
  }
}

/** Přečte kartu soupeře. Vrací null, když o něm server nic neví. */
export async function nactiHrace(uid: string): Promise<KartaHrace | null> {
  const { db, base } = await pripraveno()
  const value = (await precti({ db, base }, `players/${uid}`, 'karta hráče')) as Record<
    string,
    unknown
  > | null
  if (!value) return null
  return {
    uid,
    nick: String(value.nick ?? '?'),
    band: Number(value.band ?? 0),
    wins: Number(value.wins ?? 0),
    losses: Number(value.losses ?? 0),
    draws: Number(value.draws ?? 0),
  }
}

/* ---------- zkouška spojení ---------- */

export interface Nalez {
  krok: string
  ok: boolean
  detail: string
}

function strucne(chyba: unknown): string {
  const text = chyba instanceof Error ? chyba.message : String(chyba)
  return text.replace(/\s+/g, ' ').slice(0, 90)
}

/**
 * Zkouška spojení se serverem.
 *
 * Souboje mají tři vrstvy a každá se dá rozbít zvlášť: přihlášení jde přes
 * jednu adresu, databáze přes druhou, a ta druhá se používá dvěma způsoby —
 * běžným požadavkem a websocketem, který si drží spojení otevřené. Hra sama
 * mluví websocketem; když neprojde, ostatní vrstvy můžou vesele fungovat
 * a navenek to vypadá, že „server neodpovídá".
 *
 * Bez tohohle rozlišení se nedá poznat, jestli je chyba v přihlášení,
 * v adrese databáze, v pravidlech, nebo v tom, že síť websockety nepustí —
 * a hádat se to z jedné věty na obrazovce nedá.
 */
export async function zkouskaSpojeni(): Promise<Nalez[]> {
  const out: Nalez[] = []
  const host = new URL(CONFIG.databaseURL).host
  const ns = host.split('.')[0]

  try {
    const uid = await myUid()
    out.push({ krok: 'Přihlášení', ok: true, detail: `id ${uid.slice(0, 8)}…` })
  } catch (chyba) {
    out.push({ krok: 'Přihlášení', ok: false, detail: strucne(chyba) })
  }

  // Běžný požadavek na databázi. Pravidla ho odmítnou (a to je v pořádku) —
  // podstatné je, že vůbec dorazí odpověď, tedy že je adresa dosažitelná.
  try {
    const stopka = new AbortController()
    const budik = setTimeout(() => stopka.abort(), 8000)
    try {
      const odpoved = await fetch(`https://${host}/.json?shallow=true`, {
        signal: stopka.signal,
      })
      const text = (await odpoved.text()).replace(/\s+/g, ' ').slice(0, 60)
      out.push({ krok: 'Databáze (běžný požadavek)', ok: true, detail: `${odpoved.status} ${text}` })
    } finally {
      clearTimeout(budik)
    }
  } catch (chyba) {
    out.push({ krok: 'Databáze (běžný požadavek)', ok: false, detail: strucne(chyba) })
  }

  // Spojení, které si drží sama hra. Tohle je ze všech kroků ten
  // nejdůležitější: hra se neptá websocketem přímo, ptá se přes Firebase,
  // a ten si spojení navléká sám a chvíli mu to trvá. Měří se, jak dlouho.
  const zacatek = Date.now()
  try {
    await pripraveno()
    out.push({
      krok: 'Spojení hry s databází',
      ok: true,
      detail: `navázáno za ${((Date.now() - zacatek) / 1000).toFixed(1)} s`,
    })
  } catch (chyba) {
    out.push({
      krok: 'Spojení hry s databází',
      ok: false,
      detail: `${strucne(chyba)} (po ${((Date.now() - zacatek) / 1000).toFixed(1)} s)`,
    })
  }

  // Websocket — tudy mluví hra doopravdy.
  const websocket = await new Promise<Nalez>((hotovo) => {
    let ws: WebSocket
    try {
      ws = new WebSocket(`wss://${host}/.ws?v=5&ns=${ns}`)
    } catch (chyba) {
      hotovo({ krok: 'Databáze (websocket)', ok: false, detail: strucne(chyba) })
      return
    }
    const budik = setTimeout(() => {
      ws.close()
      hotovo({ krok: 'Databáze (websocket)', ok: false, detail: 'do 10 s se neotevřel' })
    }, 10_000)
    ws.onopen = () => {
      clearTimeout(budik)
      ws.close()
      hotovo({ krok: 'Databáze (websocket)', ok: true, detail: 'otevřel se' })
    }
    ws.onerror = () => {
      clearTimeout(budik)
      hotovo({ krok: 'Databáze (websocket)', ok: false, detail: 'spojení se neotevřelo' })
    }
  })
  out.push(websocket)

  return out
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
/**
 * Zapíše výsledek denního kola a přečte, jak dopadli sledovaní hráči.
 *
 * Dřív se tady navíc **losoval** soupeř ze všech, kdo hádanku shodou
 * okolností hráli — hráč pak vyhrál nad někým, koho nikdy neviděl, nikde se
 * na to nedalo podívat a do bilance soubojů se to počítalo stejně jako
 * skutečné klání. Porovnává se proto jen s těmi, které si sám vybral,
 * a soubojová hodnost o denních kolech neví.
 *
 * Vlastní výsledek se zapisuje **až po přečtení** a jen jednou — pravidla
 * přepis neumožní, takže druhý pokus o tutéž hádanku tiše selže a to je
 * správně.
 */
export async function playRound(
  mode: ModeId,
  puzzle: string,
  score: number,
  band: number,
  sledovani: Sledovany[] = [],
): Promise<Duel[]> {
  const { db, base, uid } = await pripraveno()
  const path = `results/${mode}/${puzzle}`

  const nalezene: Duel[] = []
  for (const kdo of sledovani) {
    const row = (await precti({ db, base }, `${path}/${kdo.uid}`, 'výsledek hráče')) as
      | { nick?: string; score?: number }
      | null
    if (!row || typeof row.score !== 'number') continue
    nalezene.push({
      uid: kdo.uid,
      nick: String(row.nick ?? kdo.nick),
      score: row.score,
      won: score === row.score ? null : score > row.score,
    })
  }

  db.set(db.ref(base, `${path}/${uid}`), {
    nick: (await precti({ db, base }, `players/${uid}/nick`, 'profil')) ?? '?',
    score,
    band,
    at: db.serverTimestamp(),
  }).catch(() => undefined)

  return nalezene
}

/* ---------- sledovaní hráči ---------- */

/**
 * Přidá hráče mezi sledované.
 *
 * Hledá se podle přezdívky, tedy tak, jak se vyzývá na souboj. Vrací null,
 * když takový hráč není, a beze změny, když už sledovaný je.
 */
export async function pridejSledovaneho(me: Me, nick: string): Promise<Me | null> {
  const uid = await findPlayer(nick)
  if (!uid) return null
  const muj = await myUid()
  if (uid === muj) throw new SoubojChyba('Sám sebe sledovat nemusíš.')
  const jmeno = String(
    (await precti(await pripraveno(), `players/${uid}/nick`, 'profil hráče')) ?? nick,
  )
  if ((me.sledovani ?? []).some((one) => one.uid === uid)) return me
  const next: Me = {
    ...me,
    sledovani: [
      ...(me.sledovani ?? []),
      { uid, nick: jmeno, od: Date.now(), wins: 0, losses: 0, draws: 0, mine: 0, theirs: 0, hotovo: [] },
    ],
  }
  saveMe(next)
  return next
}

/** Přestane hráče sledovat i s celou tabulkou proti němu. */
export function smazSledovaneho(me: Me, uid: string): Me {
  const next: Me = { ...me, sledovani: (me.sledovani ?? []).filter((one) => one.uid !== uid) }
  saveMe(next)
  return next
}

/**
 * Připíše výsledky denního kola do tabulek sledovaných hráčů.
 *
 * Klíčem je `hra:hádanka`: totéž kolo se dozvíme dvakrát — hned po dohrání
 * a pak znovu, až se dopočítají odložená kola —, a dvakrát započítat se
 * nesmí. Sleduje se až ode dne, kdy si hráče přidal; zpětně se nic nedohání.
 */
export function zapisSledovane(
  me: Me,
  mode: ModeId,
  puzzle: string,
  score: number,
  nalezene: Duel[],
): Me {
  const klic = `${mode}:${puzzle}`
  const sledovani = (me.sledovani ?? []).map((kdo) => {
    const found = nalezene.find((one) => one.uid === kdo.uid)
    if (!found || (kdo.hotovo ?? []).includes(klic)) return kdo
    return {
      ...kdo,
      wins: kdo.wins + (found.won === true ? 1 : 0),
      losses: kdo.losses + (found.won === false ? 1 : 0),
      draws: kdo.draws + (found.won === null ? 1 : 0),
      mine: kdo.mine + score,
      theirs: kdo.theirs + found.score,
      hotovo: [klic, ...(kdo.hotovo ?? [])].slice(0, 300),
    }
  })
  const next: Me = { ...me, sledovani }
  saveMe(next)
  return next
}

/** Jak dlouho se čeká, než sledovaný hráč tutéž hádanku odehraje. */
const CEKANI_DNU = 7

/**
 * Odloží kolo, u kterého ještě někdo ze sledovaných nehrál.
 *
 * Denní výzvu si každý zahraje, kdy chce; kdo hraje ráno, nemá se v tu
 * chvíli s kým srovnat. Kolo proto počká a dopočítá se při návratu do hry.
 */
export function odlozKolo(me: Me, mode: ModeId, puzzle: string, score: number): Me {
  const klic = `${mode}:${puzzle}`
  const zive = (me.cekajici ?? []).filter(
    (one) => Date.now() - one.at < CEKANI_DNU * 86_400_000 && `${one.mode}:${one.puzzle}` !== klic,
  )
  const next: Me = { ...me, cekajici: [{ mode, puzzle, score, at: Date.now() }, ...zive].slice(0, 40) }
  saveMe(next)
  return next
}

/**
 * Dopočítá odložená kola — přečte, jestli už sledovaní hráči hráli.
 *
 * Vrací novou podobu `me`; kola, u kterých se všichni sledovaní ozvali
 * (nebo která jsou starší než týden), z čekání zmizí.
 */
export async function dopocitejCekajici(me: Me): Promise<Me> {
  const sledovani = me.sledovani ?? []
  const cekajici = (me.cekajici ?? []).filter(
    (one) => Date.now() - one.at < CEKANI_DNU * 86_400_000,
  )
  if (sledovani.length === 0 || cekajici.length === 0) {
    if (cekajici.length !== (me.cekajici ?? []).length) {
      const next: Me = { ...me, cekajici }
      saveMe(next)
      return next
    }
    return me
  }
  const { db, base } = await pripraveno()
  let stav = me
  const zbyva: CekajiciKolo[] = []
  for (const kolo of cekajici) {
    const path = `results/${kolo.mode}/${kolo.puzzle}`
    const nalezene: Duel[] = []
    for (const kdo of sledovani) {
      const row = (await precti({ db, base }, `${path}/${kdo.uid}`, 'výsledek hráče')) as
        | { nick?: string; score?: number }
        | null
      if (!row || typeof row.score !== 'number') continue
      nalezene.push({
        uid: kdo.uid,
        nick: String(row.nick ?? kdo.nick),
        score: row.score,
        won: kolo.score === row.score ? null : kolo.score > row.score,
      })
    }
    if (nalezene.length > 0) stav = zapisSledovane(stav, kolo.mode, kolo.puzzle, kolo.score, nalezene)
    // Dokud se neozvali všichni, kolo čeká dál — třeba dohrají večer.
    const klic = `${kolo.mode}:${kolo.puzzle}`
    const chybi = (stav.sledovani ?? []).some((kdo) => !(kdo.hotovo ?? []).includes(klic))
    if (chybi) zbyva.push(kolo)
  }
  const next: Me = { ...stav, cekajici: zbyva }
  saveMe(next)
  return next
}

/* ---------- co si hra pamatuje sama ---------- */

const KEY = 'slova.multi.v1'

/** Jeden dohraný souboj v archivu. */
export interface DuelLog {
  /** Id zápasu — podle něj se pozná, že už je zapsaný. */
  id: string
  kind: DuelKind
  rival: string
  mine: number
  theirs: number
  /** Kdy se výsledek dozvěděl tenhle telefon (ms). */
  at: number
  /**
   * Rozpisy obou stran, zakódované (viz `game/duelDetail`).
   *
   * Bez nich by se porovnání dalo otevřít jen do chvíle, než zápas
   * ze serveru zmizí. Archiv je v telefonu a musí si vystačit sám.
   */
  mineDetail?: string
  theirsDetail?: string
  /** Skryté id soupeře — kvůli erbu a kartě hráče v porovnání. */
  rivalUid?: string
}

/**
 * Hráč, se kterým se chci každý den porovnávat.
 *
 * Denní výzvu hraje každý sám a kdy chce; porovnat se ale dá, protože je
 * pro všechny tatáž. Dřív se soupeř k porovnání **losoval** z těch, kdo
 * hádanku shodou okolností hráli taky — hráč tak vyhrál nad někým, koho
 * nikdy neviděl, nikde se na to nedalo podívat a do bilance soubojů se to
 * počítalo stejně jako skutečné klání. Teď si vybírá sám, koho chce
 * sledovat, a vede se mu proti němu dlouhodobá tabulka.
 */
export interface Sledovany {
  /** Skryté id — podle něj se čtou jeho výsledky. */
  uid: string
  nick: string
  /** Odkdy se sleduje (ms). Starší dny se zpětně nedopočítávají. */
  od: number
  wins: number
  losses: number
  draws: number
  /** Součet bodů ze dnů, kdy hráli oba. */
  mine: number
  theirs: number
  /** Kola, která jsou už započítaná (`hra:hádanka`), ať se nepřičtou dvakrát. */
  hotovo: string[]
}

/**
 * Odehrané denní kolo, u kterého se čeká, jak dopadnou sledovaní hráči.
 *
 * Soupeř si tutéž hádanku zahraje třeba večer. Kolo se proto odloží
 * a dopočítá se, až se hráč do hry vrátí — a pak zmizí.
 */
export interface CekajiciKolo {
  mode: ModeId
  puzzle: string
  score: number
  /** Kdy jsem ho odehrál (ms). Po týdnu se zahazuje. */
  at: number
}

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
  /**
   * Zablokovaní hráči — jejich skrytá id.
   *
   * Drží se v telefonu, ne na serveru: blokování je moje věc a nikdo jiný
   * se nemá dozvědět, koho jsem si odklidil. Filtruje se jím všechno, co
   * ode mě může přijít i ke mně — náhodní soupeři i došlé výzvy.
   */
  blocked: string[]
  /**
   * Archiv dohraných soubojů.
   *
   * Bilance říká jen „sedm výher", ne proti komu a jak. Server si výsledky
   * drží u zápasů, jenže ty se čtou jen do chvíle, než je hráč jednou vidí —
   * pak by se zapomněly. Archiv je proto v telefonu a je v něm padesát
   * posledních; víc by se stejně nikdo neprocházel.
   */
  log: DuelLog[]
  /** Hráči, se kterými se porovnávají denní výzvy. */
  sledovani: Sledovany[]
  /** Odehraná denní kola, u kterých se ještě čeká na sledované hráče. */
  cekajici: CekajiciKolo[]
}

const EMPTY: Me = {
  nick: '',
  wins: 0,
  losses: 0,
  draws: 0,
  matches: [],
  blocked: [],
  log: [],
  sledovani: [],
  cekajici: [],
}

/** Zablokuje hráče a rovnou uloží. */
export function blockPlayer(me: Me, uid: string): Me {
  const next: Me = {
    ...me,
    blocked: [...new Set([...(me.blocked ?? []), uid])],
    // Zablokovaný hráč zmizí i ze žebříčku denních výzev. Blokování má
    // znamenat „už ho nechci vidět", ne „nechci od něj výzvy, ale každý
    // den se s ním budu srovnávat".
    sledovani: (me.sledovani ?? []).filter((one) => one.uid !== uid),
  }
  saveMe(next)
  return next
}

/**
 * Nahlásí hráče.
 *
 * Hlášení se zapisuje jen jedním směrem — přečíst si je může jen obsluha
 * v konzoli Firebase. Kdo koho nahlásil, se tedy k nahlášenému nedostane.
 */
export async function reportPlayer(
  uid: string,
  nick: string,
  reason: string,
): Promise<void> {
  try {
    const { db, base, uid: mine } = await pripraveno()
    await db.set(db.push(db.ref(base, 'reports')), {
      about: uid,
      nick,
      reason,
      from: mine,
      at: db.serverTimestamp(),
    })
  } catch {
    // Nahlášení, které se nedoručilo, nesmí shodit obrazovku. Zablokování,
    // které se děje spolu s ním, je místní a platí tak jako tak.
  }
}

/**
 * Smaže všechno, co si o hráči drží server.
 *
 * Vyžadují to pravidla obchodů: kdo si u hry založí jméno, musí ho umět
 * zase zrušit, a to přímo z aplikace. Maže se přezdívka, záznam hráče
 * i všechny došlé výzvy. Výsledky odehraných kol zůstávají — jsou uložené
 * pod skrytým id bez jména a jsou to čísla, ne osobní údaj.
 */
export async function eraseMe(): Promise<void> {
  try {
    const { db, base, uid } = await pripraveno()
    const key = String((await precti({ db, base }, `players/${uid}/key`, 'profil')) ?? '')
    await Promise.all([
      key ? db.remove(db.ref(base, `nicks/${key}`)) : Promise.resolve(),
      db.remove(db.ref(base, `players/${uid}`)),
      db.remove(db.ref(base, `challenges/${uid}`)),
    ])
  } finally {
    // Z telefonu se maže vždycky, i když server odmítne. Kdo o smazání
    // požádal, nemá dál koukat na svoji přezdívku jen proto, že vypadla síť —
    // a chyba se mu i tak ukáže, protože se výjimka pouští dál.
    try {
      localStorage.removeItem(KEY)
    } catch {
      // Soukromé okno bez úložiště — není co mazat.
    }
  }
}

/**
 * Zapíše dohraný souboj do archivu a rovnou uloží.
 *
 * Klíčem je id zápasu: výsledek se dozvíme dvakrát — jednou na konci hry
 * a podruhé, když ho vyzvedne přehled dohraných —, a dvakrát v seznamu by
 * nedával smysl.
 */
export function zapisSouboj(me: Me, zaznam: DuelLog): Me {
  const bezNej = (me.log ?? []).filter((one) => one.id !== zaznam.id)
  const next: Me = { ...me, log: [zaznam, ...bezNej].slice(0, 50) }
  saveMe(next)
  return next
}

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
  /**
   * Rozpis kol, zakódovaný (viz `game/duelDetail`).
   *
   * Nepovinný schválně: starší telefon ho neposílá a databázi, které
   * majitel nepřepsal pravidla, neprojde. Porovnání pak ukáže jen skóre.
   */
  detail?: string
}

export interface Challenge {
  id: string
  /** Skryté id vyzývatele. */
  from: string
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
  const { db, base } = await pripraveno()
  const found = await precti({ db, base }, `nicks/${nickKey(nick)}`, 'hledání hráče')
  return found == null ? null : (found as string)
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
  const { db, base, uid } = await pripraveno()
  const target = await findPlayer(rivalNick)
  if (!target) return null
  // Vlastní přezdívka není překlep — hráč se nemá dozvědět, že „takového
  // hráče neznáme", když se jmenuje přesně takhle.
  if (target === uid) throw new SoubojChyba('Sám sebe vyzvat nemůžeš.')
  const mine = String(
    (await precti({ db, base }, `players/${uid}/nick`, 'profil')) ?? '',
  )
  /*
   * Bez zapsané přezdívky se zápas založit nedá a nemá smysl to zkoušet:
   * pravidla databáze u něj ověřují, že jméno vyzývatele sedí s tím, co
   * o něm server ví. Dřív se místo jména poslal otazník, zápis se odmítl
   * a hráč se dozvěděl jen „nepodařilo se spojit".
   */
  if (!mine) {
    throw new SoubojChyba('Nejdřív si zaber přezdívku — bez ní tě soupeř nepozná.')
  }
  const guest = String(
    (await precti({ db, base }, `players/${target}/nick`, 'profil soupeře')) ??
      rivalNick,
  )

  const row = db.push(db.ref(base, 'duels'))
  const id = row.key!
  await docekat(
    db.set(row, {
      kind,
      puzzles: puzzles.join('|'),
      host: uid,
      hostNick: mine,
      guest: target,
      guestNick: guest,
      live: 0,
      ping: db.serverTimestamp(),
      at: db.serverTimestamp(),
    }),
    'založení zápasu',
  )
  await docekat(
    db.set(db.push(db.ref(base, `challenges/${target}`)), {
      from: uid,
      nick: mine,
      kind,
      match: id,
      at: db.serverTimestamp(),
    }),
    'odeslání výzvy',
  )
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
  const { db, base } = await pripraveno()
  const found = await precti({ db, base }, `duels/${id}`, 'načtení zápasu')
  return toMatch(id, found as Record<string, unknown> | null)
}

/** Sleduje zápas. Vrací funkci, kterou se sledování ukončí. */
export function watchMatch(id: string, onChange: (match: Match | null) => void): () => void {
  return subscribe(`duels/${id}`, (value) =>
    onChange(toMatch(id, value as Record<string, unknown> | null)),
  )
}

/** Vyzývatel dá vědět, že u Voštiny pořád čeká. */
export async function pingMatch(id: string): Promise<void> {
  const { db, base } = await pripraveno()
  await db.set(db.ref(base, `duels/${id}/ping`), db.serverTimestamp()).catch(() => undefined)
}

/** Soupeř výzvu přijal — zápas se rozjede. */
export async function startMatch(id: string): Promise<void> {
  const { db, base } = await pripraveno()
  await docekat(
    db.set(db.ref(base, `duels/${id}/live`), db.serverTimestamp()),
    'start zápasu',
  )
}

/** Vyzývatel čekání vzdal. */
export async function cancelMatch(id: string): Promise<void> {
  const { db, base } = await pripraveno()
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
  const { db, base, uid } = await pripraveno()
  try {
    await docekat(db.set(db.ref(base, `duels/${id}/words/${key}`), uid), 'slovo')
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

/**
 * Zapíše vlastní výsledek zápasu.
 *
 * Rozpis kol se posílá **na dvakrát**: nejdřív s ním, a když ho databáze
 * odmítne, ještě jednou bez něj. Pravidla se totiž nasazují ručně v konzoli
 * Firebase a nikdo nemá jistotu, že už tam nová jsou; kdyby se zápis
 * odmítl celý, přišel by hráč o výsledek souboje kvůli ozdobě.
 */
export async function finishMatch(
  id: string,
  nick: string,
  score: number,
  detail?: string,
): Promise<void> {
  const { db, base, uid } = await pripraveno()
  const kam = db.ref(base, `duels/${id}/done/${uid}`)
  if (detail) {
    const proslo = await docekat(
      db.set(kam, { nick, score, detail, at: db.serverTimestamp() }),
      'zápis výsledku',
    ).then(
      () => true,
      () => false,
    )
    if (proslo) return
  }
  await docekat(
    db.set(kam, { nick, score, at: db.serverTimestamp() }),
    'zápis výsledku',
  ).catch(() => undefined)
}

/** Přečte výsledky zápasu — pro proužek v menu, kde se nesleduje nic trvale. */
export async function matchDone(id: string): Promise<Record<string, MatchScore>> {
  const { db, base } = await pripraveno()
  const found = await precti({ db, base }, `duels/${id}/done`, 'výsledky zápasu')
  return (found as Record<string, MatchScore> | null) ?? {}
}

/** Uloží bilanci soubojů i na server, ať ji vidí ostatní. */
export async function saveTally(tally: Tally): Promise<void> {
  try {
    const { db, base, uid } = await pripraveno()
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
export function watchChallenges(
  onChange: (list: Challenge[]) => void,
  blocked: string[] = [],
): () => void {
  let stop: (() => void) | null = null
  let dead = false
  void open().then(({ uid }) => {
    if (dead) return
    stop = subscribe(`challenges/${uid}`, (value) => {
      const rows = (value as Record<string, Omit<Challenge, 'id'>> | null) ?? {}
      onChange(
        Object.entries(rows)
          .map(([id, row]) => ({ id, ...row }))
          .filter((row) => !blocked.includes(row.from))
          .reverse(),
      )
    })
  })
  return () => {
    dead = true
    stop?.()
  }
}

/** Smaže vyřízenou výzvu. */
export async function dropChallenge(id: string): Promise<void> {
  const { db, base, uid } = await pripraveno()
  await db.remove(db.ref(base, `challenges/${uid}/${id}`)).catch(() => undefined)
}
