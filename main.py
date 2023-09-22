import pandas as pd 
from fastapi import FastAPI


app= FastAPI()

df_games_csv= pd.read_csv("./Games_csv")
df_reviews_final_csv= pd.read_csv("./Reviews_csv")
df_items_final_csv= pd.read_csv("./Reviews_csv")

#1
@app.get('/user_data/{user_id}')
async def userdata(user_id):
    # Filtra las revisiones del usuario especifico
    user_reviews = df_reviews_final_csv[df_reviews_final_csv["user_id.1"] == user_id]   
    # Filtra los juegos jugados por el usuario
    game_id = user_reviews["item_id"].unique()
    user_steam_games = df_games_csv[df_games_csv["id"].astype(int).isin(game_id)]
    # Calcula la cantidad de dinero gastado por el usuario
    user_steam_games.loc[:, "price"] = user_steam_games["price"].replace("$", " ").astype(float)
    dinero_gastado = user_steam_games["price"].sum()

    # Calcula el porcentaje de recomendación promedio de los juegos jugados por el usuario
    user_reviews.loc[:, "recommend"] = user_reviews["recommend"].astype(bool)
    porc_recomendacion = user_reviews["recommend"].mean() * 100

    # Calcula la cantidad de items que posee un usuario
    num_items = len(game_id)

    # Crear un diccionario con los resultados
    user_data = {
        "dinero_gastado": dinero_gastado,
        "porc_recomendacion": porc_recomendacion,
        "num_items": num_items
    }

    return user_data


#2
@app.get("/reviews_count/{start_date}")
async def count_reviews(start_date: str, end_date: str):
    # Supongamos que los datos están almacenados en un DataFrame llamado 'reviews'
    # con columnas 'date' (para la fecha) y 'recommend' (para la recomendación)

    # Filtrar las reviews entre las fechas dadas
    reviews_between_dates = df_reviews_final_csv[(df_reviews_final_csv['posted'] >= start_date) & (df_reviews_final_csv['posted'] <= end_date)]

    # Calcular la cantidad de usuarios que realizaron reviews entre las fechas dadas
    num_users = len(reviews_between_dates)

    # Calcular el porcentaje de recomendación
    if num_users > 0:
        percentage_recommendation = (reviews_between_dates['recommend'].sum() / num_users) * 100
    else:
        percentage_recommendation = 0

    return {
        "Número de usuarios": num_users, 
        "Porcentaje de recomendación": percentage_recommendation
        }


#3
@app.get("/genre/{género}")
async def genre(género):
    df_genre = df_games_csv[df_games_csv['genres'] == género]
    
    if df_genre.empty:
        return None  # Devuelve None si no se encontraron coincidencias
    
    df_merged = df_genre.merge(df_items_final_csv, left_index=True, right_index=True)
    df_sorted = df_merged.sort_values(by='playtime_forever', ascending=False)
    
    puesto = df_sorted.index.tolist().index(0) + 1
    
    return puesto


#4
@app.get("/userforgenre/{género}")
async def userforgenre(género: str):
    # Filtra las reseñas por genre
    reviews_por_género = df_games_csv[df_games_csv['genres'] == género]
    # Se agrupa por los usuarios y las horas jugadas
    horas_por_usuario = reviews_por_género.groupby('user_id.1')['horas_jugadas'].sum().reset_index()
    # Obtiene los 5 usuarios con más horas de juego
    top_usuarios = horas_por_usuario.nlargest(5, 'horas_jugadas')
    # Obtiene la URL y user_id de los 5 usuarios
    top_usuarios_info = top_usuarios.merge(df_reviews_final_csv[['user_id.1', 'user_url']], on='user_id.1')

    return top_usuarios_info[['user_url', 'user_id.1']]


