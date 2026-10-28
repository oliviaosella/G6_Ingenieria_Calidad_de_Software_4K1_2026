"""Build the final Eco Harmony Park TDD deck as self-contained Canva HTML."""

from base64 import b64encode
from html import escape
from io import BytesIO
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
ASSETS = ROOT / "04_Trabajos_Practicos/Evaluables/TPE03/G6_COD_InscripcionActividad/frontend/src/assets"
FONTS = ROOT / "04_Trabajos_Practicos/Evaluables/TPE03/G6_COD_InscripcionActividad/frontend/node_modules/@fontsource"
OUT = HERE / "ecoharmony_tdd_rebuild.html"


def raw(path: Path, mime: str) -> str:
    return f"data:{mime};base64,{b64encode(path.read_bytes()).decode()}"


def bitmap(path: Path, max_size=(1500, 1000), quality=85) -> str:
    with Image.open(path) as source:
        image = source.convert("RGBA")
        image.thumbnail(max_size, Image.Resampling.LANCZOS)
        out = BytesIO()
        image.save(out, "WEBP", quality=quality, method=2)
    return f"data:image/webp;base64,{b64encode(out.getvalue()).decode()}"


logo = raw(ASSETS / "eco-harmony-logo.svg", "image/svg+xml")
guia = {name: bitmap(ASSETS / "guia-frames" / f"{name}-0.png", (1000, 1000), 90) for name in
        ["parque", "safari", "tirolesa", "palestra", "jardineria"]}
gesture = {name: bitmap(ASSETS / "guia-assistant" / f"{name}.png", (1000, 1000), 90) for name in
           ["wave", "point", "think", "cheer"]}
confirmed = bitmap(ASSETS / "guia-confirmacion/confirmada.png", (1000, 1000), 90)
shots = {name: bitmap(HERE / f"demo-{name}.png", (1550, 950), 82) for name in
         ["home", "actividad", "turnos", "participantes", "confirmar", "comprobante"]}
nature = {name: bitmap(HERE / f"oldschool-{name}-frame.png", (1920, 1080), 78) for name in
          ["jungle", "safari", "rock", "garden"]}
fredoka = raw(FONTS / "fredoka/files/fredoka-latin-600-normal.woff2", "font/woff2")
nunito = raw(FONTS / "nunito/files/nunito-latin-700-normal.woff2", "font/woff2")


def image(src, cls, alt):
    return f'<img class="{cls}" src="{src}" alt="{escape(alt)}">'


def mark():
    return image(logo, "logo", "Eco Harmony Park")


def slide(label, cls, body, notes=""):
    key = cls.split()[0]
    decoration = {
        "cover": "jungle", "journey": "safari", "cycle": "jungle",
        "g1": "safari", "g2": "garden", "g3": "jungle", "g4": "garden",
        "g5": "rock", "deadlock": "rock", "demo": "safari",
        "evidence-map": "jungle", "ticket": "garden",
        "boundaries": "rock", "closing": "jungle",
    }.get(key, "jungle")
    return (f'<section data-document-role="page" data-label="{escape(label)}" '
            f'data-speaker-notes="{escape(notes)}" class="slide {cls} nature-{decoration}">'
            f'<div class="nature-overlay"></div>{body}{mark()}</section>')


def code(lines):
    return '<pre>' + escape(lines.strip()) + '</pre>'


slides = []

slides.append(slide("TDD en Eco Harmony Park", "cover", f'''
  <div class="sun"></div><div class="leaf leaf-a"></div><div class="leaf leaf-b"></div>
  <h1>TDD en<br><span>Eco Harmony</span><br>Park</h1>
  <p class="lead">Una expedición por RED · GREEN · REFACTOR</p>
  <div class="badge">CÓDIGO REAL<br>PRUEBAS REALES</div>
  <div class="mascot-frame hero">{image(gesture['wave'], 'mascot', 'Guía saluda')}</div>
''', "Guía abre el recorrido. Esta presentación reconstruye los ciclos a partir de las ramas TDD y de la demo real del frontend."))

slides.append(slide("La historia de usuario completa", "journey", f'''
  <h1>La historia de usuario</h1>
  <div class="mapline"></div>
  <div class="stop s1"><b>1</b><span>Elegir<br>actividad</span></div>
  <div class="stop s2"><b>2</b><span>Ver<br>turnos</span></div>
  <div class="stop s3"><b>3</b><span>Cargar<br>personas</span></div>
  <div class="stop s4"><b>4</b><span>Aceptar<br>condiciones</span></div>
  <div class="stop s5"><b>5</b><span>Reservar<br>cupos</span></div>
  <div class="stop s6"><b>6</b><span>Recibir<br>QR</span></div>
  <div class="screen-frame journey-shot">{image(shots['home'], 'screen', 'Inicio de la demo')}</div>
  <div class="mascot-frame map-mascot">{image(guia['parque'], 'mascot', 'Guía del parque')}</div>
''', "Los grupos construyeron reglas separadas que, juntas, describen el flujo completo de inscripción."))

