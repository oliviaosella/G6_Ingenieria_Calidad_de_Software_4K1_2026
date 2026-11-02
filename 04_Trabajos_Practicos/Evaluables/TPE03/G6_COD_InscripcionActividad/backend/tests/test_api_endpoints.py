from datetime import datetime

import pytest
from fastapi.testclient import TestClient

from app.dependencies import (
    get_gestor_reservas,
    get_servicio_notificaciones,
    reset_gestor_reservas,
)
from app.main import app
from app.routers import consulta_actividades
from app.services.email_service import ServicioNotificaciones


class CorreoDummy:
    def __init__(self):
        self.envios = []

    def enviar(self, destinatario, asunto, contenido, qr):
        self.envios.append(
            {
                "destinatario": destinatario,
                "asunto": asunto,
                "contenido": contenido,
                "qr": qr,
            }
        )


@pytest.fixture(autouse=True)
def preparar_entorno(monkeypatch):
    """Reinicia el GestorReservas e inyecta un emisor de prueba para aislar cada test."""
    reset_gestor_reservas()
    monkeypatch.setattr(
        consulta_actividades, "obtener_hora_actual",
        lambda: datetime(2026, 10, 27, 8, 0),
    )
    correo = CorreoDummy()
    notificaciones = ServicioNotificaciones(emisor_correo=correo)

    app.dependency_overrides[get_servicio_notificaciones] = lambda: notificaciones
    yield correo
    app.dependency_overrides.clear()


@pytest.fixture
def client():
    return TestClient(app)


def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.parametrize("origin", ["http://localhost:5173", "http://localhost:5174", "http://127.0.0.1:5174"])
def test_frontend_local_puede_consultar_api(client, origin):
    response = client.get("/actividades", headers={"Origin": origin})
    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == origin


def test_openapi_schema_generado_correctamente(client):
    response = client.get("/openapi.json")
    assert response.status_code == 200
    schema = response.json()
    assert schema["info"]["title"] == "Eco Harmony Park - API de Inscripción a Actividades"
    assert "/actividades" in schema["paths"]
    assert "/actividades/{actividad}/terminos" in schema["paths"]
    assert "/actividades/{actividad}/horarios" in schema["paths"]
    assert "/actividades/{actividad}/calendario" in schema["paths"]
    assert "/inscripciones" in schema["paths"]
    assert "/inscripciones/{id}" in schema["paths"]


def test_listar_actividades_catalogo_completo(client):
    response = client.get("/actividades")
    assert response.status_code == 200
    datos = response.json()
    assert len(datos) == 4

    nombres = [item["id"] for item in datos]
    assert nombres == ["Tirolesa", "Safari", "Palestra", "Jardinería"]

    tirolesa = next(a for a in datos if a["id"] == "Tirolesa")
    assert tirolesa["cupo"] == 10
    assert tirolesa["edad_minima"] == 8
    assert tirolesa["requiere_talle"] is True
    assert tirolesa["talles_disponibles"] == ["XS", "S", "M", "L", "XL", "XXL"]
    assert next(a for a in datos if a["id"] == "Safari")["talles_disponibles"] == []


def test_calendario_expone_cierres_ventana_y_horarios_desde_backend(client, monkeypatch):
    monkeypatch.setattr(
        consulta_actividades, "obtener_hora_actual",
        lambda: datetime(2026, 10, 26, 10, 0),
    )
    response = client.get("/actividades/Safari/calendario")
    assert response.status_code == 200
    calendario = response.json()
    assert calendario["anticipacion_minima_minutos"] == 15
    assert calendario["anticipacion_maxima_horas"] == 24
    lunes, martes = calendario["dias"]
    assert lunes == {"fecha": "2026-10-26", "estado": "cerrado", "motivo": "Cerrado los lunes", "horarios": []}
    assert martes["fecha"] == "2026-10-27"
    assert martes["estado"] == "con_horarios"
    assert martes["horarios"][0]["horario_id"] == 1
    assert martes["horarios"][0]["cupos_disponibles"] == 8


