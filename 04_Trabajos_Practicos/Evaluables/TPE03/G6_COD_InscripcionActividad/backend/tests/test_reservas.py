from concurrent.futures import ThreadPoolExecutor
import time
from app.services.reservas import GestorReservas


def test_capacidad_inicial_segun_actividad():
    # Precondiciones
    gestor = GestorReservas()

    # Pasos
    capacidad_tirolesa = gestor.obtener_capacidad_inicial("Tirolesa")
    capacidad_safari = gestor.obtener_capacidad_inicial("Safari")
    capacidad_palestra = gestor.obtener_capacidad_inicial("Palestra")
    capacidad_jardineria = gestor.obtener_capacidad_inicial("Jardinería")

    # Resultado
    assert capacidad_tirolesa == 10
    assert capacidad_safari == 8
    assert capacidad_palestra == 12
    assert capacidad_jardineria == 12


def test_reserva_valida_descuenta_cupos_correctamente():
    # Precondiciones
    gestor = GestorReservas()

    # Pasos: Para Tirolesa (que tiene 10 cupos), reservamos 2 lugares en el horario 1
    resultado = gestor.reservar(actividad="Tirolesa", horario_id=1, cantidad=2)

    # Resultado: La reserva fue exitosa y ahora quedan 8 cupos (10 - 2)
    assert resultado is True
    assert gestor.consultar_cupos(actividad="Tirolesa", horario_id=1) == 8


def test_independencia_de_cupos_entre_turnos_distintos():
    # Precondiciones
    gestor = GestorReservas()

    # Pasos: Reservamos 4 lugares en Tirolesa horario 1
    resultado = gestor.reservar(actividad="Tirolesa", horario_id=1, cantidad=4)

    # Resultado: Solo el horario 1 de Tirolesa baja a 6; el horario 2 y Safari quedan intactos
    assert resultado is True
    assert gestor.consultar_cupos(actividad="Tirolesa", horario_id=1) == 6
    assert gestor.consultar_cupos(actividad="Tirolesa", horario_id=2) == 10
    assert gestor.consultar_cupos(actividad="Safari", horario_id=1) == 8


def test_rechazar_reserva_en_horario_sin_cupos():
    # Precondiciones: En Safari (8 cupos) se reservan los 8 lugares disponibles
    gestor = GestorReservas()
    gestor.reservar(actividad="Safari", horario_id=1, cantidad=8)
    assert gestor.consultar_cupos(actividad="Safari", horario_id=1) == 0

    # Pasos: Se intenta reservar 1 lugar en ese horario ya agotado
    resultado = gestor.reservar(actividad="Safari", horario_id=1, cantidad=1)

    # Resultado: Debe rechazarse (False) y los cupos deben seguir en 0 (no quedar en -1)
    assert resultado is False
    assert gestor.consultar_cupos(actividad="Safari", horario_id=1) == 0


def test_rechazar_reserva_cuando_cupos_son_insuficientes():
    # Precondiciones: En Safari (8 cupos) se reservan 6 lugares, dejando exactamente 2 cupos disponibles
    gestor = GestorReservas()
    gestor.reservar(actividad="Safari", horario_id=1, cantidad=6)
    assert gestor.consultar_cupos(actividad="Safari", horario_id=1) == 2

    # Pasos: Se intenta reservar para 3 personas (supera los 2 cupos disponibles)
    resultado = gestor.reservar(actividad="Safari", horario_id=1, cantidad=3)

    # Resultado: Debe rechazarse (False) y los cupos deben mantenerse intactos en 2
    assert resultado is False
    assert gestor.consultar_cupos(actividad="Safari", horario_id=1) == 2


def test_crear_reserva_asocia_actividad_horario_y_participantes():
    # Precondiciones
    gestor = GestorReservas()
    participantes = [
        {"nombre": "Ana", "dni": "12345678", "edad": 25},
        {"nombre": "Pedro", "dni": "87654321", "edad": 30},
    ]

    # Pasos: Creamos una reserva pasando la lista de participantes en Tirolesa horario 1
    reserva = gestor.crear_reserva(
        actividad="Tirolesa",
        horario_id=1,
        participantes=participantes,
    )

    # Resultado: La reserva tiene asignado un id, guarda la actividad, horario y todos los participantes
    assert reserva is not None
    assert reserva["id"] is not None
    assert reserva["actividad"] == "Tirolesa"
    assert reserva["horario_id"] == 1
    assert len(reserva["participantes"]) == 2
    assert reserva["participantes"][0]["nombre"] == "Ana"
    # Y los cupos se descuentan según la cantidad de personas (10 - 2 = 8)
    assert gestor.consultar_cupos(actividad="Tirolesa", horario_id=1) == 8


def test_rechazar_reserva_con_cantidad_cero_o_negativa():
    # Precondiciones
    gestor = GestorReservas()

    # Pasos: Intentamos reservar con cantidad 0, cantidad negativa (-2), y lista vacía
    res_cero = gestor.reservar(actividad="Tirolesa", horario_id=1, cantidad=0)
    res_negativo = gestor.reservar(actividad="Tirolesa", horario_id=1, cantidad=-2)
    res_vacia = gestor.crear_reserva(actividad="Tirolesa", horario_id=1, participantes=[])

    # Resultado: Todas deben rechazarse y los cupos deben seguir intactos en 10
    assert res_cero is False
    assert res_negativo is False
    assert res_vacia is None
    assert gestor.consultar_cupos(actividad="Tirolesa", horario_id=1) == 10


