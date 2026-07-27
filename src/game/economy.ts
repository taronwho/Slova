/**
 * Inkoust — měna, za kterou se kupují nápovědy.
 *
 * Dřív se nápovědy zdarma sypaly přímo: ocenění, nová hodnost i denní várka
 * daly „jednu nápovědu" a bylo jedno, jestli si za ni hráč nechal odhalit
 * jedno písmeno, nebo rovnou celé slovo. Peněženka se tak plnila rychleji,
 * než se stíhala utrácet, a nápověda přestala být rozhodnutí.
 *
 * Teď se sbírá inkoust a nápovědy mají cenu. **Cena v inkoustu je desetina
 * bodové ceny téže nápovědy** — jedno pravidlo pro všechny hry, takže se
 * nedá splést a nová nápověda si cenu přinese sama. Prakticky to znamená, že
 * malá nápověda stojí 5 a odhalení celého slova 20; za totéž, co dřív koupilo
 * čtyři celá slova, je dnes jedno.
 *
 * Inkoust se utratí **místo bodů**, ne místo poctivé hry: kolo se pořád počítá
 * jako „s nápovědou", takže se za inkoust nedají koupit mety za hru bez
 * nápovědy. Šetří jen skóre.
 */

import type { Award } from './awards'

/**
 * Cena nápovědy v inkoustu podle její bodové ceny.
 *
 * Dělitel není deset, ale 3,3 — bodové ceny nápověd šly spolu se skóre na
 * třetinu a inkoustové ceny měly zůstat, kde byly. Malá nápověda tak pořád
 * stojí pět, odhalení celého slova dvacet.
 */
export function inkPrice(points: number): number {
  return Math.max(1, Math.round(points / 3.3))
}

/**
 * Kolik inkoustu padne za ocenění.
 *
 * Odměna roste se stupněm žebříčku, ne s počtem met. Ocenění je přes sto
 * šedesát, ale drtivá většina jich je na nižších stupních a dá jen šest —
 * teprve pátý stupeň, na který se hraje sezónu, dá čtyřicet. Kdo posbírá
 * úplně všechno za celých pět let, nastřádá kolem tisíce inkoustu, tedy
 * zhruba padesát odhalených slov. Za večer ani za měsíc se kalamář nepřeleje.
 */
export const INK_BY_TIER = [10, 6, 10, 16, 26, 40]

export function awardInk(award: Award): number {
  return INK_BY_TIER[award.tier ?? 0] ?? 10
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
 * Za kompletní denní várku, tedy za denní výzvu ve všech hrách naráz.
 *
 * Ne za každou výzvu zvlášť — jinak by denní várka sama zaplavila kalamář
 * víc než všechno ostatní dohromady.
 */
export const DAILY_INK = 8

/** Na uvítanou. Dvě střední nápovědy, ať si hráč zkusí, jak chutnají. */
export const START_INK = 30

/** Kolik inkoustu dostane hráč za jednu nápovědu zdarma ze starého profilu. */
export const LEGACY_HINT_INK = 12
