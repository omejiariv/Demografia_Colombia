# app/engine/espacial/restricciones.py

import rasterio
import numpy as np

def mascara_pendiente(raster_pendiente, max_grados=30):
    with rasterio.open(raster_pendiente) as src:
        slope = src.read(1)
        mask = slope <= max_grados
    return mask, src.transform

import geopandas as gpd

def excluir_rios(gdf_area, gdf_rios, buffer_m=50):
    rios_buf = gdf_rios.buffer(buffer_m)
    return gdf_area.overlay(
        gpd.GeoDataFrame(geometry=rios_buf),
        how="difference"
    )

def excluir_bosques(gdf_area, gdf_bosques):
    return gdf_area.overlay(gdf_bosques, how="difference")

