import pytest

from app.errors import (
    AceptacionDeOtraActividadError,
    CuposNoDisponiblesError,
    DniDuplicadoEnHorarioError,
    InconsistenciaParticipantesError,
    TerminosNoAceptadosError,
)
from app.schemas import (
    AceptacionTerminos,
    Actividad,
    SolicitudInscripcion,
    Visitante,
)
from app.services.email_service import ServicioNotificaciones
from app.services.inscripciones import inscribir_participantes
from app.services.reservas import GestorReservas




class CorreoDePrueba:
    def __init__(self):
        self.envios = []

    def enviar(self, destinatario, asunto, contenido, qr):
        self.envios.append({"destinatario": destinatario, "asunto": asunto, "contenido": contenido, "qr": qr})


def test_reserva_exitosa_genera_confirmacion_con_qr():
    gestor = GestorReservas()
    correo = CorreoDePrueba()
    notificaciones = ServicioNotificaciones(correo)

    reserva = gestor.crear_reserva(
        actividad="Tirolesa",
        horario_id=1,
        participantes=[{"nombre": "Ana", "apellido": "Pérez", "dni": "12345678", "edad": 25}],
    )
    reserva.update({"email": "ana@example.com", "fecha": "2026-10-26", "horario": "14:30"})

    notificaciones.enviar_confirmacion(reserva)

    assert gestor.consultar_cupos("Tirolesa", 1) == 9
    assert len(correo.envios) == 1
    assert correo.envios[0]["destinatario"] == "ana@example.com"
    assert "Tirolesa" in correo.envios[0]["contenido"]
    assert correo.envios[0]["qr"].startswith(b"\x89PNG\r\n\x1a\n")


def test_reserva_rechazada_no_genera_confirmacion():
    gestor = GestorReservas()
    correo = CorreoDePrueba()
    notificaciones = ServicioNotificaciones(correo)
    participantes = [{"nombre": f"Persona {i}", "dni": str(i), "edad": 20} for i in range(11)]

    reserva = gestor.crear_reserva("Tirolesa", 1, participantes)

    assert reserva is None
    assert gestor.consultar_cupos("Tirolesa", 1) == 10
    assert correo.envios == []


def test_inscripcion_exitosa_valida_terminos_reserva_cupos_y_envia_correo():
    gestor = GestorReservas()
    correo = CorreoDePrueba()
    notificaciones = ServicioNotificaciones(correo)
    solicitud = SolicitudInscripcion(
        actividad=Actividad.TIROLESA,
        horario_id=1,
        cantidad_participantes=1,
        participantes=[
            Visitante(
                nombre="Ana Pérez",
                dni="12345678",
                edad=25,
                talle_vestimenta="M",
            )
        ],
        aceptacion_terminos=AceptacionTerminos(
            actividad=Actividad.TIROLESA,
            aceptados=True,
        ),
        email="ana@example.com",
    )
    resultado = inscribir_participantes(
        solicitud=solicitud,
        gestor_reservas=gestor,
        servicio_notificaciones=notificaciones,
        fecha="2026-10-26",
        horario="14:30",
    )
    assert resultado is not None
    assert resultado["id"] == 1
    assert gestor.consultar_cupos("Tirolesa", 1, fecha="2026-10-26") == 9
    assert len(correo.envios) == 1
    assert correo.envios[0]["destinatario"] == "ana@example.com"
    assert "Tirolesa" in correo.envios[0]["contenido"]
    assert correo.envios[0]["qr"].startswith(b"\x89PNG\r\n\x1a\n")


def test_rechazo_por_terminos_no_aceptados_no_modifica_cupos_ni_envia_correo():
    gestor = GestorReservas()
    correo = CorreoDePrueba()
    notificaciones = ServicioNotificaciones(correo)

    solicitud = SolicitudInscripcion(
        actividad=Actividad.TIROLESA,
        horario_id=1,
        cantidad_participantes=1,
        participantes=[
            Visitante(
                nombre="Carlos Benítez",
                dni="22334455",
                edad=30,
                talle_vestimenta="L",
            )
        ],
        aceptacion_terminos=AceptacionTerminos(
            actividad=Actividad.TIROLESA,
            aceptados=False,
        ),
        email="carlos@example.com",
    )

    with pytest.raises(TerminosNoAceptadosError):
        inscribir_participantes(
            solicitud=solicitud,
            gestor_reservas=gestor,
            servicio_notificaciones=notificaciones,
            fecha="2026-10-26",
            horario="14:30",
        )

    assert gestor.consultar_cupos("Tirolesa", 1, fecha="2026-10-26") == 10
    assert correo.envios == []


