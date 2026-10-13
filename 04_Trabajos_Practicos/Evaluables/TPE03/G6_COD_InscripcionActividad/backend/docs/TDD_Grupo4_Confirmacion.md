# Grupo 4 — Confirmación por correo electrónico y QR

## Responsabilidad

Entregar al visitante el comprobante de su inscripción: armar el resumen,
generar un QR asociado a la reserva, enviar el correo y gestionar los
reintentos ante fallos del proveedor. El código vive en
`app/services/confirmacion.py` y `app/services/correo.py`; las pruebas en
`tests/test_confirmacion.py`.

## Contrato para los demás grupos

```python
from app.dependencies import obtener_notificador

notificador = obtener_notificador()          # o Depends(obtener_notificador)
correo = notificador.enviar_confirmacion(inscripcion)  # InscripcionConfirmada
```

- Devuelve el `Correo` enviado.
- Lanza `ServicioCorreoNoDisponibleError` si el envío falla en los 3 intentos.
  La API lo traduce a **HTTP 503 Service Unavailable**.
- Quien llama **no elige** proveedor de correo ni cantidad de reintentos:
  ambos quedan encapsulados en el Grupo 4.

El Grupo 2 (coordinador) lo invoca después de que el Grupo 5 haya guardado la
inscripción (`guardar(inscripcion)`). Si el correo falla, la reserva ya existe:
solo falla la notificación.

## Puertos (patrón Adapter)

| Puerto | Método | Implementa |
|---|---|---|
| `ServicioCorreo` | `enviar(correo: Correo) -> None` (lanza `ServicioCorreoError`) | Grupo 4 — proveedor a definir (smtplib / Resend) |
| `ConsultaHorarios` | `obtener_horario(horario_id: int) -> HorarioDisponible` | Grupo 1 |

`obtener_notificador()` en `app/dependencies.py` es el único lugar donde se
conectan los adaptadores reales. En las pruebas se usan dobles
(`FakeServicioCorreo`, `FakeConsultaHorarios`).

`horario_id` identifica un turno concreto (actividad + fecha + inicio/fin);
por eso se consulta el `HorarioDisponible` para mostrar fecha y hora.

## Decisiones

| Tema | Decisión |
|---|---|
| Reintentos | `MAX_INTENTOS = 3`; agotados → `ServicioCorreoNoDisponibleError` → 503 |
| QR | PNG (librería `qrcode`) que codifica `{URL_BASE}/inscripciones/{id}/validacion`. Validar el QR es otra US |
| Destinatario | `solicitud.email` |
| Asunto | Incluye `#<inscripcion_id>` |
| Cuerpo | Actividad, fecha (`dd/mm/aaaa`), hora de inicio y fin, `Participantes: <n>`, nombre y DNI de cada participante |
| Adjunto | `qr_png`: los bytes devueltos por `generar_qr(inscripcion)` |

## Pruebas planteadas (Red)

| # | Bloque | Comportamiento |
|---|---|---|
| 1 | Contenido | Destinatario = email de la solicitud |
| 2 | Contenido | Asunto incluye el id |
| 3 | Contenido | Cuerpo incluye la actividad (4 actividades) |
| 4 | Contenido | Cuerpo incluye fecha, inicio y fin del turno |
| 5 | Contenido | Se consulta el turno con el `horario_id` de la solicitud |
| 6 | Contenido | Cuerpo incluye la cantidad de participantes |
| 7 | Contenido | Cuerpo incluye nombre y DNI de cada participante |
| 8 | QR | URL de validación con el id |
| 9 | QR | El QR es un PNG |
| 10 | QR | Inscripciones distintas → QR distintos |
| 11 | QR | El correo adjunta el QR de la inscripción |
| 12 | Envío exitoso | Se envía un único correo |
| 13 | Envío exitoso | Falla 2 veces y el 3.º intento lo envía |
| 14 | Fallo | Falla siempre → error tras exactamente 3 intentos |
| 15 | Fallo | La API responde 503 |

## Evidencia del desarrollo

| Paso | Commit | Resultado observado |
|---|---|---|
| Red: primer test de envío (IgnacioMartin) | `a997c82`, `2d09465` | Falla por import: servicio vacío y schema propio |
| Red: suite unificada | (este commit) | 18 casos recolectados; fallan por `NotImplementedError` y 500 ≠ 503 |

### Unificación de las dos versiones paralelas

Se trabajó en paralelo y se combinaron ambas propuestas:

- **Se conservó del primer test:** inyección de dependencias por constructor,
  dobles de prueba propios (fakes), estructura `ARRANGE / ACT / ASSERT` y su
  escenario de datos (inscripción 125, `visitante@gmail.com`, Ana Pérez).
- **Se reemplazó:** el `InscripcionConfirmada` plano por el schema compartido
  con el Grupo 2; el envío con 4 parámetros por un objeto `Correo`; el estado
  `"enviado"` por devolver el `Correo` y lanzar excepción ante fallo (→ 503).
- **Se descartó:** `FakeQrGenerator` / `infrastructure/qr_generator.py`. El QR
  tiene una sola implementación, así que es una función pura (`generar_qr`).
- Su único test queda cubierto por los tests 1, 11 y 12.

## Ejecutar

Desde `backend/`:

```bash
uv sync
uv run python -m pytest tests/test_confirmacion.py -v
```
