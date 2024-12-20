import requests
import json
import random
import os
from sqlalchemy.orm import Session
from app.crud.movie_crud import get_movie_by_title

# Reemplaza con tu clave de API
API_KEY = 'be3cc19439ea0adcbb8fa17e56d8c79b'
movies_data = []

def search_movies_by_title(title, num_movies=1):
    search_url = f'https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&language=en-US&query={title}&page=1'
    response = requests.get(search_url)
    response.raise_for_status()
    data = response.json()
    return data.get('results', [])[:num_movies]


def fetch_genre_id_by_name(genre_name):
    genre_url = f'https://api.themoviedb.org/3/genre/movie/list?api_key={API_KEY}&language=en-US'
    response = requests.get(genre_url)
    response.raise_for_status()
    data = response.json()
    
    # Busca el ID del género por su nombre
    for genre in data['genres']:
        if genre['name'].lower() == genre_name.lower():
            return genre['id']
    return None


def fetch_actor_id_by_name(actor_name):
    actor_url = f'https://api.themoviedb.org/3/search/person?api_key={API_KEY}&language=en-US&query={actor_name}&page=1'
    response = requests.get(actor_url)
    response.raise_for_status()
    data = response.json()

    # Busca el ID del actor por su nombre
    for actor in data['results']:
        if actor['name'].lower() == actor_name.lower():
            return actor['id']
    return None


def fetch_director_id_by_name(director_name):
    director_url = f'https://api.themoviedb.org/3/search/person?api_key={API_KEY}&language=en-US&query={director_name}&page=1'
    response = requests.get(director_url)
    response.raise_for_status()
    data = response.json()

    # Buscar el ID del director por su nombre
    for person in data['results']:
        if person['name'].lower() == director_name.lower():
            return person['id']
    return None

def fetch_all_genres():
    """
    Fetches all genres from the TMDb API.
    
    :return: List of genres as dictionaries with 'id' and 'name' keys.
    """
    genre_url = f'https://api.themoviedb.org/3/genre/movie/list?api_key={API_KEY}&language=en-US'
    try:
        response = requests.get(genre_url)
        response.raise_for_status()
        data = response.json()
        return data['genres']
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error while fetching genres: {e}")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []


def fetch_movies_by_filters_with_names(
    actors_names=None,
    genres_names=None,
    directors_names=None,
    start_date=None,
    end_date=None,
    min_rating=None,
    num_movies=1
):
    """
    Busca películas usando filtros y excluye las películas ya presentes en la base de datos.
    
    :param db: Session - La sesión de la base de datos
    :param actors_names: list of str - Los nombres de los actores
    :param genres_names: list of str - Los nombres de los géneros
    :param directors_names: list of str - Los nombres de los directores
    :param start_date: datetime - Fecha inicial para filtrar
    :param end_date: datetime - Fecha final para filtrar
    :param min_rating: float - Rating mínimo
    :param num_movies: int - Número máximo de películas a devolver
    :return: list of dict - Lista de películas que cumplen los filtros y no están en la base de datos
    """
    # Convert names to IDs
    actor_ids = [fetch_actor_id_by_name(name) for name in actors_names] if actors_names else None
    genre_ids = [fetch_genre_id_by_name(name) for name in genres_names] if genres_names else None
    director_ids = fetch_director_id_by_name(directors_names) if directors_names else None

    # Base URL for filtering movies
    url = "https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=en-US&sort_by=popularity.desc"

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJiZTNjYzE5NDM5ZWEwYWRjYmI4ZmExN2U1NmQ4Yzc5YiIsIm5iZiI6MTczMTY5MDM0MS44MDk1MTMzLCJzdWIiOiI2NzIyMmEwOWQ5YThhNzdiNWRhNDRlZTQiLCJzY29wZXMiOlsiYXBpX3JlYWQiXSwidmVyc2lvbiI6MX0.SCOk2gZvxUpbNlYF0jwIUevnZ0ewv9r391npg4TqK-I"
    }

    # Add filters to URL
    if actor_ids:
        url += f"&with_cast={','.join(map(str, actor_ids))}"
    if genre_ids:
        url += f"&with_genres={','.join(map(str, genre_ids))}"
    if director_ids:
        url += f"&with_crew={','.join(map(str, director_ids))}"  # Crew includes directors
    if start_date:
        url += f"&primary_release_date.gte={start_date}"
    if end_date:
        url += f"&primary_release_date.lte={end_date}"
    if min_rating:
        url += f"&vote_average.gte={min_rating}"

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    data = response.json()

    # Filter out movies already in the database
    movies = []
    for movie in data.get('results', []):
        movies.append(movie)

        # Stop once we reach the requested number of movies
        if len(movies) >= num_movies:
            break

    return movies





