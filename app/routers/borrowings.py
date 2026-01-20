from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date, datetime
from app.database import get_db
from app.models import BorrowingRecord as BorrowingModel, Book, Member
from app.schemas import (
    BorrowingRecord, 
    BorrowingRecordCreate, 
    BorrowingRecordReturn, 
    BorrowingRecordRenew,
    BorrowingRecordWithDetails
)

router = APIRouter(prefix="/borrowings", tags=["Borrowing Records"])


def calculate_fine(due_date: date, return_date: date = None) -> float:
    """
    Calculate fine for overdue books.
    Fine rate: $0.50 per day overdue.
    """
    if return_date is None:
        return_date = date.today()
    
    if return_date <= due_date:
        return 0.0
    
    overdue_days = (return_date - due_date).days
    return overdue_days * 0.50


def update_overdue_status(db: Session):
    """
    Update the status of borrowings that are overdue.
    """
    today = date.today()
    overdue_borrowings = db.query(BorrowingModel).filter(
        BorrowingModel.status == "borrowed",
        BorrowingModel.due_date < today
    ).all()
    
    for borrowing in overdue_borrowings:
        borrowing.status = "overdue"
    
    db.commit()


@router.get("/", response_model=List[BorrowingRecordWithDetails], summary="Get all borrowing records")
def get_borrowings(
    status_filter: Optional[str] = Query(None, alias="status", description="Filter by status (borrowed, returned, overdue)"),
    member_id: Optional[int] = Query(None, description="Filter by member ID"),
    book_id: Optional[int] = Query(None, description="Filter by book ID"),
    overdue: Optional[bool] = Query(None, description="Filter by overdue status"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=100, description="Maximum number of records to return"),
    db: Session = Depends(get_db)
):
    """
    Retrieve all borrowing records with optional filters.
    
    - **status**: Filter by borrowing status
    - **member_id**: Filter by specific member
    - **book_id**: Filter by specific book
    - **overdue**: Filter by overdue status
    - **skip**: Pagination offset
    - **limit**: Maximum number of results
    """
    # Update overdue status first
    update_overdue_status(db)
    
    query = db.query(BorrowingModel)
    
    if status_filter:
        if status_filter not in ["borrowed", "returned", "overdue"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Status must be one of: borrowed, returned, overdue"
            )
        query = query.filter(BorrowingModel.status == status_filter)
    
    if member_id:
        query = query.filter(BorrowingModel.member_id == member_id)
    
    if book_id:
        query = query.filter(BorrowingModel.book_id == book_id)
    
    if overdue is not None:
        if overdue:
            query = query.filter(BorrowingModel.status == "overdue")
        else:
            query = query.filter(BorrowingModel.status != "overdue")
    
    borrowings = query.order_by(BorrowingModel.borrow_date.desc()).offset(skip).limit(limit).all()
    return borrowings


@router.get("/overdue", response_model=List[BorrowingRecordWithDetails], summary="Get all overdue borrowings")
def get_overdue_borrowings(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    Retrieve all overdue borrowing records.
    
    - **skip**: Pagination offset
    - **limit**: Maximum number of results
    """
    # Update overdue status first
    update_overdue_status(db)
    
    overdue_borrowings = db.query(BorrowingModel).filter(
        BorrowingModel.status == "overdue"
    ).order_by(BorrowingModel.due_date).offset(skip).limit(limit).all()
    
    return overdue_borrowings


@router.get("/{borrowing_id}", response_model=BorrowingRecordWithDetails, summary="Get borrowing record by ID")
def get_borrowing(borrowing_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a specific borrowing record by its ID.
    
    - **borrowing_id**: The ID of the borrowing record to retrieve
    """
    # Update overdue status first
    update_overdue_status(db)
    
    borrowing = db.query(BorrowingModel).filter(BorrowingModel.id == borrowing_id).first()
    if not borrowing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Borrowing record with id {borrowing_id} not found"
        )
    return borrowing


