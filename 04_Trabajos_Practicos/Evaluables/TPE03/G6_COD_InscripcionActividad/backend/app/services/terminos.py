from app.schemas import Actividad, TerminosCondiciones

# TEXTOS FICTICIOS: pendientes de aprobación del PO. No son condiciones reales.
_TERMINOS = {
    Actividad.TIROLESA: "Texto ficticio de términos de Tirolesa.",
    Actividad.SAFARI: "Texto ficticio de términos de Safari.",
    Actividad.PALESTRA: "Texto ficticio de términos de Palestra.",
    Actividad.JARDINERIA: "Texto ficticio de términos de Jardinería.",
}


def obtener_terminos(actividad: Actividad) -> TerminosCondiciones:
    return TerminosCondiciones(actividad=actividad, texto=_TERMINOS[actividad])