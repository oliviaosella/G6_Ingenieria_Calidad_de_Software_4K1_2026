import type { ActividadId, InscripcionDraft, Participante, Reserva } from './types'

const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000'

export class ApiError extends Error {
  readonly status: number
  constructor(message: string, status: number) { super(message); this.status = status }
}

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  let response: Response
  try {
    response = await fetch(`${API_URL}${path}`, options)
  } catch {
    throw new Error('No se pudo conectar con el servidor. Comprobá que el backend esté iniciado.')
  }
  if (!response.ok) {
    const body = await response.json().catch(() => null)
    const detail = body?.detail
    const message = typeof detail === 'string' ? detail
      : Array.isArray(detail) ? `El servidor rechazó estos datos: ${[...new Set(detail.map((issue) => issue.loc?.at(-1) ?? 'campo desconocido'))].join(', ')}.`
        : `La solicitud falló (${response.status}).`
    throw new ApiError(message, response.status)
  }
  return response.json() as Promise<T>
}

export type ActividadApi = {
  id: ActividadId
  categoria: string
  descripcion: string
  duracion: string
  cupo: number
  edad_minima: number
  requiere_talle: boolean
  talles_disponibles: string[]
}

export type HorarioApi = {
  horario_id: number
  hora: string
  cupos_disponibles: number
  disponible: boolean
  motivo: string | null
}

export type CalendarioApi = {
  anticipacion_minima_minutos: number
  anticipacion_maxima_horas: number
  dias: {
    fecha: string
    estado: 'con_horarios' | 'cerrado' | 'fuera_de_ventana' | 'sin_cupos'
    motivo: string | null
    horarios: HorarioApi[]
  }[]
}

export type TerminosApi = {
  actividad: ActividadId
  texto: string
  version: string
  pendiente_aprobacion: boolean
}

type InscripcionApi = {
  id: number
  actividad: ActividadId
  fecha: string
  horario: string
  participantes: { nombre: string; dni: string; edad: number; talle_vestimenta?: string | null }[]
  email: string
  qr_url: string
  qr_contenido: string
  correo_estado: string
  correo_error: string | null
  intentos_envio: number
}

const participantesParaApi = (participantes: Participante[]) => participantes.map((persona) => ({
  nombre: persona.nombre.trim(), dni: persona.dni.trim(), edad: persona.edad.trim() === '' ? null : Number(persona.edad),
  talle_vestimenta: persona.talle_vestimenta || null,
}))

const reservaDesdeApi = (result: InscripcionApi): Reserva => ({
  id: String(result.id), actividad: result.actividad, fecha: result.fecha, hora: result.horario,
  participantes: result.participantes.map((persona) => ({ ...persona, edad: String(persona.edad), talle_vestimenta: persona.talle_vestimenta || '' })),
  email: result.email, qrUrl: `${API_URL}${result.qr_url}`, qrContenido: result.qr_contenido,
  correoEstado: result.correo_estado, correoError: result.correo_error, intentosEnvio: result.intentos_envio,
})

export const listarActividades = () => request<ActividadApi[]>('/actividades')

export const consultarCalendario = (actividad: ActividadId) =>
  request<CalendarioApi>(`/actividades/${encodeURIComponent(actividad)}/calendario`)

export const consultarHorarios = (actividad: ActividadId, fecha: string) =>
  request<HorarioApi[]>(`/actividades/${encodeURIComponent(actividad)}/horarios?fecha=${fecha}`)

export const consultarTerminos = (actividad: ActividadId) =>
  request<TerminosApi>(`/actividades/${encodeURIComponent(actividad)}/terminos`)

export const validarParticipantesBackend = (actividad: ActividadId, participantes: Participante[]) =>
  request<{ valida: boolean }>('/inscripciones/validar', {
    method: 'POST', headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ actividad, cantidad: participantes.length, participantes: participantesParaApi(participantes) }),
  })

export const reenviarConfirmacion = async (id: string) =>
  reservaDesdeApi(await request<InscripcionApi>(`/inscripciones/${encodeURIComponent(id)}/reenviar-confirmacion`, { method: 'POST' }))

export async function reservar(draft: InscripcionDraft, version: string): Promise<Reserva> {
  if (!draft.actividad || draft.horarioId === null) throw new Error('Elegí una actividad y un horario.')
  const result = await request<InscripcionApi>('/inscripciones', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      actividad: draft.actividad,
      fecha: draft.fecha,
      horario_id: draft.horarioId,
      horario: draft.hora,
      cantidad_participantes: draft.participantes.length,
      participantes: participantesParaApi(draft.participantes),
      aceptacion_terminos: { actividad: draft.actividad, aceptados: draft.aceptaTerminos, version },
      email: draft.email.trim(),
    }),
  })
  return reservaDesdeApi(result)
}
