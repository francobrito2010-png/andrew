# Añadir un coche nuevo (con fotos)

Una herramienta para todo: `tools/preparar_coche.py`. Quita el fondo, endereza, recorta, exporta a WebP y **añade el coche a la web** (actualiza `cars.json` y `poster/models.json`). No hay que tocar el código.

## 1. Instalar (una sola vez)

```bash
pip install -r tools/requirements.txt
```

La primera vez descarga el modelo para quitar fondos (~180 MB).

## 2. Hacer las fotos

- **Coche entero**, sin cortar ruedas, a la misma distancia y altura en todas (~1 m, a media puerta).
- **Fondo lo más limpio posible.** Los reflejos de cristaleras o de otros coches se pueden colar en el recorte. Si pasa, retoca el PNG (o pásalo por remove.bg) y vuelve a ejecutar el comando: si la foto ya no tiene fondo, la herramienta no la recorta otra vez.
- **Showroom 3D:** 1.ª foto = 3/4 frontal (es la principal). Después, en orden alrededor del coche: trasera 3/4, trasera, otro lado, frente… (de 3 a 36 fotos). Esa es la vuelta del 360°.
- **Póster:** 1 foto **de perfil** (de lado) y 1–2 fotos de detalle (frente y trasera) para los bocetos laterales.
- Si la calle tiene pendiente y el coche sale inclinado, usa `--rotar` (por ejemplo `--rotar -5`).

## 3. Ejecutar (desde la carpeta del repo)

**Showroom 3D (página principal):**

```bash
python tools/preparar_coche.py showroom --id porsche-911-2021 \
  --fotos fotos/911-1.jpg fotos/911-2.jpg fotos/911-3.jpg \
  --marca Porsche --modelo "911 Carrera S" --ano 2021 --km 18500 --preco 139900 \
  --combustivel Gasolina --caixa Automática --cv 450
```

Lo que no sepas (año, km, precio) déjalo fuera: la web muestra "Sob consulta".

**Página póster (Coleção):**

```bash
python tools/preparar_coche.py poster --id porsche-911 \
  --foto fotos/911-perfil.jpg --esbocos fotos/911-frente.jpg fotos/911-trasera.jpg \
  --marca Porsche --modelo 911 --cursiva "CARRERA S" --cidade Stuttgart \
  --cor "#1d1d1f" --lema "THERE IS|NO|SUBSTITUTE." \
  --eslogan "Pure performance. German precision." --bandeira de \
  --cv 450 --vmax 308 --zero100 3.5 --desde 1948 \
  --icones "engine:Motor 6 cilindros|gauge:ADN de competição|wheel:Condução precisa|heritage:Herança"
```

- `--cor`: color de la banda (el de la marca o el del coche). `--cor2` es opcional; si no se indica, se oscurece sola.
- `--logo logo.png`: opcional. Sin logo, aparece el nombre de la marca.
- Iconos disponibles: `engine`, `gauge`, `aero`, `wheel`, `fiber`, `heritage`, `electric`, `seat`.
- Banderas: `uk`, `it`, `de`, `fr`, `pt`, `es`, `jp`, `us`, `se`, `none`.

Ejemplo real ya incluido: el Aston Martin Vantage Roadster del stand se añadió a la Coleção con este comando, a partir de sus fotos.

## 4. Revisar y publicar

```bash
python -m http.server     # abrir http://localhost:8000 y http://localhost:8000/poster/
git add -A && git commit -m "Añadir Porsche 911" && git push
```

Para quitar un coche: borra su bloque en `cars.json` o en `poster/models.json`, y sus imágenes.
