import { useState } from 'react'
import { ArrowRight, Flower2, Footprints, Leaf, Sparkles } from 'lucide-react'
import logo from './assets/eco-harmony-logo.svg'
import { InscripcionForm } from './inscripcion/InscripcionForm'
import { ThemeScene } from './inscripcion/actividad/ThemeScene'
import { themeName } from './inscripcion/catalogo'
import { GuiaMascot } from './inscripcion/mascota/GuiaMascot'
import type { ActividadId } from './inscripcion/types'

function FloatingMotifs({ area }: { area: 'hero' | 'booking' }) {
  return <div className={`floating-motifs motifs-${area}`} aria-hidden="true">
    <span className="motif motif-leaf"><Leaf /></span>
    <span className="motif motif-flower"><Flower2 /></span>
    <span className="motif motif-tracks"><Footprints /></span>
    <span className="motif motif-spark"><Sparkles /></span>
    <span className="motif motif-e"><img src={logo} alt="" /></span>
  </div>
}

export default function App() {
  const [actividad, setActividad] = useState<ActividadId | null>(null)
  const [confirmed, setConfirmed] = useState(false)

  return <div className="park-app" data-theme={themeName(actividad)}>
    <header className="site-header">
      <div className="shell header-inner">
        <a className="brand" href="#inicio" aria-label="Eco Harmony Park, inicio"><img src={logo} alt="" /><span><strong>eco<span>harmony</span></strong><small>PARK · EXPERIENCIAS NATURALES</small></span></a>
        <a className="header-cta" href="#inscripcion">{confirmed ? 'Tu comprobante' : 'Reservar'} <ArrowRight size={17} /></a>
      </div>
    </header>

    <main id="inicio">
      {!confirmed && <section className="hero">
        <FloatingMotifs area="hero" />
        <div className="shell hero-inner">
          <div className="hero-copy">
            <span className="eyebrow">ECO HARMONY PARK</span>
            <h1>Una aventura<br /><em>al aire libre.</em></h1>
            <p>Elegí tu actividad y reservá tu lugar en el parque.</p>
            <a className="button hero-button" href="#inscripcion">Explorar actividades <ArrowRight size={18} /></a>
          </div>
          <div className="hero-art"><div className="hero-art-frame"><ThemeScene actividad={actividad} cover /></div><GuiaMascot actividad={actividad} className="hero-guia" /></div>
        </div>
      </section>}

      <section id="inscripcion" className={`booking-section ${confirmed ? 'is-confirmed' : ''}`}>
        <FloatingMotifs area="booking" />
        <div className="shell">
          {!confirmed && <div className="booking-intro"><div><span className="eyebrow">TU VISITA</span><h2>Elegí tu próxima experiencia.</h2></div><img className="brand-stamp" src={logo} alt="" aria-hidden="true" /></div>}
          <InscripcionForm onActividadChange={setActividad} onConfirmedChange={setConfirmed} />
        </div>
      </section>
    </main>

    <footer className="site-footer"><div className="shell footer-main"><span>© 2026 Eco Harmony Park · Proyecto académico</span><a href="#inicio">Volver arriba ↑</a></div></footer>
  </div>
}
