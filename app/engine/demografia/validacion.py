# app/engine/demografia/validacion.py

def cerrar_masa(total_superior, suma_inferior, tolerancia=0.01):
    diferencia = abs(total_superior - suma_inferior)
    if diferencia > tolerancia * total_superior:
        raise ValueError(
            f"Error de masa poblacional: {diferencia}"
        )
    return True
