# Trazabilidad TDD: pruebas del backend y experiencia de inscripción

Esta revisión contrasta la documentación de los cinco subgrupos con los tests que se ejecutan en el backend integrado. La evidencia RED–GREEN–REFACTOR pertenece al historial y a las bitácoras; la interfaz muestra los comportamientos resultantes durante una inscripción normal. No ejecuta pytest ni crea reservas ficticias.

## Inventario de la suite

`python -m pytest --collect-only -q` recoge **171 casos** (incluidas parametrizaciones) en 15 archivos:

| Archivo | Casos | Alcance principal |
| --- | ---: | --- |
| `test_consulta_actividades.py` | 16 | Catálogo, horarios, cierres, anticipación y cupos. |
| `test_endpoints.py` | 7 | Contratos HTTP de actividades, turnos y validación. |
| `test_terminos.py` | 12 | Textos específicos y estabilidad de términos. |
| `test_aceptacion.py` | 32 | Aceptación, actividad correspondiente y prioridad de errores. |
| `test_participantes.py` | 12 | Nombre, DNI, edad, talle, cantidad y cupo máximo. |
| `test_notificaciones.py` | 8 | Resumen, destinatario, QR e inyección de dependencias. |
| `test_generacion_qr.py` | 3 | PNG, identificador y unicidad del QR. |
| `test_comprobante_legible.py` | 1 | Coherencia entre QR y correo. |
| `test_correo_smtp.py` | 1 | Envío SMTP con servidor falso. |
| `test_reservas.py` | 12 | Cupos, solapamientos, persistencia y concurrencia. |
| `test_integracion_inscripcion.py` | 3 | Contrato compartido y cupos en la inscripción. |
| `test_integracion.py` | 8 | Orquestación de términos, reserva, correo y rechazos. |
| `test_integracion_completa.py` | 20 | Recorrido HTTP y reglas cruzadas entre grupos. |
| `test_api_endpoints.py` | 21 | Catálogo, calendario, cierres, términos, registro, errores y CORS. |
| `test_cierre_backend.py` | 15 | SQLite, QR completo, fallos y reintentos de correo. |

Los conteos son casos recogidos, no cantidad de funciones `test_`; los tests parametrizados generan más de un caso. La suite usa relojes fijos, bases temporales y correo falso: no envía mensajes reales.

## Qué se refleja en la aplicación

| Grupo y evidencia TDD | Comportamiento visible | Garantía que sigue en el backend |
| --- | --- | --- |
| **1 · Consulta.** `test_consulta_actividades.py`, `test_endpoints.py`, `test_api_endpoints.py`. | Catálogo y calendario del API; el backend informa qué fechas están cerradas, la ventana de anticipación, los turnos y los cupos. | El backend calcula disponibilidad y vuelve a validar fecha y horario al reservar. |
| **2 · Términos.** `TDD_Juani_Integrante_2.md`, `test_terminos.py`, `test_aceptacion.py`. | Se consulta el texto de la actividad elegida y se exige su aceptación. Se envía la versión mostrada; ante cambio, se recarga y se vuelve a solicitar aceptación. | Rechaza términos no aceptados, de otra actividad o desactualizados antes de reservar. |
| **3 · Participantes.** `BITACORA_TDD_PARTICIPANTES.md`, `test_participantes.py`. | El catálogo informa edad mínima y talles disponibles; el botón de agregar respeta el cupo consultado. Antes de avanzar se llama a `/inscripciones/validar` y se muestra su resultado. | El POST final comprueba cantidad, datos individuales y reglas de la actividad otra vez. |
| **4 · Correo y QR.** `decisiones-grupo4.md`, `test_notificaciones.py`, `test_generacion_qr.py`, `test_correo_smtp.py`, `test_comprobante_legible.py`. | La confirmación muestra el QR generado por el backend y el estado de correo. Si falla, ofrece reintentar sin crear otra reserva. | Los tests verifican el contenido del comprobante, el envío con un SMTP falso y que el fallo no borra la reserva. |
| **5 · Reservas y cupos.** `TDD_Grupo5_Reservas_Cupos.md`, `test_reservas.py`. | Se vuelve a consultar el cupo antes de pasar a confirmar; si se agotó, se pide elegir otro turno. Se informa un rechazo 409 del POST si alguien tomó los últimos lugares. | SQLite aplica el descuento atómico, evita DNI solapado y sobreventa, y conserva la reserva tras reinicios. |

`test_integracion.py`, `test_integracion_completa.py`, `test_api_endpoints.py` y `test_cierre_backend.py` verifican que esas piezas funcionen juntas. La consulta previa de cupos y participantes ayuda a la persona usuaria, pero **no sustituye** la validación del POST definitivo: entre ambas llamadas puede cambiar la disponibilidad.

## Qué no corresponde mostrar como interacción del formulario

Los casos de firma de funciones, RED/GREEN/REFACTOR, concurrencia de dos gestores, atomicidad SQLite, estructura interna del correo y ausencia de rutas duplicadas son evidencia técnica. Se presentan con las bitácoras, commits y salida de pytest. Simularlos con botones dentro del formulario no demostraría que el backend ejecutó esas pruebas.

Los documentos individuales describen el estado de cada rama en su fecha. Por ejemplo, el Grupo 5 documentó inicialmente persistencia en memoria y el Grupo 4 un QR corto; la integración final utiliza SQLite y un comprobante legible completo. Para el comportamiento vigente prevalecen `INTEGRACION_GRUPOS.md`, `CIERRE_BACKEND.md`, el código integrado y los tests actuales.

## Contrato del calendario

`GET /actividades/{actividad}/calendario` devuelve `anticipacion_minima_minutos`, `anticipacion_maxima_horas` y los días que el backend permite consultar. Cada día trae `estado`, `motivo` y `horarios` con su `horario_id`, cupos y disponibilidad. El frontend genera únicamente las celdas visuales del mes; no decide qué fecha está cerrada ni convierte la hora en un identificador. `GET /actividades` incluye `talles_disponibles` derivados de `TalleVestimenta`. La validación de participantes y del correo corresponde al backend.
