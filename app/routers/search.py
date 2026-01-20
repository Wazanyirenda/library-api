from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List
from app.database import get_db
from app.models import Book as BookModel
from app.schemas import Book

router = APIRouter(prefix="/search", tags=["Search"])


@router.get("/books", response_model=List[Book])
def search_books(q: str = Query(..., min_length=1), db: Session = Depends(get_db)):
    pattern = f"%{q}%"
    return db.query(BookModel).filter(or_(
        BookModel.title.ilike(pattern),
        BookModel.author.ilike(pattern),
        BookModel.isbn.ilike(pattern),
        BookModel.genre.ilike(pattern)
    )).limit(20).all()
