import type { Participante } from '../types'

const ink = '#263c34'
const explorers = [
  { skin: '#dca078', hair: '#382c2b', cap: '#15968e', bill: '#ef803e', shirt: '#f39a56', scarf: '#117e79', cheek: '#e46e65' },
  { skin: '#a96648', hair: '#272421', cap: '#f29150', bill: '#278f87', shirt: '#78aa70', scarf: '#f4c15a', cheek: '#d96c58' },
  { skin: '#efbf96', hair: '#55352e', cap: '#80a96b', bill: '#f28a4a', shirt: '#52a7a1', scarf: '#f6bd61', cheek: '#e78373' },
  { skin: '#8e583f', hair: '#242521', cap: '#f1b75d', bill: '#188b86', shirt: '#e97f62', scarf: '#4ba69c', cheek: '#cc665b' },
  { skin: '#c88c68', hair: '#352a27', cap: '#3a9b91', bill: '#f2a858', shirt: '#b3ba69', scarf: '#eb7f55', cheek: '#e27f66' },
]

function ExplorerAvatar({ index }: { index: number }) {
  const c = explorers[index % explorers.length]
  const grin = index % 2 === 0

  return <svg viewBox="0 0 110 120" role="img" aria-label={`Explorador ${index + 1} con gorra y pañuelo`}>
    <path d="M7 115q1-27 20-41 11-7 28-7 19 0 31 9 15 12 17 39Z" fill={c.shirt} stroke={ink} strokeWidth="4" strokeLinejoin="round" />
    <path d="M11 112q6-24 20-28m68 28Q94 91 79 84" fill="none" stroke="#fff1cc" strokeWidth="3" strokeLinecap="round" opacity=".6" />
    <path d="M44 67v14q11 12 22 0V67Z" fill={c.skin} stroke={ink} strokeWidth="3" />
    <path d="M39 79q16 14 32 0l-16 22Z" fill={c.scarf} stroke={ink} strokeWidth="3" strokeLinejoin="round" />
    <path d="M56 95q4 10-2 19" fill="none" stroke={ink} strokeWidth="3" strokeLinecap="round" />
    <path d="M30 49q-5-31 25-34 29 0 26 35l3 27-16 5-31-3-12-5Z" fill={c.hair} stroke={ink} strokeWidth="4" strokeLinejoin="round" />
    <path d="M29 49q-6-4-8 3-1 9 8 13m52-16q6-4 8 3 1 9-8 13" fill={c.skin} stroke={ink} strokeWidth="3" />
    <path d="M29 42q0-24 26-25 26 1 26 25v23q-3 24-26 25-23-1-26-25Z" fill={c.skin} stroke={ink} strokeWidth="4" />
    <path d="M30 48q5-18 23-18 8 10 28 12-6-23-27-25-20 1-24 31Z" fill={c.hair} stroke={ink} strokeWidth="3" />
    <ellipse cx="42" cy="61" rx="4.2" ry="5.2" fill={ink} /><ellipse cx="67" cy="61" rx="4.2" ry="5.2" fill={ink} />
    <circle cx="43.3" cy="59.3" r="1.4" fill="#fff"/><circle cx="68.3" cy="59.3" r="1.4" fill="#fff"/>
    <path d={grin ? 'M45 73q10 10 21 0-1 12-11 12-9 0-10-12Z' : 'M45 76q10 8 21 0'} fill={grin ? '#572e2c' : 'none'} stroke={ink} strokeWidth="2.4" strokeLinecap="round" strokeLinejoin="round" />
    {grin && <path d="M48 75q8 4 15 0" stroke="#fff6d9" strokeWidth="3" strokeLinecap="round" />}
    <ellipse cx="35" cy="71" rx="4" ry="2.4" fill={c.cheek} opacity=".65"/><ellipse cx="75" cy="71" rx="4" ry="2.4" fill={c.cheek} opacity=".65"/>
    <path d="M27 36q3-29 28-30 25 1 28 30Z" fill={c.cap} stroke={ink} strokeWidth="4" strokeLinejoin="round" />
    <path d="M39 13q16-8 30 1" fill="none" stroke="#fff3ce" strokeWidth="3" strokeLinecap="round" />
    <path d="M45 24h20v9H45Z" fill={c.bill} stroke={ink} strokeWidth="2.5" />
    <path d="M14 38q41-11 82 0-1 11-41 13-40-2-41-13Z" fill={c.cap} stroke={ink} strokeWidth="4" strokeLinejoin="round" />
    <path d="M26 43q32 6 58 0" fill="none" stroke="#fff3d7" strokeWidth="2.5" strokeLinecap="round" opacity=".65" />
    <circle cx="85" cy="95" r="5" fill="#fff8d8" stroke={ink} strokeWidth="2"/><path d="M85 91v8m-4-4h8" stroke={c.scarf} strokeWidth="1.5"/>
  </svg>
}

export function ExpeditionGroup({ participantes }: { participantes: Participante[] }) {
  return <div className="expedition-group" aria-label="Grupo de expedición">
    <span className="expedition-label">Tu grupo de expedición</span>
    <div className="expedition-members">{participantes.map((persona, index) => <div className="expedition-member" key={index} style={{ animationDelay: `${index * 70}ms` }}>
      <ExplorerAvatar index={index} />
      <span>{persona.nombre.trim().split(' ')[0] || `Persona ${index + 1}`}</span>
    </div>)}</div>
  </div>
}
