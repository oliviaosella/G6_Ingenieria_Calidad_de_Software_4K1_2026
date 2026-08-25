# Repositorio de Gestión de Configuración - G6

Este repositorio centraliza los ítems de configuración de la materia y establece una forma única de identificarlos, ubicarlos, revisarlos y conservarlos. La estructura y las reglas de nombrado se basan en el documento "Lineamientos de Items de Configuración.pdf".

## Objetivos del repositorio

- Mantener separados los materiales de clase, de cátedra, de producción propia y de trabajos prácticos.
- Facilitar la búsqueda y trazabilidad de cada ítem.
- Evitar duplicados y nombres ambiguos.
- Conservar versiones estables mediante Líneas Base.
- Registrar de forma controlada los cambios posteriores a una Línea Base.

## Estructura

~~~text
G6_REPOSITORIO/             
├── README.md              
├── .gitignore             
├── 00_Gestion_Configuracion/ 
│   ├── Lineas_Base/        
│   │   ├─G6_CRITERIOS_LINEAS_BASE.md 
│
│
├── 01_Clase/               
│   ├── Notas/              
│   └── Actividades/        
│
│
├── 02_Catedra/             
│   ├── Material/           
│   ├── Libros/             
│   ├── Templates/          
│   └── Planificacion/      
│
│
├── 03_Produccion_Propia/   
│   ├── Minutas/            
│   ├── Ejercicios/         
│   ├── Resumenes/          
│    └── Código/            
│      └── NombreProyecto/ 
│
│
└── 04_Trabajos_Practicos/  
├── Evaluables/         
│   ├── TP01/          
│   └── TP02/          
├── No_Evaluables/     
└── Investigacion/     
         └── G6_TI_LineamientosGenerales.pdf 

~~~

La carpeta 00_Gestion_Configuracion se incorpora para guardar la documentación administrativa del repositorio. No modifica la clasificación académica definida en los lineamientos.

## Criterio de ubicación

| Directorio | Contenido |
| --- | --- |
| 01_Clase | Notas tomadas durante la clase y presentaciones subrayadas o anotadas por los estudiantes. |
| 02_Catedra | Material limpio y oficial proporcionado por los docentes o publicado en la UV. |
| 03_Produccion_Propia | Resúmenes, ejercicios, minutas, código, hojas de cálculo y notas elaboradas fuera de clase. |
| 04_Trabajos_Practicos | Entregables evaluables, no evaluables y trabajos de investigación. |
| 00_Gestion_Configuracion | Inventario de ítems, criterios y registros de Líneas Base, solicitudes de cambio y texto para el informe. |

## Reglas generales de nombrado

1. Se conserva el prefijo G6_ indicado por el documento de lineamientos.
2. Los prefijos, códigos, autores y abreviaturas se escriben en mayúsculas.
3. El código de autor se forma con la inicial del primer nombre y la inicial del primer apellido.
4. El contenido descriptivo se escribe en PascalCase, tal como indica el documento fuente.
5. No se utilizan espacios, tildes ni caracteres especiales en los nombres de archivo.
6. Las extensiones se escriben en minúsculas.
7. Los números de trabajos y clases se escriben con dos dígitos para mantener el orden: 01, 02, 03.
8. No se reemplaza un archivo perteneciente a una Línea Base sin aplicar el procedimiento de control de cambios.

## Convenciones por tipo de ítem

| Ítem | Regla de nombrado | Ubicación |
| --- | --- | --- |
| Minuta | G6_MI_<FECHA_MM-DD>.md | 03_Produccion_Propia/Minutas |
| Trabajo Práctico Evaluable | G6_TPE<NUMERO>.pdf | 04_Trabajos_Practicos/Evaluables |
| Trabajo Práctico No Evaluable | G6_TPN<NUMERO>_<AUTOR>.pdf | 04_Trabajos_Practicos/No_Evaluables |
| Trabajo de Investigación | G6_TI<NUMERO>.pdf | 04_Trabajos_Practicos/Investigacion |
| Ejercicio | G6_EJ_<AUTOR>_<EJERCICIO>.pdf | 03_Produccion_Propia/Ejercicios |
| Resumen | G6_RE_<AUTOR>.pdf | 03_Produccion_Propia/Resumenes |
| Nota de Clase | G6_NC_<AUTOR>_<FECHA_MM-DD>.pdf | 01_Clase |
| Libro | G6_LI_U<UNIDAD>_<LIBRO>.pdf | 02_Catedra/Libros |
| Clase de cátedra | G6_CL<NUMERO>_U<UNIDAD>.pdf | 02_Catedra/Clases |
| Código | G6_COD_<NOMBRE_COMPONENTE>_TPE<NUMERO>.<extension> | 03_Produccion_Propia/Codigo |
| Template | G6_TE_<TEMA>.pdf | 02_Catedra/Templates |
| Consigna evaluable | G6_CO_TPE<NUMERO>.pdf | 02_Catedra/Consignas |
| Consigna no evaluable | G6_CO_TPN<NUMERO>.pdf | 02_Catedra/Consignas |
| Consigna de investigación | G6_CO_TI<NUMERO>.pdf | 02_Catedra/Consignas |
| Presentación de investigación | G6_PRE_TI<NUMERO>.pptx | 04_Trabajos_Practicos/Investigacion |
| Cronograma | G6_CR.xlsx | 02_Catedra/Planificacion |
| Registro de clases grabadas | G6_CG.xlsx | 02_Catedra/Clases_Grabadas |

