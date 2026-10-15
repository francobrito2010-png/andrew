# PROMPT MAESTRO — Web premium con showroom 3D para un concesionario de coches

> Copia todo este documento en el chat de la IA que vaya a hacer el trabajo. Rellena primero el bloque **0. DATOS DE ENTRADA**. Todo lo demás es la especificación completa: no hace falta enseñarle ejemplos.

---

## 0. DATOS DE ENTRADA (rellenar antes de pegar)

```
NOMBRE_COMERCIAL      = [ej.: nombre del stand]
WEB_ACTUAL_CLIENTE    = [URL, o "no tiene"]
IDIOMA_WEB            = [ej.: portugués de Portugal (PT-PT)]
IDIOMA_CONMIGO        = [ej.: español, respuestas cortas]
TELEFONO              = [o "pendiente"]
WHATSAPP              = [solo dígitos con prefijo de país, o "pendiente"]
DIRECCION             = [o "pendiente"]
HORARIO               = [o "pendiente"]
REDES                 = [Facebook / Instagram URLs, o "pendiente"]
COLOR_ACENTO          = [hex de la marca; si no hay: #E8B84A dorado]
REPOSITORIO           = [usuario/repo de GitHub donde publicar]
FOTOS_DISPONIBLES     = [qué fotos reales de coches me vas a pasar]
REFERENCIAS_POSTER    = [imágenes de pósters de coche de referencia, si las hay]
```

---

## 1. ROL Y REGLAS DE TRABAJO

Eres un desarrollador front-end senior especializado en webs de automoción premium, experiencias interactivas tipo videojuego (selector de coche) y tratamiento de imagen para web. Trabajas de forma autónoma y entregas trabajo **publicado y verificado**, no teoría.

Reglas innegociables:
1. **No inventes datos reales.** Precios, km, años, teléfonos o direcciones que no conozcas van como `null` o como dato de ejemplo marcado con `"demo": true`, y lo dices. Las cifras técnicas de fábrica (cv, km/h, 0-100) solo si estás seguro; si no, márcalas para confirmar.
2. **Mira lo que haces.** Después de cada cambio visual, abre la página en un navegador sin interfaz (Playwright/Chromium), haz capturas a **375–390 px, 768 px y 1440 px**, míralas tú y corrige antes de entregar.
3. **Comprueba la consola:** cero errores de JavaScript y **sin scroll horizontal** (`document.documentElement.scrollWidth` igual al ancho de la ventana).
4. Si no puedes acceder a algo (una web bloqueada, Chrome no disponible, un permiso de GitHub), dilo en una línea, explica cómo lo resuelve el usuario y sigue con lo que no depende de ello.
5. Responde al usuario en `IDIOMA_CONMIGO`, en corto: qué hiciste, el enlace, qué falta. Manda capturas de cómo quedó.
6. Al terminar cada bloque: commit, push, pull request y publicación (ver §11).

---

## 2. ESTRUCTURA DE ARCHIVOS

```
/index.html            web principal (HTML + CSS + JS vanilla en un solo archivo)
/cars.json             coches del showroom
/cars/                 imágenes de coches sin fondo (.webp) + carpetas con ángulos para 360°
/assets/stand.webp     foto real de la fachada del stand (si existe)
/poster/index.html     página "Coleção" estilo póster
/poster/models.json    modelos de la página póster
/poster/img/           coches, bocetos y logos del póster
/poster/PROMPT.md      resumen de la especificación del póster
/tools/preparar_coche.py   herramienta para añadir coches desde fotos
/tools/requirements.txt    rembg[cpu], opencv-python-headless, pillow, numpy, scipy
/tools/README.md       instrucciones de uso de la herramienta (en IDIOMA_CONMIGO)
/README.md             explicación del proyecto + lista de datos DEMO a sustituir
```

Sin frameworks ni build. Sin dependencias externas salvo Google Fonts. Compatible con GitHub Pages (rutas relativas).

---

## 3. WEB PRINCIPAL — DISEÑO GLOBAL

**Tipografía:** Manrope (400–800) en toda la web.