def fetch_movie_data(movie_id):
    movie_url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US'
    
    try:
        response = requests.get(movie_url)
        response.raise_for_status()
        data = response.json()

        if 'status_code' in data and data['status_code'] == 34:
            return None
        
        credits_url = f'https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key={API_KEY}&language=en-US'
        credits_response = requests.get(credits_url)
        credits_response.raise_for_status()
        credits_data = credits_response.json()

        movie = {
            "title": data.get('title'),
            "description": data.get('overview'),
            "director": next((member['name'] for member in credits_data.get('crew', []) if member['job'] == 'Director'), None),
            "country": ', '.join(country['iso_3166_1'] for country in data.get('production_countries', [])),
            "release_date": data.get('release_date') if data.get('release_date') else None,
            "rating": (data.get('vote_average') / 2) if data.get('vote_average') else None,
            "rating_count": data.get('vote_count') if data.get('vote_count') else None,
            "likes": random.randint(0, 1000000),
            "genres": [genre['name'] for genre in data.get('genres', [])],
            "cast_members": [actor['name'] for actor in credits_data.get('cast', [])],
            "image": [
                f"https://image.tmdb.org/t/p/w500/{data['poster_path']}" if data.get('poster_path') else None,

                f"https://image.tmdb.org/t/p/w500/{data['backdrop_path']}" if data.get('backdrop_path') else None
            ],
            "trailer": get_movie_video_link(movie_id)
            }

        return movie

    except requests.exceptions.HTTPError as e:
        print(f"Error al obtener la información de la película ID {movie_id}: {e}")
    except Exception as e:
        print(f"Ocurrió un error: {e}")

def get_movie_video_link(movie_id):
    """
    Obtiene el enlace del video para una película específica usando TMDb API.
    
    Args:
        movie_id (int): ID de la película en TMDb.
    
    Returns:
        str: Enlace del video para reproducir en TMDb o un mensaje indicando que no hay videos.
    """
    # Construir la URL para el endpoint de videos
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/videos?api_key={API_KEY}"
    
    try:
        # Realizar la solicitud GET a la API
        response = requests.get(url)
        response.raise_for_status()  # Lanza una excepción si ocurre un error HTTP
        
        # Parsear la respuesta JSON
        data = response.json()
        
        # Verificar si hay videos en los resultados
        if "results" in data and len(data["results"]) > 0:
            # Tomar el primer video disponible
            video_key = data["results"][0]["key"]
            
            # Construir el enlace para reproducir el video
            video_link = f"https://www.themoviedb.org/video/play?key={video_key}"
            return video_link
        else:
            return None
    except requests.exceptions.RequestException as e:
        # Manejar errores de solicitud
        return f"Error al conectar con la API de TMDb: {e}"
    
