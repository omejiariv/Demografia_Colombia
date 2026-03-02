import pandas as pd
import streamlit as st
from engine.demografia.piramides import obtener_piramide

@st.cache_data
def cargar_datos_dane():
    return pd.read_excel(
        "data/Pob_sexo_edad_Colombia_1950-2070.xlsx"
    )

@st.cache_data
def calcular_piramide(
    ano, escala, codigo, zona
):
    df = cargar_datos_dane()
    return obtener_piramide(
        df=df,
        ano=ano,
        escala=escala,
        codigo=codigo,
        zona=zona
    )
