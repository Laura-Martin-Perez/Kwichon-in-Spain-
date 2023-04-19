import pandas as pd
import numpy as np
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import geopandas as gpd
import folium
from folium import plugins
from pycirclize import Circos
from pycirclize.parser import Matrix

def replace_col_data (df, col, data):
# Devuelve un diccionario donde se reasignan los valores de la columna del dataframe por los valores del diccionario.
# Los valores de la columna coinciden con las keys del diccionario
# Parámetros: df: dataframe
#             col: nombre de columna o lista de nombres de columnas
#             data: diccionario de datos a reemplazar

    for c in col:
        for k,v in data.items():
            df[col] = df[col].replace(k, v)
            
    return df


def migrations_tables (year_start, year_end):
    # devuelve un dataframe con la descarga de archivos de migraciones de la franja de años indicada
    # Parámetros: 
    #           year_start: año de inicio
    #           year_end: año de fin

    df = pd.DataFrame()
    for year in range (year_start, year_end+1):
        df = pd.concat([df,pd.read_csv(f'./datos/MIGRACIONES/datos_{year}/CSV/EVR_{year}.csv', sep='\t', low_memory=False)], ignore_index=True)
    
    df.drop(columns=['MUNINAC', 'MESNAC','ANONAC','CNAC','MESVAR','TAMUNACI'], inplace=True)
    
    return (df)

def plot_sankey (df, year_start, year_end,plot=True):
# Muestra gráfico Sankey pasando el dataframe y los años a visualizar
# Parámetros: df: dataframe
#             year_start: año de inicio
#             year_end: año de fin
#             plot = True:  Se puede elegir si se quiere mostrar al llamar la función o no

    year = [y for y in range(year_start,year_end+1)]
    df = df[df['ANOVAR'].isin(year)]
    df = df.groupby(by=['TAMUBAJA','TAMUALTA'], as_index=False).count()
    df['CODTAMUBAJA']= df['TAMUBAJA'].apply(lambda x: x-1)
    
    df['CODTAMUALTA']= df['TAMUALTA'].apply(lambda x: x+5)

    # Defino los colores de los nodos para el gráfico
    color_node = ['rgba(0, 40, 145, 0.8)','rgba(18, 131, 40, 0.8)','rgba(241, 234, 77, 0.8)',
                  'rgba(244, 180, 40, 0.8)', 'rgba(221, 83, 215, 0.8)','rgba(235, 10, 38, 0.8)',
                  'rgba(0, 40, 145, 0.8)','rgba(18, 131, 40, 0.8)','rgba(241, 234, 77, 0.8)',
                  'rgba(244, 180, 40, 0.8)', 'rgba(221, 83, 215, 0.8)','rgba(235, 10, 38, 0.8)'
                ]

    source = df['TAMUBAJA'].apply(lambda x: x-1).tolist()

    fig = go.Figure(data=[go.Sankey(
        node = dict(
        pad = 15,
        thickness = 20,
        line = dict(color = "black", width = 0.5),
        label = ['Hasta 10.000 habitantes', 
                'Municipio no capital de 10.001 a 20.000',
                'Municipio no capital de 20.001 a 50.000', 
                'Municipio no capital de 50.001 a 100.000',      
                'Municipio no capital de más de 100.000',        
                'Municipio capital de provincia','Hasta 10.000 habitantes', 
                'Municipio no capital de 10.001 a 20.000',
                'Municipio no capital de 20.001 a 50.000', 
                'Municipio no capital de 50.001 a 100.000',      
                'Municipio no capital de más de 100.000',        
                'Municipio capital de provincia'],
        
        x = [0.001, 0.001, 0.001, 0.001, 0.001, 0.001, 1, 1, 1, 1, 1, 1],
            
        y = [0.01, 43/200, 77/200, 115/200, 151/200, 193/200, 0.001, 43/200, 77/200, 115/200, 151/200, 193/200], 
        color = color_node
        
        ),
        link = dict(
         source = source,
         target = df['TAMUALTA'].apply(lambda x: x+5).tolist(), 
         value = df['ANOVAR'].tolist(),
         color = [color_node[i].replace('0.8','0.4') for i in source]
         ))])

    fig.update_layout(title_text=f'De {year_start} a {year_end}')
    if plot:
        fig.show()
    else:
        return fig


