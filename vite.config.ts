import { defineConfig } from 'vitest/config'
import react from '@vitejs/plugin-react'

/**
 * Datum buildu. Zobrazuje se v menu drobným písmem — když hráč hlásí, že
 * vidí starou verzi, je z něj hned poznat, jestli mu telefon drží starou
 * cache, nebo je chyba jinde.
 */
const BUILD = new Date().toISOString().slice(0, 16).replace('T', ' ')

export default defineConfig({
  base: './',
  define: { __BUILD__: JSON.stringify(BUILD) },
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
