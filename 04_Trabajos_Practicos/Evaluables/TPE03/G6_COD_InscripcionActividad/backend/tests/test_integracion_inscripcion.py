from datetime import date

from app.routers.consulta_actividades import consultar_cupos_turno
from app.routers.inscripciones import validar_participantes
from app.schemas import Actividad, Visitante


def test_rechaza_grupo_si_supera_cupos_del_turno() -> None:
    def consultar_ocupados(actividad, fecha, hora):
        return 6

    cupos = consultar_cupos_turno(
        actividad="Safari",
        fecha=date(2026, 10, 28),
        hora="10:00",
        consultar_ocupados=consultar_ocupados,
    )

    participantes = [
        Visitante(nombre="Ana", dni="12345678", edad=25),
        Visitante(nombre="Luis", dni="23456789", edad=25),
        Visitante(nombre="Eva", dni="34567890", edad=25),
    ]

    resultado = validar_participantes(
        cantidad=3,
        participantes=participantes,
        actividad=Actividad.SAFARI,
        cupos_disponibles=cupos,
    )

    assert resultado is False


def test_acepta_grupo_si_ocupa_exactamente_los_cupos_disponibles() -> None:
    def consultar_ocupados(actividad, fecha, hora):
        return 6

    cupos = consultar_cupos_turno(
        actividad="Safari",
        fecha=date(2026, 10, 28),
        hora="10:00",
        consultar_ocupados=consultar_ocupados,
    )

    participantes = [
        Visitante(nombre="Ana", dni="12345678", edad=25),
        Visitante(nombre="Luis", dni="23456789", edad=25),
    ]

    resultado = validar_participantes(
        cantidad=2,
        participantes=participantes,
        actividad=Actividad.SAFARI,
        cupos_disponibles=cupos,
    )

    assert resultado is True