@pytest.mark.parametrize(
    ("ahora", "fecha_cerrada", "motivo"),
    [
        (datetime(2026, 12, 24, 10, 0), "2026-12-25", "Cerrado el 25 de diciembre"),
        (datetime(2026, 12, 31, 10, 0), "2027-01-01", "Cerrado el 1 de enero"),
    ],
)
def test_calendario_expone_feriados_cerrados(client, monkeypatch, ahora, fecha_cerrada, motivo):
    monkeypatch.setattr(consulta_actividades, "obtener_hora_actual", lambda: ahora)
    response = client.get("/actividades/Safari/calendario")
    assert response.status_code == 200
    assert response.json()["dias"][1] == {
        "fecha": fecha_cerrada,
        "estado": "cerrado",
        "motivo": motivo,
        "horarios": [],
    }


def test_consultar_terminos_actividad_existente(client):
    response = client.get("/actividades/Tirolesa/terminos")
    assert response.status_code == 200
    datos = response.json()
    assert datos["actividad"] == "Tirolesa"
    assert "Tirolesa" in datos["texto"]


def test_consultar_terminos_actividad_invalida(client):
    response = client.get("/actividades/Inexistente/terminos")
    assert response.status_code == 422


def test_consultar_horarios_lista_nueve_turnos_con_cupos_iniciales(client):
    response = client.get("/actividades/Tirolesa/horarios?fecha=2026-10-27")
    assert response.status_code == 200
    turnos = response.json()
    assert len(turnos) == 9

    primer_turno = turnos[0]
    assert primer_turno["horario_id"] == 1
    assert primer_turno["hora"] == "09:00"
    assert primer_turno["cupos_disponibles"] == 10
    assert primer_turno["disponible"] is True

    ultimo_turno = turnos[-1]
    assert ultimo_turno["horario_id"] == 9
    assert ultimo_turno["hora"] == "17:00"


def test_post_inscripcion_exitosa_y_persistencia(client, preparar_entorno):
    correo = preparar_entorno
    payload = {
        "actividad": "Tirolesa",
        "horario_id": 1,
        "fecha": "2026-10-27",
        "horario": "09:00",
        "cantidad_participantes": 1,
        "participantes": [
            {
                "nombre": "Ana Pérez",
                "dni": "12345678",
                "edad": 25,
                "talle_vestimenta": "M",
            }
        ],
        "aceptacion_terminos": {
            "actividad": "Tirolesa",
            "aceptados": True,
        },
        "email": "ana@example.com",
    }

    response = client.post("/inscripciones", json=payload)
    assert response.status_code == 201
    datos = response.json()

    assert datos["id"] == 1
    assert datos["actividad"] == "Tirolesa"
    assert datos["horario_id"] == 1
    assert datos["email"] == "ana@example.com"
    assert datos["qr_codigo"] == "RESERVA-1"
    assert len(datos["participantes"]) == 1

    # Verifica que el correo fue despachado
    assert len(correo.envios) == 1
    assert correo.envios[0]["destinatario"] == "ana@example.com"

    # Verifica que los cupos se descontaron en la consulta de horarios
    horarios_resp = client.get("/actividades/Tirolesa/horarios?fecha=2026-10-27")
    turno_1 = next(t for t in horarios_resp.json() if t["horario_id"] == 1)
    assert turno_1["cupos_disponibles"] == 9

    # Verifica que se puede recuperar por GET /inscripciones/{id}
    reserva_resp = client.get("/inscripciones/1")
    assert reserva_resp.status_code == 200
    reserva_datos = reserva_resp.json()
    assert reserva_datos["id"] == 1
    assert reserva_datos["actividad"] == "Tirolesa"


