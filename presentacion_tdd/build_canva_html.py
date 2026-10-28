"""Build a self-contained, editable HTML slide deck for Canva import.

This script only assembles existing frontend artwork and slide text. It does
not alter the frontend or generate illustrative imagery.
"""

from base64 import b64encode
from html import escape
from pathlib import Path
import re
from io import BytesIO
from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "04_Trabajos_Practicos/Evaluables/TPE03/G6_COD_InscripcionActividad/frontend/src/assets"
FONTS = ROOT / "04_Trabajos_Practicos/Evaluables/TPE03/G6_COD_InscripcionActividad/frontend/node_modules/@fontsource"
OUT = Path(__file__).resolve().parent / "ecoharmony_tdd_canva.html"


def data(path: Path, mime: str) -> str:
    return f"data:{mime};base64,{b64encode(path.read_bytes()).decode()}"


def compact_art(path: Path) -> str:
    """Repackage existing transparent art as WebP for Canva's 10 MB limit."""
    with Image.open(path) as source:
        art = source.convert("RGBA")
        art.thumbnail((1000, 1000), Image.Resampling.LANCZOS)
        output = BytesIO()
        art.save(output, format="WEBP", quality=82, method=6)
    return f"data:image/webp;base64,{b64encode(output.getvalue()).decode()}"


logo = data(ASSETS / "eco-harmony-logo.svg", "image/svg+xml")
gif = {name: compact_art(ASSETS / "guia-frames" / f"{name}-0.png") for name in
       ["parque", "safari", "tirolesa", "palestra", "jardineria"]}
gesture = {name: compact_art(ASSETS / "guia-assistant" / f"{name}.png") for name in
           ["wave", "point", "think", "cheer"]}
confirmed = compact_art(ASSETS / "guia-confirmacion/confirmada.png")
fredoka = data(FONTS / "fredoka/files/fredoka-latin-600-normal.woff2", "font/woff2")
nunito = data(FONTS / "nunito/files/nunito-latin-700-normal.woff2", "font/woff2")


def img(src: str, cls: str, alt: str) -> str:
    return f'<img class="{cls}" src="{src}" alt="{escape(alt)}">'


def brand() -> str:
    return f'<div class="brand">{img(logo, "brand-mark", "Logo Eco Harmony Park")}<div>ECO HARMONY<br><small>PARK · TPE03</small></div></div>'


def footer(num: int, branch: str = "") -> str:
    return f'<div class="footer"><b>{num:02d} / 12</b><span>{escape(branch)}</span></div>'


def page(num: int, label: str, cls: str, content: str, notes: str = "") -> str:
    return (f'<section data-document-role="page" data-label="{escape(label)}" '
            f'data-speaker-notes="{escape(notes)}" class="page {cls}">'
            f'{content}{brand()}{footer(num, "Eco Harmony Park · Ingeniería y Calidad de Software")}</section>')


slides = []

# 01 - dramatic illustrated opening
slides.append(page(1, "La expedición TDD", "cover", f'''
  <div class="sun-disc"></div><div class="grain"></div>
  <div class="chapter">BITÁCORA DE EXPLORACIÓN  /  2026</div>
  <h1>LA EXPEDICIÓN<br><em>TDD</em></h1>
  <div class="cover-cycle"><span>RED</span><span>GREEN</span><span>REFACTOR</span></div>
  <p class="cover-sub">Cómo construimos la inscripción a actividades, una prueba por vez.</p>
  {img(gesture['wave'], 'guia cover-guia', 'Guía saluda')}
  <div class="cover-stamp">¡VAMOS<br>AL PARQUE!</div>
''', "Presentación del TPE03. Guía conduce un recorrido por los ciclos TDD documentados en las ramas."))

# 02 - route as large numbered footprints
slides.append(page(2, "Mapa de la expedición", "route", f'''
  <div class="eyebrow">01 / EL RECORRIDO</div><h2>UNA INSCRIPCIÓN,<br>CINCO ESTACIONES</h2>
  <div class="trail trail-a"></div><div class="trail trail-b"></div>
  <div class="station st1"><strong>01</strong><span>Consultar<br>actividad</span></div>
  <div class="station st2"><strong>02</strong><span>Aceptar<br>términos</span></div>
  <div class="station st3"><strong>03</strong><span>Cargar<br>participantes</span></div>
  <div class="station st4"><strong>04</strong><span>Reservar<br>cupos</span></div>
  <div class="station st5"><strong>05</strong><span>Enviar<br>confirmación</span></div>
  <div class="route-note">GRUPO 6<br><b>da vida al recorrido</b><br>con el frontend y Guía</div>
  {img(gif['parque'], 'guia route-guia', 'Guía en la paleta del parque')}
''', "Grupos 1 a 5 implementan partes del backend; Grupo 6 creó la demostración visual del frontend."))

