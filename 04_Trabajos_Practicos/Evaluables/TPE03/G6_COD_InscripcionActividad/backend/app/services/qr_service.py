from io import BytesIO
import qrcode
from qrcode.exceptions import DataOverflowError
from .comprobantes import contenido_qr

def _crear_qr(inscripcion: dict):
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=4,
    )

    qr.add_data(contenido_qr(inscripcion))
    try:
        qr.make(fit=True)
    except (DataOverflowError, ValueError) as error:
        raise DataOverflowError("El contenido supera la capacidad del QR.") from error
    return qr


def validar_capacidad_qr(inscripcion: dict) -> None:
    _crear_qr(inscripcion)


def generar_qr(inscripcion: dict) -> bytes:
    qr = _crear_qr(inscripcion)

    img = qr.make_image(
        fill_color="black",
        back_color="white"
    )

    buffer = BytesIO()
    img.save(buffer, format="PNG")

    return buffer.getvalue()
