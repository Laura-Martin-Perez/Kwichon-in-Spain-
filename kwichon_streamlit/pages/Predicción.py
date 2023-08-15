import streamlit as st
import pandas as pd

import matplotlib.pyplot as plt
import geopandas as gpd

import folium
from folium import plugins
from folium.features import GeoJsonTooltip
from streamlit_folium import st_folium

import funciones_kwichon as f

st.markdown('''
	## Recomendador de pueblos
	''')


@st.cache_data
def load_xgboost():
	model_pred= pd.read_pickle("xgboost_prov_6d.pkl")
	return model_pred

model_pred = load_xgboost()


 
@st.cache_data
def load_data_mapa():
	df = pd.read_pickle('df_prediccion.pkl')
	return (df)

df_prediccion = load_data_mapa()



@st.cache_data
def load_data_prov():
    df = pd.read_pickle('cod_prov.pkl')
    return df

cod_prov= load_data_prov()
cod_prov.set_index('CPRO', inplace=True)

list_cod_prov = cod_prov['NOMBRE'].tolist()
sel_index = cod_prov.index[0:52].tolist()


if st.sidebar.checkbox('Predicción con XGBoost'):

	st.markdown(''' ### Dime quien eres...''')


	sexo = st.multiselect('Sexo', ('Hombre', 'Mujer'))
	prov_nac = st.multiselect('Provincia de nacimiento', list_cod_prov)
	edad = st.number_input('Dime tu edad', value=0)
	prov_baja = st.multiselect('Provincia donde vives', list_cod_prov)



	if (edad < 0 ):
		st.error('Indica un valor de edad correcto')
	else:
		if st.checkbox('Buscar'):	

			if not sexo:
				st.error('Selecciona una opción de sexo')

			elif len(sexo)>1:
				st.error('Selecciona solo UNA opción de Sexo')

			else:
				if not prov_nac:
					st.error('Selecciona una opción de Provincia de nacimiento')
				elif len(prov_nac)>1:
					st.error('Selecciona solo UNA opción de Provincia de nacimiento')
				else:

					if not prov_baja:
						st.error('Selecciona una opción de Provincia donde vives')
					elif len(prov_baja)>1:
						st.error('Selecciona solo UNA opción de Provincia donde vives')
					else:

						if sexo == 'Hombre':
							s = 1
						else:	
							s = 6

						persona = pd.DataFrame({'SEXO':s, 'PROVNAC': list_cod_prov.index(prov_nac[0])+1, 'EDAD': edad, 'PROVBAJA':list_cod_prov.index(prov_baja[0])+1,}, index =[0])
						resultado = model_pred.predict_proba(persona).ravel()
						sel =  pd.Series(resultado, index=sel_index).sort_values(ascending=False).head(3).index
						prov_destino = cod_prov.loc[sel,'NOMBRE']
						lista_destino= prov_destino.index.tolist()					
						data_pred = df_prediccion[df_prediccion['Cod_prov'].isin(lista_destino)]


						st.markdown(''' ### Y te diré a que pueblo puedes ir''')

						mapa= f.plot_map_pueblos (data_pred)
						st.write('www.venteaviviraunpueblo.com   -   www.volveralpueblo.org')
						st_data = st_folium(mapa, width= 1200, height=600)

if st.sidebar.checkbox('Fin'):
	st.image('https://www.caceresimpulsa.com/wp-content/uploads/2021/01/Hervas_Panorama.jpg')