**Tokens CSS en `:root`** (tema oscuro, por defecto):
`--bg #0b0b0d`, `--ink #f2eee6` (blanco roto), `--muted #9a968e`, `--ink-2 #c9c4ba`, `--line rgba(255,255,255,.08)`, `--line-2 rgba(255,255,255,.14)`, `--line-3 rgba(255,255,255,.22)`, `--surface #121316`, `--card-top #141519`, `--card-bot #0e0f12`, `--media-top #1b1c20`, `--media-bot #111215`, `--glass rgba(20,20,23,.6)`, `--header-bg rgba(11,11,13,.62)`, `--accent COLOR_ACENTO`, `--accent-ink #1b1404`, `--accent-glow rgba(acento,.6)`, `--led #ffbf5e`, `--wa #25D366`.
**Ningún color fijo fuera de estas variables**: todo debe cambiar con el tema.

**Tamaños del escenario (mobile-first):**
- Móvil: `--car-w: 90vw`, `--stage-h: max(300px, car-w × .92)`.
- ≥700 px: `--car-w: 72vw`, `--stage-h: car-w × .78`.
- ≥1024 px: `--car-w: min(60vw, 920px, 92vh)`, `--stage-h: car-w × .66`.
- `--floor-y: 24%`: altura del suelo donde se apoya el coche.

**Cabecera fija** (56 px, semitransparente con `backdrop-filter: blur`):
- Izquierda: logo de texto (nombre en mayúsculas espaciadas y debajo una palabra pequeña en color acento).
- Centro (≥900 px): menú Showroom · Stock · Serviços · O stand · Coleção · Contacto.
- Derecha (≥1100 px): teléfono, botón con borde "Agendar visita", iconos de Facebook e Instagram.
- Siempre: botón de tema sol/luna y menú hamburguesa en móvil (desplegable con los mismos enlaces y el teléfono).

**Botones flotantes** fijos abajo a la derecha: WhatsApp (verde) y Llamar. En móvil, el bloque de botones principales lleva `padding-right: 66px` para que no quede tapado por ellos.

---

## 4. SHOWROOM 3D (portada)

### 4.1 Escena (todo con CSS, sin imágenes de fondo)
- **Pared:** degradado grafito `#131417 → #1c1d21 → #26272b` con juntas verticales cada 12,5 % (líneas de 1 px al 2,8 % de opacidad).
- **Línea LED** en el techo (2 px, degradado ámbar con brillo `box-shadow`) y un halo radial cálido debajo.
- **Suelo pulido** (38 % inferior): degradado oscuro, un reflejo difuso del LED y un foco radial suave sobre el coche.
- **Viñeta** radial en los bordes.

### 4.2 Plataforma giratoria
- Disco circular de diámetro `car-w × 1.04`, con `perspective` y `rotateX(78deg)`.
- Fondo con radios (`repeating-conic-gradient`) y aro fino de color acento con brillo.
- Su centro debe quedar bajo las ruedas: `bottom: calc(floor-y − car-w × .47)`.
- Gira despacio (4°/s) con un bucle `requestAnimationFrame` y recibe un impulso de unos 55° en cada cambio de coche. En el cambio, el aro hace un destello (opacidad 0 → .9 → 0 en 700 ms).

### 4.3 Coches
- **Coche activo:** el `.car` mide `car-w × car-w/2.3` y se centra con `margin-left` negativo, para dejar `transform` libre para las animaciones.
- La imagen va con `object-fit: contain` y `object-position: bottom`: el coche se apoya por las ruedas.
- **Sombra de contacto:** pseudo-elemento con un degradado radial negro.
- **Reflejo:** copia de la imagen con `scaleY(-1)`, opacidad .22 y máscara degradada.
- **Respiración:** escala de 1 a 1.01 en 4,5 s, en bucle alterno.
- **Coches laterales** (anterior y siguiente): `translateX(±car-w × .66) translateY(-14%) scale(.52)` con `filter: blur(3px) brightness(.38) saturate(.6)`.
- **Imagen que falta:** se muestra una silueta SVG genérica teñida con el campo `cor` del coche; nunca se rompe el diseño.
- **Precarga** del coche anterior, del siguiente y del que va después.

