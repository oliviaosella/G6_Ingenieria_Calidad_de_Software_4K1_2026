"""Generate the four tiny desktop-helper motions from their transparent art."""

from pathlib import Path
from PIL import Image, ImageOps

root = Path(__file__).resolve().parents[1] / "src/assets/guia-assistant"
size = (180, 180)
motions = {
    "wave": [(0, 8, -5), (0, 3, 3), (0, 6, -5), (0, 1, 5), (0, 8, -5)],
    "point": [(4, 7, 2), (-2, 5, -2), (-7, 4, -6), (-2, 5, -2), (4, 7, 2)],
    "think": [(0, 5, -3), (0, 1, 0), (0, 3, 3), (0, 1, 0), (0, 5, -3)],
    "cheer": [(0, 10, -3), (0, 0, 0), (0, -10, 3), (0, 0, 0), (0, 10, -3)],
}

for name, movements in motions.items():
    source = Image.open(root / f"{name}.png").convert("RGBA")
    source = ImageOps.contain(source, (160, 160), Image.Resampling.LANCZOS)
    frames = []
    for dx, dy, angle in movements:
        figure = source.rotate(angle, Image.Resampling.BICUBIC, expand=True)
        canvas = Image.new("RGBA", size)
        canvas.alpha_composite(figure, ((size[0] - figure.width) // 2 + dx, (size[1] - figure.height) // 2 + dy))
        indexed = canvas.convert("RGB").quantize(colors=255, method=Image.Quantize.MEDIANCUT)
        indexed.paste(255, mask=canvas.getchannel("A").point(lambda alpha: 255 if alpha < 100 else 0))
        frames.append(indexed)
    frames[0].save(
        root / f"{name}.gif",
        save_all=True,
        append_images=frames[1:],
        duration=(240, 190, 230, 190, 240),
        loop=0,
        disposal=2,
        transparency=255,
        optimize=False,
    )