#5
@app.get("/developer/{desarrollador}")
async def developer(desarrollador, str):
    # Filtrar el DataFrame por el desarrollador específico
    developer_df = df_games_csv[df_games_csv['developer'] == desarrollador].copy()  # Agregamos .copy() para evitar el error

    # Asegurarse de que release_date sea de tipo datetime
    developer_df['release_date'] = pd.to_datetime(developer_df['release_date'])
    
    # Crea una nueva columna release_year que contiene el año de lanzamiento de cada juego
    developer_df['release_year'] = developer_df['release_date'].dt.to_period('Y')

    # Agrupar por año y contar la cantidad de juegos y el porcentaje de contenido Free
    grouped = developer_df.groupby(developer_df['release_year'].dt.year)['developer'].count()
    free_percentage = developer_df.groupby(developer_df['release_year'].dt.year)['price'].apply(lambda x: (x == 0).mean() * 100)

    # Combinar la información en un DataFrame
    developer_info_df = pd.DataFrame({'Año': grouped, 'Porcentaje de Contenido Free': free_percentage})

    return developer_info_df



#6
@app.get("/sentiment_analysis/{año}")
async def sentiment_analysis(año: int):
    # Filtramos los DataFrames por año
    juegos_año = df_games_csv[df_games_csv["release_date"] == año]
    reviews_año = df_reviews_final_csv[df_reviews_final_csv["sentiment_analysis"] == año]

    # Obtenemos recuentos de sentimientos y los sumamos
    sentimientos_juegos = juegos_año["release_date"].value_counts().to_dict()
    sentimientos_finales = reviews_año["sentiment_analysis"].value_counts().to_dict()

    conteo_sentimientos = {"Negative": 0, "Neutral": 0, "Positive": 0}

    for sentimiento, count in sentimientos_juegos.items():
        if sentimiento in conteo_sentimientos:
            conteo_sentimientos[sentimiento] += count

    for sentimiento, count in sentimientos_finales.items():
        if sentimiento in conteo_sentimientos:
            conteo_sentimientos[sentimiento] += count

    return conteo_sentimientos


# Modelo de recomendación
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

@app.get("/recomendacion_juego/{product_id}")
async def recomendacion_juego(product_id:int):
    try: 
        # Obtiene el juego de referencia
        target_game = df_games_csv[df_games_csv["id"] == product_id]
        if target_game.empty:
            return {"message": "No se encontró el juego de referencia"}
        # Combina las etiquetas tags y genres en una sola cadena de texto
        target_game_tags_and_genres = " ".join(target_game["tags"].fillna(" ").astype(str) + " " + target_game["genres"].fillna(" ").astype(str))

        # Crea un vectorizador TF-IDF
        tfidf_vectorizer = TfidfVectorizer()

        # Configura el tamaño del lote para la lectura del juego
        chunk_size = 100  # Tamaño del lote
        similarity_scores = None

        # Procesa los juegos por lotes aplicando chunks
        for chunk in pd.read_csv("./Games_csv", chunksize=chunk_size):
            # Combina las etiquetas tags y genres en una sola cadena de texto
            chunk_tags_and_genres = " ".join(chunk["tags"].fillna(" ").astype(str) + " " + chunk["genres"].fillna(" ").astype(str))
            
            # Aplica el vectorizador TF-IDF al lote actual de juegos y al juego de referencia
            tfidf_matrix = tfidf_vectorizer.fit_transform([target_game_tags_and_genres, chunk_tags_and_genres])
            
            # Calcula la similitud entre el juego de referencia y los juegos del lote actual
            similarity_scores_batch = cosine_similarity(tfidf_matrix)

            if similarity_scores is None:
                similarity_scores = similarity_scores_batch
            else:
                similarity_scores = np.concatenate((similarity_scores, similarity_scores_batch), axis=1)
                
        if similarity_scores is not None:
            # Obtiene los índices de los juegos similares 
            similar_games_indices = similarity_scores[0].argsort()[::-1]
            # Recomienda los juegos más similares 
            num_recomendation = 5
            recommended_games = df_games_csv.iloc[similar_games_indices[1:num_recomendation + 1]]
            # Devuelve la lista con los juegos recomendados 
            return recommended_games[["app_name", "id"]].to_dict(orient="records")

        return {"message": "No se encontraron juegos similares"}
    except Exception as e:
        return {"Message": f"Error: {str(e)}"}
