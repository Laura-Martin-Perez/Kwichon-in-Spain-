import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import geopandas as gpd

import folium
from folium import plugins
from folium.features import GeoJsonTooltip
from streamlit_folium import folium_static
import json

from pycirclize import Circos
from pycirclize.parser import Matrix
import funciones_kwichon as f




st.markdown('''
	# Kwichon en España
	''')



#@st.cache_data
#def load_data_prov():
#	df_prov = gpd.read_file('provinces.geojson')
#	return(df_prov)

@st.cache_data
def load_data_mapa():
	df = pd.read_csv('df_mapa.csv', index_col=0)
	#df = gpd.GeoDataFrame(df, geometry="geometry")
	return (df)

#data_prov = load_data_prov()
#data_geo = gpd.GeoSeries(data_prov.set_index('id')['geometry']).to_json()

data_geo = json.load(open('provinces.geojson'))

data_m = load_data_mapa()
###data_mapa = gpd.GeoDataFrame(data_m, geometry="geometry")


checkbox = st.checkbox("Mapa de migraciones")
if checkbox:

	years = [y for y in range(2006, 2022)]

	start_mapa = st.selectbox(label='Desde el año:', options= years)
	end_mapa = st.selectbox(label="Hasta el año", options=years)

	checkbox = st.checkbox("Mapa")

	if checkbox:

		variable = 'SALDO'
		#mapa = f.plot_map_saldo_prov(data_geo,data_mapa,start_mapa, end_mapa,variable)
		mapa = folium.Map(location=[40,-4], zoom_start=6, width=700, height=500, tiles='CartoDB Positron') #control_scale=True,
		folium.Choropleth(
				data=data_m,###  data_mapa,
                geo_data=data_geo,  
                key_on='features.properties.id',
                columns=['PROVSALDO', variable], 
                fill_color ='Spectral', nan_fill_color='White', 
                #threshold_scale = custom_scale,
                line_color='grey', line_weight=0.1,
                legend_name=f'Movimientos migratorios entre {start_mapa} y {end_mapa} ({variable})',
                highlight = True,
                    ).add_to(mapa)

		st_data =folium_static(mapa)#, width=725)
