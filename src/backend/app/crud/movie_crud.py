# backend/app/crud/movie_crud.py
from sqlmodel import Session, select
from app.models import (Movie, MovieIn, MovieOut, MovieUpdate, Genre, CastMember, MovieGenre, MovieCast, MovieUser) 
from typing import List
from fastapi import File, UploadFile, HTTPException
from sqlalchemy.sql import func, case, extract
from app.api.routes.comments_routes import create_thread, delete_thread



# Function to create a new movie
def create_movie(db: Session, movie: MovieIn, file: UploadFile = File(None)) -> MovieOut:
    # Check if a movie with the same title already exists
    # Create new movie instance
    db_movie = Movie(
        title=movie.title,
        description=movie.description,
        director=movie.director,
        country=movie.country,
        release_date=movie.release_date,
        rating=movie.rating,
        rating_count=movie.rating_count,
        likes=movie.likes,
        image=movie.image,
        trailer=movie.trailer
    )

    # Handle genres
    for genre_name in movie.genres or []:  # Use the genres from the input
        genre = db.execute(select(Genre).where(Genre.type == genre_name)).scalars().first()
        if genre is None:
            genre = Genre(type=genre_name)  # Ensure genre type is not None
            db.add(genre)  # Add new genre to the session
        db_movie.genres.append(genre)  # Associate genre with the movie

    # Handle cast members
    for cast_name in movie.cast_members or []:
        cast_member = db.execute(select(CastMember).where(CastMember.name == cast_name)).scalars().first()
        if cast_member is None:
            cast_member = CastMember(name=cast_name)  # Ensure cast name is not None
            db.add(cast_member)  # Add new cast member to the session
        db_movie.cast_members.append(cast_member)  # Associate cast member with the movie


    # Add movie to the session and commit
    db.add(db_movie)
    db.commit()  # Commit the transaction
    db.refresh(db_movie)  # Refresh to get the updated data

    # Create a thread for the movie
    create_thread(db, db_movie.id)
    return MovieOut.model_validate(db_movie)  # Use model_validate instead of from_orm


# Function to get a list of movies with pagination
def get_movies(db: Session, skip: int = 0, limit: int = 100) -> List[MovieOut]:
    statement = select(Movie).offset(skip).limit(limit)
    results = db.execute(statement).scalars().all()
    return [MovieOut.model_validate(movie) for movie in results]  # Use model_validate

# Function to get a movie by ID
def get_movie(db: Session, movie_id: int) -> MovieOut:
    statement = select(Movie).where(Movie.id == movie_id)
    movie = db.execute(statement).scalars().first()
    if movie:
        return MovieOut.model_validate(movie)  # Use model_validate
    return None  # If movie not found

# CRUDs to get different types of list of movies
def get_movie_by_title(db: Session, movie_title: str) -> MovieOut:
    statement = select(Movie).where(Movie.title == movie_title)
    return db.execute(statement).scalars().first()

def get_movies_sorted_by_release_date(db: Session) -> List[MovieOut]:
    statement = select(Movie).order_by(Movie.release_date)
    return db.execute(statement).scalars().all()

def get_movies_sorted_by_rating(db: Session) -> List[MovieOut]:
    statement = select(Movie).order_by(Movie.rating.desc())  # Assuming higher rating is better
    return db.execute(statement).scalars().all()

def get_movies_sorted_by_likes(db: Session) -> List[MovieOut]:
    statement = select(Movie).order_by(Movie.likes.desc())  # Assuming more likes is better
    return db.execute(statement).scalars().all()

