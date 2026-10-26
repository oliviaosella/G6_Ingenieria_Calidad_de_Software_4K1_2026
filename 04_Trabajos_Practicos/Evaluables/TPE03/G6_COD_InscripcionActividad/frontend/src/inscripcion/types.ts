export type ActividadId = 'Tirolesa' | 'Safari' | 'Palestra' | 'Jardinería'

export type Participante = {
  nombre: string
  dni: string
  edad: string
  talle_vestimenta: string
}

export type InscripcionDraft = {
  actividad: ActividadId | null
  fecha: string
  hora: string
  participantes: Participante[]
  email: string
  aceptaTerminos: boolean
}

export type Reserva = {
  id: string
  actividad: ActividadId
  fecha: string
  hora: string
  participantes: Participante[]
  email: string
  qrUrl: string
  qrContenido: string
  correoEstado: string
  correoError: string | null
  intentosEnvio: number
}
