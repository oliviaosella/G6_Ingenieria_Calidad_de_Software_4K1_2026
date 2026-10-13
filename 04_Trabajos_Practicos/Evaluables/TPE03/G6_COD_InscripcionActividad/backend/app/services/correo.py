from typing import Protocol

from pydantic import BaseModel, EmailStr

from app.schemas import HorarioDisponible


class Correo(BaseModel):
    destinatario: EmailStr
    asunto: str
    cuerpo: str
    qr_png: bytes


class ServicioCorreo(Protocol):
    """Puerto del Adapter: cada proveedor (SMTP, Resend) lo implementa."""

    def enviar(self, correo: Correo) -> None:
        """Envía el correo o lanza ServicioCorreoError si falla."""


class ConsultaHorarios(Protocol):
    """Puerto hacia el Grupo 1 para resolver el turno elegido."""

    def obtener_horario(self, horario_id: int) -> HorarioDisponible:
        """Devuelve el turno identificado por horario_id."""
