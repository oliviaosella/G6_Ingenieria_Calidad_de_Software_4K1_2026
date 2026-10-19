from .qr_service import generar_qr
import smtplib
from email.message import EmailMessage


class ServicioNotificaciones:
    def __init__(self, emisor_correo):
        self.emisor_correo = emisor_correo

    def enviar_confirmacion(self, inscripcion: dict) -> None:
        self.emisor_correo.enviar(
            destinatario=inscripcion['email'],
            asunto="Confirmación de inscripción",
            contenido=preparar_resumen(inscripcion),
            qr=generar_qr(inscripcion)
        )


def preparar_resumen(inscripcion):
    return f"""INSCRIPCION CONFIRMADA A ACTIVIDAD \n
                Id inscripción: {inscripcion['id']} - Actividad: {inscripcion['actividad']}\n
                Fecha: {inscripcion['fecha']} - Horario: {inscripcion['horario']}\n
                Inscriptos: {inscripcion.get('participantes', [])}\n"""


def enviar_confirmacion(inscripcion):
    return inscripcion['email']


class CorreoSMTP:
    def __init__(
        self,
        host: str,
        puerto: int,
        usuario: str,
        contrasena: str,
        remitente: str,
        usar_tls: bool = True,
    ) -> None:
        self.host = host
        self.puerto = puerto
        self.usuario = usuario
        self.contrasena = contrasena
        self.remitente = remitente
        self.usar_tls = usar_tls

    def enviar(
        self,
        destinatario: str,
        asunto: str,
        contenido: str,
        qr: bytes,
    ) -> None:
        mensaje = EmailMessage()
        mensaje["From"] = self.remitente
        mensaje["To"] = destinatario
        mensaje["Subject"] = asunto
        mensaje.set_content(contenido)
        mensaje.add_attachment(
            qr,
            maintype="image",
            subtype="png",
            filename="inscripcion-qr.png",
        )

        with smtplib.SMTP(self.host, self.puerto, timeout=10) as servidor:
            if self.usar_tls:
                servidor.starttls()
            servidor.login(self.usuario, self.contrasena)
            servidor.send_message(mensaje)