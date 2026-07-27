/**
 * Výkladový slovníček — co která věc ve Slovech znamená.
 *
 * Hra má vlastní názvosloví (věhlas, inkoust, série, plástev) a hráč se ho
 * nikde nedozví, když ho jen uvidí v liště. Proto je **na všechno vidět
 * kliknout**: každý čip, každé číslo v profilu, každá dlaždice ocenění vede
 * buď sem, do jednoho odstavce vysvětlení, nebo rovnou na obrazovku, o které
 * se mluví. Nikde nemá zůstat popisek, na který si hráč ťukne a nic se nestane.
 *
 * Texty jsou schválně krátké — tři čtyři věty. Kdo chce víc, klikne na odkaz
 * pod výkladem; kdo si jen ověřuje, co je zač ten kalamář, odejde po první větě.
 *
 * Čísla se sem **nekopírují ručně**. Ceny nápověd i výnosy z ocenění se
 * počítají z economy.ts, takže se výklad nemůže rozejít s tím, co hra doopravdy
 * dělá.
 */

import { DAILY_INK, INK_BY_TIER, inkPrice, rankInk } from './economy'
import { RANKS } from './ranks'
import type { ModeId } from './types'

/**
 * Kam se dá z výkladu odejít.
 *
 * `term:` vede na jiné heslo slovníčku a je to jediný cíl, který hráče
 * nikam neodvede — což je zrovna uprostřed rozehraného kola to jediné, co se
 * dá nabídnout.
 */
export type ExplainTarget =
  | 'awards'
  | 'stats'
  | 'guide'
  | `rules:${ModeId}`
  | `term:${string}`

export interface Term {
  title: string
  body: string[]
  /** Odkazy pod výkladem — odsud se pokračuje dál, ne zpátky do prázdna. */
  links?: { label: string; to: ExplainTarget }[]
}

/** Cena nápovědy v inkoustu podle bodové ceny — ať se čísla ve výkladu nehádají. */
const SMALL = inkPrice(20)
const MEDIUM = inkPrice(35)
const WHOLE = inkPrice(66)

