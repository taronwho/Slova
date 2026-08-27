/**
 * Podrobnosti odehraného souboje — co kdo odevzdal a za jak dlouho.
 *
 * Výsledek souboje je jedno číslo proti druhému a to je málo: prohrát
 * o dvacet bodů kvůli jednomu zaváhání vypadá stejně jako prohrát na celé
 * čáře. Aby šlo po souboji říct **kde** se to rozhodlo, posílá si každý
 * hráč vedle skóre i krátký rozpis svých kol.
 *
 * Píše se do jednoho řetězce, ne do stromu. Důvod je praktický: pravidla
 * databáze u výsledku zápasu pouštějí dál jen to, co je v nich vyjmenované,
 * a jedna textová hodnota se dá povolit jedním řádkem. Formát je proto co
 * nejhloupější — položky za sebou oddělené `|`, uvnitř pole oddělená `~`.
 * Ani jeden ze znaků se v českém slově nevyskytuje, takže se nemusí nic
 * ošetřovat; pro jistotu se z textu při zápisu stejně vyhazují.
 *
 * Rozpis je **navíc, ne nutnost**. Kdo hraje se starším telefonem nebo mu
 * zápis neprojde, má pořád skóre — porovnání pak jen ukáže méně.
 */

/** Jeden krok souboje: kolo Vetřelce nebo ukořistěné slovo z plástve. */
export interface DuelStep {
  /** Co hráč odevzdal — vybrané slovo u Vetřelce, ukořistěné u Voštiny. */
  word: string
  /** Jak dlouho mu to trvalo (ms). U Voštiny 0, tam se po slovech neměří. */
  ms: number
  points: number
  /**
   * Správná odpověď (jen Vetřelec).
   *
   * Bez ní by u kola, kde se netrefil ani jeden, nebylo poznat, co tam
   * vlastně mělo být — a přesně na takové kolo se oba budou ptát.
   */
  odd?: string
}

/**
 * Kolik znaků rozpis unese.
 *
 * Sedí na pravidlo v databázi. Tři kola Vetřelce se vejdou do stovky,
 * plástev s pětadvaceti slovy do půl tisíce; zbytek je rezerva, aby se
 * kvůli jednomu dlouhému slovu nezahodil celý zápis.
 */
export const DETAIL_MAX = 900

const CISTIT = /[|~\n\r]/g

/**
 * Složí rozpis do řetězce.
 *
 * Když se položky nevejdou, useknou se ty poslední — v obou hrách jsou
 * první kroky ty, o kterých se pak mluví, a useknutý rozpis je pořád lepší
 * než žádný.
 */
export function encodeSteps(steps: DuelStep[]): string {
  const kusy: string[] = []
  let delka = 0
  for (const step of steps) {
    const kus = [
      step.word.replace(CISTIT, ''),
      Math.max(0, Math.round(step.ms)),
      Math.max(0, Math.round(step.points)),
      (step.odd ?? '').replace(CISTIT, ''),
    ]
      .join('~')
      // Prázdná pole na konci nemají co zabírat místo.
      .replace(/~+$/, '')
    if (delka + kus.length + 1 > DETAIL_MAX) break
    kusy.push(kus)
    delka += kus.length + 1
  }
  return kusy.join('|')
}

/** Rozebere rozpis zpátky. Co nedává smysl, se tiše přeskočí. */
export function decodeSteps(text: string | undefined | null): DuelStep[] {
  if (!text) return []
  const out: DuelStep[] = []
  for (const kus of text.split('|')) {
    if (!kus) continue
    const [word = '', ms = '', points = '', odd = ''] = kus.split('~')
    const body = Number(points)
    if (!Number.isFinite(body)) continue
    const step: DuelStep = {
      word,
      ms: Number.isFinite(Number(ms)) ? Number(ms) : 0,
      points: body,
    }
    if (odd) step.odd = odd
    out.push(step)
  }
  return out
}

/** Čas kroku k přečtení: „4,2 s". U Voštiny se čas neukazuje vůbec. */
export function stepTime(ms: number): string {
  if (ms <= 0) return '—'
  if (ms < 10_000) return `${(ms / 1000).toLocaleString('cs-CZ', { maximumFractionDigits: 1 })} s`
  return `${Math.round(ms / 1000)} s`
}