# The idea is to return the five top relaetd movies given a movie name, by genre, cast and director
def get_movies_sorted_by_related(db: Session, target_movie_title: str, limit: int = 60) -> List[MovieOut]:
    # Step 1: Get the target movie by title
    target_movie = db.execute(select(Movie).where(Movie.title == target_movie_title)).scalars().first()
    
    if not target_movie:
        return []  # Return empty list if movie is not found
    
    # Step 2: Extract target movie's related data
    target_genres = [genre.type for genre in target_movie.genres]
    target_cast_members = [cast.name for cast in target_movie.cast_members]
    target_director = target_movie.director

    # Step 3: Build the query for matching movies, excluding the target movie itself
    statement = select(Movie).where(Movie.id != target_movie.id)
    
    # Step 4: Calculate a score for each movie based on how many attributes match
    movies_with_scores = []
    for movie in db.execute(statement).scalars().all():
        score = 0

        # Check genre match
        movie_genres = [genre.type for genre in movie.genres]
        score += len(set(target_genres).intersection(set(movie_genres)))  # Count matching genres
        
        # Check cast member match
        movie_cast_members = [cast.name for cast in movie.cast_members]
        score += len(set(target_cast_members).intersection(set(movie_cast_members)))  # Count matching cast members
        
        # Check director match
        if movie.director == target_director:
            score += 1  # Count if director matches

        # Add movie and its score to the list
        movies_with_scores.append((movie, score))

    # Step 5: Sort movies by score in descending order (highest score first)
    sorted_movies = sorted(movies_with_scores, key=lambda x: x[1], reverse=True)
    
    # Step 6: Limit the results and return
    top_movies = [movie for movie, score in sorted_movies[:limit]]
    
    return [MovieOut.model_validate(movie) for movie in top_movies]
    
'''
# Function to update a movie by ID
def update_movie(db: Session, movie_id: int, movie_data: MovieUpdate) -> MovieOut:
    statement = select(Movie).where(Movie.id == movie_id)
    movie = db.execute(statement).scalars().first()
    if movie:
        for key, value in movie_data.dict(exclude_unset=True).items():
            setattr(movie, key, value)
        db.add(movie)
        db.commit()
        db.refresh(movie)  # Refresh to get updated data
        return MovieOut.model_validate(movie)  # Use model_validate
    return None  # If movie not found
'''

# Function to update a movie by title
def update_movie(db: Session, movie_title: str, movie_data: MovieUpdate) -> MovieOut:
    statement = select(Movie).where(Movie.title == movie_title)
    movie = db.execute(statement).scalars().first()
    if movie:
        for key, value in movie_data.model_dump(exclude_unset=True).items():
        
            if key not in ["genres", "cast_members"]:
                setattr(movie, key, value)
        # Handle genres
        movie.genres.clear()
        for genre_name in movie_data.genres or []:  # Use the genres from the input
            genre = db.execute(select(Genre).where(Genre.type == genre_name)).scalars().first()
            if genre is None:
                genre = Genre(type=genre_name)  # Ensure genre type is not None
                db.add(genre)  # Add new genre to the session
            movie.genres.append(genre)  # Associate genre with the movie

        # Handle cast members
        movie.cast_members.clear()
        for cast_name in movie_data.cast_members or []:
            cast_member = db.execute(select(CastMember).where(CastMember.name == cast_name)).scalars().first()
            if cast_member is None:
                cast_member = CastMember(name=cast_name)  # Ensure cast name is not None
                db.add(cast_member)  # Add new cast member to the session
            movie.cast_members.append(cast_member)  # Associate cast member with the movie
        db.add(movie)
        db.commit()
        db.refresh(movie)  # Refresh to get updated data
        return MovieOut.model_validate(movie)  # Use model_validate

    return None  # If movie not found

'''def update_movie_rating_by_title(db: Session, movie_title: str, new_rating: float):
    # Query the movie by title
    movie = db.query(Movie).filter(Movie.title == movie_title).first()
    
    # If the movie doesn't exist, return None
    if not movie:
        return None
    
    # Calculate the new average rating
    total_rating_sum = movie.rating * movie.rating_count  # Total of all previous ratings
    total_rating_sum += new_rating  # Add the new rating to the total
    movie.rating_count += 1         # Increase the count by 1
    movie.rating = total_rating_sum / movie.rating_count  # Calculate the new average
    
    # Commit the transaction and refresh the instance
    db.commit()
    db.refresh(movie)
    
    return movie'''

