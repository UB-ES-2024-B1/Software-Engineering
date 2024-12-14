# backend/app/api/routes/movie_routes.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlmodel import Session, select
from app.api.db_utils import get_db  # Import the get_db function for database session management
from app.crud import movie_crud  # Import CRUD functions for movie operations
from app.models import (Movie, MovieIn, MovieOut, MovieUser, User)  # Import movie models for input and output
from typing import List, Optional, Dict, Any
from datetime import datetime
from fastapi.responses import FileResponse
from app.api.routes.user_routes import is_admin_user
from app.api.dependencies import oauth2_scheme
from app.scrape_movies import scrape_movie, scrape_movies_by_feats, fetch_actor_id_by_name, fetch_director_id_by_name, get_actor_role

# Create a router for movie-related endpoints
router = APIRouter()

# Endpoint to create a new movie
@router.post("/", response_model=MovieOut, dependencies=[Depends(is_admin_user)])
def create_movie(movie: MovieIn, db: Session = Depends(get_db)):
    """
    Creates a new movie entry in the database.
    
    :param movie: Movie - Pydantic model containing the movie data to create
    :param db: Session - Database session dependency
    :return: MovieOut - Pydantic model representing the created movie's details
    """
    # Call the CRUD function to create a new movie record
    # Check if the email is already registered
    existing_movie = movie_crud.get_movie_by_title(db, movie_title=movie.title)
    if existing_movie:
        raise HTTPException(status_code=400, detail="Movie title already registered")
    
    movie = movie_crud.create_movie(db, movie)
    # Return the created movie details
    return movie

@router.post("/byName", response_model=MovieOut, dependencies=[Depends(is_admin_user)])
def create_movie_by_name(movie_title: str , db: Session = Depends(get_db)):
    """
    Creates a new movie entry in the database.
    
    :param movie: Movie - Pydantic model containing the movie data to create
    :param db: Session - Database session dependency
    :return: MovieOut - Pydantic model representing the created movie's details
    """
    # Call the CRUD function to create a new movie record
    movie = scrape_movie(title=movie_title)
    movie_data = MovieIn(**movie)
    existing_movie = movie_crud.get_movie_by_title(db, movie_title=movie_data.title)
    if existing_movie:
        raise HTTPException(status_code=400, detail="Movie title already registered")
    
    movie = movie_crud.create_movie(db, movie_data)
    if movie is None:
        raise HTTPException(status_code=404, detail= f"Movie not found")
    # Return the created movie details
    return movie


@router.post("/byFeatures", response_model=List[MovieOut], dependencies=[Depends(is_admin_user)])
def create_movies_by_features(
    genres_names: Optional[List[str]] = None,
    actors_names: Optional[List[str]] = None,
    directors_names: Optional[str] = None,
    min_rating: Optional[float] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    num_movies: int = Query(1, ge=1, le=10),
    db: Session = Depends(get_db)
):
    """
    Creates a list of movies based on given features like genres, actors, directors, rating, and release dates.

    Parameters:
    - genres: List of genre names to filter movies by.
    - actors: List of actor names to filter movies by.
    - directors: List of director names to filter movies by.
    - min_rating: Minimum movie rating.
    - min_release_date: Minimum release date in "YYYY-MM-DD" format.
    - max_release_date: Maximum release date in "YYYY-MM-DD" format.
    - num_movies: Maximum number of movies to fetch.
    - db: Database session.

    Returns:
    - List of newly added movies.
    """
    # Sanitize input lists
    def sanitize_list(input_list):
        if input_list and len(input_list) == 1 and input_list[0].lower() == "string":
            return None
        return input_list

    genres_names = sanitize_list(genres_names)
    actors_names = sanitize_list(actors_names)

    # Validate and convert release dates
    try:
        if start_date:
            try:
                start_date = datetime.strptime(start_date, "%d-%m-%Y").date()
            except ValueError:
                start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
            start_date = start_date.strftime("%Y-%m-%d")
            
        if end_date:
            try:
                end_date = datetime.strptime(end_date, "%d-%m-%Y").date()
            except ValueError:
                end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
            end_date = end_date.strftime("%Y-%m-%d")

    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use 'DD-MM-YYYY' or 'YYYY-MM-DD'.")

    # Fetch movies based on features
    movies = scrape_movies_by_feats(
        db=db,
        genres_names=genres_names,
        actors_names=actors_names,
        directors_names=directors_names,
        start_date=start_date,
        end_date=end_date,
        min_rating=min_rating,
        num_movies=num_movies
    )
    if movies is None:
        raise HTTPException(status_code=400, detail="No movies found based on the given features")

    # Process and add movies to the database
    added_movies = []
    for movie in movies:
        movie_data = MovieIn(**movie)
        added_movie = movie_crud.create_movie(db, movie_data)
        added_movies.append(added_movie)

    if not added_movies:
        raise HTTPException(status_code=404, detail="No new movies were added. All movies already exist.")

    return added_movies

