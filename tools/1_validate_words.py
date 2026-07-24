"""Krok 1 — ověření slovní zásoby.

Vezme frekvenční seznam českých slov (OpenSubtitles) a profiltruje ho přes
hunspellový slovník cs_CZ. Hunspell zároveň spolehlivě odstraní vlastní jména:
ta jsou ve slovníku uložena jen s velkým počátečním písmenem, takže lookup
jejich malé varianty ("praha", "brno") selže.

Výstup: tools/out/words.tsv  ->  slovo <TAB> frekvence
"""

import multiprocessing as mp
import os
import sys
import time

CZ = set("aábcčdďeéěfghiíjklmnňoópqrřsštťuúůvwxyýzž")

RAW = os.path.join(os.path.dirname(__file__), "raw")
OUT = os.path.join(os.path.dirname(__file__), "out")

MIN_LEN = 3
MAX_LEN = 9
MIN_FREQ = 2

_dict = None


def _init():
    global _dict
    from spylls.hunspell import Dictionary

    _dict = Dictionary.from_files(os.path.join(RAW, "cs_CZ"))


def _check(chunk):
    return [(w, f) for w, f in chunk if _dict.lookup(w)]


def candidates():
    with open(os.path.join(RAW, "cs_full.txt"), encoding="utf-8") as fh:
        for line in fh:
            parts = line.split()
            if len(parts) != 2:
                continue
            word, freq = parts[0], int(parts[1])
            if freq < MIN_FREQ:
                continue
            if not (MIN_LEN <= len(word) <= MAX_LEN):
                continue
            if not set(word) <= CZ:
                continue
            yield word, freq


def chunked(iterable, size):
    batch = []
    for item in iterable:
        batch.append(item)
        if len(batch) >= size:
            yield batch
            batch = []
    if batch:
        yield batch


def main():
    os.makedirs(OUT, exist_ok=True)
    cands = list(candidates())
    print(f"kandidátů: {len(cands)}", flush=True)

    started = time.time()
    done = 0
    valid = []
    with mp.Pool(processes=mp.cpu_count(), initializer=_init) as pool:
        for result in pool.imap_unordered(_check, chunked(cands, 2000)):
            valid.extend(result)
            done += 2000
            if done % 50000 < 2000:
                rate = done / max(time.time() - started, 1e-6)
                print(
                    f"  {done}/{len(cands)}  platných {len(valid)}  {rate:.0f}/s",
                    flush=True,
                )

    valid.sort(key=lambda wf: (-wf[1], wf[0]))
    path = os.path.join(OUT, "words.tsv")
    with open(path, "w", encoding="utf-8") as fh:
        for word, freq in valid:
            fh.write(f"{word}\t{freq}\n")

    print(f"hotovo: {len(valid)} platných slov -> {path}", flush=True)
    print(f"čas: {time.time() - started:.0f}s", flush=True)


if __name__ == "__main__":
    sys.exit(main())