# 03 - three large irregular type blocks
slides.append(page(3, "Red Green Refactor", "cycle", f'''
  <div class="eyebrow">02 / LA MECÁNICA</div><h2>EL CICLO QUE<br>NOS HIZO AVANZAR</h2>
  <div class="phase red"><b>RED</b><span>Una prueba falla<br>por la regla nueva.</span></div>
  <div class="phase green"><b>GREEN</b><span>El cambio mínimo<br>la hace pasar.</span></div>
  <div class="phase refactor"><b>REFACTOR</b><span>Limpiamos diseño<br>con pruebas verdes.</span></div>
  {img(gesture['think'], 'guia cycle-guia', 'Guía piensa')}
  <div class="hand-note">Si el test ya pasa,<br>todavía no hubo RED.</div>
''', "RED requiere un fallo por la razón esperada. El historial de consulta registra un caso de las 18 h que pasó sin RED real (4543df3)."))

# 04 - group 1, safari palette
slides.append(page(4, "Grupo 1: consulta", "group g1", f'''
  <div class="eyebrow">ESTACIÓN 01  /  tdd/consultar-actividad</div>
  <h2>¿QUÉ TURNO<br>SE PUEDE ELEGIR?</h2>
  <div class="big-number">15<span>MIN</span></div>
  <div class="evidence"><p><b>RED</b> <code>51a82e1</code> prueba un turno demasiado cercano.</p>
  <p><b>GREEN</b> <code>580a29f</code> lo excluye de la oferta.</p>
  <p><b>REFACTOR</b> <code>5dcebf4</code> ordena pruebas de cupos independientes.</p></div>
  <div class="side-note">También cubrieron feriados, lunes, turnos llenos<br>y la ventana de hasta 24 horas.</div>
  {img(gif['safari'], 'guia g1-guia', 'Guía en modo Safari')}
''', "Commits de la rama tdd/consultar-actividad. La prueba de 18:00 del commit 4543df3 ya pasaba y el grupo lo dejó indicado."))

# 05 - group 2, terms as ticket/contract
slides.append(page(5, "Grupo 2: términos", "group g2", f'''
  <div class="eyebrow">ESTACIÓN 02  /  tdd/terminos-confirmacion</div>
  <h2>ACEPTAR LOS TÉRMINOS<br>DE ESTA ACTIVIDAD</h2>
  <div class="ticket"><div class="ticket-top">PERMISO DE EXPLORACIÓN</div>
  <p>¿Aceptó? <b>SÍ</b></p><p>¿Corresponde a la actividad elegida? <b>SÍ</b></p>
  <div class="ticket-bottom">32 CASOS DOCUMENTADOS</div></div>
  <div class="evidence"><p><b>RED</b> <code>2ffade1</code> rechazar términos no aceptados.</p>
  <p><b>GREEN</b> <code>65665f6</code> agrega el rechazo.</p>
  <p><b>REFACTOR</b> <code>64acfe9</code> reúne combinaciones de actividades.</p></div>
  {img(gesture['point'], 'guia g2-guia', 'Guía señala las condiciones')}
  <div class="side-note">El texto de términos sigue siendo ficticio.</div>
''', "La evidencia individual del Grupo 2 registra 32 casos. Hay otro ciclo para aceptación de una actividad diferente: feb0270 y 65e00e4."))

