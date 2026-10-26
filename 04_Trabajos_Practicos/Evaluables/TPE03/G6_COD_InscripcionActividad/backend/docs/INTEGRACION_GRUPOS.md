# Integración de actividades, participantes, términos, reservas y envío

## Ramas y alcance

Base: `origin/tdd/integracion/participantes-actividades` (`1f0e799`).
Rama incorporada: `origin/tdd/integracion/terminos-reserva-envio` (`00ef906`).
La combinación se prepara en `codex/integracion-grupos-1-a-5`.

La integración cubre el backend. El frontend y sus simulaciones locales no
se modifican en esta rama.

## Resoluciones del merge

- Se conserva un solo catálogo HTTP en `/actividades`, con el formato detallado
  y los alias `nombre` y `cupo_maximo` del contrato anterior. Los tests HTTP que
  exigían exclusivamente dos campos se adaptan a esta ampliación del contrato.
- Se conserva `HorarioDisponible` con actividad, fecha, hora y estado de cupos,
  utilizado por el grupo de consulta. `/horarios` añade el identificador de turno
  requerido por el grupo de reservas. Ambas rutas aplican las mismas reglas.
- Se conservan los metadatos de `Actividad` y `TalleVestimenta`, junto con los
  modelos de solicitud, aceptación, confirmación y consulta de reserva.
- La validación de participantes se extrae a `services/participantes.py` para
  reutilizarla desde el registro definitivo sin dependencias circulares entre
  routers y servicios. Se mantienen los imports anteriores mediante reexportación.
- Se conservan tanto `/inscripciones/validar` como el registro y consulta de
  inscripciones, y se registra cada router una sola vez en FastAPI.
- Se combinan dependencias y se regenera `uv.lock`. `httpx2` se conserva para
  el TestClient de la versión actual de Starlette; las pruebas QR usan OpenCV.

## Flujo integrado

1. Consultar `GET /actividades`.
2. Consultar `GET /actividades/{actividad}/horarios?fecha=YYYY-MM-DD`.
3. Cargar participantes; opcionalmente validar con `POST /inscripciones/validar`.
4. Consultar y aceptar `GET /actividades/{actividad}/terminos`.
5. Enviar `POST /inscripciones` con el turno y todos los datos.
6. El backend vuelve a validar apertura, anticipación, correspondencia de hora e
   identificador, términos, cantidad, nombres, DNI, edades y talles. Después
   confirma la reserva de forma atómica y envía la confirmación con QR.
7. Consultar `GET /inscripciones/{id}` o volver a consultar los cupos del turno.

`horario_id` representa un inicio diario: 1 es 09:00, 2 es 10:00, hasta 9 que
representa 17:00. La fecha forma parte de la identidad del turno y de la ocupación.
Los cupos se separan por actividad, fecha e identificador; el control de DNI
superpuesto se separa por fecha e identificador, abarcando todas las actividades.

Para llamadas anteriores sin fecha, los métodos de `GestorReservas` conservan un
espacio sin fecha independiente, utilizado por sus tests unitarios históricos.
El flujo HTTP integrado siempre suministra una fecha concreta.

Ejemplo de solicitud:

```json
{
  "actividad": "Tirolesa",
  "horario_id": 2,
  "fecha": "2026-10-27",
  "horario": "10:00",
  "cantidad_participantes": 1,
  "participantes": [
    {"nombre": "Ana Pérez", "dni": "12345678", "edad": 25, "talle_vestimenta": "M"}
  ],
  "aceptacion_terminos": {"actividad": "Tirolesa", "aceptados": true},
  "email": "ana@example.com"
}
```

El ejemplo requiere consultar en un momento válido: entre 15 minutos y 24 horas
antes del turno. El reloj de producción utiliza la hora de Argentina.
Se recomienda enviar siempre `fecha` y `horario`; por compatibilidad, si se
omiten se usa la fecha actual del parque y la hora derivada de `horario_id`.

## Respuestas y errores

- 201: inscripción registrada; `qr_codigo` identifica el contenido `RESERVA-{id}`.
  El correo adjunta el PNG del QR y el resumen de la inscripción.
- 400: términos, participantes, calendario o correspondencia de turno inválidos.
- 404: actividad inexistente en `/turnos`, o reserva inexistente.
- 409: cupos insuficientes o participante ya registrado en ese turno.
- 422: estructura de solicitud inválida, fecha inválida, enum no reconocido o
  `horario_id` fuera del rango 1 a 9. `/horarios` valida la actividad como enum.

La validación previa de participantes es informativa. El POST definitivo vuelve
a validar los participantes y los cupos, sin confiar en una consulta anterior.

## Configuración y ejecución

Desde `backend`:

```bash
uv sync
uv run python -m pytest -q
uv run uvicorn app.main:app --reload
```

OpenAPI se encuentra en `/docs`. Para enviar correo real, crear `backend/.env`
con `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASSWORD`, `SMTP_FROM` y
`SMTP_USE_TLS`. No subir credenciales al repositorio. El servicio conserva la
configuración SMTP estricta de la rama de origen; no tiene envío ficticio implícito.

## Validación de la integración

Se conservan las suites de ambos orígenes. Se agregan 20 casos en
`tests/test_integracion_completa.py` para verificar:

- Recorrido HTTP desde catálogo, términos y validación hasta reserva consultable,
  actualización de cupos en ambos endpoints y correo con QR PNG.
- Rechazo de nombre, DNI, edad y talle inválidos, y de DNIs duplicados dentro
  de una solicitud, sin reservar ni enviar correo.
- Mismas reglas de lunes, festivos y anticipación en consulta y confirmación.
- Rechazo de IDs fuera de rango, hora incompatible y fecha inválida.
- Independencia de cupos y DNIs entre fechas distintas.
- Último lugar, consulta del turno lleno y rechazo de la siguiente solicitud.
- Ausencia de rutas HTTP duplicadas.

Los tests usan relojes fijos y emisores en memoria; no envían correos reales.
Las pruebas de concurrencia y decodificación del QR de las ramas de origen
también se ejecutan en la suite conjunta.

## Límites heredados

- Las reservas se almacenan en memoria del proceso. Reiniciar o ejecutar varios
  workers no proporciona persistencia compartida.
- Si SMTP falla después de registrar una reserva, la reserva permanece registrada.
  No se agrega una política de reintentos ni de compensación en esta integración.
- Los términos conservan el texto de muestra de la rama de origen.
