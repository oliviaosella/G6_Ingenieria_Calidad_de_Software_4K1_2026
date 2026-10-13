from datetime import datetime
from enum import Enum

from pydantic import BaseModel, EmailStr


class Actividad(str, Enum):
    TIROLESA = "Tirolesa"
    SAFARI = "Safari"
    PALESTRA = "Palestra"
    JARDINERIA = "Jardinería"


class Visitante(BaseModel):
    nombre: str
    dni: str
    edad: int
    talle_vestimenta: str | None = None


class HorarioDisponible(BaseModel):
    horario_id: int
    actividad: Actividad
    inicio: datetime
    fin: datetime
    cupos_disponibles: int


class TerminosCondiciones(BaseModel):
    actividad: Actividad
    texto: str


class AceptacionTerminos(BaseModel):
    actividad: Actividad
    aceptados: bool


class SolicitudInscripcion(BaseModel):
    actividad: Actividad
    horario_id: int
    cantidad_participantes: int
    participantes: list[Visitante]
    aceptacion_terminos: AceptacionTerminos
    email: EmailStr


class InscripcionConfirmada(BaseModel):
    inscripcion_id: int
    solicitud: SolicitudInscripcion
