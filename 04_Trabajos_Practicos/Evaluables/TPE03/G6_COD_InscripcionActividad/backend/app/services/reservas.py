class GestorReservas:
    def obtener_capacidad_inicial(self, actividad):
        capacidades = {
            "Tirolesa": 10,
            "Safari": 8,
            "Palestra": 12,
            "Jardinería": 12,
        }
        return capacidades.get(actividad)
