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

## Modo demostración

Con `npm run dev`, desplegar «Modo demostración · casos de prueba» sobre el formulario. Los casos de edad mínima, talle, DNI repetido y datos válidos precargan participantes. «Ejecutar validación» muestra el resultado obtenido y el esperado. El panel también permite comprobar los tres días de cierre de las FAQ.

Este modo usa la validación del frontend y las reglas de cierre visibles; no ejecuta la suite Python, no persiste reservas y no envía correos. Los nombres de tests mostrados son referencias a las pruebas del backend. El modo de demostración no se incluye en la compilación de producción. Para volver al formulario normal, pulsar «Volver a reserva real».

Las pruebas automatizadas del backend se ejecutan desde `backend` con `uv run python -m pytest` o con el Python del entorno virtual correspondiente.
