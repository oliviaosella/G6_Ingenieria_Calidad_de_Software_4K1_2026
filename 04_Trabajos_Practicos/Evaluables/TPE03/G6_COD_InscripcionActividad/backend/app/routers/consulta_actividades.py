from datetime import date, datetime, time, timedelta
from zoneinfo import ZoneInfo

from fastapi import APIRouter, Depends, HTTPException

from ..schemas import HorarioDisponible
from app.dependencies import get_gestor_reservas
from app.services.reservas import GestorReservas

router = APIRouter(prefix="/actividades", tags=["actividades"])


def obtener_hora_actual() -> datetime:
    return datetime.now(ZoneInfo("America/Argentina/Cordoba")).replace(tzinfo=None)


def consultar_actividades() -> list[dict]:
    return listar_actividades()


@router.get(
    "/{actividad}/turnos",
    response_model=list[HorarioDisponible],
    response_model_exclude_unset=True,
)
def consultar_turnos(
    actividad: str, fecha: date,
    gestor: GestorReservas = Depends(get_gestor_reservas),
) -> list[dict]:
    try:
        return turnos_con_cupos(actividad, fecha, gestor)
    except ActividadNoExisteError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error


def turnos_con_cupos(actividad: str, fecha: date, gestor: GestorReservas) -> list[dict]:
    def consultar_ocupados(actividad, fecha, hora):
        capacidad = obtener_actividad(actividad)["cupo_maximo"]
        horario_id = int(hora[:2]) - 8
        return capacidad - gestor.consultar_cupos(actividad, horario_id, fecha.isoformat())

    return listar_turnos(
        actividad=actividad, fecha=fecha,
        consultar_ocupados=consultar_ocupados,
        hora_actual=obtener_hora_actual(),
    )


class ActividadNoExisteError(ValueError):
    pass


def listar_actividades():
    return [
        {"nombre": "Tirolesa", "cupo_maximo": 10},
        {"nombre": "Safari", "cupo_maximo": 8},
        {"nombre": "Palestra", "cupo_maximo": 12},
        {"nombre": "Jardinería", "cupo_maximo": 12},
    ]


def obtener_actividad(nombre):
    for actividad in listar_actividades():
        if actividad["nombre"] == nombre:
            return actividad

    raise ActividadNoExisteError(
        f"La actividad '{nombre}' no existe"
    )


def listar_turnos(
    actividad,
    fecha: date,
    consultar_ocupados=None,
    hora_actual: datetime | None = None,
):
    obtener_actividad(actividad)

    if fecha.weekday() == 0 or (
        (fecha.month == 12 and fecha.day == 25)
        or (fecha.month == 1 and fecha.day == 1)
    ):
        return []
    turnos = []

    for hora_numero in range(9, 18):
        hora = f"{hora_numero:02d}:00"

        if hora_actual is not None:
            inicio_turno = datetime.combine(
                fecha,
                time(hora_numero, 0),
            )

            tiempo_hasta_el_turno = inicio_turno - hora_actual

            if (
                tiempo_hasta_el_turno < timedelta(minutes=15)
                or tiempo_hasta_el_turno > timedelta(hours=24)
            ):
                continue

        turno = {
            "actividad": actividad,
            "fecha": fecha.isoformat(),
            "hora": hora,
        }


        if consultar_ocupados is not None:
            cupos = consultar_cupos_turno(
                actividad=actividad,
                fecha=fecha,
                hora=hora,
                consultar_ocupados=consultar_ocupados,
            )

            turno["cupos_disponibles"] = cupos
            turno["disponible"] = cupos > 0
            turno["motivo"] = "sin cupos" if cupos == 0 else None

        horario = HorarioDisponible(**turno)
        turnos.append(horario.model_dump(mode="json", exclude_unset=True))

    return turnos


def consultar_cupos(actividad, ocupados):
    datos_actividad = obtener_actividad(actividad)

    return datos_actividad["cupo_maximo"] - ocupados

def consultar_cupos_turno(
    actividad,
    fecha,
    hora,
    consultar_ocupados,
):
    ocupados = consultar_ocupados(actividad, fecha, hora)

    return consultar_cupos(actividad, ocupados)
