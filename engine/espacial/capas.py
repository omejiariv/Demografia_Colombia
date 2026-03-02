# engine/espacial/capas.py

import geopandas as gpd

def cargar_capa(ruta, crs="EPSG:9377"):
    gdf = gpd.read_file(ruta)
    if gdf.crs != crs:
        gdf = gdf.to_crs(crs)
    return gdf