@router.post("/", response_model=BorrowingRecord, status_code=status.HTTP_201_CREATED, summary="Borrow a book")
def borrow_book(borrowing: BorrowingRecordCreate, db: Session = Depends(get_db)):
    """
    Create a new borrowing record (borrow a book).
    
    - **book_id**: ID of the book to borrow (required)
    - **member_id**: ID of the member borrowing the book (required)
    - **due_date**: Due date for returning the book (required, must be in the future)
    
    Business rules:
    - Book must exist and have available copies
    - Member must exist and be active
    - Member cannot borrow the same book twice simultaneously
    """
    # Check if book exists and is available
    book = db.query(Book).filter(Book.id == borrowing.book_id).first()
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id {borrowing.book_id} not found"
        )
    
    if book.available_copies <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Book '{book.title}' is not available (no copies available)"
        )
    
    # Check if member exists and is active
    member = db.query(Member).filter(Member.id == borrowing.member_id).first()
    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Member with id {borrowing.member_id} not found"
        )
    
    if member.status != "active":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Member '{member.name}' is not active (status: {member.status})"
        )
    
    # Check if member already has this book borrowed
    existing_borrowing = db.query(BorrowingModel).filter(
        BorrowingModel.book_id == borrowing.book_id,
        BorrowingModel.member_id == borrowing.member_id,
        BorrowingModel.status.in_(["borrowed", "overdue"])
    ).first()
    
    if existing_borrowing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Member '{member.name}' has already borrowed this book"
        )
    
    # Create borrowing record
    db_borrowing = BorrowingModel(
        book_id=borrowing.book_id,
        member_id=borrowing.member_id,
        borrow_date=date.today(),
        due_date=borrowing.due_date,
        status="borrowed"
    )
    
    # Decrease available copies
    book.available_copies -= 1
    
    db.add(db_borrowing)
    db.commit()
    db.refresh(db_borrowing)
    
    return db_borrowing


@router.put("/{borrowing_id}/return", response_model=BorrowingRecord, summary="Return a borrowed book")
def return_book(
    borrowing_id: int, 
    return_data: BorrowingRecordReturn = BorrowingRecordReturn(),
    db: Session = Depends(get_db)
):
    """
    Mark a borrowing record as returned.
    
    - **borrowing_id**: The ID of the borrowing record
    - **fine_amount**: Optional fine amount (auto-calculated if not provided)
    
    Automatically calculates fine at $0.50 per day for overdue books if not provided.
    """
    borrowing = db.query(BorrowingModel).filter(BorrowingModel.id == borrowing_id).first()
    if not borrowing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Borrowing record with id {borrowing_id} not found"
        )
    
    if borrowing.status == "returned":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This book has already been returned"
        )
    
    # Calculate fine if not provided
    return_date = date.today()
    if return_data.fine_amount is None:
        fine = calculate_fine(borrowing.due_date, return_date)
    else:
        fine = return_data.fine_amount
    
    # Update borrowing record
    borrowing.return_date = return_date
    borrowing.status = "returned"
    borrowing.fine_amount = fine
    
    # Increase available copies
    book = db.query(Book).filter(Book.id == borrowing.book_id).first()
    book.available_copies += 1
    
    db.commit()
    db.refresh(borrowing)
    
    return borrowing


@router.put("/{borrowing_id}/renew", response_model=BorrowingRecord, summary="Renew a borrowing")
def renew_borrowing(
    borrowing_id: int, 
    renew_data: BorrowingRecordRenew,
    db: Session = Depends(get_db)
):
    """
    Renew a borrowing by extending the due date.
    
    - **borrowing_id**: The ID of the borrowing record
    - **new_due_date**: New due date (required, must be in the future)
    
    Can only renew books that haven't been returned.
    """
    borrowing = db.query(BorrowingModel).filter(BorrowingModel.id == borrowing_id).first()
    if not borrowing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Borrowing record with id {borrowing_id} not found"
        )
    
    if borrowing.status == "returned":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot renew a book that has already been returned"
        )
    
    if renew_data.new_due_date <= borrowing.due_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="New due date must be later than current due date"
        )
    
    # Update due date and reset status to borrowed if it was overdue
    borrowing.due_date = renew_data.new_due_date
    if borrowing.status == "overdue":
        borrowing.status = "borrowed"
    
    db.commit()
    db.refresh(borrowing)
    
    return borrowing

