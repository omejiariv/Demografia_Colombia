# app/piramide.py

import streamlit as st
import matplotlib.pyplot as plt

def mostrar_piramide(escala, nivel, ano, zona, sexo):
    st.subheader("Pirámide poblacional")

    st.markdown(f"""
    **Escala:** {escala}  
    **Nivel:** {nivel}  
    **Año:** {ano}  
    **Zona:** {zona}  
    **Sexo:** {sexo}
    """)

    # Placeholder temporal (para verificar que ya no falla)
    fig, ax = plt.subplots()
    ax.barh(["0-4", "5-9", "10-14"], [100, 80, 60])
    ax.set_title("Pirámide (placeholder)")
    st.pyplot(fig)
