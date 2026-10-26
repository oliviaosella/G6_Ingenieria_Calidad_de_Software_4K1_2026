import pytest

from app.schemas import Actividad, TerminosCondiciones
from app.services.terminos import obtener_terminos

ACTIVIDADES = list(Actividad)


def test_obtiene_terminos_de_la_actividad_elegida():
    terminos = obtener_terminos(Actividad.TIROLESA)

    assert isinstance(terminos, TerminosCondiciones)
    assert terminos.actividad == Actividad.TIROLESA
    assert terminos.texto


@pytest.mark.parametrize("actividad", ACTIVIDADES)
def test_terminos_corresponden_a_la_actividad_pedida(actividad):
    terminos = obtener_terminos(actividad)

    assert terminos.actividad == actividad


@pytest.mark.parametrize("actividad", ACTIVIDADES)
def test_cada_actividad_tiene_texto_no_vacio(actividad):
    assert obtener_terminos(actividad).texto.strip()


def test_cada_actividad_tiene_terminos_distintos():
    textos = {obtener_terminos(actividad).texto for actividad in ACTIVIDADES}

    assert len(textos) == len(ACTIVIDADES)


def test_resultado_es_siempre_terminos_condiciones():
    for actividad in ACTIVIDADES:
        assert isinstance(obtener_terminos(actividad), TerminosCondiciones)


def test_llamadas_repetidas_devuelven_los_mismos_terminos():
    primera = obtener_terminos(Actividad.SAFARI)
    segunda = obtener_terminos(Actividad.SAFARI)

    assert primera == segunda
