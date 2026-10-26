import { useEffect, useState } from 'react'
import { CalendarDays, Clock3 } from 'lucide-react'
import { consultarHorarios } from '../api'
import type { HorarioApi } from '../api'
import type { ActividadId } from '../types'
import { fechasEnVentana, motivoCierre } from './calendario'

const dia = (fecha: string) => new Intl.DateTimeFormat('es-AR', { weekday: 'long', timeZone: 'UTC' }).format(new Date(`${fecha}T12:00:00Z`))
const fechaCorta = (fecha: string) => new Intl.DateTimeFormat('es-AR', { day: 'numeric', month: 'short', timeZone: 'UTC' }).format(new Date(`${fecha}T12:00:00Z`))

export function HorarioSection({ actividad, fecha, hora, onFecha, onHora }: { actividad: ActividadId | null; fecha: string; hora: string; onFecha: (value: string) => void; onHora: (value: string) => void }) {
  const [dias, setDias] = useState<Record<string, HorarioApi[]>>({})
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [revision, setRevision] = useState(0)
  useEffect(() => {
    const timer = window.setInterval(() => setRevision((actual) => actual + 1), 60_000)
    return () => window.clearInterval(timer)
  }, [])
  useEffect(() => {
    if (!actividad) return
    let active = true
    const fechas = fechasEnVentana()
    setDias({})
    setLoading(true)
    setError('')
    Promise.all(fechas.map((item) => consultarHorarios(actividad, item))).then((results) => {
      if (active) setDias(Object.fromEntries(fechas.map((item, index) => [item, results[index]])))
    }).catch((issue) => { if (active) setError(issue instanceof Error ? issue.message : 'No se pudieron consultar los turnos.') })
      .finally(() => { if (active) setLoading(false) })
    return () => { active = false }
  }, [actividad, revision])
  const fechas = fechasEnVentana()
  const horarios = dias[fecha] || []
  return <section aria-labelledby="horario-title" className="form-section schedule-section">
    <div className="section-heading"><h2 id="horario-title">Fecha y horario</h2><p>Próximas 24 horas · mínimo 15 minutos de anticipación.</p></div>
    {!actividad ? <div className="empty-prompt"><CalendarDays size={22} /> Primero elegí una actividad para ver los turnos.</div> : <>
      <div className="field-label"><CalendarDays size={17} /> Fecha disponible</div>
      {loading && <div className="empty-prompt">Consultando turnos…</div>}
      {error && <p className="form-error" role="alert">{error}</p>}
      {!loading && !error && <><div className="date-options">{fechas.map((item) => {
        const cierre = motivoCierre(item)
        const sinTurnos = !dias[item]?.length
        const motivo = cierre || (sinTurnos ? 'Fuera de la ventana de 24 h' : null)
        return <button className={`date-pill ${fecha === item ? 'active' : ''}`} type="button" key={item} disabled={!!motivo} onClick={() => onFecha(item)} title={motivo || undefined}><span>{dia(item)}</span><strong>{fechaCorta(item)}</strong>{motivo && <small>{motivo}</small>}</button>
      })}</div>{fechas.every((item) => !dias[item]?.length) && <div className="empty-prompt">No hay turnos reservables en las próximas 24 horas. Los lunes, el 1 de enero y el 25 de diciembre el parque está cerrado.</div>}</>}
      {fecha && !loading && <><div className="field-label time-label"><Clock3 size={17} /> Horarios <span>· Hora local del parque</span></div><div className="time-grid">{horarios.map((turno) => <button type="button" key={turno.hora} disabled={!turno.disponible} onClick={() => onHora(turno.hora)} className={`time-pill ${hora === turno.hora ? 'active' : ''}`} aria-pressed={hora === turno.hora}><strong>{turno.hora}</strong><small>{turno.disponible ? `${turno.cupos_disponibles} lugares` : 'Sin cupos'}</small></button>)}</div></>}
    </>}
  </section>
}
