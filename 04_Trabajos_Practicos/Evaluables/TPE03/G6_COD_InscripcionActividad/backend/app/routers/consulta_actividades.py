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