import pytest

from app.errors import AceptacionDeOtraActividadError, TerminosNoAceptadosError
from app.schemas import Actividad, AceptacionTerminos
from app.services.aceptacion import validar_aceptacion


def test_rechazar_terminos_no_aceptados():
    aceptacion = AceptacionTerminos(
        actividad=Actividad.TIROLESA,
        aceptados=False,
    )

    with pytest.raises(TerminosNoAceptadosError):
        validar_aceptacion(Actividad.TIROLESA, aceptacion)


def test_aceptar_terminos_de_la_actividad_elegida():
    aceptacion = AceptacionTerminos(
        actividad=Actividad.TIROLESA,
        aceptados=True,
    )

    assert validar_aceptacion(Actividad.TIROLESA, aceptacion) is None


def test_rechazar_aceptacion_de_otra_actividad():
    aceptacion = AceptacionTerminos(
        actividad=Actividad.SAFARI,
        aceptados=True,
    )

    with pytest.raises(AceptacionDeOtraActividadError):
        validar_aceptacion(Actividad.TIROLESA, aceptacion)
