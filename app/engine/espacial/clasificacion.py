# app/engine/espacial/clasificacion.py

def clasificar_densidad(valor):
    """
    Clasifica densidad poblacional (hab/km²)
    """
    if valor < 1:
        return "< 1"
    elif valor < 10:
        return "1 – 10"
    elif valor < 50:
        return "10 – 50"
    elif valor < 200:
        return "50 – 200"
    elif valor < 1000:
        return "200 – 1.000"
    else:
        return "> 1.000"
