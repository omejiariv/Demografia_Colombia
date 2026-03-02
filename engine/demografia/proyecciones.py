# engine/demografia/proyecciones.py

import pandas as pd
from .modelos import modelo_logistico

def proyectar_serie(anos, params):
    data = []
    for t in anos:
        p = modelo_logistico(t, params["K"], params["r"], params["t0"])
        data.append({"ANO": t, "POBLACION": p})
    return pd.DataFrame(data)

from .modelos import modelo_logistico_zona

def proyectar_zona(anos, params):
    rows = []
    for t in anos:
        urb, rur, tot = modelo_logistico_zona(t, params)
        rows.append({
            "ANO": t,
            "URBANO": urb,
            "RURAL": rur,
            "TOTAL": tot
        })
    return pd.DataFrame(rows)
