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