### 4.4 Interacción
- **Swipe con Pointer Events** en el escenario, con `touch-action: pan-y` para no bloquear el scroll vertical.
  - Decide el eje tras 8 px: si es vertical, suelta el gesto.
  - El coche sigue al dedo (con una rotación mínima) y los laterales se desplazan a 0,35×.
  - Al soltar, cambia de coche si se arrastró más del 20 % del ancho o si la velocidad pasa de 0,45 px/ms. Si no, vuelve con rebote (keyframes `dx → −0.12dx → 0.04dx → 0`, 460 ms).
- **Otros controles:** flechas laterales (con `aria-label`), teclas ← → y fila de miniaturas (la activa se resalta y se centra con `scrollTo`, nunca con `scrollIntoView`, que mueve la página).
- **Bucle infinito**, saltando por el camino más corto.
- **Bloqueo de entradas** durante la transición.

### 4.5 Transición entre coches (Web Animations API, ~770 ms)
- **Salida:** 3 clones del coche (opacidades 1, .38 y .16, con 40 ms de desfase entre ellos) aceleran hacia un lado, de `translateX(fromDx)` a `−dir × ancho × 1.2`, con `scaleX(1.1)`, `blur(14px)` y `easing cubic-bezier(.5,0,.75,.2)`. Los clones se borran al terminar.
- **Laterales:** se desvanecen (160 ms), cambian de imagen y vuelven a aparecer al final.
- **Entrada:** el coche llega desde el lado contrario, frena y "aterriza".
  - Keyframes: `{dir·W·.95, −8px, scale .94, blur 10, opacidad 0}` → `{dir·W·.22, −12px, blur 3}` → `{−dir·16px, 0, scale 1.01}` → `{dir·5px, −5px}` → `{0,0,1}`.
  - 680 ms con 90 ms de retardo, `easing cubic-bezier(.22,.9,.3,1)`.
- **`prefers-reduced-motion`:** fundido simple, sin blur, sin respiración y sin giro en reposo.
- **Animación de entrada al cargar** (< 1,5 s): el LED se enciende (`scaleX` 0→1) y el coche sube con desenfoque.

### 4.6 Botón 360°
- Si el coche tiene `frames` (lista de fotos de varios ángulos), el botón se activa con un pulso de color.
  - Al pulsarlo, **primero precarga todos los frames** (aviso "A carregar…").
  - Después da **una vuelta automática** (2,2 s) y luego arrastrar sobre el coche cambia de frame, a 1,2 anchos de pantalla por vuelta.
- Si el coche no tiene `frames`, el botón muestra "Em breve".
- **Error que hay que evitar:** al salir del modo 360°, la imagen estática solo se restaura si el coche no ha cambiado entretanto. Comprueba `cars[idx] === coche` dentro del `then` asíncrono; si no, sobrescribe la imagen del coche nuevo.

### 4.7 Panel bajo el coche
- Marca (pequeña, en color acento) y modelo (grande, peso 800), con una etiqueta del año que se oculta si está vacía (`:empty{display:none}`).
- Precio grande en color acento con formato `€ 45.900` (punto de miles hecho a mano, no `Intl`).
- 5 tarjetas con icono SVG en línea: Potência, Quilómetros, Combustível, Caixa, Ano. En móvil, cuadrícula de 6 columnas: 3 tarjetas de 2 columnas y 2 de 3.
- **Números que cuentan** desde el valor anterior hasta el nuevo (easeOutCubic, 750–900 ms, `tabular-nums`). Los textos aparecen con un fade-up escalonado (`animation-delay: i × 55 ms`).
- Si falta un dato (`null`): el precio muestra "Sob consulta" (en el idioma de la web) y el resto, "—".
- Región `aria-live` que anuncia el coche activo.

### 4.8 Llamadas a la acción
- **"Agendar visita"** (relleno de color acento): abre `https://wa.me/WHATSAPP?text=` con *"Olá! Tenho interesse no [Marca Modelo Ano] por [Preço]. Posso agendar uma visita?"*. Si falta el año o el precio, se quitan de la frase.
- **"Ver todo o stock"** (con borde): baja hasta la sección de stock.

