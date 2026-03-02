# app/engine/pipeline/runner.py

import os
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


# -------------------------------------------------
# Utilidad robusta de carga espacial
# -------------------------------------------------
def cargar_capa(nombre_base, crs="EPSG:9377"):
    rutas = [
        f"data/{nombre_base}.gpkg",
        f"data/{nombre_base}.shp"
    ]

    for ruta in rutas:
        if os.path.exists(ruta):
            gdf = gpd.read_file(ruta)
            if gdf.crs is None:
                gdf = gdf.set_crs(crs)
            else:
                gdf = gdf.to_crs(crs)
            return gdf

    raise FileNotFoundError(
        f"No se encontró la capa '{nombre_base}' en formatos .gpkg o .shp"
    )


# -------------------------------------------------
# Pipeline principal Antioquia
# -------------------------------------------------
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
    # 1. Capas base (ROBUSTO)
    # -------------------------
    gdf_veredas = cargar_capa("veredas")
    gdf_urbanos = cargar_capa("urbano_poligonos")

    # -------------------------
    # 2. Población total (placeholder)
    # -------------------------
    total_antioquia = 6_500_000 * (1 + 0.01 * (ano - 2020) / 5)

    gdf_veredas["POBLACION"] = total_antioquia / len(gdf_veredas)

    # -------------------------
    # 3. Urbano / Rural
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


# -------------------------------------------------
# Guardar raster temporal
# -------------------------------------------------
def guardar_raster_temporal(raster, bounds, resolucion):
    minx, miny, maxx, maxy = bounds
    transform = from_origin(minx, maxy, resolucion, resolucion)

    tmp = tempfile.NamedTemporaryFile(
        suffix=".tif",
        delete=False
    )

    with rasterio.open(
        tmp.name,
        "w",
        driver="GTiff",
        height=raster.shape[0],
        width=raster.shape[1],
        count=1,
        dtype=raster.dtype,
        crs="EPSG:9377",
        transform=transform
    ) as dst:
        dst.write(raster, 1)

    return tmp.name
