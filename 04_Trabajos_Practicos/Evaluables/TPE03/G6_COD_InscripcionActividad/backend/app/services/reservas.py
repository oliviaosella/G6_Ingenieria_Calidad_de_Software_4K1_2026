CAPACIDADES_INICIALES: dict[str, int] = {
    "Tirolesa": 10,
    "Safari": 8,
    "Palestra": 12,
    "Jardinería": 12,
}


class GestorReservas:
    def obtener_capacidad_inicial(self, actividad: str) -> int | None:
        return CAPACIDADES_INICIALES.get(actividad)
