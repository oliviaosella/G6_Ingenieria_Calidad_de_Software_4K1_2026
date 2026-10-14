from model.inscripcion import *


def test_registrar_reserva_sin_cupos():
   actividad = {
       "actividad_id": 1,
       "horario_id": 1,
       "usuario": "usuario1",
       "cupos_totales": 10,
       "inscriptos":8
       
   }
   resultado = registrar_reserva(actividad,3)
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
    resultado = registrar_reserva(actividad,2)
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
    resultado = registrar_reserva(actividad,-1)
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
    resultado1 = registrar_reserva(actividad,1)
    resultado2 = registrar_reserva(actividad,1)
    assert resultado1 == True
    assert resultado2 == False