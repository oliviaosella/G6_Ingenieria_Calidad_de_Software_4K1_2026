import pytest

from app.errors import AceptacionDeOtraActividadError, TerminosNoAceptadosError
from app.schemas import Actividad, AceptacionTerminos
from app.services.aceptacion import validar_aceptacion


ACTIVIDADES_DISTINTAS = [
    (actividad, otra)
    for actividad in Actividad
    for otra in Actividad
    if actividad != otra
]


@pytest.mark.parametrize("actividad", list(Actividad))
def test_rechazar_terminos_no_aceptados(actividad):
    aceptacion = AceptacionTerminos(
        actividad=actividad,
        aceptados=False,
    )

    with pytest.raises(TerminosNoAceptadosError):
        validar_aceptacion(actividad, aceptacion)


@pytest.mark.parametrize("actividad", list(Actividad))
def test_aceptar_terminos_de_la_actividad_elegida(actividad):
    aceptacion = AceptacionTerminos(
        actividad=actividad,
        aceptados=True,
    )

    assert validar_aceptacion(actividad, aceptacion) is None


@pytest.mark.parametrize(
    "actividad, actividad_aceptada",
    ACTIVIDADES_DISTINTAS,
)
def test_rechazar_aceptacion_de_otra_actividad(actividad, actividad_aceptada):
    aceptacion = AceptacionTerminos(
        actividad=actividad_aceptada,
        aceptados=True,
    )

    with pytest.raises(AceptacionDeOtraActividadError):
        validar_aceptacion(actividad, aceptacion)


@pytest.mark.parametrize(
    "actividad, actividad_aceptada",
    ACTIVIDADES_DISTINTAS,
)
def test_priorizar_terminos_no_aceptados_si_la_actividad_tambien_difiere(
    actividad, actividad_aceptada
):
    aceptacion = AceptacionTerminos(
        actividad=actividad_aceptada,
        aceptados=False,
    )

    with pytest.raises(TerminosNoAceptadosError):
        validar_aceptacion(actividad, aceptacion)
