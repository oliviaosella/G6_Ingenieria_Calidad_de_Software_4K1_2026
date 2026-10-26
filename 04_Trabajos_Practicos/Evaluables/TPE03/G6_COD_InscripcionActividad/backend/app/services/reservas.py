import threading

CAPACIDADES_INICIALES: dict[str, int] = {
    "Tirolesa": 10,
    "Safari": 8,
    "Palestra": 12,
    "Jardinería": 12,
}


class GestorReservas:
    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._cupos: dict[tuple[str, str | None, int], int] = {}
        self._next_id: int = 1
        self._dnis_por_horario: dict[tuple[str | None, int], set[str]] = {}
        self._reservas: dict[int, dict] = {}

    def obtener_capacidad_inicial(self, actividad: str) -> int:
        return CAPACIDADES_INICIALES.get(actividad, 0)

    def _consultar_cupos_sin_lock(self, actividad: str, horario_id: int, fecha: str | None = None) -> int:
        clave = (actividad, fecha, horario_id)
        if clave not in self._cupos:
            self._cupos[clave] = self.obtener_capacidad_inicial(actividad)
        return self._cupos[clave]

    def consultar_cupos(self, actividad: str, horario_id: int, fecha: str | None = None) -> int:
        with self._lock:
            return self._consultar_cupos_sin_lock(actividad, horario_id, fecha)

    def puede_reservar(self, actividad: str, horario_id: int, cantidad: int, fecha: str | None = None) -> bool:
        disponibles = self.consultar_cupos(actividad, horario_id, fecha)
        return 0 < cantidad <= disponibles

    def _reservar_sin_lock(self, actividad: str, horario_id: int, cantidad: int, fecha: str | None = None) -> bool:
        clave = (actividad, fecha, horario_id)
        disponibles = self._consultar_cupos_sin_lock(actividad, horario_id, fecha)
        if not (0 < cantidad <= disponibles):
            return False

        self._cupos[clave] = disponibles - cantidad
        return True

    def reservar(self, actividad: str, horario_id: int, cantidad: int, fecha: str | None = None) -> bool:
        with self._lock:
            return self._reservar_sin_lock(actividad, horario_id, cantidad, fecha)

    def _extraer_dnis(self, participantes: list[dict]) -> set[str]:
        return {p["dni"] for p in participantes if p.get("dni")}

    @property
    def proximo_id(self) -> int:
        return self._next_id

    def obtener_proximo_id(self) -> int:
        return self.proximo_id

    def dni_esta_inscripto(self, horario_id: int, dni: str, fecha: str | None = None) -> bool:
        with self._lock:
            return dni in self._dnis_por_horario.get((fecha, horario_id), set())

    def obtener_reserva(self, reserva_id: int) -> dict | None:
        with self._lock:
            reserva = self._reservas.get(reserva_id)
            return dict(reserva) if reserva is not None else None

    def crear_reserva(
        self,
        actividad: str,
        horario_id: int,
        participantes: list[dict],
        cantidad_declarada: int | None = None,
        fecha: str | None = None,
    ) -> dict | None:
        cantidad = len(participantes)
        cantidad_esperada = cantidad_declarada if cantidad_declarada is not None else cantidad

        if cantidad != cantidad_esperada:
            return None

        dnis_solicitud = self._extraer_dnis(participantes)

        with self._lock:
            clave_turno = (fecha, horario_id)
            dnis_existentes = self._dnis_por_horario.get(clave_turno, set())

            # Validación atómica de no superposición de DNIs en el turno
            if dnis_solicitud & dnis_existentes:
                return None

            # Descuento atómico de cupos
            if not self._reservar_sin_lock(actividad, horario_id, cantidad, fecha):
                return None

            # Persistencia de DNIs y emisión del ticket de reserva
            self._dnis_por_horario.setdefault(clave_turno, set()).update(dnis_solicitud)

            reserva_id = self._next_id
            reserva = {
                "id": reserva_id,
                "actividad": actividad,
                "horario_id": horario_id,
                "participantes": list(participantes),
            }
            if fecha is not None:
                reserva["fecha"] = fecha
            self._reservas[reserva_id] = reserva
            self._next_id += 1
            return dict(reserva)