def tabla_saldo_tamu (df, year_start, year_end):
# Función que genera una tabla con el año, el tamaño de municipio de alta y el saldo de migraciones
# Se le pasa como parámetros la tabla con los tamaños de municipio de alta y baja y los años del periodo a analizar.
# Parámetros: df: dataframe
#             year_start: año de inicio
#             year_end: año de fin

    # se filtran por los años solicitados
    year = [y for y in range(year_start,year_end+1)]
    df = df[df['ANOVAR'].isin(year)]
    df_saldo = pd.DataFrame()
    df_saldo_y = pd.DataFrame()

    # Se agrupa por año y tamaño de municipio
    for y in year:
        df_y = df[df['ANOVAR']==y]
        df_y = df_y.groupby(by=['TAMUBAJA','TAMUALTA'], as_index=False).count()
        condition = df_y['TAMUBAJA']==df_y['TAMUALTA']
        df_baja = df_y[~condition].groupby(by='TAMUBAJA',as_index=False).sum()
        df_alta = df_y[~condition].groupby(by='TAMUALTA',as_index=False).sum()
        df_baja = df_y.groupby(by='TAMUBAJA',as_index=False).sum()
        df_alta = df_y.groupby(by='TAMUALTA',as_index=False).sum()
        df_saldo_y['Año'] = [y for i in range(6) ]
        df_saldo_y['Tamaño_municipio_alta'] = [1,2,3,4,5,6]
        df_saldo_y['Saldo'] = df_alta['ANOVAR']- df_baja['ANOVAR']
        df_saldo = pd.concat([df_saldo, df_saldo_y], ignore_index=True)

    return df_saldo


def tabla_saldo_prov (df, year_start, year_end, df_prov, df_pob):
# Función que devuelve un dataframe donde se agrupa por provincias y se muestra el total de altas, bajas y el saldo. Se añade también el nombre de la provincia 
# y el polígono para poder mostrar en un mapa 
# Parámetros: df: dataframe
#             year_start: año de inicio
#             year_end: año de fin
#             df_prov: dataframe con los valores de geometría de las provincias
#             df_pob: datafrem con los valores de la población por provincia.

    year = [x for x in range(year_start, year_end+1)]
  
    # se filtra el dataframe de los saldos por los años solicitados
    df = df[df['ANOVAR'].isin(year)]
    # se filtra el dataframe de las poblaciones por el año de inicio del periodo a visualizar
    df_pob = df_pob[df_pob['Periodo']==year_start]

    # se eliminan las columnas innecesarias
    df.drop(columns=['SEXO','PROVNAC','EDAD','MUNIALTA','MUNIBAJA','CODMUNIALTA','CODMUNIBAJA'],inplace=True)
    df_pob.drop(columns=['Provincias'])

    df_saldo_prov = pd.DataFrame()
 

    # Agrupación por provincias de alta y baja
    df_group= df.groupby(by=['PROVALTA','PROVBAJA'], as_index=False).count()

    # Agrupación por provincias de alta: Altas
    df_baja = df_group.groupby(by='PROVBAJA',as_index=False).sum()

    # Agrupación por provincias de baja: Bajas
    df_alta = df_group.groupby(by='PROVALTA',as_index=False).sum()
 
    # Se completa el dataframe añadiendo las columnas necesarias
    df_saldo_prov['PROVSALDO'] =df_alta['PROVALTA']
    df_saldo_prov['ALTAS'] = df_alta['ANOVAR']
    df_saldo_prov['BAJAS']= df_baja['ANOVAR']
    df_saldo_prov['SALDO'] = df_alta['ANOVAR']- df_baja['ANOVAR']

    # Se añade el dataframe de provincias con nombres y datos de geometria para el mapa
    df_prov['id']= df_prov['id'].apply(int)
    df_final = df_prov.merge(df_saldo_prov, left_on="id", right_on="PROVSALDO", how="inner") 

    # Se añade la población por provincia y año
    df_final = df_pob.merge(df_final, left_on="Cod_prov", right_on="PROVSALDO", how="inner") 

    df_final.drop(columns=['Provincias' ,'Cod_prov','Periodo'], inplace=True)
        
    return df_final


