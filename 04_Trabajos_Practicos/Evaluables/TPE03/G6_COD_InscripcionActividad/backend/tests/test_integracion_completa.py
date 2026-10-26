from copy import deepcopy
from datetime import datetime

import pytest
from fastapi.testclient import TestClient

from app.dependencies import get_gestor_reservas, get_servicio_notificaciones
from app.main import app
from app.routers import consulta_actividades
from app.services.email_service import ServicioNotificaciones
from app.services.reservas import GestorReservas


class CorreoEnMemoria:
    def __init__(self):
        self.envios = []

    def enviar(self, **mensaje):
        self.envios.append(mensaje)


@pytest.fixture
def entorno(monkeypatch):
    gestor = GestorReservas()
    correo = CorreoEnMemoria()
    reloj = {"ahora": datetime(2026, 10, 27, 8)}
    monkeypatch.setattr(consulta_actividades, "obtener_hora_actual", lambda: reloj["ahora"])
    app.dependency_overrides[get_gestor_reservas] = lambda: gestor
    app.dependency_overrides[get_servicio_notificaciones] = lambda: ServicioNotificaciones(correo)
    with TestClient(app) as client:
        yield client, gestor, correo, reloj
    app.dependency_overrides.clear()


@pytest.fixture
def solicitud():
    return {
        "actividad": "Safari",
        "horario_id": 1,
        "fecha": "2026-10-27",
        "horario": "09:00",
        "cantidad_participantes": 1,
        "participantes": [{"nombre": "Ana Pérez", "dni": "12345678", "edad": 25}],
        "aceptacion_terminos": {"actividad": "Safari", "aceptados": True},
        "email": "ana@example.com",
    }


def test_flujo_catalogo_terminos_validacion_reserva_cupos_y_correo(entorno, solicitud):
    client, gestor, correo, _ = entorno
    safari = next(item for item in client.get("/actividades").json() if item["id"] == "Safari")
    assert safari["nombre"] == "Safari"
    assert safari["cupo"] == safari["cupo_maximo"] == 8
    assert client.get("/actividades/Safari/terminos").json()["actividad"] == "Safari"
    assert client.post("/inscripciones/validar", json={
        "actividad": "Safari", "cantidad": 1, "participantes": solicitud["participantes"],
    }).json() == {"valida": True}

    respuesta = client.post("/inscripciones", json=solicitud)
    assert respuesta.status_code == 201
    reserva = respuesta.json()
    assert client.get(f"/inscripciones/{reserva['id']}").json()["fecha"] == "2026-10-27"
    assert gestor.consultar_cupos("Safari", 1, "2026-10-27") == 7
    for ruta in ("turnos", "horarios"):
        respuesta = client.get(f"/actividades/Safari/{ruta}", params={"fecha": "2026-10-27"})
        assert respuesta.status_code == 200
        turno = next(item for item in respuesta.json() if item["hora"] == "09:00")
        assert turno["cupos_disponibles"] == 7
        assert turno["disponible"] is True
    assert len(correo.envios) == 1
    mensaje = correo.envios[0]
    assert mensaje["destinatario"] == "ana@example.com"
    assert "2026-10-27" in mensaje["contenido"]
    assert mensaje["qr"].startswith(b"\x89PNG\r\n\x1a\n")
    assert reserva["qr_codigo"] == f"RESERVA-{reserva['id']}"


@pytest.mark.parametrize("cambio", [
    {"nombre": ""}, {"dni": "abc"}, {"edad": -1},
])
def test_no_reserva_ni_envia_si_los_datos_personales_son_invalidos(entorno, solicitud, cambio):
    client, gestor, correo, _ = entorno
    solicitud["participantes"][0].update(cambio)
    respuesta = client.post("/inscripciones", json=solicitud)
    assert respuesta.status_code == 400
    assert gestor.consultar_cupos("Safari", 1, "2026-10-27") == 8
    assert gestor.obtener_reserva(1) is None
    assert correo.envios == []


@pytest.mark.parametrize("edad,talle", [(7, "M"), (25, None), (25, "XXXL")])
def test_confirma_con_las_reglas_de_edad_y_talle_de_la_actividad(entorno, solicitud, edad, talle):
    client, gestor, correo, _ = entorno
    solicitud["actividad"] = solicitud["aceptacion_terminos"]["actividad"] = "Tirolesa"
    solicitud["participantes"][0].update(edad=edad, talle_vestimenta=talle)
    assert client.post("/inscripciones", json=solicitud).status_code == 400
    assert gestor.consultar_cupos("Tirolesa", 1, "2026-10-27") == 10
    assert correo.envios == []


