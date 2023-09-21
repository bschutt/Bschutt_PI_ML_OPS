import pandas as pd 
from fastapi import FastAPI


app= FastAPI()

df_games_csv= pd.read_csv("./Games_csv")
df_reviews_final_csv= pd.read_csv("./Reviews_csv")

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

    return num_users, percentage_recommendation

#6
@app.get("/entiment_analysis/{año}")
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

@app.get("/recomendacion_juego/{product_id}")
async def recomendacion_juego(product_id:int):
    try: 
        # Obtiene el juego de referencia
        target_game= df_games_csv[df_games_csv["id"]== product_id]
        if target_game.empty:
            return{"message: No se encontró el juego de referencia"}
        # Combina las etiquetas tags y genres en una sola cadena de texto
        target_game_tags_and_genres= " " .join(target_game["tags"].fillna(" ").astype(str) + " " + target_game["genres"].fillna(" ").astype(str))
        
        #Crea un vectorizador TF-IDF
        tfidf_vectorizer =TfidfVectorizer()
        
        # Configura el tamaño del lote para la lectura del juego
        chunk_size = 100 # Tamaño del lote
        similarity_scores= None
        
        # Procesa los juegos por lotes aplicando chunks
        for chunk in pd.read_csv("./Games_csv", chunksize=chunk_size):
            # Combina las etiquetas tags y genres en una sola cadena de texto
            chunk_tags_and_genres= " " .join(chunk["tags"].fillna(" ").astype(str) + " " + chunk["genres"].fillna(" ").astype(str)) 
            # Aplica el vectorizador TF-IDF al lote actual de juegos y al juego de referencia
            tfidf_matrix = tfidf_vectorizer.fit_transform([target_game_tags_and_genres, chunk_tags_and_genres])
            # Calcula la similitud entre el juego de referencia y los juegos del lote actual
            if similarity_scores is None:
                similarity_scores = cosine_similarity(tfidf_matrix)
            else:
                similarity_scores = cosine_similarity(tfidf_matrix, X=similarity_scores)
        if similarity_scores is not None:
            # Obtiene los índices de los juegos similares 
            similar_games_indices = similarity_scores[0].argsort()[::-1]
            # Recomienda los juegos más similares 
            num_recomendation = 5
            recomended_games = df_games_csv[similar_games_indices[1:num_recomendation + 1]]
            # Devueve la lista con los juegos recomendados 
            return recomended_games[["app_name", "tags","genres"]].to_dict(orient="records" )
        
        return {"message":" No se encontraron juegos similares"}
    except Exception as e:
        return {"Message": f"Error: {str(e)}"}   