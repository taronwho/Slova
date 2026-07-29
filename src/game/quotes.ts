/**
 * Režim CITÁT — odkrývání výroku po písmenech.
 *
 * Na začátku je vidět zhruba pětina slov; zbytek je prázdný. Hráč zkouší
 * písmena a snaží se text doplnit dřív, než ho chyby přijdou draho.
 *
 * Proti Šibenici a Detektivovi je rozdíl v tom, **co se hádá**: ne jedno
 * slovo, ale souvislá věta, která něco říká. Odkryté „…srdcem" napoví
 * zbytek myšlenky, takže se dá uvažovat o smyslu, ne jen o písmenech.
 *
 * Nápovědy jdou po stupních od nejmlhavější k nejkonkrétnější: podobizna
 * autora, jeho zařazení, jméno, a teprve pak odkrývání slov.
 *
 * Texty jsou z českých Wikicitátů (CC BY-SA), podobizny z Wikimedia
 * Commons — v datech je jen jméno souboru, adresa se skládá tady.
 */

import { fold } from '../lib/czech'
import type { Difficulty } from './types'

export interface Quote {
  id: string
  text: string
  /** Autor výroku. */
  who: string
  /** Zařazení autora — „český spisovatel". */
  note?: string
  /** Jméno souboru s podobiznou na Wikimedia Commons. */
  art?: string
  topic: string
  difficulty: Difficulty
}

export const QUOTE_TOPICS: { id: string; label: string }[] = [
  { id: 'vse', label: 'Vše' },
  { id: 'spisovatele', label: 'Spisovatelé' },
  { id: 'mysleni', label: 'Myslitelé a vědci' },
  { id: 'politici', label: 'Politici' },
  { id: 'herci', label: 'Herci a hudebníci' },
  { id: 'osobnosti', label: 'Ostatní' },
]

/** Stálá adresa obrázku na Commons. Nic se nestahuje, jen se skládá. */
export function artUrl(file: string, width = 320): string {
  return `https://commons.wikimedia.org/wiki/Special:FilePath/${encodeURIComponent(
    file,
  )}?width=${width}`
}

export const QUOTE_KEYS = 'abcdefghijklmnopqrstuvwxyz'.split('')

/** Stupně nápovědy. Pořadí je pevné — od nejmlhavější k nejkonkrétnější. */
export type QuoteHint = 'art' | 'note' | 'who' | 'word'

export const QUOTE_COST = {
  /** Chybné písmeno. Dvojnásobek trefy — hádat naslepo se nemá vyplácet. */
  miss: 30,
  /**
   * I trefené písmeno něco stojí.
   *
   * Bez toho by se vyplatilo vyklikat abecedu a výrok si přečíst. Takhle
   * má hráč důvod tipnout celou větu, jakmile mu dojde smysl — a to je to,
   * co má tenhle režim odměňovat.
   */
  hit: 15,
  art: 25,
  note: 35,
  who: 60,
  word: 45,
} as const

/** Nad tolik chyb se kolo ukončí, ať se text nevyklikká abecedou. */
export const QUOTE_MISS_LIMIT = 14

export interface QuoteState {
  quote: Quote
  /** Základní písmena, která hráč odkryl. */
  tried: string[]
  /** Slova odkrytá zadarmo na začátku a nápovědou — indexy do words(). */
  given: number[]
  hints: QuoteHint[]
  /** Chybné tipy na celý výrok — ukazují se, ať je hráč neopakuje. */
  guesses: string[]
  /** Uhodl hráč celý výrok najednou? */
  solved: boolean
  freeHints: number
  hintCost: number
  startedAt: number
  finishedAt: number | null
}

/** Rozpad textu na slova a mezislovní znaky. */
export interface Token {
  text: string
  /** Slovo se hádá; interpunkce a mezery jsou vidět pořád. */
  word: boolean
}

export function tokens(text: string): Token[] {
  return text
    .split(/(\p{L}[\p{L}\p{M}]*)/u)
    .filter((piece) => piece !== '')
    .map((piece) => ({ text: piece, word: /^\p{L}/u.test(piece) }))
}

/** Kolik slov dostane hráč zadarmo — zhruba pětina, nejmíň jedno. */
function freeCount(words: number): number {
  return Math.max(1, Math.round(words * 0.22))
}

