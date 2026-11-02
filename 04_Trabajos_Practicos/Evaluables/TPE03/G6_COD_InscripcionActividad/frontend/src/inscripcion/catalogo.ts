import type { ActividadApi } from './api'
import type { ActividadId } from './types'

// Solo recursos visuales. Los datos y las reglas de cada actividad llegan del API.
const presentacion: Record<string, { icono: 'zipline' | 'binoculars' | 'mountain' | 'sprout'; color: string; tema: string }> = {
  Tirolesa: { icono: 'zipline', color: 'sage', tema: 'tirolesa' },
  Safari: { icono: 'binoculars', color: 'sand', tema: 'safari' },
  Palestra: { icono: 'mountain', color: 'clay', tema: 'palestra' },
  Jardinería: { icono: 'sprout', color: 'mint', tema: 'jardineria' },
}

export type ActividadInfo = ActividadApi & {
  icono: 'zipline' | 'binoculars' | 'mountain' | 'sprout' | 'default'
  color: string
}

export const presentarActividad = (actividad: ActividadApi): ActividadInfo => ({
  ...actividad,
  icono: presentacion[actividad.id]?.icono ?? 'default',
  color: presentacion[actividad.id]?.color ?? 'sage',
})

export const themeName = (actividad: ActividadId | null) => actividad ? presentacion[actividad]?.tema ?? 'parque' : 'parque'
