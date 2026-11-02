# Candidata a Línea Base `LB_TP03_rev01`

**Estado:** pendiente de revisión y aprobación independiente.  
**No existe todavía una etiqueta `LB_TP03_rev01`.**

**Solicitud de revisión:** [Issue #6 — Revisión formal para establecer LB_TP03_rev01](https://github.com/oliviaosella/G6_Ingenieria_Calidad_de_Software_4K1_2026/issues/6), asignada a `LautaroCastill0` el 2026-11-02.

## Línea Base de origen

- Etiqueta: `LB_TP03_final`
- Commit: `95787c9e834ef93f23e9105515a0175ac71d18b7`
- Fecha efectiva: 2026-10-29 11:31:58 -03:00

## Alcance candidato

- `04_Trabajos_Practicos/Evaluables/TPE03/G6_COD_InscripcionActividad/`
- `04_Trabajos_Practicos/Evaluables/TPE03/G6_TPE03_Documentacion_TDD.pdf`
- Registros `CC-LB-002`, `CC-LB-004` y `CC-LB-005`.

## Cambios respecto de `LB_TP03_final`

1. Integración del código histórico del TPE03 en `main` mediante `500ad58`.
2. Incorporación de la documentación final TDD mediante `12725c2`.
3. Incorporación de `opencv-python-headless` en `requirements.txt` y eliminación de dos advertencias del frontend mediante `cfa32ef`.
4. Incorporación del inventario y los controles automáticos mediante `074328c`.
5. Actualización de los registros de Gestión de Configuración para preparar esta revisión.

## Evidencia técnica

- [x] Instalación limpia desde `requirements.txt`.
- [x] Backend: 188 pruebas aprobadas.
- [x] Frontend: lint sin advertencias.
- [x] Frontend: build de producción correcto.
- [x] Validador del repositorio sin incumplimientos.
- [x] GitHub Actions: jobs `repository`, `tpe03-backend` y `tpe03-frontend` aprobados.
- [ ] Revisión de un integrante distinto del autor del cierre.
- [ ] Registro del nombre, usuario, fecha y evidencia de aprobación.
- [ ] Identificación del commit exacto aprobado.
- [ ] Creación y publicación de la etiqueta anotada `LB_TP03_rev01`.

## Criterio de aprobación

La candidata sólo se convierte en Línea Base cuando otro integrante verifica el alcance y la evidencia, deja una aprobación identificable y el commit aprobado se encuentra en `main` con todos los controles automáticos exitosos.

Después de la aprobación se debe:

1. completar esta ficha con el revisor, la fecha, el enlace de evidencia y el commit aprobado;
2. cambiar el estado de los registros correspondientes a `Aprobado e integrado`;
3. renombrar esta ficha como `LB_TP03_rev01.md`;
4. crear una etiqueta anotada sin modificar la fecha técnica real;
5. publicar la etiqueta y actualizar `G6_REGISTRO_LINEAS_BASE.md`.
