def calcular_cupos_disponibles(cupos_totales, inscriptos):
    return cupos_totales - inscriptos

def puede_reservar(cupos_totales, inscriptos, cantidad_reservar):
    if (cantidad_reservar <= 0):
        return False
    else:
        disponibles = calcular_cupos_disponibles(cupos_totales, inscriptos)
        return 0 < cantidad_reservar <= disponibles

def actualizar(cupos_totales, inscriptos, cantidad_reservar):
    disponibles = calcular_cupos_disponibles(cupos_totales, inscriptos)
    if puede_reservar(cupos_totales, inscriptos, cantidad_reservar):
        return disponibles - cantidad_reservar
    return disponibles


