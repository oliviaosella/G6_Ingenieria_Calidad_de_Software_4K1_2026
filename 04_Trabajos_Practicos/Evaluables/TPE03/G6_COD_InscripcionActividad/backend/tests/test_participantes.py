import pytest

from app.routers.inscripciones import validar_dni_participante
from app.schemas import Actividad
from inspect import signature
from app.routers.inscripciones import validar_participantes
from app.routers.inscripciones import validar_participante

from app.schemas import Visitante


def crear_participante(
    dni: str = "12345678",
    edad: int = 25,
    talle_vestimenta: str | None = "M",
    nombre: str = "Ana",
) -> Visitante:
    return Visitante(
        nombre=nombre,
        dni=dni,
        edad=edad,
        talle_vestimenta=talle_vestimenta,
    )


def test_validar_participantes() -> None:
    assert callable(validar_participantes)

def test_validar_participante() -> None:
    assert callable(validar_participante)

def test_validar_participantes_acepta_argumentos_esperados() -> None:
    signature(validar_participantes).bind(
        cantidad=1,
        participantes=[crear_participante()],
        actividad=Actividad.SAFARI,
    )

def test_validar_participante_acepta_argumentos_esperados() -> None:
    signature(validar_participante).bind(
        crear_participante(talle_vestimenta="XL")
    )


def test_validar_nombre() -> None:
    participante_01 = Visitante(nombre="", dni="12345678", edad=12)
    participante_02 = Visitante(nombre=" ", dni="00007434", edad=12)
    participante_03 = Visitante(nombre="-", dni="00078678", edad=12)
    participante_04 = Visitante(nombre=". Luis", dni="00003478", edad=12)
    participante_05 = Visitante(nombre="123 - Yonaguni", dni="00786334", edad=12)
    participante_06 = Visitante(nombre="Luis", dni="00009345", edad=12)
    participante_07 = Visitante(nombre="Luis Yonaguni", dni="00000487", edad=12)

    assert validar_participante(participante_01) is False
    assert validar_participante(participante_02) is False
    assert validar_participante(participante_03) is False
    assert validar_participante(participante_04) is False
    assert validar_participante(participante_05) is False
    assert validar_participante(participante_06) is True
    assert validar_participante(participante_07) is True

def test_validar_talles_vestimenta() -> None:
    participante_01 = Visitante(nombre="Pepe Bonaventura", dni="12345678", edad=28)
    participante_02 = Visitante(nombre="Pepe Bonaventura", dni="00004789", edad=28, talle_vestimenta="")
    participante_03 = Visitante(nombre="Pepe Bonaventura", dni="00000416", edad=28, talle_vestimenta="De niño")
    participante_04 = Visitante(nombre="Pepe Bonaventura", dni="00789674", edad=28, talle_vestimenta="XXXL")
    participante_05 = Visitante(nombre="Pepe Bonaventura", dni="00045678", edad=28, talle_vestimenta="XL")
    participante_06 = Visitante(nombre="Pepe Bonaventura", dni="00067864", edad=28, talle_vestimenta="M")

    assert validar_participante(participante_01) is True
    assert validar_participante(participante_02) is False
    assert validar_participante(participante_03) is False
    assert validar_participante(participante_04) is False
    assert validar_participante(participante_05) is True
    assert validar_participante(participante_06) is True

@pytest.mark.parametrize("edad, esperado", [
    (-1, False),
    (0, False),
    (1, True),
    (99, True),
    (100, True),
    (101, False),
])
def test_validar_edad_participante(edad: int, esperado: bool) -> None:
    assert validar_participante(crear_participante(edad=edad)) is esperado


def test_validar_cantidad_valida() -> None:
    participante_01 = crear_participante()
    participante_02 = crear_participante(dni="00006787")

    actividad_safari = Actividad.SAFARI

    assert validar_participantes(0, [], actividad_safari) is False
    assert validar_participantes(-1, [], actividad_safari) is False
    assert validar_participantes(1, [participante_01], actividad_safari) is True
    assert validar_participantes(2, [participante_01, participante_02],actividad_safari ) is True

def test_validar_cantidad_con_participantes_ingresados() -> None:
    participante_01 = crear_participante()
    participante_02 =crear_participante(dni="00006777")

    actividad_safari = Actividad.SAFARI

    assert validar_participantes(1, [], actividad_safari) is False
    assert validar_participantes(1, [participante_01], actividad_safari) is True
    assert validar_participantes(1, [participante_01, participante_02], actividad_safari) is False
    assert validar_participantes(3, [participante_01, participante_02], actividad_safari) is False
    assert validar_participantes(2, [participante_01, participante_02], actividad_safari) is True

def test_validar_actividad_segun_talle_requerido() -> None:
    participante = crear_participante()


    actividad_safari = Actividad.SAFARI
    actividad_tirolesa = Actividad.TIROLESA
    actividad_jardineria = Actividad.JARDINERIA
    actividad_palestra = Actividad.PALESTRA

    assert validar_participantes(1, [participante], actividad_safari) is True
    assert validar_participantes(1, [participante], actividad_tirolesa) is True
    assert validar_participantes(1, [participante], actividad_jardineria) is True
    assert validar_participantes(1, [participante], actividad_palestra) is True

@pytest.mark.parametrize("dni, esperado", [
    ("44444444", True),
    ("01234567", True),
    ("99999999", True),
    ("00000000", False),
    ("", False),
    ("1234567", False),
    ("123456789", False),
    ("12.345.678", False),
    ("1234 5678", False),
    ("1234567A", False),
    (" 12345678", False),
    ("²", False),
    ("²²²²²²²²", False),
])
def test_validar_dni_participante(dni: str, esperado: bool) -> None:
    assert validar_dni_participante(dni) is esperado

def test_validar_cantidad_no_supera_cupo_de_actividad() -> None:
    actividad_safari = Actividad.SAFARI
    participantes = [
        crear_participante(dni=str(10_000_000 + i))
        for i in range(9)
    ]
    assert validar_participantes(8, participantes[:8], actividad_safari) is True
    assert validar_participantes(9, participantes, actividad_safari) is False


def test_rechaza_grupo_si_el_segundo_participante_es_invalido() -> None:
    participantes = [
        crear_participante(dni="12345678"),
        crear_participante(dni="23456789", nombre=""),
    ]

    assert validar_participantes(2, participantes, Actividad.SAFARI) is False
