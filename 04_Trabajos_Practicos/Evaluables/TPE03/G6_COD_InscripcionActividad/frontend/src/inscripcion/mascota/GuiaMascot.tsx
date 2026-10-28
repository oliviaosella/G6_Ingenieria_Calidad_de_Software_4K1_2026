import { themeName } from '../catalogo'
import type { ActividadId } from '../types'
import celebrationGif from '../../assets/guia-confirmacion/confirmada.gif'
import celebrationStill from '../../assets/guia-confirmacion/confirmada.png'

const animatedUrls = import.meta.glob<string>('../../assets/guia-gifs/*.webp', { eager: true, query: '?url', import: 'default' })
const stillUrls = import.meta.glob<string>('../../assets/guia-frames/*-0.png', { eager: true, query: '?url', import: 'default' })

export function GuiaMascot({ actividad = null, celebrating = false, className = '' }: { actividad?: ActividadId | null; celebrating?: boolean; className?: string }) {
  const theme = themeName(actividad)
  return <span key={theme} className={`guia-mascot guia-${theme} ${celebrating ? 'celebrating' : ''} ${className}`.trim()} role="img" aria-label={`Guía, el zorro explorador del parque, ${celebrating ? 'celebra tu reserva' : 'saluda y se mueve'}`}>
    <img className="guia-animated" src={celebrating ? celebrationGif : animatedUrls[`../../assets/guia-gifs/${theme}.webp`]} alt="" aria-hidden="true" draggable="false" />
    <img className="guia-still" src={celebrating ? celebrationStill : stillUrls[`../../assets/guia-frames/${theme}-0.png`]} alt="" aria-hidden="true" draggable="false" />
  </span>
}
