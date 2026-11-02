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


def formatear_comprobante(inscripcion: dict) -> str:
    datos = datos_comprobante(inscripcion)
    lineas = []
    for numero, participante in enumerate(datos["participantes"], start=1):
        nombre = " ".join(str(participante[campo]) for campo in ("nombre", "apellido") if participante.get(campo))
        lineas.append(f"{numero}. {nombre or 'Sin nombre'}")
        for etiqueta, campo in (("DNI", "dni"), ("Edad", "edad"), ("Talle de vestimenta", "talle_vestimenta")):
            if participante.get(campo) is not None and participante[campo] != "":
                lineas.append(f"   {etiqueta}: {participante[campo]}")
    detalle = "\n".join(lineas) if lineas else "No se informaron participantes."
    return (
        "ECO HARMONY PARK\nCOMPROBANTE DE INSCRIPCIÓN\n"
        "¡Inscripción confirmada!\n\n"
        f"Código: {datos['codigo']}\nNúmero de inscripción: {datos['id']}\n\n"
        "DETALLES DE LA ACTIVIDAD\n"
        f"Actividad: {datos['actividad']}\nFecha: {datos['fecha']}\nHorario: {datos['horario']} h\n"
        f"Correo: {datos['email']}\n\nPARTICIPANTES ({datos['cantidad_participantes']})\n"
        f"{detalle}\n"
    )


def contenido_qr(inscripcion: dict) -> str:
    """Texto para lectores QR humanos, con los mismos datos que el correo."""
    return formatear_comprobante(inscripcion)
