from app.schemas import Actividad, TalleVestimenta, Visitante


def validar_participantes(
    cantidad: int,
    participantes: list[Visitante],
    actividad: Actividad,
    cupos_disponibles: int | None = None,
) -> bool:


    # 1. Validar cantidad de participantes
    if cantidad != len(participantes) or cantidad <= 0 or actividad.cupo < cantidad:
        return False

    if cupos_disponibles is not None and cantidad > cupos_disponibles:
        return False

    if not all(
        validar_participante(participante)
        for participante in participantes
    ):
        return False

    talles_validos = {talle.value for talle in TalleVestimenta}

    # 2. Validar talle según la actividad
    for participante in participantes:
        talle = participante.talle_vestimenta

        if actividad.talle_obligatorio:
            if not talle or talle not in talles_validos:
                return False
        elif talle and talle not in talles_validos:
            return False

    # 3. Validar edad segun la actividad
    if not actividad.edad_minima == 0:
        for participante in participantes:
            if participante.edad < actividad.edad_minima:
                return False

    # 4. Validar que el DNI no se repita entre participantes
    dnis = [participante.dni for participante in participantes]

    if len(dnis) != len(set(dnis)):
        return False

    return True


def validar_participante(participante: Visitante) -> bool:
    partes_nombre = participante.nombre.split()
    nombre_valido = bool(partes_nombre) and all(parte.isalpha() for parte in partes_nombre)

    talles_validos = {talle.value for talle in TalleVestimenta}
    talle = participante.talle_vestimenta

    return nombre_valido and (talle is None or talle in talles_validos) and validar_edad_positiva(participante.edad) and validar_dni_participante(participante.dni)


def validar_dni_participante(dni: str) -> bool:
    return (
        isinstance(dni, str)
        and len(dni) == 8
        and dni.isascii()
        and dni.isdigit()
        and dni != "00000000"
    )


def validar_edad_positiva(edad: int) -> bool:
    return isinstance(edad, int) and not isinstance(edad, bool) and 0 < edad <= 100
