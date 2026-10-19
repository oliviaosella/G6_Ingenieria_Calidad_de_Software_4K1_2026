import type { ActividadId } from './types'

export type ActividadInfo = {
  id: ActividadId
  categoria: string
  descripcion: string
  duracion: string
  cupo: number
  edadMinima: number
  requiereTalle: boolean
  icono: 'zipline' | 'binoculars' | 'mountain' | 'sprout'
  color: string
}

export const actividades: ActividadInfo[] = [
  { id: 'Tirolesa', categoria: 'Aventura', descripcion: 'Una vista nueva del bosque, suspendido entre los árboles.', duracion: '45 min', cupo: 10, edadMinima: 8, requiereTalle: true, icono: 'zipline', color: 'sage' },
  { id: 'Safari', categoria: 'Exploración', descripcion: 'Descubrí la vida del parque con una mirada más curiosa.', duracion: '60 min', cupo: 8, edadMinima: 0, requiereTalle: false, icono: 'binoculars', color: 'sand' },
  { id: 'Palestra', categoria: 'Desafío', descripcion: 'Elegí tu camino y alcanzá una nueva perspectiva.', duracion: '50 min', cupo: 12, edadMinima: 12, requiereTalle: true, icono: 'mountain', color: 'clay' },
  { id: 'Jardinería', categoria: 'Naturaleza', descripcion: 'Manos a la tierra para conectar con lo que crece.', duracion: '40 min', cupo: 12, edadMinima: 0, requiereTalle: false, icono: 'sprout', color: 'mint' },
]

export const actividadPorId = (id: ActividadId | null) => actividades.find((actividad) => actividad.id === id)

export const themeName = (actividad: ActividadId | null) => actividad ? ({ Tirolesa: 'tirolesa', Safari: 'safari', Palestra: 'palestra', Jardinería: 'jardineria' } as const)[actividad] : 'parque'
