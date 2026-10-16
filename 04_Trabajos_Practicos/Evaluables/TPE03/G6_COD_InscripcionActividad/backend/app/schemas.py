from enum import Enum

from pydantic import BaseModel
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
    TIROLESA = ("Tirolesa", True, 10)
    SAFARI = ("Safari", False, 8)
    PALESTRA = ("Palestra", True, 12)
    JARDINERIA = ("Jardinería", False, 12)

    talle_obligatorio: bool
    cupo: int

    def __new__(
        cls,
        value: str,
        talle_obligatorio: bool,
        cupo: int,
    ) -> "Actividad":
        obj = str.__new__(cls, value)
        obj._value_ = value
        obj.talle_obligatorio = talle_obligatorio
        obj.cupo = cupo
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
