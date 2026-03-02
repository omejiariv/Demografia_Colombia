# app/mapa.py

import leafmap.foliumap as leafmap
import streamlit as st
from modelo import obtener_raster

from engine.espacial.clasificacion import clasificar_densidad

def mapa_principal(...):

    raster_path, total = obtener_raster(ano, zona)

    m = leafmap.Map(
        center=[6.5, -75.5],
        zoom=7,
        basemap="CartoDB.Positron"
    )

    m.add_raster(
        raster_path,
        layer_name=f"Densidad {ano}",
        colormap=[
            "#f7fbff",
            "#deebf7",
            "#c6dbef",
            "#9ecae1",
            "#6baed6",
            "#2171b5"
        ],
        opacity=0.85
    )

gdf_cabeceras = gpd.read_file("data/cabeceras.gpkg")

m.add_gdf(
    gdf_cabeceras,
    layer_name="Cabeceras municipales",
    style={
        "radius": 4,
        "color": "black",
        "fillColor": "red",
        "fillOpacity": 0.9
    }
)

st.markdown("""
### Densidad poblacional (hab/km²)

- < 1
- 1 – 10
- 10 – 50
- 50 – 200
- 200 – 1.000
- > 1.000
""")


