# Guía de Integración Frontend - Backend: Eco Harmony Park

Este documento establece las pautas técnicas, contratos de datos y pasos para conectar la aplicación web interactiva ([frontend](file:///b:/Facultad/2026/ISW/Repo/Ingenieria_Calidad_de_Software_4K1_2026/04_Trabajos_Practicos/Evaluables/TPE03/G6_COD_InscripcionActividad/frontend)) con los endpoints RESTful de FastAPI ([backend](file:///b:/Facultad/2026/ISW/Repo/Ingenieria_Calidad_de_Software_4K1_2026/04_Trabajos_Practicos/Evaluables/TPE03/G6_COD_InscripcionActividad/backend)).

---

## 1. Información General y Entorno

- **URL Base de la API (Desarrollo):** `http://localhost:8000` (o `http://127.0.0.1:8000`)
- **Documentación Swagger UI interactiva:** `http://localhost:8000/docs`
- **Documentación ReDoc alternativa:** `http://localhost:8000/redoc`
- **Configuración de CORS:** Habilitado para los orígenes de desarrollo Vite:
  - `http://localhost:5173`
  - `http://127.0.0.1:5173`

---

## 2. Mapa de Endpoints y Sustitución de Mocks

| Funcionalidad / Pantalla | Endpoint Backend | Archivo Mock a Sustituir | Método HTTP |
| :--- | :--- | :--- | :---: |
| **Paso 1: Catálogo y Reglas** | `/actividades` | `src/inscripcion/catalogo.ts` | `GET` |
| **Paso 1: Turnos y Cupos** | `/actividades/{actividad}/horarios?fecha={YYYY-MM-DD}` | `src/inscripcion/horario/disponibilidadDemo.ts` | `GET` |
| **Paso 3: Términos Oficiales** | `/actividades/{actividad}/terminos` | `src/inscripcion/terminos/TerminosSection.tsx` | `GET` |
| **Paso 3: Confirmación Reserva** | `/inscripciones` | `src/inscripcion/reservas/reservasDemo.ts` | `POST` |
| **Consulta de Comprobante** | `/inscripciones/{id}` | `src/inscripcion/demoStore.ts` | `GET` |

---

## 3. Especificación Detallada de Contratos de la API

### 3.1. `GET /actividades`
Devuelve el catálogo de actividades habilitadas con sus reglas de admisión y capacidad base.

- **Respuesta 200 OK:**
  ```json
  [
    {
      "id": "Tirolesa",
      "categoria": "Aventura",
      "descripcion": "Una vista nueva del bosque, suspendido entre los árboles.",
      "duracion": "45 min",
      "cupo": 10,
      "edad_minima": 8,
      "requiere_talle": true
    },
    {
      "id": "Safari",
      "categoria": "Exploración",
      "descripcion": "Descubrí la vida del parque con una mirada más curiosa.",
      "duracion": "60 min",
      "cupo": 8,
      "edad_minima": 0,
      "requiere_talle": false
    },
    {
      "id": "Palestra",
      "categoria": "Desafío",
      "descripcion": "Elegí tu camino y alcanzá una nueva perspectiva.",
      "duracion": "50 min",
      "cupo": 12,
      "edad_minima": 12,
      "requiere_talle": true
    },
    {
      "id": "Jardinería",
      "categoria": "Naturaleza",
      "descripcion": "Manos a la tierra para conectar con lo que crece.",
      "duracion": "40 min",
      "cupo": 12,
      "edad_minima": 0,
      "requiere_talle": false
    }
  ]
  ```

---

### 3.2. `GET /actividades/{actividad}/terminos`
Devuelve el texto legal oficial de términos y condiciones para la actividad seleccionada.

- **Parámetro en ruta:** `actividad` (`Tirolesa` | `Safari` | `Palestra` | `Jardinería`)
- **Respuesta 200 OK:**
  ```json
  {
    "actividad": "Tirolesa",
    "texto": "Texto ficticio de términos de Tirolesa."
  }
  ```
- **Respuesta 422 Unprocessable Entity:** Si el nombre de la actividad no pertenece al enum válido.

---

### 3.3. `GET /actividades/{actividad}/horarios?fecha=YYYY-MM-DD`
Retorna los 9 turnos diarios (`09:00` a `17:00`) con sus cupos disponibles en tiempo real, reflejando las reservas previas confirmadas en el sistema.

- **Parámetro en ruta:** `actividad` (`Tirolesa` | `Safari` | `Palestra` | `Jardinería`)
- **Query Param:** `fecha` (por defecto `"2026-10-27"`)
- **Respuesta 200 OK:**
  ```json
  [
    {
      "horario_id": 1,
      "actividad": "Tirolesa",
      "fecha": "2026-10-27",
      "hora": "09:00",
      "cupos_disponibles": 10,
      "disponible": true
    },
    {
      "horario_id": 2,
      "actividad": "Tirolesa",
      "fecha": "2026-10-27",
      "hora": "10:00",
      "cupos_disponibles": 8,
      "disponible": true
    }
  ]
  ```

> [!NOTE]
> **Correspondencia Horario - ID:**  
> `horario_id: 1` -> `09:00` | `horario_id: 2` -> `10:00` | ... | `horario_id: 9` -> `17:00`.

---

### 3.4. `POST /inscripciones`
Orquesta la validación de términos, verificación de participantes, exclusión de DNIs duplicados en el mismo turno horario, descuento atómico de cupos y emisión de confirmación con código QR y notificación por correo.

- **Request Body (JSON):**
  ```json
  {
    "actividad": "Tirolesa",
    "horario_id": 1,
    "fecha": "2026-10-27",
    "horario": "09:00",
    "cantidad_participantes": 1,
    "participantes": [
      {
        "nombre": "Ana Pérez",
        "dni": "12345678",
        "edad": 25,
        "talle_vestimenta": "M"
      }
    ],
    "aceptacion_terminos": {
      "actividad": "Tirolesa",
      "aceptados": true
    },
    "email": "ana@example.com"
  }
  ```

- **Respuesta 201 Created:**
  ```json
  {
    "id": 1,
    "actividad": "Tirolesa",
    "horario_id": 1,
    "fecha": "2026-10-27",
    "horario": "09:00",
    "email": "ana@example.com",
    "participantes": [
      {
        "nombre": "Ana Pérez",
        "dni": "12345678",
        "edad": 25,
        "talle_vestimenta": "M"
      }
    ],
    "qr_codigo": "RESERVA-1"
  }
  ```

- **Manejo de Respuestas de Error:**
  - **`400 Bad Request`:**
    - Términos no aceptados: `"Los términos y condiciones deben ser aceptados para confirmar la inscripción."`
    - Inconsistencia de actividad: `"Los términos aceptados no corresponden a la actividad solicitada."`
    - Mismatch de cantidad: `"La cantidad de participantes declarada no coincide con los participantes enviados."`
  - **`409 Conflict`:**
    - Cupos agotados: `"No hay cupos disponibles suficientes para la actividad en el turno seleccionado."`
    - Superposición de DNI: `"Uno o más participantes ya tienen una reserva activa en este mismo turno horario."`
  - **`422 Unprocessable Entity`:** Formato incorrecto de email o tipos de datos inválidos.

---

### 3.5. `GET /inscripciones/{id}`
Permite recuperar los datos íntegros de una reserva generada previamente a partir de su identificador numérico.

- **Parámetro en ruta:** `id: int`
- **Respuesta 200 OK:**
  ```json
  {
    "id": 1,
    "actividad": "Tirolesa",
    "horario_id": 1,
    "participantes": [
      {
        "nombre": "Ana Pérez",
        "dni": "12345678",
        "edad": 25,
        "talle_vestimenta": "M"
      }
    ]
  }
  ```
- **Respuesta 404 Not Found:**
  ```json
  {
    "detail": "Reserva no encontrada."
  }
  ```

---

## 4. Guía de Migración de Archivos del Frontend

Al integrar la rama del frontend (`origin/tdd/frontend`), realizar las siguientes modificaciones puntuales:

### 1. `src/inscripcion/catalogo.ts`
- **Antes:** Arreglo estático `export const actividades = [...]`.
- **Después:** Reemplazar o alimentar la lista con una llamada:
  ```ts
  export async function cargarCatalogo(): Promise<ActividadInfo[]> {
    const res = await fetch(`${import.meta.env.VITE_API_URL}/actividades`)
    if (!res.ok) throw new Error('No se pudo cargar el catálogo de actividades')
    return res.json()
  }
  ```

### 2. `src/inscripcion/horario/disponibilidadDemo.ts`
- **Antes:** Cálculo de cupos restando de `demoStore.ts` en memoria del navegador.
- **Después:** Consultar los cupos al backend:
  ```ts
  export async function consultarHorariosApi(actividad: ActividadId, fecha: string): Promise<Horario[]> {
    const res = await fetch(`${import.meta.env.VITE_API_URL}/actividades/${encodeURIComponent(actividad)}/horarios?fecha=${fecha}`)
    if (!res.ok) throw new Error('Error al consultar horarios y cupos disponibles')
    return res.json()
  }
  ```

### 3. `src/inscripcion/terminos/TerminosSection.tsx`
- **Antes:** Texto hardcodeado *"Texto de muestra pendiente del PO"*.
- **Después:** Obtener los términos del backend al montar la sección:
  ```ts
  useEffect(() => {
    fetch(`${import.meta.env.VITE_API_URL}/actividades/${encodeURIComponent(actividad)}/terminos`)
      .then((res) => res.json())
      .then((data) => setTextoTerminos(data.texto))
  }, [actividad])
  ```

### 4. `src/inscripcion/reservas/reservasDemo.ts`
- **Antes:** Función `reservar(draft)` que guardaba en `localStorage` con ID aleatorio `EHP-...`.
- **Después:** Enviar la petición `POST /inscripciones`:
  ```ts
  export async function registrarInscripcionApi(draft: InscripcionDraft) {
    const payload = {
      actividad: draft.actividad,
      horario_id: parseInt(draft.hora.split(':')[0]) - 8, // ej. 09:00 -> horario_id 1
      fecha: draft.fecha,
      horario: draft.hora,
      cantidad_participantes: draft.participantes.length,
      participantes: draft.participantes.map(p => ({
        nombre: p.nombre,
        dni: p.dni,
        edad: parseInt(p.edad),
        talle_vestimenta: p.talle_vestimenta || null
      })),
      aceptacion_terminos: {
        actividad: draft.actividad,
        aceptados: draft.aceptaTerminos
      },
      email: draft.email
    }

    const res = await fetch(`${import.meta.env.VITE_API_URL}/inscripciones`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    })

    if (!res.ok) {
      const err = await res.json()
      throw new Error(err.detail || 'Error al procesar la inscripción')
    }

    return res.json()
  }
  ```

---

## 5. Verificación y Pruebas

1. **Ejecutar Suite de Pruebas del Backend:**
   ```bash
   cd backend
   uv run pytest -v
   ```
2. **Levantar el Servidor FastAPI en Desarrollo:**
   ```bash
   cd backend
   uv run uvicorn app.main:app --reload --port 8000
   ```
3. **Explorar y Probar Endpoints en Swagger UI:**
   - Abrir en el navegador: [http://localhost:8000/docs](http://localhost:8000/docs)
   - Ejecutar interactivamente `GET /actividades`, `GET /actividades/{actividad}/horarios` y `POST /inscripciones`.