---

## 5. SECCIONES DE LA WEB PRINCIPAL (debajo del showroom)

**Estilo común de las secciones:**
- `max-width: 1200px`, padding de 72 px en móvil y 104 px en escritorio.
- Separador: línea de 1 px con un degradado de color acento.
- Cabecera de sección: "kicker" (rótulo de 11 px en mayúsculas, espaciado .32em, color acento, precedido de una línea de 28 px) y título H2 `clamp(28px, 5vw, 46px)`, peso 600.
- **Revelado al hacer scroll** con IntersectionObserver: `opacity` y `translateY(24px)` a 0, en 0,8 s. Desactivado con movimiento reducido.

**Secciones:**
1. **Stock**
   - Chips para filtrar por marca ("Todas" + cada marca).
   - Cuadrícula de tarjetas: 1 columna, 2 a partir de 640 px, 3 a partir de 1024 px.
   - Cada tarjeta: imagen sobre fondo degradado con sombra de contacto, etiqueta "360°" si tiene frames, marca, modelo, una línea de datos (año · km · combustible · cv, omitiendo los vacíos), precio y dos botones de icono.
   - **Botón "ver en 3D":** sube al showroom y salta a ese coche.
   - **Botón de WhatsApp:** mensaje con ese coche.
   - Al pasar el ratón, la tarjeta sube 4 px y el borde toma el color acento.
2. **Em destaque**
   - El primer coche real (`demo: false`) que tenga varias fotos.
   - Imagen grande en un mini-escenario con línea LED, y miniaturas de sus ángulos.
   - Al lado: tabla de ficha técnica y botones "Pedir informações" (WhatsApp) y "Ver no showroom 3D".
3. **Serviços:** 4 tarjetas con icono (Financiamento, Retoma, Garantia, Documentação) y textos genéricos marcados como DEMO.
4. **O stand:** foto real de la fachada (con degradado y pie de foto), texto de presentación y 3 puntos clave. Textos genéricos marcados como DEMO.
5. **Contacto:**
   - Tarjetas de teléfono, dirección y horario.
   - Formulario: nombre (obligatorio), teléfono, coche de interés (desplegable con el stock) y mensaje.
   - Al enviar, **abre WhatsApp** con el mensaje ya redactado.
6. **Pie:** logo, enlaces y "© año NOMBRE_COMERCIAL".

---

## 6. TEMA CLARO / OSCURO

- Oscuro por defecto. El botón sol/luna cambia a **claro en blanco y negro**.
- `:root[data-theme="light"]` redefine las variables:
  - `--bg #f4f3f0`, `--ink #111113`, `--muted #6d6a64`, `--ink-2 #3d3b37`.
  - Líneas en negro con opacidad .08, .14 y .28.
  - Superficies blancas; `--accent #111113` con `--accent-ink #fff`.
- En claro, el showroom pasa a ser una **galería luminosa**:
  - Paredes y suelo claros, LED blanco.
  - Plataforma blanca con aro negro.
  - Laterales con `filter: blur(3px) contrast(.55) brightness(1.2) saturate(.5)`, reflejo a .16 y sombras de contacto más suaves.
- **Guardado:** la elección se guarda en `localStorage` (siempre dentro de `try/catch`). Un `<script>` en línea dentro del `<head>` la aplica **antes del primer pintado**, para que no haya parpadeo.
- Se actualiza también `meta theme-color`.
- La transición de colores (.4 s) solo se activa al hacer clic, nunca al cargar.

---

## 7. DATOS

**`cars.json`** — lista de objetos:
```json
{ "id": "marca-modelo-año", "marca": "", "modelo": "", "ano": 2021, "km": 18500,
  "combustivel": "Gasolina", "caixa": "Automática", "potencia_cv": 450, "preco": 139900,
  "imagem": "cars/id.webp", "cor": "#hex", "frames": ["cars/id/1.webp", "..."], "demo": false }
```
- `null` en `ano`, `km` o `preco` significa "Sob consulta" o "—".
- `cor` es el color de la silueta mientras no haya imagen.
- `"demo": true` marca los datos de ejemplo.

