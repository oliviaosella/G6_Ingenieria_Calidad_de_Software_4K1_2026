import type { Reserva } from './types'

const STORAGE_KEY = 'eco-harmony-park-reservas-v1'

export function leerReservas(): Reserva[] {
  try { return JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]') as Reserva[] }
  catch { return [] }
}

export function guardarReserva(reserva: Reserva) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify([...leerReservas(), reserva]))
}
