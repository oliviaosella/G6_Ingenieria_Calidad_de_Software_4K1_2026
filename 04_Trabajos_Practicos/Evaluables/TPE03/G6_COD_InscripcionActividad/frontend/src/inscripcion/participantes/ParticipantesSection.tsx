import { useState } from 'react'
import { Plus, Trash2 } from 'lucide-react'
import type { ActividadInfo } from '../catalogo'
import { participanteVacio } from '../draft'
import type { Participante } from '../types'
import { erroresDe, filtrarDni, filtrarEdad, filtrarNombre } from '../validaciones'
import type { ErroresParticipante } from '../validaciones'
import { ExpeditionGroup } from './ExpeditionGroup'

// Reinicia la animación aunque se rechace otro carácter mientras el campo todavía tiembla.
const sacudir = (campo: HTMLElement) => {
  campo.classList.remove('shake')
  void campo.offsetWidth
  campo.classList.add('shake')
}

const filtros: Partial<Record<keyof Participante, (value: string) => string>> = { nombre: filtrarNombre, dni: filtrarDni, edad: filtrarEdad }

export function ParticipantesSection({ info, cuposDisponibles, participantes, mostrarErrores, onChange }: { info: ActividadInfo; cuposDisponibles: number | null; participantes: Participante[]; mostrarErrores: boolean; onChange: (value: Participante[]) => void }) {
  const limite = Math.min(info.cupo, cuposDisponibles ?? info.cupo)
  const [tocados, setTocados] = useState<Set<string>>(new Set())
  const update = (index: number, key: keyof Participante, value: string, campo?: HTMLElement) => {
    const filtrado = filtros[key]?.(value) ?? value
    if (campo && filtrado !== value) sacudir(campo)
    onChange(participantes.map((persona, i) => i === index ? { ...persona, [key]: filtrado } : persona))
  }
  const tocar = (index: number, key: keyof ErroresParticipante) => setTocados((actuales) => new Set(actuales).add(`${index}.${key}`))
  const visible = (index: number, key: keyof ErroresParticipante, errores: ErroresParticipante) => {
    const mensaje = errores[key]
    // El DNI repetido se avisa apenas se completa, sin esperar a salir del campo.
    const cruzado = key === 'dni' && mensaje?.startsWith('Este DNI')
    return mostrarErrores || cruzado || tocados.has(`${index}.${key}`) ? mensaje : undefined
  }
  const quitar = (index: number) => { setTocados(new Set()); onChange(participantes.filter((_, i) => i !== index)) }
  return <section aria-labelledby="participantes-title" className="form-section">
    <div className="section-heading"><h2 id="participantes-title">Participantes</h2><p>Hasta {limite} personas en el turno{info.edad_minima ? ` · edad mínima ${info.edad_minima} años` : ''}. Los cupos se vuelven a verificar al continuar.</p></div>
    <div className="participant-list">{participantes.map((persona, index) => {
      const errores = erroresDe(participantes, index, info)
      const errorNombre = visible(index, 'nombre', errores)
      const errorDni = visible(index, 'dni', errores)
      const errorEdad = visible(index, 'edad', errores)
      const errorTalle = visible(index, 'talle', errores)
      return <div className="participant-card" key={index}>
        <div className="participant-title"><span className="number-badge">{String(index + 1).padStart(2, '0')}</span><h3>Participante {index + 1}</h3>{participantes.length > 1 && <button type="button" className="icon-button remove" aria-label={`Quitar participante ${index + 1}`} onClick={() => quitar(index)}><Trash2 size={17} /></button>}</div>
        <div className="input-grid">
          <label className="input-field span-two">Nombre y apellido<input autoComplete="name" value={persona.nombre} onChange={(event) => update(index, 'nombre', event.target.value, event.target)} onBlur={() => tocar(index, 'nombre')} placeholder="Ej. Ana García" aria-invalid={!!errorNombre} required />{errorNombre && <small className="field-error" role="alert">{errorNombre}</small>}</label>
          <label className="input-field">DNI<input inputMode="numeric" value={persona.dni} onChange={(event) => update(index, 'dni', event.target.value, event.target)} onBlur={() => tocar(index, 'dni')} placeholder="Sin puntos" aria-invalid={!!errorDni} required />{errorDni && <small className="field-error" role="alert">{errorDni}</small>}</label>
          <label className="input-field">Edad<input inputMode="numeric" value={persona.edad} onChange={(event) => update(index, 'edad', event.target.value, event.target)} onBlur={() => tocar(index, 'edad')} placeholder="Años" aria-invalid={!!errorEdad} required />{errorEdad && <small className="field-error" role="alert">{errorEdad}</small>}</label>
          <label className="input-field span-two">Talle de vestimenta<select value={info.requiere_talle ? persona.talle_vestimenta : ''} onChange={(event) => update(index, 'talle_vestimenta', event.target.value)} onBlur={() => tocar(index, 'talle')} aria-invalid={!!errorTalle} required={info.requiere_talle} disabled={!info.requiere_talle}><option value="">{info.requiere_talle ? 'Seleccionar talle' : 'No requerido para esta actividad'}</option>{info.talles_disponibles.map((talle) => <option key={talle} value={talle}>{talle}</option>)}</select>{errorTalle ? <small className="field-error" role="alert">{errorTalle}</small> : <small>{info.requiere_talle ? 'Talle requerido por esta actividad.' : 'Esta actividad no necesita talle.'}</small>}</label>
        </div>
      </div>
    })}</div>
    <div className="participant-footer"><span>{participantes.length} {participantes.length === 1 ? 'visitante' : 'visitantes'}{participantes.length >= limite && ` · alcanzaste el máximo de ${limite} personas`}</span><button type="button" className="add-button" disabled={participantes.length >= limite} onClick={() => onChange([...participantes, participanteVacio()])}><Plus size={18} /> Agregar participante</button></div>
    <ExpeditionGroup participantes={participantes} />
  </section>
}
