# Inscribirme a actividad

Implementación del TP03 con Python y FastAPI en el backend, y React con TypeScript en el frontend.

## Estructura del Backend
```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # Crea la aplicación FastAPI y registra las rutas
│   ├── schemas.py              # Define los datos de entrada y salida
│   └── routers/
│       ├── __init__.py
│       └── inscripciones.py    # Expone las rutas de inscripción
├── tests/
│   └── test_<funcionalidad>.py # Un archivo por funcionalidad o grupo de pruebas
├── pyproject.toml
├── requirements.txt            # para instalar dependencias utilizando pip
└── uv.lock
```

## Inicialización del repositorio

El proyecto se compone de dos partes independientes que se levantan por separado: `backend/` y `frontend/`. Para levantar el repositorio, se deben seguir los pasos correspondientes en cada una de estas carpetas.

### Backend

Desde la raíz del repositorio, entrar en `backend/` y ejecutar:

```bash
cd backend
uv sync
uv run uvicorn app.main:app --reload
```

Esto instala las dependencias indicadas en `pyproject.toml` y `uv.lock`.

La API quedará disponible en `http://127.0.0.1:8000` y su documentación en `/docs`.

Desde `backend/`, ejecutar las pruebas con `uv run python -m pytest`.

### Endpoints disponibles

| Método | Ruta | Resultado |
| --- | --- | --- |
| GET | `/health` | Estado del backend. |
| GET | `/actividades` | Actividades y sus cupos máximos. |
| GET | `/actividades/Safari/turnos?fecha=2026-10-28` | Turnos de la actividad y fecha indicadas. |
| POST | `/inscripciones/validar` | Valida los participantes y las reglas de la actividad. |

La consulta de turnos aplica los cierres y la ventana de 15 minutos a 24 horas,
usando la hora de Córdoba. Una actividad inexistente responde 404; una fecha
inválida o ausente responde 422. La ocupación real todavía no está conectada,
por lo que los turnos no incluyen cupos disponibles.

Ejemplo del cuerpo para `POST /inscripciones/validar`:

```json
{
  "actividad": "Safari",
  "cantidad": 1,
  "participantes": [
    {"nombre": "Ana", "dni": "12345678", "edad": 25}
  ]
}
```

Responde 200 con `{"valida": true}` o `{"valida": false}`. Los datos con
estructura inválida responden 422. Esta ruta no comprueba la disponibilidad
de un turno, no registra reservas ni envía correos.

### Frontend

Desde la raíz del repositorio, entrar en `frontend/` y ejecutar:

```bash
cd frontend
npm ci
npm run dev
```

`npm ci` instala las versiones indicadas en `package-lock.json`. `npm run dev` levanta la aplicación y muestra la dirección local donde queda disponible.

En resumen, la preparación para cada equipo queda unificada así: primero se instalan las dependencias del backend y luego las del frontend, ejecutando cada entorno en su respectiva carpeta.

## Comandos de creación ejecutados

Desde `backend/` se ejecutaron:

```bash
uv init --bare
uv add fastapi uvicorn
uv add --dev pytest
```

Desde `frontend/` se ejecutaron:

```bash
npm create vite@latest . -- --template react-ts
npm install
npm install react-hook-form zod @hookform/resolvers
npm install -D tailwindcss @tailwindcss/vite
```
