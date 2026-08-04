# Multiplayer — Firebase

Pravidla databáze pro Realtime Database projektu `slova-b0176`
(region `europe-west1`, kvůli latenci u českých hráčů).

## Jak je nasadit

Firebase konzole → **Build → Realtime Database → záložka Rules** → smazat
obsah, vložit `database.rules.json` → **Publish**.

## Co která větev drží

| cesta | k čemu je |
|---|---|
| `nicks/{přezdívka}` | zabrané přezdívky → id hráče |
| `players/{id}` | přezdívka, pásmo hodnosti, výhry a prohry |
| `results/{hra}/{hádanka}/{id}` | výsledek jednoho hráče v jedné hádance |
| `challenges/{komu}/{id}` | došlé výzvy — kdo vyzval a na který zápas |
| `duels/{zápas}` | zápas dvou jmenovitých hráčů: co se hraje a s kým |
| `duels/{zápas}/words/{slovo}` | komu patří které slovo v soubojové Voštině |
| `duels/{zápas}/done/{id}` | hotový výsledek jedné strany |

## Na čem stojí bezpečnost

Databáze je celá zavřená (`".read": false` v kořeni) a otevírá se jen
tam, kde je to nutné. Tři pravidla dělají většinu práce:

* **Přezdívka se nedá ukrást.** Zápis do `nicks/{přezdívka}` projde jen
  tehdy, když tam ještě nic není (`!data.exists()`) a zapisuje se vlastní
  `auth.uid`. Když dva lidé pošlou stejné jméno v tutéž vteřinu, uspěje
  právě jeden a druhý dostane chybu — bez transakcí a bez čekání.
* **Výsledek se nedá přepsat.** `results` má stejnou podmínku, takže se
  skóre nedá po prohře vylepšit. Hráč navíc smí zapsat jen pod svoje id.
* **Čas si neurčuje telefon.** `at` musí být přesně `now`, což je čas
  serveru. Jinak by šlo předstírat, že odpověď padla dřív.
* **Slovo v souboji patří tomu, kdo byl dřív.** `duels/{zápas}/words`
  má tutéž podmínku `!data.exists()`, takže se druhý zápis odmítne a hra
  z toho pozná, že slovo mezitím sebral soupeř. Do zápasu navíc smí sáhnout
  jen ti dva, kterých se týká.

Přezdívka ve výsledku se ověřuje proti `players/{id}/nick`, takže se
nedá vydávat za někoho jiného.

Co pravidla **neumí**: přepočítat skóre. Klient smí zapsat jakékoli číslo
v povoleném rozsahu. Pro souboje kamarádů to stačí; kdyby měl vzniknout
veřejný žebříček, musela by skóre počítat serverová funkce (tarif Blaze).
