from datetime import datetime

from fastapi.testclient import TestClient

from app.main import app
from app.routers import consulta_actividades


def test_endpoint_lista_actividades() -> None:
    cliente = TestClient(app)

    respuesta = cliente.get("/actividades")

    assert respuesta.status_code == 200
    assert respuesta.json() == [
        {"nombre": "Tirolesa", "cupo_maximo": 10},
        {"nombre": "Safari", "cupo_maximo": 8},
        {"nombre": "Palestra", "cupo_maximo": 12},
        {"nombre": "Jardinería", "cupo_maximo": 12},
    ]


def test_endpoint_lista_turnos_con_anticipacion(monkeypatch) -> None:
    monkeypatch.setattr(
        consulta_actividades,
        "obtener_hora_actual",
        lambda: datetime(2026, 10, 28, 9, 46),
    )
    cliente = TestClient(app)

    respuesta = cliente.get(
        "/actividades/Safari/turnos", params={"fecha": "2026-10-28"}
    )

    assert respuesta.status_code == 200
    assert respuesta.json() == [
        {"actividad": "Safari", "fecha": "2026-10-28", "hora": f"{hora}:00"}
        for hora in range(11, 18)
    ]


def test_endpoint_rechaza_actividad_inexistente() -> None:
    cliente = TestClient(app)

    respuesta = cliente.get(
        "/actividades/Acuario/turnos", params={"fecha": "2026-10-28"}
    )

    assert respuesta.status_code == 404


def test_endpoint_rechaza_fecha_invalida() -> None:
    cliente = TestClient(app)

    respuesta = cliente.get(
        "/actividades/Safari/turnos", params={"fecha": "fecha-invalida"}
    )

    assert respuesta.status_code == 422


def test_endpoint_acepta_participantes_validos() -> None:
    cliente = TestClient(app)

    respuesta = cliente.post("/inscripciones/validar", json={
        "actividad": "Safari",
        "cantidad": 2,
        "participantes": [
            {"nombre": "Ana", "dni": "12345678", "edad": 25},
            {"nombre": "Luis", "dni": "23456789", "edad": 25},
        ],
    })

    assert respuesta.status_code == 200
    assert respuesta.json() == {"valida": True}


def test_endpoint_rechaza_grupo_con_participante_invalido() -> None:
    cliente = TestClient(app)

    respuesta = cliente.post("/inscripciones/validar", json={
        "actividad": "Safari",
        "cantidad": 2,
        "participantes": [
            {"nombre": "Ana", "dni": "12345678", "edad": 25},
            {"nombre": "", "dni": "23456789", "edad": 25},
        ],
    })

    assert respuesta.status_code == 200
    assert respuesta.json() == {"valida": False}


def test_endpoint_rechaza_solicitud_incompleta() -> None:
    cliente = TestClient(app)

    respuesta = cliente.post("/inscripciones/validar", json={
        "actividad": "Safari", "cantidad": 1,
    })

    assert respuesta.status_code == 422
