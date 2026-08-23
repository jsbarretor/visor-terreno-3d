# Visor de Terreno 3D

App de Streamlit que muestra terreno global en 3D (inclinable y rotable),
usando [leafmap](https://leafmap.org/) sobre MapLibre GL JS. No depende de
Google Earth Engine.

## 1. Probarla en tu computador (opcional)

```bash
pip install -r requirements.txt
streamlit run app.py
```

Se abre en tu navegador en `http://localhost:8501`.

**Importante — vista satelital:** la opción "Vista satelital (estilo
Google Earth)" necesita una llave gratuita de MapTiler (ver sección 3).
Sin ella, la app funciona igual pero muestra el terreno con un mapa
vectorial (calles y nombres) en vez de fotos satelitales. Para usar la
llave en tu computador (a diferencia de en Streamlit Cloud), crea el
archivo `.streamlit/secrets.toml` dentro de esta misma carpeta
`DEM3D_App` con:
```toml
MAPTILER_KEY = "tu-llave-aqui"
```

## 2. Desplegarla con un enlace público (Streamlit Community Cloud, gratis)

1. Crea un repositorio en GitHub (puede ser privado o público) y sube estos
   tres archivos: `app.py`, `requirements.txt`, `README.md`.
   - Si no usas Git desde la terminal, en github.com puedes crear el
     repositorio vacío y luego arrastrar los archivos con "Add file →
     Upload files".
2. Entra a [share.streamlit.io](https://share.streamlit.io) e inicia sesión
   con tu cuenta de GitHub (créala gratis si no tienes).
3. Clic en "New app", elige el repositorio que acabas de crear, y en
   "Main file path" escribe `app.py`.
4. Clic en "Deploy". Toma uno o dos minutos la primera vez.
5. Cuando termine, Streamlit te da una URL pública
   (`https://tu-app.streamlit.app` o similar) — esa es la que puedes
   compartir.

## 3. Llave de MapTiler (necesaria para la vista satelital)

1. Crea una cuenta gratis en [maptiler.com](https://www.maptiler.com/) →
   te da una API key en tu panel ("Cloud" → "Keys").
2. **Para tu computador**: crea el archivo `.streamlit/secrets.toml`
   dentro de la carpeta `DEM3D_App` con:
   ```toml
   MAPTILER_KEY = "tu-llave-aqui"
   ```
3. **Para la app desplegada en Streamlit Community Cloud**: abre tu app →
   menú "⋮" → "Settings" → "Secrets", y pega lo mismo. Guarda — la app la
   recoge automáticamente (ver `app.py`).

## 4. Actualizar la app después de desplegada

Cualquier cambio que subas al mismo repositorio de GitHub (por ejemplo
editar `app.py`) se refleja solo en la app ya desplegada — no hay que
volver a hacer "Deploy" manualmente.
