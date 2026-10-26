const ZONA_PARQUE = 'America/Argentina/Cordoba'

export function fechaEnParque(ahora = new Date()): string {
  const partes = new Intl.DateTimeFormat('en-US', {
    timeZone: ZONA_PARQUE, year: 'numeric', month: '2-digit', day: '2-digit',
  }).formatToParts(ahora)
  const valor = (tipo: string) => partes.find((parte) => parte.type === tipo)!.value
  return `${valor('year')}-${valor('month')}-${valor('day')}`
}

export function sumarDias(fecha: string, dias: number): string {
  const dia = new Date(`${fecha}T12:00:00Z`)
  dia.setUTCDate(dia.getUTCDate() + dias)
  return dia.toISOString().slice(0, 10)
}

export function motivoCierre(fecha: string): string | null {
  if (new Date(`${fecha}T12:00:00Z`).getUTCDay() === 1) return 'Cerrado los lunes'
  if (fecha.endsWith('-01-01')) return 'Cerrado el 1 de enero'
  if (fecha.endsWith('-12-25')) return 'Cerrado el 25 de diciembre'
  return null
}

export function fechasEnVentana(ahora = new Date()): string[] {
  const hoy = fechaEnParque(ahora)
  return [hoy, sumarDias(hoy, 1)]
}
