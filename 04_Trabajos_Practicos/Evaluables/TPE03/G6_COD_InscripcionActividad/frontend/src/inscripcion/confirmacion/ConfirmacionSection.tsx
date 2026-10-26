import { useState } from 'react'
import { ArrowRight, Check, Download, Mail, RefreshCw } from 'lucide-react'
import type { Reserva } from '../types'
import { GuiaMascot } from '../mascota/GuiaMascot'
import { ConfirmacionScene } from './ConfirmacionScene'

export function ConfirmacionSection({ reserva, onNueva, onReenviar }: { reserva: Reserva; onNueva: () => void; onReenviar: () => Promise<void> }) {
  const [reenviando, setReenviando] = useState(false)
  const [error, setError] = useState('')
  const fecha = new Intl.DateTimeFormat('es-AR', { day: 'numeric', month: 'long', year: 'numeric', timeZone: 'UTC' }).format(new Date(`${reserva.fecha}T12:00:00Z`))
  const mensajeCorreo = reserva.correoEstado === 'enviado'
    ? 'El servidor de correo aceptó el comprobante. Revisá tu bandeja de entrada.'
    : reserva.correoEstado === 'fallido'
      ? 'El correo no pudo enviarse. Tu reserva sigue confirmada y podés descargar el QR.'
      : 'El envío del correo está pendiente. Tu reserva ya está confirmada.'

  const reintentar = async () => {
    setReenviando(true)
    setError('')
    try { await onReenviar() }
    catch (problem) { setError(problem instanceof Error ? problem.message : 'No se pudo reintentar el correo.') }
    finally { setReenviando(false) }
  }

  return <section className="success-screen" aria-live="polite">
    <div className="guia-celebration"><div className="success-landscape" aria-hidden="true"><ConfirmacionScene /></div><GuiaMascot actividad={reserva.actividad} celebrating /></div>
    <div className="success-seal"><Check size={24} /></div>
    <span className="eyebrow">Reserva confirmada</span><h2>¡Nos vemos en el parque!</h2><p>Tu lugar para {reserva.actividad} quedó reservado.</p>
    <div className="ticket"><div className="ticket-info"><span className="ticket-label">Tu experiencia</span><strong>{reserva.actividad}</strong><span>{fecha} · {reserva.hora} h</span><span>{reserva.participantes.length} {reserva.participantes.length === 1 ? 'participante' : 'participantes'}</span><span className="ticket-id">Código {reserva.id}</span></div><div className="ticket-qr"><img src={reserva.qrUrl} alt={`Código QR de la reserva ${reserva.id}`} /><small>Comprobante de reserva</small></div></div>
    <div className="success-note"><Mail size={18} /> {mensajeCorreo}</div>
    {error && <p className="form-error" role="alert">{error}</p>}
    <div className="success-actions">
      <a className="button secondary" href={reserva.qrUrl} download={`eco-harmony-${reserva.id}.png`}><Download size={17} /> Descargar QR</a>
      {reserva.correoEstado === 'fallido' && <button type="button" className="button secondary" disabled={reenviando} onClick={reintentar}><RefreshCw size={17} /> {reenviando ? 'Reintentando…' : 'Reintentar correo'}</button>}
      <button type="button" className="button primary" onClick={onNueva}>Nueva reserva <ArrowRight size={18} /></button>
    </div>
  </section>
}
