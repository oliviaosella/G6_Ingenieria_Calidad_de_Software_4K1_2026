from datetime import datetime
from enum import Enum

from pydantic import BaseModel, EmailStr, Field
# Clase de ejemplo incompleta
# Usar pydantic Field para validación

class Actividad(str, Enum):
    TIROLESA = "Tirolesa"
    SAFARI = "Safari"
    PALESTRA = "Palestra"
    JARDINERIA = "Jardinería"

class TalleVestimenta(str, Enum):
    XS = "XS"
    S = "S"
    M = "M"
    L = "L"
    XL = "XL"
    XXL = "XXL"


class Visitante(BaseModel):
    nombre: str
    dni: str
    edad: int
    talle_vestimenta: str | None = None
