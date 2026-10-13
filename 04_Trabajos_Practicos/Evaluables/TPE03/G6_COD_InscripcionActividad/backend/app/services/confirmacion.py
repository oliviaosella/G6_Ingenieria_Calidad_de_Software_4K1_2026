from app.schemas import InscripcionConfirmada
from app.services.correo import ConsultaHorarios, Correo, ServicioCorreo

MAX_INTENTOS = 3
URL_BASE = "http://127.0.0.1:8000"


def url_validacion(inscripcion: InscripcionConfirmada) -> str:
    raise NotImplementedError


def generar_qr(inscripcion: InscripcionConfirmada) -> bytes:
    raise NotImplementedError


class NotificadorConfirmacion:
    def __init__(
        self,
        servicio_correo: ServicioCorreo,
        consulta_horarios: ConsultaHorarios,
    ) -> None:
        self.servicio_correo = servicio_correo
        self.consulta_horarios = consulta_horarios

    def armar_correo(self, inscripcion: InscripcionConfirmada) -> Correo:
        raise NotImplementedError

    def enviar_confirmacion(self, inscripcion: InscripcionConfirmada) -> Correo:
        raise NotImplementedError
