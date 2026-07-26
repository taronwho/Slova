/**
 * Sdílené kroky pro testy v prohlížeči.
 *
 * Ovládání hry se občas mění (dlaždice místo karet, úvodní značka, panel
 * s volbami), a když je každý skript hledá po svém, opraví se po změně jen
 * některé. Odsud si je berou všechny.
 */

/** Počká, než zmizí úvodní značka — přes ni se nedá klikat. */
export async function waitReady(page) {
  await page.locator('.splash').waitFor({ state: 'detached', timeout: 8000 }).catch(() => undefined)
}

/** Po prvním spuštění režimu se otevře návod; testy ho odbaví. */
export async function dismissTutorial(page) {
  const card = page.locator('.tut-card')
  if (await card.isVisible().catch(() => false)) {
    await page.locator('.tut-head').getByText('Přeskočit').click()
    await page.waitForTimeout(250)
  }
}

/** Z menu do rozehrané hry: dlaždice režimu -> panel s volbami -> Hrát. */
export async function openGame(page, mode, { daily = false, resume = false } = {}) {
  await waitReady(page)
  await page.locator(`.mode-tile[data-mode="${mode}"]`).click()
  await page.locator('.sheet').waitFor()
  const label = daily ? /^Denní/ : resume ? /^Pokračovat/ : /^(Hrát|Nová hra)$/
  await page.locator('.sheet-actions .btn', { hasText: label }).first().click()
  await page.waitForSelector('.board', { timeout: 20000 })
  await dismissTutorial(page)
}

/** Zpět do menu, ať už je nad hrou výsledek kola, nebo ne. */
export async function goHome(page) {
  const back = page.locator('.result-actions .btn', { hasText: 'Domů' })
  if (await back.isVisible().catch(() => false)) await back.click()
  else {
    const menu = page.locator('.btn-back')
    if (await menu.isVisible().catch(() => false)) await menu.click()
    else await page.locator('.topbar .brand').click()
  }
  await page.waitForSelector('h1:has-text("Vyber si hru")')
  const scrim = page.locator('.sheet-scrim')
  if (await scrim.isVisible().catch(() => false)) {
    await scrim.click({ position: { x: 5, y: 5 } })
  }
}
