from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class Actividad(str, Enum):
    TIROLESA = "Tirolesa"
    SAFARI = "Safari"
    PALESTRA = "Palestra"
    JARDINERIA = "Jardinería"


class HorarioDisponible(BaseModel):
    horario_id: int
    actividad: Actividad
    inicio: datetime
    fin: datetime
    cupos_disponibles: int