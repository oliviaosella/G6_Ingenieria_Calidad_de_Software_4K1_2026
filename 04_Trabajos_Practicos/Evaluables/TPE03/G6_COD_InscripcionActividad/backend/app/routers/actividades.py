from datetime import date
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
        {**actividad, "nombre": actividad["id"].value, "cupo_maximo": actividad["cupo"]}
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
