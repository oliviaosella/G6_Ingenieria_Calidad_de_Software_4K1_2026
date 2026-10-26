from typing import Any

from app.errors import (
    CuposNoDisponiblesError,
    DniDuplicadoEnHorarioError,
    InconsistenciaParticipantesError,
)
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
) -> dict[str, Any]:
    """Orquesta el proceso de inscripción a una actividad.

    Valida la aceptación de los términos específicos de la actividad,
    verifica que ningún DNI esté duplicado en el turno, descuenta cupos
    de forma atómica y emite la confirmación con QR.

    Raises:
        TerminosNoAceptadosError: Si los términos no fueron aceptados.
        AceptacionDeOtraActividadError: Si los términos corresponden a otra
            actividad distinta de la solicitada.
        DniDuplicadoEnHorarioError: Si uno o más participantes ya están
            inscriptos en el horario seleccionado.
        CuposNoDisponiblesError: Si la cantidad de participantes supera los
            cupos disponibles en el horario seleccionado.
    """
    validar_aceptacion(solicitud.actividad, solicitud.aceptacion_terminos)

    
    if len(solicitud.participantes) != solicitud.cantidad_participantes:
        raise InconsistenciaParticipantesError

    for participante in solicitud.participantes:
        if gestor_reservas.dni_esta_inscripto(
            solicitud.horario_id, participante.dni
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