def test_rechazar_si_cantidad_no_coincide_con_numero_de_participantes():
    # Precondiciones
    gestor = GestorReservas()
    participantes = [
        {"nombre": "Ana", "dni": "12345678", "edad": 25},
        {"nombre": "Pedro", "dni": "87654321", "edad": 30},
    ]

    # Pasos: Se declara cantidad 3, pero se mandan 2 participantes
    reserva = gestor.crear_reserva(
        actividad="Tirolesa",
        horario_id=1,
        participantes=participantes,
        cantidad_declarada=3,
    )

    # Resultado: Debe rechazarse por inconsistencia (None) y los cupos deben seguir en 10
    assert reserva is None
    assert gestor.consultar_cupos(actividad="Tirolesa", horario_id=1) == 10


def test_rechazar_inscripcion_de_mismo_dni_en_horarios_superpuestos():
    # Precondiciones: Ana ya tiene reserva en Tirolesa en el horario 1
    gestor = GestorReservas()
    gestor.crear_reserva(
        actividad="Tirolesa",
        horario_id=1,
        participantes=[{"nombre": "Ana", "dni": "12345678", "edad": 25}],
    )

    # Pasos: Intentamos anotar a Ana en Safari en el mismo horario 1
    reserva_solapada = gestor.crear_reserva(
        actividad="Safari",
        horario_id=1,
        participantes=[{"nombre": "Ana", "dni": "12345678", "edad": 25}],
    )

    # Resultado: Debe rechazarse (None) y no ocupar cupos en Safari (deben seguir siendo 8)
    assert reserva_solapada is None
    assert gestor.consultar_cupos(actividad="Safari", horario_id=1) == 8


def test_reserva_rechazada_no_persiste_datos_ni_modifica_cupos():
    # Precondiciones: Horario 1 con capacidad inicial
    gestor = GestorReservas()

    # Pasos: Se intenta una reserva que falla (por ejemplo, pidiendo 15 cupos en Tirolesa que tiene 10)
    participantes_exceso = [{"nombre": f"Persona_{i}", "dni": f"{i}", "edad": 20} for i in range(15)]
    reserva_fallida = gestor.crear_reserva(
        actividad="Tirolesa",
        horario_id=1,
        participantes=participantes_exceso,
    )

    # Resultado:
    # 1. La reserva debe ser rechazada (None)
    assert reserva_fallida is None
    # 2. Los cupos deben seguir intactos en 10
    assert gestor.consultar_cupos(actividad="Tirolesa", horario_id=1) == 10
    # 3. El contador de reservas no debe avanzar (el próximo ID disponible debe seguir siendo 1)
    assert gestor.obtener_proximo_id() == 1
    # 4. Ningún DNI de la solicitud fallida debe quedar bloqueado
    assert gestor.dni_esta_inscripto(horario_id=1, dni="0") is False


def test_persistencia_recuperar_reserva_por_id():
    # Precondiciones
    gestor = GestorReservas()
    participantes = [{"nombre": "Laura", "dni": "99999999", "edad": 29}]
    reserva_creada = gestor.crear_reserva(
        actividad="Palestra",
        horario_id=2,
        participantes=participantes,
    )
    reserva_id = reserva_creada["id"]

    # Pasos: Recuperamos la reserva persistida usando su ID
    reserva_recuperada = gestor.obtener_reserva(reserva_id)

    # Resultado: La reserva recuperada es idéntica a la creada y contiene todos los datos
    assert reserva_recuperada is not None
    assert reserva_recuperada["id"] == reserva_id
    assert reserva_recuperada["actividad"] == "Palestra"
    assert reserva_recuperada["horario_id"] == 2
    assert reserva_recuperada["participantes"][0]["nombre"] == "Laura"
    assert gestor.obtener_reserva(9999) is None


def test_dos_solicitudes_simultaneas_por_ultimos_lugares_evita_sobreventa():
    # Precondiciones: En Safari (8 cupos) se reservan 6 lugares. Quedan exactamente 2 cupos.
    gestor = GestorReservas()
    gestor.crear_reserva(
        actividad="Safari",
        horario_id=1,
        participantes=[{"nombre": f"Ocupante_{i}", "dni": f"DNI_{i}", "edad": 20} for i in range(6)],
    )
    assert gestor.consultar_cupos(actividad="Safari", horario_id=1) == 2

    # Pasos: Dos familias (cada una de 2 personas) intentan reservar los últimos 2 cupos en paralelo
    solicitud_a = [
        {"nombre": "A1", "dni": "1001", "edad": 20},
        {"nombre": "A2", "dni": "1002", "edad": 21},
    ]
    solicitud_b = [
        {"nombre": "B1", "dni": "2001", "edad": 22},
        {"nombre": "B2", "dni": "2002", "edad": 23},
    ]

    def enviar_reserva(participantes):
        return gestor.crear_reserva(
            actividad="Safari",
            horario_id=1,
            participantes=participantes,
        )

    # Ejecución en hilos simultáneos (concurrencia)
    with ThreadPoolExecutor(max_workers=2) as executor:
        futuro_a = executor.submit(enviar_reserva, solicitud_a)
        futuro_b = executor.submit(enviar_reserva, solicitud_b)
        res_a = futuro_a.result()
        res_b = futuro_b.result()

    # Resultado:
    # 1. Exactamente una de las dos solicitudes debe tener éxito y la otra debe ser None
    reservas_exitosas = [r for r in [res_a, res_b] if r is not None]
    reservas_rechazadas = [r for r in [res_a, res_b] if r is None]

    assert len(reservas_exitosas) == 1
    assert len(reservas_rechazadas) == 1
    # 2. Los cupos deben quedar exactamente en 0 (sin sobreventa)
    assert gestor.consultar_cupos(actividad="Safari", horario_id=1) == 0
    # 3. La clase debe contar con control de sincronización seguro (lock)
    assert hasattr(gestor, "_lock")
