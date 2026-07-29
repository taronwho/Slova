/** Sdílené typy napříč všemi třemi režimy. */

export type ModeId = 'chain' | 'hive' | 'tower' | 'gallows' | 'detective' | 'tetris'

export type Difficulty = 'easy' | 'normal' | 'hard'

export const DIFFICULTY_LABEL: Record<Difficulty, string> = {
  easy: 'Snadná',
  normal: 'Střední',
  hard: 'Těžká',
}

/** Pořadí režimů všude, kde se vypisují — v menu i v nabídce denních výzev. */
export const MODE_ORDER: ModeId[] = [
  'chain',
  'hive',
  'tower',
  'gallows',
  'detective',
  'tetris',
]

/** Znak režimu na dlaždici. Kresba by se do řádku textu nevešla. */
export const MODE_GLYPH: Record<ModeId, string> = {
  chain: '→',
  hive: '⬡',
  tower: '↑',
  gallows: '?',
  detective: '§',
  tetris: '▚',
}

export const MODE_LABEL: Record<ModeId, string> = {
  chain: 'Řetěz',
  hive: 'Voština',
  tower: 'Věž',
  gallows: 'Šibenice',
  detective: 'Detektiv',
  tetris: 'Slabiky',
}

/**
 * Nadpis návodu ke hře.
 *
 * Není to jen `Jak se hraje ${název}`: Slabiky jsou množné číslo, takže se
 * *hrají*. Jedno slovo, ale v nadpisu, na který se hráč dívá pokaždé, když
 * hledá pravidla — a špatná shoda tam bije do očí.
 */
export function howToPlay(mode: ModeId): string {
  return mode === 'tetris'
    ? 'Jak se hrají Slabiky'
    : `Jak se hraje ${MODE_LABEL[mode]}`
}

export const MODE_TAGLINE: Record<ModeId, string> = {
  chain: 'Měň jedno písmeno a dojdi k cíli',
  hive: 'Skládej slova ze sedmi písmen',
  tower: 'Stav věž z přesmyček',
  gallows: 'Uhodni slovo po písmenech',
  detective: 'Poznej slovo podle indicií',
  tetris: 'Skládej padající slabiky ve slova',
}

/** Výsledek dokončeného kola — vstup do bodování i statistik. */
export interface RoundResult {
  mode: ModeId
  difficulty: Difficulty
  puzzleId: string
  score: number
  perfect: boolean
  /**
   * Splnil hráč to, o co v režimu jde? Dojít do cíle, vysbírat plástev,
   * dostavět věž, uhodnout slovo.
   *
   * Není to totéž co „kolo skončilo". Šibenici lze dohrát tak, že hráč
   * visí, a plástev lze ukončit po třech slovech — obojí je regulérní konec
   * kola, ale ani jedno není výkon, za který se má počítat čisté kolo.
   */
  success: boolean
  elapsedMs: number
  hintsUsed: number
  /** Režimově specifický detail pro sdílení a historii. */
  detail: Record<string, number | string>
}
