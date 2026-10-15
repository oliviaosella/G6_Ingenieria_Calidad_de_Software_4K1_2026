from datetime import date

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
):
    obtener_actividad(actividad)

    if fecha.weekday() == 0:
        return []

    turnos = []

    for hora_numero in range(9, 18):
        hora = f"{hora_numero:02d}:00"

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

        turnos.append(turno)

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