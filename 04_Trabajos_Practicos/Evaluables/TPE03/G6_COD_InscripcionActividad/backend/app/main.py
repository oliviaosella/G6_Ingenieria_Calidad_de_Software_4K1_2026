from fastapi import FastAPI
# pyrefly: ignore[missing-import]
from app.routers.inscripciones import router as inscripciones_router
from app.routers.consulta_actividades import router as actividades_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

app.include_router(inscripciones_router)
app.include_router(actividades_router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
