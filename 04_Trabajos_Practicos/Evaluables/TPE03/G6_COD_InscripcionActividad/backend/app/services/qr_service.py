# app/qr.py
from io import BytesIO

import qrcode


def generar_qr(url: str) -> bytes:
    imagen = qrcode.make(url)
    salida = BytesIO()
    imagen.save(salida, format="PNG")
    return salida.getvalue()