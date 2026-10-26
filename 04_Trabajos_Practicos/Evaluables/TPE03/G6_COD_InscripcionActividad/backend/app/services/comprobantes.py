import json


def datos_comprobante(inscripcion: dict) -> dict:
    """Única fuente de información para correo, QR y respuesta de confirmación."""
    return {
        "version": 1,
        "codigo": f"RESERVA-{inscripcion['id']}",
        "id": inscripcion["id"],
        "actividad": inscripcion.get("actividad", ""),
        "fecha": inscripcion.get("fecha", ""),
        "horario": inscripcion.get("horario", ""),
        "email": inscripcion.get("email", ""),
        "cantidad_participantes": len(inscripcion.get("participantes", [])),
        "participantes": [
            {clave: valor for clave, valor in participante.items()
             if clave in ("nombre", "apellido", "dni", "edad", "talle_vestimenta") and valor is not None}
            for participante in inscripcion.get("participantes", [])
        ],
    }


def contenido_qr(inscripcion: dict) -> str:
    return json.dumps(datos_comprobante(inscripcion), ensure_ascii=False, separators=(",", ":"))
