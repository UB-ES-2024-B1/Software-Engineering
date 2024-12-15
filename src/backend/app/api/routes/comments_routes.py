from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from app.api.db_utils import get_db
from app.crud.comments_crud import (
    create_thread,
    get_threads_by_movie,
    create_comment,
    get_comments_by_thread,
    update_comment_status_with_user,
    update_comment_text,
    delete_comment,
    delete_thread,
    get_comments_reported,
    get_comments_banned,
    get_comments_reported_by_user,
    get_comments_by_user,
    get_reported_comments_ordered,
    delete_reported_comment,
    ban_comment_by_id,
    clean_comment_by_id
)
from app.crud import movie_crud
from app.models import Thread, Comment, CommentUpdateRequest, CommentReportRequest, User
from app.api.dependencies import is_admin  # Import the is_admin dependency

  # Import the get_db function for database session management

router = APIRouter()

@router.post("/threads/", response_model=Thread)
def create_movie_thread(movie_id: int, session: Session = Depends(get_db)):
    """
    Create a new thread for a specific movie.
    """
    movie = movie_crud.get_movie(db=session, movie_id=movie_id)
    # If the movie does not exist, raise a 404 error
    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    thread = create_thread(session, movie_id)
    if not thread:
        raise HTTPException(status_code=400, detail="Failed to create thread.")
    return thread

@router.get("/threads/{movie_id}/", response_model=List[Thread])
def get_threads(movie_id: int, session: Session = Depends(get_db)):
    """
    Retrieve all threads for a specific movie.
    """
    threads = get_threads_by_movie(session, movie_id)
    return threads

@router.post("/", response_model=Comment)
def add_comment(thread_id: int, user_id: int, text: str,session: Session = Depends(get_db)):
    """
    Add a new comment to a thread.
    """
    comment = create_comment(session, thread_id, user_id, text)
    if not comment:
        raise HTTPException(status_code=400, detail="Failed to create comment.")
    return comment

@router.get("/threads/{thread_id}/comments/", response_model=List[Comment])
def get_thread_comments(thread_id: int, session: Session = Depends(get_db)):
    """
    Retrieve all comments for a specific thread.
    """
    comments = get_comments_by_thread(session, thread_id)
    return comments

@router.put("/{comment_id}/text", response_model=Comment)
def update_comment_text_endpoint(
    comment_id: int,
    update_data: CommentUpdateRequest,
    db: Session = Depends(get_db)
):
    """
    Endpoint to update a comment's text.
    """
    if update_data.text is None:
        raise HTTPException(status_code=400, detail="Text field is required.")
    try:
        updated_comment = update_comment_text(
            db=db,
            comment_id=comment_id,
            text=update_data.text
        )
        return updated_comment
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/{comment_id}/status", response_model=Comment)
def update_comment_status_endpoint(
    comment_id: int,
    update_data: CommentReportRequest,
    user_id: int,  # Ahora se pasa el user_id
    db: Session = Depends(get_db)
):
    """
    Endpoint to update a comment's report status and track the user who made the change.
    """
    try:
        # Llamar a la función que actualiza el estado y registra al usuario
        updated_comment = update_comment_status_with_user(
            db=db,
            comment_id=comment_id,
            reported=update_data.reported,
            user_id=user_id  # Pasar el user_id al CRUD
        )
        return updated_comment
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{comment_id}/", status_code=204)
def remove_comment(comment_id: int, session: Session = Depends(get_db)):
    """
    Delete a comment by its ID.
    """
    success = delete_comment(session, comment_id)
    if not success:
        raise HTTPException(status_code=404, detail="Comment not found.")

@router.delete("/threads/{thread_id}/", status_code=204)
def remove_thread(thread_id: int, session: Session = Depends(get_db)):
    """
    Delete a thread and all associated comments.
    """
    success = delete_thread(session, thread_id)
    if not success:
        raise HTTPException(status_code=404, detail="Thread not found.")

@router.get("/reported/", response_model=List[Comment])
def get_reported_comments(session: Session = Depends(get_db)):
    """
    Retrieve all comments that have been reported.
    """
    comments = get_comments_reported(session)
    return comments

@router.get("/reported_by_user/{user_id}/", response_model=List[Comment])
def get_reported_comments_by_user(user_id: int, session: Session = Depends(get_db)):
    """
    Retrieve all comments that have been reported by a specific user.
    """
    comments = get_comments_reported_by_user(session, user_id)
    return comments

@router.get("/banned/", response_model=List[Comment])
def get_banned_comments(session: Session = Depends(get_db)):
    """
    Retrieve all comments that have been banned.
    """
    comments = get_comments_banned(session)
    return comments

@router.get("/by_user/", response_model=List[Comment])
def get_user_comments(user_id:int, session: Session = Depends(get_db)):
    comments = get_comments_by_user(session, user_id)
    return comments

@router.get("/reported/order_by_date/", response_model=List[Comment])
def get_reported_comments_ordered_by_date(session: Session = Depends(get_db)):#, current_user: User = Depends(get_current_user)):
    """
    Retrieve all reported comments, ordered by the date they were reported.
    """
    comments = get_reported_comments_ordered(session, order_by="date")
    return comments


@router.get("/reported/order_by_user/", response_model=List[Comment])
def get_reported_comments_ordered_by_user(session: Session = Depends(get_db)):#, current_user: User = Depends(get_current_user)):
    """
    Retrieve all reported comments, grouped and ordered by the user who reported them.
    """
    comments = get_reported_comments_ordered(session, order_by="user")
    return comments


@router.get("/reported/order_by_status/", response_model=List[Comment])
def get_reported_comments_ordered_by_status(session: Session = Depends(get_db)):#, current_user: User = Depends(get_current_user)):
    """
    Retrieve all reported comments, grouped and ordered by their report status.
    """
    comments = get_reported_comments_ordered(session, order_by="status")
    return comments

@router.put("/reported_to_banned/{comment_id}/")
def ban_comment(
    comment_id: int,
    session: Session = Depends(get_db),
    user: User = Depends(is_admin)  # Ensure that only admins can access this route
):
    """
    Convert a reported comment to Banned by its ID (admin only).
    """
    comment = ban_comment_by_id(session, comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    
    return {"message": "Comment banned successfully"}

@router.put("/reported_to_clean/{comment_id}/")
def clean_comment(
    comment_id: int,
    session: Session = Depends(get_db)
    #user: User = Depends(is_admin)  # Ensure that only admins can access this route
):
    """
    Convert a reported comment to Banned by its ID (admin only).
    """
    comment = clean_comment_by_id(session, comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    
    return {"message": "Comment banned successfully"}

@router.delete("/reported/{comment_id}/", status_code=204)
def delete_reported_comment_endpoint(
    comment_id: int,
    session: Session = Depends(get_db)
    #user: User = Depends(is_admin)  # Ensure that only admins can access this route
):
    """
    Delete a reported comment by its ID (admin only).
    """
    try:
        delete_reported_comment(session, comment_id)
        return {"message": f"Comment with ID {comment_id} successfully deleted."}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
