# Criterios para establecer Líneas Base

## 1. Definición

Una Línea Base es una versión identificada, revisada y formalmente aprobada de un conjunto de Ítems de Configuración. Funciona como referencia estable para continuar el trabajo y permite conocer con precisión qué archivos integraban el proyecto en un momento determinado. Una Línea Base no se genera ante cada modificación o commit, sino únicamente cuando se alcanza un hito relevante que requiere trazabilidad, posibilidad de recuperación y control sobre los cambios posteriores.

## 2. Condiciones obligatorias

Antes de crear una Línea Base deben cumplirse todas las condiciones siguientes:

1. **Alcance definido:** se conoce qué ítems y versiones forman parte del hito.

2. **Completitud:** no faltan archivos obligatorios para el objetivo de la Línea Base.

3. **Identificación correcta:** cada archivo respeta la convención de nombrado y su ubicación.

4. **Revisión de contenido:** no existen errores conocidos que impidan utilizar o entregar el conjunto.

5. **Coherencia:** consignas, entregables, anexos, presentaciones y código se corresponden entre sí.

6. **Trazabilidad:** el inventario de ítems y el registro de cambios están actualizados.

7. **Aprobación:** el responsable del ítem y, al menos, otro integrante revisaron la versión.

8. **Integración:** todos los archivos aprobados se encuentran en la rama `main` y el repositorio no presenta cambios locales pendientes.

9. **Reproducibilidad:** cuando hay código, se documentan dependencias e instrucciones y la versión puede ejecutarse o compilarse.

10. **Identificación técnica:** se registra el commit exacto mediante una etiqueta anotada de Git.

Si una de estas condiciones no se cumple, el contenido permanece como borrador o versión en revisión.

## 3. Momentos definidos

| Línea Base         | Momento de establecimiento                                                                                                  | Alcance mínimo                                                                               | Justificación                                                                                                                      |
| ------------------ | --------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| `LB_INICIAL` | Después de aprobar la estructura, el README, el inventario y las reglas de nombrado.                                        | Documentación de gestión y árbol inicial.                                                    | Fija un punto común de partida y evita que cada integrante organice o nombre los archivos de manera diferente.                     |
| `LB_TP01_final`    | Al finalizar el Trabajo Práctico 01, una vez incorporados, revisados y aprobados todos los ítems correspondientes.          | Consigna, documentación, entregables, código, anexos y demás ítems correspondientes al TP01. | Permite conservar una referencia estable del estado final del primer Trabajo Práctico y facilita su recuperación y auditoría.      |
| `LB_TP02_final`    | Al finalizar el Trabajo Práctico 02, una vez incorporados, revisados y aprobados todos los ítems correspondientes.          | Consigna, documentación, entregables, código, anexos y demás ítems correspondientes al TP02. | Permite conservar una referencia estable del estado final del segundo Trabajo Práctico y mantener trazabilidad sobre su evolución. |
| `LB_TP03_final`    | Al finalizar el Trabajo Práctico 03, una vez incorporados, revisados y aprobados todos los ítems correspondientes.          | Consigna, documentación, entregables, código, anexos y demás ítems correspondientes al TP03. | Permite identificar y recuperar el estado aprobado del tercer Trabajo Práctico.                                                    |
| `LB_TP04_final`    | Al finalizar el Trabajo Práctico 04, una vez incorporados, revisados y aprobados todos los ítems correspondientes.          | Consigna, documentación, entregables, código, anexos y demás ítems correspondientes al TP04. | Permite conservar una referencia estable del estado final del cuarto Trabajo Práctico y facilita su comparación y auditoría.       |
| `LB_TPxx_final`    | Al finalizar cada Trabajo Práctico posterior, una vez incorporados, revisados y aprobados todos los ítems correspondientes. | Totalidad de los ítems asociados al Trabajo Práctico correspondiente.                        | Mantiene el mismo criterio de control y trazabilidad para todos los Trabajos Prácticos del proyecto.                               |

No se establecen Líneas Base independientes por cada unidad, Parciales o componente de código; estos elementos se incorporan a la Línea Base del Trabajo Práctico correspondiente. De esta forma se evita una cantidad excesiva de etiquetas manteniendo un esquema sencillo, sin perder trazabilidad.


## 4. Identificación de las Líneas Base

Formato:

```text
LB_TP<NUMERO>_final
```

La nomenclatura identifica directamente el Trabajo Práctico al que pertenece la Línea Base.

Por ejemplo:

* `LB_INICIAL`
* `LB_TP01_final`
* `LB_TP02_final`
* `LB_TP03_final`
* `LB_TP04_final`

Para los Trabajos Prácticos posteriores se mantiene el mismo criterio:

* `LB_TP05_final`
* `LB_TP06_final`
* `LB_TP07_final`

El número del Trabajo Práctico debe utilizar dos dígitos para mantener una nomenclatura uniforme.

La palabra `final` indica que se trata de la versión aprobada correspondiente al cierre de ese Trabajo Práctico.

Las etiquetas de una Línea Base ya publicada son inmutables: no se eliminan, no se mueven a otro commit y no se reutilizan.



## 5. Cambios posteriores

Todo cambio solicitado sobre un ítem incluido en una Línea Base debe:

1. Registrarse con un identificador único.

2. Explicar el motivo, el alcance y los ítems afectados.

3. Evaluar el impacto sobre otros documentos, código y entregables.

4. Ser implementado en una rama separada.

5. Ser revisado antes de integrarse en `main`.

6. Generar una nueva etiqueta si modifica el contenido de referencia de una Línea Base.


No requieren una nueva Línea Base los commits de trabajo, los borradores incompletos ni las pruebas que todavía no fueron aprobadas.


## 6. Justificación de los momentos definidos para establecer Líneas Base

La primera Línea Base se establece una vez aprobados el árbol de carpetas, el README, el inventario de ítems y las reglas de nombrado, ya que estos elementos definen la forma en que todo el grupo incorporará y administrará la información. Fijarlos antes de cargar el resto del material reduce el riesgo de archivos duplicados, ubicaciones incorrectas o criterios distintos entre integrantes.
Las devoluciones de cada trabajo práctico evaluable se eligieron como hitos porque son los momentos donde debe encontrarse incorporado y verificado todo el material producido hasta la fecha, lo que permite conservar una versión completa del repositorio en los principales momentos de evaluación y comparar con claridad el avance entre todos los trabajos prácticos evaluables.
