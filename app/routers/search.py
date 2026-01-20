from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_, func
from typing import List
from app.database import get_db
from app.models import Book as BookModel
from app.schemas import Book

router = APIRouter(prefix="/search", tags=["Search"])


@router.get("/books", response_model=List[Book], summary="Search books")
def search_books(
    q: str = Query(..., min_length=1, description="Search query (searches title, author, and ISBN)"),
    limit: int = Query(20, ge=1, le=100, description="Maximum number of results"),
    db: Session = Depends(get_db)
):
    """
    Search for books across title, author, and ISBN fields.
    
    - **q**: Search query string (required, searches across multiple fields)
    - **limit**: Maximum number of results to return (default 20, max 100)
    
    Example: `/api/search/books?q=tolkien`
    """
    search_pattern = f"%{q}%"
    
    books = db.query(BookModel).filter(
        or_(
            BookModel.title.ilike(search_pattern),
            BookModel.author.ilike(search_pattern),
            BookModel.isbn.ilike(search_pattern),
            BookModel.genre.ilike(search_pattern)
        )
    ).limit(limit).all()
    
    return books