slides.append(slide("RED, GREEN y REFACTOR", "cycle", f'''
  <h1>El ciclo TDD</h1>
  <div class="phase red"><strong>RED</strong><p>Escribir una regla observable y verla fallar por el motivo esperado.</p><span>✕</span></div>
  <div class="phase green"><strong>GREEN</strong><p>Implementar solo lo necesario para convertir el fallo en verde.</p><span>✓</span></div>
  <div class="phase refactor"><strong>REFACTOR</strong><p>Mejorar nombres, estructura y duplicación sin romper la conducta.</p><span>↻</span></div>
  <div class="tape">EL TEST ES LA EVIDENCIA DEL CAMBIO</div>
  <div class="mascot-frame think">{image(gesture['think'], 'mascot', 'Guía piensa')}</div>
''', "El ciclo no se demuestra con un hash: se demuestra mostrando qué conducta falló, qué cambio la hizo pasar y qué diseño se limpió después."))

slides.append(slide("Consulta de actividades", "g1", f'''
  <h1>Consulta de turnos</h1>
  <div class="clock"><b>09:46</b><span>14 minutos</span></div>
  <div class="codecard test"><label>RED · PRUEBA</label>{code('''def test_no_muestra_turno_si_faltan_menos_de_quince_minutos():
    resultado = listar_turnos(... hora_actual=09:46)
    horas = {turno["hora"] for turno in resultado}
    assert "10:00" not in horas''')}</div>
  <div class="codecard impl"><label>GREEN · CAMBIO MÍNIMO</label>{code('''tiempo_hasta_el_turno = inicio_turno - hora_actual
if tiempo_hasta_el_turno < timedelta(minutes=15):
    continue''')}</div>
  <div class="sticker">REFACTOR<br><small>misma regla + límite de 24 h</small></div>
  <div class="proof">También probaron: feriados · lunes · turnos llenos · cupos independientes</div>
  <div class="mascot-frame safari">{image(guia['safari'], 'mascot', 'Guía Safari')}</div>
''', "Grupo 1, rama tdd/consultar-actividad. La evidencia visible es la conducta: a las 09:46 ya no se ofrece el turno de las 10:00."))

slides.append(slide("Términos y confirmación", "g2", f'''
  <h1>Términos válidos</h1>
  <div class="contract"><b>CONDICIONES DE SAFARI</b><p>□ Acepto las condiciones de esta actividad.</p><div>ESTADO: NO ACEPTADO</div></div>
  <div class="failure">RED<br><small>DID NOT RAISE<br>TerminosNoAceptadosError</small></div>
  <div class="codecard test">{code('''with pytest.raises(TerminosNoAceptadosError):
    validar_aceptacion(actividad,
        AceptacionTerminos(actividad, aceptados=False))''')}</div>
  <div class="codecard impl">{code('''if not aceptacion.aceptados:
    raise TerminosNoAceptadosError
if aceptacion.actividad != actividad:
    raise AceptacionDeOtraActividadError''')}</div>
  <div class="stamp">32 CASOS<br>DOCUMENTADOS</div>
  <div class="mascot-frame point">{image(gesture['point'], 'mascot', 'Guía señala')}</div>
''', "Grupo 2, rama tdd/terminos-confirmacion. REFACTOR parametrizó combinaciones de actividades; el texto contractual sigue siendo ficticio."))

slides.append(slide("Carga de participantes", "g3", f'''
  <h1>Participantes y cupo</h1>
  <div class="capacity"><span>CUPO</span><b>8</b></div>
  <div class="people">● ● ● ● ● ● ● ● <i>●</i></div>
  <div class="codecard test">{code('''participantes = [crear_participante(...) for i in range(9)]
assert validar_participantes(8, participantes[:8], SAFARI) is True
assert validar_participantes(9, participantes, SAFARI) is False''')}</div>
  <div class="codecard impl">{code('''if cantidad != len(participantes) or cantidad <= 0 \
        or actividad.cupo < cantidad:
    return False''')}</div>
  <div class="passport p1">DNI<br><b>ÚNICO</b></div><div class="passport p2">TIROLESA<br><b>8+</b></div><div class="passport p3">PALESTRA<br><b>12+</b></div>
  <div class="refactor-note">REFACTOR: <b>crear_participante()</b> elimina preparación duplicada</div>
  <div class="mascot-frame tirolesa">{image(guia['tirolesa'], 'mascot', 'Guía Tirolesa')}</div>
''', "Grupo 3, rama tdd/cargar-participante. También se validaron DNI duplicado, edad mínima y talle obligatorio para Tirolesa y Palestra."))

