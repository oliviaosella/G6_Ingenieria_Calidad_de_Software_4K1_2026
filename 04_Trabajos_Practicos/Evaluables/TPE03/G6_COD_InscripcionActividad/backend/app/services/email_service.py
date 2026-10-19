from .qr_service import generar_qr
import smtplib
from email.message import EmailMessage
import os
from pathlib import Path
from dotenv import load_dotenv


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
    return f"""INSCRIPCION CONFIRMADA A ACTIVIDAD: \n- Id inscripción: {inscripcion['id']} \n- Actividad: {inscripcion['actividad']}\n- Fecha: {inscripcion['fecha']} \n- Horario: {inscripcion['horario']}\nParticipantes: {inscripcion.get('participantes', [])}\n"""


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


_RUTA_ENV = Path(__file__).resolve().parents[2] / ".env"

def _crear_emisor_correo() -> CorreoSMTP:
    load_dotenv(_RUTA_ENV)
    return CorreoSMTP(
        host=os.environ["SMTP_HOST"],
        puerto=int(os.getenv("SMTP_PORT", "587")),
        usuario=os.environ["SMTP_USER"],
        contrasena=os.environ["SMTP_PASSWORD"],
        remitente=os.getenv("SMTP_FROM", os.environ["SMTP_USER"]),
        usar_tls=os.getenv("SMTP_USE_TLS", "true").lower() == "true",
    )


def enviar_confirmacion(inscripcion: dict) -> None:
    servicio = ServicioNotificaciones(emisor_correo=_crear_emisor_correo())
    servicio.enviar_confirmacion(inscripcion)