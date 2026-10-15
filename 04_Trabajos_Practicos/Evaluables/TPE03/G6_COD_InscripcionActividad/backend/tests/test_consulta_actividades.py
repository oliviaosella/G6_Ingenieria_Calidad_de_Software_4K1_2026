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
        return ocupados_por_turno.get(
            (actividad, fecha, hora),
            0,
        )
    # Actuar: consultar Safari para esa fecha y hora.
    resultado = modulo.consultar_cupos_turno(
        actividad="Safari",
        fecha=date(2026, 10, 14),
        hora="10:00",
        consultar_ocupados=consultar_ocupados_simulado,
    )

    # Verificar: Safari tiene 8 lugares y quedan 5.
    assert resultado == 5

def test_lista_turnos_con_sus_cupos_disponibles():
    # Preparar: cada turno de Safari tiene distinta ocupacion.
    fecha = date(2026, 10, 14)

    ocupados_por_turno = {
        ("Safari", fecha, "09:00"): 2,
        ("Safari", fecha, "10:00"): 3,
        ("Safari", fecha, "17:00"): 0,
    }

    def consultar_ocupados_simulado(actividad, fecha, hora):
        return ocupados_por_turno.get(
            (actividad, fecha, hora),
            0,
        )

    # Actuar: listar turnos usando el servicio simulado.
    resultado = modulo.listar_turnos(
        actividad="Safari",
        fecha=fecha,
        consultar_ocupados=consultar_ocupados_simulado,
    )

    # Verificar: los ocupados de un turno no afectan a los otros.
    cupos_por_hora = {
        turno["hora"]: turno["cupos_disponibles"]
        for turno in resultado
    }

    assert cupos_por_hora == {
        "09:00": 6,
        "10:00": 5,
        "11:00": 8,
        "12:00": 8,
        "13:00": 8,
        "14:00": 8,
        "15:00": 8,
        "16:00": 8,
        "17:00": 8,
    }

#Turno lleno
def test_turno_lleno_informa_sin_cupos_y_no_esta_disponible():
    fecha = date(2026, 10, 14)

    ocupados_por_turno = {
        ("Safari", fecha, "10:00"): 8,
    }

    def consultar_ocupados_simulado(actividad, fecha, hora):
        return ocupados_por_turno.get(
            (actividad, fecha, hora),
            0,
        )

    resultado = modulo.listar_turnos(
        actividad="Safari",
        fecha=fecha,
        consultar_ocupados=consultar_ocupados_simulado,
    )

    turno_lleno = next(
        turno for turno in resultado
        if turno["hora"] == "10:00"
    )

    assert turno_lleno["cupos_disponibles"] == 0
    assert turno_lleno["disponible"] is False
    assert turno_lleno["motivo"] == "sin cupos"

def test_hay_un_turno_por_hora_entre_las_nueve_y_las_diecisiete():
    resultado = listar_turnos(
        actividad="Safari",
        fecha=date(2026, 10, 14),
    )

    horas = {turno["hora"] for turno in resultado}

    assert horas == {
        "09:00",
        "10:00",
        "11:00",
        "12:00",
        "13:00",
        "14:00",
        "15:00",
        "16:00",
        "17:00",
    }

def test_no_hay_turnos_el_25_de_diciembre():
    resultado = listar_turnos(
        actividad="Safari",
        fecha=date(2026, 12, 25),
    )

    assert resultado == []


def test_no_hay_turnos_el_1_de_enero():
    resultado = listar_turnos(
        actividad="Safari",
        fecha=date(2027, 1, 1),
    )

    assert resultado == []