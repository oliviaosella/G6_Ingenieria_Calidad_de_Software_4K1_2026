# Inventario de Ítems de Configuración — G6

**Estado del inventario:** 2026-11-02  
**Fuente de verificación:** archivos versionados por Git en `main` (`git ls-files`).  
**Criterio:** cada fila identifica un ítem individual o una familia homogénea administrada con la misma regla de ubicación, nombre y validación.

| ID | Ítem o familia | Ubicación | Responsable | Estado actual | Línea Base relacionada | Verificación |
| --- | --- | --- | --- | --- | --- | --- |
| IC-GC-001 | Reglas generales del repositorio | `README.md` | Grupo 6 | Vigente | `LB_INICIAL` | Revisión documental + CI |
| IC-GC-002 | Criterios de Líneas Base | `00_Gestion_Configuracion/G6_CRITERIOS_LINEAS_BASE.md` | Grupo 6 | Vigente | `LB_INICIAL` | Revisión documental |
| IC-GC-003 | Registro de cambios | `00_Gestion_Configuracion/G6_REGISTRO_CAMBIOS.md` | Grupo 6 | Vigente | No aplica | Revisión documental |
| IC-GC-004 | Registro y fichas de Líneas Base | `00_Gestion_Configuracion/Lineas_Base/Registros/` | Grupo 6 | Vigente | `LB_TP01_final` a `LB_TP03_final` | Etiquetas anotadas + commits registrados |
| IC-CL-001 | Actividades de clase | `01_Clase/Actividades/G6_ACT*.pdf` | Autor de cada actividad | En evolución | Próxima Línea Base | Nombre, formato y duplicados |
| IC-CL-002 | Notas de clase individuales y acumulativas | `01_Clase/Notas/G6_NC_*.pdf` | Autor indicado en el nombre | En evolución | Próxima Línea Base | Nombre, PDF y duplicados |
| IC-CA-001 | Consignas y guías oficiales | `02_Catedra/Consignas/G6_CO_*.pdf` | Cátedra / custodio Grupo 6 | Referencia | Próxima Línea Base | Ubicación, formato y duplicados |
| IC-CA-002 | Bibliografía oficial | `02_Catedra/Libros/G6_LI_*.pdf` | Cátedra / custodio Grupo 6 | Referencia | Próxima Línea Base | Ubicación y formato |
| IC-CA-003 | Material de clase oficial | `02_Catedra/Material/` | Cátedra / custodio Grupo 6 | Referencia | Próxima Línea Base | Ubicación y formato |
| IC-CA-004 | Planificación y cronograma | `02_Catedra/Planificacion/` y `02_Catedra/Cronograma/` | Cátedra / custodio Grupo 6 | Referencia | Próxima Línea Base | Ubicación y formato |
| IC-CA-005 | Templates editables | `02_Catedra/Templates/G6_TE_*` | Cátedra / custodio Grupo 6 | Referencia | Próxima Línea Base | Nombre y formato editable |
| IC-PP-001 | Ejercicios propios | `03_Produccion_Propia/Ejercicios/G6_EJ_*.pdf` | Autor indicado en el nombre | En evolución | Próxima Línea Base | Nombre, PDF y duplicados |
| IC-PP-002 | Resúmenes del primer parcial | `03_Produccion_Propia/Resumenes/G6_RE_P1_*.pdf` | Autor indicado en el nombre | En evolución | Próxima Línea Base | Nombre, PDF y duplicados |
| IC-PP-003 | Resúmenes del segundo parcial | `03_Produccion_Propia/Resumenes/G6_RE_P2_*.pdf` | Autor indicado en el nombre | En evolución | Próxima Línea Base | Nombre, PDF y duplicados |
| IC-TP-001 | Entregable TPE01 | `04_Trabajos_Practicos/Evaluables/TPE01/G6_TPE01.pdf` | Grupo 6 | Congelado | `LB_TP01_final` | Commit y etiqueta anotada |
| IC-TP-002 | Entregable TPE02 | `04_Trabajos_Practicos/Evaluables/TPE02/G6_TPE02.pdf` | Grupo 6 | Congelado | `LB_TP02_final` | Commit y etiqueta anotada |
| IC-TP-003 | Implementación TPE03 | `04_Trabajos_Practicos/Evaluables/TPE03/G6_COD_InscripcionActividad/` | Grupo 6 | Candidato a revisión | `LB_TP03_final`; cambios `CC-LB-002` y `CC-LB-005` candidatos a `LB_TP03_rev01` | 188 pruebas backend + build/lint frontend + CI |
| IC-TP-004 | Documentación final TDD de TPE03 | `04_Trabajos_Practicos/Evaluables/TPE03/G6_TPE03_Documentacion_TDD.pdf` | Grupo 6 | Candidato a revisión | `CC-LB-004`, candidato a `LB_TP03_rev01` | PDF de 15 páginas revisado |
| IC-GC-005 | Ficha candidata de revisión TPE03 | `00_Gestion_Configuracion/Lineas_Base/Registros/LB_TP03_rev01_CANDIDATA.md` | Grupo 6 | Pendiente de aprobación independiente | Candidata a `LB_TP03_rev01` | Checklist y evidencia de revisión |
| IC-TP-005 | Trabajos prácticos no evaluables | `04_Trabajos_Practicos/No_Evaluables/G6_TPN*.pdf` | Autor indicado en el nombre | En evolución | Próxima Línea Base | Nombre, PDF y duplicados |

## Mantenimiento

- El inventario se actualiza cuando se agrega, mueve, renombra o retira un ítem o una familia.
- Las versiones históricas se recuperan por commit o etiqueta; no se duplican archivos para representar versiones.
- El estado `Congelado` describe el contenido apuntado por la etiqueta. Los cambios posteriores permanecen visibles en `main` y deben registrarse en `G6_REGISTRO_CAMBIOS.md` cuando afecten ese contenido.