slides.append(slide("Envío de confirmación", "g4", f'''
  <h1>Confirmación por correo</h1>
  <div class="envelope"><div>PARA: visitante@gmail.com</div><b>INSCRIPCIÓN CONFIRMADA</b><p>Resumen de actividad + QR</p><span>FAKE</span></div>
  <div class="codecard test">{code('''correo_falso = CorreoFalso()
servicio = ServicioNotificaciones(emisor_correo=correo_falso)
servicio.enviar_confirmacion(inscripcion)
assert len(correo_falso.envios) == 1
assert correo_falso.envios[0]["destinatario"] == "visitante@gmail.com"''')}</div>
  <div class="codecard impl">{code('''self.emisor_correo.enviar(
    destinatario=inscripcion["email"],
    contenido=preparar_resumen(inscripcion),
    qr=generar_qr(inscripcion))''')}</div>
  <div class="decision">DECISIÓN TDD<br><small>Se revirtió SMTP porque había adelantado producción sin prueba.</small></div>
  <div class="mascot-frame cheer">{image(gesture['cheer'], 'mascot', 'Guía celebra')}</div>
''', "Grupo 4, rama tdd/envio-confirmacion-inscripcion. El doble de prueba permite verificar destinatario, resumen y QR sin infraestructura externa."))

slides.append(slide("Concurrencia de reservas", "g5", f'''
  <h1>Reservas simultáneas</h1>
  <div class="race a"><b>A</b><span>pide 2</span></div><div class="race b"><b>B</b><span>pide 2</span></div>
  <div class="finish">ÚLTIMOS<br><b>2 CUPOS</b></div>
  <div class="codecard test">{code('''with ThreadPoolExecutor(max_workers=2) as executor:
    res_a = executor.submit(enviar_reserva, solicitud_a)
    res_b = executor.submit(enviar_reserva, solicitud_b)
assert len([r for r in [res_a.result(), res_b.result()] if r]) == 1
assert gestor.consultar_cupos("Safari", 1) == 0''')}</div>
  <div class="codecard impl">{code('''with self._lock:
    cupos = self._consultar_cupos_sin_lock(...)
    if cupos < cantidad: return None
    return self._reservar_sin_lock(...)''')}</div>
  <div class="result">✓ una entra &nbsp;&nbsp; ✕ una se rechaza &nbsp;&nbsp; 0 sobreventa</div>
  <div class="mascot-frame palestra">{image(guia['palestra'], 'mascot', 'Guía Palestra')}</div>
''', "Grupo 5, ramas tdd/registrar-inscripcion y gestion-reservas-cupos. La prueba de concurrencia reproduce el riesgo real de sobreventa."))

