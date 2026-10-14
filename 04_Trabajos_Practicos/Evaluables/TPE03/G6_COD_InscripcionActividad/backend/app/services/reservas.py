CAPACIDADES_INICIALES: dict[str, int] = {
    "Tirolesa": 10,
    "Safari": 8,
    "Palestra": 12,
    "Jardinería": 12,
}


class GestorReservas:
    def __init__(self) -> None:
        self._cupos: dict[tuple[str, int], int] = {}
        self._next_id: int = 1

    def obtener_capacidad_inicial(self, actividad: str) -> int:
        return CAPACIDADES_INICIALES.get(actividad, 0)

    def consultar_cupos(self, actividad: str, horario_id: int) -> int:
        clave = (actividad, horario_id)
        if clave not in self._cupos:
            self._cupos[clave] = self.obtener_capacidad_inicial(actividad)
        return self._cupos[clave]

    def puede_reservar(self, actividad: str, horario_id: int, cantidad: int) -> bool:
        disponibles = self.consultar_cupos(actividad, horario_id)
        return 0 < cantidad <= disponibles

    def reservar(self, actividad: str, horario_id: int, cantidad: int) -> bool:
        if not self.puede_reservar(actividad, horario_id, cantidad):
            return False

        clave = (actividad, horario_id)
        cupos_actuales = self.consultar_cupos(actividad, horario_id)
        self._cupos[clave] = cupos_actuales - cantidad
        return True

    def crear_reserva(
        self,
        actividad: str,
        horario_id: int,
        participantes: list[dict],
    ) -> dict | None:
        cantidad = len(participantes)
        if not self.reservar(actividad, horario_id, cantidad):
            return None

        reserva = {
            "id": self._next_id,
            "actividad": actividad,
            "horario_id": horario_id,
            "participantes": list(participantes),
        }
        self._next_id += 1
        return reserva
