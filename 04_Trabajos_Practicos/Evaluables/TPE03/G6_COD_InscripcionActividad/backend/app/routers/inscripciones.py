from fastapi import APIRouter
from ..schemas import Visitante

router = APIRouter(prefix="/inscripciones", tags=["inscripciones"])

def validar_participantes(
    cantidad: int,
    participantes: list[dict],
    requiere_talle: bool,
) -> bool:
    ...

def validar_participante(participante: Visitante) -> bool:
    ...