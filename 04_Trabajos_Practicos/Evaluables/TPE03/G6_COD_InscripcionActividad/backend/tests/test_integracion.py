from app.services.email_service import ServicioNotificaciones
from app.services.reservas import GestorReservas


class CorreoDePrueba:
    def __init__(self):
        self.envios = []

    def enviar(self, destinatario, asunto, contenido, qr):
        self.envios.append({"destinatario": destinatario, "asunto": asunto, "contenido": contenido, "qr": qr})


def test_reserva_exitosa_genera_confirmacion_con_qr():
    gestor = GestorReservas()
    correo = CorreoDePrueba()
    notificaciones = ServicioNotificaciones(correo)

    reserva = gestor.crear_reserva(
        actividad="Tirolesa",
        horario_id=1,
        participantes=[{"nombre": "Ana", "apellido": "Pérez", "dni": "12345678", "edad": 25}],
    )
    reserva.update({"email": "ana@example.com", "fecha": "2026-10-26", "horario": "14:30"})

    notificaciones.enviar_confirmacion(reserva)

    assert gestor.consultar_cupos("Tirolesa", 1) == 9
    assert len(correo.envios) == 1
    assert correo.envios[0]["destinatario"] == "ana@example.com"
    assert "Tirolesa" in correo.envios[0]["contenido"]
    assert correo.envios[0]["qr"].startswith(b"\x89PNG\r\n\x1a\n")


def test_reserva_rechazada_no_genera_confirmacion():
    gestor = GestorReservas()
    correo = CorreoDePrueba()
    notificaciones = ServicioNotificaciones(correo)
    participantes = [{"nombre": f"Persona {i}", "dni": str(i), "edad": 20} for i in range(11)]

    reserva = gestor.crear_reserva("Tirolesa", 1, participantes)

    assert reserva is None
    assert gestor.consultar_cupos("Tirolesa", 1) == 10
    assert correo.envios == []
