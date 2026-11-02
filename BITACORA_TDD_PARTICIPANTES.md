# Bitácora de Desarrollo TDD - Registro y Validación de Participantes

**Cátedra:** Ingeniería y Calidad de Software - Año 2026  
**Institución:** Universidad Tecnológica Nacional – Facultad Regional Córdoba (UTN FRC)  
**Curso:** 4K1  
**Grupo:** N° 6  
**Trabajo Práctico:** Evaluables / TPE N° 3  
**User Story:** "Inscribirme a actividad"  
**Subgrupo / Módulo:** Registro y Validación de Participantes  

---

## 1. Especificación de la Interfaz Mínima Acordada (Punto 4.2.3)

Conforme a las pautas de arquitectura, guías de estilo (PEP 8 estricto, Type Hints) y requerimientos del PO:

### 1.1. Modelos y Esquemas (`app/schemas.py`)
- **`Actividad(str, Enum)`**:
  - `TIROLESA = ("Tirolesa", True, 10, 8)`: Talle obligatorio, cupo 10, edad mínima 8.
  - `SAFARI = ("Safari", False, 8, 0)`: Talle no obligatorio, cupo 8, todas las edades (0).
  - `PALESTRA = ("Palestra", True, 12, 12)`: Talle obligatorio, cupo 12, edad mínima 12.
  - `JARDINERIA = ("Jardinería", False, 12, 0)`: Talle no obligatorio, cupo 12, todas las edades (0).
  - Atributos:
    - `talle_obligatorio: bool`: Determina si la actividad demanda talle de vestimenta obligatorio.
    - `cupo: int`: Cupo máximo de participantes admitidos por turno.
    - `edad_minima: int`: Edad mínima requerida para participar.

- **`TalleVestimenta(str, Enum)`**:
  - `XS = "XS"`, `S = "S"`, `M = "M"`, `L = "L"`, `XL = "XL"`, `XXL = "XXL"`

- **`Visitante(BaseModel)`**:
  - `nombre: str`: Nombre y apellido (obligatorio, no vacío, caracteres alfabéticos).
  - `dni: str`: Documento Nacional de Identidad (obligatorio, numérico).
  - `edad: int`: Entero mayor o igual a 0.
  - `talle_vestimenta: str | None = None`: Talle de vestimenta (opcional u obligatorio según la actividad).