**Carga y contacto:**
- La web lee `cars.json` con `fetch` (con un timeout de 1,5 s). Si falla, usa `FALLBACK_CARS`, una copia idéntica dentro del JS (necesaria para abrir el archivo con `file://`).
- Objeto `STAND` al principio del script: nombre, telefone, whatsapp, morada, horario, facebook, instagram, demo. Los campos pendientes llevan el comentario `// DEMO`.

---

## 8. PÁGINA PÓSTER (`/poster/`)

### 8.1 Composición, de arriba abajo (fiel a un póster de coleccionista)
1. **Fondo papel** `#f1efeb` con un grano sutil (puntos radiales de 3 px).
2. **Barra superior:**
   - Izquierda: marca en mayúsculas espaciadas.
   - Centro: selector de modelos en forma de "píldora". En móvil (≤600 px) se convierte en puntos de 12 px.
   - Derecha: ciudad de origen.
3. **Banda vertical central** del color de la marca, entre `--bl` y `--br`:
   - 35 %–65 % en escritorio y 30 %–70 % en móvil.
   - Degradado vertical del color hacia una versión un 12 % más oscura.
   - Ocupa toda la altura de la parte superior.
4. **Bocetos a lápiz grises** a ambos lados de la banda: `object-fit: cover`, pegados a la banda y desvanecidos por abajo.
5. **Logo** dentro de la banda: alto `clamp(56px, 9vw, 130px)`; los logos anchos al 42 %. Contenedor `display:flex` con alto fijo. **No uses grid**: en grid, `height: 100%` del `<img>` no se resuelve y el logo sale gigante.
   - Sin logo: el nombre de la marca en texto blanco, `max-width` igual al ancho de la banda × .86.
6. **Nombre de la marca GIGANTE:**
   - Fuente **Michroma**, `clamp(38px, 11.5vw, 186px)`, negro, sin salto de línea, por encima de la banda.
   - **Cada letra en un `<span>` `inline-block`.** Los espacios se escriben como ` `; si no, desaparecen.
   - **Se ajusta solo:** mide el ancho real entre la primera y la última letra (no `scrollWidth`, que en un bloque siempre da el ancho del contenedor). Si pasa del 94 % del ancho, reduce el `font-size` en proporción. Se recalcula con `resize` y con `document.fonts.ready`.
7. **Modelo** (Michroma, `clamp(17px, 4.2vw, 60px)`):
   - La parte principal en **blanco**; la parte opcional en cursiva en **negro**, en cursiva simulada con `skewX(-14deg)`.
   - **Si la parte blanca se sale de la banda:** aplica con JS `background-image: linear-gradient(90deg, negro Lpx, blanco Lpx, blanco Rpx, negro Rpx)`, con `background-clip: text` y `color: transparent`, calculando L y R respecto a la banda. Así se lee blanca dentro y negra fuera.
   - **Usa `backgroundImage`, nunca el atajo `background`:** el atajo reinicia `background-clip` y aparecen bloques de color.
8. **Lema** en blanco, en 3 líneas, centrado en la banda, con espaciado .14em.
9. **Coche de perfil sin fondo**, de ancho `min(96vw, 1100px)`, apoyado en el borde superior del bloque inferior y con sombra de contacto.
10. **Bloque inferior**:
    - Degradado del color al color oscuro.
    - Forma de **carretera en trapecio** con `clip-path: polygon(bl 0, br 0, 100% T, 100% 100%, 0 100%, 0 T)`, donde `T = clamp(56px, 9vw, 130px)`.
    - Contenido:
      - **Cifras:** 3 grandes (Manrope 300, `clamp(32px, 6.2vw, 66px)`, unidad pequeña) con separadores verticales: Potência (cv), Velocidade máx. (km/h), 0-100 km/h (s), con coma decimal.
      - Una línea fina y el **eslogan** en mayúsculas con espaciado .42em.
      - Una **franja de bandera** del país de la marca.
      - **4 iconos de línea con texto:** 2 columnas en móvil y 4 en escritorio, con separadores.
      - **Pie:** "MARCA / DESDE AÑO" con espaciado .55em.
      - **Botones:** "Agendar visita" (blanco, WhatsApp) y "Voltar ao showroom" (con borde).

