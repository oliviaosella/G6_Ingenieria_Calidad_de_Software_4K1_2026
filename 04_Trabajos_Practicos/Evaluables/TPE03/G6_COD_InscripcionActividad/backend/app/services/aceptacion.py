from app.errors import AceptacionDeOtraActividadError, TerminosNoAceptadosError, TerminosDesactualizadosError
from app.schemas import Actividad, AceptacionTerminos
from app.services.terminos import obtener_terminos


def validar_aceptacion(
    actividad: Actividad,
    aceptacion: AceptacionTerminos,
) -> None:
    if not aceptacion.aceptados:
        raise TerminosNoAceptadosError

    if aceptacion.actividad != actividad:
        raise AceptacionDeOtraActividadError

    if aceptacion.version is not None and aceptacion.version != obtener_terminos(actividad).version:
        raise TerminosDesactualizadosError
