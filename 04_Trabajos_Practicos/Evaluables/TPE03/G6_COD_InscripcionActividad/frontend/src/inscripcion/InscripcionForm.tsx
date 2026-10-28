import { useEffect, useRef, useState } from 'react'
import { ArrowLeft, ArrowRight, Check } from 'lucide-react'
import { ApiError, consultarHorarios, consultarTerminos, listarActividades, reenviarConfirmacion, reservar, validarParticipantesBackend } from './api'
import type { TerminosApi } from './api'
import { presentarActividad } from './catalogo'
import type { ActividadInfo } from './catalogo'
import { ActividadSection } from './actividad/ActividadSection'
import { SummaryScene } from './actividad/SummaryScene'
import { ConfirmacionSection } from './confirmacion/ConfirmacionSection'
import { HorarioSection } from './horario/HorarioSection'
import { GuiaAssistant } from './mascota/GuiaAssistant'
import { ParticipantesSection } from './participantes/ParticipantesSection'
import { participanteVacio } from './draft'
import { TerminosSection } from './terminos/TerminosSection'
import type { ActividadId, InscripcionDraft, Reserva } from './types'
import { hayErrores, validarEmail } from './validaciones'

const initialDraft = (): InscripcionDraft => ({ actividad: null, fecha: '', hora: '', horarioId: null, participantes: [participanteVacio()], email: '', aceptaTerminos: false })
const steps = ['Actividad', 'Participantes', 'Confirmar']

