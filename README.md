







# PROYECTO INDIVIDUAL MLOps






## MACHINE LEARNING OPERATIONS





**INTRODUCCIÓN AL PROYECTO:**

 En el presente proyecto les muestro como hacer un trabajo situándome en el rol de un Data Sciencist, poniendo como foco central el proceso de ETL, el cual consiste en extraer, transformar y cargar datos. Este tipo de procesos se utiliza para mezclar información de diversos tipos de fuentes.
 Por último, crearé una API, a través de FastAPI (un framework de alto rendimiento para construir APIS con Python) la cual permitirá realizar diferentes consultas y un modelo capaz de recomendar peliculas similares a aquellas seleccionadas.



**PASOS DEL PROYECTO:**

1- En primer lugar se llevo a cabo el _ETL_, consistiendo en el proceso de extracción de los archivos gzip, la transformación y limpieza de la información para posteriormente la carga de los datos

2- Analisis exploratorios de los datos _(EDA)_, esto se llevó a cabo en el mismo archivo que el ETL, con la finalidad de explorar y visualizar los datos para tener un mejor entendimiento de la información que contiene el dataset, con el cual trabajaremos posteriormente.

3- En el archivo _main.py_ se desarrolló una interfaz utilizando la biblioteca FastAPI


También se puede realizar consultas y recibir respuestas en tiempo real a través de esta interfaz, lo que facilita la   utilización y aplicación práctica del modelo creado.

4- _Desarrollo del Modelo de Machine Learning:_ Para el sistema de recomendación se implementó un modelo de Machine Learning utilizando el algoritmo de similitud de cosenos.

Este modelo ha sido entrenado utilizando los datos preparados y procesados. Una vez completado el entrenamiento se utilizó la plataforma _RENDER_ para realizar el despliegue de la aplicación.

5- _Despliegue (deploy):_ Nos permite poner en funcionamiento el modelo creado y hacerlo accesible para su uso en la aplicación. Teniendo así la capacidad de realizar recomendaciones basadas en la similitud de cosenos de manera eficiente.




**OBJETIVO**

A continuación se listan las funciones y las consultas que se pueden realizar a través de la API:


* def userdata(user_id):

Ésta función recibe como parámetro un id_usuario y devuelve la cantidad de dinero gastado por el mismo


* def countreviews( YYYY-MM-DD y YYYY-MM-DD : str ):


* def genre( género : str ):

* def userforgenre( género : str ):


* def developer( desarrollador : str ):


* def sentiment_analysis( año : int ):







_LINK DEPLOYMENT:_





_LINK DEL VIDEO EXPLICATIVO:_





_LINK AL REPOSITORIO DE ARCHIVOS:_