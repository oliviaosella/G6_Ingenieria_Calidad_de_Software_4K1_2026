from app.schemas import Actividad, TerminosCondiciones


def obtener_terminos(actividad: Actividad) -> TerminosCondiciones:
    return TerminosCondiciones(
        actividad=actividad,
        texto="Texto ficticio de términos.",
    )