export const TERMS: Record<string, Term> = {
  vehlas: {
    title: 'Věhlas',
    body: [
      'Věhlas je součet **všech bodů**, které jsi kdy ve Slovech získal. Nikdy neklesá a nedá se utratit — je to čára, kterou máš za sebou.',
      `Podle věhlasu roste hodnost. Prvních pár stupňů padne hned první večer, pak se rozestupy natahují; na padesátou a poslední hodnost je potřeba přes ${(RANKS[RANKS.length - 1]!.at / 1_000_000).toLocaleString('cs-CZ')} milionu věhlasu.`,
      'Body se počítají v každé hře trochu jinak, ale do věhlasu jdou všechny stejně — je jedno, kterou z šestice hraješ.',
    ],
    links: [
      { label: 'Hodnosti a ocenění', to: 'awards' },
      { label: 'Jak se hrají Slova', to: 'guide' },
    ],
  },

  hodnost: {
    title: 'Hodnost',
    body: [
      `Padesát stupňů od Nováčka po Vládce slov. Postupuje se za věhlas, tedy za nasbírané body — a jen za ně, na ničem jiném hodnost nezávisí.`,
      `Odznak se mění po pěti hodnostech: jiný kov, jiný tvar štítu. Uvnitř pětice se stupně poznají podle počtu krokví pod znakem.`,
      `Za každou novou hodnost padne inkoust — u prvních ${rankInk(2)}, u nejvyšších ${rankInk(50)}.`,
    ],
    links: [{ label: 'Celý žebříček hodností', to: 'awards' }],
  },

  inkoust: {
    title: 'Inkoust',
    body: [
      'Inkoust je jediná měna ve hře a kupují se za něj **nápovědy**. Utrácí se místo bodů: když nápovědu zaplatíš inkoustem, skóre ti zůstane celé.',
      `Cena odpovídá tomu, jak velkou pomoc dostaneš. Malý postrk stojí kolem ${SMALL}, prozrazené písmeno ${MEDIUM}, odhalení celého slova ${WHOLE}.`,
      `Inkoust se nedá koupit za peníze ani vysedět — sype ho jen nová hodnost, každé získané ocenění (${INK_BY_TIER[1]}–${INK_BY_TIER[5]} podle stupně) a ${DAILY_INK} za kompletní denní várku ve všech šesti hrách.`,
      'Nápověda placená inkoustem je pořád nápověda: kolo s ní se nepočítá jako čisté, takže mety „bez nápovědy" se za inkoust koupit nedají.',
    ],
    links: [
      { label: 'Za co inkoust padá', to: 'awards' },
      { label: 'Jak se hrají Slova', to: 'guide' },
    ],
  },

  napoveda: {
    title: 'Nápovědy',
    body: [
      'Každá hra má vlastní nápovědy — Řetěz poradí směr, Šibenice odhalí písmeno, Věž doplní celé patro.',
      'Nápověda se dá zaplatit dvěma způsoby: **body** z právě rozehraného kola, nebo **inkoustem** z kalamáře. Inkoust je dražší na sehnání, ale skóre nechá být.',
      'Kolo, ve kterém padla jediná nápověda, není čisté. Přeruší sérii a nepočítá se do mistrovství hry — a to platí, i když se za ni platilo inkoustem.',
    ],
    links: [
      { label: 'Co je inkoust', to: 'term:inkoust' },
      { label: 'Jak se počítají body', to: 'term:body' },
    ],
  },

  serie: {
    title: 'Série',
    body: [
      'Série je řada **čistých kol** za sebou: dohraných do konce a bez jediné nápovědy.',
      'Nepočítá se každé odehrané kolo. Prohraná šibenice, vzdaná věž ani kolo s jednou nápovědou sérii utnou zpátky na nulu — jinak by číslo nic neznamenalo.',
      'Sérií se násobí skóre, takže čím delší, tím víc každé další kolo vynese.',
    ],
    links: [{ label: 'Mety za dlouhé série', to: 'awards' }],
  },

  dny: {
    title: 'Dny v řadě',
    body: [
      'Kolik dní po sobě sis Slova aspoň jednou otevřel. Je to něco jiného než série kol — tahle řada se nepřeruší tím, že se kolo nepovedlo.',
      'Den se počítá jednou, ať odehraješ jedno kolo nebo dvacet. Vynechaný den řadu utne a začíná se od jedničky.',
      'Jsou to jediné mety, které se nedají dohnat jedním večerem.',
    ],
    links: [{ label: 'Mety za návyk', to: 'awards' }],
  },

  oceneni: {
    title: 'Ocenění',
    body: [
      'Trvalé mety, které se udělují jednou a už nezmizí. Většina jich stojí v **žebříčcích** po pěti stupních — od Učně po Legendu.',
      'Ve vitríně vidíš získané stupně a vždycky jeden další, na který se zrovna hraje. Zbytek žebříčku se ukáže, až na něj dojde řada.',
      'Za každé ocenění padne inkoust; čím vyšší stupeň, tím víc.',
    ],
    links: [{ label: 'Otevřít vitrínu', to: 'awards' }],
  },

  denni: {
    title: 'Denní výzva',
    body: [
      'Šest hádanek na den, pro každou hru jedna. Všichni hráči dostanou tentýž den stejné zadání — je odvozené z data, ne z náhody.',
      `Za dohrání celé šestice padne ${DAILY_INK} inkoustu. Za jednotlivé výzvy ne, jinak by denní várka zaplavila kalamář víc než všechno ostatní dohromady.`,
      'Denní výzva se dá zahrát jen jednou. Body z ní se počítají normálně.',
    ],
  },

  body: {
    title: 'Body',
    body: [
      'Body se sbírají za dohrané kolo a jejich součet za celou dobu je věhlas.',
      'Základ dává splněný cíl hry, k němu se přičítá rychlost, čistota a zvláštní kousky — pangram ve Voštině, nejkratší cesta v Řetězu, řetěz slov ve Slabikách.',
      'Nápověda zaplacená body se odečte hned. Nevyužité nápovědy naopak na konci kola něco přinesou.',
      'Dobré kolo dá kolem čtyř set bodů. Když je štědré všechno, není štědré nic — proto čísla nejsou nafouklá.',
    ],
    links: [{ label: 'Jak se hrají Slova', to: 'guide' }],
  },

  zaklad: {
    title: 'Základní tvar',
    body: [
      'Slova pracují **jen se základními tvary** — tak, jak slovo najdeš ve slovníku. Díky tomu nesbíráš pořád dokola pády jednoho slova.',
      '**Platí:** podstatná jména v 1. pádu, jednotné i množné číslo (pes, psi, kočka, kočky), slovesa v infinitivu (psát, běhat), přídavná jména (velký), číslovky (pět), zájmena (ten), příslovce (dnes) a spojky (ale).',
      '**Neplatí:** ostatní pády (psa, psovi, psy), časované tvary (píšu, psal), rozkazy (piš) ani stupňování (rychlejší).',
      'Když ti hra slovo neuzná, bývá to skoro vždycky tímhle.',
    ],
    links: [{ label: 'Jak se hrají Slova', to: 'guide' }],
  },

  obtiznost: {
    title: 'Obtížnost',
    body: [
      'Každá hra si drží vlastní obtížnost a pamatuje si ji do příště. Mění delší slova, větší plochu a přísnější limity.',
      'Body ani ocenění na obtížnosti nezávisí — těžší hádanky ale samy o sobě vynesou víc, protože je v nich za co brát.',
    ],
  },

  odehrano: {
    title: 'Odehráno',
    body: [
      'Kolik kol máš dohraných dohromady, napříč všemi šesti hrami. Počítá se každé kolo, i to nepovedené.',
      'Na samotném počtu odehraných kol stojí jen pár met ve Vytrvalosti. Ostatní žebříčky se dívají na kola dohraná bez nápovědy — vydržet klikat umí každý.',
    ],
    links: [{ label: 'Podrobné statistiky', to: 'stats' }],
  },

  tema: {
    title: 'Vzhled',
    body: [
      'Přepíná mezi světlým a tmavým vzhledem. Třetí poloha „podle systému" se řídí nastavením telefonu, včetně nočního přepínání.',
    ],
  },

  plastev: {
    title: 'Hodnost v plástvi',
    body: [
      'Voština má vlastní žebříček uvnitř kola — od Začátečníka po Královnu. Řídí se podílem bodů, které jsi z plástve vybral, ne počtem slov.',
      'Na Královnu stačí sedmdesát procent bodů plástve. Posledních pár slov bývá těžších než celý zbytek dohromady.',
    ],
    links: [{ label: 'Pravidla Voštiny', to: 'rules:hive' }],
  },

  pangram: {
    title: 'Pangram',
    body: [
      'Slovo, ve kterém se objeví **všech sedm** písmen plástve. Bývá jich v kole jeden až tři a každý vynese násobek běžného slova.',
      'Hledá se od nejdelších slov — pangram je skoro vždycky delší než sedm písmen, protože se v něm písmena opakují.',
    ],
    links: [{ label: 'Pravidla Voštiny', to: 'rules:hive' }],
  },
}

export function term(id: string): Term | undefined {
  return TERMS[id]
}
