import { actividadPorId } from '../catalogo'
import { leerReservas } from '../demoStore'
import type { ActividadId, Horario } from '../types'

const horas = Array.from({ length: 9 }, (_, i) => `${String(i + 9).padStart(2, '0')}:00`)
const fechaLocal = (fecha: string, hora = '00:00') => new Date(`${fecha}T${hora}:00`)

export function fechaISO(fecha: Date) {
  const year = fecha.getFullYear()
  const month = String(fecha.getMonth() + 1).padStart(2, '0')
  const day = String(fecha.getDate()).padStart(2, '0')
  return `${year}-${month}-${day}`
}

function fechasDentroDe24Horas(now: Date): string[] {
  const fechas: string[] = []
  for (let offset = 0; offset <= 1; offset++) {
    const date = new Date(now.getFullYear(), now.getMonth(), now.getDate() + offset)
    const iso = fechaISO(date)
    if (date.getDay() !== 1 && !['12-25', '01-01'].includes(iso.slice(5)) && horas.some((hora) => {
      const delta = fechaLocal(iso, hora).getTime() - now.getTime()
      return delta >= 15 * 60_000 && delta <= 24 * 60 * 60_000
    })) fechas.push(iso)
  }
  return fechas
}

export function usandoRelojSimulado() { return fechasDentroDe24Horas(new Date()).length === 0 }

function relojDemo() {
  const now = new Date()
  if (!usandoRelojSimulado()) return now
  for (let offset = 1; offset <= 7; offset++) {
    const date = new Date(now.getFullYear(), now.getMonth(), now.getDate() + offset, 8)
    if (date.getDay() !== 1 && !['12-25', '01-01'].includes(fechaISO(date).slice(5))) return date
  }
  return now
}

export function fechasDisponibles(now = relojDemo()): string[] { return fechasDentroDe24Horas(now) }

export function consultarHorarios(actividad: ActividadId, fecha: string, now = relojDemo()): Horario[] {
  if (!fechasDentroDe24Horas(now).includes(fecha)) return []
  const cupoMaximo = actividadPorId(actividad)!.cupo
  const reservas = leerReservas()
  return horas.map((hora) => {
    const delta = fechaLocal(fecha, hora).getTime() - now.getTime()
    const ocupados = reservas.filter((reserva) => reserva.actividad === actividad && reserva.fecha === fecha && reserva.hora === hora)
      .reduce((total, reserva) => total + reserva.participantes.length, 0)
    const cupos = Math.max(0, cupoMaximo - ocupados)
    return { hora, cupos, disponible: delta >= 15 * 60_000 && delta <= 24 * 60 * 60_000 && cupos > 0 }
  })
}
