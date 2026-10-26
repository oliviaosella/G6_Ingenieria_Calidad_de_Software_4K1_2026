import { useEffect, useState } from 'react'
import { CalendarDays, ChevronLeft, ChevronRight, Clock3 } from 'lucide-react'
import { consultarCalendario } from '../api'
import type { CalendarioApi, HorarioApi } from '../api'
import type { ActividadId } from '../types'

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

export function HorarioSection({ actividad, fecha, hora, onFecha, onHora }: { actividad: ActividadId | null; fecha: string; hora: string; onFecha: (value: string) => void; onHora: (turno: HorarioApi) => void }) {
  const [respuesta, setRespuesta] = useState<{ actividad: string; calendario: CalendarioApi } | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [revision, setRevision] = useState(0)
  const [mesVista, setMesVista] = useState('')

  useEffect(() => {
    const timer = window.setInterval(() => setRevision((actual) => actual + 1), 60_000)
    return () => window.clearInterval(timer)
  }, [])
  useEffect(() => {
    if (!actividad) return
    let active = true
    setRespuesta(null)
    setLoading(true)
    setError('')
    consultarCalendario(actividad).then((result) => { if (active) setRespuesta({ actividad, calendario: result }) })
      .catch((issue) => { if (active) setError(issue instanceof Error ? issue.message : 'No se pudo consultar el calendario.') })
      .finally(() => { if (active) setLoading(false) })
    return () => { active = false }
  }, [actividad, revision])

  const calendario = respuesta?.actividad === actividad ? respuesta.calendario : null
  const dias = calendario?.dias ?? []
  const meses = [...new Set(dias.map((item) => item.fecha.slice(0, 7)))]
  const mesActual = meses.includes(mesVista) ? mesVista : meses[0]
  const indiceMes = meses.indexOf(mesActual)
  const nombreMes = mesActual && new Intl.DateTimeFormat('es-AR', { month: 'long', year: 'numeric', timeZone: 'UTC' })
    .format(new Date(`${mesActual}-01T12:00:00Z`))
  const tituloMes = nombreMes ? nombreMes.charAt(0).toUpperCase() + nombreMes.slice(1) : ''
  const horarios = dias.find((item) => item.fecha === fecha)?.horarios ?? []

  return <section aria-labelledby="horario-title" className="form-section schedule-section">
    <div className="section-heading"><h2 id="horario-title">Fecha y horario</h2>{calendario && <p>Próximas {calendario.anticipacion_maxima_horas} horas · mínimo {calendario.anticipacion_minima_minutos} minutos de anticipación.</p>}</div>
    {!actividad ? <div className="empty-prompt"><CalendarDays size={22} /> Primero elegí una actividad para ver los turnos.</div> : <>
      <div className="field-label"><CalendarDays size={17} /> Elegí una fecha</div>
      {loading && <div className="empty-prompt">Consultando turnos…</div>}
      {error && <p className="form-error" role="alert">{error}</p>}
      {!loading && !error && calendario && mesActual && <>
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
              const dia = dias.find((opcion) => opcion.fecha === item)
              const habilitado = dia?.estado === 'con_horarios'
              const motivo = dia?.motivo ?? (dia ? null : 'Fecha no habilitada para reservar')
              return <button
                className={`calendar-day ${fecha === item ? 'active' : ''} ${dia?.estado === 'cerrado' ? 'closed' : ''}`}
                type="button" key={item} disabled={!habilitado} aria-pressed={fecha === item}
                aria-label={`${fechaLarga(item)}${motivo ? `, ${motivo}` : habilitado ? ', con horarios' : ', no habilitada'}`}
                title={motivo || 'Ver horarios disponibles'} onClick={() => onFecha(item)}
              >{Number(item.slice(-2))}</button>
            })}
          </div>
          <p className="calendar-hint">Seleccioná una fecha habilitada para ver sus horarios.</p>
        </div>
        {dias.every((item) => item.estado !== 'con_horarios') && <div className="empty-prompt">No hay fechas reservables en la ventana informada por el servidor.</div>}
      </>}
      {fecha && !loading && <><div className="field-label time-label"><Clock3 size={17} /> Horarios <span>· Hora local del parque</span></div><div className="time-grid">{horarios.map((turno) => <button type="button" key={turno.horario_id} disabled={!turno.disponible} onClick={() => onHora(turno)} className={`time-pill ${hora === turno.hora ? 'active' : ''}`} aria-pressed={hora === turno.hora}><strong>{turno.hora}</strong><small>{turno.disponible ? `${turno.cupos_disponibles} lugares` : turno.motivo || 'Sin cupos'}</small></button>)}</div></>}
    </>}
  </section>
}
