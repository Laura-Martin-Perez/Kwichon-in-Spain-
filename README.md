# Kwichon (regreso a lo rural) en España
Análisis de los movimientos migratorios dentro de España. ¿Se están volviendo a repoblar las zonas rurales?

<img src="https://user-images.githubusercontent.com/113755985/229598369-47405110-7455-433a-afe0-997b46a52b91.png" width="500" height= "350">

## INTRODUCCIÓN
En Corea del Sur, la población está migrando a zonas rurales durante los últimos años (a raíz de la pandemia) y a este fenómeno lo llaman KWICHON. Esta palabra significa literalmente 'vuelta a lo rural').

A raíz de la pandemia, es un hecho que ha habido cambio sociológico en nuestro comportamiento y este fenómeno se ha comenzado a dar a nivel mundial.

En este proyecto quiero analizar si en España también está sucediendo durante estos últimos años una vuelta a las poblaciones rurales.
Este fenómeno también es muy positivo para repoblar las zonas rurales que durante los últimos años se han ido quedando vacías por la migración a grandes ciudades y capitales de provincia.


## ANÁLISIS
He descargado los ficheros de datos de los movimientos de población del año 2006 al 2021 del INE (Instituto Nacional de Estadística), así como los datos necesarios para obtener la relación entre códigos y nombres de municipios, provincias y comunidades autónomas.

Durante el análisis he tenido en cuenta como zonas rurales a los municipios con menos de 20.000 habitantes.

Para realizar el estudio he preparado 4 notebooks y una librería de funciones (funciones_kwichon.py) para utilizar en este proyecto.

- Kwichon_Spain_Datos.ipynb:
     Descargar la carpeta datos que contiene los archivos con las migraciones de: https://drive.google.com/drive/folders/1QGW4sFkmz6wWSkeby4oPHDzKO6STyRiB?usp=sharing
  
  Manipulación de datos y generación de 4 ficheros csv para poder utilizar en los siguientes notebooks y futuros estudios.
  Se guardan en la carpeta csv_files junto con el archivo cod_ccaa.csv.
  Se puede descargar la carpeta aquí: https://drive.google.com/drive/folders/1sncg5KzVbL3fYQish_0YwmA5XnlicorQ?usp=sharing

  * migraciones_2006_2021.csv: total de migraciones, casi 41 millones de registros. Cada registro es el movimiento de una persona.
  * solo_migr_2006_2021.csv: se eliminan del archivo anterior las migraciones de personas que se han ido a vivir al extranjero y las que han venido del extranjero. 
                             Casi 26 millones de registros.
  * cod_muni.csv: Relación de códigos de municipio y nombre.
  * cod_prov.csv: Relación de códigos de provincia y nombre.
  * cod_ccaa.csv: Relación de códigos de comunidades autónomas y nombre. Y también códigos de provincia y nombre que le pertenece a cada una.

- Kwichon_Spain_Visualizaciones_municipios.ipynb: Preparación de datos y visualización de migraciones teniendo en cuenta los tamaños del municipio.
  * Lineplot del número de migraciones por año y tamaño de municipio.
  * Gráfico Sankey de migraciones entre tamaño de municipios.
  * Gráfico de barras acumulado de migraciones distinguiendo entre las realizadas a zonas rurales o no rurales:
      Ratio del total de migraciones por por sexo.
      Migraciones por grupos de edad.
      Ratio del total de migraciones por por sexo.

- Kwichon_Spain_Visualizaciones_provincias.ipynb: Preparación de datos y visualización de migraciones teniendo en cuenta las migraciones entre provincias.
  * Mapas coropléticos:
      Saldo de migraciones entre provincias.
      Saldo de migraciones entre provincias teniendo en cuenta el ratio de migraciones por la población en el año de inicio de la exploración.
      Saldo de migraciones rurales entre provincias.
      Saldo de migraciones rurales entre provincias teniendo en cuenta el ratio de migraciones por la población en el año de inicio de la exploración.  
   * Gráficos circulares:
      Total de migraciones por provincia
      Solo migraciones entre diferentes provincias y en número superior al 10% del valor máximo
      Total de migraciones a zonas rurales por provincia  
      Solo migraciones a zonas rurales entre diferentes provincias y en número superior al 5% del valor máximo

