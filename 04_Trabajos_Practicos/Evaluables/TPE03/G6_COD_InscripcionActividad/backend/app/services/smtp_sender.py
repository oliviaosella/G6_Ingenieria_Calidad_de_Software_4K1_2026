import os
import smtplib
from email.message import EmailMessage


class EmisorSMTP:
    def __init__(self) -> None:
        self.host = os.environ["SMTP_HOST"]
        self.port = int(os.environ.get("SMTP_PORT", "587"))
        self.usuario = os.environ["SMTP_USER"]
        self.contrasena = os.environ["SMTP_PASSWORD"]
        self.remitente = os.environ.get("SMTP_FROM", self.usuario)

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

        with smtplib.SMTP(self.host, self.port) as servidor:
            servidor.starttls()
            servidor.login(self.usuario, self.contrasena)
            servidor.send_message(mensaje)