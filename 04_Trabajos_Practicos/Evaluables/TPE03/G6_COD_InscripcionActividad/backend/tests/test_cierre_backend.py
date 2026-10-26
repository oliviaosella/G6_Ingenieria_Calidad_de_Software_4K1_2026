import json
import smtplib
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

import cv2
import numpy as np
import pytest
from fastapi.testclient import TestClient

from app.dependencies import get_gestor_reservas, get_servicio_notificaciones
from app.main import app
from app.routers import consulta_actividades
from app.services import email_service, enviar_confirmacion
from app.services.qr_service import generar_qr
from app.services.reservas import GestorReservas


class CorreoControlado:
    def __init__(self):
        self.fallar = False
        self.envios = []

    def enviar(self, **mensaje):
        if self.fallar:
            raise smtplib.SMTPException("Fallo de prueba, no es un envio real")
        self.envios.append(mensaje)


@pytest.fixture
def ambiente(monkeypatch, tmp_path):
    ruta = tmp_path / "reservas.sqlite3"
    gestor = GestorReservas(ruta_db=ruta)
    correo = CorreoControlado()
    app.dependency_overrides[get_gestor_reservas] = lambda: gestor
    app.dependency_overrides[get_servicio_notificaciones] = lambda: email_service.ServicioNotificaciones(correo)
    monkeypatch.setattr(consulta_actividades, "obtener_hora_actual", lambda: datetime(2026, 10, 27, 8))
    solicitud = {
        "actividad": "Safari", "horario_id": 1, "fecha": "2026-10-27", "horario": "09:00",
        "cantidad_participantes": 1,
        "participantes": [{"nombre": "Ana Pérez", "dni": "12345678", "edad": 25}],
        "aceptacion_terminos": {"actividad": "Safari", "aceptados": True},
        "email": "ana@example.com",
    }
    with TestClient(app) as client:
        yield client, gestor, correo, solicitud, ruta
    app.dependency_overrides.clear()
    gestor.cerrar()


def leer_qr(png):
    imagen = cv2.imdecode(np.frombuffer(png, dtype=np.uint8), cv2.IMREAD_GRAYSCALE)
    texto, _, _ = cv2.QRCodeDetector().detectAndDecode(imagen)
    assert texto, "El QR debe poder leerse con un decodificador independiente"
    return json.loads(texto)


def test_qr_descargable_y_del_correo_contienen_la_inscripcion_completa(ambiente):
    client, _, correo, solicitud, _ = ambiente
    respuesta = client.post("/inscripciones", json=solicitud)
    assert respuesta.status_code == 201
    datos = respuesta.json()
    qr = client.get(datos["qr_url"])
    assert qr.status_code == 200
    assert qr.headers["content-type"] == "image/png"
    contenido = leer_qr(qr.content)
    assert contenido == json.loads(datos["qr_contenido"])
    assert contenido["codigo"] == datos["qr_codigo"]
    assert contenido["actividad"] == "Safari"
    assert contenido["fecha"] == "2026-10-27"
    assert contenido["horario"] == "09:00"
    assert contenido["email"] == "ana@example.com"
    assert contenido["cantidad_participantes"] == 1
    assert contenido["participantes"] == solicitud["participantes"]
    assert leer_qr(correo.envios[0]["qr"]) == contenido


def test_reserva_confirmada_aunque_smtp_falle_y_reintento_no_reserva_de_nuevo(ambiente):
    client, gestor, correo, solicitud, _ = ambiente
    correo.fallar = True
    respuesta = client.post("/inscripciones", json=solicitud)
    assert respuesta.status_code == 201
    datos = respuesta.json()
    assert datos["estado"] == "confirmada"
    assert datos["correo_estado"] == "fallido"
    assert datos["intentos_envio"] == 1
    assert gestor.consultar_cupos("Safari", 1, "2026-10-27") == 7
    assert client.get("/inscripciones/1").json()["correo_estado"] == "fallido"
    correo.fallar = False
    reintento = client.post("/inscripciones/1/reenviar-confirmacion")
    assert reintento.status_code == 200
    assert reintento.json()["correo_estado"] == "enviado"
    assert reintento.json()["intentos_envio"] == 2
    assert gestor.consultar_cupos("Safari", 1, "2026-10-27") == 7
    assert gestor.proximo_id == 2
    assert len(correo.envios) == 1
    assert client.post("/inscripciones/1/reenviar-confirmacion").json()["correo_estado"] == "enviado"
    assert len(correo.envios) == 1


