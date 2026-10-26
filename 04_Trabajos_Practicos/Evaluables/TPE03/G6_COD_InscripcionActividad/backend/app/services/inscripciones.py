from typing import Any

from app.errors import (
    CuposNoDisponiblesError,
    DniDuplicadoEnHorarioError,
    InconsistenciaParticipantesError,
    ParticipantesInvalidosError,
)
from app.schemas import SolicitudInscripcion
from app.services.aceptacion import validar_aceptacion
from app.services.email_service import ServicioNotificaciones
from app.services.reservas import GestorReservas
from app.services.participantes import validar_participantes


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
) -> dict[str, Any]:
    """Orquesta el proceso de inscripción a una actividad.

    Valida la aceptación de los términos específicos de la actividad,
    verifica que la cantidad declarada coincida con los participantes,
    valida que ningún DNI esté duplicado en el turno, descuenta cupos
    de forma atómica y emite la confirmación con QR.

    Raises:
        TerminosNoAceptadosError: Si los términos no fueron aceptados.
        AceptacionDeOtraActividadError: Si los términos corresponden a otra
            actividad distinta de la solicitada.
        InconsistenciaParticipantesError: Si la cantidad de participantes
            declarada no coincide con la lista enviada.
        DniDuplicadoEnHorarioError: Si uno o más participantes ya están
            inscriptos en el horario seleccionado.
        CuposNoDisponiblesError: Si la cantidad de participantes supera los
            cupos disponibles en el horario seleccionado.
        ParticipantesInvalidosError: Si los datos personales, edades, talles
            o DNIs de la solicitud no cumplen las reglas de la actividad.
    """
    validar_aceptacion(solicitud.actividad, solicitud.aceptacion_terminos)

    if len(solicitud.participantes) != solicitud.cantidad_participantes:
        raise InconsistenciaParticipantesError

    if not gestor_reservas.puede_reservar(
        solicitud.actividad.value, solicitud.horario_id,
        solicitud.cantidad_participantes, fecha,
    ):
        raise CuposNoDisponiblesError

    if not validar_participantes(
        cantidad=solicitud.cantidad_participantes,
        participantes=solicitud.participantes,
        actividad=solicitud.actividad,
    ):
        raise ParticipantesInvalidosError

    for participante in solicitud.participantes:
        if gestor_reservas.dni_esta_inscripto(
            solicitud.horario_id, participante.dni, fecha
        ):
            raise DniDuplicadoEnHorarioError

    participantes_dict = [
        participante.model_dump()
        for participante in solicitud.participantes
    ]

    reserva = gestor_reservas.crear_reserva(
        actividad=solicitud.actividad.value,
        horario_id=solicitud.horario_id,
        participantes=participantes_dict,
        cantidad_declarada=solicitud.cantidad_participantes,
        fecha=fecha,
    )

    if reserva is None:
        raise CuposNoDisponiblesError

    datos_notificacion = _armar_datos_notificacion(
        reserva=reserva,
        email=solicitud.email,
        fecha=fecha,
        horario=horario,
    )
    servicio_notificaciones.enviar_confirmacion(datos_notificacion)

    return reserva
