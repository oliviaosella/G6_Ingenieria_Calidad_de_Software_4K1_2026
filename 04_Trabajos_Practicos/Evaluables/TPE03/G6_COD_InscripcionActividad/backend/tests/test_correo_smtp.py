import smtplib

from app.services.email_service import CorreoSMTP


class SMTPFalso:
    instancias = []

    def __init__(self, host: str, port: int, timeout: float | None = None) -> None:
        self.host = host
        self.port = port
        self.timeout = timeout
        self.llamadas = []
        self.credenciales = None
        self.mensaje = None
        SMTPFalso.instancias.append(self)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def starttls(self, *args, **kwargs) -> None:
        self.llamadas.append("starttls")

    def login(self, usuario: str, contrasena: str) -> None:
        self.llamadas.append("login")
        self.credenciales = (usuario, contrasena)

    def send_message(self, mensaje) -> None:
        self.llamadas.append("send_message")
        self.mensaje = mensaje


def test_correo_smtp_envia_resumen_y_adjunta_qr(monkeypatch) -> None:
    SMTPFalso.instancias.clear()
    monkeypatch.setattr(smtplib, "SMTP", SMTPFalso)

    emisor = CorreoSMTP(
        host="smtp.gmail.com",
        puerto=587,
        usuario="cuenta@gmail.com",
        contrasena="app-password",
        remitente="cuenta@gmail.com",
    )

    qr = b"\x89PNG\r\n\x1a\nqr-de-prueba"
    emisor.enviar(
        destinatario="visitante@gmail.com",
        asunto="Confirmación de inscripción",
        contenido="Inscripción: 125 - Actividad: Tirolesa",
        qr=qr,
    )

    servidor = SMTPFalso.instancias[0]
    assert servidor.host == "smtp.gmail.com"
    assert servidor.port == 587
    assert servidor.llamadas == ["starttls", "login", "send_message"]
    assert servidor.credenciales == ("cuenta@gmail.com", "app-password")

    mensaje = servidor.mensaje
    assert str(mensaje["To"]) == "visitante@gmail.com"
    assert str(mensaje["From"]) == "cuenta@gmail.com"
    assert str(mensaje["Subject"]) == "Confirmación de inscripción"

    cuerpo = mensaje.get_body(preferencelist=("plain",)).get_content()
    assert "Inscripción: 125" in cuerpo

    adjuntos = list(mensaje.iter_attachments())
    assert len(adjuntos) == 1
    assert adjuntos[0].get_content_type() == "image/png"
    assert adjuntos[0].get_filename() == "inscripcion-qr.png"
    assert adjuntos[0].get_payload(decode=True) == qr
