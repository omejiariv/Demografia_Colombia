# engine/espacial/clasificacion.py

import numpy as np

CLASES_DENSIDAD = [
    (0, 1),
    (1, 10),
    (10, 50),
    (50, 200),
    (200, 1000),
    (1000, np.inf)
]

def clasificar_densidad(raster):
    clasificado = np.zeros_like(raster, dtype=np.uint8)

    for i, (low, high) in enumerate(CLASES_DENSIDAD, start=1):
        mask = (raster >= low) & (raster < high)
        clasificado[mask] = i

    return clasificado
