import type { ActividadId } from '../types'

const colors = {
  Tirolesa: { sky: '#9ADDE4', sun: '#FFD184', far: '#87CBC3', mid: '#4AACA9', front: '#238D92' },
  Safari: { sky: '#ABE1B9', sun: '#FFD577', far: '#9AC98F', mid: '#6CAF75', front: '#428B68' },
  Palestra: { sky: '#F5C7AD', sun: '#FFDA81', far: '#DDB8A7', mid: '#B98B82', front: '#8E646D' },
  Jardinería: { sky: '#FFE5AC', sun: '#FFF09F', far: '#CBD993', mid: '#96C27C', front: '#5B9D74' },
} as const

export function SummaryScene({ actividad }: { actividad: ActividadId | null }) {
  const theme = colors[actividad || 'Jardinería']
  return <svg className="theme-scene summary-illustration" viewBox="0 0 450 300" preserveAspectRatio="xMidYMid slice" role="img" aria-label={`Paisaje de ${actividad || 'Eco Harmony Park'}`}>
    <rect width="450" height="300" fill={theme.sky} />
    <circle cx="358" cy="63" r="35" fill={theme.sun} />
    <path d="M0 178Q100 129 200 169T450 156V300H0Z" fill={theme.far} />
    <path d="M0 215Q125 174 233 203T450 186V300H0Z" fill={theme.mid} />
    <path d="M0 260Q130 216 230 246T450 225V300H0Z" fill={theme.front} />
    <path d="M25 70q18-16 36 0m-20-9q14-19 30 0M385 106q14-12 28 0" fill="none" stroke="#FFF8E8" strokeWidth="10" strokeLinecap="round" opacity=".75" />
    {actividad === 'Tirolesa' && <g stroke="#245D5F" strokeLinecap="round" strokeLinejoin="round">
      <path d="M-10 86Q220 111 460 157" strokeWidth="4" fill="none" /><path d="M-10 94Q220 119 460 165" strokeWidth="2" fill="none" />
      <path d="M55 0v103M400 0v156" strokeWidth="9" /><path d="M172 113v30m35-25v35m35-31v38m35-32v39" strokeWidth="2" />
      <path d="m205 112 10 22h27l11-18" fill="#FFF8E8" strokeWidth="3" /><circle cx="228" cy="135" r="10" fill="#F47B38" strokeWidth="3" />
      <path d="M176 218q24-20 47-1m85 2q27-20 50 0" fill="none" stroke="#D8F0DE" strokeWidth="4" />
    </g>}
    {actividad === 'Safari' && <g>
      <path d="M46 267V128m0 13q-37-30-58-4 36 14 58 4Zm0 0q5-51 42-45-6 37-42 45Zm0 0q37-36 73-12-32 24-73 12ZM399 268V144m0 11q-37-32-61-5 34 18 61 5Zm0 0q2-46 39-42-4 33-39 42Z" fill="#458D65" stroke="#326E54" strokeWidth="7" strokeLinejoin="round" />
      <path d="M144 222q-20-14-45-4l43 31Z" fill="#EFB679" /><ellipse cx="218" cy="217" rx="72" ry="39" fill="#EFB679" />
      <path d="M256 212q14-82 39-102 14-12 27-4l12 11q8 9-2 17l-26 13-16 82Z" fill="#EFB679" /><ellipse cx="324" cy="120" rx="25" ry="17" fill="#EFB679" />
      <circle cx="332" cy="116" r="3.5" fill="#263C34" /><path d="M171 253v25m70-25v25" stroke="#D99B65" strokeWidth="14" strokeLinecap="round" />
      <path d="m171 184 13-18 15 17 14-18 15 17 13-18 16 19" fill="#FFF0B6" />
    </g>}
    {actividad === 'Palestra' && <g strokeLinejoin="round">
      <path d="M55 260 188 71l129 189ZM197 260 329 109l107 151Z" fill="#8D8E79" stroke="#5D6A5B" strokeWidth="3" />
      <path d="m160 110 28-39 31 45-31-13ZM301 140l28-31 24 35-24-12Z" fill="#FFF4E5" />
      <path d="M316 209q22-17 43-3l12-12 21 2 6 18-21 7-4 34h-10l-7-25-28 3-8 23h-10l3-33-11-7Z" fill="#F4D59E" stroke="#9C765E" strokeWidth="3" />
      <path d="m376 196 2-16m10 18 7-14" fill="none" stroke="#9C765E" strokeWidth="4" strokeLinecap="round" />
    </g>}
    {(!actividad || actividad === 'Jardinería') && <g>
      <path d="M92 269V173m83 105V194m167 78V182" stroke="#538D65" strokeWidth="5" strokeLinecap="round" />
      <path d="M92 227q-32-27-47-9 16 24 47 9Zm0-16q25-32 46-16-10 27-46 16Zm83 35q-32-29-47-9 18 24 47 9Zm0-16q25-33 44-16-8 26-44 16Zm167 18q-30-28-48-9 18 23 48 9Zm0-18q29-30 47-12-12 27-47 12Z" fill="#4B9B6C" />
      {[[92,166],[175,188],[342,176]].map(([x,y]) => <g key={x}><circle cx={x} cy={y} r="17" fill="#FFF6D5"/><circle cx={x} cy={y} r="6" fill="#EAA77A"/></g>)}
      <path d="M254 107q-29-29-36 1 3 21 31 14-23 15-8 29 17 6 23-25 6 31 23 25 15-14-8-29 28 7 31-14-7-30-36-1Z" fill="#D6946F" /><path d="M264 108v32" stroke="#875D56" strokeWidth="3" strokeLinecap="round" />
    </g>}
  </svg>
}
