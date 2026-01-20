from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models import Book as BookModel
from app.schemas import Book, BookCreate, BookUpdate, BookAvailability

router = APIRouter(prefix="/books", tags=["Books"])


@router.get("/", response_model=List[Book], summary="Get all books")
def get_books(
    genre: Optional[str] = Query(None, description="Filter by genre"),
    author: Optional[str] = Query(None, description="Filter by author"),
    available: Optional[bool] = Query(None, description="Filter by availability"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=100, description="Maximum number of records to return"),
    db: Session = Depends(get_db)
):
    """
    Retrieve all books with optional filters.
    
    - **genre**: Filter books by genre
    - **author**: Filter books by author name
    - **available**: Filter by availability (true = available copies > 0)
    - **skip**: Pagination offset
    - **limit**: Maximum number of results (default 100, max 100)
    """
    query = db.query(BookModel)
    
    if genre:
        query = query.filter(BookModel.genre.ilike(f"%{genre}%"))
    
    if author:
        query = query.filter(BookModel.author.ilike(f"%{author}%"))
    
    if available is not None:
        if available:
            query = query.filter(BookModel.available_copies > 0)
        else:
            query = query.filter(BookModel.available_copies == 0)
    
    books = query.offset(skip).limit(limit).all()
    return books


@router.get("/{book_id}", response_model=Book, summary="Get book by ID")
def get_book(book_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a specific book by its ID.
    
    - **book_id**: The ID of the book to retrieve
    """
    book = db.query(BookModel).filter(BookModel.id == book_id).first()
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id {book_id} not found"
        )
    return book


@router.get("/{book_id}/availability", response_model=BookAvailability, summary="Check book availability")
def check_book_availability(book_id: int, db: Session = Depends(get_db)):
    """
    Check the availability status of a specific book.
    
    - **book_id**: The ID of the book to check
    """
    book = db.query(BookModel).filter(BookModel.id == book_id).first()
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id {book_id} not found"
        )
    
    return BookAvailability(
        book_id=book.id,
        title=book.title,
        available_copies=book.available_copies,
        total_copies=book.total_copies,
        is_available=book.available_copies > 0
    )


@router.post("/", response_model=Book, status_code=status.HTTP_201_CREATED, summary="Create a new book")
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    """
    Create a new book in the library.
    
    - **title**: Title of the book (required)
    - **author**: Author of the book (required)
    - **isbn**: ISBN number (required, must be unique)
    - **published_year**: Year the book was published (optional)
    - **genre**: Genre of the book (optional)
    - **total_copies**: Total number of copies (default: 1)
    - **available_copies**: Number of available copies (default: same as total_copies)
    """
    # Check if ISBN already exists
    existing_book = db.query(BookModel).filter(BookModel.isbn == book.isbn).first()
    if existing_book:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Book with ISBN {book.isbn} already exists"
        )
    
    # Validate available_copies <= total_copies
    if book.available_copies > book.total_copies:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Available copies cannot exceed total copies"
        )
    
    db_book = BookModel(**book.model_dump())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


@router.put("/{book_id}", response_model=Book, summary="Update a book")
def update_book(book_id: int, book_update: BookUpdate, db: Session = Depends(get_db)):
    """
    Update an existing book's information.
    
    - **book_id**: The ID of the book to update
    - All fields are optional; only provided fields will be updated
    """
    db_book = db.query(BookModel).filter(BookModel.id == book_id).first()
    if not db_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id {book_id} not found"
        )
    
    # Check if ISBN is being updated and if it already exists
    if book_update.isbn and book_update.isbn != db_book.isbn:
        existing_book = db.query(BookModel).filter(BookModel.isbn == book_update.isbn).first()
        if existing_book:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Book with ISBN {book_update.isbn} already exists"
            )
    
    # Update only provided fields
    update_data = book_update.model_dump(exclude_unset=True)
    
    # Validate available_copies <= total_copies
    total = update_data.get('total_copies', db_book.total_copies)
    available = update_data.get('available_copies', db_book.available_copies)
    if available > total:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Available copies cannot exceed total copies"
        )
    
    for field, value in update_data.items():
        setattr(db_book, field, value)
    
    db.commit()
    db.refresh(db_book)
    return db_book


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete a book")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    """
    Delete a book from the library.
    
    - **book_id**: The ID of the book to delete
    - Cannot delete a book that is currently borrowed
    """
    db_book = db.query(BookModel).filter(BookModel.id == book_id).first()
    if not db_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id {book_id} not found"
        )
    
    # Check if book has active borrowings
    from app.models import BorrowingRecord
    active_borrowings = db.query(BorrowingRecord).filter(
        BorrowingRecord.book_id == book_id,
        BorrowingRecord.status.in_(["borrowed", "overdue"])
    ).first()
    
    if active_borrowings:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete a book that is currently borrowed"
        )
    
    db.delete(db_book)
    db.commit()
    return None