def load_existing_data(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            return json.load(f)
    return []

def save_data(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

def is_valid_movie(movie):
    return (movie.get('title') is not None and
            movie.get('description') is not None and
            movie.get('director') is not None and
            movie.get('country') is not None and
            movie.get('release_date') is not None and
            movie.get('rating') is not None and
            movie.get('rating_count') is not None and
            all(img is not None for img in movie.get('image', [])) is not None and
            movie.get('trailer') is not None) 


def scrape_movie(title=None):
    """
    Devuelve los datos de una sola película basados en el título o ID.
    
    :param title: str - El título de la película que quieres buscar
    :param movie_id: int - El ID de la película en TMDb
    :return: dict - Los datos de la película, o None si no se encuentra o es inválida
    """
    if title:
        # Busca la película por título
        movies = search_movies_by_title(title, num_movies=1)
        if not movies:
            return None
        movie_id = movies[0]['id']

    # Obtener datos completos de la película por ID
    movie_data = fetch_movie_data(movie_id)
    
    if movie_data and is_valid_movie(movie_data):
        return movie_data
    else:
        return None

def scrape_movies_by_feats(actors_names=None, genres_names=None, directors_names=None, start_date=None, end_date=None, min_rating=None, num_movies=1):
    """
    Devuelve los datos de varias películas basados en los filtros de actores, géneros, directores, rango de fechas y rating.

    :param actors_names: list of str - Los nombres de los actores que quieres filtrar
    :param genres_names: list of str - Los nombres de los géneros que quieres filtrar
    :param directors_names: list of str - Los nombres de los directores que quieres filtrar
    :param start_date: datetime - La fecha de inicio para filtrar las películas
    :param end_date: datetime - La fecha final para filtrar las películas
    :param min_rating: float - El rating mínimo de la película
    :return: list of dict - Lista con los datos de las películas que coinciden con los filtros
    """
    # Obtener las películas que coinciden con los filtros proporcionados
    movies = fetch_movies_by_filters_with_names(
        
        actors_names=actors_names,
        genres_names=genres_names,
        directors_names=directors_names,
        start_date=start_date,
        end_date=end_date,
        min_rating=min_rating,
        num_movies=num_movies
    )
    
    if not movies:
        return None

    # Obtener datos completos para todas las películas encontradas
    movie_data_list = []
    for movie in movies:
        movie_id = movie['id']
        movie_data = fetch_movie_data(movie_id)
        
        if movie_data and is_valid_movie(movie_data):
            movie_data_list.append(movie_data)

    
    return movie_data_list
def get_movies_by_actor(api_key, actor_id):
    url = f"https://api.themoviedb.org/3/discover/movie?api_key={api_key}&with_cast={actor_id}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json().get("results", [])


def get_movies_by_director(api_key, director_id):
    url = f"https://api.themoviedb.org/3/discover/movie?api_key={api_key}&with_crew={director_id}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json().get("results", [])


def get_movies_by_genre(api_key, genre_id):
    url = f"https://api.themoviedb.org/3/discover/movie?api_key={api_key}&with_genres={genre_id}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json().get("results", [])


def get_movies_by_release_date(api_key, start_date, end_date):
    url = f"https://api.themoviedb.org/3/discover/movie?api_key={api_key}&primary_release_date.gte={start_date}&primary_release_date.lte={end_date}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json().get("results", [])


def get_movies_by_rating(api_key, min_rating):
    url = f"https://api.themoviedb.org/3/discover/movie?api_key={api_key}&vote_average.gte={min_rating}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json().get("results", [])

def get_movies(api_key, db, num_movies=10, actor_ids=None, director_id=None, genre_ids=None, start_date=None, end_date=None, min_rating=None):
    movies = []
    seen_movie_ids = set()  # To avoid duplicates

    # Step 1: Fetch movies based on actors
    if actor_ids:
        for actor_id in actor_ids:
            actor_movies = get_movies_by_actor(api_key, actor_id)
            for movie in actor_movies:
                if movie["id"] not in seen_movie_ids:
                    seen_movie_ids.add(movie["id"])
                    movies.append(movie)

    # Step 2: Filter by director if no actors provided or for actor movies
    if director_id:
        director_movies = get_movies_by_director(api_key, director_id)
        movies = [movie for movie in movies if movie["id"] in {m["id"] for m in director_movies}] or director_movies

    # Step 3: Filter by genres
    if genre_ids:
        genre_movies = []
        for genre_id in genre_ids:
            genre_movies.extend(get_movies_by_genre(api_key, genre_id))
        movies = [movie for movie in movies if movie["id"] in {m["id"] for m in genre_movies}] or genre_movies

    # Step 4: Filter by release date range
    if start_date and end_date:
        date_filtered_movies = get_movies_by_release_date(api_key, start_date, end_date)
        movies = [movie for movie in movies if movie["id"] in {m["id"] for m in date_filtered_movies}] or date_filtered_movies

    # Step 5: Filter by rating
    if min_rating:
        rating_filtered_movies = get_movies_by_rating(api_key, min_rating)
        movies = [movie for movie in movies if movie["id"] in {m["id"] for m in rating_filtered_movies}] or rating_filtered_movies

    # Step 6: Remove movies that already exist in the database
    unique_movies = []
    for movie in movies:
        if not get_movie_by_title(db, movie["title"]) and movie not in unique_movies:
            unique_movies.append(movie)
        if len(unique_movies) >= num_movies:
            break

    return unique_movies


    

if __name__ == '__main__':
    api_key = "be3cc19439ea0adcbb8fa17e56d8c79b"
    

    # Define the filtering criteria
    actor_ids = fetch_actor_id_by_name("Tom Cruise")
    director_id = fetch_director_id_by_name("Brian De Palma")
    genre_ids = fetch_genre_id_by_name("Action")
    start_date = "1899-01-01"
    end_date = "2020-12-31"
    min_rating = 6.0

    movies = get_movies(
        api_key,
        num_movies=5,
        actor_ids=actor_ids,
        director_id=director_id,
        genre_ids=genre_ids,
        start_date=start_date,
        end_date=end_date,
        min_rating=min_rating,
    )

    for movie in movies:
        print(f"{movie['title']} (ID: {movie['id']})")
