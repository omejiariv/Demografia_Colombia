# app/app.py

import streamlit as st
from sidebar import sidebar
from mapa import mapa_principal
from piramide import mostrar_piramide
from engine.pipeline.runner import ejecutar_pipeline_antioquia
from engine.pipeline.runner import guardar_raster_temporal

st.set_page_config(
    page_title="Modelo Demográfico Espacial – Colombia",
    layout="wide"
)

st.title("Modelo Demográfico Espacial Multiescala")

escala, nivel, ano, zona, sexo = sidebar()

col1, col2 = st.columns([2, 1])

with col1:
    mapa_principal(escala, nivel, ano, zona)

with col2:
    mostrar_piramide(escala, nivel, ano, zona, sexo)
