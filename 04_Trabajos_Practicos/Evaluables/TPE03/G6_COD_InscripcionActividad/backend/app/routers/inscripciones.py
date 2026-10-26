from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status

from app.dependencies import get_gestor_reservas, get_servicio_notificaciones
from app.errors import (
    AceptacionDeOtraActividadError,
    CuposNoDisponiblesError,
    DniDuplicadoEnHorarioError,
    InconsistenciaParticipantesError,
    TerminosNoAceptadosError,
)
from app.schemas import (
    InscripcionExitosaResponse,
    ReservaConsultaResponse,
    SolicitudInscripcion,
)
from app.services.email_service import ServicioNotificaciones
from app.services.inscripciones import inscribir_participantes
from app.services.reservas import GestorReservas

router = APIRouter(prefix="/inscripciones", tags=["Inscripciones"])


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=InscripcionExitosaResponse,
    summary="Registrar y confirmar inscripción a una actividad",
    description=(
        "Procesa la inscripción integral: valida la aceptación de términos, la consistencia "
        "de los participantes declarados, verifica que ningún DNI esté duplicado en el mismo turno, "
        "descuenta cupos atómicamente y emite el correo con QR adjunto."
    ),
    responses={
        201: {"description": "Inscripción creada y confirmada exitosamente."},
        400: {
            "description": (
                "Bad Request: Términos no aceptados, términos de otra actividad o inconsistencia "
                "entre cantidad declarada y participantes enviados."
            )
        },
        409: {
            "description": (
                "Conflict: Cupos insuficientes en el turno seleccionado o DNI duplicado en el horario."
            )
        },
        422: {"description": "Unprocessable Entity: Formato de datos o validación Pydantic incorrectos."},
    },
)
def registrar_inscripcion(
    solicitud: SolicitudInscripcion,
    gestor_reservas: GestorReservas = Depends(get_gestor_reservas),
    servicio_notificaciones: ServicioNotificaciones = Depends(get_servicio_notificaciones),
) -> dict[str, Any]:
    fecha = solicitud.fecha if solicitud.fecha else "2026-10-27"
    horario = solicitud.horario if solicitud.horario else f"{solicitud.horario_id + 8:02d}:00"

    try:
        reserva = inscribir_participantes(
            solicitud=solicitud,
            gestor_reservas=gestor_reservas,
            servicio_notificaciones=servicio_notificaciones,
            fecha=fecha,
            horario=horario,
        )
    except TerminosNoAceptadosError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Los términos y condiciones deben ser aceptados para confirmar la inscripción.",
        )
    except AceptacionDeOtraActividadError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Los términos aceptados no corresponden a la actividad solicitada.",
        )
    except InconsistenciaParticipantesError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La cantidad de participantes declarada no coincide con los participantes enviados.",
        )
    except CuposNoDisponiblesError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="No hay cupos disponibles suficientes para la actividad en el turno seleccionado.",
        )
    except DniDuplicadoEnHorarioError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Uno o más participantes ya tienen una reserva activa en este mismo turno horario.",
        )

    return {
        "id": reserva["id"],
        "actividad": reserva["actividad"],
        "horario_id": reserva["horario_id"],
        "fecha": fecha,
        "horario": horario,
        "email": solicitud.email,
        "participantes": reserva["participantes"],
        "qr_codigo": f"RESERVA-{reserva['id']}",
    }


@router.get(
    "/{id}",
    response_model=ReservaConsultaResponse,
    summary="Consultar una reserva por ID",
    description="Permite recuperar los datos de una reserva registrada previamente.",
    responses={
        200: {"description": "Datos de la reserva encontrada."},
        404: {"description": "Reserva no encontrada."},
    },
)
def consultar_reserva(
    id: int,
    gestor_reservas: GestorReservas = Depends(get_gestor_reservas),
) -> dict[str, Any]:
    reserva = gestor_reservas.obtener_reserva(id)
    if reserva is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reserva no encontrada.",
        )
    return reserva
