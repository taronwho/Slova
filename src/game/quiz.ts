/**
 * Otázka dne — jediná hra, která se hraje jednou za den.
 *
 * Ostatních šest her je o češtině. Tahle je o všem ostatním: hráč dostane
 * holý nadpis („Poznej známou osobnost", „Hlavní město kterého státu") a
 * **předem se rozhodne, kolik indicií si vezme**. Za jednu indicii je odměna
 * trojnásobná oproti třem, takže sázka na vlastní hlavu se vyplácí — a hráč
 * se rozhoduje dřív, než uvidí, jak je otázka těžká. To je celé kouzlo.
 *
 * Indicie jdou **od nejtěžší po nejnávodnější**. První je pro člověka, který
 * se v oboru pohybuje, a většině lidí neřekne skoro nic; třetí odpověď skoro
 * prozradí. Kdo si vezme jen jednu, dostane právě tu první.
 *
 * Odměnou jsou **kapky inkoustu, ne body**. Otázka dne nemá se slovní zásobou
 * nic společného, takže by neměla hýbat věhlasem ani hodností — ta se pořád
 * získává hraním her o slovech. Zato dává nejštědřejší příjem inkoustu ve hře,
 * a proto je jednou denně: víc se jich odehrát nedá, ať hráč sedí u telefonu
 * jak chce dlouho.
 */

import { fold } from '../lib/czech'
import { hashSeed, mulberry32 } from '../lib/rng'

/**
 * Obory otázek.
 *
 * Střídají se **kolečkem, ne náhodou** — hráč jinak dostane tři sporty za
 * týden a stěžuje si právem. Pořadí v tomhle poli je pořadí dnů: první den
 * osobnost, druhý zeměpis, třetí věda… Jakmile se pole vyčerpá, začíná se
 * znovu od začátku, ale s další otázkou z každého oboru.
 */
export const QUIZ_TOPICS = [
  'osobnost',
  'zemepis',
  'veda',
  'kultura',
  'historie',
  'priroda',
  'technika',
  'sport',
  'jazyk',
  'spolecnost',
] as const

export type QuizTopic = (typeof QUIZ_TOPICS)[number]

export const TOPIC_LABEL: Record<QuizTopic, string> = {
  osobnost: 'Osobnosti',
  zemepis: 'Zeměpis',
  veda: 'Věda',
  kultura: 'Kultura',
  historie: 'Historie',
  priroda: 'Příroda',
  technika: 'Technika',
  sport: 'Sport',
  jazyk: 'Jazyk',
  spolecnost: 'Společnost',
}

export interface QuizQuestion {
  id: string
  topic: QuizTopic
  /** Nadpis. Jediné, co hráč vidí, než se rozhodne o počtu indicií. */
  ask: string
  /** Tři indicie od nejtěžší po nejnávodnější. */
  clues: [string, string, string]
  answer: string
  /**
   * Další tvary, které se uznají. Diakritiku ani velikost písmen sem psát
   * netřeba, o ty se stará `matches`.
   */
  alt?: string[]
}

/** Celý balík otázek, rozdělený po oborech. */
export type QuizDeck = Record<QuizTopic, QuizQuestion[]>

/** Kolik pokusů má hráč na jednu otázku. */
export const QUIZ_TRIES = 3

/**
 * Kolik inkoustu padne za uhodnutou otázku podle počtu vzatých indicií.
 *
 * Index je počet indicií. Jedna indicie je trojnásobek tří — kdo si troufne,
 * má za to dostat pořádně zaplaceno, jinak si každý vezme všechny tři.
 */
export const QUIZ_REWARD = [0, 30, 20, 10] as const

/**
 * Kterou otázku dostane den `day`.
 *
 * Obor se bere kolečkem podle pořadí dne, takže v každých deseti dnech padne
 * z každého oboru právě jedna otázka — dva sporty za týden nejdou vyrobit ani
 * náhodou, protože v tom není žádná náhoda.
 *
 * Uvnitř oboru se jde po pořadí, ale **zamíchaném** — sousední dny by jinak
 * dostávaly otázky, které spolu v datech sousedí (stejné písmeno, stejná
 * kategorie na Wikipedii). Míchání je odvozené z názvu oboru, takže je pro
 * všechny hráče i všechny buildy stejné.
 *
 * První opakování přijde až po `QUIZ_TOPICS.length × (nejmenší obor)` dnech.
 * Kolik to je konkrétně, spočítá `quizCycle`.
 */
export function quizFor(deck: QuizDeck, day: number): QuizQuestion | null {
  const topic = QUIZ_TOPICS[mod(day, QUIZ_TOPICS.length)]!
  const pool = deck[topic]
  if (!pool || pool.length === 0) return null
  const round = Math.floor(day / QUIZ_TOPICS.length)
  return shuffledPool(topic, pool)[mod(round, pool.length)]!
}

