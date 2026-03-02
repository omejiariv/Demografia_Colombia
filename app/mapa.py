# app/mapa.py

import streamlit as st
import geopandas as gpd
import leafmap.foliumap as leafmap

from modelo import obtener_raster
from engine.espacial.clasificacion import clasificar_densidad

def mapa_principal(escala, nivel, ano, zona):
    st.subheader("Mapa de distribución poblacional")

    st.write("Escala:", escala)
    st.write("Nivel:", nivel)
    st.write("Año:", ano)
    st.write("Zona:", zona)

    # Obtener raster
    raster_path, total = obtener_raster(ano, zona)

    # Crear mapa
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

    # Cabeceras municipales
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

    m.to_streamlit(height=600)

    # Leyenda
    st.markdown("""
    ### Densidad poblacional (hab/km²)

    - < 1  
    - 1 – 10  
    - 10 – 50  
    - 50 – 200  
    - 200 – 1.000  
    - > 1.000  
    """)
