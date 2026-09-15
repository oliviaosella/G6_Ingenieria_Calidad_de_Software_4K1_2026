# Descripción del dominio

## Contexto

Los dueños del bioparque "EcoHarmony Park" están evaluando el desarrollo de una aplicación móvil (Android, iOS) ya que la cantidad de visitantes anuales aumentaron significativamente al igual que los avances tecnológicos.

La aplicación tiene como objetivo mejorar la experiencia de los visitantes al proporcionar información útil y enriquecedora sobre:

- Las exhibiciones
- Los horarios de alimentación de los animales
- Los senderos para caminar
- Otros aspectos del parque, como la autogestión al momento de realizar la compra de entradas

Para relevar la idea se entrevistó a **Miguel Rodríguez**, uno de los propietarios de EcoHarmony Park. A continuación se transcribe la conversación.

## Entrevista con Miguel Rodríguez

> [!question] El Doce — ¿En qué consiste la aplicación?
> ¡Hola! Estoy aquí en el hermoso bioparque "EcoHarmony Park" con el Sr. Rodríguez, para hablar sobre una emocionante novedad: ¡una nueva aplicación móvil que mejorará la experiencia de los visitantes aquí en el parque! ¿Me podrías contar brevemente en qué consiste la aplicación?

**Miguel:** ¡Hola! Gracias por tomarte el tiempo para hablar conmigo. Estoy encantado de compartir más detalles sobre la idea de nuestra aplicación. En primer lugar, ofrecerá a los visitantes mapas interactivos que les ayudarán a explorar el parque de manera más eficiente. Asimismo, proporcionará información detallada sobre cada exhibición y horario de alimentación de cada especie que cuidamos. También se podrá autogestionar la compra de entradas al parque, pudiendo realizar directamente el pago a través de la pasarela de Mercado Pago, lo que permitirá agilizar el ingreso. Por último, los visitantes pueden inscribirse a las diferentes actividades diarias que posee el parque.

> [!question] El Doce — Horarios de alimentación
> Wow! Que interesante ¿Podrías explicarme cómo puede un visitante acceder a los horarios de alimentación a través de la aplicación?

**Miguel:** ¡Claro! Una vez que descarguen la aplicación y la abran, encontrarán una sección dedicada a "Horarios de Alimentación disponibles". Cada horario estará detallado de manera clara, indicando la especie, nombre del animal, edad, hora programada, sector del parque (terrestres, acuáticos o aéreos) y cuidador encargado (nombre y apellido). Por otra parte, aquellos que estén próximos a comenzar (faltando una hora) los mostraremos con un mensaje que diga: ¡Apúrate que ya comienza! Es importante considerar que los horarios se mostrarán en orden, comenzando con los más próximos a la fecha actual y extendiéndose hasta una semana en el futuro. Para que sea más amigable la interfaz pensamos en proporcionar la posibilidad de filtrar por la fecha en la que el visitante estará en el parque y que se visualicen únicamente los horarios correspondientes a la misma. Además, en una versión posterior, los visitantes podrán configurar notificaciones para recibir recordatorios de los horarios de alimentación que deseen seguir de cerca.

> [!question] El Doce — Mapa interactivo
> ¡Eso suena muy útil! ¡Al igual que el mapa interactivo! ¿Podrías comentarme cuáles serán los elementos y características del parque que estarán disponibles para visualizar en él? ¿Qué acciones podrán llevar a cabo los visitantes a través de esta herramienta?

**Miguel:** Este mapa ofrece una vista panorámica de todo el parque, dividido en sectores diferenciados por colores. Asimismo, el mapa contiene íconos informativos: "Inodoro" para identificar los baños distribuidos en el parque, una "Bolsa" para indicar los puntos de venta, y un "Micrófono" para el show especial del día. Los visitantes pueden hacer click en este último icono para obtener el nombre del show y su horario, en caso de que haya un show programado. En una futura mejora pensamos incluir en este mapa la ubicación del visitante en tiempo real.

> [!question] El Doce — Inscripción a actividades
> Para alguien como yo, con un sentido de la orientación no muy desarrollado, suena como una herramienta imprescindible, ¡jaja! ¿Hay otros aspectos del parque que también planean ofrecer a través de la aplicación? ¿Habías mencionado la inscripción a las actividades, no es cierto?

**Miguel:** Si! me estaba olvidando de comentarlo. El parque ofrece la posibilidad de realizar actividades de una hora sumamente enriquecedoras para los visitantes, entre las que se encuentran "Tirolesa", "Safari", "Palestra" y "Jardinería". Para poder realizar la inscripción deben seleccionar del conjunto de actividades la que desean realizar, eligiendo en primer lugar el horario y completando luego los datos del visitante: nombre, DNI, edad y talla de vestimenta si la actividad lo demanda. Finalmente, para concluir el proceso de inscripción, pedimos a los visitantes que acepten los términos y condiciones específicos de la actividad en la que participarán, enviando el resumen de la inscripción con un QR al mail del visitante. Nos interesa gestionar la inscripción de las actividades porque tienen cupos limitados y es muy útil para planificarlas con anterioridad según los inscriptos que tengamos.

