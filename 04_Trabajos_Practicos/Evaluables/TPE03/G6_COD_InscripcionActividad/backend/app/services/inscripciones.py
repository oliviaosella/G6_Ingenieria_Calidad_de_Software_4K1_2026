from typing import Any
from datetime import datetime, timezone
from qrcode.exceptions import DataOverflowError

from app.errors import (
    CuposNoDisponiblesError,
    DniDuplicadoEnHorarioError,
    InconsistenciaParticipantesError,
    ParticipantesInvalidosError,
    ComprobanteInvalidoError,
)
from app.schemas import SolicitudInscripcion
from app.services.aceptacion import validar_aceptacion
from app.services.email_service import ServicioNotificaciones
from app.services.reservas import GestorReservas
from app.services.participantes import validar_participantes
from app.services.terminos import obtener_terminos
from app.services.notificaciones import procesar_envio
from app.services.qr_service import validar_capacidad_qr


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

    terminos = obtener_terminos(solicitud.actividad)
    datos = {
        "email": str(solicitud.email), "horario": horario, "estado": "confirmada",
        "correo_estado": "pendiente", "correo_error": None, "intentos_envio": 0,
        "creada_en": datetime.now(timezone.utc).isoformat(),
        "aceptacion_terminos": {
            "actividad": solicitud.actividad.value, "aceptados": True,
            "version": terminos.version, "texto": terminos.texto,
            "aceptados_en": datetime.now(timezone.utc).isoformat(),
        },
    }
    try:
        # El mayor ID de SQLite reserva espacio suficiente sin asignar un ID real.
        validar_capacidad_qr({
            **datos, "id": 9223372036854775807, "actividad": solicitud.actividad.value,
            "fecha": fecha, "participantes": participantes_dict,
        })
    except DataOverflowError as error:
        raise ComprobanteInvalidoError from error

    reserva = gestor_reservas.crear_reserva(
        actividad=solicitud.actividad.value,
        horario_id=solicitud.horario_id,
        participantes=participantes_dict,
        cantidad_declarada=solicitud.cantidad_participantes,
        fecha=fecha,
        datos_adicionales=datos,
    )

    if reserva is None:
        raise CuposNoDisponiblesError

    return procesar_envio(reserva["id"], gestor_reservas, servicio_notificaciones)
