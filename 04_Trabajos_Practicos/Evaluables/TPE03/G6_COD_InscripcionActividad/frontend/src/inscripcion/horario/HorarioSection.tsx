import { useEffect, useState } from 'react'
import { CalendarDays, Clock3 } from 'lucide-react'
import { consultarHorarios } from '../api'
import type { HorarioApi } from '../api'
import type { ActividadId } from '../types'

const dia = (fecha: string) => new Intl.DateTimeFormat('es-AR', { weekday: 'long' }).format(new Date(`${fecha}T12:00:00`))
const fechaCorta = (fecha: string) => new Intl.DateTimeFormat('es-AR', { day: 'numeric', month: 'short' }).format(new Date(`${fecha}T12:00:00`))
const fechaISO = (date: Date) => `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`

export function HorarioSection({ actividad, fecha, hora, onFecha, onHora }: { actividad: ActividadId | null; fecha: string; hora: string; onFecha: (value: string) => void; onHora: (value: string) => void }) {
  const [dias, setDias] = useState<Record<string, HorarioApi[]>>({})
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  useEffect(() => {
    if (!actividad) return
    let active = true
    const now = new Date()
    const fechas = [0, 1].map((offset) => fechaISO(new Date(now.getFullYear(), now.getMonth(), now.getDate() + offset)))
    setDias({})
    setLoading(true)
    setError('')
    Promise.all(fechas.map((item) => consultarHorarios(actividad, item))).then((results) => {
      if (active) setDias(Object.fromEntries(fechas.map((item, index) => [item, results[index]])))
    }).catch((issue) => { if (active) setError(issue instanceof Error ? issue.message : 'No se pudieron consultar los turnos.') })
      .finally(() => { if (active) setLoading(false) })
    return () => { active = false }
  }, [actividad])
  const fechas = Object.keys(dias).filter((item) => dias[item].length > 0)
  const horarios = dias[fecha] || []
  return <section aria-labelledby="horario-title" className="form-section schedule-section">
    <div className="section-heading"><h2 id="horario-title">Fecha y horario</h2><p>Próximas 24 horas · mínimo 15 minutos de anticipación.</p></div>
    {!actividad ? <div className="empty-prompt"><CalendarDays size={22} /> Primero elegí una actividad para ver los turnos.</div> : <>
      <div className="field-label"><CalendarDays size={17} /> Fecha disponible</div>
      {loading && <div className="empty-prompt">Consultando turnos…</div>}
      {error && <p className="form-error" role="alert">{error}</p>}
      {!loading && !error && <div className="date-options">{fechas.length ? fechas.map((item) => <button className={`date-pill ${fecha === item ? 'active' : ''}`} type="button" key={item} onClick={() => onFecha(item)}><span>{dia(item)}</span><strong>{fechaCorta(item)}</strong></button>) : <div className="empty-prompt">No hay turnos dentro de las próximas 24 horas. Volvé a consultar más tarde.</div>}</div>}
      {fecha && !loading && <><div className="field-label time-label"><Clock3 size={17} /> Horarios <span>· Hora local del parque</span></div><div className="time-grid">{horarios.map((turno) => <button type="button" key={turno.hora} disabled={!turno.disponible} onClick={() => onHora(turno.hora)} className={`time-pill ${hora === turno.hora ? 'active' : ''}`} aria-pressed={hora === turno.hora}><strong>{turno.hora}</strong><small>{turno.disponible ? `${turno.cupos_disponibles} lugares` : 'Sin cupos'}</small></button>)}</div></>}
    </>}
  </section>
}
