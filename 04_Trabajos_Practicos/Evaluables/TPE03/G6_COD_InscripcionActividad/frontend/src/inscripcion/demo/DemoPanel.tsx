import { useState } from 'react'
import { motivoCierre } from '../horario/calendario'
import { casosParticipantes } from './casos'
import type { CasoParticipantes } from './casos'

const casosCierre = [
  { titulo: 'Lunes cerrado', fecha: '2026-10-26', esperado: 'Cerrado los lunes', test: 'test_no_hay_turnos_los_lunes' },
  { titulo: 'Navidad', fecha: '2026-12-25', esperado: 'Cerrado el 25 de diciembre', test: 'test_no_hay_turnos_el_25_de_diciembre' },
  { titulo: 'Año Nuevo', fecha: '2027-01-01', esperado: 'Cerrado el 1 de enero', test: 'test_no_hay_turnos_el_1_de_enero' },
]

export function DemoPanel({ casoActivo, resultado, onCargar, onSalir }: {
  casoActivo: CasoParticipantes | null
  resultado: string
  onCargar: (caso: CasoParticipantes) => void
  onSalir: () => void
}) {
  const [fechaProbada, setFechaProbada] = useState<string | null>(null)
  const casoFecha = casosCierre.find((caso) => caso.fecha === fechaProbada)
  const resultadoFecha = casoFecha && motivoCierre(casoFecha.fecha)
  return <details className="demo-panel" open={!!casoActivo || undefined}>
    <summary>Modo demostración · casos de prueba</summary>
    <p>Los casos usan la validación del formulario y las reglas de cierre. No ejecutan la suite Python, crean reservas ni envían correos.</p>
    <div className="demo-cases">
      {casosParticipantes.map((caso) => <button key={caso.id} type="button" className={`demo-case ${casoActivo?.id === caso.id ? 'selected' : ''}`} onClick={() => onCargar(caso)}><strong>{caso.titulo}</strong><span>{caso.descripcion}</span><small>Cargar caso</small></button>)}
    </div>
    {casoActivo && <div className="demo-result" role="status"><strong>Esperado:</strong> {casoActivo.esperado}<br /><strong>Obtenido:</strong> {resultado || 'Presioná “Ejecutar validación”.'}{resultado && <span className={resultado === casoActivo.esperado ? 'demo-pass' : 'demo-fail'}>{resultado === casoActivo.esperado ? 'Coincide con lo esperado' : 'El resultado cambió'}</span>}<small>Test relacionado: {casoActivo.test}</small><button type="button" className="demo-exit" onClick={onSalir}>Volver a reserva real</button></div>}
    <div className="demo-dates"><strong>Días de cierre de las FAQ</strong><div className="demo-cases">{casosCierre.map((caso) => <button key={caso.fecha} type="button" className="demo-case" onClick={() => setFechaProbada(caso.fecha)}><strong>{caso.titulo}</strong><span>{caso.fecha}</span><small>Probar cierre</small></button>)}</div>{casoFecha && <p role="status">Esperado: {casoFecha.esperado}. Obtenido: {resultadoFecha || 'Abierto'}. <strong>{resultadoFecha === casoFecha.esperado ? 'Coincide con lo esperado' : 'El resultado cambió'}</strong><small> Test relacionado: {casoFecha.test}</small></p>}</div>
  </details>
}
