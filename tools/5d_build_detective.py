"""Krok 5d — hádanky pro Etymologického detektiva.

Ze stažených etymologií (krok 5c) se vyberou ty, které se dají použít jako
hádanka. Rozhoduje se o **použitelnosti, ne o pravdivosti** — text je tak jak
ho napsal Wikislovník, jen očištěný a zkrácený.

Vyhazuje se:

1. **Text, který slovo prozradí.** Nejčastější případ jsou složeniny:
   „Ze spojení jest-li" u hesla *jestli* nebo „Složením slov tak a hle"
   u *takhle*. Kontroluje se shoda podle základu slova bez diakritiky, obojím
   směrem, plus úvodní formulky složenin.
2. **Příliš krátký text.** „Z praslovanského *dobrъ." je pravda, ale po
   zakrytí rekonstrukce z něj nezbyde nic, z čeho by se dalo vyjít. Hranice
   je čtyřicet dva znaků a drží se schválně tam: pod ní jsou skoro samé
   slovotvorné rozbory („Utvořeno předponou pře- od slovesa žít"), které
   odpověď vlastně prozradí.
3. **Slovní druhy, které se nehádají.** Spojky a částice; zůstávají podstatná
   a přídavná jména, slovesa a příslovce.
4. **Odkazovací ocas.** „Srovnej např. stožár, stehno, stěžeň" je ve slovníku
   užitečné, v hádance je to jmenný seznam, který o hledaném slově neříká nic.
   Krátí se navíc jen po celých větách — useknuté souvětí čtenáře jen zmate.

Výstup: public/data/detective/puzzles.json
"""

import difflib
import json
import os
import re
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
RAW = os.path.join(HERE, "raw")
DATA = os.path.join(HERE, "..", "public", "data", "detective")

# Spodní hranice je nízko schválně. „Z předpokládaného praslovanského *zvǫkъ."
# je jen čtyřicet znaků, ale hádat se z toho dá — a takových stručných hesel
# má Wikislovník stovky, o které by hra jinak přišla.
MIN_TEXT, MAX_TEXT = 42, 300
# Kolik zamaskovaných míst text ještě unese, než přestane dávat smysl.
MAX_MASKS = 2
# Značka zakrytého slova. Schválně to není výpustka — ta se v etymologických
# textech vyskytuje sama o sobě a hráč by pak nepoznal, kde je díra k hádání.
MASK = "[?]"
MIN_WORD, MAX_WORD = 4, 14
KEEP_POS = {"noun", "adj", "verb", "adv"}

# Odkazovací ocas hesla. Wikislovník za výklad rád přidá řadu příbuzných či
# jen podobně tvořených slov („Srovnej např. stožár, stehno, stěžeň“). Ve
# slovníku to smysl dává, v hádance ne: hráč čte jmenný seznam, který
# o hledaném slově neříká nic, a ještě ho svádí na scestí.
# „srov." končí tečkou, takže za ním nesmí být \b — to je hranice mezi
# písmenem a tečkou, ne mezi tečkou a mezerou.
XREF_WORD = r"(?:srov\.|srovnej\w*|srovnávej|srovnává\s+se|porovnej\w*|viz\b)"
XREF_TAIL = re.compile(
    r"(?:[;,.]\s*|\s+[—–-]\s*|\s+)"
    r"(?:(?:dále|též|také)\s+)?" + XREF_WORD + r".*$",
    re.I | re.S,
)
# Celá věta, která je jenom odkaz.
XREF_START = re.compile(r"^(?:(?:dále|též|také)\s+)?" + XREF_WORD, re.I)
# Poznámky redakce uvnitř textu: „(viz význam [3])“, „[1]“.
XREF_PAREN = re.compile(r"\s*\((?:viz|srov)[^)]*\)", re.I)
REF_NUM = re.compile(r"\s*\[\d+\]")

# Úvody, po kterých následuje rozbor složeniny — ten slovo vždycky vyzradí.
COMPOUND_START = re.compile(
    r"^(složen|slozen|ze spojení|ze slovního spojení|slovním spojením|spojením"
    r"|z\s+spojení|zdrobněl)",
    re.I,
)


