import numpy as np
import geopandas as gpd
import tempfile
import rasterio
from rasterio.transform import from_origin
from pathlib import Path

from engine.espacial.kernel import puntos_ponderados, kde_superficie
from engine.espacial.raster import crear_grid, evaluar_kde


DATA_DIR = Path("data")


def cargar_capa(path, crs="EPSG:9377"):
    if not path.exists():
        raise FileNotFoundError(f"No se encontró la capa: {path}")
    gdf = gpd.read_file(path)
    if gdf.crs is None:
        gdf = gdf.set_crs(crs)
    else:
        gdf = gdf.to_crs(crs)
    return gdf


def ejecutar_pipeline_antioquia(
    ano,
    zona="Total",
    resolucion=500
):
    """
    Devuelve:
    - raster (np.ndarray)
    - bounds
    - total poblacional
    """

    # -------------------------
    # 1. Capas base (SHP)
    # -------------------------
    gdf_veredas = cargar_capa(
        DATA_DIR / "VeredasCV.shp"
    )

    # -------------------------
    # 2. Población total (placeholder)
    # -------------------------
    total_antioquia = 6_500_000 * (1 + 0.01 * (ano - 2020) / 5)

    gdf_veredas["POBLACION"] = total_antioquia / len(gdf_veredas)

    # -------------------------
    # 3. Zona (robusto)
    # -------------------------
    if zona in ["Urbana", "Rural"]:
        # Aún no hay capa urbana → fallback seguro
        pass

    gdf = gdf_veredas

    # -------------------------
    # 4. KDE
    # -------------------------
    puntos = puntos_ponderados(gdf, "POBLACION")

    kde = kde_superficie(
        puntos,
        bandwidth=800
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
        transform=transform,
    ) as dst:
        dst.write(raster, 1)

    return tmp.name
