/**
 * Obsah návodů — texty pravidel pro hráče.
 *
 * Drží se odděleně od komponent, aby šel stejný text použít v tutoriálu při
 * prvním spuštění i v přehledu pravidel na domovské obrazovce.
 */

import { AWARDS } from './awards'
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
  | { kind: 'word-forms' }
  | { kind: 'gallows' }
  | { kind: 'gallows-fold' }
  | { kind: 'detective' }
  | { kind: 'tetris' }
  | { kind: 'tetris-chain' }

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
      title: 'Jaké tvary slov platí',
      visual: { kind: 'word-forms' },
      body: [
        'Hra pracuje **jen se základními tvary** — tak, jak slovo najdeš ve slovníku. Díky tomu nesbíráš pořád dokola pády jednoho slova.',
        '**Platí:** podstatná jména v 1. pádu — jednotné i množné číslo (pes, psi, kočka, kočky), slovesa v infinitivu (psát, běhat), přídavná jména (velký, rychlý), číslovky (pět), zájmena (ten, každý), příslovce (dnes, brzy) a spojky (nebo, ale).',
        '**Neplatí:** ostatní pády (psa, psovi, psem, psy), časované tvary (píšu, píšeš, psal), rozkazy (piš) ani stupňování (rychlejší).',
      ],
      key: 'Když ti hra slovo neuzná, bývá to tímhle — zkus jeho základní tvar.',
    },
    {
      title: 'Jeden tah = jedno písmeno',
      visual: { kind: 'chain-move' },
      body: [
        'V každém tahu smíš změnit **právě jedno** písmeno. Písmena se nepřesouvají ani nepřidávají — jen se jedno vymění za jiné.',
        'Výsledek musí být platné české slovo **v základním tvaru** — jak ho najdeš ve slovníku.',
      ],
      key: 'KOSA → KOZA je platný tah — změnilo se jediné písmeno. KOSA → KOZY ne, to jsou změny dvě.',
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
      title: 'Jaké tvary slov platí',
      visual: { kind: 'word-forms' },
      body: [
        'Hra pracuje **jen se základními tvary** — tak, jak slovo najdeš ve slovníku. Díky tomu nesbíráš pořád dokola pády jednoho slova.',
        '**Platí:** podstatná jména v 1. pádu — jednotné i množné číslo (pes, psi, kočka, kočky), slovesa v infinitivu (psát, běhat), přídavná jména (velký, rychlý), číslovky (pět), zájmena (ten, každý), příslovce (dnes, brzy) a spojky (nebo, ale).',
        '**Neplatí:** ostatní pády (psa, psovi, psem, psy), časované tvary (píšu, píšeš, psal), rozkazy (piš) ani stupňování (rychlejší).',
      ],
      key: 'Když ti hra slovo neuzná, bývá to tímhle — zkus jeho základní tvar.',
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
        'Platí jen **1. pád a infinitiv**. „Kolo" i „kola" ano, „kolem" ani „kolu" ne.',
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
      title: 'Jaké tvary slov platí',
      visual: { kind: 'word-forms' },
      body: [
        'Hra pracuje **jen se základními tvary** — tak, jak slovo najdeš ve slovníku. Díky tomu nesbíráš pořád dokola pády jednoho slova.',
        '**Platí:** podstatná jména v 1. pádu — jednotné i množné číslo (pes, psi, kočka, kočky), slovesa v infinitivu (psát, běhat), přídavná jména (velký, rychlý), číslovky (pět), zájmena (ten, každý), příslovce (dnes, brzy) a spojky (nebo, ale).',
        '**Neplatí:** ostatní pády (psa, psovi, psem, psy), časované tvary (píšu, píšeš, psal), rozkazy (piš) ani stupňování (rychlejší).',
      ],
      key: 'Když ti hra slovo neuzná, bývá to tímhle — zkus jeho základní tvar.',
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
  gallows: [
    {
      title: 'Uhodni schované slovo',
      visual: { kind: 'gallows' },
      body: [
        'Slovo je schované za prázdnými políčky — víš jen, kolik má písmen.',
        'Zkoušíš písmena. Když sedí, doplní se do všech míst, kde ve slově je. Když nesedí, přibude jeden díl šibenice.',
      ],
      key: 'Osm chybných písmen a kolo končí. Devátý díl už se nekreslí.',
    },
    {
      title: 'Háčky a čárky se nehádají',
      visual: { kind: 'gallows-fold' },
      body: [
        'Klávesnice má jen základní písmena. „u" odhalí **u**, **ú** i **ů**, „c" odhalí **c** i **č**.',
        'Hádá se slovo, ne diakritika — jinak by to bylo trápení s háčky místo hry.',
      ],
      key: 'Diakritika se doplní sama tak, jak ve slově opravdu je.',
    },
    {
      title: 'Jaké tvary slov platí',
      visual: { kind: 'word-forms' },
      body: [
        'Hra pracuje **jen se základními tvary** — tak, jak slovo najdeš ve slovníku.',
        '**Platí:** podstatná jména v 1. pádu — jednotné i množné číslo (pes, psi, kočka, kočky), slovesa v infinitivu (psát, běhat), přídavná jména (velký, rychlý), číslovky (pět), zájmena (ten, každý), příslovce (dnes, brzy) a spojky (nebo, ale).',
        '**Neplatí:** ostatní pády (psa, psovi, psem, psy), časované tvary (píšu, píšeš, psal), rozkazy (piš) ani stupňování (rychlejší).',
      ],
      key: 'Slova jsou navíc vybíraná od nejběžnějších, takže nejde o hádání raritních výrazů.',
    },
    {
      title: 'Nápovědy',
      body: [
        '**Odhal písmeno** ukáže jedno z těch, která ti ještě chybí — vybere to, které je ve slově nejčastěji.',
        '**Vyškrtni pět** zhasne na klávesnici pět písmen, která ve slově nejsou. Život tě to nestojí, jen body.',
      ],
      key: 'Nápověda zaplacená inkoustem body nestrhne. Kolo s ní ale pořád není kolo bez nápovědy.',
    },
    {
      title: 'Body',
      body: [
        'Za uhodnuté slovo je základ, k němu prémie za každý nevyužitý život.',
        'Za chybné písmeno se strhává, rychlost přidává. Kolo bez jediné chyby a bez nápovědy má násobitel.',
        'I neuhodnuté slovo něco dá — počítají se odhalená písmena.',
      ],
    },
  ],
  intruder: [
    {
      title: 'Najdi slovo, které nepatří',
      body: [
        'Dostaneš pět slov. Čtyři z nich něco spojuje. Páté je vetřelec.',
        'Vetřelec je vždycky **právě jeden**: na zbylých dvou znacích se pětice shoduje, takže ukázat jinam a mít taky pravdu nejde.',
      ],
      key: 'Nehádá se tu slovo, ale co k sobě patří.',
    },
    {
      title: 'A pak řekni proč',
      body: [
        'Když na vetřelce ukážeš, vybereš ještě ze tří nabídnutých možností, co ta ostatní čtyři spojovalo.',
        'Trefit slovo se dá i náhodou, jedna ku pěti. Pojmenovat souvislost už ne — proto je za důvod skoro tolik bodů co za samotnou trefu.',
      ],
      key: 'Nápověda umí odklidit jedno slovo, které vetřelec není. Jde ale jen do chvíle, než ukážeš.',
    },
  ],
  quotes: [
    {
      title: 'Doplň výrok',
      body: [
        'Dostaneš citát, ve kterém je vidět jen část slov. Zbytek odkrýváš po písmenech jako v Šibenici.',
        'Hádá se celá věta, ne jedno slovo — odkryté kousky napoví smysl a od něj se dá k ostatním slovům dojít.',
      ],
      key: 'Chyba kolo neukončí, jen stojí body. Po čtrnácti chybách ale kolo skončí.',
    },
    {
      title: 'Nápovědy po stupních',
      body: [
        'První nápověda ukáže podobiznu autora, druhá jeho zařazení („český spisovatel"), třetí rovnou jméno.',
        'Teprve pak se odkrývají celá slova — a vždycky to nejdelší, protože to pomůže nejvíc.',
      ],
      key: 'Podobizna se stahuje z internetu. Bez připojení se přeskočí a inkoust se nestrhne.',
    },
  ],
  detective: [
    {
      title: 'Poznej slovo podle spisu o něm',
      visual: { kind: 'detective' },
      body: [
        'Dostaneš spis: slovní druh, počet slabik, co slovo znamená — a u některých i to, odkud přišlo.',
        'Slovo samo je schované za prázdnými políčky. Víš jen, kolik má písmen.',
      ],
      key: 'Spis je z Wikislovníku. Kde by hledané slovo prozradil, je místo něj okénko s otazníkem. Celý původ se odkryje až po dohrání.',
    },
    {
      title: 'Tady se nevěší',
      body: [
        'Na rozdíl od Šibenice tě chybné písmeno nezabije — jen tě stojí body. Můžeš tedy v klidu zkoušet a přemýšlet.',
        'Kolo skončí, až slovo odhalíš, nebo když sáhneš dvanáctkrát vedle.',
      ],
      key: 'Text má být vodítko, se kterým se dá pracovat. Proto se za omyl neplatí koncem hry.',
    },
    {
      title: 'Tipni celé slovo',
      body: [
        'Když ti to z textu dojde, nemusíš doklikávat zbytek písmen. Tlačítkem **Znám ho** napíšeš slovo celé.',
        'Čím víc písmen je v tu chvíli ještě skrytých, tím vyšší prémie. Chybný tip stojí jako pár písmen vedle.',
      ],
      key: 'Diakritiku psát nemusíš — „kun" projde stejně jako „kůň".',
    },
    {
      title: 'Body',
      body: [
        'Základ je za rozluštěné slovo, k němu prémie za tip a za rychlost.',
        'Odečítají se písmena vedle, chybné tipy a nápovědy. Případ vyřešený bez jediného škobrtnutí má násobitel.',
      ],
    },
  ],

  tetris: [
    {
      title: 'Padají slabiky, ty z nich skládáš slova',
      visual: { kind: 'tetris' },
      body: [
        'Shora padá dvojice slabik. Posouváš ji doleva a doprava, otáčíš a můžeš ji nechat spadnout naráz.',
        'Jakmile dvě nebo tři sousední slabiky dají platné české slovo, slovo zmizí a co bylo nad ním, spadne dolů.',
      ],
      key: 'Vodorovně se čte zleva doprava, svisle **zdola nahoru** — tím směrem, kterým sloupec roste.',
    },
    {
      title: 'Otáčení je celá hra',
      visual: { kind: 'tetris-chain' },
      body: [
        'Dvojice má čtyři polohy a v každé se čte jinak. „ko" a „lo" dá KOLO vodorovně i svisle — jen je otočit správně.',
        'Zhruba každá třetí dvojice je rozdělené slovo. Ostatní musíš doplnit tím, co už na desce leží.',
      ],
      key: 'Delší slovo má přednost: ze „žra-lok" se nestane „lok".',
    },
    {
      title: 'Jaké tvary slov platí',
      visual: { kind: 'word-forms' },
      body: [
        'Hra pracuje **jen se základními tvary** — tak, jak slovo najdeš ve slovníku.',
        '**Platí:** podstatná jména v 1. pádu — jednotné i množné číslo, slovesa v infinitivu, přídavná jména, číslovky, zájmena, příslovce a spojky.',
        '**Neplatí:** ostatní pády, časované tvary, rozkazy ani stupňování.',
      ],
      key: 'Hra má předem spočítaný seznam devíti tisíc slov, která z padajících slabik jdou složit. Nic neodhaduje.',
    },
    {
      title: 'Řetěz a tempo',
      body: [
        'Když po zmizelém slově spadne dolů něco, co složí další slovo, řetěz pokračuje sám a násobitel roste.',
        'Každých pár složených slov přidá úroveň a s ní tempo. Kolo končí, až se nová dvojice nemá kam vejít.',
      ],
      key: 'Pauza je zdarma a kdykoli. Nápověda **Poradit** ukáže polohu, ve které se právě teď dá něco složit.',
    },
    {
      title: 'Body',
      body: [
        'Za každé slovo body podle jeho délky, za řetěz prémie a za dosaženou úroveň bonus.',
        'Kolo bez jediné nápovědy a aspoň s tuctem slov má násobitel.',
      ],
    },
  ],
}

