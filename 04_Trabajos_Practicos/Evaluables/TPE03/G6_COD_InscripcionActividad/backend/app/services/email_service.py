def preparar_resumen(inscripcion):
    return f"""Id inscripción: {inscripcion['id']} - Actividad: {inscripcion['actividad']}\n
                Fecha: {inscripcion['fecha']} - Horario: {inscripcion['horario']}\n
                Inscriptos: {inscripcion.get('participantes', [])}\n"""

def enviar_confirmacion(inscripcion):
    return inscripcion['email']