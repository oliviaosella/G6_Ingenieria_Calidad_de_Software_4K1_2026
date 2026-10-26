# Documento de Justificación y Evidencia TDD
## PRÁCTICO 6 - TDD (Evaluable) - Ingeniería y Calidad de Software 4K1 2026
**Historia de Usuario:** *Inscribirme a actividad*  
**Subgrupo / Responsabilidad:** **Grupo 5 — Gestión de Reservas y Cupos**  
**Integrantes:** Guerci, Moyano, Perez
**Rama de trabajo:** `gestion-reservas-cupos`

---

## 1. Alcance y Responsabilidad del Módulo

El objetivo de este módulo es gestionar el ciclo de vida de las reservas de actividades, garantizando la consistencia, persistencia y control estricto de cupos disponibles por actividad y turno horario, evitando problemas de sobreventa incluso ante accesos concurrentes.

### Funcionalidades clave implementadas:
1. **Control de Capacidad Inicial por Actividad:** Inicialización declarativa según el catálogo de actividades (Safari: 8, Palestra: 12, Jardinería: 12, Tirolesa: 10).
2. **Descuento Atómico de Cupos:** Descuento preciso del número de lugares solicitados asegurando la independencia entre turnos y actividades.
3. **Validación de Disponibilidad:** Rechazo preventivo cuando no hay cupos o cuando los cupos restantes son insuficientes, sin modificar el estado previo.
4. **Validación de Integridad y Consistencia:** Rechazo de solicitudes con cantidad menor o igual a cero, o inconsistencia entre el conteo numérico y la lista de participantes.
5. **Prevención de Solapamiento:** Detección y rechazo si un mismo DNI intenta inscribirse en dos actividades en un mismo horario.
6. **Persistencia en Memoria y Consulta:** Generación de identificador único (`id`) y recuperación íntegra de la reserva con copia defensiva.
7. **Concurrencia Thread-Safe (Anti-Sobreventa):** Exclusión mutua (`threading.Lock`) para prevenir condiciones de carrera cuando múltiples solicitudes simultáneas compiten por los últimos cupos disponibles.

---

## 2. Contrato de la API del Servicio (`GestorReservas`)

El servicio [`GestorReservas`](backend/app/services/reservas.py) expone los siguientes métodos públicos:

### `consultar_cupos(actividad: str, horario_id: str) -> int`
- **Descripción:** Retorna la cantidad de cupos disponibles para una actividad en un turno específico.
- **Precondiciones:** La actividad debe existir en las capacidades base del sistema.

### `crear_reserva(actividad: str, horario_id: str, cantidad: int, participantes: list[dict]) -> dict`
- **Descripción:** Valida la disponibilidad, consistencia y ausencia de solapamiento, descuenta los cupos de manera atómica, persiste la reserva y retorna el comprobante/ticket generado.
- **Retorno:**
  ```python
  {
      "id": 1,
      "actividad": "Safari",
      "horario_id": "H1",
      "cantidad": 2,
      "participantes": [
          {"nombre": "Ana", "dni": "12345678"},
          {"nombre": "Carlos", "dni": "87654321"}
      ]
  }
  ```
- **Excepciones / Errores:** Lanza `ValueError` con mensajes explicativos claros ante cupos insuficientes, datos inconsistentes o participantes duplicados en el mismo turno.

### `obtener_reserva(reserva_id: int) -> dict | None`
- **Descripción:** Obtiene una copia íntegra de la reserva registrada por su identificador único. Retorna `None` si no existe.

---

## 3. Matriz de Evidencia del Ciclo TDD (Red - Green - Refactor)

Se desarrollaron 12 pruebas unitarias siguiendo rigurosamente el ciclo de vida TDD:

| # | Test | Fase RED (Fallo inicial) | Fase GREEN (Solución mínima) | Fase REFACTOR (Mejora y diseño) |
|---|------|--------------------------|------------------------------|---------------------------------|
| **1** | `test_capacidad_inicial_segun_actividad` | `NameError: GestorReservas no definido` | Clase con diccionario estático `CAPACIDADES_INICIALES` | Definición de constantes claras y legibles |
| **2** | `test_reserva_valida_descuenta_cupos_correctamente` | `AttributeError: no existe crear_reserva` | Diccionario dinámico `_cupos` que resta `cantidad` | Estructuración de claves compuestas `(actividad, horario_id)` |
| **3** | `test_independencia_de_cupos_entre_turnos_distintos` | Turno H2 compartía cupos con H1 | Clave de diccionario combinada `(actividad, horario_id)` | Helper `_obtener_clave` para centralizar la lógica |
| **4** | `test_rechazar_reserva_en_horario_sin_cupos` | Reserva permitida aún con 0 cupos | `if cupos_actuales < cantidad: raise ValueError` | Mensajes de error declarativos y descriptivos |
| **5** | `test_rechazar_reserva_cuando_cupos_son_insuficientes` | Permitía reservas parciales o valores negativos | Validación estricta `cupos_disponibles < cantidad` | Verificación de inmutabilidad del estado ante rechazos |
| **6** | `test_crear_reserva_asocia_actividad_horario_y_participantes` | Retornaba solo booleano | Retorno de diccionario con id autoincremental y participantes | Asignación de identificador único correlativo |
| **7** | `test_rechazar_reserva_con_cantidad_cero_o_negativa` | Permitía crear reserva con cantidad `0` o `-1` | Validación `if cantidad <= 0 or not participantes: raise ValueError` | Agrupación de validaciones de entrada |
| **8** | `test_rechazar_si_cantidad_no_coincide_con_numero_de_participantes` | Se permitía mismatch entre `cantidad` y `len(participantes)` | Verificación `len(participantes) != cantidad` | Mensaje descriptivo con valores esperados vs recibidos |
| **9** | `test_rechazar_inscripcion_de_mismo_dni_en_horarios_superpuestos` | Mismo DNI podía anotarse en 2 actividades al mismo horario | Búsqueda cruzada de DNIs en reservas previas del mismo turno | Optimización de búsqueda usando operaciones de conjuntos (`set`) |
| **10** | `test_reserva_rechazada_no_persiste_datos_ni_modifica_cupos` | Posible inconsistencia de estado si fallaba a mitad de proceso | Validaciones ejecutadas antes de cualquier mutación de cupos o guardado | Garantía de atomicidad transaccional en memoria |
| **11** | `test_persistencia_recuperar_reserva_por_id` | `AttributeError: no existe obtener_reserva` | Repositorio en memoria `self._reservas[id]` | Retorno de copia defensiva (`dict.copy()`) para evitar mutaciones externas |
| **12** | `test_dos_solicitudes_simultaneas_por_ultimos_lugares_evita_sobreventa` | Condición de carrera (race condition) al ejecutar hilos concurrentes | Implementación de cerrojo `threading.Lock()` | Separación en helpers `_consultar_cupos_sin_lock` para evitar deadlocks |

---

## 4. Decisiones de Diseño y Buenas Prácticas

1. **Atomicidad de Operaciones:**
   Todas las precondiciones y reglas de negocio se evalúan antes de registrar la reserva o descontar cupos. Si alguna validación falla, el sistema aborta de inmediato sin efectos colaterales.
2. **Seguridad ante Concurrencia (Thread-Safety):**
   Se utilizó `threading.Lock()` englobando la comprobación y descuento de cupos. Para mantener el código limpio y evitar interbloqueos (deadlocks) por llamadas internas reentrantes, se desacopló la lógica de lectura interna (`_consultar_cupos_sin_lock`).
3. **Copias Defensivas (Inmutabilidad del Repositorio):**
   Al consultar reservas por ID con `obtener_reserva(id)`, se entrega una copia superficial/defensiva del diccionario y de la lista de participantes, evitando que consumidores externos corrompan el estado del repositorio en memoria.
4. **Compatibilidad con otros módulos:**
   - **Grupo 3 (Validación de Participantes):** Recibe estructuras de participantes con `nombre` y `dni`.
   - **Grupo 4 (Envío de Confirmación y Mail):** La reserva entrega un `id` numérico y conserva `participantes`, compatible directamente con el generador de QR y envío de correo (`InscripcionConfirmada`).

---
