# app/modelo.py
import streamlit as st
from engine.pipeline.runner import ejecutar_pipeline_antioquia
from engine.pipeline.runner import guardar_raster_temporal

@st.cache_data(show_spinner=True)
def obtener_raster(ano, zona):
    raster, bounds, total = ejecutar_pipeline_antioquia(
        ano=ano,
        zona=zona
    )
    raster_path = guardar_raster_temporal(
        raster, bounds, resolucion=500
    )
    return raster_path, total