/** Za kolik dní se otázka zopakuje. Hlídá to test, ať se to nezmenší. */
export function quizCycle(deck: QuizDeck): number {
  const sizes = QUIZ_TOPICS.map((topic) => deck[topic]?.length ?? 0)
  return Math.min(...sizes) * QUIZ_TOPICS.length
}

/** Zbytek po dělení, který nikdy nevrátí zápor — den může být i před epochou. */
function mod(value: number, by: number): number {
  return ((value % by) + by) % by
}

const shuffles = new Map<string, QuizQuestion[]>()

function shuffledPool(topic: QuizTopic, pool: QuizQuestion[]): QuizQuestion[] {
  const key = `${topic}:${pool.length}`
  const hit = shuffles.get(key)
  if (hit) return hit
  const random = mulberry32(hashSeed(topic))
  const out = [...pool]
  for (let i = out.length - 1; i > 0; i -= 1) {
    const j = Math.floor(random() * (i + 1))
    ;[out[i], out[j]] = [out[j]!, out[i]!]
  }
  shuffles.set(key, out)
  return out
}

export interface QuizState {
  question: QuizQuestion
  /** Kolik indicií si hráč koupil (1–3). Null, dokud se nerozhodl. */
  bought: number | null
  /** Kolik jich má odkrytých. Nikdy víc než `bought`. */
  shown: number
  /** Odpovědi, které hráč zkusil — ukazují se, ať netipuje totéž dvakrát. */
  tried: string[]
  solved: boolean
  startedAt: number
  finishedAt: number | null
}

export function createQuizState(question: QuizQuestion, now = Date.now()): QuizState {
  return {
    question,
    bought: null,
    shown: 0,
    tried: [],
    solved: false,
    startedAt: now,
    finishedAt: null,
  }
}

/** Hráč se rozhodl, kolik indicií chce. První se odkryje rovnou. */
export function buyClues(state: QuizState, count: number): QuizState {
  if (state.bought !== null) return state
  const bought = Math.max(1, Math.min(3, Math.round(count)))
  return { ...state, bought, shown: 1 }
}

/** Odkryje další koupenou indicii. */
export function revealClue(state: QuizState): QuizState {
  if (state.bought === null || state.shown >= state.bought) return state
  return { ...state, shown: state.shown + 1 }
}

export function triesLeft(state: QuizState): number {
  return Math.max(0, QUIZ_TRIES - state.tried.length)
}

export function isOver(state: QuizState): boolean {
  return state.finishedAt !== null
}

/**
 * Sedí odpověď?
 *
 * Porovnává se bez diakritiky, bez velikosti písmen a bez toho, co odpověď
 * jen doprovází — mezery, spojovníky, tečky, uvozovky. „Édith Piaf",
 * „edith piaf" i „Edith-Piaf" jsou tatáž odpověď a odmítnout to poslední by
 * bylo jen chytání za slovo.
 *
 * **A hlavně se odpouští tvar.** Hráč zná odpověď a píše ji, jak mu přijde
 * pod ruku: na „Podávání ruky" napsal „podání ruky" a hra ho odmítla. To je
 * ta nejhorší možná prohra — vědět a nedostat. Proto se porovnávají kmeny
 * jednotlivých slov s tolerancí na jedno písmeno, ne celý řetězec:
 * „podání ruky", „podávání rukou" i „podávání ruky" projdou.
 *
 * Volnost má hranici u **významu**. „Potřesení ruky" je synonymum, ne jiný
 * tvar, a žádné porovnávání písmen ho neuhodne — takové odpovědi musí být
 * vypsané v `alt` u otázky. Kontrola v `tools/5g_build_quiz.py` hlídá, aby
 * se do indicií neprozradily.
 */
export function matches(question: QuizQuestion, guess: string): boolean {
  const want = [question.answer, ...(question.alt ?? [])]
  if (want.some((text) => key(text) === key(guess))) return true
  const mine = stems(guess)
  return want.some((text) => sameStems(stems(text), mine))
}

function key(text: string): string {
  return fold(text.toLowerCase()).replace(/[^a-z0-9]+/g, '')
}

/**
 * Slova, která odpověď jen lepí dohromady.
 *
 * Kdo napíše „bitva u Hastingsu" místo „bitva u Hastingsu", nemá být
 * odmítnutý kvůli předložce, a kdo ji vynechá, taky ne.
 */
const GLUE = new Set([
  'a', 'i', 'o', 'u', 'v', 'z', 'k', 's', 'na', 'do', 'od', 'po', 'za', 'ze',
  'se', 'si', 'je', 'to', 'ta', 'ten', 'the', 'pri', 'pro', 'nad', 'pod',
])

/**
 * Kmen slova — hrubě, useknutím konce.
 *
 * Čeština ohýbá na konci, takže první písmena nesou význam. Delší slovo si
 * může dovolit delší kmen; u krátkého by useknutí smazalo všechno.
 */
