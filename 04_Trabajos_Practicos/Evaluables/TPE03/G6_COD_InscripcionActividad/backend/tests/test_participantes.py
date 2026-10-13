from inspect import signature
from app.routers.inscripciones import validar_participantes
from app.routers.inscripciones import validar_participante


def test_validar_participantes() -> None:
    assert callable(validar_participantes)

def test_validar_participante() -> None:
    assert callable(validar_participante)

def test_validar_participantes_acepta_argumentos_esperados():
    signature(validar_participantes).bind(
        cantidad=1,
        participantes=[{"datos": "datos del participante"}],
        requiere_talle=False,
    )

def test_validar_participante_acepta_argumentos_esperados():
    signature(validar_participante).bind(
        nombre="Ana",
        dni="12345678",
        edad=25,
        talle_vestimenta="XL",
    )
