import { useEffect, useRef, useState } from 'react'
import { ArrowLeft, ArrowRight, Check } from 'lucide-react'
import { actividades as actividadesLocales } from './catalogo'
import type { ActividadInfo } from './catalogo'
import { consultarTerminos, listarActividades, reservar } from './api'
import type { TerminosApi } from './api'
import { ActividadSection } from './actividad/ActividadSection'
import { SummaryScene } from './actividad/SummaryScene'
import { ConfirmacionSection } from './confirmacion/ConfirmacionSection'
import { GuiaAssistant } from './mascota/GuiaAssistant'
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
  const [actividades, setActividades] = useState<ActividadInfo[]>([])
  const [catalogoError, setCatalogoError] = useState('')
  const [terminos, setTerminos] = useState<TerminosApi | null>(null)
  const [saving, setSaving] = useState(false)
  const topRef = useRef<HTMLDivElement>(null)
  useEffect(() => {
    let active = true
    listarActividades().then((items) => {
      if (active) setActividades(items.map((item) => ({
        ...actividadesLocales.find((local) => local.id === item.id)!,
        id: item.id, categoria: item.categoria, descripcion: item.descripcion,
        duracion: item.duracion, cupo: item.cupo, edadMinima: item.edad_minima,
        requiereTalle: item.requiere_talle,
      })))
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
  const requiereTalle = draft.actividad ? actividades.find((item) => item.id === draft.actividad)?.requiereTalle : false
  const personasCargadas = draft.participantes.filter((persona) =>
    persona.nombre.trim() && persona.dni.trim() && persona.edad.trim() && (!requiereTalle || persona.talle_vestimenta)
  ).length

  const update = (change: Partial<InscripcionDraft>) => { setDraft((current) => ({ ...current, ...change })); setError('') }
  const scrollTop = () => topRef.current?.scrollIntoView({ behavior: 'smooth', block: 'start' })
  const go = (next: number) => { setStep(next); setError(''); requestAnimationFrame(scrollTop) }
  const chooseActivity = (actividad: ActividadId) => {
    update({ actividad, fecha: '', hora: '', aceptaTerminos: false, participantes: draft.participantes.map((persona) => ({ ...persona, talle_vestimenta: '' })) })
    setTerminos(null)
    onActividadChange(actividad)
  }
  const next = async () => {
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
    if (!terminos) return setError('Esperá a que se carguen las condiciones de la actividad.')
    setSaving(true)
    try { setReserva(await reservar(draft, terminos.version)); onConfirmedChange(true); setError(''); requestAnimationFrame(scrollTop) }
    catch (issue) { setError(issue instanceof Error ? issue.message : 'No se pudo guardar la reserva.') }
    finally { setSaving(false) }
  }

  return <div className={`booking-layout ${reserva ? 'is-confirmed' : ''}`} ref={topRef}>
    <div className="booking-main">
      {!reserva ? <>
        <div className="stepper" aria-label="Progreso de inscripción">{steps.map((label, index) => <div key={label} className={`step-item ${step === index ? 'current' : ''} ${step > index ? 'done' : ''}`}><span className="step-circle">{step > index ? <Check size={14} /> : index + 1}</span><span>{label}</span></div>)}</div>
        {step === 0 && <><ActividadSection value={draft.actividad} onChange={chooseActivity} actividades={actividades} />{!actividades.length && !catalogoError && <p>Cargando actividades…</p>}{catalogoError && <p className="form-error" role="alert">{catalogoError}</p>}<HorarioSection actividad={draft.actividad} fecha={draft.fecha} hora={draft.hora} onFecha={(fecha) => update({ fecha, hora: '' })} onHora={(hora) => update({ hora })} /></>}
        {step === 1 && draft.actividad && <ParticipantesSection actividad={draft.actividad} participantes={draft.participantes} onChange={(participantes) => update({ participantes })} />}
        {step === 2 && draft.actividad && <TerminosSection actividad={draft.actividad} email={draft.email} acepta={draft.aceptaTerminos} terminos={terminos} onEmail={(email) => update({ email })} onAcepta={(aceptaTerminos) => update({ aceptaTerminos })} />}
        {error && <p className="form-error" role="alert">{error}</p>}
        <div className="form-actions">{step > 0 && <button type="button" className="button back" disabled={saving} onClick={() => go(step - 1)}><ArrowLeft size={17} /> Volver</button>}<button type="button" className="button primary" disabled={saving || (step === 0 && !!catalogoError)} onClick={next}>{saving ? 'Confirmando…' : step === 2 ? 'Confirmar reserva' : 'Continuar'} <ArrowRight size={17} /></button></div>
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
