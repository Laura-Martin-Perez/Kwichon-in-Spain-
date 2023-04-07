import pandas as pd
import numpy as np
import plotly.graph_objects as go
import geopandas as gpd
import folium
from folium import plugins

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

def plot_sankey (df, year):
# Muestra gráfico Sankey pasando el dataframe y los años a visualizar

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

    fig.update_layout(title_text="Movimientos migratorios", font_size=10)
    fig.show()


def tabla_saldo_tamu (df, year):

    # se filtran por los años solicitados
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
        df_saldo_y['YEAR'] = [y for i in range(6) ]
        df_saldo_y['TAMU'] = [1,2,3,4,5,6]
        df_saldo_y['SALDO'] = df_alta['ANOVAR']- df_baja['ANOVAR']
        df_saldo = pd.concat([df_saldo, df_saldo_y], ignore_index=True)

    return df_saldo


def tabla_saldo_prov (df, year, df_prov, df_pob):
# Función que devuelve un dataframe donde se agrupa por provincias y se muestra el total de altas, bajas y el saldo. Se añade también el nombre de la provincia 
# y el polígono para poder mostrar en un mapa 
  
    # se filtran por los años solicitados
    df = df[df['ANOVAR'].isin(year)]
    df_pob = df_pob[df_pob['Periodo'].isin(year)]

    # se eliminan las columnas innecesarias
    df.drop(columns=['SEXO','PROVNAC','EDAD','MUNIALTA','MUNIBAJA','CODMUNIALTA','CODMUNIBAJA'],inplace=True)
    df_pob.drop(columns=['Provincias'])

    df_saldo_prov = pd.DataFrame()

    # Agurpación del dataframe de las poblaciones por provincia
    df_pob_agr = df_pob.groupby(by='Cod_prov', as_index=False).median()
 

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

    # se añade el dataframe de provincias con nombres y datos de geometria para el mapa
    df_prov['id']= df_prov['id'].apply(int)
    df_prov_geo = df_prov.merge(df_saldo_prov, left_on="id", right_on="PROVSALDO", how="outer") 

    # Se añade la población por provincia y año
    df_final = df_prov_geo.merge(df_pob_agr, left_on="PROVSALDO", right_on="Cod_prov", how="outer") 

    df_final.drop(columns=['Cod_prov','Periodo'], inplace=True)
        
    return df_final

def plot_map_saldo_prov(df_geo,df,year):
# Función que devuelve unm mapa coroplético por provincias mostrando el saldo de la migración de la población

    # archivo .json con polígonos de provincias
    geo = gpd.GeoSeries(df_geo.set_index('id')['geometry']).to_json()
    # Preparación de mapa de España de base
    mapa = folium.Map(location=[40,-4], zoom_start=6, width=700, height=500, control_scale=True, tiles='CartoDB Positron') 
    # Escala de colores adaptada a los valores resultantes al escoger el periodo de años
    custom_scale = (df['SALDO'].quantile((0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1))).tolist()
    # Mapa coroplético indicando las migraciones por provincia
    folium.Choropleth(
                data=df,
                geo_data=geo, 
                key_on='feature.id', 
                columns=['PROVSALDO', 'SALDO'], 
                fill_color ='Spectral',
                nan_fill_color='White', 
                threshold_scale = custom_scale,
                legend_name=f'Movimientos migratorios entre {year[0]} y {year[-1]}',
                highlight = True
                    ).add_to(mapa)

    # Se añade información sobre datos de altas, bajas y saldo de cada provincia.
    folium.features.GeoJson(
                    data =df,
                    name= f'Movimientos migratorios entre {year[0]} y {year[-1]}',
                    smooth_factor=2,
                    style_function=lambda x: {'color':'black','fillColor':'transparent','weight':0.5},
                    tooltip=folium.features.GeoJsonTooltip(
                        fields=['name',
                                'ALTAS',
                                'BAJAS',
                                'SALDO',
                                'Poblacion'
                               ],
                        aliases=["Provincia:",
                                 'Altas:',
                                 'Bajas:',
                                 "Saldo:",
                                 "Mediana de Población del periodo:"
                                ], 
                        localize=True,
                        sticky=False,
                        labels=True,
                        style="""
                            background-color: #F0EFEF;
                            border: 2px solid black;
                            border-radius: 3px;
                            box-shadow: 3px;
                        """,
                        max_width=800,),
                            highlight_function=lambda x: {'weight':3,'fillColor':'grey'},
                        ).add_to(mapa) 

    return mapa




