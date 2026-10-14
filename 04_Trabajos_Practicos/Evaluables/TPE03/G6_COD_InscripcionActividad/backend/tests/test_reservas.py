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
