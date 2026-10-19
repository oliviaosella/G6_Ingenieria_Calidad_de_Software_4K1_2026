import type { ActividadId } from '../types'
import { themeName } from '../catalogo'

export function ThemeScene({ actividad, compact = false, cover = false }: { actividad: ActividadId | null; compact?: boolean; cover?: boolean }) {
  const theme = themeName(actividad)
  return <svg className={`theme-scene theme-${theme} ${compact ? 'compact' : ''}`} viewBox="0 0 600 400" preserveAspectRatio={cover ? 'xMidYMid slice' : 'xMidYMid meet'} role="img" aria-label={`Ilustración de ${actividad || 'Eco Harmony Park'}`}>
    <g className="scene-cloud cloud-one"><ellipse cx="124" cy="76" rx="48" ry="16"/><circle cx="103" cy="65" r="18"/><circle cx="132" cy="58" r="23"/></g>
    <g className="scene-cloud cloud-two"><ellipse cx="526" cy="130" rx="37" ry="12"/><circle cx="515" cy="121" r="15"/><circle cx="536" cy="118" r="17"/></g>
    <circle className="scene-sun" cx="445" cy="93" r="58" />
    <path className="scene-hill-far" d="M0 265Q120 135 250 237T600 205V400H0Z" />
    <path className="scene-hill-mid" d="M0 300Q155 218 300 280T600 235V400H0Z" />
    <path className="scene-hill-front" d="M0 355Q175 278 340 328T600 292V400H0Z" />
    {theme === 'safari' && <g className="scene-safari">
      <path className="scene-vine" d="M86 0q-27 75 0 125M138 0q31 58 5 126M525 0q-21 65-3 128" fill="none" strokeWidth="8" strokeLinecap="round" />
      <path className="scene-leaf" d="M86 75q-35-24-35 10 20 8 35-10Zm56 17q36-22 33 12-25 9-33-12Zm380-18q30-23 30 9-21 11-30-9Z" />
      <path className="scene-palm-trunk" d="M78 369q-5-99 29-175m405 175q-15-95-37-153" fill="none" strokeWidth="13" strokeLinecap="round" />
      <path className="scene-palm-leaf" d="M108 199q-79-50-105 2 70 10 105-2Zm0 0q-18-71-68-64 15 55 68 64Zm0 0q57-70 104-37-49 38-104 37Zm366 15q-60-47-103-12 43 31 103 12Zm0 0q7-70 58-77-5 57-58 77Zm0 0q78-52 120-7-55 26-120 7Z" />
      <g className="scene-animal scene-dino">
        <path d="M290 274q-28-14-61-9l57 38Z" />
        <ellipse cx="342" cy="277" rx="67" ry="36" />
        <path d="M373 267q20-66 43-100 12-16 28-8l12 9q6 8-3 20l-23 13-20 83Z" />
        <ellipse cx="449" cy="173" rx="24" ry="16" />
        <path d="M305 299v36h17l9-35m45 0v35h17l9-37" stroke="#bd7849" strokeWidth="16" strokeLinecap="round" fill="none" />
        <circle cx="456" cy="169" r="3" fill="#293e36" />
        <path d="M302 247l8-17 13 13 14-18 13 17 13-16 12 22" fill="#f6c77d" />
      </g>
      <g className="scene-fireflies"><circle cx="188" cy="162" r="4"/><circle cx="503" cy="242" r="3"/><circle cx="119" cy="248" r="3"/></g>
    </g>}
    {theme === 'tirolesa' && <g className="scene-tirolesa">
      <path d="M15 107Q300 134 585 203" strokeWidth="4" fill="none" />
      <path d="M15 115Q300 142 585 211" strokeWidth="2" fill="none" />
      <path d="M86 0v107m420-107v190" strokeWidth="10" fill="none" />
      <path d="M140 131v36m45-30v37m45-31v40m45-32v43m45-33v44m45-30v43m45-31v44m45-30v40" strokeWidth="2" fill="none" />
      <path d="M202 135q31 14 61 2m42 16q32 13 63 3m35 12q24 15 47 7" strokeWidth="4" fill="none" className="scene-cable-ribbon" />
      <g className="scene-animal scene-bird"><path d="M398 89q-22-24-45-8 21 3 36 26 21-22 46-13-22-19-37-5Z" /></g>
      <g className="scene-animal scene-bird bird-second"><path d="M220 84q-18-20-36-7 17 2 29 21 18-18 37-10-17-16-30-4Z" /></g>
    </g>}
    {theme === 'palestra' && <g className="scene-palestra">
      <path d="M140 310 268 88l130 222ZM282 310 433 129l132 181Z" className="scene-rock" />
      <path d="m242 135 26-47 29 49-29-12ZM407 159l26-30 29 42-29-10Z" className="scene-snow" />
      <g className="scene-animal scene-goat"><path d="M404 220q22-22 52-5l11-16 22 3 8 20-20 7-4 36h-11l-7-27-30 3-9 26h-11l4-34-14-4Z" /><path d="m475 202 3-15m10 17 7-13" strokeWidth="5" strokeLinecap="round" fill="none" /></g>
      <path className="scene-rock-detail" d="m125 302 41-67 28 67m275 2 32-52 27 52" />
    </g>}
    {theme === 'jardineria' && <g className="scene-jardin">
      <path d="M90 310V208m103 108V232m217 86V220m105 82V190" strokeWidth="5" fill="none" />
      <path d="M90 265q-36-38-42-9 14 22 42 9Zm0-21q28-40 45-17-7 28-45 17Zm103 35q-32-36-46-14 14 25 46 14Zm0-22q23-36 45-18-7 30-45 18Zm217 29q-35-36-47-12 17 24 47 12Zm105-52q26-33 42-10-8 25-42 10Z" className="scene-leaf" />
      {[['90','202'],['193','225'],['410','214'],['515','184']].map(([x,y]) => <g key={x}><circle cx={x} cy={y} r="19" className="scene-flower" /><circle cx={x} cy={y} r="7" className="scene-flower-center" /></g>)}
      <g className="scene-animal scene-butterfly"><path d="M313 135q-31-34-39 0 3 24 35 16-25 17-9 32 18 7 25-29 8 36 25 29 16-15-9-32 32 8 35-16-8-34-39 0Z" /><path d="M325 134v34" strokeWidth="4" fill="none" /></g>
      <g className="scene-animal scene-butterfly butterfly-second" transform="translate(-215 88) scale(.6)"><path d="M313 135q-31-34-39 0 3 24 35 16-25 17-9 32 18 7 25-29 8 36 25 29 16-15-9-32 32 8 35-16-8-34-39 0Z"/><path d="M325 134v34" strokeWidth="4" fill="none"/></g>
    </g>}
    {theme === 'parque' && <g className="scene-parque"><path d="M132 320V190m0 15q-90-5-50-80 28-48 65-16 45-46 79 12 39 68-42 82Zm335 116V206m0 14q-83-5-47-72 28-44 59-15 40-38 71 12 34 61-39 76Z" /><g className="scene-animal scene-bird"><path d="M333 117q-22-24-45-8 21 3 36 26 21-22 46-13-22-19-37-5Z" /></g></g>}
  </svg>
}
