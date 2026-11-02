# Registro de Líneas Base — G6

Índice general de todas las Líneas Base establecidas en el repositorio del Grupo 6. Cada fila corresponde a una etiqueta ya creada y publicada; no se listan aquí borradores ni conjuntos candidatos que todavía no fueron aprobados (ver `G6_CRITERIOS_LINEAS_BASE.md` para las condiciones de aceptación).

El detalle individual de cada Línea Base — alcance, fecha, rama y hallazgos de auditoría — se guarda como un archivo aparte dentro de `00_Gestion_Configuracion/Lineas_Base/Registros/`, con el mismo nombre que la etiqueta. Esta tabla es el índice; ese archivo es la ficha.

## Índice de Líneas Base

| Etiqueta | Fecha de la etiqueta y de la entrega | Commit | Rama de referencia | Alcance | Validación | Fecha real de reconstrucción | Detalle |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `LB_INICIAL` | 2026-08-25 00:24:38 -03:00 | `61be1f2` | `main` | Estructura inicial del repositorio | Etiqueta anotada histórica | Preexistente | Etiqueta Git |
| `LB_TP01_final` | 2026-08-25 00:32:48 -03:00 | `204d5fd` | `main` | Informe `G6_TPE01.pdf` | Commit y fecha auditados | 2026-11-02 | [`LB_TP01_final.md`](LB_TP01_final.md) |
| `LB_TP02_final` | 2026-09-25 12:18:39 -03:00 | `5e18cdd` | `main` | Informe `G6_TPE02.pdf` | Commit y fecha auditados | 2026-11-02 | [`LB_TP02_final.md`](LB_TP02_final.md) |
| `LB_TP03_final` | 2026-10-29 11:31:58 -03:00 | `95787c9` | `main` (origen: `tdd/integracion-final`) | Código integrado del TPE03 | Commit, fecha, rama original e integración auditados | 2026-11-02 | [`LB_TP03_final.md`](LB_TP03_final.md) |

La etiqueta incorrecta `LB_TP06_final` fue eliminada durante la normalización del 2026-11-02 porque era liviana, apuntaba a un commit de resúmenes y no representaba una entrega TPE06.

## Cómo completar una fila

1. **Etiqueta:** el identificador exacto creado con `git tag -a`, formato `LB_TP<NUMERO>_final`.
2. **Fecha de la etiqueta y de la entrega:** fecha del commit que cerró o incorporó la entrega. En reconstrucciones históricas, el objeto de etiqueta usa esa misma fecha y la ficha conserva por separado la fecha real de reconstrucción.
3. **Commit:** los primeros 7-8 caracteres del hash sobre el que se ancló la etiqueta (`git rev-parse --short <tag>`).
4. **Alcance:** qué ítems y carpetas quedan cubiertos por esta Línea Base, en una frase. Debe coincidir con lo que efectivamente audita el checklist de la ficha en `Registros/`.
5. **Validación:** evidencia objetiva utilizada para verificar el commit, la fecha y el alcance. En reconstrucciones históricas no se inventan aprobadores retroactivos.
6. **Fecha real de reconstrucción:** fecha en que se realizó la operación técnica, aunque el objeto de etiqueta represente la fecha histórica de entrega.
7. **Detalle:** enlace relativo al archivo de ficha individual dentro de `Registros/`.

## Comandos de referencia

```bash
git tag -a LB_TP01_final <COMMIT_DE_ENTREGA> -m "Linea Base del Trabajo Practico 01"
git push origin LB_TP01_final
git rev-parse --short LB_TP01_final
```

---
*Ver también: [`../../G6_CRITERIOS_LINEAS_BASE.md`](../../G6_CRITERIOS_LINEAS_BASE.md) y [`../../G6_REGISTRO_CAMBIOS.md`](../../G6_REGISTRO_CAMBIOS.md).*
