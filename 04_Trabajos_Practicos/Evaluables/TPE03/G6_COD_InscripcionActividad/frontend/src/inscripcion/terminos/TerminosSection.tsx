import { useState } from 'react'
import { Mail } from 'lucide-react'
import type { ActividadId } from '../types'
import type { TerminosApi } from '../api'
import { validarEmail } from '../validaciones'

export function TerminosSection({ actividad, email, mostrarErrores, acepta, terminos, onEmail, onAcepta }: { actividad: ActividadId; email: string; mostrarErrores: boolean; acepta: boolean; terminos: TerminosApi | null; onEmail: (value: string) => void; onAcepta: (value: boolean) => void }) {
  const [tocado, setTocado] = useState(false)
  const errorEmail = mostrarErrores || tocado ? validarEmail(email) : null
  return <section aria-labelledby="terminos-title" className="form-section">
    <div className="section-heading"><h2 id="terminos-title">Confirmación</h2></div>
    <label className="input-field email-field"><span><Mail size={17} /> Correo electrónico</span><input type="email" autoComplete="email" value={email} onChange={(event) => onEmail(event.target.value)} onBlur={() => setTocado(true)} aria-invalid={!!errorEmail} placeholder="tu@email.com" required />{errorEmail ? <small className="field-error" role="alert">{errorEmail}</small> : <small>Te enviaremos el comprobante por correo.</small>}</label>
    <div className="terms-card"><div><strong>Condiciones de {actividad}</strong><p style={{ whiteSpace: 'pre-line' }}>{terminos?.texto || 'Cargando condiciones…'}</p>{terminos?.pendiente_aprobacion && <small>Texto pendiente de aprobación.</small>}<label className="check-line"><input type="checkbox" checked={acepta} disabled={!terminos} onChange={(event) => onAcepta(event.target.checked)} /><span>Acepto las condiciones de {actividad}.</span></label></div></div>
  </section>
}
