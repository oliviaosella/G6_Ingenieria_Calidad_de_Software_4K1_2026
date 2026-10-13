class ServicioCorreoError(Exception):
    """Falló un intento de envío en el proveedor de correo."""


class ServicioCorreoNoDisponibleError(Exception):
    """Se agotaron los intentos de envío del correo de confirmación."""
