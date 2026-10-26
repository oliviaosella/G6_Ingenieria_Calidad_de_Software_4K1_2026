import { Plus, Trash2 } from 'lucide-react'
import type { ActividadInfo } from '../catalogo'
import { participanteVacio } from '../schemas'
import type { Participante } from '../types'
import { ExpeditionGroup } from './ExpeditionGroup'

export function ParticipantesSection({ info, cuposDisponibles, participantes, onChange }: { info: ActividadInfo; cuposDisponibles: number | null; participantes: Participante[]; onChange: (value: Participante[]) => void }) {
  const limite = Math.min(info.cupo, cuposDisponibles ?? info.cupo)
  const update = (index: number, key: keyof Participante, value: string) => onChange(participantes.map((persona, i) => i === index ? { ...persona, [key]: value } : persona))
  return <section aria-labelledby="participantes-title" className="form-section">
    <div className="section-heading"><h2 id="participantes-title">Participantes</h2><p>Hasta {limite} personas en el turno{info.edadMinima ? ` · edad mínima ${info.edadMinima} años` : ''}. Los cupos se vuelven a verificar al continuar.</p></div>
    <div className="participant-list">{participantes.map((persona, index) => <div className="participant-card" key={index}>
      <div className="participant-title"><span className="number-badge">{String(index + 1).padStart(2, '0')}</span><h3>Participante {index + 1}</h3>{participantes.length > 1 && <button type="button" className="icon-button remove" aria-label={`Quitar participante ${index + 1}`} onClick={() => onChange(participantes.filter((_, i) => i !== index))}><Trash2 size={17} /></button>}</div>
      <div className="input-grid"><label className="input-field span-two">Nombre y apellido<input autoComplete="name" value={persona.nombre} onChange={(event) => update(index, 'nombre', event.target.value)} placeholder="Ej. Ana García" required /></label><label className="input-field">DNI<input inputMode="numeric" value={persona.dni} onChange={(event) => update(index, 'dni', event.target.value.replace(/\D/g, ''))} placeholder="Sin puntos" required /></label><label className="input-field">Edad<input inputMode="numeric" value={persona.edad} onChange={(event) => update(index, 'edad', event.target.value.replace(/\D/g, ''))} placeholder="Años" required /></label><label className="input-field span-two">Talle de vestimenta<select value={info.requiereTalle ? persona.talle_vestimenta : ''} onChange={(event) => update(index, 'talle_vestimenta', event.target.value)} required={info.requiereTalle} disabled={!info.requiereTalle}><option value="">{info.requiereTalle ? 'Seleccionar talle' : 'No requerido para esta actividad'}</option>{['XS', 'S', 'M', 'L', 'XL', 'XXL'].map((talle) => <option key={talle} value={talle}>{talle}</option>)}</select><small>{info.requiereTalle ? 'Necesario para el equipamiento de seguridad.' : 'Esta actividad no necesita talle.'}</small></label></div>
    </div>)}</div>
    <div className="participant-footer"><span>{participantes.length} {participantes.length === 1 ? 'visitante' : 'visitantes'}</span><button type="button" className="add-button" disabled={participantes.length >= limite} onClick={() => onChange([...participantes, participanteVacio()])}><Plus size={18} /> Agregar participante</button></div>
    <ExpeditionGroup participantes={participantes} />
  </section>
}
