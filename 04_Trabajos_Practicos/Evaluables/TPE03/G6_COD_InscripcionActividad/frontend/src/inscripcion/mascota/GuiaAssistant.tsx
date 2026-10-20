import { useEffect, useRef, useState, type CSSProperties, type PointerEvent as ReactPointerEvent } from 'react'
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
const sidePosition = (x: number, width: number) => {
  const inset = window.innerWidth <= 650 ? 24 : 36
  return x + width / 2 < window.innerWidth / 2
    ? inset
    : window.innerWidth - width - inset
}
const minimumTop = (open: boolean) => {
  const headerBottom = Math.max(0, document.querySelector('.site-header')?.getBoundingClientRect().bottom ?? 0)
  const tipHeight = open ? (document.querySelector('.guia-tip')?.getBoundingClientRect().height ?? 130) : 0
  return headerBottom + tipHeight + (open ? 32 : 24)
}

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
  const [position, setPosition] = useState<{ left: number; top: number } | null>(null)
  const drag = useRef<{ pointerId: number; startX: number; startY: number; left: number; top: number; moved: boolean } | null>(null)
  const ignoreClick = useRef(false)
  const hint = consejo(step, draft, error)
  useEffect(() => {
    const updatePosition = () => {
      const footer = document.querySelector('.site-footer')
      const overlap = footer ? Math.max(0, Math.ceil(window.innerHeight - footer.getBoundingClientRect().top)) : 0
      setFooterOffset(overlap)
      const triggerSize = open ? (window.innerWidth <= 650 ? 82 : 98) : 72
      setPosition((current) => current && ({ left: sidePosition(current.left, triggerSize), top: Math.max(minimumTop(open), Math.min(current.top, window.innerHeight - overlap - triggerSize - 8)) }))
    }
    updatePosition()
    window.addEventListener('scroll', updatePosition, { passive: true })
    window.addEventListener('resize', updatePosition)
    return () => { window.removeEventListener('scroll', updatePosition); window.removeEventListener('resize', updatePosition) }
  }, [open])
  const pointToField = () => {
    const field = document.querySelector<HTMLElement>(hint.target)
    field?.scrollIntoView({ behavior: 'smooth', block: 'center' })
    if (field?.matches('input, select, button')) field.focus({ preventScroll: true })
    else field?.querySelector<HTMLElement>('input, select, button')?.focus({ preventScroll: true })
  }

  const startDrag = (event: ReactPointerEvent<HTMLButtonElement>) => {
    if (event.pointerType === 'mouse' && event.button !== 0) return
    const rect = event.currentTarget.getBoundingClientRect()
    drag.current = { pointerId: event.pointerId, startX: event.clientX, startY: event.clientY, left: rect.left, top: rect.top, moved: false }
    event.currentTarget.setPointerCapture(event.pointerId)
  }
  const moveDrag = (event: ReactPointerEvent<HTMLButtonElement>) => {
    const current = drag.current
    if (!current || current.pointerId !== event.pointerId) return
    const dx = event.clientX - current.startX
    const dy = event.clientY - current.startY
    if (Math.abs(dx) + Math.abs(dy) < 5 && !current.moved) return
    current.moved = true
    event.preventDefault()
    const size = event.currentTarget.getBoundingClientRect()
    setPosition({
      left: sidePosition(current.left + dx, size.width),
      top: Math.max(minimumTop(open), Math.min(current.top + dy, window.innerHeight - footerOffset - size.height - 8)),
    })
  }
  const endDrag = (event: ReactPointerEvent<HTMLButtonElement>) => {
    if (drag.current?.pointerId !== event.pointerId) return
    ignoreClick.current = drag.current.moved
    drag.current = null
    if (event.currentTarget.hasPointerCapture(event.pointerId)) event.currentTarget.releasePointerCapture(event.pointerId)
  }

  const mobile = typeof window !== 'undefined' && window.innerWidth <= 650
  const tipWidth = mobile ? 198 : 247
  const triggerWidth = open ? (mobile ? 82 : 98) : 72
  const isLeft = position ? position.left + triggerWidth / 2 < window.innerWidth / 2 : mobile && open && footerOffset > 0
  const tipX = position && Math.max(8, Math.min(position.left + triggerWidth - (mobile ? 48 : 61) - tipWidth, window.innerWidth - tipWidth - 8))
  const tipLeft = position && tipX! - position.left
  const tipTail = position && Math.max(18, Math.min(position.left + triggerWidth / 2 - tipX! - 10, tipWidth - 38))
  const assistantStyle = position
    ? { left: position.left, top: position.top, right: 'auto', bottom: 'auto', '--tip-left': `${tipLeft}px`, '--tip-tail': `${tipTail}px` } as CSSProperties
    : { bottom: footerOffset + (footerOffset > 0 ? 8 : 16) }

  return createPortal(<aside className={`guia-assistant ${open ? 'is-open' : 'is-closed'} ${footerOffset > 0 ? 'near-footer' : ''} ${position ? 'is-dragged' : ''} ${isLeft ? 'is-left' : ''}`} style={assistantStyle} aria-label="Ayuda de Guía">
    {open && <div className="guia-tip" key={`${step}-${hint.target}-${hint.text}`}>
      <button className="guia-tip-close" type="button" aria-label="Cerrar ayuda de Guía" onClick={() => setOpen(false)}><X size={16} /></button>
      <strong>CONSEJO DE GUÍA</strong>
      <p aria-live="polite">{hint.text}</p>
      <button type="button" className="guia-tip-action" onClick={pointToField}>{hint.action} <ArrowUpRight size={14} /></button>
    </div>}
    <button type="button" className="guia-assistant-trigger" onPointerDown={startDrag} onPointerMove={moveDrag} onPointerUp={endDrag} onPointerCancel={endDrag} onClick={() => { if (ignoreClick.current) { ignoreClick.current = false; return } setOpen((current) => !current) }} aria-label={open ? 'Ocultar ayuda de Guía' : 'Abrir ayuda de Guía'} aria-expanded={open} title="Arrastrá para mover a Guía">
      <span className="mini-guia-porthole" aria-hidden="true" />
      <span key={hint.motion} className="mini-guia-stage" role="img" aria-label={`Guía ${hint.motion === 'wave' ? 'saluda' : hint.motion === 'point' ? 'señala' : hint.motion === 'think' ? 'piensa' : 'celebra'}`}>
        <img className={`mini-guia-animated mini-${hint.motion}`} src={animated[hint.motion]} alt="" aria-hidden="true" draggable="false" />
        <img className={`mini-guia-still mini-${hint.motion}`} src={still[hint.motion]} alt="" aria-hidden="true" draggable="false" />
      </span>
    </button>
  </aside>, document.body)
}
