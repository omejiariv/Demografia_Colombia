# app/mapa.py

import leafmap.foliumap as leafmap
import streamlit as st
import rasterio
import geopandas as gpd
import numpy as np
import tempfile

def mapa_principal(escala, ano, zona, comparativo):

    m = leafmap.Map(
        center=[6.5, -75.5],  # Antioquia
        zoom=7,
        basemap="CartoDB.Positron"
    )

    # ---- Raster principal ----
    raster_path = f"data/rasters/densidad_{ano}.tif"

    if raster_path:
        m.add_raster(
            raster_path,
            layer_name=f"Densidad {ano}",
            colormap="viridis",
            opacity=0.75
        )

    # ---- Comparativo 1950 vs 2050 ----
    if comparativo:
        raster_1950 = "data/rasters/densidad_1950.tif"
        raster_2050 = "data/rasters/densidad_2050.tif"

        m.add_raster(
            raster_1950,
            layer_name="Densidad 1950",
            colormap="Blues",
            opacity=0.6
        )

        m.add_raster(
            raster_2050,
            layer_name="Densidad 2050",
            colormap="Reds",
            opacity=0.6
        )

    # ---- Límites administrativos ----
    if escala != "Veredal":
        gdf_mpios = gpd.read_file("data/municipios.gpkg")
        m.add_gdf(
            gdf_mpios,
            layer_name="Municipios",
            style={"fillOpacity": 0, "color": "black"}
        )

    # ---- Control de capas ----
    m.add_layer_control()

    # ---- Render ----
    m.to_streamlit(height=750)
