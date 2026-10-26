import { useEffect, useState } from 'react'
import { CalendarDays, ChevronLeft, ChevronRight, Clock3 } from 'lucide-react'
import { consultarHorarios } from '../api'
import type { HorarioApi } from '../api'
import type { ActividadId } from '../types'
import { fechasEnVentana, motivoCierre } from './calendario'

const diasSemana = ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom']
const fechaLarga = (fecha: string) => new Intl.DateTimeFormat('es-AR', {
  weekday: 'long', day: 'numeric', month: 'long', year: 'numeric', timeZone: 'UTC',
}).format(new Date(`${fecha}T12:00:00Z`))

function diasDelMes(mes: string): (string | null)[] {
  const [anio, numero] = mes.split('-').map(Number)
  const primerDia = new Date(Date.UTC(anio, numero - 1, 1))
  const desplazamiento = (primerDia.getUTCDay() + 6) % 7
  const cantidad = new Date(Date.UTC(anio, numero, 0)).getUTCDate()
  return [
    ...Array<null>(desplazamiento).fill(null),
    ...Array.from({ length: cantidad }, (_, index) => `${mes}-${String(index + 1).padStart(2, '0')}`),
  ]
}

export function HorarioSection({ actividad, fecha, hora, onFecha, onHora }: { actividad: ActividadId | null; fecha: string; hora: string; onFecha: (value: string) => void; onHora: (value: string, cupos: number) => void }) {
  const [dias, setDias] = useState<Record<string, HorarioApi[]>>({})
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [revision, setRevision] = useState(0)
  const [mesVista, setMesVista] = useState(() => fechasEnVentana()[0].slice(0, 7))

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
  const meses = [...new Set(fechas.map((item) => item.slice(0, 7)))]
  const mesActual = meses.includes(mesVista) ? mesVista : meses[0]
  const indiceMes = meses.indexOf(mesActual)
  const nombreMes = new Intl.DateTimeFormat('es-AR', { month: 'long', year: 'numeric', timeZone: 'UTC' })
    .format(new Date(`${mesActual}-01T12:00:00Z`))
  const tituloMes = nombreMes.charAt(0).toUpperCase() + nombreMes.slice(1)
  const horarios = dias[fecha] || []

  return <section aria-labelledby="horario-title" className="form-section schedule-section">
    <div className="section-heading"><h2 id="horario-title">Fecha y horario</h2><p>Próximas 24 horas · mínimo 15 minutos de anticipación.</p></div>
    {!actividad ? <div className="empty-prompt"><CalendarDays size={22} /> Primero elegí una actividad para ver los turnos.</div> : <>
      <div className="field-label"><CalendarDays size={17} /> Elegí una fecha</div>
      {loading && <div className="empty-prompt">Consultando turnos…</div>}
      {error && <p className="form-error" role="alert">{error}</p>}
      {!loading && !error && <>
        <div className="booking-calendar date-options" aria-label="Calendario de fechas disponibles">
          <div className="calendar-heading">
            <button type="button" aria-label="Mes anterior" disabled={indiceMes === 0} onClick={() => setMesVista(meses[indiceMes - 1])}><ChevronLeft size={18} /></button>
            <strong>{tituloMes}</strong>
            <button type="button" aria-label="Mes siguiente" disabled={indiceMes === meses.length - 1} onClick={() => setMesVista(meses[indiceMes + 1])}><ChevronRight size={18} /></button>
          </div>
          <div className="calendar-grid" role="group" aria-label={tituloMes}>
            {diasSemana.map((nombre) => <span className="calendar-weekday" key={nombre}>{nombre}</span>)}
            {diasDelMes(mesActual).map((item, index) => {
              if (!item) return <span className="calendar-empty" key={`empty-${index}`} aria-hidden="true" />
              const cierre = motivoCierre(item)
              const enVentana = fechas.includes(item)
              const sinTurnos = enVentana && !dias[item]?.length
              const motivo = cierre || (!enVentana ? 'Fuera de las próximas 24 horas' : sinTurnos ? 'Sin horarios reservables' : null)
              return <button
                className={`calendar-day ${fecha === item ? 'active' : ''} ${cierre ? 'closed' : ''}`}
                type="button" key={item} disabled={!!motivo} aria-pressed={fecha === item}
                aria-label={`${fechaLarga(item)}${motivo ? `, ${motivo}` : ', disponible'}`}
                title={motivo || 'Ver horarios disponibles'} onClick={() => onFecha(item)}
              >{Number(item.slice(-2))}</button>
            })}
          </div>
          <p className="calendar-hint">Fechas en verde: con horarios dentro de las próximas 24 horas. El parque cierra los lunes, el 1 de enero y el 25 de diciembre.</p>
        </div>
        {fechas.every((item) => !dias[item]?.length) && <div className="empty-prompt">No hay turnos reservables en las próximas 24 horas.</div>}
      </>}
      {fecha && !loading && <><div className="field-label time-label"><Clock3 size={17} /> Horarios <span>· Hora local del parque</span></div><div className="time-grid">{horarios.map((turno) => <button type="button" key={turno.hora} disabled={!turno.disponible} onClick={() => onHora(turno.hora, turno.cupos_disponibles)} className={`time-pill ${hora === turno.hora ? 'active' : ''}`} aria-pressed={hora === turno.hora}><strong>{turno.hora}</strong><small>{turno.disponible ? `${turno.cupos_disponibles} lugares` : 'Sin cupos'}</small></button>)}</div></>}
    </>}
  </section>
}
