from datetime import date
from enum import Enum

from pydantic import BaseModel, EmailStr, Field


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


class HorarioDisponible(BaseModel):
    actividad: Actividad
    fecha: date
    hora: str
    cupos_disponibles: int | None = None
    disponible: bool | None = None
    motivo: str | None = None


class SolicitudValidacionParticipantes(BaseModel):
    actividad: Actividad
    cantidad: int
    participantes: list[Visitante]


class TerminosCondiciones(BaseModel):
    actividad: Actividad
    texto: str
    version: str = "1"
    pendiente_aprobacion: bool = True


class AceptacionTerminos(BaseModel):
    actividad: Actividad
    aceptados: bool
    version: str | None = None


class SolicitudInscripcion(BaseModel):
    actividad: Actividad
    horario_id: int = Field(ge=1, le=9)
    cantidad_participantes: int = Field(gt=0)
    participantes: list[Visitante]
    aceptacion_terminos: AceptacionTerminos
    email: EmailStr
    fecha: str = ""
    horario: str = ""


class InscripcionConfirmada(BaseModel):
    inscripcion_id: int
    solicitud: SolicitudInscripcion


class ActividadDetalleResponse(BaseModel):
    nombre: str
    cupo_maximo: int
    id: Actividad
    categoria: str
    descripcion: str
    duracion: str
    cupo: int
    edad_minima: int
    requiere_talle: bool


class HorarioConsultaResponse(BaseModel):
    horario_id: int
    actividad: Actividad
    fecha: str
    hora: str
    cupos_disponibles: int
    disponible: bool
    motivo: str | None = None


class InscripcionExitosaResponse(BaseModel):
    id: int
    actividad: Actividad
    horario_id: int
    fecha: str
    horario: str
    email: EmailStr
    participantes: list[Visitante]
    qr_codigo: str
    qr_contenido: str
    qr_url: str
    estado: str
    correo_estado: str
    correo_error: str | None = None
    intentos_envio: int


class ReservaConsultaResponse(BaseModel):
    id: int
    actividad: str
    horario_id: int
    participantes: list[dict]
    fecha: str | None = None
    horario: str | None = None
    email: EmailStr | None = None
    estado: str | None = None
    correo_estado: str | None = None
    correo_error: str | None = None
    intentos_envio: int = 0
    creada_en: str | None = None
    aceptacion_terminos: dict | None = None

    model_config = {"extra": "allow"}
