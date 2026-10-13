from app.schemas import Actividad, TerminosCondiciones
from app.services.terminos import obtener_terminos


def test_obtiene_terminos_de_la_actividad_elegida():
    terminos = obtener_terminos(Actividad.TIROLESA)

    assert isinstance(terminos, TerminosCondiciones)
    assert terminos.actividad == Actividad.TIROLESA
    assert terminos.texto