# Function to delete a movie by ID
def delete_movie(db: Session, movie_id: int) -> bool:
    statement = select(Movie).where(Movie.id == movie_id)
    result = db.execute(statement).first()
    movie = result[0] if result else None
    if movie:
        delete_thread(db, movie_id)
        db.delete(movie)
        db.commit()
        return True  # Deletion successful
    return False  # Movie not found

# Function to delete a movie by title
def delete_movie_by_title(db: Session, movie_title: str) -> bool:
    statement = select(Movie).where(Movie.title == movie_title)
    result = db.execute(statement).first()
    movie = result[0] if result else None
    if movie:
        delete_thread(db, movie.id)
        db.delete(movie)
        db.commit()
        return True  # Deletion successful
    return False  # Movie not found

# Function get movie by data release
def get_movie_by_year(db: Session, movie_year: int)-> List[MovieOut]:
    statement = select(Movie).where(extract('year', Movie.release_date) == movie_year)
    return db.execute(statement).scalars().all()

# Check if genre exist
def is_valid_genre(db: Session, movie_genre: str) -> bool:
    genre = db.execute(select(Genre).where(Genre.type == movie_genre)).scalars().first()
    return genre is not None

# Function get movies with one genre
def get_movie_by_genre(db: Session, movie_genre: str)-> List[MovieOut]:
    statement = (
        select(Movie)
        .join(Movie.genres)  # Join the genres relationship
        .where(Genre.type == movie_genre)  # Filter by the genre type
    )
    return db.execute(statement).scalars().all()

# Function get movies with multiple genre
def get_movie_by_genre_list(db: Session, genre_list: List[str])-> List[MovieOut]:
    statement = (
        select(Movie)
        .join(Movie.genres)
        .where(Genre.type.in_(genre_list))  # Filter by all specified genres
        .group_by(Movie.id)
        .having(func.count(Genre.id) == len(genre_list))  # Ensure all genres match
    )
    return db.execute(statement).scalars().all()

# Function that return the list with the movies included the pattern of searching
def get_movies_by_input(db: Session, input: str)-> List[MovieOut]:
    # Use ILIKE for case-insensitive search for partial matches
    statement = select(Movie).where(Movie.title.ilike(f"%{input}%"))
    return db.execute(statement).scalars().all()

# Intern function for update in database the movie rating
def update_movie_rating_by_id(db: Session, movie_id: int, new_rating: float):
    # Query the movie by title
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    
    # If the movie doesn't exist, return None
    if not movie:
        return None
    
    # Calculate the new average rating
    total_rating_sum = movie.rating * movie.rating_count  # Total of all previous ratings
    total_rating_sum += new_rating  # Add the new rating to the total
    movie.rating_count += 1         # Increase the count by 1
    movie.rating = total_rating_sum / movie.rating_count  # Calculate the new average
    
    # Commit the transaction and refresh the instance
    db.commit()
    db.refresh(movie)
    
    return movie

# Function to rate a specific movie by a user
def rate_movie(db: Session, user_id: int, movie_id: int, rating: float):
    if rating < 0 or rating > 5:
        raise HTTPException(
            status_code=400,  # Bad Request
            detail="Rating must be between 0 and 5."
        )
    
    # Check if a relationship already exists
    movie_user = db.query(MovieUser).filter(MovieUser.movie_id == movie_id, MovieUser.user_id == user_id).first()
    
    if not movie_user:
        # Create a new relationship with the rating
        movie_user = MovieUser(movie_id=movie_id, user_id=user_id, rating=rating)
        update_movie_rating_by_id(db, movie_id, rating)
        db.add(movie_user)
    else:
        # Update the existing rating
        remove_movie_rating_by_id(db, movie_id, user_id)
        update_movie_rating_by_id(db, movie_id, rating)
        movie_user.rating = rating
    
    db.commit()
    db.refresh(movie_user)
    return movie_user

