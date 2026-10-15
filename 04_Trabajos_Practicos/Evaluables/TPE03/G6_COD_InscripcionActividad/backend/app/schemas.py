from datetime import datetime
from enum import Enum

from pydantic import BaseModel, EmailStr, Field
"""
# Clase de ejemplo incompleta
# Usar pydantic Field para validación

class Actividad(str, Enum):
    TIROLESA = "Tirolesa"
    SAFARI = "Safari"
    PALESTRA = "Palestra"
    JARDINERIA = "Jardinería"
"""

class Actividad(str, Enum):
    TIROLESA = ("Tirolesa", True, 10, 8)
    SAFARI = ("Safari", False, 8, 0)
    PALESTRA = ("Palestra", True, 12, 12)
    JARDINERIA = ("Jardinería", False, 12, 0)

    talle_obligatorio: bool
    cupo: int
    edad_minima: int

    def __new__(
        cls,
        value: str,
        talle_obligatorio: bool,
        cupo: int,
        edad_minima: int,
    ) -> "Actividad":
        obj = str.__new__(cls, value)
        obj._value_ = value
        obj.talle_obligatorio = talle_obligatorio
        obj.cupo = cupo
        obj.edad_minima = edad_minima
        return obj


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
