import pytest
from app.routers.consulta_actividades import listar_actividades
from app.routers.consulta_actividades import (
    ActividadNoExisteError,
    obtener_actividad,
)

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