/**
 * Obchod — co se ve hře dá koupit.
 *
 * Slova zůstávají zdarma a hratelná celá. Kupuje se jen to, co hru
 * **rozšiřuje**, ne to, co by v ní jinak chybělo:
 *
 *   * **inkoust** — měna na nápovědy, kterou jde jinak nasbírat hraním,
 *   * **archivy** — staré denní výzvy a otázky, ke kterým se nový hráč
 *     jinak nedostane, protože propadly dřív, než přišel,
 *   * **kasička** — nekupuje vůbec nic, je to jen poděkování.
 *
 * Identifikátory se **nikdy nemění**. V Play Console se zakládají jednou
 * a jsou navždy svázané s tím, co si kdo koupil; přejmenování by lidem
 * sebralo, co zaplatili.
 *
 * Ceny jsou tady jen orientační, pro případ, že se nepodaří stáhnout ceník
 * z obchodu. **Platí vždycky to, co řekne Google** — mění se podle země,
 * daní i akcí a hra do toho nemá co mluvit.
 */

/** Co se s koupenou věcí stane. */
export type DruhPolozky =
  /** Spotřebuje se — inkoust přiteče do kalamáře a nákup se dá opakovat. */
  | 'spotrebni'
  /** Koupí se jednou a platí napořád. */
  | 'trvala'

export interface Polozka {
  /** Identifikátor v Play Console. Nikdy se nemění. */
  id: string
  druh: DruhPolozky
  nazev: string
  popis: string
  /** Orientační cena v korunách — skutečnou řekne obchod. */
  cena: number
  /** Kolik inkoustu přiteče. Jen u spotřebních položek. */
  inkoust?: number
  /** Nejvýhodnější balíček — v nabídce se zvýrazní. */
  doporucene?: boolean
}

/**
 * Balíčky inkoustu.
 *
 * Ceny jsou schválně měkké. Velká nápověda stojí 20 inkoustu, tedy kolem
 * šesti korun u prostředního balíčku — částka, nad kterou se člověk
 * nerozmýšlí. Kdyby jeden inkoust stál korunu, vyšla by táž nápověda na
 * dvacet a kupoval by ji málokdo.
 *
 * Větší balíček je vždycky výhodnější, ale ne tak, aby menší vypadal jako
 * past: rozdíl je zhruba dvojnásobek mezi krajními.
 */
export const INKOUST: Polozka[] = [
  {
    id: 'inkoust_100',
    druh: 'spotrebni',
    nazev: 'Kalamář',
    popis: '100 kapek inkoustu',
    cena: 29,
    inkoust: 100,
  },
  {
    id: 'inkoust_300',
    druh: 'spotrebni',
    nazev: 'Velký kalamář',
    popis: '300 kapek inkoustu',
    cena: 69,
    inkoust: 300,
    doporucene: true,
  },
  {
    id: 'inkoust_1000',
    druh: 'spotrebni',
    nazev: 'Sud inkoustu',
    popis: '1000 kapek inkoustu',
    cena: 169,
    inkoust: 1000,
  },
]

/**
 * Archivy.
 *
 * Denní výzva propadne o půlnoci a kdo přišel ke hře později, o všechny
 * předchozí přišel. Archiv je otevře zpětně — je to jediná věc v obchodě,
 * která přidává **obsah**, ne úlevu.
 */
export const ARCHIVY: Polozka[] = [
  {
    id: 'archiv_vyzev',
    druh: 'trvala',
    nazev: 'Archiv denních výzev',
    popis: 'Všechny minulé denní výzvy ve všech hrách, kdykoli k dohrání.',
    cena: 99,
  },
  {
    id: 'archiv_otazek',
    druh: 'trvala',
    nazev: 'Archiv Otázek dne',
    popis: 'Všechny otázky, které kdy padly, i s indiciemi a odpověďmi.',
    cena: 79,
  },
]

/**
 * Kasička.
 *
 * Nekupuje se za ni nic — ani inkoust, ani obsah. Je to jediná položka,
 * u které je to tak schválně: kdo dá, dává za hru, kterou už má celou.
 * Proto jsou tři, ať si každý vybere podle toho, jak moc.
 */
export const KASICKA: Polozka[] = [
  {
    id: 'kasicka_mala',
    druh: 'trvala',
    nazev: 'Kafe autorovi',
    popis: 'Malé díky. Nic za to nedostaneš — o to jde.',
    cena: 49,
  },
  {
    id: 'kasicka_stredni',
    druh: 'trvala',
    nazev: 'Oběd autorovi',
    popis: 'Větší díky.',
    cena: 99,
  },
  {
    id: 'kasicka_velka',
    druh: 'trvala',
    nazev: 'Mecenáš',
    popis: 'Za tohle se dá psát dál.',
    cena: 249,
  },
]

/** Všechno, co se dá koupit — v pořadí, v jakém to má stát v nabídce. */
export const NABIDKA: Polozka[] = [...INKOUST, ...ARCHIVY, ...KASICKA]

const PODLE_ID = new Map(NABIDKA.map((p) => [p.id, p]))

export function polozka(id: string): Polozka | undefined {
  return PODLE_ID.get(id)
}

/** Odemyká tenhle nákup archiv? Kasička se do ničeho nepočítá. */
export function odemyka(id: string): 'vyzvy' | 'otazky' | null {
  if (id === 'archiv_vyzev') return 'vyzvy'
  if (id === 'archiv_otazek') return 'otazky'
  return null
}

/**
 * Kolik inkoustu za korunu — jen pro popisek „nejvýhodnější".
 *
 * Počítá se z orientační ceny, takže po přepočtu na cizí měnu může být
 * vedle. Proto se z toho nic neodvozuje, jen se tím zvýrazní jeden řádek.
 */
export function kapekZaKorunu(p: Polozka): number {
  if (!p.inkoust || p.cena <= 0) return 0
  return p.inkoust / p.cena
}
