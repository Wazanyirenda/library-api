from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date
from app.database import get_db
from app.models import Book, Member, BorrowingRecord
from pydantic import BaseModel
from typing import List

router = APIRouter(prefix="/stats", tags=["Statistics"])


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


class BookStats(BaseModel):
    book_id: int
    title: str
    author: str
    borrow_count: int


@router.get("/overview", response_model=LibraryStats)
def get_stats(db: Session = Depends(get_db)):
    book_stats = db.query(
        func.count(Book.id).label('total'),
        func.sum(Book.total_copies).label('total_copies'),
        func.sum(Book.available_copies).label('available')
    ).first()
    
    db.query(BorrowingRecord).filter(
        BorrowingRecord.status == 'borrowed',
        BorrowingRecord.due_date < date.today()
    ).update({'status': 'overdue'}, synchronize_session=False)
    db.commit()
    
    return LibraryStats(
        total_books=book_stats.total or 0,
        total_copies=book_stats.total_copies or 0,
        available_copies=book_stats.available or 0,
        total_members=db.query(func.count(Member.id)).scalar() or 0,
        active_members=db.query(func.count(Member.id)).filter(Member.status == 'active').scalar() or 0,
        total_borrowings=db.query(func.count(BorrowingRecord.id)).scalar() or 0,
        active_borrowings=db.query(func.count(BorrowingRecord.id)).filter(
            BorrowingRecord.status.in_(['borrowed', 'overdue'])).scalar() or 0,
        overdue_borrowings=db.query(func.count(BorrowingRecord.id)).filter(
            BorrowingRecord.status == 'overdue').scalar() or 0,
        total_fines=float(db.query(func.sum(BorrowingRecord.fine_amount)).scalar() or 0)
    )


@router.get("/popular-books", response_model=List[BookStats])
def get_popular_books(limit: int = 10, db: Session = Depends(get_db)):
    return [
        BookStats(book_id=b.id, title=b.title, author=b.author, borrow_count=b.count)
        for b in db.query(
            Book.id, Book.title, Book.author,
            func.count(BorrowingRecord.id).label('count')
        ).join(BorrowingRecord).group_by(Book.id, Book.title, Book.author)
        .order_by(func.count(BorrowingRecord.id).desc()).limit(limit).all()
    ]
