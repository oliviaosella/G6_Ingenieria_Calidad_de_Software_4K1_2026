import pytest
from app.routers.consulta_actividades import *
from datetime import date
from app.routers import consulta_actividades as modulo

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

    
def test_safari_tiene_un_turno_a_las_nueve():
    resultado = listar_turnos(
        actividad="Safari",
        fecha=date(2026, 10, 14),
    )

    assert {
        turno["hora"]
        for turno in resultado
    } >= {"09:00"}


def test_safari_tiene_un_turno_a_las_diecisiete():
    resultado = listar_turnos(
        actividad="Safari",
        fecha=date(2026, 10, 14),
    )

    assert {
        turno["hora"]
        for turno in resultado
    } >= {"17:00"}


def test_safari_no_tiene_un_turno_a_las_dieciocho():
    resultado = listar_turnos(
        actividad="Safari",
        fecha=date(2026, 10, 14),
    )

    assert "18:00" not in {
        turno["hora"]
        for turno in resultado
    }


def test_no_hay_turnos_los_lunes():
    resultado = listar_turnos(
        actividad="Safari",
        fecha=date(2026, 10, 19),
    )

    assert resultado == []

def test_safari_con_tres_cupos_ocupados_muestra_cinco_disponibles():
    # Preparar: Safari tiene 8 lugares y 3 ya están ocupados.
    # El número de ocupados simula el dato recibido del grupo 5.
    ocupados = 3

    # Actuar: consultar los lugares restantes.
    resultado = modulo.consultar_cupos(
        actividad="Safari",
        ocupados=ocupados,
    )

    # Verificar: quedan 8 - 3 = 5 lugares.
    assert resultado == 5

def test_consulta_cupos_de_un_turno_especifico():
    # Preparar: el servicio simulado informa ocupados por turno.
    ocupados_por_turno = {
        ("Safari", date(2026, 10, 14), "10:00"): 3,
    }

    def consultar_ocupados_simulado(actividad, fecha, hora):
        return ocupados_por_turno.get((actividad, fecha, hora), 0)

    # Actuar: consultar Safari para esa fecha y hora.
    resultado = modulo.consultar_cupos_turno(
        actividad="Safari",
        fecha=date(2026, 10, 14),
        hora="10:00",
        consultar_ocupados=consultar_ocupados_simulado,
    )

    # Verificar: Safari tiene 8 lugares y quedan 5.
    assert resultado == 5