def tabla_kwichon (df,col, year_start, year_end):

# Función que devuelve un dataframe donde se filtra por el periodo de años pasado por parámetro, se añaden las columnas: 
# 1=destino rural (tamaño municipio 1,2 - Menos 20.000 habitantes), 0=destino no rural   (KWICHON)
# y los valores del número de migraciones en función de la columna pasada por parámetro
# Parámetros: df: dataframe
#             col: columna que determina los valores de las migraciones
#             year_start: año de inicio
#             year_end: año de fin

  
    # Se filtra el dataframe por los años solicitados
    year = [x for x in range(year_start, year_end+1)]
    df = df[df['ANOVAR'].isin(year)]

    # Se añade la columna KWICHON según sea el tamaño de municipio
    df['KWICHON']=[1 if (x==1 or x==2) else 0 for x in df['TAMUALTA']]

    # Se agrupa por la columna Kwichon contando el número de migraciones
    df_kwichon = df.groupby(by=[col,'KWICHON'], as_index=False).count()

    # Se filtra dejando solo la columna pasada por parámetro, KWICHON y ANOVAR que tienen los valores de número de migraciones
    df_kwichon = df_kwichon[[col, 'KWICHON','ANOVAR']]
    df_kwichon.columns=[col,'KWICHON','TOTAL_MIGR']   # se renombra la columna ANOVAR por TOTAL_MIGR
    # Se pone como indice la columna pasada por parámetro
    df_kwichon=df_kwichon.set_index(col)
    # Se recolocan los valores en el dataframe dejando como columnas los valores de KWICHON y los valores del número de migraciones de 'TOTAL_MIGR' 
    df_kwichon= df_kwichon.pivot(columns='KWICHON',values = 'TOTAL_MIGR')
    # Se ordenan las columnas
    df_kwichon = df_kwichon.reindex(columns=[1,0])


    return (df_kwichon)





def plot_map_saldo_prov(df_geo,df,year_start, year_end,variable):
# Función que devuelve unm mapa coroplético por provincias mostrando el saldo de la migración de la población
# Parámetros: df_geo: dataframe con los valores de geometría
#             df: dataframe con los valores del saldo / ratio de la población por provincias.
#             year_start: año de inicio
#             year_end: año de fin
#             variable: variable de los datos que se quieren mostrar por colores en el mapa

    # se convierte el df en un geodataframe
    df = gpd.GeoDataFrame(df, geometry="geometry")

    # archivo .json con polígonos de provincias
    geo = gpd.GeoSeries(df_geo.set_index('id')['geometry']).to_json()

    # Preparación de mapa de España de base
    mapa = folium.Map(location=[40,-4], zoom_start=6, width=700, height=500, control_scale=True, tiles='CartoDB Positron') 

    # Escala de colores adaptada a los valores resultantes al escoger el periodo de años
    custom_scale = (df[variable].quantile((0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1))).tolist()
    
    # Mapa coroplético indicando las migraciones por provincia
    folium.Choropleth(
                data=df,
                geo_data=geo,
                key_on='feature.id',
                columns=['PROVSALDO', variable], 
                fill_color ='RdBu', nan_fill_color='White', 
                threshold_scale = custom_scale,
                line_color='grey', line_weight=0.1,
                legend_name=f'Movimientos migratorios entre {year_start} y {year_end} ({variable})',
                highlight = True,
                    ).add_to(mapa)

    # Se añade información sobre datos de altas, bajas y saldo de cada provincia.
    folium.features.GeoJson(
                    data =df,
                    smooth_factor=2,
                    style_function=lambda x: {'color':'grey','fillColor':'transparent','weight':0.5},
                    tooltip=folium.features.GeoJsonTooltip(
                        fields=['name',
                                'ALTAS',
                                'BAJAS',
                                'SALDO',
                                'Poblacion',
                                'RATIO'
                               ],
                        aliases=['Provincia:',
                                 'Altas:',
                                 'Bajas:',
                                 'Saldo:',
                                 f'Población del año {year_start}:',
                                 'Ratio saldo vs población:'

                                ], 
                        localize=True,
                        sticky=False,
                        labels=True,
                        style="""
                            background-color: #F0EFEF;
                            border: 2px solid grey;
                            border-radius: 3px;
                            box-shadow: 3px;
                        """,
                        max_width=800,),
                            highlight_function=lambda x: {'weight':3,'fillColor':'grey'},
                        ).add_to(mapa)


    return mapa


