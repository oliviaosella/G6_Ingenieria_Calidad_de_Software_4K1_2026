from fastapi import APIRouter

router = APIRouter(prefix="/inscripciones", tags=["inscripciones"])

"""
Acá van las funciones que desarrollaría cada grupo
"""

@router.post("/notificar")
async def enviar_notificacion(inscripcion: dict) -> dict:
    return {"Datos de la inscripción": inscripcion["visitante"], "mensaje": "Notificación enviada correctamente."}