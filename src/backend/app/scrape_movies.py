import requests
import json
import random
import os

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
            "release_date": data.get('release_date') if data.get('release_date') else None,
            "rating": (data.get('vote_average') / 2) if data.get('vote_average') else None,
            "rating_count": data.get('vote_count') if data.get('vote_count') else None,
            "likes": random.randint(0, 1000000),
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

def scrape_movie(title=None, movie_id=None):
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
    elif not movie_id:
        return None

    # Obtener datos completos de la película por ID
    movie_data = fetch_movie_data(movie_id)
    
    if movie_data and is_valid_movie(movie_data):
        return movie_data
    else:
        return None