export function InscripcionForm({ onActividadChange, onConfirmedChange }: { onActividadChange: (actividad: ActividadId | null) => void; onConfirmedChange: (confirmed: boolean) => void }) {
  const [draft, setDraft] = useState(initialDraft)
  const [step, setStep] = useState(0)
  const [error, setError] = useState('')
  const [reserva, setReserva] = useState<Reserva | null>(null)
  const [actividades, setActividades] = useState<ActividadInfo[]>([])
  const [catalogoError, setCatalogoError] = useState('')
  const [terminos, setTerminos] = useState<TerminosApi | null>(null)
  const [cuposSeleccionados, setCuposSeleccionados] = useState<number | null>(null)
  const [busy, setBusy] = useState(false)
  const [intento, setIntento] = useState(false)
  const topRef = useRef<HTMLDivElement>(null)
  const info = actividades.find((item) => item.id === draft.actividad)

  useEffect(() => {
    let active = true
    listarActividades().then((items) => {
      if (active) setActividades(items.map(presentarActividad))
    }).catch((issue) => { if (active) setCatalogoError(issue instanceof Error ? issue.message : 'No se pudieron cargar las actividades.') })
    return () => { active = false }
  }, [])

  useEffect(() => {
    if (step !== 2 || !draft.actividad) return
    let active = true
    setTerminos(null)
    consultarTerminos(draft.actividad).then((result) => { if (active) setTerminos(result) })
      .catch((issue) => { if (active) setError(issue instanceof Error ? issue.message : 'No se pudieron cargar las condiciones.') })
    return () => { active = false }
  }, [step, draft.actividad])

  const personasCargadas = draft.participantes.filter((persona) =>
    persona.nombre.trim() && persona.dni.trim() && persona.edad.trim() && (!info?.requiere_talle || persona.talle_vestimenta)
  ).length
  const update = (change: Partial<InscripcionDraft>) => { setDraft((current) => ({ ...current, ...change })); setError('') }
  const scrollTop = () => topRef.current?.scrollIntoView({ behavior: 'smooth', block: 'start' })
  const go = (next: number) => { setStep(next); setError(''); setIntento(false); requestAnimationFrame(scrollTop) }
  const chooseActivity = (actividad: ActividadId) => {
    update({ actividad, fecha: '', hora: '', horarioId: null, aceptaTerminos: false, participantes: draft.participantes.map((persona) => ({ ...persona, talle_vestimenta: '' })) })
    setTerminos(null)
    setCuposSeleccionados(null)
    onActividadChange(actividad)
  }

  const next = async () => {
    if (step === 0) {
      if (!draft.actividad || !draft.fecha || draft.horarioId === null) return setError('Elegí una actividad, una fecha y un horario disponible.')
      return go(1)
    }
    if (step === 1) {
      if (!info || !draft.actividad) return setError('Volvé a elegir una actividad.')
      if (hayErrores(draft.participantes, info)) {
        setIntento(true)
        return setError('Revisá los campos marcados en rojo para continuar.')
      }
      setBusy(true)
      try {
        const [validacion, horarios] = await Promise.all([
          validarParticipantesBackend(draft.actividad, draft.participantes),
          consultarHorarios(draft.actividad, draft.fecha),
        ])
        if (!validacion.valida) return setError('Los datos de los participantes no cumplen las reglas de la actividad.')
        const turno = horarios.find((item) => item.horario_id === draft.horarioId)
        setCuposSeleccionados(turno?.cupos_disponibles ?? 0)
        if (!turno?.disponible || turno.cupos_disponibles < draft.participantes.length) {
          return setError(`El turno tiene ${turno?.cupos_disponibles ?? 0} lugares disponibles. Volvé y elegí otro horario.`)
        }
        go(2)
      } catch (problem) {
        setError(problem instanceof Error ? problem.message : 'No se pudo validar la inscripción.')
      } finally { setBusy(false) }
      return
    }
    const errorEmail = validarEmail(draft.email)
    if (errorEmail) { setIntento(true); return setError(errorEmail) }
    if (!draft.aceptaTerminos) return setError('Aceptá las condiciones de la actividad para confirmar.')
    if (!terminos) return setError('Esperá a que se carguen las condiciones de la actividad.')
    setBusy(true)
    try {
      setReserva(await reservar(draft, terminos.version))
      onConfirmedChange(true)
      setError('')
      requestAnimationFrame(scrollTop)
    } catch (problem) {
      if (problem instanceof ApiError && problem.status === 400 && problem.message.startsWith('Los términos cambiaron') && draft.actividad) {
        setTerminos(await consultarTerminos(draft.actividad).catch(() => null))
        setDraft((current) => ({ ...current, aceptaTerminos: false }))
      }
      setError(problem instanceof Error ? problem.message : 'No se pudo guardar la reserva.')
    } finally { setBusy(false) }
  }

  const nuevaReserva = () => {
    setDraft(initialDraft())
    setReserva(null)
    setCuposSeleccionados(null)
    setTerminos(null)
    onActividadChange(null)
    onConfirmedChange(false)
    go(0)
  }

  return <div className={`booking-layout ${reserva ? 'is-confirmed' : ''}`} ref={topRef}>
    <div className="booking-main">
      {!reserva ? <>
        <div className="stepper" aria-label="Progreso de inscripción">{steps.map((label, index) => <div key={label} className={`step-item ${step === index ? 'current' : ''} ${step > index ? 'done' : ''}`}><span className="step-circle">{step > index ? <Check size={14} /> : index + 1}</span><span>{label}</span></div>)}</div>
        {step === 0 && <><ActividadSection value={draft.actividad} onChange={chooseActivity} actividades={actividades} />{!actividades.length && !catalogoError && <p>Cargando actividades…</p>}{catalogoError && <p className="form-error" role="alert">{catalogoError}</p>}<HorarioSection actividad={draft.actividad} fecha={draft.fecha} hora={draft.hora} onFecha={(fecha) => { update({ fecha, hora: '', horarioId: null }); setCuposSeleccionados(null) }} onHora={(turno) => { update({ hora: turno.hora, horarioId: turno.horario_id }); setCuposSeleccionados(turno.cupos_disponibles) }} /></>}
        {step === 1 && info && <ParticipantesSection info={info} cuposDisponibles={cuposSeleccionados} participantes={draft.participantes} mostrarErrores={intento} onChange={(participantes) => update({ participantes })} />}
        {step === 2 && draft.actividad && <TerminosSection actividad={draft.actividad} email={draft.email} mostrarErrores={intento} acepta={draft.aceptaTerminos} terminos={terminos} onEmail={(email) => update({ email })} onAcepta={(aceptaTerminos) => update({ aceptaTerminos })} />}
        {error && <p className="form-error" role="alert">{error}</p>}
        <div className="form-actions">{step > 0 && <button type="button" className="button back" disabled={busy} onClick={() => go(step - 1)}><ArrowLeft size={17} /> Volver</button>}<button type="button" className="button primary" disabled={busy || (step === 0 && !!catalogoError)} onClick={next}>{busy ? step === 1 ? 'Validando…' : 'Confirmando…' : step === 2 ? 'Confirmar reserva' : 'Continuar'} <ArrowRight size={17} /></button></div>
      </> : <ConfirmacionSection reserva={reserva} onNueva={nuevaReserva} onReenviar={async () => setReserva(await reenviarConfirmacion(reserva.id))} />}
    </div>

    {!reserva && <aside className="summary-card" aria-label="Resumen de la reserva">
      <SummaryScene actividad={draft.actividad} />
      <div className="summary-content"><h3>{draft.actividad || 'Tu visita'}</h3><dl>
        <div><dt>Fecha</dt><dd>{draft.fecha ? new Intl.DateTimeFormat('es-AR', { day: 'numeric', month: 'long', timeZone: 'UTC' }).format(new Date(`${draft.fecha}T12:00:00Z`)) : '—'}</dd></div>
        <div><dt>Horario</dt><dd>{draft.hora ? `${draft.hora} h` : '—'}</dd></div>
        <div><dt>Personas</dt><dd>{personasCargadas || '—'}</dd></div>
      </dl></div>
    </aside>}
    {!reserva && <GuiaAssistant step={step} draft={draft} error={error} requiereTalle={info?.requiere_talle ?? false} />}
  </div>
}