# Slovo včetně kombinujících znamének. V rekonstrukcích jsou navíc přízvuky
# („*mě̀sto"), a kdyby se braly jako hranice slova, rozpadlo by se hledané
# slovo na dva neškodně vypadající kousky a proklouzlo by.
TOKEN_RE = re.compile(r"([^\W\d_](?:[^\W\d_]|[\u0300-\u036f])*)", re.UNICODE)


def fold(word: str) -> str:
    out = unicodedata.normalize("NFD", word.lower())
    return "".join(ch for ch in out if unicodedata.category(ch) != "Mn")


# Kostra slova: samotné souhlásky, a ještě sloučené do skupin, které se
# v češtině navzájem střídají. Staročeské „spósob" i „zpósob" tak vyjdou
# stejně jako dnešní „způsob" — a taková podoba slovo prozradí, i když se
# písmenko po písmenku neshoduje ani nezačíná stejně.
VOWELS = set("aeiouy")
CONS_GROUPS = str.maketrans({
    "z": "s", "c": "s",  # sykavky; háčky už sundal fold()
    "d": "t",
    "h": "k", "g": "k",
    "w": "v",
})


def skeleton(word: str) -> str:
    letters = [ch for ch in word if "a" <= ch <= "z"]
    return "".join(ch for ch in letters if ch not in VOWELS).translate(CONS_GROUPS)


def common_prefix(a: str, b: str) -> int:
    n = 0
    while n < len(a) and n < len(b) and a[n] == b[n]:
        n += 1
    return n


def gives_away(token: str, target: str) -> bool:
    """Prozradí tenhle výraz hledané slovo?

    Wikislovník hledané slovo běžně opakuje — ve významovém překladu („z
    praslovanského *město"), v odkazu na příbuzné slovo („souvisí se světlo")
    nebo v rozboru složeniny („pravý + -da"). Nejde o chybu textu, jen se to
    nesmí dostat k hráči.
    """
    if len(token) < 3:
        return False
    if token == target:
        return True
    # Část složeniny nebo naopak celé slovo uvnitř delšího výrazu.
    if len(token) >= 4 and (token in target or target in token):
        return True
    # Stejná souhlásková kostra — pravopisná varianta nebo starší podoba
    # („spósob" vedle „způsob"). Krátké kostry se trefují náhodou, proto tři.
    if len(token) >= 4:
        mine = skeleton(token)
        if len(mine) >= 3 and mine == skeleton(target):
            return True
    # Společný začátek. Čtyři písmena stačí i u delších slov: „psát" u
    # „psaní" nebo „rovnat" u „rovnítka" je kořen, a ten hráči odpověď
    # naservíruje. Pár planých zakrytí je menší škoda než hádanka zadarmo.
    need = min(4, len(target)) if len(target) <= 6 else 4
    if common_prefix(token, target) >= need:
        return True

    # Cizojazyčný protějšek, který vypadá skoro stejně.
    #
    # „Převzato z anglického **hurricane**, jež je odvozeno ze španělského
    # **huracán**" — u hledaného slova hurikán se tím nehádá, jen opisuje.
    # Společný začátek to nechytí (hurr- proti huri-) a souhlásková kostra
    # taky ne, protože se liší uvnitř. Podobnost celých slov ano.
    #
    # Práh 0,70 je vybraný tak, aby prošly příbuzné tvary („rovnat" u
    # rovnítka, 0,71) a neprošla slova, která k odpovědi jen vedou úvahou
    # („dělítko" u rovnítka, 0,53) — ta jsou přesně to, na čem se má hádat.
    if len(token) >= 4 and len(target) >= 4:
        if difflib.SequenceMatcher(None, token, target).ratio() >= 0.70:
            return True

    return False


