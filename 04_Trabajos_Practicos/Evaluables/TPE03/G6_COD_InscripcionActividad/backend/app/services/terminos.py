from app.schemas import Actividad, TerminosCondiciones

# TEXTOS FICTICIOS: pendientes de aprobación del PO. No son condiciones reales.
_TERMINOS = {
    actividad: f"Texto ficticio de términos de {actividad.value}."
    for actividad in Actividad
}


def obtener_terminos(actividad: Actividad) -> TerminosCondiciones:
    return TerminosCondiciones(actividad=actividad, texto=_TERMINOS[actividad])