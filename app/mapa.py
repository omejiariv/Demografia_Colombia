# app/mapa.py

import streamlit as st
import geopandas as gpd
import leafmap.foliumap as leafmap
from pathlib import Path

from modelo import obtener_raster


DATA_DIR = Path("data")


def cargar_capa(path, crs="EPSG:4326"):
    """
    Carga una capa espacial de forma robusta.
    - Verifica existencia
    - Reproyecta si es necesario
    """
    if not path.exists():
        st.error(f"No se encontró la capa: {path}")
        st.stop()

    gdf = gpd.read_file(path)

    if gdf.crs is None:
        gdf = gdf.set_crs(crs)
    else:
        gdf = gdf.to_crs(crs)

    return gdf


def mapa_principal(escala, nivel, ano, zona):
    st.subheader("Mapa de distribución poblacional")

    st.write(f"**Escala:** {escala}")
    st.write(f"**Nivel:** {nivel}")
    st.write(f"**Año:** {ano}")
    st.write(f"**Zona:** {zona}")

    # -------------------------
    # 1. Obtener raster
    # -------------------------
    try:
        raster_path, total = obtener_raster(ano, zona)
    except Exception as e:
        st.error("Error al generar el raster poblacional")
        st.exception(e)
        st.stop()

    # -------------------------
    # 2. Crear mapa base
    # -------------------------
    m = leafmap.Map(
        center=[6.5, -75.5],  # Antioquia
        zoom=7,
        basemap="CartoDB.Positron"
    )

    # -------------------------
    # 3. Raster de densidad
    # -------------------------
    m.add_raster(
        raster_path,
        layer_name=f"Densidad poblacional {ano}",
        colormap=[
            "#f7fbff",
            "#deebf7",
            "#c6dbef",
            "#9ecae1",
            "#6baed6",
            "#2171b5",
        ],
        opacity=0.85,
    )

    # -------------------------
    # 4. Cabeceras municipales
    #    (centroides de municipios)
    # -------------------------
    municipios_path = DATA_DIR / "MunicipiosAntioquia.geojson"

    if municipios_path.exists():
        gdf_municipios = cargar_capa(municipios_path)
        gdf_cabeceras = gdf_municipios.copy()
        gdf_cabeceras["geometry"] = gdf_cabeceras.centroid

        m.add_gdf(
            gdf_cabeceras,
            layer_name="Cabeceras municipales",
            style={
                "radius": 3,
                "color": "black",
                "fillColor": "red",
                "fillOpacity": 0.9,
            },
        )
    else:
        st.warning("No se encontró la capa de municipios. Se omiten cabeceras.")

    # -------------------------
    # 5. Mostrar mapa
    # -------------------------
    m.to_streamlit(height=600)

    # -------------------------
    # 6. Leyenda
    # -------------------------
    st.markdown(
        """
        ### Densidad poblacional (hab/km²)

        - < 1  
        - 1 – 10  
        - 10 – 50  
        - 50 – 200  
        - 200 – 1.000  
        - > 1.000  

        ---
        **Población total estimada:** {:,.0f}
        """.format(total)
    )
