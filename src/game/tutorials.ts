/**
 * Obsah návodů — texty pravidel pro hráče.
 *
 * Drží se odděleně od komponent, aby šel stejný text použít v tutoriálu při
 * prvním spuštění i v přehledu pravidel na domovské obrazovce.
 */

import type { ModeId } from './types'

/** Malá ukázka, která se u kroku vykreslí nad textem. */
export type TutorialVisual =
  | { kind: 'chain-goal' }
  | { kind: 'chain-move' }
  | { kind: 'chain-guard' }
  | { kind: 'chain-score' }
  | { kind: 'hive' }
  | { kind: 'hive-word' }
  | { kind: 'hive-pangram' }
  | { kind: 'hive-ranks' }
  | { kind: 'tower' }
  | { kind: 'tower-letter' }
  | { kind: 'tower-safe' }

export interface TutorialStep {
  title: string
  body: string[]
  visual?: TutorialVisual
  /** Zvýrazněná zásada — to hlavní, co si má hráč z kroku odnést. */
  key?: string
}

export const TUTORIALS: Record<ModeId, TutorialStep[]> = {
  chain: [
    {
      title: 'Dojdi od startu k cíli',
      visual: { kind: 'chain-goal' },
      body: [
        'Nahoře je startovní slovo, dole cílové. Tvým úkolem je dostat se z jednoho na druhé.',
        'Mezi nimi si postavíš řetěz slov — každé se od toho předchozího liší jen o kousek.',
      ],
      key: 'Obě slova jsou vždy stejně dlouhá.',
    },
    {
      title: 'Jeden tah = jedno písmeno',
      visual: { kind: 'chain-move' },
      body: [
        'V každém tahu smíš změnit **právě jedno** písmeno. Písmena se nepřesouvají ani nepřidávají — jen se jedno vymění za jiné.',
        'Výsledek musí být platné české slovo. Tvary jako „hrady" nebo „psala" jsou v pořádku.',
      ],
      key: 'KOSA → KOZA je platný tah. KOSA → KOSY taky. KOSA → KOZY už ne, to jsou změny dvě.',
    },
    {
      title: 'Jak tah zadáš',
      body: [
        '**Na telefonu:** klepni na písmeno, které chceš změnit — barevně se orámuje. Pak ťukni na nové písmeno na klávesnici a dej **Zahrát**.',
        '**Na počítači:** rovnou piš. Šipkami se posuneš mezi písmeny, Enter tah potvrdí.',
        'Písmena s háčky a čárkami vytáhneš **podržením** základního písmene — v rohu klávesy vidíš náhled.',
      ],
      key: 'Špatný tah nic nestojí. Hra ti řekne, co je špatně, a zkusíš to znovu.',
    },
    {
      title: 'Žádné slovo dvakrát',
      body: [
        'Slovo, které už v řetězu je, nesmíš použít znovu. Brání to chození dokola.',
        'Když se potřebuješ vrátit, použij **Vrátit tah** — poslední slovo se odebere a zkusíš to jinak.',
      ],
    },
    {
      title: 'Nejkratší cesta a strážce',
      visual: { kind: 'chain-guard' },
      body: [
        'Hra ti od začátku ukazuje **nejkratší cestu** — na kolik tahů se dá hádanka zvládnout nejlíp. Není to limit, je to meta, kterou se snažíš trefit.',
        'Ukazatel **„zbývá nejméně X tahů"** ti pořád počítá, jak daleko od cíle doopravdy jsi, i s ohledem na slova, která už jsi použil.',
        'Když by ses nějakým tahem odřízl od cíle, hra tě na to okamžitě upozorní a nabídne vrácení.',
      ],
      key: 'Nemůžeš se nenávratně zaseknout. Každá hádanka jde vždycky dohrát.',
    },
    {
      title: 'Body',
      visual: { kind: 'chain-score' },
      body: [
        'Začínáš na 1000 bodech. Za každý tah navíc oproti nejkratší cestě ztratíš 100.',
        'Přidá se bonus za rychlost a za nápovědy, které jsi nepoužil.',
        'Dojít nejkratší cestou a bez nápovědy je **perfektní kolo** — skóre se násobí jedna a půl krát.',
      ],
      key: 'Nápovědy jsou k dispozici vždy, jen stojí body. Dohrát se vyplatí za všech okolností.',
    },
  ],

  hive: [
    {
      title: 'Sedm písmen, spousta slov',
      visual: { kind: 'hive' },
      body: [
        'Dostaneš plástev se sedmi písmeny. Tvým úkolem je poskládat z nich co nejvíc českých slov.',
        'Nemusíš najít všechna — hra tě odměňuje průběžně a každé slovo se počítá.',
      ],
    },
    {
      title: 'Prostřední písmeno je povinné',
      visual: { kind: 'hive-word' },
      body: [
        'Zvýrazněné písmeno uprostřed musí být **v každém** slově, které zadáš. To je hlavní chyták celé hry.',
        'Ostatních šest písmen použiješ, jak se ti hodí — nebo vůbec.',
      ],
      key: 'Písmena se smí opakovat, klidně třikrát ve stejném slově.',
    },
    {
      title: 'Jaká slova platí',
      body: [
        'Slovo musí mít **aspoň 4 písmena**.',
        'Skloňované a časované tvary platí — „kolo", „kola", „kolem" jsou tři různá slova.',
        'Vlastní jména neplatí.',
      ],
      key: 'Háčky a čárky psát nemusíš. Napíšeš „cili" a hra uzná „cíli" — plástev diakritiku doplní sama.',
    },
    {
      title: 'Pangram',
      visual: { kind: 'hive-pangram' },
      body: [
        'V každé plástvi je aspoň jedno slovo, které použije **všech sedm** písmen. Tomu se říká pangram.',
        'Za pangram dostaneš sedm bodů navíc a hra to náležitě oslaví.',
      ],
      key: 'Kolik pangramů plástev má, vidíš v přehledu vlevo.',
    },
    {
      title: 'Jak zadávat slova',
      body: [
        '**Na telefonu:** ťukej přímo do šestiúhelníků. **Smazat** odebere poslední písmeno, **Potvrdit** slovo odešle.',
        '**Na počítači:** piš na klávesnici, Enter potvrdí, mezerník zamíchá plástev.',
        'Tlačítko **Zamíchat** přehází okrajová písmena — pomáhá, když se pohled zasekne.',
      ],
    },
    {
      title: 'Hodnosti',
      visual: { kind: 'hive-ranks' },
      body: [
        'Body za slova tě posouvají po žebříčku hodností od Začátečníka až po **Královnu češtiny**.',
        'Delší slova nesou víc bodů: čtyřpísmenné slovo bod jeden, delší tolik bodů, kolik má písmen.',
        'Plástev můžeš kdykoli uzavřít tlačítkem **Ukončit plástev** a body si necháš.',
      ],
    },
  ],

  tower: [
    {
      title: 'Stav věž ze slov',
      visual: { kind: 'tower' },
      body: [
        'Dole začínáš třípísmenným slovem. Nad ním postavíš čtyřpísmenné, pak pětipísmenné a tak dál až na vrchol.',
        'Každé patro je nové slovo — a věž roste vzhůru pod tvýma rukama.',
      ],
    },
    {
      title: 'Každé patro přidá jedno písmeno',
      visual: { kind: 'tower-letter' },
      body: [
        'Do každého patra dostaneš **jedno nové písmeno**, barevně zvýrazněné.',
        'Z něj a ze všech písmen patra pod ním složíš nové slovo.',
      ],
      key: 'Pořadí písmen je úplně na tobě. Nové slovo se od toho předchozího může lišit k nepoznání.',
    },
    {
      title: 'Použij všechna písmena',
      body: [
        'Tohle je jediné opravdové pravidlo: v každém patře musíš použít **všechna** dostupná písmena, každé právě jednou.',
        'Nemůžeš tedy žádné vynechat ani přidat.',
      ],
      key: 'Z „LES" a nového **E** nevznikne „LESE" — ale **SELE** ano. Nepřidáváš písmeno na konec, skládáš slovo celé znovu.',
    },
    {
      title: 'Jak slovo složíš',
      body: [
        '**Na telefonu:** ťukej do dlaždic v zásobníku, skládají se zleva doprava. **Smazat** vezme poslední zpět.',
        '**Na počítači:** piš na klávesnici, Enter postaví patro, mezerník zamíchá dlaždice.',
        '**Zamíchat** přehází dlaždice — často to samo napoví, jak slovo poskládat.',
      ],
    },
    {
      title: 'Zaseknout se nemůžeš',
      visual: { kind: 'tower-safe' },
      body: [
        'Protože se musí použít všechna písmena, má každé správné řešení patra stejná písmena. Ať zvolíš kterékoli, věž půjde postavit dál.',
        'Žádná tvoje volba tedy nemůže cestu nahoru uzavřít.',
      ],
      key: 'Když ti slovo nenapadne, nápověda **Odhalit písmeno** ti postupně ukáže začátek. Věž se vždycky dá dostavět.',
    },
    {
      title: 'Body',
      body: [
        'Každé postavené patro boduje podle své délky — čím výš, tím víc.',
        'Přidá se bonus za rychlost. Věž postavená bez jediné nápovědy má násobitel.',
      ],
    },
  ],
}

/** Krátký souhrn pravidel na kartu režimu. */
export const MODE_SUMMARY: Record<ModeId, string[]> = {
  chain: [
    'Změň vždy právě jedno písmeno.',
    'Každý mezikrok musí být české slovo.',
    'Žádné slovo se nesmí opakovat.',
  ],
  hive: [
    'Slova aspoň ze 4 písmen.',
    'Prostřední písmeno musí být v každém slově.',
    'Písmena se smí opakovat.',
  ],
  tower: [
    'Každé patro přidá jedno písmeno.',
    'Použij všechna písmena, v libovolném pořadí.',
    'Od tří písmen až na vrchol.',
  ],
}