def test_rechazo_por_actividad_incompatible_en_terminos_no_crea_reserva():
    gestor = GestorReservas()
    correo = CorreoDePrueba()
    notificaciones = ServicioNotificaciones(correo)

    solicitud = SolicitudInscripcion(
        actividad=Actividad.TIROLESA,
        horario_id=1,
        cantidad_participantes=1,
        participantes=[
            Visitante(
                nombre="Lucía Morales",
                dni="33445566",
                edad=22,
                talle_vestimenta="S",
            )
        ],
        aceptacion_terminos=AceptacionTerminos(
            actividad=Actividad.SAFARI,
            aceptados=True,
        ),
        email="lucia@example.com",
    )

    with pytest.raises(AceptacionDeOtraActividadError):
        inscribir_participantes(
            solicitud=solicitud,
            gestor_reservas=gestor,
            servicio_notificaciones=notificaciones,
            fecha="2026-10-26",
            horario="14:30",
        )

    assert gestor.consultar_cupos("Tirolesa", 1, fecha="2026-10-26") == 10
    assert gestor.consultar_cupos("Safari", 1, fecha="2026-10-26") == 8
    assert correo.envios == []


def test_reserva_sin_cupos_disponibles_no_envia_correo_confirmacion():
    gestor = GestorReservas()
    correo = CorreoDePrueba()
    notificaciones = ServicioNotificaciones(correo)

    # Tirolesa tiene capacidad máxima de 10 cupos; enviamos 11
    participantes = [
        Visitante(
            nombre=f"Participante {i}",
            dni=f"400000{i:02d}",
            edad=20,
            talle_vestimenta="M",
        )
        for i in range(11)
    ]

    solicitud = SolicitudInscripcion(
        actividad=Actividad.TIROLESA,
        horario_id=1,
        cantidad_participantes=11,
        participantes=participantes,
        aceptacion_terminos=AceptacionTerminos(
            actividad=Actividad.TIROLESA,
            aceptados=True,
        ),
        email="grupo@example.com",
    )

    with pytest.raises(CuposNoDisponiblesError):
        inscribir_participantes(
            solicitud=solicitud,
            gestor_reservas=gestor,
            servicio_notificaciones=notificaciones,
            fecha="2026-10-26",
            horario="14:30",
        )

    assert gestor.consultar_cupos("Tirolesa", 1, fecha="2026-10-26") == 10
    assert correo.envios == []


def test_rechazo_por_dni_duplicado_en_mismo_horario_no_emite_confirmacion():
    gestor = GestorReservas()
    correo = CorreoDePrueba()
    notificaciones = ServicioNotificaciones(correo)

    # 1. Primera inscripción exitosa con DNI 11223344 en horario 1
    solicitud_1 = SolicitudInscripcion(
        actividad=Actividad.TIROLESA,
        horario_id=1,
        cantidad_participantes=1,
        participantes=[
            Visitante(
                nombre="Martín Vega",
                dni="11223344",
                edad=28,
                talle_vestimenta="M",
            )
        ],
        aceptacion_terminos=AceptacionTerminos(
            actividad=Actividad.TIROLESA,
            aceptados=True,
        ),
        email="martin@example.com",
    )
    res_1 = inscribir_participantes(
        solicitud=solicitud_1,
        gestor_reservas=gestor,
        servicio_notificaciones=notificaciones,
        fecha="2026-10-26",
        horario="14:30",
    )
    assert res_1 is not None
    assert gestor.consultar_cupos("Tirolesa", 1, fecha="2026-10-26") == 9
    assert len(correo.envios) == 1

    # 2. Segunda solicitud con el MISMO DNI en el MISMO horario (para Safari)
    solicitud_duplicada = SolicitudInscripcion(
        actividad=Actividad.SAFARI,
        horario_id=1,
        cantidad_participantes=1,
        participantes=[
            Visitante(
                nombre="Martín Vega",
                dni="11223344",
                edad=28,
            )
        ],
        aceptacion_terminos=AceptacionTerminos(
            actividad=Actividad.SAFARI,
            aceptados=True,
        ),
        email="martin@example.com",
    )

    with pytest.raises(DniDuplicadoEnHorarioError):
        inscribir_participantes(
            solicitud=solicitud_duplicada,
            gestor_reservas=gestor,
            servicio_notificaciones=notificaciones,
            fecha="2026-10-26",
            horario="14:30",
        )

    # Los cupos de Safari deben seguir intactos (8) y no debe haber un 2do correo
    assert gestor.consultar_cupos("Safari", 1, fecha="2026-10-26") == 8
    assert len(correo.envios) == 1


def test_inconsistencia_entre_cantidad_declarada_y_lista_participantes():
    gestor = GestorReservas()
    correo = CorreoDePrueba()
    notificaciones = ServicioNotificaciones(correo)

    # Se declara cantidad_participantes=2 pero se envía solo 1 participante
    solicitud = SolicitudInscripcion(
        actividad=Actividad.TIROLESA,
        horario_id=1,
        cantidad_participantes=2,
        participantes=[
            Visitante(
                nombre="Valeria Rivas",
                dni="55667788",
                edad=26,
                talle_vestimenta="S",
            )
        ],
        aceptacion_terminos=AceptacionTerminos(
            actividad=Actividad.TIROLESA,
            aceptados=True,
        ),
        email="valeria@example.com",
    )

    with pytest.raises(InconsistenciaParticipantesError):
        inscribir_participantes(
            solicitud=solicitud,
            gestor_reservas=gestor,
            servicio_notificaciones=notificaciones,
            fecha="2026-10-26",
            horario="14:30",
        )

    assert gestor.consultar_cupos("Tirolesa", 1, fecha="2026-10-26") == 10
    assert correo.envios == []
