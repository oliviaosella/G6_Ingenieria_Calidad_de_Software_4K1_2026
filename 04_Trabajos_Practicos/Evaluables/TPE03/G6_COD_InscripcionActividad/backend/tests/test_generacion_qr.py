# tests/test_qr.py
from io import BytesIO

from PIL import Image

from app.services.qr_service import generar_qr


def test_genera_qr_png_con_la_url_de_validacion():
    url = "https://ecoharmony.example/inscripciones/125/validacion"

    resultado = generar_qr(url)

    assert resultado.startswith(b"\x89PNG\r\n\x1a\n")

    imagen = Image.open(BytesIO(resultado))
    assert imagen.format == "PNG"
    assert imagen.size[0] > 0
    assert imagen.size[1] > 0