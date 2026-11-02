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

El calendario consume `GET /actividades/{actividad}/calendario`. El backend determina la fecha local del parque, la ventana de anticipación, los cierres, los turnos y los cupos; el frontend solo dibuja esos datos en una grilla mensual. La disponibilidad se actualiza mientras el formulario está abierto. Antes de avanzar se vuelve a consultar el horario elegido con `GET /actividades/{actividad}/horarios`.

## Reglas visibles en el formulario

El formulario toma del catálogo del backend la descripción, duración, capacidad, edad mínima, obligatoriedad de talle y talles disponibles. Los datos de participantes se envían a `POST /inscripciones/validar` antes de avanzar; las reglas de nombre, DNI, edad y talle no se duplican en el frontend. La confirmación definitiva vuelve a verificar todas las reglas en el backend: una consulta previa no reserva lugares.

El frontend conserva únicamente recursos visuales asociados al identificador de actividad (colores, íconos e ilustraciones). No usa un catálogo local de reglas ni calcula por su cuenta días de cierre, límites de anticipación o identificadores de turnos.

Los términos son específicos por actividad y se envían con la versión mostrada. Si cambiaron antes de confirmar, el formulario carga la versión nueva y solicita otra aceptación. La reserva confirmada muestra el QR del backend y el estado del correo. Si el envío falla, se puede reintentar sin crear otra reserva.

La relación entre los tests de cada grupo y estos comportamientos está en [`backend/docs/TRAZABILIDAD_TDD_FRONTEND.md`](../backend/docs/TRAZABILIDAD_TDD_FRONTEND.md).

Las pruebas automatizadas del backend se ejecutan desde `backend` con `uv run python -m pytest` o con el Python del entorno virtual correspondiente.
