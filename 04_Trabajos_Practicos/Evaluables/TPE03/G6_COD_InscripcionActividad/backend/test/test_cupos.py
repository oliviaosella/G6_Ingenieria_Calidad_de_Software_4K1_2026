from model.cupos import *

def test_calcular_cupos_disponibles():
    resultado = calcular_cupos_disponibles(10,3)
    assert resultado == 7