# app/engine/espacial/kernel.py

import numpy as np

def puntos_ponderados(gdf, campo_pob, n=1000):
    puntos = []
    for _, row in gdf.iterrows():
        k = max(1, int(n * row[campo_pob] / gdf[campo_pob].sum()))
        puntos.extend(
            row.geometry.representative_point()
            for _ in range(k)
        )
    return puntos

from sklearn.neighbors import KernelDensity

def kde_superficie(puntos, bandwidth=1000):
    coords = np.array([[p.x, p.y] for p in puntos])
    kde = KernelDensity(
        bandwidth=bandwidth,
        kernel="gaussian"
    ).fit(coords)
    return kde
