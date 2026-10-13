
from app.schemas import InscripcionConfirmada, Participante
from app.services.notificacion_service import NotificacionService


class FakeQrGenerator:
    def __init__(self) -> None:
        self.inscripcion_id = None

    def generar(self, inscripcion_id: int) -> bytes:
        self.inscripcion_id = inscripcion_id
        return b"imagen_qr_ficticia"


class FakeEmailSender:
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


def test_enviar_confirmacion_exitosa() -> None:
    # ARRANGE: preparar datos de prueba
    inscripcion = InscripcionConfirmada(
        inscripcion_id=125,
        email="visitante@gmail.com",
        actividad="Tirolesa",
        fecha="2026-10-20",
        horario="14:30",
        participantes=[
            Participante(
                nombre="Ana Pérez",
                dni="12345678"
            )
        ]
    )

    qr_generator = FakeQrGenerator()
    email_sender = FakeEmailSender()

    servicio = NotificacionService(
        qr_generator=qr_generator,
        email_sender=email_sender
    )

    # ACT: ejecutar la funcionalidad
    resultado = servicio.enviar_confirmacion(inscripcion)

    # ASSERT: verificar el comportamiento
    assert resultado.estado == "enviado"
    assert qr_generator.inscripcion_id == 125
    assert len(email_sender.envios) == 1
    assert email_sender.envios[0]["destinatario"] == (
        "visitante@gmail.com"
    )
