"""Make a Canva-compatible copy of one original Guía GIF for upload testing."""

from pathlib import Path
from PIL import Image

root = Path(__file__).resolve().parents[1]
src = root / "04_Trabajos_Practicos/Evaluables/TPE03/G6_COD_InscripcionActividad/frontend/src/assets/guia-assistant/wave.gif"
dest = Path(__file__).resolve().parent / "guia-wave-canva.gif"

with Image.open(src) as image:
    frames = []
    durations = []
    for index in range(image.n_frames):
        image.seek(index)
        frame = image.convert("RGBA")
        background = Image.new("RGBA", frame.size, "#fff8e8")
        background.alpha_composite(frame)
        frames.append(background.convert("RGB").quantize(colors=128))
        durations.append(image.info.get("duration", 300))
    frames[0].save(dest, save_all=True, append_images=frames[1:], duration=durations,
                   loop=0, optimize=True)

print(dest, dest.stat().st_size)
