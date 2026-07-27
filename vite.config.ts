import { defineConfig } from 'vitest/config'
import react from '@vitejs/plugin-react'

/**
 * Datum buildu. Zobrazuje se v menu drobným písmem — když hráč hlásí, že
 * vidí starou verzi, je z něj hned poznat, jestli mu telefon drží starou
 * cache, nebo je chyba jinde.
 */
const BUILD = new Date().toISOString().slice(0, 16).replace('T', ' ')

/**
 * Kontrolní build Otázky dne.
 *
 * Otázky se v ostré hře odemykají po jedné denně, takže se dvě stě otázek
 * nedá zkontrolovat dřív než za dvě stě dní. `QUIZ_ALL=1 npm run build` udělá
 * verzi, ve které se dají projít všechny za sebou — jinak je nemá jak nikdo
 * přečíst dřív, než je uvidí hráči.
 */
const QUIZ_ALL = process.env.QUIZ_ALL === '1'

export default defineConfig({
  base: './',
  define: {
    __BUILD__: JSON.stringify(QUIZ_ALL ? `${BUILD} · kontrolní` : BUILD),
    __QUIZ_ALL__: JSON.stringify(QUIZ_ALL),
  },
  plugins: [react()],
  build: {
    target: 'es2022',
  },
  test: {
    environment: 'node',
    include: ['tests/**/*.test.ts'],
    testTimeout: 120_000,
  },
})
