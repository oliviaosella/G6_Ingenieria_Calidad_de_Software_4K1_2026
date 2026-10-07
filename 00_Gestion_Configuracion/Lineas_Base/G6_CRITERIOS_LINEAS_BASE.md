# Criterios para establecer Líneas Base

## 1. Definición

Una Línea Base es una versión identificada, revisada y aprobada de uno o más ítems de configuración que se utiliza como referencia estable para el trabajo posterior. A partir de su establecimiento, cualquier modificación debe quedar registrada, ser evaluada y generar una nueva versión de la Línea Base cuando corresponda.

Una Línea Base no se crea por cada commit ni por el simple paso del tiempo. Se crea cuando existe un hito verificable que necesita trazabilidad, recuperación y comparación.

## 2. Condiciones obligatorias

Antes de crear una Línea Base deben cumplirse todas las condiciones siguientes:

1. Alcance definido: se conoce qué ítems y versiones forman parte del hito.
2. Completitud: no faltan archivos obligatorios para el objetivo de la Línea Base.
3. Identificación correcta: cada archivo respeta la convención de nombrado y su ubicación.
4. Revisión de contenido: no existen errores conocidos que impidan utilizar o entregar el conjunto.
5. Coherencia: consignas, entregables, anexos, presentaciones y código se corresponden entre sí.
6. Trazabilidad: el inventario de ítems y el registro de cambios están actualizados.
7. Aprobación: el responsable del ítem y, al menos, otro integrante revisaron la versión.
8. Integración: todos los archivos aprobados se encuentran en la rama main y el repositorio no presenta cambios locales pendientes.
9. Reproducibilidad: cuando hay código, se documentan dependencias e instrucciones y la versión puede ejecutarse o compilarse.
10. Identificación técnica: se registra el commit exacto mediante una etiqueta anotada de Git.

Si una de estas condiciones no se cumple, el contenido permanece como borrador o versión en revisión.

## 3. Momentos definidos

| Línea Base | Momento de establecimiento | Alcance mínimo | Justificación |
| --- | --- | --- | --- |
| LB_INICIAL_V1.0 | Después de aprobar la estructura, el README, el inventario y las reglas de nombrado. | Documentación de gestión y árbol inicial. | Fija un punto común de partida y evita que cada integrante organice o nombre los archivos de manera diferente. |
| LB_P1_V1.0 | Al cerrar el primer parcial, una vez incorporados y verificados los ítems producidos hasta ese momento. | Material de cátedra, notas de clase, producción propia, trabajos prácticos y código correspondientes al primer parcial. | Permite recuperar y auditar el estado completo del repositorio al finalizar el primer hito de evaluación. |
| LB_P2_V1.0 | Al cerrar el segundo parcial, una vez incorporados y verificados los nuevos ítems y las correcciones aprobadas. | Todo lo incluido en P1 más el material, los trabajos y el código correspondientes al segundo parcial. | Consolida el avance acumulado del cursado en el segundo hito de evaluación y permite compararlo con el estado anterior. |
| LB_FINAL_V1.0 | Después de completar todas las actividades y realizar la auditoría final. | Totalidad de los ítems vigentes, inventario y registros. | Representa el estado definitivo del repositorio y sirve como evidencia del trabajo realizado durante la materia. |

No se crean Líneas Base independientes por unidad, Trabajo Práctico o componente de código. Esos elementos se integran en la Línea Base del parcial correspondiente.

## 4. Identificación de las Líneas Base

Formato:

~~~text
LB_<HITO>_V<MAYOR>.<MENOR>
~~~

Los únicos valores previstos inicialmente para HITO son INICIAL, P1, P2 y FINAL:

- LB_INICIAL_V1.0
- LB_P1_V1.0
- LB_P2_V1.0
- LB_FINAL_V1.0

P1 y P2 significan Parcial 1 y Parcial 2.

Se incrementa la versión menor ante una corrección aprobada que no cambia el alcance del hito. Se incrementa la versión mayor cuando cambia el alcance, se reemplaza un entregable aceptado o se modifica de forma sustancial su contenido.

Las etiquetas de una Línea Base ya publicada son inmutables: no se eliminan, no se mueven a otro commit y no se reutilizan.

## 5. Procedimiento de aprobación

1. El responsable propone el conjunto candidato e indica su alcance.
2. Otro integrante revisa nombres, ubicación, contenido y relación con la consigna.
3. Se resuelven las observaciones antes de aprobar.
4. Se actualizan el inventario y el registro de cambios.
5. Se integra el conjunto aprobado en main.
6. Se crea una etiqueta anotada.
7. Se completa el Registro de Líneas Base con fecha, commit, alcance y aprobadores.

Comandos de referencia:

~~~bash
git switch main
git pull
git status
git tag -a LB_P1_V1.0 -m "Linea Base correspondiente al cierre del Parcial 1"
git push origin LB_P1_V1.0
~~~

## 6. Cambios posteriores

Todo cambio solicitado sobre un ítem incluido en una Línea Base debe:

1. Registrarse con un identificador único.
2. Explicar el motivo, el alcance y los ítems afectados.
3. Evaluar el impacto sobre otros documentos, código y entregables.
4. Ser implementado en una rama separada.
5. Ser revisado antes de integrarse en main.
6. Generar una nueva etiqueta si modifica el contenido de referencia.

No requieren una nueva Línea Base los commits de trabajo, los borradores incompletos ni las pruebas que todavía no fueron aprobadas.

## 7. Responsabilidad

La aprobación es compartida: participa el autor o responsable del contenido y, como mínimo, otro integrante en función de revisor. Para la Línea Base final se requiere la conformidad de todo el grupo.
