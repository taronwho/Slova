"""Krok 6 — ikony aplikace.

Vygeneruje sadu ikon pro PWA (a tím i pro balíček do Google Play přes TWA).
Kromě běžných ikon vzniknou i „maskable" varianty, u kterých si systém může
oříznout rohy do libovolného tvaru — obsah proto musí zůstat v bezpečné zóně
uprostřed, jinak Android ustřihne půl písmene.

Písmo se bere z Outfitu, který používá i samotná hra, aby ikona seděla
se značkou.
"""

import os

from fontTools.ttLib import TTFont
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.join(os.path.dirname(__file__), "..")
OUT = os.path.join(ROOT, "public", "icons")
WOFF2 = os.path.join(
    ROOT, "node_modules", "@fontsource-variable", "outfit", "files",
    "outfit-latin-wght-normal.woff2",
)
TTF = os.path.join(OUT, ".outfit.ttf")

GREEN = (15, 169, 104)
PAPER = (250, 250, 247)

# Maskable ikona musí počítat s oříznutím: bezpečná zóna je vnitřních 80 %.
MASKABLE_SAFE = 0.62
PLAIN_SAFE = 0.78


def ensure_font() -> str:
    os.makedirs(OUT, exist_ok=True)
    if not os.path.exists(TTF):
        font = TTFont(WOFF2)
        font.flavor = None
        font.save(TTF)
    return TTF


def rounded_mask(size: int, radius_ratio: float) -> Image.Image:
    mask = Image.new("L", (size * 4, size * 4), 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle(
        (0, 0, size * 4 - 1, size * 4 - 1),
        radius=int(size * 4 * radius_ratio),
        fill=255,
    )
    return mask.resize((size, size), Image.LANCZOS)


def draw_icon(size: int, maskable: bool) -> Image.Image:
    path = ensure_font()
    image = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)

    if maskable:
        # Plná plocha — ořez si systém udělá sám.
        draw.rectangle((0, 0, size, size), fill=GREEN)
        glyph_ratio = MASKABLE_SAFE
    else:
        plate = Image.new("RGBA", (size, size), GREEN + (255,))
        image.paste(plate, (0, 0), rounded_mask(size, 0.22))
        draw = ImageDraw.Draw(image)
        glyph_ratio = PLAIN_SAFE

    font = ImageFont.truetype(path, int(size * glyph_ratio))
    # Outfit je variabilní font a bez nastavení osy by se vykreslil v základní
    # váze — na ikonu příliš tenké. Značka používá 700.
    try:
        font.set_variation_by_axes([700])
    except (OSError, AttributeError):
        pass

    box = draw.textbbox((0, 0), "S", font=font)
    x = (size - (box[2] - box[0])) / 2 - box[0]
    y = (size - (box[3] - box[1])) / 2 - box[1]
    draw.text((x, y), "S", font=font, fill=PAPER)
    return image


def main():
    os.makedirs(OUT, exist_ok=True)
    made = []
    for size in (192, 512):
        for maskable in (False, True):
            name = f"icon-maskable-{size}.png" if maskable else f"icon-{size}.png"
            draw_icon(size, maskable).save(os.path.join(OUT, name))
            made.append(name)

    # Apple touch icon nesmí být průhledná ani zaoblená — iOS si ji zaoblí sám.
    apple = Image.new("RGB", (180, 180), GREEN)
    apple.paste(draw_icon(180, True).convert("RGB"), (0, 0))
    apple.save(os.path.join(OUT, "apple-touch-icon.png"))
    made.append("apple-touch-icon.png")

    if os.path.exists(TTF):
        os.remove(TTF)

    for name in made:
        path = os.path.join(OUT, name)
        print(f"  {name}  {os.path.getsize(path) // 1024} kB")


if __name__ == "__main__":
    main()
