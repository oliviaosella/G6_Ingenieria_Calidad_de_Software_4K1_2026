import type { ActividadInfo } from './catalogo'
import type { Participante } from './types'

// Replica las reglas de backend/app/services/participantes.py para avisar mientras se escribe.

export type ErroresParticipante = { nombre?: string; dni?: string; edad?: string; talle?: string }

// Filtros de tipeo: el campo no admite caracteres que el backend rechazaría.
export const filtrarNombre = (value: string) => value.replace(/[^\p{L} ]/gu, '')
export const filtrarDni = (value: string) => value.replace(/[^0-9]/g, '').slice(0, 8)
export const filtrarEdad = (value: string) => value.replace(/[^0-9]/g, '').slice(0, 3)

export const validarNombre = (nombre: string) =>
  nombre.trim() ? null : 'Ingresá nombre y apellido.'

export const validarDni = (dni: string) => {
  if (!dni) return 'Ingresá el DNI.'
  if (dni.length < 8) return `Faltan ${8 - dni.length} dígitos: el DNI tiene 8.`
  if (dni === '00000000') return 'El DNI no puede ser 00000000.'
  return null
}

export const validarEdad = (edad: string, edadMinima: number, actividad: string) => {
  if (!edad) return 'Ingresá la edad.'
  if (Number(edad) <= 0 || Number(edad) > 100) return 'La edad debe estar entre 0-100 años.'
  if (Number(edad) < edadMinima) return `La edad mínima para ${actividad} es ${edadMinima} años.`
  return null
}

export const validarTalle = (talle: string, info: ActividadInfo) =>
  info.requiere_talle && !talle ? 'Elegí un talle.' : null

export const validarEmail = (email: string) => {
  if (!email.trim()) return 'Ingresá tu correo electrónico.'
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.trim()) ? null : 'Ingresá un correo válido (ej. tu@email.com).'
}

// Indica con qué otro participante comparte el DNI (cruce entre tarjetas).
export const dniRepetidoCon = (participantes: Participante[], index: number) => {
  const dni = participantes[index].dni
  if (dni.length < 8) return null
  const otro = participantes.findIndex((persona, i) => i !== index && persona.dni === dni)
  return otro === -1 ? null : otro + 1
}

export const erroresDe = (participantes: Participante[], index: number, info: ActividadInfo): ErroresParticipante => {
  const persona = participantes[index]
  const repetido = dniRepetidoCon(participantes, index)
  return {
    nombre: validarNombre(persona.nombre) ?? undefined,
    dni: (validarDni(persona.dni) ?? (repetido ? `Este DNI ya está cargado en el participante ${repetido}.` : null)) ?? undefined,
    edad: validarEdad(persona.edad, info.edad_minima, info.id) ?? undefined,
    talle: validarTalle(persona.talle_vestimenta, info) ?? undefined,
  }
}

export const hayErrores = (participantes: Participante[], info: ActividadInfo) =>
  participantes.some((_, index) => Object.values(erroresDe(participantes, index, info)).some(Boolean))
