import logo from '../../assets/eco-harmony-logo.svg'

export function ConfirmacionScene() {
  return <svg className="confirmation-scene" viewBox="0 0 600 280" preserveAspectRatio="xMidYMid slice" role="img" aria-label="Entrada festiva de Eco Harmony Park con árboles, flores y banderines">
    <rect width="600" height="280" fill="#FBE7B8" />
    <circle cx="490" cy="67" r="36" fill="#FFD377" />
    <path d="M0 163C104 123 190 159 270 138S468 106 600 152V280H0Z" fill="#B9D39A" />
    <path d="M0 192C95 149 172 191 267 169S452 151 600 188V280H0Z" fill="#77AB81" />
    <path d="M0 223C109 187 214 213 301 195S497 190 600 221V280H0Z" fill="#3E806A" />
    <path d="M224 280c16-36 39-55 76-74 37 19 60 38 76 74Z" fill="#F8D79F" opacity=".9" />
    <path d="M0 24c164 35 345 31 600-1" fill="none" stroke="#315B4E" strokeWidth="3" />
    <g className="confirmation-flags" stroke="#315B4E" strokeWidth="2" strokeLinejoin="round"><path d="m69 37 13 2-8 21Z" fill="#F47B38"/><path d="m143 45 14 1-7 22Z" fill="#FFF8E8"/><path d="m218 49 14 0-7 22Z" fill="#198E88"/><path d="m377 45 14-1-6 23Z" fill="#F47B38"/><path d="m457 38 14-2-4 23Z" fill="#FFF8E8"/><path d="m533 28 14-3-3 23Z" fill="#198E88"/></g>
    <g className="confirmation-tree tree-left"><path d="M66 280V113" stroke="#325E4D" strokeWidth="17" strokeLinecap="round"/><path d="M66 178 34 143M66 151l38-38" stroke="#325E4D" strokeWidth="8" strokeLinecap="round"/><circle cx="51" cy="99" r="43" fill="#4F996E"/><circle cx="97" cy="115" r="40" fill="#61A875"/><circle cx="69" cy="65" r="41" fill="#69AE7B"/><path d="M65 77c5-9 10-15 18-18" stroke="#A6CC8E" strokeWidth="3" strokeLinecap="round"/></g>
    <g className="confirmation-tree tree-right"><path d="M540 280V113" stroke="#325E4D" strokeWidth="17" strokeLinecap="round"/><path d="M540 178l-33-35M540 151l34-38" stroke="#325E4D" strokeWidth="8" strokeLinecap="round"/><circle cx="519" cy="110" r="41" fill="#4F996E"/><circle cx="566" cy="107" r="42" fill="#61A875"/><circle cx="542" cy="66" r="43" fill="#69AE7B"/><path d="M539 75c7-10 13-14 20-17" stroke="#A6CC8E" strokeWidth="3" strokeLinecap="round"/></g>
    <path d="M103 243c22-15 37-15 60 0M442 245c18-15 36-15 58 0" fill="none" stroke="#245D4E" strokeWidth="4" strokeLinecap="round" />
    <g className="confirmation-flowers" stroke="#315B4E" strokeWidth="2"><path d="M151 253v-24M467 258v-24"/><path d="M151 244c-10-8-16-6-16-6M467 249c10-8 16-6 16-6" fill="none"/><circle cx="151" cy="225" r="8" fill="#FFF8E8"/><circle cx="151" cy="225" r="3" fill="#F47B38"/><circle cx="467" cy="230" r="8" fill="#FFF8E8"/><circle cx="467" cy="230" r="3" fill="#F47B38"/></g>
    <image href={logo} x="23" y="16" width="47" height="47" className="confirmation-emblem" />
    <g className="confirmation-sparkles" fill="#F47B38"><path d="m123 87 4 10 10 4-10 4-4 10-4-10-10-4 10-4Z"/><path d="m467 119 3 8 8 3-8 3-3 8-3-8-8-3 8-3Z"/></g>
    <g className="confirmation-butterfly" fill="#F47B38" stroke="#315B4E" strokeWidth="2"><path d="M415 91c-22-20-24 13-5 10-18 14 5 26 13 3 8 23 31 11 13-3 19 3 17-30-5-10l-8 12Z"/><path d="M423 101v12" fill="none" strokeLinecap="round"/></g>
  </svg>
}
