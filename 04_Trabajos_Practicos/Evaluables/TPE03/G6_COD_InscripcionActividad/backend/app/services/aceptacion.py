from app.errors import AceptacionDeOtraActividadError, TerminosNoAceptadosError
from app.schemas import Actividad, AceptacionTerminos


def validar_aceptacion(
    actividad: Actividad,
    aceptacion: AceptacionTerminos,
) -> None:
    if not aceptacion.aceptados:
        raise TerminosNoAceptadosError

    if aceptacion.actividad != actividad:
        raise AceptacionDeOtraActividadError