def test_rechaza_dnis_repetidos_dentro_de_la_misma_solicitud(entorno, solicitud):
    client, gestor, correo, _ = entorno
    solicitud["participantes"] *= 2
    solicitud["cantidad_participantes"] = 2
    assert client.post("/inscripciones", json=solicitud).status_code == 400
    assert gestor.consultar_cupos("Safari", 1, "2026-10-27") == 8
    assert correo.envios == []


@pytest.mark.parametrize("fecha,hora_actual", [
    ("2026-10-26", datetime(2026, 10, 25, 12)),  # Lunes
    ("2026-12-25", datetime(2026, 12, 24, 12)),
    ("2027-01-01", datetime(2026, 12, 31, 12)),
    ("2026-10-27", datetime(2026, 10, 27, 8, 46)),  # Menos de 15 minutos
    ("2026-10-28", datetime(2026, 10, 27, 8)),  # Mas de 24 horas
])
def test_consulta_y_confirmacion_respetan_el_mismo_calendario(entorno, solicitud, fecha, hora_actual):
    client, gestor, correo, reloj = entorno
    reloj["ahora"] = hora_actual
    solicitud["fecha"] = fecha
    for ruta in ("turnos", "horarios"):
        respuesta = client.get(f"/actividades/Safari/{ruta}", params={"fecha": fecha})
        assert respuesta.status_code == 200
        assert "09:00" not in {item["hora"] for item in respuesta.json()}
    assert client.post("/inscripciones", json=solicitud).status_code == 400
    assert gestor.consultar_cupos("Safari", 1, fecha) == 8
    assert correo.envios == []


@pytest.mark.parametrize("horario_id,horario,fecha,estado", [
    (0, "09:00", "2026-10-27", 422),
    (10, "18:00", "2026-10-27", 422),
    (1, "10:00", "2026-10-27", 400),
    (1, "09:00", "fecha-invalida", 422),
])
def test_no_reserva_un_turno_inconsistente(entorno, solicitud, horario_id, horario, fecha, estado):
    client, gestor, correo, _ = entorno
    solicitud.update(horario_id=horario_id, horario=horario, fecha=fecha)
    assert client.post("/inscripciones", json=solicitud).status_code == estado
    assert gestor.obtener_reserva(1) is None
    assert correo.envios == []


def test_mismo_dni_y_hora_en_fechas_distintas_no_comparten_cupos(entorno, solicitud):
    client, gestor, correo, reloj = entorno
    assert client.post("/inscripciones", json=solicitud).status_code == 201
    assert gestor.consultar_cupos("Safari", 1, "2026-10-28") == 8
    assert not gestor.dni_esta_inscripto(1, "12345678", "2026-10-28")
    reloj["ahora"] = datetime(2026, 10, 27, 9)
    solicitud["fecha"] = "2026-10-28"
    assert client.post("/inscripciones", json=solicitud).status_code == 201
    assert gestor.consultar_cupos("Safari", 1, "2026-10-27") == 7
    assert gestor.consultar_cupos("Safari", 1, "2026-10-28") == 7
    assert len(correo.envios) == 2


def test_reserva_ultimo_lugar_consulta_lleno_y_rechaza_siguiente(entorno, solicitud):
    client, gestor, correo, _ = entorno
    for numero in range(8):
        datos = deepcopy(solicitud)
        datos["participantes"][0]["dni"] = str(20000000 + numero)
        assert client.post("/inscripciones", json=datos).status_code == 201
    for ruta in ("turnos", "horarios"):
        turnos = client.get(f"/actividades/Safari/{ruta}", params={"fecha": solicitud["fecha"]}).json()
        turno = next(item for item in turnos if item["hora"] == "09:00")
        assert turno["cupos_disponibles"] == 0
        assert turno["disponible"] is False
        assert turno["motivo"] == "sin cupos"
    assert client.post("/inscripciones", json=solicitud).status_code == 409
    assert len(correo.envios) == 8
    assert gestor.obtener_reserva(9) is None


def test_no_hay_rutas_duplicadas_en_la_aplicacion():
    rutas = [(ruta.path, metodo) for ruta in app.routes if hasattr(ruta, "methods") for metodo in ruta.methods]
    assert len(rutas) == len(set(rutas))
