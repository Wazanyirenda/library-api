from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date
from app.database import get_db
from app.models import Book, Member, BorrowingRecord
from pydantic import BaseModel
from typing import List

router = APIRouter(prefix="/stats", tags=["Statistics"])


class BookStats(BaseModel):
    book_id: int
    title: str
    author: str
    borrow_count: int


class LibraryStats(BaseModel):
    total_books: int
    total_copies: int
    available_copies: int
    total_members: int
    active_members: int
    total_borrowings: int
    active_borrowings: int
    overdue_borrowings: int
    total_fines: float


@router.get("/overview", response_model=LibraryStats, summary="Get library statistics")
def get_library_stats(db: Session = Depends(get_db)):
    """
    Get comprehensive library statistics and metrics.
    
    Returns:
    - Total number of books and copies
    - Member statistics
    - Borrowing statistics
    - Fine information
    """
    # Book statistics
    book_stats = db.query(
        func.count(Book.id).label('total_books'),
        func.sum(Book.total_copies).label('total_copies'),
        func.sum(Book.available_copies).label('available_copies')
    ).first()
    
    # Member statistics
    total_members = db.query(func.count(Member.id)).scalar()
    active_members = db.query(func.count(Member.id)).filter(Member.status == 'active').scalar()
    
    # Borrowing statistics
    total_borrowings = db.query(func.count(BorrowingRecord.id)).scalar()
    active_borrowings = db.query(func.count(BorrowingRecord.id)).filter(
        BorrowingRecord.status.in_(['borrowed', 'overdue'])
    ).scalar()
    
    # Update and count overdue
    db.query(BorrowingRecord).filter(
        BorrowingRecord.status == 'borrowed',
        BorrowingRecord.due_date < date.today()
    ).update({'status': 'overdue'}, synchronize_session=False)
    db.commit()
    
    overdue_borrowings = db.query(func.count(BorrowingRecord.id)).filter(
        BorrowingRecord.status == 'overdue'
    ).scalar()
    
    # Total fines
    total_fines = db.query(func.sum(BorrowingRecord.fine_amount)).scalar() or 0.0
    
    return LibraryStats(
        total_books=book_stats.total_books or 0,
        total_copies=book_stats.total_copies or 0,
        available_copies=book_stats.available_copies or 0,
        total_members=total_members or 0,
        active_members=active_members or 0,
        total_borrowings=total_borrowings or 0,
        active_borrowings=active_borrowings or 0,
        overdue_borrowings=overdue_borrowings or 0,
        total_fines=float(total_fines)
    )


@router.get("/popular-books", response_model=List[BookStats], summary="Get most borrowed books")
def get_popular_books(
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """
    Get the most frequently borrowed books.
    
    - **limit**: Number of top books to return (default 10)
    """
    popular_books = db.query(
        Book.id,
        Book.title,
        Book.author,
        func.count(BorrowingRecord.id).label('borrow_count')
    ).join(
        BorrowingRecord, Book.id == BorrowingRecord.book_id
    ).group_by(
        Book.id, Book.title, Book.author
    ).order_by(
        func.count(BorrowingRecord.id).desc()
    ).limit(limit).all()
    
    return [
        BookStats(
            book_id=book.id,
            title=book.title,
            author=book.author,
            borrow_count=book.borrow_count
        )
        for book in popular_books
    ]

