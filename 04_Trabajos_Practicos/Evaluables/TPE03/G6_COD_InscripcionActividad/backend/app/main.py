from fastapi import FastAPI
from routers.inscripciones import router as inscripciones_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

app.include_router(inscripciones_router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
