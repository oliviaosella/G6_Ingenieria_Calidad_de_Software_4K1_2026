import { useEffect, useState } from 'react'
import { ArrowRight, Check, Download, Mail } from 'lucide-react'
import QRCode from 'qrcode'
import type { Reserva } from '../types'
import { GuiaMascot } from '../mascota/GuiaMascot'

export function ConfirmacionSection({ reserva, onNueva }: { reserva: Reserva; onNueva: () => void }) {
  const [qr, setQr] = useState('')
  useEffect(() => { QRCode.toDataURL(JSON.stringify({ tipo: 'reserva-demo', id: reserva.id, actividad: reserva.actividad, fecha: reserva.fecha, hora: reserva.hora }), { width: 260, margin: 1, color: { dark: '#153d31', light: '#ffffff' } }).then(setQr) }, [reserva])
  const fecha = new Intl.DateTimeFormat('es-AR', { day: 'numeric', month: 'long', year: 'numeric' }).format(new Date(`${reserva.fecha}T12:00:00`))
  return <section className="success-screen" aria-live="polite"><div className="guia-celebration"><GuiaMascot actividad={reserva.actividad} celebrating /></div><div className="success-seal"><Check size={24} /></div><span className="eyebrow">Reserva confirmada · Demo local</span><h2>¡Nos vemos en el parque!</h2><p>Tu lugar para {reserva.actividad} quedó guardado en este navegador.</p><div className="ticket"><div className="ticket-info"><span className="ticket-label">Tu experiencia</span><strong>{reserva.actividad}</strong><span>{fecha} · {reserva.hora} h</span><span>{reserva.participantes.length} {reserva.participantes.length === 1 ? 'participante' : 'participantes'}</span><span className="ticket-id">Código {reserva.id}</span></div>{qr && <div className="ticket-qr"><img src={qr} alt={`Código QR de la reserva de demostración ${reserva.id}`} /><small>Comprobante de demo</small></div>}</div><div className="success-note"><Mail size={18} /> El correo real se habilitará al conectar el servicio de confirmación.</div><div className="success-actions">{qr && <a className="button secondary" href={qr} download={`eco-harmony-${reserva.id}.png`}><Download size={17} /> Descargar QR</a>}<button type="button" className="button primary" onClick={onNueva}>Nueva reserva <ArrowRight size={18} /></button></div></section>
}