/**
 * Která slova jsou vidět od začátku.
 *
 * Vybírají se ta kratší a rozeseto po celé větě — odkrytá spojka na kraji
 * nepomůže, ale „a", „se", „že" mezi neznámými slovy drží větu pohromadě,
 * aby z ní šlo něco vyčíst.
 */
export function openingWords(text: string, seed: number): number[] {
  const all = tokens(text)
    .map((token, index) => ({ token, index }))
    .filter((item) => item.token.word)
  const want = freeCount(all.length)
  const order = all
    .map((item, place) => ({ ...item, place }))
    .sort(
      (a, b) =>
        a.token.text.length - b.token.text.length ||
        ((a.place * 7919 + seed) % 101) - ((b.place * 7919 + seed) % 101),
    )
  return order.slice(0, want).map((item) => item.index)
}

export function createQuoteState(quote: Quote, seed: number, now = Date.now()): QuoteState {
  return {
    quote,
    tried: [],
    given: openingWords(quote.text, seed),
    hints: [],
    guesses: [],
    solved: false,
    freeHints: 0,
    hintCost: 0,
    startedAt: now,
    finishedAt: null,
  }
}

/** Základní podoba písmene — háčky a čárky se nehádají. */
const base = (letter: string): string => fold(letter.toLowerCase())

/** Je tohle písmeno odkryté? */
export function isOpen(state: QuoteState, index: number, letter: string): boolean {
  return state.given.includes(index) || state.tried.includes(base(letter))
}

/** Zbývá ještě něco zakrytého? */
export function isSolved(state: QuoteState): boolean {
  if (state.solved) return true
  return tokens(state.quote.text).every(
    (token, index) =>
      !token.word ||
      state.given.includes(index) ||
      [...token.text].every((letter) => state.tried.includes(base(letter))),
  )
}

/** Kolik písmen ve skrytých slovech odpovídá zkoušenému písmenu. */
export function countLetter(state: QuoteState, letter: string): number {
  let found = 0
  tokens(state.quote.text).forEach((token, index) => {
    if (!token.word || state.given.includes(index)) return
    for (const one of token.text) if (base(one) === base(letter)) found += 1
  })
  return found
}

export const missCount = (state: QuoteState): number =>
  state.tried.filter((letter) => countLetter({ ...state, tried: [] }, letter) === 0).length

/** Kolik zkoušených písmen ve výroku doopravdy bylo. */
export const hitCount = (state: QuoteState): number =>
  state.tried.length - missCount(state)

/** Porovnání tipu s výrokem — bez ohledu na diakritiku a interpunkci. */
const plain = (text: string): string =>
  fold(text.toLowerCase()).replace(/[^a-z0-9]+/g, ' ').trim()

export function guessQuote(state: QuoteState, guess: string): QuoteState {
  if (state.finishedAt) return state
  if (plain(guess) === plain(state.quote.text)) {
    return { ...state, solved: true, finishedAt: Date.now() }
  }
  return { ...state, guesses: [...state.guesses, guess.trim()] }
}

export function tryLetter(state: QuoteState, letter: string): QuoteState {
  const key = base(letter)
  if (state.finishedAt || state.tried.includes(key)) return state
  const next = { ...state, tried: [...state.tried, key] }
  return isSolved(next) || missCount(next) >= QUOTE_MISS_LIMIT
    ? { ...next, finishedAt: Date.now() }
    : next
}

/** Nápověda „slovo" odkryje nejdelší dosud skryté slovo — má největší váhu. */
export function revealWord(state: QuoteState): QuoteState {
  const hidden = tokens(state.quote.text)
    .map((token, index) => ({ token, index }))
    .filter(
      (item) =>
        item.token.word &&
        !state.given.includes(item.index) &&
        ![...item.token.text].every((letter) => state.tried.includes(base(letter))),
    )
    .sort((a, b) => b.token.text.length - a.token.text.length)
  if (hidden.length === 0) return state
  const next = { ...state, given: [...state.given, hidden[0]!.index] }
  return isSolved(next) ? { ...next, finishedAt: Date.now() } : next
}

/** Které nápovědy má kolo v zásobě — obrázek jen když je co ukázat. */
export function hintLadder(quote: Quote): QuoteHint[] {
  const out: QuoteHint[] = []
  if (quote.art) out.push('art')
  if (quote.note) out.push('note')
  out.push('who')
  return out
}