> [!question] El Doce — Compra de entradas
> Para finalizar esta pequeña entrevista, ¿Podrías explicarme el proceso de compra de entradas a través de la app?

**Miguel:** !Pero claro! Para realizar la compra de entradas el visitante debe registrarse en la aplicación, ingresando un mail y una contraseña. A continuación, debe ingresar a la sección "Comprar entradas" y allí indicar la fecha de visita deseada, la cantidad de entradas requeridas (que no puede superar las 10) y la edad de cada visitante. Finalmente, el sistema mostrará el monto total y se debe seleccionar la forma de pago: efectivo en caso de querer pagar en boletería o con tarjeta, donde se redirigirá al usuario a la página de Mercado Pago para completar el proceso de forma segura. Finalmente, recibirán un mensaje de confirmación vía mail y sus entradas serán verificadas al momento de ingresar al parque. La posibilidad de comprar las entradas mediante la aplicación nos parece fundamental para comenzar a probar la recepción de la aplicación, incluyendo el pago electrónico ya que creemos que será el más usado.

> [!question] El Doce — Mantenimiento de la información
> ¡Muy claro! Parece que la aplicación requiere mucha atención. ¿Tienen previsto contratar personal adicional para mantener actualizados los horarios, las actividades y todo lo que implica?

**Miguel:** No, no hay problema en ese aspecto. Planeamos gestionar esa tarea por fuera de la aplicación, a través de nuestro equipo de administradores, que se encargará de mantener todo actualizado.

**El Doce:** Ah, entiendo. ¡Gracias por compartir todos estos emocionantes detalles! Más adelante coordinamos otra nota para ver esta aplicación en funcionamiento.

--- 
## Hipótesis / IDEA del MVP
Si le damos a los visitantes de EcoHarmony Park la posibilidad de autogestionar su visita desde una app mobile (compra de entradas, consulta de mapa interactivo, horarios de alimentación e inscripción a actividades), van a adoptarla y eso va a mejorar su experiencia en el parque.

## Listado de frases verbales (US identificadas)
1. Registrarme en la aplicación
2. Comprar entradas al parque
3. Visualizar mapa interactivo del parque
4. Visualizar horarios de alimentación
5. Visualizar actividades especiales
6. Inscribirme a una actividad especial
7. Configurar recordatorios de horarios _(mencionada explícitamente como "una versión posterior")_

## Alcance del MVP

### Incluye
- Registrarme en la aplicación
- Comprar entradas al parque (efectivo y tarjeta vía Mercado Pago)
- Visualizar mapa interactivo del parque
- Visualizar horarios de alimentación
- Visualizar actividades especiales
- Inscribirme a una actividad especial

### No incluye
- Configurar y recibir recordatorios de horarios
- Ubicación del visitante en tiempo real en el mapa
- Consultar mis inscripciones
- Modificar / consultar mi usuario
- Carga y administración de actividades (se gestiona fuera de la app, por el equipo de administradores)
### Justificación del alcance para el MVP

El recorte se hizo en función de qué funcionalidades son necesarias para poner a prueba la hipótesis: que la autogestión de la visita (comprar entradas, consultar el mapa y los horarios, inscribirse a actividades) es adoptada por los visitantes y mejora su experiencia en el parque. Cada ítem incluido representa una acción de autogestión distinta que el visitante puede resolver por su cuenta, sin depender del personal del parque que es justamente lo que la hipótesis busca validar.

Lo que se dejó afuera son mejoras de comodidad que no hacen falta para validar esa hipótesis central, o funcionalidad que la propia entrevista ubica fuera del alcance actual:

- **Recordatorios de horarios:** Miguel lo menciona explícitamente como "una versión posterior".
- **Ubicación en tiempo real:** también aparece como una mejora futura del mapa interactivo.
- **Consultar mis inscripciones / modificar mi usuario:** son comodidades sobre datos ya cargados, no funcionalidad que el visitante necesite para autogestionar su visita por primera vez.
- **Carga y administración de actividades:** Miguel aclara que esa tarea la resuelve el equipo de administradores por fuera de la aplicación, así que no es parte del producto que se le entrega al visitante.

---

## User Story completa: Comprar Entradas al Parque

**Frase verbal:** Comprar Entradas al Parque

**Sintaxis**

> Como visitante registrado, quiero comprar entradas al parque de forma que pueda agilizar mi ingreso al parque y evitar las filas en boletería.

**Criterios de aceptación**

