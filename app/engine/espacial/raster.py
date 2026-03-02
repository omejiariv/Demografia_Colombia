# app/engine/espacial/raster.py

import numpy as np

def evaluar_kde(kde, grid_x, grid_y):
    xy = np.vstack([grid_x.ravel(), grid_y.ravel()]).T
    z = np.exp(kde.score_samples(xy))
    return z.reshape(grid_x.shape)

def crear_grid(bounds, resolucion=500):
    minx, miny, maxx, maxy = bounds
    x = np.arange(minx, maxx, resolucion)
    y = np.arange(miny, maxy, resolucion)
    return np.meshgrid(x, y)
