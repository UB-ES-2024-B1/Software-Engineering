from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from app.api.dependencies import get_db
from app.crud.comments_crud import (
    create_thread,
    get_threads_by_movie,
    create_comment,
    get_comments_by_thread,
    update_comment,
    delete_comment,
    delete_thread,
)
from app.models.comments_model import Thread, Comment

  # Import the get_db function for database session management

router = APIRouter()

@router.post("/threads/", response_model=Thread)
def create_movie_thread(movie_id: int, session: Session = Depends(get_db)):
    """
    Create a new thread for a specific movie.
    """
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

@router.post("/comments/", response_model=Comment)
def add_comment(thread_id: int, user_id: int, text: str, session: Session = Depends(get_db)):
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

@router.put("/comments/{comment_id}/", response_model=Comment)
def edit_comment(comment_id: int, text: str, session: Session = Depends(get_db)):
    """
    Update an existing comment.
    """
    comment = update_comment(session, comment_id, text)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found.")
    return comment

@router.delete("/comments/{comment_id}/", status_code=204)
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
