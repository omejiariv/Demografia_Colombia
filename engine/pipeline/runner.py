# engine/pipeline/runner.py

import numpy as np
import geopandas as gpd
import tempfile
import rasterio
from rasterio.transform import from_origin

from engine.demografia.proyecciones import proyectar_serie
from engine.demografia.escalas import redistribuir
from engine.espacial.urbano_rural import clasificar_urbano_rural
from engine.espacial.kernel import puntos_ponderados, kde_superficie
from engine.espacial.raster import crear_grid, evaluar_kde
from engine.espacial.calibracion import calibrar_raster


def ejecutar_pipeline_antioquia(
    ano,
    zona="Total",
    resolucion=500
):
    """
    Ejecuta el pipeline completo para Antioquia y devuelve:
    - raster (numpy array)
    - bounds
    - total poblacional
    """

    # -------------------------
    # 1. Cargar capas base
    # -------------------------
    gdf_veredas = gpd.read_file("data/veredas.gpkg").to_crs("EPSG:9377")
    gdf_urbanos = gpd.read_file("data/urbano_poligonos.gpkg").to_crs("EPSG:9377")

    # -------------------------
    # 2. Población total Antioquia (demografía)
    # -------------------------
    # (por ahora simplificado, luego entran parámetros reales)
    total_antioquia = 6500000 * (1 + 0.01 * (ano - 2020) / 5)

    gdf_veredas["POBLACION"] = (
        total_antioquia / len(gdf_veredas)
    )

    # -------------------------
    # 3. Urbano / rural
    # -------------------------
    urbano, rural = clasificar_urbano_rural(
        gdf_veredas, gdf_urbanos
    )

    if zona == "Urbana":
        gdf = urbano
    elif zona == "Rural":
        gdf = rural
    else:
        gdf = gdf_veredas

    # -------------------------
    # 4. KDE
    # -------------------------
    puntos = puntos_ponderados(gdf, "POBLACION")

    kde = kde_superficie(
        puntos,
        bandwidth=800 if zona != "Rural" else 1500
    )

    # -------------------------
    # 5. Raster
    # -------------------------
    bounds = gdf.total_bounds
    grid_x, grid_y = crear_grid(bounds, resolucion)
    raster = evaluar_kde(kde, grid_x, grid_y)

    # -------------------------
    # 6. Cierre de masa
    # -------------------------
    raster = raster * (total_antioquia / raster.sum())

    return raster, bounds, total_antioquia
