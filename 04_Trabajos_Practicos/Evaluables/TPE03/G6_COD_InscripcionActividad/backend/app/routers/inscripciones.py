from fastapi import APIRouter
from ..schemas import Actividad, TalleVestimenta, Visitante

router = APIRouter(prefix="/inscripciones", tags=["inscripciones"])

def validar_participantes(
    cantidad: int,
    participantes: list[dict],
    actividad: Actividad,
) -> bool:
    # 1. Validar cantidad de participantes
    if cantidad != len(participantes) or cantidad <= 0:
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

    # 3. Validar edad segun la actividad
    if not actividad.edad_minima == 0:
        for participante in participantes:
            if participante["edad"] < actividad.edad_minima:
                return False

    # 4. Validar que el DNI no se repita entre participantes
    dnis = []
    for participante in participantes:
        if isinstance(participante, dict):
            dnis.append(participante.get("dni"))
        else:
            dnis.append(getattr(participante, "dni", None))

    if len(dnis) != len(set(dnis)):
        return False

    return True


def validar_participante(participante: Visitante) -> bool:
    partes_nombre = participante.nombre.split()
    nombre_valido = bool(partes_nombre) and all(parte.isalpha() for parte in partes_nombre)

    talles_validos = {talle.value for talle in TalleVestimenta}
    talle = participante.talle_vestimenta

    return nombre_valido and (talle is None or talle in talles_validos)


def validar_dni_participante(dni: str) -> bool:
    return isinstance(dni, str) and dni.isdigit() and 1 <= int(dni) <= 999_999_999

