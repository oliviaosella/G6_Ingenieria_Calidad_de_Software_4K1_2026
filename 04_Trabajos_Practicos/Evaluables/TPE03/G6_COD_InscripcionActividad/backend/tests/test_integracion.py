import pytest

from app.errors import (
    AceptacionDeOtraActividadError,
    TerminosNoAceptadosError,
)
from app.schemas import (
    AceptacionTerminos,
    Actividad,
    SolicitudInscripcion,
    Visitante,
)
from app.services.email_service import ServicioNotificaciones
from app.services.inscripciones import inscribir_participantes
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


def test_inscripcion_exitosa_valida_terminos_reserva_cupos_y_envia_correo():
    gestor = GestorReservas()
    correo = CorreoDePrueba()
    notificaciones = ServicioNotificaciones(correo)
    solicitud = SolicitudInscripcion(
        actividad=Actividad.TIROLESA,
        horario_id=1,
        cantidad_participantes=1,
        participantes=[
            Visitante(
                nombre="Ana Pérez",
                dni="12345678",
                edad=25,
                talle_vestimenta="M",
            )
        ],
        aceptacion_terminos=AceptacionTerminos(
            actividad=Actividad.TIROLESA,
            aceptados=True,
        ),
        email="ana@example.com",
    )
    resultado = inscribir_participantes(
        solicitud=solicitud,
        gestor_reservas=gestor,
        servicio_notificaciones=notificaciones,
        fecha="2026-10-26",
        horario="14:30",
    )
    assert resultado is not None
    assert resultado["id"] == 1
    assert gestor.consultar_cupos("Tirolesa", 1) == 9
    assert len(correo.envios) == 1
    assert correo.envios[0]["destinatario"] == "ana@example.com"
    assert "Tirolesa" in correo.envios[0]["contenido"]
    assert correo.envios[0]["qr"].startswith(b"\x89PNG\r\n\x1a\n")
  

def test_rechazo_por_terminos_no_aceptados_no_modifica_cupos_ni_envia_correo():
    gestor = GestorReservas()
    correo = CorreoDePrueba()
    notificaciones = ServicioNotificaciones(correo)

    solicitud = SolicitudInscripcion(
        actividad=Actividad.TIROLESA,
        horario_id=1,
        cantidad_participantes=1,
        participantes=[
            Visitante(
                nombre="Carlos Benítez",
                dni="22334455",
                edad=30,
                talle_vestimenta="L",
            )
        ],
        aceptacion_terminos=AceptacionTerminos(
            actividad=Actividad.TIROLESA,
            aceptados=False,
        ),
        email="carlos@example.com",
    )

    with pytest.raises(TerminosNoAceptadosError):
        inscribir_participantes(
            solicitud=solicitud,
            gestor_reservas=gestor,
            servicio_notificaciones=notificaciones,
            fecha="2026-10-26",
            horario="14:30",
        )

    assert gestor.consultar_cupos("Tirolesa", 1) == 10
    assert correo.envios == []




def test_rechazo_por_actividad_incompatible_en_terminos_no_crea_reserva():
    gestor = GestorReservas()
    correo = CorreoDePrueba()
    notificaciones = ServicioNotificaciones(correo)

    solicitud = SolicitudInscripcion(
        actividad=Actividad.TIROLESA,
        horario_id=1,
        cantidad_participantes=1,
        participantes=[
            Visitante(
                nombre="Lucía Morales",
                dni="33445566",
                edad=22,
                talle_vestimenta="S",
            )
        ],
        aceptacion_terminos=AceptacionTerminos(
            actividad=Actividad.SAFARI,
            aceptados=True,
        ),
        email="lucia@example.com",
    )

    with pytest.raises(AceptacionDeOtraActividadError):
        inscribir_participantes(
            solicitud=solicitud,
            gestor_reservas=gestor,
            servicio_notificaciones=notificaciones,
            fecha="2026-10-26",
            horario="14:30",
        )

    assert gestor.consultar_cupos("Tirolesa", 1) == 10
    assert gestor.consultar_cupos("Safari", 1) == 8
    assert correo.envios == []