function stem(word: string): string {
  if (word.length <= 4) return word
  if (word.length <= 6) return word.slice(0, 4)
  return word.slice(0, 5)
}

function stems(text: string): string[] {
  return fold(text.toLowerCase())
    .split(/[^a-z0-9]+/)
    .filter((word) => word.length > 0 && !GLUE.has(word))
    .map(stem)
}

/**
 * Liší se dvě slova nejvýš o jedno písmeno? (vložení, smazání, záměna)
 *
 * U krátkých slov se neodpouští nic. Jedno písmeno ze tří je třetina slova
 * a „sůl" by pak brala „sil"; u čtyř a víc už je to bezpečně jen koncovka.
 */
function near(a: string, b: string): boolean {
  if (a === b) return true
  if (a.length < 4 || b.length < 4) return false
  if (Math.abs(a.length - b.length) > 1) return false
  const [short, long] = a.length <= b.length ? [a, b] : [b, a]
  let i = 0
  let j = 0
  let slack = 1
  while (i < short.length && j < long.length) {
    if (short[i] === long[j]) {
      i += 1
      j += 1
      continue
    }
    if (slack === 0) return false
    slack -= 1
    // Při stejné délce se písmeno zamění, jinak se v delším přeskočí.
    if (short.length === long.length) i += 1
    j += 1
  }
  return true
}

/**
 * Odpovídají si dvě sady kmenů?
 *
 * Musí to platit **oběma směry**: samotné „ruky" nesmí projít jako
 * „podávání ruky" a naopak. Jinak by hráč vyhrál každou otázku o dvou
 * slovech tím, že napíše to obecnější z nich.
 */
function sameStems(want: string[], got: string[]): boolean {
  if (want.length === 0 || got.length === 0) return false
  const covers = (from: string[], to: string[]) =>
    from.every((word) => to.some((other) => near(word, other)))
  return covers(want, got) && covers(got, want)
}

export interface QuizOutcome {
  state: QuizState
  correct: boolean
  /** Došly pokusy — správná odpověď se ukáže. */
  lost: boolean
}

export function guess(state: QuizState, text: string, now = Date.now()): QuizOutcome {
  if (isOver(state) || state.bought === null) {
    return { state, correct: false, lost: false }
  }
  const clean = text.trim()
  if (clean === '') return { state, correct: false, lost: false }

  const correct = matches(state.question, clean)
  const tried = [...state.tried, clean]
  const lost = !correct && tried.length >= QUIZ_TRIES
  return {
    state: {
      ...state,
      tried,
      solved: correct,
      finishedAt: correct || lost ? now : null,
    },
    correct,
    lost,
  }
}

/** Vzdání. Správná odpověď se ukáže, odměna žádná. */
export function giveUpQuiz(state: QuizState, now = Date.now()): QuizState {
  if (isOver(state)) return state
  return { ...state, finishedAt: now }
}

/** Kolik inkoustu si hráč odnese. Za neuhodnutou otázku nic. */
export function quizReward(state: QuizState): number {
  if (!state.solved || state.bought === null) return 0
  return QUIZ_REWARD[state.bought] ?? 0
}

/**
 * Povzbuzení, když se otázka nepovede.
 *
 * Patnáct obměn, ať to po čtvrtém neúspěchu nezní jako automat. Vybírá se
 * podle dne, takže se hráči tatáž věta nevrátí dva dny po sobě.
 */
export const QUIZ_CONSOLATIONS = [
  'Nevadí. Zítra je nová otázka a nová šance.',
  'Tuhle si nech projít hlavou. Zítra na tebe čeká další.',
  'Nikdo neví všechno — zkus to zítra znovu.',
  'Dneska to nevyšlo. Zítřejší otázka bude z jiného soudku.',
  'Aspoň víš něco, co jsi ráno nevěděl. Zítra zas.',
  'Škoda. Zítra si to vynahradíš.',
  'Někdy prostě ta správná myšlenka nepřijde. Zítra přijde.',
  'Tahle byla zlá. Zítra na shledanou.',
  'Nic se neděje. Zítra začínáš s čistým štítem.',
  'Zapamatuj si ji — dobré otázky se v hlavě usadí.',
  'Trefa to nebyla, ale zítra máš další pokus.',
  'Občas se nedaří. Zítra to zkusíme spolu znovu.',
  'Konec dobrý, všechno dobré — a konec je až zítra.',
  'Tuhle měl ve sbírce málokdo. Zítra bude líp.',
  'Dneska bez inkoustu. Zítra si ho vybereš zpátky.',
] as const

export function consolationFor(day: number): string {
  return QUIZ_CONSOLATIONS[mod(day, QUIZ_CONSOLATIONS.length)]!
}
