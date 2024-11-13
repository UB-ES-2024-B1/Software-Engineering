import requests
import json
import random
import os

# Reemplaza con tu clave de API
API_KEY = 'be3cc19439ea0adcbb8fa17e56d8c79b'
movies_data = []

def fetch_movie_data(movie_id):
    # URL de la película
    movie_url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US'
    
    try:
        response = requests.get(movie_url)
        response.raise_for_status()  # Lanza un error si la solicitud no fue exitosa
        data = response.json()

        # Comprobación de si hay datos válidos
        if 'status_code' in data and data['status_code'] == 34:
            return None  # Película no encontrada
        
        # URL para obtener los créditos
        credits_url = f'https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key={API_KEY}&language=en-US'
        credits_response = requests.get(credits_url)
        credits_response.raise_for_status()  # Lanza un error si la solicitud no fue exitosa
        credits_data = credits_response.json()

        print("helllo", data)
        # Estructurando los datos
        movie = {
            "title": data.get('title'),
            "description": data.get('overview'),
            "director": next((member['name'] for member in credits_data.get('crew', []) if member['job'] == 'Director'), None),
            "country": ', '.join(country['iso_3166_1'] for country in data.get('production_countries', [])),
            "release_date": data.get('release_date').replace("-", ", ") if data.get('release_date') else None,
            "rating": (data.get('vote_average') / 2) if data.get('vote_average') else None,
            "rating_count": data.get('vote_count') if data.get('vote_count') else None,
            "likes": 0,  # Puedes agregar lógica para obtener "likes"
            "genres": [genre['name'] for genre in data.get('genres', [])],
            "cast_members": [actor['name'] for actor in credits_data.get('cast', [])],
            "image": [
                f"https://image.tmdb.org/t/p/w500/{data['poster_path']}" if data.get('poster_path') else None,
                f"https://image.tmdb.org/t/p/w500/{data['backdrop_path']}" if data.get('backdrop_path') else None
            ],
            "trailer": ""
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
    # Verifica que todos los campos necesarios tengan valores válidos
    return (movie.get('title') is not None and
            movie.get('description') is not None and
            movie.get('director') is not None and
            movie.get('country') is not None and
            movie.get('release_date') is not None and
            movie.get('rating') is not None and
            movie.get('rating_count') is not None and
            all(img is not None for img in movie.get('image', [])) is not None and
            movie.get('trailer') is not None) 

def scrape_movies(num_movies=100):
    filename = 'src/backend/data_movies.json'
    existing_data = load_existing_data(filename)
    
    # Usar un conjunto para evitar duplicados
    existing_ids = {movie['title']: movie for movie in existing_data}

    while len(existing_data) < num_movies:
        movie_id = random.randint(1, 100000)  # Rango de IDs puede ser ajustado
        movie_data = fetch_movie_data(movie_id)

        # Validar que la película tenga todos los campos requeridos
        if movie_data and is_valid_movie(movie_data) and movie_data['title'] not in existing_ids:
            existing_data.append(movie_data)
            existing_ids[movie_data['title']] = movie_data  # Añadir al conjunto de IDs existentes
            print(f"Agregada: {movie_data['title']}")

    save_data(filename, existing_data)

if __name__ == '__main__':
    scrape_movies()
