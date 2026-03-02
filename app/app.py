# app/app.py

import streamlit as st
from ui/sidebar.py import sidebar
from app.mapa import mapa_principal
from app.piramide import mostrar_piramide

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

col1, col2 = st.columns([2, 1])

with col1:
    mapa_principal(
        escala=escala,
        ano=ano,
        zona=zona,
        comparativo=comparativo
    )

with col2:
    st.subheader("Pirámide poblacional")
    mostrar_piramide(
        ano=ano,
        escala="Nacional" if escala == "Departamental (Antioquia)" else escala,
        codigo=None,
        zona=zona
    )