# 06 - group 3, participant stamps
slides.append(page(6, "Grupo 3: participantes", "group g3", f'''
  <div class="eyebrow">ESTACIÓN 03  /  tdd/cargar-participante</div>
  <h2>¿QUIÉNES SALEN<br>DE EXPEDICIÓN?</h2>
  <div class="rule r1">DNI<br><b>ÚNICO</b></div><div class="rule r2">TIROLESA<br><b>8+</b></div>
  <div class="rule r3">PALESTRA<br><b>12+</b></div><div class="rule r4">TALLE<br><b>OBLIGATORIO*</b></div>
  <div class="evidence"><p><b>RED</b> <code>a4ab194</code> participantes superan el cupo.</p>
  <p><b>GREEN</b> <code>cf3c3e3</code> rechaza esa cantidad.</p>
  <p><b>REFACTOR</b> <code>dcd2e4f</code> extrae un helper para las pruebas.</p></div>
  <div class="fine">*En Tirolesa y Palestra.</div>
  {img(gif['tirolesa'], 'guia g3-guia', 'Guía en modo Tirolesa')}
''', "Grupo 3 añadió ciclos para cantidad, nombre, talle, DNI, edad mínima y cupo por actividad. Las edades provienen de su bitácora."))

# 07 - group 4, fake mail and QR
slides.append(page(7, "Grupo 4: confirmación", "group g4", f'''
  <div class="eyebrow">ESTACIÓN 04  /  tdd/envio-confirmacion-inscripcion</div>
  <h2>EL CORREO SALIÓ<br>PRIMERO EN UNA PRUEBA</h2>
  <div class="mail"><div class="mail-head">PARA: visitante@ecoharmony.park</div>
  <div class="mail-body">Tu inscripción está confirmada.<br>Resumen + QR único</div>
  <div class="mail-stamp">CORREO<br>FALSO</div></div>
  <div class="evidence"><p><b>RED</b> <code>4dd9ab7</code> espera un envío en <i>CorreoFalso</i>.</p>
  <p><b>GREEN</b> <code>7a6217c</code> hace el envío mínimo.</p>
  <p><b>REFACTOR</b> <code>c2e39ac</code> mejora resumen e imports.</p></div>
  {img(gesture['cheer'], 'guia g4-guia', 'Guía festeja el correo')}
  <div class="side-note">El servicio aún no expone un endpoint propio.</div>
''', "El grupo revirtió una implementación SMTP porque había adelantado producción sin test. Servicio de notificaciones con QR y correo, sin endpoint propio."))

# 08 - group 5, tension and concurrency
slides.append(page(8, "Grupo 5: cupos", "group g5", f'''
  <div class="eyebrow">ESTACIÓN 05  /  tdd/registrar-inscripcion + gestion-reservas-cupos</div>
  <h2>ÚLTIMOS CUPOS.<br>DOS SOLICITUDES.</h2>
  <div class="duel"><div>VISITANTE A<br><strong>2 LUGARES</strong></div><b>VS</b><div>VISITANTE B<br><strong>2 LUGARES</strong></div></div>
  <div class="result">UNA SOLA RESERVA ENTRA · SIN SOBREVENTA</div>
  <div class="evidence"><p><b>RED</b> <code>cb85c56</code> reproduce el choque simultáneo.</p>
  <p><b>GREEN</b> <code>3bceeb5</code> protege la operación con un lock.</p>
  <p><b>REFACTOR</b> <code>7c41d5c</code> evita bloqueo interno.</p></div>
  {img(gif['palestra'], 'guia g5-guia', 'Guía en modo Palestra')}
''', "La rama gestion-reservas-cupos documenta 12 pruebas: cupos, reserva, persistencia en memoria y concurrencia. También existe tdd/registrar-inscripcion con ciclos anteriores."))

# 09 - annotated commit trail
slides.append(page(9, "Anatomía de un ciclo", "anatomy", f'''
  <div class="eyebrow">03 / UN CICLO EN EL HISTORIAL</div><h2>DE UN FALLO REAL<br>A UNA REGLA SEGURA</h2>
  <div class="commit c1"><small>01 / RED</small><code>cb85c56</code><p>Dos solicitudes compiten<br>por los últimos lugares.</p></div>
  <div class="commit c2"><small>02 / GREEN</small><code>3bceeb5</code><p>Un lock protege<br>comprobación y descuento.</p></div>
  <div class="commit c3"><small>03 / REFACTOR</small><code>7c41d5c</code><p>Helper interno evita<br>deadlocks.</p></div>
  {img(gesture['think'], 'guia anatomy-guia', 'Guía estudia los commits')}
  <div class="anatomy-note">EL TEST DEBE FALLAR<br>POR EL MOTIVO ESPERADO</div>
''', "Ejemplo tomado de los tres commits consecutivos del Grupo 5 en gestion-reservas-cupos."))

