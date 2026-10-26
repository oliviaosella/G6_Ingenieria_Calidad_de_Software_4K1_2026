# Cierre del backend de integración

## Ejecutar

Desde `backend`:

```bash
uv sync --locked
uv run python -m pytest -q
uv run uvicorn app.main:app --reload
```

La suite incluye tests anteriores y nuevos: 164 casos pasan. No requiere credenciales
reales. Los tests bloquean SMTP, aíslan la configuración local y usan bases temporales.
La verificación automática no envía correos ni comprueba la entrega en Gmail.

## Gmail y contrato público

Copiar `.env.example` a `.env` y completar la cuenta, el remitente y una contraseña
de aplicación. Configuración: `SMTP_HOST=smtp.gmail.com`, `SMTP_PORT=587`,
`SMTP_USE_TLS=true`. El archivo `.env` local y la base están ignorados por Git.
Cada integrante necesita su propia configuración local; las credenciales no se
incluyen al descargar la rama. Las variables de entorno prevalecen sobre `.env`.
No registrar contraseñas en código, commits, capturas o mensajes de error.

Gmail utiliza STARTTLS con validación del certificado. Se admiten contraseñas de
aplicación copiadas con espacios, que se normalizan antes de autenticar.
También se admite SMTP con SSL implícito en el puerto 465.

El contrato público existente sigue disponible:

```python
from app.services import enviar_confirmacion

enviar_confirmacion({
    "id": 1,
    "actividad": "Safari",
    "fecha": "2026-10-27",
    "horario": "10:00",
    "email": "visitante@example.com",
    "participantes": [{"nombre": "Ana Pérez", "dni": "12345678", "edad": 25}],
})
```

Esta función hace un envío directo y propaga errores al llamador; no crea ni descuenta
reservas. Para el flujo de inscripción se debe utilizar el endpoint, que guarda
los datos y maneja estados y reintentos. El ejemplo contiene un destinatario ficticio.

## Confirmación y fallo de envío

`POST /inscripciones` devuelve 201 cuando registra la reserva, independientemente
de que el proveedor de correo esté disponible. La respuesta separa:

- `estado`: `confirmada`.
- `correo_estado`: `pendiente`, `enviando`, `enviado` o `fallido`.
- `correo_error`: mensaje genérico recuperable, sin credenciales ni respuesta
  técnica del proveedor; `null` después de un envío exitoso.
- `intentos_envio`: cantidad de intentos reclamados para esa reserva.

`enviado` significa que SMTP aceptó el mensaje; no demuestra recepción o lectura
en la bandeja del destinatario. El frontend debe mostrar la reserva confirmada
aunque el correo falle y ofrecer el comprobante y la opción de reintentar.

`POST /inscripciones/{id}/reenviar-confirmacion` vuelve a utilizar el destinatario
y los datos originales. No crea una segunda reserva ni descuenta otros cupos.
Si ya se envió, devuelve su estado sin enviar otra vez. Se evita que dos solicitudes
simultáneas reclamen el mismo envío. Si un proceso se interrumpe durante el envío,
se puede volver a reclamar después de cinco minutos.

SMTP no ofrece confirmación transaccional conjunta con SQLite: un corte de conexión
después de que el proveedor aceptó un correo puede dejar un resultado ambiguo.
El reintento manual podría reenviarlo en ese caso; no se promete entrega exactamente
una vez. No se implementan reintentos automáticos ni tareas en segundo plano.

## QR y comprobante

El correo y el QR comparten una única fuente de datos. El QR contiene JSON UTF-8 con:

- Versión del formato, referencia `RESERVA-{id}` e ID.
- Actividad, fecha, horario y correo.
- Cantidad de participantes y datos de cada uno: nombre, apellido cuando exista,
  DNI, edad y talle cuando corresponda.

La respuesta conserva `qr_codigo` como referencia corta y agrega `qr_contenido`
con el JSON y `qr_url` con una ruta relativa del backend.
`GET /inscripciones/{id}/qr` descarga el PNG con la misma información que se adjunta
al correo. El frontend debe resolver la URL respecto de su URL base de API.

Se verificó la decodificación con OpenCV, incluyendo 12 participantes y nombres
acentuados. Si los datos son demasiado extensos para un solo QR, se rechaza la
solicitud con 422 antes de registrar o descontar cupos.

## Términos y aceptación

`GET /actividades/{actividad}/terminos` devuelve:

- `actividad` y texto específico.
- `version`, derivada del contenido: modificar el texto cambia la versión.
- `pendiente_aprobacion=true`: son propuestas para que valide el PO, no textos
  aprobados ni una exención de responsabilidad.

Los textos incluyen las reglas ya acordadas: edades, talles, capacidades, horarios
de inscripción, cierres y restricciones de superposición de DNI. No agregan reglas
de cancelación ni cobros.

El frontend debe enviar la versión que mostró en
`aceptacion_terminos.version`. Si no coincide con la vigente, se responde 400
antes de reservar. Por compatibilidad con clientes anteriores puede omitirse;
en ese caso se registra la versión vigente al confirmar.

La reserva guarda actividad, aceptación, versión, copia del texto y fecha UTC de
aceptación, obtenida del servidor. Un cambio posterior de términos no reescribe
la evidencia de una inscripción ya confirmada.

## Persistencia

La aplicación usa `backend/data/reservas.sqlite3`; puede cambiarse la ruta mediante
la variable de entorno `RESERVAS_DB_PATH`. Las transacciones SQLite conservan juntos
reserva, cupos y DNI. La fecha forma parte de la identidad del turno.

Se prueban reinicio/reapertura y competencia entre dos gestores conectados al mismo
archivo por el último lugar. Para tests unitarios, `GestorReservas()` sigue usando
SQLite en memoria; la aplicación crea el gestor con una ruta persistente.

La base contiene datos de participantes y no se publica en Git. Esta configuración
está destinada a la ejecución local del TP. El frontend todavía conserva su demo
hasta que se realice la integración HTTP.
