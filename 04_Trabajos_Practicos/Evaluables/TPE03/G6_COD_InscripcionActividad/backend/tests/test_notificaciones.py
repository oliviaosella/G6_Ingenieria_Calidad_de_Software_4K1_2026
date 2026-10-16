from app.services.email_service import (
    preparar_resumen, 
    enviar_confirmacion,
    ServicioNotificaciones
)


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
            "talla_vestimenta": None
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
    assert "María" in resumen
    assert "Gómez" in resumen
    assert "87654321" in resumen


def test_resumen_actividad_requiere_vestimenta() -> None:
    # TODO: Implementar test para verificar que el resumen de la inscripcion incluya información sobre la vestimenta si la actividad lo requería.
    pass


def test_enviar_confirmacion_al_correo_del_visitante_EXITO() -> None:
    #Preparar
    inscripcion = {
        "id": 125,
        "email": "visitante@gmail.com",
        "actividad": "Tirolesa",
        "fecha": "2026-10-20",
        "horario": "14:30"
    }

    #Resultados
    resultado = enviar_confirmacion(inscripcion)

    #Validar
    assert inscripcion['email'] in resultado


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
