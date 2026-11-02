import smtplib

import pytest

from app.services import email_service


@pytest.fixture(autouse=True)
def aislar_smtp_real(monkeypatch, tmp_path):
    # Las credenciales locales no participan de los tests ni se abre SMTP real.
    monkeypatch.setattr(email_service, "_RUTA_ENV", tmp_path / "sin-configuracion.env")
    for clave in ("SMTP_HOST", "SMTP_PORT", "SMTP_USER", "SMTP_PASSWORD", "SMTP_FROM", "SMTP_USE_TLS"):
        monkeypatch.delenv(clave, raising=False)

    def smtp_bloqueado(*args, **kwargs):
        raise AssertionError("Los tests deben simular SMTP; no se permite enviar correo real.")

    monkeypatch.setattr(smtplib, "SMTP", smtp_bloqueado)
    monkeypatch.setattr(smtplib, "SMTP_SSL", smtp_bloqueado)
