








<h1 align="center"> PROYECTO INDIVIDUAL N° 1 - MLOps </h1>








## MACHINE LEARNING OPERATIONS









**INTRODUCCIÓN AL PROYECTO:**

 En este proyecto les traigo como hacer un trabajo situándome en el rol de un Data Sciencist :sunglasses: , poniendo  foco central el proceso de ETL, el cual consiste en extraer, transformar y cargar datos. Este tipo de procesos se utiliza con la finalidad de para reunir información de diversos tipos de fuentes.

 Por último, creé una API, a través de FastAPI (un framework de alto rendimiento de Python) la cual me permitirá ingresar y realizar consultas en tiempo real, y también a través de esta interfaz hacer la consulta de  un  modelo capaz de recomendar juegos similares a aquellos que se hayan seleccionado.







**PASOS DEL PROYECTO:**

1- En primer lugar se llevó a cabo el _ETL_, este procedimiento consiste en la extracción, transformación y limpieza de datos, para posteriormente realizar la carga de los datos y continuar con el paso 2.
En este proyecto en particular los archivos a extraer estaban en formato GZIP y Jason además estaban anidados, contenian una gran cantidad de nulos y duplicados.

2- Analisis exploratorios de los datos _(EDA)_, esto realizó con la finalidad de explorar y visualizar los datos para tener una mejor percepción/entendimiento de la información que contiene el dataset, con el cual trabajaremos posteriormente. Este análisis exploratorio se llevó a cabo en el mismo archivo que el ETL.

3- En el archivo _main.py_ se desarrolló una interfaz utilizando la biblioteca FastAPI.


4- _Desarrollo del Modelo de Machine Learning:_ Para el sistema de recomendación se implementó un modelo de Machine Learning utilizando el algoritmo de similitud de cosenos. Este modelo fue preparado luego de haber realizado el ETL, dejando la información lista para consumir. Una vez completa el entrenamiento utilizé la plataforma _RENDER_ para realizar el despliegue de la aplicación.

5- _Despliegue (deploy):_ Nos permite poner en funcionamiento el modelo creado y hacerlo accesible para su uso en la aplicación. Teniendo así la capacidad de realizar recomendaciones basadas en la similitud de cosenos de manera eficiente.




**OBJETIVO**

A continuación se listan las funciones y las consultas que se pueden realizar a través de la API:


* _def userdata(user_id):_

Ésta función recibe como parámetro un id_usuario y devuelve la cantidad de dinero gastado por el mismo


* _def countreviews( YYYY-MM-DD y YYYY-MM-DD : str ):_


Esta función recibe un _STR_ como parámetro y nos devuelve la cantidad de usuarios que realizaron reviews entre ciertas fechas y el porcentaje de recomendación.


* _def genre( género : str ):_

Esta función devolverá el puesto en el cual se encuentra un género.


* _def userforgenre( género : str ):_

Esta funcion devuelve el top 5 de los usuarios que mas jugaron


* _def developer( desarrollador : str ):_


* _def sentiment_analysis( año : int ):_

 Esta función nos devuelve según el año de lanzamiento, un registro de las reseñas de los usuarios.


Y por último, la función  que corresponde al modelo de aprendizaje automático


* _def recomendacion_juego( id de producto ): _

 Si ingresamos  el id de producto, debemos recibir una lista con 5 juegos recomendados similares al ingresado.




A continuación se encuentra:



:small_square: LINK DEPLOYMENT:


:link: https://pi-deploy-on34.onrender.com/docs#/


:small_square: LINK DEL VIDEO EXPLICATIVO:

:link:

_HERRAMIENTAS Y LENGUAJES UTILIZADOS:_
* :snake: Python
* :panda_face: Pandas 	
* :sparkles: Render
* :zap: FastAPI


