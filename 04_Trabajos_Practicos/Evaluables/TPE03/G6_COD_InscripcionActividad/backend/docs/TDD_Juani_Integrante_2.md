# Juani — Integrante 2

## Responsabilidad

Validar la aceptación de términos dentro del subgrupo 2. La función vive en
`app/services/aceptacion.py` y sus pruebas en `tests/test_aceptacion.py`.

## Contrato e integración

```python
validar_aceptacion(actividad: Actividad, aceptacion: AceptacionTerminos) -> None
```

- Devuelve `None` cuando los términos están aceptados y la actividad coincide.
- Lanza `TerminosNoAceptadosError` si `aceptados` es `False`.
- Lanza `AceptacionDeOtraActividadError` si se aceptaron términos de otra actividad.
- Si ambos problemas coinciden, tiene prioridad `TerminosNoAceptadosError`.
  Es una decisión de implementación para obtener un resultado determinista,
  no una prioridad exigida expresamente por la User Story.

El integrante que coordina la confirmación debe importar y llamar la función
antes de reservar o notificar:

```python
from app.services.aceptacion import validar_aceptacion

validar_aceptacion(solicitud.actividad, solicitud.aceptacion_terminos)
# Solo continuar con la inscripción si no se lanzó una excepción.
```

La función valida un modelo ya construido; los errores de estructura corresponden
a Pydantic. No obtiene textos, persiste aceptación, valida participantes, consulta
cupos, reserva ni envía correo. No necesita servicios externos ni mocks.
La integración con el coordinador queda a cargo del integrante responsable y no
fue ejecutada en esta entrega individual.

## Evidencia del desarrollo

| Paso | Commit | Resultado observado |
|---|---|---|
| Red: términos no aceptados | `2ffade1` | 1 fallo: `DID NOT RAISE TerminosNoAceptadosError` |
| Green: rechazo mínimo | `65665f6` | 1 test pasa |
| Caso de aceptación válida | `415e560` | 2 tests pasan; ya estaba soportado, sin atribuir un Red inexistente |
| Red: términos de otra actividad | `feb0270` | 1 fallo: `DID NOT RAISE AceptacionDeOtraActividadError`; 2 pasan |
| Green: comparar actividades | `65e00e4` | 3 tests pasan |
| Ampliación de cobertura | `01d89f8` | 32 casos pasan; no requirió nueva lógica de producción |

En los primeros ciclos se revisó el diseño sin encontrar cambios útiles.
Al ampliar las pruebas apareció una duplicación real: la lista de pares de
actividades distintas. Se extrajo a `ACTIVIDADES_DISTINTAS` durante Refactor,
con 32 casos pasando antes y después. El commit se identifica como
`ADD(TP): unifico combinaciones de actividades en tests (refactor)`.

## Cobertura final

| Comportamiento | Casos |
|---|---:|
| Términos no aceptados para cada actividad | 4 |
| Aceptación válida para cada actividad | 4 |
| Aceptación de otra actividad, todos los pares distintos | 12 |
| No aceptación y actividad distinta, prioridad de error | 12 |
| Total | 32 |

Se usan parámetros de pytest para ejecutar los mismos comportamientos con
Tirolesa, Safari, Palestra y Jardinería sin duplicar funciones de prueba.

## Ejecutar

Desde `backend/`:

```bash
uv sync
uv run python -m pytest tests/test_aceptacion.py -v
```

Para ejecutar todas las pruebas disponibles del backend:

```bash
uv run python -m pytest -v
```

Resultado verificado el 13/10/2026: **32 passed**. Usar `python -m pytest`
permite resolver `app` desde backend sin modificar la configuración compartida.
