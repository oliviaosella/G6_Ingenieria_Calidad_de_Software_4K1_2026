"""Convert the original Guía GIF loops to Canva-compatible silent MP4 loops."""

from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
ASSETS = ROOT / "04_Trabajos_Practicos/Evaluables/TPE03/G6_COD_InscripcionActividad/frontend/src/assets"
FFMPEG = HERE / ".deps/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe"

# Original GIF, background color matching its slide or activity card.
CLIPS = {
    "parque_slide": ("guia-gifs/parque.gif", "e7f2dc"),
    "safari_slide": ("guia-gifs/safari.gif", "e4f3e2"),
    "safari_card": ("guia-gifs/safari.gif", "b5e6c0"),
    "tirolesa_slide": ("guia-gifs/tirolesa.gif", "e2f2f1"),
    "tirolesa_card": ("guia-gifs/tirolesa.gif", "b2e6ea"),
    "palestra_slide": ("guia-gifs/palestra.gif", "ece9d1"),
    "palestra_card": ("guia-gifs/palestra.gif", "f1d3bf"),
    "jardineria_slide": ("guia-gifs/jardineria.gif", "e8efdb"),
    "jardineria_card": ("guia-gifs/jardineria.gif", "f5e3af"),
    "think_cycle": ("guia-assistant/think.gif", "f2d9b8"),
    "think_anatomy": ("guia-assistant/think.gif", "d8ece4"),
    "point_slide": ("guia-assistant/point.gif", "f8edda"),
    "cheer_slide": ("guia-assistant/cheer.gif", "f7e5d5"),
    "confirmada_slide": ("guia-confirmacion/confirmada.gif", "f2c58f"),
}

for name, (source, color) in CLIPS.items():
    target = HERE / f"motion-{name}.mp4"
    if source.startswith("guia-assistant/"):
        compose = ("[0:v]scale=380:380:flags=lanczos[fg];"
                   "[1:v][fg]overlay=(W-w)/2:(H-h)/2:shortest=1:format=auto,"
                   "format=yuv420p[v]")
    else:
        compose = ("[1:v][0:v]overlay=(W-w)/2:(H-h)/2:shortest=1:format=auto,"
                   "format=yuv420p[v]")
    command = [
        str(FFMPEG), "-hide_banner", "-loglevel", "error", "-y",
        "-ignore_loop", "1", "-i", str(ASSETS / source),
        "-f", "lavfi", "-i", f"color=c=0x{color}:s=400x450:r=12:d=4",
        "-filter_complex", compose,
        "-map", "[v]", "-t", "4", "-c:v", "libx264", "-pix_fmt", "yuv420p",
        "-movflags", "+faststart", str(target),
    ]
    subprocess.run(command, check=True)
    print(name, target.stat().st_size)
