import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import geopandas as gpd

import folium
from folium import plugins
from folium.features import GeoJsonTooltip
from streamlit_folium import st_folium

from pycirclize import Circos
from pycirclize.parser import Matrix	
import funciones_kwichon as f


st.set_option('deprecation.showPyplotGlobalUse', False)


st.markdown('''
	## Exploración de migraciones por provincias
	''')
	
years = [y for y in range(2006, 2022)]
start_prov = st.sidebar.selectbox(label='Año inicio:', options= years)
end_prov = st.sidebar.selectbox(label="Año fin", options=years)


@st.cache_data
def load_data_geo_prov():
	df = gpd.read_file('provinces.geojson')
	return(df)
 
@st.cache_data
def load_data_saldo_prov():
	df = pd.read_pickle('df_saldo_prov.pkl')
	return (df)

df_geo= load_data_geo_prov()
df_saldo_prov = load_data_saldo_prov()

@st.cache_data
def load_data_saldo_rural():
    df = pd.read_pickle('df_saldo_rural.pkl')
    return df

df_saldo_rural=load_data_saldo_rural()



@st.cache_data
def load_data_saldo():
    df = pd.read_pickle('df_saldo.pkl')
    return df

df_saldo=load_data_saldo()


@st.cache_data
def load_data_prov():
    df = pd.read_pickle('cod_prov.pkl')
    return df

cod_prov= load_data_prov()


@st.cache_data
def load_data_ccaa():
    df = pd.read_pickle('cod_ccaa.pkl')
    return df

cod_ccaa = load_data_ccaa()


@st.cache_data
def load_data_circ_rural():
    df = pd.read_pickle('df_circ_rural.pkl')
    return df

df_circ_rural=load_data_circ_rural()


dict_cod_prov = dict(zip(cod_prov['CPRO'], cod_prov['NOMBRE']))




mapa_migr = st.sidebar.checkbox("Mapa de migraciones entre provincias")
if mapa_migr:
	if start_prov <= end_prov:
		st.markdown(''' #### Mapa de migraciones entre provincias: ''')
		st.text(f'De {start_prov} a {end_prov}')
		st.write(":red[Saldo negativo], :blue[Saldo positivo]")
		variable = 'SALDO'
		mapa_saldo = f.plot_map_saldo_prov(df_geo,df_saldo_prov,start_prov, end_prov,variable)
		st_data = st_folium(mapa_saldo, width= 900, height=600)

		st.markdown(''' #### Mapa de migraciones a zonas rurales entre provincias: ''')
		st.text(f'De {start_prov} a {end_prov}')
		st.write(":red[Saldo negativo], :blue[Saldo positivo]")
		variable = 'SALDO'
		mapa_saldo_rural = f.plot_map_saldo_prov(df_geo,df_saldo_rural,start_prov, end_prov,variable)
		st_data = st_folium(mapa_saldo_rural, width= 900, height=600)

	else:
		st.error('Selecciona un rango de años correcto')
		


circular = st.sidebar.checkbox("Gráfico circular de migraciones desde y hacia municipios rurales entre provincias")

if circular:

	if start_prov <= end_prov:
		st.markdown(''' ### Gráfico circular ''')

		year = [y for y in range(start_prov,end_prov+1)]
		df_circ_rural=df_circ_rural[df_circ_rural['ANOVAR'].isin(year)]

		st.markdown(''' #### Migraciones rurales entre provincias: ''')
		st.text(f'De {start_prov} a {end_prov}')


		df_circ_rural = df_circ_rural.groupby(by=['PROVBAJA','PROVALTA'], as_index=False).count()
		col_list = ['PROVBAJA', 'PROVALTA']
		df_circ_rural_name = f.replace_col_data(df_circ_rural, col_list, dict_cod_prov)
		order = f.order_circle(df_circ_rural_name, cod_ccaa)

		fig=f.plot_circle (df_circ_rural_name, order)
		st.pyplot(fig)

		st.markdown(''' #### Migraciones rurales solo entre otras provincias: ''')
		st.text(f'De {start_prov} a {end_prov}')
		

		# Se filtra la tabla eliminando migraciones a la misma provincia y las migraciones menores al 3% del valor máximo
		df_circ_r_reducido = df_circ_rural_name[~(df_circ_rural_name['PROVBAJA']==df_circ_rural_name['PROVALTA'])]
		# se eliminan los movimientos inferiores al 5% de máximo para visualizar mejor los datos.
		limite_migr = abs(df_circ_r_reducido['ANOVAR'].max())*5/100   # se eliminan los movimientos inferiores al 5% de máximo para visualizar mejor los datos.
		df_circ_r_reducido = df_circ_r_reducido[abs(df_circ_r_reducido['ANOVAR'])>limite_migr]

		order_r_reducido = f.order_circle(df_circ_r_reducido, cod_ccaa)

		fig_rural_reducido = f.plot_circle (df_circ_r_reducido,order_r_reducido)
		st.pyplot(fig_rural_reducido)


	else:
		st.error('Selecciona un rango de años correcto')
		
