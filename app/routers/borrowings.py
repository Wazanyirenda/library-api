from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
from app.database import get_db
from app.models import BorrowingRecord as BorrowingModel, Book, Member
from app.schemas import Borrowing, BorrowingCreate, BorrowingReturn, BorrowingRenew, BorrowingWithDetails

router = APIRouter(prefix="/borrowings", tags=["Borrowings"])


def calculate_fine(due_date: date, return_date: date = None) -> float:
    if return_date is None:
        return_date = date.today()
    return max(0, (return_date - due_date).days * 0.50)


def update_overdue(db: Session):
    db.query(BorrowingModel).filter(
        BorrowingModel.status == "borrowed",
        BorrowingModel.due_date < date.today()
    ).update({'status': 'overdue'}, synchronize_session=False)
    db.commit()


@router.get("/", response_model=List[BorrowingWithDetails])
def get_borrowings(
    status_filter: Optional[str] = Query(None, alias="status"),
    member_id: Optional[int] = None,
    book_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    update_overdue(db)
    query = db.query(BorrowingModel)
    if status_filter:
        query = query.filter(BorrowingModel.status == status_filter)
    if member_id:
        query = query.filter(BorrowingModel.member_id == member_id)
    if book_id:
        query = query.filter(BorrowingModel.book_id == book_id)
    return query.all()


@router.get("/overdue", response_model=List[BorrowingWithDetails])
def get_overdue(db: Session = Depends(get_db)):
    update_overdue(db)
    return db.query(BorrowingModel).filter(BorrowingModel.status == "overdue").all()


@router.get("/{borrowing_id}", response_model=BorrowingWithDetails)
def get_borrowing(borrowing_id: int, db: Session = Depends(get_db)):
    update_overdue(db)
    borrowing = db.query(BorrowingModel).filter(BorrowingModel.id == borrowing_id).first()
    if not borrowing:
        raise HTTPException(status_code=404, detail=f"Borrowing {borrowing_id} not found")
    return borrowing


@router.post("/", response_model=Borrowing, status_code=status.HTTP_201_CREATED)
def borrow_book(borrowing: BorrowingCreate, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == borrowing.book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail=f"Book {borrowing.book_id} not found")
    if book.available_copies <= 0:
        raise HTTPException(status_code=400, detail=f"Book '{book.title}' not available")
    
    member = db.query(Member).filter(Member.id == borrowing.member_id).first()
    if not member:
        raise HTTPException(status_code=404, detail=f"Member {borrowing.member_id} not found")
    if member.status != "active":
        raise HTTPException(status_code=400, detail=f"Member not active")
    
    if db.query(BorrowingModel).filter(
        BorrowingModel.book_id == borrowing.book_id,
        BorrowingModel.member_id == borrowing.member_id,
        BorrowingModel.status.in_(["borrowed", "overdue"])
    ).first():
        raise HTTPException(status_code=400, detail="Member already has this book")
    
    db_borrowing = BorrowingModel(**borrowing.model_dump(), borrow_date=date.today(), status="borrowed")
    book.available_copies -= 1
    
    db.add(db_borrowing)
    db.commit()
    db.refresh(db_borrowing)
    return db_borrowing


@router.put("/{borrowing_id}/return", response_model=Borrowing)
def return_book(borrowing_id: int, return_data: BorrowingReturn = BorrowingReturn(), db: Session = Depends(get_db)):
    borrowing = db.query(BorrowingModel).filter(BorrowingModel.id == borrowing_id).first()
    if not borrowing:
        raise HTTPException(status_code=404, detail=f"Borrowing {borrowing_id} not found")
    if borrowing.status == "returned":
        raise HTTPException(status_code=400, detail="Book already returned")
    
    borrowing.return_date = date.today()
    borrowing.status = "returned"
    borrowing.fine_amount = return_data.fine_amount if return_data.fine_amount is not None else calculate_fine(borrowing.due_date)
    
    book = db.query(Book).filter(Book.id == borrowing.book_id).first()
    book.available_copies += 1
    
    db.commit()
    db.refresh(borrowing)
    return borrowing


@router.put("/{borrowing_id}/renew", response_model=Borrowing)
def renew_borrowing(borrowing_id: int, renew_data: BorrowingRenew, db: Session = Depends(get_db)):
    borrowing = db.query(BorrowingModel).filter(BorrowingModel.id == borrowing_id).first()
    if not borrowing:
        raise HTTPException(status_code=404, detail=f"Borrowing {borrowing_id} not found")
    if borrowing.status == "returned":
        raise HTTPException(status_code=400, detail="Cannot renew returned book")
    
    borrowing.due_date = renew_data.new_due_date
    if borrowing.status == "overdue":
        borrowing.status = "borrowed"
    
    db.commit()
    db.refresh(borrowing)
    return borrowing