Ejemplos:

- G6_MI_08-21.md
- G6_TPE01.pdf
- G6_TPN02_PT.pdf
- G6_EJ_CP_ALGORITMODEDIJKSTRA.pdf
- G6_NC_GE_08-21.pdf
- G6_LI_U2_AG.pdf
- G6_COD_LOGIN_TPE03.java

## Normas de trabajo con Git

- main contiene únicamente material revisado e integrado.
- Cada cambio se desarrolla en una rama con el formato tipo/descripcion-breve. Ejemplos: docs/readme-inicial, tpe/tpe01 o codigo/login.
- Después de la Línea Base inicial no se realizan cambios directos en main.
- Todo cambio se integra mediante una solicitud de incorporación revisada por, al menos, otro integrante.
- Cada incorporación debe actualizar el inventario o el registro de cambios cuando corresponda.
- Los mensajes de commit deben ser breves y descriptivos. Formato recomendado: TIPO: descripción. Ejemplo: DOC: incorpora criterios de Línea Base.
- Los borradores no se etiquetan como Línea Base.

## Líneas Base

Una Línea Base es un conjunto identificado, revisado y aprobado de ítems de configuración que se adopta como referencia estable. No equivale a un commit común: se establece solamente cuando existe un hito verificable y el contenido cumple los criterios de aceptación.

Las Líneas Base definidas son:
Una Línea Base es un conjunto identificado, revisado y aprobado de ítems de configuración que se adopta como referencia estable. No equivale a un commit común: se establece solamente cuando existe un hito verificable y el contenido cumple los criterios de aceptación.

Las Líneas Base definidas son:

| Momento | Etiqueta |
| --- | --- |
| Aprobación de estructura, README, inventario y reglas | LB_INICIAL |
| Cierre y aprobación del Trabajo Práctico 01 | LB_TP01_final |
| Cierre y aprobación del Trabajo Práctico 02 | LB_TP02_final |
| Cierre y aprobación de cada TP posterior | LB_TP03_final, LB_TP04_final, etc. |
| Auditoría y cierre final del repositorio | LB_FINAL |

Se crea una Línea Base independiente al concluir y aprobar cada Trabajo Práctico. El material de cátedra, las notas, la producción propia y el código asociado se integran en la Línea Base del TP correspondiente.

El detalle de condiciones, responsables y procedimiento se encuentra en `00_Gestion_Configuracion/Lineas_Base/G6_CRITERIOS_LINEAS_BASE.md`.

## Procedimiento resumido para establecer una Línea Base

1. Confirmar que el alcance del hito está completo.
2. Revisar nombres, ubicaciones, formatos y contenido.
3. Actualizar el inventario de ítems y el registro de cambios.
4. Obtener la aprobación del responsable del ítem y de otro integrante.
5. Integrar la versión aprobada en main.
6. Crear una etiqueta anotada e inmutable.
7. Registrar la etiqueta, fecha, commit, alcance y aprobadores.

Ejemplo:

~~~bash
git tag -a LB_P1_V1.0 -m "Linea Base correspondiente al cierre del Parcial 1"
git push origin LB_P1_V1.0
~~~

## Decisiones que deben validarse con la cátedra

- El documento fuente utiliza el prefijo G6_, por lo que se mantiene ese valor.
- Para las minutas se adopta .md como formato maestro por permitir comparación de cambios. Puede generarse un PDF con el mismo nombre cuando se necesite una versión de lectura.
- El documento fuente muestra la extensión .xmls para el cronograma y el registro de clases grabadas. Se normaliza a .xlsx por ser la extensión válida de Microsoft Excel.
- Si la cátedra exige otra interpretación, la corrección deberá registrarse como cambio de la norma de nombrado.

## Documentación relacionada

- Inventario: 00_Gestion_Configuracion/Inventario_IC/G6_INVENTARIO_IC.md
- Criterios de Línea Base: 00_Gestion_Configuracion/Lineas_Base/G6_CRITERIOS_LINEAS_BASE.md
- Registro de Líneas Base: 00_Gestion_Configuracion/Lineas_Base/G6_REGISTRO_LINEAS_BASE.md
- Registro de cambios: 00_Gestion_Configuracion/Control_Cambios/G6_REGISTRO_CAMBIOS.md
- Apartado listo para el informe: 00_Gestion_Configuracion/Informe/G6_JUSTIFICACION_LINEAS_BASE.md
