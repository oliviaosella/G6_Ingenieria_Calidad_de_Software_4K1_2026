from app.services.confirmacion import NotificadorConfirmacion


def obtener_notificador() -> NotificadorConfirmacion:
    """Único punto donde se eligen los adaptadores reales de correo y horarios."""
    raise NotImplementedError
