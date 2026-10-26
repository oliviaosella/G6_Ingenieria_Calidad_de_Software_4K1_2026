# Eco Harmony Park · Frontend

Interfaz React + TypeScript para inscribirse a las actividades del parque. Requiere el backend FastAPI iniciado en `http://127.0.0.1:8000`. Para usar otra dirección, definir `VITE_API_URL` en `frontend/.env.local`.

## Ejecutar

Desde la carpeta `frontend`:

```bash
npm ci
npm run dev
```

Abrir la URL indicada por Vite (normalmente `http://localhost:5173`). Para verificar cambios: `npm run build` y `npm run lint`.

El formulario consulta el catálogo, la disponibilidad y los términos en la API. Al confirmar, el backend persiste la reserva, descuenta cupos y genera el QR. El estado del correo se muestra en el comprobante. Las credenciales SMTP se configuran en `backend/.env` según `backend/.env.example`.

## Fechas y cierres

Solo se pueden reservar turnos entre 15 minutos y 24 horas antes de empezar. El selector usa la fecha local del parque (`America/Argentina/Cordoba`) y consulta la disponibilidad real del backend. Los lunes, el 1 de enero y el 25 de diciembre aparecen como cerrados y no se pueden seleccionar. Cuando un día no tiene turnos dentro de la ventana, se muestra deshabilitado con su motivo. La disponibilidad se actualiza mientras el formulario está abierto.

## Reglas visibles en el formulario

El formulario consulta las actividades y cupos del backend. Al cargar participantes, aplica mensajes inmediatos de validación y llama a `POST /inscripciones/validar` antes de avanzar. En ese momento vuelve a consultar el turno para detectar cambios de cupo. La confirmación definitiva vuelve a verificar todas las reglas en el backend: una consulta previa no reserva lugares.

Los términos son específicos por actividad y se envían con la versión mostrada. Si cambiaron antes de confirmar, el formulario carga la versión nueva y solicita otra aceptación. La reserva confirmada muestra el QR del backend y el estado del correo. Si el envío falla, se puede reintentar sin crear otra reserva.

La relación entre los tests de cada grupo y estos comportamientos está en [`backend/docs/TRAZABILIDAD_TDD_FRONTEND.md`](../backend/docs/TRAZABILIDAD_TDD_FRONTEND.md).

Las pruebas automatizadas del backend se ejecutan desde `backend` con `uv run python -m pytest` o con el Python del entorno virtual correspondiente.
