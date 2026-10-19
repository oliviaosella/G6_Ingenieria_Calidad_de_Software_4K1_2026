import { z } from 'zod'
import { actividadPorId } from './catalogo'
import type { ActividadId, Participante } from './types'

const talles = ['XS', 'S', 'M', 'L', 'XL', 'XXL']

export function validarParticipantes(participantes: Participante[], actividad: ActividadId): string | null {
  const info = actividadPorId(actividad)!
  if (!participantes.length || participantes.length > info.cupo) return `Elegí entre 1 y ${info.cupo} participantes.`
  const dnis = new Set<string>()
  for (let i = 0; i < participantes.length; i++) {
    const persona = participantes[i]
    const numero = i + 1
    if (!/^[\p{L}]+(?:[ '-][\p{L}]+)*$/u.test(persona.nombre.trim())) return `Revisá el nombre del participante ${numero}.`
    if (!/^\d{1,9}$/.test(persona.dni) || Number(persona.dni) < 1) return `Revisá el DNI del participante ${numero}.`
    if (dnis.has(persona.dni)) return 'Los DNI de los participantes no pueden repetirse.'
    dnis.add(persona.dni)
    const edad = Number(persona.edad)
    if (!/^\d+$/.test(persona.edad) || !Number.isInteger(edad) || edad < info.edadMinima || edad > 120) {
      return info.edadMinima ? `${info.id} requiere una edad mínima de ${info.edadMinima} años.` : `Revisá la edad del participante ${numero}.`
    }
    if (info.requiereTalle && !talles.includes(persona.talle_vestimenta)) return `Seleccioná el talle del participante ${numero}.`
    if (persona.talle_vestimenta && !talles.includes(persona.talle_vestimenta)) return `Revisá el talle del participante ${numero}.`
  }
  return null
}

export const emailSchema = z.email('Ingresá un correo electrónico válido.')

export const participanteVacio = (): Participante => ({ nombre: '', dni: '', edad: '', talle_vestimenta: '' })
