import pytest

from app.errors import TerminosNoAceptadosError
from app.schemas import Actividad, AceptacionTerminos
from app.services.aceptacion import validar_aceptacion


def test_rechazar_terminos_no_aceptados():
    aceptacion = AceptacionTerminos(
        actividad=Actividad.TIROLESA,
        aceptados=False,
    )

    with pytest.raises(TerminosNoAceptadosError):
        validar_aceptacion(Actividad.TIROLESA, aceptacion)