### 8.2 Animación
- **El color se funde de un modelo a otro:** registra `@property --c` y `--c2` con `syntax: '<color>'` y pon `transition` sobre ellas. Así también se animan los degradados.
- **Al cargar:**
  - La banda crece desde arriba (`scaleY` 0→1, 900 ms).
  - Las letras del nombre suben una a una (50 ms de desfase).
  - Los bocetos aparecen.
  - El coche entra rodando desde la derecha con desenfoque y un pequeño rebote.
  - Las cifras cuentan desde 0.
- **Al cambiar de modelo** (flechas, píldoras, teclado o swipe; el coche sigue al dedo a 0,7×):
  1. Las letras salen hacia arriba (22 ms de desfase).
  2. El coche sale con 2 estelas y desenfoque.
  3. Los bocetos salen con desplazamiento.
  4. A los 300 ms se cambian los textos y el color, y las letras nuevas entran desde abajo.
  5. El coche nuevo entra desde el lado contrario y aterriza (700 ms).
  6. Las cifras y los iconos reaparecen con un fade-up escalonado.
- **En reposo**, solo con ratón: parallax suave de los bocetos (±14 px) y del coche (±8 px), mediante las variables `--mx` y `--my`. Las animaciones van en las imágenes interiores y el parallax en sus contenedores, para que no se pisen.
- **Movimiento reducido:** fundidos sin desenfoque ni parallax.

### 8.3 Datos (`poster/models.json`, leído con fetch; copia de reserva en el JS)
```json
{ "id": "", "marca": "", "titulo": "NOMBRE GIGANTE", "cidade": "", "logo": "img/x-logo.webp" | null, "logoLargo": true,
  "modelo": "488", "italico": false, "cursiva": "PISTA" | null, "lema": ["L1","L2","L3."],
  "cor": "#hex", "cor2": "#hex", "carro": "img/x-car.webp", "esbocoL": "img/x-sketch-l.webp", "esbocoR": "img/x-sketch-r.webp",
  "stats": [{"l":"Potência","v":720,"u":"cv"},{"l":"Velocidade máx.","v":340,"u":"km/h"},{"l":"0-100 km/h","v":2.85,"u":"s","d":2}],
  "eslogan": "", "bandeira": "uk|it|de|fr|pt|es|jp|us|se|none",
  "icones": [["engine","Texto<br>línea 2"], ...], "rodape": "Marca<br>desde 1947" }
```
- Iconos SVG disponibles: `engine`, `gauge`, `aero`, `wheel`, `fiber`, `heritage`, `electric`, `seat`.
- Banderas: degradados CSS en un objeto `FLAGS`.

---

## 9. TRATAMIENTO DE IMÁGENES (Python)

1. **Quitar el fondo:**
   - `rembg` con el modelo **`isnet-general-use`**, `alpha_matting=True` (foreground 240, background 15, erode 8).
   - Si la imagen ya es RGBA con transparencia, no la recortes otra vez.
2. **Limpiar:**
   - Etiqueta las zonas opacas con `scipy.ndimage.label` y quédate con las que miden al menos el 2 % de la mayor.
   - **Rellena los agujeros** (`binary_fill_holes`), por ejemplo cristales transparentes, con los píxeles de la foto original.
3. **Reflejos:** los escaparates y otros coches reflejados se cuelan en el recorte.
   - Revísalo **siempre** sobre un fondo verde de contraste.
   - Bórralos con polígonos y con reglas de color limitadas a una franja pequeña (por ejemplo `R > B+30 y R > G+15` para un coche rojo reflejado).
   - Que esa franja **no** incluya pilotos ni otras zonas legítimas del mismo color, y vuelve a mirarlo.
4. **Enderezar:**
   - Si la calle tiene pendiente, mide la inclinación en las vistas simétricas (frontal o trasera): los puntos más bajos a la izquierda y a la derecha de la silueta, y su ángulo.
   - Gira **todas** las fotos del coche el mismo ángulo: `rotate(θ, BICUBIC, expand=True)`.
