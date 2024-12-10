from sqlmodel import Session, select
from app.models.comments_model import Thread, Comment
from typing import List
from app.models.comments_model import ReportStatus, CommentReportedBy
from sqlalchemy import desc, case


def create_thread(session: Session, movie_id: int) -> Thread:
    """
    Create a new thread for a movie.
    """
    thread = Thread(movie_id=movie_id)
    session.add(thread)
    session.commit()
    session.refresh(thread)
    return thread


def create_comment(session: Session, thread_id: int, user_id: int, text: str) -> Comment:
    """
    Create a new comment in a thread.
    """
    comment = Comment(thread_id=thread_id, user_id=user_id, text=text)
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
    statement = select(Comment).where(
        (Comment.thread_id == thread_id) & (Comment.reported != ReportStatus.BANNED)
    )
    results = db.execute(statement).scalars().all()
    return results

def get_comments_reported(db: Session) -> List[Comment]:
    """
    Retrieve all comments that have been reported.
    """
    statement = select(Comment).where(Comment.reported == ReportStatus.REPORTED)
    results = db.execute(statement).scalars().all()
    return results

def get_comments_reported_with_user(db: Session, user_id: int) -> List[Comment]:
    """
    Retrieve all comments that have been reported by a specific user.
    """
    statement = select(Comment).where(
        (Comment.user_id == user_id) & (Comment.reported == ReportStatus.REPORTED)
    )
    results = db.execute(statement).scalars().all()
    return results

def get_comments_reported_by_user(db: Session, user_id: int) -> List[Comment]:
    """
    Retrieve all comments that have been reported by a specific user.
    Ensure that the same comment ID does not show up more than once.
    """
    # Consulta para obtener los comentarios que fueron reportados por el usuario
    statement = select(Comment).join(
        CommentReportedBy
    ).where(
        CommentReportedBy.user_id == user_id
    ).distinct(Comment.id)
    results = db.execute(statement).scalars().all()
    return results

def get_comments_banned(db: Session) -> List[Comment]:
    """
    Retrieve all comments that have been banned.
    """
    statement = select(Comment).where(Comment.reported == ReportStatus.BANNED)
    results = db.execute(statement).scalars().all()
    return results

def update_comment_text(db: Session, comment_id: int, text: str) -> Comment:
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

def update_comment_status_with_user(
    db: Session,
    comment_id: int,
    reported: ReportStatus,
    user_id: int
) -> Comment:
    """
    Update a comment's report status and log the user who made the change.
    """
    # Obtener el comentario
    comment = db.get(Comment, comment_id)
    if not comment:
        raise ValueError("Comment not found")

    # Actualizar el estado del reporte
    comment.reported = reported
    db.add(comment)

    # Registrar quién hizo el cambio
    reported_by_entry = CommentReportedBy(
        comment_id=comment_id,
        user_id=user_id
    )
    db.add(reported_by_entry)

    # Confirmar los cambios en la base de datos
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

from sqlalchemy.orm import joinedload
from sqlalchemy import desc

def get_reported_comments_ordered(
    db: Session, 
    order_by: str = "date"
) -> List[dict]:
    """
    Retrieve reported comments ordered by date, user, or status, including the user's name.
    """
    # Base query: Retrieve reported comments with user relationship loaded
    statement = (
        select(Comment)
        .where(Comment.reported != ReportStatus.CLEAN)
        .options(joinedload(Comment.user))  # Preload the User relationship
    )

    # Apply ordering based on the specified criterion
    if order_by == "date":
        statement = statement.order_by(desc(Comment.created_at))  # Newest first
    elif order_by == "user":
        statement = statement.order_by(Comment.user_id)
    elif order_by == "status":
        statement = statement.order_by(
            case(
                (Comment.reported == ReportStatus.REPORTED, 1),
                (Comment.reported == ReportStatus.BANNED, 2),
            )
        )

    # Execute query and retrieve results
    results = db.execute(statement).scalars().all()

    # Include user name in the response
    return results

def ban_comment_by_id(db: Session, comment_id: int):
    # Busca el comentario
    comment = db.query(Comment).filter_by(id=comment_id).first()
    if not comment:
        return None
    
    # Actualiza el estado del comentario a "BANNED"
    comment.reported = "BANNED"
    db.commit()
    return comment

def delete_reported_comment(session: Session, comment_id: int) -> bool:
    """
    Delete a reported comment by its ID.

    Args:
        session (Session): The database session.
        comment_id (int): The ID of the comment to be deleted.

    Returns:
        bool: True if the comment was successfully deleted, False otherwise.

    Raises:
        ValueError: If the comment does not exist or is not reported.
    """
    # Retrieve the comment by ID
    comment = session.get(Comment, comment_id)
    
    if not comment:
        raise ValueError(f"Comment with ID {comment_id} not found.")

    if comment.reported == ReportStatus.CLEAN:
        raise ValueError(f"Comment with ID {comment_id} is not reported.")

    # Delete related records in CommentReportedBy
    session.query(CommentReportedBy).filter(CommentReportedBy.comment_id == comment_id).delete()

    # Proceed to delete the comment
    session.delete(comment)
    session.commit()
    return True