def test_sin_configuracion_smtp_la_reserva_tambien_queda_confirmada(ambiente):
    client, gestor, _, solicitud, _ = ambiente
    app.dependency_overrides[get_servicio_notificaciones] = lambda: email_service.ServicioNotificaciones()
    respuesta = client.post("/inscripciones", json=solicitud)
    assert respuesta.status_code == 201
    assert respuesta.json()["correo_estado"] == "fallido"
    assert "SMTP_PASSWORD" not in respuesta.text
    assert gestor.consultar_cupos("Safari", 1, "2026-10-27") == 7


def test_terminos_especificos_y_aceptacion_con_version_fecha_y_texto_guardados(ambiente):
    client, _, _, solicitud, _ = ambiente
    terminos = client.get("/actividades/Safari/terminos").json()
    assert terminos["version"]
    assert "Texto ficticio" not in terminos["texto"]
    assert "Safari" in terminos["texto"]
    solicitud["aceptacion_terminos"]["version"] = terminos["version"]
    assert client.post("/inscripciones", json=solicitud).status_code == 201
    aceptacion = client.get("/inscripciones/1").json()["aceptacion_terminos"]
    assert aceptacion["actividad"] == "Safari"
    assert aceptacion["aceptados"] is True
    assert aceptacion["version"] == terminos["version"]
    assert aceptacion["texto"] == terminos["texto"]
    assert datetime.fromisoformat(aceptacion["aceptados_en"]).tzinfo is not None


def test_version_de_terminos_anterior_no_reserva_ni_envia(ambiente):
    client, gestor, correo, solicitud, _ = ambiente
    solicitud["aceptacion_terminos"]["version"] = "version-anterior"
    assert client.post("/inscripciones", json=solicitud).status_code == 400
    assert gestor.consultar_cupos("Safari", 1, "2026-10-27") == 8
    assert correo.envios == []


def test_reserva_cupos_dnis_y_aceptacion_sobreviven_a_otra_instancia(ambiente):
    client, _, _, solicitud, ruta = ambiente
    assert client.post("/inscripciones", json=solicitud).status_code == 201
    otro = GestorReservas(ruta_db=ruta)
    try:
        reserva = otro.obtener_reserva(1)
        assert reserva["email"] == "ana@example.com"
        assert reserva["horario"] == "09:00"
        assert reserva["aceptacion_terminos"]["aceptados"] is True
        assert reserva["correo_estado"] == "enviado"
        assert otro.consultar_cupos("Safari", 1, "2026-10-27") == 7
        assert otro.dni_esta_inscripto(1, "12345678", "2026-10-27")
    finally:
        otro.cerrar()


def test_dos_gestores_comparten_ultimos_lugares_sin_sobreventa(tmp_path):
    ruta = tmp_path / "concurrencia.sqlite3"
    gestores = [GestorReservas(ruta_db=ruta) for _ in range(2)]
    try:
        assert gestores[0].reservar("Safari", 1, 7, "2026-10-27")
        def reservar(numero):
            return gestores[numero].crear_reserva(
                "Safari", 1, [{"nombre": "Ana", "dni": str(numero + 1)}], fecha="2026-10-27",
            )
        with ThreadPoolExecutor(max_workers=2) as executor:
            respuestas = list(executor.map(reservar, range(2)))
        assert sum(respuesta is not None for respuesta in respuestas) == 1
        assert gestores[1].consultar_cupos("Safari", 1, "2026-10-27") == 0
    finally:
        for gestor in gestores:
            gestor.cerrar()


def test_qr_y_reintento_de_reserva_inexistente_devuelven_404(ambiente):
    client, _, correo, _, _ = ambiente
    assert client.get("/inscripciones/999/qr").status_code == 404
    assert client.post("/inscripciones/999/reenviar-confirmacion").status_code == 404
    assert correo.envios == []


def test_export_publico_para_enviar_correo_sigue_funcionando(monkeypatch):
    correo = CorreoControlado()
    monkeypatch.setattr(email_service, "_crear_emisor_correo", lambda: correo)
    enviar_confirmacion({"id": 3, "email": "ana@example.com", "actividad": "Safari", "fecha": "2026-10-27", "horario": "09:00"})
    assert len(correo.envios) == 1
    assert leer_qr(correo.envios[0]["qr"])["codigo"] == "RESERVA-3"


