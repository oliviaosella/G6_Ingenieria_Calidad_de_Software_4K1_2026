from app.errors import TerminosNoAceptadosError
from app.schemas import Actividad, AceptacionTerminos


def validar_aceptacion(
    actividad: Actividad,
    aceptacion: AceptacionTerminos,
) -> None:
    if not aceptacion.aceptados:
        raise TerminosNoAceptadosError
