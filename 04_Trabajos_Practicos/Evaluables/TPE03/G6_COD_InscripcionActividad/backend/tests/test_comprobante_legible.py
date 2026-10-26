import cv2
import numpy as np

from app.services.comprobantes import contenido_qr
from app.services.email_service import preparar_resumen
from app.services.qr_service import generar_qr


def test_qr_muestra_comprobante_legible_con_la_misma_informacion_del_correo():
    inscripcion = {
        "id": 2, "actividad": "Safari", "fecha": "2026-10-27", "horario": "09:00",
        "email": "visitante@example.com",
        "participantes": [
            {"nombre": "Ana Pérez", "dni": "12345678", "edad": 25},
            {"nombre": "Luis Gómez", "dni": "23456789", "edad": 12, "talle_vestimenta": "M"},
        ],
    }
    texto = contenido_qr(inscripcion)
    assert texto.startswith("ECO HARMONY PARK\n")
    assert "COMPROBANTE DE INSCRIPCIÓN" in texto
    assert "Código: RESERVA-2\n" in texto
    assert "Número de inscripción: 2\n" in texto
    assert "Actividad: Safari\n" in texto
    assert "Fecha: 2026-10-27\n" in texto
    assert "Horario: 09:00" in texto
    assert "Correo: visitante@example.com\n" in texto
    assert "PARTICIPANTES (2)\n" in texto
    assert "1. Ana Pérez\n   DNI: 12345678\n   Edad: 25" in texto
    assert "2. Luis Gómez\n   DNI: 23456789\n   Edad: 12\n   Talle de vestimenta: M" in texto
    assert '"participantes"' not in texto
    assert preparar_resumen(inscripcion) == texto
    png = generar_qr(inscripcion)
    imagen = cv2.imdecode(np.frombuffer(png, dtype=np.uint8), cv2.IMREAD_GRAYSCALE)
    decodificado, _, _ = cv2.QRCodeDetector().detectAndDecode(imagen)
    assert decodificado == texto