def test_configuracion_gmail_admite_password_de_aplicacion_con_espacios(monkeypatch, tmp_path):
    configuracion = tmp_path / "smtp.env"
    configuracion.write_text(
        'SMTP_HOST=smtp.gmail.com\nSMTP_PORT=587\nSMTP_USER=cuenta@example.com\n'
        'SMTP_PASSWORD="abcd efgh ijkl mnop"\nSMTP_FROM=cuenta@example.com\nSMTP_USE_TLS=true\n',
        encoding="utf-8",
    )
    monkeypatch.setattr(email_service, "_RUTA_ENV", configuracion)
    emisor = email_service._crear_emisor_correo()
    assert emisor.host == "smtp.gmail.com"
    assert emisor.puerto == 587
    assert emisor.contrasena == "abcdefghijklmnop"
    assert emisor.usar_tls is True
    monkeypatch.setenv("SMTP_PORT", "465")
    assert email_service._crear_emisor_correo().puerto == 465


def test_estado_de_correo_fallido_se_puede_reintentar_despues_de_reabrir_la_base(ambiente):
    client, gestor, correo, solicitud, ruta = ambiente
    correo.fallar = True
    assert client.post("/inscripciones", json=solicitud).json()["correo_estado"] == "fallido"
    otro = GestorReservas(ruta_db=ruta)
    app.dependency_overrides[get_gestor_reservas] = lambda: otro
    try:
        correo.fallar = False
        assert client.post("/inscripciones/1/reenviar-confirmacion").json()["correo_estado"] == "enviado"
        assert otro.consultar_cupos("Safari", 1, "2026-10-27") == 7
        assert len(correo.envios) == 1
        assert gestor.obtener_reserva(1)["correo_estado"] == "enviado"
    finally:
        otro.cerrar()


def test_dos_reintentos_simultaneos_no_envian_dos_correos(ambiente):
    import threading
    from app.services.notificaciones import procesar_envio

    client, gestor, correo, solicitud, _ = ambiente
    correo.fallar = True
    client.post("/inscripciones", json=solicitud)
    comenzo, continuar = threading.Event(), threading.Event()

    class CorreoLento:
        envios = 0
        def enviar(self, **mensaje):
            self.envios += 1
            comenzo.set()
            assert continuar.wait(timeout=5)

    emisor = CorreoLento()
    servicio = email_service.ServicioNotificaciones(emisor)
    with ThreadPoolExecutor(max_workers=2) as executor:
        primero = executor.submit(procesar_envio, 1, gestor, servicio)
        try:
            assert comenzo.wait(timeout=5)
            segundo = executor.submit(procesar_envio, 1, gestor, servicio).result(timeout=5)
            assert segundo["correo_estado"] == "enviando"
        finally:
            continuar.set()
        assert primero.result(timeout=5)["correo_estado"] == "enviado"
    assert emisor.envios == 1


def test_qr_admite_los_doce_participantes_de_palestra():
    inscripcion = {
        "id": 99, "actividad": "Palestra", "fecha": "2026-10-27", "horario": "10:00", "email": "ana@example.com",
        "participantes": [
            {"nombre": "María Gómez", "dni": str(10000000 + i), "edad": 25, "talle_vestimenta": "XL"}
            for i in range(12)
        ],
    }
    datos = leer_qr(generar_qr(inscripcion))
    assert datos["cantidad_participantes"] == 12
    assert datos["participantes"] == inscripcion["participantes"]


def test_base_se_reabre_despues_de_cerrar_la_conexion(tmp_path):
    ruta = tmp_path / "reinicio.sqlite3"
    primero = GestorReservas(ruta)
    reserva = primero.crear_reserva("Safari", 1, [{"nombre": "Ana", "dni": "12345678"}], fecha="2026-10-27")
    primero.cerrar()
    segundo = GestorReservas(ruta)
    try:
        assert segundo.obtener_reserva(reserva["id"]) == reserva
        assert segundo.consultar_cupos("Safari", 1, "2026-10-27") == 7
    finally:
        segundo.cerrar()


def test_datos_que_no_caben_en_un_qr_no_crean_una_reserva_incompleta(ambiente):
    client, gestor, correo, solicitud, _ = ambiente
    solicitud["participantes"][0]["nombre"] = "A" * 5000
    assert client.post("/inscripciones", json=solicitud).status_code == 422
    assert gestor.obtener_reserva(1) is None
    assert gestor.consultar_cupos("Safari", 1, "2026-10-27") == 8
    assert correo.envios == []
