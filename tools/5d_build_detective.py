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


# Souhlásky sloučené podle toho, jak znějí. Pravopis se mezi jazyky liší,
# výslovnost o moc míň — a hráč slovo pozná sluchem, ne písmenkem.
SOUND = {
    "b": "P", "p": "P",
    "d": "T", "t": "T",
    "v": "F", "w": "F", "f": "F",
    "g": "K", "h": "K", "k": "K", "c": "K", "q": "K", "x": "K",
    "s": "S", "z": "S",
    "m": "M", "n": "N", "r": "R", "l": "L",
    # j a y jsou v přejímkách jen výplň („majlant" proti „Mailand")
    "j": "", "y": "",
}


def phonetic(word: str) -> str:
    """
    Jak slovo zhruba zní — jen souhlásky, sloučené do znělostních dvojic.

    Tohle je jádro celé kontroly. Etymologický text ze své podstaty mluví
    o slově, ze kterého to hledané vzniklo, takže si budou vždycky podobná.
    Porovnávat pravopis nestačí: „souterrain" a „suterén" mají společné jen
    první písmeno, „Mailand" a „majlant" dvě — a přesto je hráč přečte jako
    totéž slovo, protože stejně znějí. Po převodu na SRTN a MLNT je to vidět.
    """
    plain = re.sub(r"[^a-z]", "", fold(word))
    plain = re.sub(r"(.)\1+", r"\1", plain)
    # Spřežky se přepíšou na jedno písmeno, které je pak vidět v tabulce
    # níž. Musí zůstat malé: velké písmeno by v ní nikdo nenašel a tiše by
    # vypadlo — „sarcophagus" pak vycházelo SRKS místo SRKFKS a s hledaným
    # sarkofágem se nepotkalo.
    # „qu" se v latině čte kv, proto dvě písmena.
    for pair, sound in (("qu", "kv"), ("ch", "k"), ("th", "t"), ("ph", "f"), ("ck", "k")):
        plain = plain.replace(pair, sound)
    out = "".join(SOUND.get(ch, "") for ch in plain)
    return re.sub(r"(.)\1+", r"\1", out)


def longest_shared(a: str, b: str) -> int:
    """Nejdelší souvislý úsek, který mají obě slova společný."""
    best = 0
    for i in range(len(a)):
        for j in range(len(b)):
            run = 0
            while i + run < len(a) and j + run < len(b) and a[i + run] == b[j + run]:
                run += 1
            best = max(best, run)
    return best


def edits(a: str, b: str) -> int:
    """Kolik písmen se liší (vložení, smazání, záměna)."""
    if a == b:
        return 0
    previous = list(range(len(b) + 1))
    for i, left in enumerate(a, 1):
        current = [i]
        for j, right in enumerate(b, 1):
            current.append(
                min(previous[j] + 1, current[j - 1] + 1, previous[j - 1] + (left != right))
            )
        previous = current
    return previous[-1]


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
    shared_head = common_prefix(token, target)
    if shared_head >= need:
        return True

    # Kratší společný začátek, ale u krátkého slova.
    #
    # „ženský" se hádá a v textu stojí „žena", „olej" a v textu „oleum" —
    # tři písmena, jenže tvoří skoro celé to slovo, takže je to kořen se vším
    # všudy. Proti tomu „prostitutka" a „prodávat" mají taky tři, ale jen
    # zlomek slova; tam je to náhoda a zakrývat by se nemělo.
    if shared_head >= 3 and shared_head >= 0.5 * min(len(token), len(target)):
        return True

    # Cizojazyčný protějšek, který vypadá skoro stejně.
    if len(token) >= 4 and len(target) >= 4:
        if difflib.SequenceMatcher(None, token, target).ratio() >= 0.70:
            return True

    # Společný kus uprostřed slova.
    #
    # „Pochází ze slova [?], protože je **uprostřed** týdne" u středy nebo
    # „z latinského **hapsis**" u apsidy — kořen tam je, jen není na začátku,
    # takže ho porovnání předpon minulo. Hlídá se souvislý úsek čtyř písmen,
    # ale jen když sedí na začátek odpovědi nebo tvoří její většinu: „-ítko"
    # sdílí dělítko s rovnítkem taky, a to je přesně ta úvaha, na které se má
    # hádat, ne prozrazení.
    if len(target) >= 5:
        shared = longest_shared(token, target)
        if shared >= 4:
            head = any(
                target.startswith(token[i:i + shared]) for i in range(len(token) - shared + 1)
            )
            if head or shared >= 0.6 * len(target):
                return True

    # A nakonec to hlavní: **zní to stejně?**
    #
    # Porovnávání pravopisu se dá obejít donekonečna — „souterrain" má se
    # „suterénem" společné jediné písmeno, „Mailand" s „majlantem" dvě, a hráč
    # přesto obojí přečte jako odpověď. Etymologický text totiž ze své
    # podstaty mluví o slově, ze kterého to hledané vzniklo; hláskovat se to
    # může jakkoli, znít to bude pořád stejně.
    #
    # Jedno písmeno rozdílu se odpouští kvůli koncovkám („factum" proti
    # „fakt"). Krátké kostry se trefují náhodou, proto se hlídají až od dvou
    # souhlásek.
    mine, yours = phonetic(token), phonetic(target)
    if len(yours) >= 2 and len(mine) >= 2 and edits(mine, yours) <= 1:
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


