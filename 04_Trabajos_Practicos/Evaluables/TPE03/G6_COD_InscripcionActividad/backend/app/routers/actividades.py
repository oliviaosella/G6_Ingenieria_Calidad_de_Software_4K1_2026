from typing import Any
from fastapi import APIRouter, Depends, Query

from app.dependencies import get_gestor_reservas
from app.schemas import (
    Actividad,
    ActividadDetalleResponse,
    HorarioConsultaResponse,
    TerminosCondiciones,
)
from app.services.reservas import GestorReservas
from app.services.terminos import obtener_terminos

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
    return CATALOGO_ACTIVIDADES


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
    description="Retorna los 9 turnos diarios para la actividad en la fecha solicitada, informando cupos disponibles en tiempo real.",
)
def consultar_horarios(
    actividad: Actividad,
    fecha: str = Query(default="2026-10-27", description="Fecha de consulta (YYYY-MM-DD)"),
    gestor: GestorReservas = Depends(get_gestor_reservas),
) -> list[dict[str, Any]]:
    turnos: list[dict[str, Any]] = []
    for horario_id in range(1, 10):
        hora = f"{horario_id + 8:02d}:00"
        cupos = gestor.consultar_cupos(actividad.value, horario_id)
        turnos.append(
            {
                "horario_id": horario_id,
                "actividad": actividad,
                "fecha": fecha,
                "hora": hora,
                "cupos_disponibles": cupos,
                "disponible": cupos > 0,
            }
        )
    return turnos