# Intern function to add a like by the user
def add_movie_like(db: Session, movie_id: int):
    # Query the movie by title
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    
    # If the movie doesn't exist, return None
    if not movie:
        return None
    
    # Increment the likes count by 1
    movie.likes += 1
    
    # Commit the transaction and refresh the instance
    db.commit()
    db.refresh(movie)
    
    return movie
 
# Function to give a like to a specific movie by a user
def like_movie(db: Session, user_id: int, movie_id: int):
    # Check if a relationship already exists
    movie_user = db.query(MovieUser).filter(MovieUser.movie_id == movie_id, MovieUser.user_id == user_id).first()
    
    if not movie_user:
        # Create a new relationship with the like
        movie_user = MovieUser(movie_id=movie_id, user_id=user_id, liked=True)
        add_movie_like(db,movie_id)
        db.add(movie_user)
    else:
        # Toggle the like status
        movie_user.liked = True
        add_movie_like(db,movie_id)
    
    db.commit()
    db.refresh(movie_user)
    return movie_user

# Intern function to add a wish by the user
def add_movie_wish(db: Session, movie_id: int):
    # Query the movie by title
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    
    # If the movie doesn't exist, return None
    if not movie:
        return None
    
    # Commit the transaction and refresh the instance
    db.commit()
    db.refresh(movie)
    
    return movie
 
# Function to add to wish to a specific movie by a user
def wish_movie(db: Session, user_id: int, movie_id: int):
    # Check if a relationship already exists
    movie_user = db.query(MovieUser).filter(MovieUser.movie_id == movie_id, MovieUser.user_id == user_id).first()
    
    if not movie_user:
        # Create a new relationship with the wish
        movie_user = MovieUser(movie_id=movie_id, user_id=user_id, wished=True)
        add_movie_wish(db,movie_id)
        db.add(movie_user)
    else:
        # Toggle the wish status
        movie_user.wished = True
        add_movie_wish(db, movie_id)
    
    db.commit()
    db.refresh(movie_user)
    return movie_user

# Functions for get the list of movies that the user have rated by stars and by given like
def get_user_rated_movies(db: Session, user_id: int):
     # Query the Movie and MovieUser tables together to fetch ratings and titles
    movies_rated = (
        db.query(Movie.title, MovieUser.rating)
        .join(Movie, Movie.id == MovieUser.movie_id)
        .filter(MovieUser.user_id == user_id, MovieUser.rating != None)
        .all()
    )
    # Transform the results into the desired format
    return [{"title": title, "rating": rating} for title, rating in movies_rated]

def get_user_liked_movies(db: Session, user_id: int):
    # Query the Movie and MovieUser tables together to fetch liked movies
    movies_liked = (
        db.query(Movie.title)
        .select_from(MovieUser)  # Explicitly start from MovieUser
        .join(Movie, Movie.id == MovieUser.movie_id)
        .filter(MovieUser.user_id == user_id, MovieUser.liked == True)
        .all()
    )
    # Transform the results into a list of titles
    return [title for title, in movies_liked]

def get_user_wished_movies(db: Session, user_id: int):
    # Query the Movie and MovieUser tables together to fetch wished movies
    movies_wished = (
        db.query(Movie.title)
        .select_from(MovieUser)  # Explicitly start from MovieUser
        .join(Movie, Movie.id == MovieUser.movie_id)
        .filter(MovieUser.user_id == user_id, MovieUser.wished == True)
        .all()
    )
    # Transform the results into a list of titles
    return [title for title, in movies_wished]

