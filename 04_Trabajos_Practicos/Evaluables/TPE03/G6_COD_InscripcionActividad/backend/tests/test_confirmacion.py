from datetime import datetime

import pytest
from fastapi.testclient import TestClient

from app.errors import ServicioCorreoError, ServicioCorreoNoDisponibleError
from app.schemas import (
    AceptacionTerminos,
    Actividad,
    HorarioDisponible,
    InscripcionConfirmada,
    SolicitudInscripcion,
    Visitante,
)
from app.services.confirmacion import (
    NotificadorConfirmacion,
    generar_qr,
    url_validacion,
)


HORARIO = HorarioDisponible(
    horario_id=10,
    actividad=Actividad.TIROLESA,
    inicio=datetime(2026, 10, 20, 14, 30),
    fin=datetime(2026, 10, 20, 15, 30),
    cupos_disponibles=5,
)


class FakeConsultaHorarios:
    def __init__(self) -> None:
        self.consultados = []

    def obtener_horario(self, horario_id: int) -> HorarioDisponible:
        self.consultados.append(horario_id)
        return HORARIO


class FakeServicioCorreo:
    def __init__(self, fallos: int = 0) -> None:
        self.fallos = fallos
        self.intentos = 0
        self.envios = []

    def enviar(self, correo) -> None:
        self.intentos += 1
        if self.intentos <= self.fallos:
            raise ServicioCorreoError
        self.envios.append(correo)


def crear_inscripcion(
    inscripcion_id: int = 125,
    actividad: Actividad = Actividad.TIROLESA,
) -> InscripcionConfirmada:
    participantes = [
        Visitante(nombre="Ana Pérez", dni="12345678", edad=30),
        Visitante(nombre="Luis Gómez", dni="40333444", edad=12),
    ]
    solicitud = SolicitudInscripcion(
        actividad=actividad,
        horario_id=10,
        cantidad_participantes=len(participantes),
        participantes=participantes,
        aceptacion_terminos=AceptacionTerminos(
            actividad=actividad,
            aceptados=True,
        ),
        email="visitante@gmail.com",
    )
    return InscripcionConfirmada(
        inscripcion_id=inscripcion_id,
        solicitud=solicitud,
    )


def crear_notificador(
    servicio: FakeServicioCorreo | None = None,
    horarios: FakeConsultaHorarios | None = None,
) -> NotificadorConfirmacion:
    return NotificadorConfirmacion(
        servicio_correo=servicio or FakeServicioCorreo(),
        consulta_horarios=horarios or FakeConsultaHorarios(),
    )


@pytest.fixture
def inscripcion() -> InscripcionConfirmada:
    return crear_inscripcion()


# Contenido del correo

def test_correo_se_dirige_al_email_de_la_solicitud(inscripcion):
    # ARRANGE
    notificador = crear_notificador()

    # ACT
    correo = notificador.armar_correo(inscripcion)

    # ASSERT
    assert correo.destinatario == "visitante@gmail.com"


def test_asunto_incluye_el_id_de_inscripcion(inscripcion):
    # ARRANGE
    notificador = crear_notificador()

    # ACT
    correo = notificador.armar_correo(inscripcion)

    # ASSERT
    assert "#125" in correo.asunto


@pytest.mark.parametrize("actividad", list(Actividad))
def test_cuerpo_incluye_la_actividad(actividad):
    # ARRANGE
    inscripcion = crear_inscripcion(actividad=actividad)
    notificador = crear_notificador()

    # ACT
    correo = notificador.armar_correo(inscripcion)

    # ASSERT
    assert actividad.value in correo.cuerpo


def test_cuerpo_incluye_fecha_y_horario_del_turno(inscripcion):
    # ARRANGE
    notificador = crear_notificador()

    # ACT
    correo = notificador.armar_correo(inscripcion)

    # ASSERT
    assert "20/10/2026" in correo.cuerpo
    assert "14:30" in correo.cuerpo
    assert "15:30" in correo.cuerpo


def test_consulta_el_turno_elegido_en_la_solicitud(inscripcion):
    # ARRANGE
    horarios = FakeConsultaHorarios()
    notificador = crear_notificador(horarios=horarios)

    # ACT
    notificador.armar_correo(inscripcion)

    # ASSERT
    assert horarios.consultados == [10]


def test_cuerpo_incluye_la_cantidad_de_participantes(inscripcion):
    # ARRANGE
    notificador = crear_notificador()

    # ACT
    correo = notificador.armar_correo(inscripcion)

    # ASSERT
    assert "Participantes: 2" in correo.cuerpo


def test_cuerpo_incluye_nombre_y_dni_de_cada_participante(inscripcion):
    # ARRANGE
    notificador = crear_notificador()

    # ACT
    correo = notificador.armar_correo(inscripcion)

    # ASSERT
    for participante in inscripcion.solicitud.participantes:
        assert participante.nombre in correo.cuerpo
        assert participante.dni in correo.cuerpo


# QR asociado a la inscripción

def test_url_de_validacion_identifica_la_inscripcion(inscripcion):
    # ACT
    url = url_validacion(inscripcion)

    # ASSERT
    assert url == "http://127.0.0.1:8000/inscripciones/125/validacion"


def test_qr_se_genera_como_imagen_png(inscripcion):
    # ACT
    qr = generar_qr(inscripcion)

    # ASSERT
    assert qr.startswith(b"\x89PNG")


def test_inscripciones_distintas_generan_qr_distintos():
    # ARRANGE
    una = crear_inscripcion(inscripcion_id=125)
    otra = crear_inscripcion(inscripcion_id=126)

    # ACT
    qr_una = generar_qr(una)
    qr_otra = generar_qr(otra)

    # ASSERT
    assert qr_una != qr_otra


def test_correo_adjunta_el_qr_de_la_inscripcion(inscripcion):
    # ARRANGE
    notificador = crear_notificador()

    # ACT
    correo = notificador.armar_correo(inscripcion)

    # ASSERT
    assert correo.qr_png == generar_qr(inscripcion)


# Envío exitoso

def test_envio_exitoso_envia_un_unico_correo(inscripcion):
    # ARRANGE
    servicio = FakeServicioCorreo()
    notificador = crear_notificador(servicio=servicio)

    # ACT
    correo = notificador.enviar_confirmacion(inscripcion)

    # ASSERT
    assert servicio.envios == [correo]


def test_reintenta_hasta_lograr_el_envio(inscripcion):
    # ARRANGE
    servicio = FakeServicioCorreo(fallos=2)
    notificador = crear_notificador(servicio=servicio)

    # ACT
    correo = notificador.enviar_confirmacion(inscripcion)

    # ASSERT
    assert servicio.intentos == 3
    assert servicio.envios == [correo]


# Fallo del servicio de correo

def test_falla_tras_agotar_tres_intentos(inscripcion):
    # ARRANGE
    servicio = FakeServicioCorreo(fallos=99)
    notificador = crear_notificador(servicio=servicio)

    # ACT / ASSERT
    with pytest.raises(ServicioCorreoNoDisponibleError):
        notificador.enviar_confirmacion(inscripcion)
    assert servicio.intentos == 3


def test_api_responde_503_si_el_correo_no_esta_disponible():
    # ARRANGE
    from app.main import app

    @app.get("/_test/correo-caido")
    def correo_caido():
        raise ServicioCorreoNoDisponibleError

    cliente = TestClient(app, raise_server_exceptions=False)

    # ACT
    respuesta = cliente.get("/_test/correo-caido")

    # ASSERT
    assert respuesta.status_code == 503
