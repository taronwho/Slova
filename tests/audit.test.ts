/**
 * Revize provázanosti — kontroluje sliby, které hra dává v textu met.
 *
 * Meta je smlouva: co stojí v `goal`, to musí podmínka doopravdy vyžadovat.
 * Když se v dlaždici píše „bez nápovědy" a odemkne ji kolo s nápovědou,
 * hráč to pozná — a přestane vitríně věřit. Tyhle testy hrají kola nanečisto
 * a sledují, co se z nich v profilu stane.
 */

import { describe, expect, it } from 'vitest'

import { AWARDS, GROUP_LABEL } from '../src/game/awards'
import type { ModeId, RoundResult } from '../src/game/types'
import { emptyProfile, recordRound } from '../src/lib/storage'

const MODES: ModeId[] = ['chain', 'hive', 'tower', 'gallows', 'detective', 'tetris']
const DAY = '2026-07-28'

/** Kolo, které se povedlo. `hints` říká, kolik nápověd si hráč vzal. */
function round(mode: ModeId, hints: number, extra: Record<string, number> = {}): RoundResult {
  return {
    mode,
    difficulty: 'normal',
    puzzleId: `${mode}-test-${hints}-${JSON.stringify(extra)}`,
    score: 500,
    // `perfect` počítají scoring funkce a všechny v něm mají hintsUsed === 0.
    perfect: hints === 0,
    success: true,
    elapsedMs: 90_000,
    hintsUsed: hints,
    detail: {
      moves: 3,
      par: 5,
      found: 10,
      total: 10,
      pangrams: 1,
      solved: 1,
      wrong: 0,
      guessed: 2,
      words: 12,
      chain: 3,
      full: 1,
      top: 7,
      rankTop: 1,
      ...extra,
    },
  }
}

/** Které mety má profil odemčené. */
function granted(profile: ReturnType<typeof emptyProfile>): string[] {
  return AWARDS.filter((a) => profile.awards[a.id] !== undefined).map((a) => a.id)
}

describe('mety s nápovědou', () => {
  it('kolo s nápovědou neodemkne nic ze skupiny „Bez nápovědy"', () => {
    let profile = emptyProfile()
    for (const mode of MODES) {
      profile = recordRound(profile, round(mode, 2), DAY)
    }
    const clean = AWARDS.filter((a) => a.group === 'clean').map((a) => a.id)
    expect(granted(profile).filter((id) => clean.includes(id))).toEqual([])
  })

  it('kolo s nápovědou neodemkne mistrovský stupeň', () => {
    let profile = emptyProfile()
    for (let i = 0; i < 5; i++) {
      for (const mode of MODES) profile = recordRound(profile, round(mode, 1), DAY)
    }
    const mastery = AWARDS.filter((a) => a.group === 'mastery').map((a) => a.id)
    expect(granted(profile).filter((id) => mastery.includes(id))).toEqual([])
  })

  it('nápověda nuluje čítač čistých kol i sérii', () => {
    let profile = emptyProfile()
    profile = recordRound(profile, round('chain', 0), DAY)
    profile = recordRound(profile, round('hive', 0), DAY)
    expect(profile.counters.noHint).toBe(2)
    expect(profile.counters.noHintStreak).toBe(2)
    expect(profile.streak).toBe(2)

    profile = recordRound(profile, round('tower', 1), DAY)
    expect(profile.counters.noHint).toBe(2)
    expect(profile.counters.noHintStreak).toBe(0)
    expect(profile.streak).toBe(0)
  })

  it('nedotažené kolo bez nápovědy se za čisté nepočítá', () => {
    let profile = emptyProfile()
    profile = recordRound(profile, { ...round('gallows', 0), success: false }, DAY)
    expect(profile.counters.noHint).toBe(0)
    expect(profile.stats.gallows.clean).toBe(0)
  })

  it('čisté kolo v Šibenici vyžaduje i nula chyb', () => {
    let profile = emptyProfile()
    profile = recordRound(profile, round('gallows', 0, { wrong: 2 }), DAY)
    expect(profile.counters.gallowsClean).toBe(0)

    profile = recordRound(profile, round('gallows', 0, { wrong: 0 }), DAY)
    expect(profile.counters.gallowsClean).toBe(1)
  })

  it('dostavěná věž s nápovědou nezvýší čítač věží bez lešení', () => {
    let profile = emptyProfile()
    profile = recordRound(profile, round('tower', 3, { full: 1 }), DAY)
    expect(profile.counters.towerFull).toBe(1)
    expect(profile.counters.towerFullNoHint).toBe(0)
  })

  it('rychlostní meta se neměří na kole s nápovědou', () => {
    let profile = emptyProfile()
    profile = recordRound(profile, { ...round('chain', 2), elapsedMs: 10_000 }, DAY)
    expect(profile.counters.chainFastMs).toBe(0)
  })

  /**
   * Věž měla rychlostní metu bez podmínky na nápovědu, takže se dala získat
   * tím, že hráč třikrát ťukl na „Celé slovo". Řetěz to hlídal od začátku.
   */
  it('čas věže se měří jen bez nápovědy', () => {
    let profile = emptyProfile()
    profile = recordRound(profile, { ...round('tower', 4, { full: 1 }), elapsedMs: 20_000 }, DAY)
    expect(profile.counters.towerFull).toBe(1)
    expect(profile.counters.towerFastMs).toBe(0)

    profile = recordRound(profile, { ...round('tower', 0, { full: 1 }), elapsedMs: 20_000 }, DAY)
    expect(profile.counters.towerFastMs).toBe(20_000)
  })

  /** „Celé slovo" vede hráče přímo po nejkratší cestě, takže se nepočítá. */
  it('nejkratší cesta v Řetězu se počítá jen bez nápovědy', () => {
    let profile = emptyProfile()
    profile = recordRound(profile, round('chain', 1, { moves: 5, par: 5 }), DAY)
    expect(profile.counters.chainPar).toBe(0)

    profile = recordRound(profile, round('chain', 0, { moves: 5, par: 5 }), DAY)
    expect(profile.counters.chainPar).toBe(1)
  })
})

describe('text mety sedí s podmínkou', () => {
  /**
   * Meta, jejíž popis slibuje kolo bez nápovědy, se nesmí dát splnit kolem
   * s nápovědou. Test to nečte z kódu — odehraje kola s nápovědou a podívá
   * se, jestli některá taková meta padla.
   */
  it('žádná meta se slovem „nápověd" nepadne po kolech s nápovědou', () => {
    let profile = emptyProfile()
    for (let i = 0; i < 60; i++) {
      for (const mode of MODES) {
        profile = recordRound(profile, { ...round(mode, 1), puzzleId: `${mode}-${i}` }, DAY)
      }
    }
    const promised = AWARDS.filter(
      (a) => /nápověd|lešení|načisto|škobrtnut|chyby/i.test(a.goal),
    ).map((a) => a.id)
    expect(granted(profile).filter((id) => promised.includes(id))).toEqual([])
  })

  it('každá skupina met má popisek', () => {
    for (const award of AWARDS) {
      expect(GROUP_LABEL[award.group], award.id).toBeTruthy()
    }
  })
})
