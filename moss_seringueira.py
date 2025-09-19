# streamlit run .\moss_seringueira.py

# Instalar bibliotecas necessárias com:
# pip install geopandas
# pip install streamlit
# pip install folium
# pip install streamlit_folium

import geopandas as gpd
import pandas as pd
import streamlit as st
import folium
from streamlit_folium import st_folium

# Seta a página como sendo no formato 'wide'
st.set_page_config(layout="wide")

# Adiciona título e descrição ao app
st.markdown(
    "<h1 style='text-align: center;'>Seringueira Project APD and AUD</h1>",
    unsafe_allow_html=True)

# # Carregar o shapefile dos municípios do Mato Grosso (MT)
gdf_apd = gpd.read_file('/moss_seringueira/PA_APD_Seringueira_Agrupado.shp')
gdf_aud = gpd.read_file('/moss_seringueira/PA_AUD_Seringueira_Agrupado.shp')

# print(gdf_apd.head())
# print(gdf_aud.head())

# Cálculo do centróide para o mapa
centroide = gdf_aud.geometry.centroid.iloc[0]
centroid_y, centroid_x = centroide.y, centroide.x

# Cria o mapa base com camadas extras
m = folium.Map(location=[centroid_y, centroid_x], zoom_start=8, tiles=None)

folium.TileLayer('opentopomap', name='OpenTopoMap',show=False).add_to(m)
folium.TileLayer('Esri.NatGeoWorldMap', name='Esri.NatGeoWorldMap',show=False).add_to(m)
folium.TileLayer('Stadia.AlidadeSatellite', name='ImageSatellite',show=False).add_to(m)
folium.TileLayer('OpenStreetMap', name='OpenStreetMap').add_to(m)

    # Polígono do município selecionado (destaque vermelho)
folium.GeoJson(
    gdf_aud,
    name='PA_AUD_Seringueira_Agrupado',
    style_function=lambda x: {'color': 'pink', 'weight': 3, 'fillOpacity': 0.1}
).add_to(m)

    # Polígono do Estado selecionado (destaque cinza)
folium.GeoJson(
    gdf_apd,
    name='PA_APD_Seringueira_Agrupado',
    style_function=lambda x: {'color': 'yellow', 'weight': 2, 'fillOpacity': 0.1},
    control=False
).add_to(m)

# Controle das camadas de fundo
folium.LayerControl().add_to(m)

st_folium(m, width=None, height=600)
