from app.services.email_service import preparar_resumen

def test_resumen_contiene_identificador_inscripcion_EXITO() -> None:
    #Preparar
    inscripcion = {
        "id": 125,
        "email": "visitante@gmail.com",
        "actividad": "Tirolesa",
        "fecha": "2026-10-20",
        "horario": "14:30"
    }

    # Resultados
    resumen = preparar_resumen(inscripcion)
    
    # Validar
    assert "125" in resumen


def test_resumen_contiene_actividad_inscripcion() -> None:
    # ARRANGE
    inscripcion = {
        "id": 125,
        "email": "visitante@gmail.com",
        "actividad": "Tirolesa",
        "fecha": "2026-10-20",
        "horario": "14:30"
    }

    # ACT
    resumen = preparar_resumen(inscripcion)

    # ASSERT
    assert "Tirolesa" in resumen


def test_resumen_contiene_datos_inscripcion() -> None:
    # ARRANGE
    inscripcion = {
        "id": 125,
        "email": "visitante@gmail.com",
        "actividad": "Tirolesa",
        "fecha": "2026-10-20",
        "horario": "14:30",
        "cantidad_participantes": 2,
        "participantes": [{
            "nombre": "Juan",
            "apellido": "Pérez",
            "dni": "12345678",
            "talla_vestimenta": None
        },
        {
            "nombre": "María",
            "apellido": "Gómez",
            "dni": "87654321",
            "talla_vestimenta": None
        }
        ]

    }

    # ACT
    resumen = preparar_resumen(inscripcion)

    # ASSERT
    assert "125" in resumen
    assert "Tirolesa" in resumen
    assert "2026-10-20" in resumen
    assert "14:30" in resumen
    assert "Juan" in resumen
    assert "Pérez" in resumen
    assert "12345678" in resumen
    assert "María" in resumen
    assert "Gómez" in resumen
    assert "87654321" in resumen


def test_resumen_actividad_requiere_vestimenta() -> None:
    # TODO: Implementar test para verificar que el resumen de la inscripcion incluya información sobre la vestimenta si la actividad lo requería.
    pass


def test_enviar_confirmacion_al_correo_del_visitante_EXITO() -> None:
    #Preparar
    inscripcion = {
        "id": 125,
        "email": "visitante@gmail.com",
        "actividad": "Tirolesa",
        "fecha": "2026-10-20",
        "horario": "14:30"
    }

    resultado = enviar_confirmacion(inscripcion)
    #Resultados

    #Verificar
    assert inscripcion['email'] in resultado