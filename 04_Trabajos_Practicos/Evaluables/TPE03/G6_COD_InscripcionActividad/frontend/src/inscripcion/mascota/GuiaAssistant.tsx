import { useEffect, useRef, useState } from 'react'
import { createPortal } from 'react-dom'
import { ArrowUpRight, X } from 'lucide-react'
import type { InscripcionDraft } from '../types'
import { actividadPorId } from '../catalogo'
import waveGif from '../../assets/guia-assistant/wave.gif'
import pointGif from '../../assets/guia-assistant/point.gif'
import thinkGif from '../../assets/guia-assistant/think.gif'
import cheerGif from '../../assets/guia-assistant/cheer.gif'
import wavePng from '../../assets/guia-assistant/wave.png'
import pointPng from '../../assets/guia-assistant/point.png'
import thinkPng from '../../assets/guia-assistant/think.png'
import cheerPng from '../../assets/guia-assistant/cheer.png'

type Motion = 'wave' | 'point' | 'think' | 'cheer'
const animated: Record<Motion, string> = { wave: waveGif, point: pointGif, think: thinkGif, cheer: cheerGif }
const still: Record<Motion, string> = { wave: wavePng, point: pointPng, think: thinkPng, cheer: cheerPng }

function consejo(step: number, draft: InscripcionDraft, error: string): { text: string; target: string; action: string; motion: Motion } {
  if (error) return { text: error, target: '.form-error', action: 'Ver qué falta', motion: 'think' }
  if (step === 0) {
    if (!draft.actividad) return { text: '¡Hola! Soy Guía. Elegí una aventura para comenzar.', target: '.activity-grid', action: 'Ver aventuras', motion: 'wave' }
    if (!draft.fecha) return { text: `¡${draft.actividad} suena genial! Elegí el día de tu visita.`, target: '.date-options', action: 'Elegir día', motion: 'point' }
    if (!draft.hora) return { text: 'Ya tenemos día. Elegí un horario con cupos.', target: '.time-grid', action: 'Ver horarios', motion: 'point' }
    return { text: '¡Aventura elegida! Continuá para armar tu expedición.', target: '.form-actions .primary', action: 'Ir a continuar', motion: 'cheer' }
  }
  if (step === 1) {
    const incomplete = draft.participantes.some((p) => !p.nombre.trim() || !p.dni || !p.edad)
    if (incomplete) return { text: 'Contame quiénes vienen: nombre, DNI y edad de cada persona.', target: '.participant-card .input-field input', action: 'Completar datos', motion: 'point' }
    if (actividadPorId(draft.actividad!)?.requiereTalle && draft.participantes.some((p) => !p.talle_vestimenta)) return { text: 'Para esta actividad también necesito el talle de cada participante.', target: '.participant-card select', action: 'Elegir talles', motion: 'point' }
    return { text: '¡Tu equipo está listo! Continuá con los últimos datos.', target: '.form-actions .primary', action: 'Ir a continuar', motion: 'cheer' }
  }
  if (!draft.email) return { text: '¡Último paso! Escribí tu correo para identificar la reserva.', target: '.email-field input', action: 'Ir al correo', motion: 'think' }
  if (!draft.aceptaTerminos) return { text: 'Leé y aceptá las condiciones de la actividad para confirmar.', target: '.check-line input', action: 'Ver condiciones', motion: 'point' }
  return { text: '¡Todo preparado! Confirmá y nos vemos en el parque.', target: '.form-actions .primary', action: 'Ir a confirmar', motion: 'cheer' }
}

export function GuiaAssistant({ step, draft, error }: { step: number; draft: InscripcionDraft; error: string }) {
  const [open, setOpen] = useState(true)
  const [footerOffset, setFooterOffset] = useState(0)
  const footerWasVisible = useRef(false)
  const hint = consejo(step, draft, error)
  useEffect(() => {
    const updatePosition = () => {
      const footer = document.querySelector('.site-footer')
      const overlap = footer ? Math.max(0, Math.ceil(window.innerHeight - footer.getBoundingClientRect().top)) : 0
      setFooterOffset(overlap)
      if (overlap > 0 && !footerWasVisible.current) setOpen(false)
      footerWasVisible.current = overlap > 0
    }
    updatePosition()
    window.addEventListener('scroll', updatePosition, { passive: true })
    window.addEventListener('resize', updatePosition)
    return () => { window.removeEventListener('scroll', updatePosition); window.removeEventListener('resize', updatePosition) }
  }, [])
  const pointToField = () => {
    const field = document.querySelector<HTMLElement>(hint.target)
    field?.scrollIntoView({ behavior: 'smooth', block: 'center' })
    if (field?.matches('input, select, button')) field.focus({ preventScroll: true })
    else field?.querySelector<HTMLElement>('input, select, button')?.focus({ preventScroll: true })
  }

  return createPortal(<aside className={`guia-assistant ${open ? 'is-open' : 'is-closed'}`} style={{ bottom: footerOffset + (footerOffset > 0 ? 8 : 16) }} aria-label="Ayuda de Guía">
    {open && <div className="guia-tip" key={`${step}-${hint.target}-${hint.text}`}>
      <button className="guia-tip-close" type="button" aria-label="Cerrar ayuda de Guía" onClick={() => setOpen(false)}><X size={16} /></button>
      <strong>CONSEJO DE GUÍA</strong>
      <p aria-live="polite">{hint.text}</p>
      <button type="button" className="guia-tip-action" onClick={pointToField}>{hint.action} <ArrowUpRight size={14} /></button>
    </div>}
    <button type="button" className="guia-assistant-trigger" onClick={() => setOpen((current) => !current)} aria-label={open ? 'Ocultar ayuda de Guía' : 'Abrir ayuda de Guía'} aria-expanded={open}>
      <span className="mini-guia-porthole" aria-hidden="true" />
      <span key={hint.motion} className="mini-guia-stage" role="img" aria-label={`Guía ${hint.motion === 'wave' ? 'saluda' : hint.motion === 'point' ? 'señala' : hint.motion === 'think' ? 'piensa' : 'celebra'}`}>
        <img className={`mini-guia-animated mini-${hint.motion}`} src={animated[hint.motion]} alt="" aria-hidden="true" draggable="false" />
        <img className={`mini-guia-still mini-${hint.motion}`} src={still[hint.motion]} alt="" aria-hidden="true" draggable="false" />
      </span>
    </button>
  </aside>, document.body)
}
