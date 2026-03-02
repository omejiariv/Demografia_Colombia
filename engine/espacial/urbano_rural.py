# engine/espacial/urbano_rural.py

import geopandas as gpd

def clasificar_urbano_rural(veredas, poligonos_urbanos):
    urbano = gpd.overlay(veredas, poligonos_urbanos, how="intersection")
    rural = gpd.overlay(veredas, poligonos_urbanos, how="difference")
    urbano["ZONA"] = "URBANA"
    rural["ZONA"] = "RURAL"
    return urbano, rural
