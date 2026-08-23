"""
Visor de Terreno 3D (DEM) - app de Streamlit
---------------------------------------------
Muestra el terreno global en 3D (inclinable/rotable) usando leafmap sobre
MapLibre GL JS. No necesita Google Earth Engine: usa un dataset de
elevación (terreno) público que MapLibre sabe interpretar directamente.

Cómo correrlo localmente:
    pip install -r requirements.txt
    streamlit run app.py

Cómo desplegarlo con un enlace público: ver README.md
"""

import os

import streamlit as st
import leafmap.maplibregl as leafmap

st.set_page_config(page_title="Visor de Terreno 3D", layout="wide")

# La vista satelital ("3d-hybrid") necesita una llave gratuita de MapTiler.
# La vista vectorial ("3d-terrain") funciona sin llave.
# Para pruebas locales: crea el archivo ".streamlit/secrets.toml" en esta
# misma carpeta con el contenido:
#     MAPTILER_KEY = "tu-llave-aqui"
# Para la app ya desplegada en Streamlit Community Cloud: configúrala en
# Settings → Secrets (ver README.md).
maptiler_key = os.environ.get("MAPTILER_KEY")
try:
    if not maptiler_key and "MAPTILER_KEY" in st.secrets:
        maptiler_key = st.secrets["MAPTILER_KEY"]
        os.environ["MAPTILER_KEY"] = maptiler_key
except Exception:
    pass

st.title("🏔️ Visor de Terreno 3D")
st.caption(
    "Terreno global en 3D — arrastra con el botón derecho (o Ctrl+arrastrar) "
    "para rotar/inclinar la vista, o usa los controles de la izquierda."
)

# La app arranca en blanco: el usuario escribe la ubicación y pulsa
# "Generar vista 3D" para que aparezca el mapa.
if "generado" not in st.session_state:
    st.session_state.generado = False

with st.sidebar:
    st.header("Ubicación")

    lon = st.number_input("Longitud", value=None, format="%.5f", placeholder="Ej: -75.23220")
    lat = st.number_input("Latitud", value=None, format="%.5f", placeholder="Ej: 4.43890")

    generar = st.button("🔎 Generar vista 3D", type="primary", use_container_width=True)

    st.header("Vista")
    zoom = st.slider("Zoom", min_value=3, max_value=17, value=11)
    pitch = st.slider("Inclinación (0 = vista de arriba)", min_value=0, max_value=85, value=60)
    bearing = st.slider("Rotación (grados)", min_value=0, max_value=360, value=0)

    st.header("Mapa base")
    vista_satelital = st.checkbox(
        "Vista satelital (estilo Google Earth)",
        value=True,
        help="Necesita una llave gratuita de MapTiler (ver README.md).",
    )
    exageracion = st.slider(
        "Exageración del relieve", min_value=1.0, max_value=5.0, value=1.5, step=0.5
    )

    st.markdown("---")
    st.caption(
        "Consejo: sube el zoom y baja la inclinación para explorar un valle "
        "de cerca; baja el zoom y sube la inclinación para ver cordilleras "
        "enteras."
    )

    st.markdown("---")
    st.caption("Hecho por Sebastian Barreto — jsbarretor@gmail.com")

# Al pulsar el botón, se valida que haya coordenadas y se "activa" la vista.
if generar:
    if lon is None or lat is None:
        st.session_state.generado = False
        st.error("Escribe una Longitud y una Latitud antes de generar la vista.")
    else:
        st.session_state.generado = True
        st.session_state.lon = lon
        st.session_state.lat = lat

if not st.session_state.generado:
    st.info(
        "👈 Escribe una **Longitud** y una **Latitud** en el panel de la "
        "izquierda y pulsa **Generar vista 3D** para ver el terreno."
    )
    st.stop()

# A partir de aquí ya hay una ubicación confirmada (guardada en session_state
# para que los sliders de Vista/Mapa base se puedan mover sin perderla).
lon = st.session_state.lon
lat = st.session_state.lat

usar_satelite = vista_satelital and bool(maptiler_key)

if vista_satelital and not maptiler_key:
    st.warning(
        "La vista satelital necesita una llave gratuita de MapTiler. "
        "Crea una cuenta en [maptiler.com](https://www.maptiler.com/) y "
        "guarda tu llave en un archivo `.streamlit/secrets.toml` dentro de "
        "esta carpeta con el contenido `MAPTILER_KEY = \"tu-llave\"`. "
        "Mientras tanto se muestra el terreno con mapa vectorial."
    )

# "3d-hybrid" = terreno 3D + imagen satelital (estilo Google Earth).
# "3d-terrain" = terreno 3D + mapa vectorial (calles/nombres, sin fotos).
estilo = "3d-hybrid" if usar_satelite else "3d-terrain"

m = leafmap.Map(
    center=[lon, lat],
    zoom=zoom,
    pitch=pitch,
    bearing=bearing,
    style=estilo,
    exaggeration=exageracion,
)

# IMPORTANTE: por un detalle interno de la librería, add_marker/add_geojson
# no aparecen en el mapa a menos que se active esto (activa la "cola de
# mensajes" que sí queda incluida al exportar el mapa).
m.use_message_queue(True)

# Marcador (pin rojo) en la ubicación buscada. Se agrega ligeramente elevado
# (occludedOpacity=1) para que se vea aunque esté sobre terreno montañoso.
m.add_marker(
    lng_lat=[lon, lat],
    options={"color": "red", "occludedOpacity": 1},
)

m.add_layer_control(bg_layers=True)

m.to_streamlit(height=750)
