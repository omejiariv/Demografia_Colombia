# app/sidebar.py

import streamlit as st

def sidebar():
    st.sidebar.header("Parámetros")

    escala = st.sidebar.selectbox(
        "Escala de análisis",
        ["Departamental (Antioquia)", "Municipal", "Veredal"]
    )

    ano = st.sidebar.slider(
        "Año",
        min_value=1950,
        max_value=2050,
        value=2020,
        step=5
    )

    zona = st.sidebar.radio(
        "Zona",
        ["Total", "Urbana", "Rural"]
    )

    comparativo = st.sidebar.checkbox(
        "Comparar con 1950 / 2050"
    )

    return escala, ano, zona, comparativo
