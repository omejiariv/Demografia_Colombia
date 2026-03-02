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

def modelo_logistico_zona(t, params):
    """
    params = {
        'K_urb':,
        'r_urb':,
        't0_urb':,
        'K_rur':,
        'r_rur':,
        't0_rur':
    }
    """
    urb = modelo_logistico(t, params["K_urb"], params["r_urb"], params["t0_urb"])
    rur = modelo_logistico(t, params["K_rur"], params["r_rur"], params["t0_rur"])
    return urb, rur, urb + rur

