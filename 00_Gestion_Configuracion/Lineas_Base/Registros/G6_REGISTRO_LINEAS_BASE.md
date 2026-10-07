# Registro de Líneas Base — G6

Índice general de todas las Líneas Base establecidas en el repositorio del Grupo 6. Cada fila corresponde a una etiqueta ya creada y publicada; no se listan aquí borradores ni conjuntos candidatos que todavía no fueron aprobados (ver `G6_CRITERIOS_LINEAS_BASE.md` para las condiciones de aceptación).

El detalle individual de cada Línea Base — alcance completo, hallazgos de auditoría, checklist firmado — se guarda como un archivo aparte dentro de `00_Gestion_Configuracion/Lineas_Base/Registros/`, con el mismo nombre que la etiqueta (por ejemplo `Registros/LB_INICIAL_V1.0.md`). Esta tabla es el índice; ese archivo es la ficha.

## Índice de Líneas Base

| Etiqueta | Fecha | Commit (hash corto) | Alcance | Propone | Aprueban (CCC) | Detalle |
| --- | --- | --- | --- | --- | --- | --- |
| `LB_INICIAL_V1.0` | *(pendiente)* | *(pendiente)* | Estructura de carpetas aprobada, README, reglas de nombrado e inventario inicial | *(a completar)* | *(a completar)* | `Registros/LB_INICIAL_V1.0.md` |

> Fila de ejemplo. Reemplazar por los datos reales al momento de crear cada etiqueta; no dejar filas de Líneas Base ya publicadas sin sus datos completos, porque eso rompe la condición de trazabilidad exigida antes de integrar la siguiente.

## Cómo completar una fila

1. **Etiqueta:** el identificador exacto creado con `git tag -a`, formato `LB_<HITO>_V<MAYOR>.<MENOR>`.
2. **Fecha:** fecha en que se creó la etiqueta (no la fecha en que se propuso el hito).
3. **Commit:** los primeros 7-8 caracteres del hash sobre el que se ancló la etiqueta (`git rev-parse --short <tag>`).
4. **Alcance:** qué ítems y carpetas quedan cubiertos por esta Línea Base, en una frase. Debe coincidir con lo que efectivamente audita el checklist de la ficha en `Registros/`.
5. **Propone:** integrante responsable del conjunto (rol "Responsable del ítem" en la sección 8 del informe).
6. **Aprueban:** integrante(s) que revisaron según el procedimiento de aprobación — para `LB_FINAL_V1.0` deben figurar los 15 integrantes.
7. **Detalle:** enlace relativo al archivo de ficha individual dentro de `Registros/`.

## Comandos de referencia

```bash
git tag -a LB_INICIAL_V1.0 -m "Linea Base inicial: estructura, normativa e items de catedra disponibles"
git push origin LB_INICIAL_V1.0
git rev-parse --short LB_INICIAL_V1.0
```

---
*Ver también: `G6_CRITERIOS_LINEAS_BASE.md` (cuándo se establece una Línea Base) y `G6_REGISTRO_CAMBIOS.md` (modificaciones posteriores a una Línea Base ya publicada).*