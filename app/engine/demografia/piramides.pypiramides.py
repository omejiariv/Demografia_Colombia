# app/engine/demografia/piramides.py

import pandas as pd

EDADES_ORDEN = [
    "0-4","5-9","10-14","15-19","20-24","25-29",
    "30-34","35-39","40-44","45-49",
    "50-54","55-59","60-64","65-69",
    "70-74","75-79","80+"
]

def obtener_piramide(
    df,
    ano,
    escala="Nacional",
    codigo=None,
    zona="Total"
):
    """
    df: dataframe DANE sexo-edad
    escala: Nacional / Departamental / Municipal / Veredal
    codigo: código territorial (None si nacional)
    """

    base = df[df["ANO"] == ano].copy()

    # Escala
    if escala != "Nacional":
        base = base[base["CODIGO"] == codigo]

    # Zona
    if zona != "Total":
        base = base[base["ZONA"] == zona]

    # Agregación
    tabla = (
        base.groupby(["EDAD_GRUPO", "SEXO"])["POBLACION"]
        .sum()
        .reset_index()
    )

    tabla["EDAD_GRUPO"] = pd.Categorical(
        tabla["EDAD_GRUPO"],
        categories=EDADES_ORDEN,
        ordered=True
    )

    return tabla.sort_values("EDAD_GRUPO")