- El visitante debe estar registrado para realizar la compra.
- Se debe indicar la fecha de visita deseada (fecha actual o futura).
- La cantidad de entradas solicitada no puede superar las 10 en una misma transacción.
- Se debe ingresar la edad de cada visitante incluido en la compra.
- El monto total se calcula y se muestra antes de seleccionar el método de pago.
- El visitante puede elegir entre pago en efectivo (a abonar en boletería) o pago con tarjeta, redirigiendo a Mercado Pago.
- Una vez confirmada la compra, el visitante recibe un mail de confirmación.
- Las entradas quedan asociadas a la compra y se verifican al momento del ingreso al parque.

**Pruebas de usuario**

- Probar comprar entrada con usuario registrado, pago en efectivo (pasa)
- Probar comprar entrada con usuario registrado, pago con tarjeta vía Mercado Pago (pasa)
- Probar comprar menos de 10 entradas, indicando edades de los visitantes, una fecha futura y un método de pago (pago)
- Probar comprar x cantidad de entradas y visualizar el monto total antes de seleccionar el método de pago (pasa)

- Probar intentar comprar sin estar registrado (no pasa)
- Probar solicitar más de 10 entradas en una misma transacción (no pasa)
- Probar intentar confirmar sin indicar la fecha de visita (no pasa)
- Probar intentar confirmar sin ingresar la edad de algún visitante (no pasa)
- Probar comprar entradas sin seleccionar un método de pago (no pasa)
## Estimación
**Story canónica (base):** Registrarme en la aplicación — 1 SP

**SP:** 5

**Esfuerzo:** Medio ya que además de las validaciones de los campos obligatorios (fecha, edad, método de pago) y el cálculo del monto total, hay que programar dos flujos de pago completos (efectivo y tarjeta vía Mercado Pago) y el disparo del mail de confirmación, son varios módulos que hay que orquestar para mejorar la experiencia del usuario y garantizar su correcto funcionamiento.

**Complejidad:** Alta debido a la integración con la API de Mercado Pago (armar la llamada, procesar la respuesta y manejar los distintos estados posibles de una transacción) es una pieza técnica que compleja de integrar, sumada a coordinar dos caminos de pago distintos y las validaciones de cada campo obligatorio.

**Incertidumbre:** media-alta ya que asegurar que el estado de la compra en el sistema propio quede correctamente sincronizado con la confirmación del pago externo (duplicados, timeouts, reintentos) es un riesgo real.

---
## User Story completa: Inscribirse a Actividad Especial

**Frase verbal:** Inscribirse a Actividad Especial

**Sintaxis**

> Como visitante, quiero inscribirme a una actividad para llevarla a cabo durante mi visita al parque, de forma que pueda garantizar un lugar en la misma.

**Criterios de aceptación**

- El visitante debe seleccionar una de las actividades disponibles (Tirolesa, Safari, Palestra, Jardinería).
- Se debe seleccionar el horario de la actividad antes de completar los datos del visitante.
- Se deben completar los datos del visitante: nombre, DNI y edad.
- Se debe ingresar la talla de vestimenta solo si la actividad lo requiere.
- No se puede completar la inscripción si la actividad no tiene cupo disponible en el horario elegido.
- El visitante debe aceptar los términos y condiciones específicos de la actividad para confirmar la inscripción.
- Una vez confirmada la inscripción, se envía un resumen con un código QR al mail del visitante.

**Pruebas de usuario**

- Inscribirse a una actividad con cupo disponible, completando horario, datos del visitante y aceptando los términos y condiciones (pasa)

- Intentar inscribirse a una actividad sin cupo disponible en el horario elegido (no pasa)
- Intentar confirmar sin seleccionar un horario (no pasa)
- Intentar confirmar sin completar los datos obligatorios del visitante (no pasa)
- Intentar confirmar sin ingresar la talla de vestimenta en una actividad que la requiere (no pasa)
- Intentar confirmar sin aceptar los términos y condiciones (no pasa)

#### Estimación
**Story canónica (base):** Registrarme en la aplicación — 1 SP

**SP:** 3

**Esfuerzo:** medio-bajo. Además de armar la tabla de inscripciones y el formulario de datos del visitante, hay que integrar dos piezas nuevas: la generación del QR con una librería aparte como "qrcode" y el armado del mail con el resumen con una libreria como "nodemailer", no es solo un registro simple, son varias piezas que hay que coordinar.

**Complejidad:** media. El control de cupo disponible para evitar sobreventa agrega una lógica de negocio de mayor complejidad, sumado a coordinar la generación del QR con el envío del mail.

**Incertidumbre:** media. El caso de inscripciones simultáneas compitiendo por el último cupo ya que el equipo nunca lo implementó antes.

---

> [!tip] Para la clase que viene --> TP3: Recircula tus prendas - Cuida el planeta
> - MVP completo
> - Identificación de los roles
> - Descripción completa y estimación de estas US:
>     - Enviar prendas para vender
>     - Seleccionar prendas para publicar
