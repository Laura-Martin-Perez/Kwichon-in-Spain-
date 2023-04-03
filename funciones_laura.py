import pandas as pd
import numpy as np
import plotly.graph_objects as go

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
    df = df[df['ANOVAR'].isin(year)]
    df_saldo = pd.DataFrame()
    df_saldo_y = pd.DataFrame()
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
    
   






