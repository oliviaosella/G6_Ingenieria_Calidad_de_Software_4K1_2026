# Registro de Cambios — G6

Registra únicamente los cambios sobre ítems que **ya forman parte de una Línea Base publicada**. Un commit de trabajo normal, un borrador o una prueba no aprobada no generan una fila acá — solo la generan las modificaciones que la sección 5.6 del informe obliga a tramitar como control de cambios.

Si el cambio no toca ningún ítem incluido en una Línea Base, no es control de cambios: es trabajo normal, se resuelve con un commit y listo.

## Registro

| ID | Fecha de solicitud | Ítem(s) afectado(s) | Línea Base de origen | Motivo | Impacto evaluado | Rama | Estado | Nueva Línea Base |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CC-001 | 2026-09-02 | `G6_CL02_U3.pdf` | `LB_INICIAL_V1.0` | La cátedra republicó el PDF con una corrección | Solo afecta este archivo; no impacta otros ICs | `fix/catedra-cl02` | Aprobado e integrado | `LB_INICIAL_V1.1` |

> Fila de ejemplo para mostrar el formato. Borrarla al cargar el primer cambio real.

## Cómo completar una fila

1. **ID:** correlativo `CC-NNN`, no reutilizar.
2. **Ítem(s) afectado(s):** nombre exacto del archivo, según `G6_INVENTARIO_IC.md`.
3. **Línea Base de origen:** la etiqueta bajo la cual ese ítem estaba congelado hasta ahora.
4. **Motivo:** por qué se pide el cambio (una frase, no un párrafo).
5. **Impacto evaluado:** qué otros documentos, código o entregables se ven afectados — si la respuesta es "ninguno", decirlo explícitamente, no dejar vacío.
6. **Rama:** el cambio se implementa en una rama separada, nunca directo en `main` (regla del README y de la skill del repo).
7. **Estado:** `Solicitado` → `En revisión` → `Aprobado e integrado` (o `Rechazado`). Solo pasa a integrado cuando el responsable del ítem *y* al menos otro integrante lo revisaron.
8. **Nueva Línea Base:** completar solo si el cambio altera el contenido de referencia y por eso genera una nueva etiqueta (versión menor si no cambia el alcance, mayor si lo cambia — ver `G6_CRITERIOS_LINEAS_BASE.md` sección de identificación).

## Convención de commit asociada

Usar `FIX(<ÁREA>)` para la corrección puntual y, si corresponde etiquetar la nueva Línea Base en el mismo movimiento, un commit separado `BASE(GC)` para el registro. No mezclar ambos en un solo commit.

---
*Ver también: `G6_REGISTRO_LINEAS_BASE.md` (índice de Líneas Base) y `G6_CRITERIOS_LINEAS_BASE.md` (condiciones para nueva versión).*