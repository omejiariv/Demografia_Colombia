# app/piramide.py

import plotly.graph_objects as go
import streamlit as st
from modelo_demo import calcular_piramide

def mostrar_piramide(
    ano,
    escala,
    codigo,
    zona
):
    df = calcular_piramide(
        ano=ano,
        escala=escala,
        codigo=codigo,
        zona=zona
    )

    hombres = df[df["SEXO"] == "Hombres"]
    mujeres = df[df["SEXO"] == "Mujeres"]

    fig = go.Figure()

    fig.add_trace(go.Bar(
        y=hombres["EDAD_GRUPO"],
        x=-hombres["POBLACION"],
        name="Hombres",
        orientation="h"
    ))

    fig.add_trace(go.Bar(
        y=mujeres["EDAD_GRUPO"],
        x=mujeres["POBLACION"],
        name="Mujeres",
        orientation="h"
    ))

    fig.update_layout(
        title=f"Piramide poblacional {ano}",
        barmode="overlay",
        bargap=0.05,
        xaxis_title="Población",
        yaxis_title="Grupo de edad",
        template="plotly_white",
        height=600
    )

    st.plotly_chart(fig, use_container_width=True)
