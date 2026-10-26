import cv2
import numpy as np

from app.services.qr_service import generar_qr


def test_generar_qr_inscripcion_exitosa() -> None:
    # Preparar
    inscripcion = {
        "id": 125,
        "email": "visitante@gmail.com",
        "actividad": "Tirolesa",
        "fecha": "2026-10-20",
        "horario": "14:30"
    }

    # Resultados
    qr = generar_qr(inscripcion)

    # Validar
    assert isinstance(qr, bytes)
    assert qr.startswith(b"\x89PNG\r\n\x1a\n")


def test_qr_contiene_identificador_inscripcion() -> None:
    # Preparar
    inscripcion = {
        "id": 125,
        "email": "visitante@gmail.com",
        "actividad": "Tirolesa",
        "fecha": "2026-10-20",
        "horario": "14:30"
    }

    # Resultados
    qr = generar_qr(inscripcion)

    # Validar
    imagen = cv2.imdecode(
        np.frombuffer(qr, dtype=np.uint8),
        cv2.IMREAD_GRAYSCALE
    )

    assert imagen is not None

    detector = cv2.QRCodeDetector()
    contenido, _, _ = detector.detectAndDecode(imagen)

    assert contenido == "RESERVA-125"


def test_qr_es_diferente_para_cada_inscripcion() -> None:
    # Preparar
    inscripcion_1 = {"id": 125}
    inscripcion_2 = {"id": 250}

    # Resultados
    qr_1 = generar_qr(inscripcion_1)
    qr_2 = generar_qr(inscripcion_2)

    # Validar
    assert qr_1 != qr_2
