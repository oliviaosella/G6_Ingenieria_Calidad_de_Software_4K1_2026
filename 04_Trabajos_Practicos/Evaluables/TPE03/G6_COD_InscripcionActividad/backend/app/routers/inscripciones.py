from fastapi import APIRouter
from ..schemas import Actividad, TalleVestimenta, Visitante

router = APIRouter(prefix="/inscripciones", tags=["inscripciones"])

def validar_participantes(
    cantidad: int,
    participantes: list[dict],
    actividad: Actividad,
) -> bool:
    return cantidad > 0 and cantidad == len(participantes)


def validar_participante(participante: Visitante) -> bool:
    partes_nombre = participante.nombre.split()
    nombre_valido = bool(partes_nombre) and all(parte.isalpha() for parte in partes_nombre)

    talles_validos = {talle.value for talle in TalleVestimenta}
    talle = participante.talle_vestimenta

    return nombre_valido and (talle is None or talle in talles_validos)
