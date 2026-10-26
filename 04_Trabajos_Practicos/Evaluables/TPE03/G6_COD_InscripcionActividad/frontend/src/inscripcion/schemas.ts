import { z } from 'zod'
import type { ActividadInfo } from './catalogo'
import type { Participante } from './types'

const talles = ['XS', 'S', 'M', 'L', 'XL', 'XXL']

export function validarParticipantes(participantes: Participante[], info: ActividadInfo): string | null {
  if (!participantes.length || participantes.length > info.cupo) return `Elegí entre 1 y ${info.cupo} participantes.`
  const dnis = new Set<string>()
  for (let i = 0; i < participantes.length; i++) {
    const persona = participantes[i]
    const numero = i + 1
    const nombre = persona.nombre.trim().split(/\s+/)
    if (!nombre.length || !nombre.every((parte) => /^\p{L}+$/u.test(parte))) return `Revisá el nombre del participante ${numero}.`
    if (!/^\d+$/.test(persona.dni) || Number(persona.dni) < 1 || Number(persona.dni) > 999_999_999) return `Revisá el DNI del participante ${numero}.`
    if (dnis.has(persona.dni)) return 'Los DNI de los participantes no pueden repetirse.'
    dnis.add(persona.dni)
    const edad = Number(persona.edad)
    if (!/^\d+$/.test(persona.edad) || !Number.isInteger(edad) || edad < info.edadMinima) {
      return info.edadMinima ? `${info.id} requiere una edad mínima de ${info.edadMinima} años.` : `Revisá la edad del participante ${numero}.`
    }
    if (info.requiereTalle && !talles.includes(persona.talle_vestimenta)) return `Seleccioná el talle del participante ${numero}.`
    if (persona.talle_vestimenta && !talles.includes(persona.talle_vestimenta)) return `Revisá el talle del participante ${numero}.`
  }
  return null
}

export const emailSchema = z.email('Ingresá un correo electrónico válido.')

export const participanteVacio = (): Participante => ({ nombre: '', dni: '', edad: '', talle_vestimenta: '' })