# 10 - frontend identity, honest boundaries
slides.append(page(10, "Grupo 6: frontend", "frontend", f'''
  <div class="eyebrow">04 / EL PARQUE COBRA VIDA</div><h2>GUÍA CAMBIA<br>CON LA ACTIVIDAD</h2>
  <div class="colorway cw1">SAFARI{img(gif['safari'], 'little-guia', 'Guía Safari')}</div>
  <div class="colorway cw2">TIROLESA{img(gif['tirolesa'], 'little-guia', 'Guía Tirolesa')}</div>
  <div class="colorway cw3">PALESTRA{img(gif['palestra'], 'little-guia', 'Guía Palestra')}</div>
  <div class="colorway cw4">JARDINERÍA{img(gif['jardineria'], 'little-guia', 'Guía Jardinería')}</div>
  <div class="frontend-note">Fredoka + Nunito. Paisajes y gestos animados.<br>La reserva y el QR del frontend son una demo local.</div>
''', "La rama tdd/frontend construye la experiencia React y la mascota Guía. Usa localStorage, turnos simulados y comprobante de muestra; no constituye integración backend ni evidencia de ciclos TDD propios."))

# 11 - lessons + real integration boundaries
slides.append(page(11, "Aprendizajes y pendientes", "lessons", f'''
  <div class="eyebrow">05 / LO QUE DEJÓ LA EXPEDICIÓN</div><h2>LA PRUEBA NOS<br>OBLIGÓ A PRECISAR</h2>
  <div class="lesson l1"><b>REGLAS</b><span>Edades, términos, cupos y ventanas de tiempo quedaron explícitos.</span></div>
  <div class="lesson l2"><b>DEPENDENCIAS</b><span><i>CorreoFalso</i> permitió validar el envío antes de SMTP real.</span></div>
  <div class="lesson l3"><b>DISEÑO</b><span>Helpers y parametrización limpiaron pruebas sin perder cobertura.</span></div>
  <div class="next">PRÓXIMO PASO<br><strong>Alinear contratos, exponer endpoints y reemplazar la demo local.</strong></div>
  {img(gif['jardineria'], 'guia lessons-guia', 'Guía en modo Jardinería')}
''', "Los grupos implementaron módulos en ramas separadas. Integración y contratos siguen pendientes según el README del frontend y decisiones del Grupo 4."))

# 12 - memorable ending, animated confirmation
slides.append(page(12, "Cierre", "end", f'''
  <div class="starburst"></div><div class="eyebrow">FIN DE LA EXPEDICIÓN · COMIENZO DEL PRÓXIMO CICLO</div>
  <h2>UNA REGLA.<br>UNA PRUEBA.<br>UN CAMBIO MÍNIMO.</h2>
  <div class="end-line">Y DESPUÉS, UNA MEJORA SEGURA.</div>
  {img(confirmed, 'guia end-guia', 'Guía celebra la inscripción confirmada')}
  <div class="end-question">¿QUÉ CASO PROBARÍAS AHORA?</div>
''', "Cierre para abrir preguntas. La imagen animada de Guía es la original del frontend."))

# Canva's HTML importer does not preserve flow inside positioned containers.
# Keep evidence as independently positioned, single-line text objects.
def simplify_evidence(match: re.Match[str]) -> str:
    inner = re.sub(r"</?(?:b|code|i)>", "", match.group(1))
    return f'<div class="evidence">{inner}</div>'


slides = [re.sub(r'<div class="evidence">(.*?)</div>', simplify_evidence, slide, flags=re.S)
          for slide in slides]
slides = [re.sub(r'<div class="side-note">.*?</div>', '', slide, flags=re.S)
          for slide in slides]