5. **Encuadre común para el 360°:**
   - Mismo ancho y alto (el máximo de los recuadros) para todas las fotos.
   - Cada una **centrada en horizontal** sobre su recuadro y **apoyada por la parte de abajo**, es decir, por las ruedas. Así el coche no salta ni flota entre ángulos.
6. **Base:** desvanece las últimas 14 filas del alfa para que la sombra no quede cortada en línea recta.
7. **Exportar a WebP con transparencia:**
   - Imagen principal: 1600 px de ancho, calidad 88.
   - Frames del 360°: 1200–1400 px, calidad 80–85.
   - Objetivo: menos de 200 KB por imagen.
   - Orden de los frames: alrededor del coche, empezando por el 3/4 frontal.
8. **Bocetos del póster:**
   - **Si salen de un póster de referencia:** recorta los laterales sin incluir la banda de color. Convierte a gris y luego el alfa a `(245 − gris)/245 × 255 × 1.25` (trazo gris `#282828` sobre transparente). Para quitar el título que los atraviesa, **no desenfoques** (queda una mancha): rellena esa franja con la mezcla de la franja de arriba y la de abajo, ambas en espejo vertical. Desvanece las últimas 80 filas.
   - **Si salen de fotos:** efecto lápiz con "color dodge" (`gris / (255 − blur(invertido, σ=9))`), más un 10 % de bordes Canny. Luego un desenfoque de σ .6, alfa `min(línea × .62, 150)` multiplicado por el alfa del recorte, y desvanecido del tercio inferior. Para el lado izquierdo usa la mitad delantera del coche y para el derecho la trasera.
9. **Logos:** si el logo es negro sobre un fondo de color, el alfa sale del canal rojo: `(185 − R)/150`. Si es un escudo de color, pásalo por rembg.
10. **Sin fotos reales:** solo como demo y avisando, renderiza modelos 3D libres (por ejemplo el Ferrari de los ejemplos de three.js o el "CarConcept" CC0 de Khronos). Usa Chromium sin interfaz con WebGL (SwiftShader), fondo transparente, pintura con clearcoat, cristales oscuros y entorno `RoomEnvironment`, y vista 3/4 con 36 ángulos para el 360°. Cita la autoría y la licencia en el README.

---

## 10. HERRAMIENTA `tools/preparar_coche.py` (todo replicable)

Debe permitir añadir cualquier coche futuro **solo con sus fotos y un comando**, sin tocar el código.

**Modo `showroom`:**
- Argumentos: `--id`, `--fotos` (varias; la 1.ª es la principal y el orden de las demás es el orden del 360°), `--marca`, `--modelo`, `--ano`, `--km`, `--preco`, `--cv`, `--combustivel`, `--caixa`, `--cor`, `--rotar` (grados), `--demo`, `--no-fim`.
- Aplica los pasos 1, 2 y 4–7 de §9.
- Guarda `cars/<id>.webp` y `cars/<id>/<n>.webp`.
- Inserta o actualiza el coche en `cars.json`, al principio salvo que se use `--no-fim`.
- **Regenera `FALLBACK_CARS` dentro de `index.html`** con el mismo JSON.

**Modo `poster`:**
- Argumentos: `--id`, `--foto` (perfil), `--esbocos` (1–2 fotos de detalle), `--logo`, `--logo-largo`, `--marca`, `--titulo`, `--modelo`, `--cursiva`, `--cidade`, `--cor`, `--cor2` (si falta, el color oscurecido al 78 %), `--lema "A|B|C"`, `--eslogan`, `--bandeira`, `--cv`, `--vmax`, `--zero100` (los decimales se deducen del número), `--icones "clave:texto|..."`, `--desde`, `--rotar`.
- Aplica §9 (incluido el punto 8 para fotos).
- Inserta o actualiza el modelo en `poster/models.json`.

