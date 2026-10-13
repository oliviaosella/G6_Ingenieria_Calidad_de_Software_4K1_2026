from app.schemas import Actividad, TerminosCondiciones

# TEXTO FICTICIO: pendiente de aprobación del PO. No son condiciones reales.
_TEXTO_FICTICIO = "Texto ficticio de términos."


def obtener_terminos(actividad: Actividad) -> TerminosCondiciones:
    return TerminosCondiciones(actividad=actividad, texto=_TEXTO_FICTICIO)