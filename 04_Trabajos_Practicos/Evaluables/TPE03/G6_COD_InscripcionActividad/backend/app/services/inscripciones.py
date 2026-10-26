from typing import Any

from app.schemas import SolicitudInscripcion
from app.services.aceptacion import validar_aceptacion
from app.services.email_service import ServicioNotificaciones
from app.services.reservas import GestorReservas


def _armar_datos_notificacion(
    reserva: dict[str, Any],
    email: str,
    fecha: str,
    horario: str,
) -> dict[str, Any]:
    datos = dict(reserva)
    datos.update(
        {
            "email": email,
            "fecha": fecha,
            "horario": horario,
        }
    )
    return datos


def inscribir_participantes(
    solicitud: SolicitudInscripcion,
    gestor_reservas: GestorReservas,
    servicio_notificaciones: ServicioNotificaciones,
    fecha: str,
    horario: str,
) -> dict[str, Any] | None:
    validar_aceptacion(solicitud.actividad, solicitud.aceptacion_terminos)

    participantes_dict = [
        participante.model_dump()
        for participante in solicitud.participantes
    ]

    reserva = gestor_reservas.crear_reserva(
        actividad=solicitud.actividad.value,
        horario_id=solicitud.horario_id,
        participantes=participantes_dict,
        cantidad_declarada=solicitud.cantidad_participantes,
    )

    if reserva is None:
        return None

    datos_notificacion = _armar_datos_notificacion(
        reserva=reserva,
        email=solicitud.email,
        fecha=fecha,
        horario=horario,
    )
    servicio_notificaciones.enviar_confirmacion(datos_notificacion)

    return reserva