# Slova, kterými etymologické heslo jen drží větu pohromadě. Nesou stavbu
# výkladu, ne informaci o hledaném slově — „odvozeno od substantiva pomocí
# předpony" platí pro tisíce slov stejně.
FILLER = set(
    """odvozeno odvozene odvozeneho odvozena odvozeny odvozenim utvoreno utvorena
    utvoreny vzniklo vznikla vznikl vznik pochazi prejato prevzato prejaty prejate
    pres pomoci predpony predpona pripony pripona pripon koncovky substantiva
    substantivum substantivem adjektiva adjektivum adjektivem slovesa sloveso slovem
    slova slovo tvaru tvar tvary korene koren zakladu zaklad zakladem jazyka jazyky
    jazyk vyznamu vyznam vyznamem tehoz stejneho stejnym dolozeno poprve patrne
    pravdepodobne zrejme nejspis snad dale take tedy dnes puvodne puvodni puvodniho
    novejsi starsi tvarem varianta prechylenim podstatneho jmena pricesti pritomne
    minule trpne slovotvornemu slovotvorneho ktery ktera ktere kterym jehoz jejiz
    coz jako toto tento tato temer velmi""".split()
)


def informative(masked: str) -> bool:
    """
    Zbylo po zakrytí ještě něco, z čeho se dá vyjít?

    „Odvozeno od substantiva [?] pomocí předpony [?]-." má přes čtyřicet
    znaků, takže délková podmínka projde — jenže neříká vůbec nic. Sedí na
    stovky slov a hráč z ní nemá co vytěžit. Délka je špatné měřítko;
    rozhoduje, kolik zůstalo slov, která opravdu něco tvrdí.

    Tři jsou minimum: jazyk původu, doba a význam. S méně už je to hádání
    z ničeho.
    """
    plain = masked.replace(MASK, " ")
    words = [w for w in TOKEN_RE.findall(plain) if len(fold(w)) >= 4]
    return sum(1 for w in words if fold(w) not in FILLER) >= 3


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
    if len(masked) < MIN_TEXT or len(rest) < MIN_TEXT:
        return masked, False
    return masked, informative(masked)


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


def frequency_ranks() -> dict[str, int]:
    """
    Pořadí slov podle toho, jak často se v češtině používají.

    Bere se z frekvenčního seznamu staženého krokem 0. Když chybí, vrátí se
    prázdná mapa a obtížnost spadne zpátky na délku — hra se kvůli tomu
    nepostaví hůř, jen hruběji.
    """
    ranks: dict[str, int] = {}
    for name in ("cs_50k.txt", "cs_full.txt"):
        path = os.path.join(RAW, name)
        if not os.path.exists(path):
            continue
        with open(path, encoding="utf-8") as handle:
            for order, line in enumerate(handle):
                parts = line.split()
                if parts:
                    ranks.setdefault(fold(parts[0]), order)
        break
    return ranks


def assign_difficulty(puzzles: list[dict], ranks: dict[str, int]) -> None:
    """
    Rozdělí hádanky na třetiny podle toho, jak běžné to slovo je.

    Délka byla špatné měřítko a bylo to na hře vidět: mezi „těžkými" seděla
    *univerzita*, *absolutní* a *kreativní*, tedy slova, která zná každý,
    zatímco *rožeň* platil za lehký, protože je krátký. Hráč si vybral těžkou
    obtížnost a dostal dlouhé banality.

    Dělí se **podle pořadí, ne podle prahu**. Většina hesel Wikislovníku ve
    frekvenčním seznamu vůbec není — jsou vzácnější než cokoli na něm — a
    prahová hranice by pak spadla na tuhle společnou hodnotu a shrnula skoro
    celou sadu do jedné úrovně. U slov mimo seznam rozhoduje ještě délka:
    z dvou stejně neznámých je těžší to delší.
    """
    missing = len(ranks) + 1
    order = sorted(
        puzzles,
        key=lambda p: (ranks.get(fold(p["word"]), missing), len(p["word"])),
    )
    third = max(1, len(order) // 3)
    for place, puzzle in enumerate(order):
        puzzle["difficulty"] = (
            "easy" if place < third else "normal" if place < 2 * third else "hard"
        )


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
                "difficulty": None,  # doplní se, až bude znám rozsah sady
            }
        )

    # Obtížnost se rozdělí až teď, kdy je vidět celá sada.
    assign_difficulty(puzzles, frequency_ranks())

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
