/** Česká abeceda a normalizace textu. */

/** Všechna písmena, která hra uznává (bez digrafu ch — ten se počítá jako c+h). */
export const CZECH_LETTERS =
  'aábcčdďeéěfghiíjklmnňoópqrřsštťuúůvwxyýzž'.split('')

const FOLD_MAP: Record<string, string> = {
  á: 'a', č: 'c', ď: 'd', é: 'e', ě: 'e', í: 'i', ň: 'n', ó: 'o',
  ř: 'r', š: 's', ť: 't', ú: 'u', ů: 'u', ý: 'y', ž: 'z',
}

/** Odstraní diakritiku: „přílež" -> „prilez". Používá Voština. */
export function fold(word: string): string {
  let out = ''
  for (const ch of word) out += FOLD_MAP[ch] ?? ch
  return out
}

/** Bitová maska různých písmen složeného tvaru (a=bit 0 … z=bit 25). */
export function letterMask(word: string): number {
  let mask = 0
  for (const ch of fold(word)) {
    const bit = ch.charCodeAt(0) - 97
    if (bit >= 0 && bit < 26) mask |= 1 << bit
  }
  return mask
}

/** Setřídí písmena slova — podpis pro hledání přesmyček. */
export function signature(word: string): string {
  return [...word].sort().join('')
}

/**
 * Číslo se správným tvarem podstatného jména: 1 kolo, 2 kola, 5 kol.
 *
 * Čeština má tři tvary a hra je používá na deseti místech; bez tohohle se
 * v každém komponentu psal vlastní opis a někde se na jeden z tvarů zapomnělo.
 */
export function plural(count: number, one: string, few: string, many: string): string {
  const form = count === 1 ? one : count >= 2 && count <= 4 ? few : many
  return `${count} ${form}`
}

/** Očistí vstup hráče: malá písmena, bez mezer a interpunkce. */
export function normalizeInput(raw: string): string {
  return raw
    .toLowerCase()
    .replace(/\s+/g, '')
    .split('')
    .filter((ch) => CZECH_LETTERS.includes(ch))
    .join('')
}

/**
 * Rozložení virtuální klávesnice — české QWERTZ s řádkem diakritiky navrch.
 * Nejvýš 11 kláves na řádek, aby se rozložení vešlo i na úzký telefon;
 * ⌫ a potvrzení mají vlastní řádek.
 */
export const KEYBOARD_ROWS: string[][] = [
  'ěščřžýáíéó'.split(''),
  'qwertzuiop'.split('').concat(['ú']),
  'asdfghjkl'.split('').concat(['ů', 'ď']),
  'yxcvbnm'.split('').concat(['ť', 'ň']),
]
