# Repositorio de Gestión de Configuración - G6

Este repositorio centraliza los Ítems de Configuración de la materia y establece una forma única de identificarlos, ubicarlos, revisarlos y conservarlos. La estructura y las reglas de nombrado se basan en el documento "Lineamientos de Items de Configuración.pdf" y en los criterios definidos por el Grupo 6 para la Gestión de Configuración del repositorio.

## Objetivos del repositorio

- Mantener separados los materiales de clase, de cátedra, de producción propia y de trabajos prácticos.

- Facilitar la búsqueda y trazabilidad de cada Ítem de Configuración.

- Evitar duplicados, ubicaciones incorrectas y nombres ambiguos.

- Conservar versiones estables mediante Líneas Base.

- Registrar de forma controlada los cambios posteriores a una Línea Base.

## Estructura

~~~text
G6_Ingenieria_Calidad_de_Software_4K1_2026/
├── README.md
├── .gitignore
│
├── 00_Gestion_Configuracion/
│
├── 01_Clase/
│   ├── Actividades/
│   └── Notas/
│
├── 02_Catedra/
│   ├── Clases_Grabadas/
│   ├── Libros/
│   ├── Planificacion/
│   ├── Templates/
│   └── Material/
│
├── 03_Produccion_Propia/
│   ├── Codigo/
│   ├── Ejercicios/
│   ├── Minutas/
│   └── Resumenes/
│
└── 04_Trabajos_Practicos/
    ├── Evaluables/
    ├── Investigacion/
    └── No_Evaluables/
~~~

La carpeta `00_Gestion_Configuracion` se incorpora para guardar la documentación utilizada para administrar los Ítems de Configuración y sus cambios. No modifica la clasificación académica definida para el resto del repositorio.

## Criterio de ubicación

| Directorio | Contenido |
| --- | --- |
| `01_Clase` | Material generado como resultado de las clases teóricas o prácticas, como notas personales y actividades realizadas durante la clase. |
| `02_Catedra` | Material limpio y oficial proporcionado por los docentes o publicado en la UV, como bibliografía, presentaciones, templates, planificación y clases grabadas. |
| `03_Produccion_Propia` | Material elaborado por los integrantes del grupo fuera de clase, como resúmenes, ejercicios, minutas, código fuente, apuntes y planillas de cálculo. |
| `04_Trabajos_Practicos` | Trabajos Prácticos evaluables, no evaluables, trabajos de investigación, consignas y presentaciones asociadas. |
| `00_Gestion_Configuracion` | Documentación utilizada para administrar los Ítems de Configuración, definir Líneas Base y controlar los cambios. |

Cada Ítem de Configuración debe almacenarse únicamente en la ubicación correspondiente a su categoría y tipo.

Ningún archivo debe existir en más de una ubicación. Si un mismo contenido se necesita en diferentes contextos, debe referenciarse mediante un enlace en lugar de duplicarse.

## Reglas generales de nombrado

1. Se utiliza el prefijo `G6_` para identificar los archivos correspondientes al Grupo 6.

2. El código de autor se forma con la inicial del primer nombre y la inicial del primer apellido.

3. Las fechas se representan mediante el formato `mm-dd`.

4. El contenido descriptivo se escribe en PascalCase y sin espacios.

5. Las abreviaturas permiten identificar el tipo de Ítem de Configuración.

6. Las unidades se identifican mediante un número del 1 al 4.

7. Cada archivo debe respetar la regla de nombrado y la ubicación definida para su tipo de Ítem de Configuración.

8. No se reemplaza directamente un archivo perteneciente a una Línea Base sin aplicar el procedimiento de control de cambios correspondiente.

## Convenciones por tipo de ítem

| Ítem | Regla de nombrado | Ubicación |
| --- | --- | --- |
| Inventario de Ítems de Configuración | `G6_INVENTARIO_IC.md` | `00_Gestion_Configuracion/` |
| Criterios de Líneas Base | `G6_CRITERIOS_LINEAS_BASE.md` | `00_Gestion_Configuracion/` |
| Actividad de clase | `G6_ACT<NUMERO>_<mm-dd>.jpg/pdf` | `01_Clase/Actividades/` |
| Nota de Clase | `G6_NC_<AUTOR>_<FECHA>.pdf` | `01_Clase/Notas/` |
| Libro | `G6_LI_U<NRO_UNIDAD>_<LIBRO>.pdf` | `02_Catedra/Libros/` |
| Registro de clases grabadas | `G6_CG.xlsx` | `02_Catedra/Clases_Grabadas/` |
| Programa / Planificación | `G6_PL_<CONTENIDO>.pdf` | `02_Catedra/Planificacion/` |
| Presentación de clase | `G6_PPT_<NRO>_<CONTENIDO>.pdf` | `02_Catedra/Material/` |
| Template | `G6_TE_<TEMA>.pdf` | `02_Catedra/Templates/` |
| Código fuente / ejecutable | `G6_COD_<NOMBRE_COMPONENTE>.<EXTENSION>` | `03_Produccion_Propia/Codigo/` |
| Ejercicio | `G6_EJ_<AUTOR>_<EJERCICIO>.pdf` | `03_Produccion_Propia/Ejercicios/` |
| Minuta | `G6_MI_<TEMA>_<FECHA>.md` | `03_Produccion_Propia/Minutas/` |
| Resumen | `G6_RE_<AUTOR>.pdf` | `03_Produccion_Propia/Resumenes/` |
| Trabajo Práctico Evaluable | `G6_TPE<NUMERO>.pdf` | `04_Trabajos_Practicos/Evaluables/` |
| Consigna TP Evaluable | `G6_CO_TPE<NUMERO>.pdf` | `04_Trabajos_Practicos/Evaluables/` |
| Trabajo de Investigación | `G6_TI<NUMERO>.pdf` | `04_Trabajos_Practicos/Investigacion/` |
| Consigna de Investigación | `G6_CO_TPI<NUMERO>.pdf` | `04_Trabajos_Practicos/Investigacion/` |
| Presentación de Investigación | `G6_PRE_TI<NUMERO>.pptx/.ppsx` | `04_Trabajos_Practicos/Investigacion/` |
| Lineamientos Generales | `G6_TI_LineamientosGenerales.pdf` | `04_Trabajos_Practicos/Investigacion/` |
| Trabajo Práctico No Evaluable | `G6_TPN<NUMERO>_<AUTOR>.pdf` | `04_Trabajos_Practicos/No_Evaluables/` |
| Consigna TP No Evaluable | `G6_CO_TPNE<NUMERO>.pdf` | `04_Trabajos_Practicos/No_Evaluables/` |

