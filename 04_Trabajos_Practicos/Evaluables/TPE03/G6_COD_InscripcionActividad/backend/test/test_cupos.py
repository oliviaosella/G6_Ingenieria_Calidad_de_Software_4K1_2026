from model.cupos import *

def test_calcular_cupos_disponibles():
    resultado = calcular_cupos_disponibles(10,3)
    assert resultado == 7
    
def test_no_permite_reservar():
    resultado = puede_reservar(5,5,2)
    assert resultado == False
    
def test_permite_reservar():
    resultado = puede_reservar(5,3,2)
    assert resultado == True

def test_actualizar_cupos_disponibles():
    resultado = actualizar(10,3,2)
    assert resultado == 5

def test_cantidad_reservar_positiva():
    resultado = puede_reservar(10,3,-1)
    assert resultado == False
