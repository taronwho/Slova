/**
 * Placení přes Google Play.
 *
 * Slova jsou webová hra zabalená do androidí slupky (TWA). Nativní knihovna
 * Play Billing se do webu zavolat nedá, ale prohlížeč nabízí **Digital Goods
 * API**: uvnitř slupky umí říct ceny a spustit platbu, venku na webu není.
 *
 * Celý modul je proto psaný tak, aby **na webu tiše nic neuměl** a hra se
 * kvůli tomu nerozbila. `dostupne()` vrátí false, nabídka se neukáže a hráč
 * v prohlížeči hraje dál jako dosud — jen si nic nekoupí.
 *
 * ## Co tenhle modul zásadně neumí
 *
 * **Neověřuje nákup na serveru.** Kdo si upraví data v telefonu, přidá si
 * inkoust i bez placení. Je to vědomé rozhodnutí: hra si celý profil, včetně
 * inkoustu a věhlasu, drží stejně jen v telefonu, takže serverové ověřování
 * by hlídalo jedny dveře v domě bez zdí. Kdyby někdy přibyl server na
 * profily, patří ověřování k němu.
 */

/** Adresa, pod kterou se platby Google Play hlásí prohlížeči. */
const PLAY = 'https://play.google.com/billing'

/** To, co z Digital Goods API doopravdy používáme. */
interface Sluzba {
  getDetails(ids: string[]): Promise<PolozkaObchodu[]>
  listPurchases(): Promise<Nakup[]>
  consume(token: string): Promise<void>
}

export interface PolozkaObchodu {
  itemId: string
  title: string
  description?: string
  price: { currency: string; value: string }
}

export interface Nakup {
  itemId: string
  purchaseToken: string
}

interface OknoSPlatbami {
  getDigitalGoodsService?: (adresa: string) => Promise<Sluzba>
  PaymentRequest?: typeof PaymentRequest
}

function okno(): OknoSPlatbami | null {
  return typeof window === 'undefined' ? null : (window as unknown as OknoSPlatbami)
}

/** Chyba, kterou má smysl ukázat hráči. */
export class PlatbaChyba extends Error {}

let sluzba: Sluzba | null = null
let zkousenoUz = false

/**
 * Připojí se k obchodu, nebo vrátí null.
 *
 * Výsledek se pamatuje — v prohlížeči by se jinak při každém otevření
 * nabídky zkoušelo totéž a pokaždé to selhalo.
 */
async function pripoj(): Promise<Sluzba | null> {
  if (zkousenoUz) return sluzba
  zkousenoUz = true
  const w = okno()
  if (!w?.getDigitalGoodsService || !w.PaymentRequest) return null
  try {
    sluzba = await w.getDigitalGoodsService(PLAY)
  } catch {
    // Mimo slupku se ozve chybou; není to nic mimořádného.
    sluzba = null
  }
  return sluzba
}

/** Dá se v téhle podobě hry vůbec platit? */
export async function dostupne(): Promise<boolean> {
  return (await pripoj()) !== null
}

/**
 * Ceny z obchodu.
 *
 * Vrací jen to, co obchod opravdu zná — položka, kterou v Play Console
 * nikdo nezaložil, se v nabídce neukáže. Je to schválně: nabídnout něco,
 * co po ťuknutí spadne, je horší než to nenabídnout.
 */
export async function ceny(ids: string[]): Promise<Map<string, PolozkaObchodu>> {
  const s = await pripoj()
  if (!s) return new Map()
  try {
    const nalezene = await s.getDetails(ids)
    return new Map(nalezene.map((p) => [p.itemId, p]))
  } catch {
    return new Map()
  }
}

/**
 * Koupí položku a vrátí nákup.
 *
 * Spotřební položky (inkoust) se hned **spotřebují**, jinak by je obchod
 * považoval za pořád vlastněné a podruhé by je nedovolil koupit.
 */
export async function koupit(id: string, spotrebni: boolean): Promise<Nakup> {
  const s = await pripoj()
  const w = okno()
  if (!s || !w?.PaymentRequest) {
    throw new PlatbaChyba('Nakupovat jde jen v aplikaci z Google Play.')
  }

  let odpoved: PaymentResponse
  try {
    const zadost = new w.PaymentRequest(
      [{ supportedMethods: PLAY, data: { sku: id } }],
      // Částku určuje obchod podle položky; tohle je jen povinná výplň,
      // kterou Play ignoruje.
      { total: { label: 'Celkem', amount: { currency: 'CZK', value: '0' } } },
    )
    odpoved = await zadost.show()
  } catch (proc) {
    // Zrušení hráčem není chyba, kterou má cenu vypisovat jako poruchu.
    const zprava = proc instanceof Error ? proc.message : ''
    throw new PlatbaChyba(
      /abort|cancel/i.test(zprava) ? 'Nákup jsi zrušil.' : 'Platba neproběhla.',
    )
  }

  const token = String(
    (odpoved.details as { purchaseToken?: string } | undefined)?.purchaseToken ?? '',
  )
  await odpoved.complete('success')
  if (!token) throw new PlatbaChyba('Obchod nevrátil doklad o nákupu.')

  if (spotrebni) {
    try {
      await s.consume(token)
    } catch {
      // Nespotřebovaný inkoust se pozná při příštím `obnovit()` a doplní se
      // tam; shodit kvůli tomu nákup, který hráč zaplatil, by bylo horší.
    }
  }
  return { itemId: id, purchaseToken: token }
}

/**
 * Co má hráč koupené.
 *
 * Volá se při spuštění: trvalé nákupy drží Google, ne telefon, takže se po
 * přeinstalování hry nebo na novém telefonu takhle vrátí. Bez toho by hráč
 * o zaplacený archiv přišel a měl by pravdu, kdyby se zlobil.
 */
export async function obnovit(): Promise<Nakup[]> {
  const s = await pripoj()
  if (!s) return []
  try {
    return await s.listPurchases()
  } catch {
    return []
  }
}

/**
 * Spotřebuje nákup, který zůstal viset.
 *
 * Stane se to, když hra spadne mezi zaplacením a připsáním inkoustu.
 * Nákup pak v obchodě leží jako nespotřebovaný a tohle ho dořeší.
 */
export async function spotrebovat(token: string): Promise<void> {
  const s = await pripoj()
  if (!s) return
  try {
    await s.consume(token)
  } catch {
    // Když to nevyjde, zkusí se to zas příště.
  }
}

/** Jen pro testy — zapomene připojení, ať se dá zkoušet víc případů. */
export function zapomenNapojeni(): void {
  sluzba = null
  zkousenoUz = false
}