Ejemplos:

- `G6_ACT01_08-21.pdf`

- `G6_NC_GE_08-21.pdf`

- `G6_LI_U2_AG.pdf`

- `G6_PL_PlanificacionAsignatura2026.pdf`

- `G6_PPT_02_SCM.pdf`

- `G6_EJ_CP_ALGORITMODEDIJKSTRA.pdf`

- `G6_MI_ReunionTP01_08-21.md`

- `G6_TPE01.pdf`

- `G6_TPN02_PT.pdf`

- `G6_TI01.pdf`

- `G6_COD_Login.java`

## Normas de trabajo con Git

- `main` contiene el material revisado e integrado por el grupo.

- Cada tarea o corrección se desarrolla en una rama creada a partir de `main`.

- Los cambios realizados se registran mediante commits descriptivos.

- La rama de trabajo se publica en el repositorio remoto mediante `push`.

- Todo cambio destinado a incorporarse a `main` se integra mediante un Pull Request.

- El Pull Request debe ser revisado por, al menos, un integrante distinto del autor.

- Una vez aprobado, el cambio se integra mediante `merge`.

- La rama utilizada puede eliminarse una vez que los cambios hayan sido incorporados.

- Los borradores o versiones todavía no aprobadas no se etiquetan como Líneas Base.

- Los cambios posteriores sobre elementos incluidos en una Línea Base deben realizarse mediante el procedimiento de control de cambios correspondiente.

## Líneas Base

Una Línea Base es una versión identificada, revisada y formalmente aprobada de un conjunto de Ítems de Configuración que se adopta como referencia estable.

No equivale a un commit común: se establece solamente cuando existe un hito verificable y el contenido cumple los criterios definidos para su aprobación.

Las Líneas Base definidas son:

| Momento | Etiqueta |
| --- | --- |
| Aprobación de la estructura, README, inventario y reglas de nombrado | `LB_INICIAL` |
| Cierre y aprobación del Trabajo Práctico 01 | `LB_TP01_final` |
| Cierre y aprobación del Trabajo Práctico 02 | `LB_TP02_final` |
| Cierre y aprobación del Trabajo Práctico 03 | `LB_TP03_final` |
| Cierre y aprobación del Trabajo Práctico 04 | `LB_TP04_final` |
| Cierre y aprobación de cada Trabajo Práctico posterior | `LB_TPxx_final` |

Se crea una Línea Base independiente al concluir y aprobar cada Trabajo Práctico.

No se establecen Líneas Base independientes por cada unidad, parcial o componente individual. Estos elementos quedan incorporados dentro de la Línea Base del Trabajo Práctico correspondiente.

El detalle de las condiciones y del procedimiento para establecer una Línea Base se encuentra en:

`00_Gestion_Configuracion/G6_CRITERIOS_LINEAS_BASE.md`

## Procedimiento resumido para establecer una Línea Base

1. Confirmar que el alcance del hito esté definido.

2. Revisar nombres, ubicaciones y contenido de los Ítems de Configuración.

3. Comprobar la coherencia entre consignas, entregables, anexos, presentaciones y código cuando corresponda.

4. Actualizar el inventario de Ítems de Configuración y el registro de cambios.

5. Obtener la aprobación del responsable del ítem y de, al menos, otro integrante.

6. Integrar la versión aprobada en `main`.

7. Crear una etiqueta anotada de Git asociada al commit correspondiente.

Ejemplo:

~~~bash
git tag -a LB_TP01_final -m "Linea Base correspondiente al cierre del Trabajo Practico 01"

git push origin LB_TP01_final
~~~

Una vez publicada una Línea Base, la etiqueta correspondiente no debe eliminarse, reasignarse a otro commit ni reutilizarse.

## Decisiones que deben validarse con la cátedra

- Se utiliza el prefijo `G6_` para identificar los archivos correspondientes al Grupo 6.

- Para las minutas se adopta `.md` como formato por permitir registrar y comparar modificaciones mediante Git.

- Para el registro de clases grabadas se utiliza la extensión `.xlsx`.

- Las consignas se almacenan dentro de `04_Trabajos_Practicos`, junto con el tipo de Trabajo Práctico al que corresponden.

- Si la cátedra requiere modificar alguno de los criterios establecidos, la modificación deberá reflejarse en las reglas de nombrado, la estructura del repositorio y la documentación de Gestión de Configuración.

## Documentación relacionada

- Criterios de Línea Base: `00_Gestion_Configuracion/G6_CRITERIOS_LINEAS_BASE.md`

- Inventario de Ítems de Configuración: `00_Gestion_Configuracion/G6_INVENTARIO_IC.md`

- Informe del Trabajo Práctico 01: `G6_TPE01.pdf`