- Kwichon_Spain_Prediccion.ipynb: He entrenado  los datos de las migraciones entre los últimos años (2020 y 2021) con el modelo XGBoost(XGBClassifier) para obtener, a partir de las variables: sexo, edad, provincia de nacimiento y provincia de baja, la probabilidad (predictproba) del valor de la variable provincia de alta.
  Con este modelo propongo un ‘recomendador de pueblos’ en la aplicación Kwichon.py (con Streamlit).
  
  De las webs:  www.venteaviviraunpueblo.com y www.volveralpueblo.com, he extraído los pueblos mostrados y que ofrecen información para aquellas personas que quieran   
  explorar la posibilidad de ir a vivir a un pueblo.

  Se muestran en un mapa los pueblos correspondientes al resultado de la predicción de las 3 provincias de destino que el modelo indica con la probabilidad más alta.


Por último, he preparado con Streamlit una aplicación donde muestro algunos gráficos resultado del estudio pudiendo escoger el rango de años a visualizar y un ‘recomendador de pueblos’ para ayudar a explorar a que pueblo nos podemos ir a vivir.
 - Ficheros:
   * Kwichon.py
   * En el directorio pages: Exploración_municipios.py, Exploración_provincias.py y Predicción.py


## CONCLUSIONES

Los movimientos a zonas rurales representan un 38% respecto al total de migraciones.

La mayoría se realizan dentro de la misma provincia tanto a nivel global como entre municipios rurales (menos de 20.000 habitantes.

Se observa una descentralización de las principales ciudades como Madrid y Barcelona hacia provincias colindantes.

Para futuros estudios se puede observar si esto puede ser motivado por la mejora de comunicaciones con mejores infraestructuras de carreteras y transporte, o bien debido al aumento de empresas que ofrecen teletrabajo.


## Organización

4 notebooks de Jupyter, fichero de funciones para el proyecto (funciones_kwichon.py)  
Carpeta datos:  Datos descargados de www.ine.es  
Carpeta csv.files: Ficheros con las tablas generadas del notebook Kwichon_Spain_Datos  
Carpeta geojon_files: Ficheros geojson descargados para visualizar los mapas  
Carpeta xgb_filles: Ficheros generados de los entrenamientos del modelo XGBClassifier  
Carpeta kwichon_streamlit: Ficheros para la aplicación Kwichon para la presentación del proyecto. IMPORTANTE: Descargar los ficheros .pkl de este enlace: https://drive.google.com/drive/folders/1qsFj6ED1pz5MApdSHk4E5wQm3pkSd06C?usp=sharing en esta carpeta.


## Librerías utilizadas:
pandas 1.4.2  
matplotlib.pyplot 3.7.1  
seaborn 0.11.2  
geopandas 0.12.2  
folium 0.14.0  /  folium.pluggins  /  folium.features.GeoJsonTooltip  
pycirclize 0.3.0  / pycirclize.Circos   /  pycirclize.parser.Matrix  
sklearn.model_selection. train_test_split  
sklearn.metrics.classification_report  
sklearn.preprocessing.OrdinalEncoder  
xgboost.XGBClassifier  1.7.4  
streamlit 1.20.0  
streamlit-folium 0.11.1  

funciones.kwichon.py - librería de funciones para este proyecto


## Fuentes de datos:

Microdatos de la Estadística de variaciones residenciales de la web del INE (Instituto Nacional de Estadística).
https://www.ine.es/dyngs/INEbase/es/operacion.htm?c=Estadistica_C&cid=1254736177013&menu=resultados&secc=1254736195469&idp=1254734710990#!tabs-1254736195469

Para los mapas, provinces.geojon de:   https://github.com/martgnz/es-atlas

Datos de pueblos para el ‘recomendador de pueblos’ de:
 www.venteaviviraunpueblo.com 
 www.volveralpueblo.com


