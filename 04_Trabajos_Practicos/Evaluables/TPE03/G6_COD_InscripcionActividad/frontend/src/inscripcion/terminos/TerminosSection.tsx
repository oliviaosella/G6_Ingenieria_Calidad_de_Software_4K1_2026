import { Mail } from 'lucide-react'
import type { ActividadId } from '../types'

export function TerminosSection({ actividad, email, acepta, onEmail, onAcepta }: { actividad: ActividadId; email: string; acepta: boolean; onEmail: (value: string) => void; onAcepta: (value: boolean) => void }) {
  return <section aria-labelledby="terminos-title" className="form-section">
    <div className="section-heading"><h2 id="terminos-title">Confirmación</h2></div>
    <label className="input-field email-field"><span><Mail size={17} /> Correo electrónico</span><input type="email" autoComplete="email" value={email} onChange={(event) => onEmail(event.target.value)} placeholder="tu@email.com" required /><small>El comprobante se muestra en pantalla en esta demo.</small></label>
    <div className="terms-card"><div><strong>Condiciones de {actividad}</strong><p>Presentate 15 minutos antes. La actividad puede reprogramarse por clima o seguridad. Texto de muestra pendiente del PO.</p><label className="check-line"><input type="checkbox" checked={acepta} onChange={(event) => onAcepta(event.target.checked)} /><span>Acepto las condiciones de {actividad}.</span></label></div></div>
  </section>
}
