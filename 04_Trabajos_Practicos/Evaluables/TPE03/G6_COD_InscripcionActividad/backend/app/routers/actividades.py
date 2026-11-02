from datetime import date, timedelta
from typing import Any
from fastapi import APIRouter, Depends, Query

from app.dependencies import get_gestor_reservas
from app.schemas import (
    Actividad,
    ActividadDetalleResponse,
    CalendarioReservaResponse,
    HorarioConsultaResponse,
    TalleVestimenta,
    TerminosCondiciones,
)
from app.services.reservas import GestorReservas
from app.services.terminos import obtener_terminos
from app.routers import consulta_actividades

router = APIRouter(prefix="/actividades", tags=["Actividades"])

CATALOGO_ACTIVIDADES: list[dict[str, Any]] = [
    {
        "id": Actividad.TIROLESA,
        "categoria": "Aventura",
        "descripcion": "Una vista nueva del bosque, suspendido entre los árboles.",
        "duracion": "45 min",
        "cupo": 10,
        "edad_minima": 8,
        "requiere_talle": True,
    },
    {
        "id": Actividad.SAFARI,
        "categoria": "Exploración",
        "descripcion": "Descubrí la vida del parque con una mirada más curiosa.",
        "duracion": "60 min",
        "cupo": 8,
        "edad_minima": 0,
        "requiere_talle": False,
    },
    {
        "id": Actividad.PALESTRA,
        "categoria": "Desafío",
        "descripcion": "Elegí tu camino y alcanzá una nueva perspectiva.",
        "duracion": "50 min",
        "cupo": 12,
        "edad_minima": 12,
        "requiere_talle": True,
    },
    {
        "id": Actividad.JARDINERIA,
        "categoria": "Naturaleza",
        "descripcion": "Manos a la tierra para conectar con lo que crece.",
        "duracion": "40 min",
        "cupo": 12,
        "edad_minima": 0,
        "requiere_talle": False,
    },
]


@router.get(
    "",
    response_model=list[ActividadDetalleResponse],
    summary="Listar catálogo de actividades y reglas",
    description="Retorna el catálogo oficial de actividades habilitadas en el parque con sus reglas de admisión.",
)
def listar_actividades() -> list[dict[str, Any]]:
    return [
        {
            **actividad,
            "nombre": actividad["id"].value,
            "cupo_maximo": actividad["cupo"],
            "talles_disponibles": [talle.value for talle in TalleVestimenta] if actividad["requiere_talle"] else [],
        }
        for actividad in CATALOGO_ACTIVIDADES
    ]


@router.get(
    "/{actividad}/terminos",
    response_model=TerminosCondiciones,
    summary="Obtener texto de términos y condiciones",
    description="Obtiene los términos y condiciones específicos vigentes para la actividad indicada.",
)
def consultar_terminos(actividad: Actividad) -> TerminosCondiciones:
    return obtener_terminos(actividad)


@router.get(
    "/{actividad}/horarios",
    response_model=list[HorarioConsultaResponse],
    summary="Consultar turnos y cupos disponibles en tiempo real",
    description="Aplica cierres y la ventana de 15 minutos a 24 horas; informa cupos por actividad, fecha y turno.",
)
def consultar_horarios(
    actividad: Actividad,
    fecha: date = Query(description="Fecha de consulta (YYYY-MM-DD)"),
    gestor: GestorReservas = Depends(get_gestor_reservas),
) -> list[dict[str, Any]]:
    return [
        {**turno, "horario_id": int(turno["hora"][:2]) - 8}
        for turno in consulta_actividades.turnos_con_cupos(actividad.value, fecha, gestor)
    ]


@router.get(
    "/{actividad}/calendario",
    response_model=CalendarioReservaResponse,
    summary="Consultar fechas y turnos reservables",
    description="Informa desde el backend la ventana de reserva, los cierres del parque y los cupos de cada turno.",
)
def consultar_calendario(
    actividad: Actividad,
    gestor: GestorReservas = Depends(get_gestor_reservas),
) -> dict[str, Any]:
    hoy = consulta_actividades.obtener_hora_actual().date()
    dias = []
    for fecha in (hoy, hoy + timedelta(days=1)):
        horarios = consultar_horarios(actividad, fecha, gestor)
        cierre = consulta_actividades.motivo_cierre(fecha)
        if cierre:
            estado, motivo = "cerrado", cierre
        elif not horarios:
            estado, motivo = "fuera_de_ventana", "No hay horarios dentro de la ventana de reserva"
        elif not any(turno["disponible"] for turno in horarios):
            estado, motivo = "sin_cupos", "No hay cupos disponibles en esta fecha"
        else:
            estado, motivo = "con_horarios", None
        dias.append({"fecha": fecha.isoformat(), "estado": estado, "motivo": motivo, "horarios": horarios})
    return {
        "anticipacion_minima_minutos": int(consulta_actividades.ANTICIPACION_MINIMA.total_seconds() // 60),
        "anticipacion_maxima_horas": int(consulta_actividades.ANTICIPACION_MAXIMA.total_seconds() // 3600),
        "dias": dias,
    }
