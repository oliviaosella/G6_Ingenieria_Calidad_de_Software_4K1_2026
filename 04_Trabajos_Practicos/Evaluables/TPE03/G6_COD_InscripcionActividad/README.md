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
| GET | `/actividades` | Catálogo detallado, capacidades y reglas por actividad. |
| GET | `/actividades/Safari/turnos?fecha=2026-10-28` | Turnos elegibles con cupos reales del gestor. |
| GET | `/actividades/Safari/horarios?fecha=2026-10-28` | Misma disponibilidad, incluyendo `horario_id` para reservar. |
| GET | `/actividades/Safari/terminos` | Términos específicos de la actividad. |
| POST | `/inscripciones/validar` | Valida los participantes y las reglas de la actividad. |
| POST | `/inscripciones` | Valida el turno y los participantes, acepta términos, reserva y envía correo con QR. |
| GET | `/inscripciones/1` | Recupera la reserva y su aceptación y estado de correo. |
| GET | `/inscripciones/1/qr` | Descarga el QR con los datos completos. |
| POST | `/inscripciones/1/reenviar-confirmacion` | Reintenta un envío fallido sin volver a reservar. |

La consulta de turnos aplica los cierres y la ventana de 15 minutos a 24 horas,
usando la hora de Córdoba. Una actividad inexistente responde 404; una fecha
inválida o ausente responde 422. Ambas consultas de turnos usan el mismo gestor
de reservas: después de confirmar una inscripción, sus cupos se actualizan.
El catálogo conserva `nombre` y `cupo_maximo` como alias de `id` y `cupo` para
facilitar la transición entre los contratos de ambas ramas.

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

La integración completa y su configuración SMTP se describen en
[backend/docs/INTEGRACION_GRUPOS.md](backend/docs/INTEGRACION_GRUPOS.md).
Las reservas, cupos, aceptación de términos y estados de envío se conservan en
SQLite (`backend/data/reservas.sqlite3`). La base y las credenciales `.env` no se
versionan. El detalle del cierre está en
[backend/docs/CIERRE_BACKEND.md](backend/docs/CIERRE_BACKEND.md).

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
