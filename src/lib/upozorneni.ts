/**
 * Upozornění na došlou výzvu.
 *
 * Co tohle umí a co ne, ať v tom není zmatek:
 *
 * * **Umí:** dát vědět, když hra běží — i když je zrovna schovaná na pozadí
 *   nebo je hráč v jiné hře. To pokrývá většinu případů, kdy si dva lidé
 *   posílají výzvy během večera.
 * * **Neumí:** dát vědět, když je aplikace úplně zavřená. K tomu je potřeba
 *   Firebase Cloud Messaging a k němu server, který zprávu odešle — klíč
 *   k odesílání je tajný a do telefonu se dát nesmí, jinak by kdokoli mohl
 *   posílat upozornění všem hráčům. Znamenalo by to založit Cloud Function
 *   (a k ní placený tarif Firebase).
 *
 * Povolení se neptá samo od sebe při spuštění — to je otravné a prohlížeče
 * to trestají. Ptá se ve chvíli, kdy si hráč zabere přezdívku nebo otevře
 * Hru s přáteli: tam dává smysl a hráč ví, proč se ho ptáme.
 */

/** Umí tenhle prohlížeč upozornění vůbec? */
export function upozorneniJdou(): boolean {
  return typeof window !== 'undefined' && 'Notification' in window
}

export type Povoleni = 'ano' | 'ne' | 'nezeptáno' | 'nejde'

export function stavPovoleni(): Povoleni {
  if (!upozorneniJdou()) return 'nejde'
  if (Notification.permission === 'granted') return 'ano'
  if (Notification.permission === 'denied') return 'ne'
  return 'nezeptáno'
}

/**
 * Požádá o povolení. Vrací výsledek.
 *
 * Volá se z ťuknutí hráče, ne z načtení stránky — bez gesta ho některé
 * prohlížeče rovnou zamítnou a druhá šance pak už není.
 */
export async function pozadatOPovoleni(): Promise<Povoleni> {
  if (!upozorneniJdou()) return 'nejde'
  if (Notification.permission !== 'default') return stavPovoleni()
  try {
    await Notification.requestPermission()
  } catch {
    // Starší prohlížeče berou jen tvar s funkcí zpětného volání.
  }
  return stavPovoleni()
}

/**
 * Ukáže upozornění.
 *
 * Přes service worker, když je po ruce — na Androidu je to jediná cesta,
 * jak upozornění ukázat i tehdy, když je stránka na pozadí. Když worker
 * není, zkusí se obyčejné okno.
 */
export async function upozorni(titulek: string, text: string): Promise<void> {
  if (stavPovoleni() !== 'ano') return
  const nastaveni: NotificationOptions = {
    body: text,
    icon: './icons/icon-192.png',
    badge: './icons/icon-192.png',
    // Stejná značka = novější upozornění nahradí starší místo hromady.
    tag: 'slova-vyzva',
    lang: 'cs',
  }
  try {
    const worker = await navigator.serviceWorker?.getRegistration()
    if (worker) {
      await worker.showNotification(titulek, nastaveni)
      return
    }
  } catch {
    // Bez workeru se to zkusí postaru.
  }
  try {
    new Notification(titulek, nastaveni)
  } catch {
    // Android bez workeru upozornění z okna nedovolí — nedá se nic dělat.
  }
}
