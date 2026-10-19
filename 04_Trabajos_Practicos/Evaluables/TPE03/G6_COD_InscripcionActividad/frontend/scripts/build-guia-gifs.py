"""Export looping previews from Guía's four transparent PNG frames per theme."""

from pathlib import Path
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]
FRAMES = ROOT / "src" / "assets" / "guia-frames"
OUTPUT = ROOT / "src" / "assets" / "guia-gifs"
THEMES = ("parque", "safari", "tirolesa", "palestra", "jardineria")
SIZE = (320, 360)


def gif_frame(path: Path) -> Image.Image:
    image = Image.open(path).convert("RGBA")
    image = ImageOps.contain(image, SIZE, Image.Resampling.LANCZOS)
    canvas = Image.new("RGBA", SIZE)
    canvas.alpha_composite(image, ((SIZE[0] - image.width) // 2, (SIZE[1] - image.height) // 2))

    # GIF supports one transparent palette entry. Keep it unused by opaque colors.
    palette_frame = canvas.convert("RGB").quantize(colors=255, method=Image.Quantize.MEDIANCUT)
    transparent_pixels = canvas.getchannel("A").point(lambda alpha: 255 if alpha < 100 else 0)
    palette_frame.paste(255, mask=transparent_pixels)
    return palette_frame


OUTPUT.mkdir(parents=True, exist_ok=True)
for theme in THEMES:
    frames = [gif_frame(FRAMES / f"{theme}-{index}.png") for index in range(4)]
    frames[0].save(
        OUTPUT / f"{theme}.gif",
        save_all=True,
        append_images=frames[1:],
        duration=(900, 900, 900, 900),
        loop=0,
        disposal=2,
        transparency=255,
        optimize=False,
    )
    print(OUTPUT / f"{theme}.gif")
