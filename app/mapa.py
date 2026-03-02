# app/mapa.py

import streamlit as st
import geopandas as gpd
import leafmap.foliumap as leafmap
import rasterio
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from rasterio.plot import reshape_as_image
from branca.colormap import LinearColormap

from modelo import obtener_raster


def mapa_principal(escala, nivel, ano, zona):
    st.subheader("Mapa de distribución poblacional")

    st.write("Escala:", escala)
    st.write("Nivel:", nivel)
    st.write("Año:", ano)
    st.write("Zona:", zona)

    # -------------------------
    # 1. Obtener raster
    # -------------------------
    raster_path, total = obtener_raster(ano, zona)

    # -------------------------
    # 2. Leer raster con rasterio
    # -------------------------
    with rasterio.open(raster_path) as src:
        data = src.read(1)
        bounds = src.bounds
        crs = src.crs

    # Normalizar para visualización
    data = np.nan_to_num(data)
    vmax = np.percentile(data, 99)
    data = np.clip(data, 0, vmax)

    # Colormap
    cmap = cm.get_cmap("Blues")
    rgba = cmap(data / vmax)

    # Convertir a imagen
    img = (rgba[:, :, :3] * 255).astype(np.uint8)

    # -------------------------
    # 3. Crear mapa
    # -------------------------
    m = leafmap.Map(
        center=[6.5, -75.5],
        zoom=7,
        basemap="CartoDB.Positron"
    )

    # Añadir raster como imagen
    m.add_image(
        img,
        bounds=[[bounds.bottom, bounds.left], [bounds.top, bounds.right]],
        opacity=0.85,
        name=f"Densidad {ano}"
    )

    # -------------------------
    # 4. Cabeceras / municipios
    # -------------------------
    gdf_mpios = gpd.read_file("data/MunicipiosAntioquia.geojson").to_crs("EPSG:4326")

    m.add_gdf(
        gdf_mpios,
        layer_name="Municipios",
        style={
            "fillOpacity": 0,
            "color": "black",
            "weight": 1
        }
    )

    m.add_layer_control()
    m.to_streamlit(height=600)

    # -------------------------
    # 5. Leyenda
    # -------------------------
    colormap = LinearColormap(
        colors=["#f7fbff", "#deebf7", "#c6dbef", "#9ecae1", "#6baed6", "#2171b5"],
        vmin=0,
        vmax=int(vmax),
        caption="Densidad poblacional (hab/km²)"
    )

    st.markdown(colormap._repr_html_(), unsafe_allow_html=True)

    st.caption(f"Población total estimada: {int(total):,}")
