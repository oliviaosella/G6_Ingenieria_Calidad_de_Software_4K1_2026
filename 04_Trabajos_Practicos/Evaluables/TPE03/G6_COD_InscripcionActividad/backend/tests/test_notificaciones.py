from app.services.email_service import (
    preparar_resumen,
    enviar_confirmacion,
    ServicioNotificaciones
)

from app.services.qr_service import generar_qr


def test_resumen_contiene_identificador_inscripcion_EXITO() -> None:
    #Preparar
    inscripcion = {
        "id": 125,
        "email": "visitante@gmail.com",
        "actividad": "Tirolesa",
        "fecha": "2026-10-20",
        "horario": "14:30"
    }

    # Resultados
    resumen = preparar_resumen(inscripcion)
    
    # Validar
    assert "125" in resumen


def test_resumen_contiene_actividad_inscripcion() -> None:
    # ARRANGE
    inscripcion = {
        "id": 125,
        "email": "visitante@gmail.com",
        "actividad": "Tirolesa",
        "fecha": "2026-10-20",
        "horario": "14:30"
    }

    # ACT
    resumen = preparar_resumen(inscripcion)

    # ASSERT
    assert "Tirolesa" in resumen


def test_resumen_contiene_datos_inscripcion() -> None:
    # Preparar
    inscripcion = {
        "id": 125,
        "email": "visitante@gmail.com",
        "actividad": "Tirolesa",
        "fecha": "2026-10-20",
        "horario": "14:30",
        "cantidad_participantes": 2,
        "participantes": [{
            "nombre": "Juan",
            "apellido": "Pérez",
            "dni": "12345678",
            "edad": 25,
            "talla_vestimenta": "M"
        },
        {
            "nombre": "María",
            "apellido": "Gómez",
            "dni": "87654321",
            "talla_vestimenta": None
        }
        ]

    }

    # Resultados
    resumen = preparar_resumen(inscripcion)

    # Validar
    assert "125" in resumen
    assert "Tirolesa" in resumen
    assert "2026-10-20" in resumen
    assert "14:30" in resumen
    assert "Juan" in resumen
    assert "Pérez" in resumen
    assert "12345678" in resumen
    assert "1. Juan Pérez" in resumen
    assert "Edad: 25" in resumen
    assert "Talle de vestimenta: M" in resumen
    assert "María" in resumen
    assert "Gómez" in resumen
    assert "87654321" in resumen
    assert "2. María Gómez" in resumen
    assert "{'nombre':" not in resumen


def test_resumen_indica_cuando_no_hay_participantes() -> None:
    inscripcion = {
        "id": 125,
        "actividad": "Tirolesa",
        "fecha": "2026-10-20",
        "horario": "14:30",
        "participantes": [],
    }

    resumen = preparar_resumen(inscripcion)

    assert "PARTICIPANTES (0)" in resumen
    assert "No se informaron participantes." in resumen


class CorreoFalso:
    def __init__(self) -> None:
        self.envios = []

    def enviar(
        self,
        destinatario: str,
        asunto: str,
        contenido: str,
        qr: bytes
    ) -> None:
        self.envios.append({
            "destinatario": destinatario,
            "asunto": asunto,
            "contenido": contenido,
            "qr": qr
        })


def test_confirmacion_se_envia_al_visitante() -> None:
    # ARRANGE
    inscripcion = {
        "id": 125,
        "email": "visitante@gmail.com",
        "actividad": "Tirolesa",
        "fecha": "2026-10-20",
        "horario": "14:30"
    }

    correo_falso = CorreoFalso()

    servicio = ServicioNotificaciones(
        emisor_correo=correo_falso
    )

    # ACT
    servicio.enviar_confirmacion(inscripcion)

    # ASSERT
    assert len(correo_falso.envios) == 1
    assert correo_falso.envios[0]["destinatario"] == (
        "visitante@gmail.com"
    )


def test_correo_contiene_resumen_inscripcion() -> None:
    # ARRANGE
    inscripcion = {
        "id": 125,
        "email": "visitante@gmail.com",
        "actividad": "Tirolesa",
        "fecha": "2026-10-20",
        "horario": "14:30"
    }

    correo_falso = CorreoFalso()
    servicio = ServicioNotificaciones(emisor_correo=correo_falso)

    # ACT
    servicio.enviar_confirmacion(inscripcion)

    # ASSERT
    assert len(correo_falso.envios) == 1
    contenido = correo_falso.envios[0]["contenido"]
    assert "125" in contenido
    assert "Tirolesa" in contenido
    assert "2026-10-20" in contenido
    assert "14:30" in contenido


def test_correo_incluye_qr_inscripcion() -> None:
    # ARRANGE
    inscripcion = {
        "id": 125,
        "email": "visitante@gmail.com",
        "actividad": "Tirolesa",
        "fecha": "2026-10-20",
        "horario": "14:30"
    }

    correo_falso = CorreoFalso()
    servicio = ServicioNotificaciones(emisor_correo=correo_falso)

    # ACT
    servicio.enviar_confirmacion(inscripcion)

    # ASSERT
    assert len(correo_falso.envios) == 1
    qr_enviado = correo_falso.envios[0]["qr"]
    assert qr_enviado != b""
    assert qr_enviado == generar_qr(inscripcion)