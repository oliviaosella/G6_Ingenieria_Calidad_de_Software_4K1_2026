import { CalendarDays, Clock3 } from 'lucide-react'
import { consultarHorarios, fechasDisponibles, usandoRelojSimulado } from './disponibilidadDemo'
import type { ActividadId } from '../types'

const dia = (fecha: string) => new Intl.DateTimeFormat('es-AR', { weekday: 'long' }).format(new Date(`${fecha}T12:00:00`))
const fechaCorta = (fecha: string) => new Intl.DateTimeFormat('es-AR', { day: 'numeric', month: 'short' }).format(new Date(`${fecha}T12:00:00`))

export function HorarioSection({ actividad, fecha, hora, onFecha, onHora }: { actividad: ActividadId | null; fecha: string; hora: string; onFecha: (value: string) => void; onHora: (value: string) => void }) {
  const fechas = fechasDisponibles()
  const horarios = actividad && fecha ? consultarHorarios(actividad, fecha) : []
  return <section aria-labelledby="horario-title" className="form-section schedule-section">
    <div className="section-heading"><h2 id="horario-title">Fecha y horario</h2><p>Próximas 24 horas · mínimo 15 minutos de anticipación.</p></div>
    {usandoRelojSimulado() && <div className="demo-time-note">Modo presentación: se muestran turnos simulados del próximo día abierto.</div>}
    {!actividad ? <div className="empty-prompt"><CalendarDays size={22} /> Primero elegí una actividad para ver los turnos.</div> : <>
      <div className="field-label"><CalendarDays size={17} /> Fecha disponible</div>
      <div className="date-options">{fechas.length ? fechas.map((item) => <button className={`date-pill ${fecha === item ? 'active' : ''}`} type="button" key={item} onClick={() => onFecha(item)}><span>{dia(item)}</span><strong>{fechaCorta(item)}</strong></button>) : <div className="empty-prompt">No hay turnos dentro de las próximas 24 horas. Volvé a consultar más tarde.</div>}</div>
      {fecha && <><div className="field-label time-label"><Clock3 size={17} /> Horarios <span>· Hora local del parque</span></div><div className="time-grid">{horarios.map((turno) => <button type="button" key={turno.hora} disabled={!turno.disponible} onClick={() => onHora(turno.hora)} className={`time-pill ${hora === turno.hora ? 'active' : ''}`} aria-pressed={hora === turno.hora}><strong>{turno.hora}</strong><small>{turno.disponible ? `${turno.cupos} lugares` : turno.cupos ? 'Fuera de horario' : 'Sin cupos'}</small></button>)}</div></>}
    </>}
  </section>
}
