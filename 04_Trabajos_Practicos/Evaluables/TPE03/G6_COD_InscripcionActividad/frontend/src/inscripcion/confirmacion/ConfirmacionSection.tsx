import { ArrowRight, Check, Download, Mail } from 'lucide-react'
import type { Reserva } from '../types'
import { GuiaMascot } from '../mascota/GuiaMascot'
import { ConfirmacionScene } from './ConfirmacionScene'

export function ConfirmacionSection({ reserva, onNueva }: { reserva: Reserva; onNueva: () => void }) {
  const fecha = new Intl.DateTimeFormat('es-AR', { day: 'numeric', month: 'long', year: 'numeric' }).format(new Date(`${reserva.fecha}T12:00:00`))
  return <section className="success-screen" aria-live="polite"><div className="guia-celebration"><div className="success-landscape" aria-hidden="true"><ConfirmacionScene /></div><GuiaMascot actividad={reserva.actividad} celebrating /></div><div className="success-seal"><Check size={24} /></div><span className="eyebrow">Reserva confirmada</span><h2>¡Nos vemos en el parque!</h2><p>Tu lugar para {reserva.actividad} quedó reservado.</p><div className="ticket"><div className="ticket-info"><span className="ticket-label">Tu experiencia</span><strong>{reserva.actividad}</strong><span>{fecha} · {reserva.hora} h</span><span>{reserva.participantes.length} {reserva.participantes.length === 1 ? 'participante' : 'participantes'}</span><span className="ticket-id">Código {reserva.id}</span></div><div className="ticket-qr"><img src={reserva.qrUrl} alt={`Código QR de la reserva ${reserva.id}`} /><small>Comprobante de reserva</small></div></div><div className="success-note"><Mail size={18} /> {reserva.correoEstado === 'enviado' ? 'Comprobante enviado por correo.' : 'No se pudo enviar el correo. Descargá tu comprobante.'}</div><div className="success-actions"><a className="button secondary" href={reserva.qrUrl} download={`eco-harmony-${reserva.id}.png`}><Download size={17} /> Descargar QR</a><button type="button" className="button primary" onClick={onNueva}>Nueva reserva <ArrowRight size={18} /></button></div></section>
}

