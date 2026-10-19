# Eco Harmony Park · Frontend del TP

Frontend React + TypeScript listo para la presentación local de la inscripción a actividades. La identidad visual usa una **e** con vetas y una hoja, inspirada en la referencia del parque.

## Ejecutar

```bash
cd 04_Trabajos_Practicos/Evaluables/TPE03/G6_COD_InscripcionActividad/frontend
npm ci
npm run dev
```

Abrir la URL que muestra Vite (normalmente `http://localhost:5173`). Para verificar antes de presentar: `npm run build` y `npm run lint`.

## Qué funciona hoy

- Elegir Tirolesa, Safari, Palestra o Jardinería y un turno.
- Mostrar cupos, cerrar lunes/feriados definidos en la rama y limitar turnos a las próximas 24 horas con 15 minutos de anticipación.
- Agregar o quitar participantes; validar nombre, DNI único y edad. El talle es obligatorio para Tirolesa/Palestra y queda deshabilitado para las demás actividades.
- Registrar aceptación para la actividad elegida, correo y reserva de demostración.
- Descontar cupos de las reservas guardadas en `localStorage` del navegador y generar un comprobante con QR descargable.
- Cambiar paisaje y paleta al seleccionar actividad. Las escenas SVG incluyen dinosaurios, aves, mariposas o cabra con movimiento sutil. Guía cambia de color y acción con cada actividad y aparece animado en la portada y la confirmación; no forma parte del grupo de participantes.

## Mascota Guía

`src/assets/guia-frames/` contiene 20 ilustraciones transparentes: cuatro momentos para cada una de las cinco paletas (parque, safari, tirolesa, palestra y jardinería). `src/assets/guia-gifs/` contiene cinco GIF animados, uno por paleta, generados desde esas imágenes con `python scripts/build-guia-gifs.py` (requiere Pillow). El componente `src/inscripcion/mascota/GuiaMascot.tsx` muestra el GIF correspondiente a la actividad; si el sistema solicita reducir el movimiento, muestra el primer fotograma fijo.

En la confirmación se usa `src/assets/guia-confirmacion/confirmada.gif`, donde Guía sostiene el cartel «INSCRIPCION CONFIRMADA!». El GIF se puede regenerar con `python scripts/build-confirmation-gif.py` desde `confirmada.png`. La identidad visual usa Fredoka y Nunito locales, escenas SVG propias de cada actividad y el sello `e` en la portada, la reserva y el comprobante.

El asistente del formulario usa cuatro ilustraciones y GIF propios en `src/assets/guia-assistant/`: saludo, indicación, reflexión y celebración. `GuiaAssistant.tsx` cambia el gesto y el consejo según el paso y los datos cargados, permite ir al campo correspondiente y se puede cerrar o volver a abrir. Los GIF se regeneran con `python scripts/build-guia-assistant-gifs.py`; con movimiento reducido se muestran los PNG fijos.

La reserva es **una simulación local**, persistida solo en este navegador. No se envían correos ni se genera una reserva en el backend. Si el reloj real no deja ningún turno dentro de 24 horas, el modo presentación muestra turnos simulados del próximo día abierto y lo indica en pantalla. Los términos actuales son texto de muestra pendiente de aprobación del PO. El QR identifica una reserva de demostración; no es una entrada validable por el parque.

## Organización para los grupos

`src/inscripcion/InscripcionForm.tsx` compone las secciones y maneja el avance. `types.ts` y `schemas.ts` reúnen los tipos y validaciones compartidas. Cada grupo puede refinar su carpeta:

| Grupo | Carpeta | Integración pendiente |
| --- | --- | --- |
| 1 · Consulta | `actividad/`, `horario/` | Exponer y consumir actividades, horarios y cupos reales. |
| 2 · Términos | `terminos/` | Obtener términos aprobados y validar aceptación por actividad. |
| 3 · Participantes | `participantes/` | Alinear validaciones y contrato con el backend. |
| 4 · Correo y QR | `confirmacion/` | Mostrar el QR definitivo y estado del envío real. |
| 5 · Reservas/cupos | `reservas/` | Sustituir `reservasDemo.ts` por una llamada que reserve cupos de forma consistente. |

`demoStore.ts` es exclusivo de la simulación local y se retirará cuando exista persistencia real. La fuente de disponibilidad local está en `horario/disponibilidadDemo.ts`. El `InscripcionForm` debería llamar a una capa API con el mismo tipo de resultado `Reserva`, en lugar de importar el módulo demo directamente. Así se conserva la separación entre grupos.

## Referencias tomadas de las ramas `tdd/`

- `tdd/consultar-actividad`: cuatro actividades, capacidades, 9:00–17:00, cierre los lunes y 25/12 y 1/1, ventana de 15 minutos a 24 horas.
- `tdd/cargar-participante`: datos del visitante, DNI sin repetir, edades mínimas (Tirolesa 8, Palestra 12) y talle obligatorio para esas dos actividades.
- `tdd/terminos-confirmacion`: aceptación específica para la actividad; el propio backend marca los términos como ficticios.
- `tdd/registrar-inscripcion`: lógica de cupos y rechazo cuando no alcanzan.
- `tdd/envio-confirmacion-inscripcion`: confirmación por correo, todavía sin endpoint de integración del flujo.

El PDF de división asigna Grupo 2 a términos y Grupo 3 a participantes en su primera página; la tabla de la segunda página invierte esos números. Esta estructura sigue la primera asignación y los nombres funcionales de las ramas. En las ramas consultadas aún no hay endpoints de inscripción ni disponibilidad listos para consumir: solo `/health` está expuesto. Por eso el frontend funciona de forma autónoma hasta acordar el contrato HTTP y unificar el backend.