/**
 * Průvodce celou hrou — to, co návody jednotlivých her neřeknou.
 *
 * Návod k Řetězu vysvětlí Řetěz, ale nikde se hráč nedozvěděl, co je věhlas,
 * proč se mu láme série a odkud se bere inkoust. Tenhle text je proto o hře
 * jako celku a otevře se sám při úplně prvním spuštění; potom je pod tlačítkem
 * na domovské obrazovce.
 *
 * Odkaz `term` pověsí pod odstavec vysvětlivku ze slovníčku, takže se z každé
 * kapitoly dá jít o patro hloub, aniž by průvodce zbytněl do referenční příručky.
 */
export interface GuideSection {
  title: string
  body: string[]
  /** Klíč do glossary.ts — nabídne se pod textem jako „Víc o…". */
  term?: string
}

export const GUIDE: GuideSection[] = [
  {
    title: 'Soubor slovních her',
    body: [
      'Slova jsou souborem slovních her, které sdílejí jeden slovník a jeden profil. Je jedno, kterou z nich hraješ — body, hodnost i ocenění se sčítají dohromady.',
      'Každá hra má vlastní podrobný návod. Otevřeš ho na domovské obrazovce, nebo kdykoli během hraní otazníkem v horní liště.',
    ],
  },
  {
    title: 'Jedno pravidlo platí všude',
    body: [
      'Uznávají se **jen základní tvary** — tak, jak slovo stojí ve slovníku. Platí podstatná jména v 1. pádu (jednotné i množné číslo), slovesa v infinitivu a přídavná jména i číslovky v základním tvaru.',
      'Neplatí ostatní pády, časované tvary, rozkazy ani stupňování. Když ti hra slovo neuzná, bývá to skoro vždycky tímhle.',
    ],
    term: 'zaklad',
  },
  {
    title: 'Body a věhlas',
    body: [
      'Za dohrané kolo dostaneš body — základ za splněný cíl a k tomu prémie za rychlost, čistotu a povedené kousky.',
      'Součet všech bodů za celou dobu je **věhlas**. Nikdy neklesá, nedá se utratit a jenom on žene hodnost nahoru.',
      'Dobré kolo dá kolem čtyř set bodů. Čísla schválně nejsou nafouklá: když je štědré všechno, není štědré nic.',
    ],
    term: 'body',
  },
  {
    title: 'Hodnost',
    body: [
      'Padesát stupňů od Nováčka po Vládce slov. První tři hodnosti padnou hned první večer, dál se rozestupy natahují — na tu poslední se hraje roky.',
      'Odznak se mění po každých pěti hodnostech. Uvnitř pětice poznáš stupeň podle počtu krokví pod odznakem.',
    ],
    term: 'hodnost',
  },
  {
    title: 'Inkoust a nápovědy',
    body: [
      'Každá hra umí poradit. Nápověda se platí buď **body** z rozehraného kola, nebo **inkoustem** — a inkoust je ta možnost, po které ti skóre zůstane celé.',
      'Cena odpovídá velikosti pomoci: malý postrk stojí pět inkoustu, odhalení celého slova dvacet. Inkoust se nedá koupit za peníze — sype ho nová hodnost, získané ocenění a kompletní denní várka.',
      'Nápověda placená inkoustem je pořád nápověda: kolo s ní není čisté a mety „bez nápovědy" se za inkoust koupit nedají. Inkoust šetří skóre, ne poctivost.',
    ],
    term: 'inkoust',
  },
  {
    title: 'Série a dny v řadě',
    body: [
      '**Série** je řada čistých kol za sebou — dohraných do konce a bez jediné nápovědy. Násobí se jí skóre, takže se vyplatí ji držet: prohrané, vzdané i napovězené kolo ji utne na nulu.',
      '**Dny v řadě** jsou něco jiného. Počítají se dny, kdy sis hru aspoň jednou otevřel, a nepovedené kolo je nepřeruší.',
    ],
    term: 'serie',
  },
  {
    title: 'Ocenění',
    body: [
      `Trvalých met je ${AWARDS.length} a většina z nich stojí v žebříčcích po několika stupních — u mistrovství jednotlivých her od Učně po Legendu. Ve vitríně vidíš získané stupně a vždycky jeden další, na který se dá dosáhnout.`,
      'Nejvyšší stupně jsou schválně daleko. Slova mají vydržet roky, ne týden.',
    ],
    term: 'oceneni',
  },
  {
    title: 'Denní výzva',
    body: [
      'Jedna hádanka na den pro každou hru, pro všechny hráče stejná. Za dohrání celé denní várky padne inkoust.',
      'Je to nejspolehlivější způsob, jak si udržet plný kalamář — a jediný, který se nedá dohnat zpětně.',
    ],
    term: 'denni',
  },
  {
    title: 'Otázka dne',
    body: [
      'Mimo slovní hry je tu ještě jedna, která se hraje **jednou za den** a neptá se na češtinu, ale na cokoli: osobnosti, zeměpis, vědu, kulturu, historii, přírodu, techniku, sport, jazyk i společnost.',
      'Uvidíš jen nadpis a předem se rozhodneš, kolik indicií si vezmeš. První je pro znalce oboru, třetí skoro prozradí — a čím míň jich vezmeš, tím větší odměna v inkoustu.',
      'Body ani věhlas nedává, zato je to nejštědřejší zdroj inkoustu ve hře. Za neuhodnutou otázku není nic, jen povzbuzení na zítřek.',
    ],
    term: 'otazka',
  },
  {
    title: 'Když si nejsi jistý',
    body: [
      'Ve Slovech jde kliknout na všechno. Každé číslo v liště, každý čip v profilu i každá dlaždice ocenění ti po ťuknutí řekne, co znamená, nebo tě rovnou přepne tam, kde se to dá vyřešit.',
    ],
  },
]

