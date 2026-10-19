import { Binoculars, Mountain, Sprout, Waypoints } from 'lucide-react'
import { actividades } from '../catalogo'
import type { ActividadId } from '../types'
import { ThemeScene } from './ThemeScene'

const iconos = { zipline: Waypoints, binoculars: Binoculars, mountain: Mountain, sprout: Sprout }

export function ActividadSection({ value, onChange }: { value: ActividadId | null; onChange: (value: ActividadId) => void }) {
  return <section aria-labelledby="actividades-title" className="form-section">
    <div className="section-heading"><h2 id="actividades-title">Actividad</h2></div>
    <div className="activity-grid">
      {actividades.map((actividad) => {
        const Icon = iconos[actividad.icono]
        return <button key={actividad.id} type="button" className={`activity-card ${actividad.color} ${value === actividad.id ? 'selected' : ''}`} aria-pressed={value === actividad.id} onClick={() => onChange(actividad.id)}>
          <span className="activity-image"><ThemeScene actividad={actividad.id} compact cover /></span>
          <span className="activity-top"><span className="activity-icon"><Icon size={23} strokeWidth={1.7} /></span></span>
          {value === actividad.id && <span className="activity-selection-seal" aria-hidden="true"><svg viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg"><circle cx="32" cy="32" r="27" fill="#F47B38" stroke="#263C34" strokeWidth="3"/><circle cx="32" cy="32" r="21" fill="#217B73"/><path className="seal-check" d="m21 32 8 8 15-17" stroke="#FFF8E8" strokeWidth="6" strokeLinecap="round" strokeLinejoin="round"/></svg></span>}
          <strong>{actividad.id}</strong>
          <span className="activity-meta">{actividad.duracion} <span>·</span> {actividad.edadMinima ? `+${actividad.edadMinima} años` : 'Todas las edades'}</span>
        </button>
      })}
    </div>
  </section>
}
