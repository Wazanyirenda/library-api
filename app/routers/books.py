from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models import Book as BookModel
from app.schemas import Book, BookCreate, BookUpdate

router = APIRouter(prefix="/books", tags=["Books"])


@router.get("/", response_model=List[Book])
def get_books(
    genre: Optional[str] = None,
    author: Optional[str] = None,
    available: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    query = db.query(BookModel)
    if genre:
        query = query.filter(BookModel.genre.ilike(f"%{genre}%"))
    if author:
        query = query.filter(BookModel.author.ilike(f"%{author}%"))
    if available is not None:
        query = query.filter(BookModel.available_copies > 0 if available else BookModel.available_copies == 0)
    return query.all()


@router.get("/{book_id}", response_model=Book)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(BookModel).filter(BookModel.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail=f"Book {book_id} not found")
    return book


@router.post("/", response_model=Book, status_code=status.HTTP_201_CREATED)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    if db.query(BookModel).filter(BookModel.isbn == book.isbn).first():
        raise HTTPException(status_code=400, detail=f"ISBN {book.isbn} already exists")
    if book.available_copies > book.total_copies:
        raise HTTPException(status_code=400, detail="Available copies cannot exceed total")
    
    db_book = BookModel(**book.model_dump())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


@router.put("/{book_id}", response_model=Book)
def update_book(book_id: int, book_update: BookUpdate, db: Session = Depends(get_db)):
    db_book = db.query(BookModel).filter(BookModel.id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail=f"Book {book_id} not found")
    
    if book_update.isbn and book_update.isbn != db_book.isbn:
        if db.query(BookModel).filter(BookModel.isbn == book_update.isbn).first():
            raise HTTPException(status_code=400, detail=f"ISBN {book_update.isbn} already exists")
    
    update_data = book_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_book, field, value)
    
    db.commit()
    db.refresh(db_book)
    return db_book


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    from app.models import BorrowingRecord
    
    db_book = db.query(BookModel).filter(BookModel.id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail=f"Book {book_id} not found")
    
    if db.query(BorrowingRecord).filter(
        BorrowingRecord.book_id == book_id,
        BorrowingRecord.status.in_(["borrowed", "overdue"])
    ).first():
        raise HTTPException(status_code=400, detail="Cannot delete borrowed book")
    
    db.delete(db_book)
    db.commit()
