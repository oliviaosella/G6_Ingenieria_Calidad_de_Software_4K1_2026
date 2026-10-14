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