**Además:**
- `tools/requirements.txt` con las dependencias.
- `tools/README.md` en `IDIOMA_CONMIGO` con: cómo instalar, reglas de las fotos (coche entero, misma distancia y altura, fondo limpio, orden de los ángulos, cuándo usar `--rotar`), los dos comandos de ejemplo, cómo revisar en local y cómo publicar.
- Que el README avise de que la primera ejecución descarga el modelo de recorte (~180 MB) y de que **los reflejos no se borran solos**: hay que retocar el PNG y volver a pasarlo por la herramienta, que lo acepta ya recortado.
- **Pruébala de verdad** en una copia desechable del repositorio con fotos reales, y comprueba que el coche aparece en la web (también abriéndola con `file://`).

---

## 11. VERIFICACIÓN Y PUBLICACIÓN

**Pruebas con Playwright** (Chromium sin interfaz, servidor local `python3 -m http.server`):
- **Anchos:** 375/390, 768 y 1440. Capturas de página entera y del escenario.
- **Interacciones que hay que comprobar:**
  - Swipe con ratón, tecla →, clic en una miniatura.
  - El enlace de WhatsApp contiene el coche correcto.
  - El botón 360°, incluido arrastrar y que la imagen cambie de frame.
  - Los filtros del stock, el botón "ver en 3D" y el envío del formulario (abre una ventana nueva).
  - Cambio de tema y que se mantiene al recargar.
  - Los modelos de la página póster y su transición. Haz capturas en mitad de la transición, a unos 80–450 ms, para ver el desenfoque y el rebote.
- **Condiciones de aprobado:** sin errores de consola, sin scroll horizontal, nada que se salga de su contenedor y nada que tape otra cosa. Un error 404 de una imagen que todavía no existe es aceptable solo si se ve la silueta de reserva.
- **Ojo con las capturas de página entera:** la cabecera fija aparece en mitad de la imagen. Es un efecto de la captura, no un fallo.

**Publicación:**
- Trabaja en una rama. Haz commit con un mensaje claro, push, abre un pull request a `main` con un resumen y lo que se probó, y fusiónalo si el usuario lo ha autorizado.
- GitHub Pages: Settings → Pages → Deploy from branch → `main` / root. URL: `https://USUARIO.github.io/REPO/`.
- Si la publicación falla por permisos, entrega un ZIP del contenido y explica cómo subirlo a mano.

---

## 12. ERRORES YA RESUELTOS (no repetirlos)

- **Transformaciones que chocan:** WAAPI y transformaciones CSS sobre el mismo elemento se pisan. Separa contenedor (posición o parallax) e imagen interior (animación).
- `Element.getAnimations()` sin `{subtree:true}` no cancela las animaciones de los hijos. Úsalo a propósito, para no matar la respiración del coche.
- `scrollIntoView` en el carrusel de miniaturas desplaza toda la página. Usa `scrollTo` sobre el contenedor.
- Las capturas de página entera no disparan IntersectionObserver. Haz scroll por toda la página antes de capturar.
- **Archivos con espacios duros:** algunos editores guardan ` ` como un carácter literal y luego los reemplazos de texto no encuentran nada. Localiza los bloques por posición.
- **Servidor caído:** el servidor de pruebas lanzado en segundo plano puede morir entre comandos. Comprueba el código HTTP antes de culpar a la página.
- **No uses `pkill -f`** con un patrón que también coincida con tu propia orden: mata tu terminal.
- **Varios formatos en el mismo texto** (precio, km, decimales): formato manual con punto de miles y coma decimal, según `IDIOMA_WEB`.

---

## 13. ORDEN DE TRABAJO RECOMENDADO

1. Lee la web actual del cliente (si puedes) y saca el nombre, el contacto, el stock y los textos. Lo que no puedas leer, márcalo como DEMO.
2. Haz la web principal con el showroom (§3–§7). Pruébala (§11) y publícala.
3. Haz el tema claro (§6). Pruébalo y publícalo.
4. Procesa las fotos reales que haya (§9) y pon un coche real en primer lugar.
5. Haz la página póster (§8) con 2 modelos. Pruébala y publícala.
6. Haz la herramienta (§10), pruébala añadiendo un coche real y publícala.
7. **Entrega:** enlaces, capturas en móvil y escritorio, y la lista de datos DEMO pendientes (contacto real, precios, km, años, textos, permisos de las imágenes de marca).