def order_circle (df, cod_ccaa):
# Función que devuelve una lista de las provincias que aparecen en el dataframe pasado por parámetro ordenado por comunidades autónomas
# Parámetros: df: dataframe
#             cod_ccaa: dataframe con los códigos de comunidades autónomoas y provincias

    
    ccaa_list = list(cod_ccaa['Provincia'])

    provbaja_list = list(df['PROVBAJA'].unique())
    provalta_list = list(df['PROVALTA'].unique())

    # se prepara un filtro para guardar una lista ordenada con las provincias que si esten en la tabla
    mask = ((cod_ccaa['Provincia'].isin(provbaja_list)) | (cod_ccaa['Provincia'].isin(provalta_list)))
    order = [ccaa_list[i] for i in range(len(ccaa_list)) if mask[i]]

    return order



def plot_circle (df, order):
# Función que devuelve un gráfico circular de las migraciones entre provincias del dataframe pasado por parámetro en el orden establecido.
# Parámetros: df: dataframe
#             order: lista con el orden de las provincias para mostrar en el gráfico


    matrix = Matrix.parse_fromto_table(df)
    circos = Circos.initialize_from_matrix(
                    matrix,
                    space=1,
                    r_lim=(93, 100),
                    cmap="gist_rainbow",
                    label_kws=dict(size=8, r=102, color="grey", orientation='vertical'),
                    link_kws=dict(direction=1, ec="#1f1f1f",lw=1), #lw=0.5),
                    order = order
                    )

    fig = circos.plotfig()
 

def plot_map_pueblos (df):
# Función que devuelve un mapa indicando los pueblos indicados en la tabla df pasada por parámetro.
# Parámetros: df: dataframe a mostrar en el mapa datos de latitud-longitud

    mapa = folium.Map(location=[40,-4], zoom_start=6, width=700, height=500, control_scale=True, tiles='CartoDB Positron') 
    geopath = df.geometry.to_json()
    pueblos = folium.features.GeoJson(geopath)
    mapa.add_child(pueblos)
    # Se añade popup con la información y enlace a la web de los pueblos
    for i in range(0,len(df)):
        html=f"""
            <h3> {df.iloc[i]['Municipio']}<h3>
            <h4> {df.iloc[i]['Provincia']}</h4>
            <p> <a href="{df.iloc[i]['Link_web']}" target="_blank">{df.iloc[i]['Link_web']} </a> </p>
            """
    
        iframe = folium.IFrame(html=html, width=400, height=150)
        popup = folium.Popup(iframe, max_width=2650)
        folium.Marker(
            location=[df.iloc[i]['lat'], df.iloc[i]['lng']],
            popup=popup
        ).add_to(mapa)

    return mapa



