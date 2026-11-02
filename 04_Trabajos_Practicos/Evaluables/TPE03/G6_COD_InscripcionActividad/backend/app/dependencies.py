import os
from pathlib import Path

from app.services.email_service import ServicioNotificaciones
from app.services.reservas import GestorReservas

_gestor_reservas_instance = None


def get_gestor_reservas() -> GestorReservas:
    """Gestor persistente compartido por la aplicación; la inicialización es diferida."""
    global _gestor_reservas_instance
    if _gestor_reservas_instance is None:
        ruta = os.getenv("RESERVAS_DB_PATH") or Path(__file__).resolve().parents[1] / "data" / "reservas.sqlite3"
        _gestor_reservas_instance = GestorReservas(ruta_db=ruta)
    return _gestor_reservas_instance


def reset_gestor_reservas() -> GestorReservas:
    """Reinicia la instancia de GestorReservas (utilizado principalmente para pruebas)."""
    global _gestor_reservas_instance
    if _gestor_reservas_instance is not None:
        _gestor_reservas_instance.cerrar()
    _gestor_reservas_instance = GestorReservas()
    return _gestor_reservas_instance


def get_servicio_notificaciones() -> ServicioNotificaciones:
    """El SMTP se configura al enviar para no bloquear la reserva si falta configuración."""
    return ServicioNotificaciones()
