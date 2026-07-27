/**
 * Inkoust — měna, za kterou se kupují nápovědy.
 *
 * Dřív se nápovědy zdarma sypaly přímo: ocenění, nová hodnost i denní várka
 * daly „jednu nápovědu" a bylo jedno, jestli si za ni hráč nechal odhalit
 * jedno písmeno, nebo rovnou celé slovo. Peněženka se tak plnila rychleji,
 * než se stíhala utrácet, a nápověda přestala být rozhodnutí.
 *
 * Teď se sbírá inkoust a nápovědy mají cenu. **Cena v inkoustu je desetina
 * bodové ceny téže nápovědy** — jedno pravidlo pro všech pět her, takže se
 * nedá splést a nová nápověda si cenu přinese sama. Prakticky to znamená, že
 * malá nápověda stojí 5 a odhalení celého slova 20; za totéž, co dřív koupilo
 * čtyři celá slova, je dnes jedno.
 *
 * Inkoust se utratí **místo bodů**, ne místo poctivé hry: kolo se pořád počítá
 * jako „s nápovědou", takže se za inkoust nedají koupit mety za hru bez
 * nápovědy. Šetří jen skóre.
 */

import type { Award } from './awards'

/** Cena nápovědy v inkoustu podle její bodové ceny. */
export function inkPrice(points: number): number {
  return Math.max(1, Math.round(points / 10))
}

/**
 * Kolik inkoustu padne za ocenění.
 *
 * Nejvyšší stupeň rodiny za dva a půl, ostatní za deset. Přes všech
 * sedmatřicet ocenění se nasbírá kolem 450 inkoustu — tedy zhruba dvacet
 * odhalených slov za celou hru, ne dvacet za večer.
 */
export function awardInk(award: Award): number {
  return award.tier === 3 ? 25 : 10
}

/**
 * Kolik inkoustu padne za nově dosaženou hodnost.
 *
 * Roste po pěticích, stejně jako se po pěticích mění odznak. První hodnosti
 * odsýpají, takže dávají málo; vysoké hodnosti jsou na hodně dlouhou trať
 * a stojí za víc.
 */
export function rankInk(index: number): number {
  return 8 + Math.floor((index - 1) / 5) * 6
}

/**
 * Za kompletní denní várku ve všech pěti hrách.
 *
 * Ne za každou výzvu zvlášť — jinak by denní várka sama zaplavila kalamář
 * víc než všechno ostatní dohromady.
 */
export const DAILY_INK = 8

/** Na uvítanou. Dvě střední nápovědy, ať si hráč zkusí, jak chutnají. */
export const START_INK = 30

/** Kolik inkoustu dostane hráč za jednu nápovědu zdarma ze starého profilu. */
export const LEGACY_HINT_INK = 12
