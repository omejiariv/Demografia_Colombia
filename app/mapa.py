# app/mapa.py

import leafmap.foliumap as leafmap
import streamlit as st
from modelo import obtener_raster

def mapa_principal(escala, ano, zona, comparativo):

    m = leafmap.Map(
        center=[6.5, -75.5],
        zoom=7,
        basemap="CartoDB.Positron"
    )

    raster_path, total = obtener_raster(ano, zona)

    m.add_raster(
        raster_path,
        layer_name=f"Densidad {ano}",
        colormap="viridis",
        opacity=0.8
    )

    st.caption(
        f"Población total estimada: {int(total):,}"
    )

    m.add_layer_control()
    m.to_streamlit(height=750)