def compound_parts(tokens: list[str], target: str) -> set[str]:
    """
    Kousky, které dohromady dají hledané slovo.

    „…přeložením předpony über na české **nad-** (s hláskovou obměnou na
    **nád**) a ponecháním původně německého **hêr**" — ani jeden kousek sám
    o sobě nádherný neprozradí, ale poskládat se z nich dá. Samostatně jsou
    přitom příliš krátké na to, aby je zachytilo porovnání celých slov, takže
    se hledají dvojice: začátek slova a jeho zbytek.
    """
    bad: set[str] = set()
    for i, head in enumerate(tokens):
        if len(head) < 3 or not target.startswith(head):
            continue
        rest = target[len(head):]
        if len(rest) < 3:
            continue
        for tail in tokens[i + 1:]:
            if len(tail) >= 3 and common_prefix(tail, rest) >= 3:
                bad.add(head)
                bad.add(tail)
    return bad


def mask(word: str, text: str):
    """Zamaskuje prozrazující výrazy. Vrátí (text, použitelné?)."""
    if COMPOUND_START.search(text.strip()):
        return text, False

    target = fold(word)
    pieces = TOKEN_RE.split(text)
    words = [fold(p.lower()) for p in pieces if p and TOKEN_RE.fullmatch(p)]
    split_up = compound_parts(words, target)
    masks = 0
    out = []
    for piece in pieces:
        low = fold(piece.lower()) if piece else ""
        if piece and TOKEN_RE.fullmatch(piece) and (
            gives_away(low, target) or low in split_up
        ):
            masks += 1
            # Dvě zamaskovaná místa vedle sebe splynou v jedno.
            if out and out[-1] == MASK:
                continue
            out.append(MASK)
        else:
            out.append(piece)
    masked = re.sub(r"\s+", " ", "".join(out)).strip()
    masked = re.sub(r"\s+([,.;])", r"\1", masked)
    # Přepisy výslovnosti stojí v hranatých závorkách („[kybernétikos]"),
    # takže po zakrytí zbude „[[?]]" — což vypadá jako wikitext. Závorka
    # kolem samotné značky nemá co držet.
    masked = re.sub(r"\[\s*" + re.escape(MASK) + r"\s*\]", MASK, masked)

    if masks > MAX_MASKS:
        return masked, False
    # Zamaskované slovo hned v úvodu ubere textu smysl („[?] je z [?]").
    if masked.startswith(MASK):
        return masked, False
    # Bez zakrytých míst musí zbýt pořád dost textu. Jinak z indicie zůstane
    # jen slovníková formulka („Odvozeno od [?].“), na které se hádat nedá.
    rest = masked.replace(MASK, "").strip()
    return masked, len(masked) >= MIN_TEXT and len(rest) >= MIN_TEXT


