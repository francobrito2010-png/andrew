# Prompt — Showroom "Poster" de superdeportivos

Copia y pega esto en cualquier chat de código para generar (o regenerar) la página.

---

**Rol:** desarrollador front-end senior especializado en webs de automoción premium y animación web.

**Objetivo:** crear una página-showroom con el estilo de un póster de coche de colección (referencia: pósters "McLaren 720S — Driven by perfection" y "Ferrari 488 Pista — Built for passion"). Dos modelos, se pasa de uno a otro como en un selector de coche de videojuego. Debe ser **fiel a los pósters** (misma composición, colores y jerarquía) pero **dinámica**: todo se anima al cambiar de modelo.

## Composición (de arriba abajo, igual que el póster)
1. **Fondo papel** blanco roto (#f1efeb) con grano muy sutil.
2. **Barra superior fina:** marca a la izquierda, ciudad de origen a la derecha (McLaren → WOKING, Ferrari → MARANELLO), en mayúsculas pequeñas con mucho espaciado. En el centro, puntos para elegir modelo.
3. **Banda vertical central** del color de la marca (≈30 % del ancho), desde arriba hasta el coche. A los lados, **bocetos a lápiz en gris** del mismo coche, recortados del póster.
4. **Logotipo** de la marca dentro de la banda, arriba.
5. **Nombre de la marca GIGANTE** (fuente geométrica extendida tipo Michroma, negro, de lado a lado por encima de la banda) y debajo el **modelo** en cursiva ("720S", "488 PISTA").
6. **Lema** en blanco, apilado en 3 líneas dentro de la banda ("DRIVEN / BY / PERFECTION.").
7. **Coche de perfil, sin fondo**, grande, apoyado sobre la banda.
8. **Bloque inferior** del color de la marca que se abre en trapecio bajo el coche (como una carretera) y contiene:
   - 3 cifras grandes con separadores: Potência (cv), Velocidade máx. (km/h), 0-100 km/h (s).
   - Línea fina + eslogan con letras muy espaciadas.
   - Franja de bandera (Reino Unido / Italia).
   - 4 iconos de línea con texto (motor, rendimiento, aerodinámica/condução, herança).
   - Pie: "McLAREN · DESDE 1963" / "FERRARI · DESDE 1947".
   - Botones: "Agendar visita" (WhatsApp) y "Voltar ao showroom".

## Datos (comprobar antes de publicar)
- **McLaren 720S:** 720 cv, 341 km/h, 0-100 en 2,9 s, V8 4.0 biturbo. Color #E8701A → #C24F0E. Origen: Woking.
- **Ferrari 488 Pista:** 720 cv, 340 km/h, 0-100 en 2,85 s, V8 3.9 biturbo. Color #C8161D → #8C0D12. Origen: Maranello.
- Textos de la web en portugués de Portugal; los lemas de marca pueden ir en inglés, como en los pósters.

## Dinamismo (lo importante)
- **Entrada:** la banda crece desde arriba, las letras del nombre suben una a una, el coche entra rodando desde la derecha y frena con un pequeño rebote, las cifras cuentan desde 0.
- **Cambio de modelo** (flechas, swipe con Pointer Events, teclado ← →, puntos):
  - Las letras del nombre salen hacia arriba con retardo escalonado y entran las nuevas desde abajo.
  - El color de la banda y del bloque inferior **se funde** al nuevo (variable CSS registrada con `@property`, para que el degradado se anime).
  - El coche saliente acelera hacia un lado con desenfoque de movimiento; el nuevo entra por el lado contrario y "aterriza".
  - Los bocetos laterales se funden con un ligero desplazamiento (parallax).
  - Cifras, eslogan e iconos reaparecen con fade-up escalonado.
  - 800–900 ms en total, easing cubic-bezier, nunca lineal. Bloquear los inputs durante la transición.
- **En reposo:** parallax suave de bocetos y coche al mover el ratón (solo escritorio).
- `prefers-reduced-motion`: fundidos simples, sin desenfoque ni parallax.

## Técnica
- HTML + CSS + JS vanilla en un solo archivo, sin dependencias salvo Google Fonts (Michroma + Manrope).
- Animar solo transform, opacity y filter. Mobile-first (perfecto a 375 px), sin scroll horizontal.
- Imágenes WebP con transparencia: coche recortado (rembg), bocetos convertidos a trazo gris sobre transparente, logotipos.
- Accesible: aria-label en botones, foco visible, `aria-live` con el modelo actual.
