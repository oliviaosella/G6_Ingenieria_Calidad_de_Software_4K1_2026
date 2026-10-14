import pytest
from app.routers.consulta_actividades import *
from datetime import date


def test_muestra_las_actividades_con_sus_cupos():
    resultado = listar_actividades()

    assert resultado == [
        {"nombre": "Tirolesa", "cupo_maximo": 10},
        {"nombre": "Safari", "cupo_maximo": 8},
        {"nombre": "Palestra", "cupo_maximo": 12},
        {"nombre": "Jardinería", "cupo_maximo": 12},
    ]


def test_rechaza_una_actividad_inexistente():
    with pytest.raises(ActividadNoExisteError):
        obtener_actividad("Acuario")


def test_safari_tiene_un_turno_disponible_a_las_diez():
    resultado = listar_turnos(
        actividad="Safari",
        fecha=date(2026, 10, 14),
    )

    assert {
        turno["hora"]
        for turno in resultado
    } >= {"10:00"}