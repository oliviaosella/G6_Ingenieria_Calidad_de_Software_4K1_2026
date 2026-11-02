# Registro de Cambios — G6

Registra únicamente los cambios sobre ítems que **ya forman parte de una Línea Base publicada**. Un commit de trabajo normal, un borrador o una prueba no aprobada no generan una fila acá — solo la generan las modificaciones que la sección 5.6 del informe obliga a tramitar como control de cambios.

Si el cambio no toca ningún ítem incluido en una Línea Base, no es control de cambios: es trabajo normal, se resuelve con un commit y listo.

## Registro

| ID | Fecha de solicitud | Ítem(s) afectado(s) | Línea Base de origen | Motivo | Impacto evaluado | Rama | Estado | Nueva Línea Base |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CC-LB-001 | 2026-11-02 | `LB_TP01_final`, `LB_TP02_final`, `LB_TP03_final` | Etiquetas creadas el 2026-11-02 con fecha técnica actual | Corregir la fecha de los objetos de etiqueta para que coincida con la fecha real de cada entrega | No cambia los commits ni el contenido congelado; solo corrige la fecha técnica y elimina `LB_TP06_final`, que no correspondía a una entrega | `main` | Aprobado e integrado | Mismas tres etiquetas, recreadas una única vez antes de su formalización definitiva |

## Cómo completar una fila

1. **ID:** correlativo `CC-NNN`, no reutilizar.
2. **Ítem(s) afectado(s):** nombre exacto del archivo, según el inventario operativo y las reglas de nombrado del README.
3. **Línea Base de origen:** la etiqueta bajo la cual ese ítem estaba congelado hasta ahora.
4. **Motivo:** por qué se pide el cambio (una frase, no un párrafo).
5. **Impacto evaluado:** qué otros documentos, código o entregables se ven afectados — si la respuesta es "ninguno", decirlo explícitamente, no dejar vacío.
6. **Rama:** el cambio se implementa en una rama separada, nunca directo en `main` (regla del README y de la skill del repo).
7. **Estado:** `Solicitado` → `En revisión` → `Aprobado e integrado` (o `Rechazado`). Solo pasa a integrado cuando el responsable del ítem *y* al menos otro integrante lo revisaron.
8. **Nueva Línea Base:** completar solo si el cambio altera el contenido de referencia y por eso genera una etiqueta de revisión `LB_TP<NUMERO>_rev<REVISION>`. Una corrección puramente técnica de una etiqueta todavía no formalizada debe quedar documentada como excepción y no repetirse.

## Convención de commit asociada

Usar `FIX(<ÁREA>)` para la corrección puntual y, si corresponde etiquetar la nueva Línea Base en el mismo movimiento, un commit separado `BASE(GC)` para el registro. No mezclar ambos en un solo commit.

---
*Ver también: `G6_REGISTRO_LINEAS_BASE.md` (índice de Líneas Base) y `G6_CRITERIOS_LINEAS_BASE.md` (condiciones para nueva versión).*
