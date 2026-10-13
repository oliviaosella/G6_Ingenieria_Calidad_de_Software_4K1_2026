class TerminosNoDisponiblesError(Exception):
    """No se pueden obtener los términos de la actividad."""


class TerminosNoAceptadosError(Exception):
    """El visitante no aceptó los términos de la actividad."""


class AceptacionDeOtraActividadError(Exception):
    """La aceptación corresponde a una actividad distinta de la solicitada."""