css = f'''
@font-face{{font-family:Fredoka;src:url({fredoka}) format('woff2');font-weight:600}}
@font-face{{font-family:Nunito;src:url({nunito}) format('woff2');font-weight:700}}
*{{box-sizing:border-box}}html,body{{margin:0;padding:0}}body{{background:#263c34}}
.page{{width:1920px;height:1080px;position:relative;overflow:hidden;margin:0 auto;background:#fff8e8;color:#263c34;font-family:Nunito,sans-serif}}
.page:after{{content:'';position:absolute;inset:0;pointer-events:none;opacity:.13;background-image:radial-gradient(#263c34 1px,transparent 1px);background-size:10px 10px;mix-blend-mode:multiply}}
.page h1,.page h2,.phase b,.station strong,.rule b,.big-number,.result,.commit code,.end-line{{font-family:Fredoka,sans-serif;font-weight:600;letter-spacing:-.035em}}
h1,h2,p{{margin:0}}.page h2{{font-size:102px;line-height:.94;position:absolute;z-index:3}}
.eyebrow,.chapter{{position:absolute;left:92px;top:74px;font-size:27px;letter-spacing:.15em;font-weight:900;z-index:4}}
.brand{{position:absolute;left:92px;bottom:78px;display:flex;align-items:center;gap:14px;font:600 21px/1 Fredoka,sans-serif;z-index:10}}
.brand-mark{{width:70px;height:70px;object-fit:contain}}.brand small{{font:700 13px/1.3 Nunito,sans-serif;letter-spacing:.14em}}
.footer{{position:absolute;right:85px;bottom:88px;font-size:19px;letter-spacing:.1em;z-index:10;display:flex;gap:24px;align-items:center}}
.footer b{{font:600 27px Fredoka,sans-serif}}.guia{{position:absolute;object-fit:contain;z-index:4}}
.cover{{background:#f8edcd}}.cover:before{{content:'';position:absolute;left:-200px;top:-220px;width:1450px;height:1400px;background:#f6a65a;border-radius:50%;border:12px solid #263c34;transform:rotate(-16deg)}}
.cover .chapter{{top:60px}}.cover h1{{position:absolute;left:100px;top:195px;font-size:176px;line-height:.88;z-index:3}}.cover h1 em{{font-style:normal;color:#fff8e8;text-shadow:9px 9px 0 #263c34}}
.cover-guia{{height:970px;width:990px;right:-110px;top:38px;filter:drop-shadow(15px 16px 0 #263c34)}}
.cover-cycle{{position:absolute;left:103px;top:682px;z-index:5;display:flex;gap:18px}}.cover-cycle span{{font:600 43px Fredoka;background:#263c34;color:#fff8e8;padding:15px 26px;border-radius:80px;transform:rotate(-5deg)}}.cover-cycle span:nth-child(2){{background:#217b73;transform:rotate(4deg)}}.cover-cycle span:nth-child(3){{background:#f47b38;transform:rotate(-2deg)}}
.cover-sub{{position:absolute;left:106px;top:790px;width:710px;font-size:38px;line-height:1.12;z-index:4}}.cover-stamp{{position:absolute;right:105px;top:85px;border:6px double #263c34;border-radius:50%;padding:35px;transform:rotate(16deg);font:600 28px/1 Fredoka;text-align:center;z-index:6;background:#fff8e8}}
.route{{background:#e7f2dc}}.route h2{{left:92px;top:130px}}.route-guia{{height:660px;right:35px;bottom:35px;filter:drop-shadow(10px 14px 0 #263c3455)}}
.station{{position:absolute;width:270px;height:240px;border:7px solid #263c34;border-radius:47% 53% 41% 59%;background:#fff8e8;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;transform:rotate(-9deg);z-index:4;box-shadow:13px 15px 0 #263c3427}}
.station strong{{font-size:70px;line-height:.9;color:#f47b38}}.station span{{font-size:28px;line-height:1.05}}.st1{{left:106px;top:445px}}.st2{{left:405px;top:610px;background:#e7c6a6;transform:rotate(7deg)}}.st3{{left:716px;top:426px;background:#ace0d9;transform:rotate(-5deg)}}.st4{{left:1034px;top:627px;background:#f9d789;transform:rotate(9deg)}}.st5{{left:1320px;top:450px;background:#f7b2a0;transform:rotate(-5deg)}}
.route-note{{position:absolute;left:112px;top:785px;font:600 28px/1.2 Fredoka;transform:rotate(-5deg);z-index:5}}.route-note b{{color:#e55c30}}
.cycle{{background:#f2d9b8}}.cycle h2{{left:92px;top:139px}}.phase{{position:absolute;top:405px;width:525px;height:450px;border:8px solid #263c34;border-radius:48% 52% 40% 60%;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;transform:rotate(-7deg);box-shadow:18px 20px 0 #263c3430}}
.phase b{{font-size:103px;line-height:1}}.phase span{{font-size:33px;line-height:1.14}}.red{{left:70px;background:#ed6f5e;color:#fff8e8}}.green{{left:687px;background:#77b787;transform:rotate(7deg)}}.refactor{{left:1310px;background:#79c6c4;transform:rotate(-4deg)}}.refactor b{{font-size:75px}}.cycle-guia{{width:265px;height:265px;left:1140px;top:180px;transform:rotate(10deg)}}.hand-note{{position:absolute;left:85px;top:915px;font:600 28px/1 Fredoka;transform:rotate(-3deg)}}
.group h2{{left:92px;top:145px}}.group .evidence{{position:absolute;left:92px;top:740px;width:1300px;height:210px;font:700 34px/1.1 Nunito,sans-serif;z-index:5}}.evidence p{{position:absolute;left:0;margin:0;white-space:nowrap}}.evidence p:nth-child(1){{top:0}}.evidence p:nth-child(2){{top:65px}}.evidence p:nth-child(3){{top:130px}}.commit code{{font-family:Fredoka,sans-serif;color:#d4542c;font-size:34px}}
.g1{{background:#e4f3e2}}.g1 h2{{font-size:108px}}.g1-guia{{right:-30px;bottom:80px;width:780px;height:780px}}.big-number{{position:absolute;right:730px;top:220px;font-size:205px;color:#f47b38;transform:rotate(-9deg);z-index:3}}.big-number span{{font-size:75px}}.g1 .evidence{{bottom:190px}}
.g2{{background:#f8edda}}.g2 h2{{font-size:91px}}.g2-guia{{right:-25px;bottom:60px;width:630px;height:690px}}.ticket{{position:absolute;left:90px;top:415px;width:820px;height:235px;border:6px dashed #263c34;background:#fff8e8;transform:rotate(-4deg);z-index:3;padding:20px 32px;box-shadow:12px 12px 0 #e8ae77}}.ticket-top{{font:600 31px Fredoka;border-bottom:3px solid #263c34}}.ticket p{{font-size:28px;margin-top:12px}}.ticket p b{{float:right}}.ticket-bottom{{position:absolute;right:22px;bottom:13px;color:#e35b37;font:600 29px Fredoka}}.g2 .evidence{{bottom:140px;font-size:28px}}.g2 .evidence p{{margin:7px 0}}.g2 .side-note{{left:1120px;bottom:194px;width:320px}}
.g3{{background:#e2f2f1}}.g3 h2{{font-size:106px}}.g3-guia{{right:-90px;bottom:55px;width:770px;height:740px}}.rule{{position:absolute;top:420px;width:245px;height:155px;border:6px solid #263c34;border-radius:26px;background:#f8dd9e;transform:rotate(-8deg);padding:20px 10px;text-align:center;font:700 24px/1 Nunito;z-index:3;box-shadow:9px 9px 0 #263c3430}}.rule b{{font-size:49px}}.r1{{left:95px}}.r2{{left:360px;background:#f6b290;transform:rotate(5deg)}}.r3{{left:625px;background:#b5ddba;transform:rotate(-5deg)}}.r4{{left:890px;background:#f8d678;transform:rotate(7deg)}}.r4 b{{font-size:28px}}.g3 .evidence{{bottom:175px}}.fine{{position:absolute;left:930px;top:595px;font-size:21px}}
.g4{{background:#f7e5d5}}.g4 h2{{font-size:97px}}.g4-guia{{right:30px;bottom:50px;width:680px;height:680px}}.mail{{position:absolute;left:88px;top:415px;width:890px;height:245px;background:#fff8e8;border:7px solid #263c34;border-radius:18px;transform:rotate(-4deg);box-shadow:16px 15px 0 #c97b52;z-index:3}}.mail-head{{border-bottom:4px solid #263c34;padding:18px 25px;font-size:25px}}.mail-body{{padding:25px;font:600 34px/1.12 Fredoka}}.mail-stamp{{position:absolute;right:45px;bottom:25px;border:5px solid #d65b39;color:#d65b39;transform:rotate(15deg);border-radius:50%;padding:15px;font:600 19px/1 Fredoka;text-align:center}}.g4 .evidence{{bottom:150px;font-size:28px}}.g4 .evidence p{{margin:7px 0}}.g4 .side-note{{left:1170px;bottom:200px;width:300px}}
.g5{{background:#ece9d1}}.g5 h2{{font-size:112px}}.g5-guia{{right:-25px;bottom:65px;width:700px;height:730px}}.duel{{position:absolute;left:92px;top:415px;display:flex;align-items:center;gap:22px;z-index:3}}.duel div{{background:#fff8e8;border:6px solid #263c34;border-radius:35px;padding:22px 28px;font-size:26px;transform:rotate(-5deg);text-align:center}}.duel div:last-child{{transform:rotate(5deg)}}.duel strong{{font:600 40px Fredoka}}.duel>b{{font:600 43px Fredoka;color:#e36b41}}.result{{position:absolute;left:92px;top:615px;background:#80bd9d;border:5px solid #263c34;padding:13px 23px;transform:rotate(-2deg);font-size:30px;z-index:3}}.g5 .evidence{{bottom:155px;font-size:28px}}.g5 .evidence p{{margin:7px 0}}
.anatomy{{background:#d8ece4}}.anatomy h2{{left:92px;top:140px;font-size:98px}}.commit{{position:absolute;top:430px;width:430px;height:390px;border:6px solid #263c34;border-radius:27px;padding:28px;transform:rotate(-5deg);box-shadow:12px 13px 0 #263c3430}}.commit small{{font:600 29px Fredoka}}.commit code{{display:block;font-size:63px;margin:22px 0 5px}}.commit p{{font-size:28px;line-height:1.1}}.c1{{left:90px;background:#f79f86}}.c2{{left:565px;background:#a6d6aa;transform:rotate(3deg)}}.c3{{left:1040px;background:#f7d993;transform:rotate(-2deg)}}.anatomy-guia{{right:5px;bottom:105px;width:440px;height:470px}}.anatomy-note{{position:absolute;right:140px;top:180px;font:600 31px/1 Fredoka;transform:rotate(9deg)}}
.frontend{{background:#fff2db}}.frontend h2{{left:92px;top:135px;font-size:102px}}.colorway{{position:absolute;top:420px;width:390px;height:425px;border:7px solid #263c34;border-radius:24px;text-align:center;padding:20px;font:600 36px Fredoka;transform:rotate(-5deg);overflow:hidden;box-shadow:12px 13px 0 #263c3430}}.cw1{{left:82px;background:#b5e6c0}}.cw2{{left:525px;background:#b2e6ea;transform:rotate(4deg)}}.cw3{{left:968px;background:#f1d3bf;transform:rotate(-3deg)}}.cw4{{left:1410px;background:#f5e3af;transform:rotate(5deg)}}.little-guia{{position:absolute;left:0;top:60px;width:100%;height:340px;object-fit:contain}}.frontend-note{{position:absolute;left:95px;top:882px;font-size:31px;line-height:1.1}}
.lessons{{background:#e8efdb}}.lessons h2{{left:92px;top:140px;font-size:104px}}.lessons-guia{{right:-30px;bottom:40px;width:740px;height:770px}}.lesson{{position:absolute;left:92px;width:1050px;display:flex;gap:35px;align-items:center;border-bottom:4px solid #263c34;padding:12px 0;font-size:29px;line-height:1.12}}.lesson b{{font:600 43px Fredoka;color:#d85c36;min-width:260px}}.l1{{top:430px}}.l2{{top:545px}}.l3{{top:660px}}.next{{position:absolute;left:92px;top:810px;width:1140px;font:600 27px/1.15 Fredoka;color:#185a54}}.next strong{{font-size:36px;color:#263c34}}
.end{{background:#f2c58f}}.end h2{{left:92px;top:150px;font-size:118px}}.end-guia{{right:-25px;top:15px;width:880px;height:970px}}.end-line{{position:absolute;left:95px;top:620px;font-size:52px;transform:rotate(-4deg)}}.end-question{{position:absolute;left:95px;top:790px;background:#263c34;color:#fff8e8;border-radius:80px;padding:21px 34px;transform:rotate(3deg);font:600 40px Fredoka}}
'''

html = ('<!doctype html><html lang="es"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=1920,initial-scale=1">'
        f'<style>{css}</style></head><body>{"".join(slides)}</body></html>')
OUT.write_text(html, encoding="utf-8")
print(OUT)
print(f"{len(slides)} slides; {OUT.stat().st_size / 1024 / 1024:.2f} MB")
