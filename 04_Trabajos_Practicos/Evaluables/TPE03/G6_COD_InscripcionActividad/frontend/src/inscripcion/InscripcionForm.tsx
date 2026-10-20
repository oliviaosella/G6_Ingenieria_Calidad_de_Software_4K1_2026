import { useRef, useState } from 'react'
import { ArrowLeft, ArrowRight, Check } from 'lucide-react'
import { actividadPorId } from './catalogo'
import { ActividadSection } from './actividad/ActividadSection'
import { SummaryScene } from './actividad/SummaryScene'
import { ConfirmacionSection } from './confirmacion/ConfirmacionSection'
import { GuiaAssistant } from './mascota/GuiaAssistant'
import { reservar } from './reservas/reservasDemo'
import { HorarioSection } from './horario/HorarioSection'
import { ParticipantesSection } from './participantes/ParticipantesSection'
import { emailSchema, participanteVacio, validarParticipantes } from './schemas'
import { TerminosSection } from './terminos/TerminosSection'
import type { ActividadId, InscripcionDraft, Reserva } from './types'

const initialDraft = (): InscripcionDraft => ({ actividad: null, fecha: '', hora: '', participantes: [participanteVacio()], email: '', aceptaTerminos: false })
const steps = ['Actividad', 'Participantes', 'Confirmar']

export function InscripcionForm({ onActividadChange, onConfirmedChange }: { onActividadChange: (actividad: ActividadId | null) => void; onConfirmedChange: (confirmed: boolean) => void }) {
  const [draft, setDraft] = useState(initialDraft)
  const [step, setStep] = useState(0)
  const [error, setError] = useState('')
  const [reserva, setReserva] = useState<Reserva | null>(null)
  const topRef = useRef<HTMLDivElement>(null)
  const requiereTalle = draft.actividad ? actividadPorId(draft.actividad)?.requiereTalle : false
  const personasCargadas = draft.participantes.filter((persona) =>
    persona.nombre.trim() && persona.dni.trim() && persona.edad.trim() && (!requiereTalle || persona.talle_vestimenta)
  ).length

  const update = (change: Partial<InscripcionDraft>) => { setDraft((current) => ({ ...current, ...change })); setError('') }
  const scrollTop = () => topRef.current?.scrollIntoView({ behavior: 'smooth', block: 'start' })
  const go = (next: number) => { setStep(next); setError(''); requestAnimationFrame(scrollTop) }
  const chooseActivity = (actividad: ActividadId) => {
    update({ actividad, fecha: '', hora: '', aceptaTerminos: false, participantes: draft.participantes.map((persona) => ({ ...persona, talle_vestimenta: '' })) })
    onActividadChange(actividad)
  }
  const next = () => {
    if (step === 0) {
      if (!draft.actividad || !draft.fecha || !draft.hora) return setError('Elegí una actividad, una fecha y un horario disponible.')
      return go(1)
    }
    if (step === 1) {
      const issue = validarParticipantes(draft.participantes, draft.actividad!)
      if (issue) return setError(issue)
      return go(2)
    }
    const email = emailSchema.safeParse(draft.email)
    if (!email.success) return setError(email.error.issues[0].message)
    if (!draft.aceptaTerminos) return setError('Aceptá las condiciones de la actividad para confirmar.')
    try { setReserva(reservar(draft)); onConfirmedChange(true); setError(''); requestAnimationFrame(scrollTop) }
    catch (issue) { setError(issue instanceof Error ? issue.message : 'No se pudo guardar la reserva.') }
  }

  return <div className={`booking-layout ${reserva ? 'is-confirmed' : ''}`} ref={topRef}>
    <div className="booking-main">
      {!reserva ? <>
        <div className="stepper" aria-label="Progreso de inscripción">{steps.map((label, index) => <div key={label} className={`step-item ${step === index ? 'current' : ''} ${step > index ? 'done' : ''}`}><span className="step-circle">{step > index ? <Check size={14} /> : index + 1}</span><span>{label}</span></div>)}</div>
        {step === 0 && <><ActividadSection value={draft.actividad} onChange={chooseActivity} /><HorarioSection actividad={draft.actividad} fecha={draft.fecha} hora={draft.hora} onFecha={(fecha) => update({ fecha, hora: '' })} onHora={(hora) => update({ hora })} /></>}
        {step === 1 && draft.actividad && <ParticipantesSection actividad={draft.actividad} participantes={draft.participantes} onChange={(participantes) => update({ participantes })} />}
        {step === 2 && draft.actividad && <TerminosSection actividad={draft.actividad} email={draft.email} acepta={draft.aceptaTerminos} onEmail={(email) => update({ email })} onAcepta={(aceptaTerminos) => update({ aceptaTerminos })} />}
        {error && <p className="form-error" role="alert">{error}</p>}
        <div className="form-actions">{step > 0 && <button type="button" className="button back" onClick={() => go(step - 1)}><ArrowLeft size={17} /> Volver</button>}<button type="button" className="button primary" onClick={next}>{step === 2 ? 'Confirmar reserva' : 'Continuar'} <ArrowRight size={17} /></button></div>
      </> : <ConfirmacionSection reserva={reserva} onNueva={() => { setDraft(initialDraft()); setReserva(null); onActividadChange(null); onConfirmedChange(false); go(0) }} />}
    </div>

    {!reserva && <aside className="summary-card" aria-label="Resumen de la reserva">
      <SummaryScene actividad={draft.actividad} />
      <div className="summary-content"><h3>{draft.actividad || 'Tu visita'}</h3><dl>
        <div><dt>Fecha</dt><dd>{draft.fecha ? new Intl.DateTimeFormat('es-AR', { day: 'numeric', month: 'long' }).format(new Date(`${draft.fecha}T12:00:00`)) : '—'}</dd></div>
        <div><dt>Horario</dt><dd>{draft.hora ? `${draft.hora} h` : '—'}</dd></div>
        <div><dt>Personas</dt><dd>{personasCargadas || '—'}</dd></div>
      </dl></div>
    </aside>}
    {!reserva && <GuiaAssistant step={step} draft={draft} error={error} />}
  </div>
}
