"""Krok 6 — ikony aplikace.

Vygeneruje sadu ikon pro PWA (a tím i pro balíček do Google Play přes TWA).
Kromě běžných ikon vzniknou i „maskable" varianty, u kterých si systém může
oříznout rohy do libovolného tvaru — obsah proto musí zůstat v bezpečné zóně
uprostřed.

Motiv je vzatý přímo ze značky ve hře: prostřední „O" ve slově SLOVA je terč
a vedle názvu svítí tři tečky, jedna za každou hru. Ikona z toho dělá jeden
znak — kroužek složený ze tří stejných oblouků v barvách Řetězu, Voštiny
a Věže, uprostřed světlý bod. Na ploše telefonu je poznat i v 48 px a nese
přitom informaci: tři hry v jedné.
"""

import os

from PIL import Image, ImageDraw, ImageFilter

ROOT = os.path.join(os.path.dirname(__file__), "..")
OUT = os.path.join(ROOT, "public", "icons")

# Barvy značky — stejné hodnoty jako v src/styles/tokens.css.
INK = (18, 16, 44)
CHAIN = (91, 61, 245)
HIVE = (217, 135, 4)
TOWER = (226, 58, 46)
PAPER = (255, 255, 255)

# Maskable ikona musí počítat s oříznutím: bezpečná zóna je vnitřních 80 %.
MASKABLE_SCALE = 0.66
PLAIN_SCALE = 0.84

# Kreslí se čtyřnásobně a pak zmenší — hrany oblouků jsou pak hladké.
SS = 4


def rounded_mask(size: int, radius_ratio: float) -> Image.Image:
    mask = Image.new("L", (size * SS, size * SS), 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle(
        (0, 0, size * SS - 1, size * SS - 1),
        radius=int(size * SS * radius_ratio),
        fill=255,
    )
    return mask.resize((size, size), Image.LANCZOS)


def draw_icon(size: int, maskable: bool) -> Image.Image:
    big = size * SS
    plate = Image.new("RGBA", (big, big), INK + (255,))
    draw = ImageDraw.Draw(plate)

    # Rozostřené světlo vlevo nahoře, aby plocha nebyla placatá. Bez rozmazání
    # by z elipsy zůstala ostrá hrana přes celou ikonu.
    glow = Image.new("RGBA", (big, big), (0, 0, 0, 0))
    ImageDraw.Draw(glow).ellipse(
        (-big * 0.25, -big * 0.45, big * 0.8, big * 0.6), fill=CHAIN + (86,)
    )
    plate.alpha_composite(glow.filter(ImageFilter.GaussianBlur(big * 0.11)))

    scale = MASKABLE_SCALE if maskable else PLAIN_SCALE
    radius = big * 0.30 * scale
    width = int(big * 0.115 * scale)
    box = (
        big / 2 - radius,
        big / 2 - radius,
        big / 2 + radius,
        big / 2 + radius,
    )

    # Tři stejné oblouky = tři hry. Začínají nahoře a jdou po směru hodin.
    for index, color in enumerate((CHAIN, HIVE, TOWER)):
        start = -90 + index * 120 + 4
        draw.arc(box, start, start + 112, fill=color, width=width)

    # Terč uprostřed — stejný motiv jako „O" ve slově SLOVA.
    dot = radius * 0.34
    draw.ellipse(
        (big / 2 - dot, big / 2 - dot, big / 2 + dot, big / 2 + dot), fill=PAPER
    )

    image = plate.resize((size, size), Image.LANCZOS)
    if maskable:
        return image
    out = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    out.paste(image, (0, 0), rounded_mask(size, 0.22))
    return out


def mono_icon(size):
    """
    Jednobarevná ikona pro témata Androidu.

    Android 13 a novější si ikonu přebarvuje podle tapety — dostane jen tvar
    a barvu si dodá sám. Barevná ikona se pro to nedá použít: systém z ní udělá
    beztvarou placku. Kreslí se proto bílý tvar na průhledném pozadí a v téže
    bezpečné zóně jako maskable, protože i tuhle ikonu systém ořezává.
    """
    big = size * 4
    image = Image.new("RGBA", (big, big), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)

    radius = big * MASKABLE_SCALE / 2
    width = int(radius * 0.42)
    box = (
        big / 2 - radius,
        big / 2 - radius,
        big / 2 + radius,
        big / 2 + radius,
    )
    # Týž prstenec ze tří oblouků jako v barevné ikoně, jen jednou barvou.
    for index in range(3):
        start = -90 + index * 120 + 4
        draw.arc(box, start, start + 112, fill=PAPER, width=width)

    dot = radius * 0.34
    draw.ellipse(
        (big / 2 - dot, big / 2 - dot, big / 2 + dot, big / 2 + dot), fill=PAPER
    )
    return image.resize((size, size), Image.LANCZOS)


def main():
    os.makedirs(OUT, exist_ok=True)
    made = []
    for size in (192, 512):
        for maskable in (False, True):
            name = f"icon-maskable-{size}.png" if maskable else f"icon-{size}.png"
            draw_icon(size, maskable).save(os.path.join(OUT, name))
            made.append(name)

    # Jednobarevná varianta pro témata Androidu.
    mono_icon(512).save(os.path.join(OUT, "icon-mono-512.png"))
    made.append("icon-mono-512.png")

    # Ikona do obchodu. Google Play si rohy zaobluje sám a průhlednost nechce:
    # ikona s vlastními zaoblenými rohy se v obchodě zaoblí podruhé a vzniknou
    # z toho okousané okraje. Do obchodu proto jde plný čtverec bez průhlednosti.
    store_dir = os.path.join(ROOT, "play")
    os.makedirs(store_dir, exist_ok=True)
    store = Image.new("RGB", (512, 512), INK)
    store.paste(draw_icon(512, True), (0, 0), draw_icon(512, True))
    store.save(os.path.join(store_dir, "icon-512-store.png"))
    print("  play/icon-512-store.png")

    # Apple touch icon nesmí být průhledná ani zaoblená — iOS si ji zaoblí sám.
    apple = Image.new("RGB", (180, 180), INK)
    apple.paste(draw_icon(180, True).convert("RGB"), (0, 0))
    apple.save(os.path.join(OUT, "apple-touch-icon.png"))
    made.append("apple-touch-icon.png")

    for name in made:
        path = os.path.join(OUT, name)
        print(f"  {name}  {os.path.getsize(path) // 1024} kB")


if __name__ == "__main__":
    main()
