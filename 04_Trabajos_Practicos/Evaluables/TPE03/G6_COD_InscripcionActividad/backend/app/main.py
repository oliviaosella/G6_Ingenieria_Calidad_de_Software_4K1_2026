from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.actividades import router as actividades_router
from app.routers.inscripciones import router as inscripciones_router

app = FastAPI(
    title="Eco Harmony Park - API de Inscripción a Actividades",
    description=(
        "API RESTful para la consulta de catálogo de actividades, turnos y cupos en tiempo real, "
        "términos y condiciones, y registro de inscripciones con confirmación y emisión de código QR."
    ),
    version="1.0.0",
    openapi_tags=[
        {
            "name": "Actividades",
            "description": "Consulta de catálogo, términos y condiciones y disponibilidad de turnos con cupos.",
        },
        {
            "name": "Inscripciones",
            "description": "Orquestación de inscripciones a actividades y consulta de reservas.",
        },
        {
            "name": "Salud",
            "description": "Monitoreo del estado y disponibilidad del servicio.",
        },
    ],
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(actividades_router)
app.include_router(inscripciones_router)


@app.get("/health", tags=["Salud"], summary="Verificar estado del servicio")
def health() -> dict[str, str]:
    return {"status": "ok"}
