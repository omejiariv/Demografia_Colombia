# app/engine/espacial/calibracion.py

import numpy as np

def calibrar_raster(raster_modelo, raster_worldpop):
    factor = raster_worldpop.sum() / raster_modelo.sum()
    return raster_modelo * factor
