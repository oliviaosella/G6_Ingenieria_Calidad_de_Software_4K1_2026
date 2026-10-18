# Bitácora TDD: registro y validación de participantes

## Revisión inicial — 2026-10-15

### Alcance y evidencia

Se revisaron `backend/app/schemas.py`,
`backend/app/routers/inscripciones.py`,
`backend/tests/test_participantes.py` y, como contexto de integración,
`backend/app/main.py` y `backend/pyproject.toml`.
Se contrastó el comportamiento con los documentos del TP y las respuestas
del PO aportadas en la conversación.

Esta entrada registra una base existente verificada. No acredita ciclos
Red–Green–Refactor anteriores: no se observó su ejecución ni su historial.
No se modificó código de producción ni pruebas durante esta revisión.

### Implementación existente

| Elemento | Comportamiento verificado | Evaluación |
| --- | --- | --- |
| `Actividad` | Define Safari, Jardinería, Palestra y Tirolesa. | Coincide con las actividades requeridas. |
| `TalleVestimenta` | Define XS, S, M, L, XL y XXL. | Coincide con los talles definidos por el PO. |
| `Visitante` | Declara nombre, DNI y edad requeridos; talle con valor predeterminado `None`. | Estructura parcial válida. Presencia y conversión de tipos de Pydantic no equivalen a validación completa del dominio. |
| `validar_participantes` | Exige cantidad positiva e igual al largo de la lista. | Correcto para ese comportamiento aislado. No valida los datos individuales ni usa la actividad. |
| `validar_participante` | Rechaza nombre vacío o compuesto solo por espacios; admite palabras alfabéticas separadas por espacios. | La obligatoriedad está atendida parcialmente. La restricción a palabras alfabéticas no fue definida por el PO. |
| `validar_participante` | Admite talle ausente o perteneciente al conjunto permitido. Rechaza cadena vacía y talles desconocidos. | Correcto para pertenencia al catálogo. No exige talle según la actividad. |

### Pruebas existentes y ejecución

Comando ejecutado desde `backend/`, con Python 3.13 del entorno local:

```powershell
python -B -m pytest -p no:cacheprovider tests -q
```

Resultado: **8 pruebas aprobadas**.

- Cuatro pruebas comprueban existencia o compatibilidad de firmas; no
  verifican reglas de negocio. `signature(...).bind(...)` no ejecuta la función
  ni valida los tipos de los datos.
- Las otras cuatro comprueban cantidad positiva, coincidencia de cantidad
  con la lista, nombres y talles.
- Varias pruebas agrupan casos diferentes con múltiples aserciones.
  Conviene separarlos o parametrizarlos en una etapa de refactor.
- Las pruebas de cantidad usan el mismo DNI para dos personas; eso no
  demuestra una regla sobre duplicados ni un registro completo válido.

### Cumplimiento de estilo

**No cumple todavía PEP 8 estricto ni todas las convenciones del proyecto.**
La revisión fue manual y mediante inspección de líneas y AST; no se ejecutó
un linter completo, porque no están instalados pycodestyle, Ruff ni Flake8.

- Nombres de funciones en snake_case, clases en PascalCase e indentación
  de cuatro espacios: conformes en los archivos revisados.
- `schemas.py`: falta una segunda línea en blanco antes de `Actividad`
  y de `TalleVestimenta`.
- `inscripciones.py`: falta una segunda línea en blanco antes de
  `validar_participantes`; la expresión de `nombre_valido` tiene 91 caracteres.
- `test_participantes.py`: falta una segunda línea en blanco entre funciones;
  hay 14 líneas de más de 79 caracteres, espacios interiores innecesarios
  junto a llaves y una continuación de diccionario mal alineada.
- Seis funciones de test carecen de `-> None`. Esto incumple el requisito
  de Type Hints del proyecto, adicional a PEP 8.
- `list[dict]` no precisa los tipos de claves y valores. No es una infracción
  de PEP 8, pero deja incompleto el contrato de los participantes.
- Hay imports sin uso en `schemas.py` y agrupación de imports mejorable.
  Los imports sin uso son una observación de limpieza, no una regla de negocio.

### Comportamientos pendientes

Comprobaciones exploratorias ejecutadas sin agregar tests permanentes:

- `validar_participantes(1, [{}], Actividad.PALESTRA)` devuelve `True`.
- Un `Visitante` con nombre `Ana`, DNI vacío y edad `-1` es aceptado por
  `validar_participante`.

Por lo tanto, quedan pendientes los campos obligatorios a nivel de dominio,
la validez de la edad, las edades mínimas por actividad, el talle obligatorio
por actividad y la validación individual de todos los integrantes del grupo.
No deben inventarse una longitud de DNI, una edad máxima ni restricciones
de nombre sin una decisión explícita que las respalde.

