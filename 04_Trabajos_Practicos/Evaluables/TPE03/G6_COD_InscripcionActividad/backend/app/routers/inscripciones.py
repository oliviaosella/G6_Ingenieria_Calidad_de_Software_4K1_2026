from fastapi import APIRouter

router = APIRouter(prefix="/inscripciones", tags=["inscripciones"])

def validar_participantes(
    cantidad: int,
    participantes: list[dict],
    requiere_talle: bool,
) -> bool:
    ...

def validar_participante(
    nombre: str,
    dni: str,
    edad: int,
    talle_vestimenta: str | None = None,
) -> bool:
    ...