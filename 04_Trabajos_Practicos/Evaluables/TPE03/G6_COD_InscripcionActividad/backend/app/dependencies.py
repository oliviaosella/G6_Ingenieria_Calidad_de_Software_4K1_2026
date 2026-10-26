from app.services.email_service import ServicioNotificaciones, _crear_emisor_correo
from app.services.reservas import GestorReservas

_gestor_reservas_instance = GestorReservas()


def get_gestor_reservas() -> GestorReservas:
    """Retorna la instancia Singleton compartida de GestorReservas."""
    return _gestor_reservas_instance


def reset_gestor_reservas() -> GestorReservas:
    """Reinicia la instancia de GestorReservas (utilizado principalmente para pruebas)."""
    global _gestor_reservas_instance
    _gestor_reservas_instance = GestorReservas()
    return _gestor_reservas_instance


def get_servicio_notificaciones() -> ServicioNotificaciones:
    """Retorna el servicio de notificaciones con emisor SMTP estricto según .env."""
    emisor = _crear_emisor_correo()
    return ServicioNotificaciones(emisor_correo=emisor)