slides.append(slide("El refactor evitó un deadlock", "deadlock", f'''
  <h1>Refactor sin deadlock</h1>
  <div class="before"><b>ANTES</b>{code('''def reservar(...):
    with self._lock:
        cupos = self.consultar_cupos(...)
        # consultar_cupos vuelve a pedir el lock''')}<span>LOCK → LOCK → BLOQUEO</span></div>
  <div class="arrow">➜</div>
  <div class="after"><b>DESPUÉS</b>{code('''def _consultar_cupos_sin_lock(...): ...
def _reservar_sin_lock(...): ...

def reservar(...):
    with self._lock:
        return self._reservar_sin_lock(...)''')}<span>UN SOLO LÍMITE DE SINCRONIZACIÓN</span></div>
  <div class="lock-shape">🔒</div>
  <div class="mascot-frame mechanic">{image(gesture['think'], 'mascot', 'Guía revisa el diseño')}</div>
''', "El REFACTOR del Grupo 5 no agrega comportamiento: preserva los tests verdes y reorganiza las funciones para evitar adquirir el mismo lock dos veces."))

slides.append(slide("La demo conecta los casos de prueba", "demo", f'''
  <h1>Demo del flujo completo</h1>
  <div class="film f1">{image(shots['turnos'], 'screen', 'Selección de turnos')}<span>consultar-actividad<br><small>Se muestran solo turnos válidos</small></span></div>
  <div class="film f2">{image(shots['participantes'], 'screen', 'Carga de participantes')}<span>cargar-participante<br><small>Edad, DNI y cupo quedan visibles</small></span></div>
  <div class="film f3">{image(shots['confirmar'], 'screen', 'Aceptación de condiciones')}<span>terminos-confirmacion<br><small>La reserva exige aceptar Safari</small></span></div>
  <div class="mascot-frame director">{image(guia['parque'], 'mascot', 'Guía conduce la demo')}</div>
''', "La demostración se recorre de izquierda a derecha. Cada pantalla permite señalar qué rama define las reglas que el usuario observa."))

slides.append(slide("Qué demuestra cada pantalla", "evidence-map", f'''
  <h1>Guía cambia con la actividad</h1>
  <div class="variant v1">{image(guia['parque'], 'mascot', 'Guía del parque')}<b>Parque</b></div>
  <div class="variant v2">{image(guia['safari'], 'mascot', 'Guía Safari')}<b>Safari</b></div>
  <div class="variant v3">{image(guia['tirolesa'], 'mascot', 'Guía Tirolesa')}<b>Tirolesa</b></div>
  <div class="variant v4">{image(guia['palestra'], 'mascot', 'Guía Palestra')}<b>Palestra</b></div>
  <div class="variant v5">{image(guia['jardineria'], 'mascot', 'Guía Jardinería')}<b>Jardinería</b></div>
  <div class="branch-strip">La mascota funciona como narradora y confirma visualmente el contexto de cada prueba</div>
''', "Esta pantalla concentra el contrato observable entre el frontend y las reglas desarrolladas en las ramas TDD."))

slides.append(slide("El comprobante final", "ticket", f'''
  <h1>Resultado observable</h1>
  <div class="screen-frame receipt">{image(shots['comprobante'], 'screen', 'Comprobante de reserva')}</div>
  <div class="qr-note">QR GENERADO<br><small>verificado por test</small></div>
  <div class="mail-note">CORREO<br><small>verificado con fake</small></div>
  <div class="cupos-note">CUPO<br><small>reservado sin sobreventa</small></div>
  <div class="mascot-frame confirmed">{image(confirmed, 'mascot', 'Guía confirma la reserva')}</div>
''', "El comprobante sintetiza el flujo: una actividad válida, participantes válidos, cupos reservados y confirmación preparada."))

slides.append(slide("Qué está integrado y qué no", "boundaries", f'''
  <h1>Límite de la integración</h1>
  <div class="island frontend-island"><b>FRONTEND</b><p>Flujo completo, Guía, validaciones de interfaz, comprobante y almacenamiento local.</p></div>
  <div class="bridge"><span>CONTRATOS<br>PENDIENTES</span></div>
  <div class="island backend-island"><b>BACKEND POR RAMAS</b><p>Reglas probadas para turnos, términos, participantes, cupos, concurrencia y notificaciones.</p></div>
  <div class="honesty">La demo visual no reemplaza la integración: muestra el destino al que deben conectarse los módulos.</div>
  <div class="mascot-frame gardener">{image(guia['jardineria'], 'mascot', 'Guía jardinero')}</div>
''', "Cierre honesto sobre el alcance actual: el frontend usa datos locales; los módulos backend tienen evidencia TDD pero todavía necesitan un contrato común y endpoints."))

slides.append(slide("Una regla, una prueba, un cambio mínimo", "closing", f'''
  <h1>Una regla.<br>Una prueba.<br>Un cambio mínimo.</h1>
  <p>Después, mejorar el diseño sin perder el verde.</p>
  <div class="question">¿QUÉ CASO PROBARÍAMOS AHORA?</div>
  <div class="mascot-frame finale">{image(gesture['cheer'], 'mascot', 'Guía cierra la presentación')}</div>
''', "Abrir preguntas. Invitar al profesor a proponer el próximo caso y explicar cómo entraría al ciclo."))


css = f'''
@font-face{{font-family:Fredoka;src:url({fredoka}) format('woff2');font-weight:600}}
@font-face{{font-family:Nunito;src:url({nunito}) format('woff2');font-weight:700}}
*{{box-sizing:border-box}}html,body{{margin:0;background:#263c34}}.slide{{position:relative;width:1920px;height:1080px;overflow:hidden;background:#fff8e8;color:#263c34;font-family:Nunito,Arial,sans-serif}}
.slide:after{{content:"";position:absolute;inset:0;pointer-events:none;opacity:.08;background-image:radial-gradient(#263c34 1.4px,transparent 1.4px);background-size:11px 11px}}
.nature-overlay{{position:absolute;inset:0;width:100%;height:100%;background-repeat:no-repeat;background-size:cover;background-position:center;z-index:1;opacity:.23;pointer-events:none}}.nature-jungle .nature-overlay{{background-image:url({nature['jungle']})}}.nature-safari .nature-overlay{{background-image:url({nature['safari']})}}.nature-rock .nature-overlay{{background-image:url({nature['rock']})}}.nature-garden .nature-overlay{{background-image:url({nature['garden']})}}.cover .nature-overlay,.closing .nature-overlay{{opacity:.36}}.journey .nature-overlay,.demo .nature-overlay{{opacity:.29}}.evidence-map .nature-overlay{{opacity:.18}}
h1{{position:absolute;left:110px;top:68px;margin:0;z-index:8;font:600 76px/1 Fredoka,Arial,sans-serif;letter-spacing:-.03em;max-width:1500px;text-align:left}}p{{margin:0}}.logo{{position:absolute;left:86px;bottom:47px;width:88px;height:88px;object-fit:contain;z-index:20}}
.mascot-frame{{position:absolute;z-index:9;border:7px solid #263c34;background:#f8dc9a;border-radius:48% 52% 44% 56%;box-shadow:14px 16px 0 #263c3430;overflow:hidden;padding:18px}}.mascot{{width:100%;height:100%;object-fit:contain;display:block}}.screen-frame{{position:absolute;border:7px solid #263c34;background:#fff8e8;border-radius:24px;box-shadow:14px 16px 0 #263c3430;overflow:hidden;padding:8px;z-index:5}}.screen{{width:100%;height:100%;object-fit:cover;display:block;border-radius:14px}}
.codecard{{position:absolute;background:#20362f;color:#fff8e8;border:7px solid #263c34;border-radius:26px;box-shadow:13px 14px 0 #263c3430;padding:30px;z-index:6;text-align:left}}.codecard label{{display:block;color:#facb68;font:600 24px Fredoka;margin:0 0 12px 0;letter-spacing:.02em;text-align:left}}pre{{margin:0;font:700 22px/1.38 Consolas,'Courier New',monospace;white-space:pre-wrap;text-align:left}}
.cover{{background:#f4c480}}.cover .sun{{position:absolute;width:980px;height:980px;border-radius:50%;background:#f47b38;border:10px solid #263c34;right:-180px;top:-170px}}.cover h1{{font-size:132px;top:155px;left:105px;line-height:.92}}.cover h1 span{{color:#fff8e8;text-shadow:8px 8px 0 #263c34}}.cover .lead{{position:absolute;left:110px;top:650px;font:600 37px Fredoka}}.cover .badge{{position:absolute;left:115px;top:770px;border:7px double #263c34;border-radius:50%;padding:28px;transform:rotate(-9deg);font:600 27px/1 Fredoka;text-align:center;background:#fff8e8}}.cover .hero{{right:70px;top:100px;width:760px;height:860px;background:#b9dfbb;transform:rotate(4deg)}}
.journey{{background:#e8f0dc}}.journey h1{{font-size:79px}}.mapline{{position:absolute;left:170px;right:150px;top:360px;height:260px;border-top:18px dashed #ca7442;border-radius:50%;transform:rotate(3deg)}}.stop{{position:absolute;top:300px;width:205px;height:195px;border:6px solid #263c34;border-radius:50%;background:#fff8e8;text-align:center;padding-top:25px;z-index:5;transform:rotate(-7deg)}}.stop b{{display:block;font:600 55px/.9 Fredoka;color:#e0633a}}.stop span{{font-size:24px;line-height:1}}.s1{{left:110px}}.s2{{left:385px;top:405px;background:#f7d38b;transform:rotate(5deg)}}.s3{{left:670px;top:305px;background:#a9d9bf}}.s4{{left:955px;top:425px;background:#f3b19c;transform:rotate(6deg)}}.s5{{left:1240px;top:315px;background:#9dd7d3}}.s6{{left:1515px;top:420px;background:#dfc39e}}.journey-shot{{left:125px;top:650px;width:1010px;height:330px;transform:rotate(-2deg)}}.map-mascot{{right:90px;bottom:55px;width:520px;height:390px;background:#c9e6b9;transform:rotate(5deg)}}
.cycle{{background:#f5e2c2}}.cycle h1{{font-size:94px}}.phase{{position:absolute;top:290px;width:510px;height:520px;border:8px solid #263c34;border-radius:40% 60% 44% 56%;padding:90px 55px 40px;text-align:center;box-shadow:15px 17px 0 #263c3430;z-index:4}}.phase strong{{font:600 88px/.9 Fredoka}}.phase p{{font-size:30px;line-height:1.18;margin-top:28px}}.phase span{{position:absolute;right:30px;top:20px;font:600 63px Fredoka}}.red{{left:90px;background:#eb735f;color:#fff8e8;transform:rotate(-5deg)}}.green{{left:705px;background:#88c69b;transform:rotate(5deg)}}.refactor{{left:1320px;background:#71c5c0;transform:rotate(-4deg)}}.refactor strong{{font-size:61px}}.tape{{position:absolute;left:360px;bottom:95px;background:#263c34;color:#fff8e8;padding:17px 40px;font:600 35px Fredoka;transform:rotate(-3deg);z-index:10}}.think{{right:35px;bottom:16px;width:315px;height:270px;background:#f8dc9a}}
.g1{{background:#e3f0d9}}.g1 h1{{font-size:86px}}.clock{{position:absolute;left:95px;top:250px;width:350px;height:290px;border:8px solid #263c34;border-radius:50%;background:#f9d481;text-align:center;padding-top:58px;transform:rotate(-8deg)}}.clock b{{display:block;font:600 78px Fredoka}}.clock span{{font-size:27px;color:#c54f31}}.g1 .test{{left:480px;top:235px;width:960px;height:305px}}.g1 .impl{{left:190px;top:590px;width:1010px;height:240px}}.sticker{{position:absolute;left:1240px;top:585px;width:320px;height:170px;border:7px double #263c34;border-radius:50%;background:#72b993;text-align:center;padding-top:35px;transform:rotate(8deg);font:600 34px/1 Fredoka}}.sticker small{{font:700 18px Nunito}}.proof{{position:absolute;left:210px;top:870px;font-size:27px}}.safari{{right:40px;top:205px;width:390px;height:340px;background:#aedcb8}}
.g2{{background:#f8e7d4}}.g2 h1{{font-size:82px}}.contract{{position:absolute;left:100px;top:260px;width:650px;height:310px;border:7px dashed #263c34;background:#fff8e8;padding:35px;transform:rotate(-4deg);box-shadow:14px 15px 0 #d48d61}}.contract b{{font:600 36px Fredoka}}.contract p{{font-size:26px;margin:45px 0}}.contract div{{color:#d85035;font:600 27px Fredoka}}.failure{{position:absolute;left:770px;top:280px;width:350px;height:240px;border:8px solid #b74735;color:#b74735;border-radius:50%;text-align:center;padding-top:45px;transform:rotate(8deg);font:600 52px/.9 Fredoka}}.failure small{{font:700 19px/1.1 Nunito}}.g2 .test{{left:120px;top:650px;width:800px;height:240px}}.g2 .impl{{left:950px;top:620px;width:700px;height:270px}}.stamp{{position:absolute;right:75px;top:240px;border:7px double #263c34;border-radius:50%;background:#f6c66e;padding:25px;transform:rotate(12deg);font:600 26px/1 Fredoka;text-align:center}}.point{{right:70px;bottom:35px;width:300px;height:260px;background:#aed9ca}}
.g3{{background:#dcf0ef}}.g3 h1{{font-size:78px}}.capacity{{position:absolute;left:105px;top:245px;width:270px;height:260px;border:8px solid #263c34;border-radius:40%;background:#f5cb69;text-align:center;padding:35px;transform:rotate(-8deg)}}.capacity span{{display:block;font-size:29px}}.capacity b{{font:600 118px/.9 Fredoka}}.people{{position:absolute;left:420px;top:300px;font-size:61px;letter-spacing:12px}}.people i{{font-style:normal;color:#e35639;text-decoration:line-through}}.g3 .test{{left:400px;top:410px;width:1000px;height:235px}}.g3 .impl{{left:110px;top:690px;width:780px;height:200px}}.passport{{position:absolute;top:700px;width:225px;height:150px;border:6px solid #263c34;border-radius:20px;background:#f0ab8e;text-align:center;padding:20px;transform:rotate(-6deg);font-size:20px}}.passport b{{font:600 36px Fredoka}}.p1{{left:930px}}.p2{{left:1170px;background:#efcf77;transform:rotate(6deg)}}.p3{{left:1410px;background:#acd4aa}}.refactor-note{{position:absolute;left:390px;bottom:90px;font-size:24px}}.tirolesa{{right:35px;top:175px;width:400px;height:360px;background:#bce5e5}}
.g4{{background:#f4ddcb}}.g4 h1{{font-size:80px}}.envelope{{position:absolute;left:90px;top:245px;width:720px;height:300px;border:8px solid #263c34;background:#fff8e8;padding:28px;transform:rotate(-4deg);box-shadow:14px 16px 0 #ca7c54}}.envelope div{{border-bottom:3px solid #263c34;padding-bottom:14px;font-size:22px}}.envelope b{{display:block;margin-top:45px;font:600 38px Fredoka}}.envelope p{{font-size:25px}}.envelope span{{position:absolute;right:35px;bottom:30px;border:5px solid #c44e35;color:#c44e35;border-radius:50%;padding:17px;transform:rotate(14deg);font:600 28px Fredoka}}.g4 .test{{left:120px;top:620px;width:940px;height:310px}}.g4 .impl{{left:1030px;top:480px;width:710px;height:265px}}.decision{{position:absolute;left:1090px;top:790px;width:510px;background:#efba74;border:6px solid #263c34;padding:18px 24px;transform:rotate(3deg);font:600 28px Fredoka}}.decision small{{font:700 19px/1.1 Nunito}}.cheer{{right:35px;bottom:30px;width:300px;height:250px;background:#bbe0ba}}
.g5{{background:#e9ead4}}.g5 h1{{font-size:78px}}.race{{position:absolute;top:245px;width:250px;height:160px;border:7px solid #263c34;border-radius:50%;text-align:center;padding:25px;background:#f0ad88;transform:rotate(-7deg)}}.race b{{font:600 65px/.8 Fredoka}}.race span{{display:block;font-size:24px}}.race.a{{left:100px}}.race.b{{left:380px;background:#91c8bd;transform:rotate(7deg)}}.finish{{position:absolute;left:685px;top:250px;border:8px double #263c34;background:#f4cf6f;padding:22px 45px;transform:rotate(-3deg);text-align:center;font-size:24px}}.finish b{{font:600 50px Fredoka}}.g5 .test{{left:100px;top:500px;width:990px;height:330px}}.g5 .impl{{left:1120px;top:425px;width:650px;height:300px}}.result{{position:absolute;left:280px;top:875px;background:#6fb48c;color:#fff8e8;border:6px solid #263c34;padding:15px 35px;font:600 30px Fredoka;transform:rotate(-2deg)}}.palestra{{right:45px;bottom:35px;width:360px;height:300px;background:#e8c5b0}}
.deadlock{{background:#d8ece6}}.deadlock h1{{font-size:91px}}.before,.after{{position:absolute;top:270px;width:700px;height:570px;border:8px solid #263c34;border-radius:30px;padding:35px;box-shadow:15px 17px 0 #263c3430}}.before{{left:100px;background:#efa28e;transform:rotate(-3deg)}}.after{{right:100px;background:#9ed0a8;transform:rotate(3deg)}}.before b,.after b{{font:600 45px Fredoka}}.before pre,.after pre{{color:#263c34;font-size:24px;margin-top:30px}}.before span,.after span{{position:absolute;left:35px;bottom:30px;font:600 25px Fredoka}}.arrow{{position:absolute;left:880px;top:480px;font:600 85px Fredoka}}.lock-shape{{position:absolute;left:850px;top:680px;font-size:95px;transform:rotate(-9deg)}}.mechanic{{right:30px;bottom:20px;width:290px;height:250px;background:#f6d37f}}
.demo{{background:#f4dfbd}}.demo h1{{font-size:83px}}.film{{position:absolute;top:265px;width:520px;height:540px;border:10px solid #263c34;background:#263c34;padding:10px;transform:rotate(-4deg);z-index:5}}.film img{{height:445px;object-fit:cover;border-radius:0}}.film span{{display:block;color:#fff8e8;font:600 22px Fredoka;padding:13px 8px}}.f1{{left:80px}}.f2{{left:665px;transform:rotate(4deg)}}.f3{{left:1250px;transform:rotate(-3deg)}}.director{{right:50px;bottom:30px;width:290px;height:250px;background:#b9deac}}
.evidence-map{{background:#e5efe0}}.evidence-map h1{{font-size:86px}}.bigshot{{left:365px;top:235px;width:1190px;height:700px}}.callout{{position:absolute;width:300px;border:6px solid #263c34;border-radius:28px;padding:18px;background:#fff8e8;z-index:7;box-shadow:8px 9px 0 #263c3430}}.callout b{{font:600 26px Fredoka;color:#d35e3a}}.callout span{{display:block;font-size:20px;line-height:1.1}}.c1{{left:55px;top:260px;transform:rotate(-5deg)}}.c2{{left:50px;top:560px;transform:rotate(5deg)}}.c3{{right:45px;top:290px;transform:rotate(4deg)}}.c4{{right:45px;top:610px;transform:rotate(-5deg)}}.branch-strip{{position:absolute;left:380px;bottom:65px;background:#263c34;color:#fff8e8;padding:13px 30px;font-size:20px;z-index:8}}
.ticket{{background:#f7e5cf}}.ticket h1{{font-size:78px}}.receipt{{left:125px;top:235px;width:1190px;height:730px;transform:rotate(-2deg)}}.qr-note,.mail-note,.cupos-note{{position:absolute;right:90px;width:390px;border:7px solid #263c34;border-radius:50%;padding:28px;text-align:center;font:600 31px/1 Fredoka;z-index:8;transform:rotate(6deg)}}.qr-note{{top:250px;background:#efc86d}}.mail-note{{top:470px;background:#9bd0c1;transform:rotate(-5deg)}}.cupos-note{{top:690px;background:#efa58c}}.qr-note small,.mail-note small,.cupos-note small{{font:700 18px Nunito}}.confirmed{{right:25px;bottom:20px;width:330px;height:280px;background:#b6ddaa}}
.boundaries{{background:#e2ead4}}.boundaries h1{{font-size:88px}}.island{{position:absolute;top:275px;width:650px;height:490px;border:9px solid #263c34;border-radius:45% 55% 48% 52%;padding:105px 80px;text-align:center;box-shadow:17px 19px 0 #263c3430}}.island b{{font:600 53px Fredoka}}.island p{{font-size:28px;line-height:1.18;margin-top:28px}}.frontend-island{{left:90px;background:#f2c27d;transform:rotate(-4deg)}}.backend-island{{right:90px;background:#89c5ae;transform:rotate(4deg)}}.bridge{{position:absolute;left:775px;top:430px;width:370px;height:120px;border-top:16px dashed #d55f3b;text-align:center;padding-top:25px;transform:rotate(-3deg)}}.bridge span{{font:600 24px Fredoka}}.honesty{{position:absolute;left:350px;bottom:95px;width:1220px;background:#263c34;color:#fff8e8;padding:18px 40px;font-size:26px;text-align:center;transform:rotate(-1deg)}}.gardener{{right:20px;bottom:15px;width:300px;height:260px;background:#f0d993}}
.closing{{background:#f2bf7d}}.closing:before{{content:"";position:absolute;right:-210px;top:-210px;width:1050px;height:1050px;background:#e2633c;border:10px solid #263c34;border-radius:50%}}.closing h1{{font-size:121px;top:160px;left:110px;max-width:1000px}}.closing p{{position:absolute;left:115px;top:650px;font:600 39px Fredoka}}.question{{position:absolute;left:115px;top:780px;background:#263c34;color:#fff8e8;padding:20px 35px;border-radius:80px;font:600 37px Fredoka;transform:rotate(-3deg)}}.finale{{right:70px;top:105px;width:700px;height:800px;background:#b8dcae;transform:rotate(5deg)}}
.journey h1{{font-size:76px}}.cycle h1{{font-size:82px}}.g1 h1,.g2 h1,.g3 h1,.g4 h1,.g5 h1,.deadlock h1,.demo h1,.ticket h1,.boundaries h1{{font-size:80px}}.closing h1{{font-size:112px;line-height:1}}
.demo .film{{top:245px;height:570px}}.demo .film img{{height:440px}}.demo .film span{{font:600 22px/1.1 Fredoka;padding:12px 8px}}.demo .film small{{font:700 17px/1.1 Nunito;color:#f4d58b}}
.evidence-map h1{{font-size:80px}}.variant{{position:absolute;top:260px;width:325px;height:560px;border:7px solid #263c34;border-radius:44% 56% 48% 52%;padding:24px 18px 60px;background:#fff8e8;box-shadow:12px 14px 0 #263c3430;z-index:5;transform:rotate(-5deg)}}.variant .mascot{{height:100%;object-fit:contain}}.variant b{{position:absolute;bottom:24px;left:0;width:100%;text-align:center;font:600 28px Fredoka}}.v1{{left:80px;background:#c6e2b8}}.v2{{left:430px;background:#b3debd;transform:rotate(4deg)}}.v3{{left:780px;background:#b9e4e5;transform:rotate(-3deg)}}.v4{{left:1130px;background:#edc7b2;transform:rotate(5deg)}}.v5{{left:1480px;background:#f2d993;transform:rotate(-4deg)}}.evidence-map .branch-strip{{left:310px;bottom:75px;width:1300px;padding:16px 30px;font-size:23px;text-align:center;transform:rotate(-1deg)}}
.g1 .test{{transform:rotate(1deg)}}.g1 .impl{{background:#1e6658;transform:rotate(-1deg)}}
.g2 .test{{background:#fff8e8;color:#263c34;border-style:dashed;transform:rotate(-2deg)}}.g2 .impl{{background:#277a71;transform:rotate(2deg)}}
.g3 .test{{background:#20443e;transform:rotate(1deg)}}.g3 .impl{{background:#fff8e8;color:#263c34;border-style:dashed;transform:rotate(-2deg)}}
.g4 .test{{background:#fff8e8;color:#263c34;border-color:#c54f31;transform:rotate(-1deg)}}.g4 .impl{{background:#245d54;transform:rotate(2deg)}}
.g5 .test{{background:#253f35;transform:rotate(-1deg)}}.g5 .impl{{background:#f3cf72;color:#263c34;transform:rotate(2deg)}}
'''

html = ('<!doctype html><html lang="es"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=1920,initial-scale=1">'
        f'<style>{css}</style></head><body>{"".join(slides)}</body></html>')
OUT.write_text(html, encoding="utf-8")
print(OUT)
print(f"{len(slides)} slides; {OUT.stat().st_size / 1024 / 1024:.2f} MB")