Reglas confirmadas: Safari y Jardinería admiten todas las edades; Palestra
admite desde 12 años y Tirolesa desde 8, inclusive. Palestra y Tirolesa
requieren talle. El cupo disponible depende del turno y debe integrarse
con la funcionalidad responsable de disponibilidad.

Observación de integración: importar `app.main` desde `backend/` falla con
`ModuleNotFoundError: No module named 'routers'`. El módulo usa un import
que no coincide con el paquete `app`. Las pruebas actuales no importan
la aplicación y por eso no detectan este problema. El router todavía no
expone un endpoint de inscripción.

### Próximas iteraciones propuestas

1. Refactor de estilo de la base existente, sin cambiar comportamientos,
   seguido de la ejecución de las ocho pruebas.
2. Acordar la función pública que concentrará las reglas y la representación
   de entrada, respetando que GREEN solo puede modificar dominio/esquema.
   Actualmente las funciones están ubicadas en el archivo de rutas.
3. Agregar un caso por ciclo: DNI obligatorio, edad negativa, límites de edad
   de Palestra y Tirolesa, talle requerido ausente y talle opcional ausente.
   Incluir luego los casos positivos en los límites.
4. Verificar que un integrante inválido rechace el grupo completo y que
   varios integrantes válidos sean aceptados.
5. Integrar formulario y API cuando las reglas del dominio estén verificadas.

En cada ciclo: RED con fallo por el motivo esperado; GREEN con implementación
mínima; REFACTOR solo cuando exista una mejora concreta, manteniendo las
pruebas aprobadas. Registrar evidencia real de cada etapa, sin reconstruirla
retrospectivamente.

## Ciclo: cantidad de participantes no supera el cupo — 2026-10-18

Regla: la cantidad de participantes no puede superar el cupo máximo de la
actividad (Safari 8, Palestra 12, Jardinería 12, Tirolesa 10; ya definidos en
`Actividad`). El cupo disponible por turno corresponde al Grupo 1 y queda
fuera de este ciclo.

### Línea base
`uv run pytest -q` desde `backend/`: **10 pruebas aprobadas**.

### RED — commit `869d75a`
- Test: `test_validar_cantidad_no_supera_cupo_de_actividad`. Safari, 9
  participantes con DNI distinto, sin talle y con edad 25, para que el cupo sea
  el único motivo posible de rechazo.
- Casos: 8 participantes aceptados (borde inclusivo, ya pasaba) y 9 rechazados.
- Resultado: **1 fallida, 10 aprobadas**. Fallo esperado:
  `AssertionError: assert True is False` en la llamada con 9 participantes.

### Incidente durante el RED
Una corrida intermedia mostró 3 fallos. Dos eran de `test_validar_nombre` y
`test_validar_talles_vestimenta`: `schemas.py` tenía cambios sin commitear
(`Field` con longitud mínima de nombre, DNI de 7 a 8 caracteres y `talle`
tipado como enum), por lo que `Visitante(...)` lanzaba `ValidationError` antes
de llegar a la función. Esas restricciones no tenían un RED que las
justificara y contradicen la decisión de no inventar longitudes de DNI ni
restricciones de nombre. El origen probable fue un asistente del editor; el
cambio se revirtió y la línea base volvió a 10 aprobadas.

### GREEN — commit `44b78a2`
- Cambio: `actividad.cupo < cantidad` se agregó a la condición de cantidad de
  `validar_participantes`, evaluada al final del `or`.
- Resultado: **11 pruebas aprobadas**.
- Hallazgo: al ubicar la condición del cupo primero, falló
  `test_validar_cantidad_con_participantes_ingresados` con
  `AttributeError: 'bool' object has no attribute 'cupo'`. Ese test llama
  `validar_participantes(1, [], True)`: pasa un booleano donde la firma espera
  una `Actividad` (resto de cuando el parámetro era `requiere_talle`). Con el
  cupo al final, `cantidad != len(participantes)` corta el `or` y la rama del
  cupo no se ejecuta con ese dato, por lo que el defecto de la prueba sigue
  oculto.

### Pendiente
- REFACTOR: corregir el `True` del test mencionado por una `Actividad`.
- Regla 8: parametrizar la creación de participantes en las pruebas
  (DNI hardcodeados, diccionarios repetidos) y evaluar unificar `dict` y
  `Visitante`.
- Limpieza: líneas en blanco con espacios al inicio de
  `validar_participantes`.
- Integración con G1: el cupo disponible por turno todavía no se recibe.
