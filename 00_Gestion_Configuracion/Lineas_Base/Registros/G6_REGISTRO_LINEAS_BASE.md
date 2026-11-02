# Registro de Líneas Base — G6

Índice general de todas las Líneas Base establecidas en el repositorio del Grupo 6. Cada fila corresponde a una etiqueta ya creada y publicada; no se listan aquí borradores ni conjuntos candidatos que todavía no fueron aprobados (ver `G6_CRITERIOS_LINEAS_BASE.md` para las condiciones de aceptación).

El detalle individual de cada Línea Base — alcance completo, hallazgos de auditoría, checklist firmado — se guarda como un archivo aparte dentro de `00_Gestion_Configuracion/Lineas_Base/Registros/`, con el mismo nombre que la etiqueta (por ejemplo `Registros/LB_INICIAL_V1.0.md`). Esta tabla es el índice; ese archivo es la ficha.

## Índice de Líneas Base

| Etiqueta | Fecha efectiva de entrega | Commit | Rama de referencia | Alcance | Aprobación formal | Estado de reconstrucción | Detalle |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `LB_INICIAL` | 2026-08-25 00:20:39 -03:00 | `61be1f2` | `main` | Estructura inicial del repositorio | No consta en el registro actual | Etiqueta anotada preexistente; nombre legado | Etiqueta Git |
| `LB_TP01_final` | 2026-08-25 00:32:48 -03:00 | `204d5fd` | `main` | Informe `G6_TPE01.pdf` | Responsable y revisor pendientes de documentar | Reconstruida el 2026-11-02 | [`LB_TP01_final.md`](LB_TP01_final.md) |
| `LB_TP02_final` | 2026-09-25 12:18:39 -03:00 | `5e18cdd` | `main` | Informe `G6_TPE02.pdf` | Responsable y revisor pendientes de documentar | Reconstruida el 2026-11-02 | [`LB_TP02_final.md`](LB_TP02_final.md) |
| `LB_TP03_final` | 2026-10-29 11:31:58 -03:00 | `95787c9` | `tdd/integracion-final` | Código integrado del TPE03 | Responsable y revisor pendientes de documentar | Reconstruida el 2026-11-02 con observación de rama | [`LB_TP03_final.md`](LB_TP03_final.md) |

La etiqueta liviana preexistente `LB_TP06_final` no se considera una Línea Base válida: no es anotada, apunta a un commit de resúmenes y no cuenta con una ficha de alcance. Se conserva sin mover ni reutilizar para mantener la trazabilidad histórica.

## Cómo completar una fila

1. **Etiqueta:** el identificador exacto creado con `git tag -a`, formato `LB_TP<NUMERO>_final`.
2. **Fecha efectiva de entrega:** fecha del commit que cerró o incorporó la entrega. La fecha técnica de creación de la etiqueta permanece en el objeto Git.
3. **Commit:** los primeros 7-8 caracteres del hash sobre el que se ancló la etiqueta (`git rev-parse --short <tag>`).
4. **Alcance:** qué ítems y carpetas quedan cubiertos por esta Línea Base, en una frase. Debe coincidir con lo que efectivamente audita el checklist de la ficha en `Registros/`.
5. **Aprobación formal:** nombres del responsable y de, al menos, otro integrante que realizó la revisión. No se infieren aprobaciones a partir de autores de commits.
6. **Estado de reconstrucción:** indica cuándo se reconstruyó la referencia y si existe alguna excepción de rama o alcance.
7. **Detalle:** enlace relativo al archivo de ficha individual dentro de `Registros/`.

## Comandos de referencia

```bash
git tag -a LB_TP01_final <COMMIT_DE_ENTREGA> -m "Linea Base del Trabajo Practico 01"
git push origin LB_TP01_final
git rev-parse --short LB_TP01_final
```

---
*Ver también: `G6_CRITERIOS_LINEAS_BASE.md` (cuándo se establece una Línea Base) y `G6_REGISTRO_CAMBIOS.md` (modificaciones posteriores a una Línea Base ya publicada).*
