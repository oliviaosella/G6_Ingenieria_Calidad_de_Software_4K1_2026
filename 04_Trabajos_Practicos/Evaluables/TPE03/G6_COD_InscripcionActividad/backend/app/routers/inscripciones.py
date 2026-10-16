from fastapi import APIRouter
from ..schemas import Actividad, TalleVestimenta, Visitante

router = APIRouter(prefix="/inscripciones", tags=["inscripciones"])

def validar_participantes(
    cantidad: int,
    participantes: list[dict],
    actividad: Actividad,
) -> bool:
    # 1. Validar cantidad de participantes
    if cantidad != len(participantes):
        return False

    talles_validos = {talle.value for talle in TalleVestimenta}

    # 2. Validar talle según la actividad
    for participante in participantes:
        talle = participante.get("talle_vestimenta")

        if actividad.talle_obligatorio:
            if not talle or talle not in talles_validos:
                return False
        elif talle and talle not in talles_validos:
            return False

    return True



def validar_participante(participante: Visitante) -> bool:
    partes_nombre = participante.nombre.split()
    nombre_valido = bool(partes_nombre) and all(parte.isalpha() for parte in partes_nombre)

    talles_validos = {talle.value for talle in TalleVestimenta}
    talle = participante.talle_vestimenta

    return nombre_valido and (talle is None or talle in talles_validos)
