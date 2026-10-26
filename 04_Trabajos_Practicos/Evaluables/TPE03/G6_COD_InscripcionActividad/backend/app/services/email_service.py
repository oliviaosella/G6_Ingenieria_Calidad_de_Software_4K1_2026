from email.message import EmailMessage
import os
from pathlib import Path
import smtplib
import ssl

from dotenv import dotenv_values

from .comprobantes import datos_comprobante
from .qr_service import generar_qr

_RUTA_ENV = Path(__file__).resolve().parents[2] / ".env"


class ConfiguracionSMTPError(ValueError):
    """Configuración incompleta o inválida; nunca incluye credenciales en el error."""


class ServicioNotificaciones:
    def __init__(self, emisor_correo=None):
        self.emisor_correo = emisor_correo

    def enviar_confirmacion(self, inscripcion: dict) -> None:
        emisor = self.emisor_correo if self.emisor_correo is not None else _crear_emisor_correo()
        emisor.enviar(
            destinatario=inscripcion["email"], asunto="Confirmación de inscripción",
            contenido=preparar_resumen(inscripcion), qr=generar_qr(inscripcion),
        )


def preparar_resumen(inscripcion: dict) -> str:
    datos = datos_comprobante(inscripcion)
    lineas = []
    for numero, participante in enumerate(datos["participantes"], start=1):
        nombre = " ".join(str(participante[campo]) for campo in ("nombre", "apellido") if participante.get(campo))
        lineas.append(f"{numero}. {nombre or 'Sin nombre'}")
        for etiqueta, campo in (("DNI", "dni"), ("Edad", "edad"), ("Talle de vestimenta", "talle_vestimenta")):
            if participante.get(campo) is not None and participante[campo] != "":
                lineas.append(f"   {etiqueta}: {participante[campo]}")
    detalle = "\n".join(lineas) if lineas else "No se informaron participantes."
    return (
        "¡Inscripción confirmada!\n\nDETALLES DE LA ACTIVIDAD\n"
        "------------------------------------\n"
        f"Número de inscripción: {datos['id']}\nCódigo: {datos['codigo']}\n"
        f"Actividad: {datos['actividad']}\nFecha: {datos['fecha']}\nHorario: {datos['horario']}\n"
        f"Correo: {datos['email']}\n\nPARTICIPANTES ({datos['cantidad_participantes']})\n"
        f"------------------------------------\n{detalle}\n"
    )


class CorreoSMTP:
    def __init__(self, host: str, puerto: int, usuario: str, contrasena: str, remitente: str, usar_tls: bool = True) -> None:
        self.host = host
        self.puerto = puerto
        self.usuario = usuario
        self.contrasena = contrasena
        self.remitente = remitente
        self.usar_tls = usar_tls

    def enviar(self, destinatario: str, asunto: str, contenido: str, qr: bytes) -> None:
        mensaje = EmailMessage()
        mensaje["From"] = self.remitente
        mensaje["To"] = destinatario
        mensaje["Subject"] = asunto
        mensaje.set_content(contenido)
        mensaje.add_attachment(qr, maintype="image", subtype="png", filename="inscripcion-qr.png")
        contexto = ssl.create_default_context()
        if self.puerto == 465:
            conexion = smtplib.SMTP_SSL(self.host, self.puerto, timeout=10, context=contexto)
        else:
            conexion = smtplib.SMTP(self.host, self.puerto, timeout=10)
        with conexion as servidor:
            if self.usar_tls and self.puerto != 465:
                servidor.starttls(context=contexto)
            servidor.login(self.usuario, self.contrasena)
            rechazados = servidor.send_message(mensaje)
            if rechazados:
                raise smtplib.SMTPRecipientsRefused(rechazados)


def _crear_emisor_correo() -> CorreoSMTP:
    # Lee el archivo sin copiar secretos a os.environ; las variables de entorno tienen prioridad.
    valores = {**dotenv_values(_RUTA_ENV), **os.environ}
    requeridas = ("SMTP_HOST", "SMTP_USER", "SMTP_PASSWORD")
    faltantes = [clave for clave in requeridas if not valores.get(clave)]
    if faltantes:
        raise ConfiguracionSMTPError("Falta configurar: " + ", ".join(faltantes))
    try:
        puerto = int(valores.get("SMTP_PORT", "587"))
    except (ValueError, TypeError) as error:
        raise ConfiguracionSMTPError("SMTP_PORT debe ser un número de puerto válido.") from error
    if not 1 <= puerto <= 65535:
        raise ConfiguracionSMTPError("SMTP_PORT debe estar entre 1 y 65535.")
    host = valores["SMTP_HOST"].strip()
    contrasena = valores["SMTP_PASSWORD"]
    if host.lower() == "smtp.gmail.com":
        # Las contraseñas de aplicación de Google se suelen copiar en grupos separados por espacios.
        contrasena = "".join(contrasena.split())
    tls = valores.get("SMTP_USE_TLS", "true").strip().lower()
    if tls not in ("true", "false"):
        raise ConfiguracionSMTPError("SMTP_USE_TLS debe ser true o false.")
    return CorreoSMTP(
        host=host, puerto=puerto, usuario=valores["SMTP_USER"].strip(), contrasena=contrasena,
        remitente=(valores.get("SMTP_FROM") or valores["SMTP_USER"]).strip(), usar_tls=tls == "true",
    )


def enviar_confirmacion(inscripcion: dict) -> None:
    """Envío directo: `from app.services import enviar_confirmacion`.

    Propaga errores SMTP al llamador. El flujo HTTP maneja el estado y reintentos
    sobre una reserva persistida usando ServicioNotificaciones.
    """
    ServicioNotificaciones().enviar_confirmacion(inscripcion)
