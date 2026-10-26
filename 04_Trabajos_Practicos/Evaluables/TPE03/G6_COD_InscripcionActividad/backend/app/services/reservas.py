from contextlib import contextmanager
from datetime import datetime, timedelta, timezone
import json
from pathlib import Path
import sqlite3
import threading

CAPACIDADES_INICIALES = {"Tirolesa": 10, "Safari": 8, "Palestra": 12, "Jardinería": 12}


class GestorReservas:
    """SQLite transaccional; por defecto aislado en memoria para los tests unitarios."""

    def __init__(self, ruta_db: str | Path | None = None) -> None:
        self._lock = threading.RLock()
        if ruta_db is not None and str(ruta_db) != ":memory:":
            Path(ruta_db).parent.mkdir(parents=True, exist_ok=True)
        self._db = sqlite3.connect(str(ruta_db or ":memory:"), timeout=15, check_same_thread=False, isolation_level=None)
        if ruta_db is not None and str(ruta_db) != ":memory:":
            self._db.execute("PRAGMA journal_mode=WAL")
        self._db.executescript("""
            CREATE TABLE IF NOT EXISTS cupos (
                actividad TEXT NOT NULL, fecha TEXT NOT NULL, horario_id INTEGER NOT NULL,
                disponibles INTEGER NOT NULL CHECK(disponibles >= 0),
                PRIMARY KEY (actividad, fecha, horario_id)
            );
            CREATE TABLE IF NOT EXISTS reservas (
                id INTEGER PRIMARY KEY AUTOINCREMENT, datos TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS dnis (
                fecha TEXT NOT NULL, horario_id INTEGER NOT NULL, dni TEXT NOT NULL,
                PRIMARY KEY (fecha, horario_id, dni)
            );
        """)

    def cerrar(self) -> None:
        with self._lock:
            self._db.close()

    @contextmanager
    def _transaccion(self):
        with self._lock:
            self._db.execute("BEGIN IMMEDIATE")
            try:
                yield
                self._db.commit()
            except Exception:
                self._db.rollback()
                raise

    def obtener_capacidad_inicial(self, actividad: str) -> int:
        return CAPACIDADES_INICIALES.get(actividad, 0)

    def _consultar_cupos_sin_lock(self, actividad, horario_id, fecha=None):
        fila = self._db.execute(
            "SELECT disponibles FROM cupos WHERE actividad=? AND fecha=? AND horario_id=?",
            (actividad, fecha or "", horario_id),
        ).fetchone()
        return fila[0] if fila else self.obtener_capacidad_inicial(actividad)

    def consultar_cupos(self, actividad: str, horario_id: int, fecha: str | None = None) -> int:
        with self._lock:
            return self._consultar_cupos_sin_lock(actividad, horario_id, fecha)

    def puede_reservar(self, actividad, horario_id, cantidad, fecha=None) -> bool:
        return 0 < cantidad <= self.consultar_cupos(actividad, horario_id, fecha)

    def _reservar_sin_lock(self, actividad, horario_id, cantidad, fecha=None):
        disponibles = self._consultar_cupos_sin_lock(actividad, horario_id, fecha)
        if not 0 < cantidad <= disponibles:
            return False
        self._db.execute(
            "INSERT INTO cupos VALUES (?, ?, ?, ?) "
            "ON CONFLICT(actividad, fecha, horario_id) DO UPDATE SET disponibles=excluded.disponibles",
            (actividad, fecha or "", horario_id, disponibles - cantidad),
        )
        return True

    def reservar(self, actividad, horario_id, cantidad, fecha=None) -> bool:
        with self._transaccion():
            return self._reservar_sin_lock(actividad, horario_id, cantidad, fecha)

    @property
    def proximo_id(self) -> int:
        with self._lock:
            return self._db.execute("SELECT COALESCE(MAX(id), 0) + 1 FROM reservas").fetchone()[0]

    def obtener_proximo_id(self) -> int:
        return self.proximo_id

    def dni_esta_inscripto(self, horario_id, dni, fecha=None) -> bool:
        with self._lock:
            return self._db.execute(
                "SELECT 1 FROM dnis WHERE fecha=? AND horario_id=? AND dni=?",
                (fecha or "", horario_id, dni),
            ).fetchone() is not None

    def _obtener_sin_lock(self, reserva_id):
        fila = self._db.execute("SELECT datos FROM reservas WHERE id=?", (reserva_id,)).fetchone()
        return json.loads(fila[0]) if fila else None

    def obtener_reserva(self, reserva_id: int) -> dict | None:
        with self._lock:
            return self._obtener_sin_lock(reserva_id)

    def _guardar_sin_lock(self, reserva):
        self._db.execute(
            "UPDATE reservas SET datos=? WHERE id=?",
            (json.dumps(reserva, ensure_ascii=False), reserva["id"]),
        )

    def crear_reserva(self, actividad, horario_id, participantes, cantidad_declarada=None, fecha=None, datos_adicionales=None):
        cantidad = len(participantes)
        if cantidad != (cantidad_declarada if cantidad_declarada is not None else cantidad):
            return None
        dnis = [p["dni"] for p in participantes if p.get("dni")]
        if len(dnis) != len(set(dnis)):
            return None
        with self._transaccion():
            if any(self.dni_esta_inscripto(horario_id, dni, fecha) for dni in dnis):
                return None
            if not self._reservar_sin_lock(actividad, horario_id, cantidad, fecha):
                return None
            cursor = self._db.execute("INSERT INTO reservas(datos) VALUES ('{}')")
            reserva = {
                **(datos_adicionales or {}),
                "id": cursor.lastrowid, "actividad": actividad,
                "horario_id": horario_id, "participantes": participantes,
            }
            if fecha is not None:
                reserva["fecha"] = fecha
            self._db.executemany("INSERT INTO dnis VALUES (?, ?, ?)", [(fecha or "", horario_id, dni) for dni in dnis])
            self._guardar_sin_lock(reserva)
            return json.loads(json.dumps(reserva))

    def iniciar_envio(self, reserva_id: int) -> dict | None:
        """Reclama un envío pendiente/fallido; evita dos reintentos simultáneos."""
        with self._transaccion():
            reserva = self._obtener_sin_lock(reserva_id)
            if reserva is None or reserva.get("correo_estado") == "enviado":
                return None
            ahora = datetime.now(timezone.utc)
            if reserva.get("correo_estado") == "enviando":
                inicio = datetime.fromisoformat(reserva["envio_iniciado_en"])
                if ahora - inicio < timedelta(minutes=5):
                    return None
            reserva.update(correo_estado="enviando", envio_iniciado_en=ahora.isoformat(),
                           intentos_envio=reserva.get("intentos_envio", 0) + 1)
            self._guardar_sin_lock(reserva)
            return reserva

    def finalizar_envio(self, reserva_id, enviado, inicio):
        with self._transaccion():
            reserva = self._obtener_sin_lock(reserva_id)
            if reserva is not None and reserva.get("envio_iniciado_en") == inicio:
                reserva.update(
                    correo_estado="enviado" if enviado else "fallido",
                    correo_error=None if enviado else "No se pudo enviar el correo. La reserva sigue confirmada; puede reintentar el envío.",
                )
                self._guardar_sin_lock(reserva)
            return reserva
