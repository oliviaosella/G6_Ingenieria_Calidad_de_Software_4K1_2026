import { guardarReserva } from '../demoStore'
import { consultarHorarios } from '../horario/disponibilidadDemo'
import type { InscripcionDraft, Reserva } from '../types'

export function reservar(draft: InscripcionDraft): Reserva {
  const { actividad, fecha, hora, participantes, email, aceptaTerminos } = draft
  if (!actividad || !aceptaTerminos || !email || !hora) throw new Error('La solicitud está incompleta.')
  const turno = consultarHorarios(actividad, fecha).find((item) => item.hora === hora)
  if (!turno?.disponible || turno.cupos < participantes.length) throw new Error('Ese turno ya no tiene cupos suficientes. Elegí otro horario.')
  const reserva: Reserva = {
    id: `EHP-${Date.now().toString(36).toUpperCase()}-${Math.random().toString(36).slice(2, 6).toUpperCase()}`,
    actividad, fecha, hora, participantes, email, creadaEn: new Date().toISOString(),
  }
  guardarReserva(reserva)
  return reserva
}
