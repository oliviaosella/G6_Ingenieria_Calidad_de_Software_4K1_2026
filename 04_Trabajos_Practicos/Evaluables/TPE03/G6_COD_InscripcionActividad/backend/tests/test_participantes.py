from inspect import signature
from app.routers.inscripciones import validar_participantes
from app.routers.inscripciones import validar_participante


def test_validar_participantes() -> None:
    assert callable(validar_participantes)

def test_validar_participante() -> None:
    assert callable(validar_participante)
