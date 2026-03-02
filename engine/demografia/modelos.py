# engine/demografia/modelos.py
import numpy as np

def modelo_logistico(t, K, r, t0):
    """
    Modelo logístico clásico
    t  : año
    K  : capacidad de carga
    r  : tasa de crecimiento
    t0 : año de inflexión
    """
    return K / (1 + np.exp(-r * (t - t0)))