### THE SAME BUT FOR REMOVING RATING
# Intern function for remove in database the movie rating
def remove_movie_rating_by_id(db: Session, movie_id: int, user_id: int):
    # Query the movie by ID
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    
    # If the movie doesn't exist, return None
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    # Get the user's rating for this movie
    movie_user = db.query(MovieUser).filter(MovieUser.movie_id == movie_id, MovieUser.user_id == user_id).first()
    
    # If the user hasn't rated the movie, return an error
    if not movie_user:
        raise HTTPException(status_code=400, detail="No rating to remove")

    if movie_user.rating is None:
        pass
    else:
        # Get the current rating
        old_rating = movie_user.rating
        # Subtract the user's rating from the total rating sum
        total_rating_sum = movie.rating * movie.rating_count
        total_rating_sum -= old_rating  # Remove the user's rating
        movie.rating_count -= 1  # Decrease the rating count by 1

        # Recalculate the average rating
        if movie.rating_count > 0:
            movie.rating = total_rating_sum / movie.rating_count  # Calculate the new average rating
        else:
            movie.rating = 0  # If there are no ratings left, set the rating to 0

    # Update the rating in the movie_user table to None (i.e., no rating)
    movie_user.rating = None

    # Commit the changes to the database
    db.commit()
    db.refresh(movie)
    
    return movie

# Function to remove the rate a specific movie by a user
def remove_rate_movie(db: Session, user_id: int, movie_id: int):
    # Check if a relationship already exists
    movie_user = db.query(MovieUser).filter(MovieUser.movie_id == movie_id, MovieUser.user_id == user_id).first()
    
    if movie_user:
        # Remove the existing rating      
        remove_movie_rating_by_id(db, movie_id, user_id)
        movie_user.rating = None
    else:
        raise HTTPException(status_code=400, detail="No rating to remove")

    db.commit()
    db.refresh(movie_user)
    return movie_user

# Intern function to remode a like by the user
def remove_movie_like(db: Session, movie_id: int, user_id: int):
    # Query the movie by ID
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    
    # If the movie doesn't exist, return None
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    # Query to check if the user has already liked the movie (assuming a MovieUser or similar table exists)
    movie_user = db.query(MovieUser).filter(MovieUser.movie_id == movie_id, MovieUser.user_id == user_id).first()
    
    # If the user hasn't liked the movie, return an error
    if not movie_user or not movie_user.liked:
        raise HTTPException(status_code=400, detail="User hasn't liked the movie")
    
    # Decrement the likes count
    movie.likes -= 1
    
    # Mark that the user no longer likes the movie
    movie_user.liked = False
    
    # Commit the transaction and refresh the instance
    db.commit()
    db.refresh(movie)
    
    return movie
 
# Function to remove a like to a specific movie by a user
def remove_like_movie(db: Session, user_id: int, movie_id: int):
    # Check if a relationship already exists
    movie_user = db.query(MovieUser).filter(MovieUser.movie_id == movie_id, MovieUser.user_id == user_id).first()
    
    if movie_user:
        # Toggle the like status
        remove_movie_like(db,movie_id,user_id)
        movie_user.liked = False
    else:
        raise HTTPException(status_code=400, detail="No like to remove")
    
    db.commit()
    db.refresh(movie_user)
    return movie_user

# Intern function to remode a wish by the user
def remove_movie_wish(db: Session, movie_id: int, user_id: int):
    # Query the movie by ID
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    
    # If the movie doesn't exist, return None
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    # Query to check if the user has already liked the movie (assuming a MovieUser or similar table exists)
    movie_user = db.query(MovieUser).filter(MovieUser.movie_id == movie_id, MovieUser.user_id == user_id).first()
    
    # If the user hasn't wish the movie, return an error
    if not movie_user or not movie_user.wished:
        raise HTTPException(status_code=400, detail="User hasn't wish the movie")
    
    # Mark that the user no longer likes the movie
    movie_user.wished = False
    
    # Commit the transaction and refresh the instance
    db.commit()
    db.refresh(movie)
    
    return movie
 
# Function to remove a wish to a specific movie by a user
def remove_wish_movie(db: Session, user_id: int, movie_id: int):
    # Check if a relationship already exists
    movie_user = db.query(MovieUser).filter(MovieUser.movie_id == movie_id, MovieUser.user_id == user_id).first()
    
    if movie_user:
        # Toggle the like status
        remove_movie_wish(db,movie_id,user_id)
        movie_user.wished = False
    else:
        raise HTTPException(status_code=400, detail="No wish to remove")
    
    db.commit()
    db.refresh(movie_user)
    return movie_user
