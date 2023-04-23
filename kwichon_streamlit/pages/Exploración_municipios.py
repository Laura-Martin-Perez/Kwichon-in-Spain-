import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

import funciones_kwichon as f


st.markdown('''
	## Exploración de migraciones por tamaño de municipios
	''')


@st.cache_data
def load_data_saldo():
	df = pd.read_pickle('df_saldo.pkl')
	return df

data_saldo = load_data_saldo()


@st.cache_data
def load_data_tamu():
    df = pd.read_pickle('df_tamu.pkl')
    return df

data_tamu = load_data_tamu()

@st.cache_data
def load_data_edad_ratio():
    df = pd.read_pickle('df_edad_ratio.pkl')
    return df

data_edad_ratio = load_data_edad_ratio()


total = st.sidebar.checkbox("Evolución del saldo de población por tamaño de municipio destino")
if total:

	st.markdown(''' ### Evolución del saldo de población por tamaño de municipio destino (de 2006 a 2021)''')
	st.write("Tamaño municipios :blue[Hasta 10.000 habitantes] , :green[ de 10.001 a 20.000] , de 21.000 a 50.000 , :orange[ de 50.001 a 100.000] , :violet[ más de 100.000] ,  :red[ Capitales de provincia]")
	sns.set(rc = {'figure.figsize':(20,15)}, style="ticks")
	plt.style.use("dark_background")
	sns.lineplot(data=data_saldo, x='Año' , y='Saldo', hue = 'Tamaño_municipio_alta', palette=['dodgerblue','green','gold','darkorange','fuchsia','red'], linewidth= 2)
	plt.legend(labels=[ 'Hasta 10.000 habitantes',
    	                'Municipio no capital de 10.001 a 20.000',
        	            'Municipio no capital de 20.001 a 50.000', 
            	        'Municipio no capital de 50.001 a 100.000',      
                	    'Municipio no capital de más de 100.000',        
                    	'Municipio capital de provincia'	          
	                    ]);
	st.pyplot(plt.gcf()) 




edad = st.sidebar.checkbox("Migraciones por grupos de edad")
if edad:
 
	st.markdown( ''' ### Ratio de migraciones por grupos de edad (de 2020 a 2021) ''')
	data_edad_ratio.plot(title='Ratio de migraciones por grupos de edad',kind='barh', stacked=True, color=['#128328', '#9b9b9b'], figsize = (15,8),legend='reverse');
	st.pyplot(plt.gcf())



years = [y for y in range(2006, 2022)]
sankey = st.sidebar.checkbox("Migraciones entre tamaños de municipio")
if sankey:
 
	st.markdown( ''' ### Migraciones entre tamaños de municipio ''')
	start_y = st.sidebar.selectbox(label='Desde el año:', options=years)
	end_y = st.sidebar.selectbox(label="Hasta el año:", options=years)
	if start_y <= end_y:
		fig = f.plot_sankey(data_tamu,start_y, end_y, False)
		fig.update_layout(width = 800, height=600)
		st.plotly_chart(fig)
	else:
		st.error('Selecciona un rango de años correcto')



