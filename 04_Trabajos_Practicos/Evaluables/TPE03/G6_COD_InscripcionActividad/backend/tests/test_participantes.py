from inspect import signature
from app.routers.inscripciones import validar_participantes
from app.routers.inscripciones import validar_participante

from app.schemas import Actividad, Visitante

def test_validar_participantes() -> None:
    assert callable(validar_participantes)

def test_validar_participante() -> None:
    assert callable(validar_participante)

def test_validar_participantes_acepta_argumentos_esperados():
    signature(validar_participantes).bind(
        cantidad=1,
        participantes=[{"datos": "datos del participante"}],
        actividad=Actividad.SAFARI,
    )

def test_validar_participante_acepta_argumentos_esperados():
    signature(validar_participante).bind({
        "nombre": "Ana",
        "dni": "12345678",
        "edad": 25,
        "talle_vestimenta": "XL"
        })

def test_validar_cantidad_valida():
    participante_01 = { "nombre": "Ana", "dni": "12345678", "edad": 25 }
    participante_02 = { "nombre": "Esteban", "dni": "12345678", "edad": 10 }

    assert validar_participantes(0, [], Actividad.SAFARI) is False
    assert validar_participantes(-1, [], Actividad.SAFARI) is False
    assert validar_participantes(1, [participante_01], Actividad.SAFARI) is True
    assert validar_participantes(2, [participante_01, participante_02], Actividad.SAFARI) is True

def test_validar_cantidad_con_participantes_ingresados():
    participante_01 = { "nombre": "Ana", "dni": "12345678", "edad": 25 }
    participante_02 = { "nombre": "Esteban", "dni": "12345678", "edad": 10 }

    assert validar_participantes(1, [], Actividad.SAFARI) is False
    assert validar_participantes(1, [participante_01], Actividad.SAFARI) is True
    assert validar_participantes(1, [participante_01, participante_02], Actividad.SAFARI) is False
    assert validar_participantes(3, [participante_01, participante_02], Actividad.SAFARI) is False
    assert validar_participantes(2, [participante_01, participante_02], Actividad.SAFARI) is True

def test_validar_nombre():
    participante_01 = Visitante(nombre="", dni="12345678", edad=13)
    participante_02 = Visitante(nombre=" ", dni="12345678", edad=13)
    participante_03 = Visitante(nombre="-", dni="12345678", edad=13)
    participante_04 = Visitante(nombre=". Luis", dni="12345678", edad=13)
    participante_05 = Visitante(nombre="123 - Yonaguni", dni="12345678", edad=13)
    participante_06 = Visitante(nombre="Luis", dni="12345678", edad=13)
    participante_07 = Visitante(nombre="Luis Yonaguni", dni="12345678", edad=13)

    assert validar_participante(participante_01) is False
    assert validar_participante(participante_02) is False
    assert validar_participante(participante_03) is False
    assert validar_participante(participante_04) is False
    assert validar_participante(participante_05) is False
    assert validar_participante(participante_06) is True
    assert validar_participante(participante_07) is True

def test_validar_talles_vestimenta():
    participante_01 = Visitante(nombre="Pepe Bonaventura", dni="12345678", edad=28)
    participante_02 = Visitante(nombre="Pepe Bonaventura", dni="12345678", edad=28, talle_vestimenta="")
    participante_03 = Visitante(nombre="Pepe Bonaventura", dni="12345678", edad=28, talle_vestimenta="De niño")
    participante_04 = Visitante(nombre="Pepe Bonaventura", dni="12345678", edad=28, talle_vestimenta="XXXL")
    participante_05 = Visitante(nombre="Pepe Bonaventura", dni="12345678", edad=28, talle_vestimenta="XL")
    participante_06 = Visitante(nombre="Pepe Bonaventura", dni="12345678", edad=28, talle_vestimenta="M")

    assert validar_participante(participante_01) is True
    assert validar_participante(participante_02) is False
    assert validar_participante(participante_03) is False
    assert validar_participante(participante_04) is False
    assert validar_participante(participante_05) is True
    assert validar_participante(participante_06) is True
