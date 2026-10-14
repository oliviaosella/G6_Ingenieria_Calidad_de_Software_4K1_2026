CAPACIDADES_INICIALES: dict[str, int] = {
    "Tirolesa": 10,
    "Safari": 8,
    "Palestra": 12,
    "Jardinería": 12,
}


class GestorReservas:
    def __init__(self) -> None:
        self._cupos: dict[tuple[str, int], int] = {}

    def obtener_capacidad_inicial(self, actividad: str) -> int:
        return CAPACIDADES_INICIALES.get(actividad, 0)

    def consultar_cupos(self, actividad: str, horario_id: int) -> int:
        clave = (actividad, horario_id)
        if clave not in self._cupos:
            self._cupos[clave] = self.obtener_capacidad_inicial(actividad)
        return self._cupos[clave]

    def reservar(self, actividad: str, horario_id: int, cantidad: int) -> bool:
        cupos_actuales = self.consultar_cupos(actividad, horario_id)
        self._cupos[(actividad, horario_id)] = cupos_actuales - cantidad
        return True
