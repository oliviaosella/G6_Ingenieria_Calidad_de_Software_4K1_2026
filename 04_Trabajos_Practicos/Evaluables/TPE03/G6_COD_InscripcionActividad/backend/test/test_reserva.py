from model.inscripcion import *


def test_registrar_reserva_sin_cupos():
   actividad = {
       "actividad_id": 1,
       "horario_id": 1,
       "usuario": "usuario1",
       "cupos_totales": 10,
       "inscriptos":8
       
   }
   resultado = registrar_reserva(actividad,3,[])
   assert resultado == False
   assert actividad["inscriptos"] == 8
   
def test_registrar_reserva_con_cupos():
    actividad = {
         "actividad_id": 1,
         "horario_id": 1,
         "usuario": "usuario1",
         "cupos_totales": 10,
         "inscriptos":8
         
    }
    resultado = registrar_reserva(actividad,2,[])
    assert resultado == True
    assert actividad["inscriptos"] == 10
    
def test_registrar_reserva_cantidad_negativa():
    actividad = {
         "actividad_id": 1,
         "horario_id": 1,
         "usuario": "usuario1",
         "cupos_totales": 10,
         "inscriptos":8
         
    }
    resultado = registrar_reserva(actividad,-1,[])
    assert resultado == False
    assert actividad["inscriptos"] == 8
    
def test_registrar_doble_reserva():
    actividad = {
        "actividad_id": 1,
        "horario_id": 1,
        "usuario": "usuario1",
        "cupos_totales": 10,
        "inscriptos":8
    }
    resultado1 = registrar_reserva(actividad,1,[])
    resultado2 = registrar_reserva(actividad,2,[])
    assert resultado1 == True
    assert resultado2 == False
    assert actividad["inscriptos"] == 9
    
def test_registrar_reserva_actividad_none():
    actividad = None
    resultado = registrar_reserva(actividad,1,[])
    assert resultado == False
    
def test_reserva_asociada_a_actividad_horario_usuario():
    actividad = {
        "actividad_id": 1,
        "horario_id": 1,
        "usuario": "usuario1",
        "cupos_totales": 10,
        "inscriptos": 8
    }

    reservas = []

    resultado = registrar_reserva(actividad, 2, reservas)

    assert resultado is True
    assert len(reservas) == 1
    assert reservas[0]["actividad_id"] == 1
    assert reservas[0]["horario_id"] == 1
    assert reservas[0]["usuario"] == "usuario1"
    assert reservas[0]["cantidad_reservada"] == 2

def test_no_registrar_reserva_sin_cupos():
    actividad = {
        "actividad_id": 1,
        "horario_id": 1,
        "usuario": "usuario1",
        "cupos_totales": 10,
        "inscriptos": 10
    }

    reservas = []

    resultado = registrar_reserva(actividad, 1, reservas)

    assert resultado is False
    assert len(reservas) == 0
    assert actividad["inscriptos"] == 10
    
def test_reserva_asoaciada_a_actividad_horario_usuario_doble():
    actividad ={
       "actividad_id": 1,
        "horario_id": 1,
        "usuario": "usuario1",
        "cupos_totales": 10,
        "inscriptos": 8 
    }
    reservas = []
    resultado = registrar_reserva(actividad,1,reservas)
    resultado2 = registrar_reserva(actividad,1,reservas)
    assert resultado == True
    assert resultado2 == True
    assert len(reservas) == 2
    assert reservas[0]["actividad_id"] == 1
    assert reservas[0]["horario_id"] == 1
    assert reservas[0]["usuario"] == "usuario1"
    assert reservas[0]["cantidad_reservada"] == 1
    