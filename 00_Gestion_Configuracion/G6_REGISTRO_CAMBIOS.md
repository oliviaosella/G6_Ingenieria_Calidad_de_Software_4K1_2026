# Registro de Cambios — G6

Registra únicamente los cambios sobre ítems que **ya forman parte de una Línea Base publicada**. Un commit de trabajo normal, un borrador o una prueba no aprobada no generan una fila acá — solo la generan las modificaciones que la sección 5.6 del informe obliga a tramitar como control de cambios.

Si el cambio no toca ningún ítem incluido en una Línea Base, no es control de cambios: es trabajo normal, se resuelve con un commit y listo.

## Registro

| ID | Fecha de solicitud | Ítem(s) afectado(s) | Línea Base de origen | Motivo | Impacto evaluado | Rama | Estado | Nueva Línea Base |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CC-LB-001 | 2026-11-02 | `LB_TP01_final`, `LB_TP02_final`, `LB_TP03_final` | Etiquetas creadas el 2026-11-02 con fecha técnica actual | Corregir la fecha de los objetos de etiqueta para que coincida con la fecha real de cada entrega | No cambia los commits ni el contenido congelado; solo corrige la fecha técnica y elimina `LB_TP06_final`, que no correspondía a una entrega | `main` | Aprobado e integrado | Mismas tres etiquetas, recreadas una única vez antes de su formalización definitiva |
| CC-LB-002 | 2026-11-02 | Contenido de `LB_TP03_final` | `LB_TP03_final` | Integrar en `main` la rama histórica `tdd/integracion-final` | Incorpora el código fuente y pruebas del TPE03; elimina bytecode Python versionado y agrega exclusiones para artefactos generados sin modificar el commit congelado | `tdd/integracion-final` → `main` | Aprobado e integrado mediante `500ad58` | No corresponde: la etiqueta original permanece inmutable |
| CC-LB-003 | 2026-11-02 | Notas, resúmenes, ejercicios y TPN posteriores a las Líneas Base | `LB_TP01_final` a `LB_TP03_final` como referencias históricas | Normalizar nombres, convertir entregables DOCX a PDF y retirar una copia binaria duplicada | No modifica las etiquetas ni sus commits; corrige el estado actual de `main` y mantiene el historial mediante renombres detectables por Git | `main` (mantenimiento documental) | Integrado; revisión grupal pendiente | No corresponde hasta un nuevo hito aprobado |
| CC-LB-004 | 2026-11-02 | Documentación final TDD del TPE03 | `LB_TP03_final` | Recuperar el único entregable final válido de `tdd/frontend` antes de eliminar las ramas remotas | Se incorpora un PDF revisado de 15 páginas sin integrar dependencias, ejecutables ni archivos temporales de la rama | `tdd/frontend` → `main` mediante `12725c2` | Integrado; revisión grupal pendiente | No corresponde hasta una revisión aprobada del TPE03 |
| CC-LB-005 | 2026-11-02 | `backend/requirements.txt`, `frontend/src/inscripcion/InscripcionForm.tsx` y `frontend/src/inscripcion/horario/HorarioSection.tsx` del TPE03 | `LB_TP03_final` | Completar la dependencia necesaria para ejecutar las 188 pruebas desde una instalación limpia y eliminar dos advertencias del linter de React | Afecta la instalación del backend y la programación asíncrona de dos efectos del frontend; se verificaron 188 pruebas, lint, build y CI | `main` mediante `cfa32ef` (excepción ya integrada) | Integrado; revisión grupal pendiente | Candidato a `LB_TP03_rev01` |

## Cómo completar una fila

1. **ID:** correlativo `CC-NNN`, no reutilizar.
2. **Ítem(s) afectado(s):** nombre exacto del archivo, según el inventario operativo y las reglas de nombrado del README.
3. **Línea Base de origen:** la etiqueta bajo la cual ese ítem estaba congelado hasta ahora.
4. **Motivo:** por qué se pide el cambio (una frase, no un párrafo).
5. **Impacto evaluado:** qué otros documentos, código o entregables se ven afectados — si la respuesta es "ninguno", decirlo explícitamente, no dejar vacío.
6. **Rama:** usar una rama separada para código o cambios funcionales. El mantenimiento documental puede registrarse como directo en `main` cuando se valida antes del `push`.
7. **Estado:** `Solicitado` → `En revisión` → `Aprobado e integrado` (o `Rechazado`). Si el cambio fue integrado sin una segunda revisión, declararlo como `Integrado; revisión grupal pendiente` y no presentarlo como aprobado.
8. **Nueva Línea Base:** completar solo si el cambio altera el contenido de referencia y por eso genera una etiqueta de revisión `LB_TP<NUMERO>_rev<REVISION>`. Una corrección puramente técnica de una etiqueta todavía no formalizada debe quedar documentada como excepción y no repetirse.

## Convención de commit asociada

Usar `FIX(<ÁREA>)` para la corrección puntual y, si corresponde etiquetar la nueva Línea Base en el mismo movimiento, un commit separado `BASE(GC)` para el registro. No mezclar ambos en un solo commit.

---
*Ver también: `G6_REGISTRO_LINEAS_BASE.md` (índice de Líneas Base) y `G6_CRITERIOS_LINEAS_BASE.md` (condiciones para nueva versión).*
