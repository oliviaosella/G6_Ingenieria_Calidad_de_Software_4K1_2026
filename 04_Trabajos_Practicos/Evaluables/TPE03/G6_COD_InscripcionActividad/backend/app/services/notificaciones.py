import logging

from .email_service import ServicioNotificaciones
from .reservas import GestorReservas

logger = logging.getLogger(__name__)


def procesar_envio(reserva_id: int, gestor: GestorReservas, servicio: ServicioNotificaciones) -> dict | None:
    reserva = gestor.iniciar_envio(reserva_id)
    if reserva is None:
        return gestor.obtener_reserva(reserva_id)
    enviado = False
    try:
        servicio.enviar_confirmacion(reserva)
        enviado = True
    except Exception as error:
        # El proveedor puede fallar después del commit. No se expone su mensaje
        # (podría contener credenciales) ni se repite el descuento de cupos.
        logger.warning("Envío de reserva %s pendiente por %s", reserva_id, type(error).__name__)
    return gestor.finalizar_envio(reserva_id, enviado, reserva["envio_iniciado_en"])