def tidy(text: str) -> str:
    """Uklidí, co je ve slovníkovém hesle navíc a v hádance to jen mate."""
    text = XREF_PAREN.sub("", text)
    text = REF_NUM.sub("", text)
    text = XREF_TAIL.sub("", text)
    # Po odříznutí ocasu občas zůstane viset spojka nebo čárka.
    text = re.sub(r"[\s,;:]+(?:a|i|nebo|či|ale)?[\s,;:]*$", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    text = re.sub(r"\s+([,.;:])", r"\1", text)
    return text


# Tečka, která nekončí větu.
#
# „na začátku 17. století" má uprostřed tečku za řadovou číslovkou a „resp.
# románské" za zkratkou. Naivní dělení vět po tečce je tam rozsekne a indicie
# pak skončí uprostřed: „…se na začátku 17." Hráč čeká zbytek věty, který
# nikdy nepřijde — a přesně na tohle si stěžoval.
NOT_END = re.compile(
    r"(?:"
    r"\b\d+\."  # řadová číslovka: 17. století, 2. poloviny
    r"|\b(?:tzv|resp|např|srov|př|n|l|st|stol|lat|řec|něm|fr|angl|it|špan"
    r"|psl|stč|sthn|mj|aj|tj|sv|hl|pol|zač|kon)\."  # obvyklé zkratky
    r")$",
    re.IGNORECASE,
)


def sentences_of(text: str) -> list[str]:
    """
    Rozdělí text na věty a nenechá se zmást tečkou uvnitř věty.

    Rozdělí se hrubě po tečce a pak se zpátky slepí kusy, které začínaly
    číslovkou nebo zkratkou — ty žádnou větu neukončily.
    """
    rough = re.split(r"(?<=[.!?])\s+", text)
    out: list[str] = []
    for piece in rough:
        if out and NOT_END.search(out[-1]):
            out[-1] = f"{out[-1]} {piece}"
        else:
            out.append(piece)
    return out


def shorten(text: str) -> str:
    """Celé věty a rozumná délka — hádanka, ne heslo encyklopedie.

    Text se nikdy neuřízne uprostřed věty. Půlka souvětí („…, způsobem
    metafory a odvození pak i kardinální") čtenáře jen zmate; radši kratší
    indicie, která dobíhá do tečky.
    """
    text = text.strip()
    sentences = [s for s in sentences_of(text) if not XREF_START.match(s)]
    out = ""
    for sentence in sentences:
        if out and len(out) + len(sentence) + 1 > MAX_TEXT:
            break
        out = f"{out} {sentence}".strip()

    # První věta sama přes limit: zkusí se useknout na hranici souvětí.
    if len(out) > MAX_TEXT:
        clause = ""
        for piece in re.split(r"(?<=[;])\s+|\s+(?=[—–]\s)", out):
            if clause and len(clause) + len(piece) + 1 > MAX_TEXT:
                break
            clause = f"{clause} {piece}".strip()
        out = clause.rstrip(";").strip()

    # Pojistka: kdyby přes všechno indicie skončila číslovkou nebo zkratkou,
    # radši se zahodí poslední věta, než aby hráč četl nedopsanou myšlenku.
    while out and NOT_END.search(out):
        cut = out.rstrip()
        pieces = sentences_of(cut)
        if len(pieces) <= 1:
            return ""
        out = " ".join(pieces[:-1]).strip()

    # Hesla ve Wikislovníku často tečku na konci nemají. V hádance vypadá
    # text bez tečky useknutě, i když je celý.
    if out and not out.endswith((".", "!", "?")):
        out += "."
    return out


def difficulty(word: str) -> str:
    if len(word) <= 5:
        return "easy"
    return "normal" if len(word) <= 8 else "hard"


def main():
    cache = json.load(open(os.path.join(RAW, "etymology.json"), encoding="utf-8"))
    base = json.load(open(os.path.join(OUT, "lexicon_base.json"), encoding="utf-8"))
    allowed = {w for length in base for w, _ in base[length]}
    freq = {w: f for length in base for w, f in base[length]}

    puzzles = []
    dropped = {"pos": 0, "short": 0, "leak": 0, "mimo slovník": 0}

    for word, entry in cache.items():
        if not entry or not isinstance(entry, dict):
            continue
        if word not in allowed:
            dropped["mimo slovník"] += 1
            continue
        if not (MIN_WORD <= len(word) <= MAX_WORD):
            continue
        if not (set(entry.get("pos") or []) & KEEP_POS):
            dropped["pos"] += 1
            continue
        text = shorten(tidy(entry["e"]))
        if not (MIN_TEXT <= len(text) <= MAX_TEXT):
            dropped["short"] += 1
            continue
        text, usable = mask(word, text)
        if not usable:
            dropped["leak"] += 1
            continue
        puzzles.append(
            {
                "id": f"d-{len(puzzles):04d}",
                "word": word,
                "clue": text,
                "difficulty": difficulty(word),
            }
        )

    # Nejběžnější slova první — snadné úrovně mají být i ta známější.
    puzzles.sort(key=lambda p: -freq.get(p["word"], 0))
    for i, puzzle in enumerate(puzzles):
        puzzle["id"] = f"d-{i:04d}"

    os.makedirs(DATA, exist_ok=True)
    path = os.path.join(DATA, "puzzles.json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(puzzles, fh, ensure_ascii=False)

    print(f"hádanek: {len(puzzles)}")
    for reason, count in dropped.items():
        print(f"  zahozeno ({reason}): {count}")
    for level in ("easy", "normal", "hard"):
        print(f"  {level}: {sum(1 for p in puzzles if p['difficulty'] == level)}")
    print(f"\n-> {os.path.normpath(path)}")


if __name__ == "__main__":
    main()
