"""Make a looping transparent celebration GIF from Guía's signed artwork."""

from pathlib import Path
from PIL import Image, ImageOps

root = Path(__file__).resolve().parents[1]
source = Image.open(root / "src/assets/guia-confirmacion/confirmada.png").convert("RGBA")
source = ImageOps.contain(source, (348, 438), Image.Resampling.LANCZOS)
size = (380, 470)
frames = []

for dx, dy, degrees in ((0, 12, -2), (2, 4, 0), (0, 0, 2), (-2, 5, 0), (0, 12, -2)):
    figure = source.rotate(degrees, Image.Resampling.BICUBIC, expand=True)
    canvas = Image.new("RGBA", size)
    canvas.alpha_composite(figure, ((size[0] - figure.width) // 2 + dx, 4 + dy))
    indexed = canvas.convert("RGB").quantize(colors=255, method=Image.Quantize.MEDIANCUT)
    indexed.paste(255, mask=canvas.getchannel("A").point(lambda a: 255 if a < 100 else 0))
    frames.append(indexed)

frames[0].save(
    root / "src/assets/guia-confirmacion/confirmada.gif",
    save_all=True,
    append_images=frames[1:],
    duration=(190, 170, 180, 190, 200),
    loop=0,
    disposal=2,
    transparency=255,
    optimize=False,
)
