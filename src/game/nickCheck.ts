/**
 * Kontrola přezdívek.
 *
 * Přezdívku vidí soupeři — je to jediné místo ve hře, kde jeden hráč píše
 * druhému. Obchody s aplikacemi na takový obsah mají vlastní pravidla
 * a vyžadují, aby se závadné jméno dalo zachytit dřív, než ho někdo uvidí.
 *
 * Filtr je schválně **hloupý a přísný jen na jádro věci**. Nesnaží se
 * postihnout všechno, co kdo vymyslí — to nejde a pokusy o to končí u toho,
 * že hra nepustí Kokořín ani Sprostějov. Chytá dvě věci:
 *
 *   1. Jasné vulgarismy a nadávky v základním tvaru i s obvyklými obměnami
 *      (číslice místo písmen, zdvojená písmena, diakritika).
 *   2. Jména, která by se vydávala za hru samotnou nebo za obsluhu —
 *      „admin", „moderator", „slova" —, protože tím by šlo ostatní podvést.
 *
 * Zbytek řeší nahlášení a blokování, které má hráč po ruce u každého souboje.
 * Filtr je první síto, ne poslední slovo.
 */

/** Sjednotí zápis: bez diakritiky, malá písmena, číslice zpět na písmena. */
export function foldNick(nick: string): string {
  return nick
    .normalize('NFD')
    .replace(/\p{M}/gu, '')
    .toLowerCase()
    .replace(/[0@]/g, 'o')
    .replace(/1|\|/g, 'i')
    .replace(/3/g, 'e')
    .replace(/4/g, 'a')
    .replace(/5|\$/g, 's')
    .replace(/7/g, 't')
    .replace(/[^a-z]/g, '')
    // Zdvojená písmena se srazí: „kkuurrvvaa" je pořád totéž slovo.
    .replace(/(.)\1+/g, '$1')
}

/**
 * Jádra závadných slov.
 *
 * Hledají se jako podřetězce ve složeném tvaru, takže pokrývají i skloňování
 * a spřežky. Krátká jádra by chytala nevinná slova, proto tu žádné kratší
 * než čtyři písmena není.
 */
const FOUL = [
  // vulgarismy
  'kurva',
  'kurwa',
  'piqa',
  'pica',
  'picus',
  'kokot',
  'kokso',
  'mrdat',
  'mrdka',
  'mrdac',
  'prcat',
  'sracka',
  'srac',
  'hovno',
  'hovna',
  'debil',
  'idiot',
  'kretn',
  'kreten',
  'zmrd',
  'curak',
  'penis',
  'vagina',
  'prdel',
  'sperm',
  'kunda',
  'kundo',
  'buzerant',
  'buzna',
  'chcanky',
  'zkurv',
  'vyjeb',
  'nasrat',
  'posrat',
  'kokote',
  // anglické, které zná každý
  'fuck',
  'shit',
  'bitch',
  'cunt',
  'dick',
  'wank',
  'nigger',
  'nigga',
  'rape',
  'pedofil',
  'pedophil',
  // nenávist
  'hitler',
  'nacista',
  'nazi',
  'heilhitler',
  'siegheil',
  'genocid',
  // vydávání se za obsluhu nebo za hru
  'admin',
  'moderator',
  'moderace',
  'podpora',
  'support',
  'official',
  'oficialni',
  'slovahra',
]

/**
 * Je přezdívka závadná?
 *
 * Vrací důvod k zobrazení, nebo null. Důvod je schválně jeden pro všechno:
 * vypisovat, které slovo filtr zachytil, by z něj udělalo návod, jak ho obejít.
 */
export function foulNick(nick: string): string | null {
  const folded = foldNick(nick)
  if (folded.length === 0) return 'Přezdívka musí obsahovat písmena.'
  // Samotné „slova" je jméno hry; jako přezdívka by mátlo.
  if (folded === 'slova' || folded === 'sloa') {
    return 'Tuhle přezdívku si hra nechává pro sebe. Zvol jinou.'
  }
  for (const word of FOUL) {
    if (folded.includes(foldNick(word))) {
      return 'Tuhle přezdívku ostatním neukážeme. Zkus jinou.'
    }
  }
  return null
}

/** Důvody, které si hráč vybere při nahlášení. */
export const REPORT_REASONS = [
  'Vulgární nebo urážlivá přezdívka',
  'Vydává se za někoho jiného',
  'Nenávistný obsah',
  'Něco jiného',
] as const

export type ReportReason = (typeof REPORT_REASONS)[number]
