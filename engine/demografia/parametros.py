# engine/demografia/parametros.py

import pandas as pd

class ParametrosLogisticos:
    def __init__(self):
        self.params = {}

    def cargar_desde_excel(self, ruta, escala):
        df = pd.read_excel(ruta)
        self.params[escala] = df

    def obtener(self, escala, codigo):
        df = self.params[escala]
        fila = df[df["CODIGO"] == codigo].iloc[0]
        return {
            "K": fila["K"],
            "r": fila["r"],
            "t0": fila["t0"]
        }
