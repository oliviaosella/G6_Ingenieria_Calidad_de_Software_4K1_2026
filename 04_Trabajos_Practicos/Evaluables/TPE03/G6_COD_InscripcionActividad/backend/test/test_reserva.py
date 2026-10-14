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