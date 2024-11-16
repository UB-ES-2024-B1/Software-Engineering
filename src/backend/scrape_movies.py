import requests
import json
import random
import os
from typing import List, Optional

# Reemplaza con tu clave de API
API_KEY = 'be3cc19439ea0adcbb8fa17e56d8c79b'
movies_data = []

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

def fetch_movies_by_genre(genre_id, num_movies=10):
    genre_url = f'https://api.themoviedb.org/3/discover/movie?api_key={API_KEY}&language=en-US&sort_by=popularity.desc&with_genres={genre_id}'
    response = requests.get(genre_url)
    response.raise_for_status()
    data = response.json()
    return data.get('results', [])[:num_movies]

def search_movies_by_title(title, num_movies=10):
    search_url = f'https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&language=en-US&query={title}&page=1'
    response = requests.get(search_url)
    response.raise_for_status()
    data = response.json()
    return data.get('results', [])[:num_movies]

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
            "release_date": data.get('release_date').replace("-", ", ") if data.get('release_date') else None,
            "rating": (data.get('vote_average') / 2) if data.get('vote_average') else None,
            "rating_count": data.get('vote_count') if data.get('vote_count') else None,
            "likes": 270001,
            "genres": [genre['name'] for genre in data.get('genres', [])],
            "cast_members": [actor['name'] for actor in credits_data.get('cast', [])],
            "image": [
                f"https://image.tmdb.org/t/p/w500/{data['poster_path']}" if data.get('poster_path') else None,
                f"https://image.tmdb.org/t/p/original/{data['backdrop_path']}" if data.get('backdrop_path') else None
            ]
        }

        return movie

    except requests.exceptions.HTTPError as e:
        print(f"Error al obtener la información de la película ID {movie_id}: {e}")
    except Exception as e:
        print(f"Ocurrió un error: {e}")

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
            all(img is not None for img in movie.get('image', [])))

def scrape_movies(num_movies=100, genre_name=None, title=None):
    filename = 'src/backend/data_movies.json'
    existing_data = load_existing_data(filename)
    existing_ids = {movie['title']: movie for movie in existing_data}

    if genre_name:
        genre_id = fetch_genre_id_by_name(genre_name)
        if genre_id:
            movies = fetch_movies_by_genre(genre_id, num_movies)
        else:
            print(f"Género '{genre_name}' no encontrado.")
            return
    elif title:
        movies = search_movies_by_title(title, num_movies)
    else:
        movies = []

    for movie in movies:
        movie_data = fetch_movie_data(movie['id'])

        if movie_data and is_valid_movie(movie_data) and movie_data['title'] not in existing_ids:
            existing_data.append(movie_data)
            existing_ids[movie_data['title']] = movie_data
            print(f"Agregada: {movie_data['title']}")

    save_data(filename, existing_data)



def fetch_movies_by_features(
    genres: Optional[List[str]] = None,
    actors: Optional[List[str]] = None,
    directors: Optional[List[str]] = None,
    min_rating: Optional[float] = None,
    min_release_date: Optional[str] = None,
    max_release_date: Optional[str] = None,
    num_movies: int = 10
):
    """
    Fetches movies by the given features.
    
    :param genres: List of genres to filter by
    :param actors: List of actors to filter by
    :param directors: List of directors to filter by
    :param min_rating: Minimum rating for the movies
    :param min_release_date: Minimum release date in 'YYYY-MM-DD' format
    :param max_release_date: Maximum release date in 'YYYY-MM-DD' format
    :param num_movies: Number of movies to return
    :return: List of movie dictionaries
    """
    # Start constructing the query parameters for the API
    query_params = {
        'language': 'en-US',
        'sort_by': 'popularity.desc',
        'page': 1
    }

    if genres:
        genre_ids = [fetch_genre_id_by_name(genre) for genre in genres if fetch_genre_id_by_name(genre)]
        if genre_ids:
            query_params['with_genres'] = ','.join(map(str, genre_ids))

    if min_rating is not None:
        query_params['vote_average.gte'] = min_rating

    if min_release_date:
        query_params['primary_release_date.gte'] = min_release_date

    if max_release_date:
        query_params['primary_release_date.lte'] = max_release_date

    # Fetch movies using the TMDb API by the constructed parameters
    url = f'https://api.themoviedb.org/3/discover/movie?api_key={API_KEY}'
    response = requests.get(url, params=query_params)
    response.raise_for_status()
    data = response.json()

    # Filter movies based on actors and directors
    filtered_movies = []
    for movie in data.get('results', []):
        movie_data = fetch_movie_data(movie['id'])
        
        # Filter by actors
        if actors:
            cast_members = movie_data.get('cast_members', [])
            if not any(actor in cast_members for actor in actors):
                continue

        # Filter by directors
        if directors:
            director = movie_data.get('director', '')
            if not any(director == director_name for director_name in directors):
                continue

        # Add movie if it passes all filters
        if movie_data:
            filtered_movies.append(movie_data)
        
        if len(filtered_movies) >= num_movies:
            break

    return filtered_movies

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
def fetch_movies_by_filters_with_names(
    actors_names=None,
    genres_names=None,
    directors_names=None,
    start_date=None,
    end_date=None,
    min_rating=None,
    num_movies=10
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
    director_ids = [fetch_director_id_by_name(name) for name in directors_names] if directors_names else None

    # Base URL for filtering movies
    url = "https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=en-US&page=1&sort_by=popularity.desc"

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


    return data.get('results', [])[:num_movies]

if __name__ == '__main__':
    # Puedes llamar a scrape_movies con un género o título específico 
    print(fetch_movies_by_filters_with_names(actors_names=["Tom Cruise"],genres_names=["Action"], end_date="2022-11-10", num_movies=1))