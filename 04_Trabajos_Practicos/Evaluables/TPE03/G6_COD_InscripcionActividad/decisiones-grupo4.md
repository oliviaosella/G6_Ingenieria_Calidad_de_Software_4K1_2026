# Decisiones del Grupo 4 — Envío de confirmación de inscripción

| | |
| --- | --- |
| **Historia de usuario** | Inscribirme a actividad |
| **Responsabilidad** | Enviar al visitante un correo de confirmación con el resumen de la inscripción y un código QR |
| **Rama** | `tdd/envio-confirmacion-inscripcion` |
| **Integrantes (GitHub)** | `nachomartinn`, `FacuLescano`, `nachosamo` |
| **Fecha de registro** | 2026-10-19 |

Este documento registra las decisiones importantes que tomó el grupo, para
que al integrar las ramas se sepa qué espera y qué entrega este módulo.

---

## 1. Resumen para integrar (lo mínimo que hay que saber)

1. **Función pública única:**

   ```python
   from app.services import enviar_confirmacion

   enviar_confirmacion(inscripcion)  # inscripcion: dict
   ```

2. **Necesitamos que nos pasen un `dict` plano** con `id`, `email`,
   `actividad`, `fecha` y `horario` (obligatorios) y `participantes`
   (opcional). Ver [sección 3](#3-contrato-de-entrada-datos-que-requerimos).
3. **Requiere un archivo `backend/.env`** con las variables SMTP
   (ver [sección 5](#5-configuración-necesaria)). El archivo no se sube al
   repositorio.
4. **Hay incompatibilidades conocidas** con otras ramas que hay que resolver
   al integrar (ver [sección 7](#7-riesgos-y-pendientes-de-integración)).

---

## 2. Componentes entregados

| Archivo | Contenido |
| --- | --- |
| `backend/app/services/__init__.py` | Exporta `enviar_confirmacion` como punto de entrada. |
| `backend/app/services/email_service.py` | `ServicioNotificaciones`, `preparar_resumen`, `CorreoSMTP`, `_crear_emisor_correo` y la fachada `enviar_confirmacion`. |
| `backend/app/services/qr_service.py` | `generar_qr(inscripcion) -> bytes` (PNG). |
| `backend/tests/test_notificaciones.py` | Tests del resumen y del servicio de notificaciones (con `CorreoFalso`). |
| `backend/tests/test_generacion_qr.py` | Tests del QR (formato PNG, contenido decodificado y unicidad). |
| `backend/tests/test_correo_smtp.py` | Test de `CorreoSMTP` con un servidor SMTP falso (`SMTPFalso`). |

No se modificaron `main.py`, `routers/inscripciones.py` ni `schemas.py`.
El módulo **no expone ningún endpoint**: es un servicio que otro componente
debe invocar.

---

## 3. Contrato de entrada (datos que requerimos)

`enviar_confirmacion` recibe un **diccionario plano** (no un modelo Pydantic).

| Clave | Tipo esperado | ¿Obligatoria? | Uso | Si falta |
| --- | --- | --- | --- | --- |
| `id` | `int` | Sí | Número de inscripción en el resumen y contenido del QR | `KeyError` |
| `email` | `str` | Sí | Destinatario del correo | `KeyError` |
| `actividad` | `str` | Sí | Resumen | `KeyError` |
| `fecha` | `str` (ej. `"2026-10-20"`) | Sí | Resumen | `KeyError` |
| `horario` | `str` (ej. `"14:30"`) | Sí | Resumen | `KeyError` |
| `participantes` | `list[dict]` | No | Detalle de participantes | Se muestra "No se informaron participantes." |

Campos de cada participante (todos opcionales):

| Clave | Etiqueta en el correo |
| --- | --- |
| `nombre` | Se concatena con `apellido` |
| `apellido` | Se concatena con `nombre` |
| `dni` | `DNI` |
| `edad` | `Edad` |
| `talla_vestimenta` | `Talle de vestimenta` ⚠️ ver [riesgo R1](#7-riesgos-y-pendientes-de-integración) |

Ejemplo válido:

```python
inscripcion = {
    "id": 125,
    "email": "visitante@gmail.com",
    "actividad": "Tirolesa",
    "fecha": "2026-10-20",
    "horario": "14:30",
    "participantes": [
        {"nombre": "Juan", "apellido": "Pérez", "dni": "12345678",
         "edad": 25, "talla_vestimenta": "M"},
    ],
}
```

### Qué requerimos de otros grupos

| Dato | Quién debería proveerlo | Estado en su rama |
| --- | --- | --- |
| `id` de la inscripción | Grupo 5 (`gestion-reservas-cupos`) | ✅ `crear_reserva` devuelve `id`. |
| `actividad` | Grupo 5 (`gestion-reservas-cupos`) | ✅ Presente en la reserva. |
| `participantes` | Grupo 3 (`tdd/cargar-participante`) / Grupo 5 | ✅ Presente, pero con `talle_vestimenta` (ver R1). |
| `email` del visitante | Grupo 2 (`tdd/terminos-confirmacion`, `SolicitudInscripcion.email`) | ⚠️ No llega en la reserva del Grupo 5. |
| `fecha` y `horario` legibles | Grupo 1 (`tdd/consultar-actividad`) a partir del turno | ⚠️ La reserva solo tiene `horario_id`. |

---

## 4. Decisiones de diseño

### D-01 · Recibir la inscripción como `dict` y no como modelo Pydantic
- **Decisión:** el servicio trabaja con un diccionario y accede a las claves
  directamente.
- **Motivo:** cuando empezamos, `schemas.py` estaba comentado y no había un
  modelo de inscripción acordado. Un `dict` nos permitió avanzar con TDD sin
  depender de otro grupo.
- **Consecuencia:** al integrar hay que adaptar el modelo final a este
  contrato (o cambiar el contrato con un nuevo ciclo TDD).

### D-02 · Inyección de dependencias del emisor de correo
- **Decisión:** `ServicioNotificaciones` recibe un `emisor_correo` en el
  constructor. Cualquier objeto con el método
  `enviar(destinatario, asunto, contenido, qr)` sirve.
- **Motivo:** poder testear sin mandar correos reales (`CorreoFalso`) y
  desacoplar la lógica de negocio del proveedor SMTP.

### D-03 · Fachada `enviar_confirmacion(inscripcion)`
- **Decisión:** se expone una función de módulo que arma el `CorreoSMTP` real
  desde el `.env` y delega en `ServicioNotificaciones`.
- **Motivo:** que los demás grupos solo tengan que importar una función y
  pasarle la inscripción, sin conocer detalles de SMTP.

### D-04 · Generación del QR
- **Decisión:** se usa la librería `qrcode[pil]`. El QR se devuelve como
  `bytes` en formato PNG y codifica el texto **`RESERVA-{id}`**.
- **Parámetros:** `version=1`, `ERROR_CORRECT_L`, `box_size=10`, `border=4`,
  negro sobre blanco, `fit=True`.
- **Motivo:** el QR debe identificar unívocamente la inscripción; cada `id`
  genera un QR distinto. Se separó en `qr_service.py` para que pueda
  reutilizarse.
- **Consecuencia:** quien valide el QR en el ingreso debe interpretar el
  formato `RESERVA-{id}`.

### D-05 · Formato del correo
- **Asunto fijo:** `Confirmación de inscripción`.
- **Cuerpo:** texto plano (sin HTML), generado por `preparar_resumen`.
- **QR:** como archivo adjunto `inscripcion-qr.png` (`image/png`), no
  embebido en el cuerpo.

### D-06 · Estructura del resumen
- Encabezado `¡Inscripción confirmada!`, sección **DETALLES DE LA ACTIVIDAD**
  (número de inscripción, actividad, fecha, horario) y sección
  **PARTICIPANTES (N)**.
- `N` se calcula con `len(participantes)`; **no se usa
  `cantidad_participantes`** aunque venga en el diccionario.
- Los participantes se numeran (`1. Juan Pérez`). Los campos vacíos o `None`
  se omiten. Si no hay nombre ni apellido se muestra `Sin nombre`.
- Se verifica que nunca se imprima el diccionario crudo (`{'nombre': ...}`).

### D-07 · Envío por SMTP con la librería estándar
- **Decisión:** `smtplib` + `email.message.EmailMessage`, servidor de Gmail
  en el puerto 587 con `STARTTLS`, `timeout=10` segundos y login con
  contraseña de aplicación.
- **Cuenta emisora:** cuenta de Gmail compartida del equipo.
- **Motivo:** no agregar dependencias externas para el envío.

### D-08 · Configuración por variables de entorno
- **Decisión:** las credenciales se leen de `backend/.env` con
  `python-dotenv`. El `.env` está en `backend/.gitignore`.
- **Valores por defecto:** `SMTP_PORT=587`, `SMTP_FROM=SMTP_USER`,
  `SMTP_USE_TLS=true`. `SMTP_HOST`, `SMTP_USER` y `SMTP_PASSWORD` son
  obligatorias (`KeyError` si faltan).
- El `.env` se carga recién al llamar a `enviar_confirmacion`, no al importar
  el módulo, por lo que los tests no lo necesitan.

### D-09 · Sin manejo de errores en el envío
- **Estado actual:** el envío es sincrónico y las excepciones (datos
  faltantes, SMTP caído, credenciales inválidas) se propagan al llamador.
- **Pendiente de acordar:** si un fallo en el correo debe o no cancelar la
  inscripción (ver R5).

---

## 5. Configuración necesaria

Crear `backend/.env` (no se sube al repositorio):

```env
SMTP_HOST="smtp.gmail.com"
SMTP_PORT=587
SMTP_USER="<cuenta de gmail del equipo>"
SMTP_PASSWORD="<contraseña de aplicación>"
SMTP_FROM="<cuenta de gmail del equipo>"
SMTP_USE_TLS=true
```

> La contraseña de aplicación **no se escribe en el repositorio**. Se comparte
> por el canal privado del equipo.

### Dependencias agregadas

| Dependencia | Grupo | Motivo |
| --- | --- | --- |
| `qrcode[pil]` | producción | Generar el QR en PNG |
| `python-dotenv` | producción | Leer el `.env` |
| `opencv-python-headless` | dev | Decodificar el QR en los tests y verificar su contenido |

Se instalan con `uv sync` desde `backend/`.

---

## 6. Decisiones de proceso (TDD)

- **Ciclos RED → GREEN → REFACTOR** registrados en cada mensaje de commit.
- **Primer ciclo sin REFACTOR** (`d867288`): se decidió explícitamente no
  refactorizar porque la implementación mínima ya era suficiente.
- **Triangulación** en los tests del resumen (`760c74c`): se agregaron casos
  con más datos para forzar una implementación general.
- **Fake it till you make it** en el QR (`58a28bd`): primero se devolvió un
  valor fijo y luego se implementó con `qrcode` (`409d3b3`).
- **Dobles de prueba:** `CorreoFalso` (registra los envíos en memoria) y
  `SMTPFalso` (reemplaza `smtplib.SMTP` con `monkeypatch` y registra el orden
  `starttls → login → send_message`).
- **Revert por no respetar TDD** (`027a242`): se revirtió el commit
  `2c5d59e` (envío SMTP en `smtp_sender.py`) porque se agregó código de
  producción sin un test previo. Luego se reimplementó con su ciclo RED/GREEN
  (`8ae668b`) dentro de `email_service.py`.
- **Revert del merge** (`fceef53`): se revirtió el merge `214b997`, que
  solo agregaba `.vscode/settings.json` (configuración local del editor).
- **Eliminación de test obsoleto** (`a8068ce`): se quitó
  `test_enviar_confirmacion_al_correo_del_visitante_EXITO`, reemplazado por
  `test_confirmacion_se_envia_al_visitante` con `CorreoFalso`.

### Evidencia

Desde `backend/`:

```bash
uv run pytest -q
```

Resultado al 2026-10-19: **11 tests aprobados**.

| Archivo | Tests |
| --- | --- |
| `test_notificaciones.py` | `test_resumen_contiene_identificador_inscripcion_EXITO`, `test_resumen_contiene_actividad_inscripcion`, `test_resumen_contiene_datos_inscripcion`, `test_resumen_indica_cuando_no_hay_participantes`, `test_confirmacion_se_envia_al_visitante`, `test_correo_contiene_resumen_inscripcion`, `test_correo_incluye_qr_inscripcion` |
| `test_generacion_qr.py` | `test_generar_qr_inscripcion_exitosa`, `test_qr_contiene_identificador_inscripcion`, `test_qr_es_diferente_para_cada_inscripcion` |
| `test_correo_smtp.py` | `test_correo_smtp_envia_resumen_y_adjunta_qr` |

---

## 7. Riesgos y pendientes de integración

Detectados comparando esta rama con las demás al 2026-10-19. **No se
corrigieron en esta rama**: cada cambio debe hacerse con su ciclo TDD al
integrar.

| # | Problema | Impacto | Propuesta |
| --- | --- | --- | --- |
| R1 | Usamos `talla_vestimenta`; los Grupos 3 y 5 y `schemas.py` de las demás ramas usan **`talle_vestimenta`**. | El talle no aparece en el correo (no falla, se omite). | Renombrar a `talle_vestimenta` en `email_service.py` y en `test_resumen_contiene_datos_inscripcion`. |
| R2 | La reserva del Grupo 5 no tiene `email`, `fecha` ni `horario`; tiene `horario_id`. | `enviar_confirmacion` lanza `KeyError` si se le pasa la reserva tal cual. | Armar el `dict` combinando la reserva (G5), el `email` de la solicitud (G2) y la fecha/horario del turno (G1). |
| R3 | `InscripcionConfirmada` del Grupo 2 usa `inscripcion_id` y la solicitud anidada, no un `dict` plano. | Incompatible con nuestro contrato. | Adaptar en el punto de integración o acordar un único modelo. |
| R4 | Nadie llama todavía a `enviar_confirmacion`; `routers/inscripciones.py` está vacío. | El correo no se envía en el flujo real. | Invocarla después de que `crear_reserva` confirme la reserva. |
| R5 | Sin manejo de errores (D-09). | Un fallo de SMTP puede cortar la respuesta de la inscripción. | Acordar si se captura el error, se reintenta o se informa al usuario. |
| R6 | `requirements.txt` está desactualizado: no incluye `python-dotenv` ni `opencv-python-headless`. | Quien instale con `pip` no puede correr el módulo ni los tests. | Usar `uv sync` o actualizar `requirements.txt`. |
| R7 | Formato del QR `RESERVA-{id}` (D-04). | Si otro grupo valida el QR, debe usar el mismo formato. | Mantener el formato o acordar uno nuevo antes de integrar. |
