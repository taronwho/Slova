/** Sdílené typy napříč všemi třemi režimy. */

export type ModeId = 'chain' | 'hive' | 'tower'

export type Difficulty = 'easy' | 'normal' | 'hard'

export const DIFFICULTY_LABEL: Record<Difficulty, string> = {
  easy: 'Snadná',
  normal: 'Střední',
  hard: 'Těžká',
}

export const MODE_LABEL: Record<ModeId, string> = {
  chain: 'Řetěz',
  hive: 'Voština',
  tower: 'Věž',
}

export const MODE_TAGLINE: Record<ModeId, string> = {
  chain: 'Měň jedno písmeno a dojdi k cíli',
  hive: 'Skládej slova ze sedmi písmen',
  tower: 'Stav věž z přesmyček',
}

/** Výsledek dokončeného kola — vstup do bodování i statistik. */
export interface RoundResult {
  mode: ModeId
  difficulty: Difficulty
  puzzleId: string
  score: number
  perfect: boolean
  elapsedMs: number
  hintsUsed: number
  /** Režimově specifický detail pro sdílení a historii. */
  detail: Record<string, number | string>
}
