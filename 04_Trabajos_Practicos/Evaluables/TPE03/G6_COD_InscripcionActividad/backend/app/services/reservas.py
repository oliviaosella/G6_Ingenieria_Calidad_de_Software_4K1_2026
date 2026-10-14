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
        self._dnis_por_horario: dict[int, set[str]] = {}

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

    def _extraer_dnis(self, participantes: list[dict]) -> set[str]:
        return {p["dni"] for p in participantes if p.get("dni")}

    def crear_reserva(
        self,
        actividad: str,
        horario_id: int,
        participantes: list[dict],
        cantidad_declarada: int | None = None,
    ) -> dict | None:
        cantidad = len(participantes)
        cantidad_esperada = cantidad_declarada if cantidad_declarada is not None else cantidad

        if cantidad != cantidad_esperada:
            return None

        dnis_solicitud = self._extraer_dnis(participantes)
        dnis_existentes = self._dnis_por_horario.get(horario_id, set())

        # Si hay intersección de DNIs, existe superposición en el mismo horario
        if dnis_solicitud & dnis_existentes:
            return None

        if not self.reservar(actividad, horario_id, cantidad):
            return None

        self._dnis_por_horario.setdefault(horario_id, set()).update(dnis_solicitud)

        reserva = {
            "id": self._next_id,
            "actividad": actividad,
            "horario_id": horario_id,
            "participantes": list(participantes),
        }
        self._next_id += 1
        return reserva
