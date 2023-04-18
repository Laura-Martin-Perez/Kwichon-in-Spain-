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
	## Predicción con XGBOOST
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
cod_prov.drop(index=52,axis=1,inplace=True)
cod_prov.set_index('CPRO', inplace=True)

list_cod_prov = cod_prov['NOMBRE'].tolist()
sel_index = cod_prov.index.tolist()
#sel_index.pop()


if st.checkbox('Datos:'):

	st.markdown(''' ### Dime quien eres...''')


	sexo = st.multiselect('Sexo', ('Hombre', 'Mujer'))
	prov_nac = st.multiselect('Provincia de nacimiento', list_cod_prov)
	edad = st.number_input('Dime tu edad', value=0)
	prov_baja = st.multiselect('Provincia donde vives', list_cod_prov)


	if st.checkbox('Buscar'):	

		if sexo == 'Hombre':
			s = 1
		else:
			s=6

		persona = pd.DataFrame({'SEXO':s, 'PROVNAC': list_cod_prov.index(prov_nac[0]), 'EDAD': edad, 'PROVBAJA':list_cod_prov.index(prov_baja[0]),}, index =[0])


		resultado = model_pred.predict_proba(persona).ravel()
		sel =  pd.Series(resultado, index=sel_index).sort_values(ascending=False).head(3).index
		prov_destino = cod_prov.iloc[sel]['NOMBRE']
		lista_destino= prov_destino.index.tolist()
		data_pred = df_prediccion[df_prediccion['Cod_prov'].isin(lista_destino)]



		st.markdown(''' ### Y te diré a que pueblo puedes ir''')

		#st.text(f"{list_cod_prov[lista_destino[0]-1]},{list_cod_prov[lista_destino[1]-1]},{list_cod_prov[lista_destino[2]-1]}")


	
		mapa = folium.Map(location=[40,-4], zoom_start=6, width=700, height=500, control_scale=True, tiles='CartoDB Positron') 
		geopath = data_pred.geometry.to_json()
		pueblos = folium.features.GeoJson(geopath)
		mapa.add_child(pueblos)
		# Se añade popup con la información y enlace a la web de los pueblos
		for i in range(0,len(data_pred)):
			html=f"""
   		     	<h3> {data_pred.iloc[i]['Municipio']}<h3>
   	    	 	<h4> {data_pred.iloc[i]['Provincia']}</h4>
        		<p> <a href="{data_pred.iloc[i]['Link_web']}" target="_blank">{data_pred.iloc[i]['Link_web']} </a> </p>
        		"""
			iframe = folium.IFrame(html=html, width=400, height=150)
			popup = folium.Popup(iframe, max_width=2650)
			folium.Marker(
      		  	location=[data_pred.iloc[i]['lat'], data_pred.iloc[i]['lng']],
        		popup=popup
    		).add_to(mapa)

		st_data = st_folium(mapa, width= 1200, height=1100)


