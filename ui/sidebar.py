# ui/sidebar.py
import streamlit as st

def sidebar():
    st.sidebar.title("Modelo Demográfico Espacial")

    escala = st.sidebar.selectbox(
        "Escala de análisis",
        ["Nacional", "Departamental", "Municipal", "Veredal"]
    )

    nivel = st.sidebar.selectbox(
        "Nivel territorial",
        ["País", "Región", "Departamento", "CAR", "Municipio"]
    )

    ano = st.sidebar.slider("Año", 1950, 2050, 2020, step=5)

    zona = st.sidebar.radio(
        "Zona",
        ["Total", "Urbana", "Rural"]
    )

    sexo = st.sidebar.radio(
        "Sexo",
        ["Total", "Hombres", "Mujeres"]
    )

    return escala, nivel, ano, zona, sexo
