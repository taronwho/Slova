/**
 * Kresba šibenice.
 *
 * Osm dílů, jeden za každé chybné písmeno — poslední díl znamená konec kola.
 * Kreslí se stejnou linkou jako ocenění (tloušťka, zakulacené konce), aby to
 * s ostatními kresbami ve hře drželo pohromadě, a v barvě režimu.
 *
 * Každý nový díl se dokreslí animací „napíše se", ne skokem: hráč tak vidí,
 * *co* mu přibylo, i když se nekouká na počítadlo.
 */

interface Props {
  /** Kolik dílů už stojí (0–8). */
  parts: number
  /** Prohrané kolo — celá kresba zčervená. */
  lost?: boolean
}

/** Díly v pořadí, jak se staví. Osmý je současně ruce i nohy. */
const PARTS = [
  'M12 116h76', // základna
  'M30 116V16', // sloup
  'M30 16h44', // rameno
  'M30 36 50 16', // vzpěra
  'M74 16v14', // provaz
  'M74 30a11 11 0 1 1 0 22 11 11 0 0 1 0-22Z', // hlava
  'M74 52v30', // trup
  'M74 60 60 72M74 60l14 12M74 82 62 100M74 82l12 18', // ruce a nohy
]

export function Gallows({ parts, lost = false }: Props) {
  return (
    <svg
      className={`gallows-art ${lost ? 'lost' : ''}`}
      viewBox="0 0 100 124"
      role="img"
      aria-label={`Šibenice: ${parts} z ${PARTS.length} dílů`}
    >
      {PARTS.map((d, i) => (
        <path
          key={d}
          d={d}
          className={`gallows-part ${i < parts ? 'up' : ''}`}
          // Nový díl se dokreslí; starší už jen stojí, aby se při každé
          // chybě nepřekreslovalo celé lešení znovu.
          style={i === parts - 1 ? undefined : { animation: 'none' }}
        />
      ))}
    </svg>
  )
}
