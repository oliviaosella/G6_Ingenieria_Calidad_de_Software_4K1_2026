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

    turnos = [
        {
            "actividad": actividad,
            "fecha": fecha.isoformat(),
            "hora": "09:00",
        },
        {
            "actividad": actividad,
            "fecha": fecha.isoformat(),
            "hora": "10:00",
        },
        {
            "actividad": actividad,
            "fecha": fecha.isoformat(),
            "hora": "17:00",
        },
    ]

    if consultar_ocupados is not None:
        for turno in turnos:
            turno["cupos_disponibles"] = consultar_cupos_turno(
                actividad=actividad,
                fecha=fecha,
                hora=turno["hora"],
                consultar_ocupados=consultar_ocupados,
            )

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