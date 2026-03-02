# app/app.py

import streamlit as st
from sidebar import sidebar
from mapa import mapa_principal

st.set_page_config(
    page_title="Modelo Demográfico Espacial – Colombia",
    layout="wide"
)

st.title("Modelo Demográfico Espacial Multiescala")
st.markdown(
    """
    **Proyección y distribución espacial de población (1950–2050)**  
    Antioquia · Urbano / Rural · Veredal / Municipal
    """
)

# Sidebar
escala, ano, zona, comparativo = sidebar()

# Mapa
mapa_principal(
    escala=escala,
    ano=ano,
    zona=zona,
    comparativo=comparativo
)
