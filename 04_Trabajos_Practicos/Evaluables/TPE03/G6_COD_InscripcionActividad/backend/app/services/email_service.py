import smtplib
import os
from pathlib import Path

from dotenv import load_dotenv
_RUTA_ENV = Path(__file__).resolve().parents[2] / ".env"

from .qr_service import generar_qr
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
    participantes = inscripcion.get("participantes", [])
    lineas_participantes = []

    for numero, participante in enumerate(participantes, start=1):
        nombre_completo = " ".join(
            dato
            for dato in (
                participante.get("nombre"),
                participante.get("apellido"),
            )
            if dato
        )
        lineas_participantes.append(f"{numero}. {nombre_completo or 'Sin nombre'}")

        for etiqueta, campo in (
            ("DNI", "dni"),
            ("Edad", "edad"),
            ("Talle de vestimenta", "talle_vestimenta"),
        ):
            valor = participante.get(campo)
            if valor is not None and valor != "":
                lineas_participantes.append(f"   {etiqueta}: {valor}")

    detalle_participantes = (
        "\n".join(lineas_participantes)
        if lineas_participantes
        else "No se informaron participantes."
    )

    return (
        "¡Inscripción confirmada!\n"
        "\n"
        "DETALLES DE LA ACTIVIDAD\n"
        "------------------------------------\n"
        f"Número de inscripción: {inscripcion['id']}\n"
        f"Actividad: {inscripcion['actividad']}\n"
        f"Fecha: {inscripcion['fecha']}\n"
        f"Horario: {inscripcion['horario']}\n"
        "\n"
        f"PARTICIPANTES ({len(participantes)})\n"
        "------------------------------------\n"
        f"{detalle_participantes}\n"
    )


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
    """Contrato definido para enviar un correo de confirmación de inscripción a un visitante sin depender de detalles del servicio smtp. Se utiliza para desacoplar la lógica de envío de correos de la lógica de negocio de la aplicación."""
    servicio = ServicioNotificaciones(emisor_correo=_crear_emisor_correo())
    servicio.enviar_confirmacion(inscripcion)
