# Criterios para establecer Líneas Base

## 1. Definición

Una Línea Base es una versión identificada, revisada y aprobada de uno o más ítems de configuración que se utiliza como referencia estable para el trabajo posterior. A partir de su establecimiento, cualquier modificación debe quedar registrada, ser evaluada y generar una nueva versión de la Línea Base cuando corresponda.

Una Línea Base no se crea por cada commit ni por el simple paso del tiempo. Se crea cuando existe un hito verificable que necesita trazabilidad, recuperación y comparación.

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

Cada Trabajo Práctico posee su propia Línea Base independiente. Los distintos componentes de un Trabajo Práctico se integran dentro de la Línea Base correspondiente y no generan Líneas Base independientes por archivo, unidad o componente.

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



De esta manera se conserva la referencia histórica de la versión originalmente aprobada.

## 5. Procedimiento de aprobación

1. El responsable propone el conjunto candidato e indica su alcance.

2. Otro integrante revisa nombres, ubicación, contenido y relación con la consigna del Trabajo Práctico.

3. Se resuelven las observaciones antes de aprobar.

4. Se actualizan el inventario y el registro de cambios.

5. Se integra el conjunto aprobado en `main`.

6. Se crea una etiqueta anotada.

7. Se completa el Registro de Líneas Base con fecha, commit, alcance y aprobadores.

Comandos de referencia:

```bash
git switch main
git pull
git status
git tag -a LB_TP04_final -m "Linea Base correspondiente al cierre del Trabajo Practico 04"
git push origin LB_TP04_final
```

El nombre de la etiqueta debe modificarse de acuerdo con el Trabajo Práctico que se esté cerrando.

## 6. Cambios posteriores

Todo cambio solicitado sobre un ítem incluido en una Línea Base debe:

1. Registrarse con un identificador único.

2. Explicar el motivo, el alcance y los ítems afectados.

3. Evaluar el impacto sobre otros documentos, código y entregables.

4. Ser implementado en una rama separada.

5. Ser revisado antes de integrarse en `main`.

6. Generar una nueva etiqueta si modifica el contenido de referencia de una Línea Base.

Por ejemplo, si luego de establecer `LB_TP04_final` se detecta una modificación necesaria en uno de sus ítems, la etiqueta original se conserva y, una vez aprobada la modificación, se establece una nueva versión, como `LB_TP04_final_v2`.

No requieren una nueva Línea Base los commits de trabajo, los borradores incompletos ni las pruebas que todavía no fueron aprobadas.

## 7. Responsabilidad

La aprobación es compartida: participa el autor o responsable del contenido y, como mínimo, otro integrante en función de revisor.

Para cada Trabajo Práctico, la Línea Base se establece únicamente cuando el contenido correspondiente haya sido revisado y aprobado por los responsables definidos por el grupo.

La Línea Base final del proyecto requiere la conformidad de todo el grupo.

# Justificación de los momentos definidos para establecer Líneas Base

Para la organización del repositorio se considera Línea Base a una versión identificada, revisada y formalmente aprobada de un conjunto de ítems de configuración. Esta versión funciona como referencia estable para continuar el trabajo y permite conocer con precisión qué archivos integraban el proyecto en un momento determinado. Por ese motivo, una Línea Base no se genera ante cada modificación o commit, sino únicamente cuando se alcanza un hito relevante que requiere trazabilidad, posibilidad de recuperación y control sobre los cambios posteriores.

La primera Línea Base se establece una vez aprobados el árbol de carpetas, el README, el inventario de ítems y las reglas de nombrado. Este momento fue seleccionado porque dichos elementos definen la forma en que todo el grupo incorporará y administrará la información. Al fijarlos antes de cargar el resto del material, se reduce el riesgo de que aparezcan archivos duplicados, ubicaciones incorrectas o criterios diferentes entre los integrantes. Esta Línea Base inicial constituye, por lo tanto, el punto de partida común para el repositorio.

Los siguientes hitos seleccionados corresponden al cierre de cada Trabajo Práctico. En cada uno de estos momentos deben encontrarse incorporados, verificados y aprobados todos los ítems producidos para el Trabajo Práctico correspondiente, incluyendo la documentación, consignas, entregables, anexos, presentaciones y código cuando corresponda.

La decisión de establecer una Línea Base independiente para cada Trabajo Práctico permite mantener una referencia clara y específica de cada instancia de trabajo. De esta manera, es posible conocer exactamente cuál era el estado aprobado de un Trabajo Práctico al momento de su cierre, recuperar sus archivos y comparar posteriormente las modificaciones realizadas.

Por ejemplo, al finalizar el Trabajo Práctico 04 se establece la Línea Base `LB_TP04_final`. Esta etiqueta identifica el commit exacto que contiene la versión aprobada del Trabajo Práctico 04. Si posteriormente fuera necesario modificar alguno de sus elementos, la versión original permanece disponible y cualquier modificación aprobada puede quedar registrada mediante una nueva versión de la Línea Base.

No se establecen Líneas Base independientes por cada unidad, archivo, componente de código o elemento individual. Estos elementos forman parte del conjunto correspondiente al Trabajo Práctico y quedan incluidos dentro de su Línea Base. Así se evita generar una cantidad excesiva de etiquetas y se mantiene un esquema sencillo, sin perder trazabilidad.

Este criterio también permite separar correctamente los distintos hitos del proyecto. Cada Trabajo Práctico representa una unidad de trabajo con un alcance definido, por lo que su cierre constituye un momento adecuado para congelar y documentar el estado alcanzado. De esta manera, las Líneas Base se corresponden con eventos concretos del desarrollo del proyecto y no con períodos de tiempo arbitrarios.

Por último, la Línea Base inicial permite establecer las reglas generales de organización antes de comenzar a consolidar los Trabajos Prácticos. A partir de ella, cada Trabajo Práctico genera su propia Línea Base al momento de ser finalizado y aprobado.

En todos los casos, el establecimiento de una Línea Base exige que los archivos estén completos, correctamente nombrados y ubicados, revisados por el responsable y por al menos otro integrante, integrados en la rama principal y registrados en el inventario. La Línea Base se identifica mediante una etiqueta anotada de Git asociada a un commit específico. Una vez publicada, esa etiqueta no se elimina ni se reasigna.

Cualquier modificación posterior debe tramitarse mediante el control de cambios y, si altera la referencia aprobada, debe originar una nueva versión de la Línea Base correspondiente. De esta manera, los momentos seleccionados permiten mantener una referencia estable de cada Trabajo Práctico, conservar evidencia de los hitos importantes y garantizar la trazabilidad de los cambios realizados durante el proyecto. 