@router.get("/checkActor")
def check_actor(actor_name: str):
    """
    Checks if an actor exists.

    Parameters:
    - actor_name: Name of the actor to check.

    Returns:
    - True if the actor exists, False otherwise.
    """
    actor_id = fetch_actor_id_by_name(actor_name)
    return actor_id is not None

@router.get("/checkDirector")
def check_director(director_name: str):
    """
    Checks if an actor exists.

    Parameters:
    - actor_name: Name of the actor to check.

    Returns:
    - True if the actor exists, False otherwise.
    """
    director_id = fetch_director_id_by_name(director_name)
    return director_id is not None

'''@router.get("/{movie_title}/{actor_name}")
def get_actor_role_and_image(actor_name: str, movie_title: str):
    """
    Gets the roles of an actor.

    Parameters:
    - actor_name: Name of the actor to check.

    Returns:
    - List of roles of the actor.
    """
    role = get_actor_role(actor_name, movie_title)
    return role'''

# Endpoint to retrieve a list of movies
@router.get("/", response_model=List[MovieOut])
def get_movies(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieves a list of movies from the database with optional pagination.
    
    :param skip: int - The number of records to skip (default: 0)
    :param limit: int - The maximum number of records to retrieve (default: 100)
    :param db: Session - Database session dependency
    :return: list[MovieOut] - A list of MovieOut models representing each movie
    """
    # Call the CRUD function to retrieve movies with pagination
    return movie_crud.get_movies(db, skip=skip, limit=limit)

# Endpoint to retrieve a single movie by its ID
@router.get("/{movie_id}", response_model=MovieOut)
def get_movie(movie_id: int, db: Session = Depends(get_db)):
    """
    Retrieves a single movie by its ID.
    
    :param movie_id: int - The ID of the movie to retrieve
    :param db: Session - Database session dependency
    :return: MovieOut - The retrieved movie's details
    :raises HTTPException: 404 if the movie is not found
    """
    # Call the CRUD function to get a movie by ID
    movie = movie_crud.get_movie(db=db, movie_id=movie_id)
    # If the movie does not exist, raise a 404 error
    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie

# Endpoint to retrieve a single movie by its title
@router.get("/title/{movie_title}", response_model=MovieOut)
def get_movie_by_title(movie_title: str, db: Session = Depends(get_db)):
    """
    Retrieves a single movie by its title.
    
    :param movie_title: str - The title of the movie to retrieve
    :param db: Session - Database session dependency
    :return: MovieOut - The retrieved movie's details
    :raises HTTPException: 404 if the movie is not found
    """
    movie = movie_crud.get_movie_by_title(db=db, movie_title=movie_title)
    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie
    # return FileResponse(movie.image)
# Endpoint to retrieve movies by release year
@router.get("/release/{movie_year}", response_model=List[MovieOut])
def get_movies_by_release(movie_year: int, db: Session = Depends(get_db)):
    """
    Retrieves a list of movies by release year.
    
    :param movie_release: int - The release year of the movies to retrive
    :param db: Session - Database session dependency
    return: List[MovieOut] - A list of movies with release year
    """
    movie = movie_crud.get_movie_by_year(db=db, movie_year=movie_year)
    return movie

# Endpoint to retrieve movies with one genre
@router.get("/genre/{movie_genre}", response_model=List[MovieOut])
def get_movies_by_genre(movie_genre: str, db: Session = Depends(get_db)):
    """
    Retrieves a list of movies taht have one specific genre
    
    :param movie_genre: str - Genre that we want in the movies to retrive
    :param db: Session - Database session dependency
    return: List[MovieOut] - A list of movies with release year
    """
    if not movie_crud.is_valid_genre(db, movie_genre):
        raise HTTPException(status_code=404, detail="Genre not found")

    movie = movie_crud.get_movie_by_genre(db=db, movie_genre=movie_genre)
    return movie

# Endpoint to retrieve movies with multiple genre
@router.get("/genre/list/{movie_genre_list}", response_model=List[MovieOut])
def get_movies_by_list_genre(movie_genre_list: str, db: Session = Depends(get_db)):
    """
    Retrieves a list of movies taht have more than one specific genre
    
    :param movie_genre: str - Genres that we want in the movies to retrive (split by ',')   
                       Example: Action,Adventure,Science Fiction \n
    :param db: Session - Database session dependency \n
    return: List[MovieOut] - A list of movies with release year
    """
    genre_list = [genre.strip() for genre in movie_genre_list.split(",") if genre.strip()]

    for genre in genre_list:
        if not movie_crud.is_valid_genre(db, genre):
            raise HTTPException(status_code=404, detail="Genre not found")

    movie = movie_crud.get_movie_by_genre_list(db=db, genre_list=genre_list)
    return movie

# Endpoint to retrieve movies by a string of movie name given
@router.get("/search/name/{input}", response_model=List[MovieOut])
def get_movies_by_search(input: str, db: Session = Depends(get_db)):
    """
    Retrieves a list of movies that includes the input string in the movie name
    
    :param movie_name_string: str - input that users introduce to find out a list of movies with the same pattern 
                       Example: barb, panda, etc \n
    :param db: Session - Database session dependency \n
    return: List[MovieOut] - A list of movies with that pattern included
    """
    # Use the function defined above to search by name pattern
    return movie_crud.get_movies_by_input(db=db, input=input)

# Endpoint to retrieve movies sorted by release date
@router.get("/sorted/release_date", response_model=List[MovieOut])
def get_movies_sorted_by_release_date(db: Session = Depends(get_db)):
    """
    Retrieves a list of movies sorted by release date.
    
    :param db: Session - Database session dependency
    :return: List[MovieOut] - A sorted list of movies by release date
    """
    movies = movie_crud.get_movies_sorted_by_release_date(db=db)
    return movies

# Endpoint to retrieve movies sorted by rating
@router.get("/sorted/rating", response_model=List[MovieOut])
def get_movies_sorted_by_rating(db: Session = Depends(get_db)):
    """
    Retrieves a list of movies sorted by rating.
    
    :param db: Session - Database session dependency
    :return: List[MovieOut] - A sorted list of movies by rating
    """
    movies = movie_crud.get_movies_sorted_by_rating(db=db)
    return movies

# Endpoint to retrieve movies sorted by likes
@router.get("/sorted/likes", response_model=List[MovieOut])
def get_movies_sorted_by_likes(db: Session = Depends(get_db)):
    """
    Retrieves a list of movies sorted by likes.
    
    :param db: Session - Database session dependency
    :return: List[MovieOut] - A sorted list of movies by likes
    """
    movies = movie_crud.get_movies_sorted_by_likes(db=db)
    return movies

@router.get("/sorted/related_movies/{movie_title}", response_model=List[MovieOut])
def get_movies_sorted_by_related_movies(movie_title: str, db: Session = Depends(get_db)):
    """
    Retrieves a list of movies sorted by release date.
    
    :param db: Session - Database session dependency
    :return: List[MovieOut] - A sorted list of movies by release date
    """
    movies = movie_crud.get_movies_sorted_by_related(db=db, target_movie_title=movie_title)
    return movies

'''
# Endpoint to update an existing movie by its ID
@router.put("/{movie_id}", response_model=MovieOut)
def update_movie(movie_id: int, movie_data: MovieIn, db: Session = Depends(get_db)):
    """
    Updates an existing movie's details by its ID.
    
    :param movie_id: int - The ID of the movie to update
    :param movie_data: MovieUpdate - The data to update the movie with
    :param db: Session - Database session dependency
    :return: MovieOut - The updated movie's details
    :raises HTTPException: 404 if the movie is not found
    """
    # Call the CRUD function to update the movie
    updated_movie = movie_crud.update_movie(db, movie_id, movie_data)
    # If the movie does not exist, raise a 404 error
    if updated_movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    return updated_movie
'''

# Endpoint to update an existing movie by its title
@router.put("/{movie_title}", response_model=MovieOut)
def update_movie(movie_title: str, movie_data: MovieIn, db: Session = Depends(get_db)):
    """
    Updates an existing movie's details by its ID.
    
    :param movie_id: int - The ID of the movie to update
    :param movie_data: MovieUpdate - The data to update the movie with
    :param db: Session - Database session dependency
    :return: MovieOut - The updated movie's details
    :raises HTTPException: 404 if the movie is not found
    """
    # Call the CRUD function to update the movie
    updated_movie = movie_crud.update_movie(db, movie_title, movie_data)
    # If the movie does not exist, raise a 404 error
    if updated_movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    return updated_movie

# Endpoint to update only the rating of an existing movie by its title
@router.post("/rate/{movie_id}/{user_id}/{rating}")
def rate_movie_endpoint(movie_id: int, user_id: int, rating: float, db: Session = Depends(get_db)):
    # Check if the movie exists
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    # Check if the user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # If the movie exists, proceed with the rating logic
    return movie_crud.rate_movie(db, user_id, movie_id, rating)

# Endpoint to increment the likes of a movie by its title
@router.post("/like/{movie_id}/{user_id}")
def like_movie_endpoint(movie_id: int, user_id: int, db: Session = Depends(get_db)):
    # Check if the movie exists
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    # Check if the user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # If the movie exists, proceed with the like logic
    return movie_crud.like_movie(db, user_id, movie_id)

# Endpoint to add movie to wish list
@router.post("/wish/{movie_id}/{user_id}")
def wish_movie_endpoint(movie_id: int, user_id: int, db: Session = Depends(get_db)):
    # Check if the movie exists
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    # Check if the user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # If the movie exists, proceed with the wish logic
    return movie_crud.wish_movie(db, user_id, movie_id)

# Endpoint to remove the rating of an existing movie by a user
@router.post("/unrate/{movie_id}/{user_id}")
def unrate_movie_endpoint(movie_id: int, user_id: int, db: Session = Depends(get_db)):
    # Check if the movie exists
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    # Check if the user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # If the movie exists, proceed with the rating logic
    return movie_crud.remove_rate_movie(db, user_id, movie_id)

# Endpoint to increment the likes of a movie by its title
@router.post("/dislike/{movie_id}/{user_id}")
def dislike_movie_endpoint(movie_id: int, user_id: int, db: Session = Depends(get_db)):
    # Check if the movie exists
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    # Check if the user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # If the movie exists, proceed with the like logic
    return movie_crud.remove_like_movie(db, user_id, movie_id)

# Endpoint to remove wish of a movie
@router.post("/nowish/{movie_id}/{user_id}")
def nowish_movie_endpoint(movie_id: int, user_id: int, db: Session = Depends(get_db)):
    # Check if the movie exists
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    # Check if the user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # If the movie exists, proceed with the like logic
    return movie_crud.remove_wish_movie(db, user_id, movie_id)

# Endpoint to get the list of a user of ratings
@router.get("/liked_rated_and_wished_list/{user_id}")
def get_liked_and_rated_movies(user_id: int, db: Session = Depends(get_db)):
    # Format the result to return both liked and rated movies
    liked_movie_titles = movie_crud.get_user_liked_movies(db, user_id=user_id)
    rated_movie_details = movie_crud.get_user_rated_movies(db, user_id)
    wished_movie_details = movie_crud.get_user_wished_movies(db, user_id)

    return {"liked_movies": liked_movie_titles, "rated_movies": rated_movie_details, "wished_movies": wished_movie_details}

# Endpoint to get the list of a user of ratings
@router.get("/rated_list/{user_id}")
def get_rated_movies(user_id: int, db: Session = Depends(get_db)):
    # Query to get all movies rated by the user (excluding None values for rating)
    rated_movie_details = movie_crud.get_user_rated_movies(db, user_id=user_id)

    return rated_movie_details

# Endpoint to get the list of a user of ratings
@router.get("/liked_list/{user_id}")
def get_liked_movies(user_id: int, db: Session = Depends(get_db)):
    return movie_crud.get_user_liked_movies(db, user_id)

# Endpoint to get the list of a user of ratings
@router.get("/wished_list/{user_id}")
def get_wished_movies(user_id: int, db: Session = Depends(get_db)):
    return movie_crud.get_user_wished_movies(db, user_id)

# Endpoint to get the list of all ratings
@router.get("/rated/all_ratings", response_model=List[Dict[str, Any]])
def get_all_rated_movies(
    skip: int = 0,  # Default value for skip
    limit: int = 100,  # Default value for limit
    db: Session = Depends(get_db)
):
    return movie_crud.get_all_ratings(db, skip, limit)



'''# Endpoint to update only the rating of an existing movie by its title
@router.put("/{movie_title}/rating", response_model=MovieOut)
def update_movie_rating_by_title(movie_title: str, rating_data: MovieUpdateRating, db: Session = Depends(get_db)):
    """
    Updates only the rating of an existing movie by its title.
    
    :param movie_title: str - The title of the movie to update
    :param rating_data: MovieUpdateRating - The new rating data for the movie
    :param db: Session - Database session dependency
    :return: MovieOut - The updated movie's details
    :raises HTTPException: 404 if the movie is not found
    """
    # Call the CRUD function to update the movie's rating by title
    updated_movie = movie_crud.update_movie_rating_by_title(db, movie_title, rating_data.rating)
    
    # If the movie does not exist, raise a 404 error
    if updated_movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    return updated_movie

# Endpoint to increment the likes of a movie by its title
@router.put("/{movie_title}/like", response_model=MovieOut)
def add_movie_like(movie_title: str, db: Session = Depends(get_db)):
    """
    Adds one like to the movie's likes count.
    
    :param movie_title: str - The title of the movie to like
    :param db: Session - Database session dependency
    :return: MovieOut - The updated movie details with the incremented like count
    :raises HTTPException: 404 if the movie is not found
    """
    # Call the CRUD function to add a like to the movie
    updated_movie = movie_crud.add_movie_like(db, movie_title)
    
    # If the movie does not exist, raise a 404 error
    if updated_movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    return updated_movie'''

# Endpoint to delete an existing movie by its ID
@router.delete("/id/{movie_id}", response_model=dict)
def delete_movie(movie_id: int, db: Session = Depends(get_db)):
    """
    Deletes a movie from the database by its ID.
    
    :param movie_id: int - The ID of the movie to delete
    :param db: Session - Database session dependency
    :return: dict - A success message if deletion is successful
    :raises HTTPException: 404 if the movie is not found
    """
    # Call the CRUD function to delete the movie
    success = movie_crud.delete_movie(db, movie_id)
    # If the movie does not exist, raise a 404 error
    if not success:
        raise HTTPException(status_code=404, detail="Movie not found")
    return {"message": "Movie deleted successfully"}

# Endpoint to delete an existing movie by its title
@router.delete("/title/{movie_title}", response_model=dict)
def delete_movie_by_title(movie_title: str, db: Session = Depends(get_db)):
    """
    Deletes a movie from the database by its title.
    
    :param movie_title: str - The title of the movie to delete
    :param db: Session - Database session dependency
    :return: dict - A success message if deletion is successful
    :raises HTTPException: 404 if the movie is not found
    """
    # Call the CRUD function to delete the movie by title
    success = movie_crud.delete_movie_by_title(db, movie_title)
    # If the movie does not exist, raise a 404 error
    if not success:
        raise HTTPException(status_code=404, detail="Movie not found")
    return {"message": "Movie deleted successfully"}

