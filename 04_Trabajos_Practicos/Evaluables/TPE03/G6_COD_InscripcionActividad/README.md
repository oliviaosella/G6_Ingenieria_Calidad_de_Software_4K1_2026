# Inscribirme a actividad

Implementación del TP03 con Python y FastAPI en el backend, y React con TypeScript en el frontend.

## Preparación en cada computadora

El proyecto se compone de dos partes independientes que se levantan por separado: `backend/` y `frontend/`. Para levantar el repositorio, se deben seguir los pasos correspondientes en cada una de estas carpetas.

### Backend

Desde la raíz del repositorio, entrar en `backend/` y ejecutar:

```bash
cd backend
uv sync
uv run uvicorn main:app --reload
```

Esto instala las dependencias indicadas en `pyproject.toml` y `uv.lock`.

La API quedará disponible en `http://127.0.0.1:8000` y su documentación en `/docs`.

### Frontend

Desde la raíz del repositorio, entrar en `frontend/` y ejecutar:

```bash
cd frontend
npm ci
npm run dev
```

`npm ci` instala las versiones indicadas en `package-lock.json`. `npm run dev` levanta la aplicación y muestra la dirección local donde queda disponible.

En resumen, la preparación para cada equipo queda unificada así: primero se instalan las dependencias del backend y luego las del frontend, ejecutando cada entorno en su respectiva carpeta.

## Inicialización del proyecto

### Backend

Desde `backend/` se ejecutaron:

```bash
uv init --bare
uv add fastapi uvicorn
uv add --dev pytest
```

### Frontend

Desde `frontend/` se ejecutaron:

```bash
npm create vite@latest . -- --template react-ts
npm install
npm install react-hook-form zod @hookform/resolvers
npm install -D tailwindcss @tailwindcss/vite
```