def test_get_inscripcion_inexistente_retorna_404(client):
    response = client.get("/inscripciones/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Reserva no encontrada."


def test_post_inscripcion_rechaza_terminos_no_aceptados(client):
    payload = {
        "actividad": "Tirolesa",
        "horario_id": 1,
        "cantidad_participantes": 1,
        "participantes": [{"nombre": "Ana", "dni": "12345678", "edad": 25}],
        "aceptacion_terminos": {
            "actividad": "Tirolesa",
            "aceptados": False,
        },
        "email": "ana@example.com",
    }
    response = client.post("/inscripciones", json=payload)
    assert response.status_code == 400
    assert "términos y condiciones deben ser aceptados" in response.json()["detail"]


def test_post_inscripcion_rechaza_terminos_de_otra_actividad(client):
    payload = {
        "actividad": "Tirolesa",
        "horario_id": 1,
        "cantidad_participantes": 1,
        "participantes": [{"nombre": "Ana", "dni": "12345678", "edad": 25}],
        "aceptacion_terminos": {
            "actividad": "Safari",
            "aceptados": True,
        },
        "email": "ana@example.com",
    }
    response = client.post("/inscripciones", json=payload)
    assert response.status_code == 400
    assert "no corresponden a la actividad solicitada" in response.json()["detail"]


def test_post_inscripcion_rechaza_inconsistencia_cantidad_participantes(client):
    payload = {
        "actividad": "Tirolesa",
        "horario_id": 1,
        "cantidad_participantes": 2,
        "participantes": [{"nombre": "Ana", "dni": "12345678", "edad": 25}],
        "aceptacion_terminos": {
            "actividad": "Tirolesa",
            "aceptados": True,
        },
        "email": "ana@example.com",
    }
    response = client.post("/inscripciones", json=payload)
    assert response.status_code == 400
    assert "cantidad de participantes declarada no coincide" in response.json()["detail"]


def test_post_inscripcion_rechaza_dni_duplicado_en_mismo_horario(client):
    payload_1 = {
        "actividad": "Tirolesa",
        "horario_id": 2,
        "cantidad_participantes": 1,
        "participantes": [{"nombre": "Ana", "dni": "12345678", "edad": 25, "talle_vestimenta": "M"}],
        "aceptacion_terminos": {"actividad": "Tirolesa", "aceptados": True},
        "email": "ana@example.com",
    }
    resp1 = client.post("/inscripciones", json=payload_1)
    assert resp1.status_code == 201

    # Mismo DNI intenta anotarse en la misma hora (horario_id=2) en otra o misma actividad
    payload_2 = {
        "actividad": "Safari",
        "horario_id": 2,
        "cantidad_participantes": 1,
        "participantes": [{"nombre": "Ana", "dni": "12345678", "edad": 25}],
        "aceptacion_terminos": {"actividad": "Safari", "aceptados": True},
        "email": "ana2@example.com",
    }
    resp2 = client.post("/inscripciones", json=payload_2)
    assert resp2.status_code == 409
    assert "reserva activa en este mismo turno horario" in resp2.json()["detail"]


def test_post_inscripcion_rechaza_por_cupos_insuficientes(client):
    # Safari tiene cupo máximo de 8
    participantes_exceso = [
        {"nombre": f"Persona {i}", "dni": f"9000000{i}", "edad": 20}
        for i in range(9)
    ]
    payload = {
        "actividad": "Safari",
        "horario_id": 3,
        "cantidad_participantes": 9,
        "participantes": participantes_exceso,
        "aceptacion_terminos": {"actividad": "Safari", "aceptados": True},
        "email": "grupo@example.com",
    }
    response = client.post("/inscripciones", json=payload)
    assert response.status_code == 409
    assert "No hay cupos disponibles suficientes" in response.json()["detail"]


def test_post_inscripcion_rechaza_formato_email_invalido(client):
    payload = {
        "actividad": "Tirolesa",
        "horario_id": 1,
        "cantidad_participantes": 1,
        "participantes": [{"nombre": "Ana", "dni": "12345678", "edad": 25}],
        "aceptacion_terminos": {"actividad": "Tirolesa", "aceptados": True},
        "email": "no-es-un-email-valido",
    }
    response = client.post("/inscripciones", json=payload)
    assert response.status_code == 422


def test_dependencia_smtp_estricta_sin_env(monkeypatch):
    """La configuración se valida al enviar, sin impedir crear la reserva."""
    from app.services.email_service import ConfiguracionSMTPError, _crear_emisor_correo

    monkeypatch.delenv("SMTP_HOST", raising=False)
    assert get_servicio_notificaciones() is not None
    with pytest.raises(ConfiguracionSMTPError):
        _crear_emisor_correo()
