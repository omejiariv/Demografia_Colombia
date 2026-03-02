# engine/espacial/restricciones.py

import rasterio
import numpy as np

def mascara_pendiente(raster_pendiente, max_grados=30):
    with rasterio.open(raster_pendiente) as src:
        slope = src.read(1)
        mask = slope <= max_grados
    return mask, src.transform