/** Krátký souhrn pravidel na kartu režimu. */
export const MODE_SUMMARY: Record<ModeId, string[]> = {
  chain: [
    'Změň vždy právě jedno písmeno.',
    'Jen 1. pád a infinitiv.',
    'Žádné slovo se nesmí opakovat.',
  ],
  hive: [
    'Slova aspoň ze 4 písmen.',
    'Prostřední písmeno musí být v každém slově.',
    'Jen 1. pád a infinitiv.',
  ],
  tower: [
    'Každé patro přidá jedno písmeno.',
    'Použij všechna písmena, v libovolném pořadí.',
    'Jen 1. pád a infinitiv.',
  ],
  gallows: [
    'Zkoušej písmena, osm chyb a konec.',
    'Háčky a čárky se nehádají — „u" odhalí i „ů".',
    'Jen 1. pád a infinitiv.',
  ],
  detective: [
    'Spis říká, co slovo znamená a odkud je.',
    'Chyba nezabíjí, jen stojí body.',
    'Kdo na slovo přijde, může ho tipnout celé.',
  ],
  tetris: [
    'Otoč dvojici, ať dá slovo.',
    'Vodorovně zleva, svisle zdola nahoru.',
    'Jen 1. pád a infinitiv.',
  ],
  intruder: [
    'Čtyři slova něco spojuje, páté ne.',
    'Nejdřív ukaž na vetřelce, pak řekni proč.',
    'Za důvod je skoro tolik bodů co za trefu.',
  ],
  quotes: [
    'Část slov výroku dostaneš zadarmo.',
    'Zbytek odkrývej po písmenech.',
    'Nápovědy jdou od podobizny ke jménu autora.',
  ],
}
