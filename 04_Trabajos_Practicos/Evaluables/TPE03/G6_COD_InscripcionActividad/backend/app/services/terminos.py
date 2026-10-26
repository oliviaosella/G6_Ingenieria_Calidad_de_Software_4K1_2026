from hashlib import sha256

from app.schemas import Actividad, TerminosCondiciones

# Propuesta funcional para el TP; requiere validación del PO antes de su aprobación.
_COMUNES = (
    "La inscripción corresponde exclusivamente a la actividad, fecha, turno y participantes indicados. "
    "La consulta de disponibilidad no reserva lugares; la confirmación depende de los cupos al registrar la inscripción. "
    "Se aceptan inscripciones entre 15 minutos y 24 horas antes del turno. "
    "El parque permanece cerrado los lunes, el 1 de enero y el 25 de diciembre. "
    "No se permite inscribir al mismo DNI en dos actividades en el mismo turno y fecha. "
    "Los datos declarados deben ser correctos. La persona que realiza la inscripción acepta estas condiciones "
    "para los participantes que registra. Se deben seguir las indicaciones del personal."
)
_ESPECIFICOS = {
    Actividad.TIROLESA: (
        "Tirolesa: edad mínima de 8 años y talle de vestimenta obligatorio entre XS y XXL. "
        "Capacidad máxima de 10 participantes por turno. El equipo se utiliza según las indicaciones del instructor."
    ),
    Actividad.SAFARI: (
        "Safari: actividad para todas las edades, sin talle de vestimenta obligatorio. "
        "Capacidad máxima de 8 participantes por turno. Durante el recorrido se deben respetar "
        "las zonas habilitadas y las indicaciones del personal."
    ),
    Actividad.PALESTRA: (
        "Palestra: edad mínima de 12 años y talle de vestimenta obligatorio entre XS y XXL. "
        "Capacidad máxima de 12 participantes por turno. El ascenso se realiza con el equipo "
        "provisto y siguiendo las indicaciones del instructor."
    ),
    Actividad.JARDINERIA: (
        "Jardinería: actividad para todas las edades, sin talle de vestimenta obligatorio. "
        "Capacidad máxima de 12 participantes por turno. Las herramientas se utilizan "
        "en las áreas habilitadas y siguiendo las indicaciones del personal."
    ),
}


def obtener_terminos(actividad: Actividad) -> TerminosCondiciones:
    texto = f"{_ESPECIFICOS[actividad]}\n\n{_COMUNES}"
    # Cambiar el texto cambia su versión, evitando aceptar silenciosamente otro documento.
    version = sha256(texto.encode("utf-8")).hexdigest()[:16]
    return TerminosCondiciones(actividad=actividad, texto=texto, version=version, pendiente_aprobacion=True)
