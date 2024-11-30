from sqlmodel import Session, select
from app.models.comments_model import Thread, Comment
from typing import List


def create_thread(session: Session, movie_id: int) -> Thread:
    """
    Create a new thread for a movie.
    """
    thread = Thread(movie_id=movie_id)
    session.add(thread)
    session.commit()
    session.refresh(thread)
    return thread


def create_comment(session: Session, thread_id: int, user_id: int,user_name:str, text: str) -> Comment:
    """
    Create a new comment in a thread.
    """
    comment = Comment(thread_id=thread_id, user_id=user_id, text=text, user_name=user_name)
    session.add(comment)
    session.commit()
    session.refresh(comment)
    return comment


def get_threads_by_movie(db: Session, movie_id: int) -> List[Thread]:
    """
    Retrieve all threads for a specific movie.
    """
    statement = select(Thread).where(Thread.movie_id == movie_id)
    results = db.execute(statement).scalars().all()
    return results

def get_comments_by_thread(db: Session, thread_id: int) -> List[Comment]:
    """
    Retrieve all comments for a specific thread.
    """
    statement = select(Comment).where(Comment.thread_id == thread_id)
    results = db.execute(statement).scalars().all()
    return results

def update_comment(db: Session, comment_id: int, text: str) -> Comment:
    """
    Update a comment's text.
    """
    comment = db.get(Comment, comment_id)
    if comment:
        comment.text = text
        db.add(comment)
        db.commit()
        db.refresh(comment)
    return comment

def delete_comment(db: Session, comment_id: int) -> bool:
    """
    Delete a comment by ID.
    """
    comment = db.get(Comment, comment_id)
    if comment:
        db.delete(comment)
        db.commit()
        return True
    return False

def delete_thread(db: Session, thread_id: int) -> bool:
    """
    Delete a thread and all associated comments.
    """
    thread = db.get(Thread, thread_id)
    if thread:
        # Delete all associated comments
        statement = select(Comment).where(Comment.thread_id == thread_id)
        comments = db.execute(statement).scalars().all()
        for comment in comments:
            db.delete(comment)
        
        # Delete the thread
        db.delete(thread)
        db.commit()
        return True
